# ═══════════════════════════════════════════════════════════════════════
# File: clinical_report_generator.py
# Phase: 20
# Date: 2026-02-01
#
# 目的: 医師向け臨床レポートの生成
# ═══════════════════════════════════════════════════════════════════════

import datetime

class ClinicalReportGenerator:
    def generate(self, p_id: str, data: dict, result: dict, boost: float) -> str:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # 判定ロジック
        status = "SAFE (Blocked)" if result.get('is_jammed') else "DANGER (Pass)"
        if result.get('error_code', 0) != 0:
            status = f"ERROR Code: 0x{result.get('error_code'):02X}"

        rec_boost = f"+{boost:.2f} kPa" if boost else "N/A"

        report = f"""
══════════════════════════════════════════════════
NRA-IDE Clinical Report (Bio-Calibrator v1.0)
══════════════════════════════════════════════════
Date: {now}
Patient ID: {p_id}

[Measurements]
  Cell Stiffness: {data['cell_stiffness']} kPa
  Cell Viscosity: {data['cell_viscosity']} Pa*s
  Cell Diameter : {data['cell_diameter']} um
  Pore Size     : {data['pore_size']} um
  Flow Pressure : {data['flow_dp']} kPa

[Computation Result]
  Status        : {status}
  Optimal Boost : {rec_boost}

[Physician Guidance]
  Based on the Phase 2 Mesoscale Physics Model,
  the calculated drug concentration (Boost) establishes
  a physical jamming state.

[Gate Axiom Warning]
  This system provides physical evidence only.
  The final clinical decision rests solely with the physician.
══════════════════════════════════════════════════
"""
        return report

    def save(self, text: str, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✓ Report Saved: {filename}")
