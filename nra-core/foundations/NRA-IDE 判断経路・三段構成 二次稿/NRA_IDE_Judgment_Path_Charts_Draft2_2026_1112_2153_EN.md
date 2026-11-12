# NRA-IDE Judgment Path Charts (Second Draft)

- Author: M-Tokuni
- Created: 2026-11-12 21:53 JST
- Status: **non-canonical / second draft**; uses the same case IDs (CASE-01 to CASE-11) as the paper and the reference code
- Japanese version: `NRA_IDE_判断経路チャート_二次稿_2026_1112_2153_JP.md`
- **Note: the charts do not replace definitions. Passing through a chart does not prove that a record is a fact or that a classification corresponds to reality.**

## Fig. 1: Judgment path and stop (order of `gate` in the reference code)

```mermaid
flowchart TD
    D[Declare question, rule, and required inputs before evaluation] --> Q1{Is the question as declared?}
    Q1 -->|shifted| R1[Reason: INQUIRY_CHANGED<br/>CASE-05 research layer]
    Q1 --> Q2{Is the rule fixed before start<br/>and as declared?}
    Q2 -->|no| R2[Reason: RULE_NOT_PREFIXED / RULE_CHANGED<br/>CASE-06]
    Q2 --> Q3{Does the operation class match?<br/>evaluation exclusion / real separation}
    Q3 -->|mismatch or unknown| R3[Reason: OPERATION_CLASS_MISMATCH / UNCONFIRMED<br/>CASE-01]
    Q3 --> Q4{Are required inputs present?}
    Q4 -->|missing| R4[Reason: REQUIRED_INPUT_MISSING<br/>CASE-03]
    Q4 --> Q5{Filled with inference?}
    Q5 -->|inference| R5[Reason: INFERENCE_IN_PLACE_OF_FACT<br/>CASE-03]
    Q5 --> Q6{Number or statistic placed<br/>where an event is required?}
    Q6 -->|yes| R6[Reason: NOT_AN_EVENT<br/>CASE-02]
    Q6 --> Q7{Where a number is required,<br/>is it cut as a number of a declared kind?}
    Q7 -->|cannot be cut / undeclared kind| R7[Reason: NOT_QUANTIFIABLE / KIND_NOT_ALLOWED<br/>CASE-09, CASE-02]
    Q7 --> Q8{Fact axis: is it supported?}
    Q8 -->|contradicted or unconfirmed| R8[Reason: RECORD_CONTRADICTED / FACT_UNCONFIRMED<br/>CASE-07]
    Q8 --> Q9{If a new evaluation,<br/>are grounds independent of the old one?}
    Q9 -->|re-citation| R9[Reason: EVIDENCE_NOT_INDEPENDENT<br/>CASE-08]
    Q9 --> C{Is there any reason?}
    R1 & R2 & R3 & R4 & R5 & R6 & R7 & R8 & R9 --> C
    C -->|yes| S[Stop: list every reason<br/>CASE-11]
    C -->|no| E[To later domain review<br/>truth undetermined CASE-10]
    S --> L[Append stop reasons and consulted records]
    E --> L
    L --> N[If an independent new ground exists,<br/>evaluate again under a new evaluation ID]
```

**Explanation**: no check stops at the first failure; reasons are collected before deciding stop or pass. Only the evaluation concerned stops; real events, observation, and history records do not.

## Fig. 2: History boundaries (CASE-04)

```mermaid
flowchart TD
    H0[H0 series S0] --> S{Separation boundary}
    S --> H1[H1 new series SA<br/>lineage: H0]
    S --> H2[H2 new series SB<br/>lineage: H0]
    H1 --> M{Merger boundary}
    H2 --> M
    M --> H3[H3 new series SC<br/>lineage: H0, H1, H2]
    H0 -.lineage.-> L[Lineage never breaks]
    H1 -.lineage.-> L
    H2 -.lineage.-> L
    H3 -.lineage.-> L
    X1[New series without predecessor] -->|rejected: break| NG[Not added]
    X2[Reset at the boundary] -->|rejected: new is not a reset| NG
    X3[Return to S0 at merger] -->|rejected: no return| NG
```

**Explanation**: boundaries exist but history never breaks. The starting point of a new series is measured at the boundary, not restarted from zero. A merger is not a return to H0. The chart shows relations among records, not a complete model of real history.

## Fig. 3: Path of the misclassification and keeping the reasons for rejection (CASE-01, CASE-05)

```mermaid
flowchart TD
    O[Original question: does the classification exclusion fit the target?] --> P[Question shifts: look for conditions that make exclusion hold<br/>CASE-05 research layer]
    P --> Q[Four conditions of the evaluation layer<br/>pre-fixing, no return from output, record, limited scope]
    Q --> R{Are real separation and<br/>evaluation exclusion in the same layer?}
    R -->|different layers| S[CASE-01 reject application to separation<br/>the four conditions remain valid in the evaluation layer]
    R -->|undetermined| U[Keep as undecided]
    S --> T[CASE-04 treat separation and merger as boundaries]
    P -.record the shift of question.-> A[Keep the question at the time, reasons for rejection, and sources]
    S -.do not erase the old path.-> A
    U --> Z[Re-verification by a third party]
    T --> Z
    A --> Z
```

**Explanation**: the four conditions of the initial essay are not rejected. What is rejected is applying them to a real separation.

## Fig. 4: Relation among existence, reality, event, phenomenon, and number (set diagram)

![Fig. 4: Relation among existence, reality, event, phenomenon, and number (set diagram)](NRA_IDE_Draft2_fig4_three_layers_EN_2026_1112_2153.png)

**Explanation**: a set diagram drawn with overlapping inclusion, not a parent-child tree (it cannot be drawn in Mermaid, so the SVG is the original).

- Existence is the widest and contains reality (nested).
- Event and phenomenon are not contained in one another; they partly overlap. There are events outside reality (an event in probability theory, a fictional occurrence). A phenomenon is what is real appearing in an observable form, so it lies inside reality.
- A number lies inside existence and outside reality (existence other than reality). From a phenomenon to a number, one passes through the gate "can it be cut as a number?". If it cannot, do not compute.
- Fact is not a region but a truth axis over the whole figure (the band at the top).
- Formulas stand only on a number (5 in the figure). Reading back from a number to an event changes the kind of existence, and confusion arises there.

The meaning of numbers 1 to 5 in the figure is in the table of Section 1 of the paper and in the legend of the figure.

## Correspondence among paper, code, and charts

| id      | Paper | Reference code                                                             | Chart          |
| ------- | ----- | -------------------------------------------------------------------------- | -------------- |
| CASE-01 | 6.1   | `OPERATION_CLASS_MISMATCH` (EV-01)                                       | Fig. 1, Fig. 3 |
| CASE-02 | 4.2   | `NOT_AN_EVENT` (EV-02), `KIND_NOT_ALLOWED` (EV-15); ELIGIBLE if declared (EV-16) | Fig. 1, Fig. 4 |
| CASE-03 | 4.1   | `REQUIRED_INPUT_MISSING` (EV-03), `INFERENCE_IN_PLACE_OF_FACT` (EV-04) | Fig. 1         |
| CASE-04 | 5     | `HistoryLinks`                                                           | Fig. 2         |
| CASE-05 | 6.2   | `INQUIRY_CHANGED` (EV-05)                                                | Fig. 1, Fig. 3 |
| CASE-06 | 6.1   | `RULE_NOT_PREFIXED` (EV-06, EV-08), `RULE_CHANGED` (EV-07)             | Fig. 1         |
| CASE-07 | 4.3   | `RECORD_CONTRADICTED` (EV-09)                                            | Fig. 1         |
| CASE-08 | 7.2   | ELIGIBLE (EV-10), `EVIDENCE_NOT_INDEPENDENT` (EV-11)                     | Fig. 1         |
| CASE-09 | 3     | `NOT_QUANTIFIABLE` (EV-13)                                               | Fig. 1, Fig. 4 |
| CASE-10 | 3     | ELIGIBLE (EV-14)                                                           | Fig. 1         |
| CASE-11 | 7.1   | multiple reasons (EV-15)                                                   | Fig. 1         |

## About images

The images of Figs. 1 to 3 are rendered from the Mermaid sources in this file and placed in the same folder (mermaid-cli 12.2.0). The Mermaid source is authoritative; re-render the images after any edit. Fig. 4 is a set diagram that cannot be drawn in Mermaid, so the SVG is the original and the PNG is its rendering (generated 2026-11-13). Fig. 1 was redrawn to match the added reason code (`KIND_NOT_ALLOWED`) (2026-11-13). The images of the first draft correspond to the first-draft charts and are not used for the second draft.

| Figure                                | Japanese                                                         | English                                                          |
| ------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| Fig. 1 Judgment path                  | `NRA_IDE_Draft2_fig1_route_JP_2026_1112_2153.png/.svg`         | `NRA_IDE_Draft2_fig1_route_EN_2026_1112_2153.png/.svg`         |
| Fig. 2 History boundaries             | `NRA_IDE_Draft2_fig2_history_JP_2026_1112_2153.png/.svg`       | `NRA_IDE_Draft2_fig2_history_EN_2026_1112_2153.png/.svg`       |
| Fig. 3 Path of misclassification      | `NRA_IDE_Draft2_fig3_research_path_JP_2026_1112_2153.png/.svg` | `NRA_IDE_Draft2_fig3_research_path_EN_2026_1112_2153.png/.svg` |
| Fig. 4 Three layers and the fact axis | `NRA_IDE_Draft2_fig4_three_layers_JP_2026_1112_2153.png/.svg`  | `NRA_IDE_Draft2_fig4_three_layers_EN_2026_1112_2153.png/.svg`  |

Fig. 1 draws a stopping branch for each check, but the actual gate does not stop at the first failure; it collects reasons (CASE-11). The figure does not show this.
