# ═══════════════════════════════════════════════════════════════════════
# File: main.py
# Phase: 20 (Master Integration / Self-Diagnostic Support)
# Rev:  2.0 (2026-07-28) 臨床セッションの実装・PHASE_2 Rev 2.0 に同期
# ═══════════════════════════════════════════════════════════════════════

import sys
import json
import os
import argparse
import datetime

# Windows(cp932)コンソールでの UnicodeEncodeError を防ぐ。
# 状態表示は ASCII に統一済みだが、レポート本文（罫線・日本語）を
# 標準出力へ流した場合でも停止しないようにする。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")

from fpga_interface import FPGAInterface
from patient_data_validator import PatientDataValidator
from clinical_report_generator import ClinicalReportGenerator
from safety_map_visualizer import SafetyMapVisualizer
import nra_core_model as core


class NRA_IDEMaster:
    def __init__(self):
        self.fpga = FPGAInterface()
        self.validator = PatientDataValidator()
        self.generator = ClinicalReportGenerator()
        self.visualizer = SafetyMapVisualizer()

    # ── 判定の出所を明示する（レポートに記載される） ──
    def _source(self) -> str:
        return "FPGA" if self.fpga.serial else "Reference model (FPGA not connected)"

    def run_self_test(self):
        """
        自己診断（Self-Diagnostic）モード
        Phase 30 の期待値を用いて演算回路の健全性を検証する
        """
        print("--- [DIAGNOSTIC] Starting Hardware Integrity Check ---")

        # 検証用ゴールデン・テストケース (TC001: 正常, TC004: 異常系)
        test_cases = [
            {
                "id": "TC001",
                "data": {'cell_stiffness': 1.5, 'cell_viscosity': 0.05, 'cell_diameter': 12.0,
                         'pore_size': 8.0, 'flow_dp': 0.6, 'drug_boost': 0.0},
                "expected": 0x00  # Jammed=0, Error=0
            },
            {
                "id": "TC004",
                "data": {'cell_stiffness': 1.5, 'cell_viscosity': 0.00, 'cell_diameter': 12.0,
                         'pore_size': 8.0, 'flow_dp': 0.6, 'drug_boost': 0.0},
                "expected": 0x06  # Jammed=0, Error=0x03 (Viscosity Zero Violation)
            }
        ]

        for tc in test_cases:
            print(f"  Testing {tc['id']}...", end=" ")
            res = self.fpga.send_query(tc['data'], "Type A")

            # バイナリ値の再構成 (Error << 1 | Jammed)
            actual = (res['error_code'] << 1) | (1 if res['is_jammed'] else 0)

            if actual == tc['expected']:
                print("[OK]")
            else:
                print(f"[FAIL] (Actual: 0x{actual:02X}, Expected: 0x{tc['expected']:02X})")
                print("[FATAL] Ritsukan Axiom compromised. System Locking Down.")
                return False

        print("--- [DIAGNOSTIC] Hardware Integrity Verified. System Ready. ---\n")
        return True

    def run_clinical_session(self, data_path: str, out_dir: str) -> bool:
        """
        患者データ1件を処理し、レポートとジャミングマップを出力する。
        検証を通らないデータでは計算を行わない（Fail-Closed）。
        """
        # 1. 読み込み（BOM 付き JSON も受理する）
        try:
            with open(data_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERR] Cannot read patient data: {e}")
            return False

        p_id = str(data.get('patient_id', 'UNKNOWN'))
        c_type = data.get('cancer_type', 'Type A')
        print(f"--- [SESSION] Patient: {p_id} / {c_type} ---")

        timestamp = datetime.datetime.now().strftime("%y-%m%d-%H%M")
        base = os.path.join(out_dir, f"NRA-{timestamp}-{p_id[:8]}")

        # 2. 入力検証（Phase 4 の範囲）
        ok, errors = self.validator.validate(data)
        if not ok:
            print("[FAIL] Input validation rejected the data:")
            for e in errors:
                print(f"    - {e}")
            # 却下の事実も記録として残す。
            # エラーコードは参照実装の判定順序（0x03 -> 0x02 -> 0x01）に従う。
            # ここで ERR_RANGE を決め打ちすると、粘性ゼロ等の真因を取り違える。
            result = core.evaluate(data, c_type)
            if result['error_code'] == core.ERR_NONE:
                result = {'is_jammed': False, 'error_code': core.ERR_RANGE}
            report = self.generator.generate(data, result, source="Validator (rejected)")
            self.generator.save(report, base + "_REJECTED.txt")
            return False

        # 3. 判定（FPGA、未接続時は参照実装）
        result = self.fpga.send_query(data, c_type)
        judgement = ("INVALID" if result['error_code'] != core.ERR_NONE
                     else ("BLOCKED" if result['is_jammed'] else "PASSABLE"))
        print(f"  Judgement : {judgement} "
              f"(error 0x{result['error_code']:02X}, source: {self._source()})")

        # 4. レポート生成
        report = self.generator.generate(data, result, source=self._source())
        print()
        print(report)
        self.generator.save(report, base + ".txt")

        # 5. ジャミングマップ生成
        try:
            self.visualizer.generate_map(data, base + ".png")
        except Exception as e:
            print(f"[WARN] Map generation skipped: {e}")

        return result['error_code'] == core.ERR_NONE


def main():
    parser = argparse.ArgumentParser(description="NRA-IDE Master Controller")
    parser.add_argument("--data", help="Patient JSON path")
    parser.add_argument("--out", default="output",
                        help="Output directory for report and map (default: ./output)")
    parser.add_argument("--test", action="store_true", help="Run self-diagnostic and exit")
    args = parser.parse_args()

    system = NRA_IDEMaster()

    # 1. 自己診断モードの実行
    if args.test:
        sys.exit(0 if system.run_self_test() else 1)

    # 2. 通常の臨床セッション開始前の強制診断
    if not system.run_self_test():
        sys.exit(1)

    # 3. 本番データの処理
    if args.data:
        sys.exit(0 if system.run_clinical_session(args.data, args.out) else 1)
    else:
        print("Usage: python main.py --data <path> [--out <dir>]  |  python main.py --test")
        sys.exit(2)


if __name__ == "__main__":
    main()
