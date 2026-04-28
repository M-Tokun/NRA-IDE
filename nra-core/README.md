# nra-core

NRA-IDE（Nomological Ring Axioms — Intensional Dynamics Engine）のコアリポジトリです。

理論基盤・論文・実装コード・可視化・量子拡張の5領域に分類して管理します。

The core repository for NRA-IDE (Nomological Ring Axioms — Intensional Dynamics Engine).

Files are organized into five categories: theoretical foundations, papers, implementation, visualization, and quantum extension.

---

## ディレクトリ構成 / Directory Structure

```

nra-core/

├── foundations/   # 理論基盤

├── papers/        # 論文・技術文書

├── implementation/ # 実装コード

├── visualization/ # 可視化・シミュレーション

└── quantum/       # 量子拡張

```

---

## foundations/ — 理論基盤 / Theoretical Foundations

NRA（律環公理）および IDE（内包動力学エンジン）の概念的・公理的基盤を記述した文書群。

システム全体の設計思想と数理構造の出発点となります。

Documents describing the conceptual and axiomatic foundations of NRA (Nomological Ring Axioms) and IDE (Intensional Dynamics Engine).

These form the starting point for the system's design philosophy and mathematical structure.

| ファイル | 内容 |

|---|---|

| `AXIOMS_rewritten_2026-04-24_011508.md` / `.pdf` | **律環公理 公理群定義書 v1.2** — Axiom 0〜10 正式定義（二言語） |

| `Nomological_Ring_Axioms_Code_Annotated_Explanation_Dual_Fluctuation_Stable.md` | 律環公理コード付き解説（二重ゆらぎ安定版・EN） |

| `律環公理_コード付き解説_二重ゆらぎ安定版.md` | 上記の日本語版 |

| `Nomological_Ring_AxiomsとIntensional_Dynamics_Engine.md` | NRAとIDEの統合概念記述（会話記録・完全版） |

| `NRA-IDE_の応用分野_汎用性の全体像.md` | NRA-IDEの応用領域と汎用性の概観 |

> 原本は `theory/AXIOMS_rewritten_2026-04-24_011508.md`。nra-core の自己完結性のため本ディレクトリにも収録。

> The canonical source is `theory/AXIOMS_rewritten_2026-04-24_011508.md`. Copied here for nra-core self-containment.

---

## papers/ — 論文・技術文書 / Papers & Technical Documents

NRA-IDEに関する学術論文・技術レポートおよびそのPDFを格納します。

理論の形式化・拡張提案・アーキテクチャ設計を扱います。

Academic papers, technical reports, and their PDFs related to NRA-IDE.

Covers formalization of theory, extension proposals, and architectural design.

| ファイル | 内容 |

|---|---|

| `NRA_IDE_Paper_v3_rev2_20260409_2130.md` / `.pdf` | NRA-IDE論文 v3 rev2（最新版） |

| `NRA_IDE_Paper_JP_Chapter2_final_20260412_2219.md` | NRA-IDE論文 JP 第2章（確定版） |

| `NRA_IDE_Paper_JP_Chapter3_20260413_0235.md` | NRA-IDE論文 JP 第3章 |

| `IDE_AdaptiveGate_Extension_20260407_2241.md` / `.pdf` | 適応ゲート拡張の技術文書 |

| `IDE-Classical_Hybrid_Architecture_for_Scalable_Nonlinear_Simulation.md` | ハイブリッドアーキテクチャ論文（EN） |

| `IDE_Classical_Hybrid_非線形大規模シミュレーションにおけるIDEと古典計算のハイブリッドアーキテクチャ.md` / `IDE_Classical_Hybrid_Architecture.pdf` | 上記の日本語版・PDF |

| `NRA-IDE_quantum_mapping_2026-03-31_0132_JP.md` | 量子マッピング技術文書（JP） |

| `NRA-IDE_quantum_mapping_2026-03-31_0132_EN.md` | 量子マッピング技術文書（EN） |

| `deepseek_latex_20260413_157067.md` | LaTeX変換セッション記録 |

---

## implementation/ — 実装コード / Implementation

NRAおよびIDEの動作を実現するPythonスクリプト群。

基盤実装・適応ゲート拡張・センサー系応用コードを含みます。

Python scripts that realize the behavior of NRA and IDE.

Includes foundation implementations, adaptive gate extension, and applied sensor-system examples.

| ファイル | 内容 |

|---|---|

| `nra_ide_foundation_fixed_JP.py` | NRA-IDE基盤実装（日本語コメント版） |

| `nra_ide_foundation_fixed_EN.py` | NRA-IDE基盤実装（英語コメント版） |

| `IDE_AdaptiveGate_Extension_20260407_2241.py` | 適応ゲート拡張実装（動的k_eff・相対座標IDE・PDダンパー） |

| `belt_tension_nra_ide_2026-03-19_0059_JP.py` | ベルト張力 NRA-IDE実装（JP） |

| `belt_tension_nra_ide_2026-03-19_0059_EN.py` | ベルト張力 NRA-IDE実装（EN） |

| `chain_tension_nra_ide_2026-03-19_0113_JP.py` | チェーン張力 NRA-IDE実装（JP） |

| `chain_tension_nra_ide_2026-03-19_0113_EN.py` | チェーン張力 NRA-IDE実装（EN） |

---

## visualization/ — 可視化・シミュレーション / Visualization & Simulation

NRAダイナミクスのインタラクティブシミュレーション（HTML）および

解析結果のプロット画像を格納します。

Interactive simulations (HTML) of NRA dynamics and plot images of analysis results.

| ファイル | 内容 |

|---|---|

| `NRA_IDE_Axiom1_RigidityPlay_20260425.html` | **公理1「遊びのない厳密さは崩壊する」直接可視化** — τ≈0 vs τ適切 比較 |

| `NRA_IDE_AdaptiveGate_20260425.html` | **適応ゲート拡張 — 固定k vs 動的k_eff** — 3提案統合・ゼリー比喩 |

| `NRA_IDE_FullPaper_20260416.html` | NRA-IDE 論文全章インタラクティブ表示 |

| `NRA_IDE_ClassicalAI_vs_NRAIDE_20260416.html` | 古典計算AI vs NRA-IDE組み込みAI 比較 |

| `NRA_IDE_AIRisk_Layer5_20260416.html` | 現況AI学習の構造的リスクと将来予測（Layer 5） |

| `NRA_IDE_Formula_Diagram_20260416.html` | 定義式・応用式 構造図解 |

| `NRA_IDE_PropertyError_20260416.html` | 性質誤差 — なぜ破綻しないか |

| `NRA_IDE_Quantum_Error_20260416.html` | 量子誤差 — δはゼロにできない |

| `NRA_IDE_Battery_Comparison_20260412_2054.html` | スマートフォンバッテリー比較シミュレーション |

| `NRA_IDE_v2b_deg_v2_20260408.html` | τ劣化モデル — ダム・サンゴ（Axiom 4/5） |

| `NRA_IDE_v2a_basic_20260408.html` | 基本シナリオ — 作業者・橋・電池 |

| `nra_simulation_02_EN.html` | NRAシミュレーション v2（英語UI） |

| `nra_simulation_02_JP.html` | NRAシミュレーション v2（日本語UI） |

| `nra_simulation_canvas.html` | NRAキャンバスベースシミュレーション |

| `nra_foundation_plot_2026-02-20_2355.png` | NRA基盤解析プロット |

| `adaptive_gate_plot_2026-04-07_230258.png` | 適応ゲート解析プロット |

---

## quantum/ — 量子拡張 / Quantum Extension

NRA-IDEを量子計算領域へ接続するPythonスクリプトおよびセッション記録。

Lindblad方程式・NISQ・FMOモデルを用いた量子誤差制御の実装群。

Python scripts and session records connecting NRA-IDE to quantum computing.

Implementations of quantum error control using Lindblad equations, NISQ, and FMO models.

| ファイル | 内容 |

|---|---|

| `NRA-IDE_quantum_Python/01_rhizosphere_quantum_demo.py` | 根圏量子デモ — 基礎実装 |

| `NRA-IDE_quantum_Python/02_rhizosphere_nested_quantum.py` | 根圏ネスト量子デモ |

| `NRA-IDE_quantum_Python/03_nisq_fmo_2site.py` | NISQ-FMO 2サイトモデル |

| `NRA-IDE_quantum_Python/04_nisq_fmo_3site.py` | NISQ-FMO 3サイトモデル |

| `NRA-IDE_quantum_Python/05_fmo_fluctuation_path_log.py` | FMO揺らぎ経路ログ |

| `NRA-IDE_quantum_Python/06_quantum_error_control_demo.py` | 量子誤差制御デモ（IDE統合） |

| `NRA-IDE_quantum_Python/NRA-IDE_量子拡張セッションサマリー_2026-03-28.md` | 量子拡張セッションサマリー（JP） |

| `NRA-IDE_quantum_Python/NRA_IDE_Quantum_Measurement_Session_2026-03-28_1920.md` | 量子測定セッション記録（EN） |

---

*Last updated: 2026-04-25*
