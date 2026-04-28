# NRA-IDE Demo #15 — OR/ICU Continuum Monitor

## 経過蓄積型モニタリング / 手術室・集中治療室

**FILE: README_Demo15_OR_ICU_26-0321.md**  

**Author: ©M-Tokuni / NRA-IDE Project**  

**GitHub: https://github.com/M-Tokun/NRA-IDE**

---

## Core Principle / 中核原理

> **経過こそ威力。**  

> The longer the observation continues, the more reliable the structural judgment becomes.

This demo embodies a design truth that distinguishes NRA-IDE from conventional vital sign monitors:

**Knowing the present requires the past.**

Without elapsed history, δ has nowhere to accumulate. Without accumulated δ, R has no meaning.  

This is why new patients and emergency arrivals cannot benefit from NRA-IDE immediately —  

and why this limitation is stated explicitly rather than hidden.

現在を知るためには経過が必須です。  

経過がなければδは積まれず、δがなければRは意味を持ちません。  

これが新患・救急にNRA-IDEが即座には機能しない理由であり、その制約を設計として正直に表現したものがこのデモです。

---

## Why Existing Monitors Are Insufficient / 既存モニターでは足りない理由

### The point-in-time problem

```

既存バイタルモニター：

  HR > 100 → アラーム

  SpO₂ < 92% → アラーム

  各チャンネルが独立した閾値を持つ

問題：

  HR = 98（正常範囲内）

  SpO₂ = 93%（正常範囲内）

  RR = 22（やや高め・正常範囲内）

  BP = 95（やや低め・正常範囲内）

  → 全チャンネル "正常" → アラームなし

  → しかし4チャンネル合成R_totalは上昇中

  → ショック前状態に入りつつある

```

NRA-IDE computes:

$$R_{total} = \sqrt{R_{HR}^2 + R_{SpO_2}^2 + R_{RR}^2 + R_{BP}^2}$$

Each channel below its individual threshold, yet the **structural aggregate** is rising.  

This is the pre-shock warning that point-in-time monitors cannot generate.

### The reset problem

```

既存EWS（Early Warning Score）:

  イベント → スコア上昇 → 回復 → スコアリセット → "正常"

NRA-IDE:

  イベント → R上昇 → 波形回復 → residual_debt 残存 → "表面回復・構造負債継続"

```

A patient who survived a hemorrhagic event 20 minutes ago is not structurally equivalent to a patient who has been stable for 3 hours. NRA-IDE maintains this distinction. Existing monitors do not.

---

## The Warmup Period / ウォームアップ期間

This is the most important design element of Demo #15.

When the demo starts (equivalent to a new patient or emergency arrival), the accuracy indicator shows ☆☆☆☆☆. τ has not been established. R values displayed are reference-only.

As procedure time accumulates, τ is progressively established from the patient's own baseline.  

At 100% warmup, the accuracy reaches ★★★★★ and R operates at full structural reliability.

```

00:00  新患状態 / τ未確立 / R = 参考値のみ

  ↓

観測継続（執刀後 〜90秒 シミュレーション換算）

  ↓

τ確立完了 / R = 最高精度 / residual_debt が構造的意味を持つ

```

**The system does not pretend to know what it cannot know.**  

During warmup, the structural judgment is explicitly marked as unreliable.  

This is the Fail-Closed principle applied to the system's own epistemic state.

---

## What You Are Looking At / 画面の見方

### Upper Canvas — Vital Waveforms

Four simultaneous channels:

| Channel | Color | Normal Range |

|---|---|---|

| HR (heart rate) | Cyan | 60–100 bpm |

| SpO₂ | Green | 96–100% |

| RR (respiratory rate) | Orange | 12–20 /min |

| BP systolic | Purple | 90–140 mmHg |

Waveform brightness increases during FAIL-CLOSED state.

### Lower Canvas — R_total

- **τ = 1.0 line** (red dashed): FAIL-CLOSED threshold

- **0.6 line** (orange dashed): CRITICAL zone entry

- **0.35 line** (yellow dashed): CAVEAT zone entry

- **Blue shaded region (left)**: Warmup zone — R precision not yet established

- The R_total waveform color shifts from blue → yellow → orange → red as R increases

### Left Panel

| Display | Meaning |

|---|---|

| 経過蓄積 / Baseline確立 | Warmup progress. τ is being established from observation history. |

| Phase Box | Current FSM state |

| HR / SpO₂ / RR / BP | Current vital values with individual R bars |

| residual_debt | **Structural debt. Does not reset after recovery.** |

| Event Log | Timestamped event and transition record |

### Right Panel

| Display | Meaning |

|---|---|

| R_total | Composite structural approach ratio |

| δ成分分解 | Individual δ values per channel |

| 経過精度 ★ | Warmup quality. ★★★★★ = maximum structural reliability |

| 遷移履歴 | Log of all FSM state transitions with R values |

---

## FSM States / FSM状態

| State | Condition | Meaning |

|---|---|---|

| WARMING UP | warmupPct < 15% | τ not established. Observation phase. |

| ACTIVE | R_eff < 0.35 | Structural stability confirmed. |

| CAVEAT ⚠ | 0.35 ≤ R_eff < 0.6 | δ accumulation detected. Monitor closely. |

| CRITICAL 🔴 | 0.6 ≤ R_eff < 1.0 | Approaching threshold. Pre-intervention zone. |

| FAIL-CLOSED ⛔ | R_eff ≥ 1.0 or debt > 1.2 | Structural limit reached. **Human judgment required.** |

FAIL-CLOSED does not self-reset. Only `✚ 医師介入` can initiate recovery.  

Even after intervention, `residual_debt` persists — reflecting accumulated structural stress.

---

## How to Operate / 操作方法

| Button | Action |

|---|---|

| ▶ 執刀開始 | Begin procedure. δ accumulation and τ establishment start. |

| 🩸 出血イベント | Hemorrhage event. HR↑, BP↓, SpO₂↓, RR↑. Sustained δ injection. |

| 💉 麻酔深度変化 | Anesthetic depth shift. HR↓, BP↓, RR↓ (respiratory depression). |

| ⚡ 血管攣縮 | Vasospasm. Acute BP spike. Short duration. |

| ✚ 医師介入 | **Human-operated only.** Activates recovery force. Unlocks events. |

| ■ リセット | Full reset to new-patient state. |

| SPEED slider | ×1–×6 simulation speed |

**Recommended sequence for demonstration:**

1. Start with `▶ 執刀開始`

2. Observe warmup progress and accuracy stars increasing

3. After ★★★ or higher, trigger `🩸 出血イベント`

4. Watch R_total rise across multiple channels simultaneously

5. Note that residual_debt persists even after the waveform appears to recover

6. If FAIL-CLOSED activates, use `✚ 医師介入` — observe that debt remains

---

## Why This Structure Is Necessary / なぜこの構造が必要なのか

### 1. The present cannot be known without the past / 現在は経過なしに知れない

A vital sign reading at t=0 is just a number.  

The same reading at t=60 minutes is a structural statement about where this patient is heading.

```

瞬時値：  HR = 95  → "正常範囲内"

経過値：  HR = 72 → 78 → 85 → 91 → 95  → "上昇トレンド、δ蓄積中"

```

The number did not change its meaning. The **history gave it meaning.**

### 2. Multi-channel structural composition / 多チャンネル構造合成

No single vital sign tells the full story.  

HR alone cannot distinguish anxiety from hemorrhage.  

SpO₂ alone cannot distinguish respiratory depression from airway obstruction.

$$R_{total} = \sqrt{R_{HR}^2 + R_{SpO_2}^2 + R_{RR}^2 + R_{BP}^2}$$

The composition is computed in R-space, not in the original measurement space.  

**No correlation matrix. No covariance. O(n) computation.**  

Each channel contributes its structural approach ratio independently.  

The system scales to any number of channels without combinatorial explosion.

### 3. Structural debt as accumulated fatigue / 構造的負債 = 疲労蓄積

`residual_debt` is not a log entry. It is a physical state variable.

```

ログ・記録 → 過去の事実を記録する（観測）

residual_debt → 過去の超過が現在の判断に乗っている（物理量）

```

A steel beam that has been overstressed does not recover its original fatigue margin  

simply because the load was removed.  

A patient who experienced a hemorrhagic event 20 minutes ago carries structural residue.  

`residual_debt` holds this residue in the system's present state.

### 4. Honest epistemic boundary / 正直な認識境界

During warmup, the system explicitly declares its own unreliability.  

Stars remain low. R values are marked as reference-only.

This is Fail-Closed applied to the system's knowledge state:  

**"I cannot certify this judgment. Do not rely on it yet."**

Most safety systems do not make this declaration.  

They output numbers with false precision regardless of data quality.  

NRA-IDE treats epistemic uncertainty as a first-class structural condition.

### 5. Human authority is structurally enforced / 人間権限の構造的保証

FAIL-CLOSED cannot be exited by the system.  

Recovery requires `✚ 医師介入` — a human decision.

This is not a UI restriction. It is a structural statement:  

**The authority to declare a system safe belongs exclusively to the human operator.**  

Effect-Side recovery (the waveform returning to normal) does not constitute Cause-Side confirmation.

---

## Applicable Range / 適用範囲

| Context | NRA-IDE Applicable | Reason |

|---|---|---|

| New patient, first contact | ✗ No | No baseline. τ not established. |

| Emergency arrival (first 15 min) | ✗ Limited | Warmup phase. Reference only. |

| Intraoperative monitoring (after start) | ✓ Yes | δ accumulates from incision. τ established progressively. |

| ICU continuous monitoring | ✓ Yes | Hours of history. Highest structural reliability. |

| Post-op recovery room | ✓ Yes | Transition from intraoperative baseline. |

| Chronic disease outpatient follow-up | ✓ Yes | Long history. residual_debt highly meaningful. |

**This table is an honest declaration, not a limitation to hide.**  

The strength of NRA-IDE is precisely where elapsed history exists.

---

## Formula Reference / 数式参照

$$R_i = \frac{\delta_i}{\tau_i}, \quad i \in \{HR, SpO_2, RR, BP\}$$

$$R_{total} = \sqrt{\sum_i R_i^2}$$

$$\text{residual\_debt}(t) = \int_0^t (R_{total} - R_{total} \cdot k_{rec}) \, dt \cdot w_f$$

$$w_f = \frac{\text{warmupPct}}{100} \quad \text{(accuracy weight)}$$

$$R_{eff} = R_{total} + 0.4 \cdot \text{residual\_debt}$$

$$R_{eff} \geq 1.0 \Rightarrow \text{FAIL-CLOSED}$$

---

## Relation to NRA-IDE Layer Structure / NRA-IDEレイヤーとの対応

| Layer | This Demo |

|---|---|

| Layer 1 — Basic R = δ/τ | Per-channel R computation |

| Layer 3 — Dynamic τ | τ established progressively from baseline history |

| Layer 4 — Sensor Fusion | R_total = √ΣR² multi-channel composition |

Demo #15 operates at **Layer 3–4**, with explicit modeling of the warmup phase as a structural precondition.

---

*NRA-IDE Project — ©M-Tokuni*  

*https://github.com/M-Tokun/NRA-IDE*  

*https://x.com/m_tokuni*  

*README_Demo15_OR_ICU_26-0321.md*
