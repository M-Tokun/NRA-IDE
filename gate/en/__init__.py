# __init__.py
# [NRA-GATE-PACKAGE] v1.0
# ============================================================================
# [PACKAGE] NRA-IDE / GATE_MODULE
# [PURPOSE] AXIOMATIC_FOUNDATION / CONSTRAINT_ENFORCEMENT
# ============================================================================

"""
[NRA-GATE]
AUTHORITY=M-Tokun
VERSION=1.0.0
STATUS=ENFORCED
"""

__version__ = "1.0.0"
__author__ = "M-Tokun"

# [EXPORTS] CORE_CLASSES
from .nra_gate_axiom import NRAGateKernel
from .nra_gate_constraint import IdeSafetyCore, SystemState, EngineConfig
from .nra_gate_spatial import SpatialContext, SafeEngineWrapper
from .nra_gate_threshold import ThresholdGuardian, SafetyAction, SafetyStatus

__all__ = [
    # [AXIOM]
    "NRAGateKernel",
    # [CONSTRAINT]
    "IdeSafetyCore",
    "SystemState",
    "EngineConfig",
    # [SPATIAL]
    "SpatialContext",
    "SafeEngineWrapper",
    # [THRESHOLD]
    "ThresholdGuardian",
    "SafetyAction",
    "SafetyStatus",
]
