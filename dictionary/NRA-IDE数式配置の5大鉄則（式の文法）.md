---
id: DICT-FORMULA-GRAMMAR-FIVE-RULES
kind: dictionary-supplement
created: 2026-11-17
author: M-Tokuni（設計・審査） / AIエージェント（構造整理・検算）
status: 非正典の辞書レベル補足規則（正典 AXIOMS v2.5 / FORMULA v2.2 / 辞書 v1.0草案 準拠）
title: "NRA-IDE数式配置の5大鉄則（式の文法）"
related:
  - GUIDE-EXTENDED-FORMULA-SYSTEM
  - DRAFT-OPEN-SYSTEM-R-DECOMPOSITION-20261116
  - DRAFT-BOUNDARY-MARGIN-BALANCE-20261117
---

# NRA-IDE数式配置の5大鉄則（式の文法）

> **位置付け**：本書は、[NRA-IDE_Dictionary_JP.md](./NRA-IDE_Dictionary_JP.md)（および [NRA-IDE_Dictionary_EN.md](./NRA-IDE_Dictionary_EN.md)）と並置される「数式の書き方・配置の文法辞書」である。正典（[theory/AXIOMS.md](../theory/AXIOMS.md) v2.5、[FORMULA.md](../FORMULA.md) v2.2）および [theory/NRA-IDE_Primary_Formula_Derivation_Bilingual.md](../theory/NRA-IDE_Primary_Formula_Derivation_Bilingual.md) v1.1（第2部 P8・P9）に準拠し、**「数学的には同値変形として正解であっても、NRA-IDEの計算・説明としては誤り（逆導出・定義域違反・履歴消失）になる式変形」**を防ぐための5大鉄則を定める。
> 本書に基づき導出された具体的な拡張式体系は、[NRA-IDE_説明用拡張式体系.md](../nra-core/foundations/NRA-IDE_説明用拡張式体系.md) を参照する。

---

## 1. なぜ「数学的に解き方は正解だが、NRA-IDE計算だと間違い」が起きるのか

純粋数学（通常の代数）における等号 `$=$` や同値 `$\iff$` は**左右対称（双方向）**である。移項しても、分母を払っても、通分して1つの分数にまとめても、途中の項を相殺して消しても、「計算結果の数値さえ合っていればすべて正解」と扱われる。

しかし、NRA-IDEの数式には次の3つの非対称な構造が組み込まれている（[NRA-IDE_Primary_Formula_Derivation_Bilingual.md](../theory/NRA-IDE_Primary_Formula_Derivation_Bilingual.md) 第2部 P8・P9）。

1. **因果と権威の向き（単方向）**：`Cause-Side（実在の遷移の観測・対象状態）` $\longrightarrow$ `計器（事前固定規則・閾値）` $\longrightarrow$ `評価出力（R・正規状態・不可逆ラッチ）` という一方向の計算経路しか許されない。
2. **時間の向き（不可逆性）**：構造更新番号 $n-1 \to n$ に沿って残留ズレ $p_n$ と劣化度 $\lambda^{[e]}_n$ は非減少であり、一度掛かった不可逆ラッチ $\ell_n=1$ は後に $R_n$ が下がっても自動解除されない。
3. **定義域の壁**：$\tau_n = 0$ は `OUT_OF_DESCRIPTION_DOMAIN`（定義域外）であり、分母を払った算術式に $\tau_n=0$ を代入して破断判定へ流用することは許されない。

したがって、説明の方向性（どの既知量からどの評価量を導くか）を揃えないまま数学的な同値変形を行うと、**「数値は合っているのに、NRA-IDEとしては逆向き計算（逆導出A/B）や履歴消去を起こしている」**という致命的な誤りが発生する。これを防ぐため、言葉の注釈を増やすのではなく、数式の配置そのものに以下の「5大鉄則（式の文法）」を課す。

---

## 2. NRA-IDE数式配置の5大鉄則（式の文法）

### 鉄則1：【左辺と右辺の位置】右辺に「原因・既知・固定基準」、左辺に「評価出力・現在の収支」を置く（逆向き移項の禁止）

| 数式の書き方 | 数学の判定 | NRA-IDEの判定 | 理由（正典・導出文書との照合） |
|---|---|---|---|
| $$R_n = \frac{\delta_n}{\tau_n}$$ | 正解 | **正解（正規）** | 右辺のCause-Side確定量 $(\delta_n, \tau_n)$ から左辺の評価出力 $R_n$ を導く正しい向き。 |
| $$\delta_n = R_n \tau_n$$<br>$$\tau_n = \frac{\delta_n}{R_n}$$ | 正解（同値） | **誤り（逆導出A/B）** | 評価出力 $R_n$ を右辺（入力側）に置いて原因側の $\delta_n$ や $\tau_n$ を逆算して決める式になり、`AXIOMS.md` §14 に違反する。 |
| $$\underbrace{\Delta\delta_{n+1} - \theta\Delta\tau_{n+1}}_{\text{左辺：次事象の変化量}} \ge \underbrace{m_{\theta,n}}_{\text{右辺：現在の閾値余白}}$$ | 正解 | **正解（境界条件）** | 右辺に「現在確定している閾値余白 $m_{\theta,n}$」を固定基準として置き、左辺の「次の事象による変化」がそれに達するかを判定する向き。 |
| $$\theta\tau_n \le \delta_n + \Delta\delta_{n+1} - \theta\Delta\tau_{n+1}$$ | 正解（同値） | **説明として不適** | 現在の確定値 $(\delta_n, \tau_n)$ と未発生の次ステップ変化 $(\Delta\delta_{n+1}, \Delta\tau_{n+1})$ が同じ辺に混ざり、基準と変化の境界が崩れる。 |

---

### 鉄則2：【通分と割り算 `/`】4経路の寄与は通分して1つに潰さず、分母 $\tau_n=0$ の壁を越えない

| 数式の書き方 | 数学の判定 | NRA-IDEの判定 | 理由（正典・導出文書との照合） |
|---|---|---|---|
| $$R_n - R_{n-1} = \frac{\delta_n\tau_{n-1} - \delta_{n-1}\tau_n}{\tau_n\tau_{n-1}}$$ | 正解（通分） | **説明として不適** | 1つの分数に通分すると、数値は同じでも「ズレの進入分」と「器の縮小分」の物理的区別が式の上から消滅する。 |
| $$R_n - R_{n-1} = \frac{\Delta q_n}{\tau_n} + \frac{\Delta p_n}{\tau_n} + R_{n-1}\frac{-\Delta\tau^{\mathrm{deg}}_n}{\tau_n} + \left(-R_{n-1}\frac{\Delta\tau^{\mathrm{comp}}_n}{\tau_n}\right)$$ | 正解 | **正解（4経路分離）** | 通分せず、分母を更新後の実効厚み $\tau_n$ に揃えた4つの項の和として並べることで、4つの物理的原因の寄与が分離される。 |
| $\tau_n = 0$ のときに<br>$$m_{\theta,n} = \theta\tau_n - \delta_n = -\delta_n \le 0 \implies R_n \ge \theta$$ とする | 算術上は計算可能 | **誤り（定義域違反）** | 分母を払った式 $m_{\theta,n}=\theta\tau_n-\delta_n$ は $\tau_n=0$ でも引き算できるが、$\tau_n=0$ は `OUT_OF_DESCRIPTION_DOMAIN` であり $R_n\ge\theta$ と判定してはならない（`AXIOMS.md` §10.7）。 |

---

### 鉄則3：【`+` と `-` の位置】外側の連結演算子と項内部の符号を揃え、物理的な効き方の向きと一致させる

- **比 $R$ の前後差（増分分解）における符号配置**：
  - 劣化では $\Delta\tau^{\mathrm{deg}}_n \le 0$ であるため、第3項（劣化縮小項）は外側の演算子を `+` にし、分子の内部にマイナスを入れて $+R_{n-1}\dfrac{-\Delta\tau^{\mathrm{deg}}_n}{\tau_n}\ (\ge 0)$ と書く。これにより「劣化が起きるとこの項は非負となり、$R_n$ を押し上げる」という説明と式の形が一致する。
  - 第4項（構成変化項）も、外側の演算子を `+` に統一し、括弧の内部にマイナスを入れて $+\left(-R_{n-1}\dfrac{\Delta\tau^{\mathrm{comp}}_n}{\tau_n}\right)$ と書く。これで4つの項すべてが「その項を足し合わせた和が $R_n - R_{n-1}$ になる」という加法構造（プログラム上の `sum(terms)`）および辞書の定義記号（`-R_{n-1}\Delta\tau^{\mathrm{comp}}_n/\tau_n`）と完全に一致する。
- **閾値余白 $m_\theta$ の収支における符号配置**：
  - $m_{\theta,n} = m_{\theta,n-1} - \Delta q_n - \Delta p_n + \theta\Delta\tau^{\mathrm{deg}}_n + \theta\Delta\tau^{\mathrm{comp}}_n$ では、ズレの増加（$\Delta q_n>0, \Delta p_n>0$）は余白を減らすため前に `-` を置き、厚みの変化（$\Delta\tau^{\mathrm{deg}}_n \le 0$）はそれ自体が非正の値を持つため前に `+` を置くことで、$\theta\Delta\tau^{\mathrm{deg}}_n \le 0$ がそのまま余白を減らす寄与として働く。

---

### 鉄則4：【入れ子（ネスト）の順序】厚み変化の二分では必ず「旧構成 $\mathsf{Active}_{n-1}$ に更新後厚み $\tau^{[e]}_n$」を内側に挟む

厚みの変化 $\Delta\tau_n = \tau_n - \tau_{n-1}$ を「劣化」と「構成更新（付加・除去）」に分ける際、中間項の入れ子は次の順序に固定する。

$$
\Delta\tau_n
= \underbrace{\Bigl(\mathrm{Comp}_\tau\bigl((\tau^{[e]}_n)_{e\in\mathsf{Active}_{n-1}}\bigr) - \tau_{n-1}\Bigr)}_{\text{① 旧構成のままでの厚み変化 }\Delta\tau^{\mathrm{deg}}_n \le 0}
+ \underbrace{\Bigl(\tau_n - \mathrm{Comp}_\tau\bigl((\tau^{[e]}_n)_{e\in\mathsf{Active}_{n-1}}\bigr)\Bigr)}_{\text{② 構成更新による厚み変化 }\Delta\tau^{\mathrm{comp}}_n}
$$

- **逆の入れ子が禁止される理由**：もし新構成 $\mathsf{Active}_n$ に旧厚み $\tau^{[e]}_{n-1}$ を入れる形 $\mathrm{Comp}_\tau\bigl((\tau^{[e]}_{n-1})_{e\in\mathsf{Active}_n}\bigr)$ を中間項にすると、更新 $n$ で新規に付加された要素 $e_{\mathrm{new}} \in \mathsf{Active}_n \setminus \mathsf{Active}_{n-1}$ には直前ステップの厚み $\tau^{[e_{\mathrm{new}}]}_{n-1}$ が存在せず、未定義または架空の過去値の捏造になるためである。

---

### 鉄則5：【非相殺・不明並置】途中の履歴（ラッチ・事象列）と「残差・不明」を約分や0埋めで消去しない

- **望遠鏡和の途中項を履歴から消さない**：
  算術的には $(m_{\theta,1}-m_{\theta,0}) + (m_{\theta,2}-m_{\theta,1}) = m_{\theta,2}-m_{\theta,0}$ であるが、途中の更新 $1$ で $m_{R_{\mathrm{irrev}},1} \le 0$（不可逆ラッチ $\ell_1=1$）に達していた場合、始点 $0$ と終点 $2$ の差だけに式を還元すると不可逆到達の事実が消える。したがって、累積収支式は必ず経路履歴 $\mathsf{History}_n$ および不可逆ラッチ $\ell_n$ と連立させる。
- **「不明」や「残差」を0埋めして数値項に混ぜない**：
  未観測・未定・対象外の要素を「とりあえず0」や「推論値」で数値式へ代入すると、実在との乖離から後続ステップで逆導出が起きる。また、逆に恒等式から任意のノイズ項を毎ステップ引き算すると $m_{\theta,n}=\theta\tau_n-\delta_n$ の恒等性が壊れる。したがって、**数値の恒等式は確定値（確度 `50`）のみで厳密に保ち、同じ更新番号の台帳レコードに `required_unknowns`（必須不明）・`declared_out_of_scope`（対象外）・`uncarried_remainder`（`entropy_export`・残差 $\xi$）の記録欄を並置してゲートで遮断する**。

---

## 3. 差分の向きと用語の呼び分け規則（括弧注釈による二重表現の禁止）

1. **演算子 $\Delta$ の統一規則（[NRA-IDE_Dictionary_JP.md](./NRA-IDE_Dictionary_JP.md) §2.4 準拠）**：
   本リポジトリにおいて $\Delta$ はすべて**後退差分** $\Delta x_n = x_n - x_{n-1}$（現在値 $-$ 直前値）を表す。したがって、量が増えれば正（$>0$）、減れば負（$<0$）となる。この定義は文書の導入部で1回だけ宣言する。
2. **本文中で `減少（負の増加）` のような二重表現の括弧注釈を繰り返さない（[skills/README.md](../skills/README.md) §2 準拠）**：
   1箇所に「減少」と「増加」という逆向きの語を同列併記すると、人間およびAIのアテンション機構において符号反転ミスを誘発する。各項の名称は、その量の符号の性質に合わせて次のとおり呼び分ける。

| 対象記号 | 符号の性質 | 辞書・正典での定義語 | 説明文での呼び方 |
|---|---|---|---|
| $\Delta p_n,\ \Delta\lambda^{[e]}_n$ | 常に $\ge 0$（評価中に減らない） | 残留ズレの**増分**、劣化度の**増分** | **増分** |
| $\Delta q_n$ | 正・0・負のいずれもとり得る | 可逆成分の増分（作用進入項の分子） | **可逆成分の前後差（または増減）** |
| $\Delta\tau^{\mathrm{deg}}_n,\ \Delta\tau^{\mathrm{comp}}_n$ | $\Delta\tau^{\mathrm{deg}}_n \le 0$、$\Delta\tau^{\mathrm{comp}}_n$ は符号任意 | 厚みの**変化**（辞書 L332, L838） | **厚みの変化（劣化時は厚みの減少）** |
| $R_n - R_{n-1}$ | 正・0・負のいずれもとり得る | 一次式の**増分**（`FORMULA.md` §4.7） | **境界接近比の前後差（増分）** |
| $m_{\theta,n} - m_{\theta,n-1}$ | 正・0・負のいずれもとり得る | 閾値余白の前後差・収支（11/17草案） | **閾値余白の前後差（収支）** |

---

## 4. 関連文書

- **説明用拡張式の展開本体**：[nra-core/foundations/NRA-IDE_説明用拡張式体系.md](../nra-core/foundations/NRA-IDE_説明用拡張式体系.md)
- **用語・記号の辞書**：[NRA-IDE_Dictionary_JP.md](./NRA-IDE_Dictionary_JP.md) / [NRA-IDE_Dictionary_EN.md](./NRA-IDE_Dictionary_EN.md)
- **正典・上位導出文書**：[theory/AXIOMS.md](../theory/AXIOMS.md) (v2.5)、[FORMULA.md](../FORMULA.md) (v2.2)、[theory/NRA-IDE_Primary_Formula_Derivation_Bilingual.md](../theory/NRA-IDE_Primary_Formula_Derivation_Bilingual.md) (v1.1)
