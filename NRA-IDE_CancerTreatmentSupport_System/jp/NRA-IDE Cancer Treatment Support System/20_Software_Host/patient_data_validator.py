# ═══════════════════════════════════════════════════════════════════════
# File: patient_data_validator.py
# Phase: 20
# Date: 2026-02-01
# Author: M-Tokuni & AI Architects
#
# 目的: Phase 4 辞書に基づく厳格なデータ検証
# ═══════════════════════════════════════════════════════════════════════

from typing import Dict, List, Tuple

# Phase 4 定義準拠
RANGES = {
    'cell_stiffness': (0.1, 10.0),
    'cell_viscosity': (0.01, 1.0), # 0禁止
    'cell_diameter':  (5.0, 30.0),
    'pore_size':      (5.0, 15.0),
    'flow_dp':        (0.0, 5.0),
    'drug_boost':     (0.0, 10.0)
}

class PatientDataValidator:
    @staticmethod
    def validate(data: Dict[str, float]) -> Tuple[bool, List[str]]:
        errors = []

        # 1. 必須項目チェック
        for key in RANGES.keys():
            if key not in data:
                errors.append(f"Missing parameter: {key}")
                continue

            val = data[key]
            min_v, max_v = RANGES[key]

            # 2. 範囲チェック
            if not (min_v <= val <= max_v):
                errors.append(f"{key} out of range: {val} (Limit: {min_v}-{max_v})")

        # 3. 物理的整合性チェック
        if data.get('cell_viscosity', 1.0) <= 0:
             errors.append("CRITICAL: Viscosity cannot be zero (Life Axiom)")

        return (len(errors) == 0), errors

if __name__ == "__main__":
    # Test
    test_data = {'cell_stiffness': 1.5, 'cell_viscosity': 0.05} # Missing others
    ok, errs = PatientDataValidator.validate(test_data)
    print(f"Validation Result: {ok}, Errors: {errs}")
