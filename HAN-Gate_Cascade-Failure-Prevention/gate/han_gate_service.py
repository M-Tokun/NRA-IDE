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
# 【二重ゆらぎ構造について】
#   従来: R = r_raw * τ_static
#         τが静的定数 → δ(入力ゆらぎ)のみが変動 → 山が尖る
#
#   改修: R = r_raw * τ_dynamic
#         τ_dynamic = τ_base * (1 + α * EMA(r_raw))
#         EMA = 指数移動平均(直近履歴の加重平均)
#
#   効果:
#     δ(r_raw)が上昇し始めると、τも連動して大きくなる。
#     これにより、急激な山の形成前にRが閾値に近づく。
#     (連鎖反応の予兆段階でFAIL-CLOSEDが発動しやすくなる)
#
#     δ静定後はEMAが減衰し、τが基底値に戻る。
#     ヒステリシス的な挙動で「戻り」も安定する。
#
#   律環公理との対応:
#     δ: 制約からの偏差（入力ゆらぎ）
#     τ: 吸収厚み（今回から動的化）
#     R = δ/τ の精神は維持。τの動的化は吸収厚みが
#     「蓄積された偏差の履歴に応じて変化する」という
#     自然界の材料疲労・生体耐性と同じ挙動を実装する。
#
# ============================================================

from __future__ import annotations
from typing import Dict, Any
from collections import OrderedDict
import os
import time
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# ============================================================
# Config (Fail-Closed) — 環境変数で上書き可能
# ============================================================
R_OP         = float(os.getenv("R_OP",          "1.0"))   # 低いほど安全
TAU_DEFAULT  = float(os.getenv("TAU_DEFAULT",   "1.5"))   # 高いほど安全
HOLD_MS      = int(os.getenv("HOLD_MS",         "2000"))  # SILENCE保持時間(ms)
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "5000")) # メモリリーク防止

# 二重ゆらぎパラメータ
TAU_EMA_ALPHA = float(os.getenv("TAU_EMA_ALPHA", "0.3"))  # EMA平滑化係数 (0<α<1)
# α小さい → τ変化がゆっくり（安定重視）
# α大きい → τ変化が速い（即応重視）
TAU_AMPLIFY   = float(os.getenv("TAU_AMPLIFY",  "2.0"))   # τ最大増幅倍率の上限

# ============================================================
# 状態: EMA for 動的τ
# ============================================================
# スコープ別にEMAを保持する（スコープ間で影響しない）
_ema_r: Dict[str, float] = {}

def _update_ema(scope_key: str, r_raw: float) -> float:
    """
    r_rawのEMAを更新して返す。

    EMA(t) = α * r_raw(t) + (1-α) * EMA(t-1)

    初回: EMA = r_raw（ウォームアップなし）
    これにより「最初から履歴を持つ」設計になる。
    """
    alpha = TAU_EMA_ALPHA
    prev = _ema_r.get(scope_key, r_raw)
    ema = alpha * r_raw + (1.0 - alpha) * prev
    _ema_r[scope_key] = ema
    return ema

def _dynamic_tau(scope_key: str, r_raw: float, tau_base: float) -> float:
    """
    二重ゆらぎ: EMAに基づきτを動的に調整する。

    τ_dynamic = τ_base * clamp(1 + EMA(r_raw), 1.0, TAU_AMPLIFY)

    r_rawが0のとき: τ_dynamic = τ_base（基底値）
    r_rawが上昇中: τ_dynamicも上昇 → Rが早く閾値に近づく
    r_rawが下降中: EMAが減衰 → τが緩やかに基底値へ戻る

    【山の尖りを丸める理由】
      静的τでは r_raw が急増した瞬間に R が跳ね上がる（尖り）。
      動的τでは EMA の遅延効果で「τが既に膨らんでいる」状態が続く。
      つまり尖る前に R が閾値付近に留まり始め、
      閾値超過が「緩やかな丘」として現れる。
    """
    ema = _update_ema(scope_key, r_raw)
    multiplier = min(1.0 + ema, TAU_AMPLIFY)
    return tau_base * multiplier

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
# compute_R: 連鎖反応スコアの計算（二重ゆらぎ版）
# ============================================================
def compute_R(telemetry: Dict[str, float], tau: float, scope_key: str = "") -> float:
    """
    連鎖反応スコア R を計算する。

    【入力】
      retry_rate       : リトライ発生率 (req/s)
      queue_depth      : キュー滞留数
      dep_timeout_rate : 依存タイムアウト率 (req/s)
      tau              : 吸収厚み基底値

    【計算】
      r_raw = 乗算共起モデル (3指標の積)
             「1つだけ高い」では発動しない。
             「3つ同時に上昇」= 連鎖反応の構造的シグナル。

      τ_dynamic = 動的τ (EMAベース)
      R = r_raw * τ_dynamic

    【正規化係数について】
      retry/10, queue/500, dep_to/5 は
      「通常運用の上限目安」に対する相対値。
      環境に応じて TAU_DEFAULT で調整する。
      直接変更する場合は TAU_AMPLIFY も見直すこと。
    """
    retry  = max(0.0, float(telemetry.get("retry_rate",       0.0)))
    queue  = max(0.0, float(telemetry.get("queue_depth",      0.0)))
    dep_to = max(0.0, float(telemetry.get("dep_timeout_rate", 0.0)))

    # 乗算共起 (3指標が同時に上昇した時だけ高くなる)
    r_raw = (retry / 10.0) * (queue / 500.0) * (dep_to / 5.0)

    # 二重ゆらぎ: τを動的化
    tau_d = _dynamic_tau(scope_key, r_raw, tau)

    return r_raw * tau_d


# ============================================================
# should_silence: SILENCE判定 + HOLDロジック
# ============================================================
def should_silence(scope_key: str, R: float) -> bool:
    global _silence_until
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
    if R >= R_OP:
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
        tau      = float(data.get("tau") or TAU_DEFAULT)

        # Fail-Closed: テレメトリ欠損 → SILENCE
        required = ["retry_rate", "queue_depth", "dep_timeout_rate"]
        if any(k not in telemetry for k in required):
            _metrics["FAIL_CLOSED"] += 1
            _metrics["SILENCE"]     += 1
            return jsonify({
                "decision": "SILENCE",
                "R": 999.0,
                "reason": "missing telemetry (fail-closed)"
            }), 200

        scope_key = _scope_key(scope)
        R = compute_R(telemetry, tau, scope_key)

        if should_silence(scope_key, R):
            _metrics["SILENCE"] += 1
            return jsonify({
                "decision": "SILENCE",
                "R": R,
                "reason": "chain reaction detected or hold active"
            }), 200

        _metrics["PASS"] += 1
        return jsonify({
            "decision": "PASS",
            "R": R,
            "reason": "within safe envelope"
        }), 200

    except Exception:
        _metrics["FAIL_CLOSED"] += 1
        _metrics["SILENCE"]     += 1
        return jsonify({
            "decision": "SILENCE",
            "R": 999.9,
            "reason": "internal error (fail-closed)"
        }), 200


@app.post("/v1/nginx_auth")
def nginx_auth():
    try:
        retry  = float(request.headers.get("X-HAN-Retry-Rate",        "nan"))
        queue  = float(request.headers.get("X-HAN-Queue-Depth",       "nan"))
        dep_to = float(request.headers.get("X-HAN-Dep-Timeout-Rate",  "nan"))

        # NaNチェック (ヘッダー欠損 = Fail-Closed)
        if any(x != x for x in [retry, queue, dep_to]):
            raise ValueError("missing headers")

        scope_key = "nginx|default"
        R = compute_R(
            {"retry_rate": retry, "queue_depth": queue, "dep_timeout_rate": dep_to},
            TAU_DEFAULT,
            scope_key,
        )

        if should_silence(scope_key, R):
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
