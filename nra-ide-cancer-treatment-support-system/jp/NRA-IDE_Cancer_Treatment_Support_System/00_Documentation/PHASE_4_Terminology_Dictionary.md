# ═══════════════════════════════════════════════════════════════════════

# Project: NRA-IDE Cancer Treatment Support System

# Phase:   04

# File:    PHASE_4_Terminology_Dictionary.md

# ═══════════════════════════════════════════════════════════════════════



# Phase 4: Complete Terminology Dictionary



## 1. Parameters & Ranges (Q8.8 Fixed Point)



| Variable | Symbol | Unit | Range | Q8.8 Hex (Min-Max) | Note |

|:---|:---:|:---:|:---:|:---:|:---|

| `cell_stiffness` | $k$ | kPa | 0.1 - 10.0 | `0x0019` - `0x0A00` | 硬さ |

| `cell_viscosity` | $\eta$ | Pa·s | 0.01 - 1.0 | `0x0002` - `0x0100` | **0禁止** |

| `cell_diameter` | $D$ | μm | 5.0 - 30.0 | `0x0500` - `0x1E00` | 大きさ |

| `pore_size` | $d$ | μm | 5.0 - 15.0 | `0x0500` - `0x0F00` | 隙間 |

| `flow_dp` | $\Delta P$ | kPa | 0.0 - 5.0 | `0x0000` - `0x0500` | 血圧差 |

| `drug_boost` | $B$ | kPa | 0.0 - 10.0 | `0x0000` - `0x0A00` | 薬剤効果 |



## 2. Error Codes



| Code | Name | Description | Action |

|:---:|:---|:---|:---|

| `0x00` | ERR_NONE | 正常（SAFE/DANGER判定有効） | - |

| `0x01` | ERR_GEOMETRIC | すり抜け（$D < d$） | 手術検討 |

| `0x02` | ERR_NEGATIVE | 負の物理量 | 再測定 |

| `0x03` | ERR_ZERO_VISC | 粘性ゼロ | 再測定 |

| `0x04` | ERR_OVERFLOW | 演算オーバーフロー | システム点検 |

