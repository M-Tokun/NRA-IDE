import json
import enum
import os
from dataclasses import dataclass

class SafetyAction(enum.Enum):
    CONTINUE = "CONTINUE"
    LOG_WARN = "LOG_WARN"
    EMERGENCY_BRAKE = "EMERGENCY_BRAKE"
    SYSTEM_HALT = "SYSTEM_HALT"

@dataclass
class SafetyStatus:
    level_name: str
    action: SafetyAction
    ratio: float
    message: str

class ThresholdGuardian:
    def __init__(self, config_path: str = None):
        if config_path is None:
            # Default to foundation config in parent/config dir
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, 'config', 'ide_foundation_config.json')
            
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.levels = self.config["safety_levels"]

    def evaluate(self, current_fluctuation: float, defined_thickness: float) -> SafetyStatus:
        if defined_thickness <= 0: raise ValueError("Thickness must be > 0")
        ratio = abs(current_fluctuation) / defined_thickness
        
        if ratio < self.levels["level_1"]["ratio_max"]:
            return SafetyStatus(self.levels["level_1"]["name"], SafetyAction.CONTINUE, ratio, "Stable")
        elif ratio < self.levels["level_2"]["ratio_max"]:
            return SafetyStatus(self.levels["level_2"]["name"], SafetyAction.LOG_WARN, ratio, "Warning")
        elif ratio < self.levels["level_3"]["ratio_max"]:
            return SafetyStatus(self.levels["level_3"]["name"], SafetyAction.EMERGENCY_BRAKE, ratio, "Critical")
        else:
            return SafetyStatus(self.levels["level_4"]["name"], SafetyAction.SYSTEM_HALT, ratio, "HALT")

if __name__ == "__main__":
    # Test execution
    guardian = ThresholdGuardian()
    print(guardian.evaluate(5.0, 10.0))