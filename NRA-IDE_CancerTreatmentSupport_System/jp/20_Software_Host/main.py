# ═══════════════════════════════════════════════════════════════════════
# File: main.py
# Phase: 20
# Date: 2026-02-01
#
# 目的: システム全体制御
# ═══════════════════════════════════════════════════════════════════════

import sys
import json
from fpga_interface import FPGAInterface
from patient_data_validator import PatientDataValidator
from clinical_report_generator import ClinicalReportGenerator
from safety_map_visualizer import SafetyMapVisualizer

def main():
    print("--- NRA-IDE Bio-Calibrator Host System ---")

    # 1. Load Data
    try:
        with open("../30_Test_Data/sample_patient_data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠ Sample data not found.")
        return

    # 2. Validate
    ok, errs = PatientDataValidator.validate(data)
    if not ok:
        print("❌ Validation Failed:")
        for e in errs: print(f"  - {e}")
        return
    print("✓ Validation Passed")

    # 3. FPGA Processing
    fpga = FPGAInterface()
    optimal_boost = fpga.brute_force_search(data)
    fpga.close()

    if optimal_boost is None:
        print("⚠ Optimal Boost Not Found (Limit Exceeded)")
        optimal_boost = 0.0 # Default for report

    # 4. Report
    gen = ClinicalReportGenerator()
    text = gen.generate(data.get('patient_id', 'Unknown'), data,
                        {'is_jammed': True}, optimal_boost)
    gen.save(text, "../40_Output_Reports/Report.txt")

    # 5. Visualize
    viz = SafetyMapVisualizer()
    viz.generate_map(data, "../40_Output_Reports/SafetyMap.png")

    print("\n✓ All Processes Completed Successfully.")

if __name__ == "__main__":
    main()
