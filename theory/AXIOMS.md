# AXIOMS_v2.4.md
## NRA-IDE 律環公理・解釈境界レジストリ
### Nomological Ring Axioms / Intensional Dynamics Engine

**著者 / Author:** M-Tokuni  
**プロジェクト / Project:** NRA-IDE  
**版 / Version:** 2.4  
**基準旧版 / Base:** AXIOMS v2.3（v2.3の基準旧版：AXIOMS v2.2）  
**状態 / Status:** 正規版 / Canonical  
**位置付け / Role:** 唯一公理・NRA構造原則・IDE計算定義・境界状態・不可逆遷移・構造証言の正規文書

---

# 上段：AXIOMS v2.4 正規本文

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

蓄積ズレは、評価開始前に固定した基準状態から、宣言した破断方向へ測ったズレである。作用を除けば基準側へ戻る可逆成分と、作用を除いても残る不可逆成分（残留ズレ）とから成る。

基準状態は評価中に付け直さない。基準を動かさずに測ることで、過去の事象が残した残留ズレは現在の蓄積ズレに含まれ続ける。蓄積ズレが履歴を伴うとは、この意味である。基準の再宣言は、評価と評価の間でのみ許す。

Accumulated deviation is the deviation measured from a reference state fixed before evaluation begins, in the direction of the declared rupture. It consists of a reversible component, which returns toward the reference when the action is removed, and an irreversible component (residual deviation), which remains after the action is removed.

The reference state is not reset during an evaluation. Because the reference is not moved, residual deviation left by past events remains contained in the present accumulated deviation. This is what it means for accumulated deviation to carry history. The reference may be redeclared only between evaluations.

### 解釈境界コメント

\(\delta\) は、単なる瞬間値ではない。

\(\delta\) は、Cause-Sideから観測される履歴を伴う蓄積ズレである。

\(\tau\) は、意味的な許容幅、時間定数、品質スコア、類似度幅ではない。

\(\tau\) は、構造が蓄積ズレを吸収できる厚みである。

---

## 4.5 補助構造量：ω・位相・制約・仕事量・エントロピー / Auxiliary Structural Quantities

一次式・二次式を補うために、次の補助構造量を使うことができる。これらは唯一の律環公理、一次式、二次式、Cause-Side権威、正規状態、不可逆ラッチを上書きしない（§5の派生式・補助式・補完式の分類による）。

These auxiliary structural quantities may be used to support the Primary and Secondary Formulas. They do not override the sole axiom, either canonical formula, Cause-Side authority, canonical states, or the irreversible latch (classified as derived, auxiliary, or complementary under §5).

- \(\omega\)：構造連続性。構造が遷移を継続しているかを示す。ドメインが定めた連続観測または位相更新規則の下で継続が確認できるときに限り \(\omega>0\) とする。観測が欠けていることと \(\omega=0\) は同じではない。
- \(\mathrm{Phase}\)：遷移位相。対象構造が遷移のどの段階にあるかを示す内部状態。Cause-Sideに由来する遷移規則で更新する。空間座標でも、モデルが生成した埋め込みでもない。
- \(C\)：制約。対象構造へ外部から加わる負荷・制約。
- \(W\)：仕事量。ドメインが定義・単位・観測方法を明記した場合だけ使う任意量。
- \(\mathrm{entropy}\)：ドメイン固有のエントロピー相当量。ドメインが定義・算出規則を明記した場合だけ使う任意量。構造感度 \(S\)（FORMULA §3）とは別の記号であり、\(S\) をエントロピーの意味で使わない。

\(\omega\) is Structural Continuity, indicating whether the structure continues its transition. \(\omega>0\) holds only when continuity is confirmed under a domain-declared continuous observation or phase-update rule fixed before evaluation. A missing observation is not the same as \(\omega=0\).

\(\mathrm{Phase}\) is an internal state showing which stage of transition the target structure occupies, updated under a Cause-Side-derived rule. It is neither a spatial coordinate nor a model-generated embedding.

\(C\) is Constraint, an external load or constraint acting on the target structure.

\(W\) is Work, an optional domain-specific quantity used only when a domain fixes its definition, unit, and observation method.

\(\mathrm{entropy}\) is an optional domain-specific quantity. It is a symbol distinct from structural sensitivity \(S\) (FORMULA §3); \(S\) must not be reused for entropy.

\(\omega\) 、 \(\mathrm{Phase}\) 、 \(C\) 、 \(W\) 、 \(\mathrm{entropy}\) は、Cause-Side観測または評価前に固定した変換規則からのみ得る（§14）。評価出力（\(R\)、正規状態、不可逆ラッチ、その集約）から得てはならない。

\(\omega\), \(\mathrm{Phase}\), \(C\), \(W\), and \(\mathrm{entropy}\) are obtained only from Cause-Side observation or a transformation rule fixed before evaluation (§14). They must not be obtained from evaluation outputs (\(R\), canonical state, the irreversible latch, or their aggregates).

離散的な遷移で、次の段階へ持ち越さない残差を記録する場合、その残差を \(\mathrm{entropy\_export}\) と呼ぶことができる。これは熱力学的エントロピーの測定値ではなく、構造感度 \(S\) とも別の概念である。

When a discrete transition records a remainder not carried to the next stage, that remainder may be called \(\mathrm{entropy\_export}\). It is not a measurement of thermodynamic entropy and is a concept distinct from structural sensitivity \(S\).

### 解釈境界コメント

これらの補助構造量は、一次式 \(R=\delta/\tau\) を書き換えない。構造証言の補助欄として使う場合も、正規状態を置き換えず、\(R\) を下げず、不可逆ラッチを解除しない。

These auxiliary structural quantities do not rewrite the Primary Formula \(R=\delta/\tau\). When used as auxiliary testimony fields, they do not replace canonical states, lower \(R\), or release the irreversible latch.

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

`Primary`と`Secondary`は、数学的次数ではなく、IDE内の定義順序と役割を示す。基本式と二重ゆらぎ式はいずれも律環公理ではなく、IDEという計算方法・エンジンの正規計算式である。二重ゆらぎ式の側別出力と $R_{\mathrm{dir}}$ は正規Rを再定義せず、正規状態を直接分類しない。

The Nomological Ring Axiom is not itself an equation. The Primary Formula and the Secondary Formula (Dual-Fluctuation Formula) are canonical calculation systems of IDE, the computational method and engine; neither is an additional axiom. “Primary” and “Secondary” indicate definitional order and role, not mathematical degree. Directional outputs and $R_{\mathrm{dir}}$ neither redefine canonical $R$ nor directly classify canonical state.

上記2系統以外の数式は、用途に応じてIDEの**派生式、補助式、または補完式**として扱う。残存余裕、構造感度、 $\tau$ 遷移積分、数値安定化、EMA実装詳細、残差応答、ハイブリッド力学などがこれに含まれる。これらは基本式または二重ゆらぎ式を説明・計算・実装上補うことはできるが、新たな公理または第三の正規IDE計算式にならず、唯一公理、2つの正規IDE計算式、Cause-Side権威、正規状態、不可逆ラッチを上書きしてはならない。

Every other equation is classified, according to purpose, as an IDE-derived, auxiliary, or complementary formula. Such equations may support explanation, computation, or implementation, but they do not become another axiom or a third canonical IDE formula system and must not override the sole axiom, either canonical IDE formula system, Cause-Side authority, canonical states, or the irreversible latch.

### IDE補助式：残存余裕 / IDE Auxiliary Formula: Remaining Margins

「残存余裕」を出力する場合、無次元の境界余裕と、δ・τと同じ単位を持つ吸収余裕を区別する。

$$
M_R=1-R
$$

$$
M_{\tau}=\tau-\delta
$$

- $M_R$ ：無次元の境界余裕 / dimensionless boundary margin
- $M_{\tau}$ ：残存吸収余裕 / remaining absorption margin in the same unit as $\delta$ and $\tau$

両者は、有限な $\delta\ge0$ かつ有限な $\tau>0$ のときだけ定義する。`remaining margin`という単独の曖昧なフィールド名を使用してはならない。構造証言では、`remaining_ratio_margin`と`remaining_absorption_margin`を区別して出力する。

Both margins are defined only when $\delta$ is finite and non-negative and $\tau$ is finite and positive. Structural testimony distinguishes `remaining_ratio_margin` from `remaining_absorption_margin`; it must not use one ambiguous `remaining margin` field.

### 第二次式の側別補助量 / Directional Auxiliary Quantities of the Secondary Formula

上側・下側などの方向別評価が必要な場合、側別比は

$$
R_{\mathrm{upper}} =
\frac{\delta_{\mathrm{upper}}}{\tau_{\mathrm{upper}}}
$$

$$
R_{\mathrm{lower}} =
\frac{\delta_{\mathrm{lower}}}{\tau_{\mathrm{lower}}}
$$

のような添字付き補助量として記述する。

その最大値を集約する場合は、

$$
R_{\mathrm{dir}} =
\max\left(R_{\mathrm{upper}},R_{\mathrm{lower}}\right)
$$

と記述し、正規Rへ再定義してはならない。

Directional ratios are subscripted auxiliary quantities. Their aggregate, when needed, is denoted by $R_{\mathrm{dir}}$, not by the canonical $R$.

$R_{\mathrm{dir}}$ を正規状態分類へ接続する場合、評価前に固定されたCause-Sideのドメイン変換規則によって、正規の\(\delta\)と\(\tau\)を定めなければならない。

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

したがって、\(\tau=0\) はFail-Closedという正規状態ではない。

$\tau=0$ → `OUT_OF_DESCRIPTION_DOMAIN`

これは、NRA-IDEの記述体系の定義域外である。

Thus, \(\tau=0\) is not a canonical state named Fail-Closed. It is classified as `OUT_OF_DESCRIPTION_DOMAIN`.

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

Fail-Closedは正規状態名ではなく、許可されない自律処理を既定で抑止する運用原則である。\(\tau=0\) の正規分類は`OUT_OF_DESCRIPTION_DOMAIN`であり、正規Rを利用できないため、影響する評価にはFail-Closed運用原則を適用する。

Fail-Closed is not a canonical state name but an operational principle that suppresses unauthorized autonomous processing by default. The canonical classification for \(\tau=0\) is `OUT_OF_DESCRIPTION_DOMAIN`; because canonical \(R\) is unavailable, the affected evaluation is subject to the Fail-Closed operational principle.

---

## 7. NRA-IDE構造原則：τ非自然回復 / NRA-IDE Structural Principle: Non-Spontaneous Tau Recovery

構造要素の付加のない閉じた運用区間において、\(\tau\) は時間とともに増加しない。

Within a closed operational interval without the addition of a structural element, \(\tau\) does not increase with time.

この原則を計算上表現するIDE補助モデルとして、次の $\tau$ 状態遷移式を使用できる。

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

この積分式と $f$ の選択は律環公理でも正規IDE計算式でもなく、ドメイン固有の補助モデルである。ただし、閉区間内で $\tau$ を自然増加させないという本原則に反してはならない。

This integral equation and the choice of $f$ are neither the Nomological Ring Axiom nor a canonical IDE formula system; they are domain-specific auxiliary models. They must remain consistent with the principle that tau does not increase spontaneously within the closed interval.

\(\tau\) の増加は、自然回復ではなく、構造要素の付加によってのみ生じる。構造要素の付加とは、評価対象へ新しい構造要素を加えることをいう。付加は既存の構造要素の吸収厚みを回復させるものではない。加えた要素の吸収厚みは、加えた時点のCause-Side測定で定める。既存の構造要素の厚み損失と残留ズレは、付加によって減少しない。既存の要素と加えた要素の厚みを合わせる規則は、評価開始前に固定する。

壊れていない構造要素を計画的に外すこと（構造要素の除去）は劣化ではない。除去は吸収厚みを減らすが、劣化として計上しない。除去した要素を戻す場合は、改めて構造要素の付加として扱う。

したがって、減少と付加は同一過程として扱わない。

Increase of \(\tau\) arises only through the addition of a structural element, not spontaneous reversal. Addition of a structural element means adding a new structural element to the evaluation target. Addition does not restore the absorption thickness of existing structural elements. The absorption thickness of an added element is determined by Cause-Side measurement at the time of addition. Thickness loss and residual deviation of existing structural elements do not decrease through addition. The rule combining the thicknesses of existing and added elements is fixed before evaluation begins.

Planned removal of an undamaged structural element (removal of a structural element) is not degradation. Removal decreases absorption thickness but is not counted as degradation. Returning a removed element is treated anew as the addition of a structural element.

Therefore depletion and addition are not treated as the same process.

蓄積ズレの不可逆成分（残留ズレ）も、評価中に減少しない。時間経過だけで減少してよいのは、蓄積ズレの可逆成分だけである。伸び・曲がりを力で戻す矯正を行った場合は、その評価を終え、評価を宣言し直す。

The irreversible component of accumulated deviation (residual deviation) likewise does not decrease during an evaluation. Only the reversible component of accumulated deviation may decrease with the passage of time alone. If a straightening operation forces a deformation back, that evaluation ends and the evaluation is redeclared.

### 解釈境界コメント

閉じた運用区間で、\(\tau\) が自然に回復すると解釈してはならない。

動的\(\tau\)を用いる場合も、その増減が実効厚みの減少なのか、運用上の有効ゲート幅なのか、構造要素の付加または除去なのかを明示しなければならない。作用や条件による一時的な厚みの減少は、実効厚みから差し引かず、蓄積ズレの可逆成分として数える。新しい観測で宣言厚みが変わる場合は、評価中の増加として扱わず、次の評価スナップショットとして宣言し直す。

---

## 8. NRA-IDE構造原則：復元劣化 / NRA-IDE Structural Principle: Restoration Degradation

$$
\tau_{\mathrm{restored}}<\tau_0
$$

この不等式は復元劣化原則の正規制約条件であり、律環公理でも、基本式または二重ゆらぎ式に並ぶ第三の正規IDE計算式でもない。

This inequality is a canonical constraint of the restoration-degradation principle. It is neither the Nomological Ring Axiom nor a third canonical IDE formula system alongside the Primary and Secondary Formulas.

一度、破断または相転移に至った構造は、構造要素の付加を受けても初期値 \(\tau_0\) を回復しない。

ここで、 $\tau_0$ は遷移前に固定された基準吸収厚み、 $\tau_{\mathrm{restored}}$ は復元を目的とする操作の後に、同一対象・同一単位・同一Cause-Side測定規則で評価した後継構造のうち、構造要素の付加で加えた要素を除く既存の要素の吸収厚みである。復元を主張するには、この比較可能性と $\tau_{\mathrm{restored}}<\tau_0$ の双方を立証しなければならない。立証できない場合、初期構造への復元を推定してはならない。

構造要素の付加によって構成全体の吸収厚みが \(\tau_0\) を上回ることがあっても、それは初期構造への復元ではない。

A structure that has once reached rupture or phase transition does not recover its initial $\tau_0$ through the addition of structural elements. Here, $\tau_0$ is the pre-transition baseline fixed in advance, and $\tau_{\mathrm{restored}}$ is the absorption thickness of the existing elements of the successor structure, excluding elements added by the addition of structural elements, evaluated after an operation intended for restoration using the same subject, unit, and Cause-Side measurement rule. A restoration claim requires evidence of both comparability and $\tau_{\mathrm{restored}}<\tau_0$; without that evidence, restoration to the initial structure must not be inferred.

Even if the addition of structural elements makes the absorption thickness of the whole configuration exceed $\tau_0$, this is not restoration to the initial structure.

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
- `remaining_ratio_margin`（ $M_R=1-R$ ）
- `remaining_absorption_margin`（ $M_{\tau}=\tau-\delta$ ）
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

Handoffによって移るのは、現在の自律実行経路が保持する実行権限だけである。

```text
execution_authority
AUTONOMOUS_CURRENT_PATH
→ EXTERNAL_PREDEFINED
```

Handoffは、責任、法的責任、結果責任、知識、判断の正確性、安全回復、問題解決、または専門家の無謬性の移転を意味しない。構造証言の生成経路、監査ログ経路、および監査ログ保管主体もHandoffだけでは変更しない。

```text
Handoff
→ execution_authority changes
→ structural_testimony_route continues
→ audit_log_route continues
→ audit_log_custody does not change implicitly
```

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
\text{irreversible}\_\text{latched}=true
$$

一度不可逆遷移へ到達した場合、後続の瞬間的R値が低下しても、自動的に通常域へ戻してはならない。

---

### 10.5 RUPTURE_BOUNDARY

$$
R_{\mathrm{target}}\ge1.0
$$

評価前に宣言された対象構造の残存構造余裕が尽きた完全破断境界である。添字を省略した正規Rを用いる場合も、評価対象は事前に一意に宣言されていなければならない。

この状態では、通常生成、回復提案、最適化、自律判断を禁止する。

通常形式の構造証言を終了し、事前定義された破断後固定証言モードへ切り替える。

破断後固定証言は一回限りの終端メッセージではない。生存しているCause-Side観測、記録、通信経路は、それぞれが物理的に利用不能になるまで、事前定義された固定形式で証言を継続する。

```text
target_state = RUPTURE_BOUNDARY
observation_state = ACTIVE
logging_state = ACTIVE
communication_state = ACTIVE
testimony_mode = POST_RUPTURE_FIXED
```

は正当な同時状態である。

対象構造の完全破断は、センサー、ロガー、通信経路、外部監査系の完全破断、Cause-Side観測の終了、監査ログ義務の終了、または完全無出力を自動的には意味しない。

```text
対象構造の完全破断
≠ 観測系の完全破断
≠ 記録系の完全破断
≠ 通信系の完全破断
```

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
R_{\mathrm{target}}\ge1.0
$$

では、通常形式の構造証言を終了し、完全破断境界到達の事前定義された破断後固定証言モードへ切り替える。

破断後固定証言モードは、対象構造の状態を自由生成で再解釈せず、固定されたフィールドと形式で反復可能に証言するモードである。一回限りの最終メッセージを意味しない。

生存しているCause-Sideセンサー、ロガー、通信経路は、それぞれの物理的限界まで独立して観測、記録、転送を継続する。一つの観測チャネル喪失を、他チャネルの喪失または対象構造の破断へ置換してはならない。

### 正規文

$$
\boxed{
R<1.0\text{ の間、構造証言は停止しない。}
}
$$

$$
\boxed{
R_{\mathrm{target}}\ge1.0\text{ では、破断後固定証言モードへ切り替える。}
}
$$

### 解釈境界コメント

Fail-Closedは、構造証言の完全停止を意味しない。

停止するのは、自由生成、自律判断、自律操作、回復提案、最適化提案、類推補完である。

通常形式の構造証言はRが1.0へ到達するまで継続し、その後は生存経路を通じた破断後固定形式へ移行する。

### 11.1 対象別状態の分離

単一の境界状態で、評価対象と観測・記録・通信・実行権限・証言形式の全状態を表現してはならない。少なくとも次を論理的に分離する。

```text
TargetBoundaryState
ObservationChannelState
LoggingChannelState
CommunicationChannelState
ExecutionAuthorityState
StructuralTestimonyMode
```

正規値は次を含む。

```text
TargetBoundaryState:
  PERMIT
  BOUNDARY_WARNING
  HANDOFF_REQUIRED
  IRREVERSIBLE_TRANSITION
  RUPTURE_BOUNDARY

ObservationChannelState:
  ACTIVE
  OBSERVATION_LOST
  NOT_OBSERVABLE

LoggingChannelState:
  ACTIVE
  LOGGING_LOST

CommunicationChannelState:
  ACTIVE
  COMMUNICATION_LOST

StructuralTestimonyMode:
  CONTINUOUS
  POST_RUPTURE_FIXED
```

チャネル状態は正規境界状態を追加または置換しない。

### 11.2 観測経路喪失

観測不能値をゼロ、安定、安全、回復または完全破断として補完してはならない。利用可能な範囲で、各観測チャネルについて次を固定記録する。

- センサー識別子
- 最終有効観測値
- 最終有効観測時刻
- 欠測開始時刻
- 最終確認された健全性状態
- 電源状態
- 通信状態
- 観測不能理由
- 理由不明である場合の明示
- 出所および監査系列

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

では、構造証言は破断後固定証言モードへ切り替わる。

### 解釈境界コメント

Fail-Closedを「システム全体の停止」「完全無出力」「観測停止」と解釈してはならない。

---

## 13. STRUCTURAL_DISCLOSURE_LOG

有限な $\delta\ge0$ 、有限な $\tau>0$ 、有効な閾値規則によって分類できる既知の構造状態は、STRUCTURAL_DISCLOSURE_LOGとして扱う。

STRUCTURAL_DISCLOSURE_LOGには次を含む。

- PERMIT
- BOUNDARY_WARNING
- HANDOFF_REQUIRED
- IRREVERSIBLE_TRANSITION
- RUPTURE_BOUNDARY

CONFESSIONとOUT_OF_DESCRIPTION_DOMAINは、既知のR進行ではないためSTRUCTURAL_DISCLOSURE_LOGへ含めない。これらはINPUT_EXCEPTION_LOGとして記録する。

INPUT_EXCEPTION_LOGには次を含む。

- CONFESSION：不明、不正、曖昧、出所不明、単位不明、規則不明
- OUT_OF_DESCRIPTION_DOMAIN： $\tau=0$ によりRを定義できない入力

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

Cause-Side全体を時間的に更新不能な構造として扱ってはならない。固定するのは、更新権限、更新経路、出所、対象、単位、観測時刻、評価前に固定された変換規則、評価中の閾値規則、および評価に使用したスナップショットである。

新しい正規Cause-Side観測による次の評価スナップショットへの更新は許される。Effect-Sideによる観測値、閾値、境界状態、不可逆ラッチ、意味の書換えまたは補完は禁止する。

### 解釈境界コメント

Effect-Sideの出力評価を、Cause-Sideの構造変数へ逆流させてはならない。

これは、NRA-IDEの因果方向を保つための必須境界である。

### 評価出力の位置

R、正規状態、不可逆ラッチは、Cause-Side観測そのものでもEffect-Side生成物でもない。Cause-Side入力から事前固定規則で計算した評価出力である。評価出力は、監査、構造証言、状態分類、および事前固定された物理制御の指令に使える。

R, the canonical state, and the irreversible latch are neither Cause-Side observations nor Effect-Side artifacts. They are evaluation outputs computed from Cause-Side inputs by pre-fixed rules. Evaluation outputs may be used for audit, structural testimony, state classification, and pre-fixed physical-control commands.

### 逆導出の定義

次の経路を逆導出とし、自動、手動、人間レビュー、承認、版更新のいずれを介しても禁止する。

- 逆導出A（権威の逆流）：Effect-Sideから、Cause-Sideの値、閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所への経路。
- 逆導出B（計器の自己調整）：評価出力（その移動平均・集約を含む）から、同じ評価対象の基準、変換規則、閾値、有効ゲート幅への経路。段をまたぐ経路と、他の評価対象を経由して戻る経路を含み、広げる向きか狭める向きかを問わない。

他の評価対象の評価出力を、自らの評価対象の閾値または有効ゲート幅へ入れる経路は、安全側の向き（閾値を下げる、ゲート幅を狭める）に限り、かつ自らの評価出力がその評価対象へ戻る経路がない場合に限り許す。この経路の有無と規則は、評価開始前に固定する。

逆導出かどうかは、使った記号の名前ではなく、経路の出所と書き換え先で判定する。対象構造そのものの物理法則による状態の更新（例：§7のτ状態遷移式）は、書き換え先が対象構造であり、逆導出ではない。

語義の分類表は`theory/SANDWICH_ARCH.md`§8.4に置く。定義は本節による。

The following paths are reverse derivation and are prohibited, whether through automatic, manual, human-reviewed, authorized, or versioned means.

- Reverse derivation A (authority backflow): a path from Effect-Side to a Cause-Side value, threshold, state, irreversible latch, rule, transformation input, update ground, or provenance.
- Reverse derivation B (self-adjustment of the gauge): a path from an evaluation output (including its moving averages and aggregates) to the reference, transformation rule, thresholds, or effective gate width of the same evaluation target. It includes paths across steps and paths returning through another evaluation target, whether widening or narrowing.

A path that feeds an evaluation output of another evaluation target into the thresholds or effective gate width of one's own evaluation target is permitted only in the safe-side direction (lowering thresholds, narrowing gate widths), and only when no path returns one's own evaluation outputs to that other target. The existence of such a path and its rule are fixed before evaluation begins.

Whether a path is reverse derivation is judged by its origin and rewrite target, not by the name of the symbol used. An update of state by the physical law of the target structure itself (for example, the tau state-transition equation in §7) rewrites the target structure and is not reverse derivation.

The classification table of meanings is placed in `theory/SANDWICH_ARCH.md` §8.4. The definitions follow this section.

---

## 15. 現場固有物理モデル・現場固有値と不変原則の分離

### 15.1 現場固有物理モデルとIDE不変評価構造の分離

### Separation of Domain-Specific Physical Models and the Invariant IDE Evaluation Structure

NRA-IDEは、あらゆる対象の物理現象を単一の方程式によって記述する統一物理モデルではない。

唯一の律環公理「存在は生成である。」は、対象を静的実体ではなく、履歴を伴って継続する生成構造として扱うための最上位前提である。IDEは、各領域のCause-Side物理モデルから得られた蓄積ズレと吸収厚みを、境界状態、不可逆遷移および実行権限制御へ接続する計算基礎である。

モーターの焼損、水圧構造の決壊、生体組織の破断、電力系統の崩壊、AI実行系の不可逆操作では、破断または遷移を生じさせる原因変数、物理単位、観測方法、支配方程式および履歴蓄積過程が異なる。

したがって、次の項目は対象領域ごとに定義しなければならない。

- 評価対象となる構造
- Cause-Sideの観測変数
- 各変数の単位、出所および観測時刻
- 対象領域の支配方程式または実証された変換規則
- 蓄積ズレ \(\delta\) の算定規則
- 吸収厚み \(\tau\) の算定規則
- 蓄積、消耗、構造要素の付加および復元を区別する規則
- 適用可能な定義域
- 境界閾値の具体値と、その値を支える根拠
- 観測不能、欠測および計算不能時の処理

ある領域で定義された物理変数、支配方程式、\(\delta\)、\(\tau\)または閾値を、類似性だけを根拠として別領域へ移植してはならない。

$$
\delta_{\mathrm{domain\ A}}
\neq
\delta_{\mathrm{domain\ B}}
$$

$$
\tau_{\mathrm{domain\ A}}
\neq
\tau_{\mathrm{domain\ B}}
$$

同じ記号を使用していても、異なる領域の\(\delta\)および\(\tau\)は、同一の物理量、同一の単位または同一の算定過程を意味しない。

各領域で異なるのは、現象を記述するCause-Side物理モデル、観測変数、変換規則、\(\delta\)と\(\tau\)の算定方法、および閾値の具体値である。

一方、次のIDE評価構造は領域固有の物理モデルによって変更してはならない。

- 構造変数をCause-Side観測または評価前に固定されたCause-Side変換規則から得ること
- 境界接近比を \(R=\delta/\tau\) とすること
- Rが高いほど対象構造の破断境界へ接近すること
- 警告、人間委譲、不可逆遷移および完全破断を同一状態へ畳み込まないこと
- 不可逆遷移後の自動復帰を禁止すること
- Effect-Sideの出力評価によって\(\delta\)、\(\tau\)、R、閾値または不可逆ラッチを書き換えないこと
- 不明値、欠測値または定義域外の値を類推によって補完しないこと
- 自律行動の停止後も、利用可能なCause-Side経路による構造証言を継続すること

$$
\boxed{
\text{不変なのは境界評価構造であり、現場固有の物理方程式ではない。}
}
$$

NRA-IDEは既存の熱力学、電磁気学、材料力学、流体力学、生体力学、制御工学または各領域の実証モデルを置き換えない。

IDEの役割は、それらの領域固有モデルから得られたCause-Side構造量を、不可逆境界へ至る前の警告、人間委譲、自律権限停止および構造証言へ接続することである。

---

NRA-IDE is not a unified physical model that describes every physical phenomenon through a single equation.

The sole Nomological Ring Axiom, “Existence is Generation,” is the highest-level premise for treating a target not as a static entity but as a continuing generative structure with history. IDE is the computational foundation that connects accumulated deviation and absorption thickness obtained from domain-specific Cause-Side physical models to boundary states, irreversible transition, and execution-authority control.

Motor burnout, hydraulic structural failure, biological-tissue rupture, power-grid collapse, and irreversible operations in AI execution systems involve different causal variables, physical units, observation methods, governing equations, and historical accumulation processes.

The evaluation target, Cause-Side variables, units, sources, timestamps, governing equations, derivation rules for delta and tau, applicable domain, and evidence for concrete thresholds must therefore be defined separately for each domain.

A physical variable, governing equation, delta, tau, or threshold defined for one domain must not be transferred to another domain solely by analogy.

Even when the same symbols are used, delta and tau in different domains do not denote the same physical quantity, unit, or derivation process.

What remains invariant is the boundary-evaluation structure, not the domain-specific physical equation.

NRA-IDE does not replace thermodynamics, electromagnetism, material mechanics, fluid mechanics, biomechanics, control engineering, or validated models belonging to individual domains.

The role of IDE is to connect Cause-Side structural quantities obtained from those domain-specific models to warning, human handoff, suspension of autonomous authority, irreversible-transition management, and structural testimony before the target reaches its rupture boundary.

### 15.2 現場ごとに変更してよい項目

現場ごとに変更してよい項目は次である。

- \(R_{\mathrm{warn}}\) の具体値
- \(R_{\mathrm{handoff}}\) の具体値
- \(R_{\mathrm{irrev}}\) の具体値
- 観測周期
- 警告頻度
- 人間委譲先
- 物理的測定方法
- 不可逆到達後の現場対応

### 15.3 現場ごとに変更してはならない項目

現場ごとに変更してはならない項目は次である。

- \(R=\delta/\tau\)
- Rは高いほど危険
- \(R_{\mathrm{handoff}}<R_{\mathrm{irrev}}<1.0\)
- \(R_{\mathrm{irrev}}\neq R=1.0\)
- 不可逆ラッチ
- \(R<1.0\)の間は通常形式の構造証言を停止せず、対象破断後は生存経路で破断後固定証言を継続する
- 対象構造の破断と観測・記録・通信経路の状態を分離する
- Handoffで変更するのは実行権限だけである
- Effect-Sideで\(\delta\)、\(\tau\)、Rを更新しない
- 不明値を類推で補完しない
- CONFESSIONと既知の経過報告を混同しない

---

## 16. 解釈競合時の優先順位

文書、コード、コメント、例示、AI説明が競合した場合、次の順で解決する。

```text
theory/AXIOMS.md (AXIOMS_v2.4)
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

# 下段：AXIOMS v2.3 からの変更点

---

## 1. 変更の性質

v2.4は、唯一の律環公理、NRA構造原則、一次式 \(R=\delta/\tau\)、定義域、閾値の順序、正規境界状態、構造要素の付加・除去を変更しない。

v2.4は、既存のdocs説明文書群が正典に定義のないまま使っていた補助構造量（ω・位相・制約・仕事量・エントロピー）を、新設§4.5として正式に正典化する。これにより、docs文書群がこれらの量を参照する際、正典の定義を引用できるようになる。

---

## 2. 主な追加点

### 2.1 補助構造量を定義（§4.5）

ω（構造連続性）、位相、制約、仕事量、エントロピーを、一次式・二次式を補う補助構造量として定義した。出所はCause-Sideに限る（§14と同じ権威原則）。いずれも評価出力から得てはならない。

### 2.2 位相の記号を確定

docsで使われていた小文字 \(\varphi\) は、FORMULA.md §5.1の補助計算項 \(\Phi(x)\) と大小文字だけの区別になるため採らず、\(\mathrm{Phase}\) と綴りで表す。

### 2.3 エントロピーとSの区別を明記

エントロピー相当量を使う場合、構造感度 \(S\)（FORMULA §3）と混同しないことを正典で明記した。

---

## 3. 変更していないもの

- 唯一の律環公理「存在は生成である。」
- \(R=\delta/\tau\)、\(\tau>0\)、\(\tau=0\)は定義域外
- 閾値の順序 \(R_{\mathrm{warn}}<R_{\mathrm{handoff}}<R_{\mathrm{irrev}}<1.0\) と正規境界状態
- 蓄積ズレの構成と基準不動（§4）
- 構造要素の付加・除去（§7・§8）
- 逆導出A・Bの定義（§14）

---

# 下段：AXIOMS v2.2 からの変更点

---

## 1. 変更の性質

v2.3は、唯一の律環公理、NRA構造原則、一次式 \(R=\delta/\tau\)、定義域、閾値の順序、正規境界状態を変更しない。

v2.3は、吸収厚みが増える経路を「構造要素の付加」の一つに定め、その対として「構造要素の除去」を定める。v2.2までの「外部補充」「外生的な補充操作」「外生補充」「外生的な補修事象」「外生的な復元操作」は、既存の厚みや残留ズレが元に戻るとも読めたため、語を改めた。

---

## 2. 主な追加点

### 2.1 構造要素の付加と除去を定義（§7）

付加は、既存の構造要素の吸収厚みを回復させない。加えた要素の吸収厚みは加えた時点のCause-Side測定で定め、既存の要素と加えた要素の厚みを合わせる規則は評価開始前に固定する。壊れていない要素を計画的に外す除去は、劣化として計上しない。

### 2.2 残留ズレの扱いを限定（§7）

v2.2は残留ズレを「外生的な補修事象がない限り減少しない」としていた。v2.3は「評価中に減少しない」とし、伸び・曲がりを力で戻す矯正を行った場合は、評価を宣言し直すと定める。

### 2.3 動的τの区分を拡張（§7 解釈境界コメント）

作用や条件による一時的な厚みの減少は、実効厚みから差し引かず、蓄積ズレの可逆成分として数える。新しい観測で宣言厚みが変わる場合は、評価中の増加として扱わず、次の評価スナップショットとして宣言し直す。

### 2.4 \(\tau_{\mathrm{restored}}\) の範囲を明確化（§8）

\(\tau_{\mathrm{restored}}\) を、構造要素の付加で加えた要素を除く、既存の要素の吸収厚みとした。付加によって構成全体の吸収厚みが \(\tau_0\) を上回っても、初期構造への復元ではない。

---

## 3. 変更していないもの

- 唯一の律環公理「存在は生成である。」
- \(R=\delta/\tau\)、\(\tau>0\)、\(\tau=0\)は定義域外
- 閾値の順序 \(R_{\mathrm{warn}}<R_{\mathrm{handoff}}<R_{\mathrm{irrev}}<1.0\) と正規境界状態
- 蓄積ズレの構成と基準不動（§4）
- 逆導出A・Bの定義と、他の評価対象の評価出力の扱い（§14）
- 復元劣化の制約 \(\tau_{\mathrm{restored}}<\tau_0\) と、比較可能性の立証要件（§8）

---

# 下段：AXIOMS v2.1 からの変更点

---

## 1. 変更の性質

v2.2は、唯一の律環公理、NRA構造原則、一次式 \(R=\delta/\tau\)、定義域、閾値の順序、正規境界状態を変更しない。

v2.2は、蓄積ズレの定義内容を変更する。v2.1は蓄積ズレを「履歴を伴う蓄積ズレ」とだけ定め、減少し得るかどうかを定めていなかった。v2.2は、蓄積ズレが可逆成分と残留ズレから成ることを定める。これにより、蓄積ズレは作用を除けば減少する成分を含むことになる。

v2.2は、評価出力の位置と逆導出Bの禁止を追加する。

---

## 2. 主な追加点

### 2.1 蓄積ズレの構成と基準不動を定義（§4）

FORMULA.md §4.7は蓄積ズレの差分の符号を判定条件にしており、蓄積ズレの減少を排除していない。v2.1の定義はこれと両立するかどうかを示していなかった。v2.2は、基準状態を評価中に付け直さないことで、残留ズレとして履歴が蓄積ズレに保持されると定める。

### 2.2 残留ズレの非自然回復を追加（§7）

v2.1のτ非自然回復を、蓄積ズレの不可逆成分へ及ぼす。時間経過だけで減少してよいのは、蓄積ズレの可逆成分だけである。

### 2.3 評価出力の位置と逆導出Bを追加（§14）

v2.1は逆導出を、Effect-SideからCause-Sideへの経路だけで定めていた。そのため、評価出力が同じ評価対象の計器を動かす経路を、禁止とも許可とも判定できなかった。v2.2は、評価出力をCause-Side観測ともEffect-Side生成物とも異なる区分として定め、評価出力から同じ評価対象の計器への経路を逆導出Bとして禁止する。他の評価対象の評価出力は、安全側の向きで、閉路がない場合に限り使える。

---

## 3. 変更していないもの

- 唯一の律環公理「存在は生成である。」
- \(R=\delta/\tau\)、\(\tau>0\)、\(\tau=0\)は定義域外
- 閾値の順序 \(R_{\mathrm{warn}}<R_{\mathrm{handoff}}<R_{\mathrm{irrev}}<1.0\) と正規境界状態
- 逆導出A（Effect-SideからCause-Sideへの逆流）の禁止
- τ非自然回復と外生補充の区別

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
