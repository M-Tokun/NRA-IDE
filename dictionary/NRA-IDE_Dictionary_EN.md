# NRA-IDE Dictionary (English Version)

**Version:** 1.0 (draft)  
**Author:** M-Tokuni  
**Document role:** A dictionary for looking up NRA-IDE terms, symbols, and fixed names. It neither creates nor changes canonical definitions  
**Paired Japanese version:** [NRA-IDE_Dictionary_JP.md](./NRA-IDE_Dictionary_JP.md)

---

## 0. About this dictionary

### 0.1 Role

This dictionary lets you look up, in one place, the meaning, notation, permitted uses, and common confusions of the terms, symbols, and fixed names (API and output names) used in NRA-IDE. It neither creates nor changes canonical definitions. Where meanings or symbol reservations conflict, the precedence order of `theory/AXIOMS.md` §16 and `FORMULA.md` §7 govern. This dictionary holds no reservation authority of its own.

Both the author and AI agents consult this dictionary before writing a term or symbol. When a new confusion is found, it is added with a date to the "Confusion notes" of the relevant entry, and a line is added to Section 5.

### 0.2 How to look things up

| What you are looking for | Section |
|---|---|
| An English term | Section 1, Terms (alphabetical) |
| A symbol ( $\delta$ , $\mathsf{Decl}$ , $\Delta$ , etc.) | Section 2, Symbols |
| A fixed name (`delta`, `irreversible_latched`, etc.) | Section 3, Fixed names |
| Index and label conventions | Section 4 |
| When what was confused | Section 5, Confusion log |

Each entry carries an **entry ID** shared with the Japanese version (e.g., `absorption-thickness`). The same entry in the two versions is linked by this ID.

### 0.3 Fields of an entry

| Field | Content |
|---|---|
| Symbol / fixed name | The mathematical display, and the name in APIs and outputs |
| Type / unit | Structural quantity (Cause-Side), evaluation output, evaluation state, gauge, target state, declaration, map, index, or record; and the unit |
| Meaning | A summary of the canonical definition and its source. The source governs |
| Origin / permitted uses / prohibited uses | Where the value comes from, and where it may or may not be used as input |
| Notation | How it is written in this repository |
| Confusion notes | Past confusions (dated) |
| Reading risk | Meanings an English reader may wrongly take. Marked [Confirmed] or [Unconfirmed] |
| Related | Related entries |

### 0.4 Naming precedence

1. Canonical notation in `theory/AXIOMS.md`
2. Machine-readable names in `theory/axioms.json`
3. Public arguments and output fields of the normative reference implementation (`nra-core/foundations/NRA-IDE_Architecture_public.py`)
4. Symbol reservations in `FORMULA.md`
5. Only where no name exists, a new fixed name is proposed

Temporary variables used only inside an implementation (for example, the internal `ratio` in the reference implementation) are distinguished from public fixed names.

### 0.5 General notation rules

**Typeface** (following ISO 80000-2)

| Kind | Typeface | Examples |
|---|---|---|
| Variables and physical quantities | Italic | $\delta$ , $\tau$ , $q_n$ , $x$ |
| Mathematical operators and predefined functions | Upright | $\mathrm{d}$ (differential), $\partial$ , $\int$ , $\sum$ , $\prod$ , $\sin$ , $\ln$ , $\exp$ , $\lim$ , $\max$ |
| Subscripts that are variables | Italic | $i$ in $\sum_i x_i$ ; $e$ in $\tau^{[e]}$ |
| Subscripts that are names or descriptions (labels) | Upright | $R_{\mathrm{warn}}$ , $\tau_{\mathrm{upper}}$ , $q^{\mathrm{temp}}$ |
| Dimensions | Upright sans-serif capitals | length $\mathsf{L}$ , mass $\mathsf{M}$ , time $\mathsf{T}$ , electric current $\mathsf{I}$ , thermodynamic temperature $\mathsf{\Theta}$ , amount of substance $\mathsf{N}$ , luminous intensity $\mathsf{J}$ |
| Writing a dimension | Square brackets | $[F]=\mathsf{L}\,\mathsf{M}\,\mathsf{T}^{-2}$ ; a dimensionless quantity has $[Z]=1$ |

**Repository rule**: within the same document or implementation, distinct meanings must not be distinguished solely by font, letter case, typeface, or decoration. Distinct meanings use distinct base names. Standard mathematical operators, labels, and dimension symbols are outside this rule. The rule is to be proposed for `FORMULA.md` §7 and is not yet normative. However, FORMULA §7 already contains one sentence on distinguishing the transition phase $\mathrm{Phase}$ from $\Phi(x)$ (v2.4).

**Differences from current canonical notation (not yet reflected)**: in FORMULA.md, the differential in §4.7 is an italic $d$ , and the dimension symbols in §5.2 are italic $X$ and $T$ . These differ from the typeface rules above. Any change to the canon will be presented individually in diff ④. The residual $r$ and the boundary approach ratio $R$ in FORMULA.md §5 differ only by case; whether to rename or to exempt it will be decided in diff ④.

### 0.6 Marks for "Reading risk"

- [Confirmed]: confirmed by the author
- [Unconfirmed]: proposed by AI; awaiting the author's confirmation

---

## 1. Terms (alphabetical)

<a id="absorption-thickness"></a>
### Absorption Thickness
- Japanese: [吸収厚み](./NRA-IDE_Dictionary_JP.md#absorption-thickness)
- Symbol / fixed name: $\tau$ / `tau` (output `observed_tau`)
- Type / unit: structural quantity (Cause-Side); $u$
- Meaning: the thickness with which a structure can absorb accumulated deviation; the total width from the reference to rupture. Source: AXIOMS §4, §7; FORMULA §1
- Origin: Cause-Side observation, a transformation rule fixed before evaluation, or the addition of a structural element (measured at the time of addition)
- Permitted uses: computing $R$ , physical laws of the target, structural testimony, audit
- Prohibited uses: increase as spontaneous recovery; update by evaluation outputs
- Notation: the whole structure is $\tau$ ; per element $\tau^{[e]}$ ; at the start of evaluation $\tau_0$
- Confusion notes:
  - Do not confuse with the remainder. The remainder is the [Remaining Absorption Margin](#remaining-absorption-margin) $M_\tau$ (2026-09-26)
  - The only route of increase is the addition of a structural element. Do not write "replenishment" or "repair" (2026-09-29)
  - Do not subtract a temporarily narrowed width from the effective thickness (→ [Temporary Reversible Deviation](#temporary-reversible-deviation)) (2026-09-29)
- Reading risk [Unconfirmed]: do not read "thickness" as the physical thickness of a plate, or "absorption" in the chemical sense. It is the width within which accumulated deviation can be received
- Related: [Declared Thickness](#declared-thickness), [Effective Thickness](#effective-thickness), [Addition of a Structural Element](#structural-element-addition)

<a id="accumulated-deviation"></a>
### Accumulated Deviation
- Japanese: [蓄積ズレ](./NRA-IDE_Dictionary_JP.md#accumulated-deviation)
- Symbol / fixed name: $\delta$ / `delta` (output `observed_delta`)
- Type / unit: structural quantity (Cause-Side); $u$
- Meaning: the deviation measured from a reference state fixed before evaluation, in the direction of the declared rupture. It consists of a reversible component and residual deviation, and carries history because the reference is not moved. Source: AXIOMS §4, §5; FORMULA §1
- Prohibited uses: update by values derived from Effect-Side (reverse derivation A)
- Confusion notes: the canon did not state how "delta is not merely an instantaneous value" relates to "it contains a reversible component that decreases when the action is removed" (settled in v2.2; 2026-09-28)
- Reading risk [Unconfirmed]: do not read "deviation" as the statistical deviation (standard deviation)
- Related: [Reversible Deviation](#reversible-deviation), [Residual Deviation](#residual-deviation), [Reference State](#reference-state)

<a id="active-elements"></a>
### Active Elements
- Japanese: [構成](./NRA-IDE_Dictionary_JP.md#active-elements)
- Symbol / fixed name: $\mathsf{Active}_n$ / `active_elements`
- Type: set
- Meaning: the set of structural elements included in the evaluation target at step $n$ (added and not yet removed). Source: FORMULA §0.5.4
- Confusion notes:
  - it differed from the instantaneous classification $C_0$ and link conditions C1–C4 only by typeface and case; the classification and the conditions were renamed (2026-09-29)
  - it was formerly written $\mathcal{C}_n$; after AXIOMS v2.4 made constraint $C$ a canonical symbol, the two differed only by decoration, so this side was renamed (2026-09-29)
- Related: [Thickness Composition Rule](#thickness-composition-rule), [Structural Element](#structural-element)

<a id="structural-element-addition"></a>
### Addition of a Structural Element
- Japanese: [構造要素の付加](./NRA-IDE_Dictionary_JP.md#structural-element-addition)
- Meaning: adding a new structural element to the evaluation target; the only route by which absorption thickness increases. It does not restore the thickness of existing elements. The thickness of an added element is determined by Cause-Side measurement at the time of addition; the combining rule is fixed before evaluation. The agent does not matter (human reinforcement, biological repair). Source: AXIOMS §7, §8
- Prohibited uses: accepting, on the basis of $R$ alone, that an addition has been physically completed or that thickness has increased ( $R$ may trigger a pre-fixed reinforcement operation)
- Confusion notes:
  - Six expressions such as "external replenishment", "exogenous replenishment", "exogenous repair event", and "exogenous restoration operation" coexisted and could be read as something existing returning (2026-09-29)
  - Do not read build-up welding as "the degradation returned"; it is the addition of an element (the repair material) (2026-09-29)
  - Even if reinforcement makes the whole thickness exceed $\tau_0$ , it is not restoration to the initial structure (2026-09-29)
- Reading risk [Unconfirmed]: do not read "addition" as arithmetic addition of numbers
- Related: [Absorption Thickness](#absorption-thickness), [Removal of a Structural Element](#structural-element-removal), [Replenishment](#replenishment), [Repair](#repair)

<a id="applied-action"></a>
### Applied Action
- Japanese: [作用](./NRA-IDE_Dictionary_JP.md#applied-action)
- Symbol / fixed name: $a_n$ / `applied_action`
- Type: input to the target (an observed physical event)
- Meaning: the action applied to the structure at that step. The effect of conditions that temporarily narrow the receiving width (the temporary reversible deviation) is also allocated here. Source: FORMULA §0.5.3
- Confusion notes:
  - before/after in Proposition 2 were written $a$ , $b$ , and the two structures in Proposition 4 $\lambda_a$ , $\lambda_b$ , reusing the letter of the action (2026-09-29)
  - do not confuse with the [Constraint](#external-constraint) $C$ (an external condition). $C$ is not an allocation target; when its effect appears only in $\Delta\lambda_n$ or in the gauge, it does not appear in $a_n$ (2026-09-30)
- Related: [Reversible Deviation](#reversible-deviation), [Constraint](#external-constraint)

<a id="boundary-approach-ratio"></a>
### Boundary Approach Ratio
- Japanese: [境界接近比](./NRA-IDE_Dictionary_JP.md#boundary-approach-ratio)
- Symbol / fixed name: $R=\delta/\tau$ / `R` ( $R_{\mathrm{target}}$ when the target is made explicit)
- Type / unit: evaluation output; dimensionless
- Meaning: the approach ratio to the structural rupture boundary; higher means more dangerous. Source: AXIOMS §5; FORMULA §1
- Permitted uses: state classification, the irreversible latch, audit, structural testimony, pre-fixed physical-control commands. Into another target's thresholds or effective gate widths only in the safe-side direction and without a return path (AXIOMS §14)
- Prohibited uses: the gauge of the same target (reverse derivation B); target states
- Notation: when a physical law depends on a load ratio, compute it inside the law directly from Cause-Side $\delta$ and $\tau$ and write $g(\delta,\tau,\dots)$ . Do not name that ratio $R$
- Confusion notes:
  - The permitted uses were once written too narrowly as "only thresholds, gates, and physical control" (2026-09-29). The correct scope is above
  - Another structure's $R^{(i)}$ had been fed directly into this structure's degradation (2026-09-29). What enters is the observed physical event
  - Do not reuse it as a safety score or retention rate (AXIOMS §5)
- Reading risk [Unconfirmed]: some docs translate it as "structural ratio", which diverges from FORMULA
- Related: [Evaluation Output](#evaluation-output), [Reverse Derivation](#reverse-derivation)

<a id="warning-threshold"></a>
### Boundary Warning Point
- Japanese: [境界接近警告点](./NRA-IDE_Dictionary_JP.md#warning-threshold)
- Symbol / fixed name: $R_{\mathrm{warn}}$ / `r_warn` (output `thresholds.R_warn`)
- Type: gauge (threshold)
- Meaning: the point at which boundary-approach warning starts. Source: AXIOMS §9, §10.2
- Prohibited uses: change by evaluation outputs
- Related: [Pre-Boundary Human Handoff Point](#handoff-threshold), [Irreversible Transition Onset](#irreversible-threshold)

<a id="complete-rupture-boundary"></a>
### Complete Rupture Boundary
- Japanese: [完全破断境界](./NRA-IDE_Dictionary_JP.md#complete-rupture-boundary)
- Symbol / fixed name: $R=1.0$ / `RUPTURE_BOUNDARY` (state name)
- Meaning: the boundary at which the remaining absorption margin of the target declared before evaluation is exhausted. Source: AXIOMS §9, §10.5
- Confusion notes: do not equate the rupture of a part with the rupture of the whole (a part's rupture is an event for the whole). Do not reinterpret $\tau=0$ as complete rupture (→ [Out of Domain](#out-of-domain))
- Related: [Boundary Approach Ratio](#boundary-approach-ratio)

<a id="confession"></a>
### Confession
- Japanese: [告白](./NRA-IDE_Dictionary_JP.md#confession)
- Fixed name: `CONFESSION` (output `status`)
- Type: classification (a stop signal for the unknown)
- Meaning: output when a required variable, unit, time, provenance, target, or domain rule is unknown; when a value is invalid or non-finite; or when Cause-Side and Effect-Side cannot be distinguished. Source: AXIOMS §6, §10.6
- Prohibited uses: reporting a known danger approach or a known state transition
- Reading risk [Unconfirmed]: do not read "confession" in its religious or legal sense. It is a stop signal that structures the unknown
- Related: [Not Observable](#not-observable)

<a id="external-constraint"></a>
### Constraint
- Japanese: [制約](./NRA-IDE_Dictionary_JP.md#external-constraint)
- Symbol / fixed name: $C$ / `external_constraint`
- Type: auxiliary structural quantity (Cause-Side)
- Meaning: an external load, restraint, or environmental condition acting on the target structure. A quantity with a value $C_n$ at each step, as a component of the observation $o_n$ . What counts as $C$ (kind, source, unit, conversion rule) is written in words in the evaluation declaration. Source: AXIOMS §4.5, FORMULA §7
- Origin: Cause-Side observation; transformation rules fixed before evaluation
- Prohibited uses: obtaining it from evaluation outputs ( $R$ , the canonical state, the irreversible latch, or their aggregates); direct allocation into accumulated deviation or absorption thickness (allocation is to exactly one of $a_n$ , $\Delta p_n$ , $\Delta\lambda_n$ )
- Confusion notes:
  - it differed from the former symbol $\mathcal{C}_n$ of active elements only by decoration; the active-elements side was renamed to $\mathsf{Active}_n$ (2026-09-29)
  - distinguish it from "constraint" as a general word meaning a condition; for example, "the constraint $\tau_{\mathrm{restored}}<\tau_0$ " means a condition (2026-09-29)
  - $C$ is a condition; the [Applied Action](#applied-action) $a_n$ is an allocated action. What is allocated into $\delta$ or $\tau$ is exactly one of $a_n$ , $\Delta p_n$ , $\Delta\lambda_n$ ; $C$ is never an allocation target. The same factor (such as temperature) may appear in both $C$ and $a_n$ without double counting (2026-09-30)
- Reading risk [Unconfirmed]: English constraint is easily read as a constraint in optimization. Here it is a load acting from outside
- Related: [Applied Action](#applied-action), [Active Elements](#active-elements), [Evaluation Declaration](#evaluation-declaration)

<a id="decision-sufficient-state"></a>
### Decision-Sufficient State
- Japanese: [判定用十分状態](./NRA-IDE_Dictionary_JP.md#decision-sufficient-state)
- Symbol / fixed name: $Z_n$ / `decision_sufficient_state`
- Type: a record with named fields
- Meaning: a state sufficient to determine subsequent classifications. Fields: `residual_deviation`, `active_elements` (per element `declared_tau`, `degradation_fraction`, and `domain_memory` if needed), `irreversible_latched`, and if needed `reversible_state` and `domain_global_memory`
- Notation: not a positional tuple. The update rules take only the physical state (excluding the latch) as input
- Confusion notes: the tuple $(p,\lambda,\ell)$ was insufficient once elements became plural (2026-09-29). The update rules had been written with the latch as an input (2026-09-29)
- Related: [Event History](#event-history)

<a id="declared-thickness"></a>
### Declared Thickness
- Japanese: [宣言厚み](./NRA-IDE_Dictionary_JP.md#declared-thickness)
- Symbol / fixed name: $\tau_0$ / `initial_tau` (argument of `DynamicTauEngine` in the reference implementation)
- Type / unit: structural quantity (Cause-Side); $u$
- Meaning: the absorption thickness of the whole structure at the start of evaluation (before transition). With several elements, $\tau_0=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_0)_{e\in\mathsf{Active}_0}\bigr)$ . Source: AXIOMS §7 (initial absorption thickness), §8 (baseline absorption thickness); FORMULA §0.5.1, §0.5.4
- Confusion notes: writing it as "a special form for a single element only" diverged from the canon (2026-09-29)
- Related: [Absorption Thickness](#absorption-thickness), [Restored Absorption Thickness](#restored-thickness)

<a id="degradation-fraction"></a>
### Degradation Fraction
- Japanese: [劣化度](./NRA-IDE_Dictionary_JP.md#degradation-fraction)
- Symbol / fixed name: $\lambda^{[e]}_n$ / `element_degradation_fraction` ( $\lambda_n$ for a single element)
- Type: target state (dimensionless, $0\le\lambda\le1$ )
- Meaning: the fraction of an element's thickness that has been lost; $\tau^{[e]}_n=(1-\lambda^{[e]}_n)\tau^{[e]}_0$ . It does not decrease during an evaluation. Source: FORMULA §0.5.4
- Notation: general formulas use per-element $\lambda^{[e]}_n$ ; $\lambda_n$ is used only in single-element formulas
- Confusion notes: after elements became plural, the single-element $\lambda_n$ and $\tau_0$ continued to be used as the whole state, which spread to the primary formula, the lemmas, and Proposition 5 (2026-09-29)
- Related: [Structural Element](#structural-element)

<a id="dominant-side"></a>
### Dominant Side
- Japanese: [支配側](./NRA-IDE_Dictionary_JP.md#dominant-side)
- Symbol / fixed name: $D$ / `dominant_side`
- Type: auxiliary output
- Meaning: the side with the larger side-specific ratio. Source: FORMULA §4.6
- Confusion notes: the evaluation declaration had been written $\mathcal{D}$ , differing only by typeface. The declaration was renamed $\mathsf{Decl}$ (2026-09-29)

<a id="effective-thickness"></a>
### Effective Thickness
- Japanese: [実効厚み](./NRA-IDE_Dictionary_JP.md#effective-thickness)
- Symbol: $\tau_n$
- Meaning: the thickness of the whole structure at step $n$ used in the primary formula. It does not increase without the addition of a structural element. Source: FORMULA §0.5.4
- Related: [Absorption Thickness](#absorption-thickness), [Side-Specific Effective Gate Width](#side-specific-gate-width)

<a id="entropy-quantity"></a>
### Entropy Quantity
- Japanese: [エントロピー相当量](./NRA-IDE_Dictionary_JP.md#entropy-quantity)
- Symbol / fixed name: $\mathrm{entropy}$ / `entropy_quantity`
- Type: auxiliary structural quantity (optional; Cause-Side)
- Meaning: a domain-specific entropy-like quantity, used only when a domain fixes its definition and calculation rule. Source: AXIOMS §4.5, FORMULA §7
- Origin: Cause-Side observation; transformation rules fixed before evaluation
- Prohibited uses: obtaining it from evaluation outputs ( $R$ , the canonical state, the irreversible latch, or their aggregates)
- Notation: do not write it as $S$ ( $S$ is [Structural Sensitivity](#structural-sensitivity)). A remainder not carried to the next stage in a discrete transition is a separate concept called `entropy_export` (not a measurement of thermodynamic entropy; AXIOMS §4.5, docs Chapter 08)
- Reading risk [Unconfirmed]: easily read as a measured value of thermodynamic entropy
- Related: [Structural Sensitivity](#structural-sensitivity)

<a id="evaluation-archive"></a>
### Evaluation Archive
- Japanese: [保管記録](./NRA-IDE_Dictionary_JP.md#evaluation-archive)
- Symbol / fixed name: $\mathsf{Archive}$ / `evaluation_archive`
- Meaning: the sequence of records of finished evaluations. Not rewritten
- Confusion notes: formerly written $\mathcal{A}$ , differing only by typeface from the photosynthesis rate $A$ in an example (2026-09-29)

<a id="evaluation-declaration"></a>
### Evaluation Declaration
- Japanese: [評価宣言](./NRA-IDE_Dictionary_JP.md#evaluation-declaration)
- Symbol / fixed name: $\mathsf{Decl}$ / `evaluation_declaration`
- Type: declaration (fixed before evaluation)
- Meaning: the set of commitments fixed before computation begins. Required elements: target and rupture mode, unit, observations and provenance, thresholds, handling of missing or unobservable data, reference state, projection rule, allocation rule, declared thickness, composition rule. Optional elements: the mapping of the sequence of evaluations to structural continuity $\omega$ , and the identification of external conditions (constraint $C$ ). Source: FORMULA §0.5.1
- Confusion notes: formerly written $\mathcal{D}$ , differing only by typeface from the dominant side $D$ (2026-09-29)
- Related: [Evaluation Snapshot](#evaluation-snapshot)

<a id="evaluation-gauge"></a>
### Evaluation Gauge
- Japanese: [計器](./NRA-IDE_Dictionary_JP.md#evaluation-gauge)
- Symbol / fixed name: $\mathsf{Gauge}^{(\mathrm{self})}$ / `evaluation_gauge`
- Type: gauge record
- Meaning: the reference state, projection rule, thresholds, shape-transformation functions, smoothing coefficients, and effective gate widths that measure the target
- Prohibited uses: change by the evaluation outputs of the same target (reverse derivation B)
- Confusion notes: it was formerly written $\mathcal{K}^{(\mathrm{self})}$; it differed from the knee value $k$ of FORMULA §5.5 only by case and decoration, so it was renamed (2026-09-29)
- Related: [Reverse Derivation](#reverse-derivation)

<a id="evaluation-output"></a>
### Evaluation Output
- Japanese: [評価出力](./NRA-IDE_Dictionary_JP.md#evaluation-output)
- Symbol / fixed name: $\mathsf{Out}^{(\mathrm{self})}_n$ / `evaluation_output`
- Meaning: $R$ , the canonical state, and the irreversible latch. Neither Cause-Side observations nor Effect-Side artifacts; outputs computed from Cause-Side inputs by pre-fixed rules. Source: AXIOMS §14 (including side-specific ratios is the derivation document's reading)
- Permitted uses: audit, structural testimony, state classification, pre-fixed physical-control commands. Into another target's thresholds or effective gate widths only in the safe-side direction and without a return path
- Prohibited uses: the gauge of the same target (reverse derivation B); target states
- Notation: formerly written $\mathcal{Y}^{(\mathrm{self})}_n$. There was no collision, but it was renamed to align the notation of the three P9 categories (target state, gauge, evaluation output) (2026-09-29)
- Confusion notes: the permitted uses were once written too narrowly as "only thresholds, gates, and physical control" (2026-09-29)
- Related: [Boundary Approach Ratio](#boundary-approach-ratio), [Reverse Derivation](#reverse-derivation)

<a id="evaluation-snapshot"></a>
### Evaluation Snapshot
- Japanese: [評価スナップショット](./NRA-IDE_Dictionary_JP.md#evaluation-snapshot)
- Meaning: the set fixed for one evaluation: target, update authority, provenance, unit, time, transformation rule, threshold rule. New authorized Cause-Side observations may update the next snapshot. Source: FORMULA §6; AXIOMS §14
- Notation: when a new observation changes the declared thickness, do not treat it as an increase during the evaluation; redeclare it as the next evaluation snapshot
- Confusion notes: writing "the structure changed" invites "degeneration", and writing "remeasurement" invites "correction of the past". Write "the next evaluation snapshot" (2026-09-29)
- Related: [Evaluation Declaration](#evaluation-declaration)

<a id="evaluation-state"></a>
### Evaluation State
- Japanese: [評価状態](./NRA-IDE_Dictionary_JP.md#evaluation-state)
- Meaning: what is held as an evaluation output, such as the irreversible latch. Distinct from both the target's physical state and the event history
- Related: [Irreversible Latch](#irreversible-latch), [Target Physical State](#target-physical-state)

<a id="event-allocation-rule"></a>
### Event Allocation Rule
- Japanese: [分解規則](./NRA-IDE_Dictionary_JP.md#event-allocation-rule)
- Symbol / fixed name: $\mathsf{Alloc}$ / `event_allocation_rule`
- Type: map (fixed before evaluation)
- Meaning: the rule that counts each observed change in **exactly one** of: the action, the increment of residual deviation, or the increment of degradation (one change, one count). The context, authority, and provenance $\mathrm{ctx}_n$ are not a destination. Source: FORMULA §0.5.3
- Confusion notes: formerly written $\Lambda$ , differing only by case from the degradation fraction $\lambda$ (2026-09-29)
- Related: [Observation Event](#observation-event)

<a id="event-history"></a>
### Event History
- Japanese: [経路履歴](./NRA-IDE_Dictionary_JP.md#event-history)
- Symbol / fixed name: $\mathsf{History}_n$ / `event_history`
- Type: testimony record
- Meaning: the record sequence of events $\mathrm{Ev}_1,\dots,\mathrm{Ev}_n$ . It always grows and is never rewritten
- Notation: appending is $\mathsf{History}_n=\mathsf{History}_{n-1}\oplus\mathrm{Ev}_n$ ; the number of records is $\#\mathsf{History}_n$
- Confusion notes:
  - Formerly written $\mathcal{H}_n$ , differing only by case and typeface from the shape-transformation function $h$ (2026-09-29)
  - The number of records was written with $\lvert\cdot\rvert$ , the same as the absolute value (2026-09-29)
  - Do not mix the event history (a record for testimony) with the physical state or the evaluation state (2026-09-29)
- Related: [Decision-Sufficient State](#decision-sufficient-state)

<a id="instantaneous-classification"></a>
### Instantaneous Classification
- Japanese: [瞬間分類](./NRA-IDE_Dictionary_JP.md#instantaneous-classification)
- Symbol / fixed name: $\mathrm{Class}(R)$ / `instantaneous_classification`
- Meaning: the canonical classification by the interval of a valid $R$ (before the latch is applied)
- Confusion notes: formerly written $C_0(R)$ (2026-09-29)
- Related: [Target Boundary State](#target-state)

<a id="inverse-projection"></a>
### Inverse Projection
- Japanese: [逆射影](./NRA-IDE_Dictionary_JP.md#inverse-projection)
- Symbol: $\Pi^{-1}$
- Meaning: the name of a prohibited reverse path. Not the mathematical inverse map of the projection $\Pi$ . Source: SANDWICH_ARCH §8.3, §8.4
- Reading risk [Unconfirmed]: do not read it as the inverse of a linear-algebra projection
- Related: [Projection](#projection), [Reverse Derivation](#reverse-derivation)

<a id="irreversible-latch"></a>
### Irreversible Latch
- Japanese: [不可逆ラッチ](./NRA-IDE_Dictionary_JP.md#irreversible-latch)
- Symbol / fixed name: $\ell_n$ / `irreversible_latched`
- Type: evaluation state (Boolean)
- Meaning: once $R_{\mathrm{irrev}}$ is reached, it is not released automatically; $\ell_n=\ell_{n-1}\lor\mathbf{1}\{R_n\ge R_{\mathrm{irrev}}\}$ . Source: AXIOMS §10.4
- Notation: the fixed name is `irreversible_latched` (not `irreversible_latch`)
- Confusion notes: it is not released automatically by repair or addition. When redeclaring, state in the new declaration that the previous evaluation was latched (2026-09-29). Do not use it as an input to physical laws (2026-09-29)
- Reading risk [Unconfirmed]: do not read "latch" as an electronic latch that can be reset
- Related: [Irreversible Transition Onset](#irreversible-threshold)

<a id="irreversible-threshold"></a>
### Irreversible Transition Onset
- Japanese: [不可逆遷移開始点](./NRA-IDE_Dictionary_JP.md#irreversible-threshold)
- Symbol / fixed name: $R_{\mathrm{irrev}}$ / `r_irrev` (output `thresholds.R_irrev`)
- Type: gauge (threshold)
- Meaning: the point of entry into irreversible transition, after which the original structural state cannot be returned to; $R_{\mathrm{handoff}}<R_{\mathrm{irrev}}<1.0$ . Source: AXIOMS §9, §10.4

<a id="not-observable"></a>
### Not Observable
- Japanese: [観測不能](./NRA-IDE_Dictionary_JP.md#not-observable)
- Fixed name: `NOT_OBSERVABLE`
- Type: observation-channel state
- Meaning: no value can be obtained from the observation path. Output together with the reason for the missing data. Source: AXIOMS §10.2, §11.1, §11.2
- Prohibited uses: reinterpretation as CONFESSION; filling as zero, stable, or recovered
- Confusion notes: an unobservable event had been sent to CONFESSION (2026-09-28). Conversely, inputs with unknown target, unit, or provenance had once been sent to missing-data handling (2026-09-28)
- Related: [Confession](#confession)

<a id="observation-event"></a>
### Observation Event
- Japanese: [観測事象](./NRA-IDE_Dictionary_JP.md#observation-event)
- Symbol / fixed name: $\mathrm{Ev}_n$ / `observation_event`
- Type: event record (target, value, unit, provenance, time, uncertainty, order, observation path)
- Meaning: the event at update step $n$ . It advances the state from $n-1$ to $n$ . Source: FORMULA §0.5.2
- Notation: write $\mathrm{Ev}$ . $E$ is not used, so that it is not distinguished from the structural element $e$ only by case
- Confusion notes: $E_n$ and the element index $e$ differed only by case (2026-09-29)
- Related: [Event History](#event-history), [Event Allocation Rule](#event-allocation-rule)

<a id="observation-projection-rule"></a>
### Observation Projection Rule
- Japanese: [射影規則](./NRA-IDE_Dictionary_JP.md#observation-projection-rule)
- Symbol / fixed name: $\sigma$ / `observation_projection_rule`
- Type: map (fixed before evaluation)
- Meaning: the rule that maps an observation to the deviation measured from the reference state in the declared rupture direction; $\delta_n=\sigma(o_n)$ . Source: FORMULA §0.5.2
- Confusion notes: distinct from the projection $\Pi$ of SANDWICH_ARCH (2026-09-29)
- Related: [Projection](#projection)

<a id="observation-value"></a>
### Observation Value
- Japanese: [観測値](./NRA-IDE_Dictionary_JP.md#observation-value)
- Symbol / fixed name: $o_n$ / `observation_value`
- Type: Cause-Side input
- Meaning: a Cause-Side observation (may be multivariate), mapped to accumulated deviation by the projection rule. Source: FORMULA §0.5.2
- Confusion notes: formerly written $x_n$ , the same glyph as the computational state $x$ in FORMULA §5 (2026-09-29)
- Related: [Observation Projection Rule](#observation-projection-rule)

<a id="other-target"></a>
### Other Target
- Japanese: [他構造](./NRA-IDE_Dictionary_JP.md#other-target)
- Symbol / fixed name: $(i)$ / `other_target_index`
- Meaning: another structure, or a substructure, that affects this one. Its observed physical state enters this structure as an observation event. Its evaluation outputs may be used here for recording in audit and structural testimony, as safe-side gauge inputs, and as pre-fixed physical-control commands; they do not enter this structure's target state
- Related: [Subject Target](#subject-target)

<a id="out-of-domain"></a>
### Out of Domain
- Japanese: [定義域外](./NRA-IDE_Dictionary_JP.md#out-of-domain)
- Symbol / fixed name: $\emptyset$ / `OUT_OF_DESCRIPTION_DOMAIN` (output `status`)
- Meaning: the case $\tau=0$ ; $R$ cannot be defined. Source: AXIOMS §1, §6, §10.7
- Notation: in this repository $\emptyset$ means "out of domain". It is not used for the empty set; write "empty" in words
- Prohibited uses: replacing $R$ with infinity; reinterpretation as RUPTURE_BOUNDARY
- Confusion notes: with discrete updates, if $\lambda$ reaches 1 in one step, the classification is out of domain even when the previous $R$ was below 1 (2026-09-28)
- Related: [Complete Rupture Boundary](#complete-rupture-boundary)

<a id="handoff-threshold"></a>
### Pre-Boundary Human Handoff Point
- Japanese: [境界前人間委譲点](./NRA-IDE_Dictionary_JP.md#handoff-threshold)
- Symbol / fixed name: $R_{\mathrm{handoff}}$ / `r_handoff` (output `thresholds.R_handoff`)
- Type: gauge (threshold)
- Meaning: the point at which autonomous new judgment and operation stop and are handed to an external human. Only execution authority moves. Source: AXIOMS §1, §9, §10.3
- Notation: the old names `R_op`, `Rop`, `rop`, `r_op` are compatibility inputs only and are not used in new documents
- Reading risk [Unconfirmed]: do not read "handoff" as transferring responsibility. Responsibility, legal liability, and knowledge do not move (AXIOMS §10.3)
- Related: [Boundary Warning Point](#warning-threshold)

<a id="projection"></a>
### Projection
- Japanese: [射影](./NRA-IDE_Dictionary_JP.md#projection)
- Symbol: $\Pi$
- Meaning: the operation that selects only Effect-Side content permitted by the current boundary state. Not an invertible map. Source: SANDWICH_ARCH §8.2
- Related: [Inverse Projection](#inverse-projection), [Observation Projection Rule](#observation-projection-rule)

<a id="reference-state"></a>
### Reference State
- Japanese: [基準状態](./NRA-IDE_Dictionary_JP.md#reference-state)
- Type: declaration
- Meaning: the origin from which accumulated deviation is measured. Fixed before evaluation and not reset during it; redeclaration only between evaluations. Source: AXIOMS §4
- Confusion notes: an earlier draft wrote $x_{\mathrm{ref}}$ , which could be confused with the reference state $x_{\mathrm{exact}}$ of FORMULA §5–§6; it is written in words without a symbol (2026-09-28)
- Related: [Accumulated Deviation](#accumulated-deviation), [Straightening](#straightening)

<a id="remaining-absorption-margin"></a>
### Remaining Absorption Margin
- Japanese: [残存吸収余白](./NRA-IDE_Dictionary_JP.md#remaining-absorption-margin)
- Symbol / fixed name: $M_\tau=\tau-\delta$ / `remaining_absorption_margin` (old name `remaining_slack` is deprecated)
- Type / unit: derived output; $u$
- Meaning: the part of the thickness not yet entered by deviation. Source: AXIOMS §5; FORMULA §2
- Confusion notes:
  - do not confuse with the absorption thickness (total width) (2026-09-26)
  - it was also called 残存吸収余裕 (AXIOMS §5) and 残存構造余裕 / "remaining structural margin" (AXIOMS §10.5, Thesis, docs); the Japanese name was unified to 余白 (2026-09-30)
- Reading risk [Unconfirmed]: do not read "margin" as a profit margin or a safety factor
- Related: [Remaining Ratio Margin](#remaining-ratio-margin)

<a id="remaining-ratio-margin"></a>
### Remaining Ratio Margin
- Japanese: [残存比率余白](./NRA-IDE_Dictionary_JP.md#remaining-ratio-margin)
- Symbol / fixed name: $M_R=1-R$ / `remaining_ratio_margin`
- Type / unit: derived output; dimensionless
- Meaning: Source: AXIOMS §5; FORMULA §2. Do not use the ambiguous single name `remaining margin`
- Notation: "ratio" means a margin measured on the scale of the boundary approach ratio $R$ . Its value equals $M_\tau/\tau$ ( $M_R=1-R=(\tau-\delta)/\tau$ )
- Confusion notes: AXIOMS §5 called it "dimensionless boundary margin" (境界余裕). Because the Japanese 余裕 is also used to describe the total width $\tau$ (AXIOMS §3, §4), the quantity names were unified to 余白 (2026-09-30)

<a id="structural-element-removal"></a>
### Removal of a Structural Element
- Japanese: [構造要素の除去](./NRA-IDE_Dictionary_JP.md#structural-element-removal)
- Meaning: planned removal of an undamaged structural element. It is not degradation and is not counted in the degradation fraction; the thickness decreases. Returning a removed element is treated anew as addition. Source: AXIOMS §7
- Confusion notes: there was no classification for removing a healthy element (such as scaling in a server), so it could only be recorded as "broken" (2026-09-29)
- Related: [Addition of a Structural Element](#structural-element-addition)

<a id="repair"></a>
### Repair → see [Addition of a Structural Element](#structural-element-addition)
- Japanese: [補修](./NRA-IDE_Dictionary_JP.md#repair)
- May be used as an everyday word. In formulas it is treated as the addition of an element (the repair material); the degradation of existing elements does not decrease
- Confusion notes: the notation subtracting a "repair recovery" $\eta$ from the degradation fraction was abolished (2026-09-29)

<a id="replenishment"></a>
### Replenishment → see [Addition of a Structural Element](#structural-element-addition)
- Japanese: [補充](./NRA-IDE_Dictionary_JP.md#replenishment)
- Not a canonical term. "External replenishment", "exogenous replenishment", and "exogenous replenishment operation" up to AXIOMS v2.2 were changed to "addition of a structural element" in v2.3
- Confusion notes: it can be read as existing thickness returning (2026-09-29)

<a id="residual-deviation"></a>
### Residual Deviation
- Japanese: [残留ズレ](./NRA-IDE_Dictionary_JP.md#residual-deviation)
- Symbol / fixed name: $p_n$ / `residual_deviation`
- Type: target state
- Meaning: the part of accumulated deviation that remains after the action is removed (the irreversible component). It does not decrease during an evaluation. Source: AXIOMS §4, §7; FORMULA §0.5.3
- Notation: with backward differences, $p_n=p_{n-1}+\Delta p_n$ and $p_n=p_0+\sum_{m=1}^{n}\Delta p_m$
- Confusion notes: residualDebt and $D_{\mathrm{long}}$ in the demos are quantities built from $R$ , not residual deviation (2026-09-29)
- Related: [Reversible Deviation](#reversible-deviation), [Straightening](#straightening)

<a id="restoration"></a>
### Restoration
- Japanese: [復元](./NRA-IDE_Dictionary_JP.md#restoration)
- Meaning: claiming a return to the initial structure. It requires evidence of both comparability and $\tau_{\mathrm{restored}}<\tau_0$ . Source: AXIOMS §8
- Confusion notes: "return of a value", "return of the physical state", and "sameness of history" are separate questions (derivation document, Proposition 2) (2026-09-29)
- Related: [Restored Absorption Thickness](#restored-thickness)

<a id="restored-thickness"></a>
### Restored Absorption Thickness
- Japanese: [復元後の吸収厚み](./NRA-IDE_Dictionary_JP.md#restored-thickness)
- Symbol: $\tau_{\mathrm{restored}}$
- Meaning: the thickness of the existing elements of the successor structure, excluding added elements, evaluated after an operation intended for restoration with the same subject, unit, and measurement rule. Source: AXIOMS §8
- Confusion notes: reading it as the whole thickness including added elements would violate $\tau_{\mathrm{restored}}<\tau_0$ for a reinforced bridge (2026-09-29)

<a id="reverse-derivation"></a>
### Reverse Derivation
- Japanese: [逆導出](./NRA-IDE_Dictionary_JP.md#reverse-derivation)
- Meaning: the following paths are reverse derivation and are prohibited, whether automatic, manual, human-reviewed, authorized, or versioned. Source: AXIOMS §14
  - Reverse derivation A (authority backflow): a path from Effect-Side to a Cause-Side value, threshold, state, irreversible latch, rule, transformation input, update ground, or provenance
  - Reverse derivation B (self-adjustment of the gauge): a path from an evaluation output (including moving averages and aggregates) to the reference, transformation rule, thresholds, or effective gate width of the same target
- Notation: judge by the origin and rewrite target of the path, not by symbol names. Give different names to things of different origin
- Confusion notes: the same symbol $R$ was used both for a stored evaluation output and for a ratio inside a physical law (2026-09-29). The word "reverse derivation" was used in at least nine senses (2026-09-27)
- Reading risk [Unconfirmed]: do not read "derivation" as a derivative or as a mathematical derivation of a result
- Related: [Evaluation Output](#evaluation-output), [Evaluation Gauge](#evaluation-gauge)

<a id="reverse-inference"></a>
### Reverse Inference
- Japanese: [逆推論](./NRA-IDE_Dictionary_JP.md#reverse-inference)
- Meaning: estimating causes by similarity or association. Not an independent class of reverse derivation. Used as input to structural judgment it is reverse derivation A; uses outside structural judgment (such as creative writing) are outside the classification table. Source: SANDWICH_ARCH §8.4
- Confusion notes: in src/README, "Π⁻¹ (reverse inference)" and "Π⁻¹ (reverse derivation)" appear as two meanings of the same symbol (2026-09-28; note not yet reflected)
- Related: [Reverse Derivation](#reverse-derivation)

<a id="reversible-deviation"></a>
### Reversible Deviation
- Japanese: [可逆成分](./NRA-IDE_Dictionary_JP.md#reversible-deviation)
- Symbol / fixed name: $q_n$ / `reversible_deviation`
- Type: target state
- Meaning: the part of accumulated deviation that returns toward the reference when the action is removed. Source: AXIOMS §4; FORMULA §0.5.3
- Notation: determined as $q_n=\sigma(o_n)-p_n$ (FORMULA §0.5.3; derivation document, P5)
- Confusion notes: an earlier draft called it "reversible penetration"; the canonical term is "reversible component" (2026-09-28)
- Reading risk [Unconfirmed]: do not read "reversible" as the thermodynamic reversible (quasi-static) process, nor as "if the value returns, the structure returns". The event history does not return (derivation document, Proposition 2b)
- Related: [Residual Deviation](#residual-deviation), [Accumulated Deviation](#accumulated-deviation)

<a id="side-specific-gate-width"></a>
### Side-Specific Effective Gate Width
- Japanese: [側別有効ゲート幅](./NRA-IDE_Dictionary_JP.md#side-specific-gate-width)
- Symbol / fixed name: $\tau_{\mathrm{upper}}$ , $\tau_{\mathrm{lower}}$ / `tau_upper`, `tau_lower`
- Type: gauge (used only in the secondary formula)
- Meaning: may increase or decrease; does not mean spontaneous recovery of the underlying absorption thickness. Source: FORMULA §4.4
- Prohibited uses: feeding evaluation outputs ( $R$ family) into the shape-transformation functions
- Related: [Effective Thickness](#effective-thickness)

<a id="straightening"></a>
### Straightening
- Japanese: [矯正](./NRA-IDE_Dictionary_JP.md#straightening)
- Meaning: an operation that forces a stretch or bend back. Because it lowers the deviation measured from the fixed reference, it is not handled within an evaluation; the evaluation ends and is redeclared. Source: AXIOMS §7
- Confusion notes: the wording of AXIOMS v2.2, readable as "residual deviation may decrease with a repair event", was changed in v2.3 (2026-09-29)
- Related: [Residual Deviation](#residual-deviation), [Reference State](#reference-state)

<a id="structural-continuity"></a>
### Structural Continuity
- Japanese: [構造連続性](./NRA-IDE_Dictionary_JP.md#structural-continuity)
- Symbol / fixed name: $\omega$ / `omega`
- Type: auxiliary structural quantity (Cause-Side)
- Meaning: indicates whether the structure continues its transition. $\omega>0$ only when continuity is confirmed under a continuous observation or phase-update rule that the domain fixed before evaluation. Source: AXIOMS §1 (notation), §4.5
- Origin: Cause-Side observation; transformation rules fixed before evaluation
- Prohibited uses: obtaining it from evaluation outputs ( $R$ , the canonical state, the irreversible latch, or their aggregates)
- Notation: its mapping to the sequence of evaluations is declared per evaluation as an optional element of the declaration (no general rule; derivation document P0)
- Confusion notes: do not write a missing observation as $\omega=0$ (AXIOMS §4.5). The docs Chapter 12 glossary called it "transition-continuation quantity" (2026-09-29)
- Related: [Transition Phase](#transition-phase)

<a id="structural-element"></a>
### Structural Element
- Japanese: [構造要素](./NRA-IDE_Dictionary_JP.md#structural-element)
- Symbol / fixed name: $e$ / `element_id`
- Type: index
- Meaning: an element constituting the evaluation target. $e=0$ is the structure at declaration; $e\ge1$ are added elements. Each has a declared thickness $\tau^{[e]}_0$ and a degradation fraction $\lambda^{[e]}_n$ . Source: FORMULA §0.5.4
- Related: [Active Elements](#active-elements), [Addition of a Structural Element](#structural-element-addition)

<a id="structural-sensitivity"></a>
### Structural Sensitivity
- Japanese: [構造感度](./NRA-IDE_Dictionary_JP.md#structural-sensitivity)
- Symbol: $S=1/M_\tau$
- Type / unit: derived output; $u^{-1}$
- Meaning: the inverse of the remaining absorption margin. Source: FORMULA §3
- Confusion notes: do not write the entropy quantity $\mathrm{entropy}$ or `entropy_export` as $S$ (AXIOMS §4.5, FORMULA §7) (2026-09-29)
- Related: [Remaining Absorption Margin](#remaining-absorption-margin), [Entropy Quantity](#entropy-quantity)

<a id="structural-testimony"></a>
### Structural Testimony
- Japanese: [構造証言](./NRA-IDE_Dictionary_JP.md#structural-testimony)
- Meaning: continuing to record and report the state of the structure in fixed fields and formats. It does not stop while $R<1.0$ ; at $R\ge1.0$ it switches to post-rupture fixed testimony. Source: AXIOMS §11
- Reading risk [Unconfirmed]: do not read "testimony" in its courtroom sense
- Related: [Event History](#event-history)

<a id="subject-target"></a>
### Subject Target
- Japanese: [自構造](./NRA-IDE_Dictionary_JP.md#subject-target)
- Symbol / fixed name: $(\mathrm{self})$ / `subject_target`
- Meaning: the structure being evaluated. Other structures are $(i)$
- Confusion notes: formerly written with the structure name $G$ (the same glyph as $G(r)$ in FORMULA §5). The proposed $k$ was not adopted because it collides with the knee value $k$ (2026-09-29)
- Related: [Other Target](#other-target)

<a id="target-state"></a>
### Target Boundary State
- Japanese: [状態区分](./NRA-IDE_Dictionary_JP.md#target-state)
- Symbol / fixed name: $\mathsf{State}_n$ / `target_state` (values: `PERMIT`, `BOUNDARY_WARNING`, `HANDOFF_REQUIRED`, `IRREVERSIBLE_TRANSITION`, `RUPTURE_BOUNDARY`)
- Type: canonical state
- Meaning: the state determined by a valid $R$ and the latch. Source: AXIOMS §9–§11.1
- Confusion notes: formerly written $Q_n$ , differing only by case from the reversible component $q_n$ (2026-09-29)
- Related: [Instantaneous Classification](#instantaneous-classification), [Irreversible Latch](#irreversible-latch)

<a id="target-physical-state"></a>
### Target Physical State
- Japanese: [対象状態](./NRA-IDE_Dictionary_JP.md#target-physical-state)
- Symbol / fixed name: $\mathsf{Phys}^{(\mathrm{self})}_n$ / `target_physical_state`
- Type: state record
- Meaning: the target's physical state $(q_n,p_n,(\lambda^{[e]}_n)_{e\in\mathsf{Active}_n})$ . It excludes the evaluation state (latch) and the event history
- Origin: observed physical events; the target's physical laws
- Prohibited uses: reading back evaluation outputs (of this or another structure)
- Confusion notes:
  - only observed physical events enter the target state. Do not mix the physical state, the evaluation state, and the event history (2026-09-29)
  - it was formerly written $\mathcal{W}^{(\mathrm{self})}_n$; it differed from work $W$ of AXIOMS v2.4 only by decoration, so it was renamed (2026-09-29)
- Related: [Evaluation State](#evaluation-state), [Event History](#event-history)

<a id="temporary-reversible-deviation"></a>
### Temporary Reversible Deviation
- Japanese: [一時的な可逆成分](./NRA-IDE_Dictionary_JP.md#temporary-reversible-deviation)
- Symbol / fixed name: $q^{\mathrm{temp}}_n$ / `temporary_reversible_deviation`
- Type: target state (part of the reversible component $q_n$ )
- Meaning: a receiving width temporarily narrowed by an action or condition, counted on the deviation side. It returns to 0 when the condition is removed. Source: AXIOMS §7 interpretive-boundary comment (a temporary thickness reduction is counted as the reversible component); FORMULA §0.5.3
- Notation: not subtracted from the effective thickness; counted by $\mathsf{Alloc}$ as action and included in $q_n$
- Confusion notes: it had been called "temporary thickness reduction" (symbol $\mu_n$ ). Although named as a thickness, it is counted on the deviation side, so it was renamed (2026-09-29)
- Reading risk [Unconfirmed]: do not read "reversible" as the thermodynamic reversible process. Here it means "returns when the condition is removed"
- Related: [Reversible Deviation](#reversible-deviation), [Effective Thickness](#effective-thickness)

<a id="thickness-composition-rule"></a>
### Thickness Composition Rule
- Japanese: [合成規則](./NRA-IDE_Dictionary_JP.md#thickness-composition-rule)
- Symbol / fixed name: $\mathrm{Comp}_\tau$ / `thickness_composition_rule`
- Type: map (fixed before evaluation)
- Meaning: the rule that determines the effective thickness of the whole from element thicknesses; $\tau_n=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_n)_{e\in\mathsf{Active}_n}\bigr)$ . Conditions: non-decreasing in each argument; finite, non-negative, and keeping the unit; equal to the element's thickness for a single element; zero when all elements are zero; and, where removal is allowed within an evaluation, not increasing when an element is removed. Source: FORMULA §0.5.4
- Notation: a sum for parallel elements. For series ( $\min$ ), removing an element can make the whole stronger, so removal is not handled within the evaluation and is treated as a declaration change
- Confusion notes: formerly written $\Gamma$ , differing only by case from the damping coefficient $\gamma$ of FORMULA §5 (2026-09-29). While adding conditions, it was found that imposing "removal does not increase the value" on every form makes series structures unrepresentable (2026-09-29)
- Related: [Active Elements](#active-elements), [Addition of a Structural Element](#structural-element-addition)

<a id="transition-phase"></a>
### Transition Phase
- Japanese: [遷移位相](./NRA-IDE_Dictionary_JP.md#transition-phase)
- Symbol / fixed name: $\mathrm{Phase}$ / `transition_phase`
- Type: auxiliary structural quantity (Cause-Side; internal state)
- Meaning: an internal state showing which stage of transition the target structure occupies, updated under a Cause-Side-derived transition rule. Source: AXIOMS §4.5
- Origin: Cause-Side observation; transformation rules fixed before evaluation
- Prohibited uses: reading it as a spatial coordinate or a model-generated embedding; obtaining it from evaluation outputs
- Notation: spelled $\mathrm{Phase}$ ; $\varphi$ and $\phi$ are not used
- Confusion notes: the draft wrote $\varphi$ , which would differ from the auxiliary computation term $\Phi(x)$ of FORMULA §5.1 only by case, so it was renamed (2026-09-29)
- Reading risk [Unconfirmed]: English phase is easily read as a phase of matter or the phase of a wave. Here it is a stage of transition
- Related: [Structural Continuity](#structural-continuity)

<a id="work-quantity"></a>
### Work
- Japanese: [仕事量](./NRA-IDE_Dictionary_JP.md#work-quantity)
- Symbol / fixed name: $W$ / `work_quantity`
- Type: auxiliary structural quantity (optional; Cause-Side)
- Meaning: an optional quantity used only when a domain fixes its definition, unit, and observation method. Source: AXIOMS §4.5. Not included in the reserved list of FORMULA §7
- Origin: Cause-Side observation; transformation rules fixed before evaluation
- Prohibited uses: obtaining it from evaluation outputs ( $R$ , the canonical state, the irreversible latch, or their aggregates)
- Confusion notes: it differed from the former symbol $\mathcal{W}$ of the target physical state only by decoration; the target-state side was renamed to $\mathsf{Phys}$ (2026-09-29)
- Reading risk [Unconfirmed]: easily read directly as mechanical work (force × displacement). The definition is given by the domain
- Related: [Target Physical State](#target-physical-state)

---

## 2. Symbols

### 2.1 Latin letters

| Symbol | Entry |
|---|---|
| $a_n$ | [Applied Action](#applied-action) |
| $\mathsf{Active}_n$ | [Active Elements](#active-elements) |
| $C$ , $C_n$ | [Constraint](#external-constraint) |
| $\mathrm{Class}(R)$ | [Instantaneous Classification](#instantaneous-classification) |
| $\mathrm{Comp}_\tau$ | [Thickness Composition Rule](#thickness-composition-rule) |
| $\mathrm{ctx}_n$ | context, authority, and provenance ([Event Allocation Rule](#event-allocation-rule)) |
| $D$ | [Dominant Side](#dominant-side) |
| $\mathsf{Decl}$ | [Evaluation Declaration](#evaluation-declaration) |
| $e$ | [Structural Element](#structural-element) |
| $\mathrm{entropy}$ | [Entropy Quantity](#entropy-quantity) |
| $\mathrm{Ev}_n$ | [Observation Event](#observation-event) |
| $\mathrm{EvalGraph}^{(j)}$ | expanded evaluation graph (derivation document, Part 3) |
| $g_p$ , $g^{[e]}_\lambda$ | increment laws of residual deviation and element degradation (physical laws; they do not take evaluation outputs as input) |
| $\mathsf{Gauge}^{(\mathrm{self})}$ | [Evaluation Gauge](#evaluation-gauge) |
| $\mathsf{History}_n$ | [Event History](#event-history) |
| $M_R$ , $M_\tau$ | [Remaining Ratio Margin](#remaining-ratio-margin), [Remaining Absorption Margin](#remaining-absorption-margin) |
| $o_n$ | [Observation Value](#observation-value) |
| $\mathsf{Out}^{(\mathrm{self})}_n$ | [Evaluation Output](#evaluation-output) |
| $p_n$ | [Residual Deviation](#residual-deviation) |
| $\mathrm{Phase}$ | [Transition Phase](#transition-phase) |
| $\mathsf{Phys}^{(\mathrm{self})}_n$ | [Target Physical State](#target-physical-state) |
| $q_n$ , $q^{\mathrm{temp}}_n$ | [Reversible Deviation](#reversible-deviation), [Temporary Reversible Deviation](#temporary-reversible-deviation) |
| $R$ , $R_{\mathrm{target}}$ | [Boundary Approach Ratio](#boundary-approach-ratio) |
| $R_{\mathrm{warn}}$ , $R_{\mathrm{handoff}}$ , $R_{\mathrm{irrev}}$ | [Warning Point](#warning-threshold), [Handoff Point](#handoff-threshold), [Irreversible Transition Onset](#irreversible-threshold) |
| $R_{\mathrm{upper}}$ , $R_{\mathrm{lower}}$ , $R_{\mathrm{dir}}$ | side-specific ratios and directional aggregate (auxiliary; not canonical $R$ ; FORMULA §4.5, §4.6) |
| $S$ | [Structural Sensitivity](#structural-sensitivity) |
| $\mathsf{State}_n$ | [Target Boundary State](#target-state) |
| $u$ | the unit shared by $\delta$ and $\tau$ |
| $\mathsf{Update}$ | update rule (derivation document, Part 3) |
| $W$ | [Work](#work-quantity) |
| $Z_n$ | [Decision-Sufficient State](#decision-sufficient-state) |

### 2.2 Greek letters

| Symbol | Entry |
|---|---|
| $\alpha_u$ , $\alpha_l$ | smoothing coefficients (FORMULA §4.2; fixed names `alpha_upper`, `alpha_lower`) |
| $\gamma$ | damping coefficient (FORMULA §5) |
| $\delta$ , $\delta_{\mathrm{upper}}$ , $\delta_{\mathrm{lower}}$ | [Accumulated Deviation](#accumulated-deviation) (side-specific: FORMULA §4.1) |
| $\epsilon$ | minimum threshold / near-zero (AXIOMS §1) |
| $\ell_n$ | [Irreversible Latch](#irreversible-latch) |
| $\lambda^{[e]}_n$ , $\lambda_n$ | [Degradation Fraction](#degradation-fraction) |
| $\Pi$ , $\Pi^{-1}$ | [Projection](#projection), [Inverse Projection](#inverse-projection) |
| $\rho$ | reversible response (derivation document, Part 3) |
| $\sigma$ | [Observation Projection Rule](#observation-projection-rule) |
| $\tau$ , $\tau_n$ , $\tau_0$ , $\tau^{[e]}_0$ , $\tau_{\mathrm{restored}}$ | [Absorption Thickness](#absorption-thickness), [Effective Thickness](#effective-thickness), [Declared Thickness](#declared-thickness), [Restored Absorption Thickness](#restored-thickness) |
| $\tau_{\mathrm{upper}}$ , $\tau_{\mathrm{lower}}$ | [Side-Specific Effective Gate Width](#side-specific-gate-width) |
| $\Phi(x)$ | auxiliary computation term (FORMULA §5.1); distinct from the transition phase $\mathrm{Phase}$ |
| $\omega$ | [Structural Continuity](#structural-continuity) |

### 2.3 Decorated letters

There are currently no decorated-letter symbols. $\mathcal{C}_n$ , $\mathcal{W}^{(\mathrm{self})}_n$ , $\mathcal{K}^{(\mathrm{self})}$ , and $\mathcal{Y}^{(\mathrm{self})}_n$ were renamed on 2026-09-29 to $\mathsf{Active}_n$ , $\mathsf{Phys}^{(\mathrm{self})}_n$ , $\mathsf{Gauge}^{(\mathrm{self})}$ , and $\mathsf{Out}^{(\mathrm{self})}_n$ , and moved to 2.1.

### 2.4 Operators and relations (outside the rule)

| Display | Meaning | Note |
|---|---|---|
| $\sum$ | sum | state the index range |
| $\Delta$ | difference / increment | write **backward differences**: $\Delta x_n=x_n-x_{n-1}$ (FORMULA §4.7). The derivation document was aligned to backward differences on 2026-09-29 |
| $\mathrm{d}/\mathrm{d}t$ , $\partial$ | derivative, partial derivative | the differential d is upright (0.5); FORMULA §4.7 uses italic (not yet reflected) |
| $\int$ , $\lim$ | integral, limit | — |
| $\to$ | depends on context: limit, direction of a map, an edge of a computation path | as a path edge: "which quantity is computed from which" |
| $\leadsto$ | a path exists (reaches after some steps) | — |
| $\Rightarrow$ , $\not\Rightarrow$ , $\iff$ | implies, does not necessarily imply, if and only if | — |
| $\land$ , $\lor$ | and, or | $\lor$ in the latch formula is logical OR |
| $\in$ , $\subseteq$ , $\cup$ , $\exists$ | belongs to, subset, union, exists | — |
| $\emptyset$ | **out of domain** (AXIOMS §1) | not used for the empty set |
| $\max$ , $\min$ , $\arg\max$ | maximum, minimum, argument of the maximum | — |
| $\lvert x\rvert$ | absolute value | not used for the number of records (→ $\#$ ) |
| $\#$ | number of records | $\#\mathsf{History}_n$ |
| $\mathbf{1}\{\cdot\}$ | indicator function (1 if true, 0 if false) | — |
| $\approx$ , $\sim$ , $\ll$ , $\gg$ | approximately, asymptotically equal, much smaller / larger | — |
| $\oplus$ | **appending to the end of a record sequence** | not addition, direct sum, or exclusive OR |
| $\mathbb{R}$ , $\mathbb{R}_{\mathrm{finite}}$ | real numbers, finite real numbers | — |
| $\boxed{\ }$ | the concluding formula of the section | — |
| ∎ | end of proof | — |

### 2.5 Dimension symbols (outside the rule)

| Display | Meaning | Note |
|---|---|---|
| $[x]$ | the dimension of quantity $x$ | — |
| $\mathsf{L}$ , $\mathsf{M}$ , $\mathsf{T}$ , $\mathsf{I}$ , $\mathsf{\Theta}$ , $\mathsf{N}$ , $\mathsf{J}$ | ISQ base dimensions | upright sans-serif capitals (0.5) |
| $X$ , $T$ (FORMULA §5.2) | dimension of state, dimension of time | current canon uses italic (not yet reflected) |
| $[R]=1$ | dimensionless | — |

---

## 3. Fixed names (alphabetical)

| Fixed name | Entry |
|---|---|
| `active_elements` | [Active Elements](#active-elements) |
| `alpha_upper`, `alpha_lower` | smoothing coefficients (2.2) |
| `applied_action` | [Applied Action](#applied-action) |
| `audit_log` | deprecated combined view; canonical are `structural_disclosure_log` and `input_exception_log` |
| `CONFESSION` | [Confession](#confession) |
| `d_delta_dt`, `d_tau_dt` | rates of change of deviation and thickness (double fluctuation; FORMULA §4.7) |
| `decision_sufficient_state` | [Decision-Sufficient State](#decision-sufficient-state) |
| `declared_target` | declared target (FORMULA §0) |
| `delta`, `observed_delta` | [Accumulated Deviation](#accumulated-deviation) |
| `delta_upper`, `delta_lower` (arguments `current_delta_upper`, `current_delta_lower`) | side-specific accumulated deviation (FORMULA §4.1) |
| `dominant_side` | [Dominant Side](#dominant-side) |
| `element_declared_tau` | element declared thickness ([Structural Element](#structural-element)) |
| `element_degradation_fraction` | [Degradation Fraction](#degradation-fraction) |
| `element_id` | [Structural Element](#structural-element) |
| `entropy_export` | remainder not carried forward in a discrete transition (see the notation of [Entropy Quantity](#entropy-quantity)) |
| `entropy_quantity` | [Entropy Quantity](#entropy-quantity) |
| `evaluation_archive` | [Evaluation Archive](#evaluation-archive) |
| `evaluation_declaration` | [Evaluation Declaration](#evaluation-declaration) |
| `evaluation_gauge` | [Evaluation Gauge](#evaluation-gauge) |
| `evaluation_output` | [Evaluation Output](#evaluation-output) |
| `event_allocation_rule` | [Event Allocation Rule](#event-allocation-rule) |
| `event_history` | [Event History](#event-history) |
| `external_constraint` | [Constraint](#external-constraint) |
| `initial_tau` | [Declared Thickness](#declared-thickness) |
| `instantaneous_classification` | [Instantaneous Classification](#instantaneous-classification) |
| `irreversible_latched` | [Irreversible Latch](#irreversible-latch) |
| `NOT_OBSERVABLE` | [Not Observable](#not-observable) |
| `observation_event` | [Observation Event](#observation-event) |
| `observation_projection_rule` | [Observation Projection Rule](#observation-projection-rule) |
| `observation_value` | [Observation Value](#observation-value) |
| `omega` | [Structural Continuity](#structural-continuity) |
| `other_target_index` | [Other Target](#other-target) |
| `OUT_OF_DESCRIPTION_DOMAIN` | [Out of Domain](#out-of-domain) |
| `R`, `R_upper`, `R_lower`, `R_dir` | [Boundary Approach Ratio](#boundary-approach-ratio); side-specific ratios |
| `r_warn`, `r_handoff`, `r_irrev` (outputs `thresholds.R_warn`, etc.) | thresholds |
| `R_op`, `Rop`, `rop`, `r_op` | compatibility inputs (→ `R_handoff`, `r_handoff`); not used in new documents |
| `remaining_absorption_margin` (old `remaining_slack`) | [Remaining Absorption Margin](#remaining-absorption-margin) |
| `remaining_ratio_margin` | [Remaining Ratio Margin](#remaining-ratio-margin) |
| `residual_deviation` | [Residual Deviation](#residual-deviation) |
| `reversible_deviation` | [Reversible Deviation](#reversible-deviation) |
| `subject_target` | [Subject Target](#subject-target) |
| `target_physical_state` | [Target Physical State](#target-physical-state) |
| `target_state` | [Target Boundary State](#target-state) |
| `tau`, `observed_tau` | [Absorption Thickness](#absorption-thickness) |
| `tau_upper`, `tau_lower` | [Side-Specific Effective Gate Width](#side-specific-gate-width) |
| `temporary_reversible_deviation` | [Temporary Reversible Deviation](#temporary-reversible-deviation) |
| `thickness_composition_rule` | [Thickness Composition Rule](#thickness-composition-rule) |
| `transition_phase` | [Transition Phase](#transition-phase) |
| `work_quantity` | [Work](#work-quantity) |

---

## 4. Index and label conventions

### 4.1 Subscripts and superscripts

| Display | Meaning |
|---|---|
| $_n$ | update index; event $\mathrm{Ev}_n$ advances the state from $n-1$ to $n$ (not a time) |
| $_t$ | time (FORMULA, AXIOMS) |
| $_0$ | start of evaluation / before transition |
| $^{[e]}$ | structural element $e$ |
| $^{(\mathrm{self})}$ , $^{(i)}$ | this structure, another structure $i$ |
| $^{(j)}$ | evaluation index $j$ |
| $^{(-)}$ , $^{(+)}$ | before and after a single event |
| $_{\mathrm{upper}}$ , $_{\mathrm{lower}}$ | upper side, lower side (secondary formula) |
| $_{\mathrm{warn}}$ , $_{\mathrm{handoff}}$ , $_{\mathrm{irrev}}$ | kinds of threshold |
| $^{\mathrm{temp}}$ | temporary |
| $_{\mathrm{low}}$ , $_{\mathrm{high}}$ | two compared objects (derivation document, Proposition 4) |

### 4.2 Labels (outside the rule)

| Label | Meaning | Note |
|---|---|---|
| P0–P9 | premises of the derivation document | — |
| (i)–(vi) | conditions of P9 and Part 3 (Roman numerals) | distinct from the other-structure index $i$ |
| 【1】–【11】 | sections of Part 1 of the derivation document | — |
| Stages 1–7 | stages of the derivation chain | — |
| Lemmas 1–3, Propositions 0–6 (including 2a, 2b) | lemmas and propositions of the derivation document | — |
| LC-1–LC-4 | link conditions | formerly C1–C4 |
| §n | section of a document | — |
| Reverse derivation A, B | classes of reverse derivation | — |
| Upper-case English (PERMIT, etc.) | names of canonical states and classifications | — |
| "A", "B" in tables | names of compared objects | not symbols |

---

## 5. Confusion log (by date)

The content is in the "Confusion notes" of each entry. This section is a chronological guide.

| Date | What was confused with what | Entry |
|---|---|---|
| 2026-09-26 | absorption thickness (total width) and the remainder (margin) | [Absorption Thickness](#absorption-thickness), [Remaining Absorption Margin](#remaining-absorption-margin) |
| 2026-09-27 | "reverse derivation" used in at least nine senses | [Reverse Derivation](#reverse-derivation) |
| 2026-09-27 | a directional instruction taken as permission to write the canon (working procedure) | process record, Section 4 |
| 2026-09-28 | whether accumulated deviation can decrease (contains a reversible component) was not in the canon | [Accumulated Deviation](#accumulated-deviation) |
| 2026-09-28 | "reversible penetration" and the canonical "reversible component" | [Reversible Deviation](#reversible-deviation) |
| 2026-09-28 | reference state $x_{\mathrm{ref}}$ and reference state $x_{\mathrm{exact}}$ | [Reference State](#reference-state) |
| 2026-09-28 | not observable and CONFESSION (errors in both directions) | [Not Observable](#not-observable) |
| 2026-09-28 | Π⁻¹ (reverse inference) and Π⁻¹ (reverse derivation) | [Reverse Inference](#reverse-inference) |
| 2026-09-29 | replenishment, repair, restoration, and the addition of a structural element | [Addition of a Structural Element](#structural-element-addition), [Replenishment](#replenishment), [Repair](#repair) |
| 2026-09-29 | remeasurement / structural change and the next evaluation snapshot | [Evaluation Snapshot](#evaluation-snapshot) |
| 2026-09-29 | straightening and repair (does residual deviation decrease?) | [Straightening](#straightening) |
| 2026-09-29 | removing a healthy element and rupture | [Removal of a Structural Element](#structural-element-removal) |
| 2026-09-29 | a temporarily narrowed width and a decrease of effective thickness | [Temporary Reversible Deviation](#temporary-reversible-deviation) |
| 2026-09-29 | $\tau_{\mathrm{restored}}$ and the whole thickness including added elements | [Restored Absorption Thickness](#restored-thickness) |
| 2026-09-29 | another structure's evaluation output and an observed physical event | [Boundary Approach Ratio](#boundary-approach-ratio), [Other Target](#other-target) |
| 2026-09-29 | a stored evaluation output $R$ and a ratio inside a physical law | [Reverse Derivation](#reverse-derivation) |
| 2026-09-29 | physical state, evaluation state, and event history | [Target Physical State](#target-physical-state), [Event History](#event-history) |
| 2026-09-29 | single-element $\tau_0$ , $\lambda_n$ and the general multi-element form | [Degradation Fraction](#degradation-fraction), [Declared Thickness](#declared-thickness) |
| 2026-09-29 | distinctions only by typeface or case ( $\mathcal{D}$ and $D$ , $\Gamma$ and $\gamma$ , $\Lambda$ and $\lambda$ , $Q$ and $q$ , $E$ and $e$ , etc.) | each entry; 0.5 |
| 2026-09-29 | symbols added to the canon (constraint $C$ , work $W$ ) and the derivation document's $\mathcal{C}_n$ , $\mathcal{W}_n$ (distinguished only by decoration); $\mathcal{K}$ and the knee value $k$ | [Active Elements](#active-elements), [Target Physical State](#target-physical-state), [Evaluation Gauge](#evaluation-gauge) |
| 2026-09-29 | the permitted uses of evaluation outputs written too narrowly | [Evaluation Output](#evaluation-output) |
| 2026-09-29 | the direction of the difference $\Delta$ (forward and backward) | 2.4 |
| 2026-09-29 | the number of records and the absolute value ( $\lvert\cdot\rvert$ ) | [Event History](#event-history) |
| 2026-09-29 | the auxiliary structural quantities of canon v2.4 ( $\omega$ , $\mathrm{Phase}$ , $C$ , $W$ , $\mathrm{entropy}$ ) were missing from the dictionary; $\omega$ was also called "transition-continuation quantity" (docs Chapter 12) | [Structural Continuity](#structural-continuity), [Transition Phase](#transition-phase), [Constraint](#external-constraint), [Work](#work-quantity), [Entropy Quantity](#entropy-quantity) |
| 2026-09-30 | 余裕 and 余白 (the total width $\tau$ and the remainder $M_\tau$ were both called 余裕 in Japanese) | [Remaining Absorption Margin](#remaining-absorption-margin), [Remaining Ratio Margin](#remaining-ratio-margin) |
| 2026-09-30 | the constraint $C$ (a condition) and the applied action $a_n$ (an allocated input) | [Constraint](#external-constraint), [Applied Action](#applied-action) |

---

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
