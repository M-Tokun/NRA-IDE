# NRA-IDE 実証デモ集（日本語版）
# NRA-IDE Examples — Japanese Edition
<!-- README_JP.md | examples/ | 2026-03-05 -->

---

## NRA-IDE とは

**律環公理 — 内包性動力学エンジン（Nomological Ring Axioms — Intensional Dynamics Engine）**

線形概念（連続性・距離・意味）を排除し、**張力構造（制約 → 力 → 変位）** を基本とした決定論的制御エンジンです。
従来手法がブラックボックス化する高リスク領域（医療AI・自動運転・インフラ）において、
**完全に説明可能かつ誤差が累積しない** 判定メカニズムを提供します。

---

## なぜNRA-IDEは誤差を累積しないのか

機械式時計が精度を保てるのは、歯車が完璧だからではありません。
**脱進機が「完全な一歯分」という離散的なステップで進む**からです——小数点以下の残差は次のステップに持ち込まれません。

NRA-IDEはこの原則を実装しています。状態遷移を浮動小数点の連続値として処理するのではなく、
**整数位相ロック**で動作します。各ステップは構造的に完結しており、引き継がれる残差が存在しません。

> **誤差が累積しないのは「補正しているから」ではなく、
> 「誤差が生じる構造になっていないから」です。**

以下のデモ群は、この差異を可視化・定量化するために設計されています。
実装の詳細（整数位相ロック・端数廃棄）は `nra-core/` を参照してください。

---

## 閾値システムの原理

$$R = \frac{\delta}{\tau}$$

| 記号 | 意味 | 説明 |
|------|------|------|
| **δ（デルタ）** | 制約からのズレ（ゆらぎ） | 物理的に直接測定される変位 |
| **τ（タウ）** | 許容範囲（厚み） | 設計時に定義された閾値 |
| **R** | 構造比率 | δ÷τ の値で判定を行う |

| R の値 | 判定 | 動作 |
|--------|------|------|
| R < 1.0 | **SAFE** | AIが物理的根拠を提示し処理続行 |
| R ≥ 1.0 | **STOP** | 構造限界に到達。AIは出力を停止 → 人間が最終判断 |

> **設計思想：** AIは計算に徹し、倫理的・最終判断は人間が担う。（責任の境界）

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

### ⚙️ STEP 4 — 脱進機の原理（準備中）

| # | ファイル | 内容 |
|---|---------|------|
| 06 | `06_Escapement_Principle_JP.html` *（準備中）* | **なぜ歯車は誤差を累積しないのか。** 浮動小数点ドリフト vs 整数位相ロックのアニメーション比較。NRA-IDEが誤差を構造的に排除する理由を可視化。 |

---

## 組み込み方法

制御対象の「偏差（δ）」と「許容範囲（τ）」を定義するだけで物理制御が開始されます。

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

本プロジェクトは **MIT License** の下で提供されています。
研究・個人・商用を含め、無償で利用・改変・配布可能です。
再配布時には以下の著作権表示の保持が必要です：

```javascript
// Powered by NRA-IDE. (c) 2026 M-Tokuni.
// Principle: L∧P∧C∧D Verified.
```

**利用前に必ず倫理規定をお読みください。**
禁止用途（兵器・監視・逆導出Π⁻¹・安全性未確保の機器への組み込み等）は
ライセンスとは独立した専用ファイルで定義しています：

👉 **[ETHICS.md](../../theory/ETHICS.md)**

ライセンス全文は **[LICENSE](../../LICENSE)** を参照してください。

**原則検証**: L∧P∧C∧D (Logic ∧ Physics ∧ Causality ∧ Determinism)

---

## 著者情報

**M-Tokuni（とおくに）**  
理論：律環公理（Nomological Ring Axioms）/ 内包性動力学エンジン（Intensional Dynamics Engine）

- **GitHub:** https://github.com/M-Tokun/NRA-IDE
- **Twitter/X:** https://x.com/m_tokuni
- **Facebook:** https://www.facebook.com/tokuni.masa
- **Note:** https://note.com/mtokuni
- **Blog:** https://mtokuni.blogspot.com/
- **Hatena:** https://mtokuni.hatenablog.com/

---

## 引用

```
M-Tokuni (2026). NRA-IDE: 律環公理 — 内包性動力学エンジン
(Nomological Ring Axioms — Intensional Dynamics Engine).
GitHub. https://github.com/M-Tokun/NRA-IDE
```

---

## 詳細ドキュメント

- **理論定義:** [`/theory/THEORY.md`](../../theory/THEORY.md)
- **基礎理論論文:** [`/theory/Foundational_Thesis.md`](../../theory/Foundational_Thesis.md)
- **倫理規定:** [`/theory/ETHICS.md`](../../theory/ETHICS.md)
- **コア実装:** [`/nra-core/`](../../nra-core/)

---

最新版の情報については、公式リポジトリをご確認ください。
