# AGENTS.md読込ガード

## 対象と役割

操作契約はリポジトリルートのAGENTS.mdである。Codexの動作を他AIへコピーして権威にする構成ではなく、共通の判定を各ホストのhook形式へ変換する。

Claude / Codex / GeminiはSessionStartでAGENTS.md全文を追加コンテキストへ出力し、その出力成功後にセッション別記録を作成する。記録にはツール名、セッションID、正規化した契約パス、契約全文のSHA-256を含める。契約変更、古い形式の記録、異常入力、読込失敗は有効な記録にならない。

PreToolUse / BeforeToolは全ツール名に適用する。未読時に通すのは、既知のファイル読取ツールによる現在のAGENTS.mdの単独・全文読取だけである。他ファイル、複数ファイル、検索、Web、部分読取、未知の引数は現在の契約記録を必要とする。契約欠落・読込不能時は読取も拒否する。Clineのpathsは単一パスの配列またはJSON文字列を正規化し、混在したパス指定は拒否する。通過時はホストの通常の権限確認に戻る。hookから自動承認を返さない。

旧PostToolUse / AfterTool用のmarkスクリプトは、同一パス、範囲指定なし、成功応答、全文一致のすべてを確認する。新設定では開始時読込へ切り替えた。未知の応答形式から読了を推定しない。Cline 4.1.22は専用アダプターでpreToolUse/postToolUseの入れ子形式を変換する。Windows用TaskStart.ps1 / TaskResume.ps1は全文をcontextModificationへ出力した後に記録し、PreToolUse.ps1 / PostToolUse.ps1が共通判定へ接続する。単一ファイルの成功応答かつ全文一致だけを読込記録の根拠とし、未知・部分・複数ファイルの応答から推定しない。実クライアントのTaskStartと読取用PreToolUse/PostToolUseの発火は利用者提供の画面・応答とローカル記録で確認した。未読拒否と今回の設定変更後のホスト確認画面は、入口再現と区別して検証する。

## 起動と有効化

ClaudeとGeminiの起動コマンドは、それぞれCLAUDE_PROJECT_DIR / GEMINI_PROJECT_DIRからスクリプトの絶対パスを組み立てる。Codexは既存のgitルート取得コマンドを維持する。Pythonが必要であり、CodexのWindows用コマンドではpwshも必要になる。ClineのWindows入口はPSScriptRootでhelperを解決し、UTF-8入出力でPythonを呼ぶ。Pythonの起動・結果の検証に失敗するとcancel:trueを返す。Windows PowerShellとPowerShell 7で入口を局所検証した。

設定更新後は、各クライアントで設定を再読込し、セッション開始・再開のhookを発火させる。Codexではhook定義を変更したため、/hooksで変更した定義を確認して信頼する必要がある。AIがtrusted_hashを自動更新する手順は採用しない。

古いセッション記録は無効になるため、再読込前の変異操作が拒否されることは想定された動作である。現在の契約は追加コンテキスト5593文字で、実装の上限（Codex 12000文字、Claude/Gemini 10000文字、Cline 50000 UTF-16単位）以内。上限を超えた契約を切り捨てて読了にしない。

## 検証

```powershell
python -B -m unittest discover -s tests -p 'test_agents_md_guard*.py' -v
python -B local_reports/2026-10-05_permission_route_audit.py
```

テストは不正入力、旧記録、契約変更、開始時失敗、未知ツール、読取例外、全文一致、通常権限確認への移行を確認する。Claude/Geminiの設定済みコマンドは、隔離したテスト用ルートの下位ディレクトリから子プロセスとして実行する。各AIクライアントの実セッションでのhook発火・信頼状態とは区別する。

## 保証の限界

記録はリポジトリ内の.agent_stateへ保存される。ハッシュは契約の更新を検出するが、書込権限を持つ主体による記録の偽造を防ぐ署名ではない。記録が示すのは追加コンテキストを出力した事実であり、モデルによる理解やホストの配送完了の保証ではない。

hook無効化、未信頼、非対応の実行経路、Python起動前の障害、ホストのhook異常処理には依存が残る。catch可能なガード内部の例外は拒否に変換するが、プロセスを起動できない問題まで同じ方法で保証できない。

Claudeのask/denyは直接の危険コマンドや広い古い許可を整理する追加防御である。別名、引数の別表現、任意のスクリプト、API呼出しを完全に仲介するものではない。AGENTS.md読込、操作承認、sandbox、Gitの送信検査は別々の役割を持つ。操作承認の設計は[OPERATION_APPROVAL_DESIGN.md](OPERATION_APPROVAL_DESIGN.md)を参照する。

一次資料: [Claude hooks](https://code.claude.com/docs/en/hooks)、[Claude permissions](https://code.claude.com/docs/en/permissions)、[Gemini hooks](https://geminicli.com/docs/hooks/reference/)、[Codex hooks](https://learn.chatgpt.com/docs/hooks)。

## ClineとKiloの反映確認（2026-10-05）

ClineのWindows hookを追加し、導入4.1.22と同じtaskId/preToolUse/postToolUse形式に対応した。Clineを再読込し、新規タスク・再開時にAGENTS.md loadedの全文追加contextとhook状態を確認する。ローカルのマーカーは人間による操作承認を証明しない。署名・承認brokerは未接続のまま。Unixの既存入口は維持し、Windows非対応という古いコメントを更新した。

Kiloはproject .kilo/kilo.jsoncでpermission.bash=askを明示した。globalのbash=allowは変更していない。このproject設定は読込済みのbackendにキャッシュされるため、VS Codeウィンドウの再読込後にシェル確認が出ることを確認する。Kilo用読込pluginや自動依存導入は今回実装していない。

CLIやproviderが別の実行経路を使う場合、これらのVS Code用hookだけで全経路を仲介できるとは評価しない。Clineの開始時contextが出力された後、marker書込に失敗するとPythonは非zeroで終了し、Windows helperは成功contextを破棄してcancel:trueに変換する。

## 許認可境界の修正（2026-10-05）

利用者の承認後、Cline globalStateのautoApprovalSettings.actions.executeSafeCommandsとuseMcpをfalseへ変更した。他の設定は保持した。導入4.1.22のshouldAutoApproveToolが使う純粋な判定関数で、run_commands・execute_command・MCPの自動承認がfalseになることを再検証した。設定反映にはクライアント再読込が必要であり、実UIでの再確認は別工程である。

共通ガードは未読時の読取を現在の契約だけへ制限した。この変更はClaude/Codex/Geminiにも適用される。既存の有効記録後は通常のホスト判定へ戻るため、ガード単独では個別承認を証明しない。各アダプターとCline Windows入口の回帰検証で、単独契約読取、他ファイル、複数・混在指定、検索、部分読取、欠落・更新時の拒否を確認する。ローカル記録の改変、hook無効化、ホスト側例外を防ぐ独立broker・OS境界は未実装。

## Clineの空引数シリアライズ対応（2026-10-05）

導入済みCline 4.1.22は、hook入力のprotobuf toJSONで空のparameters mapを省略する。引数なしMCPのlist_allowed_directoriesではpreToolUseにtoolNameだけが残るため、アダプターはparametersが省略された場合だけ{}へ補う。明示的なnull・配列・文字列は拒否する。引数が空でも有効な契約記録がなければMCPは拒否し、読取ツールも契約対象パスが不明なら拒否する。有効記録後はcancel=falseでホスト確認へ戻す。MCP自動承認は変更しない。
