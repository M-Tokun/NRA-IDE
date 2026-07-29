# NRA-IDE Demo #14 — Power Grid Transition

## 電力系統 遷移点解析

**FILE: README_Demo14_PowerGrid_26-0321.md**  

**Author: M-Tokuni / NRA-IDE Project**  

**GitHub: https://github.com/M-Tokun/NRA-IDE**

---

## Why This Demo Exists / このデモが存在する理由

Conventional power grid monitoring answers a single question: *"Has the frequency crossed the threshold?"*  

The answer arrives **after** the transition has already occurred.

NRA-IDE asks a different question: *"How fast is the system approaching the threshold, and how much structural debt has accumulated?"*  

This answer arrives **before** the transition — while intervention is still possible.

従来の電力系統監視が答える問いは「周波数が閾値を超えたか」という一点の判断です。  

その答えが出る時、遷移はすでに起きています。

NRA-IDEが答える問いは「どの速さで閾値に近づいているか、構造的負債はいくら積まれているか」です。  

この答えは遷移の**前**に出ます。介入がまだ可能な段階で。

---

## What You Are Looking At / 画面の見方

### Upper Waveform — Frequency f [Hz]

- Nominal frequency: **50 Hz** (dashed reference line)

- The waveform color reflects the current FSM state (green / yellow / red)

- **Dual fluctuation is always present**: micro-δ (high-frequency noise) + macro-δ (system-wide swell) + spike-δ (event-triggered)

### Lower Waveform — R = δ/τ

- **τ = 1.0 line (red dashed)**: the RUPTURE_BOUNDARY threshold

- **0.4 line (yellow dashed)**: ZONE-B entry point

- The shaded region to the left of the τ line is the safe operating zone

- When R crosses 1.0, a red flash fires and the FSM transitions to RUPTURE_BOUNDARY

### Left Panel

| Display | Meaning |

|---|---|

| f [Hz] | Current frequency |

| δf [Hz] | Absolute deviation from 50 Hz |

| τ | Absorption thickness (adjustable via slider) |

| R = δ/τ | Structural approach ratio |

| FSM State | Current gate state |

| residual_debt | Accumulated structural debt — **does not reset on recovery** |

### Right Panel — Generator Units

Each bar shows the load ratio of each generating unit.  

When a unit trips, its bar goes dark and spike-δ is injected.

---

## How to Operate / 操作方法

| Button | Action |

|---|---|

| ⚡ 発電機脱落 | Trips a random online generator. HR↑, BP↓ type event. |

| 📈 需要急増 | Injects a demand surge event. Sustained δ increase. |

| 🔄 系統復旧／新評価 | Before rupture, applies human-operated grid recovery. After `RUPTURE_BOUNDARY`, starts an independent Cause-Side evaluation following external inspection. |

| ■ 独立した新評価 | Starts a new evaluation history without releasing the prior rupture record. |

| SPEED slider | Simulation speed ×1–×5 |

| τ slider | Adjust absorption thickness. Observe how threshold sensitivity changes. |

**Important**: After RUPTURE_BOUNDARY activates, the event buttons are disabled.

The prior rupture classification is never reversed. After external inspection, `🔄 系統復旧／新評価` starts a separate Cause-Side history; it does not modify the old Effect-Side record.

---

## Why This Structure Is Necessary / なぜこの構造が必要なのか

### 1. The wall detector problem — 壁検知器の問題

A smoke alarm detects fire after the fire has started.  

A conventional grid monitor detects under-frequency after the frequency has already fallen.

```

既存監視：  f < 49.0Hz → アラーム

            ↑ この時点でUFLS（負荷遮断）発動まで数百ミリ秒

            ↑ カスケード崩壊はすでに始まっている

NRA-IDE：   R の上昇速度が基準を超えた → 先行警告

            ↑ f はまだ正常範囲内

```

### 2. The spike does not erase the debt — スパイクは負債を消さない

When a generator trips, the frequency recovers naturally as other units compensate.  

The waveform returns to near-normal. Conventional monitors reset.

NRA-IDE does not reset. `residual_debt` continues to hold the accumulated structural stress.  

The system "remembers" that it was under severe load, even after the visible spike subsides.

```

既存モニター：  スパイク → 回復 → リセット → "正常"

NRA-IDE：      スパイク → 回復 → residual_debt 残存 → "表面は正常、構造は負債を抱えている"

```

This mirrors material fatigue: a steel beam that has been overstressed does not become new again just because the load was removed.

### 3. τ is a structural design parameter, not a threshold — τは閾値ではなく設計パラメータ

Conventional threshold: `f < 49.0Hz` is a wall. Do not cross it.  

NRA-IDE τ: the point at which the system **will inevitably reach** if δ accumulation continues.

The engineering question is not "did we cross the wall?" but "how long until we reach τ, and what is our residual capacity?"

### 4. Human authority and new evaluation — 人間権限と新規評価

RUPTURE_BOUNDARY does not self-reset. This is not a limitation — it is a structural guarantee.

No automatic re-energization occurs. Human inspection may authorize a separate new evaluation, but cannot release the prior rupture latch.

This implements the principle: **Cause-Side authority belongs to the human operator.**  

Effect-Side values (the recovered waveform) cannot override the gate.

---

## Formula Reference / 数式参照

$$R = \frac{\delta_f}{\tau}$$

$$\delta_f = |f_{current} - f_{nominal}|$$

$$\text{residual}\_\text{debt}(t) = \int_0^t (R - R \cdot k_{recovery}) \, dt$$

$$R_{\mathrm{target}} \geq 1.0 \Rightarrow \mathrm{RUPTURE\_BOUNDARY}$$

---

## Relation to NRA-IDE Layer Structure / NRA-IDEレイヤーとの対応

| Layer | This Demo |

|---|---|

| Layer 1 — Basic R = δ/τ | Core formula |

| Layer 3 — Dynamic τ / Damper | τ slider, spring recovery |

| Layer 4 — Sensor Fusion | Multi-generator δ composition |

Demo #14 operates primarily at **Layer 3–4**.

---

*NRA-IDE Project — M-Tokuni*  

*https://github.com/M-Tokun/NRA-IDE*  

*https://x.com/m_tokuni*  

*README_Demo14_PowerGrid_26-0321.md*
