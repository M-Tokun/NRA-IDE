# NRA-IDE Safety Map Plotter (2026-01-30)
# Description: FPGAの適合結果(+2.852kPa)に基づき、安全地帯を可視化する

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def run_visualization():
    # 1. Parameter Space
    stiffness_range = np.linspace(0.1, 2.0, 100) # Cell Base Stiffness
    pressure_range = np.linspace(100, 1000, 100) # Blood Pressure
    X, Y = np.meshgrid(stiffness_range, pressure_range)

    # 2. Fixed Conditions & Solution
    D_cell, d_gap = 12.0, 8.0
    deformation = max(0, D_cell - d_gap)
    DRUG_BOOST = 2.852 # ★FPGA Result

    # 3. Physics Logic
    alpha = 250.0
    total_stiffness = X + DRUG_BOOST
    calculated_resistance = total_stiffness * deformation * alpha
    Z = calculated_resistance - Y # Safety Factor

    # 4. Plot
    plt.figure(figsize=(10, 6))
    plt.contourf(X, Y, Z, levels=20, cmap=sns.diverging_palette(10, 130, as_cmap=True), alpha=0.8)
    plt.contour(X, Y, Z, levels=[0], colors='white', linewidths=3, linestyles='--')
    plt.title(f'Safety Map (Boost = +{DRUG_BOOST} kPa)')
    plt.xlabel('Cell Stiffness (kPa)'); plt.ylabel('Pressure (Pa)')
    plt.text(1.0, 500, "SAFE ZONE", color='white', fontweight='bold', ha='center')
    plt.show()

if __name__ == "__main__":
    run_visualization()
