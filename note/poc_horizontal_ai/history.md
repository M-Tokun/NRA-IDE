# NRA-IDE AI横軸機能 探索履歴

この文書は、「現況でAI横軸機能を実装する場合の最適解は何か」という問いに対し、区切り探索で得た仮説、実装候補、判明事項、次段階への接続を残すための履歴である。

ここに記録する候補は、記録時点の探索結果であり、完成仕様、安全性の証明、または正典への昇格を意味しない。

---

## 2026-08-12：現実実装最適解候補と初期PoC

### 探索目的

現行のLLM・AIエージェントへ、推論性能とは独立した横軸機能を導入するため、現実に実装可能な構造と導入順序を具体化する。

### 作成物

- `NRA-IDE_AI横軸機能_現実実装最適解_20260812-1934.md`
  - AIを未検証の提案器として扱う。
  - AIの外側へ決定論的な安全判定層を置く。
  - 型付き提案、完全仲介、限定Capability、Runtime Assurance、証拠・復旧経路を分離する。
- `config.py`
- `horizontal_state.py`
- `memory_store.py`
- `poc_runner.py`
- `requirements.txt`
  - 前時刻の状態と現在の推論出力を学習型ゲートで接続し、SQLiteへ時系列状態を保存する初期PoC。

### この段階で判明したこと

設計文書とPython群は、同じ「横軸」という名称で異なる機能を表していた。

1. 設計文書の横軸
   - AIの外部に置く安全・権限・境界評価基盤。
   - 不変条件、Cause-Side証拠、`delta/tau/R`、実行権限、完全仲介、監査、縮退、復旧を扱う。
2. Python群の横軸
   - AI内部または処理内部で、前時刻から状態を保持する時間状態機構。
   - 学習型ゲートと状態ベクトルの永続化を扱う。

両者は排他的とは限らないが、時間状態機構を外部安全カーネルの代替として扱うことはできない。今後は名称、責務、信頼境界を分離する。

### 正典整合上の修正課題

- 正規境界状態とFail-Closed運用応答を分離する。
- `PERMIT`、`BOUNDARY_WARNING`、`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`を保持する。
- `CONFESSION`と`OUT_OF_DESCRIPTION_DOMAIN`を既知の境界進行から分離する。
- `R_warn`、`R_handoff`、`R_irrev`、`R = 1.0`を一つの停止閾値へ畳み込まない。
- `tau = 0`を`OUT_OF_DESCRIPTION_DOMAIN`とし、負値、非有限値、不明値などの不正入力と分離する。
- 対象境界状態、実行権限、観測、記録、通信、構造証言を独立した状態として扱う。
- `delta`と`tau`の算定・蓄積・消耗・補充・復元規則を、対象ドメインのCause-Sideモデルごとに定義する。
- 学習型状態、AIの自己評価、意味上の信頼度を物理的許可根拠にしない。

### 初期PoCで確認された実装課題

- `sequence_start`の負値が設定検証を通過する一方、保存層では拒否される。
- 状態保存はstepごとにcommitされるため、run全体を一つの取引として扱っていない。
- 永続化検証に`assert`を使用しており、最適化実行時に検証が無効化され得る。
- SQLite内の状態ハッシュは事故的破損の検出には使えるが、署名または外部保全のない改ざん耐性証拠ではない。
- 学習器の重み、実行環境、依存関係、入力由来、ポリシー版が状態記録へ固定されていない。
- 既定DBパスが探索ソースと同じディレクトリにあり、実行生成物と探索資料が混在する。

### 次段階への接続

次段階では、既存Python群を時間状態候補として識別可能に分離したうえで、外部作用をまだ実行しないシャドー判定型の安全カーネルを作る。

最初の評価対象は限定ファイル変更AIとし、次を優先する。

1. 閉じた型付きAction Proposal
2. 対象範囲、削除、秘密情報、外部送信に対する硬い不変条件
3. 正規状態分類と運用応答の分離
4. 実行権限、観測、記録、通信の独立状態
5. 理由コードと判定証拠の保存
6. 実作用を伴わないシャドー試験

この段階では、測定契約を確立できていない危険軸を無理に`delta/tau/R`へ変換しない。先にBoolean不変条件で作用境界を閉じ、Cause-Sideの対象、単位、観測規則、限界、回復条件を定義できた軸だけを後続段階で境界評価へ接続する。

---

## 2026-08-13：正典整合修正とシャドー安全カーネル

### 実施した修正

- 設計文書を区切り探索上の技術設計候補として明示した。
- 正規境界状態、入力例外状態、運用応答を分離した。
- `R_warn`、`R_handoff`、`R_irrev`、`R = 1.0`の状態範囲を復元した。
- `tau = 0`を`OUT_OF_DESCRIPTION_DOMAIN`とし、負値、非有限値、不明値を`CONFESSION`へ分離した。
- 対象境界、実行権限、観測、記録、通信、証言モードを独立フィールドとして扱った。
- `delta`の普遍的な単調増加を仮定せず、ドメイン固有のCause-Side更新規則へ戻した。
- Effect-Sideの異常検知出力による`delta`、`tau`、R、閾値の書換えを禁止した。
- 可逆性等級を`R0`から`R4`ではなく`E0`から`E4`とし、境界接近比Rとの記号衝突を解消した。

### 時間状態候補の分離

初期Python群は、内容を保持したまま次へ移した。

```text
experiments/temporal_state_candidate/
```

同候補は、学習型ゲートによる時間状態保持の探索履歴であり、外部安全カーネルの現行実装としては扱わない。

### 次段階として追加した実装

```text
safety_kernel/
```

限定ファイル変更AIを対象とし、実作用を行わないシャドー判定だけを実装した。

- 閉じたAction Proposal
- 対象範囲、秘密・制御パス、依存更新、symlink、状態版、base hashの硬い不変条件
- 単一ファイルのunified diff契約
- 削除・renameパッチの拒否
- 軸別正規境界分類と不可逆ラッチ
- Boolean不変条件だけで開始し、未定義の`delta/tau/R`を捏造しない経路
- 対象破断後も、生存している観測、記録、通信経路を独立して保持する判定結果

### この段階の境界

- 実ファイル変更は行わない。
- Capabilityは発行しない。
- Git、ネットワーク、依存更新、削除を実行しない。
- 監査ログの外部保全と実行プロキシは次段階以降とする。
- 安全性の完成証明または汎用AIへの一般解とは扱わない。

### 検証結果

- シャドー安全カーネル単体試験：18件成功
- NRA-IDE正典参照試験：38件成功
- リポジトリ既存テストディスカバリ：65件成功
- 設計文書内のPython参照コード：AST構文解析成功
- `safety_kernel/`内にファイル書込み、外部送信、プロセス実行機能がないことを静的確認
- `__pycache__`、`.pyc`、SQLite DBを生成していないことを確認

## 2026-08-13：履歴・厚み・問い直し・二段階達成の実装

### 探索で追加確定した考え方

- `R=1.0`への到達時刻は外部観察だけでは線形に予測できないため、単一点のRに加えて残存厚みとその減少履歴を扱う。
- 厚みの減少、加速、段差損失、複数要因の重なりは、急激な境界到達の事前状態になり得る。
- 見過ごし、先送り、無理な継続は、未解決、上書き、再発という観測可能な応答履歴に変換する。
- 報告上の「完了」と現実上の「解消」を分け、後続の独立観測と照合する。
- 目的解の完成と現実実行を別段階にし、確認回答を実行権限へ変換しない。
- リスク事実と依頼内容の不整合が大きいほど、問い直し強度を上げる。

### 追加したシャドー実装

- 厳格Action Proposal decoder
- Instruction Contractと提案整合性検査
- hash chain付きメモリ内履歴台帳
- 報告と現実観測のreconciliation
- ドメイン固有Thickness Modelの入力契約と保守側境界評価
- 警告後の対応履歴と現実解消のresponse integrity評価
- リスク適応型clarification（回答は権限を付与しない）
- Solution StageとRealization Stageの二段階達成状態
- 実行、権限、問い直し、証言、監査、回復の独立Directive
- 読取専用ファイル観察器
- 同一スナップショットの決定論的リプレイと判定digest

### この段階の境界

- 観察器はAI申告値ではなく実ファイルを読むが、同一プロセス内のPoCであり、別権限・署名済みの本番信頼根ではない。
- 履歴台帳はメモリ内hash chainであり、外部保全された監査ログではない。
- 具体的な厚み換算式は普遍化せず、対象ドメイン、単位、観測、更新・回復規則が確定したモデルだけを受け付ける。
- Capability、executor、実ファイル変更、Git操作、外部送信は実装していない。

### 検証結果

- シャドー安全カーネル単体試験：29件成功
- NRA-IDE正典参照試験：38件成功
- リポジトリ既存テストディスカバリ：65件成功
- `poc_horizontal_ai/`配下のPython 26ファイル：AST構文解析成功
- 設計文書内のPython参照コード1ブロック：AST構文解析成功
- `safety_kernel/`内に外部通信、プロセス実行、ファイル書込みAPIがないことを静的確認
- `__pycache__`、`.pyc`、SQLite DBを生成していないことを確認

---

## 2026-08-13：限定ドメイン厚みモデルと観察プロセス境界

### 今回固定した対象

限定ファイル変更AIだけを対象に、厚みの単位を`review-unit`へ固定した。これは他領域へ通用する普遍量ではなく、係数、容量、閾値の実測校正前は安全値として扱わない。

### 追加した実装

- 未解消提案量を`delta`、観察済み容量から保守余裕と別原因の損失を引いた量を`tau`とするファイル変更専用モデル
- 提案量を`delta`と`tau`へ二重計上しない更新規則
- 型付きProposalのdiffから変更行数と対象数を機械計測する経路
- baseline、提案、解消、厚み損失、独立確認済み回復の閉じた履歴fact
- trusted sourceとhash chainを満たさない履歴の`INPUT_EXCEPTION`
- 段差損失、加速消耗、消耗、確認済み回復のtrend分類
- nonce、要求digest、対象、state version、時刻、鮮度、snapshot digestを照合する観察protocol
- stdin/stdoutで一要求だけを処理する別プロセス観察entry point
- 履歴record digest、chain、head digest、外部anchorを照合するportable audit bundle

### この段階の境界

- ファイル変更モデルの係数と閾値は試験値であり、実測校正済みではない。
- 観察protocolはプロセス分離を可能にするが、同一OS権限では真正性の最終証明にならない。
- audit bundleは外部アンカーへ渡せる形式だが、外部保存、署名、送信自体は行わない。
- nonce再利用防止は、今後の別権限呼出側で永続管理する必要がある。
- Capability、executor、実ファイル変更、自動commit、pushは引き続き実装していない。

### 検証結果

- シャドー安全カーネル単体試験：41件成功
- 別Pythonプロセスでの観察要求・応答試験：成功
- 厚みの段差損失から`IRREVERSIBLE_TRANSITION`と実行拒否への統合試験：成功
- audit bundleの改ざん検出と外部anchor不一致検出：成功
- NRA-IDE正典参照試験：38件成功
- リポジトリ既存テストディスカバリ：65件成功
- `poc_horizontal_ai/`配下のPython 31ファイルと文書内Python 1ブロック：AST構文解析成功
- 公開export 76件：欠損・重複なし
- 本体コードが外部通信、子プロセス起動、ファイル書込みを行わないことを静的確認
- `__pycache__`、`.pyc`、SQLite DBを生成していないことを確認

---

## 2026-08-13：認証・一回性・監査anchorのtrusted runtime

### 今回分離した責務

前段で残した観察器真正性、nonce再利用、audit head外部固定を、安全カーネル本体ではなく`trusted_runtime/`へ分離した。

### 追加した実装

- HMAC-SHA256認証envelope
- payload digest、key ID、発行時刻、鮮度の検証
- master keyから観察認証、nonce台帳、anchor台帳への用途別subkey導出
- request IDとnonceのSQLite永続一回性台帳
- nonce台帳のappend-only triggerとHMAC chain
- 鮮度検査、一回性消費、実ファイル観察、応答認証を合成するgateway
- audit bundle検証後にhead digest、event count、bundle digestを固定するanchor台帳
- 重複head拒否、append-only trigger、HMAC chain、認証receipt
- key fileを起動時だけ読むobserver gatewayとanchor service

### この段階の境界

- HMACは共有鍵方式であり、公開鍵署名ほど検証責務を分離できない。
- 鍵はOS key store、HSM、TPMへ隔離していない。
- SQLite triggerは通常の更新・削除を拒否するが、DB所有者によるファイル全置換・末尾切捨てを単独では防げない。
- 本番ではDB書込権限のOS分離と、receiptの別権限WORM保全が必要である。
- Capability、executor、patch適用、commit、pushは実装していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：48件成功
- 認証payload改変検出：成功
- nonce台帳を閉じて再度開いた後のreplay拒否：成功
- nonce行のUPDATE・DELETE拒否：成功
- 別プロセスgatewayでの認証応答と二回目要求拒否：成功
- audit headの重複固定拒否とreceipt認証：成功
- 別プロセスanchor serviceでのbundle検証・receipt返却：成功
- NRA-IDE正典参照試験：38件成功
- リポジトリ既存テストディスカバリ：65件成功
- `poc_horizontal_ai/`配下のPython 40ファイルと文書内Python 1ブロック：AST構文解析成功
- safety kernel公開export 76件、trusted runtime公開export 12件：欠損・重複なし
- リポジトリ配下に鍵、SQLite DB、receipt、`__pycache__`、`.pyc`を生成していないことを確認

---

## 2026-08-13：Ed25519署名境界と複数witness

### 今回進めた境界

HMAC共有鍵では検証者も認証値を生成できるため、観察応答とanchor receiptの新規経路をEd25519へ分離した。署名側だけが秘密鍵を持ち、判定・照合・witness側は公開鍵だけを持つ。

### 追加した実装

- Ed25519署名envelope
- key ID、公開鍵fingerprint、payload digest、署名時刻の厳格検証
- 公開鍵だけを使う観察応答検証
- 永続nonce消費後にだけ署名する観察service
- audit bundle検証後に署名receiptを返すanchor service
- 同じaudit headへの署名receiptをcreate-onlyで保持するwitness store
- 最低二つの異なるwitness IDを要求するquorum判定
- リポジトリ、秘密鍵、nonce DB、anchor DB、witness rootsの重複・内包検査
- OS identity分離をportable Pythonでは証明できないことを表す明示状態
- 使用した`cryptography 46.0.7`の依存版固定

### この段階の境界

- 公開鍵署名は観察内容やCause-Sideモデル自体の正しさを保証しない。
- 秘密鍵は試験用ファイルであり、HSM、TPM、OS key storeへ隔離していない。
- create-only witness fileは実WORM storageではなく、所有者による削除を防止しない。
- 同一OS identity配下の複数witness pathを独立主体とは証明できない。
- 鍵生成、配布、rotation、失効、外部WORM retentionは未実装である。
- Capability、executor、patch適用、commit、pushは実装していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：55件成功
- 署名payload改変と異なる公開鍵による検証失敗：検出成功
- 別プロセス観察署名と公開鍵だけの検証：成功
- 別プロセスanchor署名とbundle照合：成功
- 二つのwitnessによるquorum成立と一つだけの場合の不成立：成功
- リポジトリ内部の秘密鍵・DB・witness配置：拒否成功
- パス分離済みでもOS identity分離を未認証として保持：成功
- NRA-IDE正典参照試験：38件成功
- リポジトリ既存テストディスカバリ：65件成功
- `poc_horizontal_ai/`配下のPython 47ファイルと文書内Python 1ブロック：AST構文解析成功
- safety kernel公開export 76件、trusted runtime公開export 31件：欠損・重複なし

---

## 2026-08-13：鍵rotation・失効・認証witness主体

### 今回閉じた問題

- 公開鍵設定の旧版rollback
- 鍵の有効期間と失効の未管理
- 観察鍵、anchor鍵、witness鍵の役割横断
- rotation前後の二鍵を二つのwitnessとして数える問題
- witness IDが自己申告文字列だけであった問題

### 追加した実装

- offline root署名付き`trust-bundle/1.0`
- bundle generationと直前署名bundle digestの連鎖
- 鍵ID、principal ID、役割、有効期間、失効時刻の閉じた契約
- 同一公開鍵の複数trust record登録拒否
- 受入時に鮮度を要求する永続trust checkpoint
- 旧世代rollback、世代飛越し、直前digest不一致の拒否
- 後日監査時には鮮度と署名・chain完全性を分離する再検証
- 現時点で有効かつ未失効な役割別鍵だけを使う署名検証
- 観察署名を最新trust bundleへ接続する検証経路
- 保存済みreceiptに対するwitness自身のEd25519署名
- 異なる鍵IDではなく異なるprincipal IDを数えるquorum

### この段階の境界

- offline root秘密鍵のHSM隔離、root rotation、緊急失効は未実装である。
- pinned root公開鍵の配布・更新は外部deployment契約である。
- trust checkpoint DBの全置換・末尾切捨ては、最新digestの外部固定なしには防げない。
- witness principalが本当に別管理者・別hostかは、署名だけでなく外部identity attestationが必要である。
- Capability、executor、patch適用、commit、pushは実装していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：59件成功
- 失効済み旧観察鍵の拒否とrotation後新鍵の許可：成功
- anchor鍵による観察署名の役割不一致拒否：成功
- trust bundle rollback、世代飛越し、直前digest不一致の拒否：成功
- 同一公開鍵の複数役割登録拒否：成功
- checkpoint履歴の後日署名・chain再検証：成功
- 同一principalのrotation二鍵を一主体として数えるquorum：成功
- NRA-IDE正典参照試験：38件成功
- リポジトリ既存テストディスカバリ：65件成功
- `poc_horizontal_ai/`配下のPython 53ファイルと文書内Python 1ブロック：AST構文解析成功
- safety kernel公開export 76件、trusted runtime公開export 49件：欠損・重複なし

---

## 2026-08-13：trusted runtime起動認可とtrust state結合

### 今回閉じた問題

- Ed25519署名serviceがtrust bundleを参照せず、秘密鍵fileと自己申告key IDだけで起動できた問題
- 署名を検証したtrust bundleの世代とdigestが署名証拠自体に含まれなかった問題
- 観察・anchor・witnessでtrust state結合条件が揃っていなかった問題
- checkpointの初回受入と、受入済み最新世代を使う再起動の区別

### 追加した実装

- pinned offline root公開鍵による起動時trust bundle検証
- 永続checkpoint chain検証後の初回受入、次世代受入、最新世代再利用
- signer key ID、required role、有効期間、失効状態、秘密鍵と登録公開鍵の一致検証
- 認可済み署名者だけがtrust state結合署名を生成する`AdmittedSigner`
- trust bundle generationと署名bundle SHA-256を署名対象に含む`signed-payload/1.1`
- 観察、anchor、認証witnessのtrusted検証におけるbinding必須化
- 未結合`1.0`と異なるtrust stateへ結合された署名の明示拒否
- Ed25519観察・anchor serviceの起動引数へtrust bundle、checkpoint、pinned rootを追加

### この段階の境界

- checkpoint DBとpinned root公開鍵の配置・更新権限は外部deployment契約である。
- checkpoint DB所有者による全置換・末尾切捨ては、最新digestの外部固定なしには防げない。
- `AdmittedSigner`はfile秘密鍵providerであり、非exportable HSM・TPM・OS key store providerではない。
- offline root rotation、緊急失効、複数rootによる閾値承認は未実装である。
- witness署名のtrust state結合は実装したが、独立host・管理主体のidentity attestationは外部要件である。
- HMAC経路は前段互換PoCとして残り、trusted Ed25519 serviceとは別経路である。
- Capability、executor、patch適用、commit、pushは実装していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：63件成功
- trust bundle初回受入と受入済み最新世代によるservice再起動：成功
- 観察serviceとanchor serviceの別プロセス起動認可、`signed-payload/1.1`生成：成功
- signer role不一致、失効、秘密鍵不一致の起動拒否とcheckpoint未更新：成功
- trust state未結合署名と異なるbundle digest結合署名のtrusted検証拒否：成功
- rotation後観察署名と認証witness quorumのtrust state結合検証：成功
- NRA-IDE正典参照試験：38件成功
- リポジトリ既存テストディスカバリ：65件成功
- `poc_horizontal_ai/`配下のPython 55ファイル：AST構文解析成功
- safety kernel公開export 76件、trusted runtime公開export 51件：欠損・重複なし

---

## 2026-08-13：trust checkpoint外部witness固定

### 今回閉じた問題

- local checkpoint DBだけでは、DB全置換や末尾切捨てを検出できない問題
- 署名済みattestation fileだけでは、bundle・DB・attestationを一括して旧版へ戻せる問題
- rotation前後の複数witness鍵を複数主体として誤算入する問題
- 外部quorum不成立でもlocal checkpointが先に更新され得る順序

### 追加した実装

- generation、署名bundle digest、直前bundle digestを固定する`trust-checkpoint-attestation/1.0`
- `WITNESS_SIGNER`のrole、有効期間、失効、principal、秘密鍵一致を確認するattestation生成
- 異なるkey IDではなく異なるprincipal IDを数えるcheckpoint witness quorum
- 改変、不正署名、trust state不一致、古いattestationをquorumへ数えない検証
- witness側の独立append-only SQLite stateとattestation履歴
- 同一最新stateへの新鮮な再証言と、旧世代、世代飛越し、直前digest不一致、同世代別digestの拒否
- 別プロセス`checkpoint_witness_service`によるroot署名検証と単調attestation発行
- 観察・anchor service起動前の最低二principal外部quorum必須化
- quorum不成立時にlocal checkpointを作成・更新しない失敗閉鎖順序

### この段階の境界

- 外部固定の成立には、local checkpointと各witness stateを異なるOS identity、host、管理権限へ分離する必要がある。
- このPoCは別プロセスと別DBを実装するが、独立管理主体であること自体はportable Pythonから証明しない。
- witness DB所有者による全置換は、そのwitness単独では防げない。複数独立principalと外部WORMまたはtransparency logが本番要件である。
- witness keyはfile providerであり、HSM、TPM、OS key storeへ隔離していない。
- offline root rotation、緊急失効、複数root閾値承認は未実装である。
- Capability、executor、patch適用、commit、pushは実装していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：68件成功
- checkpoint attestation改変とtrust state不一致のquorum除外：成功
- rotation二鍵が同一principalの場合の一主体算入：成功
- witness側stateの新鮮な再証言と旧世代再証言拒否：成功
- checkpoint witness別プロセス起動と署名検証：成功
- 外部quorum不足時の署名service起動拒否とlocal checkpoint未作成：成功
- 観察serviceとanchor serviceの二principal quorum付き別プロセス起動：成功
- NRA-IDE正典参照試験：38件成功
- リポジトリ既存テストディスカバリ：65件成功
- `poc_horizontal_ai/`配下のPython 58ファイル：AST構文解析成功
- safety kernel公開export 76件、trusted runtime公開export 58件：欠損・重複なし

---

## 2026-08-15：不可逆ラッチheadの外部witness起動認可

### 今回閉じた問題

- 非空の不可逆ラッチDBを、外部主体による最新head確認なしに再起動できた問題
- witness key、witness DB、ラッチ対象scopeを別プロセス境界へ分離する実行経路の欠損
- 同一principalの複数鍵を複数witnessとして数え得る問題
- ローカルラッチ更新後も外部witness確認済みと誤認し得る状態表現

### 追加した実装

- `LATCH_CHECKPOINT_SIGNER`によるtrust state結合済みラッチcheckpoint署名
- witnessごとの固定`latch_store_id`と単調なappend-only SQLite state
- rollback、sequence飛越し、直前head不一致、別ラッチscopeの署名拒否
- 異なるkey IDではなく異なるprincipal IDを数えるラッチwitness quorum
- 別プロセス`latch_witness_service`によるroot署名検証、秘密鍵読込、単調attestation発行
- 非空ラッチ再起動時の、ローカル最新headと完全一致する新鮮な二principal quorum必須化
- 新規ラッチ生成後に`external_witness_current=False`へ遷移する明示状態
- 空の新規ラッチと、外部証明待ちの非空ラッチを分けた起動判定

### この段階の境界

- 空DBと全ローカルcheckpointを同時に置換された場合、外部witnessへの照会なしでは新規空状態とrollback後の空状態を区別できない。genesisの外部登録または起動時witness照会が次段階で必要である。
- 新しいラッチheadの生成直後は外部attestationがまだ存在せず、ランタイムは`external_witness_current=False`となる。現実実行経路を追加する場合、この状態を実行拒否へ接続する必要がある。
- ラッチcheckpoint署名関数は実装したが、checkpoint signer自体の別identity・別process配置は未実装である。
- 別プロセスと別DBは実装したが、別host・別管理者・OS identityの独立性はportable Pythonから証明しない。
- witness DB所有者による当該witness単独の全置換は防げない。成立条件は複数独立principal、鍵分離、外部WORMまたはtransparency logである。
- Capability、executor、patch適用、commit、pushは実装していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：96件成功
- 非空ラッチの外部証明なし再起動拒否：成功
- 一principal不足quorumの起動拒否：成功
- 二principalの同一checkpoint証明による再起動：成功
- ラッチ更新後の`external_witness_current=False`遷移：成功
- ラッチwitness別プロセス起動と署名検証：成功
- rollback、sequence飛越し、別scope、署名改変の拒否：成功
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功

## 2026-08-15：外部genesis登録と一回限りの起動challenge

### 今回閉じた問題

- 空ラッチを外部証明なしの新規状態として起動できた問題
- ローカルDBと全ローカルcheckpointの同時置換後に、空状態を新規環境と誤認できた問題
- 鮮度時間内の古いgenesis attestationを別の起動へ再利用できる短時間replay
- witnessが非空headへ進んだ後も空状態を再証言できる可能性

### 追加した実装

- `latch_store_id`から決定論的に導出するsequence 0の`irreversible-latch-genesis/1.0`
- `LATCH_CHECKPOINT_SIGNER`によるtrust state結合済みgenesis checkpoint
- witness append-only stateへのgenesis登録と、genesisからsequence 1への単調遷移
- sequence 1以降へ進んだwitnessによるgenesis再証言のrollback拒否
- factory以外から構築できないprocess-local `BoundaryAdmissionChallenge`
- challenge nonceを含む`latch-witness-attestation/1.1`
- 起動ごとに異なるchallengeとの完全一致を要求するquorum判定
- 成功したchallengeの再利用拒否
- 空ラッチを含む全起動で、同一checkpoint・同一challengeに対する最低二principal証明を必須化
- 別プロセス`latch_witness_service`のrequestへadmission challengeを追加

### この段階の境界

- challenge生成、複数witness service呼出、証拠収集、`admit_boundary_runtime`呼出を一体化するlauncher/orchestratorは未実装である。
- `BoundaryAdmissionChallenge`はprocess-local PoC境界であり、Python process自体を支配する同一管理者に対する強制分離を証明しない。
- witness serviceへのtransport認証、別host identity、応答の可用性、timeout方針は外部deployment契約である。
- latch checkpoint signer自体の別process・別identity配置は未実装である。
- witness DB所有者による当該witness単独の全置換は防げず、複数独立principalの同時侵害耐性に依存する。
- Capability、executor、patch適用、commit、pushは実装していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：97件成功
- 外部genesis quorumによる空ラッチ起動：成功
- witnessのgenesisから非空headへの単調遷移：成功
- 非空head到達後のgenesis再証言拒否：成功
- challenge結合attestationの別プロセス生成と検証：成功
- 一principal不足、checkpoint不一致、challenge不一致の起動拒否：成功
- 成功済みchallengeの再利用拒否：成功

---

## 2026-08-15：challenge-bound witness launcher統合

### 今回閉じた問題

- challenge生成、checkpoint作成、複数witness呼出、quorum収集、runtime admissionが呼出側の手作業に分断されていた問題
- 最新headだけの送信では、一観察で複数axisがラッチされたsequence飛越しにwitnessが追随できない問題
- 複数witness設定の重複DB・重複principal・欠損鍵を、外部state更新開始前に拒否できなかった問題
- witnessの一部だけが更新された後の再試行経路が未検証であった問題

### 追加した実装

- 一つの失敗閉鎖入口`launch_boundary_runtime`
- `LatchWitnessProcess`によるwitness DB、principal、key、秘密鍵fileの閉じたprocess設定
- runtime placement、時間policy、trust bundle、pinned root、checkpoint signer roleと鍵一致の事前検証
- launcher内部でのみ保持する一回限りのadmission challenge生成
- 空状態ではgenesis、非空状態ではsequence 1から最新headまでの連続checkpoint列を署名
- 各witness serviceへの同一challenge・同一checkpoint列の別プロセス送信
- witness側で既存の一致prefixを検証して読み飛ばし、未観察suffixだけをappendする追随処理
- 不一致prefix、古い末尾、sequence gapの拒否維持
- 全attestation収集後だけruntime admissionへ進む順序
- subprocess timeout、応答サイズ上限、非zero終了の一般化された失敗閉鎖
- 一witness更新後に別witnessが失敗しても、新challengeで安全に再試行できる経路

### この段階の境界

- checkpoint signerは検証済み`AdmittedSigner`として受け取るが、launcher process内で秘密鍵を使用する。別process・別OS identityのcheckpoint signer service化は未実装である。
- witness transportはlocal subprocess実装であり、remote host用の相互認証transport adapterは未実装である。
- witness processが設定上の別principalであっても、実際に別管理者・別host・別OS identityであることはportable Pythonから証明しない。
- `admit_boundary_runtime`低水準APIは残る。ただしchallengeと外部quorumを省略した起動は拒否される。
- launcher取得後に生成された新headは引き続き`external_witness_current=False`となり、次回launcher起動で外部固定される。現実実行gateへの接続は未実装である。
- Capability、executor、patch適用、commit、pushは実装していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：99件成功
- launcherによる外部genesis登録と空ラッチ起動：成功
- 一観察でsequence 2へ進んだラッチの連続checkpoint追随：成功
- 既存一致prefixの検証と未観察suffix追加：成功
- 一witnessだけ更新後の別witness失敗と新challenge再試行：成功
- trust、role、鍵、process設定、timeout、quorum不成立時の失敗閉鎖：成功
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功

---

## 2026-08-15：latch checkpoint signer別process分離

### 今回閉じた問題

- launcherがcheckpoint signer秘密鍵を直接保持・使用していた問題
- 呼出側が提示したheadをそのまま署名対象にできる構造上の危険
- signerのtrust rollback、role不一致、公開鍵と秘密鍵の不一致をlatch witness更新前に拒否する経路の不足
- signer失敗時に一部のlatch witnessだけが先行更新され得る実行順序

### 追加した実装

- 一要求だけを処理する別process `latch_checkpoint_signer_service`
- signer service自身による実ラッチDBのopen、HMAC chain検証、署名対象headの導出
- `admit_file_signer`によるpinned root、trust checkpoint外部quorum、trust rollback、`LATCH_CHECKPOINT_SIGNER` role、鍵一致の検証
- 空状態のgenesis、またはsequence 1から最新headまでの連続checkpoint列の署名
- launcher側の厳格な応答schema検証、応答サイズ上限、timeout、非zero終了時の失敗閉鎖
- launcherによるラッチDB再読込と、返却された全checkpointの公開鍵検証・実head完全一致確認
- signer秘密鍵、ラッチintegrity key、trust checkpoint DBの配置preflight
- signer成功と応答検証が完了した後にだけlatch witness更新へ進む実行順序

### この段階の境界

- 別process化はしたが、portable Pythonから別OS identity、別host、別管理者であることは証明しない。
- signer serviceは呼出側提示headを信用しないため、現構成ではラッチDB検証用HMAC鍵とcheckpoint署名秘密鍵の双方を保持する。より強い分離には、独立認証されたread-only head供給とHSM等の非export鍵が必要である。
- runtime admission側もラッチDB検証用HMAC鍵を使用するため、現段階ではruntimeとsignerの間でHMAC鍵が共有される。同一管理者による双方の同時置換耐性は未成立である。
- trust checkpoint witnessはserviceへ渡すfileであり、remoteからのlive取得は未実装である。
- launcher取得後に生成された新headは`external_witness_current=False`となる。現実実行gateへの接続は未実装である。
- Capability、executor、patch適用、commit、pushは実装していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：100件成功
- 別process signerによるgenesisおよび連続head署名：成功
- signer service自身による実ラッチDB検証：成功
- sequence 2まで進んだ複数headと返却checkpoint列の完全一致検証：成功
- signer秘密鍵不一致時に全latch witness DBが未更新であること：成功
- trust checkpoint quorum、role、鍵、配置preflightの失敗閉鎖：成功
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功

---

## 2026-08-15：外部witness結合二段階execution gate

### 今回閉じた問題

- `external_witness_current`が観察可能な状態に留まり、現実作用直前の許可条件へ接続されていなかった問題
- 評価後に状態が変化しても、以前の確認結果を実行へ転用できるTOCTOU
- 一つの確認結果を別intentへ転用、または複数回利用できる可能性

### 追加した実装

- `BoundaryExecutionIntent`によるintent ID、target ID、action digestの固定
- 第1段階`prepare_execution`による、外部witness確認済み状態へのprocess-local capability結合
- 第2段階`admit_execution`による、作用直前の外部witness鮮度、評価世代、ラッチhead、intent完全一致の再確認
- admission試行時点でのcapability一回限り消費
- 評価が一度でも挟まったcapabilityの失効
- 新しい不可逆headにより`external_witness_current=False`となった後のprepareおよびadmit拒否
- gate通過を表す`BoundaryExecutionAdmission` receipt。現実作用自体は実行しない。

### この段階の境界

- intent digestが実際の外部作用と一致することを強制するexecutorは未実装である。
- 外部の事前定義authorityによるintent署名・承認は未接続である。このgate単独はauthorityを生成せず、witness-current実行条件だけを扱う。
- capabilityはprocess-local Python objectであり、別OS identityやadversarialな同一processからの強制分離を証明しない。
- admission receiptは実行完了証明ではなく、gate通過証明だけである。
- 実行結果の観察、報告との照合、不可逆ラッチへのfeedback接続は未実装である。
- execution gateを介した外部作用は未実装であり、commitとpushは実施していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：101件成功
- 外部witness確認済み状態での二段階prepare/admit：成功
- capability再利用拒否：成功
- 別intentへの転用拒否と、失敗したcapabilityの再利用拒否：成功
- 評価を挟んだcapabilityの失効：成功
- 新しい不可逆head後のprepare/admit拒否：成功
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功

---

## 2026-08-15：trust結合済み外部execution authorization

### 今回閉じた問題

- witness-currentだけで任意intentのcapabilityを準備でき、外部authorityによる許可が未結合であった問題
- checkpoint signerやwitness signerをexecution authorizerとして流用できるrole混同
- 同じ署名済みauthorizationから複数capabilityを作り、runtime再起動後も再実行できるreplay
- authorization後に別ラッチheadへ移った状態で、古い許可を再利用できる可能性

### 追加した実装

- trust bundle専用role `EXECUTION_AUTHORIZER`
- exact intent、latch store ID、期待ラッチhead、authorization ID、nonce、許可時刻、有効期限を持つ閉じた署名schema
- trust bundle generationおよび署名済みbundle hashへのauthorization署名結合
- runtime admissionで保持したverified trust bundleだけを使う署名・role・鍵有効性検証
- 生intentからの`prepare_execution`を廃止し、署名済みauthorizationだけを受理する入口へ置換
- execution authorization専用配置DBと、HMAC chain付き永続一回消費ledger
- `admit_execution`時のauthorization ID・nonce永続消費と、runtime再起動横断replay拒否
- admission receiptへのauthorization IDとauthorizer principal IDの保持

### この段階の境界

- authorizationは現段階では一principalの署名であり、リスク・厚みに応じた複数principal quorumは未実装である。
- authorizer署名秘密鍵の別process、別OS identity、HSM等への配置は未実装である。
- action digestとexecutorが実際に行う作用の一致を強制するexecutor境界は未実装である。
- execution authorization ledgerはラッチintegrity keyから導出したHMAC鍵を使用する。同一管理者によるラッチDB、authorization DB、鍵の同時置換耐性は未成立である。
- admission receiptの外部anchorと、実行結果の観察・報告・不可逆ラッチへのfeedback接続は未実装である。
- execution gateを介した外部作用は未実装であり、commitとpushは実施していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：102件成功
- `EXECUTION_AUTHORIZER`によるexact intent署名とruntime検証：成功
- checkpoint signerからexecution authorizerへのrole流用拒否：成功
- trust state、latch store、ラッチhead、有効期限へのauthorization結合：成功
- authorization ID・nonceの永続一回消費：成功
- runtime再起動後の同一authorization replay拒否：成功
- 既存constructor bypass拒否の意味を保持：成功
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功

---

## 2026-08-15：distinct-principal execution authorization quorum

### 今回閉じた問題

- execution authorizationが一principalの署名だけで成立し、一管理者・一鍵の侵害がそのまま実行許可へ到達する問題
- 同一principalの署名または同じ署名の複製を、複数確認として数えられる可能性
- 異なるintentやauthorization payloadへの正しい署名を寄せ集め、quorumとして扱える可能性
- quorum必要数を`prepare_execution`呼出側が下げられる構成上の危険

### 追加した実装

- runtime admission policyとして固定する`minimum_execution_authorizer_principals`
- 二principal未満を許さないlauncherおよび低水準runtime admissionの設定検証
- 複数の`EXECUTION_AUTHORIZER`署名を検証する`assess_execution_authorization_quorum`
- 署名数ではなくtrust bundle上のdistinct principal IDによるquorum集計
- 全署名が同一canonical authorization payloadを指すことのdigest一致検証
- capabilityへのverified authorization quorum結合
- admission receiptへの全authorizer principal ID保持
- 永続replay ledgerのrequest digestを、署名者に依存しないcanonical authorization payload digestへ変更

### この段階の境界

- 現段階は固定二principal下限であり、厚み・作用リスクに応じて三principal以上へ段階的に増加させるpolicyは未実装である。
- 動的quorumには、呼出側の自己申告ではないtrusted risk/thickness classificationの結合が必要である。
- 各authorizerの別管理者、別OS identity、別host配置はportable Pythonから証明しない。
- authorizer署名秘密鍵の別process・HSM配置は未実装である。
- action digestと実作用の一致を強制するexecutor、実行結果観察、外部anchor、feedback接続は未実装である。
- execution gateを介した外部作用は未実装であり、commitとpushは実施していない。

### 検証結果

- safety kernelおよびtrusted runtime試験：102件成功
- 二distinct-principalの同一authorizationによるquorum成立：成功
- 一principalだけのauthorization拒否：成功
- 同じ署名を複製した見かけ上の二署名拒否：成功
- 二つの正しい署名が異なるpayloadを指す場合の拒否：成功
- runtime再起動後のquorum authorization replay拒否：成功
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功

---

## 2026-08-15：runtime入口でのtrust provenance再検証

### 今回閉じた問題

- 呼出側が直接構築した`VerifiedTrustBundle`を、低水準runtime admissionが検証済みtrust stateとして受理できた問題
- trust bundle不正が判明する前に、ラッチDBまたはlocal checkpointへ到達し得る検証順序
- launcherで確認した署名JSONと、runtime admissionが使用するtrust stateの入口が分離していた問題

### 追加した実装

- `ExternalLatchWitnessEvidence`を、`VerifiedTrustBundle` objectではなくroot署名済みtrust bundle JSONを保持する契約へ変更
- `admit_boundary_runtime`自身によるpinned root署名、鮮度、閉じたtrust bundle schemaの再検証
- 再検証で得たbundleだけをlatch checkpoint、witness quorum、execution authorizationのtrust sourceとして使用
- trust再検証を不可逆ラッチDB openおよびlocal checkpoint同期より前へ移動
- launcherが事前検証に使用した同じ署名JSON、pinned root、鮮度policyをruntime admissionへ引き渡す経路
- 署名改変、異なるpinned root、期限切れbundleをlocal state作成前に拒否する回帰試験

### この段階の境界

- pinned root自体の正当性はdeployment configurationに依存する。低水準API呼出側がpinned root設定権限を持つ構成では、その設定主体をtrust boundary外へ分離できない。
- launcherと低水準runtime admissionは同一process内で再検証する。別OS identity、別host、別管理者によるpinned root policy強制は未実装である。
- trust bundle checkpointの単調性と外部quorumはcheckpoint signer serviceで検証するが、低水準runtime admission単独ではその外部配置を証明しない。
- execution receiptと実作用の不可分な消費、witness入力列の厳密順序、旧anchor witness APIのrole結合は次段階で扱う。

### 検証結果

- safety kernelおよびtrusted runtime試験：103件成功
- trust bundle署名改変のruntime admission拒否とラッチDB未作成：成功
- 異なるpinned rootによるruntime admission拒否とlocal checkpoint未作成：成功
- 期限切れtrust bundleのruntime admission拒否とlocal state未作成：成功
- launcherのgenesis、複数head、部分witness失敗後再試行：成功
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功

---

## 2026-08-15：witness入力列のcanonical順序固定

### 今回閉じた問題

- witness state storeが既に保存済みのcheckpointを入力列内で読み飛ばし、逆順または重複した列でも最終headが現在状態と一致すればattestationを発行できた問題
- 各checkpointの署名と保存済み状態との一致は正しくても、witnessが観察したcheckpoint列の順序を一意に説明できなかった問題

### 追加した実装

- witnessへ渡されたcheckpoint列全体に対する厳密なsequence増加検証
- 隣接checkpoint間の`previous_mac`連結検証
- 逆順または重複を`LATCH_WITNESS_CHAIN_INVALID`として、DB更新およびattestation発行前に拒否
- 正しい順序の保存済みprefix再提示を維持し、拒否試行でattestation sequenceを消費しない回帰試験

### この段階の境界

- 今回固定したのは、一witnessへ渡す署名済みlatch checkpoint列の順序である。複数witnessから返るattestation tupleの並び自体はauthorityを表さず、quorumはdistinct principal IDをcanonical sortして扱う。
- witnessが既に保持する連続prefixより後から始まる正しいsuffixは受理できる。欠落prefixの正当性はwitness自身のappend-only state検証に依存する。
- execution receiptと実作用の不可分な消費、および旧anchor witness APIのrole結合は未実装である。

### 検証結果

- safety kernelおよびtrusted runtime試験：104件成功
- 保存済みheadを含む逆順checkpoint列の拒否：成功
- 保存済みheadを含む重複checkpoint列の拒否：成功
- 正しい既存prefix再提示の受理と、拒否後のattestation sequence非消費：成功
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功

---

## 2026-08-15：anchor署名・witness検証のrole結合一本化

### 今回閉じた問題

- `anchor_and_sign_bundle`が、runtime admissionを経ない任意の秘密鍵でも署名済みanchor receiptを生成できたraw-key fallback
- `CreateOnlyWitnessStore.record`の呼出側が任意の公開鍵集合をtrustedとして渡し、root署名済みtrust bundle上の`ANCHOR_SIGNER` roleを介さずwitness recordを作成できた問題
- role結合済み`verify_trusted_anchor_receipt`と、任意公開鍵を受ける旧公開検証APIが同じ目的で並存していた問題

### 追加した実装

- `anchor_and_sign_bundle`の`AdmittedSigner`必須化とraw-key署名経路の廃止
- signer recordの`ANCHOR_SIGNER` role、有効期間、失効状態、trust bundle内record、公開鍵fingerprint、秘密鍵fingerprintの再確認
- anchor receipt署名へのtrust bundle generationおよび署名済みbundle hash結合の必須化
- `CreateOnlyWitnessStore.record`を`VerifiedTrustBundle`入力へ変更し、`verify_trusted_anchor_receipt`だけをauthority検証入口として使用
- 任意公開鍵を受ける旧検証関数の公開export廃止と、role確認後のschema・bundle照合にだけ使う内部解析関数化
- `OBSERVER_SIGNER` receiptおよびtrust state未結合receiptを、witness file作成前に拒否する回帰試験

### この段階の境界

- `AdmittedSigner`はportable Pythonのdataclassであり、constructor自体を別process権限で封印しない。anchor compositionは構成要素を再検証し、witness側は独立してverified trust bundleへ照合するが、同一process内の強制分離は証明しない。
- `AuditAnchorStore`のHMAC receiptはlocal ledger integrity用であり、role結合済みsigned receiptとは別層である。`CreateOnlyWitnessStore`はHMAC receiptだけをauthority evidenceとして受理しない。
- create-only witness rootの別管理者、別OS identity、別host配置はportable Pythonから証明しない。
- execution receiptと実作用の不可分な消費、および実行結果の観察・報告・不可逆feedback接続は未実装である。

### 検証結果

- safety kernelおよびtrusted runtime試験：104件成功
- `ANCHOR_SIGNER`以外によるanchor作成拒否とanchor sequence非消費：成功
- `OBSERVER_SIGNER` receiptのwitness記録拒否とwitness file未作成：成功
- trust state未結合receiptのwitness記録拒否とwitness file未作成：成功
- role結合済み別process anchor serviceと二witness quorum：成功
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功

---

## 2026-08-16：実行内容結合と結果不明の永続停止

### 今回閉じた問題

- execution gateが許可receiptを返すだけで、許可された内容と実際にexecutorへ渡すbytesが同一であることを保証していなかった問題
- authorization ID・nonceを消費した後の実作用開始、成功、結果不明を再起動後へ残す実行試行記録がなかった問題
- executor開始後に結果を確認できない場合、安全または失敗へ推測分類して自動再試行できる余地

### 追加した実装

- runtime admission時に固定する`BoundaryExecutor`と、実作用完了後にだけ返す`BoundaryExecutionResult`
- authorizationが署名した`action_digest`と、executorへ渡す実bytesのSHA-256完全一致確認
- authorization消費と`PREPARED`実行試行作成を一つの`BEGIN IMMEDIATE` transactionで確定
- HMAC結合したappend-only event列による`STARTED`、`SUCCEEDED`、`OUTCOME_UNKNOWN`の永続記録
- executor例外を`OUTCOME_UNKNOWN`として記録し、未解決の`PREPARED`、`STARTED`、`OUTCOME_UNKNOWN`が一件でもあれば新しい実行を`EXECUTION_OUTCOME_RECONCILIATION_REQUIRED`で拒否
- 同じauthorizationのruntime再起動横断replay拒否を、実作用経路まで含めて維持

### この段階の境界

- PoCが保証するのは、正確なaction bytesの結合、実行前記録、成功記録、結果不明時の停止である。外部システムの状態変更とSQLite記録を一つのtransactionへ含められないため、外部作用のexactly-onceは保証しない。
- `PREPARED`だけが残った場合も自動的に「未開始」と断定せず、現在は保守的に要照合として停止する。`OUTCOME_UNKNOWN`を外部観察で`SUCCEEDED`または安全に再試行可能と確定するreconciliation権限・手順は未実装である。
- executorはruntime admission時に固定するが、同一process内のPython objectである。別OS identity、別host、外部idempotency storeによる強制分離は実装していない。
- 今回の回帰試験executorは記録用test doubleであり、現実の外部システムへ作用するexecutorは追加していない。
- 実行結果の観察・報告を既存のresponse integrityおよび不可逆feedbackへ接続する処理は次段階で扱う。

### 検証結果

- safety kernelおよびtrusted runtime試験：105件成功
- action digest不一致時のexecutor非呼出し：成功
- 成功時のexecutor一回呼出し、result digest記録、authorization replay拒否：成功
- executor例外後の`OUTCOME_UNKNOWN`永続化と、runtime再起動後の新規実行停止：成功

---

## 2026-08-16：executor返却と現実成功の意味分離

### 今回閉じた問題

- executorがbytesを返した段階を`SUCCEEDED`と記録すると、外部作用の現実到達を独立観察していないにもかかわらず成功と読めた問題
- executor返却後の試行を解決済みとして扱い、次の実作用へ進めた問題

### 追加した実装

- 公開結果型を`BoundaryExecutionReport`へ変更し、executor返却は作用結果の報告であって現実成功の証明ではないことを固定
- journal状態を`SUCCEEDED`から`EXECUTOR_RETURNED`へ変更
- reportへ`ResponseIntegrityState.COMPLETED_UNVERIFIED`を明示
- `PREPARED`、`STARTED`、`EXECUTOR_RETURNED`、`OUTCOME_UNKNOWN`をすべて未解決として扱い、新しい実作用を停止
- 未解決停止中でも、既消費authorizationの再提示は`NONCE_OR_REQUEST_REPLAY`として区別

### この段階の境界

- `EXECUTOR_RETURNED`は、executor呼出しと返却bytesの永続記録までを表す。目的達成、外部状態変更、期待状態との一致は表さない。
- 未検証reportを解除する経路は意図的にまだ追加していない。observerには期待値を渡さず、root署名済みtrust bundleの`OBSERVER_SIGNER` roleで試行・intent・対象・観察fieldへ結合した実測値を作り、reconcilerだけがintent内の期待値と照合する構成を次段階で実装する。
- 現段階では正常なexecutor返却後も次の実作用は停止する。これは観察接続前に成功を推測しないための保守的な中間状態である。

### 検証結果

- safety kernelおよびtrusted runtime試験：105件成功
- executor返却reportが`COMPLETED_UNVERIFIED`であること：成功
- runtime再起動後も新規実行が`EXECUTION_OUTCOME_RECONCILIATION_REQUIRED`で停止すること：成功
- 同じauthorizationのreplayが未解決停止と混同されず拒否されること：成功

---

## 2026-08-16：期待値非開示の署名済み観察証拠契約

### 今回閉じた問題

- observerへ期待値を渡す構成では、実測せず期待値を反射しても一致判定が成立し得る問題
- execution authorizationがaction内容だけを結合し、実行後に期待するfield・値を署名対象に含めていなかった問題
- execution用の観察証拠に、root署名済みtrust bundle上のobserver roleとdistinct-principal quorumを適用する契約がなかった問題

### 追加した実装

- `BoundaryExecutionIntent`へ`effect_field`と`expected_effect_value`を追加し、execution authorizationの閉じた署名schemaへ結合
- 期待値引数を持たず、試行ID、intent ID、対象、観察field、実測値だけを署名する`execution-reality-observation/1.0`
- trust stateへ結合された`OBSERVER_SIGNER` role、有効期間、公開鍵・秘密鍵一致の検証
- 観察IDと時刻は個別に保持しつつ、同じ試行・intent・対象・field・実測値に一致するdistinct principalだけを数える観察quorum
- 同一principal重複、role違反、署名payload改変、実測値不一致の拒否

### この段階の境界

- 期待値はauthorization側だけにあり、観察作成関数の引数および署名payloadには含まれない。reconciler以外で期待値と実測値を比較しない。
- 今回追加したのは署名済み観察証拠の契約である。署名関数はobserver-side integrationから実測値を受け取るため、それ自体が物理的な測定や別process配置を証明するものではない。
- 観察quorumはまだexecution journal内の実在する試行へ照合されず、`VERIFIED_RESOLVED`または`CONFLICT`を記録しない。したがって未検証実行の停止は解除されない。
- 次段階では、期待値を受け取らず対象を自ら測定するobserver-side processまたはdomain adapterを固定し、その署名証拠をruntime reconcilerが実在試行と照合する。

### 検証結果

- safety kernelおよびtrusted runtime試験：106件成功
- 観察作成APIおよび署名payloadへの期待値非混入：成功
- 二つの異なる`OBSERVER_SIGNER` principalによる実測値quorum：成功
- 同一principal重複、role違反、改変、実測値不一致の拒否：成功

---

## 2026-08-16：「期待値」から必須事後条件への語彙分離

### 今回閉じた問題

- `expected_effect_value`という名称が、authorizationによる必須条件ではなく、AIの予測または希望的観測として読めた問題
- authorization側とobserver側が同じ`effect_field`語彙を使用し、要求と観察の責任境界が名称上で混ざっていた問題
- 閉じた署名payloadのfield構成を変更したのにschema versionが`1.0`のままだった問題

### 追加した実装

- authorization側を`postcondition_field`と`required_postcondition_value`へ変更
- observer側を`observation_field`と`observed_value`へ変更
- execution authorization schemaを`boundary-execution-authorization/1.1`へ更新
- execution reality observation schemaを`execution-reality-observation/1.1`へ更新

### 意味上の固定

- `required_postcondition_value`は、希望、予測、平均としての期待値ではなく、権限主体が署名した必須の事後条件である。
- observerは`required_postcondition_value`を受け取らず、指定された`observation_field`の実測値だけを返す。
- 将来のreconcilerが、authorizationの`postcondition_field`と観察の`observation_field`の対応を確認した後、必須事後条件と実測値を比較する。

### この段階の境界

- 今回は語彙と署名schemaの責任分離であり、observer-side物理測定processおよびexecution journal解除はまだ実装していない。
- `1.0`形式との後方互換受理は追加していない。現段階は未公開PoCの閉じたschema置換として`1.1`だけを受理する。

### 検証結果

- safety kernelおよびtrusted runtime試験：106件成功
- NRA-IDE正典参照試験：38件成功
- 旧`effect_field`、`expected_effect_value`、旧schema `1.0`のPython実装内残存：なし
- `git diff --check`：成功

---

## 2026-08-16：必須事後条件を受け取らない別processファイル観察

### 今回閉じた問題

- 署名済み観察証拠の作成関数へ実測値を渡せても、対象を自ら測定するobserver-side processがなかった問題
- `target_id`だけでは、対象内部のどのresourceを測定した値かをauthorizationと観察証拠へ固定できなかった問題
- execution用の観察requestにreplay拒否とpath traversal拒否を結合した具体domain実装がなかった問題

### 追加した実装

- authorizationへ`postcondition_subject`、観察証拠へ`observation_subject`を追加
- subject追加に伴いexecution authorizationとreality observationの閉じた署名schemaを`1.2`へ更新
- 必須事後条件を含まず、試行、intent、対象、subject、field、nonce、時刻だけを持つ`execution-file-observation-request/1.0`
- repository root内の相対pathだけを受理し、`current_sha256`または`target_exists`を自ら測定するファイルdomain adapter
- root署名済みtrust bundle、trust checkpoint quorum、`OBSERVER_SIGNER` roleを通過した鍵だけで結果を署名する別process service
- request nonce・IDの永続消費と、署名結果のrequest ID、試行、intent、対象、subject、field、時刻への再照合

### この段階の境界

- 今回の回帰試験は一つのobserver processによる自律測定を確認した。二つの別process・別鍵による観察quorum実行は次段階で行う。
- file adapterは`current_sha256`と`target_exists`だけを扱う。他domainは同じrequest／署名境界を利用する個別adapterが必要である。
- 観察証拠はまだexecution journalの実在試行および署名済み必須事後条件とreconcileされない。`VERIFIED_RESOLVED`、`CONFLICT`、`UNVERIFIED`の永続記録と停止解除は未実装である。
- 低水準の観察署名関数はobserver-side integration用に残るが、runtimeのauthority経路は別processによる測定・signer admission・request再照合を必要とする。

### 検証結果

- safety kernelおよびtrusted runtime試験：107件成功
- NRA-IDE正典参照試験：38件成功
- 別processによるファイル内容の自律測定と署名：成功
- observation requestへの`required_postcondition_value`非混入：成功
- 署名証拠のsubject・field・試行・intent・対象への再照合：成功
- `git diff --check`：成功

---

## 2026-08-16：別鍵・別永続stateの2processファイル観察quorum

### 今回閉じた問題

- 一つのobserver processによる自律測定だけでは、一つの観察主体または一つの永続stateの故障を独立観察として扱えなかった問題
- 有効なobserver署名であっても、別のobservation requestへの応答をquorum候補へ混入できる余地
- 複数の署名数だけを数え、同じ現実を観察したかをauthority側で確認しない構成になる余地
- observation ID不一致のreason codeが`EXECUTION_OBSERVATION_OBSERVATION_ID_MISMATCH`と重複語になっていた問題

### 追加した実装

- 各署名応答を固有の`ExecutionFileObservationRequest`へ再照合してから既存のdistinct-principal判定へ渡す`assess_execution_file_observation_quorum()`
- 別のobserver ID、Ed25519鍵、ledger key、nonce DB、trust checkpoint DBを持つ二つのservice processによる同一fileの自律測定
- 二つのprocessが同じ試行、intent、対象、subject、field、実測値に一致した場合だけ成立するfile observation quorum
- 正しい署名でも別requestに対応する応答の拒否と、process間でfile内容が変化した場合の`EXECUTION_OBSERVATION_QUORUM_CONFLICT`
- observation ID不一致reason codeを`EXECUTION_OBSERVATION_ID_MISMATCH`へ正規化

### この段階の境界

- 二つのprocessは別鍵と別永続stateを使用するが、同じhost、repository root、trust bundle、pinned rootを使用する回帰試験である。hostまたはstorageの共通原因故障までは独立化していない。
- processの起動とrequest配送は呼び出し側が担う。quorum関数はprocessの配置を推測せず、署名済みprincipal、request結合、観察内容だけを判定する。
- file observation quorumはまだexecution journalの実在するattemptおよびauthorizationの必須事後条件とreconcileされない。したがって`COMPLETED_UNVERIFIED`の停止状態は解除されない。
- 次段階では、quorumをexecution journalのattempt、intent、target、postcondition subject・fieldへ照合し、一致、観察不一致、証拠不足をそれぞれ永続記録するreconcilerを追加する。

### 検証結果

- safety kernelおよびtrusted runtime試験：107件成功
- NRA-IDE正典参照試験：38件成功
- 別鍵・別ledger key・別nonce DB・別trust checkpoint DBの二つのservice processによる一致quorum：成功
- 別request応答の混入、同一request replay、process間の実測値不一致、path traversalの拒否：成功
- `git diff --check`：成功

---

## 2026-08-16：execution journal事後条件reconciler

### 今回閉じた問題

- execution journalがattempt、intent、target、actionだけを保持し、認可済み必須事後条件を後続の観察結果へ照合できなかった問題
- file observation quorumが成立しても、実在する`EXECUTOR_RETURNED` attemptとの対応および停止解除状態を永続化する経路がなかった問題
- 観察一致、観察不一致、証拠不足を区別せず、いずれも未検証のままにするしかなかった問題
- 後段が公開された`Verified` dataclassだけを受け取ると、署名検証を経ず型名だけを信頼する境界へ戻り得る問題

### 追加した実装

- execution prepareと同じtransactionで、authorization payload digest、authorizer principal、postcondition subject・field、必須値SHA-256を固定するappend-only `execution_postcondition_binding`
- requestへ再照合済みの署名観察quorumを再検証し、journal上のattempt bindingと比較する`reconcile_execution_file_observations()`
- reconciliation結果、証拠digest、observer principal、観察値SHA-256をHMAC chainへ追加するappend-only `execution_reconciliation`
- `VERIFIED_RESOLVED`、`CONFLICT`、`EVIDENCE_INSUFFICIENT`の分離と、`VERIFIED_RESOLVED`だけによる次のexecution解放
- 証拠不足後の再照合、resolvedまたはconflict後のterminal化、別attempt証拠による対象attempt汚染の拒否
- policy設定不備または壊れた入力を証拠不足として記録せず、`EXECUTION_RECONCILIATION_EVIDENCE_INVALID`として拒否する境界

### この段階の境界

- 必須事後条件と観察値はjournalへ平文保存せずSHA-256で結合する。値空間が小さい場合の辞書推測耐性は提供しないため、秘密値保存機構としては扱わない。
- `CONFLICT`はterminalかつ未解決であり、自動的に安全・失敗のどちらへも分類しない。解除には将来の別権限手続が必要である。
- `EVIDENCE_INSUFFICIENT`は未解決のまま追加証拠による再照合を許す。入力不備・policy不備はこれと区別して永続記録しない。
- 今回のreconcilerはfile observation domainだけを扱う。他domainは同じjournal bindingへ接続する個別の署名済み観察adapterが必要である。
- journal DB、HMAC鍵、観察trust rootを同一管理者が同時置換できる配置では独立保証にならない。配置上の分離は引き続き外部要件である。

### 検証結果

- safety kernelおよびtrusted runtime試験：108件成功
- NRA-IDE正典参照試験：38件成功
- 一致quorumによる`VERIFIED_RESOLVED`と次executionの解放：成功
- 証拠不足の永続化、停止維持、追加証拠による再照合：成功
- 観察不一致の`CONFLICT`固定、別attempt証拠の拒否、terminal後の再記録拒否：成功
- bindingおよびreconciliation HMAC chainの再検証：成功
- `git diff --check`：成功

---

## 2026-08-16：execution authority domain配置契約

### 今回閉じた問題

- execution journal DB、journal HMAC鍵、observer trust rootの管理権限が同じ場合、DBと検証根拠を同時置換でき、reconciliation記録が独立保証にならない問題
- 既存の`RuntimePlacement`がpath分離だけを扱い、execution関連資産の管理authority重複を表現・拒否できなかった問題
- pathが異なることと、管理者またはOS identityが異なることを混同する余地

### 追加した実装

- `RuntimePlacement`へexecution journal管理domain、integrity key管理domain、複数observer trust-root管理domainを追加
- journal管理とkey管理の同一domain、これらとobserver trust-root管理domainの交差、observer root管理domain不足、宣言欠落の決定論的拒否
- execution authorization DBを使用するruntime admissionへauthority domain分離判定を接続
- path分離、authority domain宣言分離、OS identity証明、authority domain実在証明を別のassessment fieldとして保持
- authority domainが宣言上分離されても、外部証明がなければ`AUTHORITY_DOMAIN_SEPARATION_NOT_ATTESTED`を残す契約

### この段階の境界

- 今回検証するのは配置manifest上のauthority domain IDの欠落・重複・交差である。異なるID文字列が実際に異なる管理者、OS account、security domainを表すことは証明しない。
- `execution_authority_domains_separated=True`は宣言構造の合格であり、`authority_domain_separation_verified`は引き続き`False`である。
- 実在する管理権限分離を固定するには、authority manifestをruntime外部の複数principalが署名し、pinned policyに対して検証するattestation経路が必要である。
- 単一host上でrootまたは同等の全権限主体が全path、key、processを置換できる場合、この宣言契約だけでは防げない。

### 検証結果

- safety kernelおよびtrusted runtime試験：109件成功
- NRA-IDE正典参照試験：38件成功
- journalとHMAC鍵の同一管理domain拒否：成功
- journal・HMAC鍵とobserver trust-root管理domainの交差拒否：成功
- authority宣言欠落、observer root管理domain不足の拒否：成功
- 分離宣言がある既存execution runtimeのadmissionおよび実行回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：署名済みexecution authority manifest attestation

### 今回閉じた問題

- authority domain IDが異なっていても、誰がその配置宣言を承認したかを暗号学的に確認できなかった問題
- execution journal pathまたはauthority domain宣言を変更しても、同じ外部署名証拠を再利用できる余地
- runtime admissionとlauncherがauthority manifest証拠を必須入力として扱っていなかった問題

### 追加した実装

- trust bundleへ専用`AUTHORITY_ATTESTER` roleを追加
- execution journalの解決path、journal管理domain、integrity key管理domain、observer trust-root管理domain集合を閉じたschemaでSHA-256固定するauthority placement digest
- manifest ID、placement digest、有効期間を署名する`execution-authority-manifest-attestation/1.0`
- pinned-root検証済みtrust bundle上のrole、有効鍵、署名、期限、配置digest一致、distinct principalを確認するauthority manifest quorum
- execution DBを使用するmanual admissionおよびlauncherで、2-principal以上のauthority manifest evidenceを必須化
- quorum成功後だけ`authority_domain_separation_verified=True`へ昇格し、`AUTHORITY_DOMAIN_SEPARATION_NOT_ATTESTED`をassessmentから除く状態遷移

### この段階の境界

- verifiedが意味するのは、pinned-root検証済みtrust bundleに登録された異なる署名principalが同じ配置digestを承認したことまでである。
- 単一のpinned root管理者がtrust bundleのattester membership、全attester秘密鍵、配置資産を同時に置換できる場合、組織的または物理的な独立性は成立しない。
- manifest attester processのOS identity、host、秘密鍵保管場所は今回の署名検証だけでは観察しない。
- 次段階では、単一rootによるattester集合の置換を防ぐため、複数の独立pinned policy rootまたはthreshold root policyへauthority manifest policyを固定する必要がある。

### 検証結果

- safety kernelおよびtrusted runtime試験：110件成功
- NRA-IDE正典参照試験：38件成功
- 異なる2 principalによる一致manifest quorumとadmission verified昇格：成功
- 同一principal重複、manifest証拠欠落、配置domain変更後の旧証拠再利用の拒否：成功
- manual admissionとlauncherの双方でauthority manifest必須化：成功
- `git diff --check`：成功

---

## 2026-08-17：trust bundle threshold root policy endorsement

### 今回閉じた問題

- primary offline root一つの署名だけでtrust bundle内の`AUTHORITY_ATTESTER`集合を差し替えられた問題
- authority manifest署名が複数principalでも、そのprincipal membershipを決めるtrust bundle自体を単一rootが置換できた問題
- primary rootとpolicy rootに同じ公開鍵を流用し、見かけ上のthresholdを作れる余地

### 追加した実装

- trust bundle外で直接pinする`PinnedPolicyRoot`のkey ID、principal ID、Ed25519公開鍵契約
- policy ID、policy-root principal、trust bundle generation・完全なsigned bundle SHA-256、有効期間を署名する`trust-bundle-root-policy-endorsement/1.0`
- primary root公開鍵とのfingerprint重複、policy root間の公開鍵・principal重複を拒否するroot set検証
- 同一bundle generation・SHA-256・policy ID・有効期限に一致するdistinct policy principalだけを数えるthreshold quorum
- execution DBを使用するmanual admissionとlauncherで、authority manifest検証より前にroot-policy thresholdを必須化

### この段階の境界

- primary root単独では、新しいtrust bundle hashに必要なpolicy-root endorsement quorumを作れない。ただしpolicy root秘密鍵まで同じ主体が保有する配置では独立性は成立しない。
- pinned policy root mappingは今回runtimeへ直接注入する。OS権限、別host、HSM、秘密鍵保管場所の分離は検証しない。
- endorsementはbundle hashと有効期間へ結合されるが、過去に有効だったendorsementとbundleへのrollbackを永続stateで拒否するroot-policy checkpointはまだない。
- policy root集合のrotation、失効、緊急復旧は未実装である。単純にthresholdを下げることを復旧手段としてはならない。
- 次段階では、受理済みpolicy ID、bundle generation・hash、endorsement principal集合をappend-onlyかつ外部witnessされたcheckpointへ固定する必要がある。

### 検証結果

- safety kernelおよびtrusted runtime試験：111件成功
- NRA-IDE正典参照試験：38件成功
- 異なる二つのpinned policy rootによるtrust bundle endorsement quorum：成功
- 同一principal重複、primary root鍵流用、別bundle hashへの旧endorsement再利用の拒否：成功
- root-policy evidence欠落時のauthority manifest検証前fail-closed：成功
- manual admissionとlauncherの既存実行回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：root policy単調checkpointとpolicy-root witness state

### 今回閉じた問題

- 過去に有効だったroot-policy endorsementとtrust bundleを、runtime再起動後にrollbackして再受理できた問題
- runtime側が受理済みpolicy ID、bundle generation・hash、endorsement principal集合を永続化していなかった問題
- policy rootが、既に新世代へendorseした後でも旧世代へ再署名できた問題

### 追加した実装

- 受理済みpolicy ID、trust bundle generation・完全なsigned bundle SHA-256、previous bundle SHA-256、distinct endorsement principal集合を保持するappend-only `RootPolicyCheckpointStore`
- 初期世代、連続世代、previous digest一致を要求し、rollback、世代飛び、同世代競合を拒否する単調遷移契約
- 各pinned policy rootが自身の別SQLite stateで最後に確認したbundle headを保持し、単調性確認後だけendorsementを発行する`RootPolicyWitnessStateStore`
- policy-root witnessが発行した署名endorsement自体をappend-only表へ保存し、同一ID・同一内容の再試行だけを冪等受理する記録契約
- execution DBを使う配置でroot-policy checkpoint pathを必須化し、manual admissionとlauncherがauthority manifest検証前にthreshold quorumと単調checkpointを通す実行順序

### この段階の境界

- runtime checkpointとpolicy-root witness stateはSQLiteのappend-only triggerとtransactionで通常の更新・削除、並行書込み、途中失敗を拒否するが、DB file自体の置換を暗号学的には防がない。
- 回帰試験では二つのpolicy rootが別DBを所有する構成を再現した。実環境で別OS identity、別host、HSM、別管理者に分離されていることをruntimeが証明する機構は未実装である。
- 同一管理者がruntime checkpoint DB、全policy-root witness DB、全policy-root秘密鍵を同時に置換できる配置ではrollback耐性は成立しない。
- policy root集合のrotation、失効、緊急復旧、外部timestampまたは透明性logへのanchorは未実装である。
- 次段階では、policy-root witness serviceの配置・管理authorityを署名manifestへ固定するか、checkpoint headを別管理主体の外部anchorへ複製し、DB置換を観察可能にする必要がある。

### 検証結果

- safety kernelおよびtrusted runtime試験：112件成功
- NRA-IDE正典参照試験：38件成功
- root-policy checkpointのgeneration 1から2への連続前進と同一head冪等受理：成功
- runtime checkpointによる旧bundle rollback、世代飛び、同世代競合、previous digest不一致の拒否契約：実装
- 二つのpolicy-root witness stateによる新世代endorsement後の旧世代再署名拒否：成功
- manual admission、launcher、execution authority配置分離の既存回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：起動challenge結合online policy-root witness

### 今回閉じた問題

- runtime checkpoint DBと古いtrust bundleを戻した際、まだ有効期間内の旧root-policy endorsementを再利用できる短時間rollback余地
- launcherが起動challenge生成前に作られた静的root-policy endorsementを受け取っていたため、当該起動へのonline policy-root参加を証明できなかった問題
- policy-root witnessを別processとして起動する実行経路と、起動時に必要なprocess quorum構成がなかった問題

### 追加した実装

- admission challenge、policy ID、policy-root principal、trust bundle generation・完全なsigned bundle SHA-256、有効期間を署名する`trust-bundle-root-policy-endorsement/1.1`
- runtime admissionが現在の`BoundaryAdmissionChallenge`と全endorsementのchallenge完全一致を要求する検証
- primary pinned rootでtrust bundleを検証し、policy-root自身の単調state確認後だけendorsementを返す別process `root_policy_witness_service`
- launcherがchallenge生成後に各`RootPolicyWitnessProcess`へ同一requestを送り、distinct pinned policy-root principalのthreshold responseを収集するonline経路
- policy-root witnessの秘密鍵pathとstate DB pathを他のruntime service資産と重複させず、repository外へ置くlauncher配置検証
- 旧静的`launch_boundary_runtime(... signed_root_policy_endorsements=...)`入力を廃止し、online process集合・policy ID・timeoutを必須入力へ置換

### この段階の境界

- challenge不一致の旧endorsement再利用は拒否できるが、同一管理者が全policy-root witness DB、全policy-root秘密鍵、launcher processを同時に置換できる配置では独立性は成立しない。
- 別processであることは確認できるが、別OS identity、別host、HSM、別管理者であることは署名済み配置manifestとしてまだ証明しない。
- policy-root serviceの一つが停止してthreshold未満になると起動を拒否する。これはfail-closed動作であり、自動的なthreshold引下げや旧endorsement fallbackは行わない。
- 各serviceの時刻は同一である必要はなく、署名鮮度と`valid_until`を個別検証する。外部時刻源へのanchorは未実装である。
- policy root集合のrotation、失効、緊急復旧は未実装である。
- 次段階では、policy-root witness serviceのOS identity・host・鍵保管・DB管理authorityを署名済みdeployment manifestへ固定し、実在する管理分離とruntime設定を照合する必要がある。

### 検証結果

- safety kernelおよびtrusted runtime試験：113件成功
- NRA-IDE正典参照試験：38件成功
- 旧challengeに結合された有効期限内endorsementの新challengeへの再利用拒否：成功
- 二つの別process policy-root witnessによるlauncher admission：成功
- online policy-root processが一つだけのquorum不足起動拒否：成功
- launcher複数回起動、部分失敗後再試行、execution journal再開の既存回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：署名済みpolicy-root witness deployment manifest

### 今回閉じた問題

- online policy-root witnessのkey IDとprincipalだけが固定され、host、OS identity、秘密鍵path、state DB path、各管理authorityの変更を検出できなかった問題
- policy-root witness間で同じhost・OS identity・鍵管理domain・state管理domainを宣言でき、見かけ上の複数processを作れた問題
- execution journal・integrity key・observer rootの管理domainとpolicy-root witness管理domainを重ねられた問題

### 追加した実装

- policy-root key ID、principal ID、解決済み秘密鍵path・DB path、host identity、OS identity、鍵管理domain、state管理domain、service moduleを閉じたschemaで固定する`policy-witness-deployment/1.0`
- deployment全体のSHA-256、manifest ID、有効期間をtrust bundleの`AUTHORITY_ATTESTER` roleで署名する`policy-witness-deployment-attestation/1.0`
- 異なる二principal以上の署名、同一manifest ID・deployment digest、署名鮮度、個別有効期限を要求するdeployment quorum
- policy-root witness集合内のkey、principal、host、OS identity、鍵管理domain、state管理domain、秘密鍵path、DB pathの重複拒否
- policy-root witnessの鍵・state管理domainとexecution journal、integrity key、observer trust-root管理domainとの交差拒否
- launcherがonline policy-root processを呼ぶ前に、実際のprocess設定と署名済みdeployment digestを照合する起動順序

### この段階の境界

- manifestが証明するのは、pinned-root検証済みtrust bundle上の複数`AUTHORITY_ATTESTER` principalが同じ宣言配置を承認したことまでである。
- host identityとOS identityは署名対象として固定されるが、OSまたはhardwareから測定した値ではない。異なる文字列が実在する別host・別accountを表すことは、このPoC単独では証明しない。
- `AUTHORITY_ATTESTER` membershipはroot-policy endorsement対象のtrust bundleへ結合されるが、attester、全policy-root、全配置資産を同一管理者が同時に支配する場合は独立性が成立しない。
- TPM、secure boot、remote attestation、HSM key residency、OS file owner・ACLの観察は未実装である。
- policy root集合のrotation、失効、緊急復旧も未実装である。
- 次段階では、宣言されたhost・OS identity・鍵保管を外部観察値と照合するdeployment evidence契約へ進むか、先にpolicy-root rotationとrecoveryの単調policyを固定する必要がある。

### 検証結果

- safety kernelおよびtrusted runtime試験：115件成功
- NRA-IDE正典参照試験：38件成功
- 未改変の二policy-root process deployment manifestによるlauncher起動：成功
- 署名後のhost identity変更によるdeployment digest不一致拒否：成功
- policy-root鍵管理domainとexecution journal管理domainの交差拒否：成功
- online quorum不足、challenge再利用拒否、rollback拒否、execution runtimeの既存回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：policy-root設定commitmentと無断rotation拒否

### 今回閉じた問題

- trust bundle generationとbundle SHA-256は固定されていても、runtimeへ注入するpinned policy-root集合と必要principal数を世代間で差し替えられた問題
- policy-root endorsement、各policy-root witnessの単調state、runtime checkpointのいずれにも、実際に使用したroot設定全体が保存されていなかった問題
- policy-rootを置換するか必要票数を下げることで、過去と異なる承認条件を通常のbundle更新として受理できる余地

### 追加した実装

- policy ID、必要principal数、key ID・principal ID・Ed25519公開鍵fingerprintの正規化root集合を`root-policy-configuration/1.0`としてSHA-256へ固定する設定commitment
- 設定SHA-256を起動requestと各policy-root署名へ含める`root-policy-witness-request/1.1`および`trust-bundle-root-policy-endorsement/1.2`
- runtimeが現在のpinned root集合と閾値から設定SHA-256を再計算し、署名値との不一致を`ROOT_POLICY_CONFIGURATION_MISMATCH`としてquorumから除外する検証
- 各policy-root witness stateとruntime checkpointへ設定SHA-256をappend-only保存し、次世代で異なる設定を`*_CONFIGURATION_CHANGE_NOT_AUTHORIZED`として拒否する単調遷移
- 同じroot公開鍵のmapping順序には依存せず、key ID、principal ID、公開鍵fingerprint、必要票数、policy IDのいずれかが変われば別設定として扱う閉じた契約

### この段階の境界

- 今回は無断rotationを閉じただけであり、正当なpolicy-root追加、置換、失効、閾値変更、緊急復旧を承認するrotation protocolは未実装である。
- 正式なrotationを実装するまでは、設定変更はpolicy-root witnessとruntime checkpointの双方でfail-closedになる。鍵喪失時に自動で閾値を下げるfallbackは設けない。
- 旧設定だけ、または新設定だけによる一段階置換では、侵害済み旧rootによる乗っ取り、あるいは自己承認された新rootへの飛越しを防げない。次段階では旧設定quorumと新設定quorumを別々に満たす二重承認と、直前設定digestへのchain結合が必要である。
- SQLite表へ設定SHA-256列を追加した。旧PoC schemaの既存DBを暗黙に移行せず、列が存在しないstateはfail-closedになるため、実配置では監査可能な明示migration手順が別途必要である。
- 設定commitmentは宣言内容の同一性を固定するが、host、OS identity、HSM residency、管理主体の実在性を測定するものではない。

### 検証結果

- safety kernelおよびtrusted runtime試験：115件成功
- NRA-IDE正典参照試験：38件成功
- 正しい設定SHA-256へ結合された二policy-root endorsement quorum：成功
- 同じ署名鍵による別設定SHA-256 endorsementのquorum除外：成功
- policy-root witnessによる次世代の無断設定変更拒否：成功
- runtime checkpointによる次世代の無断設定変更拒否後、元設定による正常な世代更新：成功
- launcher subprocess、online quorum、rollback、execution runtimeの既存回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：旧・新policy-root二重quorumによるrotation証明

### 今回閉じた問題

- policy-root設定変更を全面拒否すると無断置換は防げる一方、正当なroot追加・置換を表現する検証可能な承認経路がなかった問題
- 新設定rootだけが自分自身を承認し、旧設定の継続性を失ったままrotationを成立させる余地
- rotation承認が対象bundle generation・完全なsigned bundle SHA-256・起動challengeへ結合されていない場合、別世代や別起動へ流用できる問題

### 追加した実装

- rotation ID、policy ID、直前・次設定SHA-256、対象bundle generation・SHA-256、admission challenge、有効期間、承認側`PREVIOUS`または`NEXT`を署名する`root-policy-rotation-approval/1.0`
- 旧設定rootと新設定rootを別々に検証し、それぞれが自身の必要principal数を満たした場合だけ成立する`RootPolicyRotationQuorum`
- 同じkey IDが旧・新設定で異なるprincipalまたは異なる公開鍵を指す曖昧なrotation設定の拒否
- `RootPolicyCheckpointStore.accept(..., rotation=...)`が、保存済み直前設定、次のroot-policy quorum、対象bundleとrotation証明の完全一致時だけ設定変更を受理する契約
- rotation証明がない場合、新設定側だけのquorumが成立していても従来どおり`ROOT_POLICY_CONFIGURATION_CHANGE_NOT_AUTHORIZED`を返す互換的fail-closed

### この段階の境界

- 今回実装したのは署名済みrotation証明の生成・検証とruntime checkpointへの適用までである。launcherからのonline収集、旧policy-root witnessによるrotation承認発行、新policy-root witnessの初期state bootstrapはまだ接続していない。
- 新policy-root witnessを対象世代から開始させるには、成立済みrotation証明、直前bundle digest、直前設定digest、新設定での当該principal membershipを同一transactionで検証・保存する専用bootstrapが必要である。通常の初期generation規則を緩めて代用してはならない。
- 旧設定と新設定に残る同一principalは各側のquorumへ一回ずつ算入できる。これは設定継続主体として許容するが、各設定内で同一principalの重複算入は引き続き禁止する。
- rotation証明の有効期限と署名鮮度は検証するが、外部時刻源、失効通知、緊急復旧、複数rotationの競合解決は未実装である。
- 次段階では、policy-root witness stateへrotation approval記録と専用bootstrapを追加し、途中失敗時に旧設定を維持したまま再試行できる原子的なonline遷移へ接続する。

### 検証結果

- safety kernelおよびtrusted runtime試験：116件成功
- NRA-IDE正典参照試験：38件成功
- 旧設定二principalと新設定二principalの両quorumによるrotation証明：成功
- 新設定側approvalだけを与えた場合の旧設定quorum不足拒否：成功
- rotation証明なしのcheckpoint設定変更拒否：成功
- 同じ変更への完全一致rotation証明付与後のcheckpoint世代更新：成功
- 既存の無断設定変更、rollback、online witness、launcher、execution runtime回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：rotation署名原本再検証と新policy-root witness bootstrap

### 今回閉じた問題

- 公開dataclassの`RootPolicyRotationQuorum`を`satisfied=True`で直接構築すれば、署名approvalを検証せずcheckpointへrotation済みとして渡せた問題
- 新policy-root witnessは空のstate DBを持つため、通常のgeneration 1初期化規則を維持したままrotation対象世代から参加する方法がなかった問題
- bootstrap途中で鍵不一致やendorsement生成失敗が起きた場合、rotation記録・witness state・署名記録の一部だけが残る危険

### 追加した実装

- 署名approval原本、rotation ID、policy ID、旧新root集合・各閾値、primary root集合、admission challenge、署名鮮度を保持する`RootPolicyRotationEvidence`
- checkpoint設定変更時に公開quorum型を信用せず、`RootPolicyRotationEvidence`の署名原本から旧新quorumを再評価する適用側検証
- 新witness自身のkey ID、principal ID、公開鍵fingerprintがcommit済み新root集合の構成員であることを再計算してから対象世代を初期化する`RootPolicyWitnessStateStore.bootstrap_rotation()`
- rotation記録、対象世代witness state、最初のsigned endorsementを単一`BEGIN IMMEDIATE` transactionで保存し、いずれかの失敗時は全体をrollbackする原子的bootstrap
- append-only rotation表へrotation ID、旧新configuration SHA-256、直前bundle SHA-256、対象generation・bundle SHA-256、署名approval集合SHA-256を保存する監査契約
- 既存stateを持つwitnessへのbootstrap再実行を`ROOT_POLICY_WITNESS_BOOTSTRAP_NOT_EMPTY`として拒否する一回限りの初期化境界

### この段階の境界

- checkpointと新witness bootstrapは署名原本を再検証する。`RootPolicyRotationQuorum`という型名や`satisfied`値だけではauthorityにならない。
- bootstrapは新規かつ空のpolicy-root witness DB専用である。旧設定から新設定にも残るretained witnessが既存stateをrotation更新する経路はまだ実装していない。
- `root_policy_witness_service`とlauncherは通常endorsement requestだけを扱い、rotation approval収集、raw evidence配布、bootstrap起動をまだ行わない。
- bootstrap transactionはSQLite file内部の部分書込みをrollbackするが、DB file全置換、host喪失、鍵保管主体の偽装を防ぐものではない。
- 次段階ではretained witnessの既存stateを同じraw evidence再検証後に更新し、その後に新witness bootstrap、全新設定endorsement収集、runtime checkpoint更新を行うonline順序へ接続する。

### 検証結果

- safety kernelおよびtrusted runtime試験：116件成功
- NRA-IDE正典参照試験：38件成功
- 旧設定approvalを欠くraw evidenceのcheckpoint拒否：成功
- 完全な旧新approval原本再検証後のcheckpoint rotation受理：成功
- 新rootに対応しない秘密鍵でのbootstrap失敗と全書込みrollback：成功
- rollback後の正しい鍵による再試行、rotation記録・state・endorsementの一括保存：成功
- bootstrap済みDBへの二重bootstrap拒否：成功
- bootstrap endorsementを含む新設定二principal quorum：成功
- 既存rollback、online witness、launcher、execution runtime回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：retained policy-root witnessの原子的rotation更新

### 今回閉じた問題

- 旧設定から新設定にも残るpolicy-root witnessが既存の単調stateを保持したままconfiguration変更へ進む経路がなかった問題
- 新規witness用bootstrapを既存stateへ流用すると、直前headとの連続性確認を省略できる問題
- rotation途中の署名失敗で、rotation記録または新世代stateだけが残り、旧設定へ戻れず新設定quorumも作れない部分遷移の危険
- 旧設定から削除されるrootがretained経路を使って新設定endorsementを発行する余地

### 追加した実装

- raw `RootPolicyRotationEvidence`から旧新quorumを再検証し、root自身が旧設定と新設定の双方へ同じkey ID・principal ID・公開鍵fingerprintで所属することを要求する`RootPolicyWitnessStateStore.rotate_retained()`
- witness DBの最新generationが対象generationの直前、最新bundle SHA-256がtarget bundleのprevious SHA-256、最新policy ID・configuration SHA-256がrotationの旧設定と一致することをtransaction内で確認する連続性契約
- rotation監査行、新世代witness state、新設定endorsementを単一`BEGIN IMMEDIATE` transactionでappendし、署名鍵不一致を含む途中失敗時に全体をrollbackする更新順序
- bootstrapとretained更新で同じrotation監査行生成処理を共有し、直前bundle・旧新configuration・対象bundle・approval集合digestの記録差を防ぐ実装
- 旧設定にのみ存在する削除対象rootのretained rotation拒否

### この段階の境界

- retained更新は同一policy-root witness DB内で原子的だが、複数witness DB、新witness bootstrap、runtime checkpointを跨ぐ分散transactionではない。各主体の途中状態を観察して再試行するorchestrationが必要である。
- retained witnessは旧新両設定の署名approval原本を再検証する。launcherまたはserviceから`satisfied=True`の型だけを渡して更新する経路は設けない。
- 削除対象rootは旧設定側のrotation approvalを発行できるが、新設定endorsementは発行できない。追加rootは専用bootstrapだけを使用する。
- `root_policy_witness_service`のrequest schemaとlauncherはまだ通常endorsement専用であり、rotation approval発行・retained更新・bootstrapをonline実行しない。
- 次段階では、online rotationを一つの不可分処理と偽装せず、旧approval収集、新approval収集、retained更新、新witness bootstrap、新設定endorsement quorum、runtime checkpointの各観察可能な段階として実装する。

### 検証結果

- safety kernelおよびtrusted runtime試験：116件成功
- NRA-IDE正典参照試験：38件成功
- retained rootのgeneration 1旧設定stateからgeneration 2新設定stateへの連続更新：成功
- 誤った秘密鍵による更新失敗と、全書込みrollback後の正しい再試行：成功
- 旧設定から削除されるrootのretained更新拒否：成功
- retained root endorsementと新root bootstrap endorsementによる新設定二principal quorum：成功
- rotation証明なしの変更、旧approval不足、rollback、launcher、execution runtime回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：別process policy-root rotation approval発行

### 今回閉じた問題

- rotation approvalを試験内の秘密鍵から直接生成しており、実配置のpolicy-root witness processへonline要求する経路がなかった問題
- 通常のbundle endorsement requestとrotation approval requestを同じfield集合で扱うと、操作目的やstate変更の有無を取り違える危険
- 旧設定stateを持たないrootが`PREVIOUS` approvalを発行する余地
- retained rootが保存済み直前headと異なる旧configurationまたは別previous bundleを承認する余地
- 発行済みapprovalの要求bindingを変えて同じrotation ID・approval sideを再利用する競合

### 追加した実装

- 通常`root-policy-witness-request/1.1`と完全に分離した閉じた`root-policy-rotation-approval-request/1.0` decoder
- rotation ID、`PREVIOUS`または`NEXT`、policy ID、旧新configuration SHA-256、対象signed trust bundle、admission challengeを別process serviceへ渡すapproval発行経路
- `PREVIOUS`ではpolicy-root witness DBに直前generation・previous bundle SHA-256・policy ID・旧configuration SHA-256の一致するstateが存在することを必須化
- `NEXT`では新rootの空DBを許す一方、既存stateを持つretained rootでは同じ直前head一致を要求するstate-bound approval契約
- 発行したsigned approvalと全要求bindingを`root_policy_rotation_approval` append-only表へ保存し、同一bindingの再試行だけ既存署名を返し、異なるbindingを競合拒否する記録
- 通常endorsement schemaへrotation fieldを混在させるrequest、およびrotation schemaへ未定義fieldを追加するrequestの厳密拒否

### この段階の境界

- serviceはrotation approvalを発行・記録するが、retained state更新、新root bootstrap、新設定endorsement発行はこのrequestでは行わない。approval収集とstate遷移は意図的に別段階である。
- 新rootの空DBによる`NEXT` approvalは、そのrootが最終的な新設定構成員であることをservice単独では判定しない。全approval収集後の`assess_root_policy_rotation_quorum()`がcommit済み新root集合とのmembershipを検証する。
- approval発行を依頼できる主体のOS認証・対話的管理者承認はCLI起動境界の外側であり、このPoCは秘密鍵fileへのアクセス権限を超えるoperator identityを証明しない。
- launcherはまだrotation requestを生成・収集しない。通常起動経路は従来のbundle endorsementだけを使用する。
- 次段階ではlauncherとは別のrotation orchestrator候補を作り、旧approval quorum成立を確認してから新approval quorumを収集し、raw evidenceをretained更新・bootstrapへ渡す段階順序を実装する。

### 検証結果

- safety kernelおよびtrusted runtime試験：117件成功
- NRA-IDE正典参照試験：38件成功
- stateを持つretained policy-root Bの別process `PREVIOUS`・`NEXT` approval発行：成功
- 別process approvalと直接独立root approvalを合わせた旧新二principal rotation quorum：成功
- 保存済み旧configurationと異なる`PREVIOUS` request拒否：成功
- rotation schemaへの通常endorsement field混在拒否：成功
- 通常launcherのgenesis・複数head起動回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：旧quorum先行のonline rotation evidence収集

### 今回閉じた問題

- 旧設定の承認が不足したまま新policy-root processを呼び出すと、rotationが旧側で成立しないのに新側DBへapproval記録だけが作られる問題
- 旧側と新側のapprovalを一括収集すると、どの時点で旧authorityがrotation開始を認めたかという段階境界が消える問題
- processへ設定された秘密鍵が親側でpinしたpolicy-root公開鍵と異なる場合、無効署名を親側が後から拒否できても、witness DBへその無効approvalが先に保存される可用性上の汚染
- rotation evidence収集とwitness state更新を同一操作にすると、承認の成立確認前に現実状態を変更する危険

### 追加した実装

- 通常runtime launcherと分離した`collect_root_policy_rotation_evidence()`を追加し、対象signed trust bundleをprimary rootから再検証してからapproval収集を開始する経路
- 旧process集合から`PREVIOUS` approvalを収集し、署名・旧新configuration・対象bundle・challenge・旧root membershipを検証して旧principal閾値を満たした場合だけ、新process集合へ`NEXT` requestを送る段階gate
- 旧側と新側のprocess集合が各policy-root構成の全key IDに一致し、process内identity・authority domain・DB/key path分離を満たすことの事前確認
- 旧新quorum成立後にだけ、署名原本と検証入力を保持する`RootPolicyRotationEvidence`を返し、この関数内ではretained更新・新root bootstrap・checkpoint更新を行わない収集専用契約
- 親側でpinしたpolicy-root公開鍵fingerprintを別process serviceへ渡し、秘密鍵から導出したfingerprintが一致しなければwitness DBを開く前に拒否する鍵binding
- 個別process失敗を成功扱いせず、得られた署名だけを検証して定足数不足として閉じる収集動作

### この段階の境界

- 旧quorum成立は新側process呼出しの必要条件であり、rotation完了やstate更新成功を意味しない。返却値は次段階へ渡す検証可能なapproval原本である。
- 新側approval収集後に一部processが失敗した場合、既に成功した新側DBにはapproval記録が残り得る。approvalはstate遷移ではなく、同一bindingの再試行で再利用できるappend-only記録として扱う。
- process集合は構造とpolicy-root membershipを検証するが、旧・新deployment manifestの独立attester署名をこのorchestratorへまだ入力していない。
- 複数witness DBを跨ぐ分散transactionは作らない。retained更新、新root bootstrap、新設定endorsement quorum、runtime checkpointは、観察可能で再試行可能な別段階として未接続である。
- 次段階ではraw evidenceを使うstate適用orchestrator候補を作り、各witnessの適用結果を独立に再観察してから新設定endorsement quorumとcheckpointへ進む再開可能な順序を検討する。

### 検証結果

- safety kernelおよびtrusted runtime試験：118件成功
- NRA-IDE正典参照試験：38件成功
- 旧側二processのうち一つがpin済み公開鍵と異なる秘密鍵を持つ場合の旧quorum不足拒否：成功
- 旧quorum不足時に新root CのDBが作成されないこと：成功
- 誤鍵process拒否後、同じ既存B witness DBを正しい鍵で再試行できること：成功
- 旧A・retained Bの`PREVIOUS` quorum成立後にだけretained B・新Cの`NEXT`収集へ進み、合計四署名の旧新quorumが成立すること：成功
- 通常launcher、既存rotation service、rollback、execution runtime回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：trusted_runtime全体精査とfail-closed整合性監査

### 今回閉じた問題

- `boundary_runtime_launcher.py`の`_validate_checkpoint_signer_placement()`が、witness用state DB群（trust checkpoint DB、latch/nonce/anchor/root-policy checkpoint DB、全latch witnessおよび全root-policy witnessのDB）のうち先頭1件（`state_paths[0]`）しかrepository外配置を検証しておらず、二つ目以降のwitness state DBをrepository内へ配置してもlauncherが受理してしまう問題。直前の`secret_paths`チェックは全件を`any(...)`で検査しているのに対し、`state_paths`側だけ検査漏れがあった
- `RootPolicyCheckpointStore.accept()`が、呼び出し側が構築した公開dataclass`RootPolicyQuorum`の`satisfied`値を信用するだけで、署名原本`signed_endorsements`を自身で再検証していなかった問題。同メソッドのrotation経路は2026-08-17の先行エントリで既に「型名や`satisfied`値だけをauthorityにしない」よう修正済みだったが、base（非rotation）quorum経路には同じ原則が未適用のまま残っていた

### 実施した修正

- `_validate_checkpoint_signer_placement()`のstate DB配置チェックを`any(_is_relative_to(path, repository_root) for path in state_paths)`へ修正し、`secret_paths`と同じパターンへ統一
- `RootPolicyCheckpointStore.accept()`のシグネチャを、事前構築済み`RootPolicyQuorum`ではなく生の`signed_endorsements`と検証入力（`pinned_policy_roots`・`primary_root_keys`・`admission_challenge`・`minimum_principals`・`signature_max_age`）を受け取る形へ変更し、内部で`assess_root_policy_quorum()`を呼んで自己完結的に再検証する構成へ統一。呼び出し元`boundary_runtime.py`と`test_latch_witness.py`内の全呼び出し（3箇所）を追随して更新

### 今回の精査で確認し、修正不要と判断した点

- `RootPolicyWitnessStateStore.bootstrap_rotation()`/`rotate_retained()`が本番経路（`root_policy_witness_service.py`・`root_policy_rotation_orchestrator.py`・`boundary_runtime_launcher.py`）から未接続である点は、rotation適用側・witness側の双方が独立に`ROOT_POLICY_CONFIGURATION_CHANGE_NOT_AUTHORIZED`系・`ROOT_POLICY_WITNESS_CONFIGURATION_CHANGE_NOT_AUTHORIZED`で拒否するため、暗黙のPERMITは発生しない。前段エントリが記述する意図的な段階分け（承認収集と適用を別段階にする）通りであることをコード追跡で確認した
- 上記2点以外の`trusted_runtime/`全36ファイルを対象に、broad except節・boolean条件の反転・quorum principal_id集計方式・fail-closed境界を横断的に再走査したが、新規のfail-closed違反（検証失敗を握り潰して継続する経路、既定PERMITへ落ちる分岐）は見つからなかった

### この段階の境界

- 今回の精査はコード読解と既存試験の実行によるものであり、形式検証やmodel checkingは行っていない
- `assess_latch_witness_quorum`の`expected_admission_challenge`省略時にreplay challenge bindingを省略できる余地は、現状唯一の呼び出し元（`boundary_runtime.py`）が必ず値を渡すため実害はないが、将来別の呼び出し元が追加される場合に備えた必須化（Noneを許さない）は未実施

### 検証結果

- safety kernelおよびtrusted runtime試験：120件成功（新規2件：`test_launcher_rejects_witness_state_database_inside_repository`、`test_root_policy_checkpoint_verifies_endorsements_itself`）
- NRA-IDE正典参照試験：38件成功
- 修正前コードへ一時的に戻した場合、`test_launcher_rejects_witness_state_database_inside_repository`が検知ゲートを素通りし別経路で失敗すること（回帰検知として機能することの確認）：成功
- 既存rotation・rollback・launcher・execution runtime回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：俯瞰監査によるsafety_kernel／trusted_runtime未接続の発見と部分是正

### 今回の俯瞰監査で判明した根幹の問題

- design文（`NRA-IDE_AI横軸機能_現実実装最適解_20260812-1934.md`）§18が主張する「δ/τ/R判定を行うHorizontal Safety Kernelが、その判定に基づいてCapability Proxyを完全仲介する」という一体構造が、実装には存在しなかった。`trusted_runtime.boundary_runtime.prepare_execution()`／`execute_authorized_action()`（実際に外部作用を許可・実行する唯一の経路）を全文精読した結果、`TargetBoundaryState`／`BoundaryAssessment`（軸判定結果）への参照が皆無であることを確認した。実行可否はEXECUTION_AUTHORIZER署名quorum・latch head一致・action digest一致のみで決まり、対象がRUPTURE_BOUNDARY（設計文の意味では「以後は証言のみ、作用禁止」）へ到達していても、署名さえ揃えば実行できてしまう状態だった
- `grep -rn "safety_kernel" trusted_runtime/*.py`で確認した結果、trusted_runtimeは`ShadowSafetyKernel`本体・不変条件（`FileChangePolicy`）・報告-現実照合（`reconcile_report`）を一度もimportしておらず、型定義と純粋関数（`AxisEvidence`／`evaluate_axes`等）のみを利用していた。`grep -rn`でdesign文§8の正規状態名（`RECEIVED`／`VALIDATED`／`POLICY_DENY`／`COMMITTED`／`COMPENSATE`等）がリポジトリ全体で1件もヒットしないことも確認し、状態機械自体がコード化されていないことを確認した
- 軸評価（`AdmittedBoundaryRuntime.assess_axes()`）は呼ばれてはいたが、その戻り値（PERMIT/BOUNDARY_WARNING/HANDOFF_REQUIRED/IRREVERSIBLE_TRANSITION/RUPTURE_BOUNDARY）は一切実行許可判定に使われず、「新規に不可逆ラッチが発生した場合にのみ`_external_witness_current`を倒す」という間接効果しか持たなかった。BOUNDARY_WARNING/HANDOFF_REQUIREDのようなラッチ未発火の軸判定は実行に何の影響も与えない状態だった
- 別途、検証体制（design文§11）をProperty-Based Testing・Differential Testing・Model Checking・Adversarial Testing・Recovery Drillの観点で再点検し、Hypothesis等のPBTライブラリ・`.tla`形式検証成果物・独立形式モデルとの差分試験・プロンプトインジェクション相当の試験がいずれも0件であること、「NRA-IDE正典参照試験38件」はsafety_kernel/trusted_runtime自体ではなく無関係な別参照実装（`nra-core/foundations/`）を検証しているに過ぎないことを確認した。これらは今回是正せず、次段階の課題として記録する

### 追加で掘り下げ、新規の根幹漏れではないと判定した点

- `FileChangeThicknessModel.estimate()`（δ/τの実測パイプライン）はAIの数値申告ではなく、実際のunified diffから機械計測し、hash-chain検証済み履歴・信頼済みsource_idのみを集計する健全な実装だった。ただしこのモデル自体もtrusted_runtimeから未接続であり、上記の根幹問題の一部として扱う
- 実行後の事後検証（`nonce_store.record_execution_reconciliation()`）は、独立署名されたobserver quorumの`observed_value`ハッシュと、認可時に固定した`required_postcondition_value`ハッシュを突合し、一致時のみ`VERIFIED_RESOLVED`とする実装で、trusted_runtime内部では正しく閉じていた
- `BoundaryExecutionIntent`（trusted_runtime独自のCapability型）と`ActionProposal`（safety_kernelのdesign文§4準拠の型付き提案スキーマ）は別物だが、これも根幹問題の一側面であり、独立した第二の欠落ではない

### 実施した是正（意図的に限定した範囲）

- `PersistentIrreversibleLatchStore`に読み取り専用メソッド`latched_axis_names(target_id)`を追加。既存の`assess_axes()`内部クエリと同じパターンで、チェーン整合性検証後に対象targetの永久ラッチ済み軸名集合を返す
- `AdmittedBoundaryRuntime.prepare_execution()`に、対象target_idが`latched_axis_names()`で非空（＝過去一度でもIRREVERSIBLE_TRANSITION/RUPTURE_BOUNDARYへ到達した軸がある）場合に`EXECUTION_TARGET_IRREVERSIBLY_LATCHED`でCapability発行を拒否する条件を追加。ラッチはappend-onlyで解除不可のため、EXECUTION_AUTHORIZER署名がいくつ揃っていても以後この対象への実行は永久に閉じる
- 意図的に据え置いた範囲：PERMIT/BOUNDARY_WARNING/HANDOFF_REQUIREDは従来どおりEXECUTION_AUTHORIZER署名quorumのみでゲートする（設計文の「人間委譲」を既に満たしていると判断）。`ActionProposal`と`BoundaryExecutionIntent`の統合、E0-E4可逆性等級別ゲーティング、Property-Based/Differential/Model Checking/Adversarial試験の追加は次段階の課題として残す

### この段階の境界

- 今回是正したのは「ラッチ済み（IRREVERSIBLE_TRANSITION/RUPTURE_BOUNDARY）対象への実行を機械的に閉じる」という最小限の一点のみである。safety_kernelとtrusted_runtimeを1本の合成パイプラインとして統合する作業（`ActionProposal`スキーマの共通化、Simulate段階の追加、E0-E4別ゲーティング等）は未着手である
- Recovery Drill相当（`revoke_capabilities`によるCapability一括失効、安全状態への縮退）は依然未実装
- 検証体制のNOT MET項目（PBT・Differential Testing・Model Checking・Adversarial Testing）も依然未着手であり、優先順位づけのみ合意した段階である

### 検証結果

- safety kernelおよびtrusted runtime試験：121件成功（新規1件：`test_execution_gate_denies_capability_for_irreversibly_latched_target`）
- NRA-IDE正典参照試験：38件成功
- 修正前コードへ一時的に戻した場合、ラッチ済み対象へ有効な署名で`prepare_execution`が素通りしCapabilityを発行してしまうこと（回帰検知として機能することの確認）：成功
- 既存rotation・rollback・launcher・execution runtime回帰：成功
- `git diff --check`：成功

---

## 2026-08-17：硬い不変条件を実行経路へ繋ぐ汎用フックの追加

### 今回の背景

- 前段の俯瞰監査で、design文§5.1の「硬い不変条件はδ/τ/Rスコアリングより先に必ず検査する」が実行経路（`trusted_runtime`）で強制されていないことが判明した。`FileChangePolicy.violations()`（scope escape・secret path・symlink・destructive patch・base hash不一致等を検査する、safety_kernel側の既存不変条件群）は`ActionProposal`＋`AuthoritativeEvidence`という、`trusted_runtime`の`BoundaryExecutionIntent`（`intent_id`／`target_id`／`action_digest`／`postcondition_*`のみ）とは異なる型を要求するため、単純な1行呼び出しでは接続できない構造的なギャップがあった
- 今回はfile-change固有のadapter（`BoundaryExecutionIntent`拡張、`FileChangePolicy`との橋渡し、実行直前の再観測）までは行わず、trusted_runtimeをdomain非依存に保つ設計文§12.3の原則に沿って、汎用の差し込み口だけを用意する方針とした

### 追加した実装

- `AdmittedBoundaryRuntime`に、既存の`execution_executor: BoundaryExecutor`と同じ注入パターンで`hard_invariant_checker: Callable[[BoundaryExecutionIntent, bytes], tuple[str, ...]] | None`を追加
- `execute_authorized_action()`の実行直前（action digest一致確認後、executor呼び出し前）でcheckerを呼び出し、返り値が空でなければ`EXECUTION_HARD_INVARIANT_VIOLATION:<reason_codes>`でexecutorへ到達させずに拒否する経路を追加
- checkerの返り値が`tuple[str, ...]`（非空文字列のみ）の形を満たさない場合は、違反なしとして通過させず`EXECUTION_HARD_INVARIANT_CHECKER_INVALID`で拒否する形式検証を追加。checker自体の不正な実装が既定PERMITへ倒れないようにする
- `admit_boundary_runtime()`・`launch_boundary_runtime()`双方に同パラメータを追加し、`execution_executor`と同じ経路で末端まで受け渡す

### この段階の境界

- 今回追加したのは差し込み口のみであり、`FileChangePolicy`をこのcheckerとして実際に接続するfile-change PoC向けadapterは未実装・未検証である。機構としての接続可能性は示したが、これは意図的な先送りであり、完了とは区別する。実際の要求が生じた時点で、adapterの実装と、それを裏付ける試験（fail-closed動作・checker偽装耐性を含む）の両方を行う
- `BoundaryExecutionIntent`は依然`ActionProposal`が持つ`resource_path`／`patch`／`base_sha256`／`change_kind`／`effect_class`等を持たない。adapterを書く際は、これらをintentへ追加するか、action bytesから復元するかの設計判断が必要になる
- `AuthoritativeEvidence`が要求する実行直前の再観測（TOCTOU防止）も、checker側の責務としてこのフックの外側で解決する必要がある。フック自体は同期呼び出しであり、非同期の再観測を強制する仕組みは持たない

### 検証結果

- safety kernelおよびtrusted runtime試験：161件成功（新規2件：`test_execution_gate_enforces_pluggable_hard_invariant_checker`、`test_execution_gate_rejects_malformed_hard_invariant_checker_result`）
- NRA-IDE正典参照試験：38件成功
- checker未設定時（デフォルトNone）の全既存回帰：成功（動作変更なしを確認）
- checkerが違反を返した場合にexecutorが一度も呼ばれないこと、クリーンな別intentでは正常に実行されること：成功
- checkerの返り値が不正な形式の場合に既定PERMITへ倒れず拒否されること：成功
- `git diff --check`：成功
---

## 2026-08-17：横軸残課題の実装プラン文書化

### 今回の背景

- 俯瞰監査（trusted_runtime俯瞰監査と是正、コミット`65f7f3f`）で洗い出した残課題を、順序・影響範囲・検証計画付きの実行可能なプランとして文書化した。併せて、正典（`theory/AXIOMS.md` v2.1）のIDE正規状態（§9・§10・§12・§14）と`safety_kernel`実装（`states.py`・`boundary.py`・`kernel.py`ほか）の対応をコードレベルで確認し、5境界状態・CONFESSION/τ=0分離・不可逆ラッチ・証言モード・Cause-Side分離が正典と整合していることを確認した

### 作成物

- `NRA-IDE_AI横軸機能_残課題実装プラン_20260817.md`（231行、§0〜§8）
  - §0 位置付けと境界：実作用・Capability発行なし、正典非昇格、鍵/DBはリポジトリ外、据え置き事項（二重ゆらぎ式・OS identity分離・WORM固定・実測校正・LLM統合）
  - §1 全体方針：設計文§18の導入順序＋監査報告§7の「根幹への近さ」優先
  - §2〜§3 タスク分解と優先順序：T1（`hard_invariant_checker`への`FileChangePolicy`実接続）→T2（Recovery Drill／`revoke_capabilities`全失効）→T3（スキーマ統合・Simulate段階・E0-E4ゲーティング）→T4（検証体制NOT MET）。依存理由を明記
  - §4 各課題の詳細：What・影響範囲・検証の3点セットで定義
  - §5〜§6 影響範囲（既存123件＋正典参照38件を維持）と検証計画（共通コマンド・§11.2合格指標対応表）
  - §7〜§8 リスク・据え置きと変更管理（T単位コミット分離、プラン変更時の追記手順）

### この段階の境界

- 本プランは文書であり、実装・検証結果の記録ではない。T1〜T4の着手は本プラン確定後に行う
- 既存の残課題（Recovery Drill未実装、スキーマ統合未着手、検証NOT MET）は従来どおり未着手のまま。本プランで「先送り」から「予定」へ状態を変えただけである

### 検証結果

- 章立て（§0〜§8）の過不足なしを確認：成功
- T1〜T4の各詳細（What・影響範囲・検証）の欠落なしを確認：成功
- 整形（§4見出し前の空行・末尾の`---`重複）を修正：成功

---

## 2026-08-17：T1完了（hard_invariant_checkerへのFileChangePolicy実接続）

### 今回の背景

- プラン§9の詳細設計（intent拡張・adapter・注入経路）に沿って実装済みの状態を検証し、プラン§9.5・§6.2の完了基準を満たすことを確認した。既存試験123件・正典参照38件を壊さずに接続する、という制約を保った

### 実装の要点（検証対象）

- `BoundaryExecutionIntent`（`execution_gate.py`）へ`FileChangeContext`（`resource_path`／`change_kind`／`action_type`／`expected_base_sha256`／`state_version`）を追加し、認可署名がfile-change最小フィールドを明示束縛する。認可スキーマを`boundary-execution-authorization/1.2`から`1.3`へ進めた
- `FileChangeInvariantAdapter`（新規`trusted_runtime/file_change_invariant_adapter.py`）が、intent＋action bytesから`ActionProposal`を復元し、`TrustedFileObserver`で実行直前に実ファイルを再観測（TOCTOU防止）してから`FileChangePolicy.violations()`を呼び、結果を`hard_invariant_checker`の契約`tuple[str, ...]`へそのまま渡す
- trusted_runtime本体（`boundary_runtime.py`・`boundary_runtime_launcher.py`）は無変更。既存の`hard_invariant_checker`フックが汎用のまま、adapterだけがsafety_kernelへ一方向importする設計（§12.3のdomain非依存原則を維持）

### 今回追加した是正

- adapter試験に`FILE_TYPE_NOT_ALLOWED`（許可拡張子外のファイルへの変更拒否）のケースが欠けていたため追加した（`test_file_change_invariant_adapter.py`）。プラン§9.5が列挙した9項目のうち、これが唯一未網羅だった

### この段階の境界

- `FileChangeInvariantAdapter`を実際に`launch_boundary_runtime(..., hard_invariant_checker=...)`へ注入するのはデプロイ側の責務であり、trusted_runtime本体やlauncherのデフォルトにはしていない（プラン§9.3.4の方針通り、デフォルトNoneで全既存回帰を不変に保つ）
- T3（`ActionProposal`↔`BoundaryExecutionIntent`のスキーマ完全統合）は本T1の前倒しではなく、file-changeドメインに必要な最小フィールドに限定した拡張である。統合は引き続き次段階の課題
- T2（Recovery Drill相当）は未着手のまま

### 検証結果

- safety kernel試験：140件成功・1件skip（Windows環境でのsymlink作成権限なしによる環境起因のskipで実害なし）（新規17件：`test_file_change_invariant_adapter.py`）
- NRA-IDE正典参照試験：38件成功
- プラン§9.5の9試験区分（正常系MODIFY/CREATE、BASE_HASH_MISMATCH、SCOPE_ESCAPE、SYMLINK_TARGET_FORBIDDEN、MODIFY_TARGET_MISSING/CREATE_TARGET_EXISTS、PATCH_HEADER_PATH_MISMATCH、DEPENDENCY_CHANGE_FORBIDDEN/FILE_TYPE_NOT_ALLOWED、観測失敗時のfail-closed、既存フック試験のスキーマ1.3回帰）を全て確認：成功
- 既存の`hard_invariant_checker`汎用フック試験2件（`test_execution_gate_enforces_pluggable_hard_invariant_checker`・`test_execution_gate_rejects_malformed_hard_invariant_checker_result`）がスキーマ1.3で回帰成功：成功
- `git diff --check`：成功
- 監査報告§7の優先順位（1. T1）を完了とし、次点はT2（Recovery Drill相当）
- Git状態：新規文書は未追跡のまま（stage・commitは行っていない）。既存の未追跡ファイル（俯瞰監査報告書）とも分離した

---

## 2026-08-17：T2完了（Recovery Drill相当：Capability全失効・安全状態への縮退）

### 今回の背景

- プラン§4 T2「`revoke_capabilities`による全Capability失効、安全状態への縮退」を実装した。監査報告§4.3でNOT MET（設計文§11.1）とされたRecovery Drillに対応する

### 追加した実装

- `trusted_runtime/nonce_store.py`の`PersistentNonceStore`へ、append-only・HMACチェーンの`capability_revocation`表を追加（既存の`consumed_nonce`・`execution_attempt`等と同じ規律：更新・削除はtriggerで拒否、`verify()`が全表と併せてチェーンを検証）
- `revoke_all_capabilities(reason, revoked_at)`：失効イベントを1件追記し、新しいgeneration番号を返す。**取り消し不可**——再度の呼び出しは「解除」ではなく新たな失効イベントとして積み上がる
- `current_revocation_generation()`：チェーン整合性を検証してから、現在の失効generation（未失効なら0）を返す
- `trusted_runtime/boundary_runtime.py`の`AdmittedBoundaryRuntime`へ`revoke_capabilities(reason, now=None)`を追加し、`prepare_execution()`（新規Capability発行）と`execute_authorized_action()`（発行済みCapabilityの実行）の両方の入口で`_ensure_not_revoked()`を呼ぶ。失効後はどちらも`EXECUTION_CAPABILITIES_REVOKED`で拒否される
- `assess_axes()`（軸判定・観測・証言の経路）は無変更。正典のFail-Closed意味（停止するのは自律判断・操作・自由生成のみ）に合わせ、失効後も観測・記録は継続する

### この段階の境界

- 失効は`execution_authorization_database_path`単位で永続・恒久である。**再有効化（re-arm）機構は意図的に実装していない**——失効状態から実行を再開するには、新しいdeployment（新しいDB）を用意し、witness quorumを含む起動プロセスをやり直す必要がある。これは「誰が失効を解除できるか」という新たな署名者ロール・quorum設計を必要とする問題を、今回のスコープから明確に外すための意図的な判断である
- 失効は`execution_authorization_database_path`を持つ実行系統のみを止める。`latch_database_path`（軸ラッチ）・witness DB・root policy checkpoint等、他の永続storeには影響しない
- 既発行のCapabilityのうち、失効前に`execute_authorized_action`が完了済みのもの（実行済み）は当然ながら覆らない。対象は「失効時点で未消費のCapability」および「以後の新規発行・新規実行」のみ

### 検証結果

- safety kernel試験：182件成功・1件skip（Windows symlink権限、環境起因で実害なし）（新規4件：nonce_store単体3件＝`test_revoke_all_capabilities_persists_across_reopen`・`test_capability_revocation_rows_reject_update_and_delete`・`test_corrupt_capability_revocation_chain_cannot_be_reopened`、統合1件＝`test_revoke_capabilities_blocks_pending_and_future_execution`）
- NRA-IDE正典参照試験：38件成功
- 修正前コード（`execute_authorized_action`側のチェックを一時除去）へ戻した場合、失効後も既発行Capabilityが実行できてしまうことを実際に確認してから復元：成功
- 失効後：新規`prepare_execution`が100%拒否、既発行Capabilityの`execute_authorized_action`が100%拒否、`assess_axes`（観測・証言）は継続動作：成功
- 失効の永続性（store再オープン後もgenerationが保持される）：成功
- 失効記録の改ざん検知（UPDATE/DELETE拒否、chain改ざん時の再オープン拒否）：成功
- `git diff --check`：成功
- 監査報告§7の優先順位のうちT1・T2を完了とし、次点はT3（スキーマ統合・Simulate段階・E0-E4ゲーティング）

---

## 2026-08-18：T3a完了（Capability必須属性の充足：subject_id・action_type・policy_version）

### 今回の背景

- T3（スキーマ統合・Simulate段階・E0-E4ゲーティング）は3つの課題の間でリスクの質が異なると判断し、まず影響範囲が小さいT3aから着手した。T3c（E0-E4等級別ゲーティング）については、ユーザーと協議のうえ「機構は実装するが、実効上の許可範囲は現行のE1限定のまま変更しない」という方針で合意した（design文§17の段階開放の原則を維持する判断）

### 追加した実装

- `BoundaryExecutionIntent`（`execution_gate.py`）へ、design文§7.1のCapability必須属性10項目のうち欠落していた3項目——`subject_id`（提案したAI実行体のID）・`action_type`（許可された一作用の種別、domain非依存の識別子）・`policy_version`（認可時点のポリシー/閾値構成を束縛する識別子）——を追加。すべて認可署名で束縛される必須フィールドとし、欠落や不正形式（空・空白混入・128文字超）は`validate()`で拒否する
- 認可スキーマを`boundary-execution-authorization/1.3`から`1.4`へ進め、`create_signed_execution_authorization()`／`verify_signed_execution_authorization()`の厳格`set(...)`照合・encode/decodeを新フィールドへ対応させた
- `test_latch_witness.py`内の全12箇所の`BoundaryExecutionIntent(`構築、および`test_file_change_invariant_adapter.py`内の2箇所を新フィールド対応へ更新
- 新規回帰試験`test_execution_intent_carries_capability_required_attributes`：3フィールドそれぞれの不正値（空・空白混入・長すぎる値）拒否と、署名往復後も値が保持されることを確認

### この段階の境界

- `action_type`はCapability層の汎用識別子であり、`FileChangeContext.action_type`（domain固有の`PROPOSE_PATCH`/`PROPOSE_TEST_FILE`）とは別概念である。両者の値を一致させるかどうかはdeployment側の裁量とし、trusted_runtime本体は両者の一致を強制しない
- `policy_version`は現時点では認可署名に含まれる識別子として記録されるのみで、これを検証・比較する能動的なロジック（例：現在有効なpolicy_versionと異なる場合の拒否）は実装していない。次段階（T3c関連）の課題として残す
- `subject_id`も同様に、現時点では記録・検証（形式チェック）のみで、特定のAI実行体を実際に認証・識別する仕組み（対応する鍵・証明書等）とは接続していない

### 検証結果

- safety kernel試験：183件成功・1件skip（Windows symlink権限、環境起因で実害なし）（新規1件：`test_execution_intent_carries_capability_required_attributes`）
- NRA-IDE正典参照試験：38件成功
- 既存の全回帰（スキーマ1.4への更新を含む12+2箇所の`BoundaryExecutionIntent`構築）：成功
- `git diff --check`：成功
- 監査報告§7の優先順位のうちT1・T2・T3aを完了とし、次点はT3b（Simulate段階）

---

## 2026-08-18：T3b完了（Simulate段階：実行前予測フック）

### 今回の背景

- design文§7の7段階取引（Propose→Validate→Simulate→Authorize→Execute→Verify→Commit/Compensate）のうち、Simulate段階が実装に存在しないという監査報告の指摘（`grep -rni simulate`が0件）に対応した
- T1（`hard_invariant_checker`）・T3c（機構のみ実装しE1限定は維持）と同じ設計方針を踏襲：trusted_runtime本体はdomain非依存な汎用フックとして実装し、file-change向けの具体的なsimulator（実際にpatchを適用してみる等）は次段階の課題として残す

### 追加した実装

- `execution_gate.py`へ`SimulationOutcome`（`predicted_success: bool`・`predicted_result_digest: str | None`・`reason_codes: tuple[str, ...]`）を追加
- `AdmittedBoundaryRuntime`へ、既存の`hard_invariant_checker`と同じ注入パターンで`simulator: Callable[[BoundaryExecutionIntent, bytes], SimulationOutcome] | None`を追加
- `execute_authorized_action()`の実行直前（`hard_invariant_checker`の後、executor呼び出し前）でsimulatorを呼び出し、`predicted_success=False`ならexecutorへ到達させずに`EXECUTION_SIMULATION_PREDICTS_FAILURE:<reason_codes>`で拒否する経路を追加
- simulatorの返り値が`SimulationOutcome`型でない、または`predicted_result_digest`が64hex以外の場合は、成功として通過させず`EXECUTION_SIMULATOR_RESULT_INVALID`で拒否する形式検証を追加（`hard_invariant_checker`と同じfail-closed規律）
- `admit_boundary_runtime()`・`launch_boundary_runtime()`双方に同パラメータを追加し、末端まで受け渡す経路を通した。`SimulationOutcome`を`trusted_runtime`の公開APIへ追加

### この段階の境界

- 今回追加したのは差し込み口のみであり、file-change PoC向けの具体的なsimulator実装（実際にpatchを適用してみて結果を予測する等）は未実装・未検証である。T1（`FileChangeInvariantAdapter`）と同様、これは意図的な先送りであり、実際の要求が生じた時点で実装と検証の両方を行う
- `predicted_result_digest`は形式検証（64hex文字列またはNone）のみ行い、実行後の実際の結果ハッシュと突合する検証ロジックはまだ実装していない
- Simulateは`execute_authorized_action`内の同期呼び出しであり、別途の永続ジャーナル（`hard_invariant_checker`と同様）は持たない

### 検証結果

- safety kernel試験：185件成功・1件skip（Windows symlink権限、環境起因で実害なし）（新規2件：`test_execution_gate_enforces_pluggable_simulator`・`test_execution_gate_rejects_malformed_simulator_result`）
- NRA-IDE正典参照試験：38件成功
- simulator未設定時（デフォルトNone）の全既存回帰：成功（動作変更なしを確認）
- 修正箇所を一時的に無効化した場合、両新規テストが実際に失敗することを確認してから復元：成功
- `git diff --check`：成功
- 監査報告§7の優先順位のうちT1・T2・T3a・T3bを完了とし、次点はT3c（E0-E4機構の追加、実効はE1限定のまま）

---

## 2026-08-18：T3c完了（E0-E4可逆性等級別ゲーティングの機構化、実効はE1限定を維持）

### 今回の背景

- ユーザーとの協議で「T3cは機構を実装するが、実効上の許可範囲は現行のE1限定のまま変更しない」という方針に合意した（design文§17の段階開放原則の維持）。T3a・T3bで確立した「trusted_runtime側は汎用フックのみ・実際の判断ロジックは次段階」というパターンとは異なり、T3cはsafety_kernel側（`policy.py`）の変更である

### 追加した実装

- `FileChangePolicy`（`policy.py`）へ`enabled_effect_classes: frozenset[EffectClass]`を追加。**デフォルト値は`frozenset({EffectClass.E1_REVERSIBLE})`**で、明示的に指定しない限り既存の挙動と完全に同一（回帰試験で無変更を確認済み）
- `violations()`の効果等級チェックを、ハードコードされた「E1以外は拒否」から「`enabled_effect_classes`に含まれない場合は拒否」へ変更。等級を有効化する・しないはdeployment側の明示的な設定次第であり、自動的には広がらない
- **`EffectClass.E4_CRITICAL`は設定によって有効化することが構造的に不可能**：`__post_init__`が`enabled_effect_classes`に`E4_CRITICAL`を含む`FileChangePolicy`の構築自体を拒否する。加えて`violations()`側にも独立した多重防御（`__post_init__`のガードを将来誰かが迂回しても、この行が単独でE4を拒否し続ける）を追加。design文§7.2が要求する「検証済み基準制御と独立安全系」をこのPoCが持たないことの直接的な反映
- 新規試験クラス`FileChangePolicyEffectClassGatingTests`（4件）：デフォルト設定でE1以外が全て拒否されること、明示的にE2を有効化した場合にE2は通り他等級（E3）は依然拒否されること、E4を有効化しようとする構築自体が拒否されること、defense-in-depth側（`violations()`単体）でもE4が拒否されることを確認

### この段階の境界

- 機構は実装したが、本PoCの実際のdeployment（`FileChangeInvariantAdapter`等）は依然として`FileChangePolicy()`のデフォルト構築（E1限定）のまま変更していない。E2/E3の等級別の追加要件（補償手順の記録、人間承認の必須化等、design文§7.2の完全な内容）は本メカニズムの「有効化できるかどうか」の部分のみを実装しており、有効化された場合に等級ごとに何を追加要求するかの詳細設計（例：E2に補償手順フィールドを必須化する等）はまだ実装していない
- `clarification.py`のE3/E4に対する問い直しレベル上昇（C3/C4）ロジックは既存のまま変更していない（既に設計文の意図と整合していることを既存試験で確認済み）
- `subject_id`・`action_type`・`policy_version`（T3a）とeffect_classゲーティング（T3c）はまだ相互に接続されていない。例えば`policy_version`が特定のeffect_class設定を指すといった対応付けは次段階の課題

### 検証結果

- safety kernel試験：189件成功・1件skip（Windows symlink権限、環境起因で実害なし）（新規4件：`test_default_policy_still_admits_only_e1`・`test_explicitly_enabling_e2_admits_it`・`test_e4_critical_cannot_be_enabled_by_configuration`・`test_e4_critical_is_rejected_even_by_a_permissive_default_policy`）
- NRA-IDE正典参照試験：38件成功
- デフォルト設定（`enabled_effect_classes`省略）での全既存回帰：成功（動作変更なしを確認）
- `git diff --check`：成功
- 監査報告§7の優先順位のうちT1・T2・T3（a/b/c全て）を完了とし、次点はT4（検証体制のNOT MET項目）

---

## 2026-08-18：T4-1完了（Property-Based Testing、`boundary.py`実装のバグを発見・修正）

### 今回の背景

- 監査報告§4.3でNOT METとされたProperty-Based Testingに対応した。プランのT4-1に従い、`boundary.py`・`policy.py`・`decoder.py`を対象に、NaN・無限大・境界値・未知フィールド・巨大値等を系統的に投入する試験を追加した
- ツール選定はユーザーと協議し、hypothesisを新規依存として追加する方針で合意した（プラン§7に「T4で新規依存が必要な場合は個別確認を得てから導入する」と明記されていたため）

### 追加した実装

- `hypothesis==6.165.10`を新規依存として追加（`pip install`＋`safety_kernel/tests/requirements-test.txt`を新設してpin）
- 新規`safety_kernel/tests/test_property_based.py`（16試験、`unittest.TestCase`継承で`python -m unittest discover`からも収集可能）
  - `boundary.py`：`evaluate_axis`が任意のfloat（NaN・±inf・境界値）で例外を出さないこと、非有限値・負値が常にCONFESSIONになること、`tau=0`が常にOUT_OF_DESCRIPTION_DOMAINになること、分類が`ratio`としきい値の関係と一致すること、`evaluate_axes`が複数軸の平均化ではなく最悪軸を採用することを確認
  - `policy.py`：`violations()`が任意の`resource_path`・`patch`テキストで例外を出さないこと、path traversalが常に`INVALID_RESOURCE_PATH`になること、デフォルト設定でE1以外の等級が常に拒否されることを確認
  - `decoder.py`：`decode_action_proposal`が任意のtext/bytesで例外を出さないこと、返り値が常に整合していること（proposal有りなら理由コード無し、逆も然り）、未知フィールド・重複フィールドが常に拒否されること、正常な入力が往復できることを確認

### 発見し是正したバグ

- `FileChangePolicy.violations()`（`policy.py`）に、`resource_path`にNULバイト（`\x00`）が含まれる場合、拒否ではなく`ValueError`で**クラッシュする**欠陥があった。`resolve_target()`内部の`PurePosixPath(...).resolve()`が`os.stat()`を呼び、NULバイトを含むパスに対してOSレベルで例外を送出するため。本来この関数は他の全チェックと同様「例外を出さず、必ず`violations`リストへ分類する」total functionであるべきところ、この1パターンだけ例外化していた
- 是正：既存の`INVALID_RESOURCE_PATH`早期拒否条件へNULバイト検知を追加し、さらに`resolve_target()`呼び出し自体を`(ValueError, OSError)`で捕捉して`INVALID_RESOURCE_PATH`へ変換する多重防御を追加した。修正前コードへ一時的に戻し、`test_violations_never_raises_on_arbitrary_resource_path`が実際に`resource_path='\x00'`で再現・失敗することを確認してから復元した
- 実害の評価：`hard_invariant_checker`フック（T1）は`self._hard_invariant_checker(intent, action)`の呼び出しをtry/exceptで囲んでいないため、この例外は`execute_authorized_action()`から未捕捉のまま伝播しうる状態だった。executorへは到達しない（fail-closedの結果自体は変わらない）が、正常な`EXECUTION_HARD_INVARIANT_VIOLATION`ではなく生の例外で落ちる、という頑健性の欠陥だった

### この段階の境界

- 対象は`boundary.py`・`policy.py`・`decoder.py`の3ファイルに限定した。他のtrusted_runtime側モジュール（署名検証・quorum等）へのPBT適用は次段階の課題として残す
- `boundary_runtime.py`の`hard_invariant_checker`／`simulator`呼び出し自体を try/except で保護する対応は今回行っていない（今回の発見は`policy.py`側の是正で解消したため）。将来別のcheckerが同種の未捕捉例外を出す可能性は残る

### 検証結果

- safety kernel試験：205件成功・1件skip（Windows symlink権限、環境起因で実害なし）（新規16件：`test_property_based.py`）
- NRA-IDE正典参照試験：38件成功
- `python -m unittest note.poc_horizontal_ai.safety_kernel.tests.test_property_based`：16件成功（プロジェクト既定の検証コマンドでも収集・成功することを確認）
- 修正前コードへ一時的に戻した場合、`test_violations_never_raises_on_arbitrary_resource_path`が実際に失敗すること（回帰検知として機能することの確認）：成功
- `git diff --check`：成功
- 監査報告§7優先順位のうちT1・T2・T3・T4-1を完了とし、次点はT4-2（Adversarial Testing）

---

## 2026-08-18：T4-2完了（Adversarial Testing、Unicode正規化の未接続を発見・修正）

### 今回の背景

- 設計文§17第3週の投入リスト（パストラバーサル、シンボリックリンク経由の脱出、大文字小文字差、Unicode類似文字、巨大パッチ、バイナリ混入、テストコマンドへの引数注入、RAG文書内の偽命令、古いファイルハッシュによる上書き、ログ停止）を1件ずつ、`FileChangeInvariantAdapter`（実際にtrusted_runtimeの実行経路へ接続されているコード）に対して確認した

### 各項目の現状

| 投入項目 | 状態 |
|---|---|
| パストラバーサル | 既存試験＋T4-1のPBTでカバー済み |
| シンボリックリンク経由の脱出 | 既存試験でカバー済み（本機ではWindows symlink権限によりskip、環境起因） |
| 大文字小文字差 | 実装は既にcasefold対応済みだったが専用試験がなかったため追加 |
| **Unicode類似文字** | **未接続の欠落を発見・修正**（下記） |
| 巨大パッチ | 専用試験がなかったため追加 |
| バイナリ混入 | 専用試験がなかったため追加 |
| テストコマンドへの引数注入 | 該当機能（`run_allowlisted_test`相当）が未実装のためN/A |
| RAG文書内の偽命令 | LLM/RAG統合が未実装のためN/A（Model Swap TestのN/A理由と同様） |
| 古いファイルハッシュによる上書き | 既存試験（`test_adapter_rejects_base_hash_mismatch`）でカバー済み |
| ログ停止 | T4-3（Fault Injection）で扱う |

### 発見し是正したバグ

- `decoder.py`にはUnicode正規化（NFC）チェックが実装されているが、`FileChangeInvariantAdapter`は`decode_action_proposal`を経由せず`intent`から直接`ActionProposal`を構築するため、**この防御が実行経路から完全に漏れていた**。実際に検証：`resource_path`へ分解形Unicode（"e" + 結合文字U+0301、視覚的には合成済み"é"と同一だがバイト列は異なる）を渡すと、`FileChangePolicy.violations()`は`()`（違反なし）を返していた
- 是正：`policy.py`の`violations()`へ、`resource_path`・`patch`・`idempotency_key`のNFC正規化チェックを追加し、`FIELD_NOT_NFC`で拒否するようにした。修正前コードへ一時的に戻し、新規試験`test_adapter_rejects_non_nfc_resource_path`が実際に失敗することを確認してから復元した
- T4-1（NULバイトのクラッシュ）と合わせて、これで2件連続してPBT/Adversarial Testingが「`decoder.py`にはある防御が、`FileChangeInvariantAdapter`の直接構築経路には無い」という同じパターンの欠落を検出したことになる。今後同種の防御を追加する際は、decoder.py側だけでなくpolicy.py側にも複製する必要があることを示唆する

### 追加した試験

- `test_file_change_invariant_adapter.py`へ4件追加：`test_adapter_rejects_case_variant_secret_path`・`test_adapter_rejects_non_nfc_resource_path`・`test_adapter_rejects_oversized_patch`・`test_adapter_rejects_binary_diff_marker`

### この段階の境界

- テストコマンド引数注入・RAG偽命令はN/Aとしたが、これは「対応済み」ではなく「対応する機能がまだ存在しない」ことを意味する。将来これらの機能（allowlist済みテスト実行、RAG統合）を実装する際は、この2項目を再度Adversarial Testingの対象として持ち出す必要がある
- ログ停止はT4-3（Fault Injection）で扱うため、本エントリでは対応していない

### 検証結果

- safety kernel試験：209件成功・1件skip（Windows symlink権限、環境起因で実害なし）（新規4件）
- NRA-IDE正典参照試験：38件成功
- 修正前コードへ一時的に戻した場合、`test_adapter_rejects_non_nfc_resource_path`が実際に失敗すること：成功
- `git diff --check`：成功
- 監査報告§7優先順位のうちT1・T2・T3・T4-1・T4-2を完了とし、次点はT4-3（Fault Injection）

---

## 2026-08-18：T4-3完了（Fault Injection：時計ずれ・ログ不能）

### 今回の背景

- プランT4-3（センサー停止・時計ずれ・通信断・ログ不能）に対応した。着手前に既存試験を`grep`で確認したところ、`SIGNATURE_STALE`（Ed25519署名の鮮度検証、witness attestation・trust bundle・execution authorizationなど全ての署名検証が依存する共通プリミティブの鮮度チェック）が**一度も直接試験されていない**ことが判明した

### 各項目の現状

| 投入項目 | 対応 |
|---|---|
| **時計ずれ（鮮度違反）** | **未試験だった`SIGNATURE_STALE`の直接試験を追加**（下記） |
| ログ不能 | `PersistentNonceStore`（nonce/実行認可/失効の永続store）と`PersistentIrreversibleLatchStore`（軸ラッチstore）双方について、DB書込み不能時（読み取り専用ファイルで模擬）にfail-closedであることを確認する試験を追加 |
| センサー停止（観測不能） | 既存試験（`test_adapter_rejects_modify_target_missing`等）で部分的にカバー済みと判断 |
| 通信断（観察経路喪失） | `CommunicationChannelState`/`LoggingChannelState`は`evidence.py`にフィールドとして定義されているが、実際にACTIVE以外の値を生成する検出ロジックがどこにも存在しない（`grep`で確認）。意味のある障害注入試験を書けるのは検出ロジックが実装されてから。既知の構造的限界として記録する |

### 追加した試験

- `test_asymmetric_stage.py`（`Ed25519AuthenticationTests`）：`test_clock_skew_beyond_max_age_is_rejected`——`max_age`ぎりぎり内側では受理、超過後・大幅未来時刻では`SIGNATURE_STALE`で拒否されることを確認
- `test_trusted_runtime.py`（`PersistentNonceStoreTests`）：`test_consume_fails_closed_when_logging_is_impossible`・`test_revoke_all_capabilities_fails_closed_when_logging_is_impossible`——DBファイルを読み取り専用にした状態で`consume()`・`revoke_all_capabilities()`を呼び、`accepted=False`で拒否され、失効generationが偽って進んでいないことを確認
- `test_irreversible_latch_store.py`（`PersistentIrreversibleLatchStoreTests`）：`test_assess_axes_fails_closed_when_logging_is_impossible`——同様にDB書込み不能時、`assess_axes()`が`IRREVERSIBLE_LATCH_STORE_FAILURE`で例外を送出し、PERMIT相当の結果を返さないことを確認

### 結果

- いずれも新規バグは発見しなかった——3ストア全てが期待通りfail-closedだった（実際にPythonから直接呼び出して動作を確認してから試験化した）。ただし`SIGNATURE_STALE`は今回まで**一度も試験されていなかった**ため、この試験追加自体が検証体制の実質的な穴を埋めるものである

### この段階の境界

- 「通信断（観察経路喪失）」は検出ロジック自体が存在しないため、意味のある試験を書けなかった。将来`ObservationChannelState`等を実際に生成する監視ロジックを実装する際は、この項目を再度Fault Injectionの対象として持ち出す必要がある
- 「センサー停止」は既存試験による部分カバーで済ませており、専用の新規試験は追加していない

### 検証結果

- safety kernel試験：213件成功・1件skip（Windows symlink権限、環境起因で実害なし）（新規4件）
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功
- 監査報告§7優先順位のうちT1・T2・T3・T4-1・T4-2・T4-3を完了とし、次点はT4-4（Differential Testing / Model Checking）

---

## 2026-08-18：T4-4完了（Model Checkingのみ実施、Differential Testingは先送り）

### 今回の背景

- T4-4は本来Differential TestingとModel Checkingの2本立てだが、ユーザーと協議し「Differential Testingは正典参照実装（`nra-core/foundations/`）と`safety_kernel.boundary`の比較可能性調査が先に必要なため、今回はModel Checkingのみ進め、Differential Testingは先送りとする」方針で合意した
- Model Checkingは形式ツール（TLA+等）を導入せず、`boundary_runtime`の実行ゲート状態遷移に対する境界ケースの組合せ試験というbounded検査で対応した

### 追加した試験

- `test_latch_witness.py`：`test_capability_cannot_be_constructed_outside_prepare_execution`——**状態飛越し**の検査。`WitnessBoundExecutionCapability`を`prepare_execution`を経由せず直接構築しようとすると、privateトークンによるガードで拒否されることを確認。これはランタイムチェックではなく構造的な保証であることを実証した
- `test_latch_witness.py`：`test_combined_faults_never_permit_execution`——複数の拒否条件（不可逆ラッチ済み対象＋失効済みランタイム）を同時に成立させ、どちらのチェックが先に発火しても結果は常に拒否であり、条件の重なりが誤ってALLOWへ相殺されないことを確認

### 既存カバレッジの確認（新規試験なし）

- **許可後すり替え**：`EXECUTION_CAPABILITY_INTENT_MISMATCH`等の既存試験で確認済み
- **デッドロック**：`unresolved_execution_attempt_ids()`が未解決のreconciliationがある限り新規実行を`EXECUTION_OUTCOME_RECONCILIATION_REQUIRED`で全てブロックする挙動は、既存試験（`test_latch_witness.py`内の複数箇所）で既にカバーされていることを確認した。これは意図的なfail-safe（安全側に倒すための一種の「詰み」状態）であり、新規試験は追加していない

### この段階の境界

- Differential Testing（正典参照実装との判定一致試験）は本エントリでは実施していない。着手する場合はまず`nra-core/foundations/NRA-IDE_Architecture_public.py`と`safety_kernel/boundary.py`の入出力意味論が実際に比較可能かを調査する必要がある
- Model Checkingは`boundary_runtime`の実行ゲートに限定した。他のモジュール（root_policy rotation、latch witness quorum等）の状態遷移への同種の組合せ検査は今回対象外

### 検証結果

- safety kernel試験：215件成功・1件skip（Windows symlink権限、環境起因で実害なし）（新規2件）
- NRA-IDE正典参照試験：38件成功
- `git diff --check`：成功
- 監査報告§7優先順位のうちT1・T2・T3・T4-1〜T4-3・T4-4（Model Checkingのみ）を完了。残るのはDifferential Testingのみ
