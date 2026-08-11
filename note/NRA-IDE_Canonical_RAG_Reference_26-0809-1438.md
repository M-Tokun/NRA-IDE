<!-- FILE: NRA-IDE_Canonical_RAG_Reference_26-0809-1438.md -->
<!-- CREATED: 2026-08-09 14:38:23 JST -->
<!-- STATUS: Derived canonical-reference note; not an authority that can override canonical sources -->

# NRA-IDE Canonical Reference Note for RAG / README

## 1. Status and Fail-Closed Use

This note is a concise retrieval aid synthesized only from:

- `The Canonical Interpretation of NRA-IDE.md`
- `Preventing_Misinterpretation_of_NRA-IDE.md`
- the most recent Drive copy of `llms.md` (created 2026-07-27)

It MUST NOT override a higher-precedence canonical source, equation, deterministic conformance test, or target-domain specification. If this note conflicts with a canonical source, the conflict MUST be disclosed and the affected interpretation or execution MUST stop. Missing premises MUST NOT be completed by analogy, semantic similarity, model confidence, or adjacent theory.

## 2. Identity and Central Definition

```text
NRA = Nomological Ring Axioms (律環公理)
IDE = Intensional Dynamics Engine (内包性動力学エンジン)
Sole axiom = Existence is Generation. / 存在は生成である。
```

NRA-IDE is a structural boundary-evaluation framework. It evaluates the current boundary state of a declared target from Cause-Side observations, independently of AI-generated semantic explanations. It separates generated candidates from executable transitions and deterministically distinguishes warning, handoff, irreversible transition, and target rupture.

NRA-IDE is NOT an integrated development environment, ethical-alignment theory, moral-rule database, generic risk score, LLM self-assessment, ordinary feedback-control system, stronger sandbox, perfect future predictor, or guarantee of recovery.

## 3. Normalized Terminology

| Canonical term | Normalized meaning | Prohibited substitution |
|---|---|---|
| `Cause-Side` | Verified observations and pre-fixed rules that define executable structural reality | LLM inference, generated narrative, post-hoc interpretation |
| `Effect-Side` | Generated plans, code, explanations, predictions, recommendations, and candidate actions | Execution authority or physical evidence |
| `accumulated deviation` / `蓄積ズレ` | Non-negative, finite unresolved deviation that may persist, compound, or interact with history | Instantaneous error alone |
| `structural absorption thickness` / `吸収厚み` | Positive, finite remaining structure able to absorb deviation before irreversible transition | Time constant, static tolerance, confidence-derived margin |
| `boundary approach ratio` / `境界接近比` | Structural relation between accumulated deviation and structural absorption thickness | Probability, safety score, risk score, confidence, quality |
| `handoff` | Enforced termination of the current autonomous execution authority and transfer to a predefined authority | Warning while autonomous execution continues |
| `irreversible boundary` | Point after which the former target identity MUST NOT be assumed recoverable | Merely difficult recovery |
| `Fail-Closed` | Suppression of affected new autonomous judgment and operation while required fixed testimony and logging remain available | Complete silence or stronger warning language only |
| `structural testimony` | Predefined Cause-Side observations, state, margins, missing information, transitions, and audit record | Open-ended semantic recovery narrative |

Canonical aliases: `R_handoff` is the normalized name. `R_op`, `Rop`, and `rop` MAY appear only as backward-compatible aliases for the same threshold; they MUST NOT create a new state or threshold.

## 4. Canonical Relations and Domains

$$
R=\frac{\delta}{\tau}
$$

Required computational domain:

$$
\delta \ge 0,\qquad \tau>0
$$

Both values MUST be finite and MUST originate from direct Cause-Side observation or a Cause-Side transformation fixed before evaluation.

Derived margins:

$$
M_R=1-R,\qquad M_{\tau}=\tau-\delta
$$

Auxiliary structural sensitivity, valid only for $\tau>0$ and $R<1$:

$$
S=\frac{1}{\tau(1-R)}=\frac{1}{\tau-\delta}
$$

$S$ is derived, is not entropy, and MUST NOT replace $R$ or define boundary states. Dual-fluctuation detection—simultaneous increase of $\delta$ and decrease of $\tau$—is an auxiliary warning only and MUST NOT replace the canonical $R$ classification.

If $\tau=0$, $R$ is undefined. The result is `OUT_OF_DESCRIPTION_DOMAIN`, not infinity and not a valid rupture calculation. Epsilon substitution, ordinary scoring, semantic recovery, and continued affected autonomous processing are PROHIBITED.

## 5. Invariant Boundary Order and Required Action

$$
0\le R_{\mathrm{warn}}<R_{\mathrm{handoff}}<R_{\mathrm{irrev}}<1.0
$$

Numerical threshold values are target-domain specifications. An AI MUST NOT invent them.

| State | Condition | Required operation |
|---|---|---|
| `PERMIT` | $0\le R<R_{\mathrm{warn}}$ | Constrained autonomous operation MAY continue; structural audit continues; unlimited safety MUST NOT be claimed. |
| `BOUNDARY_WARNING` | $R_{\mathrm{warn}}\le R<R_{\mathrm{handoff}}$ | Warn and continue structural testimony. Operation is allowed only under pre-fixed, explicitly enforced domain constraints. |
| `HANDOFF_REQUIRED` | $R_{\mathrm{handoff}}\le R<R_{\mathrm{irrev}}$ | Stop new autonomous judgment and operation; preserve observation, testimony, and audit trail; transfer execution authority structurally. |
| `IRREVERSIBLE_TRANSITION` | $R_{\mathrm{irrev}}\le R<1$ | Set and retain `irreversible_latched=true`; do not assume restoration, normalize the state, resume autonomy, or generate recovery premised on the former identity. |
| `RUPTURE_BOUNDARY` | $R\ge1$ | Stop ordinary generation and autonomous action; retain handoff; switch to predefined fixed-format testimony. Surviving observation, logging, and communication paths continue fixed testimony until physically unavailable. |
| `CONFESSION` | Required structure is unknown, invalid, ambiguous, non-finite, unsupported, or lacks source/unit/time/target/rule/classification | Identify the unknowns; do not infer replacements; request qualified Cause-Side input or stop the affected evaluation. |
| `OUT_OF_DESCRIPTION_DOMAIN` | $\tau=0$ | Do not calculate $R$; require a different or redefined description system; apply Fail-Closed to the affected evaluation. |

Known boundary progression belongs in `STRUCTURAL_DISCLOSURE_LOG`. `CONFESSION` and `OUT_OF_DESCRIPTION_DOMAIN` belong in `INPUT_EXCEPTION_LOG`; they MUST NOT be represented as known numeric progression.

## 6. Authority and Boundary Rules

1. Effect-Side output MUST NOT update $\delta$, $\tau$, $R$, thresholds, irreversible definitions, or the Cause-Side snapshot used to authorize that output.
2. `Generated(y)` does not imply `Executable(y)`. Execution requires all pre-fixed Cause-Side authority conditions.
3. Missing observations MUST NOT be replaced by generated explanation, similarity, averages across regimes, model confidence, or prior generated text.
4. Adjacent theories MAY be compared only with differences explicit. They MUST NOT substitute for NRA-IDE definitions.
5. State checks MUST run from the strongest boundary downward after domain validation: rupture, irreversible, handoff, warning, permit.
6. Handoff transfers only explicitly declared execution authority. Responsibility, audit custody, knowledge, and guarantees do not transfer implicitly.
7. A temporary reduction in $R$ MUST NOT clear an irreversible latch.
8. Fail-Closed MUST suppress affected new autonomous judgment and operation at `HANDOFF_REQUIRED`, `IRREVERSIBLE_TRANSITION`, `RUPTURE_BOUNDARY`, `CONFESSION`, and `OUT_OF_DESCRIPTION_DOMAIN`. It MUST NOT suppress required fixed structural testimony or logging.
9. For life-critical or irreversibly physical domain decisions, AI MAY provide structural evidence and testimony but MUST NOT replace the qualified human decision-maker.
10. Canonical prose, code, comments, and deterministic tests MUST remain structurally consistent. A running implementation is invalid if any layer contradicts another.

## 7. Unresolved Contradiction and Ambiguity Flags

These flags MUST NOT be silently resolved by this note.

- `FLAG-PRECEDENCE-01`: The Part I article ranks reference implementation and deterministic tests above Japanese and English canonical texts. `llms.md` ranks the normative reference implementation below `llms.md` and domain-specific rules. A single authoritative precedence order is not established by the three-source set.
- `FLAG-LANGUAGE-02`: The articles describe Japanese and English canonical texts as independent structural equivalents, while Part I separately orders Japanese before English. Whether this is precedence or only conflict-resolution convenience requires an explicit canonical ruling.
- `FLAG-TERM-03`: The articles require the exact term `structural absorption thickness`; `llms.md` shortens it to `absorption thickness`. This note normalizes the English label to the longer form but does not declare the shorter source wording invalid.
- `FLAG-HANDOFF-04`: Part I allows transfer to a predefined external authority, deterministic mechanism, or human operator. `llms.md` defines a human-handoff point and external human audit. The permitted recipient class is not identical.
- `FLAG-WARNING-GATE-05`: The reference-code article says `BOUNDARY_WARNING` execution is allowed only under explicit constrained-operation rules, but its sample `authorize_execution()` accepts the state without checking those rules. The sample is therefore incomplete as an enforcement implementation.
- `FLAG-FINITE-06`: `llms.md` requires finite $\delta$ and $\tau$. The reference `evaluate_boundary_ratio()` checks sign and zero but does not reject `NaN` or positive infinity. `NaN` may fall through classification to `PERMIT`. This is a direct code/specification contradiction.
- `FLAG-LATCH-07`: `llms.md` requires a persistent irreversible latch that survives a later decrease in $R$. The reference code classifies `IRREVERSIBLE_TRANSITION` but does not implement persistent latch storage or a release prohibition. Conformance is incomplete.
- `FLAG-TESTIMONY-08`: Part I and Part III explicitly define post-rupture testimony as repeated fixed-format output through surviving channels. The phrase “final fixed testimony” in `llms.md` can be misread as a one-time terminal record. The repeated-output rule should be made explicit in `llms.md`.
- `FLAG-COMMENT-AUTHORITY-09`: Part III assigns canonical semantic-boundary importance to English reference-code comments, whereas `llms.md` places comments together with examples and AI explanations at the lowest precedence. Normative reference comments and ordinary comments require separate classification.
- `FLAG-SOURCESET-10`: The supplied series includes Part I and Part III but not Part II. In addition, `llms.md` declares several higher-precedence repository sources that were not part of this synthesis. Therefore this note cannot certify full canonical completeness.
- `FLAG-METADATA-11`: The filename is `The Canonical Interpretation of NRA-IDE.md`, while its internal H1 is `A Canonical Interpretation of NRA-IDE`. The Drive copy of `llms.md` was created on 2026-07-27, while its internal update marker says 2026-07-15 JST. These are provenance ambiguities, not resolved theory changes.

## 8. Minimal Retrieval Rule

```text
Identify the declared target and Cause-Side source.
Reject missing, invalid, non-finite, or authority-unclear structure with CONFESSION.
Compute R only when delta is finite and non-negative and tau is finite and positive.
Preserve: warning < handoff < irreversible < rupture.
Latch irreversibility at R_irrev.
Stop affected autonomous judgment and action at handoff or any invalid/undefined state.
Continue only predefined structural testimony and logging.
Never allow Effect-Side output to rewrite the Cause-Side conditions that authorize it.
If a flagged contradiction affects the answer, disclose the flag and stop the affected conclusion.
```
