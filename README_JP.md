# NRA‑IDE: 律環公理 – 内包性動力学エンジン

### **Nomological Ring Axioms – Intensional Dynamics Engine**

[![CI](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml/badge.svg)](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

<p align="center">
  <img src="./docs/NRA-IDE_git.jpg" width="700" alt="NRA-IDE LOGO">
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

## なぜNRA-IDEは誤差を累積しないのか

機械式時計が精度を保てるのは、歯車が完璧だからではありません。
**脱進機が「完全な一歯分」という離散的なステップで進む**からです——小数点以下の残差は次のステップに持ち込まれません。

NRA-IDEはこの原則を実装しています。状態遷移を浮動小数点の連続値として処理するのではなく、
**整数位相ロック**で動作します。 各ステップは構造的に完結しており、引き継がれる残差が存在しません。

---

## 構造比率（Structural Ratio）と閾値システム

従来のブラックボックスAIとは異なり、判断根拠を物理的に説明するために **閾値（Threshold）** を用います。

$$
R = \frac{\delta}{\tau}
$$

- **δ（デルタ）**: 制約からの偏差（ズレ・変位）
- **τ（タウ）**: 許容境界（張力の閾値・厚み）
- **R**: 構造比率

---

## 📜 ライセンス

本プロジェクトは **MIT License** の下で提供されています。

- 研究・個人・商用を含め、**無償で利用・改変・配布可能**
- 再配布時には **著作権表示の保持が必要**
- 
 Copyright (c) 2026 M‑Tokuni

詳細は **[LICENSE](./LICENSE)** をご確認ください。

---

<p align="center">
  <strong>Status: Lighthouse（灯台）</strong>
</p>

---

[![M-Tokuni profile views](https://u8views.com/api/v1/github/profiles/214784860/views/day-week-month-total-count.svg)](https://u8views.com/github/M-Tokun)
