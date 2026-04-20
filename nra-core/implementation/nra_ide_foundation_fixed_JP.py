# FILE: nra_ide_foundation_fixed_JP.py
# Title: NRA-IDE Foundation - DynamicState Core with Extension Reservations [fixed]
# 「厚み + ゆらぎ×2 ver.1.0 安定版」
# Author: M-Tokuni / 著作権
# Date: 2026-03-11 05:45 JST

# [FIX LOG]
#  - PLOT Path: 固定パスを削除し、相対パス "nra_foundation_plot.png" に修正
#  - BoundLaw.correct(): E_stored を正規化値の上書きから差分累積に修正
#  - ObservationLog.record(): violated判定を全違反対象に拡張

from __future__ import annotations

import math
import copy
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple

# ─────────────────────────────────────────────
# ユーティリティ
# ─────────────────────────────────────────────

def jst_now() -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")


# ─────────────────────────────────────────────
# DynamicState（正規化状態量・入れ物）
# ─────────────────────────────────────────────

@dataclass
class DynamicState:
    """
    媒質非依存の正規化状態量。value ∈ [0.0, 1.0]。
    """
    value  : float = 0.0
    rate   : float = 0.0
    buffer : float = 0.0
    tension: float = 0.0
    history: List[float] = field(default_factory=list)

    # ── [EXT: pressure] ──────────────────────────────
    pressure: float = 0.0   # [EXT: pressure] +0.0（未使用）

    # ── [EXT: viscosity] ─────────────────────────────
    viscosity_factor: float = 1.0   # [EXT: viscosity] ×1（無効）

    # ── [EXT: plasticity] ────────────────────────────
    plasticity_factor: float = 1.0  # [EXT: plasticity] ×1（無効）

    def record(self, v: float) -> None:
        self.history.append(v)

    def peak(self) -> float:
        return max(self.history) if self.history else 0.0

    def normalize(self, raw: float, raw_max: float) -> float:
        return min(1.0, max(0.0, raw / raw_max)) if raw_max > 0 else 0.0

    def denormalize(self, norm: float, raw_max: float) -> float:
        return norm * raw_max


# ─────────────────────────────────────────────
# EnergyLedger（エネルギー収支帳）
# ─────────────────────────────────────────────

@dataclass
class EnergyLedger:
    E_in       : float = 0.0   # 投入エネルギー
    E_stored   : float = 0.0   # 蓄積エネルギー
    E_dissipated: float = 0.0  # 散逸エネルギー
    E_thermal  : float = 0.0   # [EXT: thermal_dissipation] +0.0

    def balance(self) -> float:
        return self.E_in - (self.E_stored + self.E_dissipated + self.E_thermal)

    def is_conserved(self, tol: float = 1e-6) -> bool:
        return abs(self.balance()) < tol


# ─────────────────────────────────────────────
# Token（情報単位）
# ─────────────────────────────────────────────

@dataclass
class Token:
    state  : DynamicState = field(default_factory=DynamicState)
    meta   : Dict[str, Any] = field(default_factory=dict)
    ledger : EnergyLedger = field(default_factory=EnergyLedger)
    history: List[Tuple[str, DynamicState]] = field(default_factory=list, repr=False)

    def __post_init__(self):
        self.meta.setdefault("cycle", 0)
        self.meta.setdefault("created_at", jst_now())
        self.meta.setdefault("violated_laws", [])
        self.meta.setdefault("infeasible", False)

    def snapshot(self, node_name: str) -> None:
        self.history.append((node_name, copy.deepcopy(self.state)))

    def increment_cycle(self) -> None:
        self.meta["cycle"] += 1

    def log_violation(self, law_name: str) -> None:
        self.meta["violated_laws"].append({
            "law": law_name,
            "cycle": self.meta["cycle"],
            "value": self.state.value,
            "tension": self.state.tension,
        })

    def __repr__(self) -> str:
        s = self.state
        return (f"Token(cycle={self.meta['cycle']}, "
                f"value={s.value:.3f}, rate={s.rate:.3f}, "
                f"buffer={s.buffer:.3f}, tension={s.tension:.3f})")


# ─────────────────────────────────────────────
# Law（制約・力学則）
# ─────────────────────────────────────────────

class Law(ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def check(self, token: Token) -> bool: ...

    @abstractmethod
    def tension(self, token: Token) -> float: ...

    @abstractmethod
    def correct(self, token: Token) -> Optional[Token]: ...


class BoundLaw(Law):
    def __init__(self, threshold: float = 0.8, k: float = 1.0, margin: float = 0.05):
        self.threshold = threshold
        self.k         = k
        self.margin    = margin
        self._viscosity_coupling: float = 0.0  # [EXT]
        self._brittle_factor: float = 1.0      # [EXT]

    def check(self, token: Token) -> bool:
        return token.state.value <= self.threshold

    def tension(self, token: Token) -> float:
        excess = max(0.0, token.state.value - self.threshold)
        T = self.k * excess
        T += self._viscosity_coupling
        T *= self._brittle_factor
        return T

    def correct(self, token: Token) -> Optional[Token]:
        T = self.tension(token)
        if T <= 0: return token
        excess = token.state.value - self.threshold
        target = self.threshold - self.margin
        token.state.buffer += excess
        token.state.value   = max(0.0, target)
        token.state.tension = T
        token.ledger.E_dissipated += excess
        token.ledger.E_stored     += max(0.0, target) - (token.state.value - excess)
        token.ledger.E_stored      = max(0.0, token.ledger.E_stored)
        return token


class RateLimitLaw(Law):
    def __init__(self, max_rate: float = 0.2):
        self.max_rate = max_rate
        self._rate_asymmetry: float = 1.0  # [EXT]

    def check(self, token: Token) -> bool:
        return abs(token.state.rate) <= self.max_rate * self._rate_asymmetry

    def tension(self, token: Token) -> float:
        excess_rate = abs(token.state.rate) - self.max_rate
        return max(0.0, excess_rate)

    def correct(self, token: Token) -> Optional[Token]:
        if self.check(token): return token
        sign = 1.0 if token.state.rate >= 0 else -1.0
        token.state.buffer += abs(token.state.rate) - self.max_rate
        token.state.rate    = sign * self.max_rate
        return token


# ─────────────────────────────────────────────
# Node（処理単位）
# ─────────────────────────────────────────────

class Node(ABC):
    def __init__(self, name: str):
        self.name = name
        self._logger = logging.getLogger(f"NRA.{name}")

    @abstractmethod
    def process(self, token: Token) -> Token: ...

    def _record(self, token: Token) -> Token:
        token.snapshot(self.name)
        return token


class SafetyNode(Node):
    def __init__(self, name: str, laws: List[Law]):
        super().__init__(name)
        self.laws = laws

    def process(self, token: Token) -> Token:
        for law in self.laws:
            T = law.tension(token)
            if T > 0: token.state.tension = T
            if not law.check(token):
                token.log_violation(law.name)
                result = law.correct(token)
                if result is None:
                    token.meta["infeasible"] = True
                    return self._record(token)
                token = result
        return self._record(token)


class DynamicsNode(Node):
    def __init__(self, name: str, transition_fn: Optional[Callable] = None):
        super().__init__(name)
        self.transition_fn = transition_fn or self._default_transition

    @staticmethod
    def _default_transition(state: DynamicState, cycle: int) -> DynamicState:
        cost = 0.1
        cost *= state.viscosity_factor
        cost += state.pressure * 0.0
        new_rate  = cost
        new_value = min(1.0, state.value + cost)
        state.rate  = new_rate
        state.value = new_value
        state.record(new_value)
        return state

    def process(self, token: Token) -> Token:
        if token.meta.get("infeasible"): return self._record(token)
        token.state = self.transition_fn(token.state, token.meta["cycle"])
        token.ledger.E_in += token.state.rate
        return self._record(token)


class DisturbanceNode(Node):
    def __init__(self, name: str, trigger_cycles: List[int], magnitude: float = 0.5):
        super().__init__(name)
        self.trigger_cycles = trigger_cycles
        self.magnitude = magnitude

    def process(self, token: Token) -> Token:
        if token.meta["cycle"] in self.trigger_cycles:
            prev = token.state.value
            token.state.value = min(1.0, token.state.value + self.magnitude)
            token.state.rate   = token.state.value - prev
            token.ledger.E_in += self.magnitude
            token.state.record(token.state.value)
        return self._record(token)


# ─────────────────────────────────────────────
# NomologicalRing（律環エンジン）
# ─────────────────────────────────────────────

class NomologicalRing:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes

    def run_cycle(self, token: Token) -> Token:
        for node in self.nodes:
            token = node.process(token)
            if token.meta.get("infeasible"): break
        token.increment_cycle()
        return token


# ─────────────────────────────────────────────
# ObservationLog（観測層）
# ─────────────────────────────────────────────

class ObservationLog:
    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def record(self, token: Token) -> None:
        s = token.state
        self.records.append({
            "cycle"    : token.meta["cycle"],
            "value"    : s.value,
            "rate"     : s.rate,
            "buffer"   : s.buffer,
            "tension"  : s.tension,
            "E_in"     : token.ledger.E_in,
            "E_stored" : token.ledger.E_stored,
            "E_dissip" : token.ledger.E_dissipated,
            "violated" : any(v["cycle"] == token.meta["cycle"] - 1 for v in token.meta["violated_laws"]),
        })

    def plot(self, save_path: str, threshold: float = 0.8) -> None:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        cycles  = [r["cycle"] for r in self.records]
        values  = [r["value"]  for r in self.records]
        buffers = [r["buffer"] for r in self.records]
        tension = [r["tension"] for r in self.records]

        fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        axes[0].plot(cycles, values, marker="o", color="steelblue", label="state.value")
        axes[0].axhline(y=threshold, color="crimson", linestyle="--", label="threshold")
        axes[0].set_ylabel("Value")
        axes[0].legend(fontsize=8)

        axes[1].fill_between(cycles, 0, buffers, color="dodgerblue", alpha=0.3, label="buffer")
        axes[1].plot(cycles, tension, color="crimson", label="tension")
        axes[1].set_ylabel("Buffer/Tension")
        axes[1].legend(fontsize=8)

        e_in = [r["E_in"] for r in self.records]
        axes[2].plot(cycles, e_in, color="gold", label="E_in")
        axes[2].set_xlabel("Cycle")
        axes[2].set_ylabel("Energy")
        axes[2].legend(fontsize=8)

        plt.tight_layout()
        plt.savefig(save_path, dpi=120)
        plt.close()


# ─────────────────────────────────────────────
# エントリーポイント
# ─────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    laws = [BoundLaw(threshold=0.8), RateLimitLaw(max_rate=0.2)]
    nodes = [
        DisturbanceNode("Disturbance", trigger_cycles=[5, 14], magnitude=0.5),
        DynamicsNode("Dynamics"),
        SafetyNode("SafetyCheck", laws),
    ]

    ring = NomologicalRing(nodes)
    obs  = ObservationLog()
    token = Token()

    for _ in range(20):
        token = ring.run_cycle(token)
        obs.record(token)

    # 固定パスを排除し、相対パスで保存するように修正しました
    PLOT_FILE = "nra_foundation_plot_2026-02-20_2355.png"
    obs.plot(PLOT_FILE, threshold=0.8)
    print(f"Simulation completed. Plot saved as {PLOT_FILE}")
