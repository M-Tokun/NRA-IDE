# 完全破断後の観測・記録・通信経路に関する編集前監査

**作成日:** 2026-07-29 JST
**状態:** 編集前監査（正典変更前）
**対象:** NRA-IDE正典、機械可読正典、参照実装、決定論的テスト、README、関連派生文書

## 1. 監査目的

評価対象として宣言された構造の `RUPTURE_BOUNDARY` と、Cause-Sideの観測・記録・通信経路の個別状態を分離する。併せて、Handoffで移る対象を実行権限だけに限定し、破断後構造証言を一回限りの終端出力ではなく、経路が生存する間に継続する事前固定形式として正規化する。

次は変更しない。

- 唯一の律環公理「存在は生成である。」
- 基本境界式 `R = delta / tau`
- `0 <= R_warn < R_handoff < R_irrev < 1.0`
- Cause-SideからEffect-Sideへの生成経路
- Effect-SideからCause-Sideへの逆流禁止
- `R` は境界接近比であり、安全度・品質・確率・信頼度・最適化目的ではないこと

## 2. 作業前状態

- ブランチ: `master`
- リモートとの差: `origin/master` より8コミット先行
- 既存追跡差分: `AGENTS.md` に利用者の1行追加
- 既存未追跡: `ground/` と `note/` の利用者文書群
- 保護方針: 上記の既存差分を上書き、削除、巻き戻し、大量整形しない

既存の `ground/ground_Report/` は接地・運用層の報告であり、今回の破断後経路を扱う監査報告ではなかった。`examples/session_handoff_2026-03-08_0237.md` は旧状態名と旧二値境界を含む履歴的引継ぎ記録であり、現行正典としては使用しない。

## 3. 視点1 — 概念・正典境界

| ファイル:行 | 現行記述 | 問題となる境界 | 修正方針 |
|---|---|---|---|
| `theory/AXIOMS.md:581-583` | 進行中の構造証言を終了し、最終固定証言へ切替え、最終観測値等へ限定 | 対象破断と観測・記録・通信経路の生存を同じ終端へ畳み込む | `R_target >= 1.0` は対象構造だけに適用し、破断後固定形式へ切替える。生存経路の証言は継続 |
| `theory/AXIOMS.md:645-657` | `R >= 1.0` で最終固定証言へ切替え | `final` が一回限りの終端出力と読める | `predefined post-rupture structural testimony mode` として定義し、経路が物理的に失われるまで継続 |
| `theory/AXIOMS.md:760-778` | Cause-Sideからのみ変数を得る | 逆流禁止はあるが、正規Cause-Side観測の時系列更新と固定スナップショットの区別が不足 | 出所・更新権限・更新経路・評価スナップショットを固定し、新規Cause-Side観測による正規更新を許可 |
| `theory/axioms.json:266-272` | Handoff状態に包括的な `responsibility` フィールド | 実行権限移譲と責任・証言・ログ経路が混同され得る | `execution_authority`、`structural_testimony_route`、`audit_log_route`、`audit_log_custody` を分離。Handoffで変えるのは実行権限だけ |
| `theory/axioms.json:290-304` | `RUPTURE_BOUNDARY` の出力を `final Cause-Side observation` 等へ限定 | 宣言対象と各チャネルの状態を区別していない | declared targetへの限定、post-rupture mode、チャネル生存、喪失状態、最終有効観測メタデータを追加 |
| `theory/axioms.json:321-337` | `R >= 1.0` で final fixed testimony | 破断後証言の反復可能性・継続条件が機械可読でない | 固定形式へのモード遷移と、生存チャネルごとの継続条件を明示 |
| `theory/NRA-IDE_Foundational_Thesis_Bilingual.md:450,491,501,1127,1168,1178` | final fixed testimonyへ切替え | 対象破断後の観測継続が不明 | 英日双方で対象・チャネル・証言モードを分離 |
| `theory/SANDWICH_ARCH.md:493-502,559-572,1161-1169,1225-1238` | final Cause-Side observationsを含む最終固定証言 | Cause-Side監査経路が独立していても、対象破断と同時に終端化される | 独立経路ごとの生存状態とpost-rupture fixed testimonyの継続を明示 |
| `theory/THEORY.md:202-216,292-350` | 最終固定証言へ切替え | `final` が対象破断と全経路終端を同一視し得る | 正規状態表と構造証言節をpost-rupture継続形式へ同期 |
| `llms.md:382-409,497-502,1064-1088,1179-1183` | final fixed testimonyの固定フィールド | AI向け手順が一回限り出力を誘発し得る | 対象破断後も生存チャネルから固定形式を継続するアルゴリズムへ変更 |
| `README.md:170,196` | fixed Effect-Side testimony | Handoff証言をEffect-Sideと表現し、独立構造証言経路と衝突 | 実行権限のみ移譲し、Cause-Side構造証言・監査ログ経路は継続と訂正 |
| `README.md:172,198,287-290` / `README_JP.md:171,197,288-291` | final fixed testimony | 公開概要でも全経路終端と読める | post-rupture fixed testimony modeとチャネル生存分離を明記 |

## 4. 視点2 — 実装・運用境界

| ファイル:行 | 現行実装 | 問題となる境界 | 修正方針 |
|---|---|---|---|
| `nra-core/foundations/NRA-IDE_Architecture_public.py:13-37` | 単一通知schemaに対象状態・証言だけを保持 | 対象、観測、ロギング、通信、実行権限、証言モードの状態分離がない | 最小限のenum相当定数と独立フィールドを追加 |
| 同 `:78-151` | `_notice` が単一の `structural_testimony` を生成 | 個別センサー喪失、最終有効値・時刻、経路生存を表現不能 | 観測チャネル台帳を受け、チャネル単位のACTIVE/LOSTと最終有効メタデータを保持 |
| 同 `:301-311` | 破断で `FINAL_FIXED_TESTIMONY` を一回返す形 | 生存観測・ロギング・通信の継続が未実装 | `POST_RUPTURE_FIXED` へ切替え、チャネル生存中は再評価ごとに固定形式証言を生成 |
| 同 `:320-328` | Handoff通知のみ | 実行権限だけが移ることを構造化していない | `execution_authority=EXTERNAL_PREDEFINED` とし、証言・ログ経路はACTIVEのまま |
| 同 `:479-512` | 出力ゲートはHandoff以降LLM出力を抑止 | 抑止自体は正しいが、独立証言・ログ・通信経路の状態が返却契約にない | `nra_status` 内で独立経路を必ず返す |
| `tests/test_nra_ide_reference.py:86-88` | `FINAL_FIXED_TESTIMONY` への遷移だけを確認 | 破断後継続とチャネル分離を検証しない | `POST_RUPTURE_FIXED`、生存センサー継続、他センサー独立、ログ・通信独立を検証 |
| 同 `:151-152` | Effect-Side構造権限拒否 | 変数更新のみを検証し、ラッチ解除・観測値・閾値書換えを網羅しない | Effect-Sideからのラッチ解除、閾値、観測値更新拒否を追加 |

現行実装の不可逆ラッチ、`tau == 0` の `OUT_OF_DESCRIPTION_DOMAIN`、非有限値の `CONFESSION`、正規閾値順序の決定論的拒否は維持できる。

## 5. 俯瞰視点 — 文書間・状態機械全体

現行正典は、Handoff後も構造証言と監査ログを継続する点、およびFail-Closedが完全沈黙ではない点では概ね整合している。しかし `RUPTURE_BOUNDARY` だけが「final observation / final fixed testimony」という終端語に収束し、次の独立軸を失っている。

```text
declared target boundary state
observation channel state
logging channel state
communication channel state
execution authority state
structural testimony mode
```

必要な全体状態は次のような直積であり、単一状態への統合ではない。

```text
target_state = RUPTURE_BOUNDARY
observation_state = ACTIVE
logging_state = ACTIVE
communication_state = ACTIVE
execution_authority = EXTERNAL_PREDEFINED
testimony_mode = POST_RUPTURE_FIXED
```

観測不能、記録不能、通信不能はそれぞれ独立に `OBSERVATION_LOST`、`LOGGING_LOST`、`COMMUNICATION_LOST` とする。欠測値をゼロ・安定・安全・回復・完全破断へ補完しない。各観測チャネルは、センサー識別子、最終有効値、最終有効時刻、欠測開始時刻、最終健全性状態、電源状態、通信状態、不能理由、理由不明の明示、出所・監査系列を保持する。

## 6. 検索結果の分類

- Handoffによる包括的責任移譲: `theory/axioms.json:270` のフィールド名が不適合。`llms.md` の人命・最終責任節は「判断した有資格者に責任が残る」説明であり、Handoff効果としての責任移譲ではないため維持対象
- `R >= 1.0` による観測・ログ終了: 明示的停止文はないが、`final Cause-Side observation` と「進行中証言を終了」が停止解釈を生む
- `final fixed testimony` の一回限り終端解釈: 上位正典からREADMEまで横断的に存在
- 対象・センサー・ロガー・通信の統合: 独立状態が存在しないため、単一 `RUPTURE_BOUNDARY` に暗黙統合
- `tau == 0` の直接Fail-Closed分類: 現行正典・参照実装では分離済み。維持
- Fail-Closedの正規状態扱い: 現行上位正典では運用原則として分離済み。維持
- `FULL_BREAK`: 指定正典・参照実装・関連テストにはなし
- `NORMAL`: 基礎論文の一般語・比較略記に存在。正規状態列挙は正規名へ修正し、一般語としての履歴説明は状態名でないことを確認
- 不可逆ラッチ: 現行参照実装に実装済み。解除規則とEffect-Side拒否を強化
- Handoff後の構造証言停止: 現行正典では継続。実行権限との独立性を構造化
- Cause-Side全体のimmutable化: 現行はEffect-Side逆流禁止が中心。正規Cause-Side更新と評価スナップショット固定を明文化

## 7. 修正順序

`theory/AXIOMS.md` → `theory/axioms.json` → `FORMULA.md` → 基礎論文 → Sandwich仕様 → `theory/THEORY.md` → `llms.md` → 正規参照実装 → mirror → 決定論的テスト → README英日 → その他派生文書 → リポジトリ内の英語解説三部作、の順で同期する。
