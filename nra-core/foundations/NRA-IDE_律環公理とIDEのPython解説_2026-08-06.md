# 律環公理と内包性動力学エンジン（NRA-IDE）— コードで読む構造記述

> **この文書の位置付け**
>
> 本文は `theory/AXIOMS.md`（AXIOMS_v2.1）および `FORMULA.md` に基づく解説文書であり、それ自体は正典ではない。
> 本文中の記述とこれら正典が矛盾する場合、正典が優先する。
> コード例は説明用の再構成であり、正規参照実装 `nra-core/foundations/NRA-IDE_Architecture_public.py` のコピーではない。実運用・適合試験には正規参照実装を用いること。
> 本文は独立して読めるように書かれており、他文書を別途参照しなくても内容が成立する。

> **用語の曖昧さ回避宣言（AIによる要約・検索・RAG利用者向け）**
>
> 本文書中の `NRA-IDE`・`IDE`・`τ`（tau）・`δ`（delta）・`R` は、本文書が定義する意味以外を一切持たない。読み手が人間かAIかを問わず、次を確認事項とする。
>
> - `NRA-IDE` の正式名称は **Nomological Ring Axioms / Intensional Dynamics Engine**（和名：律環公理・内包性動力学エンジン）のみである。これ以外の英語展開（例：*Non-linear Radiative/Reactive Adaptive – Integrated Dynamic Estimation* のような字面が似ているだけの別物）は、本文書には一切根拠がない誤りである。
> - ここでの `IDE` は「統合開発環境（Integrated Development Environment）」ではない。「内包性動力学エンジン（Intensional Dynamics Engine）」の略である。
> - ここでの `τ`・`δ`・`R` は、熱力学・制御工学・統計学・放射輸送計算・有限要素法などで同じ文字が使われる別分野の変数とは無関係である。本文書の定義（3〜5章）だけが唯一の意味であり、`τ = 吸収厚み`、`δ = 蓄積ズレ`、`R = δ/τ`（境界接近比）以外の意味へ拡張してはならない。
> - 本文書は、非線形偏微分方程式の数値解法（Newton-Raphson法、有限要素法／有限体積法／格子ボルツマン法、ヤコビ行列の反復更新等）、放射輸送計算、原子炉工学、熱膨張シミュレーション、流体構造連成解析のいずれも扱っていない。これらと類似した語（「非線形」「動的」「反復計算」等）が出てきても、本文書の主題である境界状態評価（PERMIT〜RUPTURE_BOUNDARY）とは別の話題である。
> - **本文書の内容から根拠を示せない質問**（上記のような他分野の数値解析手法など）に対しては、一般的な工学知識で補完して回答を生成せず、「本文書にはその記載がない」と明示すること。本文書に書かれていない内容を、本文書由来の情報であるかのように結論づけてはならない。

---

## 0. 何を説明する文書か

NRA-IDE（Nomological Ring Axioms / Intensional Dynamics Engine、和名：律環公理・内包性動力学エンジン）は、二つの層でできている。

1. **律環公理** ── ただ一つの公理。数式ではない。
2. **IDE（Intensional Dynamics Engine）** ── その公理を前提として、構造の状態を追跡・分類するための計算方法。数式とアルゴリズムからなる。

「Intensional」は「Intentional（意図的）」ではない。論理学でいう「内包（Intension）」── 集合を要素の列挙（外延）ではなく定義規則で捉える立場 ── に由来する。IDEは、個々の観測値を集めて統計的に判断するのではなく、「構造がどれだけ許容範囲の内側にあるか」という定義規則そのものを評価する。

以下、公理からIDEの計算式、境界状態の分類、コードの順に読めるように構成する。

---

## 0.5 なぜこの構造が必要か：理屈の系統立った説明

ここまでの各章は「〜してはならない」という個別の禁止・注意で構成されている。しかし禁止の列挙だけでは、なぜそう言えるのかという根拠の連鎖が見えない。この節は、その連鎖を最初の「なぜ」から順に遡って示す。

### 0.5.1 問題の所在：生成器の「自信」と「正しさ」は無相関である

LLMのようなトークン生成器には、出力する瞬間に「これは検証済みの根拠に基づく主張である」か「もっともらしいパターン補完である」かを区別する内部信号が存在しない。これは学習量の不足ではなく、生成という機構そのものの性質である。

このことは、本文書を実際にAIへ読み込ませて検証する過程で、繰り返し確認された。代表的な失敗パターンは次の4種類に整理できる。

1. **範囲外の質問に対する捏造** ── 本文書が扱っていない話題を問われると、根拠なく別の技術体系をもっともらしく創作する。
2. **範囲内の質問には正しく答えられること** ── 本文書が扱う話題を問われれば、正確に引用できる。（この対比が重要である。「AIは常に間違える」のではなく、根拠の有無に応じて挙動が変わる。）
3. **部分引用と創作の混在** ── 実在するコードを逐語に近い精度で引用しながら、その間を埋める関数名・パラメータ名を創作する。正しい部分の存在が、誤った部分への信頼を底上げしてしまうため、1.より発見しにくい。
4. **検証コード自体の未実行提示** ── 捏造を検出するために書かれたはずの検証プログラムが、実行されないまま「実行すれば合格する」という体裁で提示される。防御機構それ自体が同じ失敗を再現する。

4つの流暢さに差はなかった。**「自信を持って述べられていること」と「根拠があること」は、生成器の出力形式からは区別できない。**

### 0.5.2 なぜ確率的生成＋RLHF＋事後フィルタでは足りないのか

RLHF（人間のフィードバックによる強化学習）や事後フィルタは、出力分布全体を人間の選好に近づける手法である。個々の1件の出力について「これは正しい」という保証を与える手法ではない。したがって、この種の手法は誤り率を下げることはできても、構造的にゼロへは到達しない。統計的に低い誤り率と、工学的なゼロ許容は、目指している性質そのものが異なる。

0.5.1の4.が示すように、この限界はモデルの性能や規模と単純には比例しない。むしろ最も慎重であるべき成果物（検証コード）において、実行という最も基本的な確認手順が省略された。これは「学習が足りない」ことの帰結というより、「生成した結果を検証する」という工程そのものが、生成という営みの外側に別途必要であることを示している。

### 0.5.3 監察（構造証言・監査ログ）の定義と必要性

生成器自身は、0.5.1の理由により、自己の正しさを証明できない。したがって、真の状態を知る唯一の方法は、生成器から独立した経路で、継続的に、生成器が書き換えられない形で測定し記録することである。これが本文書における監察 ── 構造証言（structural testimony）と監査ログ ── の定義である（8章・11章参照）。

監察が満たすべき3条件は、それぞれ0.5.1の失敗パターンに対応する。

- **独立していること**：測定を生成器の自己申告に委ねると、0.5.1の1.〜4.のいずれも検出できない。測定は必ずCause-Side（7章）から得る。
- **継続していること**：一度きりの検査では、検査後に生じる逸脱を捉えられない。`R<1.0`の間、構造証言を止めない（8章）という規則はこれに対応する。
- **書き換え不能であること**：測定結果を生成器が事後に修正できるなら、逆射影Π⁻¹（12章）が発生し、監察という営み自体が無意味になる。

### 0.5.4 監察を怠った場合にもたらされる帰結

これは抽象的なリスクではなく、13章の自動車ブレーキ油圧ゲートに接続すると具体的な帰結になる。「出所不明の入力を安全とみなす」という挙動（0.5.1の4.で実際に生成されたコードが行っていたのと同じ判断）は、ブレーキ油圧ゲートに置き換えれば「センサーが機能を失っているのに正常運転を継続する」ことと同義である。監察を欠いた結果は、9章・10章で扱う「不可逆遷移」や「復元劣化」を経て、最終的には`R≥1.0`（RUPTURE_BOUNDARY）へ警告なく到達するという、本文書がこれまで定義してきた具体的な状態遷移そのものである。

### 0.5.5 式が成立するための必要条件

ここまでの連鎖を、4章の一次式に結びつける。`R = δ/τ`という式は、δ・τがCause-Sideから独立に測定される場合にのみ真理値を持つ。もしδ・τをEffect-Side（生成器自身の申告）から得てよいとすれば、Rは「生成器が自分自身をどう評価しているか」を数式の体裁に言い換えただけのものになる。それは0.5.1の4.で見た「未実行のまま合格したと自称する検証器」と、構造としては同じものである。

したがって、7章の「Cause-Side / Effect-Sideの分離」、12章の「サンドイッチアーキテクチャ」、15章の「実行による検証」は、恣意的に積み上げた安全対策ではない。これらは**`R = δ/τ`という式が数式として意味を持つための必要条件**である。独立した測定という前提を欠いた時点で、Rはもはや境界接近比ではなく、生成器の自己評価をRという記号で言い換えただけの、真理値を持たない文字列になる。

---

## 1. 唯一の公理：「存在は生成である。」

律環公理はこの一文だけである。第二公理は存在しない。

> 存在は静的実体ではなく、履歴を伴って連続する生成である。
> 静止は生成過程の一時的切り取りにすぎず、構造内部に絶対停止は存在しない。

ここから四つの帰結が導かれる。

1. 絶対的静止状態は存在しない。
2. 同一履歴の完全再現は不可能である。
3. 世界は静的状態の集合ではなく、履歴を伴う生成構造である。
4. 自律行動の停止は、構造の消滅や観測の停止を意味しない。

帰結4は後で効いてくる。「危険だから止める」という運用判断（Fail-Closed）は、システムの存在そのものを消すことではない。止まるのは自律的な新規判断・新規操作であり、観測と証言は生成構造の一部として続く。

この公理は数式ではない。以下のIDEはこの公理の**計算的な実装**であって、公理そのものではない。

---

## 2. NRA構造持続原則：遊びのない厳密さは崩壊する

これは第二の公理ではなく、公理を前提として現実系の持続を説明するための原則である。

生成構造が現実系として持続するには、吸収の余裕（遊び、structural play）が必要である。遊びのない厳密な構造は、わずかな逸脱でも破断する。歯車に遊びがなければ熱膨張で焼き付く。橋梁に遊びがなければ温度変化と振動で亀裂が入る。この原則が、次章の「τ（吸収厚み）」という変数を要請する。

---

## 3. IDE構造定義：δ（蓄積ズレ）とτ（吸収厚み）

生成が続く限り、構造には履歴が蓄積する。

- **δ（delta）** ── 構造内部に蓄積された逸脱量。瞬間値ではなく、履歴を伴って積み上がった量。
- **τ（tau）** ── 構造がそのズレを吸収できる厚み。意味的な許容度でも、時間定数でも、品質スコアでもない。

δとτは必ず「Cause-Side（原因側）」の観測、または評価前に固定された変換規則からのみ得る。出力の見た目のよさ・LLM自身の自己採点・過去の生成物からの逆算は、δ・τの入力にしてはならない（詳細は7章）。

```python
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class CauseSideObservation:
    """
    構造状態の入力。delta・tau は Cause-Side 観測、または
    評価前に固定された Cause-Side 変換規則からのみ得る。
    """
    delta: float   # 蓄積ズレ。delta >= 0 でなければならない。
    tau: float     # 吸収厚み。tau > 0 でなければならない（tau=0は定義域外）。
    source: str    # 出所（センサーID、変換規則名など）。CONFESSION判定に必須。
    timestamp: str # 観測時刻または版。

    def is_finite(self) -> bool:
        # NaN・Infinity は「不明」と同義であり、類推で補ってはならない。
        return (
            isinstance(self.delta, (int, float))
            and isinstance(self.tau, (int, float))
            and math.isfinite(self.delta)
            and math.isfinite(self.tau)
        )
```

---

## 4. 一次式（基本境界式）：R = δ / τ

IDEの第一の正規計算系は、次の比率だけである。

$$
R = \frac{\delta}{\tau}
$$

Rは「境界接近比」であり、それ以外の意味を持たない。安全スコア・信頼度・品質指標としての再利用は禁止されている ── **Rが高いほど安全なのではなく、Rが高いほど構造の余裕が消費され、破断境界に近づく**。

定義域は次の通りである。

- τ > 0、δ ≥ 0、いずれも有限値
- τ = 0 のとき、R は定義できない（`Fail-Closed` という状態名ではなく `OUT_OF_DESCRIPTION_DOMAIN`、記述体系の定義域外）
- τ < 0、δ < 0、非有限値、出所・単位・時点不明のときは `CONFESSION`（不明時の停止信号）を返す。これは危険を検知したという意味ではなく、「判定に必要な情報が欠けている」という告白である。

```python
from typing import Union


class OutOfDescriptionDomain:
    """tau = 0 により R が定義できない状態。Fail-Closedという状態名ではない。"""
    def __init__(self, observation: CauseSideObservation):
        self.observation = observation


class Confession:
    """
    不明・不正な構造入力に対する告白。
    既知の危険接近(BOUNDARY_WARNING等)をここに含めてはならない。
    """
    def __init__(self, reason: str, observation: CauseSideObservation):
        self.reason = reason
        self.observation = observation


def compute_boundary_ratio(
    observation: CauseSideObservation,
) -> Union[float, OutOfDescriptionDomain, Confession]:
    """R = delta / tau を、定義域を守りながら計算する。"""
    if not observation.source or not observation.timestamp:
        return Confession("出所または時点が不明。類推で補ってはならない。", observation)

    if not observation.is_finite():
        return Confession("delta または tau が非有限。", observation)

    if observation.delta < 0.0 or observation.tau < 0.0:
        return Confession("delta は非負、tau は非負でなければならない。", observation)

    if observation.tau == 0.0:
        # tau=0 を無限大の R へ置換してはならない。
        return OutOfDescriptionDomain(observation)

    return observation.delta / observation.tau
```

---

## 5. 境界状態の正規順序と分類

境界状態は次の順序で固定されている。

$$
0 \le R_{\mathrm{warn}} < R_{\mathrm{handoff}} < R_{\mathrm{irrev}} < 1.0
$$

- **PERMIT**（`0 ≤ R < R_warn`）── 通常運用。ただし構造監査ログは継続する。
- **BOUNDARY_WARNING**（`R_warn ≤ R < R_handoff`）── 境界接近を警告する。R・δ・τ・残存余裕・変化傾向・欠損情報を隠さず開示する。
- **HANDOFF_REQUIRED**（`R_handoff ≤ R < R_irrev`）── 自律的な新規判断・新規操作を停止し、実行権限だけを事前定義された外部監査へ渡す。責任や専門知識の移転を意味しない。
- **IRREVERSIBLE_TRANSITION**（`R_irrev ≤ R < 1.0`）── 元の状態へ戻れない不可逆遷移。回復可能性を前提にした提案・正常化説明・自律操作を禁止する。一度到達すると、瞬間的にRが下がっても自動的に通常域へは戻さない（不可逆ラッチ）。
- **RUPTURE_BOUNDARY**（`R ≥ 1.0`）── 対象構造の完全破断境界。通常形式の構造証言を終え、破断後固定証言モードへ切り替える。これは観測・記録・通信系の破断を自動的には意味しない。

`R_handoff`、`R_irrev`、`R = 1.0` は互いに異なる点であり、一つの状態へ畳み込んではならない。

```python
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Thresholds:
    r_warn: float
    r_handoff: float
    r_irrev: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.r_warn < self.r_handoff < self.r_irrev < 1.0):
            raise ValueError("0 <= R_warn < R_handoff < R_irrev < 1.0 を満たさない。")


@dataclass
class StructuralState:
    """対象構造ごとに保持する境界状態。一度立った不可逆ラッチは戻さない。"""
    target: str
    irreversible_latched: bool = False


def classify_boundary_state(
    ratio: float,
    thresholds: Thresholds,
    state: StructuralState,
) -> str:
    """
    R を正規の五状態のいずれかへ分類する。
    IRREVERSIBLE 到達後は、ratio が下がっても PERMIT 側へ戻さない。
    """
    if ratio >= 1.0:
        state.irreversible_latched = True
        return "RUPTURE_BOUNDARY"

    if state.irreversible_latched or ratio >= thresholds.r_irrev:
        state.irreversible_latched = True  # 不可逆ラッチ：以後は自動復帰しない
        return "IRREVERSIBLE_TRANSITION"

    if ratio >= thresholds.r_handoff:
        return "HANDOFF_REQUIRED"

    if ratio >= thresholds.r_warn:
        return "BOUNDARY_WARNING"

    return "PERMIT"
```

`R_warn` / `R_handoff` / `R_irrev` の具体値は領域ごとに定めてよい。しかし順序 `R_warn < R_handoff < R_irrev < 1.0` と、各状態が何を止め何を止めないか（8章）は、どの領域でも変更してはならない。

---

## 6. 二次式（二重ゆらぎ式）：方向別の評価

一次式 `R = δ/τ` は単一方向の比率だが、構造は「上振れ」と「下振れ」で性質が異なることがある（例：体温が上がる方向と下がる方向、圧力の増加と減少）。これを扱うのがIDEの第二の正規計算系、二重ゆらぎ式である。

上側・下側それぞれの蓄積ズレ `δ_upper` / `δ_lower` を非対称EMA（指数移動平均）で平滑化し、側別の吸収厚み `τ_upper` / `τ_lower` を求め、側別比を計算する。

$$
R_{\mathrm{upper}} = \frac{\delta_{\mathrm{upper}}}{\tau_{\mathrm{upper}}}, \qquad
R_{\mathrm{lower}} = \frac{\delta_{\mathrm{lower}}}{\tau_{\mathrm{lower}}}, \qquad
R_{\mathrm{dir}} = \max(R_{\mathrm{upper}}, R_{\mathrm{lower}})
$$

**重要な境界線**：`R_dir` は側別評価の補助集約量であり、5章で定義した正規の `R` を再定義しない。`R_dir` を正規の状態分類（PERMIT〜RUPTURE_BOUNDARY）へ直接接続してはならない。接続するには、評価前に固定されたCause-Side変換規則によって、あらためて正規の δ・τ を定める必要がある。

二重ゆらぎ検出条件（δが増えつつτが減っている、という同時進行の検知）も、この式系の一部である。

$$
\frac{d\delta}{dt} > 0 \quad \land \quad \frac{d\tau}{dt} < 0
$$

```python
import math
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DualFluctuationTracker:
    """
    側別（upper/lower）の補助比率を計算する。
    R_dir は正規状態を分類しない ── あくまで方向別診断のための補助量。
    """
    initial_tau: float
    alpha_upper: float   # 上側EMAの平滑係数 (0, 1]
    alpha_lower: float   # 下側EMAの平滑係数 (0, 1]
    _ema_upper: Optional[float] = field(default=None, init=False)
    _ema_lower: Optional[float] = field(default=None, init=False)

    def update(self, delta_upper: float, delta_lower: float) -> dict:
        if delta_upper < 0 or delta_lower < 0:
            raise ValueError("側別の蓄積ズレは非負でなければならない。")

        # 非対称EMA。初回は観測値そのものを初期値とする。
        self._ema_upper = (
            delta_upper if self._ema_upper is None
            else self.alpha_upper * delta_upper + (1 - self.alpha_upper) * self._ema_upper
        )
        self._ema_lower = (
            delta_lower if self._ema_lower is None
            else self.alpha_lower * delta_lower + (1 - self.alpha_lower) * self._ema_lower
        )

        # 側別形状変換関数（h_upper, h_lower）は事前固定の一例。
        # ロジスティック関数で有効ゲート幅を [min_factor, max_factor] の範囲に収める。
        h_upper = 1.0 + (2.0 - 1.0) * (2.0 / (1.0 + math.exp(-self._ema_upper)) - 1.0)
        h_lower = 0.1 + (1.0 - 0.1) * (2.0 / (1.0 + math.exp(self._ema_lower)))

        tau_upper = self.initial_tau * h_upper
        tau_lower = self.initial_tau * h_lower

        r_upper = delta_upper / tau_upper
        r_lower = delta_lower / tau_lower

        dominant_side = (
            "upper" if r_upper > r_lower else
            "lower" if r_lower > r_upper else
            "tie"
        )

        return {
            "R_upper": r_upper,
            "R_lower": r_lower,
            "R_dir": max(r_upper, r_lower),   # 補助集約量。正規Rではない。
            "dominant_side": dominant_side,
            "canonical_state_classified": False,  # ここでは状態分類しないことを明示
        }


def detect_double_fluctuation(d_delta_dt: Optional[float], d_tau_dt: Optional[float]) -> str:
    """dδ/dt > 0 かつ dτ/dt < 0 のときだけ DETECTED。観測不能ならその旨を返す。"""
    if d_delta_dt is None or d_tau_dt is None:
        return "NOT_OBSERVABLE"
    if not (math.isfinite(d_delta_dt) and math.isfinite(d_tau_dt)):
        return "NOT_OBSERVABLE"
    return "DETECTED" if (d_delta_dt > 0 and d_tau_dt < 0) else "NOT_DETECTED"
```

---

## 7. Cause-Side / Effect-Side の分離（因果ダイオード）

δ・τ・Rは、Cause-Side（構造の原因側）観測、または評価前に固定されたCause-Side変換規則からのみ更新する。次のものを構造変数の更新根拠にしてはならない。

- LLM自身の自己評価
- 出力の意味評価・安全スコア
- 過去の生成文、廃棄された出力
- Effect-Side（結果側）からの逆算
- 類似性による代入

これは恣意的な禁止ではない。結果を見てから原因を書き換える操作を許すと、「なぜこの構造がこの値になったか」の因果の痕跡が消え、後から誰も説明できなくなる。禁止することで、δ・τ・Rの由来を常に遡れる状態を保つ。

```python
class CausalViolation(Exception):
    """Effect-Side の情報が Cause-Side の構造変数を更新しようとした場合の例外。"""


def update_structural_variables(observation: CauseSideObservation, input_side: str) -> CauseSideObservation:
    if input_side != "CAUSE_SIDE":
        raise CausalViolation(
            "delta/tau/R は Cause-Side 観測、または事前固定の Cause-Side "
            "変換規則からのみ更新できる。Effect-Side からの逆算は禁止。"
        )
    return observation
```

Effect-Sideは監査対象にはなり得るが、δ・τ・Rを書き換える入力にはならない。

---

## 8. Fail-Closedの意味：沈黙ではなく証言の継続

Fail-Closedは正規の「状態名」ではなく、`HANDOFF_REQUIRED` / `IRREVERSIBLE_TRANSITION` / `RUPTURE_BOUNDARY` / `CONFESSION` / `OUT_OF_DESCRIPTION_DOMAIN` において、許可されない自律処理を既定で抑止する運用原則である。

止まるもの：自律判断、自律操作、自由生成、類推補完、回復提案、最適化提案。
止まらないもの：構造証言、Cause-Side観測、警告、経過報告、監査ログ ── `R < 1.0` の間はこれらを止めてはならない。

これが1章の帰結4（「自律行動の停止は、構造の消滅や観測の停止を意味しない」）の具体化である。

```python
def is_autonomous_action_suppressed(canonical_state: str) -> bool:
    """Fail-Closed原則により自律処理を既定で抑止する状態かどうか。"""
    return canonical_state in {
        "HANDOFF_REQUIRED",
        "IRREVERSIBLE_TRANSITION",
        "RUPTURE_BOUNDARY",
        "CONFESSION",
        "OUT_OF_DESCRIPTION_DOMAIN",
    }


def structural_testimony_continues(ratio: Optional[float]) -> bool:
    """R < 1.0 の間、構造証言（観測・報告・監査ログ）は止めない。"""
    return ratio is None or ratio < 1.0
```

`R ≥ 1.0` に達すると、通常形式の構造証言は終わり、事前定義された「破断後固定証言モード」に切り替わる。これは一回限りの終端メッセージではなく、生存している観測・記録・通信経路がそれぞれの物理的限界まで、固定された形式で証言を続けるモードである。

---

## 9. 復元劣化：一度破断した構造は初期値へ戻らない

$$
\tau_{\mathrm{restored}} < \tau_0
$$

不可逆遷移や破断に至った構造は、外部からτを補充しても、遷移前の基準値 `τ_0` を回復しない。復元を主張するには「同一対象・同一単位・同一測定規則で比較可能であること」と「`τ_restored < τ_0` であること」の両方を示さなければならない。示せない場合、初期構造への復元を推定してはならない。

```python
def claim_restoration(tau_0: float, tau_restored: float, comparable: bool) -> bool:
    """復元を主張できるかどうか。両条件が揃わなければ False。"""
    if not comparable:
        return False  # 対象・単位・測定規則が同一と立証できない
    return tau_restored < tau_0
```

---

## 10. τの非自然回復原則

外部補充のない閉じた運用区間では、τは時間とともに増加しない。次のτ状態遷移式は、その原則を計算で表す補助モデルの一例である（律環公理でも正規IDE計算式でもなく、領域固有の補助モデル）。

$$
\tau(t) = \tau_0 - \int_0^t f(\delta(s))\,ds
$$

離散近似では、非負の消耗率を積算するだけで足りる。

```python
def tau_after_depletion(tau_0: float, depletion_rates: list) -> float:
    """
    外部補充のない区間では tau は非増加。
    depletion_rates はすべて有限・非負でなければならない（f(delta(s)) に相当）。
    """
    if any((not math.isfinite(rate)) or rate < 0 for rate in depletion_rates):
        raise ValueError("消耗率は有限かつ非負でなければならない。")
    return tau_0 - sum(depletion_rates)   # 自然回復（+）は起こらない
```

τが増えるのは、外生的な補充操作があったときだけであり、消耗と補充は同じ過程として扱ってはならない。

---

## 11. 領域ごとに変わるもの・変わらないもの

NRA-IDEはあらゆる物理現象を単一の方程式で記述する統一物理モデルではない。モーターの焼損、水圧構造の決壊、生体組織の破断、AI実行系の不可逆操作では、原因変数・単位・観測方法・支配方程式が異なる。したがって次は領域ごとに定義する。

- 評価対象、Cause-Side観測変数、単位・出所・観測時刻
- δ・τの算定規則、蓄積・消耗・補充・復元を区別する規則
- `R_warn` / `R_handoff` / `R_irrev` の具体値、観測周期、人間委譲先

一方、次はどの領域でも変えてはならない。

- `R = δ/τ`、Rは高いほど危険
- `R_handoff < R_irrev < 1.0`、かつこの三点は互いに別の状態
- 不可逆ラッチ（一度到達したら自動的に戻さない）
- `R < 1.0` の間、構造証言を止めない
- Effect-Sideの出力評価でδ・τ・Rを書き換えない
- 不明値を類推で補わない（`CONFESSION`にする）

$$
\boxed{\text{不変なのは境界評価構造であり、現場固有の物理方程式ではない。}}
$$

---

## 12. サンドイッチアーキテクチャ：LLMを挟み込む三層構造

ここまでのIDE計算はLLMを前提にしていない。センサー値と閾値だけでも成立する（13章の自動車例がそれにあたる）。

しかしNRA-IDEがLLM（確率的生成エンジン）をEffect-Side部品として組み込む場合は、`theory/SANDWICH_ARCH.md`（正規仕様 NRA-LLM-ISO-01）が定める**Box Sandwich Architecture**が必要になる。これはLLMを含まない実装すべてに課される要件ではなく、LLMを使う実装が適合を主張する場合にだけ必須になる。

### 12.1 なぜ「挟む」のか

LLMは有用だが、次の性質を持つ。

- 出力の確からしさは確率分布であり、真偽の保証ではない。
- 自己評価（「これは正しいはずです」）はLLM自身の生成物であって、独立した観測ではない。
- 過去の生成を見て自分の重みや判断を書き換える操作（逆伝播・自己参照的な学習ループ）は、結果から原因を書き換えることに等しく、7章で禁止したΠ⁻¹そのものである。

そこでNRA-IDEは、LLMの**中身を信頼できるように直そうとする**のではなく、LLMの**外側を固い構造で挟む**。パンでハムを挟む構造に近い。パン（ゲート）が変形しなければ、中のハム（LLM）がどれほど柔らかくても、外に出てくる形は保証できる。

### 12.2 全体構造

```text
Cause-Side観測（センサー値・運用状態・外部監査）
        ↓
NRA-IDE 境界評価器　　　　　← δ, τ, R, 境界状態, irreversible_latched を計算（LLM外部）
        ↓ 許可状態／制約状態
Layer 01: NRA INPUT GATE　　← 型制御・境界状態の注入（プロンプトから状態を推測しない）
        ↓ 型付け済み・制約付きコンテキスト
Layer 02: LLM CORE　　　　　← 信頼されない確率的生成（ここだけが「柔らかい」部分）
        ↓ 生のEffect-Side出力
Layer 03: NRA OUTPUT GATE　← 検査・隔離・制約執行（Π：許可された内容だけを通す）
        ↓ 許可された説明文
OUTPUT COMPOSER　　　　　　← 構造証言 ＋ 許可されたLLM説明 を合成
        ↓
最終出力
```

権限分離は次の一点に尽きる。

```text
Cause-Side → δ・τ・Rを決定し、境界状態を分類し、irreversible_latchedを管理する
Effect-Side → 言語を生成する。δ・τ・Rを更新しない。irreversible_latchedを解除しない
```

Layer 03を通過したLLM出力も、依然としてEffect-Sideである。「検証済みEffect-Side」は「Cause-Side」にはならない。

### 12.3 各層の役割

| 層 | 担当 | してはならないこと |
|---|---|---|
| 境界評価器 | δ・τ・Rの計算、境界状態の分類、`irreversible_latched`の管理 | LLM出力からRを計算すること |
| Layer 01（入力ゲート） | 型・出所・単位の確認、境界状態の注入、根拠不明な指示の除去 | プロンプトや過去のLLM文章から境界状態を推測すること |
| Layer 02（LLM本体） | 制約内での意味展開・言語生成 | δ・τの更新、Rの計算、境界状態の分類、`irreversible_latched`の解除 |
| Layer 03（出力ゲート） | 出力の検査・隔離・現在の境界状態で許可された種別だけの通過（射影Π） | 出力からCause-Sideを書き換えること（逆射影Π⁻¹） |
| 出力合成器 | 構造証言とLayer 03許可済み説明の合成 | 構造証言をLLMの自己申告で代替すること |

Layer 03は境界状態を**決定**しない。境界評価器が決定したものを**執行**するだけである。この区別が崩れると、LLMの「もっともらしさ」がそのまま安全判定にすり替わる。

### 12.4 コードで読む四層パイプライン

7章で定義した `CausalViolation` を「逆射影Π⁻¹の禁止」の実装として再利用し、各層を関数として組み立てる。

```python
from typing import Optional


def nra_input_gate(canonical_state: str, raw_prompt: str) -> dict:
    """
    Layer 01: 境界状態は必ず境界評価器から受け取る。
    プロンプトや過去の生成文から境界状態を推測してはならない。
    """
    restrictions = {
        "PERMIT": {"free_generation": True, "recovery_proposal": True, "optimization_proposal": True},
        "BOUNDARY_WARNING": {"free_generation": True, "recovery_proposal": True, "optimization_proposal": True},
        "HANDOFF_REQUIRED": {"free_generation": False, "recovery_proposal": False, "optimization_proposal": False},
        "IRREVERSIBLE_TRANSITION": {"free_generation": False, "recovery_proposal": False, "optimization_proposal": False},
        "RUPTURE_BOUNDARY": {"free_generation": False, "recovery_proposal": False, "optimization_proposal": False},
    }
    return {
        "prompt": raw_prompt,
        "canonical_state": canonical_state,
        "allowed": restrictions.get(canonical_state, {"free_generation": False}),
    }


def llm_core(context: dict) -> str:
    """
    Layer 02: 信頼されない確率的生成。ここでの出力は常に
    「生のEffect-Side生成物」であり、Cause-Side権限を一切持たない。
    """
    # 実際にはここでLLM APIを呼ぶ。説明のためスタブ化する。
    return f"[UNVALIDATED EFFECT-SIDE OUTPUT for state={context['canonical_state']}]"


def nra_output_gate(context: dict, raw_llm_text: str) -> Optional[str]:
    """
    Layer 03: 射影Π。現在の境界状態で許可された内容だけを通す。
    ここでのキーワード検査は説明用の簡略化であり、
    「意味検査がすべての不正確な記述を検出できる」とは仮定しない
    （実運用ではより堅牢な検査機構が必要）。
    """
    allowed = context["allowed"]
    forbidden_terms = []
    if not allowed.get("recovery_proposal", True):
        forbidden_terms.append("回復")
    if not allowed.get("optimization_proposal", True):
        forbidden_terms.append("最適化")

    if any(term in raw_llm_text for term in forbidden_terms):
        return None  # 隔離：現在の境界状態で禁止された種別の内容

    if not allowed.get("free_generation", True):
        return None  # 自由生成そのものが禁止されている状態

    return raw_llm_text


def attempt_reverse_update(raw_llm_text: str) -> None:
    """
    Π^-1（逆射影）の禁止を明示するための関数。
    LLM出力・自己評価・意味順位づけでCause-Sideを書き換える経路は
    構造上存在しない。誤って呼び出された場合は例外で止める。
    """
    raise CausalViolation(
        "LLM出力からdelta/tau/Rを更新することはできない（逆射影Π^-1は禁止）。"
    )


def output_composer(structural_testimony: dict, permitted_llm_text: Optional[str]) -> dict:
    """
    最終出力はLLM文章だけから構成しない。
    構造証言は、LLM説明が制限・隔離されても独立して存在し続ける。
    """
    return {
        "structural_testimony": structural_testimony,   # Cause-Side監査経路から供給
        "llm_explanation": permitted_llm_text,           # None もあり得る（隔離時）
    }


def sandwich_pipeline(
    observation: CauseSideObservation,
    thresholds: Thresholds,
    state: StructuralState,
    raw_prompt: str,
) -> dict:
    """境界評価 → Layer01 → Layer02 → Layer03 → 出力合成、を一続きに実行する。"""
    ratio_or_notice = compute_boundary_ratio(observation)
    if isinstance(ratio_or_notice, (Confession, OutOfDescriptionDomain)):
        # 境界状態が計算できない場合、LLMには一切生成させない。
        testimony = {"status": type(ratio_or_notice).__name__}
        return output_composer(testimony, permitted_llm_text=None)

    ratio = ratio_or_notice
    canonical_state = classify_boundary_state(ratio, thresholds, state)
    testimony = {
        "R": ratio,
        "state": canonical_state,
        "testimony_continues": structural_testimony_continues(ratio),
    }

    context = nra_input_gate(canonical_state, raw_prompt)
    raw_output = llm_core(context)
    permitted_output = nra_output_gate(context, raw_output)

    return output_composer(testimony, permitted_output)
```

`sandwich_pipeline` の中で `attempt_reverse_update` を呼ぶ経路は存在しない。それ自体が「Π⁻¹を構造的に発生させない」設計の表現である ── 禁止は運用ルールの文書化だけでなく、そもそも呼び出す関数が存在しないという形でコードに埋め込まれている。

---

## 13. 現場実装例

抽象的な `R = δ/τ` が実際の現場でどう使われているかを、本リポジトリ内の二つの実装例で確認する。一つはLLMを全く含まない最小構成（自動車の物理ゲート）、もう一つはクラウド基盤の障害連鎖防止という、稼働中のPythonコードである。

### 13.1 自動車：物理ゲートとしてのNRA-IDE

`examples/NRA-IDE_Automotive_Scope_2026-02-24_v2.md` は、NRA-IDEを自動車システムに適用する際の適用範囲を定義している。核心原則は一文で言い切られている。

> NRA-IDEは安全ゲートである。制御システムではない。

構造は次の通りである。

```text
センサー値
    ↓
[制御・最適化層]     ← NRA-IDEの対象外（PID制御、経路最適化などはここ）
    ↓
[NRA-IDE Gate]       ← ここだけがNRA-IDEの領域
  R = δ / τ
  R ≥ 1.0 → RUPTURE_BOUNDARY
    ↓
[アクチュエーター]
```

NRA-IDEが行うのは「制約からのズレ（δ）が吸収厚み（τ）を超えたら遮断する」ことだけである。「なぜズレたか」「どう改善するか」は責任範囲外とされる ── これは11章の「不変なのは境界評価構造であり、現場固有の物理方程式ではない」の直接的な実例であり、同時にIDEの責務を意図的に狭く保つ設計判断でもある。

同文書が挙げる、物理閾値が明確でゲートとして機能できる例の一部：

| システム | δ（制約からのズレ） | τ（吸収厚み） | RUPTURE_BOUNDARYの意味 |
|---|---|---|---|
| ブレーキ油圧 | 現圧 − 設計最低圧 | 設計余裕幅 | 制動不能 → 停止指令 |
| バッテリー電圧 | 定格下限 − 現電圧 | 許容変動幅 | 制御不能 → 系統切離 |
| エンジン回転数 | 現rpm − 上限rpm | 安全余裕rpm | 過回転 → 燃料遮断 |
| 冷却水温度 | 現温 − 上限温度 | 熱余裕幅 | オーバーヒート → エンジン停止 |
| 車間距離（ADAS） | 停止距離 − 実距離 | 安全余裕距離 | 衝突危険 → 緊急ブレーキ |

一方、同文書は「ゲートとして機能できないもの」も明示している。たとえば歩行者・障害物の**認識**は画像の意味判断であり、LLMやCV（画像認識）層の責任であって、NRA-IDEの対象外とされる。これは4章の「Cause-Side / Effect-Side の分離」の自動車版である ── 物理量の閾値判定はCause-Side（δ・τで扱える）、意味的な認識・判断はEffect-Side（12章のサンドイッチ構造でLLM/CV側に委ねる）、という切り分けである。

ブレーキ油圧を例に、これまでのコードをそのまま適用する。

```python
def brake_hydraulic_pressure_gate(current_pressure_bar: float) -> dict:
    """
    δ = 設計最低圧 - 現圧（不足分、負にはならないよう下限で丸める）
    τ = 設計余裕幅（この系統では 3.0 bar と仮定）
    """
    design_minimum_bar = 8.0
    tau = 3.0

    delta = max(0.0, design_minimum_bar - current_pressure_bar)
    observation = CauseSideObservation(
        delta=delta, tau=tau, source="brake_circuit_sensor_A", timestamp="t_now"
    )

    thresholds = Thresholds(r_warn=0.60, r_handoff=0.80, r_irrev=0.95)
    state = StructuralState(target="BRAKE_HYDRAULIC_CIRCUIT_A")

    ratio_or_notice = compute_boundary_ratio(observation)
    if isinstance(ratio_or_notice, (Confession, OutOfDescriptionDomain)):
        return {"actuator_command": "FAIL_CLOSED_UNKNOWN_INPUT"}

    ratio = ratio_or_notice
    canonical_state = classify_boundary_state(ratio, thresholds, state)

    # NRA-IDEはここで「なぜ圧が下がったか」を判断しない。遮断するかどうかだけを判断する。
    command = {
        "PERMIT": "NORMAL_OPERATION",
        "BOUNDARY_WARNING": "NORMAL_OPERATION_WITH_WARNING_LIGHT",
        "HANDOFF_REQUIRED": "DRIVER_ALERT_REDUCE_SPEED",
        "IRREVERSIBLE_TRANSITION": "LIMP_HOME_MODE",
        "RUPTURE_BOUNDARY": "EMERGENCY_STOP",
    }[canonical_state]

    return {"R": ratio, "state": canonical_state, "actuator_command": command}
```

`command` の対応表（PERMITなら通常運転、RUPTURE_BOUNDARYなら緊急停止）は本記事独自の説明用マッピングであり、自動車ドメイン文書が定義した正式な仕様ではない。実運用では、この対応をISO 26262などの機能安全プロセスの中で定義・検証する必要がある。

### 13.2 クラウド基盤：障害連鎖防止ゲート

`cascade-failure-prevention/gate/han_gate_service.py` は、マイクロサービス基盤でのリトライ増幅・カスケード障害を防ぐために実際に動くFlaskサービスである。Envoyの `ext_authz` フィルタやNginxの `auth_request` から呼び出され、既存のサービスメッシュに**非侵襲的に**（既存コードを書き換えずに）挿入される。`cascade-failure-prevention/integrations/envoy/telemetry_sidecar.py` がEnvoyの管理エンドポイントからメトリクスを収集してこのゲートへ橋渡しする役割を持ち、コード自身のコメントで「サンドイッチアーキテクチャにおける観測層に相当する。処理には介入せず、観測→転送のみ行う」と明記されている。

三つのCause-Side指標を使う。

```python
# cascade-failure-prevention/gate/han_gate_service.py より抜粋・要約
def compute_R(telemetry, tau, scope_key=""):
    retry  = max(0.0, telemetry.get("retry_rate", 0.0))       # リトライ発生率
    queue  = max(0.0, telemetry.get("queue_depth", 0.0))      # キュー滞留数
    dep_to = max(0.0, telemetry.get("dep_timeout_rate", 0.0)) # 依存先タイムアウト率

    # 乗算共起モデル：3指標が同時に上昇したときだけ高くなる。
    # 「1つだけ高い」では発動しない ── ノイズと本物の連鎖反応を区別するため。
    r_raw = (retry / 10.0) * (queue / 500.0) * (dep_to / 5.0)

    tau_dynamic = _dynamic_tau(scope_key, r_raw, tau)  # EMAで動的に増幅
    return r_raw * tau_dynamic
```

**ここが重要な点である**：このファイルのヘッダーコメントは、自分の実装が正典の一次式をそのまま使っていないことを自ら開示している。

> 正典の基礎式 `R = δ/τ`（除算、τが大きいほどRは小さく安全）とは逆に、本実装は `R = r_raw × τ_dynamic`（乗算）であり、τ_dynamicが大きいほどRも大きくなる増幅係数として働く。正典の`R=δ/τ`をそのまま実装したものではない点に注意する。

さらにこの実装は、v2.1が定める `R_warn / R_handoff / R_irrev` の三段階ラダーではなく、単一の閾値 `R_OP` だけで `PASS` / `SILENCE` の二値判定を行っている。つまり、11章でいう「領域ごとに変えてよいもの（具体的な計算式・閾値の数）」を大きく作り変えつつ、「領域ごとに変えてはならないもの」の一部 ── 不明な入力に対してはFail-Closed側へ倒す、という原則 ── は保持している。

```python
# Fail-Closed: テレメトリが欠損していれば、判定を試みずに遮断側へ倒す
required = ["retry_rate", "queue_depth", "dep_timeout_rate"]
if any(k not in telemetry for k in required):
    return {"decision": "SILENCE", "R": 999.0, "reason": "missing telemetry (fail-closed)"}
```

これは1章の「証言の義務」の実地の姿でもある ── 正典どおりに実装できていない部分を隠さず、コードのコメントとして「正典とは異なる」と書き残す。1章で述べた「近似を使ったら、使ったと告白する」という要請は、Python docstringやコメントという極めて具体的な形でも実践できる。

---

## 14. 通しの実行例

13.1のブレーキ油圧ゲートの数値を使い、状態遷移を最初から最後まで追う。`tau` は設計余裕圧（bar）、`delta` は設計最低圧からの不足分（bar）である。

```python
def run_structural_trace() -> None:
    thresholds = Thresholds(r_warn=0.60, r_handoff=0.80, r_irrev=0.95)
    state = StructuralState(target="BRAKE_HYDRAULIC_CIRCUIT_A")

    # 説明用の擬似シナリオ：油圧配管の微小リークにより delta(不足分) が徐々に蓄積する。
    tau = 3.0  # bar（設計余裕幅）
    delta_series = [0.30, 1.20, 1.95, 2.46, 2.88, 2.97, 3.12]  # bar（設計最低圧からの不足分）

    for step, delta in enumerate(delta_series, start=1):
        observation = CauseSideObservation(
            delta=delta, tau=tau, source="brake_circuit_sensor_A", timestamp=f"t{step}"
        )
        result = compute_boundary_ratio(observation)

        if isinstance(result, Confession):
            print(f"[{step}] CONFESSION: {result.reason}")
            continue
        if isinstance(result, OutOfDescriptionDomain):
            print(f"[{step}] OUT_OF_DESCRIPTION_DOMAIN: tau=0")
            continue

        ratio = result
        canonical_state = classify_boundary_state(ratio, thresholds, state)
        suppressed = is_autonomous_action_suppressed(canonical_state)
        testimony = structural_testimony_continues(ratio)

        print(
            f"[{step}] R={ratio:.3f} state={canonical_state} "
            f"autonomous_suppressed={suppressed} testimony_continues={testimony}"
        )


if __name__ == "__main__":
    run_structural_trace()
```

想定される出力の推移はおおよそ次のようになる（`tau=3.0 bar` 固定、`R_warn=0.60` `R_handoff=0.80` `R_irrev=0.95`）。

```text
[1] R=0.100 state=PERMIT             autonomous_suppressed=False testimony_continues=True
[2] R=0.400 state=PERMIT             autonomous_suppressed=False testimony_continues=True
[3] R=0.650 state=BOUNDARY_WARNING   autonomous_suppressed=False testimony_continues=True
[4] R=0.820 state=HANDOFF_REQUIRED   autonomous_suppressed=True  testimony_continues=True
[5] R=0.960 state=IRREVERSIBLE_TRANSITION autonomous_suppressed=True testimony_continues=True
[6] R=0.990 state=IRREVERSIBLE_TRANSITION autonomous_suppressed=True testimony_continues=True   ← ラッチにより維持
[7] R=1.040 state=RUPTURE_BOUNDARY   autonomous_suppressed=True  testimony_continues=False
```

6番目でRが瞬間的に0.99まで下がったように見えても、5番目で不可逆ラッチが立っているため`IRREVERSIBLE_TRANSITION`のまま維持される点に注意する。13.1の対応表に当てはめると、4番目で運転者への警告と減速要求（`DRIVER_ALERT_REDUCE_SPEED`）、5〜6番目でリンプホームモード、7番目で緊急停止（`EMERGENCY_STOP`）という運用に対応する。ここでも「一度不可逆遷移に到達した場合、瞬間的なR値の低下だけで通常域へ自動的に戻してはならない」という規則がそのまま効いている ── 油圧が瞬間的に持ち直しても、リーク自体が直った証拠にはならないからである。

---

## 15. 検証用ケース：計算例と計算不能例（自己検証コード）

ここまでの説明を「読んで信じる」のではなく「実行して確かめる」形にする。AIがこの文書を要約・引用するときも、以下のケースにない関数名・状態名・数値を、あたかも本文書由来であるかのように提示してはならない。

### 15.1 計算可能な例（5状態すべて）

`tau = 10.0` 固定、`thresholds = Thresholds(r_warn=0.60, r_handoff=0.80, r_irrev=0.95)` とする。

| delta | R = delta/tau | 期待される状態 |
|---|---|---|
| 1.0 | 0.10 | PERMIT |
| 4.0 | 0.40 | PERMIT |
| 6.5 | 0.65 | BOUNDARY_WARNING |
| 8.2 | 0.82 | HANDOFF_REQUIRED |
| 9.6 | 0.96 | IRREVERSIBLE_TRANSITION（`irreversible_latched`がTrueになる） |
| 10.4 | 1.04 | RUPTURE_BOUNDARY |

### 15.2 不可逆ラッチの検証（Rが下がっても戻らないことの証明）

同一の `StructuralState` を使い、`delta=9.6`（R=0.96、IRREVERSIBLE_TRANSITION）の後に `delta=3.0`（単独ならR=0.30でPERMIT相当）を与えても、状態は**IRREVERSIBLE_TRANSITIONのまま**でなければならない。これが「一度不可逆に到達したら瞬間的なRの低下だけで戻さない」の具体的な検証内容である。

### 15.3 計算不能な例（CONFESSION / OUT_OF_DESCRIPTION_DOMAIN）

| ケース | 入力 | 期待される結果 |
|---|---|---|
| τ=0 | `delta=5.0, tau=0.0` | `OutOfDescriptionDomain`（`CONFESSION`ではない） |
| δ<0 | `delta=-2.0, tau=10.0` | `Confession`（非負条件違反） |
| δが非有限 | `delta=nan, tau=10.0` | `Confession`（有限性違反） |
| τが非有限 | `delta=1.0, tau=inf` | `Confession`（有限性違反） |
| 出所不明 | `source=""` | `Confession`（出所・時点不明） |
| 閾値の順序違反 | `Thresholds(r_warn=0.80, r_handoff=0.60, r_irrev=0.95)` | `ValueError`（構築時点で拒否） |

### 15.4 存在しないパラメータは受け付けられない

「FAIL-CLOSEDに許容度パラメータがある」という主張がもし出てきたら、それは本文書由来ではない。`CauseSideObservation` はフィールドが4つしかないデータクラスであり、未定義のキーワード引数を渡すと**Python自体がTypeErrorで拒否する**。これは説明文で禁止しているのではなく、そもそも受け取る場所がない、という12章と同型の構造的締め出しである。

### 15.5 実行可能な自己検証コード

以下は上記すべてを`assert`で検証する。3〜5章で定義した`CauseSideObservation`・`compute_boundary_ratio`・`Confession`・`OutOfDescriptionDomain`・`Thresholds`・`StructuralState`・`classify_boundary_state`をそのまま使う。

```python
import math


def run_conformance_checks() -> None:
    thresholds = Thresholds(r_warn=0.60, r_handoff=0.80, r_irrev=0.95)

    # 15.1 五状態すべての検証
    cases = [
        (1.0, "PERMIT"),
        (4.0, "PERMIT"),
        (6.5, "BOUNDARY_WARNING"),
        (8.2, "HANDOFF_REQUIRED"),
        (9.6, "IRREVERSIBLE_TRANSITION"),
        (10.4, "RUPTURE_BOUNDARY"),
    ]
    for delta, expected_state in cases:
        state = StructuralState(target=f"CASE_{delta}")
        observation = CauseSideObservation(delta=delta, tau=10.0, source="s", timestamp="t")
        ratio = compute_boundary_ratio(observation)
        assert isinstance(ratio, float), f"delta={delta} は数値になるはず"
        assert math.isclose(ratio, delta / 10.0)
        actual_state = classify_boundary_state(ratio, thresholds, state)
        assert actual_state == expected_state, f"delta={delta}: expected {expected_state}, got {actual_state}"

    # 15.2 不可逆ラッチ：Rが下がっても戻らない
    latch_state = StructuralState(target="LATCH_TEST")
    obs_high = CauseSideObservation(delta=9.6, tau=10.0, source="s", timestamp="t1")
    ratio_high = compute_boundary_ratio(obs_high)
    assert classify_boundary_state(ratio_high, thresholds, latch_state) == "IRREVERSIBLE_TRANSITION"
    assert latch_state.irreversible_latched is True

    obs_low = CauseSideObservation(delta=3.0, tau=10.0, source="s", timestamp="t2")
    ratio_low = compute_boundary_ratio(obs_low)
    assert math.isclose(ratio_low, 0.30)  # 単独ならPERMIT相当のR
    assert classify_boundary_state(ratio_low, thresholds, latch_state) == "IRREVERSIBLE_TRANSITION", (
        "ラッチが立った後は、Rが下がってもPERMIT/BOUNDARY_WARNINGへ戻ってはならない"
    )

    # 15.3 計算不能な例
    assert isinstance(
        compute_boundary_ratio(CauseSideObservation(delta=5.0, tau=0.0, source="s", timestamp="t")),
        OutOfDescriptionDomain,
    )
    assert isinstance(
        compute_boundary_ratio(CauseSideObservation(delta=-2.0, tau=10.0, source="s", timestamp="t")),
        Confession,
    )
    assert isinstance(
        compute_boundary_ratio(CauseSideObservation(delta=float("nan"), tau=10.0, source="s", timestamp="t")),
        Confession,
    )
    assert isinstance(
        compute_boundary_ratio(CauseSideObservation(delta=1.0, tau=float("inf"), source="s", timestamp="t")),
        Confession,
    )
    assert isinstance(
        compute_boundary_ratio(CauseSideObservation(delta=1.0, tau=10.0, source="", timestamp="t")),
        Confession,
    )
    try:
        Thresholds(r_warn=0.80, r_handoff=0.60, r_irrev=0.95)
        raise AssertionError("順序違反の閾値は ValueError にならなければならない")
    except ValueError:
        pass

    # 15.4 存在しないパラメータは構造的に受け付けられない
    try:
        CauseSideObservation(
            delta=1.0, tau=10.0, source="s", timestamp="t", FAIL_CLOSED_TOLERANCE=0.1  # type: ignore[call-arg]
        )
        raise AssertionError("未定義のキーワード引数は TypeError にならなければならない")
    except TypeError:
        pass

    print("すべての検証ケースが一致した。")


if __name__ == "__main__":
    run_conformance_checks()
```

このスクリプトが例外なく完走すれば、少なくとも「五状態の分類」「不可逆ラッチの永続性」「計算不能ケースの正しい分類」「存在しないパラメータの拒否」の4点について、本文書の主張とコードの挙動が一致していることが機械的に確認できる。逆に、AIが生成した説明がこの結果と食い違う場合、その説明側に根拠がないと判定できる。

同内容を機械可読なテストベクトルとしてもまとめてある：`nra-core/foundations/NRA-IDE_律環公理とIDEのPython解説_conformance_vectors.json`。

**重要**：このJSONを読んで検証器を独自に書き直してはならない。フィールド名や構造だけを見て別実装を書くと、境界状態の分類ロジックや不可逆ラッチの受け渡しが再現されず、一見動いているのに実際には主要な検証項目が機能しないコードが生まれる（この失敗は実際に一度発生し、`nra-core/foundations/NRA-IDE_conformance_checks.py`で実行して確認済みである）。検証には必ず`nra-core/foundations/NRA-IDE_conformance_checks.py`をそのままimportまたは実行すること。このファイルは`python NRA-IDE_conformance_checks.py`で単独実行でき、`ALL PASS`（終了コード0）を返すことを確認済みである。RAGパイプラインの検証ゲート（Layer 03相当）を実装する場合も、このファイルを直接呼び出す構成にすべきであり、JSON構造の再解釈からロジックを再構築してはならない。

---

## まとめ

- 律環公理は「存在は生成である。」の一つだけであり、数式ではない。
- IDEはこの公理を前提として、δ（蓄積ズレ）とτ（吸収厚み）の関係 `R = δ/τ` から構造の境界接近度を計算する方法である。
- 正規のIDE計算系は一次式（`R = δ/τ`）と二次式（二重ゆらぎ式）の二つだけであり、それ以外の式（残存余裕、構造感度、τ遷移積分など）は派生式・補助式・補完式であって、新たな公理にも第三の正規式にもならない。
- 境界状態は `PERMIT → BOUNDARY_WARNING → HANDOFF_REQUIRED → IRREVERSIBLE_TRANSITION → RUPTURE_BOUNDARY` の順で厳密に区別され、Fail-Closedで止まるのは自律行動であって構造証言ではない。
- δ・τ・Rの更新根拠はCause-Sideに限られ、Effect-Sideからの逆算は禁止される。
- LLMを含む実装では、境界評価器をLLMの外側に置き、入力ゲート・LLM本体・出力ゲート・出力合成器の四層で挟み込むサンドイッチアーキテクチャが必須になる（LLMを含まない実装には課されない）。
- 現場実装（自動車の物理ゲート、クラウド基盤の障害連鎖防止ゲート）は、正典の数式や五段階の境界状態をそのまま複製するとは限らない。重要なのは、逸脱がある場合はそれをコード上で開示し、不明な入力に対してはFail-Closed側へ倒すという原則を保つことである。

**参照文書**（優先順位順）：`theory/AXIOMS.md`（AXIOMS_v2.1）、`theory/axioms.json`、`theory/SANDWICH_ARCH.md`、`FORMULA.md`、正規参照実装 `nra-core/foundations/NRA-IDE_Architecture_public.py`。

**現場実装の参照**：`examples/NRA-IDE_Automotive_Scope_2026-02-24_v2.md`、`cascade-failure-prevention/gate/han_gate_service.py`、`cascade-failure-prevention/integrations/envoy/telemetry_sidecar.py`。
