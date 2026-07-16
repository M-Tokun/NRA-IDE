# NRA-IDE 第2次CLI精査 継続Report — Causal Diode EN

- 実施日: 2026-07-15 JST
- 対象: `docs/en-US/ai/03_causal_diode_EN.md`
- 位置付け: `18_cli_second_pass_validation.md`完了後に確定した因果ダイオード境界を、1ファイル質疑形式で追加精査・整合した記録
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 再開時確認

- `AGENTS.md`、`RULES_DETAIL.md`、`CODEX.md`、`CODEX_CLI_BROWSER_WORKFLOW.md`を全文再読した。
- `18_cli_second_pass_validation.md`と`audit_manifest.json`を全文再読した。
- 18以降の既存継続報告は、再開時点では18のみだった。
- branchは`master`だった。
- 利用者の既存変更を保持し、追跡済み`nra-core/foundations/AXIOMS_rewritten_2026-04-24_011508.pdf`の削除状態を復元しなかった。
- RAW報告01～17はmanifest記録のSHA-256と全17件一致した。
- `audit_manifest.json`はJSONとして正常だった。
- 完了済みの`theory/AXIOMS.md`と`theory/axioms.json`の同期作業は再実施しなかった。

## 2. 検出した問題

変更前の対象は、因果ダイオードの禁止対象を主に`automatic authority backflow`へ限定し、次の経路を許容していた。

```text
Effect-Side result or incident record
→ qualified human investigation
→ independent Cause-Side observation and evidence
→ domain validation
→ versioned rule proposal
→ explicit authorization
→ future evaluation under the new rule
```

この記述は、旧Effect-Sideから人間調査と規則改訂を経て将来のCause-Sideへ接続できるように読めた。これは次の確定境界と衝突する。

- 因果ダイオードは`Cause-Side → Effect-Side`だけの完全な一方通行である。
- 逆流は自動・手動・人間介在・承認・版更新を問わず存在しない。
- 事故後分析と将来規則作成は古いダイオードの外側で行い、古い経路はEffect-Sideで終端する。
- 新しい対象履歴は、独立した新しいCause-Sideと新しいダイオードから開始する。
- 古いEffect-Sideを新旧いずれのCause-Sideにも変換しない。

判定: `HARD_CONFLICT / SEMANTIC_DRIFT`

## 3. 利用者決定

問題箇所、影響、推奨修正案を編集前に提示した。利用者は推奨案を`Y`で承認した。

変更単位は`docs/en-US/ai/03_causal_diode_EN.md`の因果ダイオード方向境界だけに限定した。

## 4. 修正内容

- 表題をCause-SideからEffect-Sideへの一方向経路を明示する形へ変更した。
- ダイオード内では、情報、推論、成果物、判断、権限のいずれもEffect-SideからCause-Sideへ戻らないと明記した。
- 禁止対象を自動更新だけに限定せず、手動、人間レビュー、承認、版更新、後続評価を介した逆接続も含めた。
- 外部の事故後調査、人間解釈、将来規則設計と、古いダイオード内の因果経路を分離した。
- 古い経路を次の形で終端した。

```text
Old Cause-Side
→ old Causal Diode
→ Old Effect-Side
→ TERMINAL
```

- 新履歴を次の独立経路として定義した。

```text
independently declared new target
→ new Cause-Side observations, history, and pre-fixed rules
→ new Causal Diode
→ New Effect-Side
```

- Old Effect-Sideから新旧いずれのCause-Sideにも矢印がないことを明記した。
- 旧Effect-Side値のimport、relabel、reconstruction、Cause-Side測定・構造変数・provenanceへの転換を禁止した。
- 破断・消滅後の新構造を、旧構造の復元、継続、書換えではなく、独自のCause-Sideとダイオードを持つ新履歴として明記した。
- 公理、基礎式、IDEエンジン、生存領域、安全応用の既存分類は変更しなかった。

## 5. 検証

修正後に対象全文を行番号付きで再読した。

```text
HEADINGS=15
FENCES=12
RESIDUAL_TERMS=0
TARGET_DIFF_CHECK=OK
```

残存検索対象:

- `automatic backflow`
- `narrower`
- `Effect-Side result or incident record`
- `new history may inform`
- `information can never be analyzed in the reverse direction`

コードフェンスは12件で偶数、対象限定`git diff --check`にエラーはなかった。

## 6. 判定

`docs/en-US/ai/03_causal_diode_EN.md`は、因果ダイオードを完全な一方通行として記述し、古いEffect-Sideの終端と、新しいCause-Side・新しいダイオードによる独立履歴開始を分離した。

この判定は当該1ファイルだけに限定する。リポジトリ全体の同種表現が整合済みであることは意味しない。
