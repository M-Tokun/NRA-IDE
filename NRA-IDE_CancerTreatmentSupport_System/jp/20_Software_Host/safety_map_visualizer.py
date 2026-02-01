# ═══════════════════════════════════════════════════════════════════════
# File: safety_map_visualizer.py
# Phase: 20
# Date: 2026-02-01
#
# 目的: 安全域（SAFE Zone）の可視化
# 依存: matplotlib, numpy
# ═══════════════════════════════════════════════════════════════════════

import matplotlib.pyplot as plt
import numpy as np

class SafetyMapVisualizer:
    def generate_map(self, data: dict, filename: str = "SafetyMap.png"):
        """
        簡易的な2Dマップ生成:
        横軸: Boost (0-10)
        縦軸: Pressure (0-5)
        """
        boosts = np.linspace(0, 10, 100)
        pressures = np.linspace(0, 5, 100)
        B, P = np.meshgrid(boosts, pressures)

        # Phase 2 Physics (Simplified for Viz)
        k = data['cell_stiffness']
        dx = max(0, data['cell_diameter'] - data['pore_size'])
        # Viscosity term assumed constant for static map

        # F_resist = (k + B) * dx
        # Safe if F_resist > P * Scale
        F_resist = (k + B) * dx * 0.1 # Scale factor adjust

        Z = F_resist - P

        plt.figure(figsize=(8, 6))
        plt.contourf(B, P, Z, levels=[-10, 0, 10], colors=['#FFDDDD', '#DDFFDD'])
        plt.contour(B, P, Z, levels=[0], colors='k', linewidths=2)

        # Plot Current Point
        plt.plot(0, data['flow_dp'], 'ro', label='Current')

        plt.title(f"NRA-IDE Safety Map (ID: {data.get('patient_id','Unknown')})")
        plt.xlabel("Drug Boost [kPa]")
        plt.ylabel("Blood Pressure [kPa]")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)

        plt.savefig(filename)
        plt.close()
        print(f"✓ Map Saved: {filename}")
