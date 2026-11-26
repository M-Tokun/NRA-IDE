---
name: file-operation-report
description: 削除・移動・改名・上書き・依頼外コピー・復元の記録と、誤操作検知時の停止・報告。RULES_DETAIL.md 207（40から）と AGENTS.md 66（10から）・§8から呼ばれる。
---

# ファイル操作の報告

RULES_DETAIL.md 207（ファイル操作の直後に40から）、AGENTS.md 66（誤操作の検知時に10から）、§8「ファイル操作の報告」から入る。番号は本書内だけの経路番号。戻りは DONE / STOP。

## 操作コード

| コード | 対象 |
|---|---|
| DEL | 削除（再帰を含む） |
| MOVE | 移動・改名 |
| COPY | 上書きコピー・依頼外コピー |
| RESTORE | 復元 |

## 経路

```text
10 操作中に誤DEL・誤MOVE・意図しない上書き・依頼外COPY・一部欠落・移動先不明を検知したら、
   影響範囲への書込みを止める。GOTO 20
20 判明したパス・件数・未確認範囲を直ちに報告する。GOTO 30
30 RESTOREで既存ファイルを上書きするなら、AGENTS.md §6の確認を受ける。
   承認がなければRESTOREしない。GOTO 40
40 作業終了前に対象を確かめる。対象＝DEL・MOVE・COPY・RESTORE
   （承認済み・一部実行を含む）。対象なし: GOTO 99
50 操作時刻・承認範囲と、コードごとの結果を記録する。
   DEL     → パス・件数・フォルダ配下。該当時は AGENTS.md §7 のcommit ID
   MOVE    → 元／先のパス・件数・双方の状態・内容の一致。フォルダは配下の相対パスと件数も照合
   COPY    → 元／先のパス・件数・上書きまたは依頼外作成の結果
   RESTORE → パス・復元元・照合した版・一致の有無・未復元
60 操作直前との一致を確かめられなければ「不明」とし、確認できた範囲と不足する比較元を書く。
70 1作業につき1本を保存し、最終応答に保存先を示す。
   audit/file_operations/ファイル操作報告(YYYY_MMDD_HHMM).md
75 報告書を作業ツリーに置き、その操作を含む commit 単位の指定パスに入れる（scripts/commit.py が照合）。DELを含むなら AGENTS.md §7 のcommitと同じにする。
   commitできなければ未記録の対象と理由を報告し、STOPを返す。pushは別途確認する。
99 終了。10から入ればSTOP、40から入ればDONEを返す。
```

## 書式

- パスは`AI-IDE-NRA`配下で書く（例：`NRA-IDE/theory/AXIOMS.md`）。範囲外は、操作に関係する上位フォルダから書く。ドライブ文字と利用者名を含む区間は書かない。会話上の確認（AGENTS.md §2・§6）は絶対パスのままでよい。
- 時刻は日本時間（`TZ=Asia/Tokyo`）。
- frontmatterに id・kind・created・title を付ける。idは`REPORT-FILEOP-YYYYMMDD-HHMM`。

## 機械検査の範囲

`scripts/commit.py`はcommit時に、DEL・MOVE（改名）・RESTORE（過去に削除されたパスの再追加）・COPY（追跡済みファイルと同じ内容の追加）があれば、同じcommitに報告書があり、各パスが本文に書かれていることを照合する。`scripts/fileop_gate.py`はpush前に、DEL・MOVEについて同じ検査をする。上書きコピーは変更として現れて通常の編集と区別できず、未追跡ファイルと作業ルート外の操作はGitから見えない。この範囲は本書の自己申告に留まる。
