

# ═══════════════════════════════════════════════════════════════════════

# Project: NRA-IDE Cancer Treatment Support System

# Phase:   08

# File:    PHASE_8_Technical_Manual.md

# ═══════════════════════════════════════════════════════════════════════



# Phase 8: Technical Manual



## 1. Synthesis Guide

> **注意:** 本テンプレートは合成・タイミング解析を実施していない（未実施。CHANGELOG.md 参照）。`50_Deployment/bitstreams/` 以下の `.qpf`/`.xpr` は既存の成果物ではなく、利用者が自身の合成環境で新規作成するプロジェクトの想定配置場所である。

* **Intel Quartus:** `50_Deployment/bitstreams/` に新規プロジェクトを作成し、`10_Hardware_Design/src/` の全 `.v` を追加、`constraints/` のピン配置・タイミング制約を適用して "Compile Design" を実行。

* **Xilinx Vivado:** 同様に新規プロジェクトを作成し、`.xpr` に対して "Generate Bitstream" を実行。

* **Timing Constraint:** `timing.sdc` が正しく読み込まれているか確認すること（100MHz）。



## 2. Debugging

* **LED 0 (`led_status`):** BLOCKED判定時に点灯（PASSABLE時は消灯）

* **LED 1 (`led_error`):** エラーコードが非ゼロの間、点灯

* **UART Debug:** オシロスコープでTXピンを観測し、`0xA5` ヘッダが見えるか確認。



## 3. Common Issues

* **通信しない:** ボーレートが115200か？ USBケーブルは通信用か？

* **常にエラー:** 粘性（ $\eta$ ）にゼロを入れていないか？ Phase 2のルールを確認せよ。

