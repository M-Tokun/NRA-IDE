# ═══════════════════════════════════════════════════════════════════════
# File: references.md
# Phase: 60
# Date: 2026-02-01
# Purpose: 設計根拠・物理パラメータの出典一覧（エビデンス）
# ═══════════════════════════════════════════════════════════════════════

# NRA-IDE Reference List

本リストは、論文執筆のためではなく、**システム設定値（Phase 4/60）の正当性を証明するため**のものである。

## 🔬 Category 1: Cell Mechanics (細胞物理パラメータの根拠)

**[1] Paszek, M. J., et al. (2005)**
"Tensional homeostasis and the malignant phenotype."
*Cancer Cell*, 8(3), 241-254.
> **使用箇所:** 正常乳腺細胞と腫瘍細胞の硬度差（Stiffness）の基準値設定。
> **NRA-IDEへの適用:** `cell_stiffness` の正常範囲定義に使用。

**[2] Swaminathan, V., et al. (2011)**
"Mechanical stiffness grades metastatic potential in patient tumor cells and in cancer cell lines."
*Cancer Research*, 71(15), 5075-5080.
> **使用箇所:** 「転移しやすい細胞ほど柔らかい（Softening）」という逆説的現象の根拠。
> **NRA-IDEへの適用:** Type Aモデルにおいて、低い硬度（0.5 kPa付近）でもDANGER判定を出すロジックの裏付け。

**[3] CRC Handbook of Chemistry and Physics**
"Viscosity of Water and Selected Liquids."
> **使用箇所:** 水の粘性（0.001 Pa·s）の定義。
> **NRA-IDEへの適用:** システムの物理的下限値として使用。

**[4] Wirtz, D. (2009)**
"Particle-tracking microrheology of living cells: principles and applications."
*Annual Review of Biophysics*, 38, 301-326.
> **使用箇所:** 細胞質（Cytoplasm）の粘性が水より高い（0.01-0.1 Pa·s）ことの根拠。
> **NRA-IDEへの適用:** `cell_viscosity` のデフォルト値および「粘性ゼロ禁止」ルールの根拠。

**[5] Késmárky, G., et al. (2008)**
"Plasma viscosity: a forgotten variable."
*Clinical Hemorheology and Microcirculation*, 39(1-4), 243-246.
> **使用箇所:** 全血粘度（Whole Blood Viscosity）の基準値（0.003-0.004 Pa·s）。
> **NRA-IDEへの適用:** Phase 60 Viscosity Referenceにおける血液粘性の根拠。

## 🩸 Category 2: Vascular Physics (血管・血流パラメータの根拠)

**[6] Jain, R. K. (1987)**
"Transport of molecules in the tumor interstitium: a review."
*Cancer Research*, 47(12), 3039-3051.
> **使用箇所:** 腫瘍微小環境における間質圧力（Interstitial Fluid Pressure: IFP）。
> **NRA-IDEへの適用:** `flow_dp` の上限値（5.0 kPa）設定の根拠。腫瘍内圧力は正常組織より高く、1-3 kPa程度まで上昇する。

**[7] Wirtz, D., Konstantopoulos, K., & Searson, P. C. (2011)**
"The physics of cancer: the role of physical interactions and mechanical forces in metastasis."
*Nature Reviews Cancer*, 11(7), 512-522.
> **使用箇所:** 癌細胞が毛細血管の隙間（3-8 μm）を通過するメカニズム。
> **NRA-IDEへの適用:** `pore_size` の範囲（5.0-15.0 μm）設定の根拠。毛細血管内皮の間隙は通常5-10 μm、腫瘍血管では最大15 μm程度まで拡大する。

**[8] Fung, Y. C. (1993)**
"Biomechanics: Mechanical Properties of Living Tissues." (2nd ed.)
*Springer-Verlag*, New York.
> **使用箇所:** 生体組織の力学的特性に関する包括的データ。
> **NRA-IDEへの適用:** `cell_diameter`（5.0-30.0 μm）の範囲設定。赤血球（7-8 μm）から大型癌細胞（20-30 μm）までをカバー。

## ⚙️ Category 3: Engineering (実装方式の根拠)

**[9] IEEE Standard 754-2019**
"IEEE Standard for Floating-Point Arithmetic."
> **使用箇所:** 浮動小数点の不確定性（丸め誤差）に関する定義。
> **NRA-IDEへの適用:** 本システムがこれを**採用せず**、Q8.8固定小数点を選択した理由（決定論的動作の保証）として参照。

**[10] Xilinx / Intel FPGA Documentation**
"DSP Block Usage in Artix-7 / Cyclone V."
> **使用箇所:** パイプライン設計における乗算器（DSP）のレイテンシ定義。
> **NRA-IDEへの適用:** Phase 6 のタイミング設計の基礎。

## 🏥 Category 4: Clinical Background (医学的背景)

**[11] Chaffer, C. L., & Weinberg, R. A. (2011)**
"A perspective on cancer cell metastasis."
*Science*, 331(6024), 1559-1564.
> **使用箇所:** がん転移が「物理的な障壁（Basement Membrane）」の突破から始まるというメカニズム。
> **NRA-IDEへの適用:** Phase 1 哲学（物理的封じ込め）の医学的正当性。
