# ============================================================
# nra_ide_demo15_or_icu_26-0321.py
# NRA-IDE Demo #15 — OR/ICU Continuum Monitor
# 経過蓄積型モニタリング / 手術室・集中治療室
#
# Author: M-Tokuni / NRA-IDE Project
# https://github.com/M-Tokun/NRA-IDE
#
# 依存: nra_ide_core_base_26-0321.py（同ディレクトリに置く）
#
# 単体実行:
#   python3 nra_ide_demo15_or_icu_26-0321.py
#
# このファイルが扱うもの:
#   - HR / SpO₂ / RR / BP の4チャンネル同時監視
#   - 経過蓄積によって τ が確立される（ウォームアップ構造）
#   - R_total = √(ΣR²) — チャンネル間相関を使わない O(n) 合成
#   - residual_debt = 一時回復後も消えない構造的負債
#   - 新患・救急 → ウォームアップ期間（威力なし）
#   - 経過あり → 時間が経つほど精度が上がる
#
# 設計の核心:
#   「現在を知るためには経過が必須。
#    経過こそ威力。」
# ============================================================

import math
import random
from dataclasses import dataclass
from typing import Dict, List

from nra_ide_core_base_26_0321 import FSMState, NRAChannel, NRASystemState


# ============================================================
# 患者バイタル設定（設計時固定）
# ============================================================

# τ は「設計時固定の規則」によって決まる。
# 値は観測開始後のウォームアップで徐々に確立される。
# Effect-Side（計測結果）からτへの逆流は禁止（Π⁻¹禁止）。

BASELINE: Dict[str, float] = {
    "hr":   72.0,   # 安静時心拍数 [bpm]
    "spo2": 99.0,   # 酸素飽和度 [%]
    "rr":   14.0,   # 呼吸数 [回/分]
    "bp":  120.0,   # 収縮期血圧 [mmHg]
}

TAU_BASE: Dict[str, float] = {
    "hr":   18.0,   # 許容偏差幅（設計値）
    "spo2":  3.0,
    "rr":    5.0,
    "bp":   20.0,
}


# ============================================================
# OR/ICU 継続モニタリング NRA エンジン
# ============================================================

class VitalSignNRA:
    """
    Demo #15 物理エンジン

    HR / SpO₂ / RR / BP の4チャンネルを同時監視し、
    R_total = √(ΣR²) で構造的接近比を合成する。

    ウォームアップ構造:
      - 観測開始直後: τ = 0（経過なし → R の精度なし）
      - 観測継続中: τ が徐々に確立 → R 精度が上がる
      - WARMUP_SEC 経過後: τ 確立完了 → 最高精度

    これが「新患・救急に威力なし、経過あり症例に威力あり」の構造的理由。

    Parameters
    ----------
    warmup_sec : τ確立に要する秒数（デフォルト 90 秒）
    """

    WARMUP_SEC  = 90.0   # τ確立秒数
    K_RECOVERY  = 0.10   # 復元係数

    # FSM 遷移閾値
    TH_CAVEAT      = 0.35
    TH_CRITICAL    = 0.60
    TH_FAIL_CLOSED = 1.00

    def __init__(self, warmup_sec: float = WARMUP_SEC):
        self.warmup_sec = warmup_sec

        # チャンネル初期化（τ=0 からスタート）
        self.channels: Dict[str, NRAChannel] = {
            name: NRAChannel(
                name=name,
                tau=0.0,
                baseline=BASELINE[name],
                value=BASELINE[name],
            )
            for name in ("hr", "spo2", "rr", "bp")
        }

        self.R_total:       float    = 0.0
        self.residual_debt: float    = 0.0
        self.warmup_pct:    float    = 0.0
        self.elapsed:       float    = 0.0
        self.fsm:           FSMState = FSMState.WARMUP
        self.procedure_started: bool = False

        # イベント状態
        self._bleed_decay: float = 0.0
        self._anes_decay:  float = 0.0
        self._vaso_decay:  float = 0.0
        self._intervene:   bool  = False

        self.history: List[dict] = []

    # ── メインステップ ──

    def step(self, dt: float = 0.016) -> NRASystemState:
        """
        物理を1ステップ進める。

        執刀前（procedure_started=False）は安静ゆらぎのみ。
        執刀後からウォームアップが進み、τが確立される。

        Parameters
        ----------
        dt : タイムステップ [秒]
        """
        self.elapsed += dt

        if not self.procedure_started:
            # 執刀前: 安静ゆらぎ（新患モニター接続状態）
            self._apply_resting_fluctuation(dt)
            return NRASystemState(fsm=FSMState.WARMUP, elapsed=self.elapsed)

        # ── ウォームアップ進行 ──
        self.warmup_pct = min(100.0, (self.elapsed / self.warmup_sec) * 100.0)
        wf = self.warmup_pct / 100.0   # 精度係数 0.0→1.0

        # τを段階的に確立（経過が積まれるほどτが設計値に近づく）
        for name, ch in self.channels.items():
            ch.tau = TAU_BASE[name] * wf

        # ── バイタル更新 ──
        dv = self._compute_delta_vitals(dt)
        self._apply_vitals(dv, dt)

        # ── R 計算（各チャンネル独立・Cause-Side）──
        for ch in self.channels.values():
            ch.compute_R(ch.value)

        # ── R_total ノルム合成 × 精度係数 ──
        sum_r2 = sum(ch.R ** 2 for ch in self.channels.values())
        self.R_total = math.sqrt(sum_r2) * wf

        # ── 残留負債更新 ──
        recover_force = 0.5 * dt if self._intervene else 0.0
        k_rec = self.K_RECOVERY + recover_force

        if self.R_total > 0.3:
            self.residual_debt += (
                self.R_total - self.R_total * k_rec
            ) * dt * 0.06 * wf
        else:
            self.residual_debt = max(0.0, self.residual_debt - dt * 0.02)
        self.residual_debt = min(self.residual_debt, 3.0)

        # ── FSM 遷移 ──
        self._update_fsm(wf)

        # ── ログ記録 ──
        self.history.append({
            "t":       round(self.elapsed, 3),
            "hr":      round(self.channels["hr"].value,   1),
            "spo2":    round(self.channels["spo2"].value, 2),
            "rr":      round(self.channels["rr"].value,   1),
            "bp":      round(self.channels["bp"].value,   1),
            "R_total": round(self.R_total, 5),
            "debt":    round(self.residual_debt, 5),
            "warmup":  round(self.warmup_pct, 1),
            "fsm":     self.fsm.value,
        })

        return NRASystemState(
            fsm=self.fsm,
            R_total=self.R_total,
            residual_debt=self.residual_debt,
            warmup_pct=self.warmup_pct,
            elapsed=self.elapsed,
        )

    # ── 内部メソッド ──

    def _apply_resting_fluctuation(self, dt: float):
        """執刀前の安静ゆらぎ"""
        micro = (random.random() - 0.5)
        macro = math.sin(self.elapsed * 0.18) * 0.3
        ch = self.channels
        ch["hr"].value   = max(68.0,  min(76.0,  ch["hr"].value   + micro * 0.8  * dt))
        ch["spo2"].value = max(98.0,  min(100.0, ch["spo2"].value + micro * 0.05 * dt))
        ch["rr"].value   = max(12.0,  min(16.0,  ch["rr"].value   + micro * 0.3  * dt))
        ch["bp"].value   = max(115.0, min(125.0, ch["bp"].value
                          + (micro * 1.5 + macro * 1.0) * dt))

    def _compute_delta_vitals(self, dt: float) -> dict:
        """ゆらぎ + イベントδを計算"""
        micro = (random.random() - 0.5)
        macro = math.sin(self.elapsed * 0.18) * 0.4 \
              + math.sin(self.elapsed * 0.07) * 0.3

        dv = {
            "hr":   micro * 1.2 + macro * 1.8,
            "spo2": micro * 0.1 - max(0, macro) * 0.08,
            "rr":   micro * 0.5 + macro * 0.6,
            "bp":   micro * 2.0 + macro * 3.0,
        }

        # 出血: HR↑ BP↓ SpO₂↓ RR↑
        if self._bleed_decay > 0:
            self._bleed_decay = max(0.0, self._bleed_decay - dt * 0.15)
            b = self._bleed_decay
            dv["hr"]   += b * 6.0
            dv["bp"]   -= b * 12.0
            dv["spo2"] -= b * 0.5
            dv["rr"]   += b * 2.5

        # 麻酔深度変化: HR↓ BP↓ RR↓
        if self._anes_decay > 0:
            self._anes_decay = max(0.0, self._anes_decay - dt * 0.2)
            a = self._anes_decay
            dv["hr"]  -= a * 8.0
            dv["bp"]  -= a * 15.0
            dv["rr"]  -= a * 1.5

        # 血管攣縮: BP急上昇
        if self._vaso_decay > 0:
            self._vaso_decay = max(0.0, self._vaso_decay - dt * 0.3)
            v = self._vaso_decay
            dv["bp"]  += v * 20.0
            dv["hr"]  += v * 5.0

        return dv

    def _apply_vitals(self, dv: dict, dt: float):
        """バイタル値に変化量を適用（物理上下限クリップ）"""
        ch = self.channels
        ch["hr"].value   = max(30.0,  min(180.0, ch["hr"].value   + dv["hr"]   * dt))
        ch["spo2"].value = max(80.0,  min(100.0, ch["spo2"].value + dv["spo2"] * dt))
        ch["rr"].value   = max(4.0,   min(40.0,  ch["rr"].value   + dv["rr"]   * dt))
        ch["bp"].value   = max(50.0,  min(200.0, ch["bp"].value   + dv["bp"]   * dt))

    def _update_fsm(self, wf: float):
        """FSM 遷移ロジック"""
        R_eff = self.R_total + self.residual_debt * 0.4

        if self.warmup_pct < 15.0:
            self.fsm = FSMState.WARMUP
        elif R_eff >= self.TH_FAIL_CLOSED or self.residual_debt > 1.2:
            self.fsm = FSMState.FAIL_CLOSED
        elif R_eff >= self.TH_CRITICAL:
            self.fsm = FSMState.CRITICAL
        elif R_eff >= self.TH_CAVEAT:
            self.fsm = FSMState.CAVEAT
        else:
            if self.fsm != FSMState.FAIL_CLOSED:
                self.fsm = FSMState.PERMIT

    # ── イベントトリガー（Cause-Side 入力）──

    def start_procedure(self):
        """
        執刀開始。
        δ蓄積・τ確立 が始まる。
        これ以前は「新患・救急相当」（ウォームアップ前）。
        """
        self.procedure_started = True

    def trigger_bleed(self, magnitude: float = 1.0):
        """出血イベント"""
        if self.fsm == FSMState.FAIL_CLOSED:
            return
        self._bleed_decay = magnitude + random.random() * 0.8

    def trigger_anesthesia(self, magnitude: float = 1.2):
        """麻酔深度変化"""
        if self.fsm == FSMState.FAIL_CLOSED:
            return
        self._anes_decay = magnitude + random.random() * 0.6

    def trigger_vasospasm(self, magnitude: float = 0.8):
        """血管攣縮"""
        if self.fsm == FSMState.FAIL_CLOSED:
            return
        self._vaso_decay = magnitude + random.random() * 0.5

    def trigger_intervene(self):
        """
        医師介入（人間操作）。
        FAIL-CLOSED からの唯一の脱出経路。
        residual_debt は介入後も残存する。
        """
        self._intervene = True
        if self.fsm == FSMState.FAIL_CLOSED:
            self.fsm = FSMState.CRITICAL

    def reset(self):
        """完全リセット。新患状態（経過なし）に戻る。"""
        self.__init__(self.warmup_sec)


# ============================================================
# CLI 実行
# ============================================================

def main():
    print("=" * 70)
    print("NRA-IDE Demo #15 — OR/ICU Continuum Monitor (Python Core)")
    print("経過蓄積型モニタリング")
    print("=" * 70)
    print(f"WARMUP = {VitalSignNRA.WARMUP_SEC}s  |  4チャンネル合成  |  FAIL-CLOSED 閾値 R ≥ 1.00")
    print()
    print("  新患・救急相当: ウォームアップ期間（経過なし → R 精度なし）")
    print("  経過あり:       τ確立後 → 時間が経つほど精度が上がる")
    print()

    vital = VitalSignNRA()

    print("--- フェーズ1: 執刀前（新患状態 = ウォームアップ前）---")
    for _ in range(20):
        vital.step(dt=0.05)
    ch = vital.channels
    print(f"  HR={ch['hr'].value:.1f}  SpO₂={ch['spo2'].value:.1f}"
          f"  RR={ch['rr'].value:.1f}  BP={ch['bp'].value:.1f}")
    print(f"  warmup={vital.warmup_pct:.1f}%  FSM={vital.fsm.value}")
    print(f"  → R計算精度なし（τ未確立）\n")

    print("--- フェーズ2: 執刀開始 → ウォームアップ進行 ---")
    vital.start_procedure()
    prev_fsm = vital.fsm

    events = {
        300:  ("trigger_bleed",      "🩸 出血イベント"),
        500:  ("trigger_anesthesia", "💉 麻酔深度変化"),
        700:  ("trigger_vasospasm",  "⚡ 血管攣縮"),
    }
    intervened = False

    for i in range(900):
        if i in events:
            method, label = events[i]
            getattr(vital, method)()
            print(f"  [{vital.elapsed:6.2f}s] *** {label} ***")

        if vital.fsm == FSMState.FAIL_CLOSED and not intervened:
            vital.trigger_intervene()
            intervened = True
            print(f"  [{vital.elapsed:6.2f}s] *** ✚ 医師介入（人間操作）"
                  f"  debt={vital.residual_debt:.4f} 残存 ***")

        state = vital.step(dt=0.05)

        if state.fsm != prev_fsm:
            print(
                f"  [{state.elapsed:6.2f}s]  遷移: {prev_fsm.value:12s}"
                f" → {state.fsm.value:12s}"
                f"  R={state.R_total:.4f}  debt={state.residual_debt:.4f}"
                f"  warmup={state.warmup_pct:.1f}%"
            )
            prev_fsm = state.fsm

        if i % 100 == 0:
            ch = vital.channels
            stars = "★" * int(state.warmup_pct / 20) + \
                    "☆" * (5 - int(state.warmup_pct / 20))
            print(
                f"  t={state.elapsed:6.2f}s |"
                f" HR={ch['hr'].value:5.1f}"
                f" SpO₂={ch['spo2'].value:5.1f}"
                f" RR={ch['rr'].value:4.1f}"
                f" BP={ch['bp'].value:5.1f} |"
                f" R={state.R_total:.4f} |"
                f" debt={state.residual_debt:.4f} |"
                f" {stars} |"
                f" {state.fsm.value}"
            )

    print()
    print("=== 構造設計のポイント ===")
    print("  warmup_pct:    経過が積まれるほどτが確立 → R精度が上がる")
    print("  R_total:       √ΣR² 合成 — 各値が正常範囲内でも上昇しうる")
    print("  residual_debt: 介入後も消えない構造的負債")
    print("  FAIL-CLOSED:   trigger_intervene()（人間操作）でのみ復帰")


if __name__ == "__main__":
    main()
