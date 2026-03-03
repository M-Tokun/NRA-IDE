# NRA-IDE: 律環公理 – 内包性動力
**Nomological Ring Axioms – Intensional Dynamics Engine**

<p align="center">
  <img src="./docs/NRA-IDE LOGO.jpg" width="400" alt="NRA-IDE LOGO">
</p>

---

## 🌍 For English Speakers

**Please see [README.md](./README.md) for English documentation.**

---

## 名称について

**律環公理（Nomological Ring Axioms）** は、本体系の正式名称です。  
**内包性動力** は、本プロジェクトにおける申請核名称です。  
**NRA-IDE** は、上記を統合して用いている現行プロジェクト表記です。

英語表記 **Intensional Dynamics Engine** は、既存記事・既存実装・既存参照との連続性を保つために、現時点では継続使用しています。  
ここでいう **Engine** は一般的な「統合開発環境」を意味せず、律環公理と内包性動力に基づく実装体系全体を指す旧来のプロジェクト表記です。

---

## 律環公理（Nomological Ring Axioms）とは

**線形（連続性・距離・意味）を基軸計算に用いず、  
制約構造と厚み・ゆらぎを持つ閾値によって、  
閉じた世界構造と時間の状態を記述する公理体系です。**

ここでいう **Ring** は抽象代数学における algebraic ring を指すものではなく、  
不可逆な閉鎖的連続構造を指します。

---

## NRA-IDEとは

**NRA-IDE は、律環公理と内包性動力を基礎にした実装体系です。**  
一般的な「統合開発環境（IDE）」ではありません。

本プロジェクトでは、**内包性動力** を、  
制約構造・閾値・閉世界制約に基づいて状態遷移を扱うための中核概念として用いています。

したがって、NRA-IDE は単一のソフトウェア製品名ではなく、  
**律環公理と内包性動力を基礎にした実装・記述・検証の総体** を指します。

---

## なぜ閾値システムが必要か

従来のシステムには **ブラックボックス化** が生じやすく、  
判断根拠や停止条件を物理的・構造的に説明できない場合があります。  
これは医療・自動運転・サーバー管理・航空・宇宙・水管理などの高リスク領域では致命的です。

**閾値システムは次の三点を目的とします。**

- 判断や状態遷移を **物理式および構造条件で説明可能** にする  
- **自律系と最終責任主体の境界線** を明確にする  
- システムが「判断できない」ことを **正直に示す**

---

## 閾値システムの基本式

\[
R = \frac{\delta}{\tau}
\]

- **δ（デルタ）**: 制約からのズレ（変位）  
- **τ（タウ）**: 許容範囲（厚みを持つ閾値）  
- **R**: 比率（R ≥ 1.0 で自律判定を停止または移譲）

| R の値 | 判定 | 意味 |
|--------|------|------|
| R < 1.0 | SAFE | 構造的・物理的根拠を提示可能 |
| R ≥ 1.0 | STOP | 最終判断を外部責任主体へ移譲 |

この境界により、  
**システムは計算・評価・提示に徹し、最終的な倫理判断および決定は外部責任主体が担う**  
という構造が保証されます。

---

## 基礎実装

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

# 📜 ライセンス

本プロジェクトは **MIT License** の下で提供されています。

- 研究・個人・商用を含め、**無償で利用・改変・配布可能**  
- 再配布時には **著作権表示の保持が必要**

詳細は **[LICENSE](./LICENSE)** をご確認ください。

---

## ⚠️ 注意 / Notice
**必ず倫理規定（人権・犯罪などの禁止事項）を読んでからご利用ください。**  
**Please make sure to read the Ethical Guidelines (prohibitions on human-rights violations, criminal use, etc.) before using this project.**

👉 倫理規定: **[ETHICS.md](./ETHICS.md)**

---

### 商用利用について

商用利用は MIT License に基づき許可されています。  
連絡は必須ではありませんが、可能であれば GitHub Issues にて  
一言ご連絡いただけると助かります。

---

# 📖 引用 / Citation

M-Tokuni (2026).  
**NRA-IDE: 律環公理 – 内包性動力  
(Nomological Ring Axioms – Intensional Dynamics Engine).**  
GitHub. https://github.com/M-Tokun/NRA-IDE

---

<p align="center">
  <strong>Status: Lighthouse（灯台）</strong><br>
</p>
