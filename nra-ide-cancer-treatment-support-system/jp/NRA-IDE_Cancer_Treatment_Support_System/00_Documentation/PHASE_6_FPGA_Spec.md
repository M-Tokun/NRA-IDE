# ═══════════════════════════════════════════════════════════════════════
# Project: NRA-IDE Cancer Treatment Support System
# Phase:   06
# File:    PHASE_6_FPGA_Spec.md
# ═══════════════════════════════════════════════════════════════════════

# Phase 6: FPGA Implementation Specification

## 1. Computational Logic (Q8.8)
浮動小数点（Float）は使用しない。全ての物理量は **16ビット固定小数点（整数部8bit + 小数部8bit）** で扱う。
* 分解能: $1/256 \approx 0.0039$
* 利点: 回路が単純、演算誤差が蓄積しない、検証が容易。

## 2. Pipeline Stages
* **Stage 1:** 入力ラッチ & 幾何学的判定（$D < d$ ?）
* **Stage 2:** 変形量計算（$\Delta x = D - d$）
* **Stage 3:** 弾性力・粘性力の並列計算
* **Stage 4:** 総抵抗力 $F_{resist}$ の合算
* **Stage 5:** 圧力比較判定 & エラーコード確定

## 3. Register Map
内部レジスタは全てリセット同期（`rst_n`）。
通信モジュール（UART）からのデータは、CheckSum OKのタイミングでCoreモジュールへアトミックに転送される。