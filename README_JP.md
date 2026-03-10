# NRA‑IDE: 律環公理 – 内包性動力学エンジン

### **Nomological Ring Axioms – Intensional Dynamics Engine**

[![CI](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml/badge.svg)](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

<p align="center">
  <img src="./docs/NRA-IDE_LOGO.jpg" width="700" alt="NRA-IDE LOGO">
</p>

---

## 🌍 For English Speakers

**Please see [README.md](./README.md) for English documentation.**

---

## 核公理（Core Axiom）

## 「存在は生成である」 (Existence is Generation)

本体系は、存在を固定された実体として扱いません。  
**存在は「状態遷移」として現れる** と定義します。

ここでいう「生成」とは、無からの創造を意味するのではなく、存在が状態遷移として顕現することを指します。

---

## 基本構造：時間と距離の再定義

従来の線形計算（連続性・距離・意味）を基軸とせず、以下の物理的・構造的な観点から世界を記述します。

1. **時間 (Time)**
   - 時間は独立した「原因変数」として入力しません。
   - 時間は **状態遷移の順序** として記述されます。

2. **距離 (Distance)**
   - 距離は因果を生む「駆動因子」としては扱いません。
   - 距離は **状態変化の観測結果** として記録されます。

3. **張力 (Tension)**
   - 制約境界から生じる **復元的傾向** を指します。
   - 物理的な張力だけでなく、構造的な制約として扱われます。

---

## NRA‑IDEとは

**NRA‑IDE は「統合開発環境（Integrated Development Environment）」ではありません。**  
**律環公理を実装した「内包性動力学エンジン（Intensional Dynamics Engine）」です。**

- **意味生成を行わない**: IDE は「意味」を作り出すのではなく、構造状態の評価を担当します。
- **物理的説明性**: 線形計算では扱えない張力構造・閾値構造・閉世界制約を、物理的に説明可能な形で計算します。

---

## なぜNRA-IDEは誤差を累積しないのか

機械式時計が精度を保てるのは、歯車が完璧だからではありません。
**脱進機が「完全な一歯分」という離散的なステップで進む**からです——小数点以下の残差は次のステップに持ち込まれません。

NRA-IDEはこの原則を実装しています。状態遷移を浮動小数点の連続値として処理するのではなく、
**整数位相ロック**で動作します。各ステップは構造的に完結しており、引き継がれる残差が存在しません。

> **誤差が累積しないのは「補正しているから」ではなく、
> 「誤差が生じる構造になっていないから」です。**

実装の詳細（整数位相ロック・端数廃棄）は [`nra-core/`](./nra-core/) を参照してください。

---

## 構造比率（Structural Ratio）と閾値システム

従来のブラックボックスAIとは異なり、判断根拠を物理的に説明するために **閾値（Threshold）** を用います。

$$
R = \frac{\delta}{\tau}
$$

- **δ（デルタ）**: 制約からの偏差（ズレ・変位）
- **τ（タウ）**: 許容境界（張力の閾値・厚み）
- **R**: 構造比率

### 判定ロジック

| R の値 | 判定 | 動作 |
|--------|------|------|
| **R < 1.0** | **SAFE** | システムは物理的根拠に基づき稼働（AIが処理） |
| **R ≥ 1.0** | **STOP** | 構造限界に到達。**AIは判断・出力を停止** |

### Fail-Closed（フェイル・クローズド）

本システムにおける「Fail-Closed」は単なるシステムダウンを意味しません。
**「構造状態を維持したまま出力を抑制する設計」** を指します。
R ≥ 1.0 の時点でシステムは出力を停止し、最終的な判断は人間に委ねられます。

---

## 📄 論文・理論背景

- **[基礎理論論文](./theory/Foundational_Thesis.md)** *(日英併記)*  
  構造閾値による状態遷移の記述について詳細に論じた小論文。

- **[理論定義 (THEORY.md)](./theory/THEORY.md)**  
  公理系の詳細な定義ドキュメント。

---

## Core Engine

基礎実装は `nra-core/` に集約しています。

- 📄 [nra_ide_foundation_fixed_en.py](./nra-core/nra_ide_foundation_fixed_en.py) – 英語版  
- 📄 [nra_ide_foundation_fixed_jp.py](./nra-core/nra_ide_foundation_fixed_jp.py) – 日本語版  
- 📝 [コード解説 (JP)](./nra-core/律環公理_コード付き解説_二重ゆらぎ安定版.md)  
- 📊 [検証プロット](./nra-core/nra_foundation_plot_2026-02-20_2355.png)

---

## 📂 主要プロジェクト

### 💎 NRA‑TCM Parser（テキスト結晶化法）
**[./NRA-TCM Parser/](./NRA-TCM%20Parser/)**

- 情報の位相変換（100万トークン級ログの結晶化）  
- 動的モーメンタム（没頭・飛ばし読みの自動切替）  
- 特異点検知（文脈破綻下でも核心を逃さない）

---

### 🏥 がん治療支援システム
**[./NRA-IDE_CancerTreatmentSupport_System/](./NRA-IDE_CancerTreatmentSupport_System/)**

- 物理制約による転移リスク判定  
- FPGA 実装（決定論的計算）  
- 医療機器承認を見据えた完全トレーサビリティ  

---

### 🔗 カスケード故障防止
**[./HAN-Gate_Cascade-Failure-Prevention/](./HAN-Gate_Cascade-Failure-Prevention/)**

- サーバーインフラのカスケード故障防止  
- Envoy / Nginx 統合  
- 自動車安全・クリティカルインフラ対応  

---

## 🔍 検索キーワード / Keywords

`ai-safety` `medical-ai` `text-mining` `crystallization`  
`cancer-treatment` `deterministic-computing` `fpga`  
`fail-safe` `autonomous-systems` `healthcare`  
`decision-support` `cascade-failure-prevention`  
`non-statistical` `physics-based` `structural-constraints`

---

## 📜 ライセンス

本プロジェクトは **MIT License** の下で提供されています。

- 研究・個人・商用を含め、**無償で利用・改変・配布可能**  
- 再配布時には **著作権表示の保持が必要**

詳細は **[LICENSE](./LICENSE)** をご確認ください。

---

## ⚠️ 注意

**利用前に必ず倫理規定をお読みください。**  
禁止用途（兵器・監視・逆導出Π⁻¹・安全性未確保の機器への組み込み等）は
ライセンスとは独立した専用ファイルで定義しています：

👉 **[ETHICS.md](./theory/ETHICS.md)**

---

## 📖 引用 / Citation

M‑Tokuni (2026).  
**NRA‑IDE: 律環公理 – 内包性動力学エンジン  
(Nomological Ring Axioms – Intensional Dynamics Engine).**  
GitHub. https://github.com/M-Tokun/NRA-IDE

---

<p align="center">
  <strong>Status: Lighthouse（灯台）</strong>
</p>

---

[![M-Tokuni profile views](https://u8views.com/api/v1/github/profiles/214784860/views/day-week-month-total-count.svg)](https://u8views.com/github/M-Tokun)
