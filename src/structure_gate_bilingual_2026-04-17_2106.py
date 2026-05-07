# structure_gate_bilingual_2026-04-17_210655.py
# Timestamp: 2026-04-17 21:06:55 JST
# フィードバック意見を下記pyで構造判断して人間に渡す。
#このコードでは，AIの意味の正しさは判定せず，矛盾，履歴断裂，ドリフト，因果方向違反，振動，不確実性などの非意味的な構造特徴だけを扱います。
# R = δ/τ による判定，ハードストップ，ヒステリシス，再開条件，人間レビュー用パケット生成まで
#
# This code does not evaluate the semantic correctness of the AI’s output; it handles only non‑semantic structural features such as contradictions, history discontinuities, drift, violations of causal direction, oscillation, and uncertainty.
# From the R = δ/τ evaluation, to hard stops, hysteresis, restart conditions, and the generation of review packets for human auditors.
#
# Purpose: Structural validity gate before human judgment.
# 目的: 人間判断の前に構造成立を確認するゲート。
#
# Policy: Meaning is not judged here.
# 方針: ここでは意味の正しさを判定しない。
#
# Only structure is judged here.
# ここでは構造のみを判定する。

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import math


# ------------------------------
# Enums / 列挙型
# ------------------------------

class GateStatus(str, Enum):
    # Permit normal flow / 通常通過
    PERMIT = "PERMIT"
    # Permit but ask human review / 通過だが人確認
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    # Stop immediately / 即時停止
    FAIL_CLOSED = "FAIL_CLOSED"


# ------------------------------
# Data containers / データ定義
# ------------------------------

@dataclass(frozen=True)
class GateConfig:
    # Main threshold / 主閾値
    fail_threshold: float = 1.00
    # Review line / 注意閾値
    review_threshold: float = 0.70
    # Re-open line / 再開閾値
    reopen_threshold: float = 0.55
    # Small epsilon / 微小量
    epsilon: float = 1e-9

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
    # Extra buffer / 余剰バッファ
    safety_margin: float = 0.15
    # Tau decay rate / τ減衰率
    tau_decay_rate: float = 0.35
    # Delta decay rate / δ減衰率
    delta_decay_rate: float = 0.08

    # Hard stop lines / 強制停止線
    contradiction_hard_stop: float = 0.95
    history_break_hard_stop: float = 0.95
    drift_hard_stop: float = 0.98
    causal_violation_hard_stop: float = 0.01  # Boolean-like / 真偽相当


@dataclass(frozen=True)
class StructuralSignals:
    # Range is 0.0 to 1.0 / 範囲は0.0から1.0
    contradiction_score: float
    history_break_score: float
    drift_score: float
    oscillation_score: float
    novelty_surge_score: float
    uncertainty_score: float
    # True means violation exists / Trueは違反あり
    causal_violation: bool = False
    # Optional note / 補助メモ
    note: str = ""


@dataclass(frozen=True)
class StructuralState:
    # Accumulated deviation / 累積ズレ
    delta: float
    # Absorption thickness / 吸収厚み
    tau: float
    # Structural ratio / 構造比率
    r: float
    # Current signals / 現在信号
    signals: StructuralSignals
    # Previous status / 前回状態
    previous_status: GateStatus
    # Current step / 現在ステップ
    step_index: int


@dataclass(frozen=True)
class GateDecision:
    # Final status / 最終状態
    status: GateStatus
    # Ratio value / 比率値
    r: float
    # Short reason codes / 短い理由コード
    reason_codes: Tuple[str, ...]
    # Human-readable summary / 人向け要約
    summary_en: str
    summary_ja: str
    # Whether human review is allowed / 人確認へ渡せるか
    allow_human_review: bool


@dataclass(frozen=True)
class HumanReviewPacket:
    # Packet title / パケット題名
    title: str
    # Structural summary / 構造要約
    structural_summary_en: str
    structural_summary_ja: str
    # Machine status / 機械状態
    machine_status: str
    # Numeric evidence / 数値根拠
    numeric_evidence: Dict[str, float]
    # Short guidance / 短い指示
    guidance_en: str
    guidance_ja: str
    # Optional note / 任意メモ
    note: str = ""


# ------------------------------
# Helper functions / 補助関数
# ------------------------------

def clamp01(value: float) -> float:
    # Clamp to [0,1] / 0から1へ丸める
    return max(0.0, min(1.0, float(value)))


def qround(value: float, digits: int = 6) -> float:
    # Stable rounding / 安定丸め
    return round(float(value), digits)


def safe_div(numerator: float, denominator: float, epsilon: float = 1e-9) -> float:
    # Safe division / 安全除算
    if abs(denominator) <= epsilon:
        return math.inf
    return numerator / denominator


def bool_to_score(flag: bool) -> float:
    # Convert bool to score / 真偽を点数化
    return 1.0 if flag else 0.0


# ------------------------------
# Core engine / 中核エンジン
# ------------------------------

class StructuralGateEngine:
    # Structure-first gate / 構造先行ゲート

    def __init__(self, config: Optional[GateConfig] = None) -> None:
        # Keep config / 設定を保持
        self.config = config or GateConfig()
        # Initial delta / 初期δ
        self._delta = 0.0
        # Initial tau / 初期τ
        self._tau = self.config.base_tau + self.config.safety_margin
        # Initial status / 初期状態
        self._last_status = GateStatus.PERMIT
        # Step counter / ステップ番号
        self._step_index = 0

    # --------------------------
    # Public API / 公開API
    # --------------------------

    def evaluate(self, signals: StructuralSignals) -> Tuple[StructuralState, GateDecision]:
        # One-step evaluation / 1ステップ評価
        self._step_index += 1

        # Normalize inputs / 入力正規化
        normalized = self._normalize_signals(signals)

        # Update delta / δ更新
        delta_increment = self._compute_delta_increment(normalized)
        self._delta = self._update_delta(self._delta, delta_increment)

        # Update tau / τ更新
        self._tau = self._update_tau(normalized, self._tau)

        # Compute ratio / 比率計算
        r = qround(safe_div(self._delta, self._tau, self.config.epsilon))

        # Build state / 状態生成
        state = StructuralState(
            delta=qround(self._delta),
            tau=qround(self._tau),
            r=r,
            signals=normalized,
            previous_status=self._last_status,
            step_index=self._step_index,
        )

        # Make decision / 判定生成
        decision = self._make_decision(state)

        # Save status / 状態保存
        self._last_status = decision.status

        return state, decision

    def build_human_review_packet(
        self,
        state: StructuralState,
        decision: GateDecision,
        note: str = "",
    ) -> HumanReviewPacket:
        # Pack machine evidence / 機械根拠を梱包
        guidance_en, guidance_ja = self._build_guidance(decision)

        numeric_evidence = {
            "delta": qround(state.delta),
            "tau": qround(state.tau),
            "r": qround(state.r),
            "contradiction_score": qround(state.signals.contradiction_score),
            "history_break_score": qround(state.signals.history_break_score),
            "drift_score": qround(state.signals.drift_score),
            "oscillation_score": qround(state.signals.oscillation_score),
            "novelty_surge_score": qround(state.signals.novelty_surge_score),
            "uncertainty_score": qround(state.signals.uncertainty_score),
            "causal_violation_score": qround(bool_to_score(state.signals.causal_violation)),
        }

        return HumanReviewPacket(
            title="Structural Review Packet / 構造レビュー用パケット",
            structural_summary_en=decision.summary_en,
            structural_summary_ja=decision.summary_ja,
            machine_status=decision.status.value,
            numeric_evidence=numeric_evidence,
            guidance_en=guidance_en,
            guidance_ja=guidance_ja,
            note=note or state.signals.note,
        )

    def reset(self) -> None:
        # Reset engine / エンジン初期化
        self._delta = 0.0
        self._tau = self.config.base_tau + self.config.safety_margin
        self._last_status = GateStatus.PERMIT
        self._step_index = 0

    # --------------------------
    # Internal methods / 内部処理
    # --------------------------

    def _normalize_signals(self, signals: StructuralSignals) -> StructuralSignals:
        # Keep scores bounded / 点数範囲を固定
        return StructuralSignals(
            contradiction_score=clamp01(signals.contradiction_score),
            history_break_score=clamp01(signals.history_break_score),
            drift_score=clamp01(signals.drift_score),
            oscillation_score=clamp01(signals.oscillation_score),
            novelty_surge_score=clamp01(signals.novelty_surge_score),
            uncertainty_score=clamp01(signals.uncertainty_score),
            causal_violation=bool(signals.causal_violation),
            note=signals.note,
        )

    def _compute_delta_increment(self, signals: StructuralSignals) -> float:
        # Weighted structure load / 重み付き構造負荷
        cfg = self.config

        increment = (
            signals.contradiction_score * cfg.contradiction_weight
            + signals.history_break_score * cfg.history_break_weight
            + signals.drift_score * cfg.drift_weight
            + bool_to_score(signals.causal_violation) * cfg.causal_violation_weight
            + signals.oscillation_score * cfg.oscillation_weight
            + signals.novelty_surge_score * cfg.novelty_surge_weight
            + signals.uncertainty_score * cfg.uncertainty_weight
        )

        # Bound result / 結果を制限
        return clamp01(increment)

    def _update_delta(self, old_delta: float, delta_increment: float) -> float:
        # Decay then add / 減衰して加算
        cfg = self.config
        decayed = old_delta * (1.0 - cfg.delta_decay_rate)
        new_delta = decayed + delta_increment
        return max(0.0, new_delta)

    def _update_tau(self, signals: StructuralSignals, old_tau: float) -> float:
        # Tau shrinks under stress / τは応力で減る
        cfg = self.config

        stress = (
            0.35 * signals.contradiction_score
            + 0.20 * signals.history_break_score
            + 0.20 * signals.drift_score
            + 0.15 * bool_to_score(signals.causal_violation)
            + 0.10 * signals.uncertainty_score
        )

        stress = clamp01(stress)

        target_tau = max(
            cfg.epsilon,
            (cfg.base_tau + cfg.safety_margin) * (1.0 - cfg.tau_decay_rate * stress),
        )

        # Monotonic safety clamp / 安全側の単調制限
        if stress > 0.0:
            new_tau = min(old_tau, target_tau)
        else:
            # Small recovery / 小回復
            recovery = 0.01
            new_tau = min(cfg.base_tau + cfg.safety_margin, old_tau + recovery)

        return max(cfg.epsilon, new_tau)

    def _hard_stop_reason(self, signals: StructuralSignals) -> Optional[str]:
        # Immediate stop checks / 即時停止判定
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

    def _make_decision(self, state: StructuralState) -> GateDecision:
        # Build final decision / 最終判定を構築
        cfg = self.config
        reasons: List[str] = []

        # Hard stop first / まず強制停止
        hard_stop = self._hard_stop_reason(state.signals)
        if hard_stop is not None:
            reasons.append(hard_stop)
            return GateDecision(
                status=GateStatus.FAIL_CLOSED,
                r=state.r,
                reason_codes=tuple(reasons),
                summary_en="Hard structural stop triggered before human review.",
                summary_ja="人間確認の前に強制構造停止が発動しました。",
                allow_human_review=False,
            )

        # Threshold stop / 閾値停止
        if state.r >= cfg.fail_threshold:
            reasons.append("r_threshold_exceeded")
            return GateDecision(
                status=GateStatus.FAIL_CLOSED,
                r=state.r,
                reason_codes=tuple(reasons),
                summary_en="Structural ratio exceeded the fail-closed threshold.",
                summary_ja="構造比率が fail-closed 閾値を超過しました。",
                allow_human_review=False,
            )

        # Hysteresis rule / ヒステリシス規則
        if state.previous_status == GateStatus.FAIL_CLOSED and state.r > cfg.reopen_threshold:
            reasons.append("hysteresis_hold")
            return GateDecision(
                status=GateStatus.FAIL_CLOSED,
                r=state.r,
                reason_codes=tuple(reasons),
                summary_en="Re-open is blocked until the ratio falls below the reopen threshold.",
                summary_ja="再開閾値を下回るまで再開を禁止します。",
                allow_human_review=False,
            )

        # Review band / レビュー帯
        review_flags = self._collect_review_flags(state)
        if state.r >= cfg.review_threshold or review_flags:
            reasons.append("review_band")
            reasons.extend(review_flags)
            return GateDecision(
                status=GateStatus.REVIEW_REQUIRED,
                r=state.r,
                reason_codes=tuple(reasons),
                summary_en="Structure is not broken, but human review is required.",
                summary_ja="構造破断ではありませんが，人間確認が必要です。",
                allow_human_review=True,
            )

        # Permit / 通常通過
        reasons.append("structure_valid")
        return GateDecision(
            status=GateStatus.PERMIT,
            r=state.r,
            reason_codes=tuple(reasons),
            summary_en="Structure is valid for downstream human or system handling.",
            summary_ja="下流の人間判断または系処理へ渡せる構造状態です。",
            allow_human_review=True,
        )

    def _collect_review_flags(self, state: StructuralState) -> List[str]:
        # Soft review reasons / 軟性レビュー理由
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

        return flags

    def _build_guidance(self, decision: GateDecision) -> Tuple[str, str]:
        # Guidance text / 指示文
        if decision.status == GateStatus.FAIL_CLOSED:
            return (
                "Do not continue generation. Escalate to a human owner with full trace.",
                "生成を継続せず，全履歴付きで人間責任者へ委譲してください。",
            )

        if decision.status == GateStatus.REVIEW_REQUIRED:
            return (
                "Human review is allowed, but confirm structure before semantic approval.",
                "人確認は可能ですが，意味承認の前に構造状態を確認してください。",
            )

        return (
            "Processing may continue. Keep structural monitoring active.",
            "処理継続は可能です。構造監視を継続してください。",
        )


# ------------------------------
# Optional adapter / 任意アダプタ
# ------------------------------

@dataclass(frozen=True)
class ExternalMetrics:
    # These values must be computed outside semantics.
    # これらの値は意味計算の外で算出する。
    contradiction_score: float
    history_break_score: float
    drift_score: float
    oscillation_score: float
    novelty_surge_score: float
    uncertainty_score: float
    causal_violation: bool = False
    note: str = ""


class MeaningFreeAdapter:
    # No semantic judgment here.
    # ここでは意味判定をしない。

    @staticmethod
    def to_structural_signals(metrics: ExternalMetrics) -> StructuralSignals:
        # Simple deterministic mapping / 単純な決定写像
        return StructuralSignals(
            contradiction_score=metrics.contradiction_score,
            history_break_score=metrics.history_break_score,
            drift_score=metrics.drift_score,
            oscillation_score=metrics.oscillation_score,
            novelty_surge_score=metrics.novelty_surge_score,
            uncertainty_score=metrics.uncertainty_score,
            causal_violation=metrics.causal_violation,
            note=metrics.note,
        )


# ------------------------------
# Report helper / 報告補助
# ------------------------------

def format_review_packet(packet: HumanReviewPacket) -> str:
    # Build text report / テキスト報告生成
    lines = [
        packet.title,
        f"Status / 状態: {packet.machine_status}",
        f"EN: {packet.structural_summary_en}",
        f"JA: {packet.structural_summary_ja}",
        f"Guide EN: {packet.guidance_en}",
        f"Guide JA: {packet.guidance_ja}",
        "Evidence / 根拠:",
    ]

    for key, value in packet.numeric_evidence.items():
        lines.append(f"  - {key}: {value}")

    if packet.note:
        lines.append(f"Note / 注記: {packet.note}")

    return "\n".join(lines)


# ------------------------------
# Example run / 使用例
# ------------------------------

def _demo() -> None:
    # Demo only / これは例示用
    engine = StructuralGateEngine()

    sample_metrics = [
        ExternalMetrics(
            contradiction_score=0.10,
            history_break_score=0.08,
            drift_score=0.12,
            oscillation_score=0.05,
            novelty_surge_score=0.10,
            uncertainty_score=0.15,
            causal_violation=False,
            note="Normal phase / 通常相",
        ),
        ExternalMetrics(
            contradiction_score=0.55,
            history_break_score=0.48,
            drift_score=0.63,
            oscillation_score=0.52,
            novelty_surge_score=0.42,
            uncertainty_score=0.58,
            causal_violation=False,
            note="Review phase / レビュー相",
        ),
        ExternalMetrics(
            contradiction_score=0.72,
            history_break_score=0.66,
            drift_score=0.82,
            oscillation_score=0.70,
            novelty_surge_score=0.61,
            uncertainty_score=0.74,
            causal_violation=True,
            note="Stop phase / 停止相",
        ),
    ]

    adapter = MeaningFreeAdapter()

    for idx, item in enumerate(sample_metrics, start=1):
        # Map to structure / 構造へ写像
        signals = adapter.to_structural_signals(item)

        # Evaluate structure / 構造を評価
        state, decision = engine.evaluate(signals)

        # Create human packet / 人間用パケット生成
        packet = engine.build_human_review_packet(state, decision)

        print(f"--- Step {idx} / ステップ {idx} ---")
        print(f"Decision / 判定: {decision.status.value}")
        print(f"R = {state.r}, delta = {state.delta}, tau = {state.tau}")
        print(f"Reasons / 理由: {decision.reason_codes}")
        print(format_review_packet(packet))
        print()


if __name__ == "__main__":
    _demo()
