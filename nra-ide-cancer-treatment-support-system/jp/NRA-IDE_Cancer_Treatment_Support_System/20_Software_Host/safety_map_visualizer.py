# ═══════════════════════════════════════════════════════════════════════
# File: safety_map_visualizer.py
# Phase: 20 (Safety Map Generation)
# Date: 26-0203-1740 JST
# ═══════════════════════════════════════════════════════════════════════

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

class SafetyMapVisualizer:
    """
    X軸: Drug Boost [kPa]  — 右ほど細胞が硬くなり通過しにくい
    Y軸: Blood Pressure (Flow ΔP) [kPa]  — 上ほど押し込み力が強い（危険）
    Green Zone (SAFE) : F_resist > F_flow  → 物理的封鎖成立
    Red Zone (DANGER) : F_resist <= F_flow → 転移リスク高
    """

    def generate_map(self, patient_data: dict, output_path: str) -> None:
        stiffness = patient_data.get('cell_stiffness', 1.5)
        viscosity = max(patient_data.get('cell_viscosity', 0.05), 1e-6)
        diameter  = patient_data.get('cell_diameter', 12.0)
        pore      = patient_data.get('pore_size', 8.0)
        cur_boost = patient_data.get('drug_boost', 0.0)
        cur_flow  = patient_data.get('flow_dp', 0.6)
        p_id      = patient_data.get('patient_id', 'Unknown')
        cancer    = patient_data.get('cancer_type', '')

        boost_axis = np.linspace(0.0, 10.0, 300)
        flow_axis  = np.linspace(0.0,  5.0, 300)
        B, F = np.meshgrid(boost_axis, flow_axis)

        # 物理モデル: 有効抵抗力 = (stiffness + boost) * (pore/diameter)^2 / viscosity
        resist = (stiffness + B) * (pore / diameter) ** 2 / viscosity
        is_safe = resist > F  # True = SAFE (Jamming)

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.contourf(B, F, is_safe.astype(float),
                    levels=[-0.5, 0.5, 1.5],
                    colors=['#ffcccc', '#ccffcc'], alpha=0.75)
        ax.contour(B, F, is_safe.astype(float),
                   levels=[0.5], colors=['#444444'], linewidths=1.8)

        ax.plot(cur_boost, cur_flow, 'o',
                color='black', markersize=13, zorder=5)
        ax.plot(cur_boost, cur_flow, '+',
                color='white', markersize=9, markeredgewidth=2.5, zorder=6)

        ax.set_xlim(0, 10)
        ax.set_ylim(0,  5)
        ax.set_xlabel('Drug Boost [kPa]', fontsize=12)
        ax.set_ylabel('Blood Pressure (Flow ΔP) [kPa]', fontsize=12)
        ax.set_title(
            f'NRA-IDE Safety Map\nPatient: {p_id}  ({cancer})',
            fontsize=13, fontweight='bold'
        )
        ax.grid(True, alpha=0.3)

        legend_handles = [
            mpatches.Patch(color='#ccffcc', label='SAFE Zone (Jamming)'),
            mpatches.Patch(color='#ffcccc', label='DANGER Zone (Pass-through)'),
            mlines.Line2D([], [], marker='o', color='black',
                          markersize=10, linestyle='None', label='Current State'),
        ]
        ax.legend(handles=legend_handles, loc='upper right', fontsize=10)

        dirpart = os.path.dirname(output_path)
        if dirpart:
            os.makedirs(dirpart, exist_ok=True)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"✓ Safety Map saved: {output_path}")
