# 実装計画：14-30 HTMLエラー（アクセシビリティ警告）の修正

examples フォルダ内の HTML ファイル (14_*.html から 30_*.html まで) に存在する、`<input type="range">` タグの `aria-label` もしくは `title` 属性欠落のアクセシビリティ警告（計92箇所）を修正します。

## ユーザーレビュー要求事項

> [!NOTE]
> - 本修正では、HTMLタグ自体の動作（JavaScriptやCSSのロジック）は変更せず、アクセシビリティおよび検証チェックを通過させるために `aria-label` 属性のみを追加します。
> - 英語版ファイルには英語の、日本語版ファイルには日本語の `aria-label` をそれぞれ ID に基づいて適切に割り当てます。
> - 修正は Python スクリプトを用いて自動的かつ一括で安全に行います。

## オープンクエスチョン
現時点で特にありません。

## 変更内容

各ファイルの `<input type="range" id="...">` タグに `aria-label="..."` を追加します。

### 対象ファイル一覧（32ファイル）
- `14_powergrid_transition_EN.html`, `14_powergrid_transition_JP.html`
- `15_or_icu_continuum_EN.html`, `15_or_icu_continuum_JP.html`
- `17_water_ice_phase_transition_EN.html`, `17_water_ice_phase_transition_JP.html`
- `18_chain_tension_EN1.html`, `18_chain_tension_JP.html`
- `19_air_pressure_EN.html`, `19_air_pressure_JP.html`
- `20_water_pressure_EN.html`, `20_water_pressure_JP.html`
- `21_cabg_monitor_EN.html`, `21_cabg_monitor_JP.html`
- `22_vascular_monitor_EN.html`, `22_vascular_monitor_JP.html`
- `23_sample_demo_EN.html`, `23_sample_demo_JP.html`
- `24_vehicle_mandatory_boundary_EN.html`, `24_vehicle_mandatory_boundary_JP.html`
- `25_dam_degradation_EN.html`, `25_dam_degradation_JP.html`
- `26_escapement_contactpoint_EN.html`, `26_escapement_contactpoint_JP.html`
- `27_belt_tension_EN.html`, `27_belt_tension_JP.html`
- `28_water_temp_EN.html`, `28_water_temp_JP.html`
- `29_light_lux_EN.html`, `29_light_lux_JP.html`
- `30_power_EN.html`, `30_power_JP.html`
※ `16_passive_safety_EN.html` および `16_passive_safety_JP.html` にはスライダー等が存在しないため、今回の対象外となります。

---

### [NEW] [fix_html_accessibility.py](file:///g:/git-M-Tokun/AI-IDE-NRA/NRA-IDE/local_reports/fix_html_accessibility.py)

警告を自動修復する以下の Python スクリプトを作成・実行します。

```python
import os
import glob
import re

# (マッピング定義の詳細は実装時に記述します)
# IDごとに適切な英語・日本語のラベルをマッピングし、
# <input type="range" id="..."> タグに `aria-label="..."` を挿入します。
```

## 検証計画

### 自動テスト / スクリプト検証
1. `python local_reports/fix_html_accessibility.py` を実行して一括置換。
2. 既に作成済みの詳細監査スクリプト `python local_reports/check_html_details.py` を実行し、問題が完全に「0件」になったことを確認。
3. `git diff` を確認し、意図しないタグ変更や破壊的変更が発生していないか検証。

### 手動検証
- ブラウザでの表示および、開発者ツールのアクセシビリティインスペクターで `aria-label` が正しく認識されているかを確認。
