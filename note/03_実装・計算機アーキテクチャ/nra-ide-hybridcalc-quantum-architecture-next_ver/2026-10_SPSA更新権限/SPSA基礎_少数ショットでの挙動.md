---
id: NOTE-SPSA-PRIMER-20261022
kind: note
created: 2026-10-22
title: SPSAの基本概要と量子コンピュータでの役割（少数ショット環境を含む）
status: draft
evidence: 出典（Spall 1992、Gidi ほか 2023、Periyasamy ほか 2024、Qiskit・PennyLane の資料）は本ファイルの記載のままで、2026-10-22時点では未照合。Spall 1992 の書誌は論文系列（2026-10_SPSA更新権限/）で照合済み
---

## 1. SPSAの基本概要と量子コンピュータでの役割

SPSAは、多数の未知パラメータを持つシステムの最適化を行うための**勾配法ベースの確率的最適化アルゴリズム**です。量子コンピュータの分野（Variational Quantum Eigensolver: VQEや量子ニューラルネットワーク: QNNのトレーニングなど）で非常によく使われます。

* **最大のメリット（回路評価回数の削減）**
* 通常の数値微分（有限差分法）では、パラメータ数 $p$ に対して $2p$ 回の量子回路の実行（評価）が必要になります。
* これに対し、**SPSAはパラメータ数 $p$ によらず、一律で「わずか2回」の回路評価**（正方向の摂動と負方向の摂動）だけで全パラメータの勾配を同時に推定できます。


* **更新の仕組み**
すべてのパラメータに対し、同時にランダムな微小摂動 $\Delta_k$ を与えて評価するため、パラメータ数が多い大規模な量子回路であっても計算コスト（回路の実行回数）を劇的に抑えられます。

---

## 2. 「少数ショット（Limited / Few Shots）」環境におけるSPSAの挙動

量子コンピュータでは、状態の測定結果が確率的に得られるため、期待値を高精度に得るためには多くの「ショット数（測定回数）」が必要です。しかし、実際のハードウェアでは時間的制約やノイズの影響から、ショット数を少なく（少数ショットに）せざるを得ない場面が多くあります。

* **ショットノイズに対する耐性**
SPSAはもともと確率的な近似勾配を用いるため、ある程度のノイズ（統計的ゆらぎ）に対して比較的頑健な性質を持っています。そのため、厳密な勾配を計算するパラメータシフト則（Parameter-Shift Rule）などに比べて、ショット数が限られた状況でも破綻しにくいという特徴があります。
* **少数ショット時の課題とトレードオフ**
* **勾配の分散増大:** ショット数が少なすぎると、測定のショットノイズがそのまま摂動による差分計算に直撃し、推定される勾配の分散（ブレ）が非常に大きくなります。
* **最適化の停滞・発散:** 勾配のノイズが大きすぎると、パラメータが最適値のまわりで大きく迷走したり、局所最適解から抜け出せなくなったりします。


* **対策**
少数ショットでSPSAを安定させるためには、学習率（learning rate）の減衰スケジュールや、摂動の大きさ（perturbation magnitude）のチューニング、あるいは分散を抑えるためのハイパーパラメータ調整が非常に重要になります。

---

## 3. 他の手法との比較

| 評価項目 | パラメータシフト則 (Parameter-Shift) | 有限差分法 (FDSA) | **SPSA** |
| --- | --- | --- | --- |
| **回路評価回数** | $2p$ 回（パラメータ数 $p$ に比例） | $2p$ 回 | **常に 2回**（パラメータ数に非依存） |
| **勾配の正確性** | 解析的に厳密 | 近似（パラメータ数に依存してコスト増） | 確率的近似（ランダム摂動） |
| **少数・ノイズ耐性** | ショット数が少ないと誤差に弱い | ショット数が少ないと誤差に弱い | **比較的ノイズに強いが、分散のケアが必要** |
| **主な用途** | 小〜中規模の量子回路 | 一般的な数値計算 | **大規模・多パラメータな量子回路（NISQ）** |

---

出典元：
1. SPSAの数学的・統計的基盤（原典）
SPSAは量子コンピュータ専用のアルゴリズムではなく、もともとは制御工学や統計学の分野で大規模システムの最適化手法として提案されたものです。

基礎論文（Foundational Paper）

著者: James C. Spall

タイトル: Multivariate stochastic approximation using a simultaneous perturbation gradient approximation

掲載誌: IEEE Transactions on Automatic Control, Vol. 37, No. 3, pp. 332-341, 1992.

概要: パラメータ数に依存せず常に「2回」の関数評価で全変数の勾配を近似できるという、SPSAの理論的根拠を示した最も重要な原典です。

2. 量子コンピュータ（VQE・量子機械学習）への応用・検証研究
NISQ（Noisy Intermediate-Scale Quantum）デバイスの変分量子固有ソルバー（VQE）や量子回路の最適化におけるSPSAの挙動を検証した代表的な研究です。

量子最適化アルゴリズムの比較・評価研究

著者: J. Gidi, B. Candia, A. D. Muñoz-Moller, et al.

タイトル: Stochastic optimization algorithms for quantum applications

掲載誌: Physical Review A, 108, 032409, 2023.

概要: 量子アプリケーションにおける各種確率的最適化手法（SPSAや2-SPSAなど）の性能や収束性を詳細に比較・解析した論文です。

ハイブリッド・勾配推定の拡張研究

著者: Maniraman Periyasamy, Axel Plinge, et al.

タイトル: Guided-SPSA: Simultaneous Perturbation Stochastic Approximation assisted by the Parameter Shift Rule

掲載誌: IEEE International Conference on Quantum Computing and Engineering (QCE), 2024.

概要: パラメータシフト則とSPSAを組み合わせ、量子ハードウェア上での効率的な勾配推定を行う手法を提案しています。

3. 主要な量子ソフトウェアフレームワークのドキュメント・チュートリアル
実務やシミュレーションでSPSAを利用する際の公式リファレンスです。

IBM Quantum / Qiskit Documentation

モジュール: qiskit.algorithms.optimizers.SPSA

概要: IBMの量子コンピューティング環境（Qiskit）において、VQE等の最適化に標準搭載されているSPSAオプティマイザの仕様と実装解説。

PennyLane Demos

タイトル: Optimization using SPSA (Xanadu社)

概要: 量子機械学習ライブラリ PennyLane における、SPSAを用いたパラメータ最適化の実装チュートリアル。