# __init___ja.py
# [NRAゲートパッケージ] v1.0
# ============================================================================
# [パッケージ] NRA-IDE / ゲートモジュール
# [目的] 公理的基盤 / 制約強制
# ============================================================================

"""
[NRAゲート]
権限=M-Tokun
バージョン=1.0.0
状態=強制実行
"""

__version__ = "1.0.0"
__author__ = "M-Tokun"

# [エクスポート] コアクラス
from .nra_gate_axiom_ja import NRAGateKernel
from .nra_gate_constraint_ja import IdeSafetyCore, SystemState, EngineConfig
from .nra_gate_spatial_ja import SpatialContext, SafeEngineWrapper
from .nra_gate_threshold_ja import ThresholdGuardian, SafetyAction, SafetyStatus

__all__ = [
    # [公理]
    "NRAGateKernel",
    # [制約]
    "IdeSafetyCore",
    "SystemState",
    "EngineConfig",
    # [空間]
    "SpatialContext",
    "SafeEngineWrapper",
    # [閾値]
    "ThresholdGuardian",
    "SafetyAction",
    "SafetyStatus",
]
