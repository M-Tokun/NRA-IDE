# NRA‑IDE 定義式（基礎式）
<!-- FORMULA.md | 2026-03-08 00:52 JST -->
Ver 1.00

---

## 定義式 1　基本判定式

$$
\displaystyle
R = \frac{\delta}{\tau}
$$

| 記号 | 意味 |
|------|------|
| δ（デルタ） | 制約からのズレ（偏差） |
| τ（タウ） | 設計時に決めた許容幅（厚み） |
| R | 構造比率 |

**R が 1.0 を超えた瞬間に構造限界。出力を停止する。**

---

## 定義式 2　二重ゆらぎ式（動的 τ）

### 上側ゆらぎ（拡大方向）

$$
\displaystyle
\mathrm{EMA}_{\text{upper}}(n)
= \alpha_u \cdot \delta_u
+ (1 - \alpha_u) \cdot \mathrm{EMA}_{\text{upper}}(n-1)
$$

### 下側ゆらぎ（縮小方向）

$$
\displaystyle
\mathrm{EMA}_{\text{lower}}(n)
= \alpha_l \cdot \delta_l
+ (1 - \alpha_l) \cdot \mathrm{EMA}_{\text{lower}}(n-1)
$$

### 動的 τ（非対称構造）

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

### 最終判定式（非対称二重比率）

$$
\displaystyle
R = \max\!\left(
  \frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},
  \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}}
\right)
$$

**上限側の τ は拡大し、下限側の τ は縮小する。  
この非対称性こそが NRA‑IDE の構造的核心である。**

---

*これ以外の前提をこの式は持たない。  
NRA‑IDE の構造比率は、常にこの閉じた世界の中で完結する。*

**Copyright (c) 2026  
M‑Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
