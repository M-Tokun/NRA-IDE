# NRA-IDE Quantum-Hybrid Glossary (English Version)

**Version:** 0.1 (skeleton)  
**Author:** M-Tokuni  
**Document role:** A glossary for looking up the meaning, official name, history, and common confusions of external technical terms (quantum computing, SPSA, cryogenic hardware, etc.) and of terms created where they connect to NRA-IDE. It neither creates nor changes canonical definitions  
**Paired Japanese version:** [Glossary_JP.md](./Glossary_JP.md)  
**Scope and rules:** [README.md](./README.md)

---

Status legend: [Skeleton] headings and fields only; content not yet written. [Draft] the text is written. [concepts unreconciled] the meaning and term correspondence have not been reconciled between Japanese and English. [concepts reconciled] the meaning and term correspondence have been reconciled. [full text not yet checked] the English of every field has not been checked one to one against the Japanese (when done, marked [full text checked]).

---

<a id="qh-spsa"></a>
### Simultaneous Perturbation Stochastic Approximation (SPSA)
- Japanese version: [同時摂動確率近似（SPSA）](./Glossary_JP.md#^qh-spsa) ^qh-spsa
- Category: 外部の技術用語
- Official name and origin: Simultaneous Perturbation Stochastic Approximation (abbreviated SPSA). J. C. Spall's 1992 paper (IEEE Transactions on Automatic Control 37(3), 332–341) is regarded as the representative formulation. Not specific to quantum computing; it originated as an optimization method in control engineering and statistics
- Meaning: A stochastic optimization method that perturbs all parameters at once, each component by a random sign of ±1, and approximates the gradient of all components from the difference of two evaluations (forward and backward). The number of evaluation points is two, independent of the number of parameters $p$
- How it is understood in this repository: Used to mean "two evaluation points." The number of evaluation points (two), the number of measurements (including the shots $M$ per point, $2M$), and the number of communication round trips are written as separate numbers. Fewer evaluation points per update is not written as an improvement in total shots or convergence speed
- Common confusions (dated): Using SPSA does not remove the barren plateau. The required iterations and total measurement budget can still grow exponentially (Qin 2026; Arrasmith et al. 2021). The first paper said it could be avoided (retracted 2026-10-22)
  - In the paper series, the method name "double-fluctuation nominal calculation" shared its name with the canonical "double fluctuation." The method name was changed to "few-shot SPSA nominal calculation" (2026-10-22)
- JP/EN reconciliation: The abbreviation SPSA is used as is. The Japanese official name is a literal translation that follows Spall's original title. "Simultaneous" means perturbing all parameters at once, not asynchronous (confirmed 2026-10-23)
- Sources: Spall, IEEE Transactions on Automatic Control 37(3), 332–341 (March 1992), DOI 10.1109/9.119632 (checked on Crossref, 2026-10-23). Qin, arXiv:2608.09810 (2026). Arrasmith et al., Quantum 5, 558 (2021)
- Related: [Barren plateau](#^qh-barren-plateau), [Shot](#^qh-shot), [Few-shot SPSA nominal calculation](#^qh-few-shot-spsa-nominal-calculation)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-barren-plateau"></a>
### Barren plateau
- Japanese version: [バレンプラトー（勾配消失の台地）](./Glossary_JP.md#^qh-barren-plateau) ^qh-barren-plateau
- Category: 外部の技術用語
- Official name and origin: Barren plateau (Japanese: 不毛の台地). J. R. McClean et al., Nature Communications 9, 4812 (2018), showed that for highly random variational quantum circuits the variance of the gradient shrinks exponentially with the number of qubits
- Meaning: In training variational quantum circuits, under conditions on the circuit (e.g., highly random, near a 2-design), the cost function, and the noise, the phenomenon where the variance of the cost-function gradient vanishes exponentially (e.g., $O(2^{-n})$) as the number of qubits $n$ grows. The loss landscape flattens, and when the one-shot observation variance does not shrink, distinguishing the gradient from measurement noise requires exponential measurement resources
- How it is understood in this repository: Written as a property of the loss landscape that does not disappear when the estimation method (SPSA, etc.) changes. It does not occur in every circuit; it is stated under conditions on the circuit, the cost function, and the noise (Cerezo et al. 2021: it can be avoided for some shallow circuits with local costs; Wang et al. 2021: noise can also cause it)
- Common confusions (dated): The first paper attributed the cause to "over-precise computation" and wrote the required shots as $O(2^{2n})$ (retracted 2026-10-22). If the variance is $2^{-n}$, the typical gradient is $2^{-n/2}$ and the required shots are, under conditions, $\Omega(2^{n})$
  - The description "a plateau of vanishing gradients" (勾配消失の台地) is conceptually sound (2026-10-22). The barren plateau is a kind of vanishing gradient, specifically the exponential vanishing with the number of qubits that is characteristic of variational quantum circuits. Its cause and scaling can differ from the vanishing gradient of classical neural networks
- JP/EN reconciliation: The katakana "バレンプラトー" is the main Japanese form, with the explanation "勾配消失の台地" added to the heading. The literal "不毛の台地" is not used as a term. It is not rendered only as "勾配消失" (a broader term of which the barren plateau is a kind; it would lose the exponential vanishing specific to quantum circuits) (confirmed 2026-10-23)
- Sources: McClean (Boixo, Smelyanskiy, Babbush, Neven) et al., Nature Communications 9, 4812 (2018), DOI 10.1038/s41467-018-07090-4. Cerezo (Sone, Volkoff, Cincio, Coles), Nature Communications 12, 1791 (2021), DOI 10.1038/s41467-021-21728-w. Wang et al. (Fontana, Cerezo, Sharma, Sone, Cincio, Coles), Nature Communications 12, 6961 (2021), DOI 10.1038/s41467-021-27045-6. Arrasmith et al. (2021) (all checked, 2026-10-23)
- Related: [SPSA](#^qh-spsa), [Shot](#^qh-shot)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-vqe"></a>
### Variational Quantum Eigensolver (VQE)
- Japanese version: [変分量子固有値ソルバ（VQE）](./Glossary_JP.md#^qh-vqe) ^qh-vqe
- Category: 外部の技術用語
- Official name and origin: Variational Quantum Eigensolver (abbreviated VQE). Peruzzo et al., Nature Communications 5, 4213 (2014)
- Meaning: A hybrid method that prepares a state with a parameterized quantum circuit, measures the expectation value of a Hamiltonian, and updates the parameters with a classical optimizer to find the ground-state energy approximately
- How it is understood in this repository: Written as a structure in which the quantum and classical layers form a closed loop. Measurements use finite shots and contain noise, so the information the classical side receives is inherently incomplete (April final version §2.1)
- Common confusions (dated): It does not mean VQE always breaks down. It means that a poor design tends to carry failure paths such as barren plateaus and noise (2026-10-23; April final version §2.1)
- JP/EN reconciliation: The abbreviation VQE is used. The Japanese "固有値ソルバ" translates "eigensolver"; it is not rendered "求解器" (confirmed 2026-10-23)
- Sources: Peruzzo et al., Nature Communications 5, 4213 (2014), DOI 10.1038/ncomms5213 (checked by search, 2026-10-23). April final version §2.1
- Related: [SPSA](#^qh-spsa), [Barren plateau](#^qh-barren-plateau), [Shot](#^qh-shot)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-nisq"></a>
### Noisy Intermediate-Scale Quantum (NISQ)
- Japanese version: [NISQ（ノイズのある中規模量子）](./Glossary_JP.md#^qh-nisq) ^qh-nisq
- Category: 外部の技術用語
- Official name and origin: Noisy Intermediate-Scale Quantum (abbreviated NISQ). J. Preskill, Quantum 2, 79 (2018)
- Meaning: The era or condition of noisy, intermediate-scale quantum devices that lack sufficient fault-tolerant computation. Circuit depth cannot be extended without limit
- How it is understood in this repository: Written as the condition for discussing "what is possible in principle" separately from "the failure paths on current hardware" (April final version §1)
- Common confusions (dated): The name of an era or condition, not of a particular device. Preskill speaks with near-term devices of roughly 50 to 100 qubits in mind (from the arXiv abstract). The guideline for the number of qubits in "intermediate-scale" varies across the literature (2026-10-23)
- JP/EN reconciliation: The abbreviation NISQ is used. The Japanese adds "ノイズのある中規模量子" and is not rendered only as "雑音つき" (confirmed 2026-10-23)
- Sources: Preskill, Quantum 2, 79 (2018), DOI 10.22331/q-2018-08-06-79 (checked by search, 2026-10-23). April final version §1
- Related: [VQE](#^qh-vqe), [Quantum error correction (QEC)](#^qh-qec)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-shot"></a>
### Shot
- Japanese version: [ショット](./Glossary_JP.md#^qh-shot) ^qh-shot
- Category: 外部の技術用語
- Official name and origin: Shot. Running a quantum circuit once and measuring it. A term widely used in quantum-computing implementation documents
- Meaning: The number of times the same circuit is run. An expectation value is estimated as the average over many shots; when the shots are independent and identically distributed, the standard error is $\sigma_0/\sqrt{M}$ ($M$ is the number of shots; $\sigma_0$ is the standard deviation of one shot)
- How it is understood in this repository: "The number of shots $M$," "the number of evaluation points," "the number of measurements," and "communication round trips" are written as separate numbers. For two-point SPSA, the evaluation points are two and the measurements are $2M$. Few-shot means $M$ of one to a few
- Common confusions (dated): Increasing shots reduces only the statistical fluctuation (shot noise). Decoherence and gate errors do not decrease (the four layers of April final version §6.1: the shot layer decays with $M$ and does not change in kind) (2026-10-23)
- JP/EN reconciliation: The katakana "ショット" is used. It is not written "試行" or "照射" (confirmed 2026-10-23)
- Sources: April final version §6.1. Paper series (`note/03_…/2026-10_SPSA更新権限/`) §2.2
- Related: [SPSA](#^qh-spsa), [Barren plateau](#^qh-barren-plateau), [Parameter-shift rule](#^qh-parameter-shift-rule)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-parameter-shift-rule"></a>
### Parameter-shift rule
- Japanese version: [パラメータシフト則](./Glossary_JP.md#^qh-parameter-shift-rule) ^qh-parameter-shift-rule
- Category: 外部の技術用語
- Official name and origin: Parameter-shift rule. Mitarai et al., Physical Review A 98, 032309 (2018). Schuld et al., Physical Review A 99, 032331 (2019)
- Meaning: A method that obtains an analytic gradient from the difference of two evaluations with the parameter shifted by a fixed amount (often $\pm\pi/2$), valid for gates of a particular form. Apart from shot noise, the gradient is exact
- How it is understood in this repository: Each parameter needs two evaluations, so the total is $2p$ ($p$ is the number of parameters). SPSA needs two, independent of the number of parameters
- Common confusions (dated): The differences from SPSA are the exactness of the gradient (exact / stochastic approximation) and the number of evaluations ($2p$ / 2). With few shots, both are affected by noise (2026-10-23)
- JP/EN reconciliation: Written "パラメータシフト則." Not written "パラメータ移動" (shift means shifting the value) (confirmed 2026-10-23)
- Sources: Mitarai et al., Physical Review A 98, 032309 (2018). Schuld et al. (five authors: Schuld, Bergholm, Gogolin, Izaac, Killoran), Physical Review A 99, 032331 (2019) (checked by search, 2026-10-23)
- Related: [SPSA](#^qh-spsa), [Shot](#^qh-shot), [VQE](#^qh-vqe)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-lindblad-equation"></a>
### Lindblad (GKSL) equation
- Japanese version: [リンドブラッド方程式（GKSL形式）](./Glossary_JP.md#^qh-lindblad-equation) ^qh-lindblad-equation
- Category: 外部の技術用語
- Official name and origin: Lindblad (GKSL) equation. G. Lindblad, Communications in Mathematical Physics 48, 119 (1976). Gorini, Kossakowski, and Sudarshan, Journal of Mathematical Physics 17, 821 (1976)
- Meaning: The equation for the time evolution of the density matrix of an open quantum system (under the Markov approximation, preserving complete positivity and trace; the formula below uses units with $\hbar=1$). $\dot\rho=-i[H,\rho]+\sum_k\left(L_k\rho L_k^\dagger-\tfrac12\{L_k^\dagger L_k,\rho\}\right)$
- How it is understood in this repository: In April B-1, the time-evolution kernel $F_{\mathrm{IDE}}$ on the NRA-IDE side was defined as this equation, to connect decoherence and dissipation with $\delta$ and $\tau$
- Common confusions (dated): The April $F_{\mathrm{IDE}}$ shares its symbol with the canonical "domain-specific base-dynamics term (not the IDE Primary Formula)" of FORMULA §5. Read it as a domain-specific term defined for the quantum system (2026-10-23). The validity of the Markov approximation and the coupling with SPSA need separate formulation (October paper v6.1 §7)
- JP/EN reconciliation: Written "リンドブラッド方程式" together with the GKSL form. It is also called the "Lindblad master equation" (confirmed 2026-10-23)
- Sources: Lindblad, Communications in Mathematical Physics 48, 119–130 (1976). Gorini, Kossakowski, and Sudarshan, Journal of Mathematical Physics 17, 821–825 (1976) (checked by search, 2026-10-23). GKS treat finite-dimensional (N-level) systems and Lindblad the more general case, which is why it is often called the Lindblad equation. April B-1 (`NRA-IDE_QuantumArchitecture_NextVer_B1toB3_…`)
- Related: [Observable expectation-value vector](#^qh-observable-expectation-vector), [Rate-limiting-stage principle](#^qh-rate-limiting-stage)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-observable-expectation-vector"></a>
### Observable expectation-value vector
- Japanese version: [観測量期待値ベクトル](./Glossary_JP.md#^qh-observable-expectation-vector) ^qh-observable-expectation-vector
- Category: 接続で生まれた用語（4月B-2）
- Official name and origin: Observable expectation-value vector $z_t$. Fixed in April B-2 (2026-04-21) as the state descriptor
- Meaning: The state descriptor passed to the judgment layer. Not the density matrix itself, but a vector of the expectation values $\langle O_i\rangle$ of measurable observables $O_i$. It does not require a complete copy of the unknown quantum state, and can be stored as a classical record
- How it is understood in this repository: Written as a descriptor defined for an observation purpose, not as the state itself. It can be compared with the delayed reference $z^{\mathrm{ref}}_{t-\ell}$
- Common confusions (dated): "Holding the whole" does not mean enumerating the whole state (QH-03, change log). It depends on the choice of observables, and if the chosen observables cannot identify an important change, the judgment has no meaning (October paper v6.1 §7) (2026-10-23)
- JP/EN reconciliation: Observable expectation-value vector. The Japanese "観測量" translates "observable" (a physical quantity), distinct from an observed value (observation) (confirmed 2026-10-23)
- Sources: April B-2 (`NRA-IDE_QuantumArchitecture_NextVer_B1toB3_…`). April final version §5
- Related: [Delayed-reference residual](#^qh-delayed-reference-residual), [Lindblad (GKSL) equation](#^qh-lindblad-equation)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-rate-limiting-stage"></a>
### Rate-limiting-stage principle
- Japanese version: [律速段原則](./Glossary_JP.md#^qh-rate-limiting-stage) ^qh-rate-limiting-stage
- Category: 接続で生まれた用語（4月B-3）
- Official name and origin: Rate-limiting-stage principle. April B-3 and final version §6.2. $\tau_{\mathrm{total}}=\min(\tau_{\mathrm{system}},\tau_{\mathrm{shot}}(N),\tau_{\mathrm{coh}}(T_2),\tau_{\mathrm{gate}}(D))$
- Meaning: The principle that, among several layers, the narrowest margin determines the limit of the whole. $\delta$ is combined by the sum of squares under an independence assumption, whereas $\tau$ is combined by the minimum. However, the $\tau$ values can be compared directly only when each $\tau$ is defined for the same target, in the same unit, and with the same meaning, in correspondence with $\delta$ (this comparability condition is not yet settled)
- How it is understood in this repository: The narrowest layer determines the Fail-Closed arrival time. It is not collapsed into a single quantity, so that the dominant layer can be read
- Common confusions (dated): The $\tau$ of the October 4 K stage heat budget is not among the four April layers (system, shot, coh, gate). How to add it as a rate-limiting stage is pending (change log QO-02) (2026-10-23)
  - Combining the $\tau$ values by their minimum does not hold as is when the $\tau$ of each layer has a different unit or scale (time, heat load, number of shots, tolerance). One candidate is to compute a dimensionless $R_i=\delta_i/\tau_i$ for each layer and take $R_{\mathrm{limiting}}=\max_i R_i$, but this is not settled as a replacement for the principle (2026-10-23)
- JP/EN reconciliation: Rate-limiting-stage principle. The same idea as the "rate-limiting step" of chemical engineering; not written "bottleneck principle" (confirmed 2026-10-23)
- Sources: April final version §6.2. April B-3
- Related: [4 K stage](#^qh-cryo-cmos-4k-stage), [Observable expectation-value vector](#^qh-observable-expectation-vector)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-delayed-reference-residual"></a>
### Delayed-reference residual (r_t of April; distinct from the canonical residual ξ)
- Japanese version: [遅延参照残差（4月の旧称は残渣 r_t。正典の残差 ξ とは別）](./Glossary_JP.md#^qh-delayed-reference-residual) ^qh-delayed-reference-residual
- Category: 接続で生まれた用語。正典の残差ξとは別（混同注意）
- Official name and origin: "遅延参照残差" (delayed-reference residual) $r_t$ . It was called "残渣" in the April quantum-architecture study (a former name). $r_t=z^{\mathrm{pred}}_{t+1}-z^{\mathrm{ref}}_{t-\ell}$ , where $\ell$ is the delayed-reference width (2026-04-29 final version §3.1; the notation was separated in the 2026-04-21 revision)
- Meaning: The difference between the predicted state descriptor and the reference delayed by $\ell$. The residual strength is $\delta_t=\lVert W r_t\rVert$ . A quantity within the April study, not a canonical quantity
- How it is understood in this repository: Written as a quantity distinct from the canonical "residual $\xi$" (FORMULA §5: $\xi=x_{\mathrm{exact}}-x$ , with a predefined high-precision reference state). The nonlinear correction map $C(r)=r\lvert r\rvert/(k+\lvert r\rvert)$ has the same form as the canonical second-order residual gate $G(\xi)$ (on the canonical side, $r$ was renamed $\xi$ on 2026-09-30)
- Common confusions (dated): The heading is now "遅延参照残差," and the April word "残渣" is kept as a former name (2026-10-23; the April documents are not rewritten). "残渣" and "残差" differ by one character and are read the same (ざんさ). 残渣 is a physical leftover (chemistry, food, industry; concrete and material); 残差 is the difference between an observed and a predicted value (mathematics, statistics; abstract and numerical). In short, 残渣 is a remainder of matter, and 残差 is a numerical deviation
  - The April "残渣" was used in two senses. (1) A difference: the gap between ideal and reality, or between a prediction and a reference (this entry) → write "残差." (2) A leftover or fractional remainder: the low-order fractional bits of floating point, and the metaphor of "residue-based" design and the "residue tank" → see [Fractional carry-over](#^qh-fractional-carry). Terms understood generally are "端数" (fraction), "丸め誤差" (rounding error), and "下位ビット" (low-order bits)
  - Of the April correction formula $z^{\mathrm{corr}}=z-\alpha\,g(R)\,C(r)$ , the $g(R)$ that sets the correction strength from $R$ is not adopted, because the evaluation output would return to its own input (AXIOMS §14; change log QH-22)
  - Distinct from the "fractional remainder" of the October fixed-point arithmetic (the low-order bits dropped by quantization): $r_t$ is a difference, the remainder is a leftover
- JP/EN reconciliation: English "residual" corresponds to Japanese "残差." The Japanese heading "遅延参照残差" and "Delayed-reference residual" correspond one to one. The distinction from the canonical residual ($\xi$) is kept by the words "delayed-reference." The April "残渣" is a former name; in English it corresponds to "residue" (a leftover) and is not used for the English name of this entry (confirmed 2026-10-23)
- Sources: `note/03_…/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md` §3.1. FORMULA.md §5. Change log QH-04 and QH-22. For the canonical residual $\xi$, see [Residual](../NRA-IDE_Dictionary_EN.md#^residual) in the dictionary
- Related: [Observable expectation-value vector](#^qh-observable-expectation-vector), [Fractional carry-over](#^qh-fractional-carry)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-fractional-carry"></a>
### Fractional carry-over
- Japanese version: [端数持ち越し](./Glossary_JP.md#^qh-fractional-carry) ^qh-fractional-carry
- Category: 接続で生まれた用語（10月）
- Official name and origin: Fractional carry-over. In the October paper series, the mechanism that carries the low-order fractional bits dropped by a fixed-point bit shift into the next step. The same form as delta-sigma modulation
- Meaning: Accumulate in an extended-precision accumulator before the shift, use only the integer part for the update, and keep the dropped low-order bits. $A_k\mathrel{-}=2^{F-s_k}\hat g_k$, $u_k=\mathrm{trunc}(A_k/2^F)$, $A_k\mathrel{-}=2^F u_k$ (assuming $F\ge s_k$ and no overflow)
- How it is understood in this repository: The form that adds the remainder after the shift (the first paper's form) loses the low-order bits at the shift, so the remainder is not carried over. Even when the shift amount changes midway, accumulate in a common high-precision unit (calculation memo C07)
  - Assumptions: the fixed-point rounding rule (truncation, rounding, etc.), the number of retained fractional bits $F$ and the bit width, and no overflow
- Common confusions (dated): The April "残渣" also had this sense of leftover or fractional remainder (the low-order fractional bits of floating point). The terms understood generally are "端数," "丸め誤差," and "下位ビット"; "残渣" is treated as a former name (2026-10-23). Distinct from the difference [Delayed-reference residual](#^qh-delayed-reference-residual)
- JP/EN reconciliation: Fractional carry-over. A concept close to rounding error in numerical analysis and to error feedback; it corresponds to the Japanese "端数" (confirmed 2026-10-23)
- Sources: Calculation memo C07 of the paper series (`note/03_…/2026-10_SPSA更新権限/中途計算_検算メモ.md`). v6.1 §5.2
- Related: [Quantization lock](#^qh-quantization-lock), [Delayed-reference residual](#^qh-delayed-reference-residual)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-quantization-lock"></a>
### Quantization lock (underflow freeze)
- Japanese version: [量子化ロック](./Glossary_JP.md#^qh-quantization-lock) ^qh-quantization-lock
- Category: 接続で生まれた用語（10月）
- Official name and origin: Quantization lock (a freeze by underflow). A term used in the October paper series
- Meaning: In fixed-point arithmetic, the phenomenon where a right shift brings the update below the least significant bit (LSB), so the update can stay at zero and freeze. It depends on the rounding rule of the implementation and the learning rate (shift amount); it is not a necessarily permanent stop
- How it is understood in this repository: It occurs when skips continue and the shift amount $s_k$ is increased. To prevent it, accumulate in extended precision before the shift (fractional carry-over). Reproduction example: with $\hat g=3$, $s=4$, and 64 steps, the form that adds the remainder after the shift gives a total update of 0 (the ideal is 12)
- Common confusions (dated): Despite the word "quantum" in the Japanese, this is not a phenomenon of quantum computing but of fixed-point quantization (rounding) (2026-10-23)
- JP/EN reconciliation: The Japanese "量子化" translates "quantization" (discretization of values), distinct from the quantum of quantum mechanics. In English it is "Quantization lock," never "quantum" (confirmed 2026-10-23)
- Sources: Calculation memo C07; reproduction script repro.py T4
- Related: [Fractional carry-over](#^qh-fractional-carry)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-lfsr"></a>
### Linear-feedback shift register (LFSR)
- Japanese version: [線形帰還シフトレジスタ（LFSR）](./Glossary_JP.md#^qh-lfsr) ^qh-lfsr
- Category: 外部の技術用語
- Official name and origin: Linear-feedback shift register (LFSR). A pseudo-random generator widely used in digital circuits
- Meaning: A circuit that generates a bit sequence by feeding register bits back linearly. It can be built with few resources and no multipliers
- How it is understood in this repository: Used to generate the $\pm1$ perturbation $\Delta_k$ of SPSA on an FPGA. To reproduce the same $\Delta_k$ later, record not only the seed but also the feedback polynomial (taps), the bit width, and how the output is taken
- Common confusions (dated): It is pseudo-random, so it is not identical to the assumption of mathematically independent symmetric signs. The effects of the period and of correlation between components must be evaluated separately (paper series v6.1 §10; 2026-10-23)
- JP/EN reconciliation: The abbreviation LFSR is used. Written "疑似乱数" (pseudo-random), not "乱数" (confirmed 2026-10-23)
- Sources: A general technical term (not checked against a source). Paper series v6.1 §10
- Related: [SPSA](#^qh-spsa), [Few-shot SPSA nominal calculation](#^qh-few-shot-spsa-nominal-calculation)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-pair-skip"></a>
### Pairwise skip of an update
- Japanese version: [ペア見送り](./Glossary_JP.md#^qh-pair-skip) ^qh-pair-skip
- Category: 接続で生まれた用語（10月）
- Official name and origin: Pairwise skip of an update. A term used in the October paper series. The state name is `SKIP_UPDATE` [extension] (not in reference implementation v2.1)
- Meaning: When one side of SPSA's forward/backward measurement pair is invalid, do not substitute or remeasure in a way whose comparison conditions cannot be guaranteed; skip the whole pair and keep the parameters at their previous values
- How it is understood in this repository: Substituting only one side (e.g., by the previous value), or remeasuring after the physical state has changed, loses the conditions of comparison and can bias the estimator. A remeasurement whose conditions hold (e.g., independent measurement noise) and whose decision does not depend on the measured value may not introduce bias. In this method, when those conditions cannot be guaranteed, the whole pair is skipped. A skip does not rewrite the observed values and leaves a record
- Common confusions (dated): Do not call the skipping of a finite, valid value `CONFESSION` (`CONFESSION` is the stop signal for unknown or invalid input; QH-09). Even skipping can leave a shrinkage bias from selection (calculation memo C08). A statistical skip is auxiliary, and the subject of judgment is the boundary approach ratio $R$ (QH-11) (2026-10-23)
- JP/EN reconciliation: Pairwise skip. Not written "discard" (the observed values are recorded, not thrown away) (confirmed 2026-10-23)
- Sources: Paper series v6.1 §4.4 and §5. Change log QH-09 and QH-11
- Related: [DiscardVault](#^qh-discard-vault), [Update permission](#^qh-update-authority)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-discard-vault"></a>
### DiscardVault
- Japanese version: [DiscardVault（見送り・境界越えの保管庫）](./Glossary_JP.md#^qh-discard-vault) ^qh-discard-vault
- Category: 参照実装の固定名と本稿での用い方の区別
- Official name and origin: `DiscardVault`. A class name in reference implementation v2.1 (`nra-core/foundations/NRA-IDE_Architecture_public.py`)
- Meaning: In the reference implementation, a simple list store with `store` and `retrieve_all`. It saves discarded items
- How it is understood in this repository: The October paper series proposes using it to record skipped measurement pairs (values, times, perturbation seeds, reasons) and the time, value, and excess of a boundary crossing [extension]. It is not used for updates of the main system
- Common confusions (dated): The first paper wrote that it splits into "orthogonal" and "high-frequency" parts and "guarantees 100% restoration"; this was retracted. It is a split by an amplitude threshold, neither orthogonal nor a frequency separation (QH-13; 2026-10-23)
- JP/EN reconciliation: As a fixed name, `DiscardVault` is written as is in both languages (confirmed 2026-10-23)
- Sources: Reference implementation v2.1. Paper series v6.1 §4.6 and §5.3. Change log QH-13
- Related: [Pairwise skip of an update](#^qh-pair-skip)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-update-authority"></a>
### Update permission
- Japanese version: [更新許可](./Glossary_JP.md#^qh-update-authority) ^qh-update-authority
- Category: 接続で生まれた用語（10月）
- Official name and origin: Update permission. The term used in the central proposition of the October paper v6.1, which called it "更新権限" (Update authority) (renamed 2026-10-23; the paper's text keeps the former name)
- Meaning: The permission to apply an optimization update. Re-check the boundary, time, version, and permission at the moment of application, and let no update pass without permission. $G_k\in\{0,1\}$
- How it is understood in this repository: $G_k=0$ does not mean the physical system has stopped; it means there is no permission for that optimization update. Thermal safety, QEC accuracy, and optimization convergence are established separately
- Common confusions (dated): The canonical AXIOMS §14 also has "更新権限" (a fixed item of Cause-Side: update authority, update path, provenance, etc.), so this term is called "更新許可" (update permission) to avoid the same name (2026-10-23). It was first written "更新権限." The canonical term is about fixing the rules and provenance of Cause-Side updates, a different context from permission to update optimization parameters
- JP/EN reconciliation: In English, Update permission (confirmed 2026-10-23). The canonical "更新権限" is rendered "update authority" (checked in FORMULA §6, THEORY, SANDWICH_ARCH, the foundational thesis, the dictionary's Evaluation Snapshot, and axioms.json). The former name Update authority would therefore collide with the canonical term in English as well; the two are kept apart as Update permission and update authority
- Sources: Paper series v6.1 §4.2–4.3. AXIOMS §14
- Related: [Pairwise skip of an update](#^qh-pair-skip), [Few-shot SPSA nominal calculation](#^qh-few-shot-spsa-nominal-calculation). For the canonical "update authority," see [Evaluation Snapshot](../NRA-IDE_Dictionary_EN.md#^evaluation-snapshot) in the dictionary
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-few-shot-spsa-nominal-calculation"></a>
### Few-shot SPSA nominal calculation
- Japanese version: [少数ショットSPSA名目計算](./Glossary_JP.md#^qh-few-shot-spsa-nominal-calculation) ^qh-few-shot-spsa-nominal-calculation
- Category: 接続で生まれた用語。旧称の「二重揺らぎ名目計算」は混同注意
- Official name and origin: Few-shot SPSA nominal calculation. The method name renamed on 2026-10-22 from "double-fluctuation nominal calculation" of the first October paper. "Nominal" is a term of this research (the NRA-IDE paper series) and means that coarse few-shot measured values (nominal values) are used; it is not a general academic term
- Meaning: A calculation that obtains the nominal gradient $\hat g$ from two few-shot measurements and the simultaneous all-dimension perturbation of SPSA. "Nominal" means that coarse few-shot measured values (nominal values) are used
- How it is understood in this repository: The number of evaluation points (two) is independent of the parameter dimension. The number of communication round trips depends on how the device batches its work and is evaluated separately from the number of evaluation points. It does not remove the exponential constraint of the barren plateau
- Common confusions (dated): The former name's "double fluctuation" shared its name with the canonical "[double fluctuation](../NRA-IDE_Dictionary_EN.md#^double-fluctuation)" (FORMULA §4.7: the simultaneous increase of $\delta$ and decrease of $\tau$). It is not used for the method name (QH-10; 2026-10-22)
- JP/EN reconciliation: Few-shot SPSA nominal calculation. The former name "double-fluctuation nominal calculation" is not used (confirmed 2026-10-23)
- Sources: Paper series v6.1 §3. Change log QH-10
- Related: [SPSA](#^qh-spsa), [Shot](#^qh-shot), [LFSR](#^qh-lfsr)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-cryo-cmos-4k-stage"></a>
### 4 K stage
- Japanese version: [4Kステージ](./Glossary_JP.md#^qh-cryo-cmos-4k-stage) ^qh-cryo-cmos-4k-stage
- Category: 外部の技術用語
- Official name and origin: 4 K stage. The roughly 4 K cooling stage of a dilution refrigerator (the second stage of the pulse-tube cryocoolers and the 4 K flange)
- Meaning: Cooling power depends strongly on the refrigerator configuration and on the temperature at which it is evaluated. What manufacturers state as guaranteed values is mainly the cooling power of the mixing chamber (20 mK): for Bluefors, above 14 μW (XLD450sl) to above 30 μW (XLD1000sl), depending on the model. The 4 K-stage watts appear in configuration-specific materials (checked 2026-10-23)
  - Bluefors XLDsl-4K (standard two-pulse-tube configuration): the second-stage cooling power is 1.35 W (PT415-ENH) and 2.35 W (PT425-ENH) at 4.2 K, and 0.9 W at 3 K. The 4 K flange (no load) is about 100–700 mW at 3 K and about 1800–2000 mW at 4.5 K (the mapping of table columns is not certain from the extraction)
  - Bluefors XLD1000sl: about 2000 mW at the 4 K flange at 4.5 K (configuration-specific official material). The XLD1000 is about 700 mW at 3 K
  - Oxford Instruments Proteox LX: more than 4 W can be applied to the 4 K stage, in addition to the static heat load, without affecting operation (two pulse tubes; no plate temperature stated; Quantum Design Oxford blog, 2025-06-09). The mixing chamber kept more than 25 μW at 20 mK at the same time
  - The first paper's "a few watts at the 4 K stage" is within these ranges. Values under different configurations and temperature conditions are not compared side by side
- How it is understood in this repository: The October paper series takes the heat budget of the 4 K stage as the evaluation target of the boundary approach ratio (an example). $\delta$ is the additional heat load, and $\tau$ comes from the cooling power at a declared operating temperature and the refrigerator health (Cause-Side observation)
- Common confusions (dated): Cooling power must not be evaluated at the stage temperature at that moment. At thermal equilibrium, $R\equiv1$ regardless of the load (QH-20, calculation memo C06). Declare each stage as a separate evaluation target and do not combine them into one ratio (2026-10-23)
  - The 4 K stage (a cooling stage, a place) and the control circuit placed there ([Cryo-CMOS](#^qh-cryo-cmos)) are different concepts. The entries were separated (2026-10-23)
- JP/EN reconciliation: Written "4Kステージ"; Cryo-CMOS is used as is (confirmed 2026-10-23)
- Sources: Paper series v6.1 §3.1. Calculation memo C06. Bluefors (the XLD and XLDsl-4K product pages, checked 2026-10-23). Quantum Design Oxford blog "Enabling Quantum Scale-Up" (2025-06-09). Per-stage cooling-power estimates are in arXiv:2502.01945 (the table values are not checked)
- Related: [Cryo-CMOS](#^qh-cryo-cmos), [Rate-limiting-stage principle](#^qh-rate-limiting-stage), [Quantum error correction (QEC)](#^qh-qec)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-cryo-cmos"></a>
### Cryo-CMOS (cryogenic CMOS)
- Japanese version: [Cryo-CMOS（極低温CMOS）](./Glossary_JP.md#^qh-cryo-cmos) ^qh-cryo-cmos
- Category: external technical term
- Official name and origin: Cryo-CMOS (cryogenic CMOS). A general technical term for CMOS circuits that operate at cryogenic temperatures
- Meaning: CMOS control and readout circuits designed and operated to work at cryogenic temperatures (around 4 K, etc.). They are placed near the qubits to reduce wiring from room temperature
- How it is understood in this repository: Its power consumption becomes the heat load of the cooling stage where it is placed. In the heat-budget example of the October paper series, the power consumption of Cryo-CMOS can be part of the heat load $\delta$ of the 4 K stage
- Common confusions (dated): The "4 K stage" is a cooling stage (a temperature stage, a place), whereas Cryo-CMOS is the circuit (control electronics) placed there. They are different concepts and are not combined in one entry (2026-10-23)
- JP/EN reconciliation: Cryo-CMOS is used as is (not yet confirmed)
- Sources: A general technical term (not checked against a source). Paper series v6.1 §3.1
- Related: [4 K stage](#^qh-cryo-cmos-4k-stage)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-qec"></a>
### Quantum error correction (QEC)
- Japanese version: [量子誤り訂正（QEC）](./Glossary_JP.md#^qh-qec) ^qh-qec
- Category: 外部の技術用語
- Official name and origin: Quantum error correction (QEC). Beginning with works such as P. W. Shor, Physical Review A 52, R2493 (1995)
- Meaning: A method that encodes information in several physical qubits and detects and corrects errors by syndrome measurement
- How it is understood in this repository: In the October paper series, decoding is separated as a high-speed path (path A) distinct from SPSA. Error suppression, mitigation, and correction are separate layers
- Common confusions (dated): NRA-IDE does not replace error suppression, mitigation, or correction; it is the design of structural audit and Fail-Closed judgment in a separate layer (QH-02; April README; 2026-10-23)
- JP/EN reconciliation: The abbreviation QEC is used. "誤り訂正" and "エラー補正" are not mixed (confirmed 2026-10-23)
- Sources: Shor, Physical Review A 52, R2493–R2496 (1995), DOI 10.1103/PhysRevA.52.R2493 (checked by search, 2026-10-23; the first quantum error-correcting code). Paper series v6.1 §4.1. April README
- Related: [Union-Find decoder](#^qh-union-find-decoder), [4 K stage](#^qh-cryo-cmos-4k-stage)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-union-find-decoder"></a>
### Union-Find decoder
- Japanese version: [Union-Find復号器](./Glossary_JP.md#^qh-union-find-decoder) ^qh-union-find-decoder
- Category: 外部の技術用語
- Official name and origin: Union-Find decoder. Delfosse and Nickerson, Quantum 5, 595 (2021). The FPGA implementation is Liyanage et al., arXiv:2406.08491 (2024)
- Meaning: A nearly linear-time decoding method that estimates errors by growing and merging clusters on the syndrome graph of a surface code or similar
- How it is understood in this repository: As an FPGA implementation example, Liyanage et al. report, on a Xilinx VCU129, an average of 11.5 ns per measurement round at code distance 21 (0.1% phenomenological noise), 23.7 ns at code distance 17 (equivalent circuit-level noise, as worded in the abstract), and 544 ns at code distance 51 in the resource-efficient configuration (Helios) (from the arXiv abstract). Values under different noise conditions and configurations are not compared side by side. The noise condition for distance 51 is not confirmed in the abstract excerpt
- Common confusions (dated): It is not claimed that replacing the distance with the Manhattan distance preserves the original decoding performance. On a square lattice with uniform weights it equals the shortest-path length, but a difference appears when circuit-level noise introduces diagonal edges or non-uniform weights (paper series v6.1 §4.1; 2026-10-23)
- JP/EN reconciliation: "Union-Find" is kept as the method name and not rendered "併合探索" (confirmed 2026-10-23)
- Sources: Delfosse and Nickerson, Quantum 5, 595 (2021), DOI 10.22331/q-2021-12-02-595. The worst-case complexity is $O(n\,\alpha(n))$ ($n$ is the number of physical qubits; $\alpha$ is the inverse Ackermann function) (checked by search, 2026-10-23). Liyanage et al. (abstract checked on the arXiv page)
- Related: [Quantum error correction (QEC)](#^qh-qec)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

