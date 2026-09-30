# FILE: han_gate_service.py
# TITLE: HAN Gate — Cascade Failure Prevention (Fail-Closed)
# Author: M-Tokuni (https://github.com/M-Tokun/NRA-IDE)
# Date: 2026-03-06 JST
# Temperature: 0.3 (axiom-level coherence)
#
# ============================================================
# 【修正履歴】
#   v1.0  2026-02-05: 初版
#   v1.1  2026-03-06: __future__/__name__ 破損修正、LF統一
#                     二重ゆらぎ構造（動的τ）追加
#
# 【位置付け】
#   このゲートの乗算値は、非正典の連鎖予兆スコア chain_score である。
#   chain_score = cooccurrence * dynamic_gain であり、正典の
#   R = δ/τ、吸収厚みτ、二重ゆらぎ式、正規状態分類を実装しない。
#   EMAはスコアの補助倍率を調整する。PASS/SILENCEはローカルな運用判定である。
#
# ============================================================

from __future__ import annotations
from typing import Dict, Any
from collections import OrderedDict
import math
import os
import time
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# ============================================================
# Config (Fail-Closed) — 環境変数で上書き可能
# ============================================================
CHAIN_SCORE_LIMIT = float(os.getenv("CHAIN_SCORE_LIMIT", "1.0"))
GAIN_BASE         = float(os.getenv("GAIN_BASE", "1.5"))
HOLD_MS      = int(os.getenv("HOLD_MS",         "2000"))  # SILENCE保持時間(ms)
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "5000")) # メモリリーク防止

# 非正典スコアのEMA補助倍率
GAIN_EMA_ALPHA    = float(os.getenv("GAIN_EMA_ALPHA", "0.3"))
GAIN_AMPLIFY_LIMIT = float(os.getenv("GAIN_AMPLIFY_LIMIT", "2.0"))

# ============================================================
# 状態: 共起値のEMA
# ============================================================
# スコープ別にEMAを保持する（スコープ間で影響しない）
_ema_cooccurrence: Dict[str, float] = {}

def _update_ema(scope_key: str, cooccurrence: float) -> float:
    """
    共起値のEMAを更新して返す。初回は現在値を使う。
    """
    alpha = GAIN_EMA_ALPHA
    prev = _ema_cooccurrence.get(scope_key, cooccurrence)
    ema = alpha * cooccurrence + (1.0 - alpha) * prev
    _ema_cooccurrence[scope_key] = ema
    return ema

def _dynamic_gain(scope_key: str, cooccurrence: float, base_gain: float) -> float:
    """
    共起値のEMAで非正典スコアの補助倍率を調整する。
    """
    if not math.isfinite(GAIN_EMA_ALPHA) or not 0 < GAIN_EMA_ALPHA <= 1:
        raise ValueError("invalid EMA coefficient")
    if not math.isfinite(GAIN_AMPLIFY_LIMIT) or GAIN_AMPLIFY_LIMIT < 1:
        raise ValueError("invalid gain amplification limit")
    ema = _update_ema(scope_key, cooccurrence)
    multiplier = min(1.0 + ema, GAIN_AMPLIFY_LIMIT)
    return base_gain * multiplier

# ============================================================
# 状態: SILENCE Hold (LRU-like via OrderedDict)
# ============================================================
_silence_until: OrderedDict[str, float] = OrderedDict()

# ============================================================
# 状態: メトリクスカウンタ
# ============================================================
_metrics = {"PASS": 0, "SILENCE": 0, "FAIL_CLOSED": 0}

# ============================================================
# ヘルパー関数
# ============================================================
def _scope_key(scope: Dict[str, Any]) -> str:
    return (
        f"svc={scope.get('service', '')}"
        f"|route={scope.get('route', '')}"
        f"|cl={scope.get('cluster', '')}"
    )

def _now() -> float:
    return time.time()

# ============================================================
# 非正典の連鎖予兆スコア
# ============================================================
def _nonnegative_measurement(telemetry: Dict[str, float], name: str) -> float:
    value = float(telemetry[name])
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"invalid telemetry: {name}")
    return value


def compute_chain_score(
    telemetry: Dict[str, float], base_gain: float, scope_key: str = ""
) -> float:
    """
    テレメトリの共起値とEMA補助倍率から、非正典スコアを計算する。
    正規化定数と閾値はこのゲートの例示設定で、領域根拠のある正規Rではない。
    """
    if not math.isfinite(base_gain) or base_gain <= 0:
        raise ValueError("invalid base gain")
    retry = _nonnegative_measurement(telemetry, "retry_rate")
    queue = _nonnegative_measurement(telemetry, "queue_depth")
    dep_to = _nonnegative_measurement(telemetry, "dep_timeout_rate")

    cooccurrence = (retry / 10.0) * (queue / 500.0) * (dep_to / 5.0)
    if not math.isfinite(cooccurrence):
        raise ValueError("non-finite cooccurrence")

    gain = _dynamic_gain(scope_key, cooccurrence, base_gain)
    chain_score = cooccurrence * gain
    if not math.isfinite(chain_score):
        raise ValueError("non-finite chain score")
    return chain_score

# ============================================================
# should_silence: SILENCE判定 + HOLDロジック
# ============================================================
def should_silence(scope_key: str, chain_score: float) -> bool:
    global _silence_until
    if not math.isfinite(CHAIN_SCORE_LIMIT) or CHAIN_SCORE_LIMIT <= 0:
        raise ValueError("invalid chain score limit")
    if not math.isfinite(chain_score) or chain_score < 0:
        raise ValueError("invalid chain score")
    now = _now()

    # LRU: 最近参照されたキーを末尾へ
    if scope_key in _silence_until:
        _silence_until.move_to_end(scope_key)

    # キャッシュ上限を超えたら古いエントリを削除
    while len(_silence_until) > MAX_CACHE_SIZE:
        _silence_until.popitem(last=False)

    # HOLD中か確認
    until = _silence_until.get(scope_key, 0.0)
    if now < until:
        return True

    # 閾値判定
    if chain_score >= CHAIN_SCORE_LIMIT:
        _silence_until[scope_key] = now + (HOLD_MS / 1000.0)
        return True

    return False


# ============================================================
# エンドポイント
# ============================================================
@app.get("/healthz")
def healthz():
    return "OK", 200


@app.get("/metrics")
def metrics():
    """Prometheus形式のシンプルメトリクス"""
    return (
        f"# HELP han_gate_decisions_total Total decisions made\n"
        f"# TYPE han_gate_decisions_total counter\n"
        f'han_gate_decisions_total{{decision="PASS"}} {_metrics["PASS"]}\n'
        f'han_gate_decisions_total{{decision="SILENCE"}} {_metrics["SILENCE"]}\n'
        f'han_gate_decisions_total{{decision="FAIL_CLOSED"}} {_metrics["FAIL_CLOSED"]}\n'
    ), 200, {"Content-Type": "text/plain"}


@app.post("/v1/decision")
def decision():
    try:
        data     = request.get_json(force=True, silent=True) or {}
        scope    = data.get("scope")    or {}
        telemetry = data.get("telemetry") or {}
        if "tau" in data or "base_gain" in data:
            raise ValueError("request-controlled score gain is forbidden")

        scope_key = _scope_key(scope)
        chain_score = compute_chain_score(telemetry, GAIN_BASE, scope_key)

        if should_silence(scope_key, chain_score):
            _metrics["SILENCE"] += 1
            return jsonify({
                "decision": "SILENCE",
                "chain_score": chain_score,
                "reason": "chain reaction detected or hold active"
            }), 200

        _metrics["PASS"] += 1
        return jsonify({
            "decision": "PASS",
            "chain_score": chain_score,
            "reason": "below local chain-score limit"
        }), 200

    except Exception:
        _metrics["FAIL_CLOSED"] += 1
        _metrics["SILENCE"]     += 1
        return jsonify({
            "decision": "SILENCE",
            "chain_score": None,
            "reason": "invalid or missing input, or internal error (fail-closed)"
        }), 200


@app.post("/v1/nginx_auth")
def nginx_auth():
    try:
        retry  = float(request.headers.get("X-HAN-Retry-Rate",        "nan"))
        queue  = float(request.headers.get("X-HAN-Queue-Depth",       "nan"))
        dep_to = float(request.headers.get("X-HAN-Dep-Timeout-Rate",  "nan"))

        scope_key = "nginx|default"
        chain_score = compute_chain_score(
            {"retry_rate": retry, "queue_depth": queue, "dep_timeout_rate": dep_to},
            GAIN_BASE,
            scope_key,
        )

        if should_silence(scope_key, chain_score):
            _metrics["SILENCE"] += 1
            return make_response("SILENCE", 403)

        _metrics["PASS"] += 1
        return make_response("PASS", 200)

    except Exception:
        _metrics["FAIL_CLOSED"] += 1
        _metrics["SILENCE"]     += 1
        return make_response("SILENCE", 403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
