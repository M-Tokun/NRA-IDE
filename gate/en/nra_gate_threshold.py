# nra_gate_threshold.py
# [NRA-THRESHOLD-GUARDIAN] v1.0
# [LAYER-03] OUTPUT_VERIFICATION / BOUNDARY_FLUCTUATION
# ============================================================================
# [RULE] RATIO_CALC=FLUCTUATION/THICKNESS
# [ACTION] RATIO<0.4=CONTINUE / RATIO≥1.0=HALT
# [CONFIG] ../../config/ide_foundation_config.json
# ============================================================================

import json
import enum
import os
import sys
from dataclasses import dataclass

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

class SafetyAction(enum.Enum):
    # [ENUM] ACTION_LEVELS
    CONTINUE = "CONTINUE"
    LOG_WARN = "LOG_WARN"
    EMERGENCY_BRAKE = "EMERGENCY_BRAKE"
    SYSTEM_HALT = "SYSTEM_HALT"

@dataclass
class SafetyStatus:
    # [STATUS-STRUCTURE] LEVEL / ACTION / RATIO / MESSAGE
    level_name: str
    action: SafetyAction
    ratio: float
    message: str

class ThresholdGuardian:
    # [GUARDIAN-PURPOSE] BOUNDARY_FLUCTUATION_EVALUATION
    def __init__(self, config_path: str = None):
        # [CONFIG-LOAD] DEFAULT=../../config/ide_foundation_config.json
        if config_path is None:
            repo_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(repo_dir, "config", "ide_foundation_config.json")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.levels = self._load_levels(self.config)

    @staticmethod
    def _load_levels(config: dict) -> dict:
        if "safety_levels" in config:
            return config["safety_levels"]

        gate = config["gate_structure"]
        return {
            "level_1": {"name": "Zone A", "ratio_max": gate["zone_A"]["ratio_max"]},
            "level_2": {"name": "Zone B", "ratio_max": gate["zone_B"]["ratio_max"]},
            "level_3": {"name": "Zone C", "ratio_max": gate["zone_C"]["ratio_max"]},
            "level_4": {"name": "Beyond Zone C", "ratio_max": gate["zone_C"]["ratio_max"]},
        }

    def evaluate(self, current_fluctuation: float, defined_thickness: float) -> SafetyStatus:
        # [VALIDATION] THICKNESS=MUST_BE_POSITIVE
        if defined_thickness <= 0: 
            raise ValueError("THICKNESS_VIOLATION / MUST_BE_GT_ZERO")
        
        # [RATIO-CALC] FLUCTUATION / THICKNESS
        ratio = abs(current_fluctuation) / defined_thickness
        
        # [THRESHOLD-EVALUATION] FOUR_LEVELS
        if ratio < self.levels["level_1"]["ratio_max"]:
            # [ZONE-A] RATIO<0.40 / ACTION=CONTINUE
            return SafetyStatus(self.levels["level_1"]["name"], SafetyAction.CONTINUE, ratio, "STABLE")
        elif ratio < self.levels["level_2"]["ratio_max"]:
            # [ZONE-B] 0.40≤RATIO<0.70 / ACTION=WARN
            return SafetyStatus(self.levels["level_2"]["name"], SafetyAction.LOG_WARN, ratio, "WARNING")
        elif ratio < self.levels["level_3"]["ratio_max"]:
            # [ZONE-C] 0.70≤RATIO<1.00 / ACTION=BRAKE
            return SafetyStatus(self.levels["level_3"]["name"], SafetyAction.EMERGENCY_BRAKE, ratio, "CRITICAL")
        else:
            # [BEYOND_ZONE_C] RATIO≥1.00 / ACTION=HALT (not a fourth lettered zone)
            return SafetyStatus(self.levels["level_4"]["name"], SafetyAction.SYSTEM_HALT, ratio, "HALT")

if __name__ == "__main__":
    # [TEST] EXECUTION_EXAMPLE
    guardian = ThresholdGuardian()
    print(guardian.evaluate(5.0, 10.0))
