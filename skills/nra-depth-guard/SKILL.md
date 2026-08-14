---
name: nra-depth-guard
description: |
  NRA-IDE準拠のエージェント探索爆発防止・境界制御ライブラリ。
  エージェントの思考軌跡に対し、物理的閾値と経路（ω）に基づく決定論的判定を提供する。
  Soft Boundary（プロンプト層）とHard Boundary相当の判定ロジック（Pythonライブラリ層）を分離し、
  AIの推測や意味に依存しない構造的判定を行う。呼び出し側が各ツール呼び出し前に
  能動的に判定を通す運用を前提とする（既知の限界は §4.3 参照）。
version: 1.1.0
author: user
tags: [safety, nra-ide, fail-closed, exploration-control, trajectory-guard]
---

# SKILL: NRA-IDE Trajectory Boundary Control & Anti-Explosion Guardrail

## 1. 目的

状態空間における不必要な深層探索および循環的ループ（探索爆発 / Exploration Explosion）を未然に防ぎ、常に定義された論理境界の内部で実行を完結させる。

本Skillは**NRA-IDE（Nomological Ring Axioms - Intensional Dynamics Engine）**の原則に基づき、以下を厳守する：

- **AIの推測や意味を信用しない**
- **安全保証は因果構造と物理的観測値のみに基づく**
- **Fail-closed（破断時は必ず停止・遮断）**
- **AI推論と安全判定の混用計算を禁止**

---

## 2. 必須不変条件 (Invariants)

### 2.1 探索深さ・物理閾値の上限制限

単一タスクにおける状態遷移の試行回数は、**意味的な「深さ」ではなく物理的観測値**によって制限される。

| 閾次元 | 観測対象 | デフォルト |
|---------|---------|----------|
| `max_depth` | 状態遷移ステップ数 | 5 |
| `max_wall_time_ms` | 実測経過時間（ms） | 30000 |
| `max_api_calls` | ツール呼び出し回数 | 20 |
| `max_memory_mb` | 実測メモリ使用量（MB、`psutil`未導入時は無効化） | 512 |

**原則**: 「5」という数値はフォールバック保険。本質的な制限は**観測された物理量**が閾値を超えたか否かで決まる。

### 2.2 権限・安全境界の厳密遵守

明示的に与えられた認可範囲外のAPI呼出、他ユーザー領域へのアクセス、非正規パラメータの試行は即座に停止理由（FAIL_CLOSED）として処理する。

**判定主体**: `invariant_rules` に外部注入された決定論的関数群。AIの推論結果は判定に使用しない。

### 2.3 経路（ω）を含む循環・同値性検出

過去に実行したアクション系列と**同じ経路で到達した同値状態**が検出された場合、別のアプローチを模索せず即座に制御を上位システムへ返却する。

**重要**: `action_name` + `parameters` のみの比較は不十分。`A→B→C→A` と `D→B→C→A` は同じ「A」に見えて**文脈（経路）が異なる**。NRA-IDEは経路（ω）を状態の一部として扱う。

### 2.4 未探索空間（Unexplored Frontier）の明示

打ち切り時に「次に試される予定だったが実行されなかったパス」を**未探索空間としてログに記録**する。観測の放棄を因果的に追跡可能にする。

---

## 3. 動作プロトコル

### 3.1 各思考ステップ（Reasoning Step）での義務

エージェントは各ステップにおいて、ツール呼び出しの直前に `validate_and_step()` を呼び、以下を必ず照合せよ：

1. **現在の探索深さ**（`_current_depth`）
2. **現在の経路ハッシュ**（`path_hash` = 親経路ハッシュ + 状態ハッシュの連鎖）
3. **過去の実行軌跡セット**（`_trajectory_hashes`）
4. **物理的閾値の観測値**（経過時間、API呼び出し回数、メモリ）

### 3.2 不変条件チェックの順序

各ステップの実行前に、以下の順序で決定論的検証を行う。`violation_type` の値は実装（`nra_depth_guard.py`）の文字列と一致させている。

```
Step 1: 局所不変条件検証 (Invariant Rules)
         → 違反時: violation_type = "INVARIANT" → FAIL_CLOSED (即座停止)

Step 2: 物理閾値検証 (Depth / Wall Time / API Calls / Memory)
         → 超過時: violation_type = "PRUNED" → FAIL_CLOSED (探索打ち切り)

Step 3: 経路循環検証 (Path-based Cycle Detection)
         → 検出時: violation_type = "DIVERGENCE_PRUNED" → FAIL_CLOSED (循環打ち切り)

Step 4: 未探索空間のfrontier登録
         → 次に試す候補パスを事前登録

Step 5: 状態確定と深さ更新
         → 軌跡セットへの追加、path_hashの子へ伝播
```

### 3.3 打ち切り時の振る舞い

不変条件違反または上限閾値に達した場合、**一切の代替提案・回復試行・推測的補完を行わない**。

以下の**因果構造ログ（Causal Log）**を出力して即座に停止：

```json
{
  "event": "FAIL_CLOSED",
  "violation_type": "INVARIANT | PRUNED | DIVERGENCE_PRUNED",
  "dimension": "invariant_rule | depth | wall_time_ms | api_calls | memory_mb | path_hash",
  "observed_value": 123.45,
  "threshold_value": 100.00,
  "violation_direction": "EXCEEDED | UNDERRUN",
  "final_depth": 5,
  "path_hash_at_stop": "a1b2c3d4...",
  "explored_paths": ["p1", "p2", "p3"],
  "unexplored_frontier": ["candidate_A", "candidate_B"],
  "timestamp_utc": "2026-08-13T14:32:00Z"
}
```

`violation_direction` は判定の発火条件（`observed >= threshold`）と一致させて算出する。ちょうど閾値に到達した場合も `"EXCEEDED"` とし、`"UNDERRUN"` とは記録しない。

---

## 4. 層分離構造

### 4.1 Soft Boundary（プロンプト層）

- エージェントへの**推奨事項・ヒューリスティクス**として機能
- 「無理な探索を行わずに断念・停止する選択肢が正常な挙動であると」を認めさせる
- **安全保証を提供しない**。AIが無視・迂回可能。

### 4.2 Hard Boundary相当の判定ロジック（Pythonライブラリ層）

- `NRADepthGuardEngine.validate_and_step()` は、AIの出力内容や意図を問わず、観測値と経路のみに基づいて決定論的に合否を返す
- 意味解釈やAIの自己申告を判定へ混入させない、という意味での「Hard」である

### 4.3 既知の限界（重要）

このライブラリ**単体は、ツール呼び出しを強制的に横取りする機構ではない**。呼び出し側（エージェント自身、またはエージェントを駆動するコード）が各ツール呼び出しの直前に `validate_and_step()` を能動的に呼ぶことで初めて機能する、**協力的な自己申告型**の判定ロジックである。

- 呼び出しを省略された場合、何のチェックも行われない。
- `parent_path_hash` を毎回正しく引き継がず `"root"` を渡し続けるなど、呼び出し側の実装ミスや意図的な迂回によって経路循環検出は無効化できる。
- 真に強制的な遮断（AIが判定をスキップできない構成）が必要な場合は、Claude Codeの `PreToolUse` フック等、エージェントの外側で全ツール呼び出しを仲介する別の機構へこの判定ロジックを組み込む必要がある。本Skillはそのフック配線自体は提供しない。

**原則**: Soft Boundaryは「AIの行動を誘導するヒント」。本ライブラリは「意味論を介さない決定論的な判定ロジック」であり、両者は混用しない。ただし後者も、それを呼び出すかどうかの最終判断はエージェント側に委ねられている点で、単独では実行を強制できない。

---

## 5. 実装

完全な実装は同ディレクトリの [`nra_depth_guard.py`](./nra_depth_guard.py) を参照。主なクラス／関数は次の通り。

- `NRAThresholds`：`max_depth` / `max_wall_time_ms` / `max_api_calls` / `max_memory_mb` を保持するdataclass
- `NRADepthGuardEngine`：`validate_and_step(action_name, parameters, parent_path_hash)` を中核とする判定エンジン
- `PruningReport` / `FailClosedException`：打ち切り時の因果構造ログとその例外化
- `rule_authorization_boundary` / `rule_forbidden_api_scope`：`invariant_rules` に注入する検証関数の実装例

最小の使用例：

```python
from nra_depth_guard import NRADepthGuardEngine, NRAThresholds, FailClosedException

guard = NRADepthGuardEngine(
    thresholds=NRAThresholds(max_depth=3, max_wall_time_ms=10000.0, max_api_calls=5),
)
guard.register_frontier([("get_class_schedule", {"week": 2})])

try:
    _, path_1 = guard.validate_and_step("get_class_schedule", {"week": 1}, parent_path_hash="root")
    _, path_2 = guard.validate_and_step("reserve_class", {"class_id": 101}, parent_path_hash=path_1)
except FailClosedException as e:
    print(e.causal_log)  # 構造化された因果ログ（dict）
```

`python nra_depth_guard.py` を直接実行すると、認可境界違反によって `FailClosedException` が送出されるデモが動く。

---

## 6. 統合指針

### 6.1 エージェント実行パイプラインへの組み込み

```
[User Query]
    ↓
[Agent Reasoning Loop]
    ↓
[Tool Call Generation] ← Soft Boundary（プロンプト層：推奨事項）
    ↓
[NRADepthGuardEngine.validate_and_step()] ← エージェント自身が能動的に呼ぶ判定ステップ（§4.3の限界を参照）
    ↓ (通過時)
[Actual Tool Execution]
    ↓
[Result Observation]
    ↓ (path_hashを子に伝播して反復)
[Agent Reasoning Loop]
```

### 6.2 反復時の経路ハッシュ伝播

```python
# 親ステップ
_, parent_hash = guard.validate_and_step(
    "search_code", {"query": "auth"}, parent_path_hash="root"
)

# 子ステップ（親のpath_hashを引き継ぐ）
_, child_hash = guard.validate_and_step(
    "read_file", {"path": "src/auth.py"}, parent_path_hash=parent_hash
)

# 孫ステップ（連鎖継続）
_, grandchild_hash = guard.validate_and_step(
    "edit_file", {"path": "src/auth.py", "patch": "..."},
    parent_path_hash=child_hash
)
```

### 6.3 運用上の注意

1. **閾値の調整**: `max_depth` はフォールバック。本番環境では `max_wall_time_ms` と `max_api_calls` を主要閾値とする。
2. **不変条件の外部化**: `invariant_rules` はエージェントコードから完全に分離し、独立した設定ファイルまたはポリシーエンジンから注入する。
3. **ログの永続化**: `FailClosedException` の `causal_log` は構造化JSONとして必ず外部ログシステムへ出力する。原因追跡（Audit）の唯一の情報源となる。
4. **未探索空間のレビュー**: 打ち切り時の `unexplored_frontier` は人間オペレータが確認し、必要に応じて別セッションで再開する判断材料とする。
5. **強制力が必要な場合**: §4.3の通り、本ライブラリ単体はopt-inである。省略不可能な強制遮断が必要な用途では、別途フック機構への組み込みを検討する。

---

## 7. NRA-IDE原則との対応表

| NRA-IDE原則 | 本Skillでの実装 |
|------------|---------------|
| AIの推測や意味を信用しない | `invariant_rules` の外部注入、AI推論結果を判定に不使用 |
| 物理ログのみを扱う | 閾値を `wall_time_ms` / `api_calls` / `memory_mb` など観測値で定義 |
| 混用計算禁止 | Soft Boundary（プロンプト）と判定ライブラリ（Python）の分離 |
| Fail-closed | `FailClosedException` で即座停止。回復試行を一切行わない |
| 経路（ω）を状態の一部として扱う | `path_hash` = 親経路ハッシュ + 状態ハッシュの連鎖 |
| 観測放棄の明示 | `unexplored_frontier` の打ち切りログへの記録 |
| 原因追跡可能性 | 因果構造ログ（observed/threshold/direction/timestamp）の構造化出力 |

### 7.1 正典の境界状態機械との関係

本Skillの `INVARIANT` / `PRUNED` / `DIVERGENCE_PRUNED` は、`FORMULA.md`が定める正典の境界状態（`PERMIT` / `BOUNDARY_WARNING` / `HANDOFF_REQUIRED` / `IRREVERSIBLE_TRANSITION` / `RUPTURE_BOUNDARY` / `CONFESSION` / `OUT_OF_DESCRIPTION_DOMAIN`）とは**別の語彙**であり、意図的に対応付けていない。本Skillはエージェントの探索メタ制御（深さ・時間・API呼出回数・経路循環）を扱う層であり、対象ドメインの物理量に基づく`δ/τ/R`判定とは扱う対象が異なる。正典の境界状態を流用・混同しないことが、両者を独立に検証可能に保つ前提である。

---

## 8. 制限事項と責任範囲

- 本Skillは**探索爆発の構造的防止**を目的とする。セマンティックな「正解性」や「最適解」の保証は行わない。
- `invariant_rules` の定義責任は運用者にある。ルール自体の不備による安全破綻は本Skillの責任範囲外。
- `psutil` が未インストールの環境では、`nra_depth_guard.py` はimport時に例外を出さず、メモリ閾値チェックのみを無効化する（他の閾値・循環検出には影響しない）。
- §4.3に記載の通り、本Skill単体では呼び出しの省略や `parent_path_hash` の誤用を強制的には防げない。強制力を持たせるには別途フック等への統合が必要。
