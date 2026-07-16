# 第2次CLI精査 継続報告 54 — `08_discard_logs_EN.md` 限定再検証（承認待ち）

## 対象

- `docs/en-US/ai/08_discard_logs_EN.md`
- 既存継続報告: `local_reportsDirectory/33_cli_second_pass_discard_logs_en.md`

## 現在位置の確認

- 対象ファイルを分割して全文確認した。
- 現在の SHA-256 は `EA10CD3A7F1C9327DEE104355E4E022BED86E83CF16031DCC234A8E77C8D28C9` であり、報告33の完了時ハッシュと一致する。
- `git diff --check -- docs/en-US/ai/08_discard_logs_EN.md` は問題なし。
- 報告33で確定した、Discard Logを終端済みEffect-Side記録として扱う境界、外部人間監査を旧経路外に置く境界、旧ログを将来規則やCause-Sideへ戻さない境界、履歴内計算と履歴間因果ダイオードの区別は保存されている。

## 新たに検出した問題

### 1. Handoff後の出力形式と外部人間監査の境界が不十分

問題箇所:

- `HANDOFF_REQUIRED` の説明に `fixed-schema human handoff` が残る。
- 記録項目 `ACTION` に `human handoff` が残る。
- 例示の `ACTION` に `human review required` が残る。
- 自由記述を禁止する記述は `R >= 1` の最終証言だけに限定され、固定Handoff証言へ明示的に適用されていない。

正典境界との衝突:

- Handoffは旧因果経路内から人間へ処理権限を渡して更新を続ける経路ではない。
- Fail-Closed後に残せるのは固定されたEffect-Side証言であり、人間が行うのは旧経路外の外部監査である。

影響:

- 旧Effect-Sideから人間委譲を経て次の判断・更新へ進めるように読める。
- 固定形式ではない説明生成をHandoff後に許す余地が残る。

推奨修正案:

- `fixed-schema human handoff` を、外部人間監査へ提示する `fixed Handoff testimony` として明記する。
- `ACTION` の選択肢と例示を、固定Effect-Side証言および外部人間監査の表現へ統一する。
- 固定Handoff証言と最終固定証言の双方について、自由記述の説明生成を禁止する。

### 2. 旧Effect-Sideから戻してはならない要素の列挙が不完全

問題箇所:

- 現在の非変換・非再利用一覧には値、閾値、状態、規則、変換入力、更新根拠、出所が含まれるが、正典三閾値および不可逆ラッチが明示されていない箇所がある。

正典境界との衝突:

- 旧Effect-Sideの値、三閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所は、import、名称変更、再構成、再利用によって新旧いずれのCause-Sideにも戻せない。

影響:

- 列挙されていない閾値やラッチだけを更新経路へ再投入できるとの誤読余地が残る。

推奨修正案:

- 非変換・非再利用一覧を、値、正典三閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所まで一貫して明記する。

### 3. 通常出力を抑止する状態を三状態だけとする記述が広すぎる

問題箇所:

- `there are three canonical states in which new ordinary output is suppressed` と一般化している。

正典境界との衝突:

- 既知の数値進行では `HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY` の三状態が対応するが、入力例外である `CONFESSION` と `OUT_OF_DESCRIPTION_DOMAIN` も対象となる通常出力をFail-Closedで抑止する。
- 入力例外は数値進行状態と混同せず、`INPUT_EXCEPTION_LOG` に分離して記録する必要がある。

影響:

- Fail-Closed抑止状態が三つだけであると誤認され、入力例外時の抑止と証拠記録が脱落し得る。

推奨修正案:

- 「既知の数値進行内で、この節が扱う三状態」と範囲を限定する。
- `CONFESSION` と `OUT_OF_DESCRIPTION_DOMAIN` も対象となる通常出力を抑止するが、数値進行とは混同せず `INPUT_EXCEPTION_LOG` に記録すると追記する。

### 4. 三層構造を普遍的要件のように扱う記述

問題箇所:

- 終盤で `the omission of the three-layer structure cannot be prevented by logs alone` と記述している。

正典境界との衝突:

- Pre-NRA / LLM / Post-NRA の三層はLLMを含む構成に対する実装形態であり、NRA-IDE全体の普遍的な構造要件ではない。
- 適合性の根拠は権限分離、正典挙動、証拠、テストであり、層数そのものではない。

影響:

- LLMを含まない実装まで三層構造が必須だと誤読され、理論境界が特定実装へ縮小される。

推奨修正案:

- LLMを含むシステムに限定して必要な権限分離と構成層の欠落を述べる。
- ログだけでは適合を保証せず、正典挙動と証拠・テストが必要であることを明記する。

## 保存すべき既存内容

- Discard Logは終端済みEffect-Side証言であり、新しいCause-Side入力ではない。
- 旧因果ダイオードは終端し、後続評価は独立した新対象、新しいCause-Side観測、新しい規則、新しい因果ダイオードから始まる。
- 旧Effect-Sideログを将来規則の根拠や更新入力へ変換しない。
- 履歴内の離散化・計算と、履歴間の因果ダイオードを区別する。
- `entropy_export` を熱力学的エントロピーと同一視しない。
- ログは安全保証を与えない。
- 物理的残存物は、新対象のCause-Sideで新たに観測された場合に限って扱う。

## 判定

対象ファイルは報告33完了時の内容が保存されているが、確定済み正典境界に照らした限定再検証で上記4項目を検出した。現時点では対象ファイルを編集していない。利用者の承認後、上記範囲だけを修正し、全文構造、用語残存、因果方向、Markdown形式、リンクおよびテストを再検証する。
