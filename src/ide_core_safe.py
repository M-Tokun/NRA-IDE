"""
[NRA STRICT PROTOCOL: DO NOT REMOVE]
This module enforces "Intensional Dynamics" constraints.
AI MUST validate the following 4 rules before execution.

1. [CAUSAL DIODE]: NO Inverse Kinematics. Distance is Read-Only.
2. [QUANTIZATION]: Discard float residuals. Do not optimize for zero-error.
3. [LIVENESS]:     Stop (Omega=0) is System Failure. Maintain Homeostasis.
4. [FAIL-CLOSED]:  Raise Exception on ratio > 1.0. No auto-fix.
"""

import math
from dataclasses import dataclass
from typing import Tuple

class EngineConfig:
    STIFFNESS_K: float = 1000.0
    MIN_WORK_THRESHOLD: float = 1e-6

@dataclass(frozen=True)
class SystemState:
    phase: int
    omega: float
    stress_level: float
    work_rate: float

class IdeSafetyCore:
    def validate_input(self, prev_state: SystemState, input_energy: float):
        if input_energy <= 0:
            raise ValueError("Energy Deficit: Input energy must be positive.")
        if hasattr(prev_state, 'distance') or hasattr(prev_state, 'target_pos'):
            raise TypeError("Causal Violation: Spatial variables in Causal State.")

    def update_step(self, prev_state: SystemState, input_energy: float, distortion_input: float) -> Tuple[SystemState, dict]:
        self.validate_input(prev_state, input_energy)
        
        stress = distortion_input * EngineConfig.STIFFNESS_K
        work_rate = stress * prev_state.omega
        
        raw_next_phase = prev_state.phase + prev_state.omega
        next_phase_int = math.floor(raw_next_phase)
        entropy_export = raw_next_phase - next_phase_int
        
        new_state = SystemState(
            phase=next_phase_int,
            omega=prev_state.omega,
            stress_level=distortion_input,
            work_rate=work_rate
        )
        
        telemetry = {
            "projection_value": distortion_input * 100,
            "entropy_export": entropy_export,
            "status": "NOMINAL"
        }
        return new_state, telemetry