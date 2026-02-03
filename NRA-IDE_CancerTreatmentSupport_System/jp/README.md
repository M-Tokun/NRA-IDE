
# ═══════════════════════════════════════════════════════════════════════

# Project: NRA-IDE Cancer Treatment Support System

# Phase:   Master (Root)

# File:    README.md (Final Integrated Version)

# ═══════════════════════════════════════════════════════════════════════

## 1. プロジェクト概要 (Project Overview)

**NRA-IDE**（Non-statistical Ritsukan Axiom - Integrated Deterministic Engine）は、癌細胞の物理的特性を解析し、転移リスクを決定論的に判定する次世代のがん治療支援システムです。

従来の医療AIが数百万人の「統計（平均）」に依存するのに対し、本システムは目の前の患者一人の「物理（実測値）」に依拠します。
物理法則（構造力学）によって計算される「転移が不可能な条件」を特定し、治療計画を支援します。

## 2. 核心哲学：律環公理 (The Ritsukan Axiom)

本システムの全ての設計判断は、以下の3つの公理に従っています。

1. **Physics First (物理第一主義):** 判定の根拠はすべて物理式 

 で説明可能であり、ブラックボックスを排除する。
2. **Fail-Closed (ギアメカニズム):** 通信、計算、入力のいずれかに 1ビットでも不確実性があれば、システムは安全側に倒れ、警告（Error）を発する。
3. **Gate Axiom (ゲート公理):** システムは計算機に徹する。最終的な「治療の断行」は、倫理的責任を負う医師が決定する。

## 3. 技術アーキテクチャ (Technical Architecture)

本システムは、高い再現性とリアルタイム性を保証するため、ハードウェアとソフトウェアのハイブリッド構成を採用しています。

* **Compute Layer (FPGA):** Intel Cyclone V / Xilinx Artix-7 上で動作する専用演算回路。Q8.8 固定小数点演算により、OSの介入を排した決定論的計算を実行。
* **Control Layer (Python):** 医師の入力を物理的に検証し、FPGA とバイナリプロトコルで通信。臨床レポートと安全マップ（Safety Map）を生成。
* **Verification Layer:** 物理シミュレーションに基づく期待値（Oracle）を用いた自動診断機能を備え、稼働前の健全性を証明。

## 4. クイックスタート (Quick Start)

導入と運用の詳細は以下のドキュメントを参照してください。

1. **設置:** `50_Deployment/installation_guide.md` に従い、FPGA と PC を接続。
2. **起動:** `python main.py --test` を実行し、自己診断をパスすることを確認。
3. **運用:** `python main.py --data patient.json` を実行し、臨床レポートを出力。

---
---

**免責事項:** 本システムは「物理的な計算結果」を提示する無償支援テンプレートツールです。
基本は研究用で臨床用ではありません。
---
