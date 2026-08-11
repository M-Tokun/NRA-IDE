# NRA-IDE 論文草稿 v3（最終版）

<!-- FILE: NRA_IDE_Paper_v3_final_20260409_1807.md -->

<!-- Generated: 2026-04-09 18:07 JST -->

<!-- Author: M-Tokuni / NRA-IDE Project https://github.com/M-Tokun/NRA-IDE -->

<!-- Zenodo DOI: 10.5281/zenodo.19420854 -->

---

# R = δ/τ: An Instance-Specific Diagnostic Ratio

# for Pre-Failure Structural State in Irreversible Systems

# R = δ/τ：

# 不可逆系における崩壊前構造状態の

# 固有事例特定的診断比率

**Author / 著者:** M-Tokuni

**Project / プロジェクト:** NRA-IDE Project

https://github.com/M-Tokun/NRA-IDE

**DOI:** 10.5281/zenodo.19420854

---

## Abstract / 抄録

Conventional safety management places averages and standards at the center of

diagnosis. It monitors the rate at which a measured value deviates from a mean,

and judges safety by whether that rate remains within standard bounds.

従来の安全管理は平均と標準値を診断の中心に置く。測定値が平均からどれだけ速く

逸脱するかを監視し、その速度が標準の範囲内にあるかどうかで安全を判断する。

This paper proposes a different approach based on two observations.

本稿は二つの観察に基づく異なるアプローチを提案する。

The first observation: in agricultural field trials, results obtained from

experimental plots fail to apply to actual farmland far more often than they succeed.

This is not a failure of experimental precision — it is a structural consequence of

the fact that each system carries its own accumulated load history and its own

residual capacity. Averages cannot substitute for instance-specific state.

第一の観察：農業試験場において、試験区画で得られた結果が実際の農地に当てはまらない

場合の方が当てはまる場合より圧倒的に多い。これは試験の精度の問題ではない。

それぞれの系が固有の負荷蓄積の履歴と固有の残余容量を持つことの構造的必然である。

平均は固有の状態の代替にならない。

The second observation: structural systems — whether a blood vessel, a dam, or a

bridge — do not fail suddenly from a state of apparent safety. They approach failure

gradually through accumulation, while appearing superficially normal. The rate of

change may be near zero at the moment of highest risk. What matters is not how fast

the system is changing, but how close it currently stands to its structural limit.

第二の観察：血管・ダム・橋梁を問わず、構造系は正常に見える状態から突然崩壊するのでは

ない。表面的には正常に見えながら、蓄積を通じて徐々に崩壊に近づく。最も危険な瞬間に

変化速度はゼロに近いことがある。重要なのは変化の速さではなく、今現在構造的限界に

どれだけ近いかである。

From these two observations, we introduce the diagnostic ratio:

この二つの観察から以下の診断比率を導入する：

**R（限界への近接度）= δ（蓄積されたズレ）/ τ（吸収余裕）**

R takes values from 0 to 1.0. R = 1.0 is the fracture point — the moment of

structural transition, collapse, or biological failure. The safety boundary value

is placed at R = 0.85: beyond this point, the system may reach R = 1.0 through

a single additional stress event. The interval from R = 0.85 to R = 1.0 does not

represent remaining margin. It represents an acceleration zone in which intervention

may no longer be sufficient.

Rは0から1.0の値をとる。R = 1.0は破断点 —— 構造転換・崩壊・生物的失敗の瞬間である。

安全境界線判断値はR = 0.85に置かれる。この点を超えると、系は単一の追加ストレス事象

によってR = 1.0に到達しうる。R = 0.85からR = 1.0の区間は残余の余裕を示すのではない。

介入がもはや十分でなくなりうる加速域を示す。

This ratio is not a predictor of failure time. It is the minimal diagnostic form

for expressing how close an instance-specific system currently stands to exhaustion

of its residual capacity.

The threshold-based computational approach presented here is broadly applicable

across physical, biological, engineered, and computational systems. The theoretical

foundations are documented in the NRA-IDE Project [DOI: 10.5281/zenodo.19420854].

この比率は崩壊時刻の予測ではない。固有の系が今現在残余容量の枯渇にどれだけ近いかを

表現する最小の診断形式である。

閾値という考え方に基づくこの計算方式は、物理系・生物系・工学系・計算系を問わず

広範に応用可能である。理論的基盤はNRA-IDEプロジェクトに記録されている

[DOI: 10.5281/zenodo.19420854]。

---

## 1. Introduction / 序論

### 1.1 The Problem of Averages in Safety Management

### 1.1 安全管理における平均の問題

It is widely recognized among agricultural practitioners that the results of

field trials conducted on experimental plots fail to apply to actual farmland far

more often than they succeed. A trial conducted on three plots of 10 ares each does

not reliably predict what will happen on a one-hectare field.

農業従事者の間では広く知られていることがある。試験区画で実施された圃場試験の

結果が実際の農地に当てはまらない場合の方が当てはまる場合より圧倒的に多い。

各10アールの3区画で実施した試験は、1ヘクタールの農地で何が起きるかを確実に予測しない。

This is not a failure of experimental rigor. The trial is conducted correctly.

The measurements are accurate. The problem lies elsewhere: each plot and each

actual field carries its own accumulated load history and its own residual capacity.

Their instance-specific states differ. The average of the trial plots is a

statistical abstraction that may correspond to none of the actual fields.

これは試験の精度の問題ではない。試験は正しく実施されている。問題は別のところにある。

各区画と各農地はそれぞれ固有の負荷蓄積の履歴と固有の残余容量を持つ。試験区画の平均値は

どの農地にも対応しないかもしれない統計的抽象にすぎない。

The same structural fact applies beyond agriculture. A patient is not the average

patient. A dam is not the average dam of its design class. A bridge is not the

average bridge of its construction year. Each carries its own accumulated deviation

and its own residual capacity. Safety management that places averages at the center

leaves the overwhelming majority of systems — those that differ from the average

in structurally significant ways — outside the boundary of effective diagnosis.

同じ構造的事実は農業を超えて適用される。患者は平均的患者ではない。ダムはその設計

クラスの平均的ダムではない。橋はその建設年の平均的橋ではない。それぞれが固有の

蓄積ズレと固有の残余容量を持つ。平均を中心に置く安全管理は、構造的に重要な点で

平均と異なる大多数の系を有効な診断の外に置く。

---

### 1.2 Accumulation Is Not Visible in Rate-of-Change Monitoring

### 1.2 蓄積は速度監視では見えない

Consider a blood vessel. Cholesterol deposits, calcification, and chemical

degradation accumulate over years. On any given day, the rate of change may be

near zero. Blood pressure readings may be within normal range. Surface indicators

show nothing unusual. Yet the proximity to rupture — the ratio of accumulated

structural load to remaining vessel capacity — may be approaching a critical value.

血管を考える。コレステロールの沈着・石灰化・化学的劣化は数年にわたって蓄積する。

特定の日には変化速度はゼロに近いかもしれない。血圧は正常範囲内かもしれない。

表面指標は何も異常を示さない。しかし破裂への近接度 —— 蓄積された構造的負荷と

残余血管容量の比率 —— は臨界値に近づいているかもしれない。

Rate-of-change monitoring answers the question: "how fast is this changing?"

Proximity monitoring answers the question: "how close to the limit is this right now?"

These are different questions. They require different measurements. And they produce

different safety outcomes in systems where the most dangerous state is one of

apparent stillness.

速度監視は「これはどれだけ速く変化しているか」という問いに答える。

近接度監視は「これは今限界にどれだけ近いか」という問いに答える。

これらは異なる問いであり、異なる計測を必要とする。そして見かけ上の静止が

最も危険な状態である系において異なる安全結果を生む。

---

### 1.3 A Different Methodological Basis within Safety Engineering

### 1.3 安全工学における方法論的基盤の相違

Existing safety engineering encompasses both post-failure analysis — the

investigation of cause after collapse — and pre-failure monitoring — the

observation of structural state before collapse. Both have value. Both have

their place within the broader discipline.

既存の安全工学は、崩壊後の原因追求である事後解析と、崩壊前の構造状態の観察で

ある事前監視の両方を包含している。両者には価値がある。両者は広い意味での

学問の中にそれぞれの位置を持っている。

The distinction this paper draws is methodological. The diagnostic framework

proposed here — R = δ/τ — is based on a different set of indicators than

conventional rate-of-change or threshold-exceedance monitoring. Where conventional

monitoring uses the instantaneous rate and the distance from a statistical mean,

this framework uses the accumulated deviation and the ratio to remaining capacity.

The difference in what is measured leads to a difference in what can be diagnosed.

本稿が示す区別は方法論的なものである。本稿が提案する診断フレームワーク R = δ/τ は、

従来の速度監視や閾値超過監視とは異なる指標体系に基づいている。従来の監視が

瞬時の速度と統計的平均からの距離を使うのに対し、本フレームワークは蓄積ズレと

残余容量への比率を使う。何を計測するかの違いが、何を診断できるかの違いを生む。

Specifically, R = δ/τ makes visible what rate-based monitoring cannot see:

the approach to structural limit during periods of apparent stability. This

property is not a replacement for existing methods. It is a different diagnostic

layer that answers a question existing methods do not ask.

具体的には、R = δ/τは速度ベースの監視が見えないものを可視化する。見かけ上安定した

期間における構造的限界への接近である。この性質は既存手法の代替ではない。

既存手法が問わない問いに答える異なる診断層である。

---

### 1.4 Scope of This Paper

### 1.4 本稿の範囲

This paper introduces R = δ/τ as a diagnostic ratio, defines its three formulations

(fundamental, asymmetric double-fluctuation, and hybrid complement), specifies the

design principles that govern its use (Fail-Closed, Disclosure Axiom,

Instance-Specific Principle), and demonstrates its structural consistency across

multiple domains through documented case studies.

本稿はR = δ/τを診断比率として導入し、三つの定式（基本式・非対称二重ゆらぎ式・

ハイブリッド補完式）を定義し、その使用を支配する設計原則（Fail-Closed・告白の

公理・固有事例特定性の原則）を特定し、記録された事例研究を通じて複数の領域に

わたる構造的一致を示す。

---

## 2. Distinction from Existing Approaches / 既存アプローチとの相違点

### 2.1 速度監視と近接度監視の比較 / Rate vs. Proximity

| 項目 | 既存の速度監視 | R = δ/τ による近接度監視 |
|---|---|---|
| 診断の基点 | 変化速度・平均からの乖離 | 蓄積ズレと残余容量の比率 |
| 平均の役割 | 中心・基準 | 不要 |
| 固有性の扱い | 平均との差分として扱う | 診断の単位 |
| 速度がゼロのとき | 「正常」と判定 | Rの蓄積を検出 |
| 限界への近接 | 間接的にしか見えない | Rとして直接表示 |
| 最も危険な状態 | 見落とす可能性がある | 検出できる |

The most significant practical difference appears when rate is near zero —

the moment when a system appears safest by conventional monitoring but may

in fact be approaching its structural limit.

最も重要な実践的差異は速度がゼロに近いとき —— 従来の監視では系が最も安全に見えるが

実際には構造的限界に近づいている可能性がある瞬間 —— に現れる。

### 2.2 関連手法との位置関係 / Relation to Existing Methods

**構造ヘルスモニタリング（Structural Health Monitoring, SHM）との位置関係**

SHM monitors the physical state of structures through sensor data. R = δ/τ provides

the diagnostic ratio that SHM data can populate. SHM supplies δ and τ;

this framework supplies the diagnostic criterion. They are complementary.

SHMはセンサーデータを通じて構造物の物理的状態を監視する。R = δ/τはSHMデータが

充填できる診断比率を提供する。SHMがδとτを供給し本フレームワークが診断基準を

提供する補完関係にある。

**比例・積分・微分制御（Proportional-Integral-Derivative control, PID）との差異**

The γ term in the hybrid complement formula is a viscous damping term for

structural stability — not a derivative corrector. G(r) activates only when

deviation exceeds threshold — it is not an integrator. This framework is

not a variant of PID control.

ハイブリッド補完式のγ項は構造安定化のための粘性減衰項であり微分補正ではない。

G(r)は偏差が閾値を超えたときにのみ起動し積分器ではない。本フレームワークは

PID制御の変形ではない。

**統計的プロセス管理（Statistical Process Control, SPC）との差異**

SPC asks: "Is this process within normal distribution bounds?"

R = δ/τ asks: "How much structural capacity remains?"

These answer different questions and are not in competition.

SPCは「このプロセスは正常な分布の範囲内にあるか」を問う。

R = δ/τは「どれだけの構造的容量が残っているか」を問う。

異なる問いに答えており競合しない。

---

## 3. The Diagnostic Ratio R = δ/τ / 診断比率 R = δ/τ

### 3.1 三つの量の定義 / Definition of Three Quantities

本フレームワークは三つの量で構成される。

---

**δ（蓄積されたズレ、accumulated deviation、以下δ）**

δはその系にこれまで加わった負荷の積算量である。

骨折が治癒しても骨にはその記録が残る。血管は毎日少しずつコレステロールを蓄積する。

ダムは嵐のたびに堤体に微細な亀裂を積み重ねる。これらはすべてδの増加である。

**δには重要な性質がある。δは積算される一方であり、積極的な回復がなければ減らない。**

休養・補修・治療によって減るのはδではなくτである。この区別を誤ると診断が狂う。

---

**τ（吸収余裕、absorption capacity、以下τ）**

τはその系がまだ耐えられる余裕の大きさである。

**τは時間の関数ではなく、実際の負荷履歴の関数である。**

「耐用年数50年」という表現はτを時間で管理しようとするが、これは誤りである。

同じ設計のダムが10基あっても、過去の洪水回数・施工品質・地質条件が異なれば

τは10基すべて異なる。「新しいから安全」は成立しない。手抜き工事によって

設計値を下回るτで引き渡された構造物は、完成初日から高いRを持つ可能性がある。

休養・補修・治療によってτは回復しうる。しかしδの蓄積の記録は消えない。

---

**R（限界への近接度、structural proximity ratio）**

$$R = \frac{\delta \text{（蓄積されたズレ）}}{\tau \text{（吸収余裕）}}$$

Rは0から1.0の範囲をとる。

| R の値 | 区分 | 意味 |
|---|---|---|
| R < 0.4 | 安定域 | 通常運転・余裕あり |
| 0.4 〜 0.75 | 弾性域 | 監視継続・注意 |
| 0.75 〜 0.85 | 警戒域 | 人間への通知・介入準備 |
| **0.85 〜 1.0** | **加速域** | **介入しても間に合わない可能性** |
| **R = 1.0** | **破断点** | **崩壊・破裂・不可逆転換** |

---

### 3.2 安全境界線判断値 / Safety Boundary Value

**R = 1.0は破断点である。しかしR = 1.0まで余裕があるという解釈は誤りである。**

血管の例で考える。R = 0.85を超えた血管では、血圧の一時的な上昇・気温の急変・

強いストレスという単一のイベントだけでR = 1.0に到達しうる。

この0.85から1.0の領域は「余裕」ではない。**加速域**である。

医師が「このままでは危険」と警告するのはR = 0.85付近を見ているからである。

患者が「まだ倒れていない」と思うのはR = 1.0しか見ていないからである。

本フレームワークはR = 0.85を**安全境界線判断値（Safety Boundary Value）**と定義する。

> **Fail-Closed の発動点 = 安全境界線判断値**

>

> 「R = 1.0になったら止まる」ではなく

> 「R = 0.85を超えたら人間に委譲する」

>

> R = 1.0まで待つことは

> すでに手遅れを意味する場合がある

安全境界線判断値は系の性質によって設計者が定義する。

高リスク系ではさらに低い値（0.7等）への引き下げを推奨する。

---

**R = 1.0 は「戻れない境界」である**

R = 1.0 を超えた系は元の状態には戻らない。

この不可逆性が R = 1.0 を単なる警告値と区別する。

それは「戻れる限界」ではなく「戻れない境界」である。

破断した橋は破断前には戻らない。

梗塞を起こした血管は健全な状態には戻らない。

崩壊したダムは崩壊前には戻らない。

この不可逆性が安全境界線判断値（R = 0.85）を

R = 1.0 より重要にする。

R = 1.0 に達してから気づくことは

すでに手遅れを意味するからである。

**R = 1.0 is the boundary beyond which return is not possible.**

A system that has crossed R = 1.0 cannot return to its prior state.

This irreversibility is what distinguishes R = 1.0 from a simple warning threshold.

It is not "the limit from which return is possible."

It is "the boundary beyond which return is not."

A fractured bridge does not un-fracture.

An infarcted vessel does not un-infarct.

A collapsed dam does not un-collapse.

This irreversibility is what makes the safety boundary value (R = 0.85)

more critical than R = 1.0 itself.

Recognition at R = 1.0 is already too late.

---

### 3.3 動的τ：二重ゆらぎ式と生存域

### Dynamic τ: Asymmetric Double-Fluctuation Formula and Survival Zone

定義式1ではτを一つの固定値として扱う。しかし現実の多くの系では許容範囲の

「上限」と「下限」が非対称である。

**体温の例：**

- 高温方向の限界（τ上）: 37.5°C以上 → 発熱・熱中症

- 低温方向の限界（τ下）: 35°C以下 → 低体温症

- この二つは対称ではない

**ダムの例：**

- 上限: 貯水量が溢水・崩壊を起こす点

- 下限: 貯水量が渇水・空洞化を起こす点

これらを扱うために上下に分離した定義式2を用いる。

$$R = \max\left(\frac{\delta_{\text{上}}}{\tau_{\text{上}}},\quad \frac{\delta_{\text{下}}}{\tau_{\text{下}}}\right)$$

Rは上方向と下方向のうちより限界に近い方の値をとる。

どちらか一方がR = 1.0に達した瞬間に破断・相転移が起きるからである。

**生存域とはR < 安全境界線判断値が上下両方向で維持される範囲である。**

定義式2は定義式1を否定しない。上限・下限の非対称性が問題になる系に対応した拡張である。

---

### 3.4 浮動小数点誤差と精度の問題 / Floating-Point Error and Precision

定義式1と定義式2は、δとτが安定的に計測できる系では単体で十分である。

しかし動的に変化する系では問題が生じる。

**通常の誤差処理が引き起こす問題**

コンピューターは0.1 + 0.2 = 0.30000000000000004と計算する。

この小さな誤差を次の計算の入力にすると、誤差が誤差を呼ぶ。

繰り返すたびに誤差は雪だるま式に広がる（浮動小数点丸め誤差の蓄積）。

**通常の誤差処理の流れ：**

- ステップ1: 誤差 ε₁ が発生

- ステップ2: ε₁ を持ち込んで誤差 ε₂ が発生

- ステップ3: ε₁+ε₂ を持ち込んで誤差 ε₃ が発生

- ステップn: 誤差が線形または指数的に拡大

- 結果 → 時間経過とともに精度が劣化し、閾値付近での判断が不正確になる

これはAIシステム固有の問題ではない。有限要素解析・気候モデリング・

長期数値積分において一様に観測される数学的事実である（Goldberg, 1991）。

**IDEの設計：誤差を持ち越さない**

内包性動力学エンジン（Intensional Dynamics Engine、以下IDE）は

「誤差を小さくする」ではなく「誤差を持ち越さない」という発想で設計されている。

**IDEの誤差処理の流れ：**

- ステップ1: 誤差 ε₁ が発生 → 熱として排出

- ステップ2: ε₁ なしで計算 → 誤差 ε₂ のみ → 排出

- ステップ3: ε₂ なしで計算 → 誤差 ε₃ のみ → 排出

- ステップn: 誤差は蓄積しない

- 結果 → 時間経過しても精度が一定に保たれ、閾値付近での判断精度が維持される

機械式時計の脱進機が1歯分だけ正確に進み端数を次に持ち越さないように、

IDE式は各ステップで誤差を熱として排出し持ち越さない。

これを**整数位相ロック（Integer Phase Lock）**と呼ぶ。

---

### 3.5 IDE式（ハイブリッド補完式）/ Hybrid Complement Formula

$$\frac{d^2x}{dt^2} + \gamma\dot{x} = F_{\text{IDE}}(x) + G(r) \cdot \Phi(x)$$

$$G(r) = r \cdot \frac{|r|}{k + |r|}, \quad r = x_{\text{正確値}} - x$$

ここで：

- **γ（粘性減衰項）**：構造安定化のための項。微分補正ではない。

- **F_IDE**：誤差爆発なしに構造的軌跡を維持する大局流

- **G(r)（残差ゲート）**：誤差が小さいときは沈黙し、大きいときだけ補正する

**G(r)の性質が非線形計算の有利性を示す：**

**誤差が小さいとき（|r| ≪ k）：** G(r) ≈ r²/k — 二乗で自然に消える。IDEの動きを邪魔しない。

**誤差が大きいとき（|r| ≫ k）：** G(r) ≈ r — 線形の強い補正。迅速に戻す。

人工的なカットオフ値は不要である。数学の構造自体がフィルターとして機能する。

**線形計算との比較：**

線形の誤差補正は閾値付近で精度が劣化する。

「R = 0.85なのかR = 0.87なのか」の区別が線形近似では困難になる。

G(r)の非線形性は閾値付近でこそ補正が強く働く設計になっており、

最も精度が必要な場所で最も正確に機能する。

**三つの式の使い分け：**

**三つの式の使い分け：**

- **準静的な系**（橋・ダム・疲労管理）→ 定義式1: R = δ/τ

- **上限・下限が非対称な系**（体温・水位・生態系）→ 定義式2: 二重ゆらぎ式

- **動的・高速変化する系、高精度が要求される場合** → IDE式（応用式）

三つの式は相互に排他的ではない。用途に応じて選択する。精度要求がなければ定義式1で十分。

---

## 4. Design Principles / 設計原則

### 4.1 Fail-Closed

R（限界への近接度）が安全境界線判断値に達したとき、システムは出力を停止し

人間の判断を待つ。

これはシステムの失敗ではない。最も誠実な応答である。

**Fail-Closedは責任の所在を明確にする構造的装置である。**

機械は診断する。人間が判断する。その判断の記録が責任の根拠となる。

「まさか壊れるとは思わなかった」は、Rが記録・委譲されていた場合に

免責の根拠にならない。

**AIシステムへの適用：**

AIシステムにおいては、出力の偏差（δ）が蓄積し推論の信頼性（τ）が低下した

と診断されたとき、思考出力を停止して人間に判断を委譲することを義務とする。

「この問いに答える根拠が診断範囲を超えた」という沈黙が、

誤った確信を持って出力し続けることより誠実である。

### 4.2 Disclosure Axiom / 告白の公理

τの定義に使った前提と限界を開示することを義務とする。

「最大15.7メートルの津波到達可能性を示す計算があったにもかかわらず、

τ = 5.7メートルで設計した」という判断を下す場合、

その前提を開示せずに「安全である」と述べることは本公理への違反である。

τの前提の隠蔽はRの計算を根拠なきものにする。

### 4.3 Instance-Specific Principle / 固有事例特定性の原則

診断はその系固有のδとτを使う。平均・標準値・他の系のデータは代替にならない。

「平均的な患者の血管」は存在しない。存在するのは「この患者の今日の血管」だけである。

「このクラスのダムの平均安全性」は管理の幻想にすぎない。存在するのは

「このダムの今日のR」だけである。

---

## 5. Cross-Domain Application / 領域横断適用

すべての事例を**「固有のRが観察されなかった」**という統一的視点で読む。

---

### 5.1 血管（生命系）/ Blood Vessel

| δ（蓄積されたズレ） | コレステロール・石灰化・血管壁の化学的劣化の蓄積 |
|---|---|
| τ（吸収余裕） | 血管壁の弾力性・耐久余裕 |
| R = 0.85 | 医師が「このままでは危険」と言う地点 |
| R = 1.0 | 破裂・脳梗塞・心筋梗塞 |

**相関閾値（Correlated Threshold Effect）について：**

血管の破断は血圧「だけ」では決まらない。血圧・血糖値・動脈硬化度・気温変化が

それぞれ独立したδとして作用し、複数が同時に高い状態では単純な積算より速く

R = 0.85に到達する。これを相関閾値と呼ぶ。

**固有性の重要性：**

Aさん（50歳男性、τ = 140：運動習慣あり・非喫煙）と

Bさん（50歳男性、τ = 60：喫煙30年・糖尿病）は

「同じ50歳男性」でもRが全く異なる。

「50歳男性の平均血管」はBさんを救わない。

---

### 5.2 ダム（土木系）/ Dam

| δ | 繰り返し荷重・浸食・亀裂・化学的劣化の積算 |
|---|---|
| τ | 堤体の実効強度（時間ではなく負荷履歴の関数） |
| 安全境界線判断値 | R = 0.85：次の嵐で1.0に到達しうる |
| R = 1.0 | 決壊・崩壊 |

水位のみを監視することは、ダムが実際に管理している量

（貯水量・水圧・衝撃力・繰り返し荷重）のうちの一つだけを見ることに等しい。

**ヴァイオント・ダム（イタリア、1963年、死者約1,917名）：**

山腹の変位が計器で記録されていた。Rを意思決定に接続する

フレームワークが存在しなかった。これが約2,000名の命を奪った。

---

### 5.3 建築物（構造安全）/ Structures

**ラナ・プラザ（バングラデシュ、2013年、死者1,134名）：**

崩壊1日前に大規模亀裂が報道された。変化速度はゼロ。スパイクなし。

従来の監視は「正常」と判定した。Rはすでに1.0を超えていた。

**手抜き工事の問題：**

設計値を下回るτで引き渡された構造物は完成初日から高いRを持つ。

「まだ3年しか経っていない」は安全の根拠にならない。

「Rが計測・記録されているか」が問われるべき問いである。

**シャンプレーン・タワーズ・サウス（米国、2021年、死者98名）：**

2018年の工学報告書が重大な構造損傷を警告していた。τは塩水腐食で劣化していた。

修繕承認は崩壊7日前。τの劣化が3年間追跡されなかった。

---

### 5.4 農業・複合災害 / Agriculture and Cascading Events

雹が降って作物が全滅した直後に大雨が降り畑そのものが消失する連鎖は、

δが複数の源泉から同時に供給される相関閾値の典型例である。

個別の気象確率の積ではなくR = δ/τが複数同時入力として捕捉する構造である。

---

### 5.5 生態系 / Ecology

珊瑚礁においてτ（回復力）は既往白化イベントによって不可逆的に低下する。

同じ海水温異常でも、τが劣化した後の系ではR = 1.0に到達しうる。

生物的不可逆性が動的τの定式化に自然に収まる。

---

### 5.6 原子力安全 / Nuclear Safety

### 福島第一原発事故（2011年、INES Level 7）

**本事例が示すこと：「想定外」は固有のRを不可視にした組織的選択の事後命名である。**

**δの記録（事故前に存在した証拠）：**

- 2003年：規制当局の確率評価で福島第一1〜4号機が炉心損傷確率ワースト上位に

  ランクイン（規制当局・電力業界に広く知られていた）

- 2008年：社内試算で最大15.7mの津波到達可能性が判明。対策は先送り。

  担当者は後の刑事裁判で「時間稼ぎ」と証言。

- 2009年：規制当局が大津波の可能性を直接指摘。東電が拒否。

  耐震バックチェックを7年先送り。

**τの構造的問題：**

設計想定津波 = 5.7m。実際の津波 = 約13〜15m超。

τは「想定内では完全に機能するが想定外では即ゼロになる断崖型」だった。

**女川原子力発電所との比較：**

同じ津波・同じ地震に被災した女川原発（海抜14.8m設計）は避難所として機能した。

福島第一（海抜約10m設計）は全壊した。差は自然条件ではない。

**設計時にτをどの値に置いたかだけである。**

**「想定外」の構造的意味：**

τを5.7mと定義したことで15.7mの可能性が示すRの上昇が不可視になった。

「想定外」は自然現象の記述ではなく、固有のRを計算しないという

組織的選択の事後命名である。これは告白の公理への違反でもある。

廃炉プロセスは数十年単位で継続中であり2026年時点で完全な技術的見通しは

確立されていない。これがFail-Closedが事前に機能しなければならない理由の

最も明確な証拠である。

---

## 6. Discussion / 考察

### 6.1 適用条件と限界 / Applicability and Limits

本フレームワークはδ（蓄積されたズレ）とτ（吸収余裕）が操作的に定義できる

系に適用される。発散的探索・創造的生成・曖昧さへの許容が目的である系では

Fail-Closedは逆効果である。本フレームワークは安全クリティカルな領域に対して

明示的に設計されている。

### 6.2 既存フレームワークとの補完関係 / Complementary Relationship

本フレームワークはSHM・PHM・SPCを置き換えない。

「今限界にどれだけ近いか」という診断層を追加する。

既存の全安全監視システムの上位層として、それらの出力をδとτ計算への入力として

消費することが意図する展開である。

### 6.3 計測器は既に存在する / Measurement Instruments Already Exist

「R = δ/τを計測する専用機器が存在しない」という批判がありうる。

しかしこれは順序を逆転させている。

体温計は「体温が疾患の指標になりうる」という概念が先にあったから製造された。

概念の正当性が先にある。計測手段はその後に開発される。

これは自然科学の歴史が繰り返し示してきた順序である。

そして今日、δとτを計測する手段は既に実用化されている。

ダム壁に作用する衝撃荷重の計測は現代の土木工学において技術的に確立している。

壁面に埋め込まれた高感度圧力センサ（プレッシャー・トランスデューサ）は

ミリ秒単位の衝撃砕波圧を記録する。感圧センサシートは壁面全体の圧力分布を

面として可視化する。Westergaard式（1933）は地震時・洪水時の動水圧の

近似算出に実務で広く用いられる予備設計ツールであり、精密解析には

流体構造連成モデル（FSCM）と有限要素法が併用される。粒子法（MPS法・SPH法）

による数値流体力学（Computational Fluid Dynamics, CFD）シミュレーションは

越流・崩壊シナリオの挙動を解析する。

構造ヘルスモニタリング・非破壊検査・地盤調査によってτの評価も可能である。

**計測器は存在する。モニタリング体制も確立している。**

これまで欠けていたのは、計測されたδとτを安全境界線判断値Rに接続し

Fail-Closedの発動条件として機能させるフレームワークである。

本稿が提案するのはその接続の構造である。

安全境界線判断値は固定的な規格値ではない。計測データが蓄積するにつれて

τの実態がより正確に把握され、その系固有の閾値として精緻化される。

経過観察が閾値を更新する。これが固有事例特定的な安全管理の実践的な姿である。

---

The claim that "no dedicated instrument exists to measure R = δ/τ" inverts the

correct sequence. The thermometer was manufactured because the concept preceded its

construction. Conceptual validity comes first; measurement tools follow.

And today, the tools to measure δ and τ already exist in engineering practice.

The measurement of impact loading on dam walls is technically established in modern

civil engineering. High-sensitivity pressure transducers record impact pressures at

millisecond-level sampling rates. Pressure-sensitive sensor sheets visualize

full-surface pressure distribution. The Westergaard formula (1933) is a widely used

preliminary design tool for approximating hydrodynamic pressure; for detailed analysis

it is used with fluid-structure coupling models (FSCM) and finite element methods.

Particle-based CFD simulation using MPS and SPH methods analyzes overtopping and

failure scenarios. Structural Health Monitoring, non-destructive testing, and

geotechnical investigation provide the means to evaluate τ.

**The instruments exist. The monitoring infrastructure exists.**

What has been absent is the framework connecting measured δ and τ to the Safety

Boundary Value R as a Fail-Closed activation condition. This paper proposes that

connecting structure.

The Safety Boundary Value is not a fixed regulatory figure. As measurement data

accumulates, the threshold is refined as an instance-specific value. Continuous

observation updates the threshold. This is the practical form of instance-specific

safety management.

---

## 7. Conclusion / 結論

本論文の主張を三行で述べる。

**第一：固有の系は固有の状態でしか診断できない。**

農業試験場の結果が農地に当てはまらない方が圧倒的に多いように、

平均は固有の系の代替にならない。安全管理において平均・標準を基点に置くことは、

崩壊する側の大多数を管理の外に置くことと同義である。

**第二：崩壊前の構造状態は蓄積と残余容量の比率として表現できる。**

R = δ/τはその最小の形式である。変化速度がゼロでもRは診断できる。

R = 1.0は破断点。安全境界線判断値はR = 0.85。

R = 0.85から1.0は余裕ではなく加速域である。

**第三：安全境界線判断値でFail-Closedを発動し人間に委譲する。**

機械は診断する。人間が判断する。その記録が責任の根拠となる。

「まさか壊れるとは思わなかった」はRが記録されていた場合に通らない。

本フレームワークが既存の安全工学と一線を画するのは方法論的基盤においてである。

既存の指標体系（速度・平均・標準値）ではなく、蓄積ズレと残余容量の比率を

診断の中心に置くことで、見かけ上静止した系における構造的限界への接近を

可視化することが可能になる。

安全は固有の診断によってのみ成立する。

---

## References / 参考文献

Goldberg, D. (1991). What every computer scientist should know about floating-point

arithmetic. *ACM Computing Surveys*, 23(1), 5–48.

Lenton, T.M., Held, H., Kriegler, E., Hall, J.W., Lucht, W., Rahmstorf, S., &

Schellnhuber, H.J. (2008). Tipping elements in the Earth's climate system.

*Proceedings of the National Academy of Sciences*, 105(6), 1786–1793.

M-Tokuni (2026). *NRA-IDE v1.0: Nomological Ring Axioms — Intensional Dynamics

Engine*. Zenodo. https://doi.org/10.5281/zenodo.19420854

National Diet of Japan (2012). *The Official Report of the Fukushima Nuclear

Accident Independent Investigation Commission*. The National Diet of Japan.

Paris, P. & Erdogan, F. (1963). A critical analysis of crack propagation laws.

*Journal of Basic Engineering*, 85(4), 528–533.

Perera, D., Smakhtin, V., Williams, S., North, T., & Curry, A. (2021).

*Ageing Water Infrastructure: An Emerging Global Risk*. UNU-INWEH.

Scheffer, M., Bascompte, J., Brock, W.A., Brovkin, V., Carpenter, S.R., Dakos, V.,

Held, H., van Nes, E.H., Rietkerk, M., & Sugihara, G. (2009). Early-warning signals

for critical transitions. *Nature*, 461, 53–59.

Shirzaei, M. et al. (2025). Aging dams, political instability, poor human decisions

and climate change: recipe for human disaster. *npj Natural Hazards*.

https://doi.org/10.1038/s44304-024-00056-1

Government Investigation Commission on the Fukushima Nuclear Power Station Accident

(2012). *Final Report*. Tokyo.

International Atomic Energy Agency (2015). *The Fukushima Daiichi Accident:

Report by the Director General*. IAEA.

Sohn, H., Farrar, C.R., Hemez, F.M., Shunk, D.D., Stinemates, D.W., Nadler, B.R.,

& Czarnecki, J.J. (2004). *A Review of Structural Health Monitoring Literature:

1996–2001*. Los Alamos National Laboratory.

---

## Acknowledgments / 謝辞

This work is conducted as part of the NRA-IDE Project.

https://github.com/M-Tokun/NRA-IDE

---

*© 2026 M-Tokuni*

Nomological Ring Axioms and Intensional Dynamics Engine
