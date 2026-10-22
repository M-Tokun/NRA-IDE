# NRA-IDE 量子ハイブリッド用語集（日本語版）

**Version:** 0.1（骨格）  
**Author:** M-Tokuni  
**Document role:** 量子計算・SPSA・極低温ハードウェアなど、外部の技術用語と、NRA-IDEとの接続で生まれた用語の意味・正式名・経過・混同を引くための用語集。正典の定義を作らず、変えない  
**対になる英語版:** [Glossary_EN.md](./Glossary_EN.md)  
**範囲と運用:** [README.md](./README.md)

---

状態の凡例：【骨格】見出しと欄だけ。内容は未記入。【英日未確認】日本語と英語のすり合わせが済んでいない。

---

<a id="qh-spsa"></a>
### 同時摂動確率近似（SPSA）
- 英語版：[Simultaneous Perturbation Stochastic Approximation (SPSA)](./Glossary_EN.md#^qh-spsa) ^qh-spsa
- 区分：外部の技術用語
- 正式名と由来：Simultaneous Perturbation Stochastic Approximation（略称 SPSA）。J. C. Spall が1992年に提案した（IEEE Transactions on Automatic Control 37(3), 332–341）。量子計算専用ではなく、もとは制御工学・統計の最適化手法
- 意味：全パラメータに、同時に、各成分が±1のランダムな符号の摂動を与え、2点（前進・後退）の評価値の差から、全成分の勾配を近似する確率的最適化。評価点の数が、パラメータ数 $p$ によらず2である
- 使い方（本リポジトリでの書き方）：「評価点が2」という意味で使う。評価点数（2）・測定回数（各点のショット数 $M$ を含めて $2M$）・通信往復は別の数として書き分ける。1回の更新の評価点が減ることを、総ショット数や収束の速さの改善と書かない
- 混同注意（日付付き）：SPSAを使っても、バレンプラトーは解消しない。必要な反復回数と総測定予算は指数的に増えうる（Qin 2026、Arrasmith ほか 2021）。初版論文はこれを「回避できる」と書いていた（2026-10-22に撤回）
  - 論文系列では、手法名「二重揺らぎ名目計算」が正典の「二重ゆらぎ」と同名になっていた。手法名は「少数ショットSPSA名目計算」に改めた（2026-10-22）
- 英日のすり合わせ：略称 SPSA はそのまま使う。日本語の正式名「同時摂動確率近似」は、Spall の原題の語順に合わせた直訳。「同時」は「全パラメータを同時に」の意味で、非同期の「同時」とは別（確認済みではない）
- 出典：Spall (1992)。Qin, arXiv:2608.09810 (2026)。Arrasmith ほか, Quantum 5, 558 (2021)。書誌は論文系列（`note/03_…/2026-10_SPSA更新権限/`）で照合済み（Spall のDOIは未照合）
- 関連：[バレンプラトー](#^qh-barren-plateau)、[ショット](#^qh-shot)、[少数ショットSPSA名目計算](#^qh-few-shot-spsa-nominal-calculation)
- 状態：【草稿】【英日未確認】

<a id="qh-barren-plateau"></a>
### バレンプラトー（勾配消失の台地）
- 英語版：[Barren plateau](./Glossary_EN.md#^qh-barren-plateau) ^qh-barren-plateau
- 区分：外部の技術用語
- 正式名と由来：Barren plateau（「不毛の台地」）。J. R. McClean ほか, Nature Communications 9, 4812 (2018) が、ランダム性の強い変分量子回路で、勾配の分散が量子ビット数に対して指数的に小さくなることを示した
- 意味：変分量子回路の学習で、量子ビット数 $n$ の増加とともに、コスト関数の勾配の分散が指数的（$O(2^{-n})$ など）に消える現象。損失地形が平らになり、勾配を測定ノイズから見分けるのに指数的な測定資源が要る
- 使い方（本リポジトリでの書き方）：損失地形の性質であり、推定の方法（SPSAなど）を変えても消えない、と書く。すべての回路で必ず起きるわけではなく、回路・コスト関数・ノイズの条件つきで書く（Cerezo ほか 2021：浅い回路と局所コストでは回避できる場合がある。Wang ほか 2021：ノイズも原因になる）
- 混同注意（日付付き）：初版論文は、原因を「精密過剰計算」とし、必要ショット数を $O(2^{2n})$ と書いた（2026-10-22に撤回）。分散が $2^{-n}$ なら勾配の典型値は $2^{-n/2}$ で、必要ショット数は条件つきで $\Omega(2^{n})$
  - 「勾配消失の台地」という説明は、本質を突いた正しい捉え方である（利用者の指摘、2026-10-22）。バレンプラトーは勾配消失（vanishing gradient）の一種で、とくに変分量子回路に特有の、量子ビット数に対して指数的な消失を指す。古典のニューラルネットワークの勾配消失とは、原因とスケーリングが異なる場合がある
- 英日のすり合わせ：カタカナ「バレンプラトー」を主とし、見出しに「勾配消失の台地」の説明を添える。直訳の「不毛の台地」は用語として使わない。「勾配消失」だけには訳さない（より広い語で、バレンプラトーはその一種のため。量子回路に特有の指数的な消失を表せなくなる）
- 出典：McClean ほか (2018)、DOI 10.1038/s41467-018-07090-4。Cerezo ほか, Nature Communications 12, 1791 (2021)。Wang ほか, Nature Communications 12, 6961 (2021)。Arrasmith ほか (2021)。書誌は論文系列で照合（McClean ほか以外のDOIは未照合）
- 関連：[SPSA](#^qh-spsa)、[ショット](#^qh-shot)
- 状態：【草稿】【英日未確認】

<a id="qh-vqe"></a>
### 変分量子固有値ソルバ（VQE）
- 英語版：[Variational Quantum Eigensolver (VQE)](./Glossary_EN.md#^qh-vqe) ^qh-vqe
- 区分：外部の技術用語
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-nisq"></a>
### NISQ（ノイズのある中規模量子）
- 英語版：[Noisy Intermediate-Scale Quantum (NISQ)](./Glossary_EN.md#^qh-nisq) ^qh-nisq
- 区分：外部の技術用語
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-shot"></a>
### ショット
- 英語版：[Shot](./Glossary_EN.md#^qh-shot) ^qh-shot
- 区分：外部の技術用語
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-parameter-shift-rule"></a>
### パラメータシフト則
- 英語版：[Parameter-shift rule](./Glossary_EN.md#^qh-parameter-shift-rule) ^qh-parameter-shift-rule
- 区分：外部の技術用語
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-lindblad-equation"></a>
### リンドブラッド方程式（GKSL形式）
- 英語版：[Lindblad (GKSL) equation](./Glossary_EN.md#^qh-lindblad-equation) ^qh-lindblad-equation
- 区分：外部の技術用語
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-observable-expectation-vector"></a>
### 観測量期待値ベクトル
- 英語版：[Observable expectation-value vector](./Glossary_EN.md#^qh-observable-expectation-vector) ^qh-observable-expectation-vector
- 区分：接続で生まれた用語（4月B-2）
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-rate-limiting-stage"></a>
### 律速段原則
- 英語版：[Rate-limiting-stage principle](./Glossary_EN.md#^qh-rate-limiting-stage) ^qh-rate-limiting-stage
- 区分：接続で生まれた用語（4月B-3）
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-delayed-reference-residual"></a>
### 遅延参照残差（4月の旧称は残渣 r_t。正典の残差 ξ とは別）
- 英語版：[Delayed-reference residual (r_t of April; distinct from the canonical residual ξ)](./Glossary_EN.md#^qh-delayed-reference-residual) ^qh-delayed-reference-residual
- 区分：接続で生まれた用語。正典の残差ξとは別（混同注意）
- 正式名と由来：「遅延参照残差」$r_t$ 。4月の量子アーキテクチャ検討では「残渣」と呼んでいた（旧称）。$r_t=z^{\mathrm{pred}}_{t+1}-z^{\mathrm{ref}}_{t-\ell}$ 、$\ell$ は遅延参照幅（2026-04-29 完成版 §3.1。2026-04-21 の修正版で記法を分離）
- 意味：予測した状態記述子と、遅延幅 $\ell$ だけ前の参照との差。残渣強度は $\delta_t=\lVert W r_t\rVert$ 。4月の検討の中の量で、正典の量ではない
- 使い方（本リポジトリでの書き方）：正典の「残差 $\xi$」（FORMULA §5：$\xi=x_{\mathrm{exact}}-x$ 、参照は事前定義の高精度参照状態）とは別の量として書く。非線形の補正写像 $C(r)=r\lvert r\rvert/(k+\lvert r\rvert)$ は、正典の二次残差ゲート $G(\xi)$ と同じ形である（正典側は2026-09-30に $r$ を $\xi$ に改名）
- 混同注意（日付付き）：見出しを「遅延参照残差」とし、4月の語「残渣」は旧称として残す（2026-10-23。4月の文書は書き換えない）。「残渣」と「残差」は一文字違いで、読みも同じ「ざんさ」。「残渣」は物理的な残りかす（化学・食品・工業の語。具体的・物質的）、「残差」は観測値と予測値などの差（数学・統計の語。抽象的・数理的）。「モノの残り」が残渣、「数値のずれ」が残差と覚える（利用者の整理）
  - 4月の「残渣」は二つの意味で使われていた。(1)差：理想と現実の乖離、予測と参照の差（この項目）→「残差」と書く。(2)余り物・端数：浮動小数点の下位の端数や、「残渣ベース」「残渣タンク」の比喩 → [端数持ち越し](#^qh-fractional-carry) の側。世間に通じる語は「端数」「丸め誤差」「下位ビット」
  - 4月の補正式 $z^{\mathrm{corr}}=z-\alpha\,g(R)\,C(r)$ のうち、Rで補正の強さを決める $g(R)$ は採用しない。評価出力が自分の入力へ戻るため（AXIOMS §14。変遷記録 QH-22）
  - 10月の固定小数点の「端数」（量子化で落ちる下位ビット）とは別の量（差である $r_t$ と、余り物である端数）
- 英日のすり合わせ：英語の residual は「残差」に当たる。見出しの「遅延参照残差」と Delayed-reference residual が一対一で対応する。正典の残差（$\xi$）との区別は「遅延参照」の語で保つ。4月の「残渣」は旧称で、英語では residue（残りかす）に当たり、この項目の英語名には使わない（確認済みではない）
- 出典：`note/03_…/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md` §3.1。FORMULA.md §5。変遷記録.md QH-04・QH-22。なお、既存の辞書には、正典の残差 $\xi$ の項目がない（未了。追加するときは、この項目からリンクする）
- 関連：[観測量期待値ベクトル](#^qh-observable-expectation-vector)、[端数持ち越し](#^qh-fractional-carry)
- 状態：【草稿】【英日未確認】

<a id="qh-fractional-carry"></a>
### 端数持ち越し
- 英語版：[Fractional carry-over](./Glossary_EN.md#^qh-fractional-carry) ^qh-fractional-carry
- 区分：接続で生まれた用語（10月）
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-quantization-lock"></a>
### 量子化ロック
- 英語版：[Quantization lock (underflow freeze)](./Glossary_EN.md#^qh-quantization-lock) ^qh-quantization-lock
- 区分：接続で生まれた用語（10月）
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-lfsr"></a>
### 線形帰還シフトレジスタ（LFSR）
- 英語版：[Linear-feedback shift register (LFSR)](./Glossary_EN.md#^qh-lfsr) ^qh-lfsr
- 区分：外部の技術用語
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-pair-skip"></a>
### ペア見送り
- 英語版：[Pairwise skip of an update](./Glossary_EN.md#^qh-pair-skip) ^qh-pair-skip
- 区分：接続で生まれた用語（10月）
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-discard-vault"></a>
### DiscardVault（見送り・境界越えの保管庫）
- 英語版：[DiscardVault](./Glossary_EN.md#^qh-discard-vault) ^qh-discard-vault
- 区分：参照実装の固定名と本稿での用い方の区別
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-update-authority"></a>
### 更新権限
- 英語版：[Update authority](./Glossary_EN.md#^qh-update-authority) ^qh-update-authority
- 区分：接続で生まれた用語（10月）
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-few-shot-spsa-nominal-calculation"></a>
### 少数ショットSPSA名目計算
- 英語版：[Few-shot SPSA nominal calculation](./Glossary_EN.md#^qh-few-shot-spsa-nominal-calculation) ^qh-few-shot-spsa-nominal-calculation
- 区分：接続で生まれた用語。旧称の「二重揺らぎ名目計算」は混同注意
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-cryo-cmos-4k-stage"></a>
### 4Kステージ（Cryo-CMOS）
- 英語版：[4 K stage (Cryo-CMOS)](./Glossary_EN.md#^qh-cryo-cmos-4k-stage) ^qh-cryo-cmos-4k-stage
- 区分：外部の技術用語
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-qec"></a>
### 量子誤り訂正（QEC）
- 英語版：[Quantum error correction (QEC)](./Glossary_EN.md#^qh-qec) ^qh-qec
- 区分：外部の技術用語
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

<a id="qh-union-find-decoder"></a>
### Union-Find復号器
- 英語版：[Union-Find decoder](./Glossary_EN.md#^qh-union-find-decoder) ^qh-union-find-decoder
- 区分：外部の技術用語
- 正式名と由来：
- 意味：
- 使い方（本リポジトリでの書き方）：
- 混同注意（日付付き）：
- 英日のすり合わせ：
- 出典：
- 関連：
- 状態：【骨格】【英日未確認】

