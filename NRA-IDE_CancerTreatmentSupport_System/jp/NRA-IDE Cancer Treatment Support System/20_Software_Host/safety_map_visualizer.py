# ═══════════════════════════════════════════════════════════════════════
# File: main.py
# Phase: 20 (Master Integration)
# Date: 26-0203-1740 JST
# ═══════════════════════════════════════════════════════════════════════

import sys
import json
import argparse
from fpga_interface import FPGAInterface
from patient_data_validator import PatientDataValidator
from clinical_report_generator import ClinicalReportGenerator
from safety_map_visualizer import SafetyMapVisualizer

def run_nra_ide():
    parser = argparse.ArgumentParser(description="NRA-IDE Master Controller")
    parser.add_argument("--data", required=True, help="Patient JSON path")
    args = parser.parse_args()

    print("--- NRA-IDE Cancer Treatment Support System ---")

    # 1. Load & Validate
    try:
        with open(args.data, 'r') as f:
            patient_data = json.load(f)
    except Exception as e:
        print(f"❌ Data Load Error: {e}")
        return

    is_ok, errs = PatientDataValidator.validate(patient_data)
    if not is_ok:
        print("❌ Ritsukan Axiom Violation (Safety Guard Active):")
        for e in errs: print(f"  - {e}")
        return

    # 2. FPGA Connection & Computation
    fpga = FPGAInterface()

    # 3. Optimal Boost Search (Causal Diode: Forward Only)
    print(f"🔍 Analyzing {patient_data['cancer_type']} dynamics...")
    optimal_boost = 0.0
    final_result = {'is_jammed': False, 'error_code': 0}

    for b in [i * 0.01 for i in range(1001)]: # 0.00 to 10.00 kPa
        patient_data['drug_boost'] = b
        res = fpga.send_query(patient_data, patient_data['cancer_type'])

        if res and res['error_code'] == 0 and res['is_jammed']:
            optimal_boost = b
            final_result = res
            print(f"✅ Physical Jamming Achieved at +{optimal_boost:.2f} kPa")
            break

        if res and res['error_code'] != 0:
            final_result = res
            print(f"⚠ Computation Aborted: Error 0x{res['error_code']:02X}")
            break
    else:
        print("⚠ WARNING: Jamming state not found within safety limits.")

    # 4. Generate Clinical Artifacts
    rep_gen = ClinicalReportGenerator()
    report_text = rep_gen.generate(patient_data['patient_id'], patient_data, final_result, optimal_boost)

    rep_gen.save(report_text, f"../40_Output_Reports/Report_{patient_data['patient_id']}.txt")

    viz = SafetyMapVisualizer()
    viz.generate_map(patient_data, f"../40_Output_Reports/SafetyMap_{patient_data['patient_id']}.png")

    print(f"\n✓ Session Completed. Artifacts saved to 40_Output_Reports/.")

if __name__ == "__main__":
    run_nra_ide()
