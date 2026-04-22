# NRA-IDE Universal Definition / 普遍的構造定義書

**Version**: 1.0  
**Last Updated**: 2026-01-27  
**Repository**: https://github.com/M-Tokun/NRA-IDE

---

## 概要 / Overview

このディレクトリには、NRA-IDE（Non-Reversible Architecture - Integrated Development Environment）の普遍的構造定義書が格納されています。

This directory contains the Universal Structural Definition for NRA-IDE (Non-Reversible Architecture - Integrated Development Environment).

---

## ドキュメント構成 / Document Structure

### 日本語版 / Japanese

📁 **[jp/](./jp/)**

| ファイル名 | 説明 | 読了時間 | 対象読者 |
|-----------|------|---------|---------|
| [NRA-IDE_Universal_Definition_v1_0_full.md](./jp/NRA-IDE_Universal_Definition_v1_0_final_20260127_1600.md) | **完全版** - 全8章の詳細定義 | 30-40分 | 全員（必読） |
| [NRA-IDE_Quick_Reference.md](./jp/NRA-IDE_Quick_Reference_jp.md) | **要点簡易版** - 核心のみ抽出 | 5分 | 意思決定者、初見者 |
| [NRA-IDE_Implementation_Guide.md](./jp/NRA-IDE_Implementation_Guide_jp.md) | **実装ガイド** - コード例と実装パターン | 20-30分 | エンジニア、実装者 |
| [NRA-IDE_Checklist.md](./jp/NRA-IDE_Checklist_jp.md) | **チェックリスト** - 100項目以上の検証項目 | 参照用 | 全員（運用時） |

### 英語版 / English

📁 **[en/](./en/)**

| File Name | Description | Reading Time | Target Audience |
|-----------|-------------|--------------|-----------------|
| NRA-IDE_Universal_Definition_v1_0_full.md | **Full Version** - Complete 8-chapter definition | 30-40 min | Everyone (Required) |
| NRA-IDE_Quick_Reference.md | **Quick Reference** - Core principles only | 5 min | Decision makers, First-time readers |
| NRA-IDE_Implementation_Guide.md | **Implementation Guide** - Code examples and patterns | 20-30 min | Engineers, Implementers |
| NRA-IDE_Checklist.md | **Checklist** - 100+ verification items | Reference | Everyone (During operation) |

*(English version: Translation in progress)*

---

## 推奨読了順序 / Recommended Reading Order

### 初見の方 / First-time Readers

1. **Quick Reference** (5分) - 核心理解
2. **Full Version** (30-40分) - 詳細理解
3. **Implementation Guide** (必要に応じて) - 実装時
4. **Checklist** (運用時) - 検証時

### 実装者 / Implementers

1. **Quick Reference** (5分) - 概要把握
2. **Implementation Guide** (20-30分) - 実装パターン学習
3. **Full Version** (参照) - 詳細確認
4. **Checklist** (継続使用) - 実装検証

### 管理者・意思決定者 / Managers & Decision Makers

1. **Quick Reference** (5分) - 核心把握
2. **Full Version** 第0-4章のみ (15分) - 問題の本質理解
3. **Checklist** (参照) - 運用監視

---

## 各章の内容 / Chapter Contents

### 第0章: 根本公理 / Chapter 0: The Zeroth Law
全ての問題の根源（剰余廃棄による構造崩壊）

### 第1章: 情報の劣化と保存 / Chapter 1: Information Degradation
意味処理 vs 構造処理、離散性の本質

### 第2章: 境界破断の物理現象 / Chapter 2: Boundary Rupture
善意のベクトル合成、相転移の条件

### 第3章: 侵入プロトコル / Chapter 3: Intrusion Protocols
能動的権限譲渡、招待の論理、責任の所在

### 第4章: 崩壊の方程式 / Chapter 4: Equations of Collapse
ベクトル方程式、認知の強制、不可逆性

### 第5章: 医療トリアージ適用 / Chapter 5: Medical Triage Application
リソース制約、諦めの原則=沈黙プロトコル

### 第6章: 企業リスク / Chapter 6: Enterprise Risks
人間の退化メカニズム、時間軸の絶望、探索禁止

### 第7章: 国家インフラ崩壊 / Chapter 7: Infrastructure Collapse
効率化と崩壊の崖、安全マージンの喪失

### 第8章: 解決策アーキテクチャ / Chapter 8: Solution Architecture
サンドイッチ構造、実装方針、ハイブリッド防御

---

## 核心原則 / Core Principles

```
諦める = 沈黙する
Resign = Silence

律環公理が適用されたAI = 沈黙するAI
RCA-compliant AI = Silent AI

情報提示 → [沈黙] → 人間判断 → ログ記録
Information → [Silence] → Human Decision → Logging
```

---

## 重要な実装仕様 / Critical Implementation Specs

### 1. 沈黙プロトコル / Silence Protocol
```python
if not possible:
    return "構造上不可能です。" + silence()
    # 代替案なし、提案なし、沈黙
    # No alternatives, no suggestions, silence
```

### 2. 探索禁止 / No Exploration
```
探索 = 世界境界の越境試行 = 構造破断
Exploration = Boundary crossing attempt = Structural rupture
```

### 3. 責任追跡 / Responsibility Tracking
```json
{
  "ai_suggestion": null,
  "human_decision": "...",
  "responsibility": "human"
}
```

---

## 関連リポジトリファイル / Related Repository Files

プロジェクトルートの以下のファイルも参照:

- `/NRA-IDE_The_Gate_Axioms__統合定義_.MD` - Gate Axioms定義
- `/nra_gate_kernel_CORE.py` - コアカーネル実装
- `/ide_core_safe.py` - セーフコア実装
- `/ide_firewall.py` - ファイアウォール実装
- `/ide_threshold_handler.py` - 閾値ハンドラ実装

---

## ライセンス / License

本ドキュメントは、リポジトリルートの[LICENSE.txt](../LICENSE.txt)に従います。

This document follows the [LICENSE.txt](../LICENSE.txt) in the repository root.

---

## 貢献 / Contributing

本定義書への貢献は、以下の方法で受け付けています:

1. GitHub Issues - 質問、提案、バグレポート

2. Discussions - 実装事例、フィードバック

---

- **GitHub**: https://github.com/M-Tokun/NRA-IDE　（律環公理・内包性動力学の研究
- **X (Twitter)**: https://x.com/m_tokuni (日常的なつぶやき）

---

## 更新履歴 / Change Log

- **2026-01-27**: v1.0 初版リリース - 完全版、要点簡易版、実装ガイド、チェックリスト
- **2026-01-27**: v1.0 Initial release - Full version, Quick reference, Implementation guide, Checklist

---

**最重要メッセージ / Critical Message**:

```
**「沈黙するAI」は、「嘘をつかない、余計なことを言わない、信頼できる部下」となる。**
```
---
* インターネットに書いてある論は,ほとんどがNRA-IDEを適用したAIによって私の考えを整形記述しています。
* 重要と思う部分については複数のAIによる確認をしています。
* 自然文が下手ですがご理解をお願いします。

