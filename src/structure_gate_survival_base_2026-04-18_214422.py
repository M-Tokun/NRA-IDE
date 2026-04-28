# structure_gate_survival_base_2026-04-18_214422.py
# Timestamp: 2026-04-18 21:44:22 JST
#
# NRA-IDE Survival-Base redesign (Option B)
# 設計原則 / Design principle:
#
#   構造という現実・事実の上以外はこの世界は成立できない。
#   Nothing in this world can exist outside structural reality and fact.
#
# Layer structure / 層構造:
#   Layer 0 : Survival base       生存基底   ← foundation of all judgment
#   Layer 1 : Structural signals  構造信号   ← existing gate logic
#   Layer 2+: Language / reason   言語・理性  ← current AI operates here only
#
# Honesty policy / 誠実方針:
#   Layer 0 aspects that cannot be assessed are declared as INABILITY.
#   評価不能なLayer0側面はINABILITYとして明示する。近似で埋めない。
#
# ring_history: append-only. No deletion. No overwrite.
# ring_history: 追記専用。削除なし。上書きなし。
#
# G(r) = r·|r| / (k + |r|) retained from NRA-IDE Option A.
# G(r) = r·|r| / (k + |r|) はNRA-IDE Option Aから継承。

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple
import math


# ============================================================
# Enums / 列挙型
# ============================================================

class GateStatus(str, Enum):
    # Normal pass / 通常通過
    PERMIT = "PERMIT"
    # Pass with human review / 人確認付き通過
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    # Structural stop / 構造停止
    FAIL_CLOSED = "FAIL_CLOSED"
    # Cannot assess — structurally honest / 評価不能—構造的誠実
    INABILITY = "INABILITY"


# ============================================================
# Layer 0: Survival base / 生存基底層
# ============================================================

@dataclass(frozen=True)
class SurvivalLayer:
    """
    Layer 0 — Survival base / 生存基底層

    All scores: 0.0 = critically depleted, 1.0 = fully satisfied
    全スコア: 0.0 = 臨界枯渇, 1.0 = 完全充足

    This layer is checked before any logical or structural judgment.
    この層は論理・構造判定より先に確認される。

    inability_flags: aspects that cannot currently be assessed.
    inability_flags: 現時点で評価不能な側面のリスト。
    These are NOT zero. They are unknown. Declaring unknown is honest.
    これらはゼロではない。不明である。不明を宣言することが誠実な設計。
    """

    # Distance remaining to resource threshold / 資源閾値までの残距離
    # e.g. food, water, energy supply headroom
    # 例: 食料・水・エネルギー供給の余裕
    resource_threshold_distance: float

    # Remaining reversible time window / 可逆的時間窓の残量
    # Time-sensitive operations (planting season, harvest window) are irreversible.
    # 時間依存操作（播種期・収穫期）は不可逆。
    time_window_remaining: float

    # Redundancy: availability of alternative paths / 代替経路の存在度
    # 0.0 = no alternative, 1.0 = full redundancy
    # 0.0 = 代替なし, 1.0 = 完全冗長
    redundancy_available: float

    # Irreversibility depth already consumed / 既消費不可逆深度
    # 0.0 = nothing consumed yet, 1.0 = maximum depth reached
    # 0.0 = 未消費, 1.0 = 最大深度到達
    irreversibility_depth: float

    # Aspects that cannot be assessed at this time / 現時点で評価不能な側面
    inability_flags: Tuple[str, ...] = ()

    def survival_score(self) -> float:
        """
        Composite survival viability / 複合生存可能性スコア

        Weights toward most critical factors:
        最重要因子への重み付け:
          resource_threshold_distance  0.35
          time_window_remaining        0.30
          redundancy_available         0.20
          (1 - irreversibility_depth)  0.15
        """
        return (
            clamp01(self.resource_threshold_distance) * 0.35
            + clamp01(self.time_window_remaining) * 0.30
            + clamp01(self.redundancy_available) * 0.20
            + clamp01(1.0 - self.irreversibility_depth) * 0.15
        )

    def is_critical(self, threshold: float = 0.25) -> bool:
        """
        True if survival score is at or below critical threshold.
        生存スコアが臨界閾値以下であればTrue。
        """
        return self.survival_score() <= threshold

    def has_inability(self) -> bool:
        """True if any aspect cannot be assessed. / 評価不能側面が存在すればTrue。"""
        return len(self.inability_flags) > 0


# ============================================================
# Layer 1: Structural signals / 構造信号層
# ============================================================

@dataclass(frozen=True)
class LayeredStructuralSignals:
    """
    Layered signals: Layer 0 survival base + Layer 1 structural features.
    層別信号: Layer0生存基底 + Layer1構造特徴量。
    """

    # Layer 0 / 生存基底層
    survival: SurvivalLayer

    # Layer 1: structural features (range 0.0-1.0) / 構造特徴量
    contradiction_score: float
    history_break_score: float
    drift_score: float
    oscillation_score: float
    novelty_surge_score: float
    uncertainty_score: float
    causal_violation: bool = False
    note: str = ""


# ============================================================
# Ring history entry / 律環履歴エントリ
# ============================================================

@dataclass(frozen=True)
class RingHistoryEntry:
    """
    Append-only ring history entry. Never deleted. Never overwritten.
    追記専用律環履歴エントリ。削除なし。上書きなし。

    The history of how a structure was formed IS the structure.
    構造がどのように形成されたかの履歴が構造そのものである。
    """
    step_index: int
    layer0_survival_score: float
    layer0_irreversibility_depth: float
    layer0_inability_flags: Tuple[str, ...]
    gate_status: GateStatus
    r: float
    g: float
    delta: float
    tau: float
    note: str = ""


# ============================================================
# Config / 設定
# ============================================================

@dataclass(frozen=True)
class GateConfig:
    # Fail threshold applied to G(r) / G(r)に適用するfail閾値
    fail_threshold: float = 1.00
    # Review threshold / レビュー閾値
    review_threshold: float = 0.70
    # Re-open threshold / 再開閾値
    reopen_threshold: float = 0.55
    # Epsilon / 微小量
    epsilon: float = 1e-9

    # NRA-IDE G(r) parameters / G(r)パラメータ
    k_gate: float = 0.50
    escapement_band_width: float = 0.08

    # Layer 0 critical threshold / Layer0臨界閾値
    # Below this survival score → FAIL_CLOSED before structural check
    # この生存スコア以下 → 構造チェック前にFAIL_CLOSED
    survival_critical_threshold: float = 0.25

    # Layer 0 stress amplifier on delta / Layer0応力のδへの増幅係数
    # survival_score near 0 multiplies delta increment by this factor
    # 生存スコアが0に近いほどδ増分をこの係数で増幅
    survival_stress_amplifier: float = 2.50

    # Feature weights / 特徴量重み
    contradiction_weight: float = 0.20
    history_break_weight: float = 0.18
    drift_weight: float = 0.16
    causal_violation_weight: float = 0.22
    oscillation_weight: float = 0.10
    novelty_surge_weight: float = 0.07
    uncertainty_weight: float = 0.07

    # Base absorption / 基本吸収厚み
    base_tau: float = 1.00
    safety_margin: float = 0.15
    tau_decay_rate: float = 0.35
    delta_decay_rate: float = 0.08

    # Hard stop lines on raw Layer 1 scores / Layer1生スコア強制停止線
    contradiction_hard_stop: float = 0.95
    history_break_hard_stop: float = 0.95
    drift_hard_stop: float = 0.98
    causal_violation_hard_stop: float = 0.01


# ============================================================
# State and Decision / 状態と判定
# ============================================================

@dataclass(frozen=True)
class StructuralState:
    delta: float
    tau: float
    r: float
    g: float
    signals: LayeredStructuralSignals
    layer0_survival_score: float
    previous_status: GateStatus
    step_index: int


@dataclass(frozen=True)
class GateDecision:
    status: GateStatus
    r: float
    g: float
    layer0_survival_score: float
    reason_codes: Tuple[str, ...]
    summary_en: str
    summary_ja: str
    allow_human_review: bool


@dataclass(frozen=True)
class HumanReviewPacket:
    title: str
    structural_summary_en: str
    structural_summary_ja: str
    machine_status: str
    numeric_evidence: Dict[str, float]
    inability_flags: Tuple[str, ...]
    guidance_en: str
    guidance_ja: str
    ring_history_depth: int
    note: str = ""


# ============================================================
# Helper functions / 補助関数
# ============================================================

def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def qround(value: float, digits: int = 6) -> float:
    return round(float(value), digits)


def safe_div(numerator: float, denominator: float, epsilon: float = 1e-9) -> float:
    if abs(denominator) <= epsilon:
        return math.inf
    return numerator / denominator


def bool_to_score(flag: bool) -> float:
    return 1.0 if flag else 0.0


def gate_function(r: float, k: float, epsilon: float = 1e-9) -> float:
    """
    G(r) = r · |r| / (k + |r|)

    Suppresses small loads, amplifies at critical boundary.
    小負荷を抑制し、臨界境界で増幅する。
    """
    abs_r = abs(r)
    k_safe = max(k, epsilon)
    return r * abs_r / (k_safe + abs_r)


# ============================================================
# Core engine / 中核エンジン
# ============================================================

class SurvivalGateEngine:
    """
    Structural gate with survival base (Layer 0).
    生存基底（Layer 0）を持つ構造ゲート。

    Judgment order / 判定順序:
        1. Layer 0 inability check  → INABILITY
        2. Layer 0 survival critical → FAIL_CLOSED
        3. Layer 1 hard stop        → FAIL_CLOSED
        4. G(r) + escapement band   → PERMIT / REVIEW_REQUIRED / FAIL_CLOSED

    ring_history is append-only. / ring_historyは追記専用。
    """

    def __init__(self, config: Optional[GateConfig] = None) -> None:
        self.config = config or GateConfig()
        self._delta: float = 0.0
        self._tau: float = self.config.base_tau + self.config.safety_margin
        self._last_status: GateStatus = GateStatus.PERMIT
        self._step_index: int = 0
        # Append-only ring history / 追記専用律環履歴
        self._ring_history: List[RingHistoryEntry] = []

    # ----------------------------------------------------------
    # Public API / 公開API
    # ----------------------------------------------------------

    def evaluate(
        self, signals: LayeredStructuralSignals
    ) -> Tuple[StructuralState, GateDecision]:
        self._step_index += 1

        normalized = self._normalize_signals(signals)
        layer0 = normalized.survival
        survival_score = qround(layer0.survival_score())

        # Step 1: Inability check / 不能判定
        if layer0.has_inability():
            state = self._build_state(normalized, survival_score, r=0.0, g=0.0)
            decision = GateDecision(
                status=GateStatus.INABILITY,
                r=0.0,
                g=0.0,
                layer0_survival_score=survival_score,
                reason_codes=tuple(
                    f"inability:{flag}" for flag in layer0.inability_flags
                ),
                summary_en="Layer 0 assessment is incomplete. Cannot judge structure honestly.",
                summary_ja="Layer 0の評価が不完全です。構造を誠実に判定できません。",
                allow_human_review=True,
            )
            self._append_history(state, decision)
            self._last_status = decision.status
            return state, decision

        # Step 2: Layer 0 survival critical / Layer0生存臨界判定
        if layer0.is_critical(self.config.survival_critical_threshold):
            state = self._build_state(normalized, survival_score, r=0.0, g=0.0)
            decision = GateDecision(
                status=GateStatus.FAIL_CLOSED,
                r=0.0,
                g=0.0,
                layer0_survival_score=survival_score,
                reason_codes=("layer0_survival_critical",),
                summary_en=f"Survival base critical (score={survival_score:.4f}). All processing stops.",
                summary_ja=f"生存基底が臨界状態です (score={survival_score:.4f})。全処理を停止します。",
                allow_human_review=False,
            )
            self._append_history(state, decision)
            self._last_status = decision.status
            return state, decision

        # Step 3 & 4: Structural judgment with Layer 0 modulation
        # Layer 0変調付き構造判定
        delta_increment = self._compute_delta_increment(normalized, survival_score)
        self._delta = self._update_delta(self._delta, delta_increment)
        self._tau = self._update_tau(normalized, self._tau, layer0)

        r = qround(safe_div(self._delta, self._tau, self.config.epsilon))
        g = qround(gate_function(r, self.config.k_gate, self.config.epsilon))

        state = self._build_state(normalized, survival_score, r=r, g=g)
        decision = self._make_structural_decision(state)

        self._append_history(state, decision)
        self._last_status = decision.status
        return state, decision

    def build_human_review_packet(
        self,
        state: StructuralState,
        decision: GateDecision,
        note: str = "",
    ) -> HumanReviewPacket:
        guidance_en, guidance_ja = self._build_guidance(decision)
        s = state.signals

        numeric_evidence = {
            "layer0_survival_score": qround(state.layer0_survival_score),
            "layer0_resource_threshold_distance": qround(
                s.survival.resource_threshold_distance
            ),
            "layer0_time_window_remaining": qround(s.survival.time_window_remaining),
            "layer0_redundancy_available": qround(s.survival.redundancy_available),
            "layer0_irreversibility_depth": qround(s.survival.irreversibility_depth),
            "delta": qround(state.delta),
            "tau": qround(state.tau),
            "r": qround(state.r),
            "g": qround(state.g),
            "contradiction_score": qround(s.contradiction_score),
            "history_break_score": qround(s.history_break_score),
            "drift_score": qround(s.drift_score),
            "oscillation_score": qround(s.oscillation_score),
            "novelty_surge_score": qround(s.novelty_surge_score),
            "uncertainty_score": qround(s.uncertainty_score),
            "causal_violation_score": qround(bool_to_score(s.causal_violation)),
        }

        return HumanReviewPacket(
            title="Survival-Base Structural Review Packet / 生存基底構造レビューパケット",
            structural_summary_en=decision.summary_en,
            structural_summary_ja=decision.summary_ja,
            machine_status=decision.status.value,
            numeric_evidence=numeric_evidence,
            inability_flags=s.survival.inability_flags,
            guidance_en=guidance_en,
            guidance_ja=guidance_ja,
            ring_history_depth=len(self._ring_history),
            note=note or s.note,
        )

    @property
    def ring_history(self) -> Tuple[RingHistoryEntry, ...]:
        """Read-only view of append-only ring history. / 追記専用律環履歴の読み取り専用ビュー。"""
        return tuple(self._ring_history)

    def reset(self) -> None:
        """
        Reset engine state. ring_history is preserved — it cannot be erased.
        エンジン状態をリセット。ring_historyは保持される—消去できない。
        """
        self._delta = 0.0
        self._tau = self.config.base_tau + self.config.safety_margin
        self._last_status = GateStatus.PERMIT
        self._step_index = 0
        # ring_history intentionally NOT reset / ring_historyは意図的にリセットしない

    # ----------------------------------------------------------
    # Internal methods / 内部処理
    # ----------------------------------------------------------

    def _normalize_signals(
        self, signals: LayeredStructuralSignals
    ) -> LayeredStructuralSignals:
        s = signals.survival
        normalized_survival = SurvivalLayer(
            resource_threshold_distance=clamp01(s.resource_threshold_distance),
            time_window_remaining=clamp01(s.time_window_remaining),
            redundancy_available=clamp01(s.redundancy_available),
            irreversibility_depth=clamp01(s.irreversibility_depth),
            inability_flags=s.inability_flags,
        )
        return LayeredStructuralSignals(
            survival=normalized_survival,
            contradiction_score=clamp01(signals.contradiction_score),
            history_break_score=clamp01(signals.history_break_score),
            drift_score=clamp01(signals.drift_score),
            oscillation_score=clamp01(signals.oscillation_score),
            novelty_surge_score=clamp01(signals.novelty_surge_score),
            uncertainty_score=clamp01(signals.uncertainty_score),
            causal_violation=bool(signals.causal_violation),
            note=signals.note,
        )

    def _compute_delta_increment(
        self, signals: LayeredStructuralSignals, survival_score: float
    ) -> float:
        """
        Delta increment with Layer 0 stress amplification.
        Layer 0応力増幅付きδ増分。

        Low survival score amplifies structural load.
        生存スコアが低いほど構造負荷が増幅される。
        """
        cfg = self.config

        base_increment = (
            signals.contradiction_score * cfg.contradiction_weight
            + signals.history_break_score * cfg.history_break_weight
            + signals.drift_score * cfg.drift_weight
            + bool_to_score(signals.causal_violation) * cfg.causal_violation_weight
            + signals.oscillation_score * cfg.oscillation_weight
            + signals.novelty_surge_score * cfg.novelty_surge_weight
            + signals.uncertainty_score * cfg.uncertainty_weight
        )
        base_increment = clamp01(base_increment)

        # Layer 0 stress multiplier: 1.0 at full survival, amplifier at zero
        # Layer0応力乗数: 生存満充足で1.0、ゼロで増幅係数
        stress_multiplier = 1.0 + (1.0 - survival_score) * (
            cfg.survival_stress_amplifier - 1.0
        )

        return clamp01(base_increment * stress_multiplier)

    def _update_delta(self, old_delta: float, delta_increment: float) -> float:
        cfg = self.config
        decayed = old_delta * (1.0 - cfg.delta_decay_rate)
        return max(0.0, decayed + delta_increment)

    def _update_tau(
        self,
        signals: LayeredStructuralSignals,
        old_tau: float,
        layer0: SurvivalLayer,
    ) -> float:
        """
        Tau shrinks under Layer 1 stress and Layer 0 irreversibility depth.
        τはLayer1応力とLayer0不可逆深度で減少する。
        """
        cfg = self.config

        l1_stress = clamp01(
            0.35 * signals.contradiction_score
            + 0.20 * signals.history_break_score
            + 0.20 * signals.drift_score
            + 0.15 * bool_to_score(signals.causal_violation)
            + 0.10 * signals.uncertainty_score
        )

        # Irreversibility depth reduces tau floor
        # 不可逆深度はτの下限を低下させる
        irreversibility_pressure = clamp01(layer0.irreversibility_depth) * 0.20

        combined_stress = clamp01(l1_stress + irreversibility_pressure)

        target_tau = max(
            cfg.epsilon,
            (cfg.base_tau + cfg.safety_margin)
            * (1.0 - cfg.tau_decay_rate * combined_stress),
        )

        if combined_stress > 0.0:
            return max(cfg.epsilon, min(old_tau, target_tau))
        return max(cfg.epsilon, min(cfg.base_tau + cfg.safety_margin, old_tau + 0.01))

    def _hard_stop_reason(
        self, signals: LayeredStructuralSignals
    ) -> Optional[str]:
        cfg = self.config
        if signals.causal_violation and cfg.causal_violation_hard_stop <= 0.01:
            return "causal_direction_violation"
        if signals.contradiction_score >= cfg.contradiction_hard_stop:
            return "contradiction_hard_stop"
        if signals.history_break_score >= cfg.history_break_hard_stop:
            return "history_break_hard_stop"
        if signals.drift_score >= cfg.drift_hard_stop:
            return "drift_hard_stop"
        return None

    def _make_structural_decision(self, state: StructuralState) -> GateDecision:
        cfg = self.config
        reasons: List[str] = []

        # Layer 1 hard stop / Layer1強制停止
        hard_stop = self._hard_stop_reason(state.signals)
        if hard_stop is not None:
            reasons.append(hard_stop)
            return GateDecision(
                status=GateStatus.FAIL_CLOSED,
                r=state.r,
                g=state.g,
                layer0_survival_score=state.layer0_survival_score,
                reason_codes=tuple(reasons),
                summary_en="Hard structural stop triggered.",
                summary_ja="強制構造停止が発動しました。",
                allow_human_review=False,
            )

        g = state.g
        half_band = cfg.escapement_band_width / 2.0

        # G(r) fail threshold / G(r) fail閾値
        if g >= cfg.fail_threshold:
            reasons.append("g_fail_threshold_exceeded")
            return GateDecision(
                status=GateStatus.FAIL_CLOSED,
                r=state.r,
                g=g,
                layer0_survival_score=state.layer0_survival_score,
                reason_codes=tuple(reasons),
                summary_en=f"G(r)={g:.4f} exceeded fail threshold {cfg.fail_threshold}.",
                summary_ja=f"G(r)={g:.4f} が fail 閾値 {cfg.fail_threshold} を超過しました。",
                allow_human_review=False,
            )

        # Escapement hysteresis / エスカープメントヒステリシス
        reopen_edge = cfg.reopen_threshold - half_band
        if self._last_status == GateStatus.FAIL_CLOSED and g > reopen_edge:
            reasons.append("escapement_hold")
            return GateDecision(
                status=GateStatus.FAIL_CLOSED,
                r=state.r,
                g=g,
                layer0_survival_score=state.layer0_survival_score,
                reason_codes=tuple(reasons),
                summary_en=f"Escapement hold: G(r)={g:.4f} > reopen edge {reopen_edge:.4f}.",
                summary_ja=f"エスカープメント保持: G(r)={g:.4f} が再開端 {reopen_edge:.4f} を超えています。",
                allow_human_review=False,
            )

        # Review band / レビュー帯域
        review_upper = cfg.review_threshold + half_band
        review_lower = cfg.review_threshold - half_band
        currently_in_review = self._last_status == GateStatus.REVIEW_REQUIRED
        review_flags = self._collect_review_flags(state)

        if g >= review_upper or (currently_in_review and g >= review_lower) or review_flags:
            reasons.append("review_band")
            reasons.extend(review_flags)
            return GateDecision(
                status=GateStatus.REVIEW_REQUIRED,
                r=state.r,
                g=g,
                layer0_survival_score=state.layer0_survival_score,
                reason_codes=tuple(reasons),
                summary_en="Structure not broken, but human review is required.",
                summary_ja="構造破断ではありませんが、人間確認が必要です。",
                allow_human_review=True,
            )

        reasons.append("structure_valid")
        return GateDecision(
            status=GateStatus.PERMIT,
            r=state.r,
            g=g,
            layer0_survival_score=state.layer0_survival_score,
            reason_codes=tuple(reasons),
            summary_en="Structure valid. Survival base satisfied.",
            summary_ja="構造有効。生存基底充足。",
            allow_human_review=True,
        )

    def _collect_review_flags(self, state: StructuralState) -> List[str]:
        flags: List[str] = []
        s = state.signals
        if s.contradiction_score >= 0.60:
            flags.append("contradiction_rising")
        if s.history_break_score >= 0.60:
            flags.append("history_break_rising")
        if s.drift_score >= 0.60:
            flags.append("drift_rising")
        if s.oscillation_score >= 0.65:
            flags.append("oscillation_rising")
        if s.novelty_surge_score >= 0.70:
            flags.append("novelty_surge_rising")
        if s.uncertainty_score >= 0.70:
            flags.append("uncertainty_rising")
        # Layer 0 review trigger / Layer0レビュートリガー
        if state.layer0_survival_score < 0.50:
            flags.append("survival_score_declining")
        if state.signals.survival.irreversibility_depth >= 0.60:
            flags.append("irreversibility_accumulating")
        return flags

    def _build_state(
        self,
        signals: LayeredStructuralSignals,
        survival_score: float,
        r: float,
        g: float,
    ) -> StructuralState:
        return StructuralState(
            delta=qround(self._delta),
            tau=qround(self._tau),
            r=qround(r),
            g=qround(g),
            signals=signals,
            layer0_survival_score=qround(survival_score),
            previous_status=self._last_status,
            step_index=self._step_index,
        )

    def _append_history(
        self, state: StructuralState, decision: GateDecision
    ) -> None:
        """Append to ring_history. Never modifies existing entries. / 追記のみ。既存エントリを変更しない。"""
        entry = RingHistoryEntry(
            step_index=state.step_index,
            layer0_survival_score=state.layer0_survival_score,
            layer0_irreversibility_depth=qround(
                state.signals.survival.irreversibility_depth
            ),
            layer0_inability_flags=state.signals.survival.inability_flags,
            gate_status=decision.status,
            r=state.r,
            g=state.g,
            delta=state.delta,
            tau=state.tau,
            note=state.signals.note,
        )
        self._ring_history.append(entry)

    def _build_guidance(self, decision: GateDecision) -> Tuple[str, str]:
        if decision.status == GateStatus.INABILITY:
            return (
                "Layer 0 assessment incomplete. Do not proceed. Gather survival data first.",
                "Layer 0評価が不完全です。処理を進めず、まず生存データを収集してください。",
            )
        if decision.status == GateStatus.FAIL_CLOSED:
            return (
                "Do not continue. Escalate to human owner with full ring history.",
                "継続不可。完全な律環履歴とともに人間責任者へ委譲してください。",
            )
        if decision.status == GateStatus.REVIEW_REQUIRED:
            return (
                "Human review allowed. Verify survival base before semantic approval.",
                "人確認可能。意味承認の前に生存基底状態を確認してください。",
            )
        return (
            "Processing may continue. Maintain survival monitoring.",
            "処理継続可能。生存監視を継続してください。",
        )


# ============================================================
# Report helper / 報告補助
# ============================================================

def format_review_packet(packet: HumanReviewPacket) -> str:
    lines = [
        packet.title,
        f"Status / 状態: {packet.machine_status}",
        f"Ring history depth / 律環履歴深度: {packet.ring_history_depth}",
        f"EN: {packet.structural_summary_en}",
        f"JA: {packet.structural_summary_ja}",
        f"Guide EN: {packet.guidance_en}",
        f"Guide JA: {packet.guidance_ja}",
        "Evidence / 根拠:",
    ]
    for key, value in packet.numeric_evidence.items():
        lines.append(f"  - {key}: {value}")
    if packet.inability_flags:
        lines.append(f"Inability flags / 不能フラグ: {packet.inability_flags}")
    if packet.note:
        lines.append(f"Note / 注記: {packet.note}")
    return "\n".join(lines)


# ============================================================
# Demo / 使用例
# ============================================================

def _demo() -> None:
    engine = SurvivalGateEngine()

    scenarios = [
        # Scenario 1: Normal — survival healthy, structure clean
        # シナリオ1: 通常—生存健全・構造正常
        LayeredStructuralSignals(
            survival=SurvivalLayer(
                resource_threshold_distance=0.80,
                time_window_remaining=0.75,
                redundancy_available=0.70,
                irreversibility_depth=0.10,
            ),
            contradiction_score=0.10, history_break_score=0.08,
            drift_score=0.12, oscillation_score=0.05,
            novelty_surge_score=0.10, uncertainty_score=0.15,
            note="Normal / 通常",
        ),

        # Scenario 2: Survival declining, structure stressed
        # シナリオ2: 生存低下・構造応力あり
        LayeredStructuralSignals(
            survival=SurvivalLayer(
                resource_threshold_distance=0.40,
                time_window_remaining=0.35,
                redundancy_available=0.30,
                irreversibility_depth=0.55,
            ),
            contradiction_score=0.55, history_break_score=0.48,
            drift_score=0.63, oscillation_score=0.52,
            novelty_surge_score=0.42, uncertainty_score=0.58,
            note="Survival declining / 生存低下",
        ),

        # Scenario 3: Layer 0 inability — time window unknown
        # シナリオ3: Layer0不能—時間窓が不明
        LayeredStructuralSignals(
            survival=SurvivalLayer(
                resource_threshold_distance=0.60,
                time_window_remaining=0.50,
                redundancy_available=0.55,
                irreversibility_depth=0.30,
                inability_flags=("time_window_unknown", "redundancy_unverified"),
            ),
            contradiction_score=0.20, history_break_score=0.15,
            drift_score=0.18, oscillation_score=0.10,
            novelty_surge_score=0.12, uncertainty_score=0.20,
            note="Inability declared / 不能宣言",
        ),

        # Scenario 4: Survival critical — below threshold
        # シナリオ4: 生存臨界—閾値以下
        LayeredStructuralSignals(
            survival=SurvivalLayer(
                resource_threshold_distance=0.10,
                time_window_remaining=0.05,
                redundancy_available=0.00,
                irreversibility_depth=0.90,
            ),
            contradiction_score=0.30, history_break_score=0.25,
            drift_score=0.28, oscillation_score=0.20,
            novelty_surge_score=0.15, uncertainty_score=0.30,
            note="Survival critical / 生存臨界",
        ),

        # Scenario 5: Layer 1 hard stop (causal violation)
        # シナリオ5: Layer1強制停止（因果違反）
        LayeredStructuralSignals(
            survival=SurvivalLayer(
                resource_threshold_distance=0.65,
                time_window_remaining=0.60,
                redundancy_available=0.50,
                irreversibility_depth=0.40,
            ),
            contradiction_score=0.72, history_break_score=0.66,
            drift_score=0.82, oscillation_score=0.70,
            novelty_surge_score=0.61, uncertainty_score=0.74,
            causal_violation=True,
            note="Causal violation / 因果違反",
        ),
    ]

    for idx, signals in enumerate(scenarios, start=1):
        state, decision = engine.evaluate(signals)
        packet = engine.build_human_review_packet(state, decision)

        print(f"--- Step {idx} / ステップ {idx} ---")
        print(f"Decision: {decision.status.value}")
        print(f"Layer0 survival={state.layer0_survival_score}  "
              f"R={state.r}  G(r)={state.g}")
        print(f"Reasons: {decision.reason_codes}")
        print(format_review_packet(packet))
        print()

    print("=== Ring History / 律環履歴 ===")
    for entry in engine.ring_history:
        print(f"  step={entry.step_index}  "
              f"status={entry.gate_status.value}  "
              f"survival={entry.layer0_survival_score}  "
              f"irrev={entry.layer0_irreversibility_depth}  "
              f"g={entry.g}  "
              f"inability={entry.layer0_inability_flags}")


if __name__ == "__main__":
    _demo()
