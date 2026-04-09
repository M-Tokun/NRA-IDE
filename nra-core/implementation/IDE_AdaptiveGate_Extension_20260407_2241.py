# FILE: IDE_AdaptiveGate_Extension_20260407_2241.py
#　©M-Tokuni
#
# Title: NRA-IDE Adaptive Gate Extension — Dynamic k / Relative IDE / PD Damper
# NRA-IDE 適応型ゲート拡張 — 動的k / 相対座標IDE / PDダンパー
#
# Position / 位置づけ:
#   Upper-layer extension of nra_ide_foundation_fixed_JP.py
#   nra_ide_foundation_fixed_JP.py の上位拡張層
#   Does NOT overwrite normalized_quadratic_gate — acts as adapter
#   normalized_quadratic_gate を上書きしない — アダプター層として動作
#
# Author: M-Tokuni / NRA-IDE Project https://github.com/M-Tokun/NRA-IDE
# Date  : 2026-04-07 22:41 JST

from __future__ import annotations

import math
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Callable, Dict, List, Optional, Tuple, Any

# ─────────────────────────────────────────────────────────────────
# Dependency / 依存関係
#   Requires nra_ide_foundation_fixed_JP.py in the same directory.
#   同ディレクトリに nra_ide_foundation_fixed_JP.py が必要です。
# ─────────────────────────────────────────────────────────────────

from nra_ide_foundation_fixed_JP import (
    DynamicState,
    EnergyLedger,
    Token,
    Node,
    jst_now,
)


# ─────────────────────────────────────────────────────────────────
# AdaptiveGateConfig
#   All tunable parameters for the adaptive gate layer.
#   適応型ゲート層の全チューニングパラメータ。
# ─────────────────────────────────────────────────────────────────

@dataclass
class AdaptiveGateConfig:
    # --- Proposal 2 / 案2: Dynamic k ---
    k0  : float = 1.0   # Base knee value / 基準knee値
    beta: float = 0.1   # Velocity sensitivity / 速度感度

    # --- Proposal 1 / 案1: Relative IDE ---
    alpha: float = 0.5  # IDE flow gain toward target / 目標への大局流ゲイン

    # --- Proposal 3 / 案3: PD damper ---
    P: float = 2.0      # Proportional gain / 比例ゲイン
    D: float = 0.5      # Derivative gain / 微分ゲイン

    # --- Structural ---
    gamma: float = 0.5  # Viscous damping / 粘性減衰
    dt   : float = 0.01 # Time step / 時間ステップ

    def __post_init__(self) -> None:
        assert self.k0   > 0, "k0 must be positive / k0 は正値が必要"
        assert self.beta >= 0, "beta must be non-negative / beta は非負が必要"
        assert self.dt   > 0, "dt must be positive / dt は正値が必要"


# ─────────────────────────────────────────────────────────────────
# AdaptiveGateState
#   Continuous-domain state for the gate layer (separate from Token).
#   ゲート層専用の連続値状態（Token とは独立）。
# ─────────────────────────────────────────────────────────────────

@dataclass
class AdaptiveGateState:
    x      : float = 0.0   # Current position / 現在位置
    v      : float = 0.0   # Current velocity / 現在速度
    x_exact: float = 0.0   # Target position  / 目標位置
    v_exact: float = 0.0   # Target velocity  / 目標速度
    k_eff_history : List[float] = field(default_factory=list)
    accel_history : List[float] = field(default_factory=list)


# ─────────────────────────────────────────────────────────────────
# Core gate functions / コアゲート関数群
# ─────────────────────────────────────────────────────────────────

def adaptive_quadratic_gate(r: float, rdot: float, cfg: AdaptiveGateConfig) -> Tuple[float, float]:
    """
    Proposal 2: Compute dynamic k_eff and apply second-order residual gate.
    案2: 動的 k_eff を計算し2次残差ゲートを適用する。

    Returns (G_eff, k_eff).
    戻り値: (G_eff, k_eff)

    Extends normalized_quadratic_gate(correction, knee) in the core
    by making knee a function of relative velocity |rdot|.
    コアの normalized_quadratic_gate の knee を |rdot| の関数にした拡張版。
    """
    # Dynamic knee: larger when fast → classical layer silenced during rapid transitions
    # 動的knee: 高速時に大きくなる → 急速遷移中は古典層が沈黙
    k_eff = cfg.k0 * (1.0 + cfg.beta * abs(rdot))

    # Second-order residual gate (structure unchanged from core)
    # 2次残差ゲート（コアから構造変更なし）
    ratio = abs(r) / (k_eff + abs(r))
    g_eff = r * ratio

    return g_eff, k_eff


def ide_flow(r: float, cfg: AdaptiveGateConfig) -> float:
    """
    Proposal 1: Relative-coordinate IDE flow toward target.
    案1: 目標への相対座標 IDE 大局流。

    Original: F_IDE(x) = -0.5 * x  (fixed attractor at origin)
    原式    : F_IDE(x) = -0.5 * x  (原点への固定引力)

    Extended: F_IDE(r) = alpha * r  (attractor follows target)
    拡張後  : F_IDE(r) = alpha * r  (引力源が目標を追う)
    """
    return cfg.alpha * r


def pd_phi(rdot: float, r: float, cfg: AdaptiveGateConfig) -> float:
    """
    Proposal 3: PD damper enclosed inside G(r).
    案3: G(r) の内側に封じ込めた PD ダンパー。

    Active only when |r| is large (via gate gating), so explosion is avoided.
    |r| が大きいときのみ gate 越しに作動するため計算爆発を回避。
    """
    return cfg.P + cfg.D * rdot / (1.0 + abs(r))


def compute_acceleration(gs: AdaptiveGateState, cfg: AdaptiveGateConfig) -> Tuple[float, float]:
    """
    Integrated acceleration computation combining all three proposals.
    3案を統合した加速度計算。

    Governing equation / 支配方程式:
        d²x/dt² + γ·ẋ = F_IDE(r) + G_eff(r) · Φ(r, ṙ)

    Returns (acceleration, k_eff).
    戻り値: (acceleration, k_eff)
    """
    r    = gs.x_exact - gs.x      # Local residual / 局所残差
    rdot = gs.v_exact - gs.v      # Relative velocity / 相対速度

    f_ide          = ide_flow(r, cfg)                           # Proposal 1 / 案1
    g_eff, k_eff   = adaptive_quadratic_gate(r, rdot, cfg)      # Proposal 2 / 案2
    phi            = pd_phi(rdot, r, cfg)                       # Proposal 3 / 案3

    # Viscous damping applied to own velocity (divergence prevention)
    # 粘性減衰を自速度に適用（発散防止）
    accel = f_ide + g_eff * phi - cfg.gamma * gs.v

    return accel, k_eff


# ─────────────────────────────────────────────────────────────────
# AdaptiveGateNode
#   Node subclass — plugs directly into NomologicalRing.
#   Node サブクラス — NomologicalRing にそのまま接続できる。
#
#   Reads token.state.value as x.
#   Writes updated x back into token.state.value via velocity (no direct overwrite).
#   token.state.value を x として読み込む。
#   直接上書き禁止 — 速度を経由して token.state.value に返す。
# ─────────────────────────────────────────────────────────────────

class AdaptiveGateNode(Node):
    """
    Adapter layer between AdaptiveGate and NomologicalRing.
    AdaptiveGate と NomologicalRing の間のアダプター層。

    Design contract / 設計契約:
      - Never directly overwrites token.state.value
        token.state.value を直接上書きしない
      - Passes k_eff history into token.meta for observability
        観測のため k_eff 履歴を token.meta に記録
    """

    def __init__(
        self,
        name   : str,
        cfg    : AdaptiveGateConfig,
        target_fn: Optional[Callable[[int], Tuple[float, float]]] = None,
    ) -> None:
        """
        target_fn(cycle) -> (x_exact, v_exact)
        If None, x_exact tracks token.state.value * 0.5 (demo default).
        None の場合は token.state.value * 0.5 を目標とするデモ動作。
        """
        super().__init__(name)
        self.cfg       = cfg
        self.target_fn = target_fn or self._default_target
        self._gs       = AdaptiveGateState()

    @staticmethod
    def _default_target(cycle: int) -> Tuple[float, float]:
        # Demo: static target at 0.5, zero velocity
        # デモ: 静的目標 0.5、速度ゼロ
        return 0.5, 0.0

    def process(self, token: Token) -> Token:
        if token.meta.get("infeasible"):
            return self._record(token)

        cycle = token.meta["cycle"]

        # Sync gate state with token / トークンとゲート状態を同期
        self._gs.x       = token.state.value
        self._gs.v       = token.state.rate
        self._gs.x_exact, self._gs.v_exact = self.target_fn(cycle)

        # Compute adaptive acceleration / 適応加速度計算
        accel, k_eff = compute_acceleration(self._gs, self.cfg)

        # Update via velocity (no direct overwrite / 直接上書き禁止)
        new_v = self._gs.v + accel * self.cfg.dt
        new_x = min(1.0, max(0.0, self._gs.x + new_v * self.cfg.dt))

        token.state.rate  = new_v
        token.state.value = new_x
        token.state.record(new_x)

        # Tension from residual / 残差をテンションに反映
        r = self._gs.x_exact - new_x
        token.state.tension = abs(r)

        # Observability: store k_eff / 観測用 k_eff 記録
        token.meta.setdefault("k_eff_log", []).append(
            {"cycle": cycle, "k_eff": round(k_eff, 6), "accel": round(accel, 6)}
        )

        return self._record(token)


# ─────────────────────────────────────────────────────────────────
# AdaptiveGateObserver
#   Lightweight observer for gate-specific metrics.
#   ゲート固有メトリクス用の軽量オブザーバー。
# ─────────────────────────────────────────────────────────────────

class AdaptiveGateObserver:
    def __init__(self) -> None:
        self.records: List[Dict[str, Any]] = []

    def record(self, token: Token) -> None:
        k_log  = token.meta.get("k_eff_log", [])
        latest = k_log[-1] if k_log else {"k_eff": 0.0, "accel": 0.0}
        self.records.append({
            "cycle"  : token.meta["cycle"],
            "value"  : token.state.value,
            "rate"   : token.state.rate,
            "tension": token.state.tension,
            "k_eff"  : latest["k_eff"],
            "accel"  : latest["accel"],
        })

    def summary(self) -> str:
        lines = [
            "cycle | value  | rate   | tension | k_eff  | accel",
            "------|--------|--------|---------|--------|-------",
        ]
        for r in self.records:
            lines.append(
                f"{r['cycle']:>5} | {r['value']:>6.3f} | {r['rate']:>6.3f} | "
                f"{r['tension']:>7.4f} | {r['k_eff']:>6.4f} | {r['accel']:>7.4f}"
            )
        return "\n".join(lines)

    def plot(self, save_path: str) -> None:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        cycles  = [r["cycle"]   for r in self.records]
        values  = [r["value"]   for r in self.records]
        k_effs  = [r["k_eff"]   for r in self.records]
        tension = [r["tension"] for r in self.records]
        accels  = [r["accel"]   for r in self.records]

        fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
        fig.suptitle("NRA-IDE Adaptive Gate — Dynamic k Extension", fontsize=12)

        axes[0].plot(cycles, values, marker="o", color="steelblue", label="state.value")
        axes[0].axhline(y=0.5, color="seagreen", linestyle="--", label="target (0.5)")
        axes[0].set_ylabel("Value")
        axes[0].legend(fontsize=8)

        axes[1].plot(cycles, k_effs, color="darkorange", marker="s", label="k_eff (dynamic)")
        axes[1].plot(cycles, tension, color="crimson", linestyle=":", label="tension |r|")
        axes[1].set_ylabel("k_eff / Tension")
        axes[1].legend(fontsize=8)

        axes[2].plot(cycles, accels, color="mediumpurple", marker="^", label="acceleration")
        axes[2].axhline(y=0, color="gray", linestyle="--", linewidth=0.8)
        axes[2].set_xlabel("Cycle")
        axes[2].set_ylabel("Acceleration")
        axes[2].legend(fontsize=8)

        plt.tight_layout()
        plt.savefig(save_path, dpi=120)
        plt.close()
        print(f"[AdaptiveGate] Plot saved: {save_path}")


# ─────────────────────────────────────────────────────────────────
# Entry point / エントリーポイント
#   Demo: AdaptiveGateNode inserted into existing NomologicalRing.
#   デモ: 既存 NomologicalRing に AdaptiveGateNode を差し込む。
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from nra_ide_foundation_fixed_JP import (
        BoundLaw, RateLimitLaw,
        DisturbanceNode, SafetyNode,
        NomologicalRing,
    )

    logging.basicConfig(level=logging.INFO)

    cfg = AdaptiveGateConfig(
        k0=1.0, beta=0.15, alpha=0.5,
        P=2.0, D=0.4, gamma=0.5, dt=0.05,
    )

    # Target: ramp up to 0.7 after cycle 10 / サイクル10以降に目標0.7へランプ
    def dynamic_target(cycle: int) -> Tuple[float, float]:
        x_t = 0.5 if cycle < 10 else 0.7
        return x_t, 0.0

    laws = [BoundLaw(threshold=0.85), RateLimitLaw(max_rate=0.25)]

    nodes = [
        DisturbanceNode("Disturbance", trigger_cycles=[5, 14], magnitude=0.3),
        AdaptiveGateNode("AdaptiveGate", cfg, target_fn=dynamic_target),
        SafetyNode("SafetyCheck", laws),
    ]

    ring    = NomologicalRing(nodes)
    obs     = AdaptiveGateObserver()
    token   = Token()

    for _ in range(25):
        token = ring.run_cycle(token)
        obs.record(token)

    print(obs.summary())

    PLOT_FILE = f"adaptive_gate_plot_{jst_now().replace(' ', '_').replace(':', '')}.png"
    obs.plot(PLOT_FILE)
    print(f"[AdaptiveGate] Simulation completed. / シミュレーション完了。")
