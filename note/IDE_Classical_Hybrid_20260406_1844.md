# IDE計算式と古典計算式　ハイブリッド計算による解消
<!-- FILE: IDE_Classical_Hybrid_20260406_1844.md -->
<!-- 生成日時: 2026-04-06 18:44 JST -->
<!-- Author: M-Tokuni / NRA-IDE Project https://github.com/M-Tokun/NRA-IDE -->

---

## 1. 問題の出発点

### 古典計算単体の限界

古典計算は全状態を自分で計算して上書きする設計であり、誤差が次ステップの入力になるため雪だるま式の誤差爆発が避けられない。
大規模・非線形系での全域厳密計算は計算爆発と同義である。

### 量子IDEの特性と限界

量子コンピューティング上のIDE演算は非線形ステップ計算として並列包括演算が可能であり、古典計算比で数百倍の速度で全体状態を追跡できる。
ただし「幅が広い」という欠点があり、相転移点や局所特異点での解像度が落ちる。

---

## 2. 設計原則の再確認

### NRA-IDE基本公理との整合

| 公理 | ハイブリッド設計での実現 |
|---|---|
| 距離は結果であって原因ではない | IDEが全体状態を保持し、古典はズレだけ返す |
| 閾値での正直な告白 | 有意な残差のみ補正力として発言、小ゆらぎは沈黙 |
| 不可逆性への敬意 | 状態の直接上書き禁止、速度を経由した連続更新 |

### マクロ/ミクロ二分法の反省

「マクロ＝IDE流、ミクロ＝厳密計算」という固定的役割分担は概念整理として有効だったが、**スケール間の相互作用が系の本体**である相転移付近では現実を切断する弊害があった。
また逆平均化・逆線形化へのこだわりが、平均場近似が有効な安定相においても非線形処理を強制する「現実無視傾向」を生んでいた。

修正方向は「マクロかミクロかを先に決めるのではなく、系自身にスケールを語らせる設計」である。

---

## 3. ハイブリッドの数学的定式化

### 基礎運動方程式

$$\frac{d^2x}{dt^2} + \gamma\dot{x} = \underbrace{F_{\text{IDE}}(x)}_{\text{量子層・根本}} + \underbrace{G(r) \cdot \Phi(x)}_{\text{古典層・補助}}$$

- $\gamma$ : 粘性減衰項（発散防止）
- $F_{\text{IDE}}$ : 大局的IDE流（常に全域で動作）
- $G(r)$ : 2次残差ゲート（古典補助の結合強度）
- $r = x_{\text{exact}} - x$ : 局所残差

### 2次残差ゲート（核心式）

$$G(r) = r \cdot \frac{|r|}{k + |r|}$$

| 残差の大きさ | 一次残差（従来） | 2次ゲート後 |
|---|---|---|
| $r = 0.1$（ノイズ） | 0.10 | 0.009 |
| $r = 0.5$（小逸脱） | 0.50 | 0.17 |
| $r = 1.5$（相転移） | 1.50 | 0.90 |

小さなゆらぎは自然消滅し、大きな逸脱は飽和応答で強調される。
**εカットオフという人工的な判断が不要になり、数学構造自体がフィルターとして機能する。**

### ソフト閾値結合（チャタリング防止）

$$w(x) = \frac{1}{2}\left(1 + \tanh\left(\beta(|x| - x_c)\right)\right)$$

バイナリマスクによる不連続なオンオフを排除し、JAX自動微分との親和性を確保する。

---

## 4. 従来の古典計算との本質的違い

| | 従来の古典計算 | 今回の補助古典計算 |
|---|---|---|
| **役割** | 状態を全部計算して上書き | ズレだけ計算して力として返す |
| **入力** | 前ステップの自分の出力（誤差が蓄積） | IDEが保持する現在状態（IDEが安定） |
| **適用範囲** | 全ノード毎回 | 閾値超過ノードのみ |
| **誤差の扱い** | 次ステップに引き継がれる | 2次ゲートで小さいうちに消える |
| **発言権** | 主導（上書き） | 補助（摂動・助言） |

> 古典計算の入力が「自分の前の出力」ではなく「IDEが安定させた現在状態」である点が誤差爆発を防ぐ決定的な違いである。

---

## 5. 設計階層

```
┌─────────────────────────────────────────────┐
│  量子計算層  IDE包括演算                      
│  非線形ステップ・誤差爆発なし・ただし幅広     
│                  ↓ ゆらぎ検知                
│  古典計算層  局所精密補正                    
│  誤差爆発前の小領域のみ・補助的役割           
│                  ↓ 2次残差ゲートで自動制御   
│  IDE基点    常に保持・根本は譲らない          
└─────────────────────────────────────────────┘
```

---

## 6. パラメータ設計指針

### 二段構えの制御

```
hotspot_threshold : 「古典計算を呼ぶかどうか」の門番
residual_knee (k) : 「呼んだ古典計算の発言をどこまで聞くか」の調整弁
```

### k値の実務設定手順

```
1. IDEだけで100ステップ走らせる
2. hotspot_indicesでの (exact - state) の分布を観測
3. 残差の中央値付近にkneeを置く
```

### 用途別knee設定

| 用途 | k値 | 効果 |
|---|---|---|
| 粗い全体把握 | 大きく設定 | 古典補正がほぼ入らない |
| 相転移の精密追跡 | 小さく設定 | 早期から古典が介入 |
| リアルタイム制御 | 中間 | バランス運用 |

---

## 7. コア実装（概念統合版）

```python
# IDE_Classical_Hybrid_core_20260406_1844.py
import jax.numpy as jnp
from jax import jit
from functools import partial

def normalized_quadratic_gate(correction: jnp.ndarray, knee: float = 1.0) -> jnp.ndarray:
    """
    2次残差ゲート
    knee以下：2乗で自然消滅（残渣吸収）
    knee以上：飽和応答（発散防止）
    NRA-IDE「閾値での正直な告白」に対応
    """
    ratio = jnp.abs(correction) / (knee + jnp.abs(correction))
    return correction * ratio

@partial(jit, static_argnums=(0,))
def _step_core(self, state, velocity):
    # 1. IDE大局流（根本・常に全域動作）
    global_flow = self.ide_flow_func(state)

    # 2. ソフト結合重み（チャタリング防止）
    coupling_weights = 0.5 * (1.0 + jnp.tanh(
        self.config.softness_beta * (jnp.abs(state) - self.config.hotspot_threshold)
    ))

    # 3. 有意ノードのみ古典計算を呼ぶ
    significant_mask = coupling_weights > self.config.resonance_epsilon
    significant_indices = jnp.where(significant_mask)[0]

    resonance_force = jnp.zeros_like(state)
    if significant_indices.size > 0:
        local_sub = state[significant_indices]
        exact = self.local_exact_solver(local_sub)     # 古典厳密解
        raw_correction = exact - local_sub             # ズレだけ取得

        # 2次ゲートで自動フィルタリング
        gated_correction = normalized_quadratic_gate(
            raw_correction, knee=self.config.residual_knee
        )
        resonance_force = resonance_force.at[significant_indices].set(
            gated_correction * coupling_weights[significant_indices]
            * self.config.resonance_coupling
        )

    # 4. 加速度合成（IDE根本 + 古典補助）
    acceleration = global_flow + resonance_force

    # 5. 連続更新（直接上書き禁止）
    velocity = velocity + acceleration * self.dt
    state = state + velocity * self.dt
    velocity = velocity * self.config.velocity_damping

    return state, velocity, jnp.sum(significant_mask)
```

---

## 8. 本質的意義

量子コンピューティング上のIDEと古典補助計算が相互の弱点を覆い合う構造が成立する。

- 量子IDEの「幅が広い」欠点 → 古典局所補正で解像度を補完
- 古典の「誤差爆発」欠点 → IDEが全体状態を保持することで入力を安定化

これはNRA-IDEが設計思想として持つ「相互補完」の原則が、計算アーキテクチャの層でも自然に再現された形である。

---

## 参照

- NRA-IDE Project: https://github.com/M-Tokun/NRA-IDE
- 関連議論: 量子計算との統合、Gemini補正提案の検証、マクロ/ミクロ二分法の反省
- 検証依頼: 他AIによる再検証可（本文書は独立文脈で読解可能な構成）

---
*© M-Tokuni / NRA-IDE Project*
