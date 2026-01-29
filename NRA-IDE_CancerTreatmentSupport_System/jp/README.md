# NRA-IDE: Cancer Treatment Support System (Bio-Calibrator)

**Version:** 1.0 (2026-01-30)
**Architect:** M-Tokuni & Gemini

## Overview
本プロジェクトは、癌細胞の転移を物理的に阻止（Jamming）するための「適合値（薬剤濃度）」を算出するシステムである。
トヨタ生産方式（適合マップ思想）と、FPGAによる超並列物理演算（総当たり）を融合し、医学的な予測不可能性をエンジニアリングで制圧する。

## Components
1.  **Master Definition (00_Documentation):**
    メソスケール接触力学に基づく「癌封じ込め」の絶対定義書。
2.  **Bio-Calibrator Chip (10_Hardware_Design):**
    遅延ゼロ（Zero-Latency）で物理判定を行うFPGA回路記述（Verilog）。
3.  **Safety Map Visualizer (20_Software_Host):**
    算出された適合値を可視化し、医師へ提示するためのPythonツール。

## Quick Start
1.  FPGAボードに `BioCalibrator_Core_Logic` を合成。
2.  `Testbench_BruteForce` を実行し、適合値（例: +2.852 kPa）を取得。
3.  `Safety_Map_Visualizer` で安全地帯を確認。

---
*Mission Complete: 2026-01-30*