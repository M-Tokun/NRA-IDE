# NRA‑IDE 定義式（基礎式） / NRA‑IDE Fundamental Equations
<!-- FORMULA.md | 2026-03-08 00:52 JST -->
Ver 1.00

---

# ■ 定義式 1　基本判定式  
# ■ Definition 1 — Basic Structural Ratio

$$
\displaystyle
R = \frac{\delta}{\tau}
$$

| 記号 | 意味 |
|------|------|
| δ（デルタ） | 制約からのズレ（偏差） |
| τ（タウ） | 設計時に決めた許容幅（厚み） |
| R | 構造比率 |

| Symbol | Meaning |
|--------|---------|
| δ (delta) | Deviation from constraint |
| τ (tau) | Designed tolerance boundary |
| R | Structural Ratio |

**R が 1.0 を超えた瞬間に構造限界。出力を停止する。**  
**When R exceeds 1.0, the structure reaches its limit and output must stop.**

---

# ■ 定義式 2　二重ゆらぎ式（動的 τ）  
# ■ Definition 2 — Dual-Fluctuation Formula (Dynamic τ)

---

## ● 上側ゆらぎ（拡大方向）  
## ● Upper Fluctuation (Expansion Side)

$$
\displaystyle
\mathrm{EMA}_{\text{upper}}(n)
= \alpha_u \cdot \delta_u
+ (1 - \alpha_u) \cdot \mathrm{EMA}_{\text{upper}}(n-1)
$$

**上側 EMA は拡大方向の偏差を平滑化する。**  
**The upper EMA smooths deviations in the expansion direction.**

---

## ● 下側ゆらぎ（縮小方向）  
## ● Lower Fluctuation (Contraction Side)

$$
\displaystyle
\mathrm{EMA}_{\text{lower}}(n)
= \alpha_l \cdot \delta_l
+ (1 - \alpha_l) \cdot \mathrm{EMA}_{\text{lower}}(n-1)
$$

**下側 EMA は縮小方向の偏差を平滑化する。**  
**The lower EMA smooths deviations in the contraction direction.**

---

## ● 動的 τ（非対称構造）  
## ● Dynamic τ (Asymmetric Structure)

$$
\displaystyle
\tau_{\text{upper}}
= \tau \cdot f\!\bigl(\mathrm{EMA}_{\text{upper}}\bigr)
\quad \text{（拡大方向）}
$$

$$
\displaystyle
\tau_{\text{lower}}
= \tau \cdot g\!\bigl(\mathrm{EMA}_{\text{lower}}\bigr)
\quad \text{（縮小方向）}
$$

**上限側の τ は拡大し、下限側の τ は縮小する。  
この非対称性こそが NRA‑IDE の構造的核心である。**

**The upper τ expands while the lower τ contracts.  
This asymmetry is the structural core of NRA‑IDE.**

---

## ● 最終判定式（非対称二重比率）  
## ● Final Decision Formula (Asymmetric Dual Ratio)

$$
\displaystyle
R = \max\!\left(
  \frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},
  \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}}
\right)
$$

**この式は閉じた世界で完結し、他の前提を必要としない。**  
**This formula is self‑contained and requires no external assumptions.**

---

**Copyright (c) 2026  
M‑Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
