# NRA-IDE 一次式の導出 / Derivation of the Primary Formula

**Version:** 1.1（日英対訳版 / Bilingual Edition — English / Japanese）
**Author:** M-Tokuni
**Document role:** 正典が定める一次式 $R=\delta/\tau$ について、その前段（Cause-Side観測から $\delta$ と $\tau$ を構成するまで）の導出・証明・例示を示す / Derivation, proof, and illustration of the pre-stage of the canonical Primary Formula $R=\delta/\tau$ (from Cause-Side observations to $\delta$ and $\tau$ )

> **Note:** This document presents the English version (Section I) followed by the Japanese original (Section II). The Japanese version is the primary source text; the English version is a faithful translation.
>
> 本書は、前半に英語版（Section I）、後半に日本語原文（Section II）を収めた対訳版です。日本語版が一次原文であり、英語版はその忠実な翻訳です。

---

# SECTION I — ENGLISH

## 0. Role of This Document and How to Read It

This document neither creates nor changes canonical definitions. Definitions, classifications, and precedence follow `theory/AXIOMS.md` (§16). If this document conflicts with the canon (`theory/AXIOMS.md`, `theory/axioms.json`, `FORMULA.md`, and others), the canon prevails and this document is corrected.

Among the symbols used in this document, those defined in the canon follow the canonical definitions. Symbols for which the "Defined in" column of the symbol table (Part 2, 1) names a canonical section follow the definition in that section.

All numerical values in the examples are illustrative and are not values of real members or equipment. References to external theories point to similar observations and are not grounds for the derivation. Each proof is closed within the premises of this document. The record of the deliberations is kept in `note/正典考慮課題/`.

This document consists of three parts.

- **Part 1 (for a high-school senior):** explains the whole picture with a spring, using almost no symbols. It is enough to grasp "what this is about," even without following every detail.
- **Part 2 (establishing the Primary Formula):** writes the path up to the Primary Formula (Stages 1–4) with variables, formulas, and proofs, and shows which symbol each phrase of Part 1 corresponds to.
- **Part 3 (after the Primary Formula):** writes the transitions after the Primary Formula (Stages 5–7). Part 3 precedes any decision on canonization and is not a canonical definition.

The sections of Part 1 are numbered [1]–[11], and Parts 2 and 3 show the correspondence as "→[3]". [1]–[6] and [8] correspond to Part 2; [11] to Part 3; [7] to both Part 2 (the latch in P6) and Part 3 (Stage 5); [10] to both Part 2 (P6 and the addition of a structural element in 3.3) and Part 3 (Stage 6); and [9] to both Part 2 (P9) and Part 3 (Stage 7).

---

# Part 1　Explanation for a High-School Senior

## [1] First, agree on "what to look at"

Consider an experiment of pulling a spring.

Before starting any calculation, decide the following in advance.

- Which spring to look at (the target)
- What counts as "broken" (rupture)
- How to measure the extension (the unit is mm)
- Where "zero extension" is (the reference = the natural length when the spring was bought; **this mark is never moved later**)

If you calculate without deciding these, the same number can mean different things to different people.
The NRA-IDE Primary Formula is not "a formula that divides any two numbers you like." It is **a formula that can be used only after this agreement has been made**.

## [2] Look at "how far it has come" as a ratio

Suppose this spring breaks when stretched **30 mm** beyond its natural length.
This width that can be received before breaking, 30 mm, is called the **thickness (τ)**.

If it is now stretched 12 mm, then of the way to breaking,

$$
\frac{12}{30}=0.4
$$

that is, it has come **40%** of the way.
This "extension from the reference to the present position" is called the **deviation (δ)**, and the ratio 0.4 is called **R**. When R reaches 1, the spring ruptures.

- R = 0.4 → 40% of the way
- The remaining width 30 − 12 = 18 mm → this is the "margin"

The thickness is not "what remains" but "the whole width from the reference to rupture." What remains is called the "margin" separately.

## [3] Deviation that returns and deviation that does not

As learned in physics, a spring has an **elastic limit**. Let the elastic limit of this spring be 12 mm.

- **Pull 8 mm and let go** → it returns to its original length. This is **reversible** (deviation that returns).
- **Pull 15 mm and let go** → since it went 3 mm beyond the elastic limit, it **stays 3 mm stretched** after release. This is **irreversible** (deviation that does not return). Gaps appear between the coils.

While the spring is being pulled to 15 mm, the extension can be divided into "12 mm that returns on release" and "3 mm that no longer returns." A single event contains a returning part and a non-returning part **at the same time**.

## [4] There are two kinds of things that do not return

A spring that has gone beyond its elastic limit undergoes two kinds of changes that do not return.

1. **Stays stretched:** the natural length has become 3 mm longer (the position remains shifted).
2. **Has become weaker:** invisible damage has formed inside the metal, and the width before breaking has decreased from 30 mm to **27 mm**.

1 is "deviation remained," and 2 is "the vessel itself became smaller." **They are different phenomena, so they are counted separately.**
Counting the same change in both would make it look worse than it is (double counting). Which observation is counted where is decided within the agreement of [1].

## [5] The scale contains the past just by measuring. That is why it must not be reset

If the spring that was pulled to 15 mm and released is measured **with the scale of the original natural length unchanged**, the extension reads 3 mm.
Without any calculation, **the present reading of the scale itself contains the 3 mm that stayed stretched in the past**.
"Deviation is not an instantaneous value; it carries history" does not mean some special accumulation. It means that **if you measure without moving the scale, the past remains visible in the present value**.

If, however, the present length is reset as the new "zero extension,"

- extension 0, R = 0 → **it looks "completely restored"**

but in reality,

- residual extension 3 mm, thickness 27 mm → R = 3 ÷ 27 ≈ 0.11.

Resetting the scale makes past events invisible.
That is why **the reference (the zero-extension position) stays where it was first decided**. Part 2 shows that not moving it is always on the safe side (R comes out larger).

## [6] The same appearance does not mean the same spring

Pull a new spring and a spring that was once pulled to 15 mm, both to the same position, 15 mm.

| | Extension | Thickness | R |
|---|---|---|---|
| New | 15 mm | 30 mm | 0.50 |
| Once-pulled spring | 15 mm | 27 mm | about 0.56 |

The visible extension is the same 15 mm, yet R differs. What makes the difference is **what happened in the past (the history)**.

From here comes the most important sentence of this theory.

> **Even if the value returns, the structure has not returned.**

On release, part of the extension returns (the value returns). But the 3 mm that stayed stretched, the reduced thickness, and the record of the event "pulled to 15 mm" do not disappear (the structure has not been restored).

## [7] There is a line that, once crossed, does not return automatically (→Part 2 P6, Part 3 Stage 5)

Once R crosses a set value (the irreversible transition onset) even once, the record "entered irreversibility" is not erased even if R later falls.
This is called a **latch**. Once it catches, it does not release automatically.

## [8] Being "pushed in" and "the vessel being shaved" at the same time is the most dangerous

Suppose a spring pulled to 8 mm is stretched further to 15 mm. Two things happen at the same time.

- The extension increased from 8 mm to 15 mm (pushed in)
- Having gone beyond the elastic limit, the thickness decreased from 30 mm to 27 mm (the vessel shaved)

R rises from 8/30 ≈ 0.27 to 15/27 ≈ 0.56. Of the rise of 0.29,

- about 0.26 is due to "the extension increased"
- about 0.03 is due to "the vessel became smaller"

R rises both when the numerator increases and when the denominator decreases, so **an event in which both occur at once pushes R up from two directions**.
The NRA-IDE "dual fluctuation" is a formula that watches for exactly this moment, when "deviation increases and thickness decreases at the same time."

## [9] A broken part does not mean the whole is broken (→Part 2 P9, Part 3 Stage 7)

Consider a platform supported by ten springs. One of them breaks.

- For that one spring, it is rupture (R = 1)
- For the whole platform, it is not yet rupture

But the load on the remaining nine increases, and the thickness of the whole platform decreases.
That is, **the rupture of a lower level enters the upper level as "one event."** The rupture of a part must neither be equated with the rupture of the whole nor ignored.

The same holds when the state of a neighboring spring affects this spring. The neighbor's state arrives here as an "event."

One distinction must be made here. **The spring itself** and the **ruler** that measures it (where zero extension is, from where it is considered dangerous) are different things.

- It is natural, as the physics of the spring, that the spring itself is damaged faster the harder it is pulled.
- But **you must not rewrite the ruler that measures you by looking at your own R**. Moving the danger line away when R is high hides the approach; moving it closer exaggerates the approach. In either case, R comes to reflect the convenience of the ruler rather than the state of the spring.

This is what "no reverse derivation" means. In the canon, this prohibition is called reverse derivation B (self-adjustment of the gauge).

## [10] A stretched spring does not return. To strengthen it, add. When it breaks, count anew (→Part 2 3.3, Part 3 Stage 6)

A spring that stayed stretched does not return to its original state. To make it stronger, do not "restore" the damaged spring; **add something new**.

- Example: place another spring beside it, or attach a thicker spring.
- An added spring has its own thickness. That thickness is determined by measuring at the time of addition.
- The old spring's 3 mm of permanent stretch and its weakening from 30 mm to 27 mm remain after the addition; they do not disappear.
- The whole thickness is the width that combines the old spring and the added spring. How they are combined (adding them if placed side by side, and so on) is decided in advance within the agreement of [1].
- The calculation continues after the addition, and the addition stays in the record. It may happen at any time (even right after the calculation starts).
- Conversely, an undamaged spring may be taken out. This is recorded as "removed," not "broken." When a removed spring is put back, it is treated again as "added" and measured anew at that time.

Instead of continuing the same calculation, count anew in the following cases.

- When the spring breaks (R = 1).
- When the agreement itself is changed. For example, when the stretched spring is forcibly pulled back to its original length (straightened), or when a new measurement shows that the thickness differs from the agreed value.

When counting anew,

- keep all records of the old spring in storage (do not discard them, do not rewrite them). The record "crossed the no-return line once" ([7]) is also written into the new agreement.
- Make a **new agreement** ([1]) and start counting. The R of the previous calculation and the R of the new calculation are not compared.

The "escapement" wheel in a clock is a mechanism that repeats this regularly. When one tooth's worth accumulates, it advances one step; the overshoot is not carried to the next tooth, and counting starts anew with the next tooth (in a mechanical escapement, the overshooting energy dissipates as heat). The wheel only advances and never returns to the same state at the same position.

## [11] Keep all records; a summary is enough for judgment (→Part 3)

Recording everything, "when and how many mm it was pulled," becomes very long.
But to judge what happens next, it is enough to know three things:

- the amount of permanent stretch (3 mm)
- how much weaker it has become (30 → 27 mm)
- whether the latch has caught

(for a single element; the general case is proved, with conditions, in Proposition 5 of Part 3).

However, **all records are kept for explanation and audit**. "The summary needed for judgment" and "the record needed for testimony" have different roles. The formula is shortened not by cancellation but **by summary**. Only what does not change the next judgment when erased may be erased.

---

# Part 2　Establishing the Primary Formula

## 1. Symbol Table

The names, fixed names, types, provenance, permitted uses, and points of confusion of the symbols can be looked up in the dictionary `dictionary/NRA-IDE_Dictionary_EN.md` (Japanese edition `dictionary/NRA-IDE_Dictionary_JP.md`; non-normative). This document does not distinguish symbols with different meanings only by font, case, or typeface (dictionary 0.5, FORMULA.md §7). The reserved symbols of the canon (FORMULA.md §7: $R,S,M_R,M_\tau,\delta,\tau,\omega,C,\mathrm{entropy}$ ), the symbols of AXIOMS.md §1 ( $\epsilon$ , $\emptyset$ , and others), and the auxiliary structural quantities of AXIOMS.md §4.5 ( $\omega$ , $\mathrm{Phase}$ , $C$ , $W$ , $\mathrm{entropy}$ ) are used only in their canonical meanings.

| Symbol | Name | Meaning | Defined in | Part 1 |
|---|---|---|---|---|
| $\mathsf{Decl}$ | evaluation declaration | the set of commitments fixed before computation begins | FORMULA.md §0.5.1 | [1] |
| $n$ | structural update number | the order of events (not time) | FORMULA.md §0.5.2 | — |
| $o_n$ | observation value | a Cause-Side observation (may be multivariate); a symbol distinct from the computational state $x$ of FORMULA.md §5 | FORMULA.md §0.5.2 | — |
| $\mathrm{Ev}_n$ | observation event | the event recorded $n$th | FORMULA.md §0.5.2 | — |
| $\sigma$ | projection rule | conversion from observation to accumulated deviation | FORMULA.md §0.5.2 | [5] |
| $\mathsf{Alloc}$ | allocation rule | the rule that decides where an observed change is allocated | FORMULA.md §0.5.3 | [4] |
| $a_n$ | applied action | the action applied to the structure at that step | FORMULA.md §0.5.3 | pulling force |
| $C_n$ | constraint | the value at that step of an external load, restraint, or environmental condition (a component of the observation $o_n$ ); not an allocation target | AXIOMS.md §4.5, FORMULA.md §0.5.3 | — |
| $q_n$ | reversible component | deviation that returns to 0 when the action is removed | AXIOMS.md §4 (term), FORMULA.md §0.5.3 (symbol) | [3] |
| $p_n$ | irreversible component (residual deviation) | deviation that remains after the action is removed | AXIOMS.md §4 (term), FORMULA.md §0.5.3 (symbol) | [4] 1 |
| $\lambda_n$ | degradation fraction (single element) | the fraction of thickness lost, $0\le\lambda_n\le1$ ; with several elements, the per-element $\lambda^{[e]}_n$ is used | FORMULA.md §0.5.4 | [4] 2 |
| $\tau_0$ | declared thickness | the absorption thickness of the whole structure at the start of evaluation; with several elements, $\tau_0=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_0)_{e\in\mathsf{Active}_0}\bigr)$ | FORMULA.md §0.5.1, §0.5.4; consistent with $\tau_0$ in AXIOMS.md §7, §8 | 30 mm |
| $e$ | element number | the number of a structural element; $e=0$ is the structure at declaration and $e\ge1$ are added elements | FORMULA.md §0.5.4 | [10] |
| $n_e$ | time of addition | the update number at which element $e$ was added ( $n_0=0$ ) | this document | [10] |
| $\mathsf{Active}_n$ | active elements | the set of elements included in the evaluation target at step $n$ (added and not yet removed) | FORMULA.md §0.5.4 | [10] |
| $q^{\mathrm{temp}}_n$ | temporary reversible deviation | a receiving width temporarily narrowed by an action or condition, counted on the deviation side; part of the reversible component $q_n$ | FORMULA.md §0.5.3 | — |
| $\tau^{[e]}_0$ , $\lambda^{[e]}_n$ | declared thickness and degradation fraction of an element | the declared thickness and degradation fraction of element $e$ itself (for a single element, $\tau^{[0]}_0=\tau_0$ and $\lambda^{[0]}_n=\lambda_n$ ) | FORMULA.md §0.5.4 | [10] |
| $\mathrm{Comp}_\tau$ | composition rule | the rule that determines the effective thickness of the whole from element thicknesses | FORMULA.md §0.5.4 (symbolizes "addition of a structural element" in AXIOMS.md §7) | [10] |
| $\delta_n$ | accumulated deviation | $q_n+p_n$ | AXIOMS.md §4, FORMULA.md §1, §0.5.3 | [2] [5] |
| $\tau_n$ | effective thickness | $(1-\lambda_n)\tau_0$ for a single element; in general, given by $\mathrm{Comp}_\tau$ of Stage 3 | FORMULA.md §1 ( $\tau$ ), §0.5.4 (distinction of layers) | [2] [4] |
| $\tau_{\mathrm{upper}}(n)$ , $\tau_{\mathrm{lower}}(n)$ | side-specific effective gate widths | widths used only for side-specific evaluation in the Secondary Formula | FORMULA.md §4.4 | — |
| $R_n$ | boundary approach ratio | $\delta_n/\tau_n$ | FORMULA.md §1 | [2] |
| $M_{\tau,n}$ | remaining absorption margin | $\tau_n-\delta_n$ | FORMULA.md §2 | [2] |
| $\ell_n$ | irreversible latch | 0 or 1 | AXIOMS.md §10.4 (`irreversible_latched`) | [7] |
| $\mathsf{History}_n$ | event history | the record sequence $\mathrm{Ev}_1,\dots,\mathrm{Ev}_n$ (empty at the start of evaluation) | this document | [6] [11] |
| $\mathsf{Phys}^{(\mathrm{self})}_n$ | target state | the physical state of this structure $(q_n,p_n,(\lambda^{[e]}_n)_{e\in\mathsf{Active}_n})$ ; it does not include the evaluation state ( $\ell_n$ ) or the event history ( $\mathsf{History}_n$ ) (Proposition 2). The physical state of another structure $i$ is $\mathsf{Phys}^{(i)}_n$ | this document (symbolizes the categories of AXIOMS.md §14) | [9] |
| $\mathsf{Gauge}^{(\mathrm{self})}$ | gauge | the reference, transformation rules, thresholds, and effective gate widths that measure this structure | this document (same as above) | [9] |
| $\mathsf{Out}^{(\mathrm{self})}_n$ | evaluation output | $R_n$ , side-specific ratios, $\ell_n$ , the canonical state, and their aggregates | AXIOMS.md §14 (that section lists $R$ , the canonical state, and the irreversible latch; including side-specific ratios is this document's reading) | [9] |

Symbols used only in Part 3 ( $j$ , $\mathsf{Archive}$ , $Z_n$ , $\mathsf{State}_n$ , $\mathsf{Update}$ , $\rho$ , $g_p$ , $g^{[e]}_\lambda$ , $\mathrm{EvalGraph}^{(j)}$ ) are given in Part 3.

---

## 2. Premises P0–P9

For each premise, the correspondence with the canon is shown.

### P0　Evaluation declaration (→[1])

Before computation begins ( $n=0$ ), the evaluation declaration $\mathsf{Decl}$ is fixed. $\mathsf{Decl}$ is not rewritten by the results of the evaluation.

| Required element | Content | Correspondence with the canon |
|---|---|---|
| Target and rupture mode | the structure evaluated and the mode and path regarded as complete rupture | FORMULA.md §0 |
| Unit | the unit $u$ shared by $\delta$ and $\tau$ | FORMULA.md §1 |
| Observations and provenance | the Cause-Side observations used, with their provenance, time, unit, and uncertainty | FORMULA.md §6, AXIOMS.md §14, §15.1 |
| Thresholds | $R_{\mathrm{warn}}$ , $R_{\mathrm{handoff}}$ , $R_{\mathrm{irrev}}$ | AXIOMS.md §9 |
| Handling of missing or unobservable data | the treatment when data are unobservable, missing, or not computable. An unobservable channel is reported as `NOT_OBSERVABLE` with the reason and is not filled in as zero, stable, safe, or recovered | AXIOMS.md §10.2, §11.2, §15.1 |
| Reference state | the origin from which accumulated deviation is measured | AXIOMS.md §4 |
| Projection rule $\sigma$ | Stage 1 | this document |
| Allocation rule $\mathsf{Alloc}$ | P5 | this document |
| Declared thickness $\tau_0$ | Stage 3 | this document |
| Composition rule $\mathrm{Comp}_\tau$ | the rule that determines the effective thickness of the whole from element thicknesses when structural elements are added or removed (Stage 3) | AXIOMS.md §7 (addition of a structural element) |

The composition rule is declared even in an evaluation where no addition has yet occurred. Because an addition may occur at any time (even right after $n=0$ ), deciding the rule only after an addition occurs would leave room to fit the rule to the result.

As an optional element, whether and how the sequence of evaluations is mapped to structural continuity $\omega$ may be declared. If it is not declared, there is no mapping. No general rule for the mapping is defined. The $\omega$ used for the mapping is obtained from Cause-Side observation or a pre-fixed transformation rule, as stated in AXIOMS.md §4.5 (P8).

As an optional element, the identification of external conditions (what counts as constraint $C$ : kind, source, unit, and conversion rule) may be declared. If $C$ enters the gauge, it is declared as a function fixed before evaluation.

Elements are not omitted. In a domain where a component does not exist, that component is declared to be zero (for example, $p\equiv0$ ).

**The Primary Formula is always bound to a declaration.**

$$
R_{\mathsf{Decl}}=\frac{\delta_{\mathsf{Decl}}}{\tau_{\mathsf{Decl}}}
$$

$R$ values from different declarations are not compared or transferred unless comparability is established.

$$
\mathsf{Decl}_A\neq\mathsf{Decl}_B
\;\Rightarrow\;
R_{\mathsf{Decl}_A}\text{ and }R_{\mathsf{Decl}_B}\text{ are not compared without establishing comparability}
$$

A **necessary condition** for comparability is that $\delta$ and $\tau$ are obtained for the same target, in the same unit, under the same Cause-Side measurement rules (the same condition that AXIOMS.md §8 requires for comparing $\tau_{\mathrm{restored}}$ with $\tau_0$ ). "The same measurement rules" here include that all elements of the declaration that change the meaning of $R$ are the same: the reference state, the rupture mode and rupture path, the projection rule $\sigma$ , the allocation rule $\mathsf{Alloc}$ , the composition rule $\mathrm{Comp}_\tau$ , and the meaning of the evaluation snapshot. These conditions are not sufficient conditions that guarantee a comparison is permissible. When comparing, show that the conditions are met; if any element does not meet them, do not compare. This reads FORMULA.md §0 ("the evaluation target is declared unambiguously before computation begins") and AXIOMS.md §15.1 ("do not transfer $\delta$ and $\tau$ to another domain on the basis of similarity alone") at the level of a declaration, and is not a new rule.

### P1　Deviation and the rupture boundary (→[2])

Along the declared rupture mode, the deviation measured from the reference state in the rupture direction is $\delta\ge0$ . $\delta=0$ is the reference state, and $\delta=\tau_n$ is the rupture position at the present step.

$\tau$ is not "what remains" but **the whole width from the reference to rupture**. What remains is defined separately as $M_\tau=\tau-\delta$ (FORMULA.md §2).

### P2　Observation events (→[1])

An observation event is not a single number but a unit of record.

$$
\mathrm{Ev}_n=
(\text{target},\ \text{value},\ \text{unit},\ \text{provenance},\ \text{time},\ \text{uncertainty},\ \text{order}\ n,\ \text{observation path})
$$

The time is the acquisition time or version and is kept separately from the order $n$ (FORMULA.md §6).

The following two are distinguished.

- **Unknown or invalid input:** an event whose target, unit, time, or provenance is unknown, or whose value is invalid or non-finite, is not input to the Primary Formula and results in CONFESSION (AXIOMS.md §6, §10.6). It is not filled in by analogy.
- **Merely unobservable:** when it is known that no value can be obtained from an observation channel, `NOT_OBSERVABLE` and the reason are output, and the declared handling of missing data applies (AXIOMS.md §10.2, §11.1, §11.2). Unobservability alone does not cause a transition to CONFESSION.

### P3　Commensurability

$$
[\delta]=[\tau]=u
$$

and $\delta_n$ and $\tau_n$ belong to the same $\mathsf{Decl}$ and the same $n$ .

### P4　Domain

$$
\delta_n\ge0,\qquad \tau_n>0,\qquad \delta_n,\tau_n\ \text{finite}
$$

This is exactly the domain of FORMULA.md §1. Lemma 1 shows that it is satisfied within the range $\lambda_n<1$ for a single element and, in general, within the range where the value of the composition rule is positive.

### P5　Reversible/irreversible decomposition (→[3] [4])

The allocation rule $\mathsf{Alloc}$ divides each event into the following four.

$$
\mathsf{Alloc}(\mathrm{Ev}_n)=\bigl(a_n,\ \Delta p_n,\ \Delta\lambda_n,\ \mathrm{ctx}_n\bigr)
$$

- $a_n$ : applied action (produces the reversible component). The effect of conditions that temporarily narrow the width the structure can receive ( $q^{\mathrm{temp}}_n$ , Stage 3) is also allocated here. The condition itself (constraint $C_n$ , AXIOMS.md §4.5) is not an allocation target
- $\Delta p_n\ge0$ : increment of residual deviation
- $\Delta\lambda_n\ge0$ : increment of the degradation fraction (with several structural elements, the per-element $\Delta\lambda^{[e]}_n\ge0$ )
- $\mathrm{ctx}_n$ : context, authority, and provenance

**Definition of increments:** the event $\mathrm{Ev}_n$ at update number $n$ advances the state from $n-1$ to $n$ ( $n=1,2,\dots$ ; $n=0$ is the start of evaluation). Increments are written with the same backward difference as FORMULA.md §4.7.

$$
p_n=p_{n-1}+\Delta p_n,\qquad \lambda^{[e]}_n=\lambda^{[e]}_{n-1}+\Delta\lambda^{[e]}_n
$$

Hence $p_n=p_0+\sum_{m=1}^{n}\Delta p_m$ ( $p_0$ is the residual deviation at the start of evaluation). The rule for the time evolution of the reversible component $q$ (the update rule $\mathsf{Update}$ of Stage 5 in Part 3) precedes any decision on canonization and is therefore not included in the premises of this part.

**Consistency with the projection:** the decomposition divides the value of the projection and satisfies

$$
q_n+p_n=\sigma(o_n)=\delta_n
$$

The reversible component is determined as $q_n=\sigma(o_n)-p_n$ , and $q_n\ge0$ gives $0\le p_n\le\delta_n$ . When $q_n$ is given by a model, this consistency must also hold. A violation is evidence that the declared $\sigma$ or $\mathsf{Alloc}$ does not fit the target. The temporary reversible deviation $q^{\mathrm{temp}}_n$ (a temporarily narrowed receiving width; Stage 3) is converted by $\sigma$ from the observation of the condition (temperature and so on) and included in $\delta_n$ , and $\mathsf{Alloc}$ allocates it to $q_n$ .

**One change, one allocation:** each observed physical change is allocated to **exactly one** of $a_n$ , $\Delta p_n$ , $\Delta\lambda_n$ . $\mathrm{ctx}_n$ is not an allocation target but information attached to the allocation. Which observation is allocated where is fixed in advance within $\mathsf{Alloc}$ (→ the prevention of double counting in [4]). A single event may contain several changes (the 15 mm example of [3]); even then, each change has exactly one allocation target. The constraint $C_n$ is not an allocation target. $C_n$ is a component of the observation $o_n$ and acts only as an argument of rules fixed before evaluation, such as $\sigma$ , $\mathsf{Alloc}$ , physical laws, and gauge functions. Its effect is allocated, change by change, to exactly one of $a_n$ , $\Delta p_n$ , $\Delta\lambda_n$ . The same factor (temperature and so on) may appear in both $C_n$ and $a_n$ ; since $C_n$ is not an allocation target, this is not double counting.

Addition or removal of a structural element itself is not allocated to these three destinations. It updates the composition $\mathsf{Active}_n$ and is recorded as an event (Stage 3). If separate action, residual deviation, or degradation accompanies an addition or removal, each such change follows the one-change-one-allocation rule.

### P6　Monotonicity of the irreversible components (→[4] [7] [10])

Within an evaluation, without exception,

$$
p_n\ge p_{n-1},\qquad \lambda^{[e]}_n\ge\lambda^{[e]}_{n-1}\quad(\text{each element}\ e)
$$

No operation decreases the degradation or residual deviation of existing elements. Absorption thickness increases only through the addition of a structural element (Stage 3). Removal of a structural element (Stage 3), the planned taking-out of an undamaged element, decreases the thickness but is not degradation and is not counted in $\lambda$ . Straightening, which forcibly returns an extension or bend, decreases $\delta$ measured from the fixed reference and is therefore not handled within an evaluation. When straightening is performed, that evaluation ends and a new evaluation is declared (Part 3, Stage 6).

The irreversible latch is not released automatically during an evaluation (AXIOMS.md §10.4).

$$
\ell_n\ge\ell_{n-1}
$$

The event history always grows.

$$
\mathsf{History}_n=\mathsf{History}_{n-1}\oplus \mathrm{Ev}_n,\qquad \#\mathsf{History}_n=\#\mathsf{History}_{n-1}+1
$$

$\oplus$ is not addition but "appending to the end of the record sequence," and $\#$ is the number of records.

Only the reversible component $q$ may decrease through the passage of time alone. This writes AXIOMS.md §7 (non-spontaneous recovery of $\tau$ and of residual deviation) for each decomposed component. AXIOMS.md §7 states that residual deviation does not decrease during an evaluation and that, when straightening is performed, the evaluation is declared anew.

### P7　Fixed reference (→[5])

The reference state is fixed by $\mathsf{Decl}$ and is not reset during an evaluation. Residual deviation $p_n$ is kept as part of $\delta$ , not as a shift of the reference. Redeclaring the reference is permitted only between evaluations (Part 3, Stage 6).

Correspondence with the canon: AXIOMS.md §4.

### P8　Authority

$q,p,\lambda,\tau_0$ and their increments are obtained only from Cause-Side observation or pre-fixed transformation rules. They are not back-calculated from Effect-Side outputs or visualization results (AXIOMS.md §14, reverse derivation A). The same applies when the evaluation uses auxiliary structural quantities ( $\omega$ , $\mathrm{Phase}$ , $C$ , $W$ , $\mathrm{entropy}$ of AXIOMS.md §4.5); they must not be obtained from evaluation outputs ( $R$ , the canonical state, the irreversible latch, or their aggregates) (AXIOMS.md §4.5).

P8 is a premise about **the kind of input source**. The next premise, P9, is a premise about **the shape of the computation path**, which must hold even when all input sources are Cause-Side.

### P9　Categories of target state, gauge, and evaluation output (→[9])

**Three categories:** the quantities appearing in an evaluation are divided into the following three.

| Category | Symbol | Contents | Character |
|---|---|---|---|
| Target state | $\mathsf{Phys}^{(\mathrm{self})}_n$ | $q_n,p_n,\lambda_n$ (and $\delta_n,\tau_n$ determined from them) | the physical state of the target itself; moves under the physical laws of the target |
| Gauge | $\mathsf{Gauge}^{(\mathrm{self})}$ | the reference state, $\sigma$ , thresholds, shape-transformation functions $h_{\mathrm{upper}},h_{\mathrm{lower}}$ , EMA coefficients, $\tau_{\mathrm{upper}},\tau_{\mathrm{lower}}$ | the ruler that measures the target and the lines regarded as dangerous |
| Evaluation output | $\mathsf{Out}^{(\mathrm{self})}_n$ | $R_n,R_{\mathrm{upper}},R_{\mathrm{lower}},R_{\mathrm{dir}},\ell_n$ , the canonical state, and their moving averages and aggregates | the result of reading the target with the gauge |

The position of evaluation outputs follows "Position of evaluation outputs" in AXIOMS.md §14.

**Reverse derivation** ("Definition of reverse derivation" in AXIOMS.md §14):

$$
\text{reverse derivation}\iff
\underbrace{\exists\ \text{path}\ (\text{Effect-Side output})\leadsto\mathsf{Phys}^{(\mathrm{self})}\cup\mathsf{Gauge}^{(\mathrm{self})}\cup\mathsf{Out}^{(\mathrm{self})}}_{\text{(i) reverse derivation A: authority backflow}}
\ \lor\
\underbrace{\exists\ \text{path}\ \mathsf{Out}^{(\mathrm{self})}_m\leadsto\mathsf{Gauge}^{(\mathrm{self})}\quad(\text{any step, including via other structures})}_{\text{(ii) reverse derivation B: self-adjustment of the gauge}}
$$

Reason for (ii): even if all inputs are Cause-Side, if the output of the evaluation moves its own ruler or danger lines, the gauge "adjusts itself to its own reading." Widening the width as $R$ rises hides the approach; narrowing it as $R$ rises exaggerates the approach. In either direction, $R$ comes to reflect the history of the gauge itself rather than the state of the target. It is therefore prohibited regardless of direction. The same holds when an earlier-step $R$ or a moving average of $R$ is used, or when the path returns via another structure ( $R^{(\mathrm{self})}\to\mathsf{Gauge}^{(i)}\to R^{(i)}\to\mathsf{Gauge}^{(\mathrm{self})}$ ).

**Evaluation outputs of other evaluation targets** (AXIOMS.md §14):

$$
\text{(iv)}\quad \text{an edge }\mathsf{Out}^{(i)}\to(\text{thresholds}^{(\mathrm{self})},\ \tau^{(\mathrm{self})}_{\mathrm{upper}},\ \tau^{(\mathrm{self})}_{\mathrm{lower}})\ \text{is allowed only in the safe-side direction (narrowing gate widths, lowering thresholds), and only when there is no path from }\mathsf{Out}^{(\mathrm{self})}\text{ to structure }i
$$

(iv) allows only edges to the thresholds and effective gate widths among the gauge elements. Edges that feed another structure's evaluation outputs into the reference state or the projection rule $\sigma$ are not covered by (iv). The existence and rule of such an edge are fixed before evaluation begins (AXIOMS.md §14).

Difference between (ii) and (iv): (ii) moves one's own ruler by one's own reading and is therefore prohibited regardless of direction. (iv) is an edge that receives another structure's reading; without a cycle, it is not self-adjustment. However, the widening direction would hide the approach of this structure on account of another structure's state, so it is limited to the safe side.

**The criterion is not the name of the symbol but the origin and rewrite target of the path** (AXIOMS.md §14). For that purpose, things with different origins are given different names.

- **A ratio inside a physical law:** that the law of the target state depends on the ratio of a physical load (for example, fatigue degradation progressing with the stress ratio) is legitimate as the physics of the target. This ratio is computed inside the physical law directly from Cause-Side $\delta$ and $\tau$ . It is written with the Cause-Side arguments shown directly, as in $\Delta\lambda^{[e]}_n=g^{[e]}_\lambda(\delta_n,\tau_n,\dots)$ . This ratio is not named $R$ .
- **The evaluation output $R$ :** the stored evaluation output $R$ (including its moving averages, aggregates, and state categories) must not be read back to update the target state $\mathsf{Phys}$ . This applies to the evaluation outputs of this structure and of other structures alike. The target state is obtained only from Cause-Side observation or pre-fixed transformation rules (P8, AXIOMS.md §14).
- **A rule that rewrites the gauge:** a rule that rewrites the gauge $\mathsf{Gauge}$ is a path that moves the gauge by the same ratio as the evaluation even if it is rewritten as $\delta/\tau$ without the name $R$ , and falls under (ii).

**Examples of permitted and prohibited edges:**

| Edge | Judgment | Reason |
|---|---|---|
| $\mathrm{EMA}(\delta_{\le n})\to\tau_{\mathrm{upper}},\tau_{\mathrm{lower}}$ | permitted | the input to the gauge is the history $\delta$ of the target, not an evaluation output (FORMULA.md §4.4) |
| $f(\delta)\to\Delta\lambda_n\to\tau_n$ | permitted | a physical law of the target; only in the direction of decreasing thickness (the $\tau$ state-transition equation of AXIOMS.md §7) |
| $g^{[e]}_\lambda(\delta_{n-1},\tau_{n-1},\dots)\to\lambda^{[e]}_n$ | permitted | the rewrite target is the target state; the load ratio is computed inside the physical law directly from Cause-Side $\delta$ and $\tau$ (the stored $R$ is not read back) |
| a physical event observed in structure $i$ (rupture, load transfer, and so on) $\to\mathsf{Alloc}^{(\mathrm{self})}\to a^{(\mathrm{self})},\Delta p^{(\mathrm{self})},\Delta\lambda^{(\mathrm{self})}$ | permitted | the physical state of another structure is received as a Cause-Side observation event (Part 3, Stage 7) |
| $R^{(i)}_n\to\Delta\lambda^{(\mathrm{self})}$ or any other target state of this structure | prohibited | $R^{(i)}$ is an evaluation output, not a Cause-Side observation; $\delta$ , $\tau$ , and the target state are obtained only from Cause-Side observation or pre-fixed transformation rules (AXIOMS.md §14) |
| $R^{(i)}_n\to\tau^{(\mathrm{self})}_{\mathrm{upper}}$ (narrowing) | permitted | (iv), on the safe side and without a cycle |
| $R^{(\mathrm{self})}$ or its average $\to\tau^{(\mathrm{self})}_{\mathrm{upper}},\ $ thresholds | prohibited | (ii) self-adjustment of the gauge, regardless of direction |
| $R^{(\mathrm{self})}\to\mathsf{Gauge}^{(i)}\to R^{(i)}\to\mathsf{Gauge}^{(\mathrm{self})}$ | prohibited | (ii) self-adjustment via another structure |
| LLM self-evaluation $\to\delta$ | prohibited | (i) backflow of the input source |
| $R\to\ell\to$ canonical state | permitted | computation within evaluation outputs; returns neither to the gauge nor to the target |

Two structures that influence each other can be represented without falling under (ii) by linking them through each other's target states (concentration, displacement, degradation fraction, and so on) rather than through each other's gauges.

The classification of the meanings of reverse derivation follows `theory/SANDWICH_ARCH.md` §8.4. The remaining conditions of P9 ((iii), (v), (vi)) are placed in Part 3.

---

## 3. The Derivation Chain (observation → $\delta$ , $\tau$ → $R$ )

Stages 1–3 are the pre-stage before the Primary Formula, and Stage 4 is the Primary Formula. The transitions after the Primary Formula (Stages 5–7) are placed in Part 3.

### 3.1 Stage 1　Projection: from observation to accumulated deviation

$$
\delta_n=\sigma(o_n)\ \ge0
$$

$\sigma$ is the rule that maps an observation value to "the distance measured from the reference state in the declared rupture direction." A multivariate observation is combined into one quantity here. The concrete form of $\sigma$ is a governing equation of the domain or a validated transformation rule; the "domain-specific physical equations" mentioned in FORMULA.md §0 enter here.

Example (`examples/13_photosynthesis_layer5_JP.html`): the photosynthesis rate is computed with the FvCB model, and $\delta=\max(0,\ \text{maximum photosynthesis rate}-\text{photosynthesis rate})$ . The demo itself states that "Layer 5 only generates $\delta$ ; $R=\delta/\tau$ does not change," which is an existing example of separating the projection from the judgment formula.

### 3.2 Stage 2　Decomposition: the two components of accumulated deviation

$$
\boxed{\ \delta_n=q_n+p_n\ }
$$

- $q_n$ : the part that returns to 0 when the action is removed (reversible component)
- $p_n$ : the part that remains after the action is removed (irreversible component, residual deviation)

**Proposition 0 (an observation with a fixed reference contains history):** under P5 and P7, an observation in the unloaded state with neither action nor temporary condition ( $a=0$ , $q=0$ ) gives $\delta=\sigma(o)=p_n$ . Hence the instantaneously measured $\delta_n$ contains $p_n=p_0+\sum_{m=1}^{n}\Delta p_m$ , the sum of the residual $p_0$ at the start of evaluation and the residuals of all subsequent events.

**Proof:** substituting $q_n=0$ into the consistency with the projection of P5, $q_n+p_n=\sigma(o_n)$ , gives $\sigma(o_n)=p_n$ . The form of $p_n$ follows from the definition of increments in P5. Since the reference does not move by P7, $\sigma$ measures from the same origin throughout the evaluation. ∎

$p_0$ is the deviation that already remains from the reference state at the start of evaluation. If the reference is placed at the unloaded state at the start of evaluation, $p_0=0$ (for the spring of Part 1, the natural length when it was bought).

In this way, "$\delta$ is not merely an instantaneous value; it is accumulated deviation that carries history" (AXIOMS.md §4) and implementations based on instantaneous observation are **compatible under two conditions: the fixed reference (P7) and the retention of $p$**. $q$ and $p$ are separated by observation in the unloaded state or by a model fixed in $\mathsf{Alloc}$ .

The ways of constructing $\delta$ found in existing materials are positioned as follows.

| $\delta$ in existing materials | Examples | Position in this document |
|---|---|---|
| present deviation from an optimum | examples 18, 20, 27–30 | $\delta_n$ itself; compatible with the canon if the reference is fixed and $p$ is not discarded |
| a quantity that accumulates and only increases | paper v3, Axiom2 series | the special case $q\equiv0$ |
| the amount exceeding a threshold | examples 08–11 | a different evaluation declaration with the reference state placed at the threshold |
| the degree of disagreement among several channels | examples 24 | a declaration that chooses the disagreement as $\sigma$ |
| a quantity that accumulates and returns to 0 at each jump | examples 06, 26 (escapement) | a periodic example of transitions between evaluations (Part 3, Stage 6) |

### 3.3 Stage 3　Thickness: three layers

$$
\boxed{\ \tau_n=(1-\lambda_n)\,\tau_0\ }
$$

This is the form for a single element (only the structure at declaration). The general form with addition and removal of structural elements is given below in "Addition and removal of structural elements." The declared thickness $\tau_0$ represents, as in the canon (AXIOMS.md §7, §8), the absorption thickness of the whole structure at the start of evaluation. With several elements, $\tau_0=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_0)_{e\in\mathsf{Active}_0}\bigr)$ for the active elements $\mathsf{Active}_0$ at the start of evaluation, and $\tau_0=\tau^{[0]}_0$ for a single element.

| Layer | Symbol | Character | Used in |
|---|---|---|---|
| Declared thickness | $\tau_0$ | fixed by the evaluation declaration | the starting point of each evaluation |
| Effective thickness | $\tau_n$ | non-increasing unless a structural element is added | the Primary Formula |
| Side-specific effective gate widths | $\tau_{\mathrm{upper}}(n)$ , $\tau_{\mathrm{lower}}(n)$ | may increase or decrease | only the Secondary Formula (FORMULA.md §4.4) |

As FORMULA.md §4.4 states, the side-specific effective gate widths "do not mean that the underlying absorption thickness $\tau$ has naturally recovered."

#### Addition and removal of structural elements (→[10])

The only path by which absorption thickness increases is adding a new structural element to the evaluation target (**addition of a structural element**, or simply addition). The thickness of existing elements does not return. Conversely, the planned taking-out of an undamaged structural element is called **removal of a structural element** (or simply removal). Removal is not degradation and is not counted in the degradation fraction $\lambda$ .

The structure at declaration is element $e=0$ , and elements added at update number $n_e$ are $e=1,2,\dots$ . Each element has its own declared thickness and degradation fraction. The set of elements included in the evaluation target at step $n$ (added and not yet removed) is called the **active elements** $\mathsf{Active}_n$ .

$$
\tau^{[e]}_n=(1-\lambda^{[e]}_n)\,\tau^{[e]}_0\qquad(e\in\mathsf{Active}_n)
$$

$$
\boxed{\ \tau_n=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_n)_{e\in\mathsf{Active}_n}\bigr)\ }
$$

The composition rule $\mathrm{Comp}_\tau$ is subject to the following.

1. It is non-decreasing in each argument.
2. If removal is allowed within an evaluation, removing one argument (element) does not increase the value. For forms that do not satisfy this condition (forms such as the series link $\mathrm{Comp}_\tau=\min_e\tau^{[e]}_n$ , in which removing and reconnecting a weak element makes the whole stronger), removal is not handled within the evaluation and is treated as a change of the evaluation declaration (Part 3, Stage 6).
3. The value is finite and non-negative, and its unit is $u$ , the same as the element thicknesses.
4. When the active elements consist of a single element $e$ only, $\mathrm{Comp}_\tau(\tau^{[e]}_n)=\tau^{[e]}_n$ for any $e$ . With only the element at declaration, $e=0$ , the boxed formula above is recovered.
5. When the thicknesses of all elements are 0, and when the active elements are empty, the value is 0.
6. The declared thickness $\tau^{[e]}_0$ of an added element is determined by Cause-Side measurement at the time of addition, not from evaluation outputs such as $R$ (P8, P9).
7. Additions and removals are recorded as events in the event history $\mathsf{History}$ .

When a removed element is later put back, it is treated again as an addition, and its thickness is determined by Cause-Side measurement at the time it is put back. Degradation that progressed while it was removed is included in that measurement.

**Corollary (non-increase in intervals without addition):** in an interval without addition ( $\mathsf{Active}_{n+1}\subseteq\mathsf{Active}_n$ ), $\tau_{n+1}\le\tau_n$ .

**Proof:** by P6, $\lambda^{[e]}$ of each element does not decrease, so each $\tau^{[e]}$ does not increase. By condition 1, the value of $\mathrm{Comp}_\tau$ for the remaining elements does not increase. Since removal within an evaluation occurs only when condition 2 holds, taking out a removed element does not increase the value. ∎

Hence $\tau_n$ increases only at the time of an addition, which agrees with AXIOMS.md §7: "in a closed operating interval without addition of a structural element, $\tau$ does not increase with time." An addition may occur at any time (even right after the start of evaluation). The concrete form of $\mathrm{Comp}_\tau$ differs by domain (for example, the sum $\mathrm{Comp}_\tau=\sum_e\tau^{[e]}_n$ for elements placed in parallel) and is fixed in advance in the evaluation declaration (P0).

The agent performing an addition does not matter. Reinforcement by a person and repair by a living body forming new tissue are both treated as additions. Three cases of the relation between evaluation outputs and additions are distinguished.

- Using $R$ as the trigger for a pre-fixed reinforcement operation (such as adding capacity with an autoscaler): permitted. Evaluation outputs may be used for pre-fixed physical-control commands (AXIOMS.md §14).
- Accepting, on the basis of $R$ alone, that "an addition has physically been made" or that "the thickness has increased": prohibited. Evaluation outputs are not grounds for the target state.
- Measuring anew on the Cause-Side that the addition has been made and how much thickness was added: required.

When an AI execution system claims that it has added a boundary to itself through its own output, this is not accepted as an addition unless it can be shown by Cause-Side measurement.

If element $e$ breaks ( $\lambda^{[e]}=1$ ), its thickness becomes 0. As long as the value of $\mathrm{Comp}_\tau$ is positive, the evaluation of the whole continues. "Small rupture points" within an evaluation can be represented in this form. An evaluation ends when, for example, the evaluation target as a whole reaches $R\ge1$ (Part 3, Stage 6).

**Corollary (loss of all elements):** when all active elements have broken, or all have been removed, $\tau_n=0$ by condition 5, and the result is OUT_OF_DESCRIPTION_DOMAIN (Lemma 1). Depending on the form of $\mathrm{Comp}_\tau$ , $\tau_n=0$ may result when only some elements break (for example, with the series link $\mathrm{Comp}_\tau=\min_e\tau^{[e]}_n$ , the thickness of the whole becomes 0 when one element breaks. This form satisfies conditions 1, 3, 4, and 5 but not condition 2, so removal is not handled within the evaluation).

#### Why repair is not treated as recovery

One might read a repair such as build-up welding as "the degradation fraction returned" (repair recovery). The thickness of the whole at the time of welding can be the same under either reading. The difference appears in the subsequent treatment and in the record.

Example: a member with declared thickness 30 and degradation fraction 0.2 (effective thickness 24) is strengthened by welding to the equivalent of 27. The heat of welding adds a degradation fraction of 0.02 to the base metal, and the declared thickness of the weld is 3.6 (values are illustrative).

| | Read as "the degradation fraction returned" | Read as "addition of a structural element" |
|---|---|---|
| Thickness of the whole at the time of welding | $\lambda$ is returned from 0.2 to 0.1; $30\times0.9=27$ | base metal $30\times(1-0.22)=23.4$ combined with weld 3.6 gives $27.0$ ( $\mathrm{Comp}_\tau$ is the sum) |
| Record of base-metal degradation | rewritten to 0.1; the fact that it was damaged disappears from the value | stays at 0.22 (including the part due to welding heat) |
| Degradation of the weld | assumed to progress with the same degradation fraction as the base metal | progresses under the weld's own laws (weld defects, residual stress, and other failure modes different from the base metal) |
| When the weld breaks | what broke cannot be distinguished in the formula | represented as the rupture of one element (thickness 0) |

Reading it as "the degradation fraction returned" identifies the recovery of a value, the thickness of the whole, with the restoration of the physical state of the base metal, which contradicts P6 and Proposition 2a. The practice of attaching a separate inspection record to a repaired member and reassessing its capacity also agrees with the reading as an addition.

#### Classifying cases where the thickness appears to change

| Apparent phenomenon | Classification | Effective thickness $\tau_n$ |
|---|---|---|
| returns with time | natural recovery | not increased (AXIOMS.md §7) |
| a receiving width temporarily narrowed by an action or condition returns (for example, strength reduction at high temperature, a new server warming up) | reversible change | not subtracted from $\tau_n$ (AXIOMS.md §7). In the Primary Formula it is counted as the temporary reversible deviation $q^{\mathrm{temp}}$ (see "When the receiving width narrows temporarily" below). In the Secondary Formula it is handled with the side-specific effective gate widths |
| the side-specific effective gate widths widen | change of the gauge of the Secondary Formula | not increased (FORMULA.md §4.4) |
| thresholds, filters, or gate widths are adjusted by evaluation outputs | self-adjustment of the gauge | not increased (reverse derivation B, AXIOMS.md §14) |
| the declared thickness changes with a new observation | update of the evaluation snapshot | not increased within the evaluation; redeclared as the next evaluation snapshot (FORMULA.md §6, AXIOMS.md §14) |
| reinforcement, expansion, or a new boundary | addition of a structural element | **increases** (the path of this section) |
| an element is replaced | removal of the old element (rupture, if it was broken) and addition of a new element | decreases by the old element and increases by the new element |
| an undamaged element is taken out as planned (for example, server downscaling) | removal of a structural element | decreases; not counted in $\lambda$ |
| damage is repaired (welding, filling, and so on) | addition of an element, the repair material; the degradation fraction of existing elements does not decrease | increases by the repair material |
| an extension or bend is forcibly returned | straightening | not handled within the evaluation; the evaluation ends and is redeclared (P6) |

In an AI execution system, adjusting filters or thresholds is a change of the gauge, not an increase of thickness. The thickness can be said to have increased only when another structure or boundary whose grounds can be shown on the Cause-Side has newly been established. An implementation using a dynamic $\tau$ states which row of this table each increase or decrease belongs to (AXIOMS.md §7, interpretive-boundary comment).

#### When the receiving width narrows temporarily (temporary reversible deviation)

The width that a structure can receive may narrow temporarily due to an action or condition and return when the condition ends (strength reduction at high temperature, a server warming up, and so on). Subtracting the narrowed width from the effective thickness would mean the thickness increases when it returns, which contradicts AXIOMS.md §7. The narrowed width is therefore counted on the deviation side. This quantity is the **temporary reversible deviation** $q^{\mathrm{temp}}_n\ge0$ ; the allocation rule $\mathsf{Alloc}$ allocates it to the action $a_n$ and makes it part of the reversible component $q_n$ . Permanent damage left by the condition is allocated not to $q^{\mathrm{temp}}_n$ but to $\Delta\lambda_n$ (one change, one allocation, P5).

**Corollary (safe-side character of counting on the deviation side):** let the deviation other than $q^{\mathrm{temp}}$ be $\delta\ge0$ , with $0\le q^{\mathrm{temp}}<\tau$ and $\delta+q^{\mathrm{temp}}\le\tau$ . For the ratio counted on the deviation side, $(\delta+q^{\mathrm{temp}})/\tau$ , and the ratio with the narrowed width subtracted on the thickness side, $\delta/(\tau-q^{\mathrm{temp}})$ ,

$$
\frac{\delta+q^{\mathrm{temp}}}{\tau}-\frac{\delta}{\tau-q^{\mathrm{temp}}}=\frac{q^{\mathrm{temp}}\,(\tau-\delta-q^{\mathrm{temp}})}{\tau\,(\tau-q^{\mathrm{temp}})}\ \ge0
$$

and both reach 1 simultaneously at $\delta+q^{\mathrm{temp}}=\tau$ .

**Proof:** bringing to a common denominator, the numerator is

$$
(\delta+q^{\mathrm{temp}})(\tau-q^{\mathrm{temp}})-\delta\,\tau
=q^{\mathrm{temp}}\,\tau-\delta\,q^{\mathrm{temp}}-\bigl(q^{\mathrm{temp}}\bigr)^2
=q^{\mathrm{temp}}\,(\tau-\delta-q^{\mathrm{temp}})
$$

The denominator is positive, and $q^{\mathrm{temp}}\ge0$ and $\tau-\delta-q^{\mathrm{temp}}\ge0$ , so it is non-negative. ∎

This is the form of Proposition 1 with $p$ replaced by $q^{\mathrm{temp}}$ . The rupture point does not change, and before rupture, counting on the deviation side gives an $R$ that is equal or larger (safe side). Numerical check: with $\tau=30$ , $\delta=12$ , $q^{\mathrm{temp}}=6$ , $18/30=0.60$ , $12/24=0.50$ , and the difference is $0.10=6\times12/(30\times24)$ .

Whether temporarily taking out an element for maintenance is treated as removal and re-addition or as $q^{\mathrm{temp}}$ is decided in advance in the evaluation declaration.

**Restoration degradation:** in a structure that has reached rupture or phase transition (AXIOMS.md §8), the degradation of existing elements remains as it is. This document reads $\tau_{\mathrm{restored}}$ of §8 as "the absorption thickness of existing elements, excluding added elements." Under this reading, the constraint $\tau_{\mathrm{restored}}<\tau_0$ of §8 is a constraint on existing elements and does not contradict addition. The effective thickness of the whole may exceed $\tau_0$ through addition, but that is not restoration to the initial structure. This reading and sentence are in AXIOMS.md §8.

### 3.4 Stage 4　The Primary Formula

From the above, the Primary Formula is reached in the following form.

$$
\boxed{\
R_n=\frac{\delta_n}{\tau_n}=\frac{q_n+p_n}{\mathrm{Comp}_\tau\bigl(((1-\lambda^{[e]}_n)\,\tau^{[e]}_0)_{e\in\mathsf{Active}_n}\bigr)}
\ }
$$

$$
M_{\tau,n}=\tau_n-\delta_n=\mathrm{Comp}_\tau\bigl(((1-\lambda^{[e]}_n)\,\tau^{[e]}_0)_{e\in\mathsf{Active}_n}\bigr)-q_n-p_n
$$

For a single element (only the structure at declaration), this is as follows.

$$
R_n=\frac{q_n+p_n}{(1-\lambda_n)\,\tau_0},\qquad
M_{\tau,n}=(1-\lambda_n)\tau_0-q_n-p_n
$$

In the lemmas and propositions below, statements marked "for a single element" use this form.

The numerator represents "how far it has penetrated," and the denominator "how much of the vessel remains now." The Primary Formula itself has not been changed. The only change is that the contents of $\delta$ and $\tau$ are written out in decomposed form.

---

## 4. Lemmas and Propositions

### Lemma 1　Satisfaction of the domain and its boundary

(a) General case: if $q_n,p_n\ge0$ are finite and the value of the composition rule $\tau_n=\mathrm{Comp}_\tau(\cdot)$ is positive, then $\tau_n$ is finite (condition 3 of $\mathrm{Comp}_\tau$ ) and positive, and $\delta_n=q_n+p_n\ge0$ is finite. Hence P4 is satisfied. When $\tau_n=0$ (loss of all elements and so on; the corollary in Part 2, 3.3), P4 is not satisfied.

(b) Single element: if $\tau_0>0$ , $0\le\lambda_n<1$ , and $q_n,p_n\ge0$ , all finite, then

$$
\tau_n=(1-\lambda_n)\tau_0>0,\qquad \delta_n=q_n+p_n\ge0
$$

**Proof:** (a) follows from the assumptions, condition 3 of $\mathrm{Comp}_\tau$ , and the fact that a sum of non-negative numbers is non-negative. (b) follows from the product of $1-\lambda_n>0$ and $\tau_0>0$ being positive. ∎

When $\tau_n=0$ , the result is **OUT_OF_DESCRIPTION_DOMAIN**, as in the canon ( $\tau=0$ is not replaced by an infinite $R$ ; FORMULA.md §1, AXIOMS.md §6). For a single element, $\tau_n=0$ when $\lambda_n=1$ . The order of the boundaries is described below for a single element. If $\lambda$ approaches 1 while $\delta>0$ , $R\ge1$ is reached when $\tau_n\le\delta_n$ , that is, when $\lambda_n\ge1-\delta_n/\tau_0$ . If $1-\delta_n/\tau_0\le\lambda_n<1$ at some update number, RUPTURE_BOUNDARY is recorded before OUT_OF_DESCRIPTION_DOMAIN. With discrete updates, however, $\lambda$ may reach 1 in a single step without passing through this interval. In that case, and when the thickness is exhausted while $\delta=0$ , the classification at that step is OUT_OF_DESCRIPTION_DOMAIN even if the preceding $R$ was below 1. $\tau=0$ is not reinterpreted as RUPTURE_BOUNDARY.

### Lemma 2　Dimensionlessness

If $[\delta]=[\tau]=u$ , then $[R]=1$ . $\lambda$ is a fraction and therefore dimensionless, and the unit of each element's thickness remains the unit $u$ of the declared thickness. The value of the composition rule also keeps the unit $u$ (condition 3 of $\mathrm{Comp}_\tau$ ). ∎

### Lemma 3　Monotonicity

(a) General case: in the range $\tau_n>0$ , $R_n$ is increasing in $q_n$ and $p_n$ and non-decreasing in the degradation fraction $\lambda^{[e]}_n$ of each element.

**Proof:** the denominator of $R=(q+p)/\tau$ is positive regardless of $q$ and $p$ , so $R$ is increasing in $q$ and $p$ . $\tau^{[e]}=(1-\lambda^{[e]})\tau^{[e]}_0$ is decreasing in $\lambda^{[e]}$ , and $\mathrm{Comp}_\tau$ is non-decreasing in each argument (condition 1), so $\tau$ is non-increasing in $\lambda^{[e]}$ . Since $q+p\ge0$ , $R$ is non-decreasing in $\lambda^{[e]}$ . ∎

(b) Single element:

$$
\frac{\partial R}{\partial q}=\frac{\partial R}{\partial p}=\frac{1}{(1-\lambda)\tau_0}>0,
\qquad
\frac{\partial R}{\partial \lambda}=\frac{q+p}{(1-\lambda)^2\tau_0}\ge0
$$

$R$ rises whether the deviation increases or the vessel shrinks. There are two reasons for approaching the boundary, and both are distinguished in the formula (→[4] [8]). ∎

### Proposition 1　Safe-side character of the fixed reference (→[5])

Consider the representation in which the reference is reset to the position of the residual deviation.

$$
\delta'=q,\qquad \tau'=\tau-p,\qquad R'=\frac{q}{\tau-p}\quad(\tau>p)
$$

Then the following hold.

(a) The remaining margin is the same: $M'_\tau=\tau'-\delta'=\tau-p-q=M_\tau$

(b) The rupture point is the same: $R=1\iff q+p=\tau\iff R'=1$

(c) Before rupture ( $M_\tau\ge0$ ), always

$$
R-R'=\frac{p\,M_\tau}{\tau(\tau-p)}\ge0
$$

**Proof of (c):**

$$
R-R'=\frac{(q+p)(\tau-p)-q\tau}{\tau(\tau-p)}
=\frac{p\tau-qp-p^2}{\tau(\tau-p)}
=\frac{p(\tau-q-p)}{\tau(\tau-p)}
=\frac{p\,M_\tau}{\tau(\tau-p)}
$$

The denominator is positive, and $p\ge0$ and $M_\tau\ge0$ , so it is non-negative. ∎

**Meaning:** the rupture point ( $R=1$ ) agrees in both representations. On the other hand, reaching the intermediate thresholds $R_{\mathrm{warn}}$ , $R_{\mathrm{handoff}}$ , $R_{\mathrm{irrev}}$ is **delayed** in the representation with the reset scale. Moreover, after unloading ( $q=0$ ), $R'=0$ and it is displayed as "completely returned." The fixed reference (P7) is not a matter of preference; it is **the premise for not delaying warnings and not hiding history**. When the reference is redeclared between evaluations (Part 3, Stage 6), $\tau'=\tau-p$ is enforced in order to keep the agreement of the rupture point in (b).

**Numerical check** (the spring of Part 1, $\tau=27$ , $p=3$ , $q=12$ ):

$$
R=\frac{15}{27}\approx0.556,\qquad R'=\frac{12}{24}=0.5,\qquad
\frac{p\,M_\tau}{\tau(\tau-p)}=\frac{3\times12}{27\times24}=\frac{36}{648}\approx0.056
$$

The difference $0.556-0.5=0.056$ agrees.

### Proposition 2　The return of a value does not mean the restoration of the structure (→[6])

Let $o$ be the observable value. The following three are distinguished.

- **The physical state of the target** $\mathsf{Phys}_n=(q_n,p_n,(\lambda^{[e]}_n)_{e\in\mathsf{Active}_n})$ (the target state of P9)
- **The evaluation state:** what is kept as an evaluation output, such as the irreversible latch $\ell_n$
- **The event history** $\mathsf{History}_n$ : the record of events (for audit and structural testimony)

The state before and after one observation event $\mathrm{Ev}$ is written $(-)$ and $(+)$ .

**Proposition 2a (physical state):** if $\Delta p>0$ in that event, or $\Delta\lambda^{[e]}>0$ for some element, then $\mathsf{Phys}^{(+)}\ne\mathsf{Phys}^{(-)}$ even if $o^{(+)}=o^{(-)}$ .

**Proof:** by the definition of increments in P5, $p^{(+)}=p^{(-)}+\Delta p$ and $\lambda^{[e](+)}=\lambda^{[e](-)}+\Delta\lambda^{[e]}$ . If either increment is positive, that component differs. Agreement of $o$ does not include agreement of this component. ∎

Example: the new spring and the once-pulled spring of [6] in Part 1 are at the same 15 mm position (the same $o$ ), but $p$ (0 and 3) and $\lambda$ (0 and 0.1) differ.

**Proposition 2b (event history):** for any event, $\mathsf{History}^{(+)}\ne\mathsf{History}^{(-)}$ .

**Proof:** by P6, $\#\mathsf{History}^{(+)}=\#\mathsf{History}^{(-)}+1$ . ∎

**Relation between the two propositions:** for an event entirely within the elastic range ( $\Delta p=0$ , all $\Delta\lambda^{[e]}=0$ , and $q=0$ after unloading), the physical state returns ( $\mathsf{Phys}^{(+)}=\mathsf{Phys}^{(-)}$ ). Proposition 2a asserts nothing about this case. Even so, the record that the event occurred remains in the event history (Proposition 2b). This corresponds to the corollary of the sole Nomological Ring Axiom, "exact reproduction of identical history is impossible" (AXIOMS.md §2). The return of the value ( $o$ ), the return of the physical state ( $\mathsf{Phys}$ ), and the identity of the history ( $\mathsf{History}$ ) are separate questions. "Even if the value returns, the event history does not return" is the claim of Proposition 2b, and "even if the value returns, the structure has not returned" is the claim of Proposition 2a when an irreversible change has occurred.

**Thresholds and the history of transitions:** while degradation does not progress within the safe region (the range where no threshold has been crossed), a linear computation in which $R$ is proportional to $\delta$ suffices. The value of IDE appears when a boundary called a threshold appears. Crossing a threshold means that risks, fluctuations, or changes that had been invisible or overlooked begin to appear as recognizable events. That is why the transition — when and which threshold was crossed — is kept in the event history. The irreversible latch (Part 3, Stage 5) reflects that transition in the evaluation state.

Furthermore, if $\Delta p>0$ or $\Delta\lambda>0$ , $R$ for the same action also differs (Proposition 4).

### Proposition 3　R does not exhaust the state (non-sufficiency of R)

For a single element with $\tau_0=30$ , consider the following two structures (since this is a counterexample, one suffices).

| | $q$ | $p$ | $\lambda$ | $\delta$ | $\tau$ | $R$ |
|---|---|---|---|---|---|---|
| A | 12 | 0 | 0 | 12 | 30 | 0.40 |
| B | 3 | 6 | 0.25 | 9 | 22.5 | 0.40 |

$R$ is the same, 0.40. Now apply the same action, which produces a reversible component of 15.

| | $\delta$ | $\tau$ | $R$ |
|---|---|---|---|
| A | 15 | 30 | 0.50 |
| B | 21 | 22.5 | about 0.93 |

For the same action, A is halfway and B is on the verge of rupture. Wherever the thresholds are placed, A and B do not necessarily fall into the same category.

**Conclusion:** $R$ is an **evaluation output** that indicates the approach to the boundary (AXIOMS.md §14), not the structural state itself. What should be kept is not $R$ but the physical state of the target $(p,\lambda)$ and the irreversible latch $\ell$ as the evaluation state (the distinction of Proposition 2). ∎

**Relation to existing demos:** several demos in the repository share the concern of not determining the state from the instantaneous value of $R$ alone. However, none of them implements the conclusion of Proposition 3 as it is.

| Demo | Additional variable | Use in determining the state | Position from this document |
|---|---|---|---|
| examples 14 | residualDebt | RUPTURE_BOUNDARY when $R\ge1$ or debt $>0.8$ | debt is a quantity accumulated from $R$ . Determining RUPTURE_BOUNDARY by debt does not agree with AXIOMS.md §10.5 ( $R_{\mathrm{target}}\ge1.0$ ) |
| examples 15 | residualDebt | classification by $R_{\mathrm{eff}}=R_{\mathrm{total}}+0.4\,\mathrm{debt}$ | debt is a quantity accumulated from $R$ . Classifying by a value added to $R$ requires clarifying its relation to AXIOMS.md §5 ( $R$ means only $\delta/\tau$ ) |
| examples 21 | individual thresholds for PI and MGF | boundary determined by OR with conditions other than $R$ | combined use of judgments by other observed quantities |
| examples 23, 24 | $D_{\mathrm{long}}$ | toward the stopping side when $D_{\mathrm{long}}\ge1$ | $D_{\mathrm{long}}$ is a quantity made from the moving average $R_{\mathrm{short}}$ of $R$ |

residualDebt and $D_{\mathrm{long}}$ are both aggregates made from the history of $R$ (an evaluation output) and do not correspond to $(p,\lambda)$ (the target state) of this document. Both are also implemented to decrease with the passage of time. Reading them as quantities of residual deviation or degradation would contradict the non-spontaneous recovery of AXIOMS.md §7 (P6). Since the demos are subordinate to the canon (AXIOMS.md §16), this is addressed by clarifying the position of the demos.

### Proposition 4　Thickness reduction and history sensitivity (→[6])

For a single element, let the degradation fractions of two structures be $\lambda_{\mathrm{low}}$ and $\lambda_{\mathrm{high}}$ . If $\delta>0$ and $0\le\lambda_{\mathrm{low}}<\lambda_{\mathrm{high}}<1$ , then

$$
\frac{\delta}{(1-\lambda_{\mathrm{high}})\tau_0}>\frac{\delta}{(1-\lambda_{\mathrm{low}})\tau_0}
$$

Even with the same deviation, a structure whose vessel has become smaller through its history is closer to the boundary. In the general case, by Lemma 3(a), the $R$ of a structure with a larger degradation fraction of some element is not smaller (it is larger if $\mathrm{Comp}_\tau$ is strictly increasing in that element).

**The dam counterexample** ( $\tau_0=100$ , in units of deviation):

| | Present water level | $q$ | $p$ | $\lambda$ | $\delta$ | $\tau$ | $R$ |
|---|---|---|---|---|---|---|---|
| Dam A | low | 20 | 10 | 0.4 | 30 | 60 | 0.50 |
| Dam B | high | 40 | 0 | 0 | 40 | 100 | 0.40 |

**Dam A, with the lower water level, is closer to the boundary.** Present-value monitoring (judging by water level alone) shows this order reversed.

### Proposition 6　Consistency between the increment of the Primary Formula and the dual-fluctuation detection condition (→[8])

Indices follow the backward differences of FORMULA.md §4.7 ( $\Delta\delta_n=\delta_n-\delta_{n-1}$ , $\Delta\tau_n=\tau_n-\tau_{n-1}$ ).

$$
R_n-R_{n-1}=
\underbrace{\frac{\Delta\delta_n}{\tau_n}}_{\text{penetration term}}
+
\underbrace{\delta_{n-1}\Bigl(\frac{1}{\tau_n}-\frac{1}{\tau_{n-1}}\Bigr)}_{\text{contraction term}}
$$

**Proof:**

$$
R_n-R_{n-1}=\frac{\delta_{n-1}+\Delta\delta_n}{\tau_n}-\frac{\delta_{n-1}}{\tau_{n-1}}
=\frac{\Delta\delta_n}{\tau_n}+\delta_{n-1}\Bigl(\frac{1}{\tau_n}-\frac{1}{\tau_{n-1}}\Bigr)\qquad∎
$$

For a single element, using $\tau_n=(1-\lambda_n)\tau_0$ of Stage 3, the contraction term becomes

$$
\delta_{n-1}\Bigl(\frac{1}{\tau_n}-\frac{1}{\tau_{n-1}}\Bigr)=\frac{\delta_{n-1}\,\tau_0\,(\lambda_n-\lambda_{n-1})}{\tau_n\,\tau_{n-1}}
$$

which is non-negative by P6. In the general case with several elements, it is also non-negative in intervals without addition, and it can be negative at the time of an addition.

**Corollary:** when $\tau_n,\tau_{n-1}>0$ and $\delta_{n-1}>0$ ,

$$
\bigl(\Delta\delta_n>0\ \land\ \Delta\tau_n<0\bigr)
\iff
\bigl(\text{penetration term}>0\ \land\ \text{contraction term}>0\bigr)
$$

**Proof:** the sign of the penetration term equals the sign of $\Delta\delta_n$ ( $\tau_n>0$ ). The contraction term is $\delta_{n-1}(\tau_{n-1}-\tau_n)/(\tau_n\tau_{n-1})$ , and when $\delta_{n-1}>0$ its sign equals the sign of $-\Delta\tau_n$ . ∎

**Position:** the left-hand side is the dual-fluctuation detection condition of FORMULA.md §4.7. The corollary shows that the detection condition of the Secondary Formula is **consistent** with the change of the Primary Formula (a transition in which penetration and shaving of the vessel occur at the same time and $R$ is pushed up from two directions). It does not position the Secondary Formula as a consequence of the Primary Formula. The Secondary Formula is the second canonical IDE calculation system (FORMULA.md §4).

When $\delta_{n-1}=0$ , the contraction term is 0 even if $\Delta\tau_n<0$ . In a structure into which nothing has yet penetrated, the shaving of the vessel does not appear in the increment of $R$ and remains only in $\lambda$ . This is also a form of Proposition 3.

**Numerical check** (the spring of [8] in Part 1, $\tau_0=30$ ): before, $q=8,p=0,\lambda=0$ and $R=8/30\approx0.267$ . After pulling to 15 mm, $q=12,p=3,\lambda=0.1$ , $\tau=27$ , and $R=15/27\approx0.556$ .

$$
\text{penetration term}=\frac{7}{27}\approx0.259,\qquad
\text{contraction term}=8\Bigl(\frac{1}{27}-\frac{1}{30}\Bigr)\approx0.030
$$

The sum is $0.289$ , which agrees with $0.556-0.267=0.289$ .

(Proposition 5 presupposes the update rule and is therefore placed in Part 3.)

---

## 5. Application to Three Domains

| | $q$ (reversible component) | $p$ (residual deviation) | $\lambda$ (degradation fraction) | Examples of observations |
|---|---|---|---|---|
| Spring | elastic extension | permanent extension (gaps between coils) | reduction of breaking extension due to fatigue and microcracks | displacement, natural length, spring constant |
| Dam | elastic deformation due to water pressure | residual displacement and settlement | cracks, leakage paths, loss of stiffness | water level, displacement gauges, leakage volume, turbidity, crack length |
| Motor | temperature rise due to load (returns when cooled) | 0 depending on the declaration | insulation degradation, winding damage | current, temperature, insulation resistance, smoke |

- In a domain where $p$ does not exist, such as a motor, $\mathsf{Decl}$ declares $p\equiv0$ . **The element is not deleted; it is declared to be 0.**
- "Smoke came out" or "water leaked" is not itself a value of $\Delta\lambda$ . A rule that converts the observation into $\Delta\lambda$ ( $\mathsf{Alloc}$ ) is needed for each domain.
- A motor's "the breaker tripped" is $a_n=0$ (removal of the action), not the addition of a structural element. Therefore $q$ returns to 0, but $\lambda$ does not decrease. Stopping is not recovery.
- The thermal-damage integral of the earlier draft (damage accumulated over time by the amount exceeding the limit temperature; the thickness does not recover even when the temperature falls below the limit; earlier draft §14.1) can be read as a concrete example of $\mathsf{Alloc}$ that gives $\Delta\lambda$ in the motor row.

---

## 6. Correspondence with the Canon and Existing Materials

### 6.1 Correspondence with the canonical $\tau$ state-transition equation

The auxiliary model of AXIOMS.md §7

$$
\tau(t)=\tau_0-\int_0^t f(\delta(s))\,ds
$$

corresponds, for a single element, to the special case in which this document sets $\tau_0-\tau_n=\tau_0\lambda_n$ , associates the update number $n$ with the time $t_n$ , and gives the increment of degradation as

$$
\Delta\lambda_n=\frac{1}{\tau_0}\int_{t_{n-1}}^{t_n} f(\delta(s))\,ds
$$

If $\delta$ within the interval is represented by $\delta_{n-1}$ at the start of the interval, this becomes approximately $\Delta\lambda_n\approx f(\delta_{n-1})\,\Delta t_n/\tau_0$ ( $\Delta t_n=t_n-t_{n-1}$ ). The canonical statement "within a closed interval, $\tau$ is non-increasing" has the same content as $\lambda_n\ge\lambda_{n-1}$ (P6) in this document.

In the canonical equation, $\delta$ enters the numerator of $R$ and at the same time shaves $\tau$ . This is not double counting. $\delta$ enters $R$ as "the amount of penetration," and $f(\delta)$ enters $\lambda$ as "the action by which penetration wears the vessel," because they are different physical actions. This update is due to the physical law of the target structure and is not reverse derivation (AXIOMS.md §14).

### 6.2 Correspondence with the demos

| Demo | Reading in this document | Note |
|---|---|---|
| 25 dam degradation | $\delta$ = instantaneous fluctuation ( $q$ ), $\tau=\tau_0-k\int\delta$ ( $\lambda$ ); the special case $p\equiv0$ | a straightforward implementation of AXIOMS.md §7 |
| 13 photosynthesis | an example of the projection of Stage 1 | states explicitly that it "only generates δ" |
| 06, 26 escapement | periodic transitions between evaluations in Stage 6 of Part 3 | number of jumps = evaluation number |
| 14, 15 power grid, OR/ICU | Stage 6 of Part 3 (new evaluation and archive of the old history), Proposition 3 (debt) | debt is a quantity accumulated from $R$ and decreases with time. 14 determines RUPTURE_BOUNDARY by debt (the table of Proposition 3) |
| 23, 24 sample, vehicle | Proposition 3 ( $D_{\mathrm{long}}$ ) | $D_{\mathrm{long}}$ is a quantity made from the moving average of $R$ and decreases with time. 24 widens $\tau_{\mathrm{upper}}$ by the moving average of its own evaluation output, which is reverse derivation B (P9(ii)) |
| 07–12 band gates | dynamic change of the side-specific effective gate widths | it is not stated whether this is the effective thickness or the side-specific effective gate widths. 07 builds $\tau$ from the EMA of Cause-Side deviation and is not reverse derivation B |
| 18, 20, 27–30 tension, pressure, and others | the instantaneous-observation type of Stage 2 | compatible with the canon under the fixed reference and retention of $p$ |

### 6.3 Correspondence with the earlier draft

`nra-core/foundations/NRA-IDE_動的厚みと不可逆境界_会話統合_26-0802-1830.md` gave the following before this document. Some symbols of the earlier draft collide with those of this document (dictionary 0.5), so they are shown here in words, and the formulas are referred to in the corresponding sections of the earlier draft.

| Earlier draft (section) | This document |
|---|---|
| update of deviation and thickness per transition (§4.1) | the update rule of Stage 5 in Part 3. This document splits the increment of deviation into $\Delta q+\Delta p$ and the decrease of thickness into the increments of the per-element degradation fractions |
| "if the numerator increases and the denominator decreases at the same time, it is not linear" (§4.1) | written as a formula in Proposition 6 (penetration term and contraction term) |
| residual thickness and the one-transition collapse ratio (§5) | the residual thickness is $M_{\tau,n}$ . The one-transition collapse ratio can be used together as a one-step look-ahead of Stage 5 in Part 3 |
| boundary specification (declaration of eight items; §3) | the evaluation declaration $\mathsf{Decl}$ of P0 |
| irreversible thickness loss (§9.1) | $\Delta\lambda_n$ ( $\Delta\lambda^{[e]}_n$ with several elements) |
| finite-observation proximity that deducts unobserved parts from the thickness (§11.3) | a concrete example of the declared handling of missing data (a rule that does not increase the thickness for lack of observation) |

### 6.4 Classification of the meanings of reverse derivation

The classification of the meanings of "reverse derivation," "back-calculation," "backflow," and " $\Pi^{-1}$ " in the repository follows `theory/SANDWICH_ARCH.md` §8.4. P8 and P9 of this document are the premises from which reverse derivation A, reverse derivation B, and the treatment of the evaluation outputs of other evaluation targets in that classification are derived.

---

## 7. What Is Proved, What Is Declared, and What Is Verified

| Category | Content | Treatment |
|---|---|---|
| Can be proved | Lemmas 1–3, Propositions 0–4 and 6 (Part 2), Proposition 5 (Part 3) | closed as mathematics, as in this document |
| Declared | the elements of $\mathsf{Decl}$ (including the composition rule $\mathrm{Comp}_\tau$ ), declarations of zero such as $p\equiv0$ , the reference state, and which of target state, gauge, or evaluation output each quantity belongs to | not proved; commitments fixed before computation begins |
| Requires verification | the concrete form of $\sigma$ , how degradation progresses, $\tau_0$ and the $\tau^{[e]}_0$ of added elements, the concrete form of $\mathrm{Comp}_\tau$ , the values of the thresholds, and the conversion from observation to $\Delta\lambda$ | supported by measurement and experiment in the domain; the canon defines only the form and conditions |

The premise formulas need not "all be proved." What this document undertakes is up to the **proofs** and the **framework of declaration** in the table above. Concrete functional forms are left to each domain.

The elements of the evaluation declaration (including $\sigma$ , $\mathsf{Alloc}$ , and $\mathrm{Comp}_\tau$ ), one change one allocation, and consistency with the projection are defined in form and conditions by FORMULA.md §0.5 (v2.1). The fixed reference, the composition of accumulated deviation, and the addition and removal of structural elements are defined by AXIOMS.md §4 and §7. This document gives their derivation, proofs, and examples.

---

# Part 3　After the Primary Formula (before a decision on canonization)

This part deals with the transitions after the Primary Formula (transitions within an evaluation, transitions between evaluations, and links with hierarchies and other structures). The content of this part precedes any decision on canonization and is not a canonical definition. If it is canonized, it will be reflected in FORMULA.md and elsewhere after that decision.

## 1. Symbols of This Part

| Symbol | Name | Meaning | Part 1 |
|---|---|---|---|
| $\mathsf{Update}$ | update rule | the rule that advances the state within an evaluation (Stage 5) | — |
| $\rho$ | reversible response | the function that gives the reversible component from the action | — |
| $g_p$ , $g^{[e]}_\lambda$ | laws of irreversible increments | the functions that give the increments of residual deviation and degradation fraction | — |
| $\mathrm{Class}(R)$ | instantaneous classification | the canonical classification by intervals of valid $R$ (before reflecting the latch) | [7] |
| $\mathsf{State}_n$ | target boundary state | PERMIT to RUPTURE_BOUNDARY (reflecting the latch) | [7] |
| $j$ | evaluation number | which evaluation declaration it is | [10] |
| $\mathsf{Archive}$ | evaluation archive | the sequence of records of finished evaluations | [10] |
| $Z_n$ | decision-sufficient state | a record with named fields: residual deviation $p_n$ , active elements $\mathsf{Active}_n$ with each element's declared thickness and degradation fraction, and the irreversible latch $\ell_n$ (additional state if needed); a combination of the physical state and the evaluation state (dictionary "Decision-Sufficient State") | [11] |
| $\mathrm{EvalGraph}^{(j)}$ | expanded evaluation graph | a directed graph showing, over all steps of evaluation $j$ , from which quantities each quantity was computed | [9] |

## 2. The Remaining Conditions of P9

The directed graph that takes quantities as vertices and "a quantity was used to compute another quantity" as directed edges, connecting all steps of evaluation $j$ , is called the **expanded evaluation graph** $\mathrm{EvalGraph}^{(j)}$ . Its vertices include the quantities of other structures $i$ and Effect-Side outputs. $\mathrm{EvalGraph}^{(j)}$ contains no reverse derivation ((i) and (ii) of P9 in Part 2) and, in addition to (iv), satisfies the following.

$$
\text{(iii)}\quad \text{edges into the target state are limited to updates by the physical laws of the target, events through }\mathsf{Alloc}\text{ (}\Delta p\ge0,\ \Delta\lambda\ge0\text{), or the addition of a structural element}
$$

$$
\text{(v)}\quad \text{the computation at each step has no cycle, and the order of computation within the same step is declared in}\ \mathsf{Decl}
$$

$$
\text{(vi)}\quad \text{the existence of edges and the computation rule of each edge are fixed before evaluation as elements of}\ \mathsf{Decl}
$$

## 3. Stage 5　Transitions within an evaluation (→[7])

**Update rule $\mathsf{Update}$ :**

Increments are written with the same backward differences as P5 of Part 2 (the event at update number $n$ advances the state from $n-1$ to $n$ ).

$$
q_n=\rho(a_n),\qquad \rho(0)=0,\qquad \rho\ge0
$$

$$
p_n=p_{n-1}+\Delta p_n,\qquad \lambda^{[e]}_n=\lambda^{[e]}_{n-1}+\Delta\lambda^{[e]}_n,\qquad 0\le\lambda^{[e]}_n\le1
$$

When a structural element is added at update number $n$ , the new element is added to the active elements $\mathsf{Active}_n$ , starting with its $\lambda$ at 0 and its declared thickness at the value measured on the Cause-Side at the time of addition (Part 2, 3.3). When a structural element is removed, that element is taken out of the active elements. No term that decreases $\lambda$ is placed (P6).

In domains that take time to return, such as cooling, $q_n=\rho(q_{n-1},a_n)$ , with the condition that " $q\to0$ if $a=0$ continues." Only $q$ is allowed to decay spontaneously (P6).

The increment of $R$ , $R_n-R_{n-1}$ , splits into the penetration term and the contraction term as in Proposition 6 of Part 2.

**Order of classification:** at each update number, before computing $R$ , judge in the following order.

1. If the input is unknown, invalid, or non-finite (including unknown target, unit, time, or provenance), the result is **CONFESSION** (AXIOMS.md §6, §10.6). $R$ is not computed.
2. If $\tau_n=0$ , the result is **OUT_OF_DESCRIPTION_DOMAIN** (AXIOMS.md §6, §10.7). $R$ is not computed.
3. Only otherwise ( $\tau_n>0$ , $\delta_n\ge0$ , finite), compute $R_n$ and update the latch and the target boundary state below.

In cases 1 and 2, the latch $\ell$ keeps its value and is not updated by $R$ (the latch is not released automatically). When the data are merely unobservable, `NOT_OBSERVABLE` and the reason are output, and there is no transition to CONFESSION (P2 of Part 2).

**Latch and target boundary state** (→[7]):

$$
\ell_n=\ell_{n-1}\ \lor\ \mathbf{1}\{R_n\ge R_{\mathrm{irrev}}\}
$$

The instantaneous classification $\mathrm{Class}(R)$ is the canonical interval classification (PERMIT / BOUNDARY_WARNING / HANDOFF_REQUIRED / IRREVERSIBLE_TRANSITION / RUPTURE_BOUNDARY). Place the order

$$
\text{PERMIT}<\text{BOUNDARY\_WARNING}<\text{HANDOFF\_REQUIRED}<\text{IRREVERSIBLE\_TRANSITION}<\text{RUPTURE\_BOUNDARY}
$$

on the target boundary states, and set

$$
\mathsf{State}_n=
\begin{cases}
\mathrm{Class}(R_n) & \ell_n=0\\[2pt]
\max\bigl(\mathrm{Class}(R_n),\ \text{IRREVERSIBLE\_TRANSITION}\bigr) & \ell_n=1
\end{cases}
$$

Even if $R$ falls after the latch, the state does not automatically return below IRREVERSIBLE_TRANSITION (AXIOMS.md §10.4).

## 4. Stage 6　Transitions between evaluations (end of the old path and a new evaluation) (→[10])

Evaluation $j$ ends at any of the following events.

- $\mathsf{State}_n=\text{RUPTURE\_BOUNDARY}$ (rupture or transition of the evaluation target as a whole; the rupture of a part does not end it)
- OUT_OF_DESCRIPTION_DOMAIN ( $\tau=0$ ; loss of all elements and so on). Since it is outside the description domain, $R$ cannot continue to be computed within that evaluation. Structural testimony through the surviving observation and recording paths continues (AXIOMS.md §11)
- A change of the evaluation declaration, including:
  - a change of the target, rupture mode, reference, or rules (including replacement of the evaluation target itself)
  - a case where the declared thickness changes with a new observation (redeclared as the next evaluation snapshot; FORMULA.md §6, AXIOMS.md §14)
  - straightening (P6)
  - an addition that cannot be represented by the declared composition rule $\mathrm{Comp}_\tau$
  - a removal when the composition rule does not satisfy condition 2 (Part 2, 3.3)

The addition of a structural element does not end the evaluation as long as it can be represented by the composition rule (Part 2, 3.3). CONFESSION is a stop signal for the unknown and does not end the evaluation. Until the unknown is resolved, $R$ is not computed and the target boundary state is not advanced.

Operations at the end:

$$
\mathsf{Archive}\leftarrow\mathsf{Archive}\oplus\bigl(\mathsf{Decl}_j,\ \mathsf{History}^{(j)},\ Z^{(j)}_{\mathrm{final}}\bigr)
$$

$$
\mathsf{Decl}_j\ \longrightarrow\ \mathsf{Decl}_{j+1},\qquad j\leftarrow j+1
$$

- The records of the old evaluation are archived and not rewritten. What is carried into the new evaluation is not the summary but **$\tau_0^{(j+1)}$ determined by a new Cause-Side measurement**.
- If the latch caught in evaluation $j$ , that record is kept in $\mathsf{Archive}$ , and $\mathsf{Decl}_{j+1}$ also states that "the latch caught in the previous evaluation." No claim is made that the $R$ of evaluation $j$ and the $R$ of evaluation $j+1$ can be compared (comparability in P0 of Part 2).
- When restoration to the initial structure is claimed after reaching rupture or phase transition, both comparability (same target, same unit, same measurement rules) and $\tau_{\mathrm{restored}}<\tau_0^{(j)}$ are established, as in AXIOMS.md §8. $\tau_{\mathrm{restored}}$ here is the absorption thickness of existing elements, excluding added elements. Even if the declared thickness of the whole, including added elements, exceeds $\tau_0^{(j)}$ , that is not restoration (Part 2, 3.3).
- Redeclaring the reference state is permitted only here (P7, AXIOMS.md §4). When the reference is reset to the position of the residual deviation, $\tau_0^{(j+1)}\le\tau_n^{(j)}-p_n^{(j)}$ , unless a structural element has been added or the thickness has been measured anew by a new Cause-Side measurement. This is this document's safe-side condition for resetting the reference, derived from Proposition 1(b) (agreement of the rupture point), and not a general rule of the canon. If the reference is not reset, $p_n^{(j)}$ appears as $p_0$ in the observations of the new evaluation even without carrying over a summary (Proposition 0). The declared thickness of the new evaluation is determined by a new Cause-Side measurement (the next evaluation snapshot; FORMULA.md §6, AXIOMS.md §14). Even if its value comes out larger than $\tau_n^{(j)}$ of the old evaluation, it is not an increase within an evaluation, and no claim is made that the $R$ of the old and new evaluations can be compared.
- The evaluation number $j$ and the evaluation archive $\mathsf{Archive}$ do not decrease. The structure does not return to the same state and keeps advancing. Whether and how the sequence of evaluations is mapped to structural continuity $\omega$ is declared per evaluation as an optional element of the evaluation declaration (P0 of Part 2). No general rule for the mapping is defined.

**Correspondence with the escapement** (`examples/06_Escapement_Principle_JP.html`, `examples/26_escapement_contactpoint_JP.html`): in the evaluation for each tooth, when $\delta$ reaches $\tau$ the escapement jumps, the overshoot $\delta-\tau$ is not carried to the next tooth, and the next tooth is counted from $\delta=0$ (in a mechanical escapement, the overshooting energy dissipates as heat). This document reads each tooth as one evaluation, the jump as the transition between evaluations of Stage 6, and the overshoot as "a quantity not carried into the new evaluation" (though kept in the archive). The number of jumps corresponds to $j$ .

**Relation to existing demos:** `examples/14_powergrid_transition_JP.html` and `examples/15_or_icu_continuum_JP.html` fix RUPTURE_BOUNDARY, then start an "independent new Cause-Side evaluation" and archive the old history. They are existing implementations of Stage 6.

## 5. Stage 7　Links with hierarchies and other structures (→[9])

When this structure has substructures $i$ (finitely many), or is influenced by another structure $i$ , the **observed physical state** of the other enters this structure as an observation event.

$$
\mathrm{Ev}^{(\mathrm{self})}_{n}=\bigl(\text{physical state observed in structure }i,\dots\bigr),\qquad
\mathsf{Alloc}^{(\mathrm{self})}\bigl(\mathrm{Ev}^{(\mathrm{self})}_n\bigr)=\bigl(a^{(\mathrm{self})}_n,\ \Delta p^{(\mathrm{self})}_n,\ \Delta\lambda^{(\mathrm{self})}_n,\ \mathrm{ctx}^{(\mathrm{self})}_n\bigr)
$$

The rupture of a part (an observed rupture event: one spring broke) is a special case of this event. The part's evaluation output $R^{(i)}_n\ge1$ itself is not put into the target state of this structure. $R^{(i)}$ (the evaluation output of another structure) can be used in this structure for the following: records in audit and structural testimony, safe-side gauge inputs under P9(iv) (lowering thresholds, narrowing gate widths), and pre-fixed physical-control commands (AXIOMS.md §14). It is not put into the target state of this structure. Part and whole, and this structure and another structure, are **separate evaluations with separate declarations**, linked in the formulas by observed physical events.

The conditions under which a link does not constitute reverse derivation are derived from P9 as follows. They are not independent rules but consequences of P9.

| Condition | Content | Grounds |
|---|---|---|
| LC-1 No self-adjustment | the evaluation outputs of this structure ( $R$ , its averages and aggregates, $\mathsf{State}$ ) are not returned to the gauge of this structure (side-specific effective gate widths, thresholds, reference, projection); the same applies when returning via another structure | P9(ii) (AXIOMS.md §14) |
| LC-2 Direction | the observed physical state of the other enters this structure only as an event through $\mathsf{Alloc}^{(\mathrm{self})}$ : as an action $a$ (for example, the load increases because a neighboring spring broke), or as $\Delta p\ge0$ , $\Delta\lambda\ge0$ . It does not enter in the direction of decreasing $p$ or $\lambda$ . The evaluation outputs of the other do not enter the target state of this structure. They enter the gauge of this structure only at thresholds and effective gate widths, and only in the safe-side direction of narrowing gate widths or lowering thresholds | P9(iii)(iv), P6 |
| LC-3 No cycles | when quantities of the other are used in the same step, an order of computation that forms no cycle is declared; mutual links are represented between target states, not between gauges | P9(iv)(v) |
| LC-4 Fixed in advance | the existence of links, conversion rules, and thresholds are fixed before evaluation as elements of $\mathsf{Decl}^{(\mathrm{self})}$ , and link events are recorded in $\mathsf{History}$ | P9(vi) |

Relation to existing demos:

- `examples/12_agri_mol_antagonism_JP.html` (shrinks $\tau_K$ when $R_{\mathrm{Mg}}\ge0.7$ ) is an edge from another structure's evaluation output into this structure's gauge in the narrowing direction and satisfies LC-1 and LC-2. Computing Mg first within the same frame forms no cycle, so declaring that order also satisfies LC-3. However, since $\tau_K$ returns when $R_{\mathrm{Mg}}$ falls, it should be declared as a link of side-specific effective gate widths rather than of the effective thickness $\tau_n$ .
- `examples/24_vehicle_mandatory_boundary_JP.html` (widens $\tau_{\mathrm{upper}}$ by its own $R_{\mathrm{short}}$ ) falls under LC-1 (self-adjustment of the gauge) even though it uses the value of the previous frame, and since it widens, it also does not meet LC-2.
- `examples/07_HAN_gate_live_JP.html` builds the dynamic change of $\tau$ from the EMA of Cause-Side deviation rather than from $R$ , and does not fall under LC-1. The comment in that demo, "changing $\tau$ from the result value disables the causal diode," is an earlier example of the same idea as P9(ii) (though the multiplication $R=r_{\mathrm{raw}}\times\tau$ in that demo remains a separate issue).

## 6. Proposition 5　Sufficiency of the decision summary (→[11])

The **decision-sufficient state** $Z_n$ is taken to be not a positional tuple but a record with the following named fields (dictionary "Decision-Sufficient State").

- residual deviation $p_n$
- active elements $\mathsf{Active}_n$ , and for each element $e\in\mathsf{Active}_n$ , its declared thickness $\tau^{[e]}_0$ and degradation fraction $\lambda^{[e]}_n$
- irreversible latch $\ell_n$

The fields of $Z_n$ other than the latch ( $p_n$ , the active elements, and each element's declared thickness and degradation fraction) are the physical state, written $\mathsf{Phys}_n$ . Suppose the update rule has the following form (backward differences; the event at update number $n$ advances the state from $n-1$ to $n$ ; $e\in\mathsf{Active}_{n-1}$ ).

$$
q_n=\rho(a_n),\quad
\Delta p_n=g_p(\mathsf{Phys}_{n-1},a_n),\quad
\Delta\lambda^{[e]}_n=g^{[e]}_\lambda(\mathsf{Phys}_{n-1},a_n)
$$

Since the update rule is a physical law, it does not take the latch $\ell$ (an evaluation state) or the evaluation outputs $R$ and $\mathsf{State}$ as inputs (P9 of Part 2). $\ell_n$ is included in $Z_n$ in order to determine the next target boundary state.

The event $\mathrm{Ev}_n$ consists of the action $a_n$ and additions (including the declared thickness measured at the time of addition) and removals of structural elements.

**Proposition 5:** under the same evaluation declaration $\mathsf{Decl}$ (the same thresholds, the same composition rule, the same rules), two histories whose $Z_n$ at step $n$ are the same follow the same classification (CONFESSION, OUT_OF_DESCRIPTION_DOMAIN, or the same $R$ ) and the same $\mathsf{State}$ from $n+1$ onward, provided that the subsequent sequences of events $\mathrm{Ev}_{n+1},\mathrm{Ev}_{n+2},\dots$ are the same. $R_n$ at step $n$ itself depends on $q_n$ and is therefore not determined by $Z_n$ alone (the claim concerns $n+1$ onward).

**Proof:** by induction on $n$ . If $Z_n$ and the event $\mathrm{Ev}_{n+1}$ are equal, the rules above give equal $q_{n+1}=\rho(a_{n+1})$ , $p_{n+1}=p_n+g_p(\mathsf{Phys}_n,a_{n+1})$ , and equal $\lambda^{[e]}_{n+1}$ for each element. Since the additions and removals are equal, $\mathsf{Active}_{n+1}$ is equal, and the declared thicknesses of added elements are also equal (as the same measured values). By the same composition rule, $\tau_{n+1}$ is equal, and $\delta_{n+1}=q_{n+1}+p_{n+1}$ is also equal. The order of classification in Stage 5 of Part 3 gives the same result for the same input, so the classifications are equal. If $R_{n+1}$ is determined, it is equal, and $\ell_{n+1}$ and $\mathsf{State}_{n+1}$ are also equal. Hence $Z_{n+1}$ is also equal. ∎

For a single element, the active elements are $\{0\}$ and the declared thickness $\tau_0$ is fixed by the evaluation declaration, so $Z_n$ reduces to $(p_n,\lambda_n,\ell_n)$ .

**Meaning:**

- For judgment, the long history $\mathsf{History}$ may be summarized into $Z_n$ .
- **Whether a summary is sufficient is determined by the form of the update rule.** For example, in a domain such as metal fatigue, where the progress of degradation changes with the number of cycles so far, the number of cycles must be added to $Z_n$ as a field (additional domain state). In a domain such as cooling, where $q_n=\rho(q_{n-1},a_n)$ (Stage 5), $q_n$ is added as a field. Which fields may be dropped is determined by the declared rules. With named fields, omissions in updating the summary when state is added can be checked by the presence or absence of fields.
- For structural testimony and audit, $\mathsf{History}$ itself is kept. **The decision summary $Z$ and the testimony record $\mathsf{History}$ have different roles.**

Reference: the idea of "identifying histories whose subsequent behavior is the same" has a structure similar to the Myhill–Nerode equivalence of automata theory. However, the proof above does not depend on that theory and is closed within the premises of this document.

---

# SECTION II — 日本語（原文）

## 0. 本書の位置付けと読み方

本書は、正典の定義を作らず、変えない。定義・分類・優先順位は `theory/AXIOMS.md`（§16）に従う。本書と正典（`theory/AXIOMS.md`、`theory/axioms.json`、`FORMULA.md` ほか）が衝突した場合は正典が優先し、本書を修正する。

本書が用いる記号のうち、正典に定義があるものは正典の定義による。記号表（第2部1）の「定義箇所」欄に正典の節を記した記号は、その節の定義による。

例に出てくる数値はすべて説明用であり、実在の部材・設備の値ではない。外部理論への言及は類似の指摘であり、導出の根拠ではない。各証明は本書の前提だけで閉じている。検討の経緯は `note/正典考慮課題/` に記録がある。

本書は三部から成る。

- **第1部（高校3年生向け）**：ばねを使い、記号をほとんど使わずに全体像を説明する。細部を追えなくても、「何の話か」がつかめればよい。
- **第2部（一次式の成立）**：一次式に至るまで（段1〜段4）を、変数・式・証明で書く。第1部の言葉がどの記号に対応するかを示す。
- **第3部（一次式の後段）**：一次式の後の遷移（段5〜段7）を書く。第3部は正典化の判断前であり、正典の定義ではない。

第1部の各節には番号【1】〜【11】を振り、第2部・第3部で「→【3】」のように対応を示す。【1】〜【6】と【8】は第2部に、【11】は第3部に、【7】は第2部（P6のラッチ）と第3部（段5）の両方に、【10】は第2部（P6・3.3の構造要素の付加）と第3部（段6）の両方に、【9】は第2部（P9）と第3部（段7）の両方に対応する。

---

# 第1部　高校3年生への説明

## 【1】まず「何を見るか」を約束する

ばねを引っ張る実験を考える。

計算を始める前に、次を先に決めておく。

- どのばねを見るのか（対象）
- 何が起きたら「壊れた」とするのか（破断）
- 伸びを何で測るのか（単位は mm）
- どこを「伸び0」とするのか（基準＝買ってきたときの自然長。**この目盛りは後で動かさない**）

これを決めずに計算すると、同じ数字でも人によって意味が変わってしまう。
NRA-IDEの一次式は「好きな二つの数を割る式」ではない。**この約束が先にあって初めて使える式**である。

## 【2】「どこまで来たか」を割合で見る

このばねは、自然長から **30 mm** 伸ばすと切れるとする。
この「壊れるまでに受け止められる幅」30 mm を **厚み（τ）** と呼ぶ。

いま 12 mm 伸ばしているなら、壊れるまでの道のりのうち

$$
\frac{12}{30}=0.4
$$

つまり **4割** まで来ている。
この「基準から今の位置までの伸び」を **ズレ（δ）**、割合 0.4 を **R** と呼ぶ。R が 1 になったら破断である。

- R = 0.4 → 道のりの4割
- 残りの幅 30 − 12 = 18 mm → これが「余白」

厚みは「残り」ではなく「基準から破断までの全体の幅」である。残りは別に「余白」と呼ぶ。

## 【3】戻るズレと、戻らないズレ

物理で習うとおり、ばねには **弾性限界** がある。このばねの弾性限界を 12 mm とする。

- **8 mm 引いて離す** → 元の長さに戻る。これが **可逆**（戻るズレ）。
- **15 mm 引いて離す** → 弾性限界を 3 mm 越えたので、離しても **3 mm 伸びたまま** になる。これが **不可逆**（戻らないズレ）。コイルの間に隙間ができる。

15 mm 引いている最中の伸びは、「離せば戻る 12 mm」と「もう戻らない 3 mm」に分けられる。一つの出来事の中に、戻る部分と戻らない部分が **同時に** 入っている。

## 【4】戻らないものは2種類ある

弾性限界を越えたばねには、戻らない変化が二種類起きている。

1. **伸びっぱなし**：自然長が 3 mm 長くなった（位置がずれたまま）。
2. **弱くなった**：金属の内部に目に見えない傷ができて、切れるまでの幅が 30 mm から **27 mm** に減った。

1は「ズレが残った」、2は「器そのものが小さくなった」。**別の現象なので、別々に数える。**
同じ変化を両方に数えると、実際より悪く見積もってしまう（二重に数える）。どの観測をどちらに数えるかは、【1】の約束の中で決めておく。

## 【5】目盛りは測るだけで過去を含む。だから付け直してはいけない

15 mm 引いて離した後のばねを、**最初の自然長の目盛りのまま**測ると、伸びは 3 mm と読める。
何も計算しなくても、**今の目盛りの読みそのものに、過去に伸びっぱなしになった 3 mm が入っている**。
「ズレは瞬間の値ではなく、履歴を伴う」というのは、特別な積算をするという意味ではなく、**目盛りを動かさずに測れば、今の値に過去が残って見える**という意味である。

ところが、今の長さを新しい「伸び0」に付け直すと、

- 伸び 0、R = 0 → **「完全に元通り」に見える**

しかし本当は、

- 残った伸び 3 mm、厚み 27 mm → R = 3 ÷ 27 ≒ 0.11

である。目盛りを付け直すと、過去の出来事が見えなくなる。
だから **基準（伸び0の位置）は最初に決めたまま動かさない**。第2部で、動かさない方が常に安全側（R が大きく出る）になることを示す。

## 【6】同じ見た目でも、同じばねではない

新品のばねと、一度 15 mm 引いたばねを、どちらも同じ位置まで 15 mm 引く。

| | 伸び | 厚み | R |
|---|---|---|---|
| 新品 | 15 mm | 30 mm | 0.50 |
| 一度引いたばね | 15 mm | 27 mm | 約 0.56 |

見た目の伸びは同じ 15 mm なのに、R が違う。違いを生んでいるのは **過去に何があったか（履歴）** である。

ここから、この理論で一番大事な文が出てくる。

> **値が戻っても、構造は戻っていない。**

離せば伸びの一部は戻る（値の復帰）。しかし、伸びっぱなしの 3 mm、減った厚み、「15 mm 引かれた」という出来事の記録は消えない（構造は復元していない）。

## 【7】一度越えたら、自動では戻らない線がある（→第2部P6、第3部段5）

R が決められた値（不可逆遷移開始点）を一度でも越えたら、その後 R が下がっても「不可逆に入った」という記録を消さない。
これを **ラッチ**（掛け金）と呼ぶ。一度かかると、自動では外れない。

## 【8】「押し込まれる」と「器が削られる」が同時に起きると一番危ない

8 mm 引いていたばねを、15 mm まで引き伸ばしたとする。このとき二つのことが同時に起きる。

- 伸びが 8 mm → 15 mm に増えた（押し込み）
- 弾性限界を越えたので、厚みが 30 mm → 27 mm に減った（器の削れ）

R は 8/30 ≒ 0.27 から 15/27 ≒ 0.56 へ上がる。上がった 0.29 のうち、

- 約 0.26 は「伸びが増えた」せい
- 約 0.03 は「器が小さくなった」せい

である。R は分子が増えても分母が減っても上がるので、**両方が同時に起きる出来事は、R を二方向から押し上げる**。
NRA-IDEの「二重ゆらぎ」は、まさにこの「ズレが増えて、同時に厚みが減る」瞬間を見張る式である。

## 【9】部分が壊れても、全体が壊れたとは限らない（→第2部P9、第3部段7）

ばね10本で支える台を考える。そのうち1本が切れた。

- その1本にとっては破断（R = 1）
- 台全体にとっては、まだ破断ではない

しかし残り9本の負担は増え、台全体の厚みは減る。
つまり **下の階層の破断は、上の階層にとっては「一つの出来事」として入ってくる**。部分の破断を全体の破断と同じにしてもいけないし、無視してもいけない。

隣のばねの状態が、こちらのばねに影響する場合も同じである。隣の状態は「出来事」としてこちらに届く。

ここで区別しておくことがある。**ばねそのもの**と、ばねを測る**物差し**（どこを伸び0とするか、どこから危険とみなすか）は別物である。

- ばねそのものが、強く引かれるほど早く傷むのは、ばねの物理として自然である。
- しかし、**自分の R を見て、自分を測る物差しを書き換えてはいけない**。R が高いときに危険線を遠ざければ接近が隠れ、近づければ接近が大げさになる。どちらの場合も、R はばねの状態ではなく、物差しの都合を映すようになる。

これが「逆導出をしない」ということの中身である。正典では、この禁止を逆導出B（計器の自己調整）と呼ぶ。

## 【10】伸びたばねは戻らない。強くするには足す。切れたら数え直す（→第2部3.3、第3部段6）

伸びっぱなしになったばねは、元には戻らない。強くしたいときは、傷んだばねを「元に戻す」のではなく、**新しいものを足す**。

- 例：隣にもう1本ばねを並べる。太いばねを添える。
- 足したばねには、足したばね自身の厚みがある。その厚みは、足した時点で測って決める。
- 古いばねの伸びっぱなしの 3 mm と、30 mm から 27 mm への弱りは、足しても消えずに残る。
- 全体の厚みは、古いばねと足したばねを合わせた幅になる。どう合わせるか（並べれば足し算、など）は、【1】の約束の中で先に決めておく。
- 足しても計算は続き、足したことは記録に残る。いつ足してもよい（計算を始めてすぐでもよい）。
- 逆に、壊れていないばねを外すこともある。これは「壊れた」ではなく「外した」と記録する。外したばねを戻すときは、もう一度「足した」として、その時点で測り直す。

同じ計算を続けずに数え直すのは、次の場合である。

- ばねが切れたとき（R = 1）。
- 約束そのものを変えるとき。例えば、伸びたばねを力ずくで元の長さへ引き戻した（矯正した）とき。新しく測ったら、厚みが約束した値と違っていたとき。

数え直すときは、

- 古いばねの記録は、全部保管して残す（捨てない、書き換えない）。「戻らない線を一度越えた」という記録（【7】）も、新しい約束に書き込む。
- **新しい約束**（【1】）を結び直して数え始める。前の計算の R と、新しい計算の R は比べない。

時計の中の「脱進機」の歯車は、これを規則正しく繰り返す仕組みである。一歯分たまると一つ進み、はみ出した端数は次の歯へ持ち越さずに、次の歯で新しく数え始める（機械の脱進機では、はみ出したエネルギーは熱として散る）。歯車は進むだけで、同じ位置の同じ状態には戻らない。

## 【11】記録は全部残し、判断は要約で足りる（→第3部）

「いつ、何mm引いたか」を全部記録すると、とても長くなる。
でも次に何が起きるかを判断するには、

- 伸びっぱなしの量（3 mm）
- どれだけ弱くなったか（30 → 27 mm）
- ラッチがかかっているか

の3つを知っていれば足りる（要素が一つの場合。一般の場合は第3部の命題5で、条件つきで証明する）。

ただし、**説明や監査のためには全部の記録を残す**。「判断に必要な要約」と「証言に必要な記録」は役割が違う。式は約分で短くするのではなく、**要約で短くする**。消してよいのは、消しても次の判断が変わらないものだけである。

---

# 第2部　一次式の成立

## 1. 記号表

記号の名前・固定名・型・出所・使ってよい先・混同しやすい点は、辞書 `dictionary/NRA-IDE_Dictionary_JP.md` （英語版 `dictionary/NRA-IDE_Dictionary_EN.md`。非規範）で引ける。本書は、字体・大小・書体の違いだけで別の意味の記号を区別しない（辞書0.5、FORMULA.md §7）。正典の予約記号（FORMULA.md §7： $R,S,M_R,M_\tau,\delta,\tau,\omega,C,\mathrm{entropy}$ ）、AXIOMS.md §1の記号（ $\epsilon$ 、 $\emptyset$ ほか）、AXIOMS.md §4.5の補助構造量（ $\omega$ 、 $\mathrm{Phase}$ 、 $C$ 、 $W$ 、 $\mathrm{entropy}$ ）は、正典の意味でだけ使う。

| 記号 | 名称 | 意味 | 定義箇所 | 第1部 |
|---|---|---|---|---|
| $\mathsf{Decl}$ | 評価宣言 | 計算開始前に固定する約束の組 | FORMULA.md §0.5.1 | 【1】 |
| $n$ | 構造更新番号 | 事象の順序（時刻ではない） | FORMULA.md §0.5.2 | — |
| $o_n$ | 観測値 | Cause-Sideの観測（多変数可）。FORMULA.md §5の計算状態 $x$ とは別の記号 | FORMULA.md §0.5.2 | — |
| $\mathrm{Ev}_n$ | 観測事象 | $n$番目に記録された出来事 | FORMULA.md §0.5.2 | — |
| $\sigma$ | 射影規則 | 観測から蓄積ズレへの変換 | FORMULA.md §0.5.2 | 【5】 |
| $\mathsf{Alloc}$ | 分解規則 | 観測された変化の計上先を決める規則 | FORMULA.md §0.5.3 | 【4】 |
| $a_n$ | 作用 | その時点で構造に加わっている作用 | FORMULA.md §0.5.3 | 引く力 |
| $C_n$ | 制約 | 外部から加わる負荷・拘束・環境条件の時点の値（観測 $o_n$ の成分）。計上先ではない | AXIOMS.md §4.5、FORMULA.md §0.5.3 | — |
| $q_n$ | 可逆成分 | 作用を除けば0へ戻るズレ | AXIOMS.md §4（語）、FORMULA.md §0.5.3（記号） | 【3】 |
| $p_n$ | 不可逆成分（残留ズレ） | 作用を除いても残るズレ | AXIOMS.md §4（語）、FORMULA.md §0.5.3（記号） | 【4】1 |
| $\lambda_n$ | 劣化度（要素が一つの場合） | 厚みが失われた割合、 $0\le\lambda_n\le1$ 。要素が複数のときは要素ごとの $\lambda^{[e]}_n$ を使う | FORMULA.md §0.5.4 | 【4】2 |
| $\tau_0$ | 宣言厚み | 評価開始時の構造全体の吸収厚み。要素が複数なら $\tau_0=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_0)_{e\in\mathsf{Active}_0}\bigr)$ | FORMULA.md §0.5.1・§0.5.4。AXIOMS.md §7・§8の $\tau_0$ と整合 | 30 mm |
| $e$ | 要素番号 | 構造要素の番号。 $e=0$ は宣言時の構造、 $e\ge1$ は付加した要素 | FORMULA.md §0.5.4 | 【10】 |
| $n_e$ | 付加時点 | 要素 $e$ が加わった更新番号（ $n_0=0$ ） | 本書 | 【10】 |
| $\mathsf{Active}_n$ | 構成 | 時点 $n$ に評価対象に含まれている要素の集合（付加され、まだ除去されていない要素） | FORMULA.md §0.5.4 | 【10】 |
| $q^{\mathrm{temp}}_n$ | 一時的な可逆成分 | 作用や条件で一時的に狭まる受け止め幅を、ズレの側に数えた量。可逆成分 $q_n$ の一部 | FORMULA.md §0.5.3 | — |
| $\tau^{[e]}_0$、 $\lambda^{[e]}_n$ | 要素の宣言厚み・劣化度 | 要素 $e$ 自身の宣言厚みと劣化度（要素が一つなら $\tau^{[0]}_0=\tau_0$ 、 $\lambda^{[0]}_n=\lambda_n$ ） | FORMULA.md §0.5.4 | 【10】 |
| $\mathrm{Comp}_\tau$ | 合成規則 | 要素の厚みから全体の実効厚みを定める規則 | FORMULA.md §0.5.4（AXIOMS.md §7「構造要素の付加」を記号化） | 【10】 |
| $\delta_n$ | 蓄積ズレ | $q_n+p_n$ | AXIOMS.md §4、FORMULA.md §1・§0.5.3 | 【2】【5】 |
| $\tau_n$ | 実効厚み | 要素が一つなら $(1-\lambda_n)\tau_0$ 。一般には段3の $\mathrm{Comp}_\tau$ による | FORMULA.md §1（ $\tau$ ）、§0.5.4（層の区別） | 【2】【4】 |
| $\tau_{\mathrm{upper}}(n)$、 $\tau_{\mathrm{lower}}(n)$ | 側別有効ゲート幅 | 二次式の側別評価にだけ使う幅 | FORMULA.md §4.4 | — |
| $R_n$ | 境界接近比 | $\delta_n/\tau_n$ | FORMULA.md §1 | 【2】 |
| $M_{\tau,n}$ | 残存吸収余白 | $\tau_n-\delta_n$ | FORMULA.md §2 | 【2】 |
| $\ell_n$ | 不可逆ラッチ | 0 または 1 | AXIOMS.md §10.4（`irreversible_latched`） | 【7】 |
| $\mathsf{History}_n$ | 経路履歴 | $\mathrm{Ev}_1,\dots,\mathrm{Ev}_n$ の記録列（評価開始時は空） | 本書 | 【6】【11】 |
| $\mathsf{Phys}^{(\mathrm{self})}_n$ | 対象状態 | 自構造の物理状態 $(q_n,p_n,(\lambda^{[e]}_n)_{e\in\mathsf{Active}_n})$ 。評価状態（ $\ell_n$ ）と経路履歴（ $\mathsf{History}_n$ ）は含まない（命題2）。他構造 $i$ の物理状態は $\mathsf{Phys}^{(i)}_n$ | 本書（AXIOMS.md §14の区分を記号化） | 【9】 |
| $\mathsf{Gauge}^{(\mathrm{self})}$ | 計器 | 自構造を測る基準・変換規則・閾値・有効ゲート幅 | 本書（同上） | 【9】 |
| $\mathsf{Out}^{(\mathrm{self})}_n$ | 評価出力 | $R_n$、側別比、 $\ell_n$、正規状態と、その集約 | AXIOMS.md §14（同節は $R$・正規状態・不可逆ラッチを挙げる。側別比を含めるのは本書の読み） | 【9】 |

第3部だけで使う記号（ $j$ 、 $\mathsf{Archive}$ 、 $Z_n$ 、 $\mathsf{State}_n$ 、 $\mathsf{Update}$ 、 $\rho$ 、 $g_p$ 、 $g^{[e]}_\lambda$ 、 $\mathrm{EvalGraph}^{(j)}$ ）は第3部に示す。

---

## 2. 前提 P0〜P9

各前提について、正典との対応を示す。

### P0　評価宣言（→【1】）

計算開始（ $n=0$ ）の前に、評価宣言 $\mathsf{Decl}$ を固定する。 $\mathsf{Decl}$ は評価の結果によって書き換えない。

| 必須要素 | 内容 | 正典との対応 |
|---|---|---|
| 評価対象と破断様式 | 評価する構造と、完全破断とみなす様式・経路 | FORMULA.md §0 |
| 単位 | $\delta$ と $\tau$ に共通の単位 $u$ | FORMULA.md §1 |
| 観測の種類と出所 | 使用するCause-Side観測と、その出所・時点・単位・不確かさ | FORMULA.md §6、AXIOMS.md §14・§15.1 |
| 閾値 | $R_{\mathrm{warn}}$、 $R_{\mathrm{handoff}}$、 $R_{\mathrm{irrev}}$ | AXIOMS.md §9 |
| 欠測・観測不能の処理 | 観測不能、欠測、計算不能のときの扱い。観測不能は`NOT_OBSERVABLE`と欠損理由で示し、0・安定・安全・回復として補完しない | AXIOMS.md §10.2・§11.2・§15.1 |
| 基準状態 | 蓄積ズレを測る原点 | AXIOMS.md §4 |
| 射影規則 $\sigma$ | 段1 | 本書 |
| 分解規則 $\mathsf{Alloc}$ | P5 | 本書 |
| 宣言厚み $\tau_0$ | 段3 | 本書 |
| 合成規則 $\mathrm{Comp}_\tau$ | 構造要素を付加・除去したときに、要素の厚みから全体の実効厚みを定める規則（段3） | AXIOMS.md §7（構造要素の付加） |

合成規則は、付加がまだない評価でも宣言する。付加はいつ起きてもよい（ $n=0$ の直後でもよい）ので、付加が起きてから規則を決めると、規則を結果に合わせて決める余地が生まれるからである。

任意要素として、評価の系列と構造連続性 $\omega$ との対応づけの有無と方法を宣言できる。宣言しない場合は、対応づけなしとする。対応づけの一般規則は定めない。対応づけに使う $\omega$ は、AXIOMS.md §4.5のとおりCause-Side観測または事前固定の変換規則から得る（P8）。

任意要素として、外部条件の同定（何を制約 $C$ とするか：種類・出所・単位・換算規則）を宣言できる。 $C$ を計器へ入れる場合は、評価前に固定した関数として宣言する。

要素は省かない。ある成分が存在しない領域では、その成分が0であることを宣言する（例： $p\equiv0$ ）。

**一次式は常に宣言に紐づく**。

$$
R_{\mathsf{Decl}}=\frac{\delta_{\mathsf{Decl}}}{\tau_{\mathsf{Decl}}}
$$

異なる宣言の $R$ は、比較可能性を立証しない限り比較・移植しない。

$$
\mathsf{Decl}_A\neq\mathsf{Decl}_B
\;\Rightarrow\;
R_{\mathsf{Decl}_A}\text{ と }R_{\mathsf{Decl}_B}\text{ は、比較可能性の立証なしには比較しない}
$$

比較可能性の**必要条件**は、同一対象・同一単位・同一のCause-Side測定規則で $\delta$ と $\tau$ を得ていることである（AXIOMS.md §8が $\tau_{\mathrm{restored}}$ と $\tau_0$ の比較に求める条件と同じ）。ここでの「同一の測定規則」は、 $R$ の意味を変える宣言の要素がすべて同じであることを含む。すなわち、基準状態、破断様式・破断経路、射影規則 $\sigma$ 、分解規則 $\mathsf{Alloc}$ 、合成規則 $\mathrm{Comp}_\tau$ 、評価スナップショットの意味である。これらの条件は、比較してよいことを保証する十分条件ではない。比較する場合は、条件を満たすことを示し、満たさない要素があれば比較しない。これは、FORMULA.md §0「評価対象は計算開始前に一意に宣言する」と、AXIOMS.md §15.1の「類似性だけを根拠に $\delta$・$\tau$ を別領域へ移植しない」を、宣言単位で読んだものであり、新しい規則ではない。

### P1　ズレと破断境界（→【2】）

宣言した破断様式に沿って、基準状態から破断方向へ測ったズレを $\delta\ge0$ とする。 $\delta=0$ が基準状態、 $\delta=\tau_n$ が現時点での破断位置である。

$\tau$ は「残り」ではなく、**基準から破断までの総幅**である。残りは $M_\tau=\tau-\delta$ として別に定義する（FORMULA.md §2）。

### P2　観測事象（→【1】）

観測事象は数値一つではなく、記録単位である。

$$
\mathrm{Ev}_n=
(\text{対象},\ \text{値},\ \text{単位},\ \text{出所},\ \text{時点},\ \text{不確かさ},\ \text{順序}\ n,\ \text{観測経路})
$$

時点は取得時刻または版であり、順序 $n$ とは別に持つ（FORMULA.md §6）。

次の二つを区別する。

- **不明・不正な入力**：対象・単位・時点・出所のいずれかが不明な事象、値が不正または非有限な事象は、一次式へ入力せず、CONFESSIONとする（AXIOMS.md §6・§10.6）。類推で補完しない。
- **観測できないだけの場合**：観測チャネルから値が得られないことが分かっている場合は、`NOT_OBSERVABLE`と欠損理由を出力し、評価宣言の欠測処理に従う（AXIOMS.md §10.2・§11.1・§11.2）。観測不能だけを理由にCONFESSIONへ移行しない。

### P3　比較可能性

$$
[\delta]=[\tau]=u
$$

かつ、 $\delta_n$ と $\tau_n$ は同一の $\mathsf{Decl}$・同一の $n$ に属する。

### P4　定義域

$$
\delta_n\ge0,\qquad \tau_n>0,\qquad \delta_n,\tau_n\ \text{は有限}
$$

これはFORMULA.md §1の定義域そのものである。要素が一つの場合は $\lambda_n<1$ の範囲で、一般には合成規則の値が正の範囲で満たされることを、補題1で示す。

### P5　可逆・不可逆の分解（→【3】【4】）

分解規則 $\mathsf{Alloc}$ は、各事象を次の四つへ分ける。

$$
\mathsf{Alloc}(\mathrm{Ev}_n)=\bigl(a_n,\ \Delta p_n,\ \Delta\lambda_n,\ \mathrm{ctx}_n\bigr)
$$

- $a_n$：作用（可逆成分を生む）。構造が受け止められる幅を一時的に狭める条件の効果（ $q^{\mathrm{temp}}_n$ 、段3）もここに計上する。条件そのもの（制約 $C_n$ 、AXIOMS.md §4.5）は計上先ではない
- $\Delta p_n\ge0$：残留ズレの増分
- $\Delta\lambda_n\ge0$：劣化度の増分（構造要素が複数あるときは要素ごとの $\Delta\lambda^{[e]}_n\ge0$ ）
- $\mathrm{ctx}_n$：文脈・権限・出所

**増分の定義**：更新番号 $n$ の事象 $\mathrm{Ev}_n$ が、状態を $n-1$ から $n$ へ進める（ $n=1,2,\dots$ 。 $n=0$ は評価開始時）。増分は、FORMULA.md §4.7と同じ後退差分で書く。

$$
p_n=p_{n-1}+\Delta p_n,\qquad \lambda^{[e]}_n=\lambda^{[e]}_{n-1}+\Delta\lambda^{[e]}_n
$$

したがって $p_n=p_0+\sum_{m=1}^{n}\Delta p_m$ である（ $p_0$ は評価開始時の残留ズレ）。可逆成分 $q$ の時間変化の規則（第3部段5の更新規則 $\mathsf{Update}$ ）は、正典化の判断前なので本部の前提に含めない。

**射影との整合**：分解は射影の値を分けるものであり、

$$
q_n+p_n=\sigma(o_n)=\delta_n
$$

を満たす。可逆成分は $q_n=\sigma(o_n)-p_n$ として定まり、 $q_n\ge0$ より $0\le p_n\le\delta_n$ である。モデルで $q_n$ を与える場合も、この整合を満たさなければならない。満たさないことは、 $\sigma$ か $\mathsf{Alloc}$ の宣言が対象に合っていないことの証拠である。一時的な可逆成分 $q^{\mathrm{temp}}_n$ （一時的に狭まった受け止め幅。段3）は、 $\sigma$ が条件の観測（温度など）から換算して $\delta_n$ に含め、 $\mathsf{Alloc}$ が $q_n$ に計上する。

**一変化一計上**：観測された一つの物理的変化は、 $a_n$・$\Delta p_n$・$\Delta\lambda_n$ のうち**ちょうど一つ**に計上する。 $\mathrm{ctx}_n$ は計上先ではなく、計上に付随する情報である。どの観測をどれに計上するかは $\mathsf{Alloc}$ の中で事前に固定する（→【4】の二重計上防止）。一つの事象が複数の変化を含むことはある（【3】の15 mmの例）。その場合も、変化ごとに計上先は一つである。制約 $C_n$ は計上先にしない。 $C_n$ は観測 $o_n$ の成分であり、 $\sigma$ ・ $\mathsf{Alloc}$ ・物理法則・計器の関数など、評価前に固定した規則の引数としてだけ効く。その効果は、変化ごとに $a_n$ ・ $\Delta p_n$ ・ $\Delta\lambda_n$ のちょうど一つに計上する。同じ因子（温度など）が $C_n$ と $a_n$ の両方に現れることはあるが、 $C_n$ は計上先ではないので二重計上ではない。

構造要素の付加・除去そのものは、この三つの計上先に含めない。構成 $\mathsf{Active}_n$ の更新として扱い、事象として記録する（段3）。付加・除去に伴う別個の作用・残留ズレ・劣化には、各変化に一変化一計上を適用する。

### P6　不可逆成分の単調性（→【4】【7】【10】）

評価の中では、例外なく

$$
p_n\ge p_{n-1},\qquad \lambda^{[e]}_n\ge\lambda^{[e]}_{n-1}\quad(\text{各要素}\ e)
$$

とする。既存の要素の劣化と残留ズレは、どのような操作でも減らさない。吸収厚みが増えるのは、構造要素の付加（段3）による場合だけである。壊れていない要素を計画的に外す構造要素の除去（段3）は、厚みを減らすが劣化ではないので、 $\lambda$ に計上しない。伸び・曲がりを力で戻す矯正は、固定した基準から測った $\delta$ を下げるので、評価の中では扱わない。矯正した場合はその評価を終え、新しい評価として宣言し直す（第3部段6）。

不可逆ラッチは、評価中に自動では解除しない（AXIOMS.md §10.4）。

$$
\ell_n\ge\ell_{n-1}
$$

経路履歴は常に伸びる。

$$
\mathsf{History}_n=\mathsf{History}_{n-1}\oplus \mathrm{Ev}_n,\qquad \#\mathsf{History}_n=\#\mathsf{History}_{n-1}+1
$$

$\oplus$ は加算ではなく「記録列の末尾への接続」、 $\#$ は記録の個数である。

時間経過だけで減ってよいのは可逆成分 $q$ だけである。これはAXIOMS.md §7（τ非自然回復と、残留ズレの非自然回復）を、分解した成分ごとに書いたものである。AXIOMS.md §7は、残留ズレは評価中に減少せず、矯正を行った場合は評価を宣言し直すと定める。

### P7　基準不動（→【5】）

基準状態は $\mathsf{Decl}$ で固定し、評価中に付け直さない。残留ズレ $p_n$ は基準の移動ではなく、 $\delta$ の一部として保持する。基準の再宣言は評価と評価の間でのみ許す（第3部段6）。

正典との対応：AXIOMS.md §4。

### P8　権威

$q,p,\lambda,\tau_0$ およびそれらの増分は、Cause-Side観測または事前固定の変換規則からのみ得る。Effect-Side出力や可視化結果から逆算しない（AXIOMS.md §14、逆導出A）。評価で補助構造量（AXIOMS.md §4.5の $\omega$ 、 $\mathrm{Phase}$ 、 $C$ 、 $W$ 、 $\mathrm{entropy}$ ）を使う場合も同じであり、評価出力（ $R$ 、正規状態、不可逆ラッチ、その集約）から得てはならない（AXIOMS.md §4.5）。

P8は**入力元の種類**についての前提である。次のP9は、入力元がすべてCause-Sideであっても成り立たなければならない**計算経路の形**についての前提である。

### P9　対象状態・計器・評価出力の区分（→【9】）

**三つの区分**：評価に現れる量を、次の三つに分ける。

| 区分 | 記号 | 含まれるもの | 性質 |
|---|---|---|---|
| 対象状態 | $\mathsf{Phys}^{(\mathrm{self})}_n$ | $q_n,p_n,\lambda_n$（と、そこから決まる $\delta_n,\tau_n$ ） | 対象そのものの物理状態。対象の物理法則で動く |
| 計器 | $\mathsf{Gauge}^{(\mathrm{self})}$ | 基準状態、 $\sigma$、閾値、形状変換関数 $h_{\mathrm{upper}},h_{\mathrm{lower}}$、EMA係数、 $\tau_{\mathrm{upper}},\tau_{\mathrm{lower}}$ | 対象を測る物差しと、危険とみなす線 |
| 評価出力 | $\mathsf{Out}^{(\mathrm{self})}_n$ | $R_n,R_{\mathrm{upper}},R_{\mathrm{lower}},R_{\mathrm{dir}},\ell_n$、正規状態と、それらの移動平均・集約 | 計器で対象を読んだ結果 |

評価出力の位置はAXIOMS.md §14「評価出力の位置」による。

**逆導出**（AXIOMS.md §14「逆導出の定義」）：

$$
\text{逆導出}\iff
\underbrace{\exists\ \text{経路}\ (\text{Effect-Side出力})\leadsto\mathsf{Phys}^{(\mathrm{self})}\cup\mathsf{Gauge}^{(\mathrm{self})}\cup\mathsf{Out}^{(\mathrm{self})}}_{\text{(i) 逆導出A：権威の逆流}}
\ \lor\
\underbrace{\exists\ \text{経路}\ \mathsf{Out}^{(\mathrm{self})}_m\leadsto\mathsf{Gauge}^{(\mathrm{self})}\quad(\text{任意の段、他構造経由を含む})}_{\text{(ii) 逆導出B：計器の自己調整}}
$$

(ii)の理由：入力がすべてCause-Sideでも、評価の出力が自分の物差しや危険線を動かせば、計器が「自分の読みに合わせて自分を調整する」ことになる。 $R$ が上がるほど幅を広げれば接近は隠れ、 $R$ が上がるほど幅を狭めれば接近は誇張される。どちらの向きでも、 $R$ は対象の状態ではなく計器自身の履歴を映すようになる。したがって向きを問わず禁止する。前段の $R$ や $R$ の移動平均を使っても、他構造を経由して戻っても（ $R^{(\mathrm{self})}\to\mathsf{Gauge}^{(i)}\to R^{(i)}\to\mathsf{Gauge}^{(\mathrm{self})}$ ）同じである。

**他の評価対象の評価出力**（AXIOMS.md §14）：

$$
\text{(iv)}\quad \mathsf{Out}^{(i)}\to(\text{閾値}^{(\mathrm{self})},\ \tau^{(\mathrm{self})}_{\mathrm{upper}},\ \tau^{(\mathrm{self})}_{\mathrm{lower}})\ \text{の辺は、安全側（ゲート幅を狭める・閾値を下げる）に限り、}\mathsf{Out}^{(\mathrm{self})}\text{から構造}i\text{への経路がない場合に限る}
$$

(iv)が許すのは、計器のうち閾値と有効ゲート幅への辺だけである。基準状態や射影規則 $\sigma$ へ他構造の評価出力を入れる辺は、(iv)の対象ではない。この辺の有無と規則は、評価開始前に固定する（AXIOMS.md §14）。

(ii)と(iv)の違い：(ii)は自分の読みで自分の物差しを動かすので、向きを問わず禁止する。(iv)は他の構造の読みを受け取る辺であり、閉路がなければ自己調整にはならない。ただし広げる向きは、他の構造の状態を理由に自構造の接近を隠すことになるので、安全側に限る。

**判定の基準は記号の名前ではなく、経路の出所と書き換え先である**（AXIOMS.md §14）。そのために、出所の違うものには違う名前を使う。

- **物理法則の中の比**：対象状態の法則が、物理的な負荷の比に依存すること（例えば、疲労劣化が応力比で進むこと）は、対象の物理として正当である。この比は、物理法則の中で、Cause-Sideの $\delta$ と $\tau$ から直接計算する。書き方は $\Delta\lambda^{[e]}_n=g^{[e]}_\lambda(\delta_n,\tau_n,\dots)$ のように、Cause-Side由来の引数を直接示す。この比に $R$ という名前を付けない。
- **評価出力 $R$ **：保存された評価出力 $R$ （その移動平均・集約・状態区分を含む）を読み戻して、対象状態 $\mathsf{Phys}$ を更新してはならない。自構造の評価出力でも、他構造の評価出力でも同じである。対象状態はCause-Side観測または事前固定の変換規則からのみ得る（P8、AXIOMS.md §14）。
- **計器を書き換える規則**：計器 $\mathsf{Gauge}$ を書き換える規則は、 $R$ という名前を使わずに $\delta/\tau$ で書き直しても、評価と同じ比で計器を動かす経路であり、(ii)に当たる。

**許される辺と許されない辺の例**：

| 辺 | 判定 | 理由 |
|---|---|---|
| $\mathrm{EMA}(\delta_{\le n})\to\tau_{\mathrm{upper}},\tau_{\mathrm{lower}}$ | 許される | 計器への入力が対象の履歴 $\delta$ で、評価出力ではない（FORMULA.md §4.4） |
| $f(\delta)\to\Delta\lambda_n\to\tau_n$ | 許される | 対象の物理法則。厚みを減らす向きのみ（AXIOMS.md §7の $\tau$ 状態遷移式） |
| $g^{[e]}_\lambda(\delta_{n-1},\tau_{n-1},\dots)\to\lambda^{[e]}_n$ | 許される | 書き換え先が対象状態。物理法則の中で、Cause-Sideの $\delta$ ・ $\tau$ から負荷比を直接計算する（保存された $R$ を読み戻さない） |
| 構造 $i$ で観測された物理的事象（破断・荷重の移動など） $\to\mathsf{Alloc}^{(\mathrm{self})}\to a^{(\mathrm{self})},\Delta p^{(\mathrm{self})},\Delta\lambda^{(\mathrm{self})}$ | 許される | 他構造の物理状態を、Cause-Side観測の事象として受け取る（第3部段7） |
| $R^{(i)}_n\to\Delta\lambda^{(\mathrm{self})}$ など自構造の対象状態 | 許されない | $R^{(i)}$ は評価出力であり、Cause-Side観測ではない。 $\delta$ ・ $\tau$ と対象状態はCause-Side観測または事前固定の変換規則からのみ得る（AXIOMS.md §14） |
| $R^{(i)}_n\to\tau^{(\mathrm{self})}_{\mathrm{upper}}$（狭める向き） | 許される | (iv) 安全側で、閉路がない場合 |
| $R^{(\mathrm{self})}$ またはその平均 $\to\tau^{(\mathrm{self})}_{\mathrm{upper}},\ $ 閾値 | 許されない | (ii) 計器の自己調整。向きを問わない |
| $R^{(\mathrm{self})}\to\mathsf{Gauge}^{(i)}\to R^{(i)}\to\mathsf{Gauge}^{(\mathrm{self})}$ | 許されない | (ii) 他構造を経由した自己調整 |
| LLM自己評価 $\to\delta$ | 許されない | (i) 入力元の逆流 |
| $R\to\ell\to$ 正規状態 | 許される | 評価出力の中での計算。計器にも対象にも戻らない |

相互に影響し合う二つの構造は、互いの計器ではなく、互いの対象状態（濃度・変位・劣化度など）を通して連結すれば、(ii)に当たらずに表せる。

逆導出の語義の分類は `theory/SANDWICH_ARCH.md` §8.4 による。P9の残りの条件（(iii)(v)(vi)）は第3部に置く。

---

## 3. 導出の鎖（観測 → $\delta$・$\tau$ → $R$）

段1〜段3は一次式に至る前段、段4は一次式である。一次式の後の遷移（段5〜段7）は第3部に置く。

### 3.1 段1　射影：観測から蓄積ズレへ

$$
\delta_n=\sigma(o_n)\ \ge0
$$

$\sigma$ は、観測値を「基準状態から、宣言した破断方向へ測った距離」に移す規則である。多変数の観測はここで一つの量へまとめる。 $\sigma$ の具体形は、領域の支配方程式または実証された変換規則であり、FORMULA.md §0の言う「現場固有の物理式」がここに入る。

例（`examples/13_photosynthesis_layer5_JP.html`）：FvCBモデルで光合成速度を計算し、 $\delta=\max(0,\ \text{最大光合成速度}-\text{光合成速度})$ とする。デモ自身が「Layer 5 は $\delta$ を生成するだけ、 $R=\delta/\tau$ は変わらない」と書いており、射影と判定式の分離の既存例である。

### 3.2 段2　分解：蓄積ズレの二成分

$$
\boxed{\ \delta_n=q_n+p_n\ }
$$

- $q_n$：作用を除けば0へ戻る部分（可逆成分）
- $p_n$：作用を除いても残る部分（不可逆成分、残留ズレ）

**命題0（固定基準の観測は履歴を含む）**：P5・P7の下で、作用も一時的な条件もない除荷状態（ $a=0$ 、 $q=0$ ）での観測は $\delta=\sigma(o)=p_n$ を与える。したがって、瞬間に測った $\delta_n$ は、評価開始時の残留分 $p_0$ と、それ以後の全事象の残留分を合わせた $p_n=p_0+\sum_{m=1}^{n}\Delta p_m$ を含む。

**証明**：P5の射影との整合 $q_n+p_n=\sigma(o_n)$ に $q_n=0$ を入れると $\sigma(o_n)=p_n$ 。 $p_n$ の形はP5の増分の定義による。基準がP7により動かないので、 $\sigma$ は評価の間ずっと同じ原点から測る。∎

$p_0$ は、評価開始時点で基準状態からすでに残っているズレである。評価開始時の除荷状態に基準を置けば $p_0=0$ となる（第1部のばねでは、買ってきたときの自然長）。

これにより、AXIOMS.md §4の「 $\delta$ は単なる瞬間値ではない。履歴を伴う蓄積ズレ」と、瞬間観測型の実装は、**基準不動（P7）と $p$ の保持**という二条件の下で両立する。 $q$ と $p$ の分離は、除荷時観測、または $\mathsf{Alloc}$ で固定したモデルで行う。

既存資料に見られる $\delta$ の作り方は、次のように位置づく。

| 既存資料での $\delta$ | 例 | 本書での位置 |
|---|---|---|
| 最適値からの現在偏差 | examples 18, 20, 27〜30 | $\delta_n$ そのもの。基準不動かつ $p$ を捨てなければ正典と両立 |
| 積算され一方的に増える量 | 論文 v3、Axiom2系 | $q\equiv0$ の特別な場合 |
| 閾値からのはみ出し量 | examples 08〜11 | 基準状態を閾値へ置いた別の評価宣言 |
| 複数系統の不一致度 | examples 24 | $\sigma$ として不一致度を選んだ宣言 |
| 積算して跳躍時に0へ戻す量 | examples 06, 26（脱進機） | 評価間の遷移の周期的な例（第3部段6） |

### 3.3 段3　厚み：三層に分ける

$$
\boxed{\ \tau_n=(1-\lambda_n)\,\tau_0\ }
$$

これは要素が一つ（宣言時の構造だけ）の場合の形である。構造要素を付加・除去する一般の形は、下の「構造要素の付加と除去」で示す。宣言厚み $\tau_0$ は、正典（AXIOMS.md §7・§8）と同じく、評価開始時の構造全体の吸収厚みを表す。要素が複数あるときは、評価開始時の構成 $\mathsf{Active}_0$ について $\tau_0=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_0)_{e\in\mathsf{Active}_0}\bigr)$ であり、要素が一つなら $\tau_0=\tau^{[0]}_0$ である。

| 層 | 記号 | 性質 | 使う場所 |
|---|---|---|---|
| 宣言厚み | $\tau_0$ | 評価宣言で固定 | 各評価の出発点 |
| 実効厚み | $\tau_n$ | 構造要素の付加がない限り非増加 | 一次式 |
| 側別有効ゲート幅 | $\tau_{\mathrm{upper}}(n)$、 $\tau_{\mathrm{lower}}(n)$ | 増減してよい | 二次式（FORMULA.md §4.4）だけ |

側別有効ゲート幅は、FORMULA.md §4.4のとおり「基礎吸収厚み $\tau$ そのものの自然回復を意味しない」。

#### 構造要素の付加と除去（→【10】）

吸収厚みが増える経路は、評価対象へ新しい構造要素を加えること（**構造要素の付加**、略して付加）だけである。既存の要素の厚みが戻るのではない。逆に、壊れていない構造要素を計画的に外すことを**構造要素の除去**（略して除去）という。除去は劣化ではないので、劣化度 $\lambda$ には計上しない。

宣言時の構造を要素 $e=0$ とし、更新番号 $n_e$ に加わった要素を $e=1,2,\dots$ とする。各要素は自身の宣言厚みと劣化度を持つ。時点 $n$ に評価対象に含まれている要素（付加され、まだ除去されていない要素）の集合を**構成** $\mathsf{Active}_n$ とする。

$$
\tau^{[e]}_n=(1-\lambda^{[e]}_n)\,\tau^{[e]}_0\qquad(e\in\mathsf{Active}_n)
$$

$$
\boxed{\ \tau_n=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_n)_{e\in\mathsf{Active}_n}\bigr)\ }
$$

合成規則 $\mathrm{Comp}_\tau$ には次を課す。

1. 各引数について非減少である。
2. 評価の中で除去を認める場合、引数（要素）を一つ外しても値は増えない。この条件を満たさない形（直列の連結 $\mathrm{Comp}_\tau=\min_e\tau^{[e]}_n$ のように、弱い要素を外してつなぎ直すと全体が強くなる形）では、除去を評価の中で扱わず、評価宣言の変更（第3部段6）とする。
3. 値は有限かつ非負であり、単位は要素の厚みと同じ $u$ である。
4. 構成がただ一つの要素 $e$ だけのときは、どの $e$ についても $\mathrm{Comp}_\tau(\tau^{[e]}_n)=\tau^{[e]}_n$ である。宣言時の要素 $e=0$ だけなら、上の枠の式に戻る。
5. すべての要素の厚みが0のとき、および構成が空のとき、値は0である。
6. 付加した要素の宣言厚み $\tau^{[e]}_0$ は、加えた時点のCause-Side測定で定める。 $R$ などの評価出力から定めない（P8・P9）。
7. 付加と除去は、事象として経路履歴 $\mathsf{History}$ に記録する。

外した要素を後で戻す場合は、改めて付加として扱い、戻した時点のCause-Side測定で厚みを定める。外していた間に進んだ劣化も、その測定に含まれる。

**系（付加のない区間での非増加）**：付加がない区間（ $\mathsf{Active}_{n+1}\subseteq\mathsf{Active}_n$ ）では $\tau_{n+1}\le\tau_n$ 。

**証明**：P6より各要素の $\lambda^{[e]}$ は減らないので、各 $\tau^{[e]}$ は増えない。条件1より、残る要素について $\mathrm{Comp}_\tau$ の値は増えない。評価の中で除去が起きるのは条件2を満たす場合だけなので、除去した要素を外しても値は増えない。∎

したがって $\tau_n$ が増えるのは付加の時点だけであり、AXIOMS.md §7の「構造要素の付加のない閉じた運用区間において、 $\tau$ は時間とともに増加しない」と一致する。付加はいつ起きてもよい（評価の開始直後でもよい）。 $\mathrm{Comp}_\tau$ の具体形は領域ごとに異なり（例：並列に並べた要素なら和 $\mathrm{Comp}_\tau=\sum_e\tau^{[e]}_n$ ）、評価宣言で事前に固定する（P0）。

付加を行う主体は問わない。人が補強する場合も、生体が新しい組織を作って修復する場合も、付加として扱う。評価出力と付加の関係は、次の三つを区別する。

- $R$ を、事前に固定した補強操作（オートスケーラーの増設など）の引き金に使う：許される。評価出力は事前固定された物理制御の指令に使える（AXIOMS.md §14）。
- $R$ だけを根拠に、「付加が物理的に済んだ」「厚みが増えた」と認める：許されない。評価出力は対象状態の根拠にならない。
- 付加が済んだことと加わった厚みを、Cause-Sideで測り直す：必須である。

AIの実行系が自らの出力で自らに境界を加えたと主張する場合も、Cause-Side測定で示せない限り付加と認めない。

要素 $e$ が壊れた（ $\lambda^{[e]}=1$ ）場合、その要素の厚みは0になる。 $\mathrm{Comp}_\tau$ の値が正である限り、全体の評価は続く。評価の中の「小さな破断点」は、この形で表せる。評価が終わるのは、評価対象全体が $R\ge1$ に達した場合などである（第3部段6）。

**系（全要素の喪失）**：構成のすべての要素が壊れた場合、またはすべて除去された場合、条件5より $\tau_n=0$ であり、OUT_OF_DESCRIPTION_DOMAINとなる（補題1）。 $\mathrm{Comp}_\tau$ の形によっては、一部の要素の破断で $\tau_n=0$ になることもある（例：直列の連結 $\mathrm{Comp}_\tau=\min_e\tau^{[e]}_n$ では、一つの要素が壊れると全体の厚みが0になる。この形は条件1・3・4・5を満たすが、条件2を満たさないので、評価の中で除去を扱わない）。

#### 補修回復分として扱わない理由

肉盛り溶接のような補修を、「劣化度が戻った」（補修回復分）と読む考え方もある。溶接した時点の全体の厚みは、どちらの読み方でも同じになりうる。違いはその後の扱いと記録に出る。

例：宣言厚み30、劣化度0.2（実効厚み24）の部材を、溶接で27相当まで強化する。溶接の熱で母材に劣化度0.02が加わり、溶接部の宣言厚みを3.6とする（数値は説明用）。

| | 劣化度が戻ったと読む | 構造要素の付加と読む |
|---|---|---|
| 溶接した時点の全体の厚み | $\lambda$ を0.2から0.1へ戻す。 $30\times0.9=27$ | 母材 $30\times(1-0.22)=23.4$ に溶接部3.6を合わせて $27.0$ （ $\mathrm{Comp}_\tau$ は和） |
| 母材の劣化の記録 | 0.1へ書き換わり、傷んでいたことが値から消える | 0.22のまま残る（溶接熱による分を含む） |
| 溶接部の劣化 | 母材と同じ劣化度で進む前提になる | 溶接部自身の法則で進む（溶接欠陥・残留応力など、母材と異なる壊れ方） |
| 溶接部が壊れたとき | 何が壊れたかを式の上で区別できない | 要素一つの破断（厚み0）として表せる |

劣化度が戻ったと読むのは、全体の厚みという値の復帰を、母材の物理状態の復元と同一視することであり、P6と命題2aに反する。補修した部材に別の検査記録を付け、耐力を見直して扱う実務も、付加の読み方と一致する。

#### 厚みが変わったように見える場合の分類

| 見かけの現象 | 分類 | 実効厚み $\tau_n$ |
|---|---|---|
| 時間がたつと戻る | 自然回復 | 増やさない（AXIOMS.md §7） |
| 作用や条件で一時的に狭まった受け止め幅が戻る（例：高温時の強度低下、暖機中の新サーバー） | 可逆な変化 | $\tau_n$ から差し引かない（AXIOMS.md §7）。一次式では一時的な可逆成分 $q^{\mathrm{temp}}$ として数える（下の「一時的に受け止め幅が狭まる場合」）。二次式では側別有効ゲート幅で扱う |
| 側別有効ゲート幅が広がる | 二次式の計器の変化 | 増やさない（FORMULA.md §4.4） |
| 閾値・フィルター・ゲート幅を評価出力で調整する | 計器の自己調整 | 増やさない（逆導出B、AXIOMS.md §14） |
| 新しい観測で宣言厚みが変わる | 評価スナップショットの更新 | 評価の中では増やさない。次の評価スナップショットとして宣言し直す（FORMULA.md §6、AXIOMS.md §14） |
| 補強・増設・新しい境界を設ける | 構造要素の付加 | **増える**（本節の経路） |
| 要素を取り替える | 旧要素の除去（壊れていれば破断）と新要素の付加 | 旧要素の分が減り、新要素の分が増える |
| 壊れていない要素を計画的に外す（例：サーバーの縮退） | 構造要素の除去 | 減る。 $\lambda$ には計上しない |
| 傷を直す（溶接・充填など） | 補修材という要素の付加。既存要素の劣化度は減らない | 補修材の分だけ増える |
| 伸び・曲がりを力で戻す | 矯正 | 評価の中では扱わない。評価を終え、宣言し直す（P6） |

AIの実行系では、フィルターや閾値の調整は計器の変化であり、厚みの増加ではない。厚みが増えたといえるのは、Cause-Sideで根拠を示せる別の構造・境界を新たに設けた場合だけである。動的な $\tau$ を用いる実装は、その増減がこの表のどれに当たるかを明示する（AXIOMS.md §7 解釈境界コメント）。

#### 一時的に受け止め幅が狭まる場合（一時的な可逆成分）

作用や条件によって、構造が受け止められる幅が一時的に狭まり、条件が去れば戻る場合がある（高温時の強度低下、暖機中のサーバーなど）。狭まった幅を実効厚みから差し引くと、戻るときに厚みが増えることになり、AXIOMS.md §7に反する。そこで、狭まった幅はズレの側に数える。この量を**一時的な可逆成分** $q^{\mathrm{temp}}_n\ge0$ とし、分解規則 $\mathsf{Alloc}$ で作用 $a_n$ に計上して、可逆成分 $q_n$ の一部とする。条件が残した恒久的な傷みは、 $q^{\mathrm{temp}}_n$ ではなく $\Delta\lambda_n$ に計上する（一変化一計上、P5）。

**系（ズレの側に数える安全側性）**： $q^{\mathrm{temp}}$ 以外のズレを $\delta\ge0$ とし、 $0\le q^{\mathrm{temp}}<\tau$ 、 $\delta+q^{\mathrm{temp}}\le\tau$ とする。ズレの側に数えた比 $(\delta+q^{\mathrm{temp}})/\tau$ と、狭まった幅を厚みの側で差し引いた比 $\delta/(\tau-q^{\mathrm{temp}})$ について、

$$
\frac{\delta+q^{\mathrm{temp}}}{\tau}-\frac{\delta}{\tau-q^{\mathrm{temp}}}=\frac{q^{\mathrm{temp}}\,(\tau-\delta-q^{\mathrm{temp}})}{\tau\,(\tau-q^{\mathrm{temp}})}\ \ge0
$$

であり、両者は $\delta+q^{\mathrm{temp}}=\tau$ で同時に1になる。

**証明**：通分すると、分子は

$$
(\delta+q^{\mathrm{temp}})(\tau-q^{\mathrm{temp}})-\delta\,\tau
=q^{\mathrm{temp}}\,\tau-\delta\,q^{\mathrm{temp}}-\bigl(q^{\mathrm{temp}}\bigr)^2
=q^{\mathrm{temp}}\,(\tau-\delta-q^{\mathrm{temp}})
$$

である。分母は正、 $q^{\mathrm{temp}}\ge0$ 、 $\tau-\delta-q^{\mathrm{temp}}\ge0$ より非負。∎

これは命題1の $p$ を $q^{\mathrm{temp}}$ に置き換えた形である。破断点は変わらず、破断の手前ではズレの側に数えた方が $R$ が同じか大きく出る（安全側）。数値確認： $\tau=30$ 、 $\delta=12$ 、 $q^{\mathrm{temp}}=6$ で、 $18/30=0.60$ 、 $12/24=0.50$ 、差 $0.10=6\times12/(30\times24)$ 。

保守のために要素を一時的に外す場合を、除去と再付加として扱うか、 $q^{\mathrm{temp}}$ として扱うかは、評価宣言で事前に決めておく。

**復元劣化**：破断または相転移に至った構造（AXIOMS.md §8）では、既存の要素の劣化はそのまま残る。本書は、§8の $\tau_{\mathrm{restored}}$ を「付加した要素を除く、既存の要素の吸収厚み」と読む。この読みでは、§8の制約 $\tau_{\mathrm{restored}}<\tau_0$ は既存の要素についての制約となり、付加と矛盾しない。付加によって全体の実効厚みが $\tau_0$ を上回ることはありうるが、それは初期構造への復元ではない。この読みと一文は、AXIOMS.md §8にある。

### 3.4 段4　一次式

以上から、一次式は次の形で到達する。

$$
\boxed{\
R_n=\frac{\delta_n}{\tau_n}=\frac{q_n+p_n}{\mathrm{Comp}_\tau\bigl(((1-\lambda^{[e]}_n)\,\tau^{[e]}_0)_{e\in\mathsf{Active}_n}\bigr)}
\ }
$$

$$
M_{\tau,n}=\tau_n-\delta_n=\mathrm{Comp}_\tau\bigl(((1-\lambda^{[e]}_n)\,\tau^{[e]}_0)_{e\in\mathsf{Active}_n}\bigr)-q_n-p_n
$$

要素が一つ（宣言時の構造だけ）の場合は、次のとおりである。

$$
R_n=\frac{q_n+p_n}{(1-\lambda_n)\,\tau_0},\qquad
M_{\tau,n}=(1-\lambda_n)\tau_0-q_n-p_n
$$

以下、補題・命題で「要素が一つの場合」と記したものは、この形を使う。

分子は「どれだけ入り込んだか」、分母は「器が今どれだけ残っているか」を表す。一次式そのものは変えていない。変えたのは、 $\delta$ と $\tau$ の中身を分解して書いたことだけである。

---

## 4. 補題と命題

### 補題1　定義域の充足と境界

(a) 一般の場合： $q_n,p_n\ge0$ が有限で、合成規則の値 $\tau_n=\mathrm{Comp}_\tau(\cdot)$ が正ならば、 $\tau_n$ は有限（ $\mathrm{Comp}_\tau$ の条件3）かつ正で、 $\delta_n=q_n+p_n\ge0$ は有限である。したがってP4を満たす。 $\tau_n=0$ （全要素の喪失など。第2部3.3の系）のときはP4を満たさない。

(b) 要素が一つの場合： $\tau_0>0$ 、 $0\le\lambda_n<1$ 、 $q_n,p_n\ge0$ で、いずれも有限ならば、

$$
\tau_n=(1-\lambda_n)\tau_0>0,\qquad \delta_n=q_n+p_n\ge0
$$

**証明**：(a)は仮定と $\mathrm{Comp}_\tau$ の条件3、非負数の和が非負であることによる。(b)は $1-\lambda_n>0$ と $\tau_0>0$ の積が正であることによる。∎

$\tau_n=0$ のときは、正典どおり**OUT_OF_DESCRIPTION_DOMAIN**とする（ $\tau=0$ を無限大の $R$ へ置き換えない。FORMULA.md §1、AXIOMS.md §6）。要素が一つの場合、 $\lambda_n=1$ のときに $\tau_n=0$ となる。以下、要素が一つの場合について境界の順序を述べる。 $\delta>0$ のまま $\lambda$ が1へ近づく場合、 $\tau_n\le\delta_n$ となった時点、すなわち $\lambda_n\ge1-\delta_n/\tau_0$ で $R\ge1$ に達する。ある更新番号で $1-\delta_n/\tau_0\le\lambda_n<1$ となれば、OUT_OF_DESCRIPTION_DOMAINより先にRUPTURE_BOUNDARYが記録される。ただし離散の更新では、 $\lambda$ がこの区間を経ずに一度で1に達することがある。その場合、および $\delta=0$ のまま厚みが尽きる場合は、直前の $R$ が1未満でも、その時点の分類はOUT_OF_DESCRIPTION_DOMAINである。 $\tau=0$ をRUPTURE_BOUNDARYへ読み替えない。

### 補題2　無次元性

$[\delta]=[\tau]=u$ ならば $[R]=1$。 $\lambda$ は割合なので無次元であり、各要素の厚みの単位は宣言厚みの単位 $u$ のまま変わらない。合成規則の値も単位 $u$ を保つ（ $\mathrm{Comp}_\tau$ の条件3）。∎

### 補題3　単調性

(a) 一般の場合： $\tau_n>0$ の範囲で、 $R_n$ は $q_n$ と $p_n$ について増加し、各要素の劣化度 $\lambda^{[e]}_n$ について非減少である。

**証明**： $R=(q+p)/\tau$ の分母は $q$ 、 $p$ によらず正なので、 $q$ 、 $p$ について増加する。 $\tau^{[e]}=(1-\lambda^{[e]})\tau^{[e]}_0$ は $\lambda^{[e]}$ について減少し、 $\mathrm{Comp}_\tau$ は各引数について非減少（条件1）なので、 $\tau$ は $\lambda^{[e]}$ について非増加である。 $q+p\ge0$ より、 $R$ は $\lambda^{[e]}$ について非減少である。∎

(b) 要素が一つの場合：

$$
\frac{\partial R}{\partial q}=\frac{\partial R}{\partial p}=\frac{1}{(1-\lambda)\tau_0}>0,
\qquad
\frac{\partial R}{\partial \lambda}=\frac{q+p}{(1-\lambda)^2\tau_0}\ge0
$$

ズレが増えても、器が縮んでも、 $R$ は上がる。境界へ近づく理由が二種類あり、どちらも式の中で区別されている（→【4】【8】）。∎

### 命題1　基準不動の安全側性（→【5】）

基準を残留ズレの位置へ付け直した表現を考える。

$$
\delta'=q,\qquad \tau'=\tau-p,\qquad R'=\frac{q}{\tau-p}\quad(\tau>p)
$$

このとき次が成り立つ。

(a) 残存余白は同じ： $M'_\tau=\tau'-\delta'=\tau-p-q=M_\tau$

(b) 破断点は同じ： $R=1\iff q+p=\tau\iff R'=1$

(c) 破断前（ $M_\tau\ge0$ ）では常に

$$
R-R'=\frac{p\,M_\tau}{\tau(\tau-p)}\ge0
$$

**証明（c）**：

$$
R-R'=\frac{(q+p)(\tau-p)-q\tau}{\tau(\tau-p)}
=\frac{p\tau-qp-p^2}{\tau(\tau-p)}
=\frac{p(\tau-q-p)}{\tau(\tau-p)}
=\frac{p\,M_\tau}{\tau(\tau-p)}
$$

分母は正、 $p\ge0$ 、 $M_\tau\ge0$ より非負。∎

**意味**：破断点（ $R=1$ ）は両表現で一致する。一方、途中の閾値 $R_{\mathrm{warn}}$・$R_{\mathrm{handoff}}$・$R_{\mathrm{irrev}}$ への到達は、目盛りを付け直した表現の方が**遅れる**。さらに除荷後（ $q=0$ ）は $R'=0$ となり、「完全に戻った」と表示される。基準不動（P7）は好みの問題ではなく、**警告を遅らせず、履歴を隠さないための前提**である。評価と評価の間で基準を再宣言する場合（第3部段6）に $\tau'=\tau-p$ を守らせるのは、(b)の破断点の一致を保つためである。

**数値確認**（第1部のばね、 $\tau=27$ 、 $p=3$ 、 $q=12$ ）：

$$
R=\frac{15}{27}\approx0.556,\qquad R'=\frac{12}{24}=0.5,\qquad
\frac{p\,M_\tau}{\tau(\tau-p)}=\frac{3\times12}{27\times24}=\frac{36}{648}\approx0.056
$$

差は $0.556-0.5=0.056$ で一致する。

### 命題2　値の復帰は構造の復元を意味しない（→【6】）

観測できる値を $o$ とする。次の三つを区別する。

- **対象の物理状態** $\mathsf{Phys}_n=(q_n,p_n,(\lambda^{[e]}_n)_{e\in\mathsf{Active}_n})$ （P9の対象状態）
- **評価状態**：不可逆ラッチ $\ell_n$ など、評価出力として保持するもの
- **経路履歴** $\mathsf{History}_n$ ：事象の記録（監査・構造証言のため）

一つの観測事象 $\mathrm{Ev}$ を挟んだ前を $(-)$ 、後を $(+)$ で表す。

**命題2a（物理状態）**：その事象で $\Delta p>0$ 、またはある要素で $\Delta\lambda^{[e]}>0$ ならば、 $o^{(+)}=o^{(-)}$ であっても $\mathsf{Phys}^{(+)}\ne\mathsf{Phys}^{(-)}$ 。

**証明**：P5の増分の定義より $p^{(+)}=p^{(-)}+\Delta p$ 、 $\lambda^{[e](+)}=\lambda^{[e](-)}+\Delta\lambda^{[e]}$ 。いずれかの増分が正なら、その成分が異なる。 $o$ の一致は、この成分の一致を含まない。∎

例：第1部【6】の新品のばねと一度引いたばねは、同じ15 mmの位置（ $o$ が同じ）にあるが、 $p$ （0と3）と $\lambda$ （0と0.1）が異なる。

**命題2b（経路履歴）**：どの事象についても $\mathsf{History}^{(+)}\ne\mathsf{History}^{(-)}$ 。

**証明**：P6より $\#\mathsf{History}^{(+)}=\#\mathsf{History}^{(-)}+1$ 。∎

**二つの命題の関係**：完全に弾性範囲の事象（ $\Delta p=0$ 、すべての $\Delta\lambda^{[e]}=0$ 、除荷後 $q=0$ ）では、物理状態は元に戻る（ $\mathsf{Phys}^{(+)}=\mathsf{Phys}^{(-)}$ ）。命題2aは、この場合について何も主張しない。それでも、事象が起きたという記録は経路履歴に残る（命題2b）。これは唯一の律環公理の帰結「同一履歴の完全再現は不可能である」（AXIOMS.md §2）に対応する。値の復帰（ $o$ ）、物理状態の復帰（ $\mathsf{Phys}$ ）、履歴の同一（ $\mathsf{History}$ ）は別々の問いであり、「値は戻っても、経路履歴は戻らない」は命題2bの主張、「値は戻っても、構造は戻っていない」は、不可逆な変化があった場合の命題2aの主張である。

**閾値と遷移の履歴**：安全域（どの閾値も越えていない範囲）で劣化が進まない間は、 $R$ は $\delta$ に比例する線形の計算で足りる。IDEの価値が現れるのは、閾値という境界が現れたときである。閾値を越えることは、それまで見えていなかった、または見過ごしていたリスク・変動・変化が、分かりやすい事象として見え始めることを意味する。だから、いつ・どの閾値を越えたかという遷移を、経路履歴に残す。不可逆ラッチ（第3部段5）は、その遷移を評価状態に反映したものである。

さらに $\Delta p>0$ または $\Delta\lambda>0$ なら、同じ作用に対する $R$ も異なる（命題4）。

### 命題3　Rは状態を決め尽くさない（R非十分性）

要素が一つの場合で、 $\tau_0=30$ として、次の二つの構造を考える（反例なので、一つ示せば足りる）。

| | $q$ | $p$ | $\lambda$ | $\delta$ | $\tau$ | $R$ |
|---|---|---|---|---|---|---|
| A | 12 | 0 | 0 | 12 | 30 | 0.40 |
| B | 3 | 6 | 0.25 | 9 | 22.5 | 0.40 |

$R$ は同じ0.40である。ここへ、可逆成分15を生む同じ作用を加える。

| | $\delta$ | $\tau$ | $R$ |
|---|---|---|---|
| A | 15 | 30 | 0.50 |
| B | 21 | 22.5 | 約0.93 |

同じ作用に対して、Aは道のりの半分、Bは破断寸前になる。閾値をどこに置いても、AとBが同じ区分に入るとは限らない。

**結論**： $R$ は境界接近を示す**評価出力**（AXIOMS.md §14）であり、構造状態そのものではない。保持すべきなのは $R$ ではなく、対象の物理状態 $(p,\lambda)$ と、評価状態としての不可逆ラッチ $\ell$ である（命題2の区別）。∎

**既存デモとの関係**：リポジトリの複数のデモは、 $R$ の瞬間値だけで状態を決めない、という点で同じ問題意識を持っている。ただし、どれも命題3の結論をそのまま実装したものではない。

| デモ | 追加の変数 | 状態決定への使い方 | 本書から見た位置 |
|---|---|---|---|
| examples 14 | residualDebt | $R\ge1$ または debt $>0.8$ でRUPTURE_BOUNDARY | debtは $R$ から積算した量。debtでRUPTURE_BOUNDARYを判定する点は、AXIOMS.md §10.5（ $R_{\mathrm{target}}\ge1.0$ ）と一致しない |
| examples 15 | residualDebt | $R_{\mathrm{eff}}=R_{\mathrm{total}}+0.4\,\mathrm{debt}$ で分類 | debtは $R$ から積算した量。 $R$ に加算した値で分類する点は、AXIOMS.md §5（ $R$ は $\delta/\tau$ だけを意味する）との関係の整理が要る |
| examples 21 | PI・MGFの個別閾値 | $R$ 以外の条件とのORで境界確定 | 別の観測量による判定の併用 |
| examples 23, 24 | $D_{\mathrm{long}}$ | $D_{\mathrm{long}}\ge1$ で停止側へ | $D_{\mathrm{long}}$ は $R$ の移動平均 $R_{\mathrm{short}}$ から作った量 |

residualDebtと $D_{\mathrm{long}}$ は、いずれも $R$ （評価出力）の履歴から作った集約であり、本書の $(p,\lambda)$ （対象状態）には当たらない。また、いずれも時間経過で減る実装になっている。これらを残留ズレや劣化の量として読むなら、AXIOMS.md §7の非自然回復（P6）と一致しない。デモは正典の下位にあるので（AXIOMS.md §16）、デモの位置付けの整理で対応する。

### 命題4　厚み縮小と履歴感応性（→【6】）

要素が一つの場合、二つの構造の劣化度を $\lambda_{\mathrm{low}}$ 、 $\lambda_{\mathrm{high}}$ とする。 $\delta>0$ 、 $0\le\lambda_{\mathrm{low}}<\lambda_{\mathrm{high}}<1$ ならば

$$
\frac{\delta}{(1-\lambda_{\mathrm{high}})\tau_0}>\frac{\delta}{(1-\lambda_{\mathrm{low}})\tau_0}
$$

同じズレでも、履歴で器が小さくなった構造ほど境界に近い。一般の場合は、補題3(a)より、ある要素の劣化度が大きい構造の $R$ は小さくならない（ $\mathrm{Comp}_\tau$ がその要素について厳密に増加するなら、大きくなる）。

**ダムの反例**（ $\tau_0=100$ 、単位はズレ単位）：

| | 現在の水位 | $q$ | $p$ | $\lambda$ | $\delta$ | $\tau$ | $R$ |
|---|---|---|---|---|---|---|---|
| ダムA | 低い | 20 | 10 | 0.4 | 30 | 60 | 0.50 |
| ダムB | 高い | 40 | 0 | 0 | 40 | 100 | 0.40 |

**水位が低いダムAの方が境界に近い**。現在値型監視（水位だけで判定）では、この順序が逆に見える。

### 命題6　一次式の増分と二重ゆらぎ検出条件の整合（→【8】）

添字はFORMULA.md §4.7の後退差分（ $\Delta\delta_n=\delta_n-\delta_{n-1}$ 、 $\Delta\tau_n=\tau_n-\tau_{n-1}$ ）に揃える。

$$
R_n-R_{n-1}=
\underbrace{\frac{\Delta\delta_n}{\tau_n}}_{\text{進入項}}
+
\underbrace{\delta_{n-1}\Bigl(\frac{1}{\tau_n}-\frac{1}{\tau_{n-1}}\Bigr)}_{\text{縮小項}}
$$

**証明**：

$$
R_n-R_{n-1}=\frac{\delta_{n-1}+\Delta\delta_n}{\tau_n}-\frac{\delta_{n-1}}{\tau_{n-1}}
=\frac{\Delta\delta_n}{\tau_n}+\delta_{n-1}\Bigl(\frac{1}{\tau_n}-\frac{1}{\tau_{n-1}}\Bigr)\qquad∎
$$

要素が一つの場合、段3の $\tau_n=(1-\lambda_n)\tau_0$ を用いると、縮小項は

$$
\delta_{n-1}\Bigl(\frac{1}{\tau_n}-\frac{1}{\tau_{n-1}}\Bigr)=\frac{\delta_{n-1}\,\tau_0\,(\lambda_n-\lambda_{n-1})}{\tau_n\,\tau_{n-1}}
$$

となり、P6より非負である。要素が複数ある一般の場合も、付加のない区間では非負であり、付加の時点では負になりうる。

**系**： $\tau_n,\tau_{n-1}>0$ 、 $\delta_{n-1}>0$ のとき、

$$
\bigl(\Delta\delta_n>0\ \land\ \Delta\tau_n<0\bigr)
\iff
\bigl(\text{進入項}>0\ \land\ \text{縮小項}>0\bigr)
$$

**証明**：進入項の符号は $\Delta\delta_n$ の符号に等しい（ $\tau_n>0$ ）。縮小項は $\delta_{n-1}(\tau_{n-1}-\tau_n)/(\tau_n\tau_{n-1})$ であり、 $\delta_{n-1}>0$ のとき符号は $-\Delta\tau_n$ の符号に等しい。∎

**位置付け**：左辺はFORMULA.md §4.7の二重ゆらぎ検出条件である。系は、二次式の検出条件が一次式の変化（押し込みと器の削れが同時に起き、 $R$ が二方向から押し上げられる遷移）と**整合する**ことを示す。二次式を一次式の帰結として位置づけるものではない。二次式はIDEの第二の正規計算系である（FORMULA.md §4）。

$\delta_{n-1}=0$ のときは、 $\Delta\tau_n<0$ でも縮小項は0になる。まだ何も押し込まれていない構造では、器の削れは $R$ の増分に現れず、 $\lambda$ にだけ残る。これも命題3の一つの形である。

**数値確認**（第1部【8】のばね、 $\tau_0=30$ ）：前は $q=8,p=0,\lambda=0$ で $R=8/30\approx0.267$ 。15 mmまで引いた後は $q=12,p=3,\lambda=0.1$ で $\tau=27$ 、 $R=15/27\approx0.556$ 。

$$
\text{進入項}=\frac{7}{27}\approx0.259,\qquad
\text{縮小項}=8\Bigl(\frac{1}{27}-\frac{1}{30}\Bigr)\approx0.030
$$

和は $0.289$ で、 $0.556-0.267=0.289$ と一致する。

（命題5は、更新規則を前提とするので第3部に置く。）

---

## 5. 三つの領域への当てはめ

| | $q$（可逆成分） | $p$（残留ズレ） | $\lambda$（劣化度） | 観測の例 |
|---|---|---|---|---|
| ばね | 弾性伸び | 永久伸び（コイルの隙間） | 疲労・微小亀裂による破断伸びの低下 | 変位、自然長、ばね定数 |
| ダム | 水圧による弾性変形 | 残留変位・沈下 | 亀裂・漏水経路・剛性低下 | 水位、変位計、漏水量、濁り、亀裂長 |
| モーター | 負荷による温度上昇（冷えれば戻る） | 宣言次第では0 | 絶縁劣化・巻線損傷 | 電流、温度、絶縁抵抗、煙 |

- モーターのように $p$ が存在しない領域では、 $\mathsf{Decl}$ で $p\equiv0$ と宣言する。**要素を消すのではなく、0であることを宣言する**。
- 「煙が出た」「漏水した」は、それ自体が $\Delta\lambda$ の値ではない。観測を $\Delta\lambda$ へ変換する規則（ $\mathsf{Alloc}$ ）がドメインごとに必要である。
- モーターの「ブレーカーが落ちた」は、 $a_n=0$（作用の除去）であって、構造要素の付加ではない。したがって $q$ は0へ戻るが、 $\lambda$ は減らない。停止は回復ではない。
- 先行草案の熱損傷積分（限界温度を超えた分を時間で積算した損傷。温度が限界より下がっても厚みは回復しない。先行草案§14.1）は、モーター行の $\Delta\lambda$ を与える $\mathsf{Alloc}$ の具体例として読める。

---

## 6. 正典・既存資料との対応

### 6.1 正典の $\tau$ 状態遷移式との対応

AXIOMS.md §7の補助モデル

$$
\tau(t)=\tau_0-\int_0^t f(\delta(s))\,ds
$$

は、要素が一つの場合に、本書で $\tau_0-\tau_n=\tau_0\lambda_n$ とおき、更新番号 $n$ に時刻 $t_n$ を対応させて、劣化の増分を

$$
\Delta\lambda_n=\frac{1}{\tau_0}\int_{t_{n-1}}^{t_n} f(\delta(s))\,ds
$$

とした特別な場合に当たる。区間内で $\delta$ を区間の始めの $\delta_{n-1}$ で代表させれば、近似として $\Delta\lambda_n\approx f(\delta_{n-1})\,\Delta t_n/\tau_0$ （ $\Delta t_n=t_n-t_{n-1}$ ）となる。正典の「閉区間内で $\tau$ は非増加」は、本書の $\lambda_n\ge\lambda_{n-1}$（P6）と同じ内容である。

正典の式では、 $\delta$ が $R$ の分子に入り、同時に $\tau$ を削っている。これは二重計上ではない。 $\delta$ は「進入量」として $R$ に入り、 $f(\delta)$ は「進入が器を摩耗させる作用」として $\lambda$ に入る。別の物理作用だからである。この更新は対象構造の物理法則によるものであり、逆導出ではない（AXIOMS.md §14）。

### 6.2 デモとの対応

| デモ | 本書での読み | 注記 |
|---|---|---|
| 25 ダム劣化 | $\delta$ ＝瞬間ゆらぎ（ $q$ ）、 $\tau=\tau_0-k\int\delta$（ $\lambda$ ）。 $p\equiv0$ の特別な場合 | AXIOMS.md §7の素直な実装 |
| 13 光合成 | 段1の射影の例 | 「δを生成するだけ」と明記 |
| 06, 26 脱進機 | 第3部段6の周期的な評価間遷移 | 跳躍回数＝評価番号 |
| 14, 15 電力・OR/ICU | 第3部段6（新評価と旧履歴アーカイブ）、命題3（debt） | debtは $R$ から積算した量で、時間経過で減る。14はdebtでRUPTURE_BOUNDARYを判定している（命題3の表） |
| 23, 24 サンプル・車両 | 命題3（ $D_{\mathrm{long}}$ ） | $D_{\mathrm{long}}$ は $R$ の移動平均から作った量で、時間経過で減る。24は自身の評価出力の移動平均で $\tau_{\mathrm{upper}}$ を広げており、逆導出B（P9(ii)）に当たる |
| 07〜12 帯域ゲート | 側別有効ゲート幅の動的変化 | 実効厚みか側別有効ゲート幅かの明示がない。07は $\tau$ をCause-Side偏差のEMAから作っており、逆導出Bに当たらない |
| 18, 20, 27〜30 張力・圧力等 | 段2の瞬間観測型 | 基準不動と $p$ 保持の下で正典と両立 |

### 6.3 先行草案との対応

`nra-core/foundations/NRA-IDE_動的厚みと不可逆境界_会話統合_26-0802-1830.md` は、本書より前に次を与えている。先行草案の記号は本書の記号と衝突するものがあるので（辞書0.5）、ここでは語で示し、式は先行草案の該当節を参照する。

| 先行草案（節） | 本書 |
|---|---|
| ズレと厚みの一転移ごとの更新（§4.1） | 第3部段5の更新規則。本書はズレの増分を $\Delta q+\Delta p$ 、厚みの減少を要素ごとの劣化度の増分に分けた |
| 「分子増加と分母減少が同時なら線形ではない」（§4.1） | 命題6（進入項と縮小項）で式にした |
| 残余厚みと一転移崩壊比（§5） | 残余厚みは $M_{\tau,n}$ 。一転移崩壊比は、第3部段5の一段先読みとして併用できる |
| 境界仕様（8項目の宣言。§3） | P0の評価宣言 $\mathsf{Decl}$ |
| 不可逆厚み損失（§9.1） | $\Delta\lambda_n$ （要素が複数なら $\Delta\lambda^{[e]}_n$ ） |
| 未観測分を厚みから控除する有限観測近接（§11.3） | 評価宣言の欠測処理（観測不足で厚みを増やさない規則）の具体例 |

### 6.4 逆導出の語義の分類

リポジトリ内の「逆導出」「逆算」「逆流」「 $\Pi^{-1}$ 」の語義の分類は、`theory/SANDWICH_ARCH.md` §8.4 による。本書のP8・P9は、その分類のうち逆導出A・逆導出B・他の評価対象の評価出力の扱いを導く前提である。

---

## 7. 証明するもの・宣言するもの・検証するもの

| 区分 | 内容 | 扱い |
|---|---|---|
| 証明できる | 補題1〜3、命題0〜4・6（第2部）、命題5（第3部） | 本書のとおり、数学として閉じる |
| 宣言するもの | $\mathsf{Decl}$ の各要素（合成規則 $\mathrm{Comp}_\tau$ を含む）、 $p\equiv0$ などの0の宣言、基準状態、各量が対象状態・計器・評価出力のどれに属するか | 証明しない。計算開始前に固定する約束 |
| 検証が必要 | $\sigma$ の具体形、劣化の進み方、 $\tau_0$ と付加した要素の $\tau^{[e]}_0$ 、 $\mathrm{Comp}_\tau$ の具体形、閾値の値、観測から $\Delta\lambda$ への変換 | ドメインの実測・実験で裏付ける。正典では形と条件だけを定める |

前提式を「すべて証明する」必要はない。本書が引き受けるのは、上の表の**証明**と**宣言の枠組み**までである。具体的な関数形は各ドメインに委ねる。

評価宣言の要素（ $\sigma$ ・ $\mathsf{Alloc}$ ・ $\mathrm{Comp}_\tau$ を含む）、一変化一計上、射影との整合は、FORMULA.md §0.5（v2.1）が形と条件を定める。基準不動、蓄積ズレの構成、構造要素の付加・除去はAXIOMS.md §4・§7が定める。本書は、それらの導出・証明・例を示す。

---

# 第3部　一次式の後段（正典化の判断前）

本部は、一次式の後の遷移（評価内の遷移、評価間の遷移、階層・他構造との連結）を扱う。本部の内容は正典化の判断前であり、正典の定義ではない。正典化する場合は、その判断を経てFORMULA.md等に反映する。

## 1. 本部の記号

| 記号 | 名称 | 意味 | 第1部 |
|---|---|---|---|
| $\mathsf{Update}$ | 更新規則 | 評価内で状態を進める規則（段5） | — |
| $\rho$ | 可逆応答 | 作用から可逆成分を与える関数 | — |
| $g_p$ 、 $g^{[e]}_\lambda$ | 不可逆増分の法則 | 残留ズレ・劣化度の増分を与える関数 | — |
| $\mathrm{Class}(R)$ | 瞬間分類 | 有効な $R$ の区間による正典の分類（ラッチを反映する前） | 【7】 |
| $\mathsf{State}_n$ | 状態区分 | PERMIT 〜 RUPTURE_BOUNDARY（ラッチを反映） | 【7】 |
| $j$ | 評価番号 | 何番目の評価宣言か | 【10】 |
| $\mathsf{Archive}$ | 保管記録 | 終了した評価の記録の列 | 【10】 |
| $Z_n$ | 判定用十分状態 | 名前付きの欄を持つ記録：残留ズレ $p_n$ 、構成 $\mathsf{Active}_n$ と各要素の宣言厚み・劣化度、不可逆ラッチ $\ell_n$ （必要なら追加状態）。物理状態と評価状態の組（辞書「判定用十分状態」） | 【11】 |
| $\mathrm{EvalGraph}^{(j)}$ | 展開評価グラフ | 評価 $j$ の全段で、どの量からどの量を計算したかを表す有向グラフ | 【9】 |

## 2. P9の残りの条件

量を頂点、「ある量を使って別の量を計算した」ことを有向辺とし、評価 $j$ の全段をつないだ有向グラフを**展開評価グラフ** $\mathrm{EvalGraph}^{(j)}$ とする。頂点には他構造 $i$ の量とEffect-Side出力も含める。 $\mathrm{EvalGraph}^{(j)}$ は逆導出（第2部P9の(i)(ii)）を含まず、(iv)に加えて次を満たす。

$$
\text{(iii)}\quad \text{対象状態への辺は、対象の物理法則による更新か、}\mathsf{Alloc}\text{を通した事象（}\Delta p\ge0,\ \Delta\lambda\ge0\text{）、または構造要素の付加に限る}
$$

$$
\text{(v)}\quad \text{各段の計算は閉路を持たず、同一段内の計算順序は}\ \mathsf{Decl}\ \text{で宣言する}
$$

$$
\text{(vi)}\quad \text{辺の有無と各辺の計算規則は}\ \mathsf{Decl}\ \text{の要素として評価前に固定する}
$$

## 3. 段5　評価内の遷移（→【7】）

**更新規則 $\mathsf{Update}$**：

増分は第2部P5と同じ後退差分で書く（更新番号 $n$ の事象が、状態を $n-1$ から $n$ へ進める）。

$$
q_n=\rho(a_n),\qquad \rho(0)=0,\qquad \rho\ge0
$$

$$
p_n=p_{n-1}+\Delta p_n,\qquad \lambda^{[e]}_n=\lambda^{[e]}_{n-1}+\Delta\lambda^{[e]}_n,\qquad 0\le\lambda^{[e]}_n\le1
$$

更新番号 $n$ で構造要素を付加した場合は、新しい要素を構成 $\mathsf{Active}_n$ に加え、その $\lambda$ を0、宣言厚みを付加時点のCause-Side測定値として始める（第2部3.3）。構造要素を除去した場合は、その要素を構成から外す。 $\lambda$ を減らす項は置かない（P6）。

冷却のように戻るまでに時間がかかる領域では、 $q_n=\rho(q_{n-1},a_n)$ とし、「 $a=0$ が続けば $q\to0$ 」を満たすことを条件とする。自然減衰が許されるのは $q$ だけである（P6）。

$R$ の増分 $R_n-R_{n-1}$ は、第2部の命題6のとおり進入項と縮小項に分かれる。

**分類の順序**：各更新番号で、 $R$ を計算する前に次の順で判定する。

1. 入力が不明・不正・非有限（対象・単位・時点・出所の不明を含む）なら、**CONFESSION**とする（AXIOMS.md §6・§10.6）。 $R$ を計算しない。
2. $\tau_n=0$ なら、**OUT_OF_DESCRIPTION_DOMAIN**とする（AXIOMS.md §6・§10.7）。 $R$ を計算しない。
3. それ以外（ $\tau_n>0$ 、 $\delta_n\ge0$ 、有限）のときだけ、 $R_n$ を計算し、下のラッチと状態区分を更新する。

1・2の場合、ラッチ $\ell$ は値を保ち、 $R$ による更新をしない（ラッチは自動で解除しない）。観測できないだけの場合は `NOT_OBSERVABLE` と欠損理由を出力し、CONFESSIONへ移さない（第2部P2）。

**ラッチと状態区分**（→【7】）：

$$
\ell_n=\ell_{n-1}\ \lor\ \mathbf{1}\{R_n\ge R_{\mathrm{irrev}}\}
$$

瞬間分類 $\mathrm{Class}(R)$ は正典の区間分類（PERMIT／BOUNDARY_WARNING／HANDOFF_REQUIRED／IRREVERSIBLE_TRANSITION／RUPTURE_BOUNDARY）とする。状態区分に

$$
\text{PERMIT}<\text{BOUNDARY\_WARNING}<\text{HANDOFF\_REQUIRED}<\text{IRREVERSIBLE\_TRANSITION}<\text{RUPTURE\_BOUNDARY}
$$

の順序を置き、

$$
\mathsf{State}_n=
\begin{cases}
\mathrm{Class}(R_n) & \ell_n=0\\[2pt]
\max\bigl(\mathrm{Class}(R_n),\ \text{IRREVERSIBLE\_TRANSITION}\bigr) & \ell_n=1
\end{cases}
$$

とする。ラッチ後に $R$ が下がっても、IRREVERSIBLE_TRANSITIONより下の区分へは自動で戻らない（AXIOMS.md §10.4）。

## 4. 段6　評価間の遷移（旧経路の終了と新評価）（→【10】）

次のいずれかの事象で、評価 $j$ を終了する。

- $\mathsf{State}_n=\text{RUPTURE\_BOUNDARY}$ （評価対象全体の破断・転移。部分の破断では終了しない）
- OUT_OF_DESCRIPTION_DOMAIN（ $\tau=0$ 。全要素の喪失など）。記述領域の外なので、その評価の中で $R$ を計算し続けることはできない。生存している観測・記録の経路による構造証言は続ける（AXIOMS.md §11）
- 評価宣言の変更。次を含む。
  - 対象・破断様式・基準・規則の変更（評価対象そのものの交換を含む）
  - 新しい観測で宣言厚みが変わる場合（次の評価スナップショットとして宣言し直す。FORMULA.md §6、AXIOMS.md §14）
  - 矯正（P6）
  - 宣言した合成規則 $\mathrm{Comp}_\tau$ で表せない付加
  - 合成規則が条件2を満たさない場合の除去（第2部3.3）

構造要素の付加は、合成規則で表せる限り、評価を終了させない（第2部3.3）。CONFESSIONは不明時の停止信号であり、評価を終了させるものではない。不明が解消するまで $R$ を計算せず、状態区分を進めない。

終了時の操作：

$$
\mathsf{Archive}\leftarrow\mathsf{Archive}\oplus\bigl(\mathsf{Decl}_j,\ \mathsf{History}^{(j)},\ Z^{(j)}_{\mathrm{final}}\bigr)
$$

$$
\mathsf{Decl}_j\ \longrightarrow\ \mathsf{Decl}_{j+1},\qquad j\leftarrow j+1
$$

- 旧評価の記録は保管し、書き換えない。新評価へ持ち込むのは要約ではなく、**新しいCause-Side測定で決めた $\tau_0^{(j+1)}$**である。
- 評価 $j$ でラッチがかかった場合、その記録を $\mathsf{Archive}$ に残し、 $\mathsf{Decl}_{j+1}$ にも「前の評価でラッチがかかっていた」ことを記す。評価 $j$ と評価 $j+1$ の $R$ は、比較できるとは主張しない（第2部P0の比較可能性）。
- 破断または相転移に至った後に初期構造への復元を主張する場合は、AXIOMS.md §8のとおり、比較可能性（同一対象・同一単位・同一測定規則）と $\tau_{\mathrm{restored}}<\tau_0^{(j)}$ の双方を立証する。ここでの $\tau_{\mathrm{restored}}$ は、付加した要素を除く既存の要素の吸収厚みである。付加した要素を含む全体の宣言厚みが $\tau_0^{(j)}$ を上回っても、復元ではない（第2部3.3）。
- 基準状態の再宣言は、ここでのみ許す（P7、AXIOMS.md §4）。基準を残留ズレの位置へ付け直す場合は、構造要素の付加がなく、新しいCause-Side測定で厚みを測り直していない限り、 $\tau_0^{(j+1)}\le\tau_n^{(j)}-p_n^{(j)}$ とする。これは命題1(b)（破断点の一致）から導かれる、基準を付け直すときの本書の安全側の条件であり、正典の一般規則ではない。基準を付け直さない場合は、要約を持ち込まなくても、新評価の観測に $p_n^{(j)}$ が $p_0$ として現れる（命題0）。新評価の宣言厚みは、新しいCause-Side測定で定める（次の評価スナップショット。FORMULA.md §6、AXIOMS.md §14）。その値が旧評価の $\tau_n^{(j)}$ より大きく出ても、評価の中の増加ではなく、旧評価と新評価の $R$ を比較できるとは主張しない。
- 評価番号 $j$ と保管記録 $\mathsf{Archive}$ は減らない。構造は同じ状態へ戻らず、進み続ける。評価の系列と構造連続性 $\omega$ との対応づけは、評価宣言の任意要素として評価ごとに宣言する（第2部P0）。対応づけの一般規則は定めない。

**脱進機との対応**（`examples/06_Escapement_Principle_JP.html`、`examples/26_escapement_contactpoint_JP.html`）：一歯ごとの評価で $\delta$ が $\tau$ に達すると跳躍し、端数 $\delta-\tau$ を次の歯へ持ち越さず、 $\delta=0$ から次の歯を数える（機械の脱進機では、はみ出したエネルギーは熱として散る）。本書では、各歯を一つの評価、跳躍を段6の評価間遷移、端数を「新評価へ持ち込まない量」（保管記録には残す）として読む。跳躍の回数が $j$ に当たる。

**既存デモとの関係**：`examples/14_powergrid_transition_JP.html`、`examples/15_or_icu_continuum_JP.html`は、RUPTURE_BOUNDARYを固定したうえで「独立した新Cause-Side評価」を開始し、旧履歴をアーカイブする。段6の既存実装例である。

## 5. 段7　階層と他構造との連結（→【9】）

自構造が部分構造 $i$ （有限個）を持つとき、または他の構造 $i$ から影響を受けるとき、相手の**観測された物理状態**は、自構造への観測事象として入る。

$$
\mathrm{Ev}^{(\mathrm{self})}_{n}=\bigl(\text{構造}i\text{で観測された物理状態},\dots\bigr),\qquad
\mathsf{Alloc}^{(\mathrm{self})}\bigl(\mathrm{Ev}^{(\mathrm{self})}_n\bigr)=\bigl(a^{(\mathrm{self})}_n,\ \Delta p^{(\mathrm{self})}_n,\ \Delta\lambda^{(\mathrm{self})}_n,\ \mathrm{ctx}^{(\mathrm{self})}_n\bigr)
$$

部分の破断（ばねが1本切れた、という観測された破断事象）は、この事象の特別な場合である。部分の評価出力 $R^{(i)}_n\ge1$ そのものを自構造の対象状態へ入れるのではない。 $R^{(i)}$ （他構造の評価出力）は、自構造では次に使える：監査・構造証言での記録、P9(iv)の安全側の計器入力（閾値を下げる・ゲート幅を狭める）、事前固定された物理制御の指令（AXIOMS.md §14）。自構造の対象状態へは入れない。部分と全体、自構造と他構造は、**別々の宣言を持つ別々の評価**であり、式としては観測された物理的事象でつながる。

連結が逆導出に当たらない条件は、P9から次のように導かれる。独立の規則ではなく、P9の帰結である。

| 条件 | 内容 | 根拠 |
|---|---|---|
| LC-1 自己調整の禁止 | 自構造の評価出力（ $R$ 、その平均・集約、 $\mathsf{State}$ ）を、自構造の計器（側別有効ゲート幅、閾値、基準、射影）へ戻さない。他構造を経由して戻る場合も同じ | P9(ii)（AXIOMS.md §14） |
| LC-2 方向 | 相手の観測された物理状態は、自構造へは $\mathsf{Alloc}^{(\mathrm{self})}$ を通した事象としてのみ入る。すなわち、作用 $a$ （例：隣のばねが切れて負担が増える）、または $\Delta p\ge0$・$\Delta\lambda\ge0$ である。 $p$・$\lambda$ を減らす向きには入らない。相手の評価出力は、自構造の対象状態へは入らない。自構造の計器へは、閾値と有効ゲート幅にだけ、ゲート幅を狭める・閾値を下げる安全側の向きでのみ入る | P9(iii)(iv)、P6 |
| LC-3 非閉路 | 同一段で相手の量を使う場合は、閉路を作らない計算順序を宣言する。相互連結は計器どうしではなく対象状態どうしで表す | P9(iv)(v) |
| LC-4 事前固定 | 連結の有無・変換規則・閾値は $\mathsf{Decl}^{(\mathrm{self})}$ の要素として評価前に固定し、連結事象は $\mathsf{History}$ へ記録する | P9(vi) |

既存デモとの関係：

- `examples/12_agri_mol_antagonism_JP.html`（ $R_{\mathrm{Mg}}\ge0.7$ で $\tau_K$ を縮小）は、他構造の評価出力から自構造の計器へ、狭める向きで入る辺であり、LC-1・LC-2を満たす。同一フレームでMgを先に計算する順序は閉路を作らないので、順序を宣言すればLC-3も満たす。ただし $R_{\mathrm{Mg}}$ が下がると $\tau_K$ も戻るので、実効厚み $\tau_n$ ではなく側別有効ゲート幅の連結として宣言すべきである。
- `examples/24_vehicle_mandatory_boundary_JP.html`（自構造の $R_{\mathrm{short}}$ で $\tau_{\mathrm{upper}}$ を拡大）は、前フレームの値を使っていてもLC-1（計器の自己調整）に当たり、拡大の向きなのでLC-2にも合わない。
- `examples/07_HAN_gate_live_JP.html`は、 $\tau$ の動的変化を $R$ ではなくCause-Side偏差のEMAから作っており、LC-1に当たらない。同デモのコメントにある「結果値から $\tau$ を変化させると因果ダイオードが無効化される」は、P9(ii)と同じ考え方の先行例である（ただし同デモの $R=r_{\mathrm{raw}}\times\tau$ という掛け算は、別の問題として残る）。

## 6. 命題5　判定用要約の十分性（→【11】）

**判定用十分状態** $Z_n$ を、位置で並べる組ではなく、次の名前付きの欄を持つ記録とする（辞書「判定用十分状態」）。

- 残留ズレ $p_n$
- 構成 $\mathsf{Active}_n$ と、各要素 $e\in\mathsf{Active}_n$ の宣言厚み $\tau^{[e]}_0$ と劣化度 $\lambda^{[e]}_n$
- 不可逆ラッチ $\ell_n$

$Z_n$ のうち、ラッチを除く欄（ $p_n$ 、構成、各要素の宣言厚みと劣化度）は物理状態であり、これを $\mathsf{Phys}_n$ と書く。更新規則が次の形をしているとする（後退差分。更新番号 $n$ の事象が状態を $n-1$ から $n$ へ進める。 $e\in\mathsf{Active}_{n-1}$ ）。

$$
q_n=\rho(a_n),\quad
\Delta p_n=g_p(\mathsf{Phys}_{n-1},a_n),\quad
\Delta\lambda^{[e]}_n=g^{[e]}_\lambda(\mathsf{Phys}_{n-1},a_n)
$$

更新規則は物理法則なので、評価状態であるラッチ $\ell$ や、評価出力 $R$ ・ $\mathsf{State}$ を入力にしない（第2部P9）。 $\ell_n$ が $Z_n$ に含まれるのは、次の状態区分を決めるためである。

事象 $\mathrm{Ev}_n$ は、作用 $a_n$ と、構造要素の付加（付加の時点で測った宣言厚みを含む）・除去から成る。

**命題5**：同じ評価宣言 $\mathsf{Decl}$ （同じ閾値・同じ合成規則・同じ規則）の下で、時点 $n$ の $Z_n$ が同じ二つの履歴は、その後の事象の列 $\mathrm{Ev}_{n+1},\mathrm{Ev}_{n+2},\dots$ が同じなら、 $n+1$ 以後、同じ分類（CONFESSION、OUT_OF_DESCRIPTION_DOMAIN、または同じ $R$ ）と同じ $\mathsf{State}$ をたどる。時点 $n$ の $R_n$ そのものは $q_n$ に依存するので、 $Z_n$ だけでは決まらない（主張は $n+1$ 以後についてである）。

**証明**： $n$ についての帰納法。 $Z_n$ と事象 $\mathrm{Ev}_{n+1}$ が等しければ、上の規則から $q_{n+1}=\rho(a_{n+1})$ 、 $p_{n+1}=p_n+g_p(\mathsf{Phys}_n,a_{n+1})$ 、各要素の $\lambda^{[e]}_{n+1}$ が等しい。付加・除去が等しいので $\mathsf{Active}_{n+1}$ が等しく、付加した要素の宣言厚みも（同じ測定値として）等しい。同じ合成規則により $\tau_{n+1}$ が等しく、 $\delta_{n+1}=q_{n+1}+p_{n+1}$ も等しい。第3部段5の分類の順序は同じ入力に同じ結果を与えるので、分類が等しい。 $R_{n+1}$ が定まる場合はそれが等しく、 $\ell_{n+1}$ と $\mathsf{State}_{n+1}$ も等しい。よって $Z_{n+1}$ も等しい。∎

要素が一つの場合は、構成が $\{0\}$ で、宣言厚み $\tau_0$ は評価宣言で決まっているので、 $Z_n$ は $(p_n,\lambda_n,\ell_n)$ に戻る。

**意味**：

- 判定のためには、長い履歴 $\mathsf{History}$ を $Z_n$ へ要約してよい。
- **要約が十分かどうかは、更新規則の形で決まる**。例えば金属疲労のように、これまでの繰返し回数で劣化の進み方が変わる領域では、繰返し回数を $Z_n$ の欄（領域の追加状態）に加えなければならない。冷却のように $q_n=\rho(q_{n-1},a_n)$ とする領域（段5）では、 $q_n$ を欄に加える。消してよい欄は、宣言した規則が決める。名前付きの欄にしておけば、状態を加えたときに要約の更新漏れを欄の有無で検査できる。
- 構造証言・監査のためには、 $\mathsf{History}$ そのものを保持する。**判定用要約 $Z$ と証言用記録 $\mathsf{History}$ は役割が違う**。

参考：「以後の振る舞いが同じになる履歴を同一視する」という考え方は、オートマトン理論のMyhill–Nerode同値と似た構造を持つ。ただし上の証明はその理論に依存しておらず、本書の前提だけで閉じている。

---

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
