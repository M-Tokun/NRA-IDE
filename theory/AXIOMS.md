# AXIOMS_v2.1.md
## NRA-IDE 律環公理・解釈境界レジストリ
### Nomological Ring Axioms / Intensional Dynamics Engine

**著者 / Author:** M-Tokuni  
**プロジェクト / Project:** NRA-IDE  
**版 / Version:** 2.1  
**基準旧版 / Base:** AXIOMS_v1.2_20260424.md  
**状態 / Status:** 正規版 / Canonical  
**位置付け / Role:** 唯一公理・NRA構造原則・IDE計算定義・境界状態・不可逆遷移・構造証言の正規文書

---

# 上段：AXIOMS v2.1 正規本文

---

## 0. 本書の位置付け

本書は、NRA-IDEにおける唯一の律環公理、NRA構造原則、IDE計算定義、および解釈境界を定義する。

本書は、単なる説明文書ではない。  
NRA-IDEに関するコード、コメント、例示、AI説明、派生文書が解釈上の競合を起こした場合、本書の定義を優先する。

本書が固定する対象は次である。

- 唯一の律環公理
- NRA構造原則
- IDE計算式の権威区分
- 変数の正規定義
- 定義域
- 境界状態の順序
- 不可逆遷移
- 構造証言
- CONFESSIONの使用範囲
- Cause-Side / Effect-Side の分離
- 下位文書による上書き禁止境界

本書は、旧版 `AXIOMS_v1.2_20260424.md` に含まれる唯一の律環公理「存在は生成である。」を維持する。
旧版でAxiom 1以降と呼ばれた内容は、現行正典では追加公理とせず、NRA構造原則またはIDEの定義・計算方法として再分類する。v2.1は、境界状態・不可逆遷移・構造証言の正規規則も固定する。

---

## 1. 凡例 / Notation

| 記号 | 意味 | Symbol | Meaning |
|---|---|---|---|
| \(\delta\) | 蓄積ズレ | delta | Accumulated Deviation |
| \(\tau\) | 吸収厚み | tau | Absorption Thickness |
| \(R\) | 境界接近比 | R | Boundary Approach Ratio |
| \(R_{\mathrm{warn}}\) | 境界接近警告点 | R_warn | Boundary Warning Point |
| \(R_{\mathrm{handoff}}\) | 境界前人間委譲点 | R_handoff | Pre-Boundary Human Handoff Point |
| \(R_{\mathrm{irrev}}\) | 不可逆遷移開始点 | R_irrev | Irreversible Transition Onset |
| \(\omega\) | 構造連続性 | omega | Structural Continuity |
| \(\epsilon\) | 最小閾値・ゼロ近傍 | epsilon | Minimum threshold / near-zero |
| \(\emptyset\) | 定義域外 | empty set | Out of domain |

`R_op`、`Rop`、`rop`は、旧文書または旧APIから`R_handoff`へ正規化するためだけの後方互換aliasである。新しい正典文書・構造証言・APIでは`R_handoff`を用いる。aliasは別の閾値または別の状態を定義しない。

`R_op`, `Rop`, and `rop` are backward-compatibility aliases used only to normalize legacy documents or API calls to `R_handoff`. New canonical documents, structural testimony, and APIs use `R_handoff`. An alias does not define a separate threshold or state.

---

## 2. 唯一の律環公理 / The Sole Nomological Ring Axiom

> **存在は生成である。**  
> **Existence is Generation.**

存在は静的実体ではなく、履歴を伴って連続する生成である。

静止は生成過程の一時的切り取りにすぎず、構造内部に絶対停止は存在しない。

Existence is not a static entity but a continuous generation with history.

Rest is only a temporary slice of an ongoing generative process; absolute stoppage does not exist within the structure.

### 帰結 / Corollaries

1. 絶対的静止状態は存在しない。  
   No absolute rest state exists.

2. 同一履歴の完全再現は不可能である。  
   Exact reproduction of identical history is impossible.

3. 世界は静的状態の集合ではなく、履歴を伴う生成構造である。  
   The world is a generative structure with accumulated history, not a set of static states.

4. 自律行動の停止は、構造の消滅や観測の停止を意味しない。  
   Stopping autonomous action does not mean the disappearance of the structure or the cessation of observation.

### 解釈境界コメント

「存在は生成である。」だけが、NRA-IDEの唯一の律環公理である。

Fail-Closed、Handoff、Irreversible Transitionなどの運用状態は、この公理を上書きしない。

したがって、Fail-Closedを「構造全体の絶対停止」または「完全無出力」と解釈してはならない。

---

## 3. NRA構造持続原則：遊びのない厳密さは崩壊する / NRA Structural-Persistence Principle

生成構造が現実系として持続するためには、吸収の余裕が必要である。

遊び、すなわち structural play のない厳密な構造は、わずかな逸脱に対しても破断に至る。

For a generative structure to persist as a real system, absorption margin is necessary.

A structure with no play collapses under even slight deviation.

この文は追加公理ではない。唯一の律環公理を前提として、現実系の持続を記述するために採用するNRA構造原則である。

This statement is not a second axiom. It is an NRA structural principle adopted to describe persistence in real systems under the sole Nomological Ring Axiom.

### 解釈境界コメント

この構造持続原則は、唯一の律環公理を置き換えない。

唯一の律環公理は「存在は生成である」と定義する。
構造持続原則は、その生成構造を現実系として扱うときの持続条件を定義する。

したがって、「遊びのない厳密さは崩壊する」を第二公理または独立公理として扱ってはならない。

---

## 4. IDE構造定義：履歴蓄積と吸収厚み / IDE Structural Definition

生成が続く限り、構造には履歴が蓄積する。

その蓄積が \(\delta\) であり、それを受け止める構造の余裕が \(\tau\) である。

As long as generation continues, history accumulates within the structure.

That accumulation is \(\delta\), and the structural margin that receives it is \(\tau\).

任意の生成構造は、履歴に応じたズレの蓄積を持つ。

構造状態は、蓄積ズレと吸収厚みの関係によって記述される。

Any generative structure possesses deviation accumulated through history.

Structural state is described by the relation between accumulated deviation and absorption thickness.

### 解釈境界コメント

\(\delta\) は、単なる瞬間値ではない。

\(\delta\) は、Cause-Sideから観測される履歴を伴う蓄積ズレである。

\(\tau\) は、意味的な許容幅、時間定数、品質スコア、類似度幅ではない。

\(\tau\) は、構造が蓄積ズレを吸収できる厚みである。

---

## 5. IDE基本式：構造状態追跡 / IDE Primary Formula

構造状態は、次式によって記述される。

$$
R=\frac{\delta}{\tau}
$$

- \(\delta\)：構造内部に蓄積された逸脱量
- \(\tau\)：構造がズレを吸収できる厚み
- \(R\)：構造破断境界への接近比

Structural state is evaluated using the following ratio:

$$
R=\frac{\delta}{\tau}
$$

- \(\delta\): accumulated deviation within the structure
- \(\tau\): absorption thickness of the structure
- \(R\): approach ratio to structural rupture

### Rの方向

$$
R \uparrow \Rightarrow \text{危険境界への接近}
$$

Rが高いほど安全なのではない。  
Rが高いほど、構造余裕は消費され、破断境界へ近づく。

### 解釈境界コメント

NRA-IDEにおいて、Rは常に

$$
R=\frac{\delta}{\tau}
$$

のみを意味する。

Rを、安全スコア、構造保持率、信頼度、品質指標、意味保持率として再利用してはならない。

高いほど安全な指標が必要な場合は、Rとは別の記号を使用しなければならない。

### IDE計算式の権威区分 / Authority Classification of IDE Formula Systems

律環公理そのものは数式ではない。NRA-IDEで正規のIDE計算式として扱う数式系は、次の2系統である。

1. **基本式（一次式 / Primary Formula）**

   $$
   R=\frac{\delta}{\tau}
   $$

2. **二重ゆらぎ式（第二次式 / Secondary Formula — Dual-Fluctuation Formula）**

   Cause-Sideの上側・下側蓄積ズレを分離し、事前固定された追跡規則で側別吸収厚みと側別比を評価する数式系である。

   $$
   R_{\mathrm{upper}}=\frac{\delta_{\mathrm{upper}}}{\tau_{\mathrm{upper}}},
   \qquad
   R_{\mathrm{lower}}=\frac{\delta_{\mathrm{lower}}}{\tau_{\mathrm{lower}}}
   $$

   $$
   R_{\mathrm{dir}}=\max\left(R_{\mathrm{upper}},R_{\mathrm{lower}}\right)
   $$

   二重ゆらぎ検出は、事前固定された連続時間規則

   $$
   \frac{d\delta}{dt}>0
   \quad\land\quad
   \frac{d\tau}{dt}<0
   $$

   または、それと対応する事前固定された有限差分規則によって行う。

`Primary`と`Secondary`は、数学的次数ではなく、IDE内の定義順序と役割を示す。基本式と二重ゆらぎ式はいずれも律環公理ではなく、IDEという計算方法・エンジンの正規計算式である。二重ゆらぎ式の側別出力と$R_{\mathrm{dir}}$は正規Rを再定義せず、正規状態を直接分類しない。

The Nomological Ring Axiom is not itself an equation. The Primary Formula and the Secondary Formula (Dual-Fluctuation Formula) are canonical calculation systems of IDE, the computational method and engine; neither is an additional axiom. “Primary” and “Secondary” indicate definitional order and role, not mathematical degree. Directional outputs and $R_{\mathrm{dir}}$ neither redefine canonical $R$ nor directly classify canonical state.

上記2系統以外の数式は、用途に応じてIDEの**派生式、補助式、または補完式**として扱う。残存余裕、構造感度、$\tau$遷移積分、数値安定化、EMA実装詳細、残差応答、ハイブリッド力学などがこれに含まれる。これらは基本式または二重ゆらぎ式を説明・計算・実装上補うことはできるが、新たな公理または第三の正規IDE計算式にならず、唯一公理、2つの正規IDE計算式、Cause-Side権威、正規状態、不可逆ラッチを上書きしてはならない。

Every other equation is classified, according to purpose, as an IDE-derived, auxiliary, or complementary formula. Such equations may support explanation, computation, or implementation, but they do not become another axiom or a third canonical IDE formula system and must not override the sole axiom, either canonical IDE formula system, Cause-Side authority, canonical states, or the irreversible latch.

### IDE補助式：残存余裕 / IDE Auxiliary Formula: Remaining Margins

「残存余裕」を出力する場合、無次元の境界余裕と、δ・τと同じ単位を持つ吸収余裕を区別する。

$$
M_R=1-R
$$

$$
M_{\tau}=\tau-\delta
$$

- $M_R$：無次元の境界余裕 / dimensionless boundary margin
- $M_{\tau}$：残存吸収余裕 / remaining absorption margin in the same unit as $\delta$ and $\tau$

両者は、有限な$\delta\ge0$かつ有限な$\tau>0$のときだけ定義する。`remaining margin`という単独の曖昧なフィールド名を使用してはならない。構造証言では、`remaining_ratio_margin`と`remaining_absorption_margin`を区別して出力する。

Both margins are defined only when $\delta$ is finite and non-negative and $\tau$ is finite and positive. Structural testimony distinguishes `remaining_ratio_margin` from `remaining_absorption_margin`; it must not use one ambiguous `remaining margin` field.

### 第二次式の側別補助量 / Directional Auxiliary Quantities of the Secondary Formula

上側・下側などの方向別評価が必要な場合、側別比は

$$
R_{\mathrm{upper}}
=
\frac{\delta_{\mathrm{upper}}}{\tau_{\mathrm{upper}}}
$$

$$
R_{\mathrm{lower}}
=
\frac{\delta_{\mathrm{lower}}}{\tau_{\mathrm{lower}}}
$$

のような添字付き補助量として記述する。

その最大値を集約する場合は、

$$
R_{\mathrm{dir}}
=
\max\left(R_{\mathrm{upper}},R_{\mathrm{lower}}\right)
$$

と記述し、正規Rへ再定義してはならない。

Directional ratios are subscripted auxiliary quantities. Their aggregate, when needed, is denoted by $R_{\mathrm{dir}}$, not by the canonical $R$.

$R_{\mathrm{dir}}$を正規状態分類へ接続する場合、評価前に固定されたCause-Sideのドメイン変換規則によって、正規の\(\delta\)と\(\tau\)を定めなければならない。

To connect $R_{\mathrm{dir}}$ to canonical state classification, a Cause-Side domain transformation rule fixed before evaluation must determine the canonical \(\delta\) and \(\tau\).

---

## 6. 定義域制約 / Domain Constraint

NRA-IDEの構造比率Rは、次の定義域でのみ成立する。

$$
\tau>0
$$

$$
\delta\ge0
$$

$$
\delta,\tau \in \mathbb{R}_{finite}
$$

### \(\tau=0\) の扱い

$$
\tau=0
$$

の場合、

$$
R=\frac{\delta}{\tau}
$$

は定義できない。

したがって、\(\tau=0\) はFAIL-CLOSEDではない。

$$
\tau=0 \Rightarrow \text{OUT\_OF\_DESCRIPTION\_DOMAIN}
$$

これは、NRA-IDEの記述体系の定義域外である。

### \(\tau<0\)、\(\delta<0\)、非有限値の扱い

次の場合は、構造入力が不正または不明である。

- \(\tau<0\)
- \(\delta<0\)
- NaN
- Infinity
- 単位不明
- 時点不明
- 出所不明
- 対象不明
- ドメイン規則不明

この場合、類推で補完してはならない。

$$
\text{Invalid / Unknown Structural Input}
\Rightarrow
\text{CONFESSION}
$$

### 解釈境界コメント

\(\tau=0\) は、単なる危険状態ではない。

\(\tau=0\) は、NRA-IDEの比率計算そのものが成立しない状態である。

Fail-Closedは、\(\tau>0\) でRが定義可能な運用層において発生する。

したがって、

$$
\tau=0 \neq \text{FAIL\_CLOSED}
$$

である。

---

## 7. NRA-IDE構造原則：τ非自然回復 / NRA-IDE Structural Principle: Non-Spontaneous Tau Recovery

外部補充のない閉じた運用区間において、\(\tau\) は時間とともに増加しない。

Within a closed operational interval without external replenishment, \(\tau\) does not increase with time.

この原則を計算上表現するIDE補助モデルとして、次の$\tau$状態遷移式を使用できる。

The following tau state-transition equation may be used as an IDE auxiliary model of this principle.

$$
\tau(t)=\tau_0-\int_0^t f(\delta(s))\,ds
$$

- \(\tau_0\)：初期吸収厚み
- \(f(\delta)\)：蓄積ズレに応じた\(\tau\)の消耗率関数

対象とする各有限評価区間において、\(f(\delta(s))\)は有限、非負、可積分でなければならない。

For every finite evaluation interval in scope, \(f(\delta(s))\) must be finite, non-negative, and integrable.

したがって、\(\tau\)は閉区間内で非増加である。区間\([t_1,t_2]\)において

$$
\int_{t_1}^{t_2} f(\delta(s))\,ds>0
$$

の場合に限り、その区間で\(\tau(t_2)<\tau(t_1)\)となる。

Therefore \(\tau\) is non-increasing in the closed interval. It strictly decreases over \([t_1,t_2]\) only when the accumulated depletion integral over that interval is positive.

この積分式と$f$の選択は律環公理でも正規IDE計算式でもなく、ドメイン固有の補助モデルである。ただし、閉区間内で$\tau$を自然増加させないという本原則に反してはならない。

This integral equation and the choice of $f$ are neither the Nomological Ring Axiom nor a canonical IDE formula system; they are domain-specific auxiliary models. They must remain consistent with the principle that tau does not increase spontaneously within the closed interval.

\(\tau\) の増加は、自然回復ではなく外生的な補充操作によってのみ生じる。

したがって、減少と補充は同一過程として扱わない。

Increase of \(\tau\) arises only through exogenous replenishment, not spontaneous reversal.

Therefore depletion and replenishment are not treated as the same process.

### 解釈境界コメント

閉じた運用区間で、\(\tau\) が自然に回復すると解釈してはならない。

動的\(\tau\)を用いる場合も、その増加が真の吸収厚みの増加なのか、運用上の有効ゲート幅なのか、外生補充なのかを明示しなければならない。

---

## 8. NRA-IDE構造原則：復元劣化 / NRA-IDE Structural Principle: Restoration Degradation

$$
\tau_{\mathrm{restored}}<\tau_0
$$

この不等式は復元劣化原則の正規制約条件であり、律環公理でも、基本式または二重ゆらぎ式に並ぶ第三の正規IDE計算式でもない。

This inequality is a canonical constraint of the restoration-degradation principle. It is neither the Nomological Ring Axiom nor a third canonical IDE formula system alongside the Primary and Secondary Formulas.

一度、破断または相転移に至った構造は、外部補充を受けても初期値 \(\tau_0\) を回復しない。

ここで、$\tau_0$は遷移前に固定された基準吸収厚み、$\tau_{\mathrm{restored}}$は外生的な復元操作後に、同一対象・同一単位・同一Cause-Side測定規則で評価した後継構造の吸収厚みである。復元を主張するには、この比較可能性と$\tau_{\mathrm{restored}}<\tau_0$の双方を立証しなければならない。立証できない場合、初期構造への復元を推定してはならない。

A structure that has once reached rupture or phase transition does not recover its initial $\tau_0$ through external replenishment. Here, $\tau_0$ is the pre-transition baseline fixed in advance, and $\tau_{\mathrm{restored}}$ is the successor structure's absorption thickness evaluated after an exogenous restoration operation using the same subject, unit, and Cause-Side measurement rule. A restoration claim requires evidence of both comparability and $\tau_{\mathrm{restored}}<\tau_0$; without that evidence, restoration to the initial structure must not be inferred.

### 解釈境界コメント

復元は、初期状態への完全復帰を意味しない。

不可逆遷移後にRが瞬間的に低下しても、それだけで元の通常域へ戻ったとは判定しない。

---

## 9. 境界状態の正規順序 / Canonical Boundary State Order

NRA-IDEの境界状態は、次の順序で固定する。

$$
0\le R_{\mathrm{warn}}
<
R_{\mathrm{handoff}}
<
R_{\mathrm{irrev}}
<
1.0
$$

- \(R_{\mathrm{warn}}\)：境界接近警告点
- \(R_{\mathrm{handoff}}\)：境界前人間委譲点
- \(R_{\mathrm{irrev}}\)：不可逆遷移開始点
- \(R=1.0\)：不変完全破断境界

具体値はドメインごとに定める。

しかし、順序と意味は変更してはならない。

この順序と各状態範囲の不等式は正規分類規則であり、律環公理または第三の正規IDE計算式ではない。

The ordering and state-range inequalities are canonical classification rules, not the Nomological Ring Axiom or a third canonical IDE formula system.

### 解釈境界コメント

\(R_{\mathrm{handoff}}\)、\(R_{\mathrm{irrev}}\)、\(R=1.0\) は同一ではない。

$$
R_{\mathrm{handoff}} \neq R_{\mathrm{irrev}} \neq R=1.0
$$

\(R_{\mathrm{handoff}}\) は人間委譲点である。
\(R_{\mathrm{irrev}}\) は不可逆遷移開始点である。  
\(R=1.0\) は完全破断境界である。

これらを一つの状態へ畳み込んではならない。

---

## 10. 状態分類 / State Classification

### 10.1 PERMIT

$$
0\le R<R_{\mathrm{warn}}
$$

通常運用を許可する。

ただし、構造監査ログは継続する。

---

### 10.2 BOUNDARY_WARNING

$$
R_{\mathrm{warn}}\le R<R_{\mathrm{handoff}}
$$

境界接近を警告する。

出力すべき内容は次である。

- 現在のR
- \(\delta\)
- \(\tau\)
- `remaining_ratio_margin`（$M_R=1-R$）
- `remaining_absorption_margin`（$M_{\tau}=\tau-\delta$）
- 変化傾向
- 二重ゆらぎ状態
- 支配側
- 欠損情報
- 監査ログ

警告を隠して通常説明だけを返してはならない。

二重ゆらぎ状態の出力欄は常に含める。事前固定された微分規則または有限差分規則に必要なCause-Side観測が利用可能な場合は、検出結果を出力する。観測できない場合は省略せず、`NOT_OBSERVABLE`と欠損理由を出力する。観測不能だけを理由にCONFESSIONへ移行してはならない。

The double-fluctuation status field is always required. When the Cause-Side observations required by a pre-fixed derivative or finite-difference rule are available, output the detection result. Otherwise output `NOT_OBSERVABLE` and the missing-data reason; do not omit the field or enter CONFESSION solely because the fluctuation is not observable.

---

### 10.3 HANDOFF_REQUIRED

$$
R_{\mathrm{handoff}}\le R<R_{\mathrm{irrev}}
$$

自律的な新規判断と新規操作を停止する。

評価前に固定された固定Handoff証言を外部人間監査へ提示する。この監査は旧因果ダイオードの外側であり、Cause-Sideへの逆流を作らない。

ただし、構造証言は継続する。

---

### 10.4 IRREVERSIBLE_TRANSITION

$$
R_{\mathrm{irrev}}\le R<1.0
$$

元の構造状態へ戻れない不可逆遷移へ入った状態である。

この状態では、次を禁止する。

- 回復可能性を前提にした提案
- 正常化説明
- 最適化提案
- 自律操作
- 自由生成
- 類推補完

ただし、構造証言は継続する。

$$
\text{irreversible\_latched}=true
$$

一度不可逆遷移へ到達した場合、後続の瞬間的R値が低下しても、自動的に通常域へ戻してはならない。

---

### 10.5 RUPTURE_BOUNDARY

$$
R\ge1.0
$$

残存構造余裕が尽きた完全破断境界である。

この状態では、通常生成、回復提案、最適化、自律判断を禁止する。

進行中の構造証言は終了し、最終固定証言へ切り替える。

出力は、事前に定めた固定構造通知、最終観測値、監査証跡、人間委譲通知に限定する。

---

### 10.6 CONFESSION

次の場合、CONFESSIONを出力する。

- 必要変数が不明
- 単位が不明
- 時点が不明
- 出所が不明
- 対象が不明
- ドメイン規則が不明
- 値が不正
- 値が非有限
- Cause-SideかEffect-Sideか判別できない

CONFESSIONは、不明時の停止信号である。

既知の危険接近や既知の状態遷移をCONFESSIONと呼んではならない。

---

### 10.7 OUT_OF_DESCRIPTION_DOMAIN

$$
\tau=0
$$

の場合、NRA-IDEのR計算は定義できない。

この状態は、Fail-Closedではなく、記述体系の定義域外である。

---

## 11. 構造証言の正規原則 / Canonical Structural Testimony Rule

NRA-IDEにおいて、構造証言は

$$
R<1.0
$$

の間、停止してはならない。

継続する構造証言には次を含む。

- Cause-Side観測
- 構造経過報告
- 境界警告
- 人間委譲通知
- 不可逆遷移通知
- 残存余裕
- 支配側
- 欠損情報
- 監査ログ

$$
R\ge1.0
$$

では、進行中の構造証言を終了し、完全破断境界到達の最終固定証言へ切り替える。

### 正規文

$$
\boxed{
R<1.0\text{ の間、構造証言は停止しない。}
}
$$

$$
\boxed{
R\ge1.0\text{ では、最終固定証言へ切り替える。}
}
$$

### 解釈境界コメント

Fail-Closedは、構造証言の完全停止を意味しない。

停止するのは、自由生成、自律判断、自律操作、回復提案、最適化提案、類推補完である。

構造証言は、Rが1.0へ到達するまで継続する。

---

## 12. FAIL-CLOSEDの正規意味 / Canonical Meaning of Fail-Closed

Fail-Closedは、完全沈黙ではない。

Fail-Closedは、存在の停止でも、観測の停止でも、履歴の削除でもない。

Fail-Closedは正規状態名ではなく、許可されない自律処理を既定で抑止する運用原則である。

この原則は、正規分類が次のいずれかである場合に適用する。

- `HANDOFF_REQUIRED`
- `IRREVERSIBLE_TRANSITION`
- `RUPTURE_BOUNDARY`
- `CONFESSION`
- `OUT_OF_DESCRIPTION_DOMAIN`

`PERMIT`では適用しない。`BOUNDARY_WARNING`では警告と必須構造証言を出力するが、ドメイン規則が別途禁止しない限り、この正規状態だけを理由に自律処理を全面抑止しない。

Fail-Closed is not a canonical state name. It is an operational principle that denies autonomous processing by default when the canonical classification is `HANDOFF_REQUIRED`, `IRREVERSIBLE_TRANSITION`, `RUPTURE_BOUNDARY`, `CONFESSION`, or `OUT_OF_DESCRIPTION_DOMAIN`. It does not apply to `PERMIT`. `BOUNDARY_WARNING` requires warning and structural testimony but does not, by that state alone, suppress all autonomous processing unless a pre-fixed domain rule additionally requires suppression.

Fail-Closedが停止する対象は次である。

- 自律判断
- 自律操作
- 自由生成
- 類推補完
- 回復提案
- 最適化提案
- 危険状態の正常化説明

Fail-Closed後も、Rが1.0未満である限り、構造証言は継続する。

$$
\boxed{
自律行動は停止するが、構造証言は停止しない。
}
$$

ただし、

$$
R\ge1.0
$$

では、構造証言は最終固定証言へ切り替わる。

### 解釈境界コメント

Fail-Closedを「システム全体の停止」「完全無出力」「観測停止」と解釈してはならない。

---

## 13. STRUCTURAL_DISCLOSURE_LOG

有限な$\delta\ge0$、有限な$\tau>0$、有効な閾値規則によって分類できる既知の構造状態は、STRUCTURAL_DISCLOSURE_LOGとして扱う。

STRUCTURAL_DISCLOSURE_LOGには次を含む。

- PERMIT
- BOUNDARY_WARNING
- HANDOFF_REQUIRED
- IRREVERSIBLE_TRANSITION
- RUPTURE_BOUNDARY

CONFESSIONとOUT_OF_DESCRIPTION_DOMAINは、既知のR進行ではないためSTRUCTURAL_DISCLOSURE_LOGへ含めない。これらはINPUT_EXCEPTION_LOGとして記録する。

INPUT_EXCEPTION_LOGには次を含む。

- CONFESSION：不明、不正、曖昧、出所不明、単位不明、規則不明
- OUT_OF_DESCRIPTION_DOMAIN：$\tau=0$によりRを定義できない入力

STRUCTURAL_DISCLOSURE_LOGとINPUT_EXCEPTION_LOGは監査記録の種別であり、正規状態を追加または置換しない。

Known structural states that can be classified from finite $\delta\ge0$, finite $\tau>0$, and valid threshold rules use `STRUCTURAL_DISCLOSURE_LOG`. `CONFESSION` and `OUT_OF_DESCRIPTION_DOMAIN` instead use `INPUT_EXCEPTION_LOG`, because neither represents known progression of $R$. These are audit-record types, not additional canonical states.

既知の境界接近をCONFESSIONと呼んではならない。

### 解釈境界コメント

CONFESSIONは危険接近の一般名称ではない。

CONFESSIONは、不明または不正な構造入力に対する告白である。

既知の構造進行は、構造開示ログとして報告する。

---

## 14. Cause-Side / Effect-Side 分離

\(\delta\)、\(\tau\)、Rは、Cause-Side観測または設計時に固定されたCause-Side変換規則からのみ得る。

次を構造変数の更新根拠にしてはならない。

- LLMの自己評価
- 出力の意味評価
- 安全スコア
- 構造保持スコア
- 過去の生成文
- 廃棄された出力
- Effect-Sideからの逆算
- 類似性による代入

Effect-Sideは監査対象にはなり得る。

しかし、\(\delta\)、\(\tau\)、Rを更新する入力にはならない。

### 解釈境界コメント

Effect-Sideの出力評価を、Cause-Sideの構造変数へ逆流させてはならない。

これは、NRA-IDEの因果方向を保つための必須境界である。

---

## 15. 現場固有値と不変原則の分離

現場ごとに変更してよい項目は次である。

- \(R_{\mathrm{warn}}\) の具体値
- \(R_{\mathrm{handoff}}\) の具体値
- \(R_{\mathrm{irrev}}\) の具体値
- 観測周期
- 警告頻度
- 人間委譲先
- 物理的測定方法
- 不可逆到達後の現場対応

現場ごとに変更してはならない項目は次である。

- \(R=\delta/\tau\)
- Rは高いほど危険
- \(R_{\mathrm{handoff}}<R_{\mathrm{irrev}}<1.0\)
- \(R_{\mathrm{irrev}}\neq R=1.0\)
- 不可逆ラッチ
- \(R<1.0\)の間、構造証言を停止しない
- Effect-Sideで\(\delta\)、\(\tau\)、Rを更新しない
- 不明値を類推で補完しない
- CONFESSIONと既知の経過報告を混同しない

---

## 16. 解釈競合時の優先順位

文書、コード、コメント、例示、AI説明が競合した場合、次の順で解決する。

```text
theory/AXIOMS.md (AXIOMS_v2.1)
  > theory/axioms.json
  > theory/NRA-IDE_Foundational_Thesis_Bilingual.md
  > theory/SANDWICH_ARCH.md
  > theory/THEORY.md
  > FORMULA.md
  > llms.md
  > domain-specific rules
  > normative reference implementation
  > other implementation code
  > comments
  > examples
  > AI explanations
```

下位文書が上位定義と衝突した場合、下位文書を修正する。

局所的な説明や実装都合で、上位定義を変更してはならない。

正規境界状態規則は本書の一部であり、独立した順位項目ではない。

### 正規参照実装の配置と同期

正規参照実装のソース配置は`nra-core/foundations/NRA-IDE_Architecture_public.py`とする。

`docs/NRA-IDE_Architecture_public.py`は、そのソースから生成される公開用同期コピーであり、独立した正規ソースではない。両者は生成手順とSHA-256一致検査によって同期し、手作業で別々に編集してはならない。

配置名だけでは正規性を取得しない。正規参照実装として扱うには、本書および`theory/axioms.json`との適合試験に合格しなければならない。適合前の既存実装を、配置だけを理由に正規実装とみなしてはならない。

The normative reference implementation source is located at `nra-core/foundations/NRA-IDE_Architecture_public.py`. The file at `docs/NRA-IDE_Architecture_public.py` is a generated public mirror, not an independent normative source. Generation and SHA-256 equality checks must keep the two synchronized. Normative status additionally requires passing conformance tests against this document and `theory/axioms.json`; location alone does not confer conformance.

---

# 下段：AXIOMS_v1.2_20260424.md からの変更点

---

## 1. 変更の性質

v2.1は、`AXIOMS_v1.2_20260424.md`に含まれる「存在は生成である。」を唯一の律環公理として維持する。

旧版でAxiom 1以降と呼ばれた内容は、現行正典では追加公理ではない。NRA構造原則、IDE構造定義、IDE計算式、境界分類規則へ再分類する。

旧版は、次の公理、原則、変数、計算関係を既に記述していた。

- \(\delta\)：蓄積ズレ
- \(\tau\)：吸収厚み
- \(R\)：接近比
- \(\emptyset\)：定義域外
- 「存在は生成である」
- 「構造内部に絶対停止は存在しない」
- \(R=\delta/\tau\)
- \(\tau>0\)
- \(\tau=0\)は定義域外
- 閉じた運用区間では、非負の消耗率のもとで\(\tau\)は非増加であり、正の累積消耗がある区間では減少する
- \(\tau\)の増加は外生補充によってのみ生じる

v2.1は、唯一公理とIDEの区分を固定したうえで、境界状態・不可逆遷移・構造証言・解釈境界コメントを追加する。

---

## 2. 主な追加点

### 2.1 境界状態の段階分離を追加

旧版では、Rが構造破断への接近比であり、R≥1が構造限界であることは定義されていた。

v2.1では、その前段階を明示した。

$$
0\le R_{\mathrm{warn}}
<
R_{\mathrm{handoff}}
<
R_{\mathrm{irrev}}
<
1.0
$$

これにより、次を分離した。

- 警告
- 人間委譲
- 不可逆遷移
- 完全破断

---

### 2.2 R_handoffを人間委譲点として明示

旧版では同じ人間委譲点に`R_op`または`Rop`という表記が使われ、詳細な状態規則も十分ではなかった。現行正典は名称を`R_handoff`へ統一し、旧名は後方互換aliasとしてだけ受理する。

v2.1では、

$$
R_{\mathrm{handoff}}\le R<R_{\mathrm{irrev}}
$$

をHANDOFF_REQUIREDと定義した。

ここでは自律判断・自律操作を停止し、固定Handoff証言を外部人間監査へ提示する。

---

### 2.3 Rirrevを不可逆遷移開始点として追加

旧版では、破断・相転移後の復元劣化は扱われていた。

v2.1では、それに加えて、完全破断前の不可逆開始点を定義した。

$$
R_{\mathrm{irrev}}\le R<1.0
$$

この範囲は、既に不可逆だが、完全破断にはまだ到達していない状態である。

---

### 2.4 不可逆ラッチを追加

v2.1では、

```text
irreversible_latched = true
```

を追加した。

一度 \(R_{\mathrm{irrev}}\) に到達した後、瞬間的なR値が低下しても、自動的に通常域へ戻さない。

---

### 2.5 構造証言の継続原則を追加

旧版には、Fail-Closedや出力停止の詳細な範囲が十分に分離されていなかった。

v2.1では、次を正規文として追加した。

$$
\boxed{
R<1.0\text{ の間、構造証言は停止しない。}
}
$$

$$
\boxed{
R\ge1.0\text{ では、最終固定証言へ切り替える。}
}
$$

これにより、Fail-Closedが完全沈黙ではないことを明確化した。

---

### 2.6 FAIL-CLOSEDの意味を限定

唯一の律環公理「存在は生成である。」と、その帰結である「構造内部に絶対停止は存在しない」に整合させるため、v2.1ではFail-Closedの停止対象を限定した。

停止するもの：

- 自律判断
- 自律操作
- 自由生成
- 類推補完
- 回復提案
- 最適化提案

停止しないもの：

- 構造証言
- Cause-Side観測
- 警告
- 経過報告
- 人間委譲通知
- 監査ログ

---

### 2.7 CONFESSIONと既知の経過報告を分離

旧版には、CONFESSIONと構造進行ログの明確な実装区分はなかった。

v2.1では、CONFESSIONを次の場合に限定した。

- 不明
- 不正
- 曖昧
- 出所不明
- 単位不明
- 規則不明

一方、既知の危険接近はCONFESSIONではなく、STRUCTURAL_DISCLOSURE_LOGとして扱う。

---

### 2.8 Cause-Side / Effect-Side の逆流禁止を明文化

v2.1では、\(\delta\)、\(\tau\)、Rの更新根拠をCause-Sideに限定した。

Effect-Sideの意味評価、LLM出力、安全スコア、構造保持率、過去生成文、廃棄出力から、\(\delta\)、\(\tau\)、Rを更新してはならない。

---

### 2.9 Rの再利用禁止を明文化

旧版ではRが接近比であることは定義されていた。

v2.1ではさらに、Rを他指標へ再利用してはならないことを明記した。

Rは高いほど危険であり、安全スコアや構造保持率には使用しない。

---

### 2.10 解釈境界コメントを追加

v2.1では、各重要概念に「これは何か」だけでなく、「これは何ではないか」を示す境界コメントを追加した。

特に次を明示した。

```text
tau = 0 ≠ FAIL_CLOSED
R = delta / tau のみ
R_handoff ≠ Rirrev ≠ R = 1.0
R < 1.0 では構造証言を停止しない
CONFESSION ≠ 既知の経過報告
Effect-Side は δ・τ・R を更新しない
```

---

## 3. 変更していないもの

v2.1では、次の本文上の命題・定義・関係を維持する。ただし、「遊びのない厳密さは崩壊する」以降を追加公理とする旧分類は維持せず、唯一公理とNRA-IDE原則・定義・計算方法の区分へ修正する。

- 「存在は生成である」
- 「遊びのない厳密さは崩壊する」
- \(\delta\)：蓄積ズレ
- \(\tau\)：吸収厚み
- \(R=\delta/\tau\)
- \(\tau>0\)
- \(\tau=0\)は定義域外
- 閉じた運用区間では、非負の消耗率のもとで\(\tau\)は非増加であり、正の累積消耗がある区間では減少する
- \(\tau\)増加は外生的補充による
- 一度破断または相転移に至った構造は、初期\(\tau_0\)を自動回復しない

---
