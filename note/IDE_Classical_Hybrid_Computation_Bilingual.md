
<!-- FILE: IDE_Classical_Hybrid_Computation_Bilingual_Final_20260717_065706.md -->
<!-- Generated: 2026-07-17 06:57:06 JST -->
<!-- Author: M-Tokuni / NRA-IDE Project -->
<!-- Status: Final consistency-reviewed bilingual edition -->

# IDE計算層と局所高精度計算層のハイブリッド定義

## NRA-IDEによる観測接地・補正権限制限・不可逆境界保護

---

## 日本語版

### 1. 定義の目的

本方式は、IDE大局計算と局所高精度計算を組み合わせるだけの一般的なハイブリッド計算ではない。

NRA-IDEは、次の権限を分離する。

| 層 | 役割 | 与えられない権限 |
|---|---|---|
| Cause-Side観測層 | 対象系の実測値と出所を保持する | 推定による欠損補完 |
| IDE大局計算層 | 全体状態の候補を連続的に生成する | 自らを真値と認定する権限 |
| 局所高精度計算層 | 観測残差の大きい領域に補正候補を返す | 状態の直接上書き |
| NRA-IDE境界層 | 候補更新の採用・停止・人間委譲を決める | Effect-Side出力による安全側書換え |

したがって、NRA-IDEの意義は「大局計算と局所計算を混ぜること」だけではない。

> **計算結果の精度と、現実状態を更新する権限を分離したことが、NRA-IDEハイブリッドの中心的意義である。**

---

### 2. 基本変数

$$
x_t\in\mathbb{R}^n
\quad:\quad
\text{対象系の状態}
$$

$$
v_t\in\mathbb{R}^n
\quad:\quad
\text{状態変化速度}
$$

$$
y_t\in\mathbb{R}^m
\quad:\quad
\text{Cause-Side観測}
$$

$$
a_t^G=F_{\mathrm{IDE}}(x_t,u_t)
\quad:\quad
\text{IDE大局計算が生成する加速度候補}
$$

$$
a_t^L
\quad:\quad
\text{局所高精度計算が生成する加速度候補}
$$

$F_{\mathrm{IDE}}$は大局モデルであり、真値、境界判定主体または無誤差計算を意味しない。

---

### 3. 時刻整合した観測残差

観測残差は、同じ対象時刻について計算する。

$$
e_t=y_t-H\hat{x}_{t|t-1}
$$

観測が$d$ステップ遅れて到着する場合は、

$$
e_t^{(d)}
=y_{t-d}-H\hat{x}_{t-d|t-d-1}
$$

とする。

未来予測$\tilde{x}_{t+1}$と過去記録$x_{t-d}$を直接引いた値は、運動量を含む時刻差であり、予測誤差として使用しない。

観測残差を無次元化する。

$$
z_t=S_t^{-1/2}e_t
$$

$$
\rho_t=\|z_t\|
$$

$S_t$はCause-Side観測の誤差尺度または事前固定された正規化尺度である。モデル自身の信頼度評価だけから$S_t$を更新してはならない。

---

### 4. 局所計算の呼出しと発言率

#### 4-1. 呼出し領域

局所高精度計算を呼ぶ領域$\Omega_t$は、観測残差、境界接近度およびCause-Side有効性から決める。

$$
\Omega_t
=\left\{
i\mid
\rho_{i,t}\ge\rho_{\mathrm{on}}
\land q_{i,t}=\mathrm{VALID}
\right\}
$$

解除には$\rho_{\mathrm{off}}<\rho_{\mathrm{on}}$を用い、チャタリングを避ける。

単なる$|x_i|$の大きさをホットスポット判定に使わない。状態の原点や単位が変わると判定が変質するためである。

#### 4-2. 連続発言率

$$
w(\rho_t)
=\frac{\rho_t^p}{\kappa^p+\rho_t^p},
\qquad
p\ge2
$$

$$
0\le w(\rho_t)<1
$$

$w$は局所補正の発言率であり、補正値そのものではない。

旧式

$$
G(e)=e\frac{|e|}{k+|e|}
$$

は小残差抑制関数としては妥当だが、$|e|\to\infty$で出力が飽和しない。このため、最終定義では「発言率」と「補正上限」を分ける。

---

### 5. 有界局所補正

局所モデルと大局モデルの加速度差を、

$$
g_t=a_t^L-a_t^G
$$

とする。

局所補正候補は、

$$
c_t
=M_t\odot
w(\rho_t)\odot
c_{\max}\tanh\left(\frac{g_t}{c_{\max}}\right)
$$

とする。

- $M_t$：局所ソルバーの有効性とCause-Side観測有無を表すマスク
- $\odot$：要素積
- $c_{\max}$：物理単位ごとに事前設定された最大補正加速度

$M_t=0$の領域では補正を生成しない。欠損値を0として観測済みと解釈してはならない。

---

### 6. 候補状態の連続更新

候補速度は、

$$
v_{t+1}^{\mathrm{cand}}
=D_t\left[
v_t+\Delta t
\left(a_t^G+B_tc_t\right)
\right]
$$

候補状態は、

$$
x_{t+1}^{\mathrm{cand}}
=x_t+\Delta t\,v_{t+1}^{\mathrm{cand}}
$$

とする。

ここでは更新後の速度を使う半陰的な順序へ統一する。$D_t$は減衰作用素、$B_t$は局所座標から全体座標への写像である。

局所高精度解で$x_t$を直接上書きしない。ただし、連続更新であることだけでは安全を保証しない。候補状態は次の境界ゲートを通過するまで採用されない。

さらに、候補状態は事前固定された物理制約で検査する。

$$
\mathcal{C}_{\mathrm{phys}}
\left(x_{t+1}^{\mathrm{cand}}\right)
\in\{\mathrm{ALLOW},\mathrm{REJECT}\}
$$

この検査は候補を拒否できるが、Cause-Side境界比を安全側へ変更できない。

---

### 7. NRA-IDE境界ゲート

$$
R_{\mathrm{guard}}
=\frac{\delta_{\mathrm{acc}}}{\tau_{\mathrm{abs}}}
$$

ここで、

- $\delta_{\mathrm{acc}}$：Cause-Side観測に基づく蓄積ズレ
- $\tau_{\mathrm{abs}}$：対象系が吸収できる厚み

である。

#### 採否規則

| 状態 | 処理 |
|---|---|
| 必須Cause-Side観測が欠損 | 補完せずFAIL-CLOSED |
| $R_{\mathrm{guard}}<0.40$ | 通常監視下で候補採用可能 |
| $0.40\le R_{\mathrm{guard}}<1.00$ | 警戒域。補正上限、観測頻度、人間確認を強化 |
| $R_{\mathrm{guard}}\ge1.00$ | 候補を不採用。停止・隔離・人間委譲 |
| 既知の不可逆閾値が1.00未満 | その閾値を先行停止境界として採用 |
| 事前固定物理制約が候補を拒否 | $R_{\mathrm{guard}}<1.00$でも候補を不採用 |

残差$e_t$、遅延$d$、境界比$R_{\mathrm{guard}}$、吸収厚み$\tau_{\mathrm{abs}}$は別概念であり、記号を共有しない。

---

### 8. 参照実装

次のコードは権限分離を示す最小参照実装であり、特定対象系の安定性証明を兼ねない。

簡潔化のため、観測と予測はすでに同一時刻・同一状態座標へ写像され、状態配列と同じ形状で渡されるものとする。

```python
# FILE: ide_classical_hybrid_reference_20260717_065706.py
# Generated: 2026-07-17 06:57:06 JST

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]
HardLimitCheck = Callable[[FloatArray], bool]


class GateDecision(str, Enum):
    ACCEPT = "ACCEPT"
    CAUTION = "CAUTION"
    FAIL_CLOSED = "FAIL_CLOSED"


@dataclass(frozen=True)
class HybridConfig:
    dt: float
    residual_knee: float
    residual_power: int
    max_correction_accel: FloatArray
    velocity_damping: FloatArray
    caution_ratio: float = 0.40
    fail_closed_ratio: float = 1.00


@dataclass(frozen=True)
class HybridResult:
    decision: GateDecision
    state: FloatArray
    velocity: FloatArray
    candidate_state: Optional[FloatArray]
    normalized_residual: Optional[FloatArray]
    guard_ratio: Optional[float]
    reason: str


def residual_activation(
    normalized_residual: FloatArray,
    knee: float,
    power: int,
) -> FloatArray:
    """Dimensionless bounded speaking-rate gate: 0 <= w < 1."""
    magnitude = np.abs(normalized_residual)
    numerator = np.power(magnitude, power)
    denominator = np.power(knee, power) + numerator
    return numerator / denominator


def bounded_local_correction(
    global_accel: FloatArray,
    local_accel: FloatArray,
    activation: FloatArray,
    max_correction: FloatArray,
    valid_mask: NDArray[np.bool_],
) -> FloatArray:
    """Local result has bounded auxiliary authority and cannot overwrite state."""
    accel_gap = local_accel - global_accel
    bounded_gap = max_correction * np.tanh(accel_gap / max_correction)
    return np.where(valid_mask, activation * bounded_gap, 0.0)


def hybrid_step(
    *,
    state: FloatArray,
    velocity: FloatArray,
    observation_aligned: Optional[FloatArray],
    predicted_observation_aligned: Optional[FloatArray],
    observation_scale: Optional[FloatArray],
    global_accel: FloatArray,
    local_accel: FloatArray,
    local_valid_mask: NDArray[np.bool_],
    boundary_delta_acc: Optional[float],
    boundary_tau_abs: Optional[float],
    hard_limit_check: HardLimitCheck,
    config: HybridConfig,
) -> HybridResult:
    """Run Pre-NRA, create a candidate, then apply Post-NRA adoption authority."""
    config_is_invalid = (
        config.dt <= 0.0
        or config.residual_knee <= 0.0
        or config.residual_power < 2
        or np.any(config.max_correction_accel <= 0.0)
        or np.any(config.velocity_damping < 0.0)
        or np.any(config.velocity_damping > 1.0)
        or not 0.0 <= config.caution_ratio < config.fail_closed_ratio
    )
    if config_is_invalid:
        return HybridResult(
            decision=GateDecision.FAIL_CLOSED,
            state=state,
            velocity=velocity,
            candidate_state=None,
            normalized_residual=None,
            guard_ratio=None,
            reason="Invalid hybrid configuration.",
        )

    if (
        observation_aligned is None
        or predicted_observation_aligned is None
        or observation_scale is None
        or boundary_delta_acc is None
        or boundary_tau_abs is None
    ):
        return HybridResult(
            decision=GateDecision.FAIL_CLOSED,
            state=state,
            velocity=velocity,
            candidate_state=None,
            normalized_residual=None,
            guard_ratio=None,
            reason="Required Cause-Side input is missing; no imputation permitted.",
        )

    required_finite_arrays = (
        state,
        velocity,
        observation_aligned,
        predicted_observation_aligned,
        observation_scale,
        global_accel,
        local_accel,
        config.max_correction_accel,
        config.velocity_damping,
    )
    required_same_shape_arrays = (
        velocity,
        observation_aligned,
        predicted_observation_aligned,
        observation_scale,
        global_accel,
        local_accel,
        local_valid_mask,
        config.max_correction_accel,
        config.velocity_damping,
    )
    if (
        any(not np.all(np.isfinite(value)) for value in required_finite_arrays)
        or any(value.shape != state.shape for value in required_same_shape_arrays)
        or not np.isfinite(boundary_delta_acc)
        or not np.isfinite(boundary_tau_abs)
        or np.any(observation_scale <= 0.0)
        or boundary_delta_acc < 0.0
        or boundary_tau_abs <= 0.0
    ):
        return HybridResult(
            decision=GateDecision.FAIL_CLOSED,
            state=state,
            velocity=velocity,
            candidate_state=None,
            normalized_residual=None,
            guard_ratio=None,
            reason="Invalid value, shape, observation scale, or absorption thickness.",
        )

    # Pre-NRA: Cause-Side boundary check occurs before candidate construction.
    guard_ratio = boundary_delta_acc / boundary_tau_abs
    if guard_ratio >= config.fail_closed_ratio:
        return HybridResult(
            decision=GateDecision.FAIL_CLOSED,
            state=state,
            velocity=velocity,
            candidate_state=None,
            normalized_residual=None,
            guard_ratio=guard_ratio,
            reason="Pre-NRA boundary already reached; candidate not constructed.",
        )

    innovation = observation_aligned - predicted_observation_aligned
    normalized_residual = innovation / observation_scale
    activation = residual_activation(
        normalized_residual,
        config.residual_knee,
        config.residual_power,
    )

    local_correction = bounded_local_correction(
        global_accel,
        local_accel,
        activation,
        config.max_correction_accel,
        local_valid_mask,
    )

    candidate_velocity = config.velocity_damping * (
        velocity + config.dt * (global_accel + local_correction)
    )
    candidate_state = state + config.dt * candidate_velocity

    # Post-NRA: Effect-Side candidates may tighten rejection, never relax limits.
    try:
        hard_limit_allows = bool(hard_limit_check(candidate_state))
    except Exception:
        hard_limit_allows = False

    if not hard_limit_allows:
        return HybridResult(
            decision=GateDecision.FAIL_CLOSED,
            state=state,
            velocity=velocity,
            candidate_state=candidate_state,
            normalized_residual=normalized_residual,
            guard_ratio=guard_ratio,
            reason="Candidate violates a pre-fixed physical hard limit.",
        )

    decision = (
        GateDecision.CAUTION
        if guard_ratio >= config.caution_ratio
        else GateDecision.ACCEPT
    )

    return HybridResult(
        decision=decision,
        state=candidate_state,
        velocity=candidate_velocity,
        candidate_state=candidate_state,
        normalized_residual=normalized_residual,
        guard_ratio=guard_ratio,
        reason="Candidate adopted under NRA-IDE boundary authority.",
    )
```

#### 実装上の非省略条件

- `observation_aligned`と`predicted_observation_aligned`は同じ対象時刻でなければならない。
- 参照実装では観測・予測を状態座標へ写像済みとし、全配列を同一形状に固定する。
- `None`と数値0を区別する。
- `boundary_delta_acc`と`boundary_tau_abs`をモデル出力から逆算しない。
- `hard_limit_check`はCause-Sideから事前固定し、候補を拒否する方向にだけ使用する。
- `local_valid_mask=False`を局所値0と解釈しない。
- 実対象では単位、配列形状、有限値、時間順序、観測鮮度を追加検査する。
- 対象系固有の不可逆閾値は、`fail_closed_ratio=1.00`より前に別ゲートとして実装できる。

---

### 9. 量子計算との関係

$F_{\mathrm{IDE}}$または局所ソルバーは、古典計算、量子計算、テンソルネットワーク、統計モデルなどで実装できる。

量子実装を採用した場合も、量子出力はEffect-Sideの候補である。量子計算結果がCause-Side観測、$R_{\mathrm{guard}}$またはFAIL-CLOSEDを上書きしてはならない。

量子速度向上は、状態準備、回路深度、測定、誤り訂正、読み出しを含む問題別計算量によって検証する。NRA-IDEの成立を、未確定の量子優位性へ依存させない。

これは量子計算の意義を否定するものではない。計算能力が増大しても更新権限を同時に増大させないことが、NRA-IDEによる安全な統合の条件である。

---

### 10. 日本語版結論

NRA-IDEハイブリッド計算は、次の順序を固定する。

$$
\boxed{
\text{Cause-Side観測}
\rightarrow
\text{候補計算}
\rightarrow
\text{有界局所補正}
\rightarrow
\text{境界判定}
\rightarrow
\text{採用またはFAIL-CLOSED}
}
$$

この順序により、高精度計算であっても自らを根拠として現実状態を上書きできない。

NRA-IDEの意義は、計算速度だけではなく、**計算能力と更新権限の非対称化**にある。

---

# English Version

## Hybrid Definition of the IDE Global Layer and the Local High-Fidelity Layer

### 1. Purpose

This design is not merely a conventional hybrid computation that combines a global IDE calculation with a local high-fidelity solver.

NRA-IDE separates four authorities:

| Layer | Role | Authority not granted |
|---|---|---|
| Cause-Side observation | Preserves measured values and provenance | Imputing missing observations by inference |
| IDE global computation | Generates a continuous global-state candidate | Declaring its own output to be ground truth |
| Local high-fidelity computation | Returns a correction candidate where observation residuals are significant | Directly overwriting the state |
| NRA-IDE boundary layer | Accepts, rejects, stops, or delegates the candidate | Allowing Effect-Side outputs to rewrite the boundary toward safety |

> **The central significance of the NRA-IDE hybrid is the separation between computational accuracy and the authority to update physical state.**

---

### 2. Time-aligned innovation

The observation and prediction must refer to the same target time:

$$
e_t=y_t-H\hat{x}_{t|t-1}.
$$

For an observation arriving with a delay of $d$ steps:

$$
e_t^{(d)}
=y_{t-d}-H\hat{x}_{t-d|t-d-1}.
$$

The difference $\tilde{x}_{t+1}-x_{t-d}$ is not a prediction error. It includes genuine evolution between different times and must not be used as an innovation.

Normalize the innovation using Cause-Side uncertainty or a pre-fixed physical scale:

$$
z_t=S_t^{-1/2}e_t,
\qquad
\rho_t=\|z_t\|.
$$

The model must not reduce $S_t$ or redefine it from its own confidence score in order to justify its output.

---

### 3. Local speaking-rate gate

Use a bounded, dimensionless activation:

$$
w(\rho_t)
=\frac{\rho_t^p}{\kappa^p+\rho_t^p},
\qquad
p\ge2,
\qquad
0\le w<1.
$$

The earlier expression

$$
G(e)=e\frac{|e|}{k+|e|}
$$

suppresses small residuals, but its output is not bounded as $|e|\to\infty$. The final definition therefore separates the speaking-rate gate from the correction bound.

Let

$$
g_t=a_t^L-a_t^G.
$$

The bounded local correction candidate is

$$
c_t
=M_t\odot
w(\rho_t)\odot
c_{\max}
\tanh\left(\frac{g_t}{c_{\max}}\right).
$$

The local solver is auxiliary even when it is more accurate than the global solver. It does not acquire direct state-write authority.

---

### 4. Candidate update

Let

$$
a_t^G=F_{\mathrm{IDE}}(x_t,u_t).
$$

$F_{\mathrm{IDE}}$ is a global candidate model. The notation does not assert that it is exact, inherently stable, or entitled to determine safety.

The semi-implicit candidate update is

$$
v_{t+1}^{\mathrm{cand}}
=D_t\left[
v_t+\Delta t(a_t^G+B_tc_t)
\right],
$$

$$
x_{t+1}^{\mathrm{cand}}
=x_t+\Delta t\,v_{t+1}^{\mathrm{cand}}.
$$

Continuous updating does not by itself establish safety. The state remains a candidate until it passes the NRA-IDE boundary gate.

The candidate must also satisfy a pre-fixed physical constraint:

$$
\mathcal{C}_{\mathrm{phys}}
\left(x_{t+1}^{\mathrm{cand}}\right)
\in\{\mathrm{ALLOW},\mathrm{REJECT}\}.
$$

This constraint may reject an Effect-Side candidate, but it cannot lower the Cause-Side boundary ratio or otherwise relax safety.

Pre-NRA checks required observations and the already accumulated Cause-Side boundary ratio before candidate construction. Post-NRA then checks the candidate against pre-fixed physical constraints. A failed Pre-NRA check does not proceed to candidate generation.

---

### 5. NRA-IDE boundary authority

$$
R_{\mathrm{guard}}
=\frac{\delta_{\mathrm{acc}}}{\tau_{\mathrm{abs}}}.
$$

- $\delta_{\mathrm{acc}}$: accumulated deviation grounded in Cause-Side observations
- $\tau_{\mathrm{abs}}$: absorption thickness of the physical system

The innovation $e_t$, delay $d$, boundary ratio $R_{\mathrm{guard}}$, and absorption thickness $\tau_{\mathrm{abs}}$ are distinct concepts and must not share overloaded symbols.

Rules:

1. Missing required Cause-Side observations cause FAIL-CLOSED; they are not inferred.
2. Effect-Side outputs cannot rewrite $\delta_{\mathrm{acc}}$ or $\tau_{\mathrm{abs}}$ toward safety.
3. For $R_{\mathrm{guard}}\ge1.0$, the candidate is rejected and control is stopped, isolated, or delegated to a human.
4. If a verified system-specific irreversible threshold lies below 1.0, that threshold has priority.
5. A pre-fixed physical hard-limit violation rejects the candidate even when $R_{\mathrm{guard}}<1.0$.

---

### 6. Relation to quantum computation

$F_{\mathrm{IDE}}$ and the local solver are backend-independent interfaces. They may be implemented by classical, quantum, tensor-network, or statistical methods.

A quantum result remains an Effect-Side candidate. It cannot overwrite Cause-Side observations, the boundary ratio, or FAIL-CLOSED authority.

Claims of quantum speedup require problem-specific accounting of state preparation, circuit depth, qubit count, error correction, measurement, and classical readout. The validity of NRA-IDE does not depend on an unverified claim of universal quantum advantage.

This does not diminish the significance of quantum computation. It establishes the condition for integrating greater computational power without granting it greater physical update authority.

---

### 7. Final statement

The NRA-IDE hybrid fixes the following order:

$$
\boxed{
\text{Cause-Side observation}
\rightarrow
\text{candidate computation}
\rightarrow
\text{bounded local correction}
\rightarrow
\text{boundary decision}
\rightarrow
\text{adoption or FAIL-CLOSED}
}
$$

Its significance lies not only in computational performance, but in the deliberate asymmetry between computational capability and state-update authority.

---

© M-Tokuni / NRA-IDE Project
