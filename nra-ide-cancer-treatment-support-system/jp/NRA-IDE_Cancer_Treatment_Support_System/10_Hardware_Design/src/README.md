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
| **Top** | `10_Top_Module.v` | システム統合、通信/演算シーケンス制御 | 実装済（Rev 2.0） |
| **I/O** | `10_UART_Interface.v` | 115200bps 8N1 全二重シリアル通信 | 実装済（Rev 2.0 でビット周期を修正） |
| **Core** | `10_Cancer_Treatment_Selector.v` | 癌腫別（Type A/B）演算器の選択と統合 | 実装済 |
| **Logic** | `10_BioCalibrator_TypeA.v` | 単一細胞ジャミング判定（5段パイプライン） | 実装済（Rev 2.0） |
| **Logic** | `10_BioCalibrator_TypeB.v` | 集団力学封鎖判定 | **未実装スタブ。`0x06` を返す** |
| **Sim** | `10_Testbench_Integration.v` | 全系統合検証（7ケース＋チェックサム異常） | 実装済（Rev 2.0） |

`../simulation/` には `10_Testbench_TypeA_Cases.v`（演算コア単体、7ケース）、`10_Testbench_BruteForce.v`、`10_wave_config.do` がある。

> **削除記録（2026-07-29）:** `../simulation/10_Testbench_TypeA.v` を削除した。
> 名前に反してテストベンチではなく `10_BioCalibrator_TypeA.v` の複製であり、
> 同名モジュール `BioCalibrator_TypeA_Jamming` の二重定義になっていた。
> さらに複製元が Rev 1.0（次元不整合のあった旧式）のままだったため、
> コンパイル順序によっては旧式が採用され、警告もなく誤判定に戻る危険があった。
> 削除と同時に `10_Testbench_TypeA_Cases.v` を新設し、演算コア単体で
> 7ケースを検証できるようにした（§7 参照。7/7 PASS）。

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

### 解消済（2026-07-29）

1. ~~**`10_Top_Module.v` が断片。**~~ Rev 2.0 で実装した。
2. ~~**統合テストベンチのチェックサムが誤り。**~~ Rev 2.0 でタスク内計算に変更。旧版は `0x00` を直書きしており、正しくは `0x10` であった（Fail-Closed が働けば必ず破棄される値）。
3. ~~**`[cite:]` マーカーの残存。**~~ `10_Cancer_Treatment_Selector.v` の4箇所を除去した。なお当該4箇所はいずれも `//` コメント内にあり、**構文エラーではなかった**（旧記載を訂正）。コード行に混入して実害があったのは削除済の `10_Testbench_TypeA.v` の方である。
4. ~~**`10_BioCalibrator_TypeB.v` が断片。**~~ 未実装を明示するスタブに置き換えた（`0x06 ERR_UNSUPPORTED` を返す）。§6 参照。
5. **UART のビット周期に off-by-one があった。** `rx_cnt == BIT_PERIOD` は0から数えて `BIT_PERIOD+1` クロック待つため、実効ボーレートが `CLK_FREQ/(BIT_PERIOD+1)` になっていた。115200 では誤差 0.115% で顕在化しないが、シミュレーションでボーレートを上げると8ビット目で隣のビットを読む。`BIT_PERIOD - 1` に修正済。

### 未解消

6. **UART にフレーミング検証が無い。** ストップビットを確認せずに `rx_valid` を立てている。Fail-Closed の観点では、フレーミングエラーを検出してパケットを破棄すべきである。
7. **`deform_velocity` と `cell_count` がプロトコルに無い。** §4 参照。
8. **合成は未実施。** シミュレーションは通るが、Vivado / Quartus での合成・タイミング解析は行っていない。

## 6. 修正履歴 (Major Fixes)

### Rev 2.0 (2026-07-28 〜 07-29)

**演算コア**

* **判定式の次元不整合を是正。** 旧版は `(E+B)*(D-d)` を `dP` と直接比較しており、次元が閉じていなかった。応力に乗じるべきは変位ではなく歪み `(D-d)/D`（無次元）である。この誤りにより、幾何エラー以外は常に BLOCKED へ張り付いていた。
* **パイプラインのラッチ漏れを是正。** 旧版は Stage 2 で `i_cell_stiffness` 等を入力ポートから直接読んでおり、1クロック遅延した `r_delta_x` と食い違っていた。
* パイプラインを3段から5段へ。全段をリセット同期に変更。
* エラーコード `0x02`（範囲外）、`0x03`（粘性ゼロ）、`0x04`（オーバーフロー）を実装。

**統合（2026-07-29）**

* `10_Top_Module.v` を新規実装。UART 受信 → チェックサム検証 → 演算 → 3バイト応答のシーケンス制御。チェックサム不一致時は破棄し応答しない（ホストが再送し、3回失敗で `0x05 ERR_COMM`）。
* `10_BioCalibrator_TypeB.v` を未実装スタブに置換。未検証の現象論モデルを回路にすると判定が出てしまい、出た判定は読まれる。根拠のない数値を出すより出さない方が安全側であるという判断による。ホスト側 `nra_core_model.evaluate()` も Type B に `0x06` を返しており、挙動を一致させてある。
* `10_UART_Interface.v` のビット周期 off-by-one を修正（§5-5）。
* `10_Testbench_Integration.v` を書き直し。チェックサム自動計算、3バイト応答の照合、チェックサム異常時の無応答確認を追加。
* `../simulation/10_Testbench_TypeA_Cases.v` を新規作成。演算コア単体で7ケースを検証する。

### Rev 1.0 まで

1. **パイプライン同期エラー**: 計算完了フラグ `o_out_valid` を追加。
2. **Type B 演算精度**: 内部レジスタを 32bit から 40bit へ拡張。
3. **UARTサンプリング不備**: 受信バッファの1クロック遅延を考慮し計算開始タイミングを調整。
4. **送信ロジック欠落**: `UART_Interface` に送信（TX）ステートマシンを実装。

## 7. 実行方法 (How to Run)

Icarus Verilog での検証手順。両テストベンチとも Phase 30 の7ケースを検証する。

```bash
# 演算コア単体（高速。数秒で完了する）
iverilog -Wall -o tb.vvp 10_BioCalibrator_TypeA.v \
    ../simulation/10_Testbench_TypeA_Cases.v
vvp tb.vvp

# 全系統合（UART を含む）
iverilog -Wall -o itb.vvp 10_Top_Module.v 10_Cancer_Treatment_Selector.v \
    10_BioCalibrator_TypeA.v 10_BioCalibrator_TypeB.v \
    10_UART_Interface.v 10_Testbench_Integration.v
vvp itb.vvp

# 実機ボーレート(115200)で確認する場合（数分かかる）
iverilog -PTestbench_Integration.BAUD_RATE=115200 -o itb.vvp <同じソース>
vvp itb.vvp
```

統合テストベンチは既定でボーレートを 1 Mbps に上げてある。115200 では1ビットが
8681 ns となり、8ケースで約12 ms・100MHz で240万クロックエッジを要して現実的
でないためである。ビット周期は `CLK_FREQ / BAUD_RATE` で決まるので、比を保てば
論理の検証としては等価である。**115200 でも 8/8 通過することは確認済み。**

### 検証結果（2026-07-29, Icarus Verilog 11.0）

| テストベンチ | 結果 |
|:---|:---|
| `10_Testbench_TypeA_Cases.v`（演算コア単体） | **7 / 7 PASS** |
| `10_Testbench_Integration.v`（全系, 1 Mbps） | **8 / 8 PASS** |
| `10_Testbench_Integration.v`（全系, 115200 bps） | **8 / 8 PASS** |

期待値は `30_Test_Data/expected_results.json` と同一である。参照実装
`20_Software_Host/nra_core_model.py` が同じ演算をビット単位で再現しているため、
段ごとの中間値の突き合わせにも使える。

**ただし、これはモデルの妥当性を示すものではない。** RTL と参照実装が同じ式を
実装していることの確認までである。式が現実の細胞挙動を記述しているかは
`検証プロトコル_マイクロ流路試験.md` による実験で検証されるべきものであり、未実施である。
