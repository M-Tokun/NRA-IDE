# nra_gate_spatial.py
# [NRA-SPATIAL-ISOLATION] v1.0
# [LAYER-02] SPATIAL_CALCULATION / DISTANCE_FIREWALL
# ============================================================================
# [RULE] DISTANCE_CALC=ALLOWED_HERE_ONLY
# [ISOLATION] SPATIAL_VAR=NEVER_IN_CAUSAL_STATE
# [WRAPPER] CORE=PROTECTED / SPATIAL=ISOLATED
# ============================================================================

from dataclasses import dataclass
from .nra_gate_constraint import IdeSafetyCore, SystemState

@dataclass
class SpatialContext:
    # [SPATIAL-VARS] X / Y / Z / BOUNDARY
    x: float
    y: float
    z: float
    boundary_radius: float

    def measure_distortion(self) -> float:
        # [CRITICAL] DISTANCE_CALC=ALLOWED_HERE_ONLY
        current_radius = (self.x**2 + self.y**2)**0.5
        gap = current_radius - self.boundary_radius
        # [QUANTIZATION] NEGATIVE=ZERO
        return max(0.0, gap)

class SafeEngineWrapper:
    # [WRAPPER-PURPOSE] ISOLATE_SPATIAL / PROTECT_CAUSAL
    def __init__(self):
        # [CORE-INJECTION] CAUSAL_DOMAIN=PROTECTED
        self.core = IdeSafetyCore()

    def update(self, state: SystemState, context: SpatialContext) -> tuple:
        # [PROTOCOL] SPATIAL→DISTORTION→CAUSAL
        # [FIREWALL] DISTANCE_NEVER_ENTERS_CORE
        distortion = context.measure_distortion()
        return self.core.update_step(state, input_energy=1.0, distortion_input=distortion)
