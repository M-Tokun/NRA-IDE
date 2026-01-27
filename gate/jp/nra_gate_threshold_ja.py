# nra_gate_threshold_ja.py
# [NRA閾値監視] v1.0
# [レイヤー03] 出力検証 / 境界揺らぎ
# ============================================================================
# [規則] 比率計算=揺らぎ/厚さ
# [動作] 比率<0.4=継続 / 比率≥1.0=停止
# [設定] ../config/ide_foundation_config.json
# ============================================================================

import json
import enum
import os
from dataclasses import dataclass

class SafetyAction(enum.Enum):
    # [列挙型] 動作レベル
    CONTINUE = "継続"
    LOG_WARN = "警告記録"
    EMERGENCY_BRAKE = "緊急停止"
    SYSTEM_HALT = "システム停止"

@dataclass
class SafetyStatus:
    # [状態構造] レベル / 動作 / 比率 / メッセージ
    level_name: str
    action: SafetyAction
    ratio: float
    message: str

class ThresholdGuardian:
    # [監視目的] 境界揺らぎ評価
    def __init__(self, config_path: str = None):
        # [設定読込] デフォルト=../config/ide_foundation_config.json
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, 'config', 'ide_foundation_config.json')
            
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.levels = self.config["safety_levels"]

    def evaluate(self, current_fluctuation: float, defined_thickness: float) -> SafetyStatus:
        # [検証] 厚さ=正である必要
        if defined_thickness <= 0: 
            raise ValueError("厚さ違反 / ゼロより大きい必要")
        
        # [比率計算] 揺らぎ / 厚さ
        ratio = abs(current_fluctuation) / defined_thickness
        
        # [閾値評価] 4レベル
        if ratio < self.levels["level_1"]["ratio_max"]:
            # [ゾーンA] 比率<0.40 / 動作=継続
            return SafetyStatus(self.levels["level_1"]["name"], SafetyAction.CONTINUE, ratio, "安定")
        elif ratio < self.levels["level_2"]["ratio_max"]:
            # [ゾーンB] 0.40≤比率<0.70 / 動作=警告
            return SafetyStatus(self.levels["level_2"]["name"], SafetyAction.LOG_WARN, ratio, "警告")
        elif ratio < self.levels["level_3"]["ratio_max"]:
            # [ゾーンC] 0.70≤比率<1.00 / 動作=緊急停止
            return SafetyStatus(self.levels["level_3"]["name"], SafetyAction.EMERGENCY_BRAKE, ratio, "危機")
        else:
            # [ゾーンD] 比率≥1.00 / 動作=停止
            return SafetyStatus(self.levels["level_4"]["name"], SafetyAction.SYSTEM_HALT, ratio, "停止")

if __name__ == "__main__":
    # [テスト] 実行例
    guardian = ThresholdGuardian()
    print(guardian.evaluate(5.0, 10.0))
