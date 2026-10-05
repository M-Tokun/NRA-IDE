# 操作承認の検査モジュール — E第一段階

状態: 第一段階は承認済み・実装済み。第二段階の実ホスト接続、第三段階のOS権限・sandbox設置は未実装。

操作契約はリポジトリルートのAGENTS.md。設計全体は[操作承認設計案](../agents-md-guard/OPERATION_APPROVAL_DESIGN.md)を参照する。設計案の「未承認・未実装」は提案作成時の状態であり、今回実装した範囲は同案の第一段階4ファイルである。

## 実装したこと

`manifest.py`は要求の型、絶対パス、対象の実体パス・ファイルID・内容ハッシュ、契約ハッシュ、予定操作ハッシュ、期限を検査する。承認対象と再観測した対象の正規化JSONが一致しなければ拒否する。対象の追加だけでなく削減・順序変更・影響の変更も別の要求として扱う。

`git_manifest.py`は観測済みのGit送信情報を検査する。単一の送信先URL、既存branchへの明示した単一refspec、HEADと送信元OIDの一致、fresh fetch時刻、incomingなし、outgoing全体と依頼範囲の一致、fast-forward、追加refなし、forceやhook回避なしを要求する。

`check_request()`は検査結果をCheckResult(valid, reason)として返す。真偽だけの「承認済み」フラグ、会話文字列、AGENTS.md読込マーカーから承認を発行する機能はない。外部の真正性検証と一回限りの消費を行う2つのcallbackがなければ拒否する。callbackによるエラーには固定コードを使い、入力URL・秘密値・例外本文を結果へ出さない。

## 入力とAPI

Python 3.11以降の標準ライブラリだけを使用する。モジュールのディレクトリをimportパスへ追加して読み込む。

- `snapshot_file(path)`: 存在する通常ファイルまたは存在しない作成先の観測。path、realpath、exists、sha256、identity(device/inode)を返す。ディレクトリと末端のsymlinkを拒否し、読取中のファイル差替えも検出する。
- `validate_manifest(value, now=..., max_fetch_age=300)`: 型・期限・対象・Git情報の検査。異常は固定コードのManifestError。
- `observe_files(approved, now=...)`: 対象ファイルとAGENTS.mdを実際に再読取する。Git用には使えない。
- `manifest_hash(value)`: キーをソートしたASCII JSONのSHA-256。オブジェクトのキー順序は結果に影響しない。配列順序は保持する。
- `validate_git_snapshot(value, now=..., max_fetch_age=300)`: 取得済みのGit情報の検査。ネットワークやGitコマンドは実行しない。
- `check_request(approved, current, receipt, now=..., verify_receipt=..., consume_once=...)`: 対象一致と外部承認の検査。チェック通過時だけ一回限りの消費を要求する。

要求の厳密なキーはschema_version(1)、request_id、session_id、repo_realpath、agents_sha256、operation、impact、plan_sha256、created_at、expires_at、targets、git。識別子は英数字・underscore・hyphenの1〜200文字。時刻はUTC Unix秒の有限非負数。期限は現在時刻を含まない上限であり、now == expires_atでは拒否する。boolを整数・時刻として扱わない。

パスは実行OSでnormcase(abspath(path))と同一の絶対パスを使用する。repo_realpathは収集側でrealpathまで解決する。file_changeではtargetsを最低1件、gitをnullとする。git_pushではtargetsを空配列、gitを送信情報とする。インストール・認証・一般MCP操作など未知のoperationは拒否する。

予定操作の具体的な動詞、書込予定内容、移動先、復元の影響などを収集側が構造化し、その正規化JSONのハッシュをplan_sha256へ結合する。UIにはその同じ予定操作を表示する。このモジュールが説明文やハッシュから実際の操作内容を推測することはない。移動・上書きは元と先の両方をtargetsへ入れる責任が収集側にある。

Git情報のキーはremote、push_urls、local_ref、remote_ref、refspec、head_oid、source_oid、remote_oid、fetched_at、incoming、outgoing、scope_commits、fast_forward、flags、extra_ref_updates。outgoingは古い順でHEADを最後に置く。scope_commitsは今回の依頼対象全体で、outgoingと集合が同一であることを要求する。SHA-1またはSHA-256の完全OIDを使用する。flagsはforce、delete、no_verify、hook_bypass、follow_tags、mirror、all、tagsをすべてbool falseにする。

初期対応は既存branchだけで、新規branchにはdefault-branchの基点証拠を集めるadapterが必要なため拒否する。branch名はGitの完全な文法より狭いASCII部分集合。URLはHTTPS、SSH、file URL、scp形式SSHの限定した表記に対応する。HTTPS userinfo、password、query、fragment、空白、非対応schemeを拒否する。生のローカルパスはfile URLに置き換える。ただしURLのpath等に任意の秘密値が含まれないことまで推測できないため、収集側も秘密値を含む宛先を避け、manifest全体を無加工でログへ出さない。

検証器はreceiptの署名・発行者・保存元を真正性検証した後だけ、approval_id、request_id、session_id、manifest_sha256、issued_at、expires_atを持つclaimsを返す。未検証ならNone。consume_once(approval_id, manifest_sha256)は保護された保存領域で原子的に一度だけ消費し、成功時だけ厳密なbool trueを返す。

## 信頼境界と未実装部分

任意のPython callbackを渡せることは強制的な保護ではない。AIと同じ実行主体が常に成功するcallbackやGit snapshotを偽造すれば、局所チェックを通すことはできる。このAPIは将来の保護されたbroker内部で使う部品であり、AIプロセスへ承認発行権を与えない。

Gitのfetch成功、完全なcommit集合、祖先関係、実際のURL展開、実行引数をこのモジュール自身が取得・実証するわけではない。信頼できる収集器がGitから観測する必要がある。既存のfresh fetch観測と同じfetched_atを承認前後で保持して比較するため、再fetchした場合は新しい承認対象になる。300秒の既定値と承認期限はbrokerの方針として決め、AI側から緩和できないようにする。

ファイル再観測から実行までの競合、署名鍵、OSの別実行主体、監査ログ、atomicな消費と実行の結合、失敗後の結果確認、shell/MCP/ネットワーク経由の迂回防止は未実装。将来brokerが対象を再観測し、競合を排除し、承認消費と固定した操作を仲介する必要がある。チェックのvalid=trueを、現在のhookやpre-pushで実行許可として使用してはならない。

## 検証と二つの視点

```powershell
python -B -m unittest discover -s tests -p test_operation_approval.py -v
```

27件のテストで、正常な対象照合、一回限りの消費、期限の境界、未検証承認、backend障害、型不正、対象・予定操作・契約変更、実ファイルの変更・消失・新規出現、ファイルID・実体パスの変化、読取中の差替え、HEAD・送信先・ref・commit集合、複数送信先、追加ref、incoming、依頼外commit、force/hook回避、古いfetch、秘密を含むURLのエラー出力を確認した。

真正性検証・消費はテスト用mockであり、署名検証・保護された保存先・実クライアントの承認UIは検証していない。実体パス差替えと読取中の競合はmockによる再現。ファイルの内容変更・契約変更・消失・新規出現は隔離した一時領域で実際に行って検証した。Windowsのlstat/fstatではctimeの値が異なるため、ctimeは同じ取得API内の前後で比較し、device/inode/size/mtimeは取得方法をまたいで比較する。

第一視点（意味）: 読込記録と人間の承認を分離し、操作対象を正確に結合する部品を追加した。検査成功を実行権限と同一視しない。

第二視点（実装）: 異常入力や状態の変化は拒否する。実際のファイル再観測を含むテストを行い、backend未接続で通過しないことを確認した。

俯瞰視点: AGENTS.md、RULES_DETAIL.md §9、承認済み設計案と照合した。今回の変更は新規4ファイルだけで、既存hookやAI設定へは接続していない。Codex/OpenAI固有機能の変更ではないためOpenAI Docs Skillは未適用。固定した実装・再現テストのため探索ループ用Skillも未適用。公開の依頼はないため公開Skillも未適用。

全体判定: 第一段階の実装・精査・局所再検証は完了。操作承認の強制は第二・第三段階が未実装で未完了。解消済みは要求照合部品の追加とテスト。残る対象は保護されたbroker/ホスト接続・OS境界で、導入先と権限を確定した具体案について別途承認が必要である。

## 新規発見: Git追跡の例外

既存.gitignoreの82行目 `/skills/*` により、新規operation-approval配下3ファイルは保存されていてもGitの追跡候補に現れない。`git check-ignore -v`で確認した。テストファイルは追跡候補に現れる。元の許可対象は新規4ファイルなので、.gitignoreは変更していない。

修正案: 既存の共有Skill例外（85行目 `!/skills/agents-md-guard/`）の直後に `!/skills/operation-approval/` を1行追加する。影響: このディレクトリを共有用の追跡候補へ加える。stage/commitや公開を行う変更ではない。他のローカルSkillや*.pycの除外は維持する。承認: AGENTS.md §4の既存記述保護により別途必要。第一段階の保存・局所検証は完了、共有のための追跡調整は未解消として区別する。

解消記録（2026-10-05）: 利用者の承認後、.gitignoreへ上記1行を追加した。3ファイルが除外されず未追跡の共有候補として表示されること、*.pycは引き続き除外されることを再検証した。共有のための追跡調整は解消完了。
