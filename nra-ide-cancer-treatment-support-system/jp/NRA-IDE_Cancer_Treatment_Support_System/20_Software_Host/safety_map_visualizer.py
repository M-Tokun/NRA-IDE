# ═══════════════════════════════════════════════════════════════════════
# File: safety_map_visualizer.py
# Phase: 20 (Safety Map Generation)
# Rev:  2.0 (2026-07-28) 判定式を Phase 10 演算コアと同一に統一
# ═══════════════════════════════════════════════════════════════════════

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# 判定ロジックは参照実装に一本化する。本ファイルに独自の式を持たせない。
from nra_core_model import (
    to_q88 as _to_q88,
    fixed_terms as _fixed_terms,
    check_inputs as _check_inputs,
    required_boost as _required_boost,
    DEFAULT_DEFORM_VELOCITY,
    ERR_VISC0, ERR_GEOM, ERR_RANGE, ERR_NAME,
)


class SafetyMapVisualizer:
    """
    X軸: Drug Boost B [kPa]      — 右ほど細胞が硬くなり、通過しにくくなる
    Y軸: Flow ΔP [kPa]           — 上ほど押し込み力が強く、通過しやすくなる

    判定式は PHASE_2 Rev 2.0 の応力比較形であり、
    10_BioCalibrator_TypeA.v の固定小数点演算をビット単位で再現している。

        sigma_el = (E + B) * (D - d)/D
        sigma_v  = 12 * eta * v * D / (1000 * d^2)
        sigma_el + sigma_v > ΔP  =>  BLOCKED

    独自の近似式を持ってはならない。本図の境界線は FPGA の判定境界と一致する。
    """

    def required_boost(self, patient_data: dict):
        """
        現在の ΔP に対し BLOCKED を成立させるのに必要な最小 Boost [kPa]。
        判定は参照実装 nra_core_model に委譲する。
        """
        return _required_boost(patient_data)

    def generate_map(self, patient_data: dict, output_path: str) -> None:
        q = {k: _to_q88(patient_data.get(k, 0.0)) for k in
             ('cell_stiffness', 'cell_viscosity', 'cell_diameter',
              'pore_size', 'flow_dp', 'drug_boost')}
        E_q, eta_q = q['cell_stiffness'], q['cell_viscosity']
        D_q, d_q = q['cell_diameter'], q['pore_size']
        v_q = _to_q88(patient_data.get('deform_velocity', DEFAULT_DEFORM_VELOCITY))
        cur_boost = patient_data.get('drug_boost', 0.0)
        cur_flow  = patient_data.get('flow_dp', 0.6)
        p_id      = patient_data.get('patient_id', 'Unknown')
        cancer    = patient_data.get('cancer_type', '')

        boost_axis = np.linspace(0.0, 10.0, 301)
        flow_axis  = np.linspace(0.0,  5.0, 301)
        B_q = (boost_axis * 256).astype(np.int64)
        F_q = (flow_axis * 256).astype(np.int64)

        # 妥当性判定も参照実装に委譲する（Boost は軸なので 0 で評価）
        # エラー名は nra_core_model.ERR_NAME を参照する（本ファイルに複製しない）
        err_code = _check_inputs(dict(q, drug_boost=0))
        err = (f'0x{err_code:02X} {ERR_NAME[err_code]}'
               if err_code in (ERR_VISC0, ERR_RANGE, ERR_GEOM) else None)

        if err:
            # 異常時は転移リスク側（全面 PASSABLE）へ倒す＝Fail-Closed
            is_blocked = np.zeros((len(F_q), len(B_q)), dtype=float)
        else:
            strain, sigma_v = _fixed_terms(eta_q, D_q, d_q, v_q)
            sigma_el = ((E_q + B_q) * strain) >> 8          # (1, nB)
            sigma_tot = sigma_el + sigma_v
            is_blocked = (sigma_tot[None, :] > F_q[:, None]).astype(float)

        Bg, Fg = np.meshgrid(boost_axis, flow_axis)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.contourf(Bg, Fg, is_blocked,
                    levels=[-0.5, 0.5, 1.5],
                    colors=['#ffcccc', '#ccffcc'], alpha=0.75)
        if 0.0 < is_blocked.mean() < 1.0:
            ax.contour(Bg, Fg, is_blocked,
                       levels=[0.5], colors=['#444444'], linewidths=1.8)

        # clip_on=False: 軸端（B=0 等）でも現在地マーカーを欠けさせない
        ax.plot(cur_boost, cur_flow, 'o',
                color='black', markersize=13, zorder=5, clip_on=False)
        ax.plot(cur_boost, cur_flow, '+',
                color='white', markersize=9, markeredgewidth=2.5,
                zorder=6, clip_on=False)

        ax.set_xlim(0, 10)
        ax.set_ylim(0,  5)
        ax.set_xlabel('Drug Boost B [kPa]', fontsize=12)
        ax.set_ylabel('Flow Pressure ΔP [kPa]', fontsize=12)

        subtitle = f'ERROR {err} — judgement invalid' if err else \
                   'Boundary identical to FPGA decision (Q8.8)'
        ax.set_title(
            f'NRA-IDE Jamming Map\nPatient: {p_id}  ({cancer})\n{subtitle}',
            fontsize=12, fontweight='bold'
        )
        ax.grid(True, alpha=0.3)

        legend_handles = [
            mpatches.Patch(color='#ccffcc', label='BLOCKED (cell cannot pass)'),
            mpatches.Patch(color='#ffcccc', label='PASSABLE (escape route open)'),
            mlines.Line2D([], [], marker='o', color='black',
                          markersize=10, linestyle='None', label='Current State'),
        ]
        ax.legend(handles=legend_handles, loc='upper right', fontsize=10)

        # BLOCKED は臨床的な「投与可」を意味しない（Gate Axiom）
        fig.text(0.5, 0.005,
                 'BLOCKED indicates physical containment only. '
                 'Treatment decision rests with the physician.',
                 ha='center', fontsize=8, color='#555555')

        dirpart = os.path.dirname(output_path)
        if dirpart:
            os.makedirs(dirpart, exist_ok=True)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"[OK] Jamming Map saved: {output_path}")
