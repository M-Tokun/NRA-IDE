# ═══════════════════════════════════════════════════════════════════════

# Project: NRA-IDE Cancer Treatment Support System

# Phase:   05

# File:    PHASE_5_System_Architecture.md

# Rev:     2.0 (2026-07-28) プロトコル定義を実装に一致させる

# ═══════════════════════════════════════════════════════════════════════



# Phase 5: System Architecture



## 1. Data Flow Pipeline



1.  **Input:** 医師が測定値をPythonホストに入力

2.  **Validate:** Python側で範囲チェック（Phase 4準拠）。範囲外なら送信せず却下する

3.  **Transport:** USB-UART経由でバイナリ送信（Big Endian）

4.  **Compute:** FPGAがQ8.8固定小数点演算（5段パイプライン）

5.  **Output:** 判定フラグとエラーコードを返信

6.  **Report:** Pythonが臨床レポートとジャミングマップを生成



FPGA が接続されていない場合、手順3〜5は参照実装 `20_Software_Host/nra_core_model.py` が代行する。参照実装は RTL の演算をビット単位で再現しており、判定結果は一致しなければならない。レポートには判定の出所（FPGA / 参照実装）を必ず記載する。



## 2. Hardware Selection



* **Target A:** Intel Cyclone V (DE0-CV) - コストパフォーマンス重視

* **Target B:** Xilinx Artix-7 (Basys 3) - 教育・入手性重視

* **Why FPGA?** 決定論的動作とパイプライン処理による高スループット（総当たり探索の高速化）のため。



> **注記:** 決定論の再現性そのものは、固定小数点演算であれば汎用CPUでもビット厳密に得られる。FPGA の実質的な利点は総当たり探索の速度であって、再現性ではない。判定1件の所要時間は UART 往復（約1.5 ms）が支配的であり、演算時間（50 ns）は無視できる。



## 3. Communication Protocol (Binary)



### 3.1 Host -> FPGA : 14 Bytes



| Offset | 内容 | 形式 |
|:---|:---|:---|
| `[00]` | Header | `0xA5`（Type A） / `0xA6`（Type B） |
| `[01-12]` | Payload | 6 パラメータ × 2 バイト（Q8.8, Big Endian） |
| `[13]` | Checksum | ペイロード12バイトの XOR |



パラメータ順: `stiffness`, `viscosity`, `diameter`, `pore_size`, `flow_dp`, `drug_boost`



### 3.2 FPGA -> Host : 3 Bytes



| Offset | 内容 | 形式 |
|:---|:---|:---|
| `[00]` | Header | 受信したヘッダと同一（`0xA5` / `0xA6`） |
| `[01]` | Data | `(Error << 1) \| Jammed` |
| `[02]` | Checksum | `Header ^ Data` |



`Jammed = 1` が `BLOCKED`、`0` が `PASSABLE` である。ホストは3回まで再送し、それでも応答が不正なら `0x05 ERR_COMM` として Fail-Closed する。



> **Rev 1.0 からの訂正:** 旧版は応答3バイトを「Status / Error / Checksum」と定義していたが、実装は上表のとおりヘッダ・合成データ・チェックサムである。また `0xA6`（Type B）の記載自体が無かった。



### 3.3 既知の欠落



現行プロトコルは **`deform_velocity` ($v$) と `cell_count` ($N$) を搬送しない。**



* $v$ は Type A の粘性項に必要。ホスト・FPGA とも標準値 200 μm/s (`0xC800`) を定数として用いる。

* $N$ は Type B の必須入力であり、**このため Type B は原理的に動作しない。** FPGA 側の `BioCalibrator_TypeB_Collective` は未実装スタブであり、`0x06 ERR_UNSUPPORTED` を返す。ホスト側 `nra_core_model.evaluate()` も同じ挙動である。



両者を追加する場合、パケット長は 14 → 17 バイト（ $v$ 2B + $N$ 1B）となる。ヘッダによる版の区別が必要になる。
