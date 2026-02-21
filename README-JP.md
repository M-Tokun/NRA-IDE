# NRA-IDE: 律環公理統合開発環境
**Nomological Ring Axioms – Integrated Development Environment**

<p align="center">
  <img src="./docs/NRA-IDE LOGO.jpg" width="400" alt="NRA-IDE LOGO">
</p>

---

## 🌍 For English Speakers

**Please see [README.md](./README.md) for English documentation.**

---

## 律環公理（Nomological Ring Axioms）とは

**線形（連続性・距離・意味）を基軸計算に用いず、  
張力構造と厚み・ゆらぎを持つ閾値によって  
閉じた世界構造と時間の状態を記述する公理体系です。**

---

## NRA-IDEとは

律環公理を実装した **統合開発環境（Integrated Development Environment）** です。

---

## なぜ閾値システムが必要か

従来の AI は **ブラックボックス** であり、判断根拠を物理的に説明できません。  
これは医療・自動運転などの高リスク領域では致命的です。

**閾値システムは：**

- AI の判断を **物理式で完全に説明可能** にする  
- **AI と人間の責任境界線** を明確にする  
- システムが「判断できない」ことを **正直に示す**

---

## 閾値システムの仕組み



\[
R = \frac{\delta}{\tau}
\]



- **δ（デルタ）**: 制約からのズレ（変位）  
- **τ（タウ）**: 許容範囲（張力の閾値）  
- **R**: 比率（R ≥ 1.0 で AI は判断停止）

| R の値 | 判定 | 意味 |
|--------|------|------|
| R < 1.0 | SAFE | AI が物理的根拠を提示 |
| R ≥ 1.0 | STOP | 人間が最終判断 |

この境界により、  
**AI は計算に徹し、倫理的判断は人間が担う** 構造が保証されます。

---
## Core Engine

## Core Engine

基礎実装は `nra-core/` に集約しています。

- 📄 [nra_ide_foundation_fixed_en.py](./nra-core/nra_ide_foundation_fixed_en.py) – 英語版  
- 📄 [nra_ide_foundation_fixed_jp.py](./nra-core/nra_ide_foundation_fixed_jp.py) – 日本語版  
- 📝 [Annotated Explanation (EN)](./nra-core/Nomological_Ring_Axioms_Code_Annotated_Explanation_Dual_Fluctuation_Stable.md)  
- 📝 [コード解説 (JP)](./nra-core/律環公理_コード付き解説_二重ゆらぎ安定版.md)  
- 📊 [検証プロット](./nra-core/nra_foundation_plot_2026-02-20_2355.png)

---

# 📂 主要プロジェクト

### 💎 NRA-TCM Parser（テキスト結晶化法）
**[./NRA-TCM Parser/](./NRA-TCM%20Parser/)**

- 情報の位相変換（100万トークン級ログの結晶化）  
- 動的モーメンタム（没頭／飛ばし読みの自動切替）  
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

# 📄 ドキュメント・サンプル

理論的背景や詳細な解説は `examples` ディレクトリにあります。

- **日本語ドキュメント**  
  → [./examples/JP/README_JP.md](./examples/JP/README_JP.md)

- **English Documentation**  
  → [./examples/EN/README_EN.md](./examples/EN/README_EN.md)

---

# 🔍 検索キーワード / Keywords

`ai-safety` `medical-ai` `text-mining` `crystallization`  
`cancer-treatment` `deterministic-computing` `fpga`  
`fail-safe` `autonomous-systems` `healthcare`  
`decision-support` `cascade-failure-prevention`  
`non-statistical` `physics-based` `structural-constraints`

---

# 🔗 外部リンク

- **Note 記事**: https://note.com/mtokuni  
- **Facebook**: https://www.facebook.com/tokuni.masa  

---

# 📜 ライセンス

本プロジェクトは **MIT License** の下で提供されています。

- 研究・個人・商用を含め、**無償で利用・改変・配布可能**  
- 再配布時には **著作権表示の保持が必要**

詳細は **[LICENSE](./LICENSE)** をご確認ください。

### 商用利用について

商用利用は MIT License に基づき許可されています。  
連絡は必須ではありませんが、可能であれば GitHub Issues にて  
一言ご連絡いただけると助かります。

---

# 📖 引用 / Citation

M‑Tokuni (2026).  
**NRA-IDE: 律環公理統合開発環境  
(Nomological Ring Axioms – Integrated Development Environment).**  
GitHub. https://github.com/M-Tokun/NRA-IDE

---

<p align="center">
  <strong>Status: Lighthouse（灯台）</strong><br>
  発見可能。売り込まない。ただし消えない。
</p>

