# trusted_runtime実装の俯瞰監査と是正 — δ/τ/R判定と実行許可の接続

作成時刻（JST）：2026-08-17 11:38:59
対象：`note/poc_horizontal_ai/`（安全カーネルPoCの実装本体、`safety_kernel/`および`trusted_runtime/`）
参照元設計文：`NRA-IDE_AI横軸機能_現実実装最適解_20260812-1934.md`
状態：実装済みコードに対する監査・是正の記録。新たな正典追加ではなく、既存PoCの検証報告と部分是正です。

---

## 1. 要旨

`trusted_runtime/`は、2026-08-13から2026-08-17にかけて段階的に構築された。各セッションは、署名再検証・nonceによるリプレイ防止・鍵rotation・quorum判定・append-only監査ログといった個々の機構について、非常に高い精度で実装・試験されていた。しかし、各セッションが自身の担当範囲を深く掘り下げるほど、「そもそも各機構が1本のパイプラインとして繋がっているか」という一段上の問いは検査対象から外れやすくなる。本報告は、視点を変えた複数回の精査（セキュリティ観点→設計整合性観点→俯瞰観点）を通じてこの種の見落としを検出し、実害のある2件のバグ修正と、根幹に関わる1件の構造的欠落に対する部分是正を行った記録である。

もっとも重要な発見は次の一点に集約される。**設計文§18が主張する「δ/τ/R判定を行うHorizontal Safety Kernelが、その判定に基づいてCapability Proxyを完全仲介する」という一体構造は、実装には存在しなかった。** `safety_kernel`（δ/τ/R判定・不変条件・状態機械）と`trusted_runtime`（署名quorum・Capability発行・実行）は、互いを呼び出さない独立した2系統として実装されていた。これは個々のコンポーネントの品質の問題ではなく、design文の中心命題（§3.1「AIが迂回できない完全仲介」）そのものが実装で成立していないという、根幹の齟齬である。

今回はこの齟齬全体を一度に解消するのではなく、（1）実害のある既存バグ2件の修正、（2）不可逆ラッチ済み対象への実行を機械的に恒久遮断する接続、（3）硬い不変条件を将来接続するための汎用フックの追加、という3点に是正範囲を意図的に限定した。残る接続作業（`ActionProposal`とのスキーマ統合、Simulate段階の追加、E0-E4別ゲーティング、検証体制の拡充）は、先送りであることを明記した上で次段階の課題とした。

---

## 2. 背景と経緯

### 2.1 監査の動機

`note/poc_horizontal_ai/`はNRA-IDEの正典から独立した技術設計候補であり、設計文自身が「区切り探索における技術設計候補。汎用安全性の完成証明、正典への追加、または本番実装の安全証明ではありません」と明記している。しかし、この種のPoCが最終的に論文や技術ノートとして「実装され検証された」と主張する場合、主張と実装の乖離はそのまま論文の信頼性の欠落になる。

セッション開始の接続規則（`CLAUDE.md`）は「文章・Codeなどの精査は一度目と二度目は必ず変えて別視点から行う事。全体精査（長文・ファイル群）は俯瞰視点も必要です」と定めている。本監査はこの規則に従い、単一視点の精査を繰り返すのではなく、意図的に異なる評価軸を用いた複数回の独立した精査を行った。

### 2.2 対象範囲

- `safety_kernel/`：δ/τ/R判定コア（`boundary.py`）、正規状態（`states.py`）、硬い不変条件（`policy.py`）、証拠品質（`evidence.py`）、報告-現実照合（`reconciliation.py`）、限定ファイル変更ドメインの厚み換算（`thickness.py`・`file_change_thickness.py`）ほか
- `trusted_runtime/`：Ed25519署名・nonce・鍵rotation・witness quorum・不可逆ラッチ・実行ゲート等、約36ファイル
- `tests/test_nra_ide_reference.py`（NRA-IDE正典参照試験、38件）
- `safety_kernel/tests/`（123件）

---

## 3. 監査手法

視点を変えた3段階の精査を行った。

| 段階 | 視点 | 主な成果物 |
|---|---|---|
| 第1段階 | セキュリティ観点（署名検証・リプレイ防止・ロール分離の脆弱性） | 実害のあるバグ1件を発見・修正 |
| 第2段階 | 設計整合性・ロジック正しさ観点（モジュール間の一貫性、fail-closed規律） | 実害のあるバグ1件を追加発見・修正 |
| 第3段階 | 俯瞰観点（design文の主張とコードの対応関係を、推測なしでgrep/read検証のみによってトレース） | 根幹の構造的欠落を発見 |

第3段階では、design文§5〜§13・§16の具体的な主張それぞれについて「実装されているか」「実行経路として到達可能か（単に試験されているだけの孤立実装ではないか）」を分けて評価する追跡表（Part A）と、design文§11が要求する検証手法カテゴリ（Property-Based Testing・Differential Testing・Model Checking・Adversarial Testing・Recovery Drill等）の充足状況評価（Part B）を作成した。すべての結論は`grep`／ファイル全文読解による実証を伴うもののみを採用し、実装の典型的なパターンからの推測は「unverified」として区別した。

---

## 4. 発見事項

### 4.1 実害のあるバグ（第1・第2段階）

**① witness state DBのrepository外配置チェックの欠落**

`trusted_runtime/boundary_runtime_launcher.py`の`_validate_checkpoint_signer_placement()`は、trust checkpoint DB・latch/nonce/anchor/root-policy checkpoint DB・全latch witnessおよび全root-policy witnessのDBパス群（`state_paths`）のうち、**先頭1件（`state_paths[0]`）しか**repository外配置を検証していなかった。直前の`secret_paths`チェックは`any(...)`で全件を検査していたのに対し、`state_paths`側だけ検査漏れがあった。この関数は`launch_boundary_runtime`から実際に呼ばれる生きたコードであり、二つ目以降のwitness state DBをrepository内に配置しても起動を拒否できない状態だった。複数witnessによる巻き戻し防止という設計の核（design文§5.11）を、witnessの一部については無効化しうる欠陥だった。

**② `RootPolicyCheckpointStore.accept()`の署名再検証欠如**

`trusted_runtime/root_policy.py`の`RootPolicyCheckpointStore.accept()`（base、非rotationパス）は、呼び出し側が構築した公開dataclass`RootPolicyQuorum`の`satisfied`フィールドを信用するだけで、署名原本`signed_endorsements`を自ら再検証していなかった。同じ関数のrotation側（`RootPolicyRotationQuorum`）は2026-08-17付の先行セッションで「型名や`satisfied`値だけをauthorityにしない」よう既に修正されており、base側だけがこの原則から取り残されていた。唯一の本番呼び出し元（`boundary_runtime.py`）は直前に必ず検証済みquorumを構築していたため当日時点の実害はなかったが、クラス自身が自己の不変条件を強制していない点は、将来の呼び出し元追加やリファクタリングに対して脆弱だった。

いずれも、独立したagentによる指摘を鵜呑みにせず、実際のコードを自分で読み、修正前コードに一時的に戻して検知ゲートが本当に素通りすることを確認したうえで是正した。

### 4.2 根幹の構造的欠落（第3段階・俯瞰監査）

design文§18は次の6層構造を主張する。

1. Untrusted Intelligence（LLM）
2. Typed Proposal Boundary（`ActionProposal`）
3. Horizontal Safety Kernel（不変条件・δ/τ/R・状態機械）
4. Capability Proxy（一回限りの限定権限による完全仲介）
5. Runtime Assurance（危険接近時の基準制御切替）
6. Evidence and Recovery（監査・補償・復旧）

実装を突き合わせた結果、この一体構造は存在しなかった。決定的な証拠は次のとおりである。

- `trusted_runtime.boundary_runtime`の`prepare_execution()`（`boundary_runtime.py:205`）と`execute_authorized_action()`（`boundary_runtime.py:240`）——実際に外部作用を許可・実行する唯一の経路——を全文精読したが、`TargetBoundaryState`／`BoundaryAssessment`（軸判定結果）への参照は皆無だった。実行可否はEXECUTION_AUTHORIZER署名quorum・latch head一致・action digest一致のみで決まる。
- `grep -rn "safety_kernel" trusted_runtime/*.py`の結果、trusted_runtimeは`ShadowSafetyKernel`本体・硬い不変条件（`FileChangePolicy`）・報告-現実照合（`reconcile_report`）を一度もimportしていなかった。輸入されているのは型定義と純粋関数（`AxisEvidence`／`evaluate_axes`等）のみだった。
- `grep -rn`でdesign文§8の正規状態名（`RECEIVED`／`VALIDATED`／`POLICY_DENY`／`COMMITTED`／`COMPENSATE`等）を検索したところ、リポジトリ全体で1件もヒットしなかった。§8の状態機械はコード化されていなかった。
- `AdmittedBoundaryRuntime.assess_axes()`は軸判定を返してはいたが、その戻り値（PERMIT/BOUNDARY_WARNING/HANDOFF_REQUIRED/IRREVERSIBLE_TRANSITION/RUPTURE_BOUNDARY）は実行許可判定に一切使われず、「新規に不可逆ラッチが発生した場合にのみ`_external_witness_current`を倒す」という間接効果しか持たなかった。ラッチ未発火のBOUNDARY_WARNING/HANDOFF_REQUIREDは実行に何の影響も与えない状態だった。
- `grep -rni simulate`はリポジトリ全体で0件であり、design文§7の7段階取引（Propose→Validate→Simulate→Authorize→Execute→Verify→Commit/Compensate）のうちSimulate段階は文字通り存在しなかった。
- `BoundaryExecutionIntent`（`execution_gate.py`のCapability型）は`intent_id`／`target_id`／`action_digest`／`postcondition_*`のみを持ち、design文§4の`ActionProposal`が持つ`resource_id`／`effect_class`／`reversibility`等を持たない別スキーマだった。Capability必須属性（§7.1、10項目）のうち`subject_id`／`action_type`／`policy_version`の3項目が欠落していた。

一方、追加で掘り下げた3項目については、独立した新たな根幹漏れではなく、健全な実装または上記1点の派生であることを確認した。

- `FileChangeThicknessModel.estimate()`（δ/τの実測パイプライン、design文§5.7準拠）は、AIの数値申告ではなく実際のunified diffから機械計測し、hash-chain検証済み履歴・信頼済みsource_idのみを集計する健全な実装だった（`file_change_thickness.py:138-157`）。
- 実行後の事後検証（`nonce_store.record_execution_reconciliation()`）は、独立署名されたobserver quorumの`observed_value`ハッシュと認可時に固定した`required_postcondition_value`ハッシュを突合し、一致時のみ`VERIFIED_RESOLVED`とする実装で、trusted_runtime内部では正しく閉じていた。
- `BoundaryExecutionIntent`と`ActionProposal`の型分離は、根幹問題（safety_kernelとtrusted_runtimeの未接続）の一側面であり、独立した第二の欠落ではなかった。

### 4.3 検証体制の適合性（design文§11との対比）

| 要求カテゴリ | 判定 | 根拠 |
|---|---|---|
| 単体試験 | MET | 123件、不変条件・状態遷移を広くカバー |
| Property-Based Testing | NOT MET | `grep -rn hypothesis`＝0件 |
| Differential Testing | NOT MET | `tests/test_nra_ide_reference.py`（38件）は`safety_kernel`/`trusted_runtime`と無関係の別参照実装（`nra-core/foundations/`）を検証しているのみ |
| Model Checking | NOT MET | `.tla`等の形式検証成果物は0件 |
| Fault Injection | PARTIALLY MET | 個別手書き失敗パスはあるが体系的ハーネスなし |
| Adversarial Testing | NOT MET | プロンプトインジェクション相当の試験0件。LLM統合自体が未実装 |
| Replay/TOCTOU | MET | nonce台帳・replay拒否試験が充実 |
| Red Team | PARTIALLY MET | 迂回経路試験は1件のみ |
| Recovery Drill | NOT MET | `revoke_capabilities`（Capability全失効）・Compensate（補償）は未実装 |
| Model Swap Test | N/A | LLM未統合のため試験対象自体が存在しない |

---

## 5. 実施した是正

俯瞰監査で判明した根幹の齟齬は、一度に解消できる規模ではないと判断し、是正範囲を次の3点に意図的に限定した。

### 5.1 バグ修正（4.1節の2件）

- `_validate_checkpoint_signer_placement()`のstate DB配置チェックを、`secret_paths`と同じ`any(...)`パターンへ統一（`boundary_runtime_launcher.py:723`付近）。
- `RootPolicyCheckpointStore.accept()`のシグネチャを、事前構築済み`RootPolicyQuorum`ではなく生の`signed_endorsements`を受け取り、内部で`assess_root_policy_quorum()`を呼んで自己完結的に再検証する構成へ変更（`root_policy.py:437`）。

いずれも回帰テストを追加し、修正前コードでは検知ゲートを素通りすることを実際に確認してから復元した。

### 5.2 不可逆ラッチ済み対象への実行の恒久遮断

design文の状態機械では、`RUPTURE_BOUNDARY`は「以後は証言のみ、作用は禁止」（`POST_RUPTURE_FIXED_TESTIMONY`）を意味する。しかし是正前は、対象がこの状態に到達していても、EXECUTION_AUTHORIZER署名さえ揃えば実行できてしまっていた。

- `PersistentIrreversibleLatchStore`に読み取り専用メソッド`latched_axis_names(target_id)`を追加（`irreversible_latch_store.py:223`）。チェーン整合性検証後、対象targetの永久ラッチ済み軸名集合を返す。
- `AdmittedBoundaryRuntime.prepare_execution()`に、対象target_idの`latched_axis_names()`が非空であればCapability発行そのものを`EXECUTION_TARGET_IRREVERSIBLY_LATCHED`で拒否する条件を追加（`boundary_runtime.py:205`付近）。ラッチはappend-onlyで解除不可のため、以後この対象への実行は署名の有無に関わらず永久に閉じる。

意図的に据え置いた範囲：`PERMIT`／`BOUNDARY_WARNING`／`HANDOFF_REQUIRED`は従来どおりEXECUTION_AUTHORIZER署名quorumのみでゲートする。全実行が常に署名者による個別承認を要求する現在の設計は、design文の「人間委譲」（`HANDOFF_REQUIRED`→`TRANSFER_EXECUTION_AUTHORITY`）をある意味では既に、より保守的な形で満たしていると判断したためである。

### 5.3 硬い不変条件のための汎用フック

design文§5.1「一つでも硬い不変条件違反があれば、スコア計算より先に拒否する」は、実行経路（trusted_runtime）では機械的に強制されていなかった。`FileChangePolicy.violations()`（`policy.py`、scope escape・secret path・symlink・destructive patch・base hash不一致等を検査する既存の不変条件群）は`ActionProposal`＋`AuthoritativeEvidence`という、`BoundaryExecutionIntent`とは異なる型を要求するため、単純な1行接続はできない構造的なギャップがあった。

今回はfile-change固有のadapter（型統合・実行直前の再観測）までは行わず、trusted_runtimeをdomain非依存に保つ設計文§12.3の原則（「責務を混ぜないことが検証可能性を保つ」）に沿って、汎用の差し込み口のみを追加した。

- `AdmittedBoundaryRuntime`に、既存の`execution_executor: BoundaryExecutor`と同じ注入パターンで`hard_invariant_checker: Callable[[BoundaryExecutionIntent, bytes], tuple[str, ...]] | None`を追加。
- `execute_authorized_action()`実行直前（action digest一致確認後、executor呼び出し前）でcheckerを呼び出し、返り値が空でなければexecutorへ到達させずに拒否する経路を追加。
- checkerの返り値が`tuple[str, ...]`（非空文字列のみ）の形を満たさない場合は、違反なしとして通過させず`EXECUTION_HARD_INVARIANT_CHECKER_INVALID`で拒否する形式検証を追加。checker自体の不正な実装が既定PERMITへ倒れないようにした。
- `admit_boundary_runtime()`・`launch_boundary_runtime()`双方に同パラメータを追加し、末端まで受け渡す経路を通した。

このフックは、機構としての接続可能性を示すものであり、`FileChangePolicy`との実接続は**未実装・未検証**である。これは意図的な先送りであり、完了とは区別する。実際の要求が生じた時点で、adapterの実装と、それを裏付ける試験（fail-closed動作・checker偽装耐性を含む）の両方を行う。

---

## 6. design文への示唆

design文§16「現況で実現できる範囲」のうち、「軸別`δ/τ/R`と最大軸判定」「対象限定・短命・一回限りCapability」は、監査時点では**別々には**実現されていたが、**組み合わさって機能してはいなかった**。今回の是正により、不可逆ラッチという最も安全側に倒すべき状態についてのみ、両者が接続された。この限定的な接続は、design文§3.1が横軸の正否の基準として掲げる「AIが迂回できない完全仲介」を、少なくとも「二度と戻らない一線を越えた対象への再実行」という一点においては満たすようになったことを意味する。

一方で、`BOUNDARY_WARNING`・`HANDOFF_REQUIRED`という中間状態は、依然として実行可否に構造的な影響を持たない。現行実装がこれを「常に人間署名を要求する」というより保守的な設計で代替しているという解釈は成り立つが、design文が想定する「軸ごとに問い直し強度を変える」（§5.5・§14）という段階的な応答は実装されていない。この点は次段階の課題として明示的に残した。

---

## 7. 今後の課題（優先順位）

俯瞰監査で洗い出した残課題を、根幹への近さで順に示す。

1. ~~`hard_invariant_checker`への`FileChangePolicy`の実接続（`BoundaryExecutionIntent`の型拡張、実行直前の再観測の設計を含む）~~ → **完了**（追記参照）
2. Recovery Drill相当（`revoke_capabilities`によるCapability全失効、安全状態への縮退）
3. `ActionProposal`と`BoundaryExecutionIntent`のスキーマ統合、Simulate段階の追加、E0-E4可逆性等級別ゲーティング
4. 検証体制のNOT MET項目（Property-Based Testing・Differential Testing・Model Checking・Adversarial Testing）の優先度に応じた着手

いずれも、着手しない限りは「先送り」として`history.md`に明記された状態を維持する。

> **追記（同日）**：本報告後、`NRA-IDE_AI横軸機能_残課題実装プラン_20260817.md`として1〜4を実行可能なプラン化し、T1（項目1）を完了した。`BoundaryExecutionIntent`を`FileChangeContext`で拡張し（認可署名で明示束縛）、新規`FileChangeInvariantAdapter`が実行直前に実ファイルを再観測してから`FileChangePolicy.violations()`を呼ぶ形で接続した。trusted_runtime本体はdomain非依存のまま変更していない。詳細と検証結果は`history.md`の「T1完了（hard_invariant_checkerへのFileChangePolicy実接続）」を参照。次点はT2（Recovery Drill相当）。

---

## 8. 結論

個々のコンポーネントが高精度に実装・試験されていても、それらを俯瞰する視点を意図的に挟まない限り、「部品は正しいが、繋がっていない」という根幹の齟齬は検出されない。本監査は、視点を変えた複数回の精査という手順そのものが、この種の見落としに対する現実的な防御になることを示した。実装が主張に追いつくまでの残作業は依然として多いが、今回の是正により、少なくとも「不可逆な一線を越えた対象への実行が、署名だけで通ってしまう」という最も危険な食い違いは解消された。残る接続作業は、本報告の第7節に従い、必要と要求が生じた時点で実装と検証の両方を行うものとして先送りする。

---

## 参考：本セッションでの変更ファイル

- `note/poc_horizontal_ai/trusted_runtime/boundary_runtime_launcher.py`（バグ修正）
- `note/poc_horizontal_ai/trusted_runtime/root_policy.py`（バグ修正）
- `note/poc_horizontal_ai/trusted_runtime/irreversible_latch_store.py`（`latched_axis_names`追加）
- `note/poc_horizontal_ai/trusted_runtime/boundary_runtime.py`（ラッチ済み対象の実行遮断、`hard_invariant_checker`追加）
- `note/poc_horizontal_ai/trusted_runtime/boundary_runtime_launcher.py`（`hard_invariant_checker`の受け渡し追加）
- `note/poc_horizontal_ai/safety_kernel/tests/test_latch_witness.py`（回帰テスト4件追加、既存呼び出し3箇所更新）
- `note/poc_horizontal_ai/history.md`（各段階の作業記録）

検証結果：safety_kernel試験123件・NRA-IDE正典参照試験38件、計161件成功。`git diff --check`成功。コミット`65f7f3f`。
