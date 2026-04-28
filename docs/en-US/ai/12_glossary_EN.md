# 12 Glossary



<!-- FILE: 12_glossary_EN.md -->



---



## Boundary



The structural limit that defines whether a system remains within a viable operational state.



When this boundary is exceeded, the system transitions to Fail-Closed behavior.



---



## Causal Diode



A structural principle that allows causal flow in only one direction.



It prevents discarded values, logs, or previous outputs from re-entering the computational path.



---



## Constraint Thickness (τ)



The structural thickness of a constraint boundary.



It represents the allowable range of variation that a system can tolerate without structural failure.



---



## Deviation (δ)



The measured deviation of a system state from its constraint boundary.



Deviation indicates how far the system has moved toward the structural limit.



---



## Domain Tuning



The process of selecting appropriate observables and parameters for a specific operational domain.



Different systems require different measurements to evaluate structural conditions.



---



## Fail-Closed



A structural safety mechanism in which the system stops producing output once the structural boundary is exceeded.



This prevents the system from continuing operation beyond its safe limits.



---



## Observable



A measurable quantity used to evaluate the structural state of a system.



Observables vary depending on the domain in which the system is applied.



---



## Residual Values



Small numerical remnants produced during computation, often originating from floating-point operations or measurement noise.



In NRA-IDE these values are discarded and recorded in the Discard Log rather than reused.



---



## Discard Log



A write-only record of residual values and structural events that were removed from the computation path.



Discard Logs preserve structural evidence without influencing future calculations.



---



## SILENCE



A structural state in which the system stops producing output after exceeding its operational boundary while maintaining causal continuity.



Responsibility is transferred to the next agent, typically a human operator.



---



## HALT



A state in which the system has lost operational continuity and cannot proceed further.



HALT represents a structural breakdown rather than a controlled transition.



---



## Structural Ratio (R)



The ratio used to evaluate structural deviation.



```id="k48j3d"

R = δ / τ

```



When



```id="i9q6y4"

R ≥ 1.0

```



the structural boundary has been exceeded.



---



## NRA (Nomological Ring Axioms)



A set of structural principles describing how dynamic systems maintain viability within constraint boundaries.



---



## IDE (Intensional Dynamics Engine)



An implementation framework based on NRA principles.



The IDE evaluates structural states and enforces boundary conditions within dynamic systems.

