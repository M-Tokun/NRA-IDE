# FILE: chain_tension_nra_ide_20260319_0113.py
# TITLE: チェーン張力管理 NRA-IDE ゆらぎ利用型自動調整サンプル
# Author: M-Tokuni / NRA-IDE Project
# Generated: 2026-03-19 01:13 JST
#
# 設計原則：
#   ゆらぎは除去すべきノイズではなく「構造固有の追跡対象」
#   dR/dt（R値変化速度）とゆらぎパターンを制御信号として使用
#   R >= 1.0 → Fail-Closed（自動調整権限を人間に返却）
#   自動調整はR < 1.0の範囲でのみ動作
#
# ポリゴン効果（多角形効果）：
#   チェーンはスプロケット噛み合いで周期的張力ゆらぎが発生
#   このゆらぎパターンの変質が異常の予兆となる
# -------------------------------------------------------

import math
import time
from dataclasses import dataclass, field
from typing import List

# -------------------------------------------------------
# 定数定義
# -------------------------------------------------------

T_OPTIMAL   = 800.0    # N : 設計最適張力
T_MIN       = 620.0    # N : 許容下限（伸び・外れリスク）
T_MAX       = 1000.0   # N : 許容上限（破断・スプロケット損傷）

R_WARN      = 0.75     # WARNING 閾値
R_FAIL      = 1.0      # Fail-Closed 閾値

# ポリゴン効果パラメータ
SPROCKET_TEETH  = 17          # スプロケット歯数
POLYGON_AMP     = 35.0        # N : 正常時ゆらぎ振幅
POLYGON_PERIOD  = 1.0 / 5.0   # s : 基本周期（5Hz想定）

# 自動調整パラメータ
ADJ_GAIN_FINE   = 0.15   # 微調整ゲイン（R < 0.75）
ADJ_GAIN_AHEAD  = 0.35   # 先行調整ゲイン（R >= 0.75）
ADJ_MAX_STEP    = 25.0   # N/step : 1回の最大調整量
ADJ_HISTORY     = 8      # dR/dt 計算に使う履歴数

# -------------------------------------------------------
# データ構造
# -------------------------------------------------------

@dataclass
class ChainState:
    """チェーン状態スナップショット"""
    timestamp:  float
    t_raw:      float    # 生張力（ゆらぎ込み）
    t_smooth:   float    # 平滑化張力
    delta:      float    # 蓄積ズレ δ
    tau:        float    # 吸収厚み τ
    R:          float    # 接近比 R = δ/τ
    drdt:       float    # R変化速度 dR/dt
    polygon_amp: float   # 検出ゆらぎ振幅
    status:     str      # SAFE / WARNING / FAIL_CLOSED
    adj_output: float    # 自動調整量 [N]
    adj_reason: str      # 調整理由

@dataclass
class RingBuffer:
    """固定長履歴バッファ"""
    capacity: int
    data: List[float] = field(default_factory=list)

    def push(self, v: float):
        self.data.append(v)
        if len(self.data) > self.capacity:
            self.data.pop(0)

    def mean(self) -> float:
        return sum(self.data) / len(self.data) if self.data else 0.0

    def amplitude(self) -> float:
        if len(self.data) < 2:
            return 0.0
        return max(self.data) - min(self.data)

# -------------------------------------------------------
# NRA-IDE コア計算
# -------------------------------------------------------

def calc_ide(t_smooth: float) -> tuple:
    """
    接近比 R = δ / τ
    τ = 最適値から当該方向の構造限界までの全余裕
    """
    delta = abs(t_smooth - T_OPTIMAL)
    tau   = (T_MAX - T_OPTIMAL) if t_smooth >= T_OPTIMAL \
            else (T_OPTIMAL - T_MIN)
    tau   = max(tau, 0.01)
    R     = delta / tau
    return delta, tau, R

# -------------------------------------------------------
# ゆらぎ生成（ポリゴン効果シミュレーション）
# -------------------------------------------------------

def polygon_fluctuation(t: float, amp: float) -> float:
    """
    スプロケット噛み合いによる周期的ゆらぎ
    基本波 + 高調波で現実のチェーンゆらぎを模倣
    """
    freq = 1.0 / POLYGON_PERIOD
    v  = amp * math.sin(2 * math.pi * freq * t)
    v += amp * 0.3 * math.sin(2 * math.pi * freq * 2 * t + 0.4)
    v += amp * 0.1 * math.sin(2 * math.pi * freq * 3 * t + 0.9)
    return v

# -------------------------------------------------------
# 自動調整計算（ゆらぎ利用型）
# -------------------------------------------------------

def calc_adjustment(R: float, drdt: float,
                    poly_amp: float, t_smooth: float) -> tuple:
    """
    ゆらぎのdR/dtとパターン変質を制御信号として使用

    R < 0.5               : 調整不要
    0.5 ≤ R < R_WARN     : 微調整（ゆらぎ方向追従）
    R_WARN ≤ R < R_FAIL  : 先行調整（到達予測から算出）
    R >= R_FAIL           : Fail-Closed（調整権限返却）
    """
    if R >= R_FAIL:
        return 0.0, "FAIL_CLOSED：調整権限を人間に返却"

    # ゆらぎ振幅異常検出（正常振幅の1.5倍超で予兆）
    amp_ratio = poly_amp / POLYGON_AMP if POLYGON_AMP > 0 else 1.0
    amp_warn  = amp_ratio > 1.5

    # 最適値への方向
    direction = 1.0 if t_smooth < T_OPTIMAL else -1.0

    if R < 0.5 and not amp_warn:
        return 0.0, "正常：調整不要"

    elif R < R_WARN:
        # 微調整：偏差に比例、ゆらぎ振幅異常時は補正追加
        gain  = ADJ_GAIN_FINE * (1.0 + 0.5 if amp_warn else 1.0)
        adj   = direction * min(abs(t_smooth - T_OPTIMAL) * gain,
                                ADJ_MAX_STEP * 0.5)
        reason = f"微調整（R={R:.3f}" + \
                 ("・振幅異常検出" if amp_warn else "") + "）"
        return adj, reason

    else:
        # 先行調整：dR/dtから到達予測し先行制御
        if drdt > 0.001:
            # R上昇中：到達時間を予測して必要調整量を先行投入
            eta = (R_FAIL - R) / drdt   # 到達予測時間 [s]
            urgency = max(0.0, 1.0 - eta * 0.5)  # 切迫度
            gain    = ADJ_GAIN_AHEAD * (1.0 + urgency)
        else:
            gain = ADJ_GAIN_AHEAD

        adj    = direction * min(abs(t_smooth - T_OPTIMAL) * gain,
                                 ADJ_MAX_STEP)
        reason = f"先行調整（R={R:.3f} dR/dt={drdt:+.4f}）"
        return adj, reason

# -------------------------------------------------------
# シミュレーション実行
# -------------------------------------------------------

def run_simulation():
    print("=" * 68)
    print(" NRA-IDE チェーン張力管理 ゆらぎ利用型自動調整 シミュレーション")
    print(f" T_OPT={T_OPTIMAL}N  T_MIN={T_MIN}N  T_MAX={T_MAX}N")
    print("=" * 68)

    T_SIM    = 8.0     # 総シミュレーション時間 [s]
    DT       = 0.05    # タイムステップ [s]
    steps    = int(T_SIM / DT)

    # 初期張力（意図的に低め設定してR上昇→自動調整を観察）
    t_current = 700.0

    # バッファ
    smooth_buf = RingBuffer(capacity=10)
    R_buf      = RingBuffer(capacity=ADJ_HISTORY)
    raw_buf    = RingBuffer(capacity=20)
    history: List[ChainState] = []

    print(f"\n{'t[s]':>5} {'T_raw':>7} {'T_smt':>7} "
          f"{'δ':>6} {'τ':>6} {'R':>7} "
          f"{'dR/dt':>8} {'状態':>12} {'調整[N]':>8}")
    print("-" * 90)

    for i in range(steps):
        t = i * DT

        # ポリゴン効果ゆらぎ付加
        fluct = polygon_fluctuation(t, POLYGON_AMP)
        t_raw = t_current + fluct

        # 平滑化（移動平均）
        smooth_buf.push(t_raw)
        raw_buf.push(t_raw)
        t_smooth = smooth_buf.mean()

        # NRA-IDE コア計算
        delta, tau, R = calc_ide(t_smooth)

        # dR/dt 計算
        R_buf.push(R)
        if len(R_buf.data) >= 2:
            drdt = (R_buf.data[-1] - R_buf.data[-2]) / DT
        else:
            drdt = 0.0

        # ゆらぎ振幅検出
        poly_amp = raw_buf.amplitude()

        # 状態判定
        if R >= R_FAIL:
            status = "FAIL_CLOSED"
        elif R >= R_WARN:
            status = "WARNING"
        else:
            status = "SAFE"

        # 自動調整計算
        adj, reason = calc_adjustment(R, drdt, poly_amp, t_smooth)

        # 調整適用（Fail-Closed時は適用しない）
        if status != "FAIL_CLOSED":
            t_current += adj
            t_current = max(min(t_current, T_MAX + 50), T_MIN - 50)

        # 記録
        state = ChainState(
            timestamp=t, t_raw=t_raw, t_smooth=t_smooth,
            delta=delta, tau=tau, R=R, drdt=drdt,
            polygon_amp=poly_amp, status=status,
            adj_output=adj, adj_reason=reason
        )
        history.append(state)

        # 5ステップごとに表示
        if i % 5 == 0:
            st_sym = {'SAFE':'✓','WARNING':'▲','FAIL_CLOSED':'✕'}[status]
            print(f"{t:5.2f} {t_raw:7.1f} {t_smooth:7.1f} "
                  f"{delta:6.1f} {tau:6.1f} {R:7.4f} "
                  f"{drdt:+8.4f} {st_sym+status:>13} {adj:+8.1f}")

    print("\n" + "=" * 68)
    # サマリー
    safe_n = sum(1 for s in history if s.status == "SAFE")
    warn_n = sum(1 for s in history if s.status == "WARNING")
    fail_n = sum(1 for s in history if s.status == "FAIL_CLOSED")
    total  = len(history)
    print(f" SAFE       : {safe_n:3d} steps ({safe_n/total*100:.1f}%)")
    print(f" WARNING    : {warn_n:3d} steps ({warn_n/total*100:.1f}%)")
    print(f" FAIL_CLOSED: {fail_n:3d} steps ({fail_n/total*100:.1f}%)")
    adj_total = sum(abs(s.adj_output) for s in history)
    print(f" 総調整量   : {adj_total:.1f} N")
    print("=" * 68)
    print(" 設計原則：自動調整はR<1.0の範囲のみ。R>=1.0は人間に返却。")
    print("=" * 68)


if __name__ == "__main__":
    run_simulation()
