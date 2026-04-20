# IDE Formula and Classical Formula — Resolution via Hybrid Computation
NRA-IDE Definition (Applied Formula)

```
Quantum computation layer : IDE comprehensive operation (nonlinear steps, no error explosion, but broad)
                             ↓ fluctuation detection
Classical computation layer: local precision correction (small region only, before error explosion; auxiliary role)
                             ↓ quadratic residual gate controls coupling strength automatically
IDE base point             : always maintained — the foundation is never relinquished
```

This hierarchy holds for three reasons.
Quantum IDE can process state spaces in parallel and comprehensively, but its resolution drops at individual phase-transition points due to its broad coverage.
Classical computation offers high resolution but cannot handle the whole system due to error explosion.
The quadratic residual gate is a mechanism by which the system itself decides "where to invoke classical computation."

---

## Formalised as a base equation

$$\frac{d^2x}{dt^2} + \gamma\dot{x} = \underbrace{F_{IDE}(x)}_{\text{quantum layer · foundation}} + \underbrace{G(r) \cdot \Phi(x)}_{\text{classical layer · auxiliary}}$$

$$G(r) = r \cdot \frac{|r|}{k + |r|}, \quad r = x_{exact} - x$$

$G(r)$ is the quadratic residual gate itself.
When $r$ is small, $G \approx 0$ and the classical layer falls silent; when $r$ is large, a saturating response provides precision correction.
The IDE term $F_{IDE}$ operates across the entire domain at all times and never relinquishes the foundation.

---

## The tuning point — "it depends on the use case"

In this equation, adaptation to different use cases reduces to adjusting a single parameter: $k$ (the knee value).

| Use case | $k$ setting | Effect |
|---|---|---|
| Coarse global overview | Large | Classical correction barely activates |
| Precise tracking of phase transitions | Small | Classical intervenes from early stages |
| Real-time control | Intermediate | Balanced operation |

The IDE foundation is always maintained while $k$ alone continuously varies the degree of exactness.
This is a continuous lever, not a binary switch.

---

## Fundamental significance

When IDE rides on quantum computing, the weakness of quantum IDE — its broad coverage — is compensated by the classical auxiliary, and the weakness of classical computation — error explosion — is avoided because IDE maintains the global picture.
Each covers the other's weakness with its own strength.
This can be said to be a natural re-emergence, at the level of computational architecture, of the "mutual complementarity" principle that NRA-IDE's design philosophy has held from the beginning.
The key is to select the right layer according to the use case (and units involved).
