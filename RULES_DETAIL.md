# RULES_DETAIL.md — NRA-IDE 実行詳細規則
```text
#ROUTE RULES_DETAIL v2 ; 正本。本文と食い違えば 990。番号はこのブロック内だけ（AGENTS.md の経路番号とは別）
#RETURN 990=STOP 998=ASK 999=DONE ; 呼び出し元へは語だけを返す。番号をブロックの外へ持ち出さない
#CONST ; 全経路で常に成立。破れたら 990
C1 秘密値（password・token・秘密鍵・.envの値）を出力・ログ・commit・メッセージに含めない。値の確認だけのために開かない。認証済みCLIの内部利用とAIの値読取は分ける ; §4
C2 秘密値の入力・変更・再発行は利用者が行う。漏えい疑いは値を再掲せず、対象と対処だけ報告 ; §4
C3 force-push・--force-with-lease・先頭+refspec・non-ff・remote ref削除・hook回避をしない。履歴改変は対象OIDと影響を提示して利用者管理の手順へ返す ; §3
C4 Markdown=LF・$$数式。Program=フラグ・境界にコメント ; §8
C5 同じ目的・範囲で確認を繰り返さない ; §1
C6 未回答・曖昧・番号外の入力を承認にしない。commit前の包括的なpush依頼はpush確認ではない ; §3
C7 pushはコミット単位。ファイル数で分割しない ; §3
#END-CONST
10  入口。AGENTS.md 20 の手順：作業ルート → status・未追跡 → 対象/既存/対象外を分離 → 対象と操作を提示。同じ依頼で済んでいれば繰り返さない（C5） ; §1 GOTO 20
21  IF 対象に作業ルート外を含む: GOTO 600
22  IF 種別=依存導入: GOTO 500
23  IF 種別=精査の承認: GOTO 950
24  IF 種別=精査: GOTO 910
25  IF 種別=ファイル変更: GOTO 200
26  IF 種別=Git: GOTO 300
27  IF 種別=読取・回答: GOTO 999
28  GOTO 990
200 IF 利用者記述 AND 箇所の承認なし: 箇所・原文・問題と根拠・修正案・影響を提示 GOTO 990 ; §2
    ELSE 既存差分を保持し最小差分で編集。AGENTS.md は候補で 210 の検査を先に行い、最後に1回の編集で反映する（反映後の照合は再読み込みの後） GOTO 210
210 IF 想定外ファイル OR 既存差分喪失 OR 意図しない生成物 OR diff --check失敗 OR 関連検証失敗 OR C4違反 GOTO 700 ; §2
    ELSE GOTO 999
300 IF 選択=1: GOTO 310 ; §3
301 IF 選択=2: GOTO 320 ; §3
302 IF 選択=3: GOTO 990 ; §3 push は AGENTS.md 55〜57 で処理。ここへの到達は経路逸脱
303 GOTO 990 ; rebase・filter-repo・force・branch・restore・曖昧・無回答
310 読取のみ ; §3 GOTO 999
320 IF 関連テストを特定できない: 未検証を記録 GOTO 340 ; §3
    ELSE 予想所要時間を1回提示（A3）。IF >120秒 AND 実行方法の確認なし GOTO 990 ELSE GOTO 330
330 完走まで待つ（途中確認をしない）。終了後にログ末尾だけ見る。IF 失敗 GOTO 700 ELSE GOTO 340 ; §3
340 今回対象だけを明示パスでstage。Git管理外の一時ファイルを追加しない ; §3 GOTO 350
350 IF cached差分≠対象 GOTO 990 ELSE 内容に対応したメッセージ（削除は対象と理由を明記）でcommit。IF 失敗 GOTO 700 ELSE commit IDを報告 GOTO 999 ; §3
500 package・version・目的・書込み先・project/global・lockfile・注意点を提示 ; §5
    IF 承認なし GOTO 990 ELSE A5の一次情報で確認し、確認できない項目は未確認と記録 GOTO 999
600 "警告: {絶対パス}: {操作と影響}" を提示 ; §6 GOTO 601
601 IF 書込み AND 承認なし: GOTO 990
602 IF 削除・再帰移動 AND ディレクトリ内と未確認: GOTO 990
603 IF 広いパス OR 未解決変数 OR 曖昧glob: GOTO 990
604 GOTO 999
700 成功と報告しない。GOSUB docs/ERROR_MANUAL.md ; §7 GOTO 990
910 指摘ごとに再現（入力・操作・期待値・実測値）。数値は実行して確かめる ; §9 GOTO 920
920 格付け：維持（根本に反する・向きが逆・内部矛盾・非保守側）／格下げ（精度不足・領域差） GOTO 930
930 修正案一覧（箇所・原文・問題と根拠・修正案・影響〔日英版・README・関連文書〕・推奨） GOTO 940
940 承認を依頼 GOTO 990
950 承認済み項目だけ修正・同期 GOTO 960
960 910 と同じ手順で再検証。新規の問題は未承認として記録 GOTO 970
970 再現手順をスクリプトで local_reports/ に残す GOTO 980
980 報告：解消済み・未解消・未検証・新規発見 GOTO 999
990 STOP：不足・違反・必要な承認と影響をまとめ、呼び出し元へ STOP を返す
998 ASK：push確認を待つ。呼び出し元へ ASK を返す
999 END：呼び出し元へ DONE を返す
```

## 参照資料

規則は上のブロックが正本である。ここには文例・一覧・参照先だけを置く。

### A3 テスト時間の提示と確認の文例（320）

- 提示：「全件テストは約4分です」
- 確認：「120秒制限を超えるため、バックグラウンド実行でよいですか？」

### A5 依存関係の安全性確認に使う一次情報（500）

- 公式package registry
- 公式upstream repository
- 公式release notes
- lockfile、checksum、署名
- GitHub Advisory Database
- OSV.dev
- package manager標準のaudit機能

Qiita、Snyk、ブログ、掲示板は補助情報として扱い、問題の指摘がないことを安全性の証明にしない。npm公式はnpm系packageにだけ用いる。Python、Rust、Java等には各エコシステムの公式情報を用いる。

### A9 精査の参照先（910〜980）

Codex CLIとブラウザ版の分担、修正後の検証・報告の具体手順は`CODEX_CLI_BROWSER_WORKFLOW.md`を参照する。
