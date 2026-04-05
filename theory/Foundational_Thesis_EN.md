# Nomological Ring Axioms and the Intensional Dynamics Engine
## — A Structural Description of Threshold-Driven State Transitions —
### ( Part I: General Audience / Part II: Specialist Audience )

Author: M-Tokuni
NRA-IDE Project
Version 2.0 (English)

---

# Part I: General Audience
## "Why Does the World Sometimes Break Suddenly?"

---

## Abstract

We intuitively feel that change happens gradually. Yet in reality, bridges collapse without warning, bodies reach their limits, and power grids cascade into failure — all while measured values showed almost no change until that very moment.

Part I presents a framework for understanding this "suddenness" in structural terms rather than mathematical equations. No specialist knowledge is required. Only three concepts are needed: **accumulation**, **margin**, and **limit**.

---

## 1. Introduction: Phenomena That Continuous Change Cannot Explain

### 1.1 Before a Disaster, People Can Only Stand in Shock

On March 11, 2011, when the tsunami from the Great East Japan Earthquake overtopped the seawalls, the people standing there could do nothing. The seawalls had been functioning exactly as designed — until that moment.
Meteorological readings had been rising. Ground stress had been accumulating. Yet no one could accurately predict "how many minutes until it overflows." What was being observed was the *rate of change*. But the essence of the problem was *the distance remaining to the boundary*.
This is not unique to tsunamis.
A mountain slope weakens slowly over decades. Then in one instant, it collapses. A bridge's steel absorbs millions of repetitive vibrations. Then on a quiet morning, it suddenly fractures. A physician confirms that a patient's test values are within normal range. Yet the following day, an organ stops functioning.

**In every case, the rate of change was small. But the approach to the boundary had been advancing.**

Most conventional scientific descriptions are built around "velocity," "acceleration," and "rate of change." Newtonian mechanics and calculus are prime examples, functioning with exceptional precision in stable regions. However, these frameworks are not well suited to directly describing *how close a state is to its boundary*.
That is the starting point of this framework.

### 1.2 Why Could It Not Be Predicted?

The reason it could not be predicted was not that the wrong quantities were being measured. The problem was the **perspective** of measurement.
Measuring "velocity" requires time. Measuring "distance" requires a reference point. Both are quantities for describing *how change progresses*.
But when a structure approaches its limit, the essential question lies elsewhere.

**"How much more can this structure endure?"**

Answering this question requires different quantities. Not "velocity" but "accumulated amount." Not "distance" but "remaining margin." This framework is built around the ratio of those two quantities.

---

## 2. Core Axiom: Existence Is Generation

### 2.1 Static States Do Not Exist

The idea at the foundation of this framework can be expressed in a single sentence.

**Existence is generation.**

This is not a philosophical declaration — it is a structural observation.
A cup sitting on a desk appears to be at rest. Yet within it, molecules are vibrating and the material is continuously accumulating microscopic stress. "Stillness" is an approximation at the scale of human observation, not a structural reality.
The same holds for the living body. Even during sleep, the heart beats, cells metabolize, and neurons transmit signals. Complete stasis means death — and even that proceeds at the molecular level as a process of decomposition.

**Absolute stillness exists nowhere.**

### 2.2 History Accumulates

From the axiom "existence is generation," an important consequence follows.
Generative processes **accumulate history**.
Metal accumulates fatigue through repeated stress. The body consumes its capacity for repair as it ages. Infrastructure accumulates degradation through use. AI systems accumulate error.
This accumulation is difficult to see. It often does not appear on the surface of measured values. But it proceeds with certainty. And when the accumulation built up within a structure crosses a threshold — a state transition occurs.

### 2.3 The Same History Never Recurs

A further consequence follows.
Since generative processes carry history, **an identical state can never be perfectly reproduced**.
This is a structural qualification of the premise that "identical conditions yield identical results." Even when surface conditions are the same, if the internally accumulated histories differ, the structural response will differ.
This perspective carries important meaning for explaining the gap between reproducibility in laboratory experiments and behavior in real operational environments.

---

## 3. Intuitive Explanation of the Primary Equation

### 3.1 The Analogy of the Mechanical Clock

To understand the operating principle of this framework, consider the escapement mechanism of a mechanical clock.
A mechanical clock maintains accuracy not because its gears are perfect. It is because **the escapement advances in discrete, complete steps of exactly one tooth** — no fractional remainder carries forward.
Microscopic errors dissipate as heat rather than accumulating into the next calculation. Each step is structurally complete.
This is the operating principle of this framework. Rather than stacking continuous approximations, each state transition is made structurally complete, preventing the accumulation of error.

### 3.2 Three Quantities

This framework is composed of only three quantities.

**δ (delta): Accumulated Deviation**

The amount of deviation accumulated within a structure as history. For materials this corresponds to fatigue; for biological systems, stress; for engineered systems, load accumulation. δ tends to increase over time.

**τ (tau): Absorption Thickness**

The amount of margin a structure has for absorbing accumulated deviation. For materials this corresponds to toughness; for biological systems, tolerance; for engineered systems, buffer capacity. τ is determined at design time and may change with conditions.

τ is **not a time constant**. It is a structural margin of tolerance, independent of the time axis.

**R: Structural Ratio**

The ratio of δ to τ, defined by the following equation.

$$R = \frac{\delta}{\tau}$$

This is the primary equation of this framework.

### 3.3 What R Signifies

The value of R indicates the current structural state of the system.
When R is close to 0, accumulated deviation is small relative to the structural margin. The system is in a stable region — normal operating state.

As R approaches 1.0, accumulated deviation is exhausting the structural margin. The approach to the boundary is advancing.

**When R exceeds 1.0, the structure can no longer absorb the deviation. A state transition occurs.**

In materials engineering this transition is called "fracture." In medicine, "organ failure." In power engineering, "cascading power failure." In this framework all of these are treated uniformly as "states beyond the structural threshold."

### 3.4 Everyday Examples

**Stress Fracture**

When a marathon runner continues training without adequate rest, microscopic cracks accumulate in bone (increase in δ). The bone's repair capacity is finite; when accumulation outpaces repair, margin decreases (decrease in τ). When R exceeds 1.0, a fracture occurs. The problem was not the "velocity" of training volume but the ratio of accumulation to margin.

**Bridge Collapse**

A bridge absorbs microscopic vibration with each passing vehicle. How far the accumulation of this stress (δ) has progressed relative to the design tolerance (τ) determines the bridge's remaining service life. Even when appearance is unchanged, R is quietly approaching 1.0.

**Burnout**

The human body absorbs daily stress (τ). But stress that cannot be absorbed accumulates (δ). If τ does not recover through rest, R continues to rise. It is not the continuous change of "feeling a little tired" — at the moment a threshold is crossed, the body ceases to function.

---

## 4. Summary (Part I)

### 4.1 What Problem Is Being Solved

Conventional monitoring and control frameworks are built around "the rate of change." Temperature rising at a certain rate, pressure increasing at a certain rate, values deviating from norms at a certain rate — these are monitored, and the design responds *after* an anomaly appears.
But here lies a fundamental problem.

**State transitions occur before anomalies appear.**

The moment a bridge fractures, a bone breaks, an organ stops — in every case, while measured values were "still within normal range," the internal accumulation had already exceeded its limit. Monitoring velocity is not fast enough.
What this framework seeks to solve is this problem: the shift from "monitoring that notices after an anomaly appears" to "diagnosis that grasps proximity to the boundary in real time."

### 4.2 What Kind of Solution Is Being Pursued

This framework does not aim at "prediction."
Calculating "when it will break" is nearly impossible in most real systems. Too many variables, too complex a history. The more refined the predictive model, the more likely it diverges from reality.

What this framework aims at is **diagnosis**.

"How close is this structure to its limit right now?" — this single point is evaluated through the simple ratio R = δ/τ. If R is 0.3, there is margin. If R is 0.8, caution is needed. If R exceeds 1.0, a state transition has already occurred.
Even without prediction, diagnosis is possible. With diagnosis, the decision to intervene can be delegated to a human operator. This is the form of resolution this framework seeks.

### 4.3 How to Change the Way of Seeing

Understanding this framework requires changing only one thing about what is monitored.

| Conventional perspective | This framework's perspective |
|--------------------------|------------------------------|
| Monitor the rate of change | Monitor the ratio of accumulation to margin (R) |
| Feel reassured that values are "still within normal range" | Judge by "what is the value of R" |
| Respond after an anomaly appears | Intervene when R approaches 1.0 |
| Track change along a time axis | Read the current value of the structural ratio |
| Build refined predictive models | Measure δ and τ and calculate the ratio |

This shift in perspective requires no new measurement instruments. No need to learn a new theory from scratch. What is required is only a change in the question: "what do we measure?"

Measure accumulated deviation δ. Define absorption thickness τ. Monitor the ratio R. When R approaches 1.0, call for judgment — this simple procedure is the only structurally sound and practical means of preparing for "sudden collapse."

Part II defines this framework rigorously from a specialist perspective, detailing the dynamic τ extension formula, Integer Phase Lock, Fail-Closed design, and application across domains.

---

# Part II: Specialist Audience
## "Structural Definitions of the Nomological Ring Axioms and the Intensional Dynamics Engine"

---

## 5. Relationship to Existing Theories

### 5.1 Differences from Continuum Mechanics and Calculus

Classical dynamical theories based on Newtonian mechanics and calculus describe system behavior through the time derivatives of state. This framework has extremely high descriptive power in stable regions (R ≪ 1).
This framework does not deny these theories. However, there is a fundamental difference in perspective.

Classical dynamics describes **"how the system changes."**
This framework evaluates **"how close the system is to its structural threshold."**
The former is the description of a trajectory; the latter is the diagnosis of proximity. These are complementary and do not conflict.

### 5.2 Differences from PID Control

PID control is a control theory that corrects deviation through three terms: proportional (P), integral (I), and derivative (D).
The R = δ/τ of this framework may appear superficially similar to the proportional term of PID, but the two are fundamentally different.

| Aspect | PID Control | This Framework (NRA-IDE) |
|--------|-------------|--------------------------|
| Purpose | Return deviation to zero (optimization) | Evaluate proximity to structural limit (diagnosis) |
| Meaning of τ | Does not exist | Structural tolerance width (independent of time) |
| Treatment of residuals | Accumulated as integral term | Expelled as heat, not carried forward |
| Form of output | Continuous control quantity | Discrete state judgment (R < 1 / R ≥ 1) |
| Role of human | System corrects autonomously | Human takes over when R ≥ 1 |

τ is not a time constant. τ is the thickness of the tolerance width that a structure holds by design — a structural quantity independent of the time axis.

### 5.3 Differences from Statistical Methods and Machine Learning

Statistical methods and machine learning probabilistically estimate future states from past data distributions. These function powerfully in regions where large amounts of data exist and distributions are stable.
The differences from this framework are as follows.
Statistical methods learn "average behavior." This framework evaluates "the current state of an individual structure." The former is set-theoretic; the latter is individualist.
Furthermore, statistical methods presuppose probabilistic approximation. This framework does not use probabilistic reasoning; it performs deterministic computation of R from measured values of δ and τ.

---

## 6. Rigorous Description of the Definition Equations

### 6.1 Primary Equation: Basic Structural Ratio

$$R = \frac{\delta}{\tau}$$

**Rigorous definitions of each quantity**

**δ (delta): Accumulated Deviation**
The amount of deviation accumulated as history within a structure. δ is a non-negative real number, updated with each state transition of the structure. The rate of accumulation of δ differs by domain and target.

**τ (tau): Absorption Thickness**
The amount of margin a structure has for absorbing accumulated deviation. τ is a positive real number, defined at design time. τ is not a time constant; it is a structural parameter independent of the time axis. τ may change dynamically (see 6.2).

**R: Structural Ratio**
The ratio of δ to τ. R is a dimensionless real number indicating proximity to the structural threshold.

**Decision Criteria**

| Value of R | Structural State | System Behavior |
|------------|-----------------|-----------------|
| R < 1 | Stable region | Continue normal output |
| R = 1 | Structural threshold | Output warning, notify human |
| R > 1 | Threshold exceeded | Cease output, delegate to human |

When R exceeds 1.0, the system does not make autonomous judgments. It presents information, falls silent, and delegates final judgment to the human operator. This is called **Fail-Closed**.

### 6.2 Secondary Equation: Dynamic τ — Dual-Fluctuation Formula

A static τ cannot appropriately handle asymmetric variation in the expansion and contraction directions. To address this, dynamic τ is defined.

**Upper EMA (Expansion-Direction Fluctuation)**

$$\mathrm{EMA}_{\text{upper}}(n) = \alpha_u \cdot \delta_u + (1 - \alpha_u) \cdot \mathrm{EMA}_{\text{upper}}(n-1)$$

The upper EMA smooths deviation δ_u in the expansion direction. α_u is the upper smoothing coefficient (0 < α_u ≤ 1).

**Lower EMA (Contraction-Direction Fluctuation)**

$$\mathrm{EMA}_{\text{lower}}(n) = \alpha_l \cdot \delta_l + (1 - \alpha_l) \cdot \mathrm{EMA}_{\text{lower}}(n-1)$$

The lower EMA smooths deviation δ_l in the contraction direction. α_l is the lower smoothing coefficient (0 < α_l ≤ 1).

**Asymmetric Definition of Dynamic τ**

$$\tau_{\text{upper}} = \tau \cdot f\!\bigl(\mathrm{EMA}_{\text{upper}}\bigr)$$

$$\tau_{\text{lower}} = \tau \cdot g\!\bigl(\mathrm{EMA}_{\text{lower}}\bigr)$$

The upper τ expands in the expansion direction; the lower τ contracts in the contraction direction. This asymmetry is the structural core of this framework. Most real systems exhibit different response characteristics in the expansion and contraction directions.

**Final Decision Formula (Asymmetric Dual Ratio)**

$$R = \max\!\left( \frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},\ \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}} \right)$$

The larger of the upper and lower ratios is adopted as R. This formula **operates within a closed world** and requires no external assumptions.

### 6.3 Definition of Phase Transition

What occurs when R exceeds 1.0 is not merely a "numerical exceedance." The system **transitions to a qualitatively different state**. This framework calls this a **phase transition**.

The structure is identical to phase transitions in physics — water becoming ice, liquid becoming gas. A continuous quantity changes, and at a certain threshold the phase changes suddenly. The change was continuous, but the state transition occurred discontinuously.
Phase transitions in this framework are defined as follows.

```
R < 1.0  : Stable phase   (accumulated deviation within absorption thickness)
R = 1.0  : Phase transition point (structural threshold)
R > 1.0  : Post-transition phase (structure unable to absorb deviation)
```

The critical point is that the post-transition phase is **structurally different** from the pre-transition phase. Even if R is returned below 1.0, the accumulated history does not disappear. A fractured bone does not return to its original state. A collapsed bridge does not recover naturally. **Phase transitions are irreversible.**
This irreversibility is the basis for "intervening before R approaches 1.0." The value lies in diagnosis before transition, not in response after transition.

### 6.4 The Survival Domain Formed by Dual Fluctuation

To understand the asymmetric structure of dynamic τ visually, consider the Survival Domain formed by τ.

```
  ── τ_upper ──────────────────────  Upper boundary (expansion direction)
        ↑
   Survival Domain
  (space where fluctuation is tolerated)
        ↓
  ── τ_lower ──────────────────────  Lower boundary (contraction direction)
```

This is called the **Survival Domain**. As long as the system's state remains within the Survival Domain, fluctuation is absorbed by the structure and no phase transition occurs.
The dual-fluctuation formula matters because τ_upper and τ_lower **move asymmetrically**.
When fluctuation in the expansion direction grows larger, τ_upper expands — the system attempts to tolerate that fluctuation over a wider range.
When fluctuation in the contraction direction grows larger, τ_lower contracts — the system tightens the margin on the lower side, structurally constraining excessive contraction.
This asymmetric movement **changes the shape of the Survival Domain**. Rather than a simple symmetric region, it is a living boundary that reshapes itself in response to the system's state.

**Reinterpretation of R**

The final decision formula $R = \max\!\left( \frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},\ \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}} \right)$ evaluates "how close the current state is to which boundary of the Survival Domain." It simultaneously monitors approach to the upper and lower boundaries, adopting the ratio of the more dangerous side as R.

### 6.5 The Survival Domain and Homeostasis

The concept of the Survival Domain shares the same structure as **homeostasis** in biology.
The human body maintains core temperature within a Survival Domain of approximately 36–37°C. Even when body temperature fluctuates, the organism attempts to return to within the Survival Domain through sweating, fever, and vasoconstriction. The moment the Survival Domain is significantly exceeded, organs begin to lose function — a phase transition occurs.
Blood glucose is the same. Blood pressure is the same. All of these are maintained within the asymmetric Survival Domain formed by τ_upper and τ_lower.

This framework generalizes the structure of biological homeostasis to materials, infrastructure, and AI systems.

**The Perspective of Designing the Survival Domain**

In system design using this framework, setting τ becomes the question: "where is the Survival Domain placed?" A larger τ means a wider Survival Domain, allowing the system to tolerate more fluctuation. A smaller τ means a narrower Survival Domain: the system is controlled more precisely, but the risk of phase transition rises.

Furthermore, the asymmetric ratio of τ_upper to τ_lower is a design decision about "which direction of fluctuation to tolerate more." In medicine, the tolerance width differs between excessive treatment (expansion direction) and insufficient treatment (contraction direction). In infrastructure, degradation characteristics differ between overload and underload. Explicitly incorporating this asymmetry into design is the essential meaning of dynamic τ.

---

## 7. Design Principles of the IDE (Intensional Dynamics Engine)

### 7.1 Integer Phase Lock

This engine does not process state transitions as continuous floating-point values. Each state transition is treated as a **discrete, structurally complete step**.

Residual ε (the fractional remainder generated by floating-point arithmetic) is not carried forward to the next step. Residuals are **expelled as heat**. This structurally prevents the accumulation of error.

```
In computing R = δ / τ :
  Integer part of quotient  →  used for next state judgment
  Residual ε                →  discarded (expelled as heat)
  Carry-over                →  prohibited
```

This principle follows the same logic as the escapement of a mechanical clock.

### 7.2 Fail-Closed Design

Fail-Closed does not mean system halt. It refers to a design that **suppresses output while maintaining structural state**.

When R ≥ 1.0 is judged:
- The system does not make autonomous judgments, offer alternatives, or engage in exploration
- It presents only information about the structural state
- It falls silent and waits for human judgment
- It records human judgment in a log, making the locus of responsibility clear

This is not "giving up" — it is **the clarification of the division of responsibility between human and machine**. The machine diagnoses; the human judges.

### 7.3 Axiom of Confession

This framework obligates disclosure of the fact when approximate computation has been used. This is called the **Axiom of Confession**.

Cases requiring disclosure:
- When floating-point arithmetic is used: report "Linear approximation distortion has occurred."
- When causal inversion (back-projection) is used: report "Causal violation (inverse projection) detected."
- When the linear domain is exceeded: report "Linear boundary exceeded."

This axiom does not prohibit approximation. It **prohibits concealing the use of approximation**. The purpose is to secure the information a human needs to make an appropriate judgment.

---

## 8. Application Across Domains

### 8.1 Medical Domain

δ = Physiological pressure (accumulation of stress, load, inflammatory markers, etc.)
τ = Biological resilience (organ reserve, immune capacity, repair capability)

In cancer treatment support, the ratio of accumulated physical load from treatment (δ) to patient tolerance (τ) is continuously evaluated. When R approaches a set alert level, adjustment of treatment intensity is presented to the physician. The IDE does not judge. It presents diagnostic information and delegates final judgment to the physician.

### 8.2 Infrastructure Domain

δ = Accumulation of structural deviation (fatigue, degradation, load history)
τ = Design tolerance (safety factor, buffer capacity)

For power networks, bridges, and building structures, using dynamic τ enables the precursors of cascading failure to be evaluated as a structural ratio. Rather than anomalous readings from a single sensor, the accumulated state of the entire system is visualized as R.

### 8.3 AI Safety Domain

δ = Model output deviation, hallucination frequency, error accumulation
τ = Design tolerance for error, confidence boundary

Whether an AI system's output is within a structurally trustworthy range is evaluated by R. When R ≥ 1.0, output is halted and the matter is delegated to a human. This structurally prevents the worst case of "AI asserting a lie with confidence."

---

## 9. Prevention of Misreading: Strict Boundaries of Definition

Because this framework uses terminology similar to existing theoretical frameworks, the following misreadings are liable to occur. They are explicitly denied here.

**τ is not a time constant.**
τ is a structural tolerance width independent of the time axis. A time constant is defined as a function of time; τ is a structural parameter defined at design time.

**R = δ/τ is not SNR (signal-to-noise ratio).**
SNR is the ratio of signal to noise power — an information-theoretic concept. R is the ratio of structural deviation to tolerance width — a structural diagnostic quantity for threshold judgment.

**Floating-point arithmetic is not prohibited.**
In accordance with the Axiom of Confession, disclosure when used is obligatory. Not use itself, but concealment, is prohibited.

**Integer Phase Lock does not mean all values must be integers.**
It means each state transition is structurally complete. The principle is that residuals are not carried forward to the next step.

**Fail-Closed is not system halt.**
It refers to a design that suppresses output while maintaining structural state and waits for human judgment.

**NRA-IDE is not an Integrated Development Environment.**
IDE is an abbreviation of Intensional Dynamics Engine. It is an engine for evaluating structural state, not a software development tool.

---

## 10. Conclusion

This paper has presented the Nomological Ring Axioms and the Intensional Dynamics Engine in a two-part structure.
Part I began from the real-world problem of sudden state transitions that continuous change cannot explain, and presented the shift in perspective from "monitoring velocity" to "diagnosing the structural ratio."
Part II provided rigorous definitions of the primary equation R = δ/τ and the asymmetric dual ratio using dynamic τ, and described the three design principles of Integer Phase Lock, Fail-Closed, and the Axiom of Confession.
The core of this framework is diagnosis, not prediction. Not calculating "when it will break," but evaluating "how dangerous it is right now" and realizing a structure that, the moment a threshold is exceeded, delegates judgment to a human.
This principle can be applied as an identical structure across different domains: materials, medicine, infrastructure, and AI safety. As a unified diagnostic framework crossing domain boundaries, the applicability of this framework is broad.

---

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
