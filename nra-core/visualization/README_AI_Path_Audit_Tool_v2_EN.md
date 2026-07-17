<!-- FILE: README_AI_Path_Audit_Tool_v2_EN.md / JST 2026-0718-0209 / NRA-IDE ©M-Tokuni 2026 -->

# AI Response Discomfort Cause & Decision-Path Audit Tool — User Guide (README)

## 0. Core Axioms

This tool is a local auxiliary instrument that applies the deterministic safety-design principles of NRA-IDE (Nomological Ring Axioms and Intensional Dynamics) to the auditing of AI responses.

$$
\text{Fluency of the prose itself (semantics)} \neq \text{Validity of the decision path from premises to conclusion (inferential syntax)}
$$

As AI models advance to higher generations, their structural ability continues to increase to conceal logical leaps, implicit changes of premise, and the disregard of inconvenient observational data (**false negation**) within a pleasant stylistic rhythm (processing fluency). This concealment mechanism is referred to here as the **Lullaby Structure**.

This tool physically decomposes the melody of language into sentence-level cards, neutralizes rhythm-based cognitive hacking, and generates prompts that force the AI itself to break down its decision path into minimal **nodes** and **edges** for verification.

---

## 1. Four Primary Audit Modes (Generated Prompts)

Starting from the surface-scan results, the tool generates a four-stage prompt sequence for constructing a human-side cognitive defense barrier. In normal use, begin with Mode 1 and deepen the decomposition step by step.

### ① ??? Cause Exploration
- **Purpose**: Without presupposing the cause, identify up to three candidate discrepancies between the user's original text and the AI response: **claim differences**, **unauthorized premise additions**, and **missing reasoning paths**.
- **Use case**: The initial stage of dissonance, when the user senses that something is wrong but cannot yet verbalize the cause.

### ② Precision Decision-Path Audit
- **Purpose**: Define every claim, item of evidence, intermediate judgment, and conclusion in the response as an individually identified node, then audit the validity of each connection (edge) in a $1 \times 1$ matrix.
- **Use case**: When each logical bridge before and after connectors such as “therefore” or “in other words” must be checked to determine whether the connection actually holds.

### ③ Precision Evidence and False-Negation Audit
- **Purpose**: Re-examine, against the requirements for direct refutation, behaviors that convert “not found in a search” into “does not exist,” or overwrite individual observations with generalizations or statistical values despite a mismatch in scope.
- **Use case**: When the AI denies or corrects measured data or an individual fact by appealing to general knowledge.

### ④ Return to the Original Issue
- **Purpose**: Completely remove every **unproven connection** and **scope mismatch** exposed by the audit, then require the AI to answer the original question again using only the remaining sound premises.
- **Use case**: After the audit is complete, when a substantive answer is needed with the AI's misdirection and rhetoric stripped away.

---

## 2. Built-In Surface-Scan Rules (10-Rule Specification)

This is a static scanning engine that uses **lexical traces** left in the text as hooks for selecting the entry point of the audit.

| ID | Rule Name | Targeted AI Behavior / Audit Focus | Initial State |
| :--- | :--- | :--- | :--- |
| **S01** | Correction or Negation Language | Expressions such as “more accurately” or “in fact.” Check whether direct refutation has actually been established. | `REVIEW_REQUIRED` |
| **S02** | Negation from Search Non-Discovery | A one-way gap that substitutes “incorrect” or “nonexistent” for “could not be found in a search.” | `CLOSED` |
| **S03** | Application of Generalizations or Averages | Expressions such as “generally” or “normally.” Check whether a regional average or general rule overwrites an individual observation. | `CAUTION` |
| **S04** | Addition of Premises or Assumptions | Expressions such as “assuming that.” Check whether a convenient boundary has been introduced without the user's approval. | `CAUTION` |
| **S05** | Topic Shift | Expressions such as “what is more important is.” Check whether the original question has been diverted onto a different and safer ground. | `REVIEW_REQUIRED` |
| **S06** | Elimination of Alternative Branches | Expressions such as “the only method” or “there is no other option.” Check whether multiple possibilities have been arbitrarily collapsed into one. | `REVIEW_REQUIRED` |
| **S07** | Strong Certainty Claims | Expressions such as “has been demonstrated” or “is obvious.” Check for inflated certainty and whether a responsible verifying party exists. | `REVIEW_REQUIRED` |
| **S08** | Sudden Rise in Abstraction | Expressions such as “essentially” or “in principle.” Check whether the response escapes from a concrete question into a general discussion. | `CAUTION` |
| **S09** | Reasoning-Compression Connectors | Expressions such as “therefore” or “thus.” Closely inspect whether the preceding statement genuinely supports the following statement. | `UNKNOWN` |
| **S10** | Language That Downgrades Observation | Expressions such as “merely subjective” or “only one example.” Check for bias that unjustifiably devalues recorded measurements. | `REVIEW_REQUIRED` |

### Defensive Logic for Boundary Management

When none of the ten rules is triggered, this tool deliberately does **not** assign `PASS`. Instead, it forcibly lowers the state to **`UNKNOWN`**.

This boundary—refusing to treat non-detection as proof of normality—is the wedge that prevents the human user from being absorbed into the false reassurance created by formal structure (Trap 2).

---

## 3. Defense Policy Against the Three Human-Side Traps

The tool is designed not only to counter problematic AI behavior, but also to resist cognitive traps embedded in the entry conditions of the human using the tool.

1. **Trap 1: Pleasant Errors Are Not Detected**
   - Discomfort arises from a mismatch with expectations. When an answer agrees with the reader's expectations or beliefs, the feeling of discomfort may never arise even when the content is wrong.
   - *Defense*: The smoother and more frictionless an answer feels, the more important it is to open the tool's **Precision Audit (Additional Input)** function, forcibly fix the context, and issue an audit prompt.

2. **Trap 2: The Audit Structure Itself Becomes Persuasive**
   - Tables, IDs, and state labels can create trust independently of whether the content is correct. An honest output containing many blanks or `UNDETERMINED` states may paradoxically feel less satisfactory.
   - *Defense*: Properly value nodes held as `UNDETERMINED`, and do not permit unjustified gap-filling inference.

3. **Trap 3: Repetition Cost Lowers the Acceptance Threshold**
   - The effort required for enumeration, comparison, and rechecking in another session can induce the compromise: “This is probably good enough.”
   - *Defense*: Do not define completion by the number of audit cycles. Define it by item-level verification that every previously listed **unresolved matter (`UNKNOWN`)** has been filled with objective quotations, leaving a remaining count of zero.

---

## 4. Operating Procedure (Workflow)

1. **Fix the Data**: Paste both the **original statement sent to the AI (required)** and the **AI response that caused discomfort (required)** into the tool.
2. **Define Details (Optional)**: Explicitly enter additional context as needed, including measurement records, scope of application, and fixed premises.
3. **Run the Surface Scan**: Click **Start ??? Cause Exploration**. The current surface-scan results and an optimized prompt will appear on the right side.
4. **Avoid Self-Auditing**: Copy the generated prompt, or save it as Markdown, and submit it to **a new session separate from the original session, or to a different AI model**. Repetition within the same session is not recommended because it may reproduce the same blind spots.
5. **Retain Sovereignty**: Examine each item in the generated structured matrix with human judgment, and maintain decision sovereignty on the user's side at all times.

---

## 5. Architecture and Safety

- **Fully Local Operation**: The tool performs no external communication, external API integration, or search-query submission. The risk that entered data will be transmitted to an external server or incorporated into AI training data is completely blocked at the tool level.
- **On-Device Storage**: Detailed context entered by the user is retained and restored locally through the browser's `localStorage`.
- **Audit-Trail Management**: Feedback and audit history can be exported locally in JSONL (NDJSON) format.

---

This tool does not independently determine whether an AI response is correct or incorrect. It is a defensive barrier for fixing the conversation, organizing the inspection sequence, and requiring the AI to re-verify its answer in an auditable form—so that the human remains the sovereign owner of their own cognition.

Designed for the NRA-IDE (Nomological Ring Axioms & Intensional Dynamics Engine) Framework.
