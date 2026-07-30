# NRA-IDE IPL 3-Layer Monitor — Design Philosophy and Structural Rationale

<!-- FILE: NRA-IDE_IPL_3Layer_Monitor_EN.md / 2026-03-06 21:44 -->

**Version:** 2.0.0

**Target Domain:** Nuclear power plants and similar / Multi-Physics Systems

**Positioning:** This file is an **explanatory document** that describes the design philosophy and the rationale of the layer structure.

For the formal definitions of the base equations and sensor definitions, refer to `Multi-Physics_Safety_Gate_Architecture_EN.md`.

The equations in this document and in the Architecture document are structural formulas. The position of each limit is declared per domain; exact numerical agreement is not required. See `Multi-Physics_Safety_Gate_Architecture_EN.md` § 0.

---

## 1. Why the Structure Was Revised from 3 Dimensions to 3 Layers and 5 Domains

The initial version (v1.0) consisted only of the three-dimensional orthogonal synthesis of heat, pressure, and stress.

A close examination of the mechanical domains of a multi-physics coupled system shows that five exist in total. The question is whether all five may be placed in the base equation $\sqrt{\sum R^2}$ , and the answer is no. The reason lies in structural causal relations.

| # | Mechanical Domain | Placement in the Base Equation | Reason |
|---|---|---|---|
| ① | Thermodynamics | ✅ Base equation (orthogonal synthesis) | A physical dimension independent of the others |
| ② | Fluid dynamics (pressure) | ✅ Base equation (orthogonal synthesis) | A physical dimension independent of the others |
| ③ | Solid and structural mechanics (stress) | ✅ Base equation (orthogonal synthesis) | A physical dimension independent of the others |
| ④ | Electromagnetics | ❌ Separate layer: judgment of observation integrity | A question of the reliability of the measured value itself |
| ⑤ | Nuclear reaction dynamics (neutrons) | ❌ Separate layer: independent SCRAM judgment | Upstream causality on the cause side of ① |

---

## 2. The Roles and Independence of the Three Layers

Each layer does not reference the judgment result of another layer; the moment its own $R$ exceeds the threshold, it independently issues Fail-Closed. This is called **IPL (Independent Protection Layers)**.

```

Layer A (Electromagnetics)　　Layer B (Nuclear reaction)　　Layer C (Heat / Pressure / Stress)

The layers are fully independent. None waits for the judgment of another. Any one of them can issue Fail-Closed on its own.

```

It becomes clear if one considers a design that raises an alarm only on the combined judgment of all layers. If any single layer keeps returning "normal" because of a software bug or a fault, the siren never sounds even though the remaining layers have detected the limit. The IPL design structurally eliminates this common cause failure (CCF).

---

## 3. Layer A (Electromagnetics): Why It Is Placed Outside the Base Equation

### Plain Explanation

Electromagnetics here means "**checking whether the readings of the thermometers and pressure gauges can be trusted**".

The inside of a reactor is a strong electromagnetic noise environment. Electromagnetic drive units for control rods, high-power cables, and instrumentation signal lines coexist, and **EMI (electromagnetic interference)** contaminates the weak electrical signals picked up by the sensors. A temperature that is actually normal may read as abnormal, or the reverse may occur.

The NRA-IDE base equation $R = \delta / \tau$ assumes that $\delta$ (the value returned by the sensor) is accurate. If that assumption collapses, the whole equation becomes meaningless.

### Structural Rationale

Heat, pressure, and stress are physical quantities that express "**what is happening**".

The electromagnetic layer is a meta-level judgment that expresses "**whether the observed value is correct**".

Treating these as the same dimension is a conflation that ignores causal order. Layer A is therefore placed outside the base equation as an independent layer.

Layer A neither permits nor blocks another layer. When the reliability of a measured value is lost, that value is treated as invalid; other observation, logging, and communication are not stopped.

For the definition of $R_{em}$ , see `Multi-Physics_Safety_Gate_Architecture_EN.md` § 2.

---

## 4. Layer B (Nuclear Reaction Dynamics): Why It Is Placed Outside the Base Equation

### Plain Explanation

In a reactor, the nuclei of nuclear fuel such as uranium receive neutrons, split, and generate heat. Controlling the speed of this "chain reaction" is the essence of reactor operation.

When the number of neutrons begins to rise sharply beyond the permissible range, heat generation accelerates and temperature, pressure, and stress all rise together. In other words, **an abnormality in the nuclear reaction is the root cause of all of heat, pressure, and stress**.

This is not something to be placed on the same level as the base equation of Layer C; it is "the upstream condition that determines whether the phenomena handled by the base equation occur at all".

### Structural Rationale

Heat, pressure, and stress are mutually independent physical dimensions, so orthogonal synthesis holds. An increase in the nuclear reaction, however, is the direct cause of heat generation. Placing $R_{nuke}$ in the same equation as $R_{heat}$ would put cause and effect on the same plane, which is structurally incorrect.

Layer B is therefore placed before the base equation as an independent layer. Layer B issues SCRAM on its own, without waiting for the computation of Layer C. The case of $R_{nuke} \geq 1.0$ is this situation.

For the definition of $R_{nuke}$ , see `Multi-Physics_Safety_Gate_Architecture_EN.md` § 3.

---

## 5. Layer C (Three-Dimensional Orthogonal Synthesis): Why These Three Can Be Orthogonally Synthesized

Heat, pressure, and stress are mutually independent in the following sense.

A state of high temperature with low pressure can occur (such as loss of core cooling after a gas leak). A state of high pressure with small structural stress can occur (a location with a large design margin). A state of excessive stress with normal heat and pressure can occur (localized material fatigue).

Because it can actually happen that one of them reaches its limit while the others remain in the safe region, the three-dimensional orthogonal synthesis expresses this independence geometrically and accurately.

For the base equations and sensor definitions, see `Multi-Physics_Safety_Gate_Architecture_EN.md` § 4 and § 5.

---

## 6. List of Corresponding Files

| File | Contents | Nature |
|---|---|---|
| `Multi-Physics_Safety_Gate_Architecture_EN.md` | Base equations, sensor definitions, topology | Implementation specification (Source of Truth) |
| `NRA-IDE_IPL_3Layer_Monitor_EN.md` (this document) | Rationale for the 3-layer, 5-domain structure; plain explanation | Design philosophy and commentary |
| `NRA-IDE_08_Multi-Physics-Safety-Gate_EN.html` | Operating POC of Layer C | Interactive demo |
| `NRA-IDE_IPL_3Layer_Monitor_EN.html` | Visualization of independent alarms in three layers | Interactive demo |

---

*This file is an explanatory document on design philosophy and rationale. It does not duplicate the definitions of the base equations.*

*When another AI re-verifies this material, refer to it together with `Multi-Physics_Safety_Gate_Architecture_EN.md`.*
