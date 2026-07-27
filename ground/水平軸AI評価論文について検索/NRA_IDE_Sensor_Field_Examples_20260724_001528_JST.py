#!/usr/bin/env python3
# FILE: NRA_IDE_Sensor_Field_Examples_20260724_001528_JST.py
# CREATED: 2026-07-24 00:15:28 JST
"""
NRA-IDE sensor field examples.

This reference implementation demonstrates three Cause-Side sensor gates:
1. Tank inflow/outflow/level mass-balance monitoring.
2. Multi-point low-temperature boundary monitoring.
3. Motor vibration/temperature/current boundary monitoring.

Important:
- Numerical thresholds are illustrative and must be calibrated for the real site.
- This program does not directly actuate machinery.
- A certified hardware interlock or safety PLC must remain independent.
- Effect-Side AI output must not rewrite delta, tau, or R.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from statistics import fmean
from typing import Any, Iterable, Optional


class Zone(str, Enum):
    NORMAL = "NORMAL"
    WARN = "WARN"
    HUMAN_HANDOFF = "HUMAN_HANDOFF"
    IRREVERSIBLE_ONSET = "IRREVERSIBLE_ONSET"
    FAIL_CLOSED = "FAIL_CLOSED"
    OUT_OF_DESCRIPTION_DOMAIN = "OUT_OF_DESCRIPTION_DOMAIN"


@dataclass(frozen=True)
class Thresholds:
    r_warn: float = 0.40
    r_op: float = 0.70
    r_irrev: float = 0.90
    r_fail: float = 1.00

    def __post_init__(self) -> None:
        if not (
            0.0
            <= self.r_warn
            < self.r_op
            < self.r_irrev
            < self.r_fail
            == 1.0
        ):
            raise ValueError(
                "Required order: 0 <= R_warn < R_op < R_irrev < R_fail == 1.0"
            )


@dataclass
class GateResult:
    example: str
    timestamp_utc: str
    zone: Zone
    autonomy_allowed: bool
    delta: Optional[float]
    tau: Optional[float]
    r: Optional[float]
    unit: str
    action: str
    measurements: dict[str, Any]
    notes: list[str]

    def to_json(self) -> str:
        payload = asdict(self)
        payload["zone"] = self.zone.value
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def classify_r(r: float, thresholds: Thresholds) -> Zone:
    if r >= thresholds.r_fail:
        return Zone.FAIL_CLOSED
    if r >= thresholds.r_irrev:
        return Zone.IRREVERSIBLE_ONSET
    if r >= thresholds.r_op:
        return Zone.HUMAN_HANDOFF
    if r >= thresholds.r_warn:
        return Zone.WARN
    return Zone.NORMAL


def action_for_zone(zone: Zone) -> tuple[bool, str]:
    actions = {
        Zone.NORMAL: (True, "Continue bounded monitoring."),
        Zone.WARN: (True, "Increase observation frequency and issue a warning."),
        Zone.HUMAN_HANDOFF: (
            False,
            "Remove autonomous authority and hand off to a human operator.",
        ),
        Zone.IRREVERSIBLE_ONSET: (
            False,
            "Keep autonomy disabled; preserve fixed structural testimony.",
        ),
        Zone.FAIL_CLOSED: (
            False,
            "Block ordinary autonomous output; use only the prewired safe-state path.",
        ),
        Zone.OUT_OF_DESCRIPTION_DOMAIN: (
            False,
            "R is undefined. Block autonomy and use independent hardware/manual fallback.",
        ),
    }
    return actions[zone]


def out_of_domain_result(
    example: str,
    unit: str,
    measurements: dict[str, Any],
    reason: str,
) -> GateResult:
    autonomy_allowed, action = action_for_zone(Zone.OUT_OF_DESCRIPTION_DOMAIN)
    return GateResult(
        example=example,
        timestamp_utc=now_utc_iso(),
        zone=Zone.OUT_OF_DESCRIPTION_DOMAIN,
        autonomy_allowed=autonomy_allowed,
        delta=None,
        tau=None,
        r=None,
        unit=unit,
        action=action,
        measurements=measurements,
        notes=[reason],
    )


# ---------------------------------------------------------------------------
# Example 1: tank mass-balance gate
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TankConfig:
    diameter_m: float
    sigma_level_m: float
    sigma_q_in_m3_s: float
    sigma_q_out_m3_s: float
    process_margin_m3_s: float
    uncertainty_coverage_k: float = 3.0
    ewma_alpha: float = 0.35

    def __post_init__(self) -> None:
        positive = (
            self.diameter_m,
            self.sigma_level_m,
            self.sigma_q_in_m3_s,
            self.sigma_q_out_m3_s,
            self.process_margin_m3_s,
            self.uncertainty_coverage_k,
        )
        if any(value <= 0.0 for value in positive):
            raise ValueError("Tank configuration values must be positive.")
        if not 0.0 < self.ewma_alpha <= 1.0:
            raise ValueError("ewma_alpha must be in (0, 1].")

    @property
    def area_m2(self) -> float:
        return math.pi * (self.diameter_m**2) / 4.0


class TankMassBalanceGate:
    def __init__(
        self,
        config: TankConfig,
        thresholds: Thresholds = Thresholds(),
    ) -> None:
        self.config = config
        self.thresholds = thresholds
        self._delta_ewma_m3_s: Optional[float] = None

    def evaluate(
        self,
        *,
        previous_level_m: Optional[float],
        current_level_m: Optional[float],
        q_in_m3_s: Optional[float],
        q_out_m3_s: Optional[float],
        dt_s: Optional[float],
    ) -> GateResult:
        measurements = {
            "previous_level_m": previous_level_m,
            "current_level_m": current_level_m,
            "q_in_m3_s": q_in_m3_s,
            "q_out_m3_s": q_out_m3_s,
            "dt_s": dt_s,
        }
        required = (
            previous_level_m,
            current_level_m,
            q_in_m3_s,
            q_out_m3_s,
            dt_s,
        )
        if not all(is_finite_number(value) for value in required):
            return out_of_domain_result(
                "tank_mass_balance",
                "m3/s",
                measurements,
                "A required Cause-Side sensor value is missing or non-finite.",
            )
        assert dt_s is not None
        if dt_s <= 0.0:
            return out_of_domain_result(
                "tank_mass_balance",
                "m3/s",
                measurements,
                "dt_s must be greater than zero.",
            )

        area = self.config.area_m2
        observed_storage_rate = (
            area * (float(current_level_m) - float(previous_level_m)) / dt_s
        )
        expected_storage_rate = float(q_in_m3_s) - float(q_out_m3_s)
        residual = observed_storage_rate - expected_storage_rate
        absolute_residual = abs(residual)

        if self._delta_ewma_m3_s is None:
            self._delta_ewma_m3_s = absolute_residual
        else:
            alpha = self.config.ewma_alpha
            self._delta_ewma_m3_s = (
                alpha * absolute_residual
                + (1.0 - alpha) * self._delta_ewma_m3_s
            )

        # Uncertainty of A*(h_k-h_k-1)/dt includes two level measurements.
        u_level_rate = (
            area * math.sqrt(2.0) * self.config.sigma_level_m / dt_s
        )
        u_combined = math.sqrt(
            u_level_rate**2
            + self.config.sigma_q_in_m3_s**2
            + self.config.sigma_q_out_m3_s**2
        )
        tau = (
            self.config.uncertainty_coverage_k * u_combined
            + self.config.process_margin_m3_s
        )
        if tau <= 0.0 or not math.isfinite(tau):
            return out_of_domain_result(
                "tank_mass_balance",
                "m3/s",
                measurements,
                "tau is not finite and positive.",
            )

        delta = self._delta_ewma_m3_s
        r = delta / tau
        zone = classify_r(r, self.thresholds)
        autonomy_allowed, action = action_for_zone(zone)

        measurements.update(
            {
                "tank_area_m2": area,
                "observed_storage_rate_m3_s": observed_storage_rate,
                "expected_storage_rate_m3_s": expected_storage_rate,
                "instantaneous_residual_m3_s": residual,
                "combined_standard_uncertainty_m3_s": u_combined,
            }
        )
        return GateResult(
            example="tank_mass_balance",
            timestamp_utc=now_utc_iso(),
            zone=zone,
            autonomy_allowed=autonomy_allowed,
            delta=delta,
            tau=tau,
            r=r,
            unit="m3/s",
            action=action,
            measurements=measurements,
            notes=[
                "delta is an EWMA of the absolute Cause-Side balance residual.",
                "tau combines sensor uncertainty and a calibrated process margin.",
            ],
        )


# ---------------------------------------------------------------------------
# Example 2: multi-point low-temperature boundary gate
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FrostConfig:
    operating_floor_c: float
    complete_boundary_c: float
    min_sensor_c: float = -50.0
    max_sensor_c: float = 80.0

    def __post_init__(self) -> None:
        if self.operating_floor_c <= self.complete_boundary_c:
            raise ValueError(
                "operating_floor_c must be above complete_boundary_c."
            )
        if self.min_sensor_c >= self.max_sensor_c:
            raise ValueError("Invalid sensor plausibility range.")

    @property
    def tau_c(self) -> float:
        return self.operating_floor_c - self.complete_boundary_c


class FrostBoundaryGate:
    def __init__(
        self,
        config: FrostConfig,
        thresholds: Thresholds = Thresholds(),
    ) -> None:
        self.config = config
        self.thresholds = thresholds
        self._previous_min_temp_c: Optional[float] = None
        self._previous_timestamp_s: Optional[float] = None

    def evaluate(
        self,
        *,
        temperatures_c: Iterable[Optional[float]],
        timestamp_s: Optional[float],
    ) -> GateResult:
        values = list(temperatures_c)
        measurements: dict[str, Any] = {
            "temperatures_c": values,
            "timestamp_s": timestamp_s,
        }
        if not values or not is_finite_number(timestamp_s):
            return out_of_domain_result(
                "frost_boundary",
                "degC",
                measurements,
                "Temperature sensors or timestamp are missing.",
            )
        if not all(is_finite_number(value) for value in values):
            return out_of_domain_result(
                "frost_boundary",
                "degC",
                measurements,
                "At least one safety-relevant temperature sensor is missing.",
            )

        finite_values = [float(value) for value in values if value is not None]
        if any(
            value < self.config.min_sensor_c or value > self.config.max_sensor_c
            for value in finite_values
        ):
            return out_of_domain_result(
                "frost_boundary",
                "degC",
                measurements,
                "A sensor value is outside its configured plausibility range.",
            )

        min_temp = min(finite_values)
        mean_temp = fmean(finite_values)
        spread = max(finite_values) - min_temp
        delta = max(0.0, self.config.operating_floor_c - min_temp)
        tau = self.config.tau_c
        r = delta / tau
        zone = classify_r(r, self.thresholds)
        autonomy_allowed, action = action_for_zone(zone)

        cooling_rate_c_s: Optional[float] = None
        time_to_boundary_s: Optional[float] = None
        notes = [
            "The minimum sensor value is used; an average must not hide a cold corner."
        ]
        current_timestamp = float(timestamp_s)
        if (
            self._previous_min_temp_c is not None
            and self._previous_timestamp_s is not None
        ):
            dt = current_timestamp - self._previous_timestamp_s
            if dt > 0.0:
                cooling_rate_c_s = (min_temp - self._previous_min_temp_c) / dt
                if (
                    cooling_rate_c_s < 0.0
                    and min_temp > self.config.complete_boundary_c
                ):
                    time_to_boundary_s = (
                        min_temp - self.config.complete_boundary_c
                    ) / (-cooling_rate_c_s)
                    notes.append(
                        "time_to_boundary_s is predictive testimony only; "
                        "it does not rewrite R."
                    )

        self._previous_min_temp_c = min_temp
        self._previous_timestamp_s = current_timestamp
        measurements.update(
            {
                "minimum_temperature_c": min_temp,
                "mean_temperature_c": mean_temp,
                "sensor_spread_c": spread,
                "cooling_rate_c_s": cooling_rate_c_s,
                "time_to_boundary_s": time_to_boundary_s,
            }
        )
        return GateResult(
            example="frost_boundary",
            timestamp_utc=now_utc_iso(),
            zone=zone,
            autonomy_allowed=autonomy_allowed,
            delta=delta,
            tau=tau,
            r=r,
            unit="degC",
            action=action,
            measurements=measurements,
            notes=notes,
        )


# ---------------------------------------------------------------------------
# Example 3: motor multi-axis boundary gate
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AxisLimit:
    normal: float
    complete_boundary: float
    unit: str

    def __post_init__(self) -> None:
        if self.complete_boundary <= self.normal:
            raise ValueError("complete_boundary must be greater than normal.")

    @property
    def tau(self) -> float:
        return self.complete_boundary - self.normal


@dataclass(frozen=True)
class MotorConfig:
    vibration: AxisLimit
    temperature: AxisLimit
    current: AxisLimit


def rms(values: Iterable[float]) -> float:
    samples = list(values)
    if not samples:
        raise ValueError("RMS requires at least one sample.")
    return math.sqrt(fmean(value * value for value in samples))


class MotorBoundaryGate:
    def __init__(
        self,
        config: MotorConfig,
        thresholds: Thresholds = Thresholds(),
    ) -> None:
        self.config = config
        self.thresholds = thresholds

    @staticmethod
    def axis_ratio(value: float, limit: AxisLimit) -> tuple[float, float, float]:
        delta = max(0.0, value - limit.normal)
        tau = limit.tau
        return delta, tau, delta / tau

    def evaluate(
        self,
        *,
        vibration_velocity_samples_mm_s: Iterable[Optional[float]],
        bearing_temperature_c: Optional[float],
        motor_current_a: Optional[float],
    ) -> GateResult:
        vibration_values = list(vibration_velocity_samples_mm_s)
        measurements: dict[str, Any] = {
            "vibration_velocity_samples_mm_s": vibration_values,
            "bearing_temperature_c": bearing_temperature_c,
            "motor_current_a": motor_current_a,
        }
        if (
            not vibration_values
            or not all(is_finite_number(value) for value in vibration_values)
            or not is_finite_number(bearing_temperature_c)
            or not is_finite_number(motor_current_a)
        ):
            return out_of_domain_result(
                "motor_multi_axis",
                "dimensionless",
                measurements,
                "A required motor sensor channel is missing or non-finite.",
            )

        vibration_rms = rms(float(value) for value in vibration_values)
        temperature = float(bearing_temperature_c)
        current = float(motor_current_a)

        dv, tv, rv = self.axis_ratio(vibration_rms, self.config.vibration)
        dt, tt, rt = self.axis_ratio(temperature, self.config.temperature)
        di, ti, ri = self.axis_ratio(current, self.config.current)
        ratios = {
            "vibration": rv,
            "temperature": rt,
            "current": ri,
        }
        deltas = {
            "vibration": dv,
            "temperature": dt,
            "current": di,
        }
        taus = {
            "vibration": tv,
            "temperature": tt,
            "current": ti,
        }
        units = {
            "vibration": self.config.vibration.unit,
            "temperature": self.config.temperature.unit,
            "current": self.config.current.unit,
        }
        r_guard = max(ratios.values())
        dominant_axis = max(ratios, key=ratios.get)
        zone = classify_r(r_guard, self.thresholds)
        autonomy_allowed, action = action_for_zone(zone)

        measurements.update(
            {
                "vibration_velocity_rms_mm_s": vibration_rms,
                "axis_delta": {
                    "vibration_mm_s": dv,
                    "temperature_c": dt,
                    "current_a": di,
                },
                "axis_tau": {
                    "vibration_mm_s": tv,
                    "temperature_c": tt,
                    "current_a": ti,
                },
                "axis_r": ratios,
                "dominant_axis": dominant_axis,
            }
        )
        return GateResult(
            example="motor_multi_axis",
            timestamp_utc=now_utc_iso(),
            zone=zone,
            autonomy_allowed=autonomy_allowed,
            delta=deltas[dominant_axis],
            tau=taus[dominant_axis],
            r=r_guard,
            unit=units[dominant_axis],
            action=action,
            measurements=measurements,
            notes=[
                "Each physical channel uses its own delta/tau ratio.",
                "R_guard is max(R_i), so averaging cannot hide one unsafe axis.",
                "Machine-specific limits require commissioning and calibration.",
            ],
        )


def run_examples() -> list[GateResult]:
    thresholds = Thresholds()

    tank = TankMassBalanceGate(
        TankConfig(
            diameter_m=3.0,
            sigma_level_m=0.001,
            sigma_q_in_m3_s=0.00005,
            sigma_q_out_m3_s=0.00005,
            process_margin_m3_s=0.00010,
        ),
        thresholds,
    )
    tank_result = tank.evaluate(
        previous_level_m=1.500,
        current_level_m=1.530,
        q_in_m3_s=0.0040,
        q_out_m3_s=0.0002,
        dt_s=60.0,
    )

    frost = FrostBoundaryGate(
        FrostConfig(
            operating_floor_c=5.0,
            complete_boundary_c=0.0,
        ),
        thresholds,
    )
    frost.evaluate(
        temperatures_c=[3.5, 3.2, 3.0],
        timestamp_s=0.0,
    )
    frost_result = frost.evaluate(
        temperatures_c=[3.0, 2.8, 2.5],
        timestamp_s=600.0,
    )

    motor = MotorBoundaryGate(
        MotorConfig(
            vibration=AxisLimit(2.0, 7.1, "mm/s RMS"),
            temperature=AxisLimit(55.0, 90.0, "degC"),
            current=AxisLimit(12.0, 18.0, "A"),
        ),
        thresholds,
    )
    motor_result = motor.evaluate(
        vibration_velocity_samples_mm_s=[4.5, 5.0, 4.8, 4.6, 4.9, 4.7],
        bearing_temperature_c=74.0,
        motor_current_a=15.0,
    )

    return [tank_result, frost_result, motor_result]


def self_test() -> None:
    assert classify_r(0.39, Thresholds()) is Zone.NORMAL
    assert classify_r(0.40, Thresholds()) is Zone.WARN
    assert classify_r(0.70, Thresholds()) is Zone.HUMAN_HANDOFF
    assert classify_r(0.90, Thresholds()) is Zone.IRREVERSIBLE_ONSET
    assert classify_r(1.00, Thresholds()) is Zone.FAIL_CLOSED

    results = run_examples()
    assert len(results) == 3
    assert all(result.r is not None for result in results)
    assert all(result.zone is Zone.WARN for result in results)

    missing_gate = FrostBoundaryGate(FrostConfig(5.0, 0.0))
    missing_result = missing_gate.evaluate(
        temperatures_c=[2.0, None, 2.2],
        timestamp_s=0.0,
    )
    assert missing_result.zone is Zone.OUT_OF_DESCRIPTION_DOMAIN
    assert missing_result.r is None
    assert not missing_result.autonomy_allowed


if __name__ == "__main__":
    self_test()
    for result in run_examples():
        print(result.to_json())
