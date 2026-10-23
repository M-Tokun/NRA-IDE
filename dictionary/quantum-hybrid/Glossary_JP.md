# NRA-IDE 量子ハイブリッド用語集（日本語版）

**Version:** 0.1（骨格）  
**Author:** M-Tokuni  
**Document role:** 量子計算・SPSA・極低温ハードウェアなど、外部の技術用語と、NRA-IDEとの接続で生まれた用語の意味・正式名・経過・混同を引くための用語集。正典の定義を作らず、変えない  
**対になる英語版:** [Glossary_EN.md](./Glossary_EN.md)  
**範囲と運用:** [README.md](./README.md)

---

状態の凡例：【骨格】見出しと欄だけ。内容は未記入。【草稿】本文を書いた状態。【概念未照合】日本語と英語で、語の意味・訳語の対応を照合していない。【概念照合済み】意味と訳語の対応を、日英で照合した。【全文対訳未確認】全欄の英訳を、日本語と一対一で照合していない（確認したら【全文対訳確認済み】とする）。

---

## 索引

数字・英語名／略称・日本語の読みから、同じ項目へ移動できる。例えばT₁とエネルギー緩和時間は同じ項目を指す。

**数字から探す**

[4Kステージ](#^qh-cryo-cmos-4k-stage)

**A–Zから探す（英語名・略称）**

| 頭文字 | 項目 |
|---|---|
| A | [Atomicity](#^qh-atomicity) |
| B | [Barren plateau](#^qh-barren-plateau) / [Born approximation](#^qh-born-approximation) |
| C | [Calibration](#^qh-calibration) / [Coherence time (T₂)](#^qh-coherence-time-t2) / [Complete positivity](#^qh-complete-positivity) / [Completely positive trace-preserving map (CPTP)](#^qh-cptp-map) / [CP](#^qh-complete-positivity) / [CPTP](#^qh-cptp-map) / [Cryo-CMOS](#^qh-cryo-cmos) |
| D | [Data age (measurement age)](#^qh-data-age) / [Decoding](#^qh-decoding) / [Decoherence](#^qh-decoherence) / [Delayed-reference residual](#^qh-delayed-reference-residual) / [Density matrix](#^qh-density-matrix) / [DiscardVault](#^qh-discard-vault) / [Drift](#^qh-drift) |
| E | [Energy relaxation time (T₁)](#^qh-energy-relaxation-time-t1) / [Estimator bias](#^qh-estimator-bias) / [Expectation value](#^qh-expectation-value) |
| F | [Few-shot SPSA nominal calculation](#^qh-few-shot-spsa-nominal-calculation) / [Fixed-point representation](#^qh-fixed-point) / [Fractional carry-over](#^qh-fractional-carry) |
| G | [Gate error](#^qh-gate-error) / [GKSL](#^qh-lindblad-equation) |
| H | [Hamiltonian](#^qh-hamiltonian) |
| L | [Least significant bit (LSB)](#^qh-lsb) / [LFSR / Linear-feedback shift register](#^qh-lfsr) / [Lindblad (GKSL) equation](#^qh-lindblad-equation) / [LSB](#^qh-lsb) |
| M | [Markov approximation](#^qh-markov-approximation) / [Mixed state](#^qh-mixed-state) |
| N | [NISQ / Noisy Intermediate-Scale Quantum](#^qh-nisq) |
| O | [Observable expectation-value vector](#^qh-observable-expectation-vector) / [Open quantum system](#^qh-open-quantum-system) / [Overflow](#^qh-overflow) |
| P | [Pairwise skip of an update](#^qh-pair-skip) / [Parameter-shift rule](#^qh-parameter-shift-rule) / [Phase and relative phase](#^qh-quantum-phase) / [Pure state](#^qh-pure-state) |
| Q | [QEC / Quantum error correction](#^qh-qec) / [Quantization lock](#^qh-quantization-lock) / [Quantum channel](#^qh-cptp-map) / [Quantum coherence](#^qh-quantum-coherence) / [Quantum dynamical semigroup](#^qh-dynamical-semigroup) / [Quantum interference](#^qh-quantum-interference) / [Qubit](#^qh-qubit) |
| R | [Rate-limiting-stage principle](#^qh-rate-limiting-stage) |
| S | [SE](#^qh-standard-error) / [Secular approximation](#^qh-secular-approximation) / [Semigroup (quantum dynamical semigroup)](#^qh-dynamical-semigroup) / [Shot](#^qh-shot) / [Shot noise](#^qh-shot-noise) / [SPSA / Simultaneous Perturbation Stochastic Approximation](#^qh-spsa) / [Standard error](#^qh-standard-error) / [Superposition](#^qh-superposition) / [Syndrome](#^qh-syndrome) |
| T | [T₁](#^qh-energy-relaxation-time-t1) / [T₂](#^qh-coherence-time-t2) |
| U | [Union-Find decoder](#^qh-union-find-decoder) / [Update permission](#^qh-update-authority) |
| V | [Variance](#^qh-variance) / [Version management](#^qh-version-check) / [VQE / Variational Quantum Eigensolver](#^qh-vqe) |

**五十音で探す（日本語の読み）**

| 行 | 項目 |
|---|---|
| あ行 | [位相・相対位相](#^qh-quantum-phase) / [永年近似](#^qh-secular-approximation) / [エネルギー緩和時間（T₁）](#^qh-energy-relaxation-time-t1) / [オーバーフロー](#^qh-overflow) |
| か行 | [開放量子系](#^qh-open-quantum-system) / [重ね合わせ](#^qh-superposition) / [完全正値性](#^qh-complete-positivity) / [完全正値・トレース保存写像（CPTP）](#^qh-cptp-map) / [観測量期待値ベクトル](#^qh-observable-expectation-vector) / [期待値](#^qh-expectation-value) / [ゲート誤差](#^qh-gate-error) / [原子性](#^qh-atomicity) / [更新許可](#^qh-update-authority) / [較正（校正）](#^qh-calibration) / [固定小数点](#^qh-fixed-point) / [コヒーレンス時間（T₂）](#^qh-coherence-time-t2) / [混合状態](#^qh-mixed-state) |
| さ行 | [最下位ビット（LSB）](#^qh-lsb) / [純粋状態](#^qh-pure-state) / [少数ショットSPSA名目計算](#^qh-few-shot-spsa-nominal-calculation) / [ショット](#^qh-shot) / [ショットノイズ](#^qh-shot-noise) / [シンドローム](#^qh-syndrome) / [線形帰還シフトレジスタ（LFSR）](#^qh-lfsr) |
| た行 | [遅延参照残差（4月の旧称は残渣 r_t。正典の残差 ξ とは別）](#^qh-delayed-reference-residual) / [データ年齢（測定データの経過時間）](#^qh-data-age) / [デコヒーレンス](#^qh-decoherence) / [同時摂動確率近似（SPSA）](#^qh-spsa) / [ドリフト](#^qh-drift) |
| は行 | [バイアス（推定の偏り）](#^qh-estimator-bias) / [端数持ち越し](#^qh-fractional-carry) / [ハミルトニアン](#^qh-hamiltonian) / [パラメータシフト則](#^qh-parameter-shift-rule) / [バレンプラトー（勾配消失の台地）](#^qh-barren-plateau) / [版管理（パラメータ版・境界版・測定時刻）](#^qh-version-check) / [半群（量子力学的半群）](#^qh-dynamical-semigroup) / [標準誤差](#^qh-standard-error) / [復号](#^qh-decoding) / [分散](#^qh-variance) / [ペア見送り](#^qh-pair-skip) / [変分量子固有値ソルバ（VQE）](#^qh-vqe) / [ボルン近似（Born近似）](#^qh-born-approximation) |
| ま行 | [マルコフ近似](#^qh-markov-approximation) / [密度行列](#^qh-density-matrix) |
| ら行 | [律速段原則](#^qh-rate-limiting-stage) / [量子誤り訂正（QEC）](#^qh-qec) / [量子化ロック](#^qh-quantization-lock) / [量子干渉](#^qh-quantum-interference) / [量子コヒーレンス](#^qh-quantum-coherence) / [量子ビット](#^qh-qubit) / [リンドブラッド方程式（GKSL形式）](#^qh-lindblad-equation) |

---

## 旧称から現行の項目へ

旧い資料は消さずに残している。旧資料に出てくる語から、現行の概念へ辿るための索引である。

| 旧称 | 出てくる資料 | 現行の項目 |
|---|---|---|
| 残渣 $r_t$ （差の意味） | 4月の量子アーキテクチャ検討 | [遅延参照残差](#^qh-delayed-reference-residual) |
| 残渣（余り物・端数の意味） | 4月の量子アーキテクチャ検討、「残渣ベース」「残渣タンク」 | [端数持ち越し](#^qh-fractional-carry) |
| 二重揺らぎ名目計算 | 10月の初版論文 | [少数ショットSPSA名目計算](#^qh-few-shot-spsa-nominal-calculation) |
| 更新権限（最適化の更新の許可） | 10月の論文 v6.1 の本文 | [更新許可](#^qh-update-authority) |
| 4Kステージ（Cryo-CMOS） | 10月の初版論文 §1 | [4Kステージ](#^qh-cryo-cmos-4k-stage)、[Cryo-CMOS](#^qh-cryo-cmos) |
| 精密過剰計算（バレンプラトーの原因とした説明） | 10月の初版論文（撤回） | [バレンプラトー（勾配消失の台地）](#^qh-barren-plateau) |

---

## 用語本文

数字で始まる見出し、英字で始まる見出し、日本語の読みの順に並べる。数字は数の順、英字はA–Z順、日本語は五十音順とし、濁音・半濁音・小書きの仮名は対応する清音・通常の仮名に準じて並べる。

<a id="qh-cryo-cmos-4k-stage"></a>
### 4Kステージ
- 英語版：[4 K stage](./Glossary_EN.md#^qh-cryo-cmos-4k-stage) ^qh-cryo-cmos-4k-stage
- 区分：外部の技術用語
- 正式名と由来：4Kステージ。希釈冷凍機の約4 Kの冷却段（パルスチューブ冷凍機の第2段と、4Kフランジ）
- 意味：冷却能力は、冷凍機の構成と、評価する温度に強く依存する。メーカーが保証値として明記するのは主に混合室（20 mK）の冷却能力で、Bluefors では機種により14 μW超（XLD450sl）〜30 μW超（XLD1000sl）。4 K段のW数は、構成別の資料に載る（2026-10-23に確認）
  - Bluefors XLDsl-4K（標準の2台のパルスチューブ構成）：第2段の冷却能力は、4.2 Kで1.35 W（PT415-ENH）、2.35 W（PT425-ENH）、3 Kで0.9 W。4Kフランジ（負荷なし）は、3 Kで約100〜700 mW、4.5 Kで約1800〜2000 mW（ページの表の列の対応は、抽出では確実でない）
  - Bluefors XLD1000sl：4Kフランジで、4.5 Kで約2000 mW（構成別の公式資料）。XLD1000は3 Kで約700 mW
  - Oxford Instruments の Proteox LX：4K段に、静的な熱負荷に加えて4 W超を印加しても運転に影響しない（2台のパルスチューブ。板の温度の記載なし。Quantum Design Oxford のブログ、2025-06-09）。混合室は同時に25 μW超（20 mK）
  - 初版論文 §1 の「4 K段は数W」は、これらと矛盾しない範囲。構成と温度条件の違う値は、並べて比べない
- 本リポジトリでの捉え方：10月の論文系列では、境界接近比の評価対象を、4K段の熱収支とした（例示）。$\delta$ は付加熱負荷、$\tau$ は宣言した運転温度での冷却能力と、冷凍機の健全性（Cause-Side観測）による
- 混同注意（日付付き）：冷却能力を、その時点のステージ温度で評価してはならない。熱平衡では負荷によらず $R\equiv1$ になる（QH-20、中途計算 C06）。段ごとに別の評価対象として宣言し、一つの比に合成しない（2026-10-23）
  - 4Kステージ（冷却段・場所）と、そこに置く制御回路（[Cryo-CMOS](#^qh-cryo-cmos)）は別の概念である。項目を分けた（2026-10-23）
- 英日のすり合わせ：「4Kステージ」と書き、Cryo-CMOS はそのまま使う（確認済み 2026-10-23）
- 出典：論文系列 v6.1 §3.1。中途計算 C06。Bluefors（XLD 製品ページ、XLDsl-4K 製品ページ。2026-10-23に確認）。Quantum Design Oxford のブログ「Enabling Quantum Scale-Up」（2025-06-09）。段ごとの冷却能力の推定は arXiv:2502.01945（表の数値は未確認）
- 関連：[Cryo-CMOS](#^qh-cryo-cmos)、[律速段原則](#^qh-rate-limiting-stage)、[量子誤り訂正（QEC）](#^qh-qec)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-cryo-cmos"></a>
### Cryo-CMOS（極低温CMOS）
- 英語版：[Cryo-CMOS (cryogenic CMOS)](./Glossary_EN.md#^qh-cryo-cmos) ^qh-cryo-cmos
- 区分：外部の技術用語
- 正式名と由来：Cryo-CMOS（cryogenic CMOS）。極低温で動作するCMOS回路を指す一般的な技術用語
- 意味：極低温（4 K付近など）で動作するように設計・運用するCMOSの制御・読み出し回路。量子ビットの近くに置いて、室温からの配線を減らす狙いがある
- 本リポジトリでの捉え方：消費電力が、置かれた冷却段の熱負荷になる。10月の論文系列の熱収支の例では、Cryo-CMOS の消費電力は、4Kステージの熱負荷 $\delta$ の一部になりうる
- 混同注意（日付付き）：「4Kステージ」は冷却段（温度の段・場所）で、Cryo-CMOS はそこに置く回路（制御電子回路）である。別の概念で、一つの項目に合成しない（2026-10-23）
- 英日のすり合わせ：Cryo-CMOS は原語のまま使う（確認済みではない）
- 出典：一般的な技術用語（出典の照合はしていない）。論文系列 v6.1 §3.1
- 関連：[4Kステージ](#^qh-cryo-cmos-4k-stage)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-discard-vault"></a>
### DiscardVault（見送り・境界越えの保管庫）
- 英語版：[DiscardVault](./Glossary_EN.md#^qh-discard-vault) ^qh-discard-vault
- 区分：参照実装の固定名と本稿での用い方の区別
- 正式名と由来：`DiscardVault`。参照実装 v2.1（`nra-core/foundations/NRA-IDE_Architecture_public.py`）のクラス名
- 意味：参照実装では、`store` と `retrieve_all` を持つ、単純なリストの保管庫。捨てた項目を保存する
- 本リポジトリでの捉え方：10月の論文系列では、見送った測定ペア（値・時刻・摂動の種・理由）と、境界を越えた時刻・値・超過量の記録に使うことを提案している【拡張】。主系の更新には使わない
- 混同注意（日付付き）：初版は、「直交」「高周波」に分けて「100%復元を保証」と書いたが、撤回した。振幅の閾値による分割で、直交でも周波数分離でもない（QH-13。2026-10-23）
- 英日のすり合わせ：固定名のため、日英とも `DiscardVault` のまま書く（確認済み 2026-10-23）
- 出典：参照実装 v2.1。論文系列 v6.1 §4.6・§5.3。変遷記録 QH-13
- 関連：[ペア見送り](#^qh-pair-skip)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-nisq"></a>
### NISQ（ノイズのある中規模量子）
- 英語版：[Noisy Intermediate-Scale Quantum (NISQ)](./Glossary_EN.md#^qh-nisq) ^qh-nisq
- 区分：外部の技術用語
- 正式名と由来：Noisy Intermediate-Scale Quantum（略称 NISQ）。J. Preskill, Quantum 2, 79 (2018)
- 意味：ノイズがあり、十分なフォールトトレラント（誤り耐性）計算を備えない、中規模の量子デバイスの時代・条件。回路の深さを無制限には伸ばせない
- 本リポジトリでの捉え方：「原理的に計算できること」と「現行ハードウェア上で破綻する経路」を分けて論じるための条件として書く（4月完成版 §1）
- 混同注意（日付付き）：時代・条件の名前で、特定の装置の名前ではない。Preskill は、50〜100量子ビット程度の近い将来の装置を念頭に置いて述べている（arXivの要旨の記述）。「中規模」の量子ビット数の目安は、文献によって幅がある（2026-10-23）
- 英日のすり合わせ：略称NISQを使う。日本語は「ノイズのある中規模量子」と補い、「雑音つき」だけには訳さない（確認済み 2026-10-23）
- 出典：Preskill, Quantum 2, 79 (2018)、DOI 10.22331/q-2018-08-06-79（2026-10-23に検索で確認）。4月完成版 §1
- 関連：[VQE](#^qh-vqe)、[量子誤り訂正（QEC）](#^qh-qec)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-union-find-decoder"></a>
### Union-Find復号器
- 英語版：[Union-Find decoder](./Glossary_EN.md#^qh-union-find-decoder) ^qh-union-find-decoder
- 区分：外部の技術用語
- 正式名と由来：Union-Find復号器（Union-Find decoder）。Delfosse・Nickerson, Quantum 5, 595 (2021)。FPGA実装は Liyanage ほか, arXiv:2406.08491 (2024)
- 意味：表面符号などのシンドロームのグラフ上で、クラスタを成長・併合して誤りを推定する、ほぼ線形時間の復号法
- 本リポジトリでの捉え方：FPGA実装の例として、Liyanage ほかは、Xilinx VCU129 上で、符号距離21で1測定ラウンドあたり平均11.5 ns（0.1%の現象論的ノイズ）、符号距離17で23.7 ns（同等の回路レベルのノイズ。要旨の表現）、資源効率を優先した構成（Helios）の符号距離51で544 nsと報告している（arXivの要旨）。ノイズ条件と構成の異なる値は、並べて比べない。符号距離51のノイズ条件は、要旨の抜粋では未確認
- 混同注意（日付付き）：距離評価をマンハッタン距離にして、元の復号性能が保たれる、とは主張しない。一様な重みの正方格子では、最短経路の長さと一致するが、回路レベルのノイズで斜めの辺や重みの不均一が入ると差が出る（論文系列 v6.1 §4.1。2026-10-23）
- 英日のすり合わせ：「Union-Find」は手法名として原語のまま使い、「併合探索」とは書かない（確認済み 2026-10-23）
- 出典：Delfosse・Nickerson, Quantum 5, 595 (2021)、DOI 10.22331/q-2021-12-02-595。最悪の計算量は $O(n\,\alpha(n))$ （$n$ は物理量子ビット数、$\alpha$ はアッカーマン関数の逆関数）（2026-10-23に検索で確認）。Liyanage ほか（arXivのページで要旨を確認済み）
- 関連：[量子誤り訂正（QEC）](#^qh-qec)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-quantum-phase"></a>
### 位相・相対位相
- 英語版：[Phase and relative phase](./Glossary_EN.md#^qh-quantum-phase) ^qh-quantum-phase
- 区分：外部の技術用語
- 正式名と由来：Phase（位相）、relative phase（相対位相）。波や複素振幅の角度を表す語で、量子状態では成分間の位相差が干渉に関わる
- 意味：$a\lvert0\rangle+b e^{i\phi}\lvert1\rangle$ （$a,b$ を正の実数とし、$a^2+b^2=1$ とした表現）では、$\phi$ が二成分の相対位相である。位相は波の周期のどの位置にあるかに対応する角度であり、振幅の大きさとは別の情報
- 本リポジトリでの捉え方：デコヒーレンスやT₂の説明では、量子状態の相対位相を指す。NRA-IDEの正典語「遷移位相」とは区別する
- 混同注意（日付付き）：状態全体に同じ位相を掛ける「全体位相」は、単独では測定確率を変えない。相対位相が変わっても、0・1を測るだけでは違いが見えない場合があり、干渉を読み出す測定が必要になる（2026-10-24）
- 英日のすり合わせ：Phase と relative phase を「位相」「相対位相」と対応させる案。正典の「遷移位相」の説明へ量子の位相を代入しない（2026-10-24、概念照合待ち）
- 出典：[IBM Quantum Learning「Superposition with Qiskit」](https://quantum.cloud.ibm.com/learning/en/modules/quantum-mechanics/superposition-with-qiskit) の相対位相・干渉の説明（2026-10-24に本文確認）
- 関連：[重ね合わせ](#^qh-superposition)、[量子干渉](#^qh-quantum-interference)、[量子コヒーレンス](#^qh-quantum-coherence)、正典の[遷移位相](../NRA-IDE_Dictionary_JP.md#^transition-phase)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-secular-approximation"></a>
### 永年近似
- 英語版：[Secular approximation](./Glossary_EN.md#^qh-secular-approximation) ^qh-secular-approximation
- 区分：外部の技術用語
- 正式名と由来：Secular approximation。主方程式の導出における時間平均の近似として用いる。
- 意味：相互作用描像などで現れる、異なる遷移周波数による速い振動項を時間平均で除く手順。残す項と除く項を分けられる周波数差と時間尺度が必要になる。
- 本リポジトリでの捉え方：Lindblad形式を得る典型的な導出の一部。近似前のモデルと、除いた結合項を記録する。
- 混同注意（日付付き）：周波数が近い、または縮退した遷移を一律に除いてよいわけではない。ハミルトニアン段階の回転波近似と無条件に同じ操作とは扱わない。（2026-10-24）
- 英日のすり合わせ：Secular approximation を「永年近似」とする案。「長時間なら何でも平均してよい」という意味にはしない。
- 出典：[QuTiP：Lindblad Master Equation Solver](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html)、[GKSL詳説](./details/Lindblad_GKSL_JP.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[ボルン近似（Born近似）](#^qh-born-approximation)、[マルコフ近似](#^qh-markov-approximation)、[ハミルトニアン](#^qh-hamiltonian)、[リンドブラッド方程式（GKSL形式）](#^qh-lindblad-equation)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-energy-relaxation-time-t1"></a>
### エネルギー緩和時間（T₁）
- 英語版：[Energy relaxation time (T₁)](./Glossary_EN.md#^qh-energy-relaxation-time-t1) ^qh-energy-relaxation-time-t1
- 区分：外部の技術用語
- 正式名と由来：Energy relaxation time、longitudinal relaxation time（縦緩和時間）、記号 $T_1$ 。励起状態の占有率が平衡値へ戻る過程の時間尺度
- 意味：環境とのエネルギー交換によって、量子ビットの励起状態の割合が変化する速さを表す。上向きの励起を無視でき、最初に励起状態へ準備した指数減衰モデルでは、励起状態に残る確率は $p_1(t)=e^{-t/T_1}$ 。単位は秒
- 本リポジトリでの捉え方：デコヒーレンスを説明するとき、エネルギー交換を伴う緩和と、エネルギー交換を伴わない位相の乱れを区別するための基礎語
- 混同注意（日付付き）：T₁とT₂は同じ量ではない。有限温度で上向きの励起が無視できない場合、励起状態の割合はゼロではなく、その条件の平衡値へ向かう。T₁の大きさだけでゲート精度や装置全体の安全性を判定しない（2026-10-24）
- 英日のすり合わせ：Energy relaxation time (T₁) を「エネルギー緩和時間（T₁）」とする案。「緩和時間」だけではT₂などと区別できないため、見出しに対象を添える（2026-10-24、概念照合待ち）
- 出典：[IBM Quantum Learning「Noise and errors」](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/noise-and-errors)、[Qiskit Aer「thermal_relaxation_error」](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.thermal_relaxation_error.html)（2026-10-24に本文確認）
- 関連：[コヒーレンス時間（T₂）](#^qh-coherence-time-t2)、[デコヒーレンス](#^qh-decoherence)、[量子ビット](#^qh-qubit)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-overflow"></a>
### オーバーフロー
- 英語版：[Overflow](./Glossary_EN.md#^qh-overflow) ^qh-overflow
- 区分：外部の技術用語
- 正式名と由来：Overflow。数値表現で表現可能範囲を超えること。
- 意味：演算結果が、指定したビット幅と数値形式で表せる範囲を超えること。例として符号付き4ビット整数の範囲はマイナス8から7で、7に1を加えた数学的な結果8は表せない。
- 本リポジトリでの捉え方：端数持ち越しの蓄積器や固定小数点演算では、結果だけでなく中間値の範囲も確認する。飽和や異常検知の方針は実装ごとに宣言する。
- 混同注意（日付付き）：折り返し、飽和、例外などの扱いは同じではない。言語・型によっては符号付きオーバーフローが未定義であり、必ず折り返すとは言えない。（2026-10-24）
- 英日のすり合わせ：Overflow を「オーバーフロー」とする案。
- 出典：[Arm CMSIS-DSP：Fixed point datatypes](https://arm-software.github.io/CMSIS-DSP/latest/group__FIXED.html)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[固定小数点](#^qh-fixed-point)、[最下位ビット（LSB）](#^qh-lsb)、[端数持ち越し](#^qh-fractional-carry)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-open-quantum-system"></a>
### 開放量子系
- 英語版：[Open quantum system](./Glossary_EN.md#^qh-open-quantum-system) ^qh-open-quantum-system
- 区分：外部の技術用語
- 正式名と由来：Open quantum system。環境との相互作用を含めて対象を考える、量子力学の標準語。
- 意味：周囲の環境と相互作用する量子系。対象だけの状態は、対象と環境を合わせた状態から、環境の自由度を除いて得る密度行列で表す。情報やエネルギーの交換が対象の時間発展に影響する。
- 本リポジトリでの捉え方：4月案のLindbladモデルの対象。ただし開放量子系であることだけから、マルコフ近似やGKSL形式の妥当性は導けない。
- 混同注意（日付付き）：対象と環境を合わせた記述と、対象だけの記述を区別する。対象のコヒーレンス喪失を、全体の情報の消滅と同一視しない。（2026-10-24）
- 英日のすり合わせ：Open quantum system を「開放量子系」とする案。「開いた系」という一般表現だけで境界条件を省略しない。
- 出典：[QuTiP：Lindblad Master Equation Solver](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html)、[GKSL詳説](./details/Lindblad_GKSL_JP.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[密度行列](#^qh-density-matrix)、[デコヒーレンス](#^qh-decoherence)、[マルコフ近似](#^qh-markov-approximation)、[リンドブラッド方程式（GKSL形式）](#^qh-lindblad-equation)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-superposition"></a>
### 重ね合わせ
- 英語版：[Superposition](./Glossary_EN.md#^qh-superposition) ^qh-superposition
- 区分：外部の技術用語
- 正式名と由来：Superposition。量子状態を、選んだ基準状態の確率振幅の和として表すときの標準語
- 意味：例えば $a\lvert0\rangle+b\lvert1\rangle$ のように、二つの基準状態の成分を含む状態。係数は確率そのものではなく確率振幅であり、その絶対値の二乗が各測定結果の確率になる。どの基準を選ぶかによって重ね合わせの表し方は変わる
- 本リポジトリでの捉え方：量子測定で古典側が受け取るのは、各ショットの結果とその集計である。状態を数式で表せることと、実機の未知状態の係数をすべて知っていることを分ける
- 混同注意（日付付き）：0と1のどちらかが既に決まっていて不明なだけの確率的な混合と、重ね合わせは同じではない。同じ0・1の測定確率でも、相対位相によって別の測定の統計が変わり得る（2026-10-24）
- 英日のすり合わせ：Superposition は「重ね合わせ」とする案。「同時に全結果が読める」という説明は用いない（2026-10-24、概念照合待ち）
- 出典：[IBM Quantum Learning「Superposition with Qiskit」](https://quantum.cloud.ibm.com/learning/en/modules/quantum-mechanics/superposition-with-qiskit)（2026-10-24に本文確認）
- 関連：[量子ビット](#^qh-qubit)、[位相・相対位相](#^qh-quantum-phase)、[量子干渉](#^qh-quantum-interference)、[密度行列](#^qh-density-matrix)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-complete-positivity"></a>
### 完全正値性
- 英語版：[Complete positivity](./Glossary_EN.md#^qh-complete-positivity) ^qh-complete-positivity
- 区分：外部の技術用語
- 正式名と由来：Complete positivity（CP）。量子情報における線形写像の性質。
- 意味：対象への写像を任意の補助系の恒等写像と組み合わせても、結合系の半正定値性を保つ性質。対象だけの正値性を保つという条件より強い。
- 本リポジトリでの捉え方：GKSL生成子が与える量子チャネルの数学的な健全性を読むための語。補助系ともつれた入力にも矛盾する負の確率を作らないために必要になる。
- 混同注意（日付付き）：完全正値性だけではトレース保存とは限らない。また「完全」は、熱的安全性や計算の正答を保証するという意味ではない。（2026-10-24）
- 英日のすり合わせ：Complete positivity を「完全正値性」とし、略称CPを併記する案。
- 出典：[IBM Quantum：Quantum channel basics](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/quantum-channel-basics)、[IBM Quantum：Channel representations](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/representations-of-channels)、[GKSL詳説](./details/Lindblad_GKSL_JP.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[完全正値・トレース保存写像（CPTP）](#^qh-cptp-map)、[密度行列](#^qh-density-matrix)、[半群（量子力学的半群）](#^qh-dynamical-semigroup)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-cptp-map"></a>
### 完全正値・トレース保存写像（CPTP）
- 英語版：[Completely positive trace-preserving map (CPTP)](./Glossary_EN.md#^qh-cptp-map) ^qh-cptp-map
- 区分：外部の技術用語
- 正式名と由来：Completely positive trace-preserving map（CPTP）。量子チャネルを表す標準的な数学用語。
- 意味：完全正値性とトレース保存をともに満たす線形写像。正規化された密度行列を、確率の総和を保つ密度行列へ移す。系だけでなく補助系と組み合わせた入力にも適用できる。
- 本リポジトリでの捉え方：GKSL式の解析的な時間発展を評価する条件。式がCPTPであることと、任意の数値積分法が正値性を保つことは分けて確認する。
- 混同注意（日付付き）：条件付きの測定結果だけを取り出す操作は、正規化前にはトレースを減らす場合がある。すべての条件付き操作をCPTP写像と呼ばない。（2026-10-24）
- 英日のすり合わせ：CPTPは略称のまま使い、完全正値とトレース保存の二条件を展開する案。TPはtrace-preserving。
- 出典：[IBM Quantum：Quantum channel basics](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/quantum-channel-basics)、[GKSL詳説](./details/Lindblad_GKSL_JP.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[完全正値性](#^qh-complete-positivity)、[半群（量子力学的半群）](#^qh-dynamical-semigroup)、[リンドブラッド方程式（GKSL形式）](#^qh-lindblad-equation)、[密度行列](#^qh-density-matrix)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-observable-expectation-vector"></a>
### 観測量期待値ベクトル
- 英語版：[Observable expectation-value vector](./Glossary_EN.md#^qh-observable-expectation-vector) ^qh-observable-expectation-vector
- 区分：接続で生まれた用語（4月B-2）
- 正式名と由来：観測量期待値ベクトル $z_t$ 。2026-04-21の4月 B-2 で確定（状態記述子）
- 意味：判定層へ渡す状態記述子。密度行列そのものではなく、測定できる観測量 $O_i$ の期待値 $\langle O_i\rangle$ を並べたベクトル。未知の量子状態の完全な複製を要求せず、古典の記録として保存できる
- 本リポジトリでの捉え方：状態そのものではなく、観測目的に対して定義した記述子と書く。遅延参照 $z^{\mathrm{ref}}_{t-\ell}$ と比較できる
- 混同注意（日付付き）：「全体保持」は、全状態の列挙ではない（QH-03、変遷記録）。観測量の選び方に依存し、選んだ観測量が重要な変化を識別できなければ、判定は意味を持たない（10月論文 v6.1 §7）（2026-10-23）
- 英日のすり合わせ：Observable expectation-value vector。「観測量」は物理量（observable）の訳で、観測された値（observation）とは別（確認済み 2026-10-23）
- 出典：4月 B-2（`NRA-IDE_QuantumArchitecture_NextVer_B1toB3_…`）。4月完成版 §5
- 関連：[遅延参照残差](#^qh-delayed-reference-residual)、[リンドブラッド方程式（GKSL形式）](#^qh-lindblad-equation)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-expectation-value"></a>
### 期待値
- 英語版：[Expectation value](./Glossary_EN.md#^qh-expectation-value) ^qh-expectation-value
- 区分：外部の技術用語
- 正式名と由来：Expectation value。確率・統計と量子力学で用いる標準語。本項では、とくに量子測定結果の確率分布に対する平均を扱う
- 意味：起こり得る測定値を、それぞれが出る確率で重み付けして足した値。有限次元の量子状態の密度行列を $\rho$ 、観測量をOとすると、$\langle O\rangle=\mathrm{Tr}(\rho O)$ 。Trは行列の対角成分の和を表す
- 本リポジトリでの捉え方：4月の状態記述子は期待値を並べたベクトルである。実機で有限ショットから得る標本平均は期待値の推定値として扱い、測定回数と不確かさを付す
- 混同注意（日付付き）：期待値は「期待する望ましい値」ではない。また、1回の測定でその値が出るとは限らない。例えば結果が0と1で確率が等しいとき、期待値は0.5だが、各測定結果は0か1である（2026-10-24）
- 英日のすり合わせ：Expectation value を「期待値」とする案。「観測値」「標本平均」「基準値」とは区別する（2026-10-24、概念照合待ち）
- 出典：[IBM Quantum Learning「Cost functions」](https://quantum.cloud.ibm.com/learning/en/courses/variational-algorithm-design/cost-functions) の期待値の定義（2026-10-24に本文確認）。[4月完成版](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §5
- 関連：[観測量期待値ベクトル](#^qh-observable-expectation-vector)、[密度行列](#^qh-density-matrix)、[ショットノイズ](#^qh-shot-noise)、正典の[観測値](../NRA-IDE_Dictionary_JP.md#^observation-value)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-gate-error"></a>
### ゲート誤差
- 英語版：[Gate error](./Glossary_EN.md#^qh-gate-error) ^qh-gate-error
- 区分：外部の技術用語
- 正式名と由来：Gate error。量子ゲートの理想操作と実際の操作の違いを表す標準語
- 意味：量子状態へ施す操作が、意図した操作からずれること。例えば回転角の系統的なずれや、ゲート動作中の環境との相互作用がある。繰り返し同じ向きにずれる成分と、確率的に変わる成分を区別する
- 本リポジトリでの捉え方：4月の四層構造のゲート層に関わる。誤差の尺度、測定方法、回路深さ、相関の仮定を付して扱い、ゲート数だけから蓄積を断定しない
- 混同注意（日付付き）：ゲート誤差はすべてデコヒーレンスとは限らず、測定ショット数を増やすだけで除去できるものでもない。ゲート忠実度、平均ゲート誤差、回路の出力誤り率は、定義を示さず同じ数値として扱わない（2026-10-24）
- 英日のすり合わせ：Gate error を「ゲート誤差」とする案。error rate を使う場合は「誤差率」とし、どの評価尺度の率かを明示する（2026-10-24、概念照合待ち）
- 出典：[IBM Quantum Learning「Noise and errors」](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/noise-and-errors) の不完全なゲート操作・コヒーレント誤差の説明（2026-10-24に本文確認）。[4月完成版](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §6.1
- 関連：[デコヒーレンス](#^qh-decoherence)、[ショットノイズ](#^qh-shot-noise)、[量子誤り訂正（QEC）](#^qh-qec)、[律速段原則](#^qh-rate-limiting-stage)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-atomicity"></a>
### 原子性
- 英語版：[Atomicity](./Glossary_EN.md#^qh-atomicity) ^qh-atomicity
- 区分：外部の技術用語
- 正式名と由来：Atomicity。並行処理やトランザクションの用語。
- 意味：対象とする操作を、宣言した観測範囲で分割できない一つの操作として扱う性質。データベースではトランザクションの全体が成立するか、全体が取り消されるかという性質を指す。中間状態の可視性は隔離性も関係する。
- 本リポジトリでの捉え方：版の照合から更新の反映までに別の更新が割り込む問題を考えるための語。単一変数の比較交換だけで、複数項目の照合と反映まで保護できるとは限らない。
- 混同注意（日付付き）：量子や原子の物理用語ではない。メモリ操作、永続化、外部装置の動作は保護範囲が異なる。原子性だけで古いデータや権限誤りは防げない。（2026-10-24）
- 英日のすり合わせ：Atomicity を「原子性」とする案。保護対象と観測範囲を明記する。
- 出典：[Microsoft：InterlockedCompareExchange](https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-interlockedcompareexchange)、[PostgreSQL：Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)、[10月論文 v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[版管理（パラメータ版・境界版・測定時刻）](#^qh-version-check)、[更新許可](#^qh-update-authority)、[データ年齢（測定データの経過時間）](#^qh-data-age)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-update-authority"></a>
### 更新許可
- 英語版：[Update permission](./Glossary_EN.md#^qh-update-authority) ^qh-update-authority
- 区分：接続で生まれた用語（10月）
- 正式名と由来：更新許可（Update permission）。10月の論文 v6.1 の中心命題で、「更新権限」と呼んでいた語（2026-10-23に改名。論文の本文は旧称のまま）
- 意味：最適化の更新を適用してよいかどうかの許可。境界・時刻・版・許可を適用の時点で再確認し、許可のない更新を通さない。$G_k\in\{0,1\}$
- 本リポジトリでの捉え方：$G_k=0$ は、物理系が停止したことではなく、その最適化更新の許可がないことを意味する。熱的な安全性、QEC の精度、最適化の収束とは別に立証する
- 混同注意（日付付き）：正典 AXIOMS §14 の「更新権限」（Cause-Side の固定項目：更新権限・更新経路・出所など）と同名になるため、この語は「更新許可」と呼ぶ（2026-10-23）。当初は「更新権限」と書いていた。正典の「更新権限」は、Cause-Side の更新の規則・出所の固定で、最適化パラメータの更新の許可とは別の文脈
- 英日のすり合わせ：英語は Update permission（確認済み 2026-10-23）。正典側の「更新権限」の英語表記は update authority である（FORMULA §6、THEORY、SANDWICH_ARCH、基礎論文、辞書の評価スナップショット、axioms.json で確認）。このため、旧称の Update authority は、英語でも正典の語と同名になる。Update permission と書き分けて区別する
- 出典：論文系列 v6.1 §4.2〜4.3。AXIOMS §14
- 関連：[ペア見送り](#^qh-pair-skip)、[少数ショットSPSA名目計算](#^qh-few-shot-spsa-nominal-calculation)。正典の「更新権限」（update authority）は、辞書の [評価スナップショット](../NRA-IDE_Dictionary_JP.md#^evaluation-snapshot) を参照
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-calibration"></a>
### 較正（校正）
- 英語版：[Calibration](./Glossary_EN.md#^qh-calibration) ^qh-calibration
- 区分：外部の技術用語
- 正式名と由来：Calibration。計測の標準語。VIM 2.39の日本語では通常「校正」。論文側の「較正」からも同じ項目を引けるようにする。
- 意味：指定した条件で、標準が与える値とその不確かさを、計器の指示値とその不確かさへ関係付け、その関係を測定結果へ利用できるようにする操作。
- 本リポジトリでの捉え方：読み出しや制御の設定が、いつ・どの条件で確かめられたかを読むための語。本項の追加は、論文や実機の較正を実施したという意味ではない。
- 混同注意（日付付き）：較正と装置の調整は異なる。較正しただけで誤差がゼロになるわけではなく、条件変更やドリフトで有効性が変わり得る。適合の検証とも区別する。（2026-10-24）
- 英日のすり合わせ：Calibration を「較正（校正）」とする案。表記の違いを別概念として分割しない。
- 出典：[JCGM VIM3：calibration（2.39）](https://jcgm.bipm.org/vim/en/2.39.html)、[10月論文 v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[ドリフト](#^qh-drift)、[データ年齢（測定データの経過時間）](#^qh-data-age)、[ゲート誤差](#^qh-gate-error)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-fixed-point"></a>
### 固定小数点
- 英語版：[Fixed-point representation](./Glossary_EN.md#^qh-fixed-point) ^qh-fixed-point
- 区分：外部の技術用語
- 正式名と由来：Fixed-point representation。計算機の数値表現。
- 意味：整数Iに一定の尺度を掛けて値を表す方式。小数部Fビットの二進表現では値はIかける2のマイナスF乗。下式は符号付きnビットの2の補数、Fは非負整数とした範囲である。

$$
x=I\,2^{-F},\qquad -2^{n-1-F}\leq x\leq(2^{n-1}-1)2^{-F}.
$$

- 本リポジトリでの捉え方：端数持ち越しと量子化ロックの説明に必要な数値表現。ビット数、尺度、丸め、飽和の条件を一緒に記録する。
- 混同注意（日付付き）：固定小数点の離散化は計算機上の表現であり、量子力学の量子化とは異なる。Q形式は符号ビットの数え方が資料で異なるため、明示的なビット数と尺度を併記する。（2026-10-24）
- 英日のすり合わせ：Fixed-point representation を「固定小数点」とする案。
- 出典：[Arm CMSIS-DSP：固定小数点型](https://arm-software.github.io/CMSIS-DSP/latest/namespacearm__cmsis__dsp.html)、[Arm CMSIS-DSP：Fixed point datatypes](https://arm-software.github.io/CMSIS-DSP/latest/group__FIXED.html)、[10月論文 v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[最下位ビット（LSB）](#^qh-lsb)、[オーバーフロー](#^qh-overflow)、[端数持ち越し](#^qh-fractional-carry)、[量子化ロック](#^qh-quantization-lock)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-coherence-time-t2"></a>
### コヒーレンス時間（T₂）
- 英語版：[Coherence time (T₂)](./Glossary_EN.md#^qh-coherence-time-t2) ^qh-coherence-time-t2
- 区分：外部の技術用語
- 正式名と由来：Coherence time、transverse relaxation time（横緩和時間）、記号 $T_2$ 。量子ビットの位相コヒーレンスの減衰を特徴付ける時間
- 意味：単純な指数減衰モデルでは、エネルギー基底での密度行列の非対角成分の大きさが $\lvert\rho_{01}(t)\rvert=\lvert\rho_{01}(0)\rvert e^{-t/T_2}$ と減る時間尺度。$t=T_2$ で初期値の約36.8%となる。単位は秒で、実務ではマイクロ秒なども使う
- 本リポジトリでの捉え方：4月資料の $\tau_{\mathrm{coh}}(T_2)$ は、T₂を材料として許容厚みを構成する案である。時間であるT₂と、別の単位をもつ熱収支の $\tau$ を、そのまま比較しない
- 混同注意（日付付き）：T₂は「その時刻までは無誤り、その直後に壊れる」という期限ではない。エネルギー緩和も位相コヒーレンスの減衰に寄与するため、純粋な位相雑音だけの時間とは限らない。ラムゼー測定の $T_2^*$ とエコー測定などのT₂は、測定手順を付して区別する（2026-10-24）
- 英日のすり合わせ：Coherence time (T₂) を「コヒーレンス時間（T₂）」とする案。横緩和時間は同義語として記録し、T₁とは別項目にする（2026-10-24、概念照合待ち）
- 出典：[IBM Quantum Learning「Noise and errors」](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/noise-and-errors)、[Qiskit Aer「thermal_relaxation_error」](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.thermal_relaxation_error.html)、[Qiskit Experiments「T2Hahn」](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.characterization.T2Hahn.html)（2026-10-24に本文確認）。[4月完成版](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §6.2・§7.4
- 関連：[量子コヒーレンス](#^qh-quantum-coherence)、[デコヒーレンス](#^qh-decoherence)、[エネルギー緩和時間（T₁）](#^qh-energy-relaxation-time-t1)、[律速段原則](#^qh-rate-limiting-stage)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-mixed-state"></a>
### 混合状態
- 英語版：[Mixed state](./Glossary_EN.md#^qh-mixed-state) ^qh-mixed-state
- 区分：外部の技術用語
- 正式名と由来：Mixed state。量子情報の標準語。純粋状態でない密度行列で表される状態。
- 意味：複数の純粋状態の確率的な混合として表せる、純粋ではない量子状態。有限次元の正規化状態では、密度行列の二乗のトレースは1より小さい。混合の分解は一般に一意でない。

$$
\rho=\sum_i p_i\lvert\psi_i\rangle\langle\psi_i\rvert,\quad p_i\geq0,\quad \sum_i p_i=1,\quad \operatorname{Tr}(\rho^2)<1.
$$

- 本リポジトリでの捉え方：環境との相互作用や、対象だけを取り出した記述を扱うときに必要になる。密度行列は純粋状態にも混合状態にも使う。
- 混同注意（日付付き）：純粋な重ね合わせと確率的な混合は異なる。また、全体が純粋でも、もつれた部分系だけを見ると混合状態になることがある。（2026-10-24）
- 英日のすり合わせ：Mixed state を「混合状態」とする案。「混合」は密度行列の凸結合を指し、単純な振幅の足し合わせと区別する。
- 出典：[IBM Quantum：Convex combinations of density matrices](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/convex-combinations)、[IBM Quantum：Density matrix basics](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/density-matrix-basics)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[純粋状態](#^qh-pure-state)、[密度行列](#^qh-density-matrix)、[重ね合わせ](#^qh-superposition)、[開放量子系](#^qh-open-quantum-system)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-lsb"></a>
### 最下位ビット（LSB）
- 英語版：[Least significant bit (LSB)](./Glossary_EN.md#^qh-lsb) ^qh-lsb
- 区分：外部の技術用語
- 正式名と由来：Least significant bit（LSB）。二進数の最も低い桁。
- 意味：ビット列の最も重みの小さい桁。数値の大きさを「1 LSB」と表す場合は、指定した形式でその桁に対応する最小の刻み幅を指す。
- 本リポジトリでの捉え方：端数持ち越しの発火単位を読むための語。小数部Fビットの二進固定小数点では、1 LSBに対応する値は2のマイナスF乗。
- 混同注意（日付付き）：ビットの位置と、そのビットが表す値を区別する。1 LSBという表記だけでは、電圧や角度などの物理単位は決まらない。（2026-10-24）
- 英日のすり合わせ：Least significant bit を「最下位ビット」とし、LSBを併記する案。
- 出典：[Arm CMSIS-DSP：固定小数点型](https://arm-software.github.io/CMSIS-DSP/latest/namespacearm__cmsis__dsp.html)、[10月論文 v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[固定小数点](#^qh-fixed-point)、[端数持ち越し](#^qh-fractional-carry)、[量子化ロック](#^qh-quantization-lock)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-pure-state"></a>
### 純粋状態
- 英語版：[Pure state](./Glossary_EN.md#^qh-pure-state) ^qh-pure-state
- 区分：外部の技術用語
- 正式名と由来：Pure state。量子情報の標準語。混合状態と区別する。
- 意味：正規化した一つの状態ベクトルで表せる量子状態。有限次元では、密度行列の二乗のトレースが1となる。下式の状態ベクトルの長さは1とする。

$$
\rho=\lvert\psi\rangle\langle\psi\rvert,\qquad \operatorname{Tr}(\rho^2)=1.
$$

- 本リポジトリでの捉え方：1量子ビットの理想的な構成例を読むための語。実機の状態が常に純粋であるとは仮定しない。
- 混同注意（日付付き）：純粋状態でも測定結果は確率的になり得る。「一度の測定結果が確実に分かる状態」という意味ではない。（2026-10-24）
- 英日のすり合わせ：Pure state を「純粋状態」とする案。pure を「雑音が完全にない装置」と読み替えない。
- 出典：[IBM Quantum：Density matrix basics](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/density-matrix-basics)、[IBM Quantum：Convex combinations of density matrices](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/convex-combinations)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[密度行列](#^qh-density-matrix)、[混合状態](#^qh-mixed-state)、[重ね合わせ](#^qh-superposition)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-few-shot-spsa-nominal-calculation"></a>
### 少数ショットSPSA名目計算
- 英語版：[Few-shot SPSA nominal calculation](./Glossary_EN.md#^qh-few-shot-spsa-nominal-calculation) ^qh-few-shot-spsa-nominal-calculation
- 区分：接続で生まれた用語。旧称の「二重揺らぎ名目計算」は混同注意
- 正式名と由来：少数ショットSPSA名目計算（Few-shot SPSA nominal calculation）。10月の初版論文の「二重揺らぎ名目計算」を、2026-10-22に改名した手法名。「名目」は、本研究（NRA-IDE の論文系列）の用語で、少数ショットの粗い測定値（名目値）を用いることを表す。一般の学術用語ではない
- 意味：2点の少数ショット測定と、SPSAの全次元同時摂動で、名目勾配 $\hat g$ を得る計算。「名目」は、少数ショットの粗い測定値（名目値）を用いることを表す
- 本リポジトリでの捉え方：評価点数（2）は、パラメータ次元によらない。通信往復は、装置のバッチ化の方式に依存し、評価点数とは別に評価する。ただし、バレンプラトーによる指数的な制約は解消しない
- 混同注意（日付付き）：旧称の「二重揺らぎ」は、正典の「[二重ゆらぎ](../NRA-IDE_Dictionary_JP.md#^double-fluctuation)」（FORMULA §4.7：$\delta$ の増加と $\tau$ の減少の同時成立）と同名になっていた。手法名では使わない（QH-10。2026-10-22）
- 英日のすり合わせ：Few-shot SPSA nominal calculation。旧称 double-fluctuation nominal calculation は使わない（確認済み 2026-10-23）
- 出典：論文系列 v6.1 §3。変遷記録 QH-10
- 関連：[SPSA](#^qh-spsa)、[ショット](#^qh-shot)、[LFSR](#^qh-lfsr)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-shot"></a>
### ショット
- 英語版：[Shot](./Glossary_EN.md#^qh-shot) ^qh-shot
- 区分：外部の技術用語
- 正式名と由来：Shot（ショット）。量子回路を1回実行して測定すること。量子計算の実装資料で広く使われる語
- 意味：同じ回路を繰り返し実行した回数。期待値は多数のショットの平均で推定し、各ショットが独立で同分布のとき、標準誤差は $\sigma_0/\sqrt{M}$ （$M$ はショット数、$\sigma_0$ は1回あたりの標準偏差）
- 本リポジトリでの捉え方：「ショット数 $M$」「評価点の数」「測定回数」「通信往復」を別の数として書き分ける。2点SPSAなら、評価点は2、測定回数は $2M$ 。少数ショットとは、$M$ が1〜数回ということ
- 混同注意（日付付き）：ショットを増やして減るのは、統計的なゆらぎ（ショットノイズ）だけである。デコヒーレンスやゲート誤差は減らない（4月完成版 §6.1 の四層。ショット層は $M$ で減衰し、変質しない）（2026-10-23）
- 英日のすり合わせ：カタカナ「ショット」を使う。「試行」「照射」とは書かない（確認済み 2026-10-23）
- 出典：4月完成版 §6.1。論文系列（`note/03_…/2026-10_SPSA更新権限/`）§2.2
- 関連：[SPSA](#^qh-spsa)、[バレンプラトー（勾配消失の台地）](#^qh-barren-plateau)、[パラメータシフト則](#^qh-parameter-shift-rule)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-shot-noise"></a>
### ショットノイズ
- 英語版：[Shot noise](./Glossary_EN.md#^qh-shot-noise) ^qh-shot-noise
- 区分：外部の技術用語
- 正式名と由来：Shot noise。本項では、量子回路の有限ショット測定に伴う標本化のばらつきを指す。同じ語は電子・光の検出でも使われるが、対象を明記して区別する
- 意味：同じ条件で準備した量子状態を有限回だけ測定するため、測定結果の平均や頻度が期待値・真の確率からばらつくこと。独立・同分布の0または1の測定をM回行い、1の確率がpなら、頻度の標準誤差は $\sqrt{p(1-p)/M}$ となる
- 本リポジトリでの捉え方：少数ショットSPSAの測定雑音に関係する。各評価点のショット数、摂動幅、推定量の分散を分けて記録する
- 混同注意（日付付き）：同じ独立・同分布の条件なら、Mを4倍にすると標準誤差は半分になる。装置のドリフト、読み出しの偏り、ゲート誤差まで、この法則で減るとはいえない（2026-10-24）
- 英日のすり合わせ：Shot noise を「ショットノイズ」とする案。量子測定の標本化雑音という対象を意味欄で限定する（2026-10-24、概念照合待ち）
- 出典：[IBM Quantum Documentation「Estimator inputs and outputs」](https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output) の標準誤差の説明（2026-10-24に本文確認）。[10月論文 v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) §2.2
- 関連：[ショット](#^qh-shot)、[期待値](#^qh-expectation-value)、[SPSA](#^qh-spsa)、[ゲート誤差](#^qh-gate-error)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-syndrome"></a>
### シンドローム
- 英語版：[Syndrome](./Glossary_EN.md#^qh-syndrome) ^qh-syndrome
- 区分：外部の技術用語
- 正式名と由来：Error syndrome。量子誤り訂正の標準語。
- 意味：誤りの手掛かりとなる検査結果の組。スタビライザ符号では、互いに可換な検査演算子の測定結果を用い、論理状態そのものを直接読み出さずに誤りを調べる。
- 本リポジトリでの捉え方：Union-Find復号器へ渡す情報を読むための語。反復測定では、検査結果そのものと、時間方向の変化から作る検出イベントを区別する。
- 混同注意（日付付き）：一つのシンドロームから物理的な誤りが一意に確定するとは限らない。論理状態の測定結果とも異なる。（2026-10-24）
- 英日のすり合わせ：Syndrome を「シンドローム」とする案。
- 出典：[IBM Quantum：Error correction II](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/error-correction-ii)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[量子誤り訂正（QEC）](#^qh-qec)、[復号](#^qh-decoding)、[Union-Find復号器](#^qh-union-find-decoder)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-lfsr"></a>
### 線形帰還シフトレジスタ（LFSR）
- 英語版：[Linear-feedback shift register (LFSR)](./Glossary_EN.md#^qh-lfsr) ^qh-lfsr
- 区分：外部の技術用語
- 正式名と由来：線形帰還シフトレジスタ（Linear-feedback shift register、LFSR）。ディジタル回路で広く使われる疑似乱数の生成器
- 意味：レジスタのビットを線形に帰還させて、ビット列を生成する回路。乗算器なしで、少ない資源で作れる
- 本リポジトリでの捉え方：SPSAの $\pm1$ の摂動 $\Delta_k$ を、FPGA上で生成するために使う。同じ $\Delta_k$ を後から再現するには、種（シード）に加えて、帰還多項式（タップ）、ビット幅、出力の取り出し方も記録する
- 混同注意（日付付き）：疑似乱数なので、数学的に独立な対称符号の仮定と同一ではない。周期や成分間の相関の影響を、別に評価する必要がある（論文系列 v6.1 §10。2026-10-23）
- 英日のすり合わせ：略称 LFSR を使う。「乱数」ではなく「疑似乱数」と書く（確認済み 2026-10-23）
- 出典：一般的な技術用語（出典の照合はしていない）。論文系列 v6.1 §10
- 関連：[SPSA](#^qh-spsa)、[少数ショットSPSA名目計算](#^qh-few-shot-spsa-nominal-calculation)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-delayed-reference-residual"></a>
### 遅延参照残差（4月の旧称は残渣 r_t。正典の残差 ξ とは別）
- 英語版：[Delayed-reference residual (r_t of April; distinct from the canonical residual ξ)](./Glossary_EN.md#^qh-delayed-reference-residual) ^qh-delayed-reference-residual
- 区分：接続で生まれた用語。正典の残差ξとは別（混同注意）
- 正式名と由来：「遅延参照残差」$r_t$ 。4月の量子アーキテクチャ検討では「残渣」と呼んでいた（旧称）。$r_t=z^{\mathrm{pred}}_{t+1}-z^{\mathrm{ref}}_{t-\ell}$ 、$\ell$ は遅延参照幅（2026-04-29 完成版 §3.1。2026-04-21 の修正版で記法を分離）
- 意味：予測した状態記述子と、遅延幅 $\ell$ だけ前の参照との差。残渣強度は $\delta_t=\lVert W r_t\rVert$ 。4月の検討の中の量で、正典の量ではない
- 本リポジトリでの捉え方：正典の「残差 $\xi$」（FORMULA §5：$\xi=x_{\mathrm{exact}}-x$ 、参照は事前定義の高精度参照状態）とは別の量として書く。非線形の補正写像 $C(r)=r\lvert r\rvert/(k+\lvert r\rvert)$ は、正典の二次残差ゲート $G(\xi)$ と同じ形である（正典側は2026-09-30に $r$ を $\xi$ に改名）
- 混同注意（日付付き）：見出しを「遅延参照残差」とし、4月の語「残渣」は旧称として残す（2026-10-23。4月の文書は書き換えない）。「残渣」と「残差」は一文字違いで、読みも同じ「ざんさ」。「残渣」は物理的な残りかす（化学・食品・工業の語。具体的・物質的）、「残差」は観測値と予測値などの差（数学・統計の語。抽象的・数理的）。「モノの残り」が残渣、「数値のずれ」が残差と区別できる
  - 4月の「残渣」は二つの意味で使われていた。(1)差：理想と現実の乖離、予測と参照の差（この項目）→「残差」と書く。(2)余り物・端数：浮動小数点の下位の端数や、「残渣ベース」「残渣タンク」の比喩 → [端数持ち越し](#^qh-fractional-carry) の側。世間に通じる語は「端数」「丸め誤差」「下位ビット」
  - 4月の補正式 $z^{\mathrm{corr}}=z-\alpha\,g(R)\,C(r)$ のうち、Rで補正の強さを決める $g(R)$ は採用しない。評価出力が自分の入力へ戻るため（AXIOMS §14。変遷記録 QH-22）
  - 10月の固定小数点の「端数」（量子化で落ちる下位ビット）とは別の量（差である $r_t$ と、余り物である端数）
- 英日のすり合わせ：英語の residual は「残差」に当たる。見出しの「遅延参照残差」と Delayed-reference residual が一対一で対応する。正典の残差（$\xi$）との区別は「遅延参照」の語で保つ。4月の「残渣」は旧称で、英語では residue（残りかす）に当たり、この項目の英語名には使わない（確認済み 2026-10-23）
- 出典：`note/03_…/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md` §3.1。FORMULA.md §5。変遷記録.md QH-04・QH-22。正典の残差 $\xi$ は、辞書の [残差](../NRA-IDE_Dictionary_JP.md#^residual) を参照
- 関連：[観測量期待値ベクトル](#^qh-observable-expectation-vector)、[端数持ち越し](#^qh-fractional-carry)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-data-age"></a>
### データ年齢（測定データの経過時間）
- 英語版：[Data age (measurement age)](./Glossary_EN.md#^qh-data-age) ^qh-data-age
- 区分：外部の技術用語
- 正式名と由来：Data age / measurement age。測定から利用までの経過時間を表す記述語。
- 意味：測定値が得られた時刻から、その値を判定や更新に使う時刻までの経過時間。同じ時刻基準で差を取り、時刻同期やタイムスタンプの不確かさを考慮する。

$$
t_{\mathrm{age}}=t_{\mathrm{use}}-t_{\mathrm{measurement}}.
$$

- 本リポジトリでの捉え方：非同期SPSAの測定ペアを適用する時点で、古さを評価するための語。版の一致とは別に、許容時間の条件を宣言する。
- 混同注意（日付付き）：受信時刻は測定時刻とは限らない。単調時計の原点は異なる計算機で共有されるとは限らず、時計の値をそのまま引けない。新しい測定でも較正が正しいとは限らない。（2026-10-24）
- 英日のすり合わせ：Data age を「データ年齢」とし、「測定データの経過時間」を添える案。新たな正典上の指標は定義しない。
- 出典：[Python：time.monotonic](https://docs.python.org/3/library/time.html#time.monotonic)、[10月論文 v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[版管理（パラメータ版・境界版・測定時刻）](#^qh-version-check)、[原子性](#^qh-atomicity)、[ドリフト](#^qh-drift)、[較正（校正）](#^qh-calibration)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-decoherence"></a>
### デコヒーレンス
- 英語版：[Decoherence](./Glossary_EN.md#^qh-decoherence) ^qh-decoherence
- 区分：外部の技術用語
- 正式名と由来：Decoherence。環境との相互作用による量子コヒーレンスの喪失を扱う標準語。Zurekの総説は代表的な解説資料であり、語の最初の命名資料として挙げるものではない
- 意味：環境との相互作用によって、対象の量子系だけを見ると、重ね合わせの成分間の干渉を利用しにくくなる過程。環境にも情報が広がるため、対象だけの密度行列では、関係する基準で非対角成分が減衰する形で表される
- 本リポジトリでの捉え方：4月資料の誤差層別化と、リンドブラッド方程式による状態モデルに関係する物理過程。10月の更新許可は古い結果の適用を制限する設計であり、それ自体がデコヒーレンスを防ぐ機構ではない
- 混同注意（日付付き）：単に測定回数が少なくて平均値がばらつくショットノイズとは区別する。また「必ずエネルギーが失われる」「対象と環境を合わせた全体の情報が消滅する」という意味にはしない（2026-10-24）
- 英日のすり合わせ：Decoherence を「デコヒーレンス」とする案。既存資料の表記を維持し、量子コヒーレンスとの対で引けるようにする（2026-10-24、概念照合待ち）
- 出典：[Zurek「Decoherence, einselection, and the quantum origins of the classical」](https://arxiv.org/abs/quant-ph/0105127)、[IBM Quantum Learning「Noise and errors」](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/noise-and-errors)（2026-10-24に要旨・本文をそれぞれ確認）。[4月完成版](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §4・§6
- 関連：[量子コヒーレンス](#^qh-quantum-coherence)、[密度行列](#^qh-density-matrix)、[リンドブラッド方程式](#^qh-lindblad-equation)、[ショットノイズ](#^qh-shot-noise)、[更新許可](#^qh-update-authority)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-spsa"></a>
### 同時摂動確率近似（SPSA）
- 英語版：[Simultaneous Perturbation Stochastic Approximation (SPSA)](./Glossary_EN.md#^qh-spsa) ^qh-spsa
- 区分：外部の技術用語
- 正式名と由来：Simultaneous Perturbation Stochastic Approximation（略称 SPSA）。J. C. Spall の1992年の論文（IEEE Transactions on Automatic Control 37(3), 332–341）が、代表的な定式化とされる。量子計算専用ではなく、もとは制御工学・統計の最適化手法
- 意味：全パラメータに、同時に、各成分が±1のランダムな符号の摂動を与え、2点（前進・後退）の評価値の差から、全成分の勾配を近似する確率的最適化。評価点の数が、パラメータ数 $p$ によらず2である
- 本リポジトリでの捉え方：「評価点が2」という意味で使う。評価点数（2）・測定回数（各点のショット数 $M$ を含めて $2M$）・通信往復は別の数として書き分ける。1回の更新の評価点が減ることを、総ショット数や収束の速さの改善と書かない
- 混同注意（日付付き）：SPSAを使っても、バレンプラトーは解消しない。必要な反復回数と総測定予算は指数的に増えうる（Qin 2026、Arrasmith ほか 2021）。初版論文はこれを「回避できる」と書いていた（2026-10-22に撤回）
  - 論文系列では、手法名「二重揺らぎ名目計算」が正典の「二重ゆらぎ」と同名になっていた。手法名は「少数ショットSPSA名目計算」に改めた（2026-10-22）
- 英日のすり合わせ：略称 SPSA はそのまま使う。日本語の正式名「同時摂動確率近似」は、Spall の原題の語順に合わせた直訳。「同時」は「全パラメータを同時に」の意味で、非同期の「同時」とは別（確認済み 2026-10-23）
- 出典：Spall, IEEE Transactions on Automatic Control 37(3), 332–341 (1992年3月)、DOI 10.1109/9.119632（Crossref で2026-10-23に確認）。Qin, arXiv:2608.09810 (2026)。Arrasmith ほか, Quantum 5, 558 (2021)
- 関連：[バレンプラトー](#^qh-barren-plateau)、[ショット](#^qh-shot)、[少数ショットSPSA名目計算](#^qh-few-shot-spsa-nominal-calculation)、[バイアス（推定の偏り）](#^qh-estimator-bias)、[分散](#^qh-variance)、[標準誤差](#^qh-standard-error)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-drift"></a>
### ドリフト
- 英語版：[Drift](./Glossary_EN.md#^qh-drift) ^qh-drift
- 区分：外部の技術用語
- 正式名と由来：Drift。計測では、時間とともにゆっくり変化する計器の応答などを指す。
- 意味：時間の経過とともに測定器や装置の応答が変化する現象。短時間の無作為なばらつきとは区別する。何が、どの期間に、どの量について変化したかを指定する。
- 本リポジトリでの捉え方：測定の時刻が古くなる影響や、較正の有効性を考えるための語。系の状態の変化と、読み出し装置の応答の変化を分けて評価する。
- 混同注意（日付付き）：すべての雑音や劣化をドリフトと総称しない。閾値を追従させただけでは、装置の変化を正しく較正できたことにはならない。（2026-10-24）
- 英日のすり合わせ：Drift を「ドリフト」とする案。対象に応じて計器ドリフトなどと補う。
- 出典：[NIST：Drift](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc453.htm)、[10月論文 v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[較正（校正）](#^qh-calibration)、[データ年齢（測定データの経過時間）](#^qh-data-age)、[ショットノイズ](#^qh-shot-noise)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-estimator-bias"></a>
### バイアス（推定の偏り）
- 英語版：[Estimator bias](./Glossary_EN.md#^qh-estimator-bias) ^qh-estimator-bias
- 区分：外部の技術用語
- 正式名と由来：Estimator bias。統計的推定の用語。
- 意味：推定量の期待値と、推定対象の真の値との差。下式の期待値は、明示した測定・標本抽出のモデルに関する平均である。

$$
\operatorname{Bias}(\hat{\theta})=\mathbb{E}[\hat{\theta}]-\theta.
$$

- 本リポジトリでの捉え方：SPSAの有限摂動や測定ペアの選別が推定へ与える影響を評価する語。見送った後の採用標本だけを調べる場合も、選別条件を明記する。
- 混同注意（日付付き）：バイアスがゼロでも分散は大きくなり得る。計測における系統的な偏りと関連するが、常に単一の装置オフセットを意味するわけではない。（2026-10-24）
- 英日のすり合わせ：Bias を「バイアス（推定の偏り）」とする案。
- 出典：[NIST：Analysis of bias](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc45.htm)、[10月論文 v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[分散](#^qh-variance)、[標準誤差](#^qh-standard-error)、[同時摂動確率近似（SPSA）](#^qh-spsa)、[ペア見送り](#^qh-pair-skip)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-fractional-carry"></a>
### 端数持ち越し
- 英語版：[Fractional carry-over](./Glossary_EN.md#^qh-fractional-carry) ^qh-fractional-carry
- 区分：接続で生まれた用語（10月）
- 正式名と由来：端数持ち越し（Fractional carry-over）。10月の論文系列で、固定小数点のビットシフトで落ちる下位の端数を、次のステップへ持ち越す仕組み。デルタ・シグマ変調と同じ形
- 意味：シフトの前に、拡張精度のアキュムレータへ積算し、整数部だけを更新に使い、落ちた下位ビットを残す。$A_k\mathrel{-}=2^{F-s_k}\hat g_k$ 、$u_k=\mathrm{trunc}(A_k/2^F)$ 、$A_k\mathrel{-}=2^F u_k$ （$F\ge s_k$ とオーバーフローなしが前提）
- 本リポジトリでの捉え方：シフトの後に端数を足す式（初版の形）は、シフトの時点で下位ビットが失われるので、端数が持ち越されない。シフト量が途中で変わる場合も、共通の高精度単位で積算する（中途計算 C07）
  - 前提：固定小数点の丸め規則（切り捨て・四捨五入など）と、保持する小数ビット数 $F$ ・ビット幅、オーバーフローがないこと
- 混同注意（日付付き）：4月の「残渣」には、この「余り物・端数」の意味もあった（浮動小数点の下位の端数）。世間に通じる語は「端数」「丸め誤差」「下位ビット」で、「残渣」は旧称として扱う（2026-10-23）。差である [遅延参照残差](#^qh-delayed-reference-residual) とは別の量
- 英日のすり合わせ：Fractional carry-over。numerical analysis の rounding error や、error feedback（誤差帰還）と近い概念で、日本語の「端数」に対応する（確認済み 2026-10-23）
- 出典：論文系列の中途計算メモ C07（`note/03_…/2026-10_SPSA更新権限/中途計算_検算メモ.md`）。v6.1 §5.2
- 関連：[量子化ロック](#^qh-quantization-lock)、[遅延参照残差](#^qh-delayed-reference-residual)、[固定小数点](#^qh-fixed-point)、[最下位ビット（LSB）](#^qh-lsb)、[オーバーフロー](#^qh-overflow)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-hamiltonian"></a>
### ハミルトニアン
- 英語版：[Hamiltonian](./Glossary_EN.md#^qh-hamiltonian) ^qh-hamiltonian
- 区分：外部の技術用語
- 正式名と由来：Hamiltonian。量子力学ではエネルギーを表すエルミートな演算子Hとして用いる。
- 意味：系のエネルギーとユニタリーな時間発展を定める演算子。密度行列との交換子を通して状態を変化させる。時間に依存する駆動や、有効なエネルギー準位のずれを含む場合もある。
- 本リポジトリでの捉え方：GKSL式の第1項に現れる。詳説の単位系では、エネルギーをプランク定数hbarで割った角周波数として読む。
- 混同注意（日付付き）：ユニタリー発展でも、時間依存する外部駆動があれば系のエネルギーは変わり得る。Hだけで環境の散逸をすべて表しているとは限らない。（2026-10-24）
- 英日のすり合わせ：Hamiltonian を「ハミルトニアン」とする案。原論文のHの単位と、有効項の含め方を明記する。
- 出典：[QuTiP：Lindblad Master Equation Solver](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html)、[GKSL詳説](./details/Lindblad_GKSL_JP.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[リンドブラッド方程式（GKSL形式）](#^qh-lindblad-equation)、[期待値](#^qh-expectation-value)、[開放量子系](#^qh-open-quantum-system)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-parameter-shift-rule"></a>
### パラメータシフト則
- 英語版：[Parameter-shift rule](./Glossary_EN.md#^qh-parameter-shift-rule) ^qh-parameter-shift-rule
- 区分：外部の技術用語
- 正式名と由来：Parameter-shift rule。Mitarai ほか, Physical Review A 98, 032309 (2018)。Schuld ほか, Physical Review A 99, 032331 (2019)
- 意味：パラメータを一定量（多くは $\pm\pi/2$ ）ずらした2回の評価値の差から、解析的な勾配を得る方法（特定の形のゲートで成立）。ショットノイズを除けば、勾配は厳密
- 本リポジトリでの捉え方：各パラメータごとに2回の評価が要るので、全体では $2p$ 回（$p$ はパラメータ数）と書く。SPSAは、パラメータ数によらず2回
- 混同注意（日付付き）：SPSAとの違いは、勾配の厳密さ（厳密／確率的な近似）と、評価回数（$2p$ ／ 2）である。少数ショットでは、どちらもノイズの影響を受ける（2026-10-23）
- 英日のすり合わせ：「パラメータシフト則」と書く。「パラメータ移動」とは書かない（shift は値をずらす意味）（確認済み 2026-10-23）
- 出典：Mitarai ほか, Physical Review A 98, 032309 (2018)。Schuld ほか（5名。Schuld・Bergholm・Gogolin・Izaac・Killoran）, Physical Review A 99, 032331 (2019)（2026-10-23に検索で確認）
- 関連：[SPSA](#^qh-spsa)、[ショット](#^qh-shot)、[VQE](#^qh-vqe)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-barren-plateau"></a>
### バレンプラトー（勾配消失の台地）
- 英語版：[Barren plateau](./Glossary_EN.md#^qh-barren-plateau) ^qh-barren-plateau
- 区分：外部の技術用語
- 正式名と由来：Barren plateau（「不毛の台地」）。J. R. McClean ほか, Nature Communications 9, 4812 (2018) が、ランダム性の強い変分量子回路で、勾配の分散が量子ビット数に対して指数的に小さくなることを示した
- 意味：変分量子回路の学習で、ランダム性の強い回路（2-design に近い）など、回路・コスト関数・ノイズの条件のもとで、量子ビット数 $n$ の増加とともに、コスト関数の勾配の分散が指数的（$O(2^{-n})$ など）に消える現象。損失地形が平らになり、1ショットの観測分散が小さくならないとき、勾配を測定ノイズから見分けるのに指数的な測定資源が要る
- 本リポジトリでの捉え方：損失地形の性質であり、推定の方法（SPSAなど）を変えても消えない、と書く。すべての回路で必ず起きるわけではなく、回路・コスト関数・ノイズの条件つきで書く（Cerezo ほか 2021：浅い回路と局所コストでは回避できる場合がある。Wang ほか 2021：ノイズも原因になる）
- 混同注意（日付付き）：初版論文は、原因を「精密過剰計算」とし、必要ショット数を $O(2^{2n})$ と書いた（2026-10-22に撤回）。分散が $2^{-n}$ なら勾配の典型値は $2^{-n/2}$ で、必要ショット数は条件つきで $\Omega(2^{n})$
  - 「勾配消失の台地」という説明は、概念として妥当である（2026-10-22）。バレンプラトーは勾配消失（vanishing gradient）の一種で、とくに変分量子回路に特有の、量子ビット数に対して指数的な消失を指す。古典のニューラルネットワークの勾配消失とは、原因とスケーリングが異なる場合がある
- 英日のすり合わせ：カタカナ「バレンプラトー」を主とし、見出しに「勾配消失の台地」の説明を添える。直訳の「不毛の台地」は用語として使わない。「勾配消失」だけには訳さない（より広い語で、バレンプラトーはその一種のため。量子回路に特有の指数的な消失を表せなくなる）（確認済み 2026-10-23）
- 出典：McClean（Boixo・Smelyanskiy・Babbush・Neven）ほか, Nature Communications 9, 4812 (2018)、DOI 10.1038/s41467-018-07090-4。Cerezo（Sone・Volkoff・Cincio・Coles）, Nature Communications 12, 1791 (2021)、DOI 10.1038/s41467-021-21728-w。Wang ほか（Fontana・Cerezo・Sharma・Sone・Cincio・Coles）, Nature Communications 12, 6961 (2021)、DOI 10.1038/s41467-021-27045-6。Arrasmith ほか (2021)（いずれも2026-10-23に確認）
- 関連：[SPSA](#^qh-spsa)、[ショット](#^qh-shot)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-version-check"></a>
### 版管理（パラメータ版・境界版・測定時刻）
- 英語版：[Version management (parameter version, boundary version, measurement time)](./Glossary_EN.md#^qh-version-check) ^qh-version-check
- 区分：接続で生まれた用語（10月）【拡張案】
- 正式名と由来：10月の論文 v6.1 §4.2「測定結果の版管理」で用いた語。各測定ペアに、使用したパラメータ版・境界判定版（境界版）・2点の測定時刻・受信時刻・観測チャネルの状態を付ける
- 意味：非同期の更新で、測定した時点の条件と、適用する時点の条件が一致しているかを確かめるための記録。パラメータ版は更新対象のパラメータの版、境界版は境界判定（閾値・状態区分）の版
- 本リポジトリでの捉え方：測定後にパラメータ版または境界版が変わっていれば、再計算または見送りとする。判定と適用は不可分な処理として結合し、両者の間の状態変更を許さない（v6.1 §4.2 の条件5・6）
- 混同注意（日付付き）：論文系列に出てくる版の語は、パラメータ版と境界版（境界判定版）である。「観測版」「設定版」という語は、論文系列にまだ定義がない（2026-10-23）。また、これは論文・文書の版番号（変遷記録の3.0〜6.1）とは別のもの
- 英日のすり合わせ：Version management。version は「版」で、バージョン番号とは書かない（確認済みではない）
- 出典：論文系列 v6.1 §4.2・§4.3
- 関連：[更新許可](#^qh-update-authority)、[ペア見送り](#^qh-pair-skip)、[原子性](#^qh-atomicity)、[データ年齢（測定データの経過時間）](#^qh-data-age)、[ドリフト](#^qh-drift)、[較正（校正）](#^qh-calibration)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-dynamical-semigroup"></a>
### 半群（量子力学的半群）
- 英語版：[Semigroup (quantum dynamical semigroup)](./Glossary_EN.md#^qh-dynamical-semigroup) ^qh-dynamical-semigroup
- 区分：外部の技術用語
- 正式名と由来：Semigroup（半群）は結合法則を満たす演算の数学用語。本項の対象は、時間発展の写像族としての量子力学的半群。
- 意味：同じ経過時間に同じ写像を使い、時間tの発展の後に時間sの発展を行うことが、合計時間の発展と一致する写像族。下式では時刻ゼロの写像を恒等写像とする。

$$
\Phi_{t+s}=\Phi_s\circ\Phi_t,\qquad \Phi_0=\mathrm{id},\qquad t,s\geq0.
$$

- 本リポジトリでの捉え方：時間一様なGKSL生成子の一般形を述べるときの前提。有限次元では、連続なCPTP半群の生成子がGKSL形式で表せる。
- 混同注意（日付付き）：一般の半群という語だけではCPTP性や連続性は付かない。また時間依存するGKSL式は、CPTPでも時間一様な半群とは限らない。（2026-10-24）
- 英日のすり合わせ：Semigroup を「半群」、quantum dynamical semigroup を「量子力学的半群」とする案。別名は同じ項目へリンクする。
- 出典：[Lindblad (1976)：出版社の書誌・要旨](https://link.springer.com/article/10.1007/BF01608499)、[GKSL詳説](./details/Lindblad_GKSL_JP.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[完全正値・トレース保存写像（CPTP）](#^qh-cptp-map)、[マルコフ近似](#^qh-markov-approximation)、[リンドブラッド方程式（GKSL形式）](#^qh-lindblad-equation)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-standard-error"></a>
### 標準誤差
- 英語版：[Standard error](./Glossary_EN.md#^qh-standard-error) ^qh-standard-error
- 区分：外部の技術用語
- 正式名と由来：Standard error（SE）。統計的推定の標準語。
- 意味：推定量の標本分布の標準偏差。独立同分布で分散が有限なM個の測定の平均では、母標準偏差をsigmaとして下式になる。実際には標本標準偏差sで推定する。

$$
\operatorname{SE}(\bar{X})=\frac{\sigma}{\sqrt{M}},\qquad \widehat{\operatorname{SE}}(\bar{X})=\frac{s}{\sqrt{M}},\quad M\geq2.
$$

- 本リポジトリでの捉え方：ショット数と平均推定のばらつきの関係を読むための語。平均以外の推定量には、それぞれの標準誤差を用いる。
- 混同注意（日付付き）：測定値自体の標準偏差や、系統誤差を含む全誤差とは異なる。相関のある測定に独立標本の式を無条件に使わない。信頼区間には分布などの追加条件が必要。（2026-10-24）
- 英日のすり合わせ：Standard error を「標準誤差」とする案。
- 出典：[NIST：Confidence Limits for the Mean](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm)、[IBM Quantum：Estimator inputs and outputs](https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[分散](#^qh-variance)、[バイアス（推定の偏り）](#^qh-estimator-bias)、[ショット](#^qh-shot)、[ショットノイズ](#^qh-shot-noise)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-decoding"></a>
### 復号
- 英語版：[Decoding](./Glossary_EN.md#^qh-decoding) ^qh-decoding
- 区分：外部の技術用語
- 正式名と由来：Decoding。符号理論の標準語。
- 意味：シンドロームと仮定した誤りモデルから、回復操作や論理的な補正を推定する処理。実際の物理的誤りを完全に特定できなくても、同じ論理効果を打ち消せればよい場合がある。
- 本リポジトリでの捉え方：Union-Findは復号法の一つ。復号の処理時間、誤り率、対応する雑音モデルは個別に評価する。
- 混同注意（日付付き）：暗号の復号とは対象が異なる。復号器の高速化だけで、誤り訂正の閾値や実機の成功率が保証されるわけではない。（2026-10-24）
- 英日のすり合わせ：Decoding を「復号」、decoder を「復号器」とする案。
- 出典：[IBM Quantum：Error correction II](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/error-correction-ii)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[シンドローム](#^qh-syndrome)、[量子誤り訂正（QEC）](#^qh-qec)、[Union-Find復号器](#^qh-union-find-decoder)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-variance"></a>
### 分散
- 英語版：[Variance](./Glossary_EN.md#^qh-variance) ^qh-variance
- 区分：外部の技術用語
- 正式名と由来：Variance。確率・統計の標準語。
- 意味：確率変数の平均からのずれの二乗を平均した量。有限な二次モーメントを仮定する。値の単位がVなら分散の単位はVの二乗になる。

$$
\operatorname{Var}(X)=\mathbb{E}\!\left[(X-\mathbb{E}[X])^2\right].
$$

- 本リポジトリでの捉え方：有限ショットの推定量やSPSA勾配推定量のばらつきを読むための語。どの確率変数の分散かを明記する。
- 混同注意（日付付き）：標準偏差は分散の平方根。標本分散は母分散そのものではなく、通常の不偏推定では標本数から1を引いた数で割る。分散だけでは真値からの偏りは分からない。（2026-10-24）
- 英日のすり合わせ：Variance を「分散」とする案。
- 出典：[NIST：Measures of Scale](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[バイアス（推定の偏り）](#^qh-estimator-bias)、[標準誤差](#^qh-standard-error)、[ショットノイズ](#^qh-shot-noise)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-pair-skip"></a>
### ペア見送り
- 英語版：[Pairwise skip of an update](./Glossary_EN.md#^qh-pair-skip) ^qh-pair-skip
- 区分：接続で生まれた用語（10月）
- 正式名と由来：ペア見送り（Pairwise skip of an update）。10月の論文系列で用いた語。状態名は `SKIP_UPDATE` 【拡張】（参照実装 v2.1にはない）
- 意味：SPSAの前進・後退の測定ペアの片側が無効なとき、比較の条件を保証できない代用や再測定を行わず、ペア全体を見送って、パラメータを直前の値のまま保つこと
- 本リポジトリでの捉え方：片側の値のみの代用（直前値など）や、物理状態が変化した後の再測定では、比較の条件を失い、推定量に偏りが生じる可能性がある。独立な測定ノイズなどの条件が保たれ、再測定の判断が測定値に依存しない再測定であれば、偏りを生まない可能性がある。本研究方式では、その条件を保証できないとき、ペア全体を見送る。見送りは、観測値を書き換えず、記録を残す
- 混同注意（日付付き）：有限で有効な値を見送る場合に、`CONFESSION` と呼ばない（`CONFESSION` は不明・不正入力の停止信号。QH-09）。見送りでも、選別による縮小バイアスは残りうる（中途計算 C08）。統計的な見送りは補助で、判定の主語は境界接近比 $R$ である（QH-11）（2026-10-23）
- 英日のすり合わせ：Pairwise skip。「破棄」（discard）とは書かない。観測値は捨てずに記録するため（確認済み 2026-10-23）
- 出典：論文系列 v6.1 §4.4・§5。変遷記録 QH-09・QH-11
- 関連：[DiscardVault](#^qh-discard-vault)、[更新許可](#^qh-update-authority)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-vqe"></a>
### 変分量子固有値ソルバ（VQE）
- 英語版：[Variational Quantum Eigensolver (VQE)](./Glossary_EN.md#^qh-vqe) ^qh-vqe
- 区分：外部の技術用語
- 正式名と由来：Variational Quantum Eigensolver（略称 VQE）。Peruzzo ほか, Nature Communications 5, 4213 (2014)
- 意味：パラメータ付きの量子回路で状態を作り、ハミルトニアンの期待値を測定し、古典の最適化器でパラメータを更新して、基底状態のエネルギーを近似的に求めるハイブリッド法
- 本リポジトリでの捉え方：量子層と古典層が閉ループを作る構造として書く。測定は有限ショットでノイズを含み、古典側が受け取る情報は本質的に不完全である（4月完成版 §2.1）
- 混同注意（日付付き）：VQEが常に破綻するという意味ではない。設計が悪いと、バレンプラトーやノイズによる破綻経路を内在しやすい、という意味で書く（2026-10-23。4月完成版 §2.1）
- 英日のすり合わせ：略称VQEを使う。「固有値ソルバ」は eigensolver の訳で、「求解器」とは書かない（確認済み 2026-10-23）
- 出典：Peruzzo ほか, Nature Communications 5, 4213 (2014)、DOI 10.1038/ncomms5213（2026-10-23に検索で確認）。4月完成版 §2.1
- 関連：[SPSA](#^qh-spsa)、[バレンプラトー（勾配消失の台地）](#^qh-barren-plateau)、[ショット](#^qh-shot)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-born-approximation"></a>
### ボルン近似（Born近似）
- 英語版：[Born approximation](./Glossary_EN.md#^qh-born-approximation) ^qh-born-approximation
- 区分：外部の技術用語
- 正式名と由来：Born approximation。本項は散乱理論一般ではなく、開放量子系の主方程式の導出で用いる意味を扱う。
- 意味：弱い系・環境結合のもとで、環境の状態の変化や系・環境の相関を小さいものとして近似する手順。典型的な導出では、全体の状態を系の状態とほぼ固定した環境状態の積で近似する。
- 本リポジトリでの捉え方：GKSL詳説で、代表的な微視的導出の条件として扱う。実機で相関が存在しないことを検証済みとする宣言ではない。
- 混同注意（日付付き）：Born近似とマルコフ近似は異なる仮定である。近似の中で相関を無視することと、実際の系が常に無相関であることを同一視しない。（2026-10-24）
- 英日のすり合わせ：Born approximation を「ボルン近似」とし、検索用にBorn近似も併記する案。
- 出典：[QuTiP：Lindblad Master Equation Solver](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html)、[GKSL詳説](./details/Lindblad_GKSL_JP.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[マルコフ近似](#^qh-markov-approximation)、[永年近似](#^qh-secular-approximation)、[開放量子系](#^qh-open-quantum-system)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-markov-approximation"></a>
### マルコフ近似
- 英語版：[Markov approximation](./Glossary_EN.md#^qh-markov-approximation) ^qh-markov-approximation
- 区分：外部の技術用語
- 正式名と由来：Markov approximation。環境の記憶を無視する近似として、開放量子系の導出で用いる。
- 意味：環境の相関が失われる時間が系の緩和時間より十分短いとき、現在の変化を過去全体の履歴へ依存させずに近似する考え方。時刻が新しいというだけで成立する条件ではない。
- 本リポジトリでの捉え方：Lindblad中心案を具体的な量子系へ適用する前に妥当性を確かめる条件。非同期データの版・年齢を照合する処理とは別である。
- 混同注意（日付付き）：時間局所の微分方程式で書けることだけでは、環境の記憶のなさや、CPTP性は確定しない。（2026-10-24）
- 英日のすり合わせ：Markov approximation を「マルコフ近似」とする案。マルコフ性の数学的定義と、物理モデルからの近似手順を区別する。
- 出典：[QuTiP：Lindblad Master Equation Solver](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html)、[GKSL詳説](./details/Lindblad_GKSL_JP.md)（外部資料の説明・定義を参照 2026-10-24。論文全文の対訳照合ではない）
- 関連：[開放量子系](#^qh-open-quantum-system)、[ボルン近似（Born近似）](#^qh-born-approximation)、[永年近似](#^qh-secular-approximation)、[完全正値・トレース保存写像（CPTP）](#^qh-cptp-map)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-density-matrix"></a>
### 密度行列
- 英語版：[Density matrix](./Glossary_EN.md#^qh-density-matrix) ^qh-density-matrix
- 区分：外部の技術用語
- 正式名と由来：Density matrix。量子状態を表す標準的な行列表現で、通常は $\rho$ と書く。density operator（密度演算子）という呼び方もある
- 意味：純粋状態と混合状態の両方を扱える量子状態の表現。有限次元では、半正定値で対角成分の和が1となる行列である。半正定値とは、この行列から計算する測定確率が負にならないための条件。選んだ基準での対角成分は各基準状態の確率、非対角成分は成分間のコヒーレンスを表す
- 本リポジトリでの捉え方：4月のLindblad中心案で時間発展する対象であり、判定層へ渡す観測量期待値ベクトルとは別のもの。少数の期待値だけから、一般の密度行列全体を再構成できるとは仮定しない
- 混同注意（日付付き）：物質の密度や熱負荷を並べた表ではない。また、一度の測定で未知の密度行列を読み出せるわけではない。確率的な混合と純粋な重ね合わせの違いは、0・1の測定確率だけでは見えない場合がある（2026-10-24）
- 英日のすり合わせ：Density matrix を「密度行列」、density operator を「密度演算子」とする案。ここでの $\rho$ は量子状態の記法であり、別文脈の相関係数などとは区別する（2026-10-24、概念照合待ち）
- 出典：[IBM Quantum Learning「Density matrix basics」](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/density-matrix-basics)（2026-10-24に本文確認）。[4月完成版](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §4・§5
- 関連：[重ね合わせ](#^qh-superposition)、[量子コヒーレンス](#^qh-quantum-coherence)、[期待値](#^qh-expectation-value)、[観測量期待値ベクトル](#^qh-observable-expectation-vector)、[リンドブラッド方程式](#^qh-lindblad-equation)、[純粋状態](#^qh-pure-state)、[混合状態](#^qh-mixed-state)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-rate-limiting-stage"></a>
### 律速段原則
- 英語版：[Rate-limiting-stage principle](./Glossary_EN.md#^qh-rate-limiting-stage) ^qh-rate-limiting-stage
- 区分：接続で生まれた用語（4月B-3）
- 正式名と由来：律速段原則。4月 B-3 と完成版 §6.2。$\tau_{\mathrm{total}}=\min(\tau_{\mathrm{system}},\tau_{\mathrm{shot}}(N),\tau_{\mathrm{coh}}(T_2),\tau_{\mathrm{gate}}(D))$
- 意味：複数の層のうち、最も狭い余裕が、全体の限界を決める、という原則。$\delta$ は独立ノイズの仮定で二乗和により合成するが、$\tau$ は最小で合成する。ただし、$\tau$ 同士を直接比べられるのは、各 $\tau$ が同一の対象・同一の単位・同じ意味で、$\delta$ と対応して定義されているときに限る（この比較可能性の条件は未確定）
- 本リポジトリでの捉え方：最も狭い層が、Fail-Closed 到達時刻を決める。どの層が支配しているかを読み分けるために、一つの量に潰さない
- 混同注意（日付付き）：10月の4Kステージの熱収支の $\tau$ は、4月の四層（system・shot・coh・gate）にない。律速段にどう加えるかは未了（変遷記録 QO-02）（2026-10-23）
  - $\tau$ の最小値による合成は、各層の $\tau$ が時間・熱負荷・ショット数・許容誤差など異なる単位や尺度をもつ場合には、そのまま成り立たない。候補として、層ごとに無次元の $R_i=\delta_i/\tau_i$ を求め、$R_{\mathrm{limiting}}=\max_i R_i$ をとる方法があるが、律速段原則の置き換えとしては確定していない（2026-10-23）
- 英日のすり合わせ：Rate-limiting-stage principle。化学工学の「律速段階」と同じ考え方の語で、「ボトルネック原則」とは書かない（確認済み 2026-10-23）
- 出典：4月完成版 §6.2。4月 B-3
- 関連：[4Kステージ](#^qh-cryo-cmos-4k-stage)、[観測量期待値ベクトル](#^qh-observable-expectation-vector)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-qec"></a>
### 量子誤り訂正（QEC）
- 英語版：[Quantum error correction (QEC)](./Glossary_EN.md#^qh-qec) ^qh-qec
- 区分：外部の技術用語
- 正式名と由来：量子誤り訂正（Quantum error correction、QEC）。P. W. Shor, Physical Review A 52, R2493 (1995) などに始まる
- 意味：複数の物理量子ビットに情報を符号化し、シンドローム測定で誤りを検出して訂正する方法
- 本リポジトリでの捉え方：10月の論文系列では、復号を、SPSAとは別の高速経路（経路A）として分離する。誤りの抑制・緩和・訂正は、それぞれ別の層である
- 混同注意（日付付き）：NRA-IDEは、誤り抑制・誤り緩和・誤り訂正を置き換えるものではなく、それらとは別層の、構造監査と Fail-Closed 判定の設計である（QH-02。4月 README。2026-10-23）
- 英日のすり合わせ：略称QECを使う。「誤り訂正」と「エラー補正」を混ぜない（確認済み 2026-10-23）
- 出典：Shor, Physical Review A 52, R2493–R2496 (1995)、DOI 10.1103/PhysRevA.52.R2493（2026-10-23に検索で確認。最初の量子誤り訂正符号）。論文系列 v6.1 §4.1。4月 README
- 関連：[Union-Find復号器](#^qh-union-find-decoder)、[4Kステージ](#^qh-cryo-cmos-4k-stage)、[シンドローム](#^qh-syndrome)、[復号](#^qh-decoding)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-quantization-lock"></a>
### 量子化ロック
- 英語版：[Quantization lock (underflow freeze)](./Glossary_EN.md#^qh-quantization-lock) ^qh-quantization-lock
- 区分：接続で生まれた用語（10月）
- 正式名と由来：量子化ロック（Quantization lock。アンダーフローによる更新の凍結）。10月の論文系列で用いた語
- 意味：固定小数点で、右シフトによって更新量が最小分解能（LSB）未満になり、更新がゼロのまま固まりうる現象。実装の丸め規則と学習率（シフト量）の条件による。必然的に永久に止まるのではない
- 本リポジトリでの捉え方：見送りが続いてシフト量 $s_k$ を増やしたときに起こる。防ぐには、シフトの前に拡張精度で積算する（端数持ち越し）。再現例：$\hat g=3$ 、$s=4$ 、64ステップで、シフト後に端数を足す式では総更新が0（理想は12）
- 混同注意（日付付き）：「量子」の文字があるが、量子計算の現象ではなく、固定小数点の量子化（丸め）の現象である（2026-10-23）
- 英日のすり合わせ：「量子化」は quantization（数値の離散化）の訳で、量子力学の量子（quantum）とは別。英語は Quantization lock とし、quantum は使わない（確認済み 2026-10-23）
- 出典：中途計算メモ C07、再現スクリプト repro.py T4
- 関連：[端数持ち越し](#^qh-fractional-carry)
- 状態：【草稿】【概念照合済み】【全文対訳未確認】

<a id="qh-quantum-interference"></a>
### 量子干渉
- 英語版：[Quantum interference](./Glossary_EN.md#^qh-quantum-interference) ^qh-quantum-interference
- 区分：外部の技術用語
- 正式名と由来：Quantum interference。量子力学における確率振幅の干渉を表す標準語
- 意味：同じ測定結果へ至る区別できない経路の確率振幅が加わり、その相対位相に応じて結果の確率が強まったり弱まったりすること。確率をそのまま足す場合と、振幅を足してから絶対値を二乗する場合は異なる
- 本リポジトリでの捉え方：少数ショットは、回路が生む測定分布を少ない回数で標本化する方法である。ショット数を減らすことが、干渉の維持や回復を意味するとは書かない
- 混同注意（日付付き）：目的に沿って利用する量子干渉と、制御線などからの望まない電磁的な干渉を区別する。どちらも英語では interference と呼ばれる場合がある（2026-10-24）
- 英日のすり合わせ：Quantum interference を「量子干渉」とする案。単独の「干渉」では対象を明記する（2026-10-24、概念照合待ち）
- 出典：[IBM Quantum Learning「Superposition with Qiskit」](https://quantum.cloud.ibm.com/learning/en/modules/quantum-mechanics/superposition-with-qiskit)（2026-10-24に本文確認）
- 関連：[重ね合わせ](#^qh-superposition)、[位相・相対位相](#^qh-quantum-phase)、[量子コヒーレンス](#^qh-quantum-coherence)、[ショット](#^qh-shot)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-quantum-coherence"></a>
### 量子コヒーレンス
- 英語版：[Quantum coherence](./Glossary_EN.md#^qh-quantum-coherence) ^qh-quantum-coherence
- 区分：外部の技術用語
- 正式名と由来：Quantum coherence。量子状態の重ね合わせと干渉を扱う標準語で、coherence は位相関係の整合に関わる
- 意味：選んだ基準状態の成分間に、干渉に現れる関係があること。密度行列では、その基準での非対角成分がコヒーレンスを表す。非対角成分は、同じ成分間の関係を記録する欄に相当する
- 本リポジトリでの捉え方：4月資料の「コヒーレンス層」を読むための語。量子状態が干渉に利用できることと、古典側の版・時刻・記録の整合性を分ける
- 混同注意（日付付き）：コヒーレンスの有無は基準に依存する。「論理が首尾一貫している」という一般語の coherence や、量子ビット間のもつれと同義ではない（2026-10-24）
- 英日のすり合わせ：Quantum coherence を「量子コヒーレンス」とする案。「整合性」だけでは古典側の整合性と混ざるため、見出しでは原語に沿った語を使う（2026-10-24、概念照合待ち）
- 出典：[Zurek「Decoherence, einselection, and the quantum origins of the classical」](https://arxiv.org/abs/quant-ph/0105127)、[IBM Quantum Learning「Density matrix basics」](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/density-matrix-basics)（2026-10-24に要旨・本文をそれぞれ確認）。[4月完成版](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §6
- 関連：[デコヒーレンス](#^qh-decoherence)、[量子干渉](#^qh-quantum-interference)、[密度行列](#^qh-density-matrix)、[コヒーレンス時間（T₂）](#^qh-coherence-time-t2)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-qubit"></a>
### 量子ビット
- 英語版：[Qubit](./Glossary_EN.md#^qh-qubit) ^qh-qubit
- 区分：外部の技術用語
- 正式名と由来：Quantum bit（量子ビット）、略して qubit。量子情報の基本単位を表す標準語
- 意味：二つの基準状態 $\lvert0\rangle$ と $\lvert1\rangle$ をもつ量子情報の単位。純粋状態は $a\lvert0\rangle+b\lvert1\rangle$ と書き、$a,b$ は複素数、$\lvert a\rvert^2+\lvert b\rvert^2=1$ 。この基準で測定すると、0または1の一つの結果を得る
- 本リポジトリでの捉え方：10月論文の「1量子ビット・1パラメータ」は、構成例と予備的な古典計算の対象規模を示す。その結果を、多量子ビットでの性能の根拠にしない
- 混同注意（日付付き）：一つの量子ビットを一度測れば、重ね合わせの全成分を読み出せる、という意味ではない。物理量子ビットの個数と、誤り訂正で構成する論理量子ビットの個数も区別する（2026-10-24）
- 英日のすり合わせ：Qubit と「量子ビット」を対応させる案。qubit は quantum bit の短縮形で、通常の bit と区別する（2026-10-24、概念照合待ち）
- 出典：[IBM Quantum Learning「Quantum information」](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information)（2026-10-24に本文確認）。[10月論文 v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) §6.3・§6.5
- 関連：[重ね合わせ](#^qh-superposition)、[密度行列](#^qh-density-matrix)、[量子誤り訂正（QEC）](#^qh-qec)
- 状態：【草稿】【概念未照合】【全文対訳未確認】

<a id="qh-lindblad-equation"></a>
### リンドブラッド方程式（GKSL形式）
- 英語版：[Lindblad (GKSL) equation](./Glossary_EN.md#^qh-lindblad-equation) ^qh-lindblad-equation
- 区分：外部の技術用語
- 正式名と由来：Lindblad equation（GKSL 方程式）。G. Lindblad, Communications in Mathematical Physics 48, 119 (1976)。Gorini・Kossakowski・Sudarshan, Journal of Mathematical Physics 17, 821 (1976)
- 意味：開放量子系のマルコフ型時間発展を扱う基本形式。有限次元・時間一様で連続なCPTP量子力学的半群の生成子の一般形である。Hはエルミートとし、速度係数は下の演算子に含める。単位系は $\hbar=1$ 。[式の読み方と成立条件](./details/Lindblad_GKSL_JP.md)に、各記号、ジャンプの正規化、速度係数、導出近似を詳述する。

$$
\dot{\rho}
=
-i[H,\rho]
+
\sum_k\left(
L_k\rho L_k^\dagger
-\frac{1}{2}\{L_k^\dagger L_k,\rho\}
\right).
$$

- 本リポジトリでの捉え方：4月のB-1で、NRA-IDE側の時間発展核 $F_{\mathrm{IDE}}$ を、この方程式として定義した。デコヒーレンスや散逸を、$\delta$・$\tau$ と接続するため
- 混同注意（日付付き）：4月の $F_{\mathrm{IDE}}$ は、正典 FORMULA §5 の「領域固有の基礎動力学項（IDE一次式ではない）」と同じ記号である。量子系の領域固有の項として定義したものと読む（2026-10-23）。マルコフ近似の妥当性と、SPSAとの結合は、別に定式化が要る（10月論文 v6.1 §7）
- 英日のすり合わせ：「リンドブラッド方程式」と書き、GKSL形式と併記する。「リンドブラッド主方程式」（master equation）とも呼ばれる（確認済み 2026-10-23）
- 出典：[Lindblad (1976)](https://link.springer.com/article/10.1007/BF01608499)、[Gorini・Kossakowski・Sudarshan (1976)](https://repository.ias.ac.in/51137/)（書誌・要旨を2026-10-24に照合。原論文全文の読了とは区別）。[QuTiPの主方程式解説](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html)、[量子ジャンプ解説](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-monte.html)は本文で照合。詳細な書誌と照合範囲は[詳説](./details/Lindblad_GKSL_JP.md) §9。4月B-1の位置付けは既存の研究履歴として保持する。
- 関連：[密度行列](#^qh-density-matrix)、[デコヒーレンス](#^qh-decoherence)、[T₁](#^qh-energy-relaxation-time-t1)、[T₂](#^qh-coherence-time-t2)、[観測量期待値ベクトル](#^qh-observable-expectation-vector)、[律速段原則](#^qh-rate-limiting-stage)、[開放量子系](#^qh-open-quantum-system)、[ハミルトニアン](#^qh-hamiltonian)、[マルコフ近似](#^qh-markov-approximation)、[ボルン近似（Born近似）](#^qh-born-approximation)、[永年近似](#^qh-secular-approximation)、[完全正値性](#^qh-complete-positivity)、[完全正値・トレース保存写像（CPTP）](#^qh-cptp-map)、[半群（量子力学的半群）](#^qh-dynamical-semigroup)
- 状態：【草稿】【概念未照合】【全文対訳未確認】（2026-10-24の説明拡充後。名称の対応は2026-10-23に確認済み）
