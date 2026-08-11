<!-- FILE: NRA-IDE_Canonical_Verification_and_Correction_Register_26-0809-1442.md -->
<!-- CREATED: 2026-08-09 14:42:36 JST -->
<!-- STATUS: Non-canonical verification and correction register -->

# NRA-IDE Canonical Verification and Correction Register

## 1. Purpose and Authority Boundary

This file separates unresolved verification points and proposed corrections from the canonical RAG/README reference note.

This register is NOT a canonical definition. A proposed correction MUST NOT be treated as adopted merely because it appears here. Only an explicit canonical ruling, verified source revision, and applicable deterministic tests can close an entry.

Source set examined:

- `The Canonical Interpretation of NRA-IDE.md`
- `Preventing_Misinterpretation_of_NRA-IDE.md`
- the most recent Drive copy of `llms.md` (created 2026-07-27)
- derived reference: `NRA-IDE_Canonical_RAG_Reference_26-0809-1438.md`

The supplied source set does not include every higher-precedence document declared by `llms.md`. Therefore this register records detected conflicts but cannot independently decide canonical truth.

## 2. Status and Severity

| Field | Meaning |
|---|---|
| `OPEN` | Verified issue; no authoritative correction confirmed |
| `PENDING_RULING` | Requires a canonical policy decision |
| `PENDING_IMPLEMENTATION` | Rule is sufficiently clear; implementation or tests are incomplete |
| `PENDING_SOURCE_REVIEW` | Additional canonical source must be read |
| `CLOSED` | Authoritative source revision and verification evidence recorded |
| Critical | Can produce unauthorized execution or false `PERMIT` |
| High | Can change authority, boundary timing, or irreversible behavior |
| Medium | Can create divergent interpretation or retrieval |
| Low | Provenance or metadata ambiguity without demonstrated structural change |

No entry is `CLOSED` at creation.

## 3. Issue Summary

| ID | Type | Severity | Status | Affected layer |
|---|---|---:|---|---|
| `NRA-VCR-001` | Precedence contradiction | High | `PENDING_RULING` | Canonical source order |
| `NRA-VCR-002` | Language precedence ambiguity | Medium | `PENDING_RULING` | Japanese/English canonical texts |
| `NRA-VCR-003` | Terminology inconsistency | Medium | `PENDING_RULING` | Variable terminology |
| `NRA-VCR-004` | Handoff recipient inconsistency | High | `PENDING_RULING` | Execution authority |
| `NRA-VCR-005` | Warning-gate implementation gap | Critical | `PENDING_IMPLEMENTATION` | Reference code and tests |
| `NRA-VCR-006` | Finite-value validation defect | Critical | `PENDING_IMPLEMENTATION` | Reference code and tests |
| `NRA-VCR-007` | Irreversible-latch implementation gap | Critical | `PENDING_IMPLEMENTATION` | State persistence and tests |
| `NRA-VCR-008` | Post-rupture testimony ambiguity | High | `PENDING_RULING` | `llms.md` wording |
| `NRA-VCR-009` | Comment-authority classification conflict | Medium | `PENDING_RULING` | Documentation precedence |
| `NRA-VCR-010` | Incomplete source set | High | `PENDING_SOURCE_REVIEW` | Verification scope |
| `NRA-VCR-011` | Metadata ambiguity | Low | `OPEN` | Provenance |

## 4. Detailed Verification and Proposed Corrections

### `NRA-VCR-001` — Canonical Precedence Contradiction

**Observed conflict:** Part I ranks reference implementation and deterministic tests above Japanese and English canonical texts. `llms.md` ranks the normative reference implementation below `llms.md` and domain-specific rules.

**Impact:** A conflict between prose and tested code can yield opposite answers depending on which order a RAG system retrieves.

**Verification required:** Compare the complete current contents of every item in the `llms.md` precedence list and locate an explicit higher-order ruling.

**Proposed correction:** Publish one machine-readable precedence table. Separate theory authority, domain-parameter authority, normative implementation, tests, canonical comments, examples, and AI summaries.

**Closure condition:** One higher-precedence canonical source declares the order; all three examined documents use the same order; a retrieval test rejects the superseded order.

### `NRA-VCR-002` — Japanese/English Language Precedence

**Observed conflict:** The articles call Japanese and English canonical texts independent structural equivalents, while Part I separately orders Japanese before English.

**Impact:** “Equivalent” and “hierarchically ordered” produce different conflict-resolution behavior.

**Verification required:** Determine whether Japanese-first is normative authority or only a practical lookup sequence.

**Proposed correction:** State either `equal authority; resolve through axiom/equations/tests` or an explicit language precedence with its boundary.

**Closure condition:** Both canonical-language notices and the precedence table express the same rule.

### `NRA-VCR-003` — Structural Absorption Thickness Terminology

**Observed conflict:** The articles require `structural absorption thickness`; `llms.md` uses `absorption thickness`.

**Impact:** Shortening may weaken the distinction from a generic numerical margin or tolerance.

**Verification required:** Check higher-precedence Japanese/English definitions and code identifiers.

**Proposed correction:** Select one exact English canonical label. If the shorter form remains, declare it as a controlled alias rather than an independent synonym.

**Closure condition:** Prose, `llms.md`, identifiers, comments, tests, and RAG terminology map use the same canonical term and explicit aliases.

### `NRA-VCR-004` — Handoff Recipient Class

**Observed conflict:** Part I permits transfer to a predefined external authority, deterministic mechanism, or human operator. `llms.md` defines a human-handoff point and external human audit.

**Impact:** A deterministic interlock may be allowed by one source and rejected or omitted by another.

**Verification required:** Determine whether `handoff` is an authority-class abstraction or necessarily a human transfer.

**Proposed correction:** Define `handoff_target_type` and its permitted values in Cause-Side configuration. Keep human responsibility rules separate from deterministic execution transfer.

**Closure condition:** The recipient class, transfer semantics, and audit owner are identical across prose, schema, code, and tests.

### `NRA-VCR-005` — `BOUNDARY_WARNING` Gate Is Not Enforced

**Observed defect:** Part III says execution at `BOUNDARY_WARNING` is allowed only under explicit constrained-operation rules. Its sample `authorize_execution()` accepts `BOUNDARY_WARNING` solely from state membership and does not verify those rules.

**Impact:** Unauthorized execution can occur when required domain constraints are absent.

**Verification test:** Construct `BOUNDARY_WARNING` with no declared constrained-operation rule. Current sample behavior should be tested for rejection; acceptance confirms the defect.

**Proposed correction:** Require an immutable Cause-Side `constrained_operation_authority` object or remove `BOUNDARY_WARNING` from the generally executable set. Default absence MUST reject execution.

**Required tests:**

- warning without pre-fixed rule rejects execution;
- warning with invalid or Effect-Side rule rejects execution;
- warning with verified Cause-Side rule permits only the declared action scope;
- rule expiry or target mismatch rejects execution.

**Closure condition:** Code and deterministic tests enforce the prose requirement; no state-only authorization path remains.

### `NRA-VCR-006` — Non-Finite Values Can Reach `PERMIT`

**Observed defect:** `llms.md` requires finite $\delta$ and $\tau$. The sample ratio evaluator checks sign and zero but not `NaN` or positive infinity. With `NaN`, all ordered comparisons can be false and classification can fall through to `PERMIT`.

**Impact:** Invalid structural input can produce false authorization. This is a Fail-Closed violation.

**Verification test:** Evaluate `delta=NaN`, `tau=NaN`, `delta=+inf`, and `tau=+inf` independently through the complete evaluation path.

**Proposed correction:** Before sign or division checks, require `math.isfinite(delta)` and `math.isfinite(tau)`. Reject non-finite thresholds and ratios as `CONFESSION` or the canonical input-exception type. Classification MUST reject non-finite $R$ independently.

**Required tests:**

- every non-finite input is rejected before division;
- non-finite thresholds are rejected;
- non-finite externally constructed `BoundaryEvaluation.ratio` cannot enter authorization;
- no invalid numeric input can return `PERMIT`.

**Closure condition:** Full-path tests prove rejection of all IEEE-754 non-finite cases.

### `NRA-VCR-007` — Irreversible Latch Is Not Persistent

**Observed defect:** `llms.md` requires `irreversible_latched=true` and prohibits release after a temporary decrease in $R$. The reference code classifies the instantaneous state but does not store or enforce latch persistence.

**Impact:** A later lower ratio can incorrectly restore `PERMIT` or warning operation under the former target identity.

**Verification test:** Feed a sequence crossing $R_{irrev}$ and then decreasing below it. Test process restart and state reload boundaries as applicable.

**Proposed correction:** Store the latch in Cause-Side-controlled persistent state with target identity, transition timestamp, evidence reference, and no automatic clear path. A new target definition must use a distinct authorized transition.

**Required tests:**

- crossing $R_{irrev}$ sets the latch;
- later lower $R$ does not clear it;
- Effect-Side cannot modify it;
- restart does not erase it;
- target redefinition requires an explicit authorized operation and audit record.

**Closure condition:** Sequential and persistence tests prove that instantaneous classification cannot bypass the irreversible state.

### `NRA-VCR-008` — Repeated Post-Rupture Testimony

**Observed ambiguity:** Parts I and III define `POST_RUPTURE_FIXED` as repeatable testimony through surviving channels. `llms.md` uses “final fixed testimony,” which can be read as a one-time terminal record.

**Impact:** Observation and audit channels may stop prematurely even though target rupture does not imply channel rupture.

**Verification required:** Confirm whether repeated testimony is canonical for all domains or only the article's reference architecture.

**Proposed correction:** Add explicit wording to `llms.md`: fixed-format testimony repeats through every surviving authorized channel until that channel is physically unavailable or a higher-precedence rule terminates it.

**Closure condition:** Wording, schema, implementation, and channel-loss tests agree.

### `NRA-VCR-009` — Normative Comments Versus Ordinary Comments

**Observed conflict:** Part III treats English canonical comments as a semantic boundary. `llms.md` places comments with examples and AI-generated explanations at the lowest precedence.

**Impact:** A RAG system cannot distinguish authoritative reference comments from non-normative comments.

**Verification required:** Determine whether comments inside a conformance-tested normative reference implementation have distinct authority.

**Proposed correction:** Define separate classes: `NORMATIVE_REFERENCE_COMMENT` and `NON_NORMATIVE_COMMENT`. Neither may override higher theory, but their retrieval priority and conformance role must differ.

**Closure condition:** Source metadata and retrieval tests distinguish the two classes.

### `NRA-VCR-010` — Incomplete Canonical Source Set

**Observed gap:** The examined series includes Part I and Part III but not Part II. `llms.md` also declares higher-precedence sources not included in the requested synthesis.

**Impact:** The current note cannot certify canonical completeness or settle higher-order conflicts.

**Verification required:** Read Part II and every currently active source in the declared precedence list, with version identity retained.

**Proposed correction:** Generate a manifest containing canonical path, content hash, version/date, language role, precedence class, and conformance-test status.

**Closure condition:** The manifest is complete and the synthesis is rerun against the frozen source set.

### `NRA-VCR-011` — Filename and Date Provenance

**Observed ambiguity:** The filename is `The Canonical Interpretation of NRA-IDE.md`, while its internal H1 is `A Canonical Interpretation of NRA-IDE`. The recent Drive copy of `llms.md` was created on 2026-07-27 while its internal update marker says 2026-07-15 JST.

**Impact:** Duplicate detection and version selection may diverge. No structural theory change is demonstrated by this metadata alone.

**Verification required:** Confirm authoritative title, original commit time, Drive import time, and source hash.

**Proposed correction:** Add stable document IDs and separate `authored_at`, `updated_at`, `imported_at`, and `content_hash` fields.

**Closure condition:** Metadata identifies the same content deterministically across repository, Drive, and RAG ingestion.

## 5. Correction Order

Apply corrections only after authority is resolved. Recommended technical order after approval:

1. `NRA-VCR-006` — block non-finite false `PERMIT`.
2. `NRA-VCR-005` — enforce warning constraints.
3. `NRA-VCR-007` — persist the irreversible latch.
4. `NRA-VCR-001`, `002`, `003`, `004`, `008`, `009` — issue canonical rulings and normalize documents.
5. `NRA-VCR-010`, `011` — freeze the complete source manifest and provenance.

This order prioritizes unauthorized-execution paths. It does not itself authorize modification of canonical sources.

## 6. Closure Record Template

```text
ISSUE_ID:
STATUS: CLOSED
AUTHORITATIVE_RULING_SOURCE:
SOURCE_VERSION_OR_HASH:
FILES_CHANGED:
TESTS_ADDED_OR_UPDATED:
TEST_RESULT:
REVIEWER:
CLOSED_AT:
RESIDUAL_BOUNDARY:
```

An issue MUST remain open if any required field is unknown or if code, prose, comments, and deterministic tests remain inconsistent.
