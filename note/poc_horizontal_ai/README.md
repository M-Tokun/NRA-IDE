# NRA-IDE AI横軸機能 PoC (`note/poc_horizontal_ai`) 概要

本ディレクトリ (`note/poc_horizontal_ai/`) は、NRA-IDEにおける**AI横軸安全機能（推論性能とは独立した決定論的安全カーネルおよび信頼できる実行基盤）**の概念設計、PoC（Proof of Concept）実装、監査報告、および実験モジュールを収容しています。

## 1. 全体コンセプト

NRA-IDEにおける機能分離の原則：
- **縦軸（AIモデル）**：推論、探索、コード生成、計画立案などの思考・提案能力。AIは「権限を持たない未検証の提案器」として扱います。
- **横軸（安全基盤）**：AIモデルから独立した決定論的安全カーネルおよび信頼できる実行基盤。すべての外部作用（ファイル変更、コマンド実行等）を完全仲介し、危険距離 ($\delta$)、許容時間 ($\tau$)、不可逆変化の厚み ($R$)、および暗号的証明に基づいて安全判定・実行を制御します。

---

## 2. ディレクトリ構成とファイル一覧

### 2.1 ルートドキュメント (設計・監査・計画・履歴)

| ファイル名 | 役割・概要 |
| :--- | :--- |
| [NRA-IDE_AI横軸機能_現実実装最適解_20260812-1934.md](./NRA-IDE_AI横軸機能_現実実装最適解_20260812-1934.md) | 横軸安全基盤の根本設計書。AI提案と実行権限の分離、完全仲介、安全指標 ($\delta, \tau, R$)、および段階的導入手順を記述。 |
| [NRA-IDE_AI横軸機能_trusted_runtime俯瞰監査と是正_20260817-1138.md](./NRA-IDE_AI横軸機能_trusted_runtime俯瞰監査と是正_20260817-1138.md) | `safety_kernel/` および `trusted_runtime/` の構造・セキュリティ・整合性に関する俯瞰監査結果および是正記録。 |
| [NRA-IDE_AI横軸機能_残課題実装プラン_20260817.md](./NRA-IDE_AI横軸機能_残課題実装プラン_20260817.md) | PoCにおける残課題（Property-Based Testing, Adversarial Testing, Model Checking, Differential Testing等）の実施計画・ロードマップ。 |
| [history.md](./history.md) | 本PoCにおける設計・実装・監査・修正・検証の時系列実施ログ。 |

---

### 2.2 サブディレクトリ (実装・実験モジュール)

#### ① [`safety_kernel/`](./safety_kernel) (安全カーネル PoC)
AIモデルからの提案（Action Proposal）を評価し、作用の安全性を判定するシャドー安全カーネルの実装。
詳細説明は [safety_kernel/README.md](./safety_kernel/README.md) を参照。

- **モジュール概要**:
  - [`kernel.py`](./safety_kernel/kernel.py): 安全判定エンジンのメインエントリ。
  - [`boundary.py`](./safety_kernel/boundary.py): 判定境界および $\delta, \tau, R$ メトリクス評価。
  - [`policy.py`](./safety_kernel/policy.py): 硬い禁止条件・安全状態ポリシーの定義。
  - [`instruction_contract.py`](./safety_kernel/instruction_contract.py): AI提案のパースと条件固定。
  - [`observer_protocol.py`](./safety_kernel/observer_protocol.py) / [`observer.py`](./safety_kernel/observer.py): 観察プロトコルおよび観測器。
  - [`audit_bundle.py`](./safety_kernel/audit_bundle.py) / [`evidence.py`](./safety_kernel/evidence.py): 判定証拠と監査バンドルの生成。
  - [`file_change_thickness.py`](./safety_kernel/file_change_thickness.py): ファイル変更不可逆厚みの差分計算モデル。
  - [`tests/`](./safety_kernel/tests): テストスイート（単体・対向・故障注入・Property-based等）。

#### ② [`trusted_runtime/`](./trusted_runtime) (信頼できる実行基盤 PoC)
シャドー安全カーネルの判定から鍵・一回性管理を分離し、暗号的署名・Quorum認証・非対称認証・改ざん不可レシーシプトを提供する実行保護基盤。
詳細説明は [trusted_runtime/README.md](./trusted_runtime/README.md) を参照。

- **モジュール概要**:
  - [`boundary_runtime.py`](./trusted_runtime/boundary_runtime.py): 境界実行ランタイム本体。
  - [`root_policy.py`](./trusted_runtime/root_policy.py): 最上位アクセス制御およびセキュリティポリシー。
  - [`execution_gate.py`](./trusted_runtime/execution_gate.py): 実行ゲート（無認証作用の阻止）。
  - [`asymmetric_auth.py`](./trusted_runtime/asymmetric_auth.py) / [`auth.py`](./trusted_runtime/auth.py): Ed25519 署名 / HMAC 認証。
  - [`nonce_store.py`](./trusted_runtime/nonce_store.py) / [`anchor_store.py`](./trusted_runtime/anchor_store.py): リプレイ防止 Nonce 管理および Anchor 固定。
  - [`latch_witness.py`](./trusted_runtime/latch_witness.py) / [`witness_store.py`](./trusted_runtime/witness_store.py): 不逆ラッチ証言および Quorum 証人ストレージ。

#### ③ [`experiments/`](./experiments) (実験モジュール)
- **[`temporal_state_candidate/`](./experiments/temporal_state_candidate)**:
  - 学習型ゲートによる時間状態保持（Horizontal State）の初期探索PoC (`horizontal_state.py`, `memory_store.py`, `poc_runner.py`)。現行 `safety_kernel/` とは分離して保持。詳細説明は [experiments/temporal_state_candidate/README.md](./experiments/temporal_state_candidate/README.md) を参照。

---

## 3. テストの実行方法

各モジュールの検証は以下のコマンドで実施できます。

```powershell
# safety_kernel のテスト実行
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s note/poc_horizontal_ai/safety_kernel/tests -v

# trusted_runtime の単体・結合検証 (リポジトリルートから)
python -m unittest discover -s note/poc_horizontal_ai/trusted_runtime -p "test_*.py" -v
```
