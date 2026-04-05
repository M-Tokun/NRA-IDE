# ═══════════════════════════════════════════════════════════════════════
# File: PHASE_60_Practical_Resources.md
# Phase: 60
# Date: 2026-02-01
# Purpose: 実務用物理定数・パラメータソース（データブック）
# ═══════════════════════════════════════════════════════════════════════

# Phase 60: Practical Resources

## 1. Cell Stiffness ($k_{cell}$) Reference
FPGAに入力する際の基準値。異常値検知（Phase 20）の根拠となる。

| Cell Type | Stiffness (kPa) | Source | Note |
|:---|:---:|:---:|:---|
| Normal Breast | 0.4 - 0.8 | [1] | 正常細胞は柔らかい |
| Breast Tumor (Avg) | 1.5 - 4.0 | [1] | がん化すると硬くなる（ECM硬化） |
| Metastatic (High) | 0.5 - 1.0 | [2] | **注意:** 転移能が高い細胞は逆に柔らかくなる（変形しやすいため） |

## 2. Viscosity ($\eta$) Reference
Phase 2 物理モデルにおいて、動的な抵抗力を決定する重要パラメータ。
**警告: 0入力禁止（律環公理違反）**

| Material | Viscosity (Pa·s) | Source | Note |
|:---|:---:|:---:|:---|
| Water | 0.001 | [3] | 物理的下限基準 |
| Cytoplasm | 0.01 - 0.1 | [4] | 細胞質（細胞内部の液体） |
| Whole Blood | 0.003 - 0.004 | [5] | 血液全体（参考値） |

## 3. Cell Diameter ($D$) Reference
癌細胞サイズの基準値。

| Cell Type | Diameter (μm) | Source | Note |
|:---|:---:|:---:|:---|
| Red Blood Cell | 7 - 8 | [8] | 比較基準（通過しやすい） |
| Normal Epithelial | 10 - 15 | [8] | 正常上皮細胞 |
| Cancer Cell (Typical) | 15 - 25 | [8] | 腫瘍細胞（肥大傾向） |
| Large Cancer Cell | 25 - 30 | [8] | 大型癌細胞（System上限付近） |

## 4. Pore Size ($d$) Reference
血管内皮の隙間サイズ。転移の物理的障壁。

| Vessel Type | Pore Size (μm) | Source | Note |
|:---|:---:|:---:|:---|
| Normal Capillary | 5 - 8 | [7] | 正常毛細血管（tight junction） |
| Tumor Vasculature | 10 - 15 | [7] | 腫瘍血管（漏れやすい構造） |

## 5. Flow Pressure ($\Delta P$) Reference
血流による推進力。

| Condition | Pressure (kPa) | Source | Note |
|:---|:---:|:---:|:---|
| Normal Interstitial | 0.0 - 0.3 | [6] | 正常組織間質圧 |
| Tumor Core | 1.0 - 3.0 | [6] | 腫瘍中心部（高圧） |
| Hypertensive Peak | 3.0 - 5.0 | [6] | 高血圧・炎症時（System上限） |

## 6. Q8.8 Conversion Table
現場エンジニア向け早見表（16bit Hex）。

| Float | Hex (Q8.8) | Meaning |
|:---:|:---:|:---|
| 0.01 | `0x0002` | 粘性下限付近 |
| 0.1 | `0x0019` | 最小分解能付近 |
| 0.5 | `0x0080` | 正常細胞相当 |
| 1.0 | `0x0100` | 基準単位 (1.0) |
| 5.0 | `0x0500` | 直径/隙間の下限 |
| 10.0| `0x0A00` | システム上限値 |
| 30.0| `0x1E00` | 直径の上限 |

## 7. Reference Link
詳細な出典情報は同ディレクトリの `references.md` を参照のこと。
