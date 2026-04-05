# ═══════════════════════════════════════════════════════════════════════
# File: README_TestData.md
# Phase: 30
# Date: 2026-02-01
# Author: M-Tokuni & AI Architects
# ═══════════════════════════════════════════════════════════════════════

# Phase 30: Test Data Specification

## 1. Overview
本ディレクトリは、NRA-IDEシステムの物理的整合性を検証するためのテストデータセットを含む。
全てのデータは「因果ダイオード（Causal Diode）」原則に基づき、測定値から順方向に生成されている。

## 2. File List
* `sample_patient_data.json`: システム入力用の標準JSONフォーマット。
* `validation_test_cases.csv`: 25種類の網羅的テストケース（正常系、異常系、境界値）。
* `expected_results.json`: 各ケースに対する物理シミュレーションの期待値と、その物理的根拠。

## 3. Usage
ホストプログラム（Phase 20）にて以下のように使用する。

```bash
# 単体テスト実行
python main.py --input ../30_Test_Data/sample_patient_data.json

# 一括バリデーション（開発者用）
# CSVを読み込み、期待値通りか検証するスクリプト（Phase 20に追加実装した場合）
# python run_validation.py --csv ../30_Test_Data/validation_test_cases.csv

## 4. Maintenance
月次メンテナンス時に本データセットを実行し、判定結果が変わっていないことを確認すること（回帰テスト）。