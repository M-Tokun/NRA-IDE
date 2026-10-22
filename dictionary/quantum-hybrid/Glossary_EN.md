# NRA-IDE Quantum-Hybrid Glossary (English Version)

**Version:** 0.1 (skeleton)  
**Author:** M-Tokuni  
**Document role:** A glossary for looking up the meaning, official name, history, and common confusions of external technical terms (quantum computing, SPSA, cryogenic hardware, etc.) and of terms created where they connect to NRA-IDE. It neither creates nor changes canonical definitions  
**Paired Japanese version:** [Glossary_JP.md](./Glossary_JP.md)  
**Scope and rules:** [README.md](./README.md)

---

Status legend: [Skeleton] headings and fields only; content not yet written. [JP/EN unreconciled] the Japanese and English have not been reconciled.

---

<a id="qh-spsa"></a>
### Simultaneous Perturbation Stochastic Approximation (SPSA)
- Japanese version: [同時摂動確率近似（SPSA）](./Glossary_JP.md#^qh-spsa) ^qh-spsa
- Category: 外部の技術用語
- Official name and origin: Simultaneous Perturbation Stochastic Approximation (abbreviated SPSA). Proposed by J. C. Spall in 1992 (IEEE Transactions on Automatic Control 37(3), 332–341). Not specific to quantum computing; it originated as an optimization method in control engineering and statistics
- Meaning: A stochastic optimization method that perturbs all parameters at once, each component by a random sign of ±1, and approximates the gradient of all components from the difference of two evaluations (forward and backward). The number of evaluation points is two, independent of the number of parameters $p$
- How it is written in this repository: Used to mean "two evaluation points." The number of evaluation points (two), the number of measurements (including the shots $M$ per point, $2M$), and the number of communication round trips are written as separate numbers. Fewer evaluation points per update is not written as an improvement in total shots or convergence speed
- Common confusions (dated): Using SPSA does not remove the barren plateau. The required iterations and total measurement budget can still grow exponentially (Qin 2026; Arrasmith et al. 2021). The first paper said it could be avoided (retracted 2026-10-22)
  - In the paper series, the method name "double-fluctuation nominal calculation" shared its name with the canonical "double fluctuation." The method name was changed to "few-shot SPSA nominal calculation" (2026-10-22)
- JP/EN reconciliation: The abbreviation SPSA is used as is. The Japanese official name is a literal translation that follows Spall's original title. "Simultaneous" means perturbing all parameters at once, not asynchronous (not yet confirmed)
- Sources: Spall (1992). Qin, arXiv:2608.09810 (2026). Arrasmith et al., Quantum 5, 558 (2021). Bibliographic details were checked in the paper series (`note/03_…/2026-10_SPSA更新権限/`); Spall's DOI is not yet checked
- Related: [Barren plateau](#^qh-barren-plateau), [Shot](#^qh-shot), [Few-shot SPSA nominal calculation](#^qh-few-shot-spsa-nominal-calculation)
- Status: [Draft] [JP/EN unreconciled]

<a id="qh-barren-plateau"></a>
### Barren plateau
- Japanese version: [バレンプラトー（勾配消失の台地）](./Glossary_JP.md#^qh-barren-plateau) ^qh-barren-plateau
- Category: 外部の技術用語
- Official name and origin: Barren plateau (Japanese: 不毛の台地). J. R. McClean et al., Nature Communications 9, 4812 (2018), showed that for highly random variational quantum circuits the variance of the gradient shrinks exponentially with the number of qubits
- Meaning: In training variational quantum circuits, the phenomenon where the variance of the cost-function gradient vanishes exponentially (e.g., $O(2^{-n})$) as the number of qubits $n$ grows. The loss landscape flattens, and distinguishing the gradient from measurement noise requires exponential measurement resources
- How it is written in this repository: Written as a property of the loss landscape that does not disappear when the estimation method (SPSA, etc.) changes. It does not occur in every circuit; it is stated under conditions on the circuit, the cost function, and the noise (Cerezo et al. 2021: it can be avoided for some shallow circuits with local costs; Wang et al. 2021: noise can also cause it)
- Common confusions (dated): The first paper attributed the cause to "over-precise computation" and wrote the required shots as $O(2^{2n})$ (retracted 2026-10-22). If the variance is $2^{-n}$, the typical gradient is $2^{-n/2}$ and the required shots are, under conditions, $\Omega(2^{n})$
  - The description "a plateau of vanishing gradients" (勾配消失の台地) captures the essence correctly (the user's remark, 2026-10-22). The barren plateau is a kind of vanishing gradient, specifically the exponential vanishing with the number of qubits that is characteristic of variational quantum circuits. Its cause and scaling can differ from the vanishing gradient of classical neural networks
- JP/EN reconciliation: The katakana "バレンプラトー" is the main Japanese form, with the explanation "勾配消失の台地" added to the heading. The literal "不毛の台地" is not used as a term. It is not rendered only as "勾配消失" (a broader term of which the barren plateau is a kind; it would lose the exponential vanishing specific to quantum circuits)
- Sources: McClean et al. (2018), DOI 10.1038/s41467-018-07090-4. Cerezo et al., Nature Communications 12, 1791 (2021). Wang et al., Nature Communications 12, 6961 (2021). Arrasmith et al. (2021). Checked in the paper series (DOIs other than McClean et al. not yet checked)
- Related: [SPSA](#^qh-spsa), [Shot](#^qh-shot)
- Status: [Draft] [JP/EN unreconciled]

<a id="qh-vqe"></a>
### Variational Quantum Eigensolver (VQE)
- Japanese version: [変分量子固有値ソルバ（VQE）](./Glossary_JP.md#^qh-vqe) ^qh-vqe
- Category: 外部の技術用語
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-nisq"></a>
### Noisy Intermediate-Scale Quantum (NISQ)
- Japanese version: [NISQ（ノイズのある中規模量子）](./Glossary_JP.md#^qh-nisq) ^qh-nisq
- Category: 外部の技術用語
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-shot"></a>
### Shot
- Japanese version: [ショット](./Glossary_JP.md#^qh-shot) ^qh-shot
- Category: 外部の技術用語
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-parameter-shift-rule"></a>
### Parameter-shift rule
- Japanese version: [パラメータシフト則](./Glossary_JP.md#^qh-parameter-shift-rule) ^qh-parameter-shift-rule
- Category: 外部の技術用語
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-lindblad-equation"></a>
### Lindblad (GKSL) equation
- Japanese version: [リンドブラッド方程式（GKSL形式）](./Glossary_JP.md#^qh-lindblad-equation) ^qh-lindblad-equation
- Category: 外部の技術用語
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-observable-expectation-vector"></a>
### Observable expectation-value vector
- Japanese version: [観測量期待値ベクトル](./Glossary_JP.md#^qh-observable-expectation-vector) ^qh-observable-expectation-vector
- Category: 接続で生まれた用語（4月B-2）
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-rate-limiting-stage"></a>
### Rate-limiting-stage principle
- Japanese version: [律速段原則](./Glossary_JP.md#^qh-rate-limiting-stage) ^qh-rate-limiting-stage
- Category: 接続で生まれた用語（4月B-3）
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-delayed-reference-residual"></a>
### Delayed-reference residual (r_t of April; distinct from the canonical residual ξ)
- Japanese version: [遅延参照残差（4月の旧称は残渣 r_t。正典の残差 ξ とは別）](./Glossary_JP.md#^qh-delayed-reference-residual) ^qh-delayed-reference-residual
- Category: 接続で生まれた用語。正典の残差ξとは別（混同注意）
- Official name and origin: "遅延参照残差" (delayed-reference residual) $r_t$ . It was called "残渣" in the April quantum-architecture study (a former name). $r_t=z^{\mathrm{pred}}_{t+1}-z^{\mathrm{ref}}_{t-\ell}$ , where $\ell$ is the delayed-reference width (2026-04-29 final version §3.1; the notation was separated in the 2026-04-21 revision)
- Meaning: The difference between the predicted state descriptor and the reference delayed by $\ell$. The residual strength is $\delta_t=\lVert W r_t\rVert$ . A quantity within the April study, not a canonical quantity
- How it is written in this repository: Written as a quantity distinct from the canonical "residual $\xi$" (FORMULA §5: $\xi=x_{\mathrm{exact}}-x$ , with a predefined high-precision reference state). The nonlinear correction map $C(r)=r\lvert r\rvert/(k+\lvert r\rvert)$ has the same form as the canonical second-order residual gate $G(\xi)$ (on the canonical side, $r$ was renamed $\xi$ on 2026-09-30)
- Common confusions (dated): The heading is now "遅延参照残差," and the April word "残渣" is kept as a former name (2026-10-23; the April documents are not rewritten). "残渣" and "残差" differ by one character and are read the same (ざんさ). 残渣 is a physical leftover (chemistry, food, industry; concrete and material); 残差 is the difference between an observed and a predicted value (mathematics, statistics; abstract and numerical). Remember: 残渣 is a remainder of matter, 残差 is a numerical deviation (the user's summary)
  - The April "残渣" was used in two senses. (1) A difference: the gap between ideal and reality, or between a prediction and a reference (this entry) → write "残差." (2) A leftover or fractional remainder: the low-order fractional bits of floating point, and the metaphor of "residue-based" design and the "residue tank" → see [Fractional carry-over](#^qh-fractional-carry). Terms understood generally are "端数" (fraction), "丸め誤差" (rounding error), and "下位ビット" (low-order bits)
  - Of the April correction formula $z^{\mathrm{corr}}=z-\alpha\,g(R)\,C(r)$ , the $g(R)$ that sets the correction strength from $R$ is not adopted, because the evaluation output would return to its own input (AXIOMS §14; change log QH-22)
  - Distinct from the "fractional remainder" of the October fixed-point arithmetic (the low-order bits dropped by quantization): $r_t$ is a difference, the remainder is a leftover
- JP/EN reconciliation: English "residual" corresponds to Japanese "残差." The Japanese heading "遅延参照残差" and "Delayed-reference residual" correspond one to one. The distinction from the canonical residual ($\xi$) is kept by the words "delayed-reference." The April "残渣" is a former name; in English it corresponds to "residue" (a leftover) and is not used for the English name of this entry (not yet confirmed)
- Sources: `note/03_…/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md` §3.1. FORMULA.md §5. Change log QH-04 and QH-22. Note: the existing dictionary has no entry for the canonical residual $\xi$ (pending; when added, link to it from this entry)
- Related: [Observable expectation-value vector](#^qh-observable-expectation-vector), [Fractional carry-over](#^qh-fractional-carry)
- Status: [Draft] [JP/EN unreconciled]

<a id="qh-fractional-carry"></a>
### Fractional carry-over
- Japanese version: [端数持ち越し](./Glossary_JP.md#^qh-fractional-carry) ^qh-fractional-carry
- Category: 接続で生まれた用語（10月）
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-quantization-lock"></a>
### Quantization lock (underflow freeze)
- Japanese version: [量子化ロック](./Glossary_JP.md#^qh-quantization-lock) ^qh-quantization-lock
- Category: 接続で生まれた用語（10月）
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-lfsr"></a>
### Linear-feedback shift register (LFSR)
- Japanese version: [線形帰還シフトレジスタ（LFSR）](./Glossary_JP.md#^qh-lfsr) ^qh-lfsr
- Category: 外部の技術用語
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-pair-skip"></a>
### Pairwise skip of an update
- Japanese version: [ペア見送り](./Glossary_JP.md#^qh-pair-skip) ^qh-pair-skip
- Category: 接続で生まれた用語（10月）
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-discard-vault"></a>
### DiscardVault
- Japanese version: [DiscardVault（見送り・境界越えの保管庫）](./Glossary_JP.md#^qh-discard-vault) ^qh-discard-vault
- Category: 参照実装の固定名と本稿での用い方の区別
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-update-authority"></a>
### Update authority
- Japanese version: [更新権限](./Glossary_JP.md#^qh-update-authority) ^qh-update-authority
- Category: 接続で生まれた用語（10月）
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-few-shot-spsa-nominal-calculation"></a>
### Few-shot SPSA nominal calculation
- Japanese version: [少数ショットSPSA名目計算](./Glossary_JP.md#^qh-few-shot-spsa-nominal-calculation) ^qh-few-shot-spsa-nominal-calculation
- Category: 接続で生まれた用語。旧称の「二重揺らぎ名目計算」は混同注意
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-cryo-cmos-4k-stage"></a>
### 4 K stage (Cryo-CMOS)
- Japanese version: [4Kステージ（Cryo-CMOS）](./Glossary_JP.md#^qh-cryo-cmos-4k-stage) ^qh-cryo-cmos-4k-stage
- Category: 外部の技術用語
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-qec"></a>
### Quantum error correction (QEC)
- Japanese version: [量子誤り訂正（QEC）](./Glossary_JP.md#^qh-qec) ^qh-qec
- Category: 外部の技術用語
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

<a id="qh-union-find-decoder"></a>
### Union-Find decoder
- Japanese version: [Union-Find復号器](./Glossary_JP.md#^qh-union-find-decoder) ^qh-union-find-decoder
- Category: 外部の技術用語
- Official name and origin:
- Meaning:
- How it is written in this repository:
- Common confusions (dated):
- JP/EN reconciliation:
- Sources:
- Related:
- Status: [Skeleton] [JP/EN unreconciled]

