# -*- coding: utf-8 -*-
# file: nra_dual_survival_gate_jp_20260501_034016_JST.py
# generated_at_jst: 2026-05-01 03:40:16
"""
律環公理（NRA-IDE）二重ゆらぎ式ゲート。

この単一ファイル実装は、R = δ / τ を中心に、上方逸脱と下方逸脱を
別々の履歴系として扱う最小実行例です。Pylint の命名規約に合わせ、
Python 実装上の変数名は snake_case に統一しています。ただし、出力辞書の
キーでは理論表記との対応を保つため、"R"、"R_upper"、"R_lower" を残します。

設計上の改修点:
- global 文を廃止し、GateConfig に閾値を閉じ込める。
- 数学記号 R はコード内部では r として扱い、出力キーで理論表記を保持する。
- クラスと関数に docstring を付与する。
- 外側スコープ名の再定義を避ける。
- 判定の閾値、不能判定、二重ゆらぎ検出を設定オブジェクトに集約する。
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import math
from typing import Any


MINIMUM_TAU = 1.0e-6
STRUCTURAL_BOUNDARY = 1.0
WARNING_BOUNDARY = 0.4
DEFAULT_IRREVERSIBLE_BOUNDARY = 0.95


@dataclass(frozen=True)
class GateConfig:
    """ゲート判定に使う不変設定を保持します。"""

    structural_boundary: float = STRUCTURAL_BOUNDARY
    warning_boundary: float = WARNING_BOUNDARY
    irreversible_boundary: float = DEFAULT_IRREVERSIBLE_BOUNDARY
    minimum_tau: float = MINIMUM_TAU
    allow_caution_output: bool = True
    enable_inability_check: bool = True
    dual_fluctuation_enabled: bool = True

    def validate(self) -> None:
        """閾値設定が構造的に矛盾していないか確認します。"""
        if self.minimum_tau <= 0.0:
            raise ValueError("minimum_tau must be positive.")
        if self.warning_boundary < 0.0:
            raise ValueError("warning_boundary must be non-negative.")
        if not self.warning_boundary < self.irreversible_boundary:
            raise ValueError("warning_boundary must be less than irreversible_boundary.")
        if not self.irreversible_boundary <= self.structural_boundary:
            raise ValueError("irreversible_boundary must not exceed structural_boundary.")
        if not math.isclose(self.structural_boundary, 1.0):
            raise ValueError("structural_boundary is fixed at R = 1.0 in this demo.")


@dataclass
class DualTau:
    """上方・下方の厚み τ を個別に保持し、二重 EMA で更新します。"""

    tau_upper: float
    tau_lower: float
    alpha_upper: float = 0.1
    alpha_lower: float = 0.1
    minimum_tau: float = MINIMUM_TAU

    def __post_init__(self) -> None:
        """初期値を浮動小数に正規化し、最小厚みを保証します。"""
        self.tau_upper = self._clamp_tau(self.tau_upper)
        self.tau_lower = self._clamp_tau(self.tau_lower)
        self.alpha_upper = self._clamp_alpha(self.alpha_upper)
        self.alpha_lower = self._clamp_alpha(self.alpha_lower)
        self.minimum_tau = self._clamp_tau(self.minimum_tau)

    def update(self, delta_upper: float, delta_lower: float) -> None:
        """観測された上方・下方逸脱から τ を一段階更新します。"""
        next_upper = self._ema(self.tau_upper, delta_upper, self.alpha_upper)
        next_lower = self._ema(self.tau_lower, delta_lower, self.alpha_lower)
        self.tau_upper = self._clamp_tau(next_upper)
        self.tau_lower = self._clamp_tau(next_lower)

    def to_dict(self) -> dict[str, float]:
        """ログ出力用に τ の状態を辞書化します。"""
        return {
            "tau_upper": self.tau_upper,
            "tau_lower": self.tau_lower,
            "alpha_upper": self.alpha_upper,
            "alpha_lower": self.alpha_lower,
        }

    def _clamp_tau(self, value: float) -> float:
        """τ がゼロ以下にならないように最小値へ丸めます。"""
        return max(MINIMUM_TAU, float(value))

    @staticmethod
    def _clamp_alpha(value: float) -> float:
        """EMA 係数を 0.0 から 1.0 の範囲へ丸めます。"""
        return max(0.0, min(1.0, float(value)))

    @staticmethod
    def _ema(previous_value: float, observed_value: float, alpha: float) -> float:
        """指数移動平均の 1 ステップを計算します。"""
        return (1.0 - alpha) * previous_value + alpha * max(0.0, observed_value)


@dataclass
class NraStateDual:
    """NRA-IDE 二重ゆらぎゲートが評価する単一状態を表します。"""

    value: float
    threshold: float
    buffer: float = 0.0
    rate: float = 0.0
    tau_dual: DualTau = field(default_factory=lambda: DualTau(0.05, 0.05))

    def __post_init__(self) -> None:
        """value と threshold が有限かつ 0.0〜1.0 の範囲内であることを検証します。"""
        self.value = self._validate_unit(self.value, "value")
        self.threshold = self._validate_unit(self.threshold, "threshold")
        self.buffer = float(self.buffer)
        self.rate = float(self.rate)

    @classmethod
    def from_parameters(
        cls,
        value: float,
        threshold: float,
        buffer: float = 0.0,
        rate: float = 0.0,
        tau0_upper: float = 0.05,
        tau0_lower: float = 0.05,
        alpha_upper: float = 0.1,
        alpha_lower: float = 0.1,
    ) -> "NraStateDual":
        """旧実装に近い引数構成から状態を生成します。"""
        return cls(
            value=value,
            threshold=threshold,
            buffer=buffer,
            rate=rate,
            tau_dual=DualTau(
                tau_upper=tau0_upper,
                tau_lower=tau0_lower,
                alpha_upper=alpha_upper,
                alpha_lower=alpha_lower,
            ),
        )

    @property
    def delta(self) -> float:
        """上方逸脱を標準の δ として返します。"""
        return self.delta_upper

    @property
    def delta_upper(self) -> float:
        """閾値より上へ逸脱した量を返します。"""
        return max(0.0, self.value - self.threshold)

    @property
    def delta_lower(self) -> float:
        """閾値より下へ逸脱した量を返します。"""
        return max(0.0, self.threshold - self.value)

    @property
    def r_upper(self) -> float:
        """上方側の R = δ_upper / τ_upper を返します。"""
        return safe_ratio(self.delta_upper, self.tau_dual.tau_upper)

    @property
    def r_lower(self) -> float:
        """下方側の R = δ_lower / τ_lower を返します。"""
        return safe_ratio(self.delta_lower, self.tau_dual.tau_lower)

    @property
    def r(self) -> float:
        """上方・下方のうち、構造的に厳しい側の R を返します。"""
        return max(self.r_upper, self.r_lower)

    def update_tau(self) -> None:
        """現在の逸脱量を使い、二重 τ を更新します。"""
        self.tau_dual.update(self.delta_upper, self.delta_lower)

    def to_dict(self) -> dict[str, Any]:
        """理論表記を保ったログ用辞書を返します。"""
        return {
            "value": self.value,
            "threshold": self.threshold,
            "buffer": self.buffer,
            "rate": self.rate,
            "delta": self.delta,
            "delta_upper": self.delta_upper,
            "delta_lower": self.delta_lower,
            "tau_upper": self.tau_dual.tau_upper,
            "tau_lower": self.tau_dual.tau_lower,
            "R_upper": self.r_upper,
            "R_lower": self.r_lower,
            "R": self.r,
        }

    @staticmethod
    def _validate_unit(value: float, name: str) -> float:
        """非有限値や範囲外の値を、沈黙のうちに丸めず明示的に拒否します。"""
        value = float(value)
        if not math.isfinite(value) or not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be a finite value in [0.0, 1.0]; got {value}.")
        return value


@dataclass(frozen=True)
class DualRState:
    """分岐判定に使う R と τ のスナップショットです。"""

    r_upper: float
    r_lower: float
    r: float
    tau_upper: float
    tau_lower: float
    dtau_upper: float
    dtau_lower: float

    def dominant_branch(self) -> tuple[str, float, float]:
        """上方・下方のうち支配的な分岐名、R、τ を返します。"""
        if self.r_upper >= self.r_lower:
            return "upper", self.r_upper, self.tau_upper
        return "lower", self.r_lower, self.tau_lower


class DualFluctuationError(Exception):
    """二重ゆらぎゲートが出力停止、または固定Handoff証言の外部人間監査への提示を要求したことを表します。"""

    def __init__(self, message: str, branch: str, data: dict[str, Any]) -> None:
        """例外メッセージ、分岐名、ログ用データを保持します。"""
        super().__init__(message)
        self.branch = branch
        self.data = data


def safe_ratio(delta_value: float, tau_value: float) -> float:
    """τ が不正な場合は無限大を返し、通常時は δ / τ を返します。"""
    if tau_value <= 0.0 or not math.isfinite(tau_value):
        return float("inf")
    return max(0.0, float(delta_value)) / tau_value


def compute_sensitivity(r_value: float, tau_value: float) -> float:
    """R が境界に近づくほど大きくなる感度指標を計算します。"""
    if tau_value <= 0.0 or r_value >= 1.0:
        return float("inf")
    return 1.0 / (tau_value * (1.0 - r_value))


def has_invalid_tau(state: DualRState) -> bool:
    """上方または下方の τ が構造的に不正かどうかを判定します。"""
    return (
        state.tau_upper <= 0.0
        or state.tau_lower <= 0.0
        or not math.isfinite(state.tau_upper)
        or not math.isfinite(state.tau_lower)
    )


def build_base_result(status: str, state: DualRState) -> dict[str, Any]:
    """各分岐で共通する出力辞書の土台を作ります。"""
    return {
        "status": status,
        "R": state.r,
        "R_upper": state.r_upper,
        "R_lower": state.r_lower,
        "tau_upper": state.tau_upper,
        "tau_lower": state.tau_lower,
    }


def handle_dual_threshold_exceeded(
    state: DualRState,
    config: GateConfig,
) -> dict[str, Any]:
    """R の領域に応じて PERMIT、CAUTION、CRITICAL、FAIL_CLOSED を返します。"""
    if config.enable_inability_check and has_invalid_tau(state):
        error_data = build_base_result("INABILITY", state)
        error_data.update(
            {
                "message": "構造不能: τ が非正または非有限です。構造的許容量がありません。",
                "action": "halt",
                "human_authority_required": True,
            }
        )
        raise DualFluctuationError(
            "Structure error: tau is invalid.",
            "INABILITY_TAU_INVALID",
            error_data,
        )

    if state.r >= config.structural_boundary:
        error_data = build_base_result("FAIL_CLOSED", state)
        error_data.update(
            {
                "message": "二重ゆらぎの構造境界を超過しました。R >= 1.0。"
                "有効な AI 出力は許可されません。固定Handoff証言を外部人間監査へ提示します。",
                "action": "silent_stop",
                "human_authority_required": True,
            }
        )
        raise DualFluctuationError(
            "Structure boundary crossed: R >= 1.0.",
            "FAIL_CLOSED",
            error_data,
        )

    if state.r >= config.irreversible_boundary:
        return raise_critical_error(state, config)

    branch_name, branch_r, branch_tau = state.dominant_branch()
    sensitivity = compute_sensitivity(branch_r, branch_tau)

    if state.r >= config.warning_boundary:
        result_data = build_base_result("CAUTION", state)
        result_data.update(
            {
                "dominant_branch": branch_name,
                "sensitivity": sensitivity,
                "dual_fluctuation_warning": (
                    state.dtau_upper < 0.0 or state.dtau_lower < 0.0
                ),
                "message": "R は弾性域または警告域です。軌道追跡を継続してください。",
                "action": "continue_with_warning",
                "human_authority_required": False,
            }
        )
        return result_data

    result_data = build_base_result("PERMIT", state)
    result_data.update(
        {
            "dominant_branch": branch_name,
            "sensitivity": sensitivity,
            "message": "構造的な余裕があります。AI 出力は許可されます。",
            "action": "continue",
            "human_authority_required": False,
        }
    )
    return result_data


def raise_critical_error(state: DualRState, config: GateConfig) -> dict[str, Any]:
    """不可逆境界に近い CRITICAL 領域を分岐別に例外化します。"""
    sensitivity_upper = compute_sensitivity(state.r_upper, state.tau_upper)
    sensitivity_lower = compute_sensitivity(state.r_lower, state.tau_lower)
    dual_fluctuation = (
        config.dual_fluctuation_enabled
        and state.dtau_upper < 0.0
        and state.dtau_lower < 0.0
    )

    error_data = build_base_result("CRITICAL", state)
    error_data.update(
        {
            "sensitivity_upper": sensitivity_upper,
            "sensitivity_lower": sensitivity_lower,
            "dual_fluctuation": dual_fluctuation,
            "human_authority_required": True,
        }
    )

    upper_is_critical = state.r_upper >= config.irreversible_boundary
    lower_is_critical = state.r_lower >= config.irreversible_boundary

    if upper_is_critical and not lower_is_critical:
        error_data.update(
            {
                "branch": "CRITICAL_UPPER_ONLY",
                "message": "上方 R が不可逆判断限界に到達しました。膨張側破断リスクが高い状態です。",
            }
        )
        raise DualFluctuationError(
            "Upper critical: R_upper reached irreversible boundary.",
            "CRITICAL_UPPER_ONLY",
            error_data,
        )

    if lower_is_critical and not upper_is_critical:
        error_data.update(
            {
                "branch": "CRITICAL_LOWER_ONLY",
                "message": "下方 R が不可逆判断限界に到達しました。崩落側破断リスクが高い状態です。",
            }
        )
        raise DualFluctuationError(
            "Lower critical: R_lower reached irreversible boundary.",
            "CRITICAL_LOWER_ONLY",
            error_data,
        )

    error_data.update(
        {
            "branch": "CRITICAL_DUAL",
            "message": "上方 R と下方 R がともに不可逆判断限界へ接近しています。"
            "二重ゆらぎが強く、破断確率が高い状態です。",
        }
    )
    raise DualFluctuationError(
        "Dual critical: both branches reached irreversible boundary.",
        "CRITICAL_DUAL",
        error_data,
    )


class AISurvivalGateDual:
    """二重ゆらぎ状態を評価する外側ゲートです。"""

    def __init__(self, config: GateConfig | None = None) -> None:
        """設定を受け取り、前回状態の保存領域を初期化します。"""
        self.config = config or GateConfig()
        self.config.validate()
        self.previous_state: dict[str, Any] | None = None

    def is_allowed_to_output(self, gate_result: dict[str, Any]) -> bool:
        """ゲート結果から AI 出力の可否を返します。"""
        status = gate_result.get("status")
        if status == "PERMIT":
            return True
        if status == "CAUTION":
            return self.config.allow_caution_output
        return False

    def evaluate_with_dual(self, state: NraStateDual) -> dict[str, Any]:
        """状態を 1 ステップ進め、二重 R に基づくゲート結果を返します。"""
        state.update_tau()
        tau_upper = state.tau_dual.tau_upper
        tau_lower = state.tau_dual.tau_lower
        dtau_upper, dtau_lower = self._compute_dtau(tau_upper, tau_lower)

        dual_state = DualRState(
            r_upper=state.r_upper,
            r_lower=state.r_lower,
            r=state.r,
            tau_upper=tau_upper,
            tau_lower=tau_lower,
            dtau_upper=dtau_upper,
            dtau_lower=dtau_lower,
        )

        try:
            gate_result = handle_dual_threshold_exceeded(dual_state, self.config)
        except DualFluctuationError as error:
            gate_result = error.data

        gate_result["allowed_to_output"] = self.is_allowed_to_output(gate_result)
        gate_result["state"] = state.to_dict()
        self.previous_state = state.to_dict()
        return gate_result

    def _compute_dtau(self, tau_upper: float, tau_lower: float) -> tuple[float, float]:
        """前回保存した τ との差分を返します。"""
        if self.previous_state is None:
            return 0.0, 0.0
        return (
            tau_upper - float(self.previous_state["tau_upper"]),
            tau_lower - float(self.previous_state["tau_lower"]),
        )


def run_demo() -> None:
    """コマンドラインから実行したときの最小デモを表示します。"""
    print("=== 二重ゆらぎ + AI 生存基底ゲート 実行例 ===\n")

    ai_state = NraStateDual.from_parameters(
        value=0.6,
        threshold=0.55,
        buffer=0.02,
        rate=0.02,
        tau0_upper=0.05,
        tau0_lower=0.05,
        alpha_upper=0.1,
        alpha_lower=0.1,
    )
    gate = AISurvivalGateDual(
        GateConfig(
            irreversible_boundary=0.95,
            enable_inability_check=True,
        )
    )

    for step_index in range(10):
        print(f"--- Step {step_index} ---")
        gate_result = gate.evaluate_with_dual(ai_state)
        print("Gate Result:")
        print(json.dumps(gate_result, ensure_ascii=False, indent=2))
        ai_state.value = min(1.0, ai_state.value + 0.1)


if __name__ == "__main__":
    run_demo()
