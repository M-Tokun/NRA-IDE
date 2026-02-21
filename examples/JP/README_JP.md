# NRA-IDE 実証デモ集（日本語版）
# NRA-IDE Examples — Japanese Edition
<!-- README_JP.md | examples/jp/ | 2026-02-09 -->

---

## NRA-IDE とは

**律環公理統合開発環境（Nomological Ring Axioms — Integrated Development Environment）**

線形概念（連続性・距離・意味）を排除し、**張力構造（制約 → 力 → 変位）** を基本とした決定論的制御エンジンです。
従来手法がブラックボックス化する高リスク領域（医療AI・自動運転・インフラ）において、
**完全に説明可能かつ誤差が累積しない** 判定メカニズムを提供します。

---

## 閾値システムの原理

$$R = \frac{\delta}{\tau}$$

| 記号 | 意味 | 説明 |
|------|------|------|
| **δ（デルタ）** | 制約からのズレ(ゆらぎ) | 物理的に直接測定される変位 |
| **τ（タウ）** | 許容範囲（厚み） | 設計時に定義された閾値 |
| **R** | 比率 | δ÷τ の値で判定を行う |

| R の値 | 判定 | 動作 |
|--------|------|------|
| R < 1.0 | **SAFE** | AIが物理的根拠を提示し処理続行 |
| R ≥ 1.0 | **STOP** | システム停止 → 人間が最終判断 |

> **設計思想：** AIは計算に徹し、倫理的/最終判断は人間が担う。（責任の境界）

---

## デモ一覧（推奨閲覧順）

ブラウザで開くだけで動作します（インストール不要）。

### 📚 STEP 1 — まず「なぜ？」を理解する

| # | ファイル | 内容 |
|---|---------|------|
| 01 | [01_Why_No_Distance_JP.html](./01_Why_No_Distance_JP.html) | **なぜ距離・微分積分・浮動小数点を使わないのか？** タブ切替で4つの視点から視覚的に解説。従来手法との根本的な違いを理解する入口。 |
| 02 | [02_Error_Accumulation_JP.html](./02_Error_Accumulation_JP.html) | **誤差積算の恐怖。** 同一初期値から10万ステップ走らせ、従来手法と律環公理の誤差蓄積を比較。医療・自動運転・金融それぞれの破綻ラインを表示。 |

### 🔬 STEP 2 — 動作の違いを体感する

| # | ファイル | 内容 |
|---|---------|------|
| 03 | [03_HAN_vs_Legacy_JP.html](./03_HAN_vs_Legacy_JP.html) | **HAN（非線形適応制御） vs Legacy（If-Then固定制御）のリアルタイム比較。** 外乱・突発負荷に対する追従性と安定性の差を、波形グラフで実証。 |
| 04 | [04_HAN_Stress_Test_JP.html](./04_HAN_Stress_Test_JP.html) | **意図的に80msの高負荷をかける極限実験。** Legacy は盲目的に命令を実行しFPSが崩壊。HAN は張力検知により負荷を適応的に軽減し、描画を維持。 |

### 📊 STEP 3 — 閾値メカニズムを可視化する

| # | ファイル | 内容 |
|---|---------|------|
| 05 | [05_IDE_Threshold_Visualizer_JP.html](./05_IDE_Threshold_Visualizer_JP.html) | **R = δ/τ の動的変化を位相スコープで表示。** 整数位相ロック・残差破棄のメカニズムをリアルタイムに確認。 |

---

## 組み込み方法

ご自身のプログラムに制御ロジックを組み込む場合、
制御対象の「歪み（Violation = δ）」と「許容範囲（τ）」を定義するだけで物理制御が開始されます。

```javascript
// 最小構成の例
function gate(delta, tau) {
    const R = delta / tau;
    if (R >= 1.0) return "STOP";   // FAIL_CLOSED
    return "SAFE";
}
```

**実装例：医療AI（がん治療薬剤投与制御）**
```javascript
// 腫瘍への薬剤到達可能性を物理的に検証
const tumorResistance = measureResistance();  // δ（腫瘍の抵抗力）
const infusionPressure = getPumpCapacity();   // τ（ポンプの投与圧力）

const deliveryStatus = gate(tumorResistance, infusionPressure);

if (deliveryStatus === "STOP") {
    alert("物理的到達不能を検出。医師の判断が必要です。");
    // AIは判断を停止し、人間（医師）に最終決定を委ねる
}
```

具体的な実装パターンは各デモのソースコード内に記載されています。

---

## 適用領域

### 🏥 医療AI
- **課題**: 腫瘍への薬剤到達可能性の不確実性
- **NRA解決策**: 投与経路の物理的整合性を検証
- **閾値**: R = （腫瘍抵抗力） / （投与圧力）

### 🚗 自動運転
- **課題**: ブラックボックス判断による安全性問題
- **NRA解決策**: 衝突回避の構造的制約検証
- **閾値**: R = （衝突余裕時間） / （制動能力）

### 🖥️ インフラ耐障害性
- **課題**: 分散システムのカスケード障害
- **NRA解決策**: 負荷限界監視による障害伝播防止
- **閾値**: R = （負荷超過量） / （バッファ容量）

| 領域 | δ（制約からのズレ） | τ（許容範囲） | R ≥ 1.0 の意味 |
|------|---------------------|---------------|-----------------|
| 医療AI | 腫瘍抵抗力 | 投与圧力 | 薬剤が物理的に届かない |
| 自動運転 | 障害物までの余裕 | 制動距離 | 衝突危険 → 緊急停止 |
| インフラ | 負荷超過量 | バッファサイズ | サーバー過負荷 → 遮断 |

---

## ライセンス

**Copyright (c) 2026 M-Tokuni**

### 個人・非商用利用
- 自由に利用・改変・配布可能
- ただし、クレジット表記必須：以下を配布資料・コード内に残してください

```javascript
// Powered by NRA-IDE. (c) 2026 M-Tokuni.
// Principle: L∧P∧C∧D Verified.
```

### 商用利用　-　（無償ですが、できればお問い合わせ欄に書いてください）

- お問い合わせ：[GitHub Issues](https://github.com/M-Tokun/NRA-IDE/issues)

### 禁止事項
以下の用途での使用を厳格に禁止します：

- **逆導出（Π⁻¹）**: 距離・座標から内部状態を導出する実装
- **兵器・軍事システム**: 武器、誘導、攻撃支援への利用
- **監視・弾圧システム**: 差別的制御システムへの利用
- **安全性未確保の医療機器・車両・航空機**への組み込み
- その他、物理的・心理的・社会的危害を引き起こす可能性のあるあらゆる応用

詳細は `LICENSE.txt` を参照してください。

**原則検証**: L∧P∧C∧D (Logic ∧ Physics ∧ Causality ∧ Determinism)

---

## 著者情報

**著者**: M-Tokuni (とおくに)  
**理論**: 律環公理（Nomological Ring Axioms）/ 内包性動力学エンジン（Intensional Dynamics Engine）

### 公式リンク
- **GitHub**: https://github.com/M-Tokun/NRA-IDE
- **Twitter/X**: https://x.com/m_tokuni
- **Facebook**: https://www.facebook.com/tokuni.masa

etc :https://note.com/mtokuni   https://mtokuni.blogspot.com/   https://mtokuni.hatenablog.com/
---

## 引用

学術的または技術的文脈で本プロジェクトを引用する場合：

```
M-Tokuni (2026). NRA-IDE: 律環公理統合開発環境
(Nomological Ring Axioms - Integrated Development Environment).
GitHub. https://github.com/M-Tokun/NRA-IDE
```

---

## 詳細ドキュメント

技術的な整合性原則（L∧P∧C∧D）やコア理論については、以下を参照してください：

- **理論基盤**: `/docs/` フォルダ内の技術文書
- **実装仕様**: 各HTMLファイルのソースコード内コメント
- **統合定義**: `NRA-IDE_The_Gate_Axioms__統合定義_.MD`

---

最新版の情報については、公式リポジトリをご確認ください。
