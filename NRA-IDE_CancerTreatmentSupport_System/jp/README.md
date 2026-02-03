# ═══════════════════════════════════════════════════════════════════════
# Project: NRA-IDE Cancer Treatment Support System (Bio-Calibrator)
# Type:    Medical Engineering Protocol / Reference Design
# Phase:   00 (Root)
# File:    README.md
# Updated: 2026-02-03 13:40:27 JST
# Change:  §4 — 「臨床」削除、LICENSE特約事項1・免責事項との整合修正
# ═══════════════════════════════════════════════════════════════════════

# NRA-IDE Protocol: Cancer Metastasis Suppression Framework

**Version:** 1.0 (Final Template / Snapshot)
**Architect:** M-Tokuni
**Concept:** "Physics over Statistics"

## 1. Project Identity
本パッケージは、特定のソフトウェア製品ではなく、**癌転移を物理的に阻止するための「設計図（プロトコル）」および「実装テンプレート」**である。

「医学的な予測不可能性」に対し、構造力学とFPGAを用いた「決定論的エンジニアリング」でアプローチする手法（NRA-IDE）を体系化し、無償のテンプレートとして医療・工学分野へ提供する。

## 2. Ritsukan Axiom (The Constitution)
**律環公理（Ritsukan Axiom）**は、本システムのアルゴリズムではなく、**遵守すべき「物理的・論理的憲法」**である。
本テンプレートを使用する場合、以下の公理を削除・改変することはできない。

1.  **因果ダイオード (Causal Diode):**
    「結果（SAFE）」を得るために「入力（物理パラメータ）」を逆算・操作することを禁ずる。
2.  **ギアメカニズム (Fail-Closed):**
    計算プロセスにおける不整合（欠損、ゼロ粘性）は、すべて「DANGER（停止）」として処理しなければならない。
3.  **ゲート公理 (Gate Axiom):**
    システムは物理的根拠のみを提示する。最終的な臨床判断と責任は、人間（医師）が保持する。

## 3. Package Structure
本パッケージには、プロトコルを構成する9つのフェーズと実装例が含まれている。

* `00_Documentation/`: **[Protocol]** 哲学、物理モデル、公理定義（仕様書の本体）
* `10_Hardware_Design/`: **[Reference]** FPGA回路の参照実装（Verilog HDL）
* `20_Software_Host/`: **[Reference]** ホスト制御の参照実装（Python）
* `30_Test_Data/`: **[Validation]** 物理整合性検証用データセット
* `40_Output_Reports/`: **[Template]** 臨床レポート様式
* `50_Deployment/`: **[Guide]** 導入・運用ガイドライン
* `60_Research/`: **[Resource]** 実務用物理定数データ

## 4. Usage
本プロジェクトは**「無償の医療支援テンプレート」**である。
著作権は保持されるが、研究・教育を目的とした利用において、誰でも自由に利用・改変・再配布が可能である（MIT License準拠）。

臨床適用には、別途規制当局（PMDA・FDA等）による承認が必要である。

ただし、**「律環公理」を無視した改変を行った場合、それはもはやNRA-IDEではない。**

---

## ⚠️ Version & Language Policy

**Version:**
This package is a **Fixed Snapshot (v1.0)**.
本パッケージは、整合性が検証された固定バージョンです。外部リポジトリの更新による影響を受けません。

**Language:**
The official language of this protocol is **Japanese ONLY**.
誤訳による医療リスクを回避するため、公式な英語版は提供されません。
To avoid medical risks caused by mistranslation, an official English version will not be provided.
