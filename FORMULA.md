# NRA‑IDE 定義式（基礎式） / NRA‑IDE Fundamental Equations

Ver 1.00  

<!-- FORMULA.md | 2026-03-11 式をgit文に合わせる-->

---

# ■ 定義式 1　基本判定式  

# ■ Definition 1 — Basic Structural Ratio

$$\displaystyle R = \frac{\delta}{\tau}$$

### 日本語（Japanese）

- **δ（デルタ）**：制約からのズレ（偏差）  

- **τ（タウ）**：設計時に決めた許容幅（厚み）  

- **R**：構造比率  

- **R が 1.0 に到達した場合、構造余裕は失われる。通常の生成は行わず、事前に定めた最小限の構造通知のみを返した後、自律処理を停止する。**

### English

- **δ (delta)**: deviation from the constraint  

- **τ (tau)**: designed tolerance boundary  

- **R**: structural ratio  

- **When R reaches 1.0, structural slack is exhausted. The system suppresses normal generation, returns only a predefined minimal structural notice, and then halts autonomous processing.**

---

# ■ 定義式 2　二重ゆらぎ式（動的 τ）  

# ■ Definition 2 — Dual-Fluctuation Formula (Dynamic τ)

---

## ● 上側ゆらぎ（拡大方向）  

## ● Upper Fluctuation (Expansion Side)

$$\displaystyle \mathrm{EMA}_{\text{upper}}(n) = \alpha_u \cdot \delta_u + (1 - \alpha_u) \cdot \mathrm{EMA}_{\text{upper}}(n-1)$$

### 日本語  

上側 EMA は **拡大方向の偏差** を平滑化する。

### English  

The upper EMA smooths **deviations in the expansion direction**.

---

## ● 下側ゆらぎ（縮小方向）  

## ● Lower Fluctuation (Contraction Side)

$$\displaystyle \mathrm{EMA}_{\text{lower}}(n) = \alpha_l \cdot \delta_l + (1 - \alpha_l) \cdot \mathrm{EMA}_{\text{lower}}(n-1)$$

### 日本語  

下側 EMA は **縮小方向の偏差** を平滑化する。

### English  

The lower EMA smooths **deviations in the contraction direction**.

---

## ● 動的 τ（非対称構造）  

## ● Dynamic τ (Asymmetric Structure)

$$\displaystyle \tau_{\text{upper}} = \tau \cdot f\!\bigl(\mathrm{EMA}_{\text{upper}}\bigr) \quad \text{（拡大方向）}$$

$$\displaystyle \tau_{\text{lower}} = \tau \cdot g\!\bigl(\mathrm{EMA}_{\text{lower}}\bigr) \quad \text{（縮小方向）}$$

### 日本語  

- 上限側の τ は **拡大** し、  

- 下限側の τ は **縮小** する。  

この非対称性こそが NRA‑IDE の構造的核心である。

### English  

- The upper τ **expands**,  

- The lower τ **contracts**.  

This asymmetry is the structural core of NRA‑IDE.

---

## ● 最終判定式（非対称二重比率）  

## ● Final Decision Formula (Asymmetric Dual Ratio)

$$\displaystyle R = \max\!\left( \frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},\ \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}} \right)$$

### 日本語

この判定式は、Effect-Sideの意味評価、スコア、過去の生成出力を入力に使用しない。

Cause-Side由来の δ と、設計時に固定された τ の決定規則に基づいて、構造比率 R を算出する。

### English

This decision formula does not use Effect-Side semantic evaluations, scores, or prior generated outputs as inputs.

It derives the structural ratio R from Cause-Side δ and a τ-determination rule fixed at design time.

---

## 判定後の出力規則

R が 1.0 に到達した場合、構造余裕は失われる。通常の生成は行わず、事前に定めた最小限の構造通知のみを返した後、自律処理を停止する。

## Output Rule After Determination

When R reaches 1.0, structural slack is exhausted. The system suppresses normal generation, returns only a predefined minimal structural notice, and then halts autonomous processing.

---

**Copyright (c) 2026  

M‑Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
