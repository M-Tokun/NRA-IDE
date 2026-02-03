# ═══════════════════════════════════════════════════════════════════════
# File: run_validation.py
# Phase: 30 (Verification Infrastructure)
# Date: 26-0203-1800 JST
# ═══════════════════════════════════════════════════════════════════════

import csv
import json
import sys
import os
sys.path.append('../20_Software_Host')
from fpga_interface import FPGAInterface

def run_automated_test():
    print("--- NRA-IDE Automated Validation Suite ---")

    # 1. Load Expected Oracle
    try:
        with open('expected_results.json', 'r') as f:
            oracle = json.load(f)['test_case_expectations']
    except Exception as e:
        print(f"❌ Oracle Load Error: {e}")
        return

    # 2. Initialize Interface
    fpga = FPGAInterface()

    # 3. Process CSV Test Cases
    results = []
    passed_count = 0

    with open('validation_test_cases.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tid = row['test_id']
            print(f"Testing {tid}: {row['note']}...", end=' ')

            # Input construction
            p = {
                'cell_stiffness': float(row['stiff']),
                'cell_viscosity': float(row['visc']),
                'cell_diameter':  float(row['diam']),
                'pore_size':      float(row['pore']),
                'flow_dp':        float(row['flow']),
                'drug_boost':     float(row['boost'])
            }

            # Query FPGA
            res = fpga.send_query(p, row['type'])

            # Oracle Verification
            # rx_data = (Error << 1) | Jammed
            actual_hex = (res['error_code'] << 1) | (1 if res['is_jammed'] else 0)
            expected_hex = int(oracle[tid]['expected_binary'], 16)

            if actual_hex == expected_hex:
                print("✅ PASS")
                passed_count += 1
            else:
                print(f"❌ FAIL (Actual: 0x{actual_hex:02X}, Expected: 0x{expected_hex:02X})")

    # 4. Final Summary
    print(f"\nSummary: {passed_count} / {len(oracle)} cases passed.")
    if passed_count == len(oracle):
        print("✓ SYSTEM INTEGRITY VERIFIED (Ritsukan Level 1)")
    else:
        print("⚠ SYSTEM INTEGRITY COMPROMISED")

if __name__ == "__main__":
    run_automated_test()
