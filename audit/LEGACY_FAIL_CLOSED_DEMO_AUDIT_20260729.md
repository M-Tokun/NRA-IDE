# 旧デモ `FAIL_CLOSED` 編集前監査

**作成日:** 2026-07-29 JST
**状態:** 編集前監査
**対象:** `examples/` および `nra-core/implementation/` の旧デモ・関連説明

## 1. 監査結果

`FAIL_CLOSED` または `FAIL-CLOSED` は69ファイル、319箇所に存在した。

| 種別 | ファイル数 | 主な意味 |
|---|---:|---|
| HTML | 52 | JavaScript状態値、画面ラベル、ログ、図中説明 |
| Markdown | 8 | デモ仕様、README、AUTOSAR連携、履歴 |
| Python | 9 | Enum、状態比較、閾値定数、ログ |

この319箇所は同じ意味ではない。正規状態名、運用原則、装置指令、CSS等の表示実装、履歴を区別せず一括置換すると、新しい境界不整合を作る。

## 2. 視点1 — 正典・意味分類

### A. `R >= 1.0` の状態名

`R >= 1.0` の分類名として `FAIL_CLOSED` を返すコードと表示がある。これは現行正典では `RUPTURE_BOUNDARY` へ移行する。

代表例:

- `examples/nra_ide_core_base_2026-03-21.py`
- `examples/nra_ide_demo14_powergrid_2026-03-21.py`
- `examples/nra_ide_demo15_or_icu_2026-03-21.py`
- `nra-core/implementation/belt_tension_nra_ide_2026-03-19_0059*.py`
- `nra-core/implementation/chain_tension_nra_ide_2026-03-19_0113*.py`
- `examples/14_powergrid_transition_*.html`
- 張力、圧力、温度、照度、電力、相転移、相関監視の各HTML

### B. 運用原則・抑止動作

不正入力、`CONFESSION`、装置停止、Watchdog、AUTOSAR P-Port指令などで使うFail-Closedは、正規状態名ではなく運用原則または装置動作である。この用途は `Fail-Closed suppression`、`fail_closed_suppression`、または「抑止指令」として残し、`RUPTURE_BOUNDARY`へ偽装しない。

代表例:

- `examples/47_FPGA_Demo_SPEED_*.html` の `S_CONFESS`
- `examples/NRA-IDE_AUTOSAR_Integration_2026-02-24_v2.md`
- `examples/NRA-IDE_OTA_Gate_Verification_2026-02-24_v1.md`
- `examples/NRA-IDE_Connection_vs_Mixing_*.html`

### C. 履歴

- `examples/session_handoff_2026-03-08_0237.md`

旧二値境界の履歴的引継ぎ記録であるため、現行正典として再利用しない旨を明示して変更しない。

## 3. 視点2 — 実装・運用分類

### 実行状態を持つPython 9ファイル

Enum値、状態比較、状態遷移、表示集計を一体で変更する必要がある。`TH_FAIL_CLOSED` は `TH_RUPTURE_BOUNDARY` へ変更する。後続の人間操作を「同じ破断対象の復旧」と記述せず、ドメイン固有の再検査または独立した新評価履歴の開始として扱う。

### 実行状態を持つHTML 19ファイル

JavaScriptの状態値と比較式を `RUPTURE_BOUNDARY` へ変更し、表示文字列も同期する。CSSの `fail`、`fail-hi`、`badge-fail` 等は表示クラスであり、正規状態APIではないため無理に改名しない。

### 表示・説明中心のHTML／Markdown

`R >= 1.0` のラベルは `RUPTURE_BOUNDARY` とする。停止・遮断・外部判断要求は「Fail-Closedという状態」ではなく、`RUPTURE_BOUNDARY`または別の正規分類に対する運用応答として記述する。

### 閾値記号

`R_FAIL` はデモ内部の変数名であって正規状態ではないが、正規境界との混同を減らすため、変更対象ファイルでは `R_RUPTURE` へ移行する。

## 4. 俯瞰視点 — 移行後モデル

状態分類と運用応答を次の二層に分離する。

```text
classification:
  PERMIT
  BOUNDARY_WARNING
  HANDOFF_REQUIRED
  IRREVERSIBLE_TRANSITION
  RUPTURE_BOUNDARY
  CONFESSION
  OUT_OF_DESCRIPTION_DOMAIN

operational response:
  permit
  warn
  stop affected autonomous processing
  fail-closed suppression
  fixed structural testimony
  external predefined authority
```

したがって、次のように移行する。

```text
R >= 1.0
旧: state = FAIL_CLOSED
新: state = RUPTURE_BOUNDARY
    operational_response = fail_closed_suppression
```

一方、`CONFESSION`に対する抑止は次であり、`RUPTURE_BOUNDARY`へ変更しない。

```text
classification = CONFESSION
operational_response = fail_closed_suppression
```

## 5. 変更方針

1. `FAIL_CLOSED` を状態値として使う箇所は `RUPTURE_BOUNDARY` へ変更する。
2. `TH_FAIL_CLOSED` は `TH_RUPTURE_BOUNDARY`、`R_FAIL` は対象ファイル内で `R_RUPTURE` へ変更する。
3. `R >= 1.0` の画面ラベルとログは `RUPTURE_BOUNDARY` へ変更する。
4. `CONFESSION`、Watchdog、AUTOSAR装置指令等の抑止は `Fail-Closed suppression` と明記する。
5. CSSクラス、配色キー、グラフ系列名の `fail` は表示実装として維持する。
6. 履歴文書は変更しない。
7. 変更後、Python構文、HTML内JavaScript構文、対象語grep、デモ固有テスト、リポジトリ検証を行う。
