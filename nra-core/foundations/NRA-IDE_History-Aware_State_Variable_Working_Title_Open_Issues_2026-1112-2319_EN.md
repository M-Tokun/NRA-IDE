# NRA-IDE: Open Issues on the "History-Aware State Variable" (Working Title)

- Recorded: 2026-11-12 23:19 JST
- Recommended location: `nra-core/foundations/`
- Status: **undecided / non-canonical design candidate** (the name is also undecided; does not approve any change to implementation, formal definitions, or the dictionary)
- Author: M-Tokuni
- Source: Section 2 and the comparison table of `dictionary/追記予定.txt` (2026-11-12). Terms are aligned with the organization of the second draft of the judgment path / three-part set (fact, event, reality, existence).
- Japanese version: `NRA-IDE：履歴付き状態変数（仮称）の検討事項（設計候補・未確定）2026-1112-2319.md`
- Related: `NRA-IDE 判断経路・三段構成 二次稿/` (paper Section 8 and Appendix C)

## 0. Most important boundaries (check first)

1. **Do not fix the name.** "History-aware state variable" is a working title. What is needed is not a variable as such but a container that does not lose the connection among state, fact-finding, grounds, and history. Fix the necessary data and boundaries before the name.
2. **Do not put it in the dictionary.** Once published, a dictionary heading ID cannot be removed (DICT-ID-LOST in `scripts/check_dictionary.py`). An ID for a working title would remain even if the name changes. Make it an entry again after the name and structure are decided.
3. **Do not overlap with existing NRA-IDE definitions.** The dictionary records a confusion about mixing target state, evaluation state, and event history (2026-09-29). Where this proposal overlaps with existing definitions is checked first, in issue Q-01 of Section 5.
4. **Do not define by borrowing an existing technology.** Event Sourcing is a reference technology and not an NRA-IDE definition (second draft, Appendix C).

## 1. Provisional definition (from the source)

A logical data structure that has a function for referring to the current state of a target and a function for tracking the records, grounds, rules, and judgment history used to derive that state.

Unlike an ordinary variable that overwrites a single value, it keeps separately the change of the state and the change of the grounds on which the state was judged.

## 2. Required components (candidates) and correspondence with the second-draft fields

| id | Component (source) | Content | Field in paper Section 8 of the second draft |
|---|---|---|---|
| E-01 | target identifier | what state is handled | `subject` |
| E-02 | state value | state at a defined time and range | (the value of a record; no dedicated field) |
| E-03 | reference to grounds | information used to derive the state | `dependencies` |
| E-04 | kind of information | distinction among measurement, statistic, inference, record of an event, etc. | `kind` |
| E-05 | judgment status | established, not established, unknown, etc. | `support` |
| E-06 | applied rule | the computation rule that derived the state, and its version | `rule_id`, `rule_version`, `declared_at` |
| E-07 | history reference | connection to earlier judgments, corrections, and rejected paths | `previous_evaluation_id`, `predecessor_ids` |
| E-08 | re-verification condition | what must hold for a judgment to be re-verified | **no counterpart** (close to `review_trigger` of the first draft, which the second draft does not adopt) |

## 3. Boundaries of application (from the source)

1. Do not identify the information kept in a state variable with the real event itself.
2. Do not implicitly convert a measured value, a statistic, or an inference into confirmed information about a real event.
3. When a required condition is unknown, stop the computation that depends on it.
4. Even when a correction occurs, keep the earlier judgment and the reason for the correction.
5. For separation and merger, handle the dependencies among multiple histories separately.
6. Starting a new computation does not mean erasing past events or earlier judgments.

Correspondence with the second draft: 1 to 2.2 and 2.3; 2 to 4.2; 3 to 4.1 and 7.1; 4 to 4.3 and 7.2; 5 and 6 to Section 5 (boundaries).

## 4. Difference from Event Sourcing (comparison table of the source)

| Aspect | Event Sourcing | History-aware state variable (working title) |
|---|---|---|
| What it expresses | a design method that stores state changes | a data structure that refers to a state and the grounds of its establishment |
| Main purpose | reconstruction of state; audit | tracking of state, grounds, and judgments |
| Past records | stored append-only | storing is a requirement |
| Truth judgment | the method itself does not guarantee it | a separate verification mechanism is needed |
| Separation and merger | an individual data model is needed | undecided |
| Theoretical status | existing technology | a research candidate in NRA-IDE |

Key caution: in Event Sourcing, the event store becomes the system of record inside the system. Do not directly replace this description with the view of the second draft that "a record points to an event and is not the event itself."

## 5. Open issues

| id | Item | Content |
|---|---|---|
| Q-01 | **Overlap with existing definitions (top priority)** | Where it overlaps with and differs from the dictionary's Target Physical State (physical state; excludes evaluation state and event history), Evaluation State (irreversible latch, etc.), Event History (append-only sequence of event records), Evaluation Archive (records of finished evaluations), and Decision-Sufficient State $Z_n$. Does holding state, history, and grounds in one container violate "do not mix physical state, evaluation state, and event history" (2026-09-29)? |
| Q-02 | Name | Stays a working title. Decide a name that expresses the role of the container, following the dictionary's "naming precedence" |
| Q-03 | Rule for identifying a state and an event | The state value belongs to the third layer (numeric cut) and the event to the second layer. How to separate the identifiers |
| Q-04 | Verification conditions needed for fact-finding | Who decides the judgment status (established, not established, unknown), and by what procedure. Connects to U-08 of the second draft (independence of grounds) |
| Q-05 | History references at separation and merger | How to hold the boundary disciplines of Section 5 of the second draft (lineage is inherited, not a reset, no return) as a data structure. `HistoryLinks` of the second draft is only a minimal prototype of a record graph |
| Q-06 | Correspondence with existing NRA-IDE computation definitions | Relation to the evaluation declaration $\mathsf{Decl}$, the evaluation snapshot, and $\mathsf{Active}_n$ (FORMULA §0.5.1, §0.5.4) |
| Q-07 | Formal conditions for detecting reverse derivation | Within this document, limited to detecting "do not fill missing parts with inference". Detection of the canonical reverse derivations A and B is out of scope |
| Q-08 | How to hold re-verification conditions (E-08) | The second draft has no corresponding field. Do not make it a ban on unlimited study |
| Q-09 | When and how to put it in the dictionary | After the name and structure are decided. Decide together with whether to include the external technology Event Sourcing |

## 6. Operating boundaries

- This document is a study record and does not create new canonical formulas, canonical states, or dictionary entries.
- `FORMULA.md`, `theory/AXIOMS.md`, the dictionary, and the reference implementation are not changed.
- When referring to this in a new session, **read Section 0 and Q-01 of Section 5 first**.
