#　READ ME
<p align="center"> <img src="./docs/NRA-IDE LOGO.jpg" width="400" alt="NRA-IDE LOGO"> </p>
# NRA-IDE: Intensional Dynamics Project

## Nomological Ring Axioms & Intensional Dynamics Engine

> **System Status**: Reference Implementation v1.0
> **License**: BSD 3-Clause (Strict Causal Enforcement)

### 🌌 Project Overview

This repository implements the **NRA-IDE Project**, a framework for "Intensional Dynamics" where causal integrity (truthfulness of logic) precedes spatial accuracy.
本リポジトリは、空間的正確性よりも因果的整合性（論理の誠実さ）を優先する「内包的力学」を実装した、NRA-IDEプロジェクトの参照実装です。

#### 📦 Package Structure / 構成

* **`src/`**: Core engine implementation / エンジン基幹部
* `ide_core_safe.py`: Phase-lock logic & residual discarding / 位相ロックと端数廃棄
* `ide_firewall.py`: Spatial-to-Causal translation layer / 空間・因果変換レイヤー
* `ide_threshold_handler.py`: Safety ratio evaluation / 安全率評価と制御


* **`examples/`**: Proof-of-concept demonstrations / 実証デモ
* `HAN_Micro-POC_01.html`: Visual homeostasis demo / 恒常性維持の視覚デモ
* `HAN_Deep_Stress_Test.html`: Stress test with thread-blocking / スレッド占有型・極限負荷デモ（解説コメント付）



---

### 🚀 Quick Start / クイックスタート

#### 1. Experience the Physics (Demos) / 物理制御を体感する

We provide two levels of demonstration to show the "Elasticity" of HAN.
HANの「弾性」を体感するために、2つの深度のデモを用意しています。

* **[Demo 1: Visual Homeostasis (Standard)](https://www.google.com/search?q=./examples/HAN_Micro-POC_01.html)**
* *Best for understanding how the system maintains balance under varying loads.*
* システムが負荷に応じて柔軟にバランスを保つ様子を視覚的に理解できます。


* **[Demo 2: Deep Stress Test (Advanced)](https://www.google.com/search?q=./examples/HAN_Deep_Stress_Test.html)**
* *Simulates heavy CPU-blocking (80ms spikes) to show how HAN creates "breathing space" for the thread. Includes detailed logic comments.*
* 意図的なスレッド占有（80ms）を行い、HANがどのように「処理の隙間」を作り出すかを実証します。コード内の日本語コメントで論理を解説しています。



#### 2. Local Setup / ローカルセットアップ

```bash
# Clone the repository
git clone https://github.com/M-Tokun/NRA-IDE.git

# Run the threshold evaluation logic
cd NRA-IDE
python3 src/ide_threshold_handler.py

```

---

### 🏗️ Core Principles / 基本原則

The system enforces the following constraints via `src/ide_core_safe.py`:
`src/ide_core_safe.py` を通じ、以下の制約を物理的に強制します。

1. **CAUSAL DIODE**: No Inverse Kinematics. Distance is read-only.
* 逆算の禁止。距離は結果であり、入力ではありません。


2. **QUANTIZATION**: Discard float residuals to prevent error accumulation.
* 誤差蓄積を防ぐための端数廃棄。


3. **LIVENESS**: Homeostasis must be maintained;  is treated as failure.
* 恒常性維持。停止はシステム不全とみなします。



---

### 🤝 Request for Community Guidance / 物理学コミュニティの皆様へ

[English] I approach this project with great respect for physics. My background is in practical business (Agriculture & Management). I use neologisms to describe the "Intensional Dynamics" paradigm. If you find terminological inaccuracies, please guide me via GitHub Issues.

[日本語] 私は物理学に深い敬意を持っていますが、専門の研究者ではなく実業の背景を持つ者です。「内包的力学」というパラダイムを説明するため、一部に独自の用語定義を含みます。用語法に不正確な点があれば、ぜひ GitHub Issues にてご指導ください。

(C) 2026 NRA-IDE Project / M-Tokun


---

