# ═══════════════════════════════════════════════════════════════════════
# Project: NRA-IDE Cancer Treatment Support System
# Phase:   02
# File:    PHASE_2_Mesoscale_Physics.md
# ═══════════════════════════════════════════════════════════════════════

# Phase 2: Mesoscale Physics Protocol

## 1. Governing Equation (支配方程式)
細胞が血管の隙間（Pore）を通過できるか否かは、以下の抵抗力 $F_{resist}$ と 血流圧力 $\Delta P$ の闘争で決まる。

$$F_{resist} > \Delta P \cdot A \implies \text{SAFE (Blocked)}$$

### Type A: Jamming Model (Single Cell)
$$F_{resist} = (k_{cell} + Boost) \cdot \Delta x + \eta \cdot \frac{dv}{dt}$$

* $k_{cell}$: 細胞の硬さ（弾性係数） [kPa]
* $Boost$: 薬剤による硬化補強分 [kPa]
* $\Delta x$: 変形量（細胞直径 - 隙間サイズ） [μm]
* $\eta$: 細胞質および周囲水分の粘性 [Pa·s] **(※省略禁止)**

### Type B: Collective Model (Multi-Cell)
$$F_{collective} = N \cdot F_{single} \cdot (1 + \alpha \sqrt{N})$$

* $N$: 細胞数（クラスターサイズ）
* $\sqrt{N}$: 集団による非線形スクラム効果

## 2. Critical Rule: Viscosity
**「水分の粘性（$\eta$）をゼロにしてはならない」**
静的な硬さ（$k$）だけでなく、急激な血圧変動に耐えるには粘性抵抗（ダンパー効果）が不可欠である。
$\eta = 0$ の入力データは、物理的にあり得ないため即座にエラー（Error 0x03）とする。