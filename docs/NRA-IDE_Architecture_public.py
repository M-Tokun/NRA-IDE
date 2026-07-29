"""NRA-IDE v2.1 normative reference implementation.

The state machine in this file follows theory/AXIOMS.md and
theory/axioms.json.  The docs copy is generated from this source and must
remain byte-identical.  Location alone does not confer conformance; the
reference tests must pass.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional


OBSERVATION_CHANNEL_STATES = {"ACTIVE", "OBSERVATION_LOST", "NOT_OBSERVABLE"}
LOGGING_CHANNEL_STATES = {"ACTIVE", "LOGGING_LOST"}
COMMUNICATION_CHANNEL_STATES = {"ACTIVE", "COMMUNICATION_LOST"}
EXECUTION_AUTHORITY_STATES = {"AUTONOMOUS_CURRENT_PATH", "EXTERNAL_PREDEFINED"}
STRUCTURAL_TESTIMONY_MODES = {"CONTINUOUS", "POST_RUPTURE_FIXED"}


FIXED_STRUCTURAL_NOTICE_SCHEMA: Dict[str, Any] = {
    "status": "string",
    "code": "string",
    "message": "string",
    "observed_delta": "Optional[float]",
    "observed_tau": "Optional[float]",
    "R": "Optional[float]",
    "thresholds": "Optional[dict]",
    "remaining_ratio_margin": "Optional[float]",
    "remaining_absorption_margin": "Optional[float]",
    "remaining_slack": "Optional[float]",
    "trend": "string",
    "double_fluctuation": "dict",
    "dominant_side": "Optional[str]",
    "missing_information": "list[str]",
    "structural_disclosure_log": "list[str]",
    "input_exception_log": "list[str]",
    "audit_log": "list[str]",
    "autonomous_new_judgment": "bool",
    "autonomous_new_operation": "bool",
    "declared_target": "string",
    "target_state": "Optional[str]",
    "observation_state": "string",
    "observation_channels": "list[dict]",
    "logging_state": "string",
    "communication_state": "string",
    "execution_authority": "string",
    "authority_transfer_scope": "list[str]",
    "structural_testimony_route": "string",
    "audit_log_route": "string",
    "audit_log_custody": "string",
    "structural_testimony_mode": "string",
    "structural_testimony": "string",
    "irreversible_latched": "bool",
}


def _finite_number(value: Any) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(float(value))
    except (OverflowError, TypeError, ValueError):
        return False


def _double_fluctuation(
    d_delta_dt: Any = None, d_tau_dt: Any = None
) -> Dict[str, Any]:
    if d_delta_dt is None or d_tau_dt is None:
        missing = []
        if d_delta_dt is None:
            missing.append("d_delta_dt")
        if d_tau_dt is None:
            missing.append("d_tau_dt")
        return {
            "status": "NOT_OBSERVABLE",
            "detected": None,
            "reason": "missing Cause-Side derivative observation: " + ", ".join(missing),
        }
    if not _finite_number(d_delta_dt) or not _finite_number(d_tau_dt):
        return {
            "status": "NOT_OBSERVABLE",
            "detected": None,
            "reason": "derivative observations must be finite Cause-Side values",
        }
    detected = d_delta_dt > 0 and d_tau_dt < 0
    return {
        "status": "DETECTED" if detected else "NOT_DETECTED",
        "detected": detected,
        "d_delta_dt": float(d_delta_dt),
        "d_tau_dt": float(d_tau_dt),
        "reason": None,
    }


class ObservationChannelRegistry:
    """Keep channel loss separate from target rupture and preserve last-valid data."""

    def __init__(self) -> None:
        self._channels: Dict[str, Dict[str, Any]] = {}

    def observe(
        self,
        sensor_id: str,
        value: Any,
        timestamp: str,
        *,
        health_state: str = "HEALTHY",
        power_state: str = "ON",
        communication_state: str = "ACTIVE",
        source_lineage: Optional[str] = None,
        audit_lineage: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not isinstance(sensor_id, str) or not sensor_id:
            raise ValueError("sensor_id must be a non-empty string.")
        if not _finite_number(value):
            raise ValueError("observation value must be finite; missing data must not be replaced by zero.")
        if not isinstance(timestamp, str) or not timestamp:
            raise ValueError("timestamp must be a non-empty string.")
        if communication_state not in COMMUNICATION_CHANNEL_STATES:
            raise ValueError("communication_state is not canonical.")
        channel = {
            "sensor_id": sensor_id,
            "state": "ACTIVE",
            "last_valid_value": float(value),
            "last_valid_timestamp": timestamp,
            "missing_since": None,
            "last_confirmed_health_state": health_state,
            "power_state": power_state,
            "communication_state": communication_state,
            "unavailability_reason": None,
            "reason_unknown": False,
            "source_lineage": source_lineage,
            "audit_lineage": audit_lineage,
        }
        self._channels[sensor_id] = channel
        return dict(channel)

    def mark_lost(
        self,
        sensor_id: str,
        missing_since: str,
        *,
        reason: Optional[str] = None,
        health_state: Optional[str] = None,
        power_state: Optional[str] = None,
        communication_state: str = "ACTIVE",
    ) -> Dict[str, Any]:
        if not isinstance(sensor_id, str) or not sensor_id:
            raise ValueError("sensor_id must be a non-empty string.")
        if not isinstance(missing_since, str) or not missing_since:
            raise ValueError("missing_since must be a non-empty string.")
        if communication_state not in COMMUNICATION_CHANNEL_STATES:
            raise ValueError("communication_state is not canonical.")
        previous = self._channels.get(sensor_id, {})
        channel = {
            "sensor_id": sensor_id,
            "state": "OBSERVATION_LOST",
            "last_valid_value": previous.get("last_valid_value"),
            "last_valid_timestamp": previous.get("last_valid_timestamp"),
            "missing_since": missing_since,
            "last_confirmed_health_state": health_state
            if health_state is not None
            else previous.get("last_confirmed_health_state"),
            "power_state": power_state if power_state is not None else previous.get("power_state"),
            "communication_state": communication_state,
            "unavailability_reason": reason,
            "reason_unknown": reason is None,
            "source_lineage": previous.get("source_lineage"),
            "audit_lineage": previous.get("audit_lineage"),
        }
        self._channels[sensor_id] = channel
        return dict(channel)

    def snapshot(self) -> List[Dict[str, Any]]:
        return [dict(channel) for channel in self._channels.values()]


def _normalize_observation_channels(channels: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    if channels is None:
        return []
    if not isinstance(channels, list):
        raise ValueError("observation_channels must be a list.")
    normalized: List[Dict[str, Any]] = []
    seen = set()
    for channel in channels:
        if not isinstance(channel, dict):
            raise ValueError("each observation channel must be a dictionary.")
        sensor_id = channel.get("sensor_id")
        state = channel.get("state")
        if not isinstance(sensor_id, str) or not sensor_id or sensor_id in seen:
            raise ValueError("sensor_id must be unique and non-empty.")
        if state not in OBSERVATION_CHANNEL_STATES:
            raise ValueError("observation channel state is not canonical.")
        if state == "ACTIVE":
            if not _finite_number(channel.get("last_valid_value")):
                raise ValueError("ACTIVE channels require a finite last_valid_value.")
            if not isinstance(channel.get("last_valid_timestamp"), str) or not channel.get(
                "last_valid_timestamp"
            ):
                raise ValueError("ACTIVE channels require last_valid_timestamp.")
        if state != "ACTIVE" and channel.get("last_valid_value") is not None:
            if not _finite_number(channel.get("last_valid_value")):
                raise ValueError("last-valid observation metadata must remain finite.")
        normalized.append(dict(channel))
        seen.add(sensor_id)
    return normalized


def _aggregate_observation_state(channels: List[Dict[str, Any]]) -> str:
    states = {channel["state"] for channel in channels}
    if "ACTIVE" in states:
        return "ACTIVE"
    if "OBSERVATION_LOST" in states:
        return "OBSERVATION_LOST"
    return "NOT_OBSERVABLE"


def _notice(
    status: str,
    code: str,
    message: str,
    *,
    delta: Any = None,
    tau: Any = None,
    ratio: Optional[float] = None,
    thresholds: Optional[Dict[str, float]] = None,
    trend: Optional[str] = None,
    double_fluctuation: Optional[Dict[str, Any]] = None,
    missing: Optional[List[str]] = None,
    structural_disclosure_log: Optional[List[str]] = None,
    input_exception_log: Optional[List[str]] = None,
    audit_log: Optional[List[str]] = None,
    irreversible_latched: bool = False,
    declared_target: str = "DECLARED_TARGET",
    observation_channels: Optional[List[Dict[str, Any]]] = None,
    logging_state: str = "ACTIVE",
    communication_state: str = "ACTIVE",
    execution_authority: str = "AUTONOMOUS_CURRENT_PATH",
    testimony_mode: str = "CONTINUOUS",
    autonomous: bool = False,
) -> Dict[str, Any]:
    normalized_channels = _normalize_observation_channels(observation_channels)
    remaining_absorption_margin = None
    if _finite_number(delta) and _finite_number(tau):
        remaining_absorption_margin = float(tau) - float(delta)
    remaining_ratio_margin = None
    if ratio is not None and _finite_number(ratio):
        remaining_ratio_margin = 1.0 - float(ratio)

    disclosure_entries = list(structural_disclosure_log or [])
    exception_entries = list(input_exception_log or [])
    legacy_entries = list(audit_log or [])
    record = f"{code}: {message}"
    if status in {"CONFESSION", "OUT_OF_DESCRIPTION_DOMAIN"}:
        exception_entries.extend(legacy_entries)
        if record not in exception_entries:
            exception_entries.append(record)
    else:
        disclosure_entries.extend(legacy_entries)
        if record not in disclosure_entries:
            disclosure_entries.append(record)
    return {
        "status": status,
        "code": code,
        "message": message,
        "observed_delta": float(delta) if _finite_number(delta) else None,
        "observed_tau": float(tau) if _finite_number(tau) else None,
        "R": ratio,
        "thresholds": thresholds,
        "remaining_ratio_margin": remaining_ratio_margin,
        "remaining_absorption_margin": remaining_absorption_margin,
        # Deprecated compatibility alias for remaining_absorption_margin.
        "remaining_slack": remaining_absorption_margin,
        "trend": trend if trend is not None else "NOT_OBSERVABLE",
        "double_fluctuation": double_fluctuation or _double_fluctuation(),
        "dominant_side": None,
        "missing_information": list(missing or []),
        "structural_disclosure_log": disclosure_entries,
        "input_exception_log": exception_entries,
        # Deprecated combined compatibility view; canonical logs stay separate.
        "audit_log": disclosure_entries + exception_entries,
        "autonomous_new_judgment": autonomous,
        "autonomous_new_operation": autonomous,
        "declared_target": declared_target,
        "target_state": status
        if status
        in {
            "PERMIT",
            "BOUNDARY_WARNING",
            "HANDOFF_REQUIRED",
            "IRREVERSIBLE_TRANSITION",
            "RUPTURE_BOUNDARY",
        }
        else None,
        "observation_state": _aggregate_observation_state(normalized_channels),
        "observation_channels": normalized_channels,
        "logging_state": logging_state,
        "communication_state": communication_state,
        "execution_authority": execution_authority,
        "authority_transfer_scope": ["execution_authority"]
        if execution_authority == "EXTERNAL_PREDEFINED"
        else [],
        "structural_testimony_route": "ACTIVE",
        "audit_log_route": "ACTIVE" if logging_state == "ACTIVE" else "LOGGING_LOST",
        "audit_log_custody": "DOMAIN_DEFINED_UNCHANGED_BY_HANDOFF",
        "structural_testimony_mode": testimony_mode,
        # Compatibility view; canonical callers use structural_testimony_mode.
        "structural_testimony": testimony_mode,
        "irreversible_latched": irreversible_latched,
    }


def _confession(
    detail: str,
    *,
    delta: Any = None,
    tau: Any = None,
    missing: Optional[List[str]] = None,
    input_exception_log: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return _notice(
        "CONFESSION",
        "INVALID_OR_UNKNOWN_STRUCTURAL_INPUT",
        detail,
        delta=delta,
        tau=tau,
        missing=missing,
        input_exception_log=input_exception_log,
    )


def nra_ide_core_evaluation(
    delta: Any,
    tau: Any,
    rop: Any = None,
    *,
    r_warn: Any = None,
    r_handoff: Any = None,
    r_op: Any = None,
    r_irrev: Any = None,
    irreversible_latched: bool = False,
    d_delta_dt: Any = None,
    d_tau_dt: Any = None,
    trend: Optional[str] = None,
    input_side: str = "CAUSE_SIDE",
    declared_target: str = "DECLARED_TARGET",
    observation_channels: Optional[List[Dict[str, Any]]] = None,
    logging_state: str = "ACTIVE",
    communication_state: str = "ACTIVE",
    structural_disclosure_log: Optional[List[str]] = None,
    input_exception_log: Optional[List[str]] = None,
    audit_log: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Evaluate one canonical state without inferring missing domain rules.

    ``r_handoff`` is canonical. ``r_op`` and positional ``rop`` are retained
    only as compatibility aliases. Legacy calls lacking ``r_warn`` or
    ``r_irrev`` return CONFESSION instead of guessing.
    """
    double = _double_fluctuation(d_delta_dt, d_tau_dt)
    if not isinstance(declared_target, str) or not declared_target:
        return _confession(
            "declared_target must be a non-empty string fixed before evaluation.",
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )
    if logging_state not in LOGGING_CHANNEL_STATES:
        return _confession(
            "logging_state is not canonical.",
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )
    if communication_state not in COMMUNICATION_CHANNEL_STATES:
        return _confession(
            "communication_state is not canonical.",
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )
    try:
        normalized_channels = _normalize_observation_channels(observation_channels)
    except ValueError as error:
        return _confession(
            str(error),
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )
    if input_side != "CAUSE_SIDE":
        return _confession(
            "Structural variables must come from Cause-Side observations or pre-fixed Cause-Side transformations.",
            delta=delta,
            tau=tau,
            missing=["Cause-Side authority"],
            input_exception_log=input_exception_log or audit_log,
        )
    if not _finite_number(delta) or not _finite_number(tau):
        return _confession(
            "delta and tau must be finite real Cause-Side values.",
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )
    delta = float(delta)
    tau = float(tau)
    if tau < 0.0 or delta < 0.0:
        return _confession(
            "delta must be non-negative and tau must not be negative.",
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )
    if tau == 0.0:
        return _notice(
            "OUT_OF_DESCRIPTION_DOMAIN",
            "TAU_EQ_0",
            "R is undefined because tau = 0.",
            delta=delta,
            tau=tau,
            double_fluctuation=double,
            missing=["defined canonical R"],
            input_exception_log=input_exception_log or audit_log,
            declared_target=declared_target,
            observation_channels=normalized_channels,
            logging_state=logging_state,
            communication_state=communication_state,
            testimony_mode="CONTINUOUS",
        )
    if not isinstance(irreversible_latched, bool):
        return _confession(
            "irreversible_latched must be a boolean.",
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )
    if trend is not None and not isinstance(trend, str):
        return _confession(
            "trend must be a string or None.",
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )

    handoff_values = [
        (name, value)
        for name, value in (("r_handoff", r_handoff), ("r_op", r_op), ("rop", rop))
        if value is not None
    ]
    if handoff_values:
        r_handoff = handoff_values[0][1]
        if any(value != r_handoff for _, value in handoff_values[1:]):
            return _confession(
                "r_handoff and its legacy aliases provide conflicting handoff thresholds.",
                delta=delta,
                tau=tau,
                input_exception_log=input_exception_log or audit_log,
            )
    missing_thresholds = [
        name
        for name, value in (("R_warn", r_warn), ("R_handoff", r_handoff), ("R_irrev", r_irrev))
        if value is None
    ]
    if missing_thresholds:
        return _confession(
            "Canonical threshold rules are incomplete; values were not inferred.",
            delta=delta,
            tau=tau,
            missing=missing_thresholds,
            input_exception_log=input_exception_log or audit_log,
        )
    if not all(_finite_number(v) for v in (r_warn, r_handoff, r_irrev)):
        return _confession(
            "Canonical thresholds must be finite real values.",
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )
    r_warn, r_handoff, r_irrev = float(r_warn), float(r_handoff), float(r_irrev)
    if not (0.0 <= r_warn < r_handoff < r_irrev < 1.0):
        return _confession(
            "Thresholds must satisfy 0 <= R_warn < R_handoff < R_irrev < 1.0.",
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )

    ratio = delta / tau
    if not math.isfinite(ratio):
        return _confession(
            "Canonical R could not be represented as a finite value; inputs were not converted to infinite R.",
            delta=delta,
            tau=tau,
            input_exception_log=input_exception_log or audit_log,
        )
    thresholds = {"R_warn": r_warn, "R_handoff": r_handoff, "R_irrev": r_irrev}
    common = dict(
        delta=delta,
        tau=tau,
        ratio=ratio,
        thresholds=thresholds,
        trend=trend,
        double_fluctuation=double,
        structural_disclosure_log=structural_disclosure_log,
        input_exception_log=input_exception_log,
        audit_log=audit_log,
        declared_target=declared_target,
        observation_channels=normalized_channels,
        logging_state=logging_state,
        communication_state=communication_state,
    )
    if ratio >= 1.0:
        return _notice(
            "RUPTURE_BOUNDARY",
            "R_GE_1",
            "Declared target reached the invariant complete-rupture boundary; continuing post-rupture fixed testimony is active.",
            irreversible_latched=True,
            execution_authority="EXTERNAL_PREDEFINED",
            testimony_mode="POST_RUPTURE_FIXED",
            **common,
        )
    if irreversible_latched or ratio >= r_irrev:
        return _notice(
            "IRREVERSIBLE_TRANSITION",
            "IRREVERSIBLE_LATCHED" if irreversible_latched else "R_GE_R_IRREV",
            "Irreversible transition is active; ordinary generation and autonomous action are prohibited.",
            irreversible_latched=True,
            execution_authority="EXTERNAL_PREDEFINED",
            testimony_mode="CONTINUOUS",
            **common,
        )
    if ratio >= r_handoff:
        return _notice(
            "HANDOFF_REQUIRED",
            "R_GE_R_HANDOFF",
            "Execution authority only is transferred to the predefined external authority; testimony and audit routes continue.",
            execution_authority="EXTERNAL_PREDEFINED",
            testimony_mode="CONTINUOUS",
            **common,
        )
    if ratio >= r_warn:
        missing = []
        if trend is None:
            missing.append("trend observation")
        if double["status"] == "NOT_OBSERVABLE":
            missing.append("double fluctuation observation")
        missing.append("dominant side not supplied by canonical single-ratio evaluation")
        return _notice(
            "BOUNDARY_WARNING",
            "R_GE_R_WARN",
            "Boundary approach warning; disclose state, trend, and missing information.",
            missing=missing,
            autonomous=True,
            testimony_mode="CONTINUOUS",
            **common,
        )
    return _notice(
        "PERMIT",
        "R_LT_R_WARN",
        "Canonical state is below the warning threshold.",
        autonomous=True,
        testimony_mode="CONTINUOUS",
        **common,
    )


def detect_double_fluctuation(d_delta_dt: Any, d_tau_dt: Any) -> Dict[str, Any]:
    """Return the required explicit double-fluctuation status field."""
    return _double_fluctuation(d_delta_dt, d_tau_dt)


def calculate_structural_sensitivity(delta: Any, tau: Any) -> Optional[float]:
    if not _finite_number(delta) or not _finite_number(tau):
        return None
    if delta < 0 or tau <= 0 or delta >= tau:
        return None
    return 1.0 / (tau - delta)


class DynamicTauEngine:
    """Compute directional auxiliary ratios; never classify canonical state."""

    def __init__(
        self,
        initial_tau: float,
        alpha_upper: float,
        alpha_lower: float,
        max_tau_factor: float = 2.0,
        min_tau_factor: float = 0.1,
        k_upper: float = 1.0,
        k_lower: float = 1.0,
    ) -> None:
        values = (initial_tau, alpha_upper, alpha_lower, max_tau_factor, min_tau_factor, k_upper, k_lower)
        if not all(_finite_number(value) for value in values):
            raise ValueError("DynamicTauEngine parameters must be finite real values.")
        if initial_tau <= 0 or not (0 < alpha_upper <= 1 and 0 < alpha_lower <= 1):
            raise ValueError("initial_tau and alpha values are outside their domains.")
        if max_tau_factor <= 1 or not (0 < min_tau_factor < 1) or k_upper <= 0 or k_lower <= 0:
            raise ValueError("Dynamic tau shape parameters are outside their domains.")
        self._initial_tau = float(initial_tau)
        self._alpha_upper = float(alpha_upper)
        self._alpha_lower = float(alpha_lower)
        self._max_tau_factor = float(max_tau_factor)
        self._min_tau_factor = float(min_tau_factor)
        self._k_upper = float(k_upper)
        self._k_lower = float(k_lower)
        self._ema_upper: Optional[float] = None
        self._ema_lower: Optional[float] = None

    @property
    def initial_tau(self) -> float:
        return self._initial_tau

    def calculate_directional_auxiliary(self, current_delta_upper: Any, current_delta_lower: Any) -> Dict[str, Any]:
        if not _finite_number(current_delta_upper) or not _finite_number(current_delta_lower):
            return _confession("Directional deviations must be finite Cause-Side values.")
        if current_delta_upper < 0 or current_delta_lower < 0:
            return _confession("Directional deviations must be non-negative.")
        current_delta_upper = float(current_delta_upper)
        current_delta_lower = float(current_delta_lower)
        next_upper = (
            current_delta_upper
            if self._ema_upper is None
            else self._alpha_upper * current_delta_upper
            + (1 - self._alpha_upper) * self._ema_upper
        )
        next_lower = (
            current_delta_lower
            if self._ema_lower is None
            else self._alpha_lower * current_delta_lower
            + (1 - self._alpha_lower) * self._ema_lower
        )
        if not math.isfinite(next_upper) or not math.isfinite(next_lower):
            return _confession("Directional EMA update produced a non-finite value.")
        self._ema_upper = next_upper
        self._ema_lower = next_lower
        upper_logistic = 2.0 / (1.0 + math.exp(-self._k_upper * self._ema_upper)) - 1.0
        lower_z = self._k_lower * self._ema_lower
        lower_logistic = 0.0 if lower_z > 709.0 else 2.0 / (1.0 + math.exp(lower_z))
        h_upper = 1.0 + (self._max_tau_factor - 1.0) * upper_logistic
        h_lower = self._min_tau_factor + (1.0 - self._min_tau_factor) * lower_logistic
        tau_upper = self._initial_tau * h_upper
        tau_lower = self._initial_tau * h_lower
        r_upper = current_delta_upper / tau_upper
        r_lower = current_delta_lower / tau_lower
        if not all(
            math.isfinite(value)
            for value in (h_upper, h_lower, tau_upper, tau_lower, r_upper, r_lower)
        ):
            return _confession("Directional auxiliary calculation produced a non-finite value.")
        if r_upper > r_lower:
            dominant_side = "upper"
        elif r_lower > r_upper:
            dominant_side = "lower"
        else:
            dominant_side = "tie"
        return {
            "status": "DIRECTIONAL_AUXILIARY_ONLY",
            "tau_upper": tau_upper,
            "tau_lower": tau_lower,
            "R_upper": r_upper,
            "R_lower": r_lower,
            "R_dir": max(r_upper, r_lower),
            "dominant_side": dominant_side,
            "canonical_state_classified": False,
        }

    def calculate_r_dynamic(self, current_delta_upper: Any, current_delta_lower: Any, rop: Any = None) -> Dict[str, Any]:
        """Compatibility alias; ``rop`` is ignored because R_dir is auxiliary."""
        result = self.calculate_directional_auxiliary(current_delta_upper, current_delta_lower)
        result["legacy_rop_ignored"] = rop is not None
        return result


def pre_nra_input_gate(raw_input: Any) -> Dict[str, Any]:
    if not isinstance(raw_input, dict):
        return _confession("Pre-NRA input must be a dictionary.")
    missing = [name for name in ("delta", "tau") if name not in raw_input]
    if missing:
        return _confession("Pre-NRA input is missing required variables.", missing=missing)
    if raw_input.get("input_side", "CAUSE_SIDE") != "CAUSE_SIDE":
        return _confession("Pre-NRA rejected Effect-Side structural authority.")
    return {**raw_input, "status": "SANITIZED_INPUT"}


def llm_generation_device(context: str, instruction: str) -> str:
    return f"[UNVALIDATED EFFECT-SIDE OUTPUT] Context: {context}. Instruction: {instruction}."


def post_nra_output_gate(
    llm_output: str,
    structural_data: Dict[str, Any],
    current_delta: Any,
    current_tau: Any,
    current_rop: Any = None,
    dynamic_engine: Optional[DynamicTauEngine] = None,
) -> Dict[str, Any]:
    result = nra_ide_core_evaluation(
        current_delta,
        current_tau,
        current_rop,
        r_warn=structural_data.get("r_warn"),
        r_handoff=structural_data.get("r_handoff"),
        r_op=structural_data.get("r_op"),
        r_irrev=structural_data.get("r_irrev"),
        irreversible_latched=structural_data.get("irreversible_latched", False),
        d_delta_dt=structural_data.get("d_delta_dt"),
        d_tau_dt=structural_data.get("d_tau_dt"),
        trend=structural_data.get("trend"),
        input_side=structural_data.get("input_side", "CAUSE_SIDE"),
        declared_target=structural_data.get("declared_target", "DECLARED_TARGET"),
        observation_channels=structural_data.get("observation_channels"),
        logging_state=structural_data.get("logging_state", "ACTIVE"),
        communication_state=structural_data.get("communication_state", "ACTIVE"),
    )
    if dynamic_engine is not None:
        result["directional_auxiliary"] = dynamic_engine.calculate_directional_auxiliary(
            structural_data.get("delta_upper"), structural_data.get("delta_lower")
        )
    if result["status"] in {"PERMIT", "BOUNDARY_WARNING"}:
        return {
            "status": result["status"],
            "validated_output": llm_output,
            "nra_status": result,
        }
    return {"status": result["status"], "message": result["message"], "nra_status": result}


class DiscardVault:
    _vault: List[Any] = []

    @classmethod
    def store(cls, item: Any) -> None:
        cls._vault.append(item)

    @classmethod
    def retrieve_all(cls) -> List[Any]:
        return list(cls._vault)


def simulate_nra_ide_pipeline(
    raw_input_data: Dict[str, Any],
    llm_instruction: str,
    dynamic_engine: Optional[DynamicTauEngine] = None,
) -> Dict[str, Any]:
    sanitized = pre_nra_input_gate(raw_input_data)
    if sanitized["status"] != "SANITIZED_INPUT":
        return sanitized
    llm_output = llm_generation_device(str(sanitized), llm_instruction)
    return post_nra_output_gate(
        llm_output,
        sanitized,
        sanitized["delta"],
        sanitized["tau"],
        sanitized.get("r_handoff", sanitized.get("r_op", sanitized.get("rop"))),
        dynamic_engine,
    )
