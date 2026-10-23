# NRA-IDE Quantum-Hybrid Glossary (English Version)

**Version:** 0.1 (skeleton)  
**Author:** M-Tokuni  
**Document role:** A glossary for looking up the meaning, official name, history, and common confusions of external technical terms (quantum computing, SPSA, cryogenic hardware, etc.) and of terms created where they connect to NRA-IDE. It neither creates nor changes canonical definitions  
**Paired Japanese version:** [Glossary_JP.md](./Glossary_JP.md)  
**Scope and rules:** [README.md](./README.md)

---

Status legend: [Skeleton] headings and fields only; content not yet written. [Draft] the text is written. [concepts unreconciled] the meaning and term correspondence have not been reconciled between Japanese and English. [concepts reconciled] the meaning and term correspondence have been reconciled. [full text not yet checked] the English of every field has not been checked one to one against the Japanese (when done, marked [full text checked]).

---

## Index

Look up entries by number, English name or abbreviation, or Japanese reading. T₁ and エネルギー緩和時間, for example, lead to the same entry.

**Numbers**

[4 K stage](#^qh-cryo-cmos-4k-stage)

**A–Z (English names and abbreviations)**

| Initial | Entries |
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

**Japanese names (gojūon order)**

| Row | Entries |
|---|---|
| あ行 | [位相・相対位相](#^qh-quantum-phase) / [永年近似](#^qh-secular-approximation) / [エネルギー緩和時間（T₁）](#^qh-energy-relaxation-time-t1) / [オーバーフロー](#^qh-overflow) |
| か行 | [開放量子系](#^qh-open-quantum-system) / [重ね合わせ](#^qh-superposition) / [完全正値性](#^qh-complete-positivity) / [完全正値・トレース保存写像（CPTP）](#^qh-cptp-map) / [観測量期待値ベクトル](#^qh-observable-expectation-vector) / [期待値](#^qh-expectation-value) / [ゲート誤差](#^qh-gate-error) / [原子性](#^qh-atomicity) / [更新許可](#^qh-update-authority) / [較正（校正）](#^qh-calibration) / [固定小数点](#^qh-fixed-point) / [コヒーレンス時間（T₂）](#^qh-coherence-time-t2) / [混合状態](#^qh-mixed-state) |
| さ行 | [最下位ビット（LSB）](#^qh-lsb) / [純粋状態](#^qh-pure-state) / [少数ショットSPSA名目計算](#^qh-few-shot-spsa-nominal-calculation) / [ショット](#^qh-shot) / [ショットノイズ](#^qh-shot-noise) / [シンドローム](#^qh-syndrome) / [線形帰還シフトレジスタ（LFSR）](#^qh-lfsr) |
| た行 | [遅延参照残差（4月の旧称は残渣 r_t。正典の残差 ξ とは別）](#^qh-delayed-reference-residual) / [データ年齢（測定データの経過時間）](#^qh-data-age) / [デコヒーレンス](#^qh-decoherence) / [同時摂動確率近似（SPSA）](#^qh-spsa) / [ドリフト](#^qh-drift) |
| は行 | [バイアス（推定の偏り）](#^qh-estimator-bias) / [端数持ち越し](#^qh-fractional-carry) / [ハミルトニアン](#^qh-hamiltonian) / [パラメータシフト則](#^qh-parameter-shift-rule) / [バレンプラトー（勾配消失の台地）](#^qh-barren-plateau) / [版管理（パラメータ版・境界版・測定時刻）](#^qh-version-check) / [半群（量子力学的半群）](#^qh-dynamical-semigroup) / [標準誤差](#^qh-standard-error) / [復号](#^qh-decoding) / [分散](#^qh-variance) / [ペア見送り](#^qh-pair-skip) / [変分量子固有値ソルバ（VQE）](#^qh-vqe) / [ボルン近似（Born近似）](#^qh-born-approximation) |
| ま行 | [マルコフ近似](#^qh-markov-approximation) / [密度行列](#^qh-density-matrix) |
| ら行 | [律速段原則](#^qh-rate-limiting-stage) / [量子誤り訂正（QEC）](#^qh-qec) / [量子化ロック](#^qh-quantization-lock) / [量子干渉](#^qh-quantum-interference) / [量子コヒーレンス](#^qh-quantum-coherence) / [量子ビット](#^qh-qubit) / [リンドブラッド方程式（GKSL形式）](#^qh-lindblad-equation) |

---

## From former names to current entries

The old documents are kept, not deleted. This index leads from a word in an old document to the current concept.

| Former name | Appears in | Current entry |
|---|---|---|
| 残渣 $r_t$ (in the sense of a difference) | April quantum-architecture study | [Delayed-reference residual](#^qh-delayed-reference-residual) |
| 残渣 (in the sense of a leftover or fractional remainder) | April quantum-architecture study; "residue-based" and "residue tank" | [Fractional carry-over](#^qh-fractional-carry) |
| Double-fluctuation nominal calculation | The first October paper | [Few-shot SPSA nominal calculation](#^qh-few-shot-spsa-nominal-calculation) |
| 更新権限 (permission to update optimization) | The text of the October paper v6.1 | [Update permission](#^qh-update-authority) |
| 4 K stage (Cryo-CMOS) | The first October paper §1 | [4 K stage](#^qh-cryo-cmos-4k-stage), [Cryo-CMOS](#^qh-cryo-cmos) |
| Over-precise computation (the explanation given as the cause of the barren plateau) | The first October paper (retracted) | [Barren plateau](#^qh-barren-plateau) |

---

## Entries

Entries are ordered by number, then by English heading from A to Z. The Japanese edition orders Japanese headings by reading; both editions retain the same entry IDs.

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

<a id="qh-atomicity"></a>
### Atomicity
- Japanese version: [原子性](./Glossary_JP.md#^qh-atomicity) ^qh-atomicity
- Category: External technical term
- Official name and origin: Atomicity. A term in concurrency and transactions.
- Meaning: A property treating an operation as indivisible within its declared observation scope. In databases, atomicity means a transaction takes effect in full or is rolled back in full. Visibility of intermediate states also concerns isolation.
- How it is understood in this repository: Used to reason about intervening updates between version validation and applying an update. A compare-and-swap on one variable does not necessarily protect validation and application across multiple fields.
- Common confusions (dated): This is not an atomic-physics term. Memory operations, persistence, and physical-device actions have different protection scopes. Atomicity alone does not prevent stale data or permission errors. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Atomicity and 原子性. Specify the protected operation and observation scope.
- Sources: [Microsoft: InterlockedCompareExchange](https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-interlockedcompareexchange); [PostgreSQL: Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html); [October paper v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Version management (parameter version, boundary version, measurement time)](#^qh-version-check), [Update permission](#^qh-update-authority), [Data age (measurement age)](#^qh-data-age)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-born-approximation"></a>
### Born approximation
- Japanese version: [ボルン近似（Born近似）](./Glossary_JP.md#^qh-born-approximation) ^qh-born-approximation
- Category: External technical term
- Official name and origin: Born approximation. This entry concerns its use in deriving open-system master equations, not scattering theory in general.
- Meaning: A weak-coupling approximation treating changes in the environment and system–environment correlations as small. A typical derivation approximates the joint state by a product of the system state and a nearly fixed environmental state.
- How it is understood in this repository: Treated in the GKSL detail as a condition of a representative microscopic derivation, not a declaration that absence of correlations has been verified in a device.
- Common confusions (dated): Born and Markov approximations are distinct assumptions. Neglecting correlations in an approximation is not the same as their always being absent physically. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Born approximation and ボルン近似, also retaining Born近似 as a lookup form.
- Sources: [QuTiP: Lindblad Master Equation Solver](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html); [GKSL detailed explanation](./details/Lindblad_GKSL_EN.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Markov approximation](#^qh-markov-approximation), [Secular approximation](#^qh-secular-approximation), [Open quantum system](#^qh-open-quantum-system)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-calibration"></a>
### Calibration
- Japanese version: [較正（校正）](./Glossary_JP.md#^qh-calibration) ^qh-calibration
- Category: External technical term
- Official name and origin: Calibration. A standard metrology term defined in VIM 2.39, normally written 校正 in Japanese metrology. The paper's spelling 較正 leads to the same entry.
- Meaning: An operation establishing, under specified conditions, a relationship between reference values with uncertainties and instrument indications with uncertainties, then using that relationship to obtain measurement results.
- How it is understood in this repository: Used to understand when and under which conditions readout or control settings were characterized. Adding this entry does not mean calibration of the paper's model or hardware has been performed.
- Common confusions (dated): Calibration differs from adjustment. It does not eliminate all error, and changes in conditions or drift can affect its validity. It is also distinct from verification of conformity. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Calibration and 較正（校正）. The two Japanese spellings are not separate concepts.
- Sources: [JCGM VIM3: calibration (2.39)](https://jcgm.bipm.org/vim/en/2.39.html); [October paper v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Drift](#^qh-drift), [Data age (measurement age)](#^qh-data-age), [Gate error](#^qh-gate-error)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-coherence-time-t2"></a>
### Coherence time (T₂)
- Japanese version: [コヒーレンス時間（T₂）](./Glossary_JP.md#^qh-coherence-time-t2) ^qh-coherence-time-t2
- Category: External technical term
- Official name and origin: Coherence time or transverse relaxation time, symbol $T_2$. A time characterizing decay of a qubit's phase coherence
- Meaning: In a simple exponential-decay model, the magnitude of an off-diagonal density-matrix entry in the energy basis decays as $\lvert\rho_{01}(t)\rvert=\lvert\rho_{01}(0)\rvert e^{-t/T_2}$. At $t=T_2$, about 36.8% of its initial magnitude remains. The unit is seconds; microseconds and other scales are also used
- How it is understood in this repository: April's $\tau_{\mathrm{coh}}(T_2)$ is a proposal to construct an allowance using T₂. Do not directly compare T₂, a time, with a thermal-balance $\tau$ having a different unit
- Common confusions (dated): T₂ is not a deadline before which no error occurs and after which the qubit suddenly fails. Energy relaxation also contributes to coherence decay, so T₂ is not necessarily a time for pure phase noise alone. Distinguish Ramsey $T_2^*$ from echo and other T₂ measurements by specifying the measurement procedure (2026-10-24)
- JP/EN reconciliation: Proposed pair: Coherence time (T₂) and コヒーレンス時間（T₂）. Record transverse relaxation time as a synonym, keeping T₁ in a separate entry (2026-10-24; reconciliation pending)
- Sources: [IBM Quantum Learning, "Noise and errors"](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/noise-and-errors), [Qiskit Aer, "thermal_relaxation_error"](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.thermal_relaxation_error.html), and [Qiskit Experiments, "T2Hahn"](https://qiskit-community.github.io/qiskit-experiments/stubs/qiskit_experiments.library.characterization.T2Hahn.html) (text checked 2026-10-24). [April final version](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §6.2 and §7.4
- Related: [Quantum coherence](#^qh-quantum-coherence), [Decoherence](#^qh-decoherence), [Energy relaxation time (T₁)](#^qh-energy-relaxation-time-t1), [Rate-limiting-stage principle](#^qh-rate-limiting-stage)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-complete-positivity"></a>
### Complete positivity
- Japanese version: [完全正値性](./Glossary_JP.md#^qh-complete-positivity) ^qh-complete-positivity
- Category: External technical term
- Official name and origin: Complete positivity (CP). A property of linear maps in quantum information.
- Meaning: The property that a map preserves positive semidefiniteness of joint states when combined with the identity map on any ancillary system. It is stronger than positivity on the system alone.
- How it is understood in this repository: A term for the mathematical consistency of quantum channels generated by GKSL dynamics. It prevents inconsistent negative probabilities even for inputs entangled with an ancillary system.
- Common confusions (dated): Complete positivity alone does not imply trace preservation. Complete does not mean guaranteeing thermal safety or a correct computational answer. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Complete positivity and 完全正値性, with abbreviation CP.
- Sources: [IBM Quantum: Quantum channel basics](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/quantum-channel-basics); [IBM Quantum: Channel representations](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/representations-of-channels); [GKSL detailed explanation](./details/Lindblad_GKSL_EN.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Completely positive trace-preserving map (CPTP)](#^qh-cptp-map), [Density matrix](#^qh-density-matrix), [Semigroup (quantum dynamical semigroup)](#^qh-dynamical-semigroup)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-cptp-map"></a>
### Completely positive trace-preserving map (CPTP)
- Japanese version: [完全正値・トレース保存写像（CPTP）](./Glossary_JP.md#^qh-cptp-map) ^qh-cptp-map
- Category: External technical term
- Official name and origin: Completely positive trace-preserving map (CPTP). The standard mathematical description of a quantum channel.
- Meaning: A linear map that is both completely positive and trace-preserving. It maps normalized density matrices to density matrices while preserving total probability, including when applied to a system correlated with an ancilla.
- How it is understood in this repository: A property of the analytic evolution generated by GKSL equations. Check it separately from positivity preservation by a chosen numerical integration method.
- Common confusions (dated): An operation selecting a particular measurement outcome can decrease trace before renormalization. Not every conditional operation is a CPTP map. (2026-10-24)
- JP/EN reconciliation: Keep CPTP as an abbreviation and expand its two conditions. TP means trace-preserving.
- Sources: [IBM Quantum: Quantum channel basics](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/quantum-channel-basics); [GKSL detailed explanation](./details/Lindblad_GKSL_EN.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Complete positivity](#^qh-complete-positivity), [Semigroup (quantum dynamical semigroup)](#^qh-dynamical-semigroup), [Lindblad (GKSL) equation](#^qh-lindblad-equation), [Density matrix](#^qh-density-matrix)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-data-age"></a>
### Data age (measurement age)
- Japanese version: [データ年齢（測定データの経過時間）](./Glossary_JP.md#^qh-data-age) ^qh-data-age
- Category: External technical term
- Official name and origin: Data age / measurement age. A descriptive term for elapsed time between measurement and use.
- Meaning: Elapsed time from acquiring a measurement to using it for a decision or update. Compute the difference on a common time base and account for clock synchronization and timestamp uncertainty.

$$
t_{\mathrm{age}}=t_{\mathrm{use}}-t_{\mathrm{measurement}}.
$$

- How it is understood in this repository: Used to assess measurement-pair age when applying asynchronous SPSA updates. Declare an acceptable-age condition separately from version equality.
- Common confusions (dated): Reception time is not necessarily measurement time. Monotonic-clock origins are not necessarily shared between computers, so raw readings cannot automatically be subtracted. A fresh measurement does not guarantee valid calibration. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Data age and データ年齢, with an explanatory measurement-age label. No new canonical metric is defined.
- Sources: [Python: time.monotonic](https://docs.python.org/3/library/time.html#time.monotonic); [October paper v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Version management (parameter version, boundary version, measurement time)](#^qh-version-check), [Atomicity](#^qh-atomicity), [Drift](#^qh-drift), [Calibration](#^qh-calibration)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-decoding"></a>
### Decoding
- Japanese version: [復号](./Glossary_JP.md#^qh-decoding) ^qh-decoding
- Category: External technical term
- Official name and origin: Decoding. A standard coding-theory term.
- Meaning: The process of inferring a recovery operation or logical correction from a syndrome and an assumed error model. Exact identification of the physical error is not always needed if its logical effect can be corrected.
- How it is understood in this repository: Union-Find is one decoding method. Evaluate decoding latency, failure rate, and supported noise models separately.
- Common confusions (dated): The context differs from decryption. A faster decoder alone does not guarantee an error-correction threshold or hardware success rate. (2026-10-24)
- JP/EN reconciliation: Proposed pairs: Decoding and 復号; decoder and 復号器.
- Sources: [IBM Quantum: Error correction II](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/error-correction-ii) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Syndrome](#^qh-syndrome), [Quantum error correction (QEC)](#^qh-qec), [Union-Find decoder](#^qh-union-find-decoder)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-decoherence"></a>
### Decoherence
- Japanese version: [デコヒーレンス](./Glossary_JP.md#^qh-decoherence) ^qh-decoherence
- Category: External technical term
- Official name and origin: Decoherence. The standard term for loss of quantum coherence through interaction with the environment. Zurek's review is a representative explanatory source, not a citation for the first coining of the term
- Meaning: A process in which interaction with the environment makes interference between superposition components less accessible when considering the quantum system alone. Information also spreads into the environment; in the system's reduced density matrix, this appears as decay of off-diagonal entries in the relevant basis
- How it is understood in this repository: A physical process relevant to the April error layers and the Lindblad state model. October's update permission restricts application of old results; it is not itself a mechanism that prevents decoherence
- Common confusions (dated): Distinguish it from shot noise, where an estimated mean fluctuates because there are few measurements. It does not necessarily involve energy loss, nor does it mean destruction of information in the combined system and environment (2026-10-24)
- JP/EN reconciliation: Proposed pair: Decoherence and デコヒーレンス. Keep the spelling used in existing documents and link it with quantum coherence (2026-10-24; reconciliation pending)
- Sources: [Zurek, "Decoherence, einselection, and the quantum origins of the classical"](https://arxiv.org/abs/quant-ph/0105127), and [IBM Quantum Learning, "Noise and errors"](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/noise-and-errors) (abstract and text, respectively, checked 2026-10-24). [April final version](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §4 and §6
- Related: [Quantum coherence](#^qh-quantum-coherence), [Density matrix](#^qh-density-matrix), [Lindblad equation](#^qh-lindblad-equation), [Shot noise](#^qh-shot-noise), [Update permission](#^qh-update-authority)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-density-matrix"></a>
### Density matrix
- Japanese version: [密度行列](./Glossary_JP.md#^qh-density-matrix) ^qh-density-matrix
- Category: External technical term
- Official name and origin: Density matrix. A standard matrix representation of a quantum state, usually written $\rho$. It is also called a density operator
- Meaning: A representation covering both pure and mixed quantum states. In finite dimensions, it is a positive-semidefinite matrix with diagonal entries summing to 1. Positive semidefiniteness is required to prevent negative probabilities in measurements computed from the matrix. In a chosen basis, diagonal entries give basis-state probabilities and off-diagonal entries represent coherence between components
- How it is understood in this repository: The object evolving in April's Lindblad-centered proposal; it differs from the observable expectation-value vector passed to the judgment layer. A few expectation values are not assumed sufficient to reconstruct an arbitrary full density matrix
- Common confusions (dated): It is not a table of material densities or thermal loads. One measurement does not reveal an unknown density matrix. A probabilistic mixture and a pure superposition can be indistinguishable from their 0/1 probabilities alone (2026-10-24)
- JP/EN reconciliation: Proposed pairs: Density matrix and 密度行列; density operator and 密度演算子. Here $\rho$ denotes a quantum state and is distinguished from a correlation coefficient or other uses in different contexts (2026-10-24; reconciliation pending)
- Sources: [IBM Quantum Learning, "Density matrix basics"](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/density-matrix-basics) (text checked 2026-10-24). [April final version](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §4 and §5
- Related: [Superposition](#^qh-superposition), [Quantum coherence](#^qh-quantum-coherence), [Expectation value](#^qh-expectation-value), [Observable expectation-value vector](#^qh-observable-expectation-vector), [Lindblad equation](#^qh-lindblad-equation), [Pure state](#^qh-pure-state), [Mixed state](#^qh-mixed-state)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-drift"></a>
### Drift
- Japanese version: [ドリフト](./Glossary_JP.md#^qh-drift) ^qh-drift
- Category: External technical term
- Official name and origin: Drift. In metrology, a slow change in instrument response over time.
- Meaning: A change in instrument or device response over time, distinguished from short-term random variation. Specify what changed, over which interval, and in which quantity.
- How it is understood in this repository: Used to assess effects of measurement age and calibration validity. Distinguish changes in the system state from changes in readout response.
- Common confusions (dated): Do not label every noise source or degradation as drift. Adapting a threshold alone does not demonstrate that device changes have been correctly calibrated. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Drift and ドリフト. Specify instrument drift or another scope where appropriate.
- Sources: [NIST: Drift](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc453.htm); [October paper v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Calibration](#^qh-calibration), [Data age (measurement age)](#^qh-data-age), [Shot noise](#^qh-shot-noise)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-energy-relaxation-time-t1"></a>
### Energy relaxation time (T₁)
- Japanese version: [エネルギー緩和時間（T₁）](./Glossary_JP.md#^qh-energy-relaxation-time-t1) ^qh-energy-relaxation-time-t1
- Category: External technical term
- Official name and origin: Energy relaxation time or longitudinal relaxation time, symbol $T_1$. The time scale for the excited-state population to approach its equilibrium value
- Meaning: Describes how quickly a qubit's excited-state population changes through energy exchange with the environment. In an exponential-decay model initialized in the excited state, with negligible upward excitation, the probability of remaining excited is $p_1(t)=e^{-t/T_1}$. The unit is seconds
- How it is understood in this repository: A basic term for distinguishing energy-exchanging relaxation from phase disturbances without energy exchange when describing decoherence
- Common confusions (dated): T₁ and T₂ are different quantities. At finite temperature where upward excitation cannot be neglected, the excited-state population approaches the equilibrium value for those conditions rather than zero. T₁ alone does not determine gate accuracy or the safety of the whole device (2026-10-24)
- JP/EN reconciliation: Proposed pair: Energy relaxation time (T₁) and エネルギー緩和時間（T₁）. "Relaxation time" alone does not distinguish it from T₂ and other times, so the heading specifies its subject (2026-10-24; reconciliation pending)
- Sources: [IBM Quantum Learning, "Noise and errors"](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/noise-and-errors), and [Qiskit Aer, "thermal_relaxation_error"](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.thermal_relaxation_error.html) (text checked 2026-10-24)
- Related: [Coherence time (T₂)](#^qh-coherence-time-t2), [Decoherence](#^qh-decoherence), [Qubit](#^qh-qubit)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-estimator-bias"></a>
### Estimator bias
- Japanese version: [バイアス（推定の偏り）](./Glossary_JP.md#^qh-estimator-bias) ^qh-estimator-bias
- Category: External technical term
- Official name and origin: Estimator bias. A statistical-estimation term.
- Meaning: The difference between an estimator's expected value and the true value being estimated. The expectation below is over the specified measurement or sampling model.

$$
\operatorname{Bias}(\hat{\theta})=\mathbb{E}[\hat{\theta}]-\theta.
$$

- How it is understood in this repository: Used to assess effects of finite SPSA perturbations and selection of measurement pairs. State selection conditions when analyzing only retained samples.
- Common confusions (dated): Zero bias can coexist with large variance. Bias relates to systematic measurement effects but does not always mean a single instrument offset. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Estimator bias and バイアス（推定の偏り）.
- Sources: [NIST: Analysis of bias](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc45.htm); [October paper v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Variance](#^qh-variance), [Standard error](#^qh-standard-error), [Simultaneous Perturbation Stochastic Approximation (SPSA)](#^qh-spsa), [Pairwise skip of an update](#^qh-pair-skip)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-expectation-value"></a>
### Expectation value
- Japanese version: [期待値](./Glossary_JP.md#^qh-expectation-value) ^qh-expectation-value
- Category: External technical term
- Official name and origin: Expectation value. A standard term in probability, statistics, and quantum mechanics. Here the focus is the mean of a quantum-measurement outcome distribution
- Meaning: The sum of possible measurement values weighted by their probabilities. For a finite-dimensional quantum state with density matrix $\rho$ and observable O, $\langle O\rangle=\mathrm{Tr}(\rho O)$. Tr denotes the sum of a matrix's diagonal entries
- How it is understood in this repository: April's state descriptor is a vector of expectation values. A sample mean from finitely many device shots is an estimate of an expectation value and is accompanied by its shot count and uncertainty
- Common confusions (dated): An expectation value is not a desired value. It need not occur as an individual measurement result: equally probable results 0 and 1 have expectation 0.5, while each result remains either 0 or 1 (2026-10-24)
- JP/EN reconciliation: Proposed pair: Expectation value and 期待値. Distinguish it from an observed value, sample mean, and reference value (2026-10-24; reconciliation pending)
- Sources: Expectation-value definition in [IBM Quantum Learning, "Cost functions"](https://quantum.cloud.ibm.com/learning/en/courses/variational-algorithm-design/cost-functions) (text checked 2026-10-24). [April final version](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §5
- Related: [Observable expectation-value vector](#^qh-observable-expectation-vector), [Density matrix](#^qh-density-matrix), [Shot noise](#^qh-shot-noise), canonical [Observation value](../NRA-IDE_Dictionary_EN.md#^observation-value)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-fixed-point"></a>
### Fixed-point representation
- Japanese version: [固定小数点](./Glossary_JP.md#^qh-fixed-point) ^qh-fixed-point
- Category: External technical term
- Official name and origin: Fixed-point representation. A numerical representation in computing.
- Meaning: A representation multiplying an integer I by a fixed scale. With F binary fractional bits, the value is I times 2 to the power minus F. The range below assumes signed n-bit two's-complement integers and nonnegative integer F.

$$
x=I\,2^{-F},\qquad -2^{n-1-F}\leq x\leq(2^{n-1}-1)2^{-F}.
$$

- How it is understood in this repository: Needed for fractional carry-over and quantization lock. Record bit width, scale, rounding, and saturation conditions together.
- Common confusions (dated): Fixed-point discretization is a computational representation, distinct from quantum-mechanical quantization. Q-format conventions can count sign bits differently; state explicit widths and scales. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Fixed-point representation and 固定小数点.
- Sources: [Arm CMSIS-DSP: fixed-point data types](https://arm-software.github.io/CMSIS-DSP/latest/namespacearm__cmsis__dsp.html); [Arm CMSIS-DSP: Fixed point datatypes](https://arm-software.github.io/CMSIS-DSP/latest/group__FIXED.html); [October paper v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Least significant bit (LSB)](#^qh-lsb), [Overflow](#^qh-overflow), [Fractional carry-over](#^qh-fractional-carry), [Quantization lock (underflow freeze)](#^qh-quantization-lock)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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
- Related: [Quantization lock](#^qh-quantization-lock), [Delayed-reference residual](#^qh-delayed-reference-residual), [Fixed-point representation](#^qh-fixed-point), [Least significant bit (LSB)](#^qh-lsb), [Overflow](#^qh-overflow)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-gate-error"></a>
### Gate error
- Japanese version: [ゲート誤差](./Glossary_JP.md#^qh-gate-error) ^qh-gate-error
- Category: External technical term
- Official name and origin: Gate error. The standard term for a difference between an ideal quantum-gate operation and the actual operation
- Meaning: Deviation of an operation on a quantum state from its intended operation. Examples include systematic rotation-angle errors and interaction with the environment during gate operation. Distinguish components that repeatedly deviate in the same direction from components that vary stochastically
- How it is understood in this repository: Relevant to the gate layer of April's four-layer structure. Specify the error metric, measurement method, circuit depth, and correlation assumptions; do not infer accumulation from gate count alone
- Common confusions (dated): Not every gate error is decoherence, nor can gate errors be removed merely by increasing the shot count. Gate fidelity, average gate error, and circuit output-error probability are not interchangeable numbers without their definitions (2026-10-24)
- JP/EN reconciliation: Proposed pair: Gate error and ゲート誤差. If using "error rate," write 誤差率 and specify the metric whose rate is meant (2026-10-24; reconciliation pending)
- Sources: Imperfect-gate and coherent-error explanations in [IBM Quantum Learning, "Noise and errors"](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/noise-and-errors) (text checked 2026-10-24). [April final version](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §6.1
- Related: [Decoherence](#^qh-decoherence), [Shot noise](#^qh-shot-noise), [Quantum error correction (QEC)](#^qh-qec), [Rate-limiting-stage principle](#^qh-rate-limiting-stage)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-hamiltonian"></a>
### Hamiltonian
- Japanese version: [ハミルトニアン](./Glossary_JP.md#^qh-hamiltonian) ^qh-hamiltonian
- Category: External technical term
- Official name and origin: Hamiltonian. In quantum mechanics, the Hermitian operator H representing energy.
- Meaning: The operator specifying a system's energy and unitary evolution. It changes the state through a commutator with the density matrix and may include time-dependent driving or effective energy-level shifts.
- How it is understood in this repository: Appears in the first term of the GKSL equation. The detailed explanation uses angular-frequency units, energy divided by hbar.
- Common confusions (dated): Unitary evolution can change system energy under time-dependent external driving. H alone does not necessarily include all environmental dissipation. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Hamiltonian and ハミルトニアン. State the units of H and which effective terms are included.
- Sources: [QuTiP: Lindblad Master Equation Solver](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html); [GKSL detailed explanation](./details/Lindblad_GKSL_EN.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Lindblad (GKSL) equation](#^qh-lindblad-equation), [Expectation value](#^qh-expectation-value), [Open quantum system](#^qh-open-quantum-system)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-lsb"></a>
### Least significant bit (LSB)
- Japanese version: [最下位ビット（LSB）](./Glossary_JP.md#^qh-lsb) ^qh-lsb
- Category: External technical term
- Official name and origin: Least significant bit (LSB). The lowest-order bit of a binary word.
- Meaning: The bit position with the smallest weight. As a numerical amount, one LSB means the smallest increment associated with that position in the specified format.
- How it is understood in this repository: Used for the increment triggering fractional carry-over. With F binary fractional bits, one LSB corresponds to a value of 2 to the power minus F.
- Common confusions (dated): Distinguish the bit position from its numerical weight. The label one LSB alone does not specify a physical unit such as voltage or angle. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Least significant bit and 最下位ビット, retaining LSB.
- Sources: [Arm CMSIS-DSP: fixed-point data types](https://arm-software.github.io/CMSIS-DSP/latest/namespacearm__cmsis__dsp.html); [October paper v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Fixed-point representation](#^qh-fixed-point), [Fractional carry-over](#^qh-fractional-carry), [Quantization lock (underflow freeze)](#^qh-quantization-lock)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-lindblad-equation"></a>
### Lindblad (GKSL) equation
- Japanese version: [リンドブラッド方程式（GKSL形式）](./Glossary_JP.md#^qh-lindblad-equation) ^qh-lindblad-equation
- Category: 外部の技術用語
- Official name and origin: Lindblad (GKSL) equation. G. Lindblad, Communications in Mathematical Physics 48, 119 (1976). Gorini, Kossakowski, and Sudarshan, Journal of Mathematical Physics 17, 821 (1976)
- Meaning: A basic form for Markovian open-system dynamics, giving the general generator of a continuous, time-homogeneous CPTP quantum dynamical semigroup in finite dimensions. H is Hermitian and rates are incorporated in the operators below, in units with $\hbar=1$. [Reading the formula and its conditions](./details/Lindblad_GKSL_EN.md) explains the symbols, jump normalization, rate conventions, and derivation approximations.

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

- How it is understood in this repository: In April B-1, the time-evolution kernel $F_{\mathrm{IDE}}$ on the NRA-IDE side was defined as this equation, to connect decoherence and dissipation with $\delta$ and $\tau$
- Common confusions (dated): The April $F_{\mathrm{IDE}}$ shares its symbol with the canonical "domain-specific base-dynamics term (not the IDE Primary Formula)" of FORMULA §5. Read it as a domain-specific term defined for the quantum system (2026-10-23). The validity of the Markov approximation and the coupling with SPSA need separate formulation (October paper v6.1 §7)
- JP/EN reconciliation: Written "リンドブラッド方程式" together with the GKSL form. It is also called the "Lindblad master equation" (confirmed 2026-10-23)
- Sources: [Lindblad (1976)](https://link.springer.com/article/10.1007/BF01608499), and [Gorini, Kossakowski, and Sudarshan (1976)](https://repository.ias.ac.in/51137/) (bibliographies and abstracts checked 2026-10-24; distinct from reading the full original papers). [QuTiP master-equation documentation](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html) and [quantum-jump documentation](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-monte.html) checked in the text. Full references and verification scope are in the [detailed explanation](./details/Lindblad_GKSL_EN.md), §9. The April B-1 positioning is retained as research history.
- Related: [Density matrix](#^qh-density-matrix), [Decoherence](#^qh-decoherence), [T₁](#^qh-energy-relaxation-time-t1), [T₂](#^qh-coherence-time-t2), [Observable expectation-value vector](#^qh-observable-expectation-vector), [Rate-limiting-stage principle](#^qh-rate-limiting-stage), [Open quantum system](#^qh-open-quantum-system), [Hamiltonian](#^qh-hamiltonian), [Markov approximation](#^qh-markov-approximation), [Born approximation](#^qh-born-approximation), [Secular approximation](#^qh-secular-approximation), [Complete positivity](#^qh-complete-positivity), [Completely positive trace-preserving map (CPTP)](#^qh-cptp-map), [Semigroup (quantum dynamical semigroup)](#^qh-dynamical-semigroup)
- Status: [Draft] [concepts unreconciled] [full text not yet checked] (after the 2026-10-24 expansion; the term correspondence was confirmed 2026-10-23)


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

<a id="qh-markov-approximation"></a>
### Markov approximation
- Japanese version: [マルコフ近似](./Glossary_JP.md#^qh-markov-approximation) ^qh-markov-approximation
- Category: External technical term
- Official name and origin: Markov approximation. Used in open-system derivations to neglect environmental memory.
- Meaning: An approximation treating evolution without dependence on the full past history when environmental correlations decay much faster than system relaxation. A recent timestamp alone does not establish this condition.
- How it is understood in this repository: An applicability condition to check before using the Lindblad-centered proposal for a particular quantum system. It differs from checking asynchronous data versions and age.
- Common confusions (dated): A time-local differential equation alone does not establish absence of environmental memory or the CPTP property. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Markov approximation and マルコフ近似. Distinguish mathematical definitions of Markovianity from approximation steps in a physical derivation.
- Sources: [QuTiP: Lindblad Master Equation Solver](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html); [GKSL detailed explanation](./details/Lindblad_GKSL_EN.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Open quantum system](#^qh-open-quantum-system), [Born approximation](#^qh-born-approximation), [Secular approximation](#^qh-secular-approximation), [Completely positive trace-preserving map (CPTP)](#^qh-cptp-map)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-mixed-state"></a>
### Mixed state
- Japanese version: [混合状態](./Glossary_JP.md#^qh-mixed-state) ^qh-mixed-state
- Category: External technical term
- Official name and origin: Mixed state. A standard quantum-information term for a state whose density matrix is not pure.
- Meaning: A non-pure quantum state representable as a probabilistic mixture of pure states. For a normalized finite-dimensional state, the trace of the squared density matrix is less than 1. The mixture decomposition is generally not unique.

$$
\rho=\sum_i p_i\lvert\psi_i\rangle\langle\psi_i\rvert,\quad p_i\geq0,\quad \sum_i p_i=1,\quad \operatorname{Tr}(\rho^2)<1.
$$

- How it is understood in this repository: Needed when describing environmental interaction or a subsystem alone. Density matrices represent both pure and mixed states.
- Common confusions (dated): A pure superposition differs from a probabilistic mixture. A subsystem of an entangled pure joint state can also be mixed. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Mixed state and 混合状態. Mixture refers to a convex combination of density matrices, not simply adding amplitudes.
- Sources: [IBM Quantum: Convex combinations of density matrices](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/convex-combinations); [IBM Quantum: Density matrix basics](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/density-matrix-basics) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Pure state](#^qh-pure-state), [Density matrix](#^qh-density-matrix), [Superposition](#^qh-superposition), [Open quantum system](#^qh-open-quantum-system)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-open-quantum-system"></a>
### Open quantum system
- Japanese version: [開放量子系](./Glossary_JP.md#^qh-open-quantum-system) ^qh-open-quantum-system
- Category: External technical term
- Official name and origin: Open quantum system. A standard quantum-mechanical term for a system considered with its interaction with an environment.
- Meaning: A quantum system interacting with an environment. Its state alone is represented by a density matrix obtained by tracing out the environmental degrees of freedom from the joint state. Exchanges of information or energy affect its evolution.
- How it is understood in this repository: The subject of April's Lindblad model. Being open does not itself justify a Markov approximation or GKSL form.
- Common confusions (dated): Distinguish the joint system–environment description from the reduced system description. Loss of system coherence is not identical to destruction of all information in the combined system. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Open quantum system and 開放量子系. An informal description as an open system does not replace specifying its system–environment boundary.
- Sources: [QuTiP: Lindblad Master Equation Solver](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html); [GKSL detailed explanation](./details/Lindblad_GKSL_EN.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Density matrix](#^qh-density-matrix), [Decoherence](#^qh-decoherence), [Markov approximation](#^qh-markov-approximation), [Lindblad (GKSL) equation](#^qh-lindblad-equation)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-overflow"></a>
### Overflow
- Japanese version: [オーバーフロー](./Glossary_JP.md#^qh-overflow) ^qh-overflow
- Category: External technical term
- Official name and origin: Overflow. Exceeding the representable range of a numerical format.
- Meaning: An arithmetic result outside the range of the specified bit width and format. For example, signed four-bit integers range from minus eight to seven, so the mathematical result eight from seven plus one is unrepresentable.
- How it is understood in this repository: Check intermediate ranges as well as outputs in fractional carry accumulators and fixed-point arithmetic. Declare saturation and fault-detection policies for each implementation.
- Common confusions (dated): Wrapping, saturation, and exceptions are different behaviors. Signed overflow can be undefined for particular languages and types; wrapping is not universal. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Overflow and オーバーフロー.
- Sources: [Arm CMSIS-DSP: Fixed point datatypes](https://arm-software.github.io/CMSIS-DSP/latest/group__FIXED.html) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Fixed-point representation](#^qh-fixed-point), [Least significant bit (LSB)](#^qh-lsb), [Fractional carry-over](#^qh-fractional-carry)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-quantum-phase"></a>
### Phase and relative phase
- Japanese version: [位相・相対位相](./Glossary_JP.md#^qh-quantum-phase) ^qh-quantum-phase
- Category: External technical term
- Official name and origin: Phase and relative phase. Terms for the angles of waves or complex amplitudes; differences between component phases affect interference in quantum states
- Meaning: In $a\lvert0\rangle+b e^{i\phi}\lvert1\rangle$, with $a,b$ chosen as positive real numbers satisfying $a^2+b^2=1$, $\phi$ is the relative phase between the two components. Phase is an angle corresponding to a position within a wave cycle and carries information distinct from amplitude magnitude
- How it is understood in this repository: In descriptions of decoherence and T₂, phase means the relative phase of a quantum state. It is distinguished from the canonical NRA-IDE term "transition phase"
- Common confusions (dated): Multiplying the entire state by the same "global phase" does not by itself change measurement probabilities. A relative-phase change may be invisible when only measuring 0/1; a measurement that reads out interference is then needed (2026-10-24)
- JP/EN reconciliation: Proposed pairs: Phase and 位相; relative phase and 相対位相. Do not substitute quantum phase into the definition of the canonical "transition phase" (2026-10-24; reconciliation pending)
- Sources: Relative-phase and interference explanations in [IBM Quantum Learning, "Superposition with Qiskit"](https://quantum.cloud.ibm.com/learning/en/modules/quantum-mechanics/superposition-with-qiskit) (text checked 2026-10-24)
- Related: [Superposition](#^qh-superposition), [Quantum interference](#^qh-quantum-interference), [Quantum coherence](#^qh-quantum-coherence), canonical [Transition phase](../NRA-IDE_Dictionary_EN.md#^transition-phase)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-pure-state"></a>
### Pure state
- Japanese version: [純粋状態](./Glossary_JP.md#^qh-pure-state) ^qh-pure-state
- Category: External technical term
- Official name and origin: Pure state. A standard quantum-information term distinguished from a mixed state.
- Meaning: A quantum state represented by one normalized state vector. In finite dimensions, the trace of its squared density matrix is 1. The state vector below has unit norm.

$$
\rho=\lvert\psi\rangle\langle\psi\rvert,\qquad \operatorname{Tr}(\rho^2)=1.
$$

- How it is understood in this repository: A term needed for the ideal one-qubit constructive example. Actual device states are not assumed always pure.
- Common confusions (dated): Measurement outcomes can be probabilistic even for a pure state. Pure does not mean that one measurement outcome is known with certainty. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Pure state and 純粋状態. Pure is not a description of an entirely noiseless device.
- Sources: [IBM Quantum: Density matrix basics](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/density-matrix-basics); [IBM Quantum: Convex combinations of density matrices](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/convex-combinations) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Density matrix](#^qh-density-matrix), [Mixed state](#^qh-mixed-state), [Superposition](#^qh-superposition)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-quantum-coherence"></a>
### Quantum coherence
- Japanese version: [量子コヒーレンス](./Glossary_JP.md#^qh-quantum-coherence) ^qh-quantum-coherence
- Category: External technical term
- Official name and origin: Quantum coherence. A standard term concerning superposition and interference in quantum states; coherence concerns the consistency of phase relationships
- Meaning: Relationships between components in a chosen basis that can manifest as interference. The off-diagonal entries of a density matrix in that basis represent coherence. These entries record relationships between the corresponding components
- How it is understood in this repository: A term needed to read the "coherence layer" in the April documents. The usability of a quantum state for interference differs from consistency of classical versions, timestamps, and records
- Common confusions (dated): Coherence is basis-dependent. It is not synonymous with the everyday meaning of logical consistency, or with entanglement between qubits (2026-10-24)
- JP/EN reconciliation: Proposed pair: Quantum coherence and 量子コヒーレンス. The heading follows the source term because 整合性 alone could be confused with classical consistency (2026-10-24; reconciliation pending)
- Sources: [Zurek, "Decoherence, einselection, and the quantum origins of the classical"](https://arxiv.org/abs/quant-ph/0105127), and [IBM Quantum Learning, "Density matrix basics"](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/density-matrix-basics) (abstract and text, respectively, checked 2026-10-24). [April final version](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md) §6
- Related: [Decoherence](#^qh-decoherence), [Quantum interference](#^qh-quantum-interference), [Density matrix](#^qh-density-matrix), [Coherence time (T₂)](#^qh-coherence-time-t2)
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
- Related: [Union-Find decoder](#^qh-union-find-decoder), [4 K stage](#^qh-cryo-cmos-4k-stage), [Syndrome](#^qh-syndrome), [Decoding](#^qh-decoding)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-quantum-interference"></a>
### Quantum interference
- Japanese version: [量子干渉](./Glossary_JP.md#^qh-quantum-interference) ^qh-quantum-interference
- Category: External technical term
- Official name and origin: Quantum interference. The standard term for interference between probability amplitudes in quantum mechanics
- Meaning: Probability amplitudes for indistinguishable paths leading to the same measurement outcome add, increasing or decreasing its probability according to their relative phases. Adding probabilities directly differs from adding amplitudes and then taking their squared magnitude
- How it is understood in this repository: Few-shot measurement samples the distribution produced by a circuit a small number of times. Reducing the shot count does not mean preserving or restoring interference
- Common confusions (dated): Distinguish useful quantum interference from unwanted electromagnetic interference involving control lines or other components. Both may be called "interference" in English (2026-10-24)
- JP/EN reconciliation: Proposed pair: Quantum interference and 量子干渉. When writing "interference" alone, specify its subject (2026-10-24; reconciliation pending)
- Sources: [IBM Quantum Learning, "Superposition with Qiskit"](https://quantum.cloud.ibm.com/learning/en/modules/quantum-mechanics/superposition-with-qiskit) (text checked 2026-10-24)
- Related: [Superposition](#^qh-superposition), [Phase and relative phase](#^qh-quantum-phase), [Quantum coherence](#^qh-quantum-coherence), [Shot](#^qh-shot)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-qubit"></a>
### Qubit
- Japanese version: [量子ビット](./Glossary_JP.md#^qh-qubit) ^qh-qubit
- Category: External technical term
- Official name and origin: Quantum bit, shortened to qubit. The standard term for a basic unit of quantum information
- Meaning: A unit of quantum information with two basis states, $\lvert0\rangle$ and $\lvert1\rangle$. A pure state is written $a\lvert0\rangle+b\lvert1\rangle$, where $a,b$ are complex numbers and $\lvert a\rvert^2+\lvert b\rvert^2=1$. Measurement in this basis gives one result, either 0 or 1
- How it is understood in this repository: "One qubit, one parameter" in the October paper specifies the size of the constructive example and preliminary classical calculation. Its results are not evidence of performance with many qubits
- Common confusions (dated): Measuring a qubit once does not reveal every component of its superposition. The number of physical qubits also differs from the number of logical qubits constructed using error correction (2026-10-24)
- JP/EN reconciliation: Proposed pair: Qubit and 量子ビット. Qubit abbreviates quantum bit and is distinguished from an ordinary bit (2026-10-24; reconciliation pending)
- Sources: [IBM Quantum Learning, "Quantum information"](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/quantum-information) (text checked 2026-10-24). [October paper v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) §6.3 and §6.5
- Related: [Superposition](#^qh-superposition), [Density matrix](#^qh-density-matrix), [Quantum error correction (QEC)](#^qh-qec)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-secular-approximation"></a>
### Secular approximation
- Japanese version: [永年近似](./Glossary_JP.md#^qh-secular-approximation) ^qh-secular-approximation
- Category: External technical term
- Official name and origin: Secular approximation. A time-averaging approximation used in master-equation derivations.
- Meaning: A procedure removing rapidly oscillating terms associated with different transition frequencies, for example in the interaction picture. Frequency separations and time scales must justify separating retained and discarded terms.
- How it is understood in this repository: Part of a representative derivation of Lindblad form. Record the pre-approximation model and the couplings removed.
- Common confusions (dated): Near-degenerate or degenerate transitions cannot be discarded indiscriminately. Do not unconditionally identify this with a rotating-wave approximation made at the Hamiltonian level. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Secular approximation and 永年近似. It does not permit averaging away arbitrary terms merely by considering long times.
- Sources: [QuTiP: Lindblad Master Equation Solver](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html); [GKSL detailed explanation](./details/Lindblad_GKSL_EN.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Born approximation](#^qh-born-approximation), [Markov approximation](#^qh-markov-approximation), [Hamiltonian](#^qh-hamiltonian), [Lindblad (GKSL) equation](#^qh-lindblad-equation)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-dynamical-semigroup"></a>
### Semigroup (quantum dynamical semigroup)
- Japanese version: [半群（量子力学的半群）](./Glossary_JP.md#^qh-dynamical-semigroup) ^qh-dynamical-semigroup
- Category: External technical term
- Official name and origin: Semigroup is a mathematical term for an associative operation. This entry focuses on quantum dynamical semigroups as families of evolution maps.
- Meaning: A family using the same map for the same elapsed time, where evolution for time t followed by time s equals evolution for the total elapsed time. The time-zero map below is the identity.

$$
\Phi_{t+s}=\Phi_s\circ\Phi_t,\qquad \Phi_0=\mathrm{id},\qquad t,s\geq0.
$$

- How it is understood in this repository: An assumption in the general-form statement for a time-homogeneous GKSL generator. In finite dimensions, generators of continuous CPTP semigroups have GKSL form.
- Common confusions (dated): Semigroup alone does not imply the CPTP property or continuity. A time-dependent GKSL equation can be CPTP without giving a time-homogeneous semigroup. (2026-10-24)
- JP/EN reconciliation: Proposed pairs: Semigroup and 半群; quantum dynamical semigroup and 量子力学的半群. Both names lead to this entry.
- Sources: [Lindblad (1976): publisher bibliography and abstract](https://link.springer.com/article/10.1007/BF01608499); [GKSL detailed explanation](./details/Lindblad_GKSL_EN.md) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Completely positive trace-preserving map (CPTP)](#^qh-cptp-map), [Markov approximation](#^qh-markov-approximation), [Lindblad (GKSL) equation](#^qh-lindblad-equation)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-shot-noise"></a>
### Shot noise
- Japanese version: [ショットノイズ](./Glossary_JP.md#^qh-shot-noise) ^qh-shot-noise
- Category: External technical term
- Official name and origin: Shot noise. Here it means sampling fluctuations from finite-shot quantum-circuit measurements. The term is also used in electronic and optical detection, so specify the subject
- Meaning: Fluctuation of measured means or frequencies around their expectation values or true probabilities because identically prepared quantum states are measured only a finite number of times. For M independent, identically distributed 0/1 measurements with probability p of result 1, the standard error of the frequency is $\sqrt{p(1-p)/M}$
- How it is understood in this repository: Relevant to measurement noise in few-shot SPSA. Record the shot count per evaluation point, perturbation width, and estimator variance separately
- Common confusions (dated): Under the same independent, identically distributed conditions, quadrupling M halves the standard error. This scaling does not imply the same reduction of device drift, readout bias, or gate error (2026-10-24)
- JP/EN reconciliation: Proposed pair: Shot noise and ショットノイズ. The meaning field restricts the subject to sampling noise in quantum measurements (2026-10-24; reconciliation pending)
- Sources: Standard-error explanation in [IBM Quantum Documentation, "Estimator inputs and outputs"](https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output) (text checked 2026-10-24). [October paper v6.1](../../note/03_実装・計算機アーキテクチャ/nra-ide-hybridcalc-quantum-architecture-next_ver/2026-10_SPSA更新権限/NRA-IDE_QuantumHybrid_LogicalHypothesis_v6.1_2026-10-22.md) §2.2
- Related: [Shot](#^qh-shot), [Expectation value](#^qh-expectation-value), [SPSA](#^qh-spsa), [Gate error](#^qh-gate-error)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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
- Related: [Barren plateau](#^qh-barren-plateau), [Shot](#^qh-shot), [Few-shot SPSA nominal calculation](#^qh-few-shot-spsa-nominal-calculation), [Estimator bias](#^qh-estimator-bias), [Variance](#^qh-variance), [Standard error](#^qh-standard-error)
- Status: [Draft] [concepts reconciled] [full text not yet checked]

<a id="qh-standard-error"></a>
### Standard error
- Japanese version: [標準誤差](./Glossary_JP.md#^qh-standard-error) ^qh-standard-error
- Category: External technical term
- Official name and origin: Standard error (SE). A standard statistical-estimation term.
- Meaning: The standard deviation of an estimator's sampling distribution. For the mean of M independent identically distributed measurements with finite variance and population standard deviation sigma, the expression below applies. In practice it is estimated using sample standard deviation s.

$$
\operatorname{SE}(\bar{X})=\frac{\sigma}{\sqrt{M}},\qquad \widehat{\operatorname{SE}}(\bar{X})=\frac{s}{\sqrt{M}},\quad M\geq2.
$$

- How it is understood in this repository: Used to relate shot count to uncertainty in a sample mean. Other estimators require their own standard-error calculations.
- Common confusions (dated): Different from the standard deviation of individual observations or total error including systematic effects. Do not apply the independent-sample formula unconditionally to correlated measurements. Confidence intervals require additional distributional assumptions. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Standard error and 標準誤差.
- Sources: [NIST: Confidence Limits for the Mean](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm); [IBM Quantum: Estimator inputs and outputs](https://quantum.cloud.ibm.com/docs/en/guides/estimator-input-output) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Variance](#^qh-variance), [Estimator bias](#^qh-estimator-bias), [Shot](#^qh-shot), [Shot noise](#^qh-shot-noise)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-superposition"></a>
### Superposition
- Japanese version: [重ね合わせ](./Glossary_JP.md#^qh-superposition) ^qh-superposition
- Category: External technical term
- Official name and origin: Superposition. The standard term used when a quantum state is expressed as a sum of chosen basis states weighted by probability amplitudes
- Meaning: A state containing components of two basis states, for example $a\lvert0\rangle+b\lvert1\rangle$. Its coefficients are probability amplitudes, not probabilities; their squared magnitudes give the probabilities of the measurement results. How superposition is expressed depends on the chosen basis
- How it is understood in this repository: The classical side receives individual shot results and their aggregation. Being able to write a state mathematically differs from knowing every coefficient of an unknown state in a device
- Common confusions (dated): Superposition differs from a probabilistic mixture in which the system is already either 0 or 1 and only that choice is unknown. States with the same 0/1 measurement probabilities can have different statistics in another measurement because of their relative phase (2026-10-24)
- JP/EN reconciliation: Proposed pair: Superposition and 重ね合わせ. Avoid explaining it as being able to read all results simultaneously (2026-10-24; reconciliation pending)
- Sources: [IBM Quantum Learning, "Superposition with Qiskit"](https://quantum.cloud.ibm.com/learning/en/modules/quantum-mechanics/superposition-with-qiskit) (text checked 2026-10-24)
- Related: [Qubit](#^qh-qubit), [Phase and relative phase](#^qh-quantum-phase), [Quantum interference](#^qh-quantum-interference), [Density matrix](#^qh-density-matrix)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

<a id="qh-syndrome"></a>
### Syndrome
- Japanese version: [シンドローム](./Glossary_JP.md#^qh-syndrome) ^qh-syndrome
- Category: External technical term
- Official name and origin: Error syndrome. A standard term in quantum error correction.
- Meaning: A collection of check outcomes providing information about errors. Stabilizer codes measure commuting check operators to investigate errors without directly reading out the logical state.
- How it is understood in this repository: Needed to understand information supplied to a Union-Find decoder. With repeated measurements, distinguish raw check outcomes from detection events constructed from changes over time.
- Common confusions (dated): A syndrome need not uniquely identify a physical error and is not a measurement outcome of the logical state. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Syndrome and シンドローム.
- Sources: [IBM Quantum: Error correction II](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/error-correction-ii) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Quantum error correction (QEC)](#^qh-qec), [Decoding](#^qh-decoding), [Union-Find decoder](#^qh-union-find-decoder)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-variance"></a>
### Variance
- Japanese version: [分散](./Glossary_JP.md#^qh-variance) ^qh-variance
- Category: External technical term
- Official name and origin: Variance. A standard probability and statistics term.
- Meaning: The expected squared deviation of a random variable from its mean, assuming a finite second moment. If values have units of volts, variance has units of volts squared.

$$
\operatorname{Var}(X)=\mathbb{E}\!\left[(X-\mathbb{E}[X])^2\right].
$$

- How it is understood in this repository: Used to describe variation in finite-shot estimators and SPSA gradient estimators. Specify which random variable the variance concerns.
- Common confusions (dated): Standard deviation is the square root of variance. Sample variance estimates population variance; its usual unbiased form divides by sample size minus one. Variance alone does not measure bias from the true value. (2026-10-24)
- JP/EN reconciliation: Proposed pair: Variance and 分散.
- Sources: [NIST: Measures of Scale](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm) (external explanations/definitions consulted 2026-10-24; not a full-paper translation check)
- Related: [Estimator bias](#^qh-estimator-bias), [Standard error](#^qh-standard-error), [Shot noise](#^qh-shot-noise)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]

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

<a id="qh-version-check"></a>
### Version management (parameter version, boundary version, measurement time)
- Japanese version: [版管理（パラメータ版・境界版・測定時刻）](./Glossary_JP.md#^qh-version-check) ^qh-version-check
- Category: term created at the connection (October) [extension proposal]
- Official name and origin: A term used in §4.2 "Version management of measurement results" of the October paper v6.1. Each measurement pair is tagged with the parameter version used, the boundary-judgment version (boundary version), the two measurement times, the reception time, and the state of the observation channel
- Meaning: A record for confirming, in an asynchronous update, that the conditions at the time of measurement match the conditions at the time of application. The parameter version is the version of the parameters to be updated; the boundary version is the version of the boundary judgment (thresholds and state classification)
- How it is understood in this repository: If the parameter version or the boundary version has changed after the measurement, the update is recomputed or skipped. Judgment and application are coupled as an indivisible operation, and no state change is allowed between them (conditions 5 and 6 of v6.1 §4.2)
- Common confusions (dated): The version terms in the paper series are the parameter version and the boundary version (boundary-judgment version). The terms "observation version" and "configuration version" are not yet defined in the paper series (2026-10-23). Also distinct from the version numbers of papers and documents (3.0 to 6.1 in the change log)
- JP/EN reconciliation: Version management. "Version" means a "版" and is not written as a version number (not yet confirmed)
- Sources: Paper series v6.1 §4.2 and §4.3
- Related: [Update permission](#^qh-update-authority), [Pairwise skip of an update](#^qh-pair-skip), [Atomicity](#^qh-atomicity), [Data age (measurement age)](#^qh-data-age), [Drift](#^qh-drift), [Calibration](#^qh-calibration)
- Status: [Draft] [concepts unreconciled] [full text not yet checked]
