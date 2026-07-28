# Phase 10: Communication & Calculation Infrastructure

**Project:** NRA-IDE Cancer Treatment Support System

**Rev:** 2.0 (2026-07-28) — PHASE_2 Rev 2.0 / PHASE_6 Rev 2.0 に同期

**Author:** M-Tokuni, AI (Architect)

---

## 1. 概要 (Overview)

本フォルダは、律環公理（NRA）に基づくがん治療支援システムの基盤となる第10フェーズの成果物である。

主要な目的は、ホストPCとのバイナリ通信（UART）の確立と、物理演算パイプライン（BioCalibrator）の同期実装である。

## 2. ファイル構成 (File Structure)

| 分類 | ファイル名 | 役割 | 状態 |
| :--- | :--- | :--- | :--- |
| **Top** | `10_Top_Module.v` | システム統合、通信/演算シーケンス制御 | **断片。module/endmodule を欠く** |
| **I/O** | `10_UART_Interface.v` | 115200bps 8N1 全二重シリアル通信 | 実装済 |
| **Core** | `10_Cancer_Treatment_Selector.v` | 癌腫別（Type A/B）演算器の選択と統合 | `[cite:]` マーカーが残存 |
| **Logic** | `10_BioCalibrator_TypeA.v` | 単一細胞ジャミング判定（5段パイプライン） | 実装済（Rev 2.0） |
| **Logic** | `10_BioCalibrator_TypeB.v` | 集団力学封鎖判定（40bit演算） | **断片。ポート定義・比較ロジックを欠く** |
| **Sim** | `10_Testbench_Integration.v` | 全系統合検証用テストベンチ | チェックサム値が誤り（下記 §5） |

`../simulation/` には `10_Testbench_BruteForce.v`、`10_wave_config.do`、`10_Testbench_TypeA.v` がある。
このうち `10_Testbench_TypeA.v` は**テストベンチではなく TypeA モジュールの複製**であり、
本フォルダの `10_BioCalibrator_TypeA.v` と同名モジュールの二重定義になる。整理を要する。

制約ファイルは `../constraints/` にある（`10_timing.sdc`、`10_pinout_cyclone_v.qsf`、`10_pinout_artix_7.xdc`）。

## 3. 演算コア (BioCalibrator TypeA)

判定式は PHASE_2 Rev 2.0 の応力比較形である。全項 kPa で、両辺は同次元。

```
sigma_el = (E + B) * (D - d)/D
sigma_v  = 12 * eta * v * D / (1000 * d^2)
sigma_el + sigma_v > dP   =>   BLOCKED
```

* 5段パイプライン。`i_in_valid` から5クロック後に `o_out_valid` が立つ。
* 除算器を持たず、定数ROM（`1/D` を Q0.16、`0.012/d^2` を Q0.24）で逆数を与える。
* 全段リセット同期。Stage 1 で全入力を同時にラッチする。
* エラーは `0x03`（粘性ゼロ）→ `0x02`（範囲外）→ `0x01`（幾何）の順に評価する。
* 異常時は `o_is_jammed = 0`（PASSABLE）へ倒す。転移リスクが有る側が安全側である。

詳細は `00_Documentation/PHASE_6_FPGA_Spec.md` を参照。

## 4. 通信プロトコル (Communication Protocol)

ホストPC → FPGA は 14バイトのバイナリパケットである。

| Offset | 内容 | 形式 |
| :--- | :--- | :--- |
| `[00]` | Header | `0xA5`（Type A） / `0xA6`（Type B） |
| `[01-02]` | Stiffness $E$ | Q8.8 Big Endian |
| `[03-04]` | Viscosity $\eta$ | Q8.8 |
| `[05-06]` | Diameter $D$ | Q8.8 |
| `[07-08]` | Pore Size $d$ | Q8.8 |
| `[09-10]` | Flow $\Delta P$ | Q8.8 |
| `[11-12]` | Drug Boost $B$ | Q8.8 |
| `[13]` | Checksum | ペイロード12バイトの XOR |

FPGA → ホストは 3バイト（Header / `(Error << 1) | Jammed` / `Header ^ Data`）。

### ⚠ 既知のプロトコル欠落

現行の14バイトには **`deform_velocity` ($v$) と `cell_count` ($N$) が含まれていない。**

* $v$ は TypeA の粘性項に必要。ホストは標準値 200 μm/s を仮定している。
* $N$ は TypeB の必須入力。**このため TypeB は原理的に動作しない。**

チェックサムは「実機実装推奨」ではなく**必須**である。Fail-Closed の一部を成す。

## 5. 既知の不具合 (Known Issues)

1. **`10_Top_Module.v` が断片。** 合成もシミュレーションもできない。トップが無いため `10_Testbench_Integration.v` も動作しない。
2. **`10_Testbench_Integration.v` のチェックサムが誤り。** `0x00` を送出しているが、当該ペイロードの XOR は `0x11` である。Fail-Closed が正しく動作すれば必ず弾かれる。
3. **`[cite:]` マーカーの残存。** `10_Cancer_Treatment_Selector.v` に4箇所、`../simulation/10_Testbench_TypeA.v` に6箇所。Verilog の構文エラーとなる。
4. **`10_BioCalibrator_TypeB.v` が断片。** ポート定義と比較ロジックを欠く。
5. **UART にフレーミング検証が無い。** ストップビットを確認せずに `rx_valid` を立てている。

## 6. 修正履歴 (Major Fixes)

### Rev 2.0 (2026-07-28)

* **判定式の次元不整合を是正。** 旧版は `(E+B)*(D-d)` を `dP` と直接比較しており、次元が閉じていなかった。応力に乗じるべきは変位ではなく歪み `(D-d)/D`（無次元）である。この誤りにより、幾何エラー以外は常に BLOCKED へ張り付いていた。
* **パイプラインのラッチ漏れを是正。** 旧版は Stage 2 で `i_cell_stiffness` 等を入力ポートから直接読んでおり、1クロック遅延した `r_delta_x` と食い違っていた。
* パイプラインを3段から5段へ。全段をリセット同期に変更。
* エラーコード `0x02`（範囲外）、`0x03`（粘性ゼロ）、`0x04`（オーバーフロー）を実装。

### Rev 1.0 まで

1. **パイプライン同期エラー**: 計算完了フラグ `o_out_valid` を追加。
2. **Type B 演算精度**: 内部レジスタを 32bit から 40bit へ拡張。
3. **UARTサンプリング不備**: 受信バッファの1クロック遅延を考慮し計算開始タイミングを調整。
4. **送信ロジック欠落**: `UART_Interface` に送信（TX）ステートマシンを実装。

## 7. 実行方法 (How to Run)

> **注意: 現状ではシミュレーションを実行できない。** §5-1 の通りトップモジュールが断片であり、§5-3 の構文エラーも残っている。以下は修正完了後の手順である。

1. `10_Testbench_Integration.v` を読み込み、`../simulation/10_wave_config.do` を適用する。
2. 14バイトパケットを供給し、`uart_tx` から3バイトの応答が返ることを確認する。
3. 応答2バイト目が `(Error << 1) | Jammed` である。`0x01` なら BLOCKED、`0x00` なら PASSABLE、`0x06` なら粘性ゼロエラー。

期待値は `30_Test_Data/expected_results.json` の7ケースと一致しなければならない。
参照実装 `20_Software_Host/nra_core_model.py` が同じ演算をビット単位で再現しているため、
段ごとの中間値の突き合わせにも使える。
