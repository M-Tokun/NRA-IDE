
# ═══════════════════════════════════════════════════════════════════════

# Project: NRA-IDE Cancer Treatment Support System

# Phase:   50 (Deployment)

# File:    50_Deployment/installation_guide.md

# ═══════════════════════════════════════════════════════════════════════

## 1. システム要件 (System Requirements)

本システムは、リアルタイム物理演算を担う **FPGAハードウェア** と、制御・分析を担う **ホストPC** のハイブリッド構成です。

### ハードウェア要件

* **Target FPGA (いずれか1つ):**
* Xilinx Artix-7 (Basys 3 推奨)
* Intel Cyclone V (DE0-CV 推奨)


* **Host PC:** * OS: Ubuntu 22.04 LTS (推奨) または Windows 10/11
* Interface: USB 2.0/3.0 ポート x1 (UART通信用)



### ソフトウェア要件

* **EDA Tool:** * Xilinx Vivado (Artix-7 用)
* Intel Quartus Prime (Cyclone V 用)


* **Environment:** Python 3.8以上

---

## 2. ハードウェアのセットアップ (Hardware Provisioning)

### ステップ 1: ビットストリームの合成と書き込み

1. 開発環境（Vivado/Quartus）を起動し、プロジェクトファイルを開く。
2. `10_Hardware_Design/src/` の全 Verilog ファイルをソースとして追加する。
3. 使用するボードに合わせた制約ファイル (`.xdc` または `.qsf`) を読み込む。
4. **Synthesis** および **Implementation** を実行し、タイミング制約 (`timing.sdc`) が 100MHz で満たされていることを確認する。
5. 生成されたビットストリーム (`.bit` または `.sof`) を FPGA に書き込む。

### ステップ 2: 物理接続の確認

* FPGA ボードを USB ケーブルでホスト PC に接続する。
* ボード上の **LED 1 (Red)** が点滅していないことを確認する（点滅は内部エラーを示す）。

---

## 3. ソフトウェア環境の構築 (Software Environment)

### ステップ 1: ライブラリのインストール

ホスト PC のターミナルで `20_Software_Host` ディレクトリに移動し、依存関係を解決します。

```bash
pip install -r requirements.txt

```

> **主要依存関係:** `pyserial`, `numpy`, `matplotlib`

### ステップ 2: シリアルポートの権限設定 (Linuxのみ)

USB-UART デバイスへのアクセス権限を付与します。

```bash
sudo usermod -a -G dialout $USER
# その後、再ログインが必要

```

---

## 4. 初期疎通・自己診断テスト (Initial Self-Test)

システムが「律環公理」に従って正しく動作するか、運用開始前に必ず以下の自己診断を実行してください。

1. `20_Software_Host/main.py` を `--test` モード（※実装予定）または標準サンプルデータで実行します。
2. `30_Test_Data/sample_patient_data.json` を読み込ませ、FPGA からレスポンスが返るか確認します。
3. **LED 0 (Green)** が判定成功時に点灯することを確認します。

---

## 5. トラブルシューティング (Troubleshooting)

| 症状 | 原因 | 対策 |
| --- | --- | --- |
| 通信エラー (0x04) | ボーレート不一致 / ケーブル不良 | 115200bps 設定を確認。ケーブルを通信用に交換。 |
| 常に Error 0x03 | 粘性パラメータが 0 | 入力データを確認。 は 0 にできない。 |
| レポートが生成されない | 書き込み権限不足 | `40_Output_Reports/` のパーミッションを確認。 |

---
