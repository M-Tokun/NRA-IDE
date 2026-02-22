# FILE: nra_ide_foundation_fixd.py
# Title: NRA-IDE Foundation - DynamicState Core with Extension Reservations [fixed]
# 「厚み　+　ゆらぎ×2　ver.1.0 安定版」
 Author: M-Tokuni / 著作権
 Date: 2026-02-21 04:52 JST

# [FIX LOG]
  - BoundLaw.correct(): E_stored を正規化値の上書きから差分累積に修正
  - ObservationLog.record(): violated判定を全違反対象に拡張（[-1]のみ → any()）

# [既知の制約 / EXT予約]
  - E_bal（エネルギー収支残差）は補正フェーズのみ追跡のため正値が残る
     完全な保存則閉合には E_stored の全フェーズ統合が必要
     → [EXT: full_energy_closure] として次バージョンで対応予定

# 設計思想：
   DynamicState を「入れ物」として固定。
   媒質・対象が変わっても同じ入れ物を使う。
   各Law は遷移関数（どう動かすか）として差し替える。

# 拡張予約について：
   現状で未実装の力学項は × 1 または + 0.0 として明示的に残す。
   コメントに「[EXT: 拡張名]」を付与——次回実装の接続点。
   消さない、省略しない、平均化しない。

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

    全ての力学計算はこの入れ物を通す。
    媒質の違いは Law（遷移関数）で表現し、入れ物の形は変えない。

    フィールド説明：
      value   : 現在の状態値（0=完全安定、1=限界点）
      rate    : 変化率 dv/dt（速度）
      buffer  : 散逸待ちエネルギー（誤差の逃げ場。消去しない）
      tension : 制約からの距離が生む復元力（張力）
      history : 瞬時値の履歴（突出記録。平均化しない）
    """
    value  : float = 0.0
    rate   : float = 0.0
    buffer : float = 0.0
    tension: float = 0.0
    history: List[float] = field(default_factory=list)

    # ── [EXT: pressure] ──────────────────────────────
    # 圧力項（人体・流体系）
    # 現状：未使用のため + 0.0
    # 実装時：pressure: float = 0.0 を追加し、
    #   TensionLaw.compute() 内で
    #   tension += pressure_coefficient * self.pressure
    pressure: float = 0.0   # [EXT: pressure] +0.0（未使用）

    # ── [EXT: viscosity] ─────────────────────────────
    # 粘性係数（変化率を抑制。急激な突出を物理的に不可能にする）
    # 現状：×1（乗算なので無効化）
    # 実装時：rate_limited = rate * viscosity_factor (0 < v_factor <= 1)
    viscosity_factor: float = 1.0   # [EXT: viscosity] ×1（無効）

    # ── [EXT: plasticity] ────────────────────────────
    # 塑性変形係数（超過後に基準値自体がずれる。履歴依存）
    # 現状：×1（基準値変化なし）
    # 実装時：threshold_shift += plasticity * max(0, value - threshold)
    plasticity_factor: float = 1.0  # [EXT: plasticity] ×1（無効）

    def record(self, v: float) -> None:
        """瞬時値をそのまま記録（平均化しない）"""
        self.history.append(v)

    def peak(self) -> float:
        """突出値（最大瞬時値）"""
        return max(self.history) if self.history else 0.0

    def normalize(self, raw: float, raw_max: float) -> float:
        """次元付き物理量を [0,1] に正規化"""
        return min(1.0, max(0.0, raw / raw_max)) if raw_max > 0 else 0.0

    def denormalize(self, norm: float, raw_max: float) -> float:
        """[0,1] を次元付き物理量に逆変換"""
        return norm * raw_max


# ─────────────────────────────────────────────
# EnergyLedger（エネルギー収支帳）
# ─────────────────────────────────────────────

@dataclass
class EnergyLedger:
    """
    エネルギー保存則の記録係。
    E_in = E_stored + E_dissipated（保存則）を毎サイクル検証。

    誤差はbufferへ逃がす（消去しない）。
    """
    E_in       : float = 0.0   # 投入エネルギー（外乱・行動コスト）
    E_stored   : float = 0.0   # 系に蓄積されたエネルギー
    E_dissipated: float = 0.0  # 散逸エネルギー（buffer経由で放出）

    # ── [EXT: thermal_dissipation] ───────────────────
    # 熱散逸（高速変動時の損失。現状 +0.0）
    E_thermal  : float = 0.0   # [EXT: thermal_dissipation] +0.0

    def balance(self) -> float:
        """保存則の誤差 = E_in - (E_stored + E_dissipated)"""
        return self.E_in - (self.E_stored + self.E_dissipated + self.E_thermal)

    def is_conserved(self, tol: float = 1e-6) -> bool:
        return abs(self.balance()) < tol


# ─────────────────────────────────────────────
# Token（情報単位）
# ─────────────────────────────────────────────

@dataclass
class Token:
    """
    環を循環するデータパケット。
    state: DynamicState（入れ物）
    meta : システム管理情報
    ledger: エネルギー収支
    history: 観測ログ（事後記録のみ）
    """
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
    """
    DynamicState に作用する力学則の抽象基底。

    check()  : 制約を満たしているか
    tension(): 制約からの距離に比例する復元力（張力）
    correct(): 張力を使って状態を修正。誤差はbufferへ。
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def check(self, token: Token) -> bool: ...

    @abstractmethod
    def tension(self, token: Token) -> float:
        """
        復元力の計算。
        距離（超過量）が力を生む——距離から力を導出しない原則の
        「導出」とはここでは「距離そのものを力とする」ことを指す。
        比例係数 k を介した変換は許容。
        """
        ...

    @abstractmethod
    def correct(self, token: Token) -> Optional[Token]:
        """
        張力を使って修正。超過エネルギーはbufferへ逃がす（消去しない）。
        修正不能 → None を返す（不能性）。
        """
        ...


class BoundLaw(Law):
    """
    汎用上限制約。
    DynamicState.value が threshold を超えないことを保証。

    張力：T = k * max(0, value - threshold)
    修正：value を threshold - margin に引き戻し、超過分を buffer へ
    """

    def __init__(
        self,
        threshold: float = 0.8,    # 上限（正規化値）
        k        : float = 1.0,    # 張力係数
        margin   : float = 0.05,   # クリップマージン（次サイクルの安全圏）
    ):
        self.threshold = threshold
        self.k         = k
        self.margin    = margin

        # ── [EXT: viscosity_coupling] ─────────────────
        # 張力計算に粘性を結合（変化率が大きいほど抵抗を追加）
        # 現状：+0.0
        # 実装時：T += viscosity * abs(token.state.rate)
        self._viscosity_coupling: float = 0.0  # [EXT: viscosity_coupling] +0.0

        # ── [EXT: brittle_threshold] ──────────────────
        # 脆性破砕点（この値を超えたら張力が急激に解放）
        # 現状：×1（通常の線形張力のまま）
        # 実装時：if value > brittle_threshold: T *= brittle_amplifier
        self._brittle_factor: float = 1.0      # [EXT: brittle_threshold] ×1

    def check(self, token: Token) -> bool:
        return token.state.value <= self.threshold

    def tension(self, token: Token) -> float:
        excess = max(0.0, token.state.value - self.threshold)
        T = self.k * excess
        T += self._viscosity_coupling          # [EXT: viscosity_coupling]
        T *= self._brittle_factor              # [EXT: brittle_threshold]
        return T

    def correct(self, token: Token) -> Optional[Token]:
        T = self.tension(token)
        if T <= 0:
            return token

        excess = token.state.value - self.threshold
        target = self.threshold - self.margin

        # 超過エネルギーをbufferへ逃がす（消去しない）
        token.state.buffer += excess
        token.state.value   = max(0.0, target)
        token.state.tension = T

        # エネルギー収支に記録
        # FIX: E_stored は差分の累積（正規化値の上書き → 誤差発生のため修正）
        token.ledger.E_dissipated += excess
        token.ledger.E_stored     += max(0.0, target) - (token.state.value - excess)
        token.ledger.E_stored      = max(0.0, token.ledger.E_stored)  # 下限保護

        return token


class RateLimitLaw(Law):
    """
    変化率制約（粘性媒質モデルの基礎）。
    rate が max_rate を超えないことを保証。

    急激な突出を物理的に不可能にする——人体・土壌水分系向け。
    鉱物・病害虫系では無効化（max_rate=inf）して使う。
    """

    def __init__(self, max_rate: float = 0.2):
        self.max_rate = max_rate

        # ── [EXT: rate_asymmetry] ─────────────────────
        # 増加方向と減少方向で max_rate を非対称に設定
        # 現状：×1（対称）
        # 実装時：max_rate_up / max_rate_down を独立に設定
        self._rate_asymmetry: float = 1.0  # [EXT: rate_asymmetry] ×1

    def check(self, token: Token) -> bool:
        return abs(token.state.rate) <= self.max_rate * self._rate_asymmetry

    def tension(self, token: Token) -> float:
        excess_rate = abs(token.state.rate) - self.max_rate
        return max(0.0, excess_rate)

    def correct(self, token: Token) -> Optional[Token]:
        if self.check(token):
            return token
        sign = 1.0 if token.state.rate >= 0 else -1.0
        # 超過した変化率はbufferへ蓄積
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
    """推論ダイオード兼安全検証ノード。全Lawを適用。"""

    def __init__(self, name: str, laws: List[Law]):
        super().__init__(name)
        self.laws = laws

    def process(self, token: Token) -> Token:
        for law in self.laws:
            T = law.tension(token)
            if T > 0:
                token.state.tension = T
            if not law.check(token):
                self._logger.warning(f"違反: {law.name} | T={T:.4f} | v={token.state.value:.3f}")
                token.log_violation(law.name)
                result = law.correct(token)
                if result is None:
                    token.meta["infeasible"] = True
                    self._logger.error(f"不能性: {law.name}")
                    return self._record(token)
                token = result
        return self._record(token)


class DynamicsNode(Node):
    """
    状態遷移ノード。
    transition_fn: (DynamicState, cycle) -> DynamicState
    として外部注入可能。媒質ごとに差し替える。
    """

    def __init__(
        self,
        name: str,
        transition_fn: Optional[Callable] = None,
        raw_max: float = 100.0,
    ):
        super().__init__(name)
        self.transition_fn = transition_fn or self._default_transition
        self.raw_max = raw_max

    @staticmethod
    def _default_transition(state: DynamicState, cycle: int) -> DynamicState:
        """
        デフォルト遷移：線形加算（×1媒質係数・+0粘性項）

        compute相当の操作として value を +0.1 変化させる。
        実環境では transition_fn を差し替えて使う。
        """
        cost = 0.1   # 基本コスト

        # ── [EXT: viscosity] ─────────────────────────
        # 粘性項：rate の変化を抑制
        # 現状：×1（抑制なし）
        # 実装時：cost *= state.viscosity_factor
        cost *= state.viscosity_factor   # [EXT: viscosity] ×1

        # ── [EXT: pressure] ──────────────────────────
        # 圧力項：追加コスト
        # 現状：+0.0
        # 実装時：cost += state.pressure * pressure_coefficient
        cost += state.pressure * 0.0     # [EXT: pressure] +0.0

        new_rate  = cost
        new_value = min(1.0, state.value + cost)
        state.rate  = new_rate
        state.value = new_value
        state.record(new_value)          # 瞬時値記録（平均化しない）
        return state

    def process(self, token: Token) -> Token:
        if token.meta.get("infeasible"):
            return self._record(token)
        token.state = self.transition_fn(token.state, token.meta["cycle"])
        # エネルギー収支：投入量を記録
        token.ledger.E_in += token.state.rate
        return self._record(token)


class DisturbanceNode(Node):
    """
    外乱注入ノード。
    正規化値で指定（magnitude ∈ [0, 1]）。
    """

    def __init__(
        self,
        name: str,
        trigger_cycles: List[int],
        magnitude: float = 0.5,
    ):
        super().__init__(name)
        self.trigger_cycles = trigger_cycles
        self.magnitude = magnitude

    def process(self, token: Token) -> Token:
        if token.meta["cycle"] in self.trigger_cycles:
            self._logger.warning(
                f"外乱注入 [cycle={token.meta['cycle']}]: +{self.magnitude}"
            )
            prev = token.state.value
            token.state.value = min(1.0, token.state.value + self.magnitude)
            token.state.rate   = token.state.value - prev
            token.ledger.E_in += self.magnitude   # エネルギー収支に計上
            token.state.record(token.state.value)
        return self._record(token)


# ─────────────────────────────────────────────
# NomologicalRing（律環エンジン）
# ─────────────────────────────────────────────

class NomologicalRing:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self._logger = logging.getLogger("NRA.Ring")

    def run_cycle(self, token: Token) -> Token:
        self._logger.debug(f"=== Cycle {token.meta['cycle']} ===")
        for node in self.nodes:
            token = node.process(token)
            if token.meta.get("infeasible"):
                self._logger.warning(f"不能性 @ {node.name}")
                break
        token.increment_cycle()
        return token

    def run(self, token: Token, max_cycles: int = 20) -> Token:
        for _ in range(max_cycles):
            token = self.run_cycle(token)
        return token


# ─────────────────────────────────────────────
# ObservationLog（観測層）
# ─────────────────────────────────────────────

class ObservationLog:
    """処理に関与しない純粋な観測・可視化層"""

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
            "peak"     : s.peak(),
            "E_in"     : token.ledger.E_in,
            "E_stored" : token.ledger.E_stored,
            "E_dissip" : token.ledger.E_dissipated,
            "conserved": token.ledger.is_conserved(),
            # FIX: 同サイクル内の複数違反を全て検出（[-1]だけ参照する問題を修正）
            "violated" : any(
                v["cycle"] == token.meta["cycle"] - 1
                for v in token.meta["violated_laws"]
            ),
        })

    def print_table(self) -> None:
        print(f"\n{'cycle':>5} | {'value':>6} | {'rate':>6} | "
              f"{'buffer':>7} | {'tension':>7} | {'peak':>6} | "
              f"{'E_bal':>6} | status")
        print("-" * 72)
        for r in self.records:
            bal = r["E_in"] - r["E_stored"] - r["E_dissip"]
            viol = "⚠️ " if r["violated"] else "✅"
            print(
                f"{r['cycle']:5d} | {r['value']:6.3f} | {r['rate']:+6.3f} | "
                f"{r['buffer']:7.3f} | {r['tension']:7.4f} | {r['peak']:6.3f} | "
                f"{bal:+6.4f} | {viol}"
            )

    def plot(self, save_path: str, threshold: float = 0.8) -> None:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        cycles  = [r["cycle"] for r in self.records]
        values  = [r["value"]  for r in self.records]
        buffers = [r["buffer"] for r in self.records]
        tension = [r["tension"] for r in self.records]

        fig, axes = plt.subplots(3, 1, figsize=(13, 10), sharex=True)

        # ── 上段：state.value vs threshold ──
        axes[0].plot(cycles, values, marker="o", color="steelblue",
                     linewidth=2, label="state.value")
        axes[0].axhline(y=threshold, color="crimson", linestyle="--",
                        linewidth=1.5, label=f"threshold={threshold}")
        axes[0].fill_between(cycles, 0, threshold, color="limegreen",
                             alpha=0.07, label="Safe zone")
        for r in self.records:
            if r["violated"]:
                axes[0].axvspan(r["cycle"]-0.4, r["cycle"]+0.4,
                                color="orange", alpha=0.2)
        axes[0].set_ylabel("Normalized Value")
        axes[0].set_title("NRA-IDE Foundation: DynamicState Dynamics")
        axes[0].legend(fontsize=8)
        axes[0].grid(True, alpha=0.3)

        # ── 中段：buffer（誤差の逃げ場）と tension ──
        axes[1].fill_between(cycles, 0, buffers, color="dodgerblue",
                             alpha=0.4, label="buffer (dissipated energy)")
        axes[1].plot(cycles, tension, color="crimson", linewidth=1.5,
                     label="tension (restoring force)")
        axes[1].set_ylabel("Buffer / Tension")
        axes[1].legend(fontsize=8)
        axes[1].grid(True, alpha=0.3)

        # ── 下段：エネルギー収支 ──
        e_in    = [r["E_in"]    for r in self.records]
        e_store = [r["E_stored"] for r in self.records]
        e_diss  = [r["E_dissip"] for r in self.records]
        axes[2].plot(cycles, e_in,    color="gold",      linewidth=1.5, label="E_in")
        axes[2].plot(cycles, e_store, color="steelblue", linewidth=1.5, label="E_stored")
        axes[2].plot(cycles, e_diss,  color="tomato",    linewidth=1.5, label="E_dissipated")
        axes[2].set_xlabel("Cycle")
        axes[2].set_ylabel("Energy")
        axes[2].legend(fontsize=8)
        axes[2].grid(True, alpha=0.3)
        axes[2].set_xticks(cycles)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        print(f"\n📊 プロット保存: {save_path}")
        plt.close()


# ─────────────────────────────────────────────
# エントリーポイント（動作確認）
# ─────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s | %(levelname)s | %(message)s",
    )

    print(f"=== NRA-IDE Foundation [{jst_now()}] ===\n")

    # 制約（デフォルト設定）
    laws = [
        BoundLaw(threshold=0.8, k=1.0, margin=0.05),
        RateLimitLaw(max_rate=0.2),
    ]

    # ノード構成（最小構成）
    nodes = [
        DisturbanceNode("Disturbance", trigger_cycles=[5, 14], magnitude=0.5),
        DynamicsNode("Dynamics"),
        SafetyNode("SafetyCheck", laws),
    ]

    ring = NomologicalRing(nodes)
    obs  = ObservationLog()

    token = Token()   # DynamicState デフォルト値から開始

    for _ in range(20):
        token = ring.run_cycle(token)
        obs.record(token)

    print(f"最終トークン: {token}")
    print(f"エネルギー保存: {token.ledger.is_conserved(tol=1e-4)}")
    obs.print_table()

    PLOT = "/home/claude/nra_foundation_plot_2026-02-20_2355.png"
    obs.plot(PLOT, threshold=0.8)
    print(f"\n=== 完了 [{jst_now()}] ===")
