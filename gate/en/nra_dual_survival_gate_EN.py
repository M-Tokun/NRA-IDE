# -*- coding: utf-8 -*-
# file: nra_dual_survival_gate_en_20260501_034016_JST.py
# generated_at_jst: 2026-05-01 03:40:16
"""
Nomological Ring Axioms (NRA-IDE) dual-fluctuation gate.

This single-file implementation is a minimal executable example that evaluates
upper and lower deviations as separate history systems around R = δ / τ. The
Python implementation uses snake_case names for Pylint compliance. The output
dictionary intentionally preserves the theory notation keys "R", "R_upper", and
"R_lower" so that logs remain readable as NRA-IDE records.

Refactoring summary:
- Removed the global statement and moved thresholds into GateConfig.
- Represented mathematical R as r inside Python while preserving R in logs.
- Added class and function docstrings.
- Avoided redefining names from outer scopes.
- Centralized threshold, inability, and dual-fluctuation options in one config.
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
    """Immutable configuration for gate judgment."""

    structural_boundary: float = STRUCTURAL_BOUNDARY
    warning_boundary: float = WARNING_BOUNDARY
    irreversible_boundary: float = DEFAULT_IRREVERSIBLE_BOUNDARY
    minimum_tau: float = MINIMUM_TAU
    allow_caution_output: bool = True
    enable_inability_check: bool = True
    dual_fluctuation_enabled: bool = True

    def validate(self) -> None:
        """Validate that the threshold configuration is structurally consistent."""
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
    """Stores upper and lower τ values and updates them with dual EMA."""

    tau_upper: float
    tau_lower: float
    alpha_upper: float = 0.1
    alpha_lower: float = 0.1
    minimum_tau: float = MINIMUM_TAU

    def __post_init__(self) -> None:
        """Normalize initial values and guarantee a minimum structural thickness."""
        self.tau_upper = self._clamp_tau(self.tau_upper)
        self.tau_lower = self._clamp_tau(self.tau_lower)
        self.alpha_upper = self._clamp_alpha(self.alpha_upper)
        self.alpha_lower = self._clamp_alpha(self.alpha_lower)
        self.minimum_tau = self._clamp_tau(self.minimum_tau)

    def update(self, delta_upper: float, delta_lower: float) -> None:
        """Update τ by one step from observed upper and lower deviations."""
        next_upper = self._ema(self.tau_upper, delta_upper, self.alpha_upper)
        next_lower = self._ema(self.tau_lower, delta_lower, self.alpha_lower)
        self.tau_upper = self._clamp_tau(next_upper)
        self.tau_lower = self._clamp_tau(next_lower)

    def to_dict(self) -> dict[str, float]:
        """Return τ state as a log-ready dictionary."""
        return {
            "tau_upper": self.tau_upper,
            "tau_lower": self.tau_lower,
            "alpha_upper": self.alpha_upper,
            "alpha_lower": self.alpha_lower,
        }

    def _clamp_tau(self, value: float) -> float:
        """Clamp τ to a strictly positive minimum."""
        return max(MINIMUM_TAU, float(value))

    @staticmethod
    def _clamp_alpha(value: float) -> float:
        """Clamp an EMA coefficient into the interval [0.0, 1.0]."""
        return max(0.0, min(1.0, float(value)))

    @staticmethod
    def _ema(previous_value: float, observed_value: float, alpha: float) -> float:
        """Compute one exponential-moving-average step."""
        return (1.0 - alpha) * previous_value + alpha * max(0.0, observed_value)


@dataclass
class NraStateDual:
    """Single state evaluated by the NRA-IDE dual-fluctuation gate."""

    value: float
    threshold: float
    buffer: float = 0.0
    rate: float = 0.0
    tau_dual: DualTau = field(default_factory=lambda: DualTau(0.05, 0.05))

    def __post_init__(self) -> None:
        """Normalize state values into the interval [0.0, 1.0]."""
        self.value = self._clamp_unit(self.value)
        self.threshold = self._clamp_unit(self.threshold)
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
        """Create a state from parameters close to the original implementation."""
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
        """Return the upper deviation as the standard δ value."""
        return self.delta_upper

    @property
    def delta_upper(self) -> float:
        """Return deviation above the threshold."""
        return max(0.0, self.value - self.threshold)

    @property
    def delta_lower(self) -> float:
        """Return deviation below the threshold."""
        return max(0.0, self.threshold - self.value)

    @property
    def r_upper(self) -> float:
        """Return upper-side R = δ_upper / τ_upper."""
        return safe_ratio(self.delta_upper, self.tau_dual.tau_upper)

    @property
    def r_lower(self) -> float:
        """Return lower-side R = δ_lower / τ_lower."""
        return safe_ratio(self.delta_lower, self.tau_dual.tau_lower)

    @property
    def r(self) -> float:
        """Return the stricter R among upper and lower branches."""
        return max(self.r_upper, self.r_lower)

    def update_tau(self) -> None:
        """Update the dual τ values from the current deviations."""
        self.tau_dual.update(self.delta_upper, self.delta_lower)

    def to_dict(self) -> dict[str, Any]:
        """Return a log dictionary that preserves theory notation."""
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
    def _clamp_unit(value: float) -> float:
        """Clamp a value into the interval [0.0, 1.0]."""
        return max(0.0, min(1.0, float(value)))


@dataclass(frozen=True)
class DualRState:
    """Snapshot of R and τ values used for branch judgment."""

    r_upper: float
    r_lower: float
    r: float
    tau_upper: float
    tau_lower: float
    dtau_upper: float
    dtau_lower: float

    def dominant_branch(self) -> tuple[str, float, float]:
        """Return the dominant branch name, R, and τ."""
        if self.r_upper >= self.r_lower:
            return "upper", self.r_upper, self.tau_upper
        return "lower", self.r_lower, self.tau_lower


class DualFluctuationError(Exception):
    """Indicates that the gate requires output blocking or human delegation."""

    def __init__(self, message: str, branch: str, data: dict[str, Any]) -> None:
        """Store exception message, branch name, and log data."""
        super().__init__(message)
        self.branch = branch
        self.data = data


def safe_ratio(delta_value: float, tau_value: float) -> float:
    """Return δ / τ, or infinity when τ is invalid."""
    if tau_value <= 0.0 or not math.isfinite(tau_value):
        return float("inf")
    return max(0.0, float(delta_value)) / tau_value


def compute_sensitivity(r_value: float, tau_value: float) -> float:
    """Compute a sensitivity index that grows as R approaches the boundary."""
    if tau_value <= 0.0 or r_value >= 1.0:
        return float("inf")
    return 1.0 / (tau_value * (1.0 - r_value))


def has_invalid_tau(state: DualRState) -> bool:
    """Return whether upper or lower τ is structurally invalid."""
    return (
        state.tau_upper <= 0.0
        or state.tau_lower <= 0.0
        or not math.isfinite(state.tau_upper)
        or not math.isfinite(state.tau_lower)
    )


def build_base_result(status: str, state: DualRState) -> dict[str, Any]:
    """Build the shared base dictionary for gate results."""
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
    """Return PERMIT, CAUTION, CRITICAL, or FAIL_CLOSED according to R."""
    if config.enable_inability_check and has_invalid_tau(state):
        error_data = build_base_result("INABILITY", state)
        error_data.update(
            {
                "message": "Structural inability: τ is non-positive or non-finite. "
                "No structural tolerance is available.",
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
                "message": "The dual-fluctuation structural boundary was crossed. "
                "R >= 1.0. No valid AI output is permitted. "
                "Delegation to human judgment is required.",
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
                "message": "R is in the elastic or warning domain; "
                "the trajectory must continue to be tracked.",
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
            "message": "Sufficient structural slack exists. AI output is permitted.",
            "action": "continue",
            "human_authority_required": False,
        }
    )
    return result_data


def raise_critical_error(state: DualRState, config: GateConfig) -> dict[str, Any]:
    """Raise branch-specific CRITICAL errors near the irreversible boundary."""
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
                "message": "Upper R reached the irreversible judgment boundary. "
                "The expansion-side fracture risk is high.",
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
                "message": "Lower R reached the irreversible judgment boundary. "
                "The collapse-side fracture risk is high.",
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
            "message": "Both upper R and lower R are approaching the irreversible "
            "judgment boundary. Dual fluctuation is strong, and the fracture "
            "probability is high.",
        }
    )
    raise DualFluctuationError(
        "Dual critical: both branches reached irreversible boundary.",
        "CRITICAL_DUAL",
        error_data,
    )


class AISurvivalGateDual:
    """Outer gate that evaluates dual-fluctuation states."""

    def __init__(self, config: GateConfig | None = None) -> None:
        """Receive configuration and initialize previous-state storage."""
        self.config = config or GateConfig()
        self.config.validate()
        self.previous_state: dict[str, Any] | None = None

    def is_allowed_to_output(self, gate_result: dict[str, Any]) -> bool:
        """Return whether AI output is allowed for the gate result."""
        status = gate_result.get("status")
        if status == "PERMIT":
            return True
        if status == "CAUTION":
            return self.config.allow_caution_output
        return False

    def evaluate_with_dual(self, state: NraStateDual) -> dict[str, Any]:
        """Advance the state by one step and return the dual-R gate result."""
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
        """Return differences from the previously stored τ values."""
        if self.previous_state is None:
            return 0.0, 0.0
        return (
            tau_upper - float(self.previous_state["tau_upper"]),
            tau_lower - float(self.previous_state["tau_lower"]),
        )


def run_demo() -> None:
    """Print a minimal command-line demo when this file is executed directly."""
    print("=== Dual Fluctuation + AI Survival Basis Gate Execution Example ===\n")

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
