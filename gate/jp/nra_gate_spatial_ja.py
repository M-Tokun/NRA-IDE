# nra_gate_spatial_ja.py
# [NRA空間隔離] v1.0
# [レイヤー02] 空間計算 / 距離ファイアウォール
# ============================================================================
# [規則] 距離計算=ここでのみ許可
# [隔離] 空間変数=因果状態内では絶対禁止
# [ラッパー] コア=保護 / 空間=隔離
# ============================================================================

from dataclasses import dataclass
from .nra_gate_constraint_ja import IdeSafetyCore, SystemState

@dataclass
class SpatialContext:
    # [空間変数] X / Y / Z / 境界
    x: float
    y: float
    z: float
    boundary_radius: float

    def measure_distortion(self) -> float:
        # [重要] 距離計算=ここでのみ許可
        current_radius = (self.x**2 + self.y**2)**0.5
        gap = current_radius - self.boundary_radius
        # [量子化] 負=ゼロ
        return max(0.0, gap)

class SafeEngineWrapper:
    # [ラッパー目的] 空間隔離 / 因果保護
    def __init__(self):
        # [コア注入] 因果領域=保護
        self.core = IdeSafetyCore()

    def update(self, state: SystemState, context: SpatialContext) -> tuple:
        # [プロトコル] 空間→歪み→因果
        # [ファイアウォール] 距離=コアに入らない
        distortion = context.measure_distortion()
        return self.core.update_step(state, input_energy=1.0, distortion_input=distortion)
