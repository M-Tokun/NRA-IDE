# IDE Adaptive Gate Extension

# IDE 適応型ゲート拡張式

- “By further reinforcing the design principle of preserving transitions without distortion while retaining the tracking of property‑errors, the architecture becomes effective for specific applications such as high‑precision requirements and dynamic target‑tracking.”

- 「遷移を絶対に崩さず、[性質誤差]の追従を残す」という設計思想をさらに強化し、特定の用途（高精度要求や動的な目標追従など）で役立つ

<!-- FILE: IDE_AdaptiveGate_Extension_20260407_2241.md -->

<!-- 生成日時: 2026-04-07 22:41 JST -->

<!-- Author: M-Tokuni / NRA-IDE Project https://github.com/M-Tokun/NRA-IDE -->

---

## Positioning

## 位置づけ

This document belongs to `nra-core` as an extension definition.

It does **not replace** `normalized_quadratic_gate` in `nra_ide_foundation_fixed_JP.py`,

but defines a dynamic extension as an upper layer above it.

本文書は `nra-core` に属する拡張定義です。

`nra_ide_foundation_fixed_JP.py` の `normalized_quadratic_gate` を**差し替えるものではなく**、その上位層として動的拡張を定義します。

| Existing | Position of This Document |

|---|---|

| `normalized_quadratic_gate` (fixed k) | Core — immutable |

| Adaptive Gate Extension (dynamic k) | Upper extension of core |

| 既存 | 本文書の位置 |

|---|---|

| `normalized_quadratic_gate`（固定 k） | コア・不変 |

| 適応型ゲート拡張（動的 k） | コアの上位拡張 |

---

## Design Philosophy: "The Inside Fluctuates and Absorbs"

## 設計思想：「内側が揺らいで吸収する」

In the original `G(r)`, `k` was a fixed value — a structural filter but with a constant response characteristic.

The core of this extension is the design in which **`k` is coupled to the system's own state, so that the gate itself absorbs error not as an external correction but as an internal structural deformation**.

元の `G(r)` は構造フィルターとして機能しますが、`k` は固定値でした。

本拡張の核心は、**`k` を系の状態に連動させることで、ゲート自体が誤差を外側から修正するのではなく、内側の構造変形として吸収する**という設計です。

> "Not the center moving (external coordinate shift), but the inside fluctuating and absorbing (structural response of the ring itself)."

> 「中心が動く（外部座標の移動）」ではなく、「内側が揺らいで吸収する（律環の構造自体が応答する）」

This aligns with the NRA-IDE principle that the shape of the nomological ring itself responds to error — a property intrinsic to intensional dynamics.

これは NRA-IDE の内包性動力学が持つ性質、すなわち律環の形そのものが誤差に応答するという原則と整合します。

### Intuitive Analogy: A Cylindrical Jelly

### 直感的比喩：円柱状のゼリー

Think of the nomological ring as a **cylinder of jelly**.

律環を**円柱状のゼリー**として想像してください。

| Material | Behavior under force | Analogy |

|---|---|---|

| Steel cylinder | Reflects force rigidly — no deformation | Classical computation (rigid overwrite) |

| Water | Cannot hold its shape — collapses | Unconstrained system (divergence) |

| **Jelly cylinder** | **Deforms inside, disperses force, holds its shape** | **NRA-IDE adaptive gate** |

| 素材 | 力に対する挙動 | 対応 |

|---|---|---|

| 鋼鉄の円柱 | 力をそのまま跳ね返す・変形なし | 古典計算（剛体的上書き） |

| 水 | 形を保てない・崩壊 | 拘束のない系（発散） |

| **ゼリーの円柱** | **内側で変形して力を分散・形は保つ** | **NRA-IDE 適応型ゲート** |

When force is applied, the jelly does not break and does not bounce back — it deforms internally and absorbs.

The overall cylindrical form (the nomological ring) is preserved throughout.

This is exactly the behavior of dynamic $k_{\text{eff}}$: the gate widens or narrows on the inside in response to the state, without the outer structure ever collapsing.

押されるとゼリーは壊れず、跳ね返しもしない — 内側で変形して吸収します。

円柱という全体の形（律環）は終始保たれます。

これが動的 $k_{\text{eff}}$ の挙動そのものです。外側の構造を崩さないまま、ゲートが内側で状態に応じて広がったり狭まったりします。

---

## Reference: Existing Second-Order Residual Gate

## 基礎：既存の2次残差ゲート（参照）

$$G(r) = r \cdot \frac{|r|}{k + |r|}, \quad r = x_{\text{exact}} - x$$

Fixed $k$: response characteristic is constant regardless of system state.

The properties of silencing small fluctuations and saturating large deviations are preserved in this extension.

$k$ 固定：系の状態によらず一定の応答特性。

小ゆらぎ沈黙・大逸脱飽和応答の性質は本拡張でも維持されます。

---

## Extension Proposals

## 拡張案

---

### Proposal 1: Target-Tracking IDE (Relative Coordinate Extension)

### 案1：目標追従型 IDE（相対座標への拡張）

**Use case:** When the target value $x_{\text{exact}}$ changes dynamically.

**用途：** 目標値 $x_{\text{exact}}$ が動的に変化する場合。

$$F_{\text{IDE}}(x, x_{\text{exact}}) = -\alpha (x - x_{\text{exact}})$$

The original IDE layer was a fixed attractor always pulling toward the origin.

By redefining it relative to the distance $r$ from the target, **the global flow itself pursues the target**.

This reduces the burden on $G(r)$ to "forcibly pull back", maintaining smooth transitions while eliminating steady-state error.

元の IDE 層は常に原点を目指す固定引力でした。これを目標値からの相対距離 $r$ に基づく形に変更することで、**大局流そのものが目標を追いかける**構造になります。

古典補正 $G(r)$ が「無理やり引き戻す」負担が減り、遷移の滑らかさを維持したまま定常偏差をゼロにできます。

---

### Proposal 2: Explosion-Suppression $k$ (Dynamic Sensitivity Control)

### 案2：計算爆発抑制型 $k$ （動的感度制御）

**Use case:** Preventing divergence when transition velocity is very high.

**用途：** 遷移速度が非常に速い局面での発散防止。

$$k_{\text{eff}} = k_0 \cdot (1 + \beta |\dot{r}|)$$

| State | Behavior of $k_{\text{eff}}$ | Effect |

|---|---|---|

| High-speed transition ($|\dot{r}|$ large) | Automatically increases | Classical layer suppressed; IDE inertia prioritized |

| Low-speed / converging ($|\dot{r}|$ small) | Decreases | Classical precision correction fully active |

| 状態 | $k_{\text{eff}}$ の挙動 | 効果 |

|---|---|---|

| 高速遷移時（ $|\dot{r}|$ 大） | 自動的に増大 | 古典層の介入が弱まり IDE の慣性が優先 |

| 低速・収束時（ $|\dot{r}|$ 小） | 小さくなる | 古典層の精度補正がフルに機能 |

"Safety (transition preservation) at high speed; precision at low speed" — dynamic allocation of computational resources.

This is not external adjustment of $k$, but the gate structure autonomously varying its response width from the inside.

「速いときは遷移維持を、遅いときは精度を」という**計算資源の動的配分**が可能です。

これは `k` を外から調整するのではなく、ゲート構造が内側から応答幅を自律的に変える挙動です。

---

### Proposal 3: High-Precision Convergence $\Phi(x)$ (PD Element)

### 案3：高精度追い込み型 $\Phi(x)$ （PD 要素の導入）

**Use case:** Improving convergence precision when computational capacity allows.

**用途：** 計算量に余裕がある場合の収束精度向上。

$$\Phi(x, v) = P + D \cdot \frac{v}{1 + |r|}$$

Applying PD control across the full domain causes computational explosion.

By enclosing it inside $G(r)$, it acts as **a high-precision damper that activates only when error is large**.

Preservation of property error is handled by the IDE layer; "snap-to" precision at convergence is handled by the classical differential term.

通常の PD 制御を全域に適用すると計算爆発の原因になりますが、 $G(r)$ の内側に封じ込めることで**「誤差が大きいときだけ働く高精度ダンパー」**として機能します。

性質誤差の保持は IDE 層が担保し、収束時の「ピタッと止まる精度」は古典層の微分項が受け持ちます。

---

## Integrated Formula

## 統合式

$$\frac{d^2x}{dt^2} + \gamma\dot{x} = F_{\text{IDE}}(x, x_{\text{exact}}) + G_{\text{eff}}(r) \cdot \Phi(x, v)$$

$$G_{\text{eff}}(r) = r \cdot \frac{|r|}{k_{\text{eff}} + |r|}, \quad k_{\text{eff}} = k_0 (1 + \beta|\dot{r}|)$$

$$F_{\text{IDE}} = 0.5 \cdot r, \quad \Phi(x, v) = P + D \cdot \frac{v}{1 + |r|}$$

---

## Reference Implementation (Conceptual Code)

## 参照実装（概念コード）

```python

# IDE_AdaptiveGate_Extension_20260407_2241.py

import numpy as np

def compute_acceleration_advanced(x, v, x_exact, v_exact, k0=1.0, beta=0.1, P=2.0, D=0.5):

    """

    Acceleration computation via adaptive gate extension.

    Upper-layer extension of normalized_quadratic_gate

    in nra_ide_foundation_fixed_JP.py.

    適応型ゲート拡張による加速度計算。

    nra_ide_foundation_fixed_JP.py の normalized_quadratic_gate の上位拡張。

    """

    r    = x_exact - x

    rdot = v_exact - v

    # Proposal 2: dynamic k — gate autonomously controls response width from inside

    # 案2: 動的 k（内側が揺らいで応答幅を自律制御）

    k_eff = k0 * (1.0 + beta * np.abs(rdot))

    # Proposal 1: relative-coordinate IDE — global flow pursues target

    # 案1: 相対座標 IDE（大局流が目標を追いかける）

    f_ide = 0.5 * r

    # Proposal 3: high-precision correction through gate

    # 案3: ゲートを通した高精度補正

    g_val = r * np.abs(r) / (k_eff + np.abs(r))

    phi   = P + D * rdot / (1.0 + np.abs(r))

    return f_ide + g_val * phi - 0.5 * v

```

---

## Connection to Existing Core

## 既存コアとの接続

```

nra_ide_foundation_fixed_JP.py

  └── normalized_quadratic_gate(correction, knee)  ← fixed k / core immutable

        ↑                                             固定 k・コア不変

IDE_AdaptiveGate_Extension (this document)

  └── compute_acceleration_advanced()               ← dynamic k / upper extension

        generates k_eff and passes it to G(r)         動的 k・上位拡張

                                                       k_eff を生成して G(r) に渡す構造

```

This extension does not overwrite the core.

It is positioned as an adapter layer that computes `k_eff` and passes it down.

本拡張はコアを上書きしません。`k_eff` を計算して渡すアダプター層として位置づけます。

---

## Correspondence with NRA-IDE Axioms

## NRA-IDE 公理との対応

| Axiom | Realization in This Extension |

|---|---|

| Distance is result, not cause | $r$ is computed as a response result, not used as direct input |

| Honest confession at threshold | When $k_{\text{eff}}$ is large, the classical layer falls silent |

| Respect for irreversibility | Continuous update via velocity; direct overwrite prohibited — inherited |

| 公理 | 本拡張での実現 |

|---|---|

| 距離は結果であって原因ではない | $r$ は入力ではなく応答の結果として計算される |

| 閾値での正直な告白 | $k_{\text{eff}}$ が大きいとき古典層は沈黙する |

| 不可逆性への敬意 | 速度経由の連続更新・直接上書き禁止は継承 |

---

## References

## 参照

- `nra-core/nra_ide_foundation_fixed_JP.py`

- `nra-core/IDE_Classical_Hybrid_非線形大規模シミュレーション...md`

- NRA-IDE Project: https://github.com/M-Tokun/NRA-IDE

---

*© M-Tokuni / NRA-IDE Project*
