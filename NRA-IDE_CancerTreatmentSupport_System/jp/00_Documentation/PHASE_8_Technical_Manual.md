
# ═══════════════════════════════════════════════════════════════════════
# Project: NRA-IDE Cancer Treatment Support System
# Phase:   08
# File:    PHASE_8_Technical_Manual.md
# ═══════════════════════════════════════════════════════════════════════

# Phase 8: Technical Manual

## 1. Synthesis Guide
* **Intel Quartus:** `50_Deployment/bitstreams/` の `.qpf` を開き、"Compile Design" を実行。
* **Xilinx Vivado:** `.xpr` を開き、"Generate Bitstream" を実行。
* **Timing Constraint:** `timing.sdc` が正しく読み込まれているか確認すること（100MHz）。

## 2. Debugging
* **LED 0 (Green):** SAFE判定時に点灯
* **LED 1 (Red):** エラー発生時に点滅
* **UART Debug:** オシロスコープでTXピンを観測し、`0xA5` ヘッダが見えるか確認。

## 3. Common Issues
* **通信しない:** ボーレートが115200か？ USBケーブルは通信用か？
* **常にエラー:** 粘性（$\eta$）にゼロを入れていないか？ Phase 2のルールを確認せよ。