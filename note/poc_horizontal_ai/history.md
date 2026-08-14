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
