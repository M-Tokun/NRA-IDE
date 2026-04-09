# nra-core

NRA-IDE（Nomological Ring Axioms — Intensional Dynamics Engine）のコアリポジトリです。
理論基盤・論文・実装コード・可視化の4領域に分類して管理します。

The core repository for NRA-IDE (Nomological Ring Axioms — Intensional Dynamics Engine).
Files are organized into four categories: theoretical foundations, papers, implementation, and visualization.

---

## ディレクトリ構成 / Directory Structure

```
nra-core/
├── foundations/   # 理論基盤
├── papers/        # 論文・技術文書
├── implementation/ # 実装コード
└── visualization/ # 可視化・シミュレーション
```

---

## foundations/ — 理論基盤 / Theoretical Foundations

NRA（律環公理）および IDE（内包動力学エンジン）の概念的・公理的基盤を記述した文書群。
システム全体の設計思想と数理構造の出発点となります。

Documents describing the conceptual and axiomatic foundations of NRA (Nomological Ring Axioms) and IDE (Intensional Dynamics Engine).
These form the starting point for the system's design philosophy and mathematical structure.

| ファイル | 内容 |
|---|---|
| `Nomological_Ring_Axioms_Code_Annotated_Explanation_Dual_Fluctuation_Stable.md` | 律環公理コード付き解説（二重ゆらぎ安定版） |
| `Nomological_Ring_AxiomsとIntensional_Dynamics_Engine.md` | NRAとIDEの統合概念記述 |
| `律環公理_コード付き解説_二重ゆらぎ安定版.md` | 上記の日本語版 |
| `NRA-IDE_の応用分野_汎用性の全体像.md` | NRA-IDEの応用領域と汎用性の概観 |

---

## papers/ — 論文・技術文書 / Papers & Technical Documents

NRA-IDEに関する学術論文・技術レポートおよびそのPDFを格納します。
理論の形式化・拡張提案・アーキテクチャ設計を扱います。

Academic papers, technical reports, and their PDFs related to NRA-IDE.
Covers formalization of theory, extension proposals, and architectural design.

| ファイル | 内容 |
|---|---|
| `NRA_IDE_Paper_v3_rev1_20260409_1923.md` / `.pdf` | NRA-IDE論文 v3 rev1（最新版） |
| `IDE_AdaptiveGate_Extension_20260407_2241.md` / `.pdf` | 適応ゲート拡張の技術文書 |
| `IDE-Classical_Hybrid_Architecture_for_Scalable_Nonlinear_Simulation.md` | 非線形大規模シミュレーション向けハイブリッドアーキテクチャ論文 |
| `IDE_Classical_Hybrid_非線形大規模シミュレーション…md` / `.pdf` | 上記の日本語版・PDF |

---

## implementation/ — 実装コード / Implementation

NRAおよびIDEの動作を実現するPythonスクリプト群。
基盤実装・適応ゲートの拡張コードを含みます。

Python scripts that realize the behavior of NRA and IDE.
Includes foundation implementations and adaptive gate extensions.

| ファイル | 内容 |
|---|---|
| `nra_ide_foundation_fixed_EN.py` | NRA-IDE基盤実装（英語コメント版） |
| `nra_ide_foundation_fixed_JP.py` | NRA-IDE基盤実装（日本語コメント版） |
| `IDE_AdaptiveGate_Extension_20260407_2241.py` | 適応ゲート拡張実装 |

---

## visualization/ — 可視化・シミュレーション / Visualization & Simulation

NRAダイナミクスのインタラクティブシミュレーション（HTML）および
解析結果のプロット画像を格納します。

Interactive simulations (HTML) of NRA dynamics and plot images of analysis results.

| ファイル | 内容 |
|---|---|
| `nra_simulation_02_EN.html` | NRAシミュレーション v2（英語UI） |
| `nra_simulation_02_JP.html` | NRAシミュレーション v2（日本語UI） |
| `nra_simulation_canvas.html` | NRAキャンバスベースシミュレーション |
| `NRA_IDE_v2a_basic_20260408.html` | NRA-IDE v2a 基本動作シミュレーション |
| `NRA_IDE_v2b_deg_v2_20260408.html` | NRA-IDE v2b 縮退モデルシミュレーション |
| `nra_foundation_plot_2026-02-20_2355.png` | NRA基盤解析プロット |
| `adaptive_gate_plot_2026-04-07_230258.png` | 適応ゲート解析プロット |

---

*Last updated: 2026-04-09*
