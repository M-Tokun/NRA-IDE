# NRA-IDE 定義式（基礎式）
<!-- FORMULA.md | 2026-03-08 00:52 JST -->
Ver 1.00
---

## 定義式 1　基本判定式

$$R = \frac{\delta}{\tau}$$

| 記号 | 意味 |
|------|------|
| δ（デルタ） | 制約からのズレ |
| τ（タウ） | 設計時に決めた許容幅 |
| R | その比率 |

R が 1.0 を超えた瞬間に構造限界。出力を止める。

---

## 定義式 2　二重ゆらぎ式（動的τ）

$$\text{EMA\_upper}(n) = \alpha_u \cdot \delta_u + (1 - \alpha_u) \cdot \text{EMA\_upper}(n-1)$$

$$\text{EMA\_lower}(n) = \alpha_l \cdot \delta_l + (1 - \alpha_l) \cdot \text{EMA\_lower}(n-1)$$

$$\tau_{\text{upper}} = \tau \cdot f(\text{EMA\_upper}) \quad \text{（拡大方向）}$$

$$\tau_{\text{lower}} = \tau \cdot g(\text{EMA\_lower}) \quad \text{（縮小方向）}$$

$$R = \max\!\left(\frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},\ \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}}\right)$$

上限側のτは拡大し、下限側のτは縮小する。この非対称性が構造の核心。

---

*これ以外の前提をこの式は持たない。*

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
