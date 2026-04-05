# ═══════════════════════════════════════════════════════════════════════
# File: SafetyMap_Description.md
# Phase: 40
# Date: 2026-02-01
# ═══════════════════════════════════════════════════════════════════════

# Safety Map Visualization Guide

## 1. Overview
`safety_map_visualizer.py` によって生成される `SafetyMap.png` は、現在の患者の状態が「物理的な安全域（SAFE Zone）」に対してどこに位置するかを可視化する。

## 2. Axis Definitions
* **X-Axis (Horizontal): Drug Boost [kPa]**
  * 薬剤投与によって補強される細胞硬度。
  * 右に行くほど細胞が硬くなり、通過しにくくなる。
* **Y-Axis (Vertical): Blood Pressure [kPa]**
  * 血流による推進力。
  * 上に行くほど圧力が高まり、細胞が押し込まれやすくなる（危険）。

## 3. Zones
* **🟩 Green Zone (SAFE):**
  * 物理的封鎖（Jamming）が成立している領域。
  * $F_{resist} > F_{flow}$
* **🟥 Red Zone (DANGER):**
  * 細胞が変形して通過可能な領域。
  * 転移リスクが高い状態。

## 4. Usage
医師はこのマップを見て、「現在の血圧（Y）に対して、どれだけの薬剤（X）が必要か」を直感的に判断する。