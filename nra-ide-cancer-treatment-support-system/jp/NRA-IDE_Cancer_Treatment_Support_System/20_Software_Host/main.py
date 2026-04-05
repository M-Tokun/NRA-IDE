# ═══════════════════════════════════════════════════════════════════════
# File: main.py
# Phase: 20 (Master Integration / Self-Diagnostic Support)
# Date: 26-0203-1825 JST
# ═══════════════════════════════════════════════════════════════════════

import sys
import argparse
import time
from fpga_interface import FPGAInterface
from patient_data_validator import PatientDataValidator
from clinical_report_generator import ClinicalReportGenerator
from safety_map_visualizer import SafetyMapVisualizer

class NRA_IDEMaster:
    def __init__(self):
        self.fpga = FPGAInterface()
        self.validator = PatientDataValidator()
        self.generator = ClinicalReportGenerator()

    def run_self_test(self):
        """
        自己診断（Self-Diagnostic）モード
        Phase 30 の期待値を用いて FPGA 演算回路の健全性を検証する
        """
        print("--- [DIAGNOSTIC] Starting Hardware Integrity Check ---")

        # 検証用ゴールデン・テストケース (TC001: 正常, TC004: 異常系)
        test_cases = [
            {
                "id": "TC001",
                "data": {'cell_stiffness': 1.5, 'cell_viscosity': 0.05, 'cell_diameter': 12.0,
                         'pore_size': 8.0, 'flow_dp': 0.6, 'drug_boost': 0.0},
                "expected": 0x00 # Jammed=0, Error=0
            },
            {
                "id": "TC004",
                "data": {'cell_stiffness': 1.5, 'cell_viscosity': 0.00, 'cell_diameter': 12.0,
                         'pore_size': 8.0, 'flow_dp': 0.6, 'drug_boost': 0.0},
                "expected": 0x06 # Jammed=0, Error=0x03 (Viscosity Zero Violation)
            }
        ]

        for tc in test_cases:
            print(f"  Testing {tc['id']}...", end=" ")
            res = self.fpga.send_query(tc['data'], "Type A")

            # バイナリ値の再構成 (Error << 1 | Jammed)
            actual = (res['error_code'] << 1) | (1 if res['is_jammed'] else 0)

            if actual == tc['expected']:
                print("✅ OK")
            else:
                print(f"❌ FAILED (Actual: 0x{actual:02X}, Expected: 0x{tc['expected']:02X})")
                print("⚠ FATAL: Ritsukan Axiom compromised. System Locking Down.")
                return False

        print("--- [DIAGNOSTIC] Hardware Integrity Verified. System Ready. ---\n")
        return True

    def run_clinical_session(self, data_path):
        # ... (前回のセッション実行ロジック)
        pass

def main():
    parser = argparse.ArgumentParser(description="NRA-IDE Master Controller")
    parser.add_argument("--data", help="Patient JSON path")
    parser.add_argument("--test", action="store_true", help="Run self-diagnostic and exit")
    args = parser.parse_args()

    system = NRA_IDEMaster()

    # 1. 自己診断モードの実行
    if args.test:
        success = system.run_self_test()
        sys.exit(0 if success else 1)

    # 2. 通常の臨床セッション開始前の強制診断（推奨）
    if not system.run_self_test():
        sys.exit(1)

    # 3. 本番データの処理
    if args.data:
        system.run_clinical_session(args.data)
    else:
        print("Usage: python main.py --data <path> or --test")

if __name__ == "__main__":
    main()
