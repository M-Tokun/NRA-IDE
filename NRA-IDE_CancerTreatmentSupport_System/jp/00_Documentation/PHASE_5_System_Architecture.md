# ═══════════════════════════════════════════════════════════════════════
# Project: NRA-IDE Cancer Treatment Support System
# Phase:   05
# File:    PHASE_5_System_Architecture.md
# ═══════════════════════════════════════════════════════════════════════

# Phase 5: System Architecture

## 1. Data Flow Pipeline
1.  **Input:** 医師が測定値をPythonホストに入力
2.  **Validate:** Python側で範囲チェック（Phase 4準拠）
3.  **Transport:** USB-UART経由でバイナリ送信（Big Endian）
4.  **Compute:** FPGAがQ8.8固定小数点演算（5段パイプライン）
5.  **Output:** 判定フラグとエラーコードを返信
6.  **Report:** Pythonが臨床レポートと安全マップを生成

## 2. Hardware Selection
* **Target A:** Intel Cyclone V (DE0-CV) - コストパフォーマンス重視
* **Target B:** Xilinx Artix-7 (Basys 3) - 教育・入手性重視
* **Why FPGA?** 決定論的動作とパイプライン処理による高スループット（総当たり探索の高速化）のため。

## 3. Communication Protocol (Binary)
* **Host -> FPGA:** 14 Bytes
    * Header (1B): `0xA5`
    * Payload (12B): 6 Parameters x 2 Bytes (Q8.8)
    * Checksum (1B): XOR Sum
* **FPGA -> Host:** 3 Bytes
    * Status (1B): `0x01`(SAFE) / `0x00`(DANGER)
    * Error (1B): Error Code
    * Checksum (1B): XOR Sum