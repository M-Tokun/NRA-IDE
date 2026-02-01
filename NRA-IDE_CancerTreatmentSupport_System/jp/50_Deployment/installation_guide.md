# ═══════════════════════════════════════════════════════════════════════
# File: installation_guide.md
# Phase: 50
# Date: 2026-02-01
# ═══════════════════════════════════════════════════════════════════════

# NRA-IDE Installation Guide

## 1. Prerequisites
* **Host PC:** Windows 10/11 or Linux (Ubuntu 22.04+)
* **Python:** Version 3.10 or higher
* **FPGA:** Intel Cyclone V or Xilinx Artix-7 Board
* **Connection:** USB-UART Cable (FTDI recommended)

## 2. Setup Steps

### **Step 1: パッケージの配置**
配布された `NRA-IDE_CancerTreatmentSupport_System` フォルダを、任意の作業ディレクトリ（例: `C:\Projects\` や `~/projects/`）に配置します。

### **Step 2: 依存ライブラリのインストール**
コマンドライン（ターミナル）を開き、`20_Software_Host` ディレクトリへ移動して実行します。

```bash
cd 20_Software_Host
pip install -r requirements.txt
```

### **Step 3: FPGAへの書き込み**
`10_Hardware_Design` 内のソースコードを使用し、各FPGAツール（Quartus/Vivado）で合成・書き込みを行います。

※本パッケージにはバイナリファイル（.sof/.bit）は含まれていません。必ずソースから合成してください。

### **Step 4: 動作確認**
FPGAとPCをUSBケーブルで接続し、自己診断モードを実行します。

```bash
python main.py --test
```

## 3. Safety Check
運用開始前に必ず `30_Test_Data` のバリデーションを実行し、全テストがPASSすることを確認せよ。
