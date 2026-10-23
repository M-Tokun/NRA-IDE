# Lindblad (GKSL) equation: reading the formula and its conditions

**Document role:** An explanation of an external technical term; it neither defines nor changes the NRA-IDE canon  
**Dictionary entry:** [Lindblad (GKSL) equation](../Glossary_EN.md#^qh-lindblad-equation)  
**Paired Japanese version:** [Lindblad_GKSL_JP.md](./Lindblad_GKSL_JP.md)  
**Updated:** 2026-10-24  
**Status:** [Draft] [concepts unreconciled] [full text not yet checked]

**Related glossary entries:** [Open quantum system](../Glossary_EN.md#^qh-open-quantum-system), [Hamiltonian](../Glossary_EN.md#^qh-hamiltonian), [Pure state](../Glossary_EN.md#^qh-pure-state), [Mixed state](../Glossary_EN.md#^qh-mixed-state), [Markov approximation](../Glossary_EN.md#^qh-markov-approximation), [Born approximation](../Glossary_EN.md#^qh-born-approximation), [Secular approximation](../Glossary_EN.md#^qh-secular-approximation), [Complete positivity](../Glossary_EN.md#^qh-complete-positivity), [Completely positive trace-preserving map (CPTP)](../Glossary_EN.md#^qh-cptp-map), [Semigroup (quantum dynamical semigroup)](../Glossary_EN.md#^qh-dynamical-semigroup)

## 1. The equation and its overall meaning

This is called the Lindblad equation, or the GKSL equation (Gorini–Kossakowski–Sudarshan–Lindblad equation). It is a basic form for Markovian evolution of an open quantum system interacting with its environment. It is not an unconditional description of every open quantum system.

The discussion primarily concerns finite-dimensional systems, in units with $\hbar=1$. H is a Hermitian Hamiltonian and may include effective terms such as environment-induced energy-level shifts. With time measured in seconds, H is read in angular-frequency units, meaning energy divided by $\hbar$.

$$
\dot{\rho}
=
-i[H,\rho]
+
\sum_k\left(
L_k\rho L_k^\dagger
-\frac{1}{2}\{L_k^\dagger L_k,\rho\}
\right).
$$

| Symbol | Meaning |
|---|---|
| $\rho$ | The system's [density matrix](../Glossary_EN.md#^qh-density-matrix), representing its quantum state |
| $\dot{\rho}$ | The time derivative of the density matrix |
| H | The Hamiltonian, determining the system's energy and reversible motion |
| $L_k$ | A Lindblad, jump, or collapse operator, specifying the action and strength of an environmental process |
| k | An index distinguishing processes |
| $\dagger$ | The adjoint: complex conjugation and transposition |
| I | The identity operator |
| $\operatorname{Tr}$ | The trace: the sum of a matrix's diagonal entries |

The time derivative, commutator, and anticommutator are defined by:

$$
\dot{\rho}=\frac{\mathrm{d}\rho}{\mathrm{d}t},
\qquad [A,B]=AB-BA,
\qquad \{A,B\}=AB+BA.
$$

The first term describes Hamiltonian, unitary evolution. The second describes non-unitary environmental effects, such as energy relaxation, pure dephasing, and photon loss. Pure dephasing reduces [quantum coherence](../Glossary_EN.md#^qh-quantum-coherence) without exchanging energy.

## 2. The first term: the closed-system von Neumann equation

Without environmental terms, the equation becomes the von Neumann equation for a density matrix.

$$
\dot{\rho}=-i[H,\rho].
$$

This evolution is unitary. It does not imply that relative phases always remain fixed, or that coherence in a chosen basis stays unchanged. The Hamiltonian can change [relative phases](../Glossary_EN.md#^qh-quantum-phase).

The system's energy [expectation value](../Glossary_EN.md#^qh-expectation-value) is conserved when the H used here is time-independent. Under time-dependent external driving, energy can change even during unitary evolution. In these units:

$$
\frac{\mathrm{d}}{\mathrm{d}t}\operatorname{Tr}(H(t)\rho(t))
=
\operatorname{Tr}(\dot{H}(t)\rho(t))
$$

Distinguish a closed-system description from a driven system receiving external work.

## 3. The second term: the dissipator

The entire second term is called the dissipator.

$$
\mathcal{D}[\rho]
=
\sum_k\left(
L_k\rho L_k^\dagger
-\frac{1}{2}\{L_k^\dagger L_k,\rho\}
\right).
$$

Despite this name, not every term necessarily lowers the energy. Suitable operators can also describe pure dephasing or thermal excitation.

The coupling operator and its coefficient can be separated as follows:

$$
L_k=\sqrt{\gamma_k}\,A_k,
\qquad \gamma_k\geq0.
$$

For dimensionless $A_k$, $\gamma_k$ has units of inverse seconds and $L_k$ has units of inverse square-root seconds. In the equation above, the rate coefficient is already included in $L_k$; do not multiply by the same coefficient again outside the dissipator.

The coefficient's name $\gamma_k$ alone does not determine an observable's decay rate. Specify the operator normalization and the quantity whose decay is meant. Section 6 gives a dephasing example.

## 4. Reading the jump and no-jump terms

One quantum-jump representation describes the probabilities of processes over short times, starting from a normalized state. The jump term itself is not a normalized post-jump state:

$$
L_k\rho L_k^\dagger.
$$

Its trace corresponds to a jump rate. The infinitesimal probability and normalized state conditioned on that jump are:

$$
p_k(\mathrm{d}t)
=
\mathrm{d}t\,
\operatorname{Tr}(L_k\rho L_k^\dagger)
+O((\mathrm{d}t)^2),
\qquad
\rho_k^{\mathrm{jump}}
=
\frac{L_k\rho L_k^\dagger}
{\operatorname{Tr}(L_k\rho L_k^\dagger)}
$$

If the denominator is zero, that process has zero rate; do not construct the conditional state by division.

The unnormalized state on a no-jump path is acted on by:

$$
K_0
=
I-\left(iH+\frac{1}{2}\sum_k L_k^\dagger L_k\right)\mathrm{d}t
+O((\mathrm{d}t)^2).
$$

That state is represented by the following matrix, whose trace corresponds to the no-jump probability:

$$
K_0\rho K_0^\dagger.
$$

The no-jump term does not merely restore the norm to 1; it changes the conditional state itself. The anticommutator alone does not preserve trace. Probability is conserved by the jump and no-jump contributions together. This is one representation associated with environmental monitoring, not a claim that individual jumps are directly observed in every experiment. See also [QuTiP's quantum-jump explanation](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-monte.html).

## 5. Probability conservation and CPTP

In finite dimensions, cyclicity of the trace gives, for each process:

$$
\begin{aligned}
\operatorname{Tr}\!\left(
L_k\rho L_k^\dagger
-\frac{1}{2}\{L_k^\dagger L_k,\rho\}
\right)
&=
\operatorname{Tr}(L_k^\dagger L_k\rho)
-\frac{1}{2}\operatorname{Tr}(L_k^\dagger L_k\rho)
-\frac{1}{2}\operatorname{Tr}(\rho L_k^\dagger L_k)
\\
&=0.
\end{aligned}
$$

The commutator also has zero trace. Therefore, if the initial trace is 1:

$$
\frac{\mathrm{d}}{\mathrm{d}t}\operatorname{Tr}\rho
=
\operatorname{Tr}\dot{\rho}
=0,
\qquad
\operatorname{Tr}\rho(t)=1
$$

is maintained. Trace 1 alone, however, does not ensure that probabilities cannot become negative.

The importance of the GKSL form is that, under appropriate conditions, it generates **completely positive, trace-preserving (CPTP)** evolution.

- Positivity: preserves positive semidefiniteness of the density matrix, preventing negative measurement probabilities.
- Complete positivity: the operation on the system preserves positivity of the joint state even when a correlated ancillary quantum system is included.
- Trace preservation: keeps the sum of measurement probabilities equal to 1.

A representative setting in which "most general" is precise is the **generator of a continuous, time-homogeneous CPTP quantum dynamical semigroup in finite dimensions**. Time-homogeneous means using the same map for the same elapsed time. For a generator $\mathcal{L}$ with constant H and $L_k$:

$$
\Phi_t=e^{t\mathcal{L}},
\qquad
\Phi_{t+s}=\Phi_t\circ\Phi_s,
\qquad t,s\geq0
$$

is the semigroup property. The abstracts of [Gorini–Kossakowski–Sudarshan](https://repository.ias.ac.in/51137/) and [Lindblad](https://link.springer.com/article/10.1007/BF01608499) identify the scope of this general form.

Time-dependent GKSL forms with time-dependent H and nonnegative rates also generate CPTP evolution under suitable regularity conditions, but generally do not form a time-homogeneous semigroup. Do not call the equation unconditionally most general for "all open systems" or for "every definition of Markovianity."

## 6. Common examples and rate conventions

### Spontaneous emission and energy relaxation

Let e denote the excited state and g the ground state, and define the lowering operator by:

$$
\sigma_-=\lvert g\rangle\langle e\rvert,
\qquad
L=\sqrt{\gamma}\,\sigma_-,
\qquad \gamma\geq0.
$$

Without external driving or upward excitation, the excited-state population decays as:

$$
\dot{\rho}_{ee}=-\gamma\rho_{ee},
\qquad
\rho_{ee}(t)=\rho_{ee}(0)e^{-\gamma t},
\qquad T_1=\frac{1}{\gamma}\quad(\gamma>0).
$$

This corresponds to the exponential-decay model in the [T₁ entry](../Glossary_EN.md#^qh-energy-relaxation-time-t1).

### Pure dephasing

Here $\gamma_\phi$ is defined as the **off-diagonal decay rate** without energy exchange. In this convention:

$$
L=\sqrt{\frac{\gamma_\phi}{2}}\,\sigma_z,
\qquad
\sigma_z=
\begin{pmatrix}
1&0\\
0&-1
\end{pmatrix},
\qquad \gamma_\phi\geq0
$$

gives the following dissipator contribution, excluding Hamiltonian evolution:

$$
\mathcal{D}[\rho]
=
\frac{\gamma_\phi}{2}(\sigma_z\rho\sigma_z-\rho),
\qquad
\dot{\rho}_{01}=-\gamma_\phi\rho_{01},
\qquad
\dot{\rho}_{00}=\dot{\rho}_{11}=0
$$

The original example without the factor of one half is mathematically valid as well, but its off-diagonal decay rate is twice the named coefficient:

$$
L=\sqrt{\gamma_\phi}\,\sigma_z
\quad\Longrightarrow\quad
\dot{\rho}_{01}=-2\gamma_\phi\rho_{01}.
$$

Thus, interpreting $\gamma_\phi$ as the pure-dephasing rate requires an explicit coefficient convention. When energy relaxation is also included, only in a model adding independent exponential-decay processes do we have:

$$
\frac{1}{T_2}
=
\frac{1}{2T_1}+\gamma_\phi
$$

Read this with the [T₂ entry](../Glossary_EN.md#^qh-coherence-time-t2). Do not extend it to every non-exponential noise process.

### Photon leakage from an optical cavity

A cavity is a resonator confining light, and a is the annihilation operator that removes one photon. Its leakage term is:

$$
L=\sqrt{\kappa}\,a,
\qquad \kappa\geq0.
$$

In a loss-only model without driving or thermal excitation, the mean photon-number decay rate differs from the field-amplitude decay rate. The following expressions show only the dissipator's contribution, excluding phase rotation due to the free Hamiltonian:

$$
\frac{\mathrm{d}}{\mathrm{d}t}\langle a^\dagger a\rangle
=-\kappa\langle a^\dagger a\rangle,
\qquad
\frac{\mathrm{d}}{\mathrm{d}t}\langle a\rangle
=-\frac{\kappa}{2}\langle a\rangle.
$$

For infinite-dimensional photon systems, separately check operator domains and any numerical photon-number cutoff. Do not unconditionally extend the finite-dimensional general-form discussion.

## 7. Derivation approximations and applicability

A typical microscopic derivation from a system–environment model uses assumptions such as:

- Weak coupling / Born approximation: treats the system's effect on the environment as small and approximates system–environment correlations.
- Markov approximation: assumes the environment's correlation time is short compared with the system's relaxation time, allowing environmental memory to be neglected.
- Secular approximation: removes rapidly oscillating terms associated with different transition frequencies through suitable time averaging. It is related to rotating-wave approximations but must not unconditionally be identified with a rotating-wave approximation made at the Hamiltonian level.

These are **conditions of a representative microscopic derivation**, not simply a list of necessary conditions for the mathematical GKSL structure. Phenomenological models and other derivations can also yield GKSL form. Device applications require checking H, the operators, rates, environmental memory, initial correlations, and time scales. See also [QuTiP's derivation and approximation discussion](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html).

An analytically CPTP equation does not imply positivity preservation by every time step and every numerical integration method. Verify the properties of the equation separately from those of its numerical solution.

## 8. Scope of the NRA-IDE connection

This equation models quantum-state evolution. It has a different role from NRA-IDE's boundary-approach ratio, update permission, and observation-testimony rules. Preservation of a density matrix's trace does not establish thermal safety, measurement sufficiency, SPSA convergence, or permission to apply an old result.

Distinguish adopting this equation as the April proposal's evolution kernel from validating the model for a target system. See [Observable expectation-value vector](../Glossary_EN.md#^qh-observable-expectation-vector), [Decoherence](../Glossary_EN.md#^qh-decoherence), and [Update permission](../Glossary_EN.md#^qh-update-authority).

## 9. Sources and verification scope

1. G. Lindblad, [On the generators of quantum dynamical semigroups](https://link.springer.com/article/10.1007/BF01608499), Communications in Mathematical Physics 48, 119–130 (1976), DOI 10.1007/BF01608499. Publisher bibliography and abstract checked 2026-10-24; this is distinct from reading the full original paper.
2. V. Gorini, A. Kossakowski, E. C. G. Sudarshan, [Completely positive dynamical semigroups of N-level systems](https://repository.ias.ac.in/51137/), Journal of Mathematical Physics 17, 821–825 (1976), DOI 10.1063/1.522979. Bibliography and abstract checked in the institutional repository on the same date; the full original paper was not obtained.
3. [QuTiP, "Lindblad Master Equation Solver"](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html): equation, collapse operators incorporating rate coefficients, and representative derivation approximations checked in the text on the same date.
4. [QuTiP, "Monte Carlo Solver"](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-monte.html): jump probabilities, normalized conditional states, and no-jump evolution checked in the text on the same date.

The trace cancellation in §5 and rate conventions in §6 are verified directly from the equations. Classical finite-dimensional calculations check the mathematics and its implementation; they are not device tests or validation of the coupled NRA-IDE system.
