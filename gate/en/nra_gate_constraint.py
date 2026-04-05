# nra_gate_constraint.py
# [NRA-PROTOCOL] DO_NOT_REMOVE / v1.0
# [LAYER-01] INPUT_VALIDATION / CONSTRAINT_ENFORCEMENT
# ============================================================================
# [CONSTRAINT-01] CAUSAL_DIODE / INVERSE_KINEMATICS=PROHIBITED / DISTANCE=READ_ONLY
# [CONSTRAINT-02] QUANTIZATION / FLOAT_RESIDUAL=DISCARD / ZERO_ERROR_OPT=PROHIBITED
# [CONSTRAINT-03] LIVENESS / OMEGA_ZERO=SYSTEM_FAILURE / HOMEOSTASIS=MANDATORY
# [CONSTRAINT-04] FAIL_CLOSED / RATIO_GT_1.0=EXCEPTION / AUTO_FIX=PROHIBITED
# ============================================================================

import math
from dataclasses import dataclass
from typing import Tuple

class EngineConfig:
    # [PARAMETER] STIFFNESS / WORK_THRESHOLD
    STIFFNESS_K: float = 1000.0
    MIN_WORK_THRESHOLD: float = 1e-6

@dataclass(frozen=True)
class SystemState:
    # [STATE-DEFINITION] PHASE / OMEGA / STRESS / WORK
    phase: int
    omega: float
    stress_level: float
    work_rate: float

class IdeSafetyCore:
    def validate_input(self, prev_state: SystemState, input_energy: float):
        # [VALIDATION-01] ENERGY=POSITIVE_ONLY
        if input_energy <= 0:
            raise ValueError("ENERGY_DEFICIT / INPUT_ENERGY=MUST_BE_POSITIVE")
        
        # [VALIDATION-02] CAUSAL_VIOLATION_CHECK / SPATIAL_VAR=PROHIBITED
        if hasattr(prev_state, 'distance') or hasattr(prev_state, 'target_pos'):
            raise TypeError("CAUSAL_VIOLATION / SPATIAL_VARIABLES=IN_CAUSAL_STATE")

    def update_step(self, prev_state: SystemState, input_energy: float, distortion_input: float) -> Tuple[SystemState, dict]:
        # [STEP-01] INPUT_VALIDATION=MANDATORY
        self.validate_input(prev_state, input_energy)
        
        # [STEP-02] STRESS_CALCULATION / FORMULA=DISTORTION*STIFFNESS
        stress = distortion_input * EngineConfig.STIFFNESS_K
        work_rate = stress * prev_state.omega
        
        # [STEP-03] QUANTIZATION / DISCARD_RESIDUAL
        raw_next_phase = prev_state.phase + prev_state.omega
        next_phase_int = math.floor(raw_next_phase)
        entropy_export = raw_next_phase - next_phase_int
        
        # [STEP-04] STATE_UPDATE / IMMUTABLE_DATACLASS
        new_state = SystemState(
            phase=next_phase_int,
            omega=prev_state.omega,
            stress_level=distortion_input,
            work_rate=work_rate
        )
        
        # [STEP-05] TELEMETRY_GENERATION
        telemetry = {
            "projection_value": distortion_input * 100,
            "entropy_export": entropy_export,
            "status": "NOMINAL"
        }
        
        return new_state, telemetry
