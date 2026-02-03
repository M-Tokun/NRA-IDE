# ═══════════════════════════════════════════════════════════════════════
# File: clinical_report_generator.py
# Date: 26-0203-1714 JST
# ═══════════════════════════════════════════════════════════════════════

import datetime

class ClinicalReportGenerator:
    def generate(self, p_id: str, data: dict, result: dict, boost: float) -> str:
        # JST規程書式: YY-MMDD-HHMM [cite: 2025-12-12]
        now = datetime.datetime.now() + datetime.timedelta(hours=0) # 既にJST想定
        timestamp = now.strftime("%y-%m%d-%H%M")

        # 判定表示の適正化
        status = "SAFE (Blocked)" if result.get('is_jammed') else "DANGER (Pass)"
        if result.get('error_code', 0) != 0:
            status = f"ERROR Code: 0x{result.get('error_code'):02X}"

        # 臨床精度の固定（小数点2位）
        rec_boost = f"+{boost:.2f} kPa" if boost > 0 else "0.00 kPa (Not Required)"

        report = f"""
══════════════════════════════════════════════════
NRA-IDE Clinical Report (Bio-Calibrator v1.1)
══════════════════════════════════════════════════
Report ID: NRA-{timestamp}-{p_id[:4]}
Date     : {timestamp} JST
Patient  : {p_id}

[Computation Result]
  Status        : {status}
  Optimal Boost : {rec_boost}
... (略)
"""
        return report
