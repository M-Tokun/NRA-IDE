# FILE: telemetry_sidecar.py
# TITLE: Telemetry Sidecar — Envoy ext_authz + HAN Gate Bridge
# Author: M-Tokuni (https://github.com/M-Tokun/NRA-IDE)
# Date: 2026-03-06 JST
#
# 【修正履歴】
#   v1.0  2026-02-05: 初版
#   v1.1  2026-03-06: __future__/__name__ 破損修正、LF統一
#
# 【役割】
#   Envoy admin エンドポイントからメトリクスをスクレイプし、
#   HAN Gate の /v1/decision に渡す「橋渡し」サイドカー。
#   Envoy ↔ HAN Gate のプロトコル変換を担う。
#
#   サンドイッチアーキテクチャにおける「観測層」に相当する。
#   処理には介入せず、観測→転送のみ行う。

from __future__ import annotations
import os
import time
import requests
from flask import Flask, request, make_response
from typing import Dict, Any, Optional

app = Flask(__name__)

# ============================================================
# Config
# ============================================================
ENVOY_ADMIN     = os.getenv("ENVOY_ADMIN_URL",  "http://127.0.0.1:9901")
HAN_GATE_URL    = os.getenv("HAN_GATE_URL",     "http://han-gate.han.svc.cluster.local:8080/v1/decision")
SCRAPE_INTERVAL = float(os.getenv("SCRAPE_INTERVAL", "1.0"))

# ============================================================
# インメモリキャッシュ (スクレイプ結果)
# ============================================================
_last_metrics: Dict[str, Any] = {
    "retry_rate":      0.0,
    "queue_depth":     0.0,
    "dep_timeout_rate": 0.0,
    "timestamp":       0.0,
    "_retry_count":    0,
    "_timeout_count":  0,
}


def scrape_envoy_stats() -> Optional[Dict[str, float]]:
    """
    Envoy admin /stats エンドポイントから関連メトリクスを取得する。

    【最適化: filterパラメータ使用】
      全メトリクスではなく必要な4種類のみ取得。
      ペイロード削減 + CPU負荷軽減。

    【Fail-Closed設計】
      取得失敗時は None を返す。
      呼び出し元で None → SILENCE として扱う。
      「測れないなら止める」= 律環公理の不能性出力。
    """
    try:
        filter_regex = "upstream_rq_(retry|timeout|pending|active)"
        url = f"{ENVOY_ADMIN}/stats?format=json&usedonly&filter={filter_regex}"

        resp = requests.get(url, timeout=0.5)
        if resp.status_code != 200:
            return None  # Fail-Closed

        stats = resp.json().get("stats", [])

        retry_count   = 0
        timeout_count = 0
        queue_depth   = 0

        for stat in stats:
            name  = stat.get("name",  "")
            value = stat.get("value",  0)

            # overflow/reset はノイズとして除外
            if "overflow" in name or "reset" in name:
                continue

            if "upstream_rq_retry"   in name:
                retry_count   += value
            elif "upstream_rq_timeout" in name:
                timeout_count += value
            elif "upstream_rq_pending" in name or "upstream_rq_active" in name:
                queue_depth   += value

        # レート計算
        now      = time.time()
        last_ts  = _last_metrics.get("timestamp", now - SCRAPE_INTERVAL)
        dt       = max(now - last_ts, 0.1)

        last_retry   = _last_metrics.get("_retry_count",   0)
        last_timeout = _last_metrics.get("_timeout_count", 0)

        # Envoy再起動によるカウンタリセット対応
        if retry_count   < last_retry:   last_retry   = 0
        if timeout_count < last_timeout: last_timeout = 0

        retry_rate   = max(0.0, (retry_count   - last_retry)   / dt)
        timeout_rate = max(0.0, (timeout_count - last_timeout) / dt)

        # キャッシュ更新
        _last_metrics.update({
            "retry_rate":       retry_rate,
            "queue_depth":      queue_depth,
            "dep_timeout_rate": timeout_rate,
            "timestamp":        now,
            "_retry_count":     retry_count,
            "_timeout_count":   timeout_count,
        })

        return {
            "retry_rate":       retry_rate,
            "queue_depth":      queue_depth,
            "dep_timeout_rate": timeout_rate,
        }

    except Exception:
        return None  # Fail-Closed


# ============================================================
# エンドポイント
# ============================================================
@app.route("/healthz")
def healthz():
    return "OK", 200


@app.route("/", methods=["GET", "POST"])
def ext_authz_handler():
    """
    Envoy ext_authz からのリクエストを受け付ける。

    フロー:
      1. Envoy admin スクレイプ
      2. HAN Gate /v1/decision に転送
      3. PASS(200) / SILENCE(403) を Envoy に返す
    """
    headers = request.headers
    service = headers.get("x-envoy-service", "default")
    route   = headers.get("x-envoy-route",   "default")

    # スクレイプ
    telemetry = scrape_envoy_stats()
    if telemetry is None:
        # Fail-Closed: テレメトリ取得失敗
        resp = make_response("Telemetry Failure", 403)
        resp.headers["x-han-decision"] = "SILENCE"
        return resp

    # HAN Gate に転送
    try:
        gate_resp = requests.post(
            HAN_GATE_URL,
            json={
                "scope":     {"service": service, "route": route},
                "telemetry": telemetry,
            },
            timeout=0.1,
        )
        decision = gate_resp.json().get("decision", "SILENCE")
    except Exception:
        decision = "SILENCE"  # Fail-Closed

    if decision == "PASS":
        resp = make_response("", 200)
        resp.headers["x-han-decision"] = "PASS"
        return resp

    resp = make_response("Chain reaction detected", 403)
    resp.headers["x-han-decision"] = "SILENCE"
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
