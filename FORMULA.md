# NRA-IDE 定義式（基礎式）
<!-- FORMULA.md | 2026-03-08 00:52 JST -->
Ver 1.00
---

## 定義式 1　基本判定式

$$
\displaystyle R = \frac{\delta}{\tau}
$$

| 記号 | 意味 |
|------|------|
| δ（デルタ） | 制約からのズレ |
| τ（タウ） | 設計時に決めた許容幅 |
| R | その比率 |

R が 1.0 を超えた瞬間に構造限界。出力を止める。

---

## 定義式 2　二重ゆらぎ式（動的τ）

$$
\displaystyle
\mathrm{EMA}_{\text{upper}}(n)
= \alpha_u \cdot \delta_u
+ (1 - \alpha_u) \cdot \mathrm{EMA}_{\text{upper}}(n-1)
$$

$$
\displaystyle
\mathrm{EMA}_{\text{lower}}(n)
= \alpha_l \cdot \delta_l
+ (1 - \alpha_l) \cdot \mathrm{EMA}_{\text{lower}}(n-1)
$$

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

$$
\displaystyle
R = \max\!\left(
  \frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},
  \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}}
\right)
$$


上限側のτは拡大し、下限側のτは縮小する。この非対称性が構造の核心。

---

*これ以外の前提をこの式は持たない。*

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
