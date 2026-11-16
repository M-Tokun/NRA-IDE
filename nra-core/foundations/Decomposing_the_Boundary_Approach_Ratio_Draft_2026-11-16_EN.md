---
id: DRAFT-OPEN-SYSTEM-R-DECOMPOSITION-20261116-EN
kind: draft
created: 2026-11-16
author: M-Tokuni
status: Non-canonical explanation (approved by the user, 2026-11-16). Sentence-level JP/EN check done; seven new terms registered in the dictionaries
classification: current explanatory
title: "Decomposing the Boundary-Approach Ratio — Derived Formulas for Reading Open Systems from the Primary Formula"
related:
  - DIALOG-OPEN-DYNAMICS-REVIEW-20261116
  - DRAFT-OPEN-SYSTEM-R-DECOMPOSITION-20261116
---

**Author: M-Tokuni** / Japanese version: [開放系_境界接近比の増分分解_論文草案_2026-11-16.md](./開放系_境界接近比の増分分解_論文草案_2026-11-16.md) (the Japanese version is the paired original; terms follow `FORMULA.md` and the dictionary)

# Decomposing the Boundary-Approach Ratio — Derived Formulas for Reading Open Systems from the Primary Formula

> **Status**: This is a non-canonical explanation (approved by the user, 2026-11-16) and is not canonical. Every formula here is a derived or auxiliary formula in the sense of `theory/AXIOMS.md` v2.5 §5. It changes neither the Nomological Ring Axiom, the Primary Formula, the Secondary Formula, the canonical states, the thresholds, nor the irreversible latch. Numerical examples are demonstration values, not measurements.

## Abstract

An open system receives events from outside that cannot be known in advance. This paper does not add a new term for this fact. It opens up the Primary Formula $R=\delta/\tau$ instead.

1. The increment of $R$ splits exactly into four paths: action penetration, residual penetration, degradation contraction, and composition change (Eq. 3).
2. $R$ is the sum of a part that returns when the action is removed and a part that does not (Eq. 4). The part that does not return does not decrease unless a structural element is added.
3. How large the next event must be to reach each threshold is determined by the current $\delta$ and $\tau$ alone (Eq. 5). The size the structure can still receive can be shown without predicting the event.

All three are algebraic identities obtained from the Primary Formula and the definitions of `FORMULA.md` §0.5; they contain no new assumption.

## 1. Starting Point

Three dialogue records[^1] left two issues for describing open systems: separating physical action entering from outside from the observer's not-knowing, and connecting that description to $\delta$, $\tau$, and $R$.

This paper starts from the second. The Primary Formula is basic and short. What an open system asks is "why did $R$ move," "how much of it returns," and "how much more can be received." These can be answered by opening up the Primary Formula.

The definitions are those of `FORMULA.md` §0.5. $n$ is the structural update number and denotes the order of events; time is kept in each event record.

$$
R_n=\frac{\delta_n}{\tau_n},\qquad \delta_n=q_n+p_n,\qquad \tau_n=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_n)_{e\in\mathsf{Active}_n}\bigr)
\tag{1}
$$

- $q_n$: reversible component. $p_n$: residual deviation, which does not decrease during evaluation.
- $\tau^{[e]}_n=(1-\lambda^{[e]}_n)\,\tau^{[e]}_0$: $\lambda^{[e]}_n$ is the degradation fraction, which does not decrease during evaluation.
- $\mathsf{Active}_n$: the composition, changed by addition or removal of a structural element.

## 2. Distinctions: Boundary and Transition

Before writing formulas, the words "boundary" and "transition" are separated by what they refer to. Putting different types into one symbol creates a path by which a change on the natural side rewrites the evaluation standard.

**Boundaries are divided into three.**

| Kind | Content | Example | Handling when it changes |
|---|---|---|---|
| Structural boundary of the target | Physically part of the target structure | Cell membrane, ice–water interface, root surface | Enters the event allocation rule $\mathsf{Alloc}$ (Eq. 2) as an observed physical change |
| Declared boundary | A division of the evaluation target fixed in the evaluation declaration | Field plot, range of the member evaluated | End the evaluation and redeclare |
| Evaluation boundary | Thresholds on $R$ | $R_{\mathrm{warn}}$, $R_{\mathrm{handoff}}$, $R_{\mathrm{irrev}}$, $1.0$ | Not changed during evaluation |

**Transitions are divided into four.**

| Kind | What changes | Symbol |
|---|---|---|
| Update of the target state | Physical state of the target | $(q_n,p_n,\lambda_n)$ |
| Update of the composition | Addition/removal of a structural element | $\mathsf{Active}_n$ |
| Transition of the evaluation state | Canonical state and irreversible latch | `PERMIT` → … → `RUPTURE_BOUNDARY` |
| Switch of declaration | The evaluation itself | $\mathsf{Decl}\to\mathsf{Decl}'$ |

The first two occur on the target side and are known by Cause-Side observation. The third is an evaluation output determined by $R$ and the thresholds. The fourth occurs only between evaluations, and $R$ is not compared across the switch. Evaluation outputs are not fed back into the target state (AXIOMS §14).

## 3. Formulas

### 3.1 Allocation of Events (restatement of the canon)

An observation event $\mathrm{Ev}_n$ has exactly one allocation target under the allocation rule.

$$
\mathsf{Alloc}(\mathrm{Ev}_n)=\bigl(a_n,\ \Delta p_n,\ \Delta\lambda_n,\ \mathrm{ctx}_n\bigr)
\tag{2}
$$

The action $a_n$ produces the reversible component, $\Delta p_n\ge0$ increases residual deviation, and $\Delta\lambda_n\ge0$ increases the degradation fraction. Addition or removal of a structural element is recorded as an update of $\mathsf{Active}_n$. A receiving width temporarily narrowed by a condition that returns when the condition ends ($q^{\mathrm{temp}}_n$, `FORMULA.md` §0.5.3) is likewise allocated to $a_n$ and included in $q_n$ (the action penetration term and the reversible part of the ratio).

### 3.2 Splitting the Change of Thickness into Two

$\Delta\tau_n=\tau_n-\tau_{n-1}$ is split into the change that occurs when the composition is kept at $n-1$, and the change due to an update of the composition.

$$
\Delta\tau^{\mathrm{deg}}_n=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_n)_{e\in\mathsf{Active}_{n-1}}\bigr)-\tau_{n-1}\ \le 0,
\qquad
\Delta\tau^{\mathrm{comp}}_n=\tau_n-\mathrm{Comp}_\tau\bigl((\tau^{[e]}_n)_{e\in\mathsf{Active}_{n-1}}\bigr)
$$

$\Delta\tau_n=\Delta\tau^{\mathrm{deg}}_n+\Delta\tau^{\mathrm{comp}}_n$. $\Delta\tau^{\mathrm{deg}}_n\le0$ follows from $\lambda$ not decreasing and $\mathrm{Comp}_\tau$ being non-decreasing in each argument. $\Delta\tau^{\mathrm{comp}}_n$ can be positive only through addition of a structural element (AXIOMS §7).

### 3.3 Increment Decomposition (the core of this paper)

When $\tau_{n-1}>0$ and $\tau_n>0$:

$$
\boxed{
R_n-R_{n-1}
=\underbrace{\frac{\Delta q_n}{\tau_n}}_{\text{action penetration term}}
+\underbrace{\frac{\Delta p_n}{\tau_n}}_{\text{residual penetration term}}
+\underbrace{R_{n-1}\,\frac{-\Delta\tau^{\mathrm{deg}}_n}{\tau_n}}_{\text{degradation contraction term}}
-\underbrace{R_{n-1}\,\frac{\Delta\tau^{\mathrm{comp}}_n}{\tau_n}}_{\text{composition term}}
}
\tag{3}
$$

The derivation takes two lines. Into the decomposition into penetration and contraction terms in the note of `FORMULA.md` §4.7,

$$
R_n-R_{n-1}=\frac{\Delta\delta_n}{\tau_n}+\delta_{n-1}\left(\frac{1}{\tau_n}-\frac{1}{\tau_{n-1}}\right),
$$

substitute $\Delta\delta_n=\Delta q_n+\Delta p_n$ and $\delta_{n-1}\bigl(\tfrac{1}{\tau_n}-\tfrac{1}{\tau_{n-1}}\bigr)=R_{n-1}\,\tfrac{-\Delta\tau_n}{\tau_n}$, then split $\Delta\tau_n$ as in 3.2.

The four terms differ in the nature of their sign.

| Term | Sign | Meaning | Corresponding field operation |
|---|---|---|---|
| Action penetration | Either | The part that moves with the action | Reduce or stop the action |
| Residual penetration | $\ge0$ | Increase of the part that remains after the action is removed | Cannot be undone during evaluation |
| Degradation contraction | $\ge0$ | The part where the capacity has narrowed through damage | Cannot be undone during evaluation |
| Composition | Lowers $R$ on addition, raises it on removal | The part where the composition of the capacity changed | Addition/removal of a structural element |

During an evaluation, only two paths can lower $R$: reducing the action and adding a structural element. Residual deviation and degradation proceed in one direction only. Straightening a bend or stretch by force (correction) ends the evaluation and redeclares it; it is not a term of Eq. 3.

The double-fluctuation detection condition $\Delta\delta_n>0\land\Delta\tau_n<0$, when $\delta_{n-1}>0$, corresponds in Eq. 3 to "the contributions of the first two terms sum to a positive value" and "the contributions of the last two terms sum to a positive value." Eq. 3 does not replace the detection condition; it discloses which path acted when the condition holds. When $\delta_{n-1}=0$ ($R_{n-1}=0$), the latter two terms of Eq. 3 become 0, and the vessel contraction in that update appears in the denominator $\tau_n$ of the first two terms and in the decrease of the threshold margin $m_{\theta,n}$ of Eq. 5.

### 3.4 The Part That Returns and the Part That Does Not

Splitting only the numerator of Eq. 1 gives:

$$
R_n=\underbrace{\frac{q_n}{\tau_n}}_{R_{\mathrm{rev},n}}+\underbrace{\frac{p_n}{\tau_n}}_{R_{\mathrm{res},n}},
\qquad R_n\ \ge\ R_{\mathrm{res},n}
\tag{4}
$$

$R_{\mathrm{res},n}$ is the approach that remains even if all action is removed now. Since $p_n$ does not decrease and $\tau_n$ does not increase unless a structural element is added, $R_{\mathrm{res},n}$ does not decrease unless a structural element is added. $p_n$ does not decrease, but if $\tau_n$ increases through addition of a structural element, $R_{\mathrm{res},n}=p_n/\tau_n$ decreases. Also, even if $m_{\theta,n}>0$, the irreversible latch $\ell_n=1$ that was engaged after reaching $R_{\mathrm{irrev}}$ in the past is not automatically released (AXIOMS §10.4).

If $R_{\mathrm{res},n}$ is at or above a threshold, removing the action alone does not bring $R$ below that threshold. This disclosure gives people in the field material to judge whether stopping will bring it back or not. $R_{\mathrm{rev}}$ and $R_{\mathrm{res}}$ do not redefine $R$ and do not classify canonical states. State classification is done by $R$ and the thresholds alone.

### 3.5 How Large a Single Next Event the Structure Can Receive

For a threshold $\theta$ (any of $R_{\mathrm{warn}}$, $R_{\mathrm{handoff}}$, $R_{\mathrm{irrev}}$, $1.0$), define the threshold margin:

$$
m_{\theta,n}=\theta\,\tau_n-\delta_n
\tag{5a}
$$

When $\tau_{n+1}>0$, the following equivalence holds.

$$
\boxed{
R_{n+1}\ \ge\ \theta
\iff
\Delta\delta_{n+1}-\theta\,\Delta\tau_{n+1}\ \ge\ m_{\theta,n}
}
\tag{5b}
$$

At $\theta=1$, $m_{1,n}=\tau_n-\delta_n=M_\tau$ (remaining absorption margin, `FORMULA.md` §2). $m_{\theta,n}\le0$ means that threshold has already been reached. $m_{\theta,n}\le0$ means that the current $R_n$ is at or above that threshold (the holding of the irreversible latch engaged after reaching $R_{\mathrm{irrev}}$ in the past is separate).

Eq. 5 does not say what will happen next. From current observations alone, it says how much an event that has occurred must increase $\delta$ and decrease $\tau$ to reach each threshold. The $-\theta\,\Delta\tau$ on the left shows that a decrease of thickness acts with weight $\theta$. Eq. 5 is an equivalence condition on the next step's $\Delta\delta,\Delta\tau$; it does not predict the magnitude or timing of the event. $m_{\theta,n}>0$ is the margin as of now; a decrease of thickness $\Delta\tau<0$ in the next event is not taken into account.

## 4. Where "the Unknown" Is Placed

One dialogue record made the unknown a term $\Gamma(t)$ of the formula and treated it as a force that drives the system. This paper does not make the unknown a term. What drives the system is physical action entering from outside; the unknown is a state of the record. Its placement divides into four.

| Situation | Handling | Relation to the formulas |
|---|---|---|
| The event occurred and was observed | Enters as $\mathrm{Ev}_n$ into Eq. 2 and is allocated to the four paths of Eq. 3 | Whether it was foreseen does not affect allocation |
| No value can be obtained from the observation channel | Output `NOT_OBSERVABLE` with the reason; not filled with 0, stable, or safe | Disclose that $R_n$ is the value up to the last update that could be observed |
| Target, unit, time, or provenance is unknown | `CONFESSION`; not input to the Primary Formula | Stop the affected evaluation |
| Has not occurred yet | No term is placed in the formulas | The threshold margin of Eq. 5 shows the size that can be received |

An outbreak of pests and abnormal high temperature are, once they occur, observed physical events. Not having known them in advance does not change where they are allocated. Preparation for what is not known is held on the structural side, as the thickness of $\tau$ and the threshold margin. This is one reading of the NRA Structural-Persistence Principle of AXIOMS §3 (strictness without play collapses).

## 5. Numerical Example (demonstration values)

One element, $\tau_0=10$, $\mathrm{Comp}_\tau$ is the sum, and the thresholds are declared as $0.5$, $0.7$, $0.9$, $1.0$. All units are $u$. The values are placed to check the formulas and are not measurements in any domain.

| | $q$ | $p$ | $\lambda$ | $\tau$ | $\delta$ | $R$ | $R_{\mathrm{res}}$ |
|---|---|---|---|---|---|---|---|
| $n-1$ | 2 | 1 | 0.1 | 9 | 3 | 1/3 ≈ 0.333 | 1/9 ≈ 0.111 |
| $n$: action up, residual up, degradation | 3.5 | 1.5 | 0.2 | 8 | 5 | 5/8 = 0.625 | 3/16 ≈ 0.188 |
| $n+1$: only an element (thickness 4) added | 3.5 | 1.5 | 0.2 | 12 | 5 | 5/12 ≈ 0.417 | 1/8 = 0.125 |

The increment $7/24$ of update $n$ splits by Eq. 3 as follows.

| Action penetration | Residual penetration | Degradation contraction | Composition | Total |
|---|---|---|---|---|
| 3/16 | 1/16 | 1/24 | 0 | 7/24 |

The threshold margins at update $n$ are $m_{0.5}=-1$ (boundary warning point already reached), $m_{0.7}=0.6$, $m_{0.9}=2.2$, $m_{1}=3$. If $\Delta\delta-0.7\,\Delta\tau$ in the next event is $0.6$ or more, the pre-boundary human handoff point is reached.

At update $n+1$, the addition lowers $R$ by $5/24$. $p$ and $\lambda$ are unchanged. $R_{\mathrm{res}}$ fell because capacity was added; the residual deviation and degradation of the existing element remain. This is not restoration to the initial structure (AXIOMS §8).

The check was done with `nra-core/foundations/open_system_R_decomposition_check_20261116.py`. It computes in rational numbers, and Eqs. 3, 4, and 5b all agreed exactly.

## 6. When Continuous Time Can Be Used

Only when a domain has fixed a differentiation rule before evaluation, a form corresponding to Eq. 3 can be written.

$$
\frac{dR}{dt}=\frac{1}{\tau}\frac{d\delta}{dt}-\frac{R}{\tau}\frac{d\tau}{dt}
\tag{6}
$$

This is the derivative of $R=\delta/\tau$, not a formula that introduces time as a cause. $d\delta/dt$ and $d\tau/dt$ are obtained from direct observation or a pre-fixed rule. Dynamics specific to the target, such as growth or metabolism, enter on the side of the projection rule $\sigma$ as the governing equations of the domain. The formulas here do not replace them (AXIOMS §15.1).

## 7. What This Paper Does Not Claim

- Prediction of when an irreversible transition or rupture will occur.
- Comparison of $R$, $R_{\mathrm{res}}$, or $m_\theta$ across different evaluation declarations.
- Preparation for modes of failure other than the declared rupture mode. The threshold margin is meaningful only for the declared target, unit, and rupture mode.
- Describing natural phenomena by a single equation.

## 8. Discussion

The Primary Formula answers "how far has it come" with one ratio. Eq. 3 answers "by what," Eq. 4 answers "how much of it returns," and Eq. 5 answers "how much more can be received." All of them are information already at hand once $\delta$ and $\tau$ are obtained; no additional observation or estimation is required.

The field sense that the dialogue records valued corresponds to this decomposition. Discoloured leaves, the smell of soil, and hydraulic vibration become $\mathrm{Ev}_n$ as observable physical events. Human intervention appears in Eq. 3 as reducing the action and as adding a structural element. That some regions cannot be filled by computation is held as records by `NOT_OBSERVABLE` and `CONFESSION`.

On reproducibility as well, the same evaluation declaration and the same sequence of events give the same $R$. That history never becomes identical twice is compatible with the gauge reproducing (AXIOMS §2, supplement).

## 9. Symbols and Terms (tentative)

Names not in the canon are tentative. They were registered at the same time in both the Japanese and English dictionaries (2026-11-16; the reversible part and the residual part of the ratio are separate entries, seven in all).

| Symbol | Japanese (tentative) | English (tentative) | Class |
|---|---|---|---|
| $\Delta q_n/\tau_n$ | 作用進入項 | action penetration term | derived |
| $\Delta p_n/\tau_n$ | 残留進入項 | residual penetration term | derived |
| $R_{n-1}(-\Delta\tau^{\mathrm{deg}}_n)/\tau_n$ | 劣化縮小項 | degradation contraction term | derived |
| $R_{n-1}\,\Delta\tau^{\mathrm{comp}}_n/\tau_n$ | 構成変化項 | composition term | derived |
| $R_{\mathrm{rev},n}$, $R_{\mathrm{res},n}$ | 可逆接近分、残留接近分 | reversible part, residual part of the ratio | derived |
| $m_{\theta,n}$ | 閾値余白 | threshold margin | derived |

"Penetration term" and "contraction term" are terms of `FORMULA.md` §4.7. The action penetration term is the increment $\Delta q_n$ of the reversible component produced by the action $a_n$, divided by $\tau_n$; it is not the action $a_n$ itself. The name "reversible penetration" was recorded in the dictionary (Reversible Deviation, confusion notes, 2026-09-28) as a rejected earlier name and is therefore not used. "Reversible component" follows `FORMULA.md` §0.5.3 (the dictionary entry is Reversible Deviation).

## 10. Unverified Items

- Application to data from a real domain. The only check in this paper is the verification of identities.
- The general sign properties of $\Delta\tau^{\mathrm{comp}}_n$ when $\mathrm{Comp}_\tau$ is other than a sum (parallel, series, etc.).
- Collisions of the tentative names and symbols with the dictionaries were checked by searching terms and symbols and by `scripts/check_dictionary.py`. Completeness against semantic collisions is not guaranteed.
- Disclosure of $R_n$ when unobservable and the conditions for continuing evaluation (the Primary Formula $R_n=\delta_n/\tau_n$ is undefined when $\delta_n,\tau_n$ cannot be obtained).

[^1]: Under `note/06_対話セッション記録/`: "現実の開放系を記述する「泥臭い応用式」の骨格…", "NRA-IDE_開いた動的構造式", and "…対照精査および正典v2.5整合報告" (all recorded 2026-11-16).
