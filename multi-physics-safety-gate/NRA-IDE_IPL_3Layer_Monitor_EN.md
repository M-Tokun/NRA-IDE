

# 📘 **NRA-IDE_IPL_3Layer_Monitor.md — English Translation 



## NRA-IDE IPL 3-Layer Monitor — Design Philosophy and Structural Rationale  

**FILE:** NRA-IDE_IPL_3Layer_Monitor.md / 2026-03-06 21:44



**Version:** 2.0.0  

**Target Domain:** Nuclear power plants / Multi-Physics Systems  

**Positioning:** This document explains the design philosophy and structural rationale of the layered architecture.  

Formal definitions of the base equations and sensor specifications are provided in `Multi-Physics_Safety_Gate_Architecture.md`.



---



## 1. Why the Architecture Was Revised from 3 Dimensions to 5 Layers



The initial version (v1.0) consisted solely of a 3‑dimensional orthogonal synthesis of heat, pressure, and stress.



A detailed examination of the physical domains in a multi-physics coupled system reveals a total of five domains. The key question is whether all five should be included in the base equation  

\(\sqrt{\sum R^2}\).  

The answer is no, due to structural causal relationships.



| # | Physical Domain | Placement in Base Equation | Reason |

|---|---|---|---|

| ① | Thermodynamics | ✅ Included | Independent physical dimension |

| ② | Fluid Dynamics (Pressure) | ✅ Included | Independent physical dimension |

| ③ | Solid/Structural Mechanics (Stress) | ✅ Included | Independent physical dimension |

| ④ | Electromagnetics | ❌ Pre-layer: Data Integrity Assurance | Concerns the reliability of measurement itself |

| ⑤ | Nuclear Reaction Dynamics | ❌ Pre-layer: Gate Permission | Upstream causal factor of ① |



---



## 2. Roles and Independence of the Three Layers



Each layer issues a Fail-Closed signal independently the moment its own \(R\) exceeds the threshold.  

This structure is called **IPL (Independent Protection Layers)**.



```

Layer A (Electromagnetics) → Layer B (Nuclear Reaction) → Layer C (Heat / Pressure / Stress)

Each layer is fully independent and does not wait for the others.

```



If the system were designed to issue alarms only based on a combined judgment of all layers, a single software bug or failure in any one layer could cause it to always return “normal.”  

Even if the other layers detect a limit exceedance, the alarm would never sound.  

The IPL architecture structurally eliminates this common-cause failure (CCF).



---



## 3. Layer A (Electromagnetics): Why It Is Placed Outside the Base Equation



### Plain Explanation



In this context, electromagnetics refers to **verifying whether the temperature and pressure readings from sensors can be trusted**.



Inside a reactor, strong electromagnetic noise is present. Electromagnetic drive systems for control rods, high‑power cables, and instrumentation lines coexist, and EMI (electromagnetic interference) contaminates the weak sensor signals.  

This can cause false high or false low readings.



The NRA‑IDE base equation \(R = \delta / \tau\) assumes that \(\delta\) (the measured value) is accurate.  

If this assumption collapses, the entire equation becomes meaningless.



### Structural Rationale



Heat, pressure, and stress represent **what is happening**.  

The electromagnetic layer represents **whether the observation itself is trustworthy**.



Treating these as the same dimension ignores causal order.  

Therefore, Layer A is placed outside the base equation as a prerequisite assurance layer.



Definitions of \(R_{em}\) are provided in `Multi-Physics_Safety_Gate_Architecture.md` §2.



---



## 4. Layer B (Nuclear Reaction Dynamics): Why It Is Placed Outside the Base Equation



### Plain Explanation



In a reactor, nuclear fuel undergoes fission when struck by neutrons, generating heat.  

Controlling the speed of this chain reaction is the essence of reactor operation.



If neutron flux begins to increase beyond acceptable limits, heat generation accelerates, causing temperature, pressure, and stress to rise together.  

Thus, **abnormal nuclear reactions are the upstream cause of all three quantities**.



This is not something to be placed alongside the base equation; it determines whether the phenomena handled by the base equation will occur in the first place.



### Structural Rationale



Heat, pressure, and stress are independent physical dimensions and can be orthogonally synthesized.  

However, an increase in nuclear reaction rate is the direct cause of heat generation.  

Placing \(R_{nuke}\) in the same equation as \(R_{heat}\) mixes cause and effect, which is structurally incorrect.



Therefore, Layer B is an independent gate that precedes the base equation.  

If \(R_{nuke} \ge 1.0\), SCRAM is issued immediately without waiting for Layer C.



Definitions of \(R_{nuke}\) are provided in `Multi-Physics_Safety_Gate_Architecture.md` §3.



---



## 5. Layer C (3-Dimensional Orthogonal Synthesis): Why These Three Can Be Combined



Heat, pressure, and stress are independent in the following sense:



- High temperature with low pressure can occur (e.g., coolant loss after depressurization).  

- High pressure with low stress can occur (e.g., components with large design margins).  

- Excessive stress with normal temperature and pressure can occur (e.g., localized fatigue).



Since each can reach its limit independently, 3‑dimensional orthogonal synthesis accurately represents their independence.



Formal definitions are provided in `Multi-Physics_Safety_Gate_Architecture.md` §4–5.



---



## 6. File List



| File | Content | Nature |

|---|---|---|

| `Multi-Physics_Safety_Gate_Architecture.md` | Base equations, sensor definitions, topology | Source of Truth |

| `NRA-IDE_IPL_3Layer_Monitor.md` | Rationale for 5-layer structure | Design philosophy |

| `NRA-IDE_08_Multi-Physics-Safety-Gate.html` | Layer C demonstration | Interactive demo |

| `NRA-IDE_IPL_3Layer_Monitor.html` | 3-layer independent alarm visualization | Interactive demo |



---



*This document explains the design philosophy and rationale. Base equations are not redefined here.*  

*For AI-based revalidation, please refer to this file together with `Multi-Physics_Safety_Gate_Architecture.md`.*



---

