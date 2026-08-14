# ═══════════════════════════════════════════════════════════════════════

# File: README_TestData.md

# Phase: 30

# Rev:  2.0 (2026-07-28) 実体との齟齬を是正

# Author: M-Tokuni & AI Architects

# ═══════════════════════════════════════════════════════════════════════



# Phase 30: Test Data Specification



## 1. Overview



本ディレクトリは、NRA-IDEシステムの物理的整合性を検証するためのテストデータセットを含む。

全てのデータは「因果ダイオード（Causal Diode）」原則に基づき、測定値から順方向に生成されている。



期待値は PHASE_2 Rev 2.0 の応力比較形に基づく。旧版（次元不整合のあった $k\cdot\Delta x$ 形）の期待値ではない。



## 2. File List



| ファイル | 内容 |
|:---|:---|
| `sample_patient_data.json` | システム入力用の標準JSONフォーマット（1件） |
| `validation_test_cases.csv` | **7件**のテストケース（正常系・異常系・境界値） |
| `expected_results.json` | 各ケースの期待値（`expected_binary = (error_code << 1) \| is_jammed`） |
| `run_validation.py` | CSV と期待値を突き合わせる一括検証スクリプト |



## 3. Test Cases



| ID | 内容 | 期待判定 | expected_binary |
|:---|:---|:---|:---|
| TC001 | 標準（薬なし） | PASSABLE | `0x00` |
| TC002 | 標準（薬あり B=3.0） | BLOCKED | `0x01` |
| TC003 | 硬い細胞 E=3.0 | BLOCKED | `0x01` |
| TC004 | 粘性ゼロ（禁止入力） | ERR 0x03 | `0x06` |
| TC005 | すり抜け（直径 < 隙間） | ERR 0x01 | `0x02` |
| TC006 | 高血圧・軟細胞 | PASSABLE | `0x00` |
| TC007 | 最大投与 B=10.0 | BLOCKED | `0x01` |



`validation_test_cases.csv` は **UTF-8 BOM 付き**である。読み込みには `utf-8-sig` を用いること。`utf-8` で開くと先頭列名が `\uFEFFtest_id` となり、1行目で KeyError になる。



## 4. Usage



```bash

# 一括検証（本ディレクトリで実行すること。相対パスに依存する）

cd 30_Test_Data

python run_validation.py



# 単体セッション

cd ../20_Software_Host

python main.py --data ../30_Test_Data/sample_patient_data.json --out ./output

```



FPGA が接続されていない場合、判定は参照実装 `nra_core_model.py`（RTL のビット単位再現）で行われる。したがって本検証はハードウェアなしで完走する。



**ただし、本検証が通ることは RTL が正しいことを意味しない。** 参照実装と RTL が同じ式を実装していることの確認までである。RTL 自体の検証にはシミュレータが要る。



## 5. Maintenance



月次メンテナンス時に本データセットを実行し、判定結果が変わっていないことを確認すること（回帰テスト）。



判定式・RTL・参照実装のいずれかを変更した場合は、変更前に本検証を実行して基準を確認し、変更後に再実行して差分の有無を確認する。
