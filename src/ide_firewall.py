from dataclasses import dataclass
from .ide_core_safe import IdeSafetyCore, SystemState

@dataclass
class SpatialContext:
    x: float
    y: float
    z: float
    boundary_radius: float

    def measure_distortion(self) -> float:
        # Distance calculation is allowed ONLY here
        current_radius = (self.x**2 + self.y**2)**0.5
        gap = current_radius - self.boundary_radius
        return max(0.0, gap)

class SafeEngineWrapper:
    def __init__(self):
        self.core = IdeSafetyCore()

    def update(self, state: SystemState, context: SpatialContext) -> tuple:
        distortion = context.measure_distortion()
        return self.core.update_step(state, input_energy=1.0, distortion_input=distortion)