# ═══════════════════════════════════════════════════════════════════════
# File: clinical_report_generator.py
# Phase: 20 (Report Generation)
# Rev:  2.0 (2026-07-28) PHASE_2 Rev 2.0 の語彙・判定式に同期
#
# 出力書式は 40_Output_Reports/NRA_IDE_Report_Template.txt と一致させること。
# 判定の中間量（歪み・弾性応力・粘性応力）を必ず記載する。判定の根拠を
# 示さないレポートは Physics First に反する。
# ═══════════════════════════════════════════════════════════════════════

import datetime
import os

import nra_core_model as core

_ERR_NAME = {
    core.ERR_NONE:        "ERR_NONE",
    core.ERR_GEOM:        "ERR_GEOMETRIC",
    core.ERR_RANGE:       "ERR_RANGE",
    core.ERR_VISC0:       "ERR_ZERO_VISC",
    core.ERR_OVF:         "ERR_OVERFLOW",
    core.ERR_COMM:        "ERR_COMM",
    core.ERR_UNSUPPORTED: "ERR_UNSUPPORTED",
}

_ERR_MEANING = {
    core.ERR_GEOM:        "細胞直径が隙間より小さく、変形せずに通過する",
    core.ERR_RANGE:       "入力が Phase 4 の定義範囲外である。再測定を要する",
    core.ERR_VISC0:       "粘性ゼロは生体では起こり得ない。測定系の異常を疑う",
    core.ERR_OVF:         "演算がオーバーフローした。システム点検を要する",
    core.ERR_COMM:        "FPGA と通信できなかった。結線・電源を点検する",
    core.ERR_UNSUPPORTED: "未実装の癌腫タイプが指定された",
}

SEP = "═" * 58


class ClinicalReportGenerator:

    def generate(self, patient_data: dict, result: dict,
                 source: str = "FPGA") -> str:
        """
        patient_data : 入力パラメータ（patient_id, cancer_type を含む）
        result       : {'is_jammed': bool, 'error_code': int}
        source       : 判定の出所（"FPGA" / "Reference model (no FPGA)"）
        """
        now = datetime.datetime.now()          # JST 運用前提
        timestamp = now.strftime("%y-%m%d-%H%M")
        p_id = str(patient_data.get('patient_id', 'UNKNOWN'))

        err = result.get('error_code', core.ERR_NONE)
        jammed = bool(result.get('is_jammed', False))

        # 参照実装による独立計算。[Reference] 節と突き合わせに用いる
        ref = core.evaluate(patient_data,
                            patient_data.get('cancer_type', 'Type A'))

        # ── 入力（Q8.8 量子化後の値を表示する。判定はこの値で行われる） ──
        q = {k: core.to_q88(patient_data.get(k, 0.0)) for k in core.RANGES_Q88}
        v_raw = patient_data.get('deform_velocity')
        v_q = core.to_q88(v_raw if v_raw is not None
                          else core.DEFAULT_DEFORM_VELOCITY)
        v_note = "" if v_raw is not None else "  [system default]"

        lines = [
            SEP,
            "NRA-IDE Computation Report (Bio-Calibrator v2.0)",
            SEP,
            f"Report ID : NRA-{timestamp}-{p_id[:8]}",
            f"Date      : {timestamp} JST",
            f"Patient   : {p_id}",
            "",
            "[Input Parameters]  (Q8.8 quantized)",
            f"  Young's modulus (E) : {q['cell_stiffness'] / 256:8.3f} kPa",
            f"  Viscosity       (eta): {q['cell_viscosity'] / 256:8.3f} Pa*s",
            f"  Cell diameter   (D) : {q['cell_diameter'] / 256:8.3f} um",
            f"  Pore size       (d) : {q['pore_size'] / 256:8.3f} um",
            f"  Flow pressure   (dP): {q['flow_dp'] / 256:8.3f} kPa",
            f"  Drug boost      (B) : {q['drug_boost'] / 256:8.3f} kPa",
            f"  Deform velocity (v) : {v_q / 256:8.3f} um/s{v_note}",
            "",
        ]

        # ── 判定根拠（計算可能な場合のみ） ──
        if err == core.ERR_NONE:
            strain, sigma_v = core.fixed_terms(
                q['cell_stiffness'], q['cell_viscosity'],
                q['cell_diameter'], q['pore_size'], v_q)
            sigma_el = ((q['cell_stiffness'] + q['drug_boost']) * strain) >> 8
            total = sigma_el + sigma_v
            lines += [
                "[Computation]  sigma_resist > dP  =>  BLOCKED",
                f"  Strain (D-d)/D        : {strain / 256:8.3f}",
                f"  Elastic stress sig_el : {sigma_el / 256:8.3f} kPa",
                f"  Viscous stress sig_v  : {sigma_v / 256:8.3f} kPa",
                f"  Total resistance      : {total / 256:8.3f} kPa",
                f"  Driving pressure dP   : {q['flow_dp'] / 256:8.3f} kPa",
                "",
            ]
        else:
            lines += [
                "[Computation]",
                "  判定は実行されていない（入力または通信の異常）",
                "",
            ]

        # ── 判定結果 ──
        if err == core.ERR_NONE:
            judgement = "BLOCKED" if jammed else "PASSABLE"
            meaning = ("細胞は隙間を通過できない"
                       if jammed else
                       "細胞は変形して通過しうる（転移経路が開いている）")
        else:
            judgement = "INVALID"
            meaning = _ERR_MEANING.get(err, "未定義のエラー")

        lines += [
            "[Result]",
            f"  Judgement : {judgement}",
            f"  Error code: 0x{err:02X} ({_ERR_NAME.get(err, 'UNKNOWN')})",
            f"  Meaning   : {meaning}",
            "",
        ]

        # ── 参考値: BLOCKED を成立させる最小 Boost ──
        # 判定の出所によらず、参照実装の計算に基づく値を示す
        if err == core.ERR_NONE:
            rb = core.required_boost(patient_data)
            if rb is None:
                rb_text = "算出不能"
            elif ref['is_jammed']:
                rb_text = "0.00 kPa (already BLOCKED)"
            else:
                rb_text = f"+{rb:.2f} kPa"
            lines += [
                "[Reference]  (reference model)",
                f"  Minimum boost for BLOCKED: {rb_text}",
                "",
            ]

        # ── 検証層: FPGA と参照実装の突き合わせ ──
        if err in (core.ERR_NONE, core.ERR_GEOM, core.ERR_RANGE, core.ERR_VISC0):
            if (ref['is_jammed'], ref['error_code']) != (jammed, err):
                lines += [
                    "[!] DISCREPANCY: FPGA と参照実装の判定が一致しない",
                    f"    FPGA      : jammed={jammed}, err=0x{err:02X}",
                    f"    Reference : jammed={ref['is_jammed']}, "
                    f"err=0x{ref['error_code']:02X}",
                    "    本レポートを臨床判断に用いてはならない。",
                    "",
                ]

        # ── 来歴 ──
        # 本レポートはリポジトリから切り離されて単独で流通しうる。
        # どのモデルで・検証済みか否かを、成果物自身が名乗る必要がある。
        lines += [
            "[Provenance]",
            f"  Model      : {core.MODEL_NAME} / {core.MODEL_VERSION}",
            f"  Validation : {core.VALIDATION_STATUS}",
            f"  Source     : {source}",
            f"  Template   : {core.TEMPLATE_NAME}",
            f"               {core.TEMPLATE_URL}",
            "",
            "[Physician's Gate]",
            "  本判定は物理的封鎖の可否のみを示す。投薬の可否を意味しない。",
            "  最終的な治療方針は、倫理的責任を負う医師が決定する。",
            "",
            "  表示された数値は物理モデルの計算結果であり、実測値ではない。",
            "  本モデルは実験による検証を経ていない。",
            "",
            "  本テンプレートは薬機法上の医療機器ではなく、研究・教育目的に限る。",
            "  IEC 62304 の文脈では SOUP（由来不明ソフトウェア）に分類される。",
            "  医療機器開発に用いる場合、V&V・リスク管理・規制申請は",
            "  利用者の責任に属する。",
            f"  {core.COPYRIGHT}",
            f"  {core.LICENSE_NOTE}",
            SEP,
        ]
        return "\n".join(lines) + "\n"

    def save(self, report_text: str, output_path: str) -> None:
        dirpart = os.path.dirname(output_path)
        if dirpart:
            os.makedirs(dirpart, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"[OK] Report saved: {output_path}")
