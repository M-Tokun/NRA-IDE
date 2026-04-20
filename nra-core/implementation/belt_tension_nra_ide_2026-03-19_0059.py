# FILE: belt_tension_nra_ide_20260319_0059.py
# TITLE: ベルトコンベアー・Vベルト張力管理 NRA-IDE サンプル式
# Author: M-Tokuni / NRA-IDE Project
# Generated: 2026-03-19 00:59 JST
#
# 設計原則：
#   距離は結果であり原因ではない
#   δ = 最適値からの蓄積ズレ [N]
#   τ = 最適値から当該方向の限界までの全余裕 [N]
#   R = δ / τ  →  R >= 1.0 で Fail-Closed（即時停止）
#
# τの物理的意味：
#   上限方向ズレ時：τ = T_max - T_optimal（破断・軸受損傷までの余裕）
#   下限方向ズレ時：τ = T_optimal - T_min（スリップ発生までの余裕）
#   R は [0,1] が許容内、1.0超過で構造限界到達として自然に定義される
# -------------------------------------------------------

from dataclasses import dataclass

# -------------------------------------------------------
# 定数定義（実機に合わせて調整）
# -------------------------------------------------------

# ベルトコンベアー向け（平ベルト・スラット等）
CONVEYOR_T_OPTIMAL  = 500.0   # N : 設計最適張力
CONVEYOR_T_MIN      = 400.0   # N : 許容下限（スリップ発生限界）
CONVEYOR_T_MAX      = 650.0   # N : 許容上限（破断・軸受損傷限界）

# Vベルト向け（断面形状 A・B・C 型を想定）
VBELT_T_OPTIMAL     = 300.0   # N : 設計最適張力
VBELT_T_MIN         = 240.0   # N : 許容下限
VBELT_T_MAX         = 380.0   # N : 許容上限

# 閾値定義
R_WARNING   = 0.75   # この値を超えたら予兆警告
R_CRITICAL  = 1.0    # この値以上で Fail-Closed

# -------------------------------------------------------
# データ構造
# -------------------------------------------------------

@dataclass
class BeltState:
    """ベルト状態の記録構造"""
    belt_id:   str
    t_current: float   # 現在張力 [N]
    t_optimal: float   # 最適張力 [N]
    t_min:     float   # 許容下限 [N]
    t_max:     float   # 許容上限 [N]
    timestamp: float   # タイムスタンプ [s]

@dataclass
class IDEResult:
    """NRA-IDE 評価結果"""
    delta:  float   # 蓄積ズレ δ [N]
    tau:    float   # 吸収厚み τ [N]
    R:      float   # 接近比 R = δ/τ
    status: str     # SAFE / WARNING / FAIL_CLOSED
    action: str     # 推奨アクション

# -------------------------------------------------------
# NRA-IDE コア計算
# -------------------------------------------------------

def calc_delta(t_current: float, t_optimal: float) -> float:
    """
    蓄積ズレ δ の計算
    現在張力と最適張力の絶対偏差
    「距離ではなく制約からのズレ」として定義
    """
    return abs(t_current - t_optimal)


def calc_tau(t_current: float, t_optimal: float,
             t_min: float, t_max: float) -> float:
    """
    吸収厚み τ の計算
    最適値から当該方向の構造限界までの全余裕

    上限方向ズレ：τ = T_max - T_optimal
      → 破断・軸受損傷に至るまでの全余裕
    下限方向ズレ：τ = T_optimal - T_min
      → スリップ発生に至るまでの全余裕

    R = δ/τ は [0,1] が許容内として自然に定義される
    """
    if t_current >= t_optimal:
        tau = t_max - t_optimal
    else:
        tau = t_optimal - t_min
    return max(tau, 0.01)   # ゼロ割り保護


def evaluate_belt(state: BeltState) -> IDEResult:
    """
    NRA-IDE ベルト張力評価
    R = δ / τ

    R < 0.75  : SAFE（正常稼働継続）
    R >= 0.75 : WARNING（予兆検出・点検前倒し）
    R >= 1.0  : FAIL_CLOSED（即時停止・整合性なければ不能）
    """
    delta = calc_delta(state.t_current, state.t_optimal)
    tau   = calc_tau(state.t_current, state.t_optimal,
                     state.t_min, state.t_max)

    # 許容域完全逸脱（定義域外）→ 即 Fail-Closed
    if state.t_current < state.t_min or state.t_current > state.t_max:
        R = delta / tau
        return IDEResult(
            delta=delta, tau=tau, R=R,
            status="FAIL_CLOSED",
            action="即時停止：張力が許容域を逸脱（テンショナー交換）"
        )

    R = delta / tau

    if R >= R_CRITICAL:
        status = "FAIL_CLOSED"
        action = "即時停止：テンショナー調整または交換"
    elif R >= R_WARNING:
        status = "WARNING"
        action = "予兆検出：次回点検を前倒し実施"
    else:
        status = "SAFE"
        action = "正常稼働継続"

    return IDEResult(delta=delta, tau=tau, R=R,
                     status=status, action=action)

# -------------------------------------------------------
# 実行サンプル
# -------------------------------------------------------

def run_sample():
    print("=" * 65)
    print(" NRA-IDE ベルト張力管理 サンプル実行")
    print(" 設計原則：R = δ/τ  R>=1.0 → Fail-Closed")
    print("=" * 65)

    test_cases = [
        # (belt_id, t_current, 状況説明)
        ("CONV-01", 505.0, "正常範囲（最適値近傍）"),
        ("CONV-02", 455.0, "下限方向 WARNING 帯"),
        ("CONV-03", 415.0, "下限接近（Fail-Closed直前）"),
        ("CONV-04", 395.0, "下限超過（即時停止）"),
        ("CONV-05", 585.0, "上限方向 WARNING 帯"),
        ("CONV-06", 638.0, "上限接近（Fail-Closed直前）"),
        ("CONV-07", 660.0, "上限超過（即時停止）"),
        ("VBLT-01", 302.0, "Vベルト正常"),
        ("VBLT-02", 255.0, "Vベルト下限 WARNING"),
        ("VBLT-03", 368.0, "Vベルト上限 WARNING"),
    ]

    for belt_id, t_current, desc in test_cases:
        if belt_id.startswith("CONV"):
            t_opt, t_min, t_max = (
                CONVEYOR_T_OPTIMAL, CONVEYOR_T_MIN, CONVEYOR_T_MAX)
        else:
            t_opt, t_min, t_max = (
                VBELT_T_OPTIMAL, VBELT_T_MIN, VBELT_T_MAX)

        state = BeltState(
            belt_id=belt_id, t_current=t_current,
            t_optimal=t_opt, t_min=t_min, t_max=t_max,
            timestamp=0.0
        )
        r = evaluate_belt(state)

        print(f"\n [{belt_id}] {desc}")
        print(f"   現在張力 : {t_current:6.1f} N"
              f"  (最適:{t_opt:.0f} / 範囲:{t_min:.0f}〜{t_max:.0f})")
        print(f"   δ={r.delta:6.1f}N  τ={r.tau:6.1f}N  R={r.R:.3f}")
        print(f"   状態     : {r.status}")
        print(f"   対応     : {r.action}")

    print("\n" + "=" * 65)
    print(" 整合性がない場合は不能を返す（Fail-Closed原則）")
    print("=" * 65)


if __name__ == "__main__":
    run_sample()
