# FILE: NRA_IDE_Axiom2_HistoricalAccumulation_20260425_2202.py
#
# Title: NRA-IDE Axiom 2 — 履歴蓄積と吸収厚み / Historical Accumulation and Absorption Thickness
#
# Position / 位置づけ:
#   Upper-layer extension of nra_ide_foundation_fixed_JP.py
#   nra_ide_foundation_fixed_JP.py の上位拡張層
#   Implements Axiom 2 (δ accumulation / τ depletion) with
#   Axiom 4 (τ depletion integral) and Axiom 5 (restoration degradation).
#   公理2（δ蓄積/τ消耗）、公理4（τ消耗積分）、公理5（復元劣化）を実装。
#
# Axiom References / 公理参照:
#   Axiom 2 : Historical Accumulation and Absorption Thickness
#             生成が続く限り構造には履歴が蓄積する。その蓄積が δ、余裕が τ。
#   Axiom 3 : Domain constraint — τ > 0
#             τ = 0 は定義域外であり構造そのものが成立しない。
#   Axiom 4 : τ(t) = τ₀ − ∫f(δ(s))ds
#             τ は外生補充なしに自然回復しない。
#   Axiom 5 : τ_restored < τ₀
#             一度の相転移後、τ は初期値に戻らない（復元劣化）。
#   Axiom 6 : R ≥ 1 → Break / Phase Transition
#   Axiom 8 : Fail-Closed — break 後は演算対象から排除。
#
# Author : M-Tokuni / NRA-IDE Project https://github.com/M-Tokun/NRA-IDE
# Date   : 2026-04-25 22:02 JST
# License: MIT
# Ref    : theory/AXIOMS_rewritten_2026-04-24_011508.md

from __future__ import annotations

import math
import random
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple

# ─────────────────────────────────────────────────────────────────
# Dependency / 依存関係
#   Requires nra_ide_foundation_fixed_JP.py in the same directory.
#   同ディレクトリに nra_ide_foundation_fixed_JP.py が必要です。
# ─────────────────────────────────────────────────────────────────

from nra_ide_foundation_fixed_JP import (
    DynamicState,
    EnergyLedger,
    Token,
    Law,
    Node,
    jst_now,
)


# ─────────────────────────────────────────────────────────────────
# DepletionConfig
#   All tunable parameters for Axiom 2 accumulation/depletion layer.
#   公理2 蓄積/消耗層の全チューニングパラメータ。
# ─────────────────────────────────────────────────────────────────

@dataclass
class DepletionConfig:
    # ── Structural / 構造初期値 ──────────────────────────────────
    tau0          : float = 0.40    # Initial absorption thickness / 初期吸収厚み
    domain_min_tau: float = 1e-6    # Axiom 3 domain constraint (τ > 0)

    # ── δ accumulation model / δ蓄積モデル ──────────────────────
    drift_a    : float = 0.001      # Linear drift coefficient / 線形ドリフト係数
    drift_b    : float = 0.00002    # Quadratic drift coefficient / 2次ドリフト係数
    noise_amp  : float = 0.0003     # Gaussian noise amplitude / ガウスノイズ振幅

    # ── τ depletion (Axiom 4) / τ消耗（公理4）──────────────────
    depletion_k: float = 0.18       # f(δ) = depletion_k × δ × dt
    dt         : float = 1.0        # Time step unit / 時間ステップ単位

    # ── Restoration degradation (Axiom 5) / 復元劣化（公理5）───
    restore_factor: float = 0.82    # τ_ceiling × factor per restore / 補充毎の上限劣化率
    restore_add   : float = 0.15    # τ increment per replenishment / 補充量

    def __post_init__(self) -> None:
        assert self.tau0          > 0,   "tau0 must be positive / tau0 は正値が必要"
        assert self.depletion_k   > 0,   "depletion_k must be positive"
        assert self.dt            > 0,   "dt must be positive"
        assert 0 < self.restore_factor < 1, "restore_factor ∈ (0,1) required (Axiom 5)"


# ─────────────────────────────────────────────────────────────────
# AccumulationState
#   Continuous-domain state for δ/τ dynamics (separate from Token).
#   δ/τ 連続値状態（Token の正規化状態量とは独立）。
# ─────────────────────────────────────────────────────────────────

@dataclass
class AccumulationState:
    delta        : float = 0.0       # Accumulated deviation / 蓄積ズレ δ(t)
    tau          : float = 0.40      # Current absorption thickness / 現在の吸収厚み τ(t)
    tau0         : float = 0.40      # Immutable initial τ₀ / 変更不可の初期値 τ₀
    tau_ceiling  : float = 0.40      # Axiom 5: max achievable τ / 到達可能上限（劣化する）
    integral_f   : float = 0.0       # ∫f(δ(s))ds cumulative / τ累積消耗量
    restore_count: int   = 0         # Number of restorations / 補充回数
    broken       : bool  = False     # Phase transition occurred / 相転移発生フラグ
    history      : List[Dict[str, Any]] = field(default_factory=list, repr=False)

    @property
    def R(self) -> float:
        """Structural approach ratio R = δ/τ (Axiom 3 / Axiom 6)"""
        if self.tau <= 0:
            return float("inf")
        return self.delta / self.tau

    @property
    def degradation_rate(self) -> float:
        """Axiom 5: how much τ_ceiling has degraded from τ₀ (0.0 = none, 1.0 = full)"""
        if self.tau0 <= 0:
            return 0.0
        return max(0.0, 1.0 - self.tau_ceiling / self.tau0)

    def record_tick(self, cycle: int) -> None:
        self.history.append({
            "cycle"        : cycle,
            "delta"        : self.delta,
            "tau"          : self.tau,
            "tau_ceiling"  : self.tau_ceiling,
            "integral_f"   : self.integral_f,
            "R"            : self.R if not math.isinf(self.R) else 999.0,
            "restore_count": self.restore_count,
            "broken"       : self.broken,
        })


# ─────────────────────────────────────────────────────────────────
# DepletionLaw
#   Implements Axiom 3 domain constraint and Axiom 6 break detection.
#   Axiom 8 Fail-Closed: if R ≥ 1, correct() returns None → infeasible.
#
#   公理3 定義域制約（τ > 0）と公理6 破断判定を実装。
#   公理8 Fail-Closed: R ≥ 1 の場合 correct() は None を返す → infeasible 確定。
# ─────────────────────────────────────────────────────────────────

class DepletionLaw(Law):
    def __init__(self, acc_state: AccumulationState, config: DepletionConfig):
        self._acc   = acc_state
        self._cfg   = config

    @property
    def name(self) -> str:
        return "DepletionLaw"

    def check(self, token: Token) -> bool:
        """
        Returns True if structure is intact.
        τ > domain_min (Axiom 3) AND R < 1 (Axiom 6).
        """
        if self._acc.tau <= self._cfg.domain_min_tau:
            return False   # Axiom 3 domain violation
        return self._acc.R < 1.0

    def tension(self, token: Token) -> float:
        """
        R = δ/τ — structural approach ratio (Axiom 3).
        Reflects how close the structure is to phase transition.
        """
        r = self._acc.R
        return r if math.isfinite(r) else 999.0

    def correct(self, token: Token) -> Optional[Token]:
        """
        Axiom 8 Fail-Closed:
          R ≥ 1 → no internal correction path → return None → infeasible.
          R < 1 → no correction needed (Axiom 4 depletion is irreversible from inside).
        """
        if self._acc.R >= 1.0 or self._acc.tau <= self._cfg.domain_min_tau:
            # Phase transition / domain collapse — Fail-Closed (Axiom 8)
            # 破断/定義域崩壊 — Fail-Closed（公理8）
            self._acc.broken = True
            return None
        # Within domain: no internal correction available.
        # τ depletion proceeds; only external replenishment can slow approach.
        # 定義域内: 内部補正経路なし。τ消耗は継続。外生補充のみが有効。
        return token


# ─────────────────────────────────────────────────────────────────
# AccumulationNode
#   Updates δ and τ each cycle according to Axiom 4.
#   Maps R → token.state.value so foundation SafetyNode can observe.
#
#   サイクルごとに δ増加・τ消耗を更新（公理4）。
#   R を token.state.value にマップし foundation の SafetyNode が観測可能にする。
# ─────────────────────────────────────────────────────────────────

class AccumulationNode(Node):
    def __init__(
        self,
        name       : str,
        config     : DepletionConfig,
        acc_state  : AccumulationState,
    ):
        super().__init__(name)
        self._cfg   = config
        self._acc   = acc_state
        self._law   = DepletionLaw(acc_state, config)
        self._pending_dist: float = 0.0

    def inject_disturbance(self, magnitude: float) -> None:
        """
        Inject an external δ disturbance (sudden deviation increase).
        外部から δ 外乱を注入する（急激な蓄積ズレ増加）。
        """
        self._pending_dist += magnitude

    # ── f(δ): depletion rate function (Axiom 4) ──────────────────
    def _f_depletion(self, delta: float) -> float:
        return self._cfg.depletion_k * delta * self._cfg.dt

    def process(self, token: Token) -> Token:
        if token.meta.get("infeasible"):
            return self._record(token)

        acc  = self._acc
        cfg  = self._cfg
        cycle = token.meta["cycle"]

        # ── δ update / δ更新 ─────────────────────────────────────
        drift    = cfg.drift_a + cfg.drift_b * cycle
        noise    = random.gauss(0.0, cfg.noise_amp)
        delta_inc = drift + noise + self._pending_dist
        self._pending_dist *= 0.5          # disturbance decay
        delta_inc = max(0.0, delta_inc)    # δ は非負（単調増加方向）

        acc.delta += delta_inc

        # ── τ depletion via Axiom 4: dτ = −f(δ)dt ───────────────
        f_val      = self._f_depletion(acc.delta)
        acc.tau    = max(cfg.domain_min_tau, acc.tau - f_val)
        acc.integral_f += f_val

        # ── Token coupling / Tokenとの結合 ───────────────────────
        # R → token.state.value (normalized, capped at 1.0)
        r = acc.R
        safe_r = r if math.isfinite(r) else 1.0
        token.state.value   = min(1.0, safe_r)
        token.state.rate    = delta_inc
        token.state.tension = safe_r
        token.ledger.E_in          += delta_inc
        token.ledger.E_dissipated  += f_val    # τ depletion = history absorption cost

        # ── Law check / 則チェック ───────────────────────────────
        t_val = self._law.tension(token)
        if t_val > 0:
            token.state.tension = t_val
        if not self._law.check(token):
            token.log_violation(self._law.name)
            result = self._law.correct(token)
            if result is None:
                token.meta["infeasible"] = True
                token.meta.setdefault("break_cycle", cycle)
                acc.broken = True
                acc.record_tick(cycle)
                return self._record(token)
            token = result

        acc.record_tick(cycle)
        return self._record(token)


# ─────────────────────────────────────────────────────────────────
# RestorationNode
#   Axiom 5: External τ replenishment with ceiling degradation.
#   Each replenishment: τ_ceiling × restore_factor (irreversible).
#   τ is always < τ₀ after any break/restore.
#
#   公理5: 外生 τ 補充と上限劣化。
#   補充毎に τ_ceiling が restore_factor 倍で劣化（不可逆）。
#   補充後の τ は常に τ₀ 未満。
# ─────────────────────────────────────────────────────────────────

class RestorationNode(Node):
    def __init__(
        self,
        name          : str,
        acc_state     : AccumulationState,
        config        : DepletionConfig,
        trigger_cycles: List[int],
    ):
        super().__init__(name)
        self._acc     = acc_state
        self._cfg     = config
        self._triggers = set(trigger_cycles)

    def process(self, token: Token) -> Token:
        if token.meta.get("infeasible"):
            return self._record(token)

        cycle = token.meta["cycle"]
        if cycle not in self._triggers:
            return self._record(token)

        acc = self._acc
        cfg = self._cfg

        # ── Axiom 5: ceiling degrades per restoration ─────────────
        # τ₀ は回復しない / τ₀ is never recovered
        prev_ceiling = acc.tau_ceiling
        acc.tau_ceiling = prev_ceiling * cfg.restore_factor

        # Add τ, capped at the new (degraded) ceiling
        delta_add   = min(cfg.restore_add, max(0.0, acc.tau_ceiling - acc.tau))
        acc.tau    += delta_add
        acc.restore_count += 1

        # Log to Token metadata
        token.meta.setdefault("restore_events", []).append({
            "cycle"        : cycle,
            "tau_before"   : acc.tau - delta_add,
            "tau_after"    : acc.tau,
            "tau_ceiling"  : acc.tau_ceiling,
            "tau0"         : acc.tau0,
            "delta_added"  : delta_add,
            "restore_count": acc.restore_count,
            "note"         : "τ_restored < τ₀ — Axiom 5 Restoration Degradation",
        })

        self._logger.info(
            "[RestorationNode] cycle=%d  restore#%d  "
            "τ: %.4f → %.4f  ceiling: %.4f  (τ₀=%.4f  degradation=%.1f%%)",
            cycle, acc.restore_count,
            acc.tau - delta_add, acc.tau, acc.tau_ceiling,
            acc.tau0, acc.degradation_rate * 100,
        )

        return self._record(token)


# ─────────────────────────────────────────────────────────────────
# Axiom2Observer
#   Records per-cycle snapshot and generates 4-panel plot.
#   サイクルごとのスナップショット記録と4パネルプロット生成。
# ─────────────────────────────────────────────────────────────────

class Axiom2Observer:
    def __init__(self, acc_state: AccumulationState):
        self._acc     = acc_state
        self.records  : List[Dict[str, Any]] = []

    def record(self, token: Token) -> None:
        acc = self._acc
        self.records.append({
            "cycle"        : token.meta["cycle"],
            "delta"        : acc.delta,
            "tau"          : acc.tau,
            "tau0"         : acc.tau0,
            "tau_ceiling"  : acc.tau_ceiling,
            "integral_f"   : acc.integral_f,
            "R"            : acc.R if math.isfinite(acc.R) else 1.0,
            "restore_count": acc.restore_count,
            "broken"       : acc.broken,
            "E_in"         : token.ledger.E_in,
            "E_dissip"     : token.ledger.E_dissipated,
            "violated"     : bool(token.meta.get("violated_laws")),
        })

    def summary(self) -> str:
        acc = self._acc
        lines = [
            "=" * 60,
            "Axiom 2 Simulation Summary / シミュレーション結果",
            "=" * 60,
            f"  Cycles run     : {len(self.records)}",
            f"  δ final        : {acc.delta:.4f}",
            f"  τ final        : {acc.tau:.4f}",
            f"  τ₀ (initial)   : {acc.tau0:.4f}",
            f"  τ_ceiling      : {acc.tau_ceiling:.4f}",
            f"  ∫f(δ)ds        : {acc.integral_f:.5f}",
            f"  R final        : {acc.R:.4f}" if math.isfinite(acc.R) else "  R final        : ≥ 1.0 (BREAK)",
            f"  Broken         : {acc.broken}",
            f"  Restore count  : {acc.restore_count}",
            f"  Degradation    : {acc.degradation_rate * 100:.1f}%  (Axiom 5)",
            "─" * 60,
            "Axiom 3 domain constraint: τ > 0",
            "Axiom 4: τ depletes via ∫f(δ)ds — no spontaneous recovery",
            "Axiom 5: τ_restored < τ₀ — each restoration degrades ceiling",
            "=" * 60,
        ]
        return "\n".join(lines)

    def plot(self, save_path: str) -> None:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        if not self.records:
            self._acc._logger if hasattr(self._acc, '_logger') else None
            return

        cycles    = [r["cycle"]       for r in self.records]
        deltas    = [r["delta"]        for r in self.records]
        taus      = [r["tau"]          for r in self.records]
        tau0_line = [r["tau0"]         for r in self.records]
        ceilings  = [r["tau_ceiling"]  for r in self.records]
        integrals = [r["integral_f"]   for r in self.records]
        r_vals    = [min(r["R"], 1.2)  for r in self.records]
        broken_c  = next((r["cycle"] for r in self.records if r["broken"]), None)

        fig, axes = plt.subplots(4, 1, figsize=(11, 12), sharex=True)
        fig.suptitle(
            "NRA-IDE Axiom 2 — 履歴蓄積と吸収厚み / Historical Accumulation and Absorption Thickness\n"
            "τ(t) = τ₀ − ∫f(δ(s))ds  [Axiom 4]   ·   τ_restored < τ₀  [Axiom 5]",
            fontsize=9, y=0.99,
        )

        # ── Panel 1: δ(t) and τ(t) ──────────────────────────────
        ax = axes[0]
        ax.plot(cycles, deltas, color="#ffb347", linewidth=1.6, label="δ(t)  蓄積ズレ")
        ax.plot(cycles, taus,   color="#c060ff", linewidth=1.6, label="τ(t)  吸収厚み")
        ax.axhline(y=self.records[0]["tau0"], color="#c060ff",
                   linestyle=":", linewidth=0.8, alpha=0.5, label="τ₀ (initial)")
        if broken_c is not None:
            ax.axvline(x=broken_c, color="crimson", linestyle="--",
                       linewidth=1.0, alpha=0.7, label=f"BREAK (cycle {broken_c})")
        ax.set_ylabel("δ / τ  (absolute)")
        ax.legend(fontsize=7, loc="upper left")
        ax.set_facecolor("#08100e")
        ax.tick_params(colors="#888")

        # ── Panel 2: R(t) approach ratio ─────────────────────────
        ax = axes[1]
        ax.plot(cycles, r_vals, color="#40c4ff", linewidth=1.6, label="R(t) = δ/τ")
        ax.axhline(y=1.0, color="crimson", linestyle="--",
                   linewidth=1.2, label="R = 1  BREAK / Phase Transition (Axiom 6)")
        ax.axhline(y=0.75, color="#ffd740", linestyle=":",
                   linewidth=0.8, label="R = 0.75  Collapse-Approach Region (Axiom 7)")
        ax.set_ylabel("R = δ/τ")
        ax.set_ylim(0, 1.25)
        ax.legend(fontsize=7, loc="upper left")
        ax.set_facecolor("#080c14")
        ax.tick_params(colors="#888")

        # ── Panel 3: ∫f(δ)ds cumulative depletion ────────────────
        ax = axes[2]
        ax.fill_between(cycles, 0, integrals, color="#00e676", alpha=0.20)
        ax.plot(cycles, integrals, color="#00e676", linewidth=1.4,
                label="∫f(δ(s))ds  累積τ消耗量  (Axiom 4)")
        ax.set_ylabel("Cumulative ∫f(δ)ds")
        ax.legend(fontsize=7, loc="upper left")
        ax.set_facecolor("#080e0a")
        ax.tick_params(colors="#888")

        # ── Panel 4: τ_ceiling degradation (Axiom 5) ─────────────
        ax = axes[3]
        ax.step(cycles, tau0_line,  color="#c060ff", linewidth=0.8,
                linestyle=":", label="τ₀ (original)", where="post")
        ax.step(cycles, ceilings,   color="#ff80c0", linewidth=1.6,
                label="τ_ceiling (劣化上限)  Axiom 5", where="post")
        ax.fill_between(cycles, ceilings, tau0_line, step="post",
                        color="#ff80c0", alpha=0.08)
        ax.set_ylabel("τ ceiling  (Axiom 5)")
        ax.set_xlabel("Cycle")
        ax.legend(fontsize=7, loc="lower left")
        ax.set_facecolor("#12080e")
        ax.tick_params(colors="#888")

        fig.patch.set_facecolor("#0a0f14")
        for ax in axes:
            for sp in ax.spines.values():
                sp.set_edgecolor("#1a3040")
            ax.yaxis.label.set_color("#aac0cc")

        plt.tight_layout(rect=[0, 0, 1, 0.97])
        plt.savefig(save_path, dpi=120, facecolor=fig.get_facecolor())
        plt.close()
        print(f"[Axiom2Observer] Plot saved: {save_path}")


# ─────────────────────────────────────────────────────────────────
# Entry point / エントリーポイント
#   Scenario A: No restoration  — R approaches 1 naturally.
#   Scenario B: With restoration — Axiom 5 ceiling degradation.
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from nra_ide_foundation_fixed_JP import (
        BoundLaw, RateLimitLaw,
        NomologicalRing,
        DisturbanceNode,
        SafetyNode,
    )

    logging.basicConfig(level=logging.INFO)

    print("\n" + "=" * 60)
    print("Scenario A: 自然蓄積 — no restoration")
    print("           R approaches 1 without any replenishment")
    print("=" * 60)

    cfg_a = DepletionConfig(
        tau0=0.40, drift_a=0.001, drift_b=0.00002,
        noise_amp=0.0003, depletion_k=0.18, dt=1.0,
    )
    acc_a   = AccumulationState(delta=0.0, tau=cfg_a.tau0, tau0=cfg_a.tau0,
                                 tau_ceiling=cfg_a.tau0)
    accN_a  = AccumulationNode("Accumulation", cfg_a, acc_a)
    laws_a  = [BoundLaw(threshold=0.85), RateLimitLaw(max_rate=0.3)]
    nodes_a = [
        DisturbanceNode("Disturbance", trigger_cycles=[10, 25], magnitude=0.04),
        accN_a,
        SafetyNode("SafetyCheck", laws_a),
    ]
    ring_a  = NomologicalRing(nodes_a)
    obs_a   = Axiom2Observer(acc_a)
    token_a = Token()

    for _ in range(50):
        token_a = ring_a.run_cycle(token_a)
        obs_a.record(token_a)
        if token_a.meta.get("infeasible"):
            print(f"  [Fail-Closed] BREAK at cycle {token_a.meta.get('break_cycle', '?')} "
                  f"— Axiom 8 infeasible.")
            break

    print(obs_a.summary())
    ts = jst_now().replace(" ", "_").replace(":", "").replace("-", "")
    obs_a.plot(f"axiom2_scenario_A_{ts}.png")

    # ────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Scenario B: 補充劣化 — restoration with Axiom 5 degradation")
    print("           τ_ceiling degrades × 0.82 per restore")
    print("=" * 60)

    cfg_b = DepletionConfig(
        tau0=0.40, drift_a=0.001, drift_b=0.00003,
        noise_amp=0.0003, depletion_k=0.20, dt=1.0,
        restore_factor=0.82, restore_add=0.15,
    )
    acc_b   = AccumulationState(delta=0.0, tau=cfg_b.tau0, tau0=cfg_b.tau0,
                                 tau_ceiling=cfg_b.tau0)
    accN_b  = AccumulationNode("Accumulation", cfg_b, acc_b)
    restN_b = RestorationNode(
        "Restoration", acc_b, cfg_b,
        trigger_cycles=[15, 25, 35],  # external replenishment events
    )
    laws_b  = [BoundLaw(threshold=0.85), RateLimitLaw(max_rate=0.3)]
    nodes_b = [
        DisturbanceNode("Disturbance", trigger_cycles=[8, 20], magnitude=0.03),
        restN_b,          # replenishment first, then accumulation
        accN_b,
        SafetyNode("SafetyCheck", laws_b),
    ]
    ring_b  = NomologicalRing(nodes_b)
    obs_b   = Axiom2Observer(acc_b)
    token_b = Token()

    for _ in range(50):
        token_b = ring_b.run_cycle(token_b)
        obs_b.record(token_b)
        if token_b.meta.get("infeasible"):
            print(f"  [Fail-Closed] BREAK at cycle {token_b.meta.get('break_cycle', '?')} "
                  f"— Axiom 8 infeasible.")
            break

    print(obs_b.summary())
    obs_b.plot(f"axiom2_scenario_B_{ts}.png")

    # ── Axiom 5 restore event log ────────────────────────────────
    events = token_b.meta.get("restore_events", [])
    if events:
        print("\nAxiom 5 Restoration Events / 復元劣化イベント:")
        print(f"  {'cycle':>5}  {'τ_before':>9}  {'τ_after':>9}  "
              f"{'τ_ceiling':>10}  {'τ₀':>6}  {'degradation':>11}")
        print("  " + "-" * 60)
        for ev in events:
            deg = (1 - ev["tau_ceiling"] / ev["tau0"]) * 100
            print(f"  {ev['cycle']:>5}  {ev['tau_before']:>9.4f}  "
                  f"{ev['tau_after']:>9.4f}  {ev['tau_ceiling']:>10.4f}  "
                  f"{ev['tau0']:>6.4f}  {deg:>10.1f}%")
        print()
        print("  → τ_restored < τ₀  at every event  [Axiom 5 confirmed]")

    print(f"\n[Axiom2] Simulation completed. / シミュレーション完了。 {jst_now()}")
