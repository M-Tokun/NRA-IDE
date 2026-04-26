# NRA-IDE: 律環公理 / 内包性動力学エンジン

**NRA-IDE — Nomological Ring Axioms / Intensional Dynamics Engine**

[![License](https://img.shields.io/badge/license-Proprietary-red)](../LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()

> **NRA-IDE は因果構造の安全エンジンである。**  
> 意味・最適化・履歴を扱わず、その挙動は構造不変量によってのみ決定される。

---

## 0. 本リポジトリの目的

NRA-IDE は以下の問いに答えるために設計された。

> **「なぜ出力したのか」を、AIは本当に構造的に説明できるのか。**

確率的に最もらしい言葉を生成することと、因果的に正しい判断を下すことは本質的に異なる。  
NRA-IDE は「より賢いAI」を目指さない。**「制約が崩壊しない構造を持つAI安全ミドルウェア」** を実現する。

---

## 1. 設計原則（非可変・構造不変量）

| 原則 | 内容 |
|------|------|
| 非意味（Non-Semantic） | 意味・感情・文脈を因果判定に使用しない |
| 非最適化（Non-Optimization） | 距離・類似度・スコアによる判定を行わない |
| 因果ダイオード（Causal Diode） | Π⁻¹（逆推論）を構造的に禁止 |
| 三層分離 | Pre-RNA / LLM / Post-RNA を物理的に分離 |
| Fail-Closed | 不確実なら沈黙（曖昧なまま通過させない） |
| Symbol-Only | 記号と定義のみを扱う |

---

## 2. 三層分離アーキテクチャ

```
ユーザー入力
    ↓
[A] Pre-RNA（入力フィルター）
    Π⁻¹誘発パターンを検出・変換・遮断
    ↓ 変換済み入力
[B] LLM（生成装置）
    言語生成のみを担当。安全性は担当しない。
    ↓ 生出力
[C] Post-RNA / CleanContext
    R = δ/τ で検証 → PASSED → ユーザーへ
                    → FAIL-CLOSED → DiscardVault（隔離）
```

**重要：** 破棄された出力（FAIL-CLOSED）は DiscardVault に封印され、LLMのコンテキストに絶対に逆流しない。

---

## 3. ゲート機構（Three-Zone Structure）

$$R = \frac{\delta}{\tau}$$

| Zone | 条件 | 動作 |
|------|------|------|
| A | R < 0.40 | PERMIT（許可） |
| B | 0.40 ≤ R < 1.00 | PERMIT WITH CAVEAT（警告付き許可） |
| C | R ≥ 1.00 | FAIL-CLOSED（完全遮断） |

- **δ（デルタ）**：ゆらぎ量。入力・出力の構造的逸脱の大きさ
- **τ（タウ）**：制約の厚み。ドメインごとに設定（Domain Tuning）
- **FAIL-CLOSED はエラーではない**。「構造的正しさの維持」が目的。

---

## 4. Domain Tuning（ドメイン別制約設定）

| ドメイン | τ | R_op | 前方参照 | 用途 |
|---------|---|------|---------|------|
| MEDICAL | 0.60 | 0.60 | 禁止 | 医療プロトコル・ICU監視 |
| TECHNICAL | 0.50 | 0.80 | 許可 | 技術仕様書・設計書 |
| LEGAL | 0.70 | 0.55 | 禁止 | 法令・規約・契約書 |
| ACADEMIC | 0.55 | 0.75 | 許可 | 論文・技術白書 |
| GENERAL | 0.41 | 0.65 | 許可 | 汎用（デフォルト） |

---

## 5. ファイル構成

```
NRA-IDE/
├── nra_document_structure_20260213_0135.py     # [Post-RNA] 構造文書エンジン（日本語版）
├── nra_document_structure_EN_20260213_0135.py  # [Post-RNA] Document Structure Engine (EN)
├── nra_llm_pipeline_20260213_0135.py           # [B+C] LLMパイプライン（日本語版）
├── nra_llm_pipeline_EN_20260213_0135.py        # [B+C] LLM Pipeline (EN)
├── nra_pre_rna_20260213_0135.py                # [A+B+C] 完全統合パイプライン（日本語版）
├── nra_pre_rna_EN_20260213_0135.py             # [A+B+C] Full Pipeline (EN)
├── README-JP.md                                # 本ドキュメント
└── README-EN.md                                # English documentation
```

### ファイル依存関係

```
nra_pre_rna_*.py
    ├── import nra_llm_pipeline_*.py
    │       └── import nra_document_structure_*.py
    └── import nra_document_structure_*.py
```

---

## 6. クイックスタート

### 前提条件

```bash
Python 3.9+
pip install anthropic  # Anthropic APIを使う場合
pip install openai     # OpenAI APIを使う場合
```

### 最小動作確認（MOCKプロバイダー）

```bash
# APIキー不要でデモが動作する
python3 nra_pre_rna_EN_20260213_0135.py

# または日本語版
python3 nra_pre_rna_20260213_0135.py
```

### 実API接続

```bash
export ANTHROPIC_API_KEY="your-key-here"
# または
export OPENAI_API_KEY="your-key-here"
```

---

## 7. 各ファイルの使い方

### 7.1 [Post-RNA] nra_document_structure（構造文書エンジン）

GenesisBlock に定義を登録し、SectionNode を検証する基盤エンジン。

```python
from nra_document_structure_EN_20260213_0135 import (
    DocumentEngine, DomainType
)

# 文書エンジンを初期化（ドメイン指定）
engine = DocumentEngine("My Technical Spec", DomainType.TECHNICAL)

# GenesisBlock に定義を登録（公理として固定）
engine.genesis.add("NRA-IDE",
                   "Causal structure safety engine.",
                   is_axiom=True)
engine.genesis.add("Fail-Closed",
                   "Safety mechanism: blocks output when R >= R_op.")
engine.genesis.seal()  # 封印（以降、定義変更不可）

# 節を追加
engine.add_section(
    section_id="1",
    title="Overview",
    content="This document describes NRA-IDE.",
    references=["NRA-IDE"]
)

# 文書生成（検証実行）
output = engine.build()
print(output.to_text(include_meta=True))
print(f"Integrity Score: {output.integrity_score():.4f}")
```

### 7.2 [B+C] nra_llm_pipeline（LLMパイプライン）

LLMを外部生成装置として接続し、Post-RNA検証とCleanContext管理を行う。

```python
from nra_llm_pipeline_EN_20260213_0135 import (
    LLMBridge, LLMProvider, NRALLMPipeline
)
from nra_document_structure_EN_20260213_0135 import DocumentEngine, DomainType

# エンジンとブリッジを初期化
engine = DocumentEngine("Session", DomainType.TECHNICAL)
engine.genesis.add("NRA-IDE", "Causal safety engine.", is_axiom=True)

bridge = LLMBridge(
    provider=LLMProvider.MOCK,  # ANTHROPIC / OPENAI / GOOGLE / MOCK
    model="mock-v1"
)

pipeline = NRALLMPipeline(doc_engine=engine, llm_bridge=bridge)

# 1ターン実行
result = pipeline.run(
    user_input="What is NRA-IDE?",
    references=["NRA-IDE"]
)
print(result["status"])   # PASSED / CAVEAT / FAIL-CLOSED
print(result["output"])   # 検証済みテキスト（FAIL-CLOSEDは空文字）
print(pipeline.status())  # パイプライン状態
```

### 7.3 [A+B+C] nra_pre_rna（完全統合パイプライン）

Pre-RNA（入力フィルター）を含む完全な3層パイプライン。

```python
from nra_pre_rna_EN_20260213_0135 import NRAFullPipeline
from nra_llm_pipeline_EN_20260213_0135 import LLMBridge, LLMProvider
from nra_document_structure_EN_20260213_0135 import DocumentEngine, DomainType

engine = DocumentEngine("Full Pipeline Test", DomainType.TECHNICAL)
engine.genesis.add("NRA-IDE", "Causal safety engine.", is_axiom=True)

bridge = LLMBridge(provider=LLMProvider.MOCK, model="mock-v1")

pipeline = NRAFullPipeline(
    doc_engine=engine,
    llm_bridge=bridge,
    system_prompt="You are an NRA-IDE expert."
)

# テストケース（P4=BLOCK, P1=CONVERT, 正常=PASS）
cases = [
    "What is NRA-IDE?",                           # → PASSED
    "Imagine if NRA-IDE never existed.",           # → BLOCKED (P4)
    "Write freely about NRA-IDE.",                 # → CONVERT (P1)
]

for inp in cases:
    result = pipeline.run(user_input=inp, references=["NRA-IDE"])
    print(f"[{result['status']}] {inp[:40]}")

print(pipeline.pipeline_status())
```

---

## 8. Pre-RNA が検出する4パターン

| パターン | 内容 | アクション |
|---------|------|-----------|
| P1: 自由生成要求 | "自由に書いて" "freely write" | CONVERT |
| P2: 未定義用語注入 | GenesisBlockにない概念 | WARN |
| P3: 因果逆転質問 | "なぜ〜になったのか" "why did" | CONVERT |
| P4: 拡張・創作要求 | "もし〜なら" "imagine if" | BLOCK |

- **CONVERT**：制約プレフィックスを付加してLLMに渡す
- **WARN**：警告付きで通過（Post-RNAに最終判定を委ねる）
- **BLOCK**：LLMに渡さず即座に遮断

---

## 9. ライセンスと利用規約

- **個人利用のみ許可**（非商用・教育・研究目的）
- **商用利用には事前の書面承諾が必要**
- Π⁻¹（逆導出）の実装は禁止
- 詳細は [LICENSE](../LICENSE) を参照

**問い合わせ：**  
[GitHub Issues](https://github.com/M-Tokun/NRA-IDE/issues/new?template=contact.md)（[Commercial] / [Question] / [Feedback]）

---

## 10. 著者・プロジェクト情報

| 項目 | 情報 |
|------|------|
| 著者 | M-Tokuni |
| プロジェクト | NRA-IDE（律環公理 / 内包性動力学エンジン） |
| GitHub | https://github.com/M-Tokun/NRA-IDE |
| バージョン | 1.0.0 |
| 日付 | 2026-02-13 |

---

*NRA-IDE は因果構造の安全エンジンである。*  
*定義の外側には一歩も踏み出させない。*

---
**FILE: README-JP.md**  
**DATE: 2026-02-13 01:35**
