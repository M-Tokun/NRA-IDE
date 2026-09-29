# NRA-IDE 辞書（日本語版）

**Version:** 1.0（草案）  
**Author:** M-Tokuni  
**Document role:** NRA-IDEの用語・記号・固定名を引くための辞書。正典の定義を作らず、変えない  
**対になる英語版:** [NRA-IDE_Dictionary_EN.md](./NRA-IDE_Dictionary_EN.md)

---

## 0. この辞書について

### 0.1 位置付け

本書は、NRA-IDEで使う用語・記号・固定名（API名・出力名）の意味、書き方、使ってよい先、混同しやすい点を、一か所で引けるようにした辞書である。本書は正典の定義を作らず、変えない。意味または記号の予約が競合する場合は、`theory/AXIOMS.md` §16の優先順位と `FORMULA.md` §7に従う。本書は独自の予約権限を持たない。

利用者もAIも、用語や記号を書く前に本書を引く。新しい混同に気づいたら、その見出しの「混同注意」に日付付きで追記し、5章に一行加える。

### 0.2 引き方

| 探したいもの | 引く部 |
|---|---|
| 日本語の用語 | 1章 用語の部（五十音順） |
| 記号（ $\delta$ 、 $\mathsf{Decl}$ 、 $\Delta$ など） | 2章 記号の部 |
| 英語の固定名（`delta`、`irreversible_latched` など） | 3章 固定名の部 |
| 添字・ラベルの約束 | 4章 |
| いつ何を混同したか | 5章 混同の記録 |

各見出しには、英語版と共通の**見出しID**（例：`absorption-thickness`）を付けてある。日本語版と英語版の同じ見出しは、このIDでつながる。

### 0.3 見出しの欄

| 欄 | 内容 |
|---|---|
| 記号・固定名 | 数学での表示と、API・出力での名前 |
| 型・単位 | 構造量（Cause-Side）、評価出力、評価状態、計器、対象状態、宣言、写像、添字、記録 のいずれか。単位 |
| 意味 | 正典の定義の要約と定義元。定義は定義元を正とする |
| 出所・使ってよい先・使ってはならない先 | 値の出どころと、入力にしてよい先・いけない先 |
| 書き方 | 本リポジトリでの書き方 |
| 混同注意 | 過去に混同した点（日付付き） |
| 受け取り方の違い | 英語の読み手が別の意味に取りやすい点。【確認済み】【未確認】の印を付ける |
| 関連 | 関連する見出し |

### 0.4 名前の採用順

1. `theory/AXIOMS.md` の正規表記
2. `theory/axioms.json` の機械可読名
3. 正規参照実装（`nra-core/foundations/NRA-IDE_Architecture_public.py`）の公開引数・出力フィールド
4. `FORMULA.md` の記号予約
5. 既存の名前がない場合だけ、新しい固定名を提案する

実装の中だけで使う一時変数（例：参照実装の内部の `ratio`）は、公開の固定名とは区別する。

### 0.5 書き方の一般規則

**書体**（国際規格 ISO 80000-2 の書き方に従う）

| 種類 | 書体 | 例 |
|---|---|---|
| 変数・物理量 | 斜体 | $\delta$ 、 $\tau$ 、 $q_n$ 、 $x$ |
| 数学演算子・定義済み関数 | 立体 | $\mathrm{d}$ （微分）、 $\partial$ 、 $\int$ 、 $\sum$ 、 $\prod$ 、 $\sin$ 、 $\ln$ 、 $\exp$ 、 $\lim$ 、 $\max$ |
| 変数を表す添字 | 斜体 | $\sum_i x_i$ の $i$ 、 $\tau^{[e]}$ の $e$ |
| 名前・説明を表す添字（ラベル） | 立体 | $R_{\mathrm{warn}}$ 、 $\tau_{\mathrm{upper}}$ 、 $q^{\mathrm{temp}}$ |
| 次元 | サンセリフの立体大文字 | 長さ $\mathsf{L}$ 、質量 $\mathsf{M}$ 、時間 $\mathsf{T}$ 、電流 $\mathsf{I}$ 、熱力学温度 $\mathsf{\Theta}$ 、物質量 $\mathsf{N}$ 、光度 $\mathsf{J}$ |
| 次元の書き方 | 大括弧 | $[F]=\mathsf{L}\,\mathsf{M}\,\mathsf{T}^{-2}$ 、無次元量は $[Z]=1$ |

**本リポジトリの規則**：同一文書または同一実装の中では、字体・大小文字・書体・装飾の違いだけで、別の意味の記号を区別しない。別の意味には別の基底名を使う。規則の対象外は、標準の数学演算子、ラベル、次元の記号である。この規則は `FORMULA.md` §7へ提示する予定であり、現時点では規範ではない。ただし、遷移位相 $\mathrm{Phase}$ と $\Phi(x)$ の区別については、FORMULA §7に一文がある（v2.4）。

**正典の現在の書き方との違い（未反映）**：FORMULA.md §4.7の微分は斜体の $d$ 、§5.2の次元の記号は斜体の $X$ 、 $T$ である。上の書体の規則とは違う。正典を改める場合は、差分④で個別に提示する。FORMULA.md §5の残差 $r$ と境界接近比 $R$ は大小だけの区別であり、扱い（改名するか、規則の対象外にするか）は差分④で判断する。

### 0.6 「受け取り方の違い」の印

- 【確認済み】：利用者が確認した内容
- 【未確認】：AIの案。利用者の確認を待つ

---

## 1. 用語の部（五十音順）

<a id="temporary-reversible-deviation"></a>
### 一時的な可逆成分（いちじてきなかぎゃくせいぶん）
- 英語版：[Temporary Reversible Deviation](./NRA-IDE_Dictionary_EN.md#temporary-reversible-deviation)
- 記号・固定名： $q^{\mathrm{temp}}_n$ ／ `temporary_reversible_deviation`
- 型：対象状態（可逆成分 $q_n$ の一部）
- 意味：作用や条件で一時的に狭まった受け止め幅を、ズレの側に数えた量。条件が去れば0に戻る。定義元：AXIOMS §7 解釈境界コメント（一時的な厚みの減少は可逆成分として数える）、FORMULA §0.5.3
- 書き方：実効厚みから差し引かない。 $\mathsf{Alloc}$ で作用に計上し、 $q_n$ に含める
- 混同注意：「一時的な厚みの減少」と呼んでいた（記号 $\mu_n$ ）。名前は厚みなのに、実際はズレの側に数える量だったため、改名した（2026-09-29）
- 受け取り方の違い【未確認】：英語の reversible は、熱力学の可逆過程と読まれやすい。ここでは「条件が去れば戻る」の意味
- 関連：[可逆成分](#reversible-deviation)、[実効厚み](#effective-thickness)

<a id="entropy-quantity"></a>
### エントロピー相当量（えんとろぴーそうとうりょう）
- 英語版：[Entropy Quantity](./NRA-IDE_Dictionary_EN.md#entropy-quantity)
- 記号・固定名： $\mathrm{entropy}$ ／ `entropy_quantity`
- 型：補助構造量（任意、Cause-Side）
- 意味：ドメイン固有のエントロピー相当量。ドメインが定義・算出規則を明記した場合だけ使う。定義元：AXIOMS §4.5、FORMULA §7
- 出所：Cause-Side観測、評価前に固定した変換規則
- 使ってはならない先：評価出力（ $R$ 、正規状態、不可逆ラッチ、その集約）から得ること
- 書き方： $S$ で書かない（ $S$ は[構造感度](#structural-sensitivity)）。離散的な遷移で次の段階へ持ち越さない残差は別の概念で、 `entropy_export` と呼ぶ（熱力学的エントロピーの測定値ではない。AXIOMS §4.5、docs 08章）
- 受け取り方の違い【未確認】：熱力学のエントロピーの測定値と読まれやすい
- 関連：[構造感度](#structural-sensitivity)

<a id="reversible-deviation"></a>
### 可逆成分（かぎゃくせいぶん）
- 英語版：[Reversible Deviation](./NRA-IDE_Dictionary_EN.md#reversible-deviation)
- 記号・固定名： $q_n$ ／ `reversible_deviation`
- 型：対象状態
- 意味：蓄積ズレのうち、作用を除けば基準側へ戻る部分。定義元：AXIOMS §4、FORMULA §0.5.3
- 書き方： $q_n=\sigma(o_n)-p_n$ として定まる（FORMULA §0.5.3、導出文書P5）
- 混同注意：以前の案では「可逆進入」と呼んでいた。正典の語は「可逆成分」（2026-09-28）
- 受け取り方の違い【未確認】：「可逆」を「値が戻れば構造も戻る」と読まない。値が戻っても経路履歴は戻らない（導出文書 命題2b）
- 関連：[残留ズレ](#residual-deviation)、[蓄積ズレ](#accumulated-deviation)

<a id="complete-rupture-boundary"></a>
### 完全破断境界（かんぜんはだんきょうかい）
- 英語版：[Complete Rupture Boundary](./NRA-IDE_Dictionary_EN.md#complete-rupture-boundary)
- 記号・固定名： $R=1.0$ ／ `RUPTURE_BOUNDARY`（状態名）
- 意味：評価前に宣言した対象構造の残存吸収余白が尽きた境界。定義元：AXIOMS §9・§10.5
- 混同注意：部分の破断を全体の破断と同じにしない（部分の破断は全体への事象）。 $\tau=0$ を完全破断へ読み替えない（→[定義域外](#out-of-domain)）
- 関連：[境界接近比](#boundary-approach-ratio)

<a id="observation-event"></a>
### 観測事象（かんそくじしょう）
- 英語版：[Observation Event](./NRA-IDE_Dictionary_EN.md#observation-event)
- 記号・固定名： $\mathrm{Ev}_n$ ／ `observation_event`
- 型：事象の記録（対象・値・単位・出所・時点・不確かさ・順序・観測経路）
- 意味：更新番号 $n$ の事象。状態を $n-1$ から $n$ へ進める。定義元：FORMULA §0.5.2
- 書き方： $\mathrm{Ev}$ と書く。構造要素の $e$ と大小だけで区別しないため、 $E$ は使わない
- 混同注意： $E_n$ と要素番号 $e$ が大小だけの区別になっていた（2026-09-29）
- 関連：[経路履歴](#event-history)、[分解規則](#event-allocation-rule)

<a id="observation-value"></a>
### 観測値（かんそくち）
- 英語版：[Observation Value](./NRA-IDE_Dictionary_EN.md#observation-value)
- 記号・固定名： $o_n$ ／ `observation_value`
- 型：Cause-Side入力
- 意味：Cause-Sideの観測（多変数でよい）。射影規則で蓄積ズレへ移す。定義元：FORMULA §0.5.2
- 混同注意：以前は $x_n$ と書いていた。FORMULA §5の計算状態 $x$ と字形が同じなので改めた（2026-09-29）
- 関連：[射影規則](#observation-projection-rule)

<a id="not-observable"></a>
### 観測不能（かんそくふのう）
- 英語版：[Not Observable](./NRA-IDE_Dictionary_EN.md#not-observable)
- 固定名：`NOT_OBSERVABLE`
- 型：観測チャネルの状態
- 意味：観測経路から値が得られないこと。欠損理由とともに出力する。定義元：AXIOMS §10.2・§11.1・§11.2
- 使ってはならない先：CONFESSIONへの読み替え。0・安定・回復としての補完
- 混同注意：観測できない事象をCONFESSIONへ送る誤りがあった（2026-09-28）。逆に、対象・単位・出所が不明な入力まで欠測処理へ回す行き過ぎもあった（2026-09-28）
- 関連：[告白](#confession)

<a id="reference-state"></a>
### 基準状態（きじゅんじょうたい）
- 英語版：[Reference State](./NRA-IDE_Dictionary_EN.md#reference-state)
- 型：宣言
- 意味：蓄積ズレを測る原点。評価開始前に固定し、評価中に付け直さない。再宣言は評価と評価の間でのみ許す。定義元：AXIOMS §4
- 混同注意：以前の案で $x_{\mathrm{ref}}$ と書いたが、FORMULA §5・§6の参照状態 $x_{\mathrm{exact}}$ と紛れるので、記号を置かず語で書く（2026-09-28）
- 関連：[蓄積ズレ](#accumulated-deviation)、[矯正](#straightening)

<a id="inverse-projection"></a>
### 逆射影（ぎゃくしゃえい）
- 英語版：[Inverse Projection](./NRA-IDE_Dictionary_EN.md#inverse-projection)
- 記号： $\Pi^{-1}$
- 意味：禁止された逆向き経路の名前。射影 $\Pi$ の数学的な逆写像ではない。定義元：SANDWICH_ARCH §8.3・§8.4
- 受け取り方の違い【未確認】：英語の inverse projection は、線形代数の射影の逆と読まれやすい
- 関連：[射影](#projection)、[逆導出](#reverse-derivation)

<a id="reverse-inference"></a>
### 逆推論（ぎゃくすいろん）
- 英語版：[Reverse Inference](./NRA-IDE_Dictionary_EN.md#reverse-inference)
- 意味：類似・連想による原因の推定。逆導出の独立の区分としない。構造判定の入力に使えば逆導出Aに当たり、構造判定の外での用法（創作など）は分類表の対象外。定義元：SANDWICH_ARCH §8.4
- 混同注意：src/README の「Π⁻¹（逆推論）」と「Π⁻¹（逆導出）」が同じ記号の二つの意味で並んでいる（2026-09-28。注記は未反映）
- 関連：[逆導出](#reverse-derivation)

<a id="reverse-derivation"></a>
### 逆導出（ぎゃくどうしゅつ）
- 英語版：[Reverse Derivation](./NRA-IDE_Dictionary_EN.md#reverse-derivation)
- 意味：次の経路を逆導出とし、自動・手動・人間レビュー・承認・版更新のいずれを介しても禁止する。定義元：AXIOMS §14
  - 逆導出A（権威の逆流）：Effect-Sideから、Cause-Sideの値・閾値・状態・不可逆ラッチ・規則・変換入力・更新根拠・出所への経路
  - 逆導出B（計器の自己調整）：評価出力（移動平均・集約を含む）から、同じ評価対象の基準・変換規則・閾値・有効ゲート幅への経路
- 書き方：判定は記号の名前ではなく、経路の出所と書き換え先で行う。出所の違うものには違う名前を付ける
- 混同注意：同じ $R$ という記号を、保存された評価出力と物理法則の中の比の両方に使っていた（2026-09-29）。「逆導出」の語が少なくとも九つの意味で使われていた（2026-09-27）
- 受け取り方の違い【未確認】：英語の derivation は、微分（derivative）や数学の導出と読まれやすい
- 関連：[評価出力](#evaluation-output)、[計器](#evaluation-gauge)

<a id="absorption-thickness"></a>
### 吸収厚み（きゅうしゅうあつみ）
- 英語版：[Absorption Thickness](./NRA-IDE_Dictionary_EN.md#absorption-thickness)
- 記号・固定名： $\tau$ ／ `tau`（出力 `observed_tau`）
- 型・単位：構造量（Cause-Side）、 $u$
- 意味：構造が蓄積ズレを吸収できる厚み。基準から破断までの総幅。定義元：AXIOMS §4・§7、FORMULA §1
- 出所：Cause-Side観測、評価前に固定した変換規則、構造要素の付加（加えた時点の測定）
- 使ってよい先： $R$ の計算、対象の物理法則、構造証言、監査
- 使ってはならない先：自然回復としての増加、評価出力による更新
- 書き方：構造全体は $\tau$ 、要素ごとは $\tau^{[e]}$ 、評価開始時は $\tau_0$
- 混同注意：
  - 「残り」と混同しない。残りは[残存吸収余白](#remaining-absorption-margin) $M_\tau$ （2026-09-26）
  - 増える経路は構造要素の付加だけ。「補充」「補修」とは書かない（2026-09-29）
  - 一時的に狭まる幅を実効厚みから差し引かない（→[一時的な可逆成分](#temporary-reversible-deviation)）（2026-09-29）
- 受け取り方の違い【未確認】：英語の thickness は板の物理的な厚さ、absorption は化学の吸収と読まれやすい。ここでは「蓄積ズレを受け止められる幅」
- 関連：[宣言厚み](#declared-thickness)、[実効厚み](#effective-thickness)、[構造要素の付加](#structural-element-addition)

<a id="warning-threshold"></a>
### 境界接近警告点（きょうかいせっきんけいこくてん）
- 英語版：[Boundary Warning Point](./NRA-IDE_Dictionary_EN.md#warning-threshold)
- 記号・固定名： $R_{\mathrm{warn}}$ ／ `r_warn`（出力 `thresholds.R_warn`）
- 型：計器（閾値）
- 意味：境界接近の警告を始める点。定義元：AXIOMS §9・§10.2
- 使ってはならない先：評価出力による変更
- 関連：[境界前人間委譲点](#handoff-threshold)、[不可逆遷移開始点](#irreversible-threshold)

<a id="boundary-approach-ratio"></a>
### 境界接近比（きょうかいせっきんひ）
- 英語版：[Boundary Approach Ratio](./NRA-IDE_Dictionary_EN.md#boundary-approach-ratio)
- 記号・固定名： $R=\delta/\tau$ ／ `R`（評価対象を明示するときは $R_{\mathrm{target}}$ ）
- 型・単位：評価出力、無次元
- 意味：構造破断境界への接近比。高いほど危険。定義元：AXIOMS §5、FORMULA §1
- 使ってよい先：状態分類、不可逆ラッチ、監査、構造証言、事前固定された物理制御の指令。他の評価対象の閾値・有効ゲート幅へは、安全側の向きで閉路がない場合に限る（AXIOMS §14）
- 使ってはならない先：同じ評価対象の計器（逆導出B）、対象状態
- 書き方：物理法則の中で負荷の比を使うときは、Cause-Sideの $\delta$ ・ $\tau$ から直接計算し、 $g(\delta,\tau,\dots)$ と書く。その比に $R$ という名前を付けない
- 混同注意：
  - 「評価出力は閾値・ゲートと物理制御にだけ使える」と狭く書いた（2026-09-29）。正しくは上の「使ってよい先」
  - 他構造の $R^{(i)}$ を自構造の劣化へ直接入れていた（2026-09-29）。入るのは観測された物理的事象
  - 安全スコア・保持率として再利用しない（AXIOMS §5）
- 受け取り方の違い【未確認】：docs の用語集では「構造比」と訳している箇所があり、FORMULA の「境界接近比」と割れている
- 関連：[評価出力](#evaluation-output)、[逆導出](#reverse-derivation)

<a id="handoff-threshold"></a>
### 境界前人間委譲点（きょうかいぜんにんげんいじょうてん）
- 英語版：[Pre-Boundary Human Handoff Point](./NRA-IDE_Dictionary_EN.md#handoff-threshold)
- 記号・固定名： $R_{\mathrm{handoff}}$ ／ `r_handoff`（出力 `thresholds.R_handoff`）
- 型：計器（閾値）
- 意味：自律的な新規判断・操作を止め、外部の人間へ委譲する点。移るのは実行権限だけ。定義元：AXIOMS §1・§9・§10.3
- 書き方：旧名 `R_op`・`Rop`・`rop`・`r_op` は互換入力としてだけ使い、新しい文書では使わない
- 受け取り方の違い【未確認】：英語の handoff は責任ごと引き渡すと読まれやすい。責任・法的責任・知識は移らない（AXIOMS §10.3）
- 関連：[境界接近警告点](#warning-threshold)

<a id="straightening"></a>
### 矯正（きょうせい）
- 英語版：[Straightening](./NRA-IDE_Dictionary_EN.md#straightening)
- 意味：伸び・曲がりを力で戻す操作。固定した基準から測った蓄積ズレを下げるので、評価の中では扱わない。行ったら評価を終え、宣言し直す。定義元：AXIOMS §7
- 混同注意：「補修事象があれば残留ズレは減ってよい」と読める書き方（AXIOMS v2.2）を、v2.3で改めた（2026-09-29）
- 関連：[残留ズレ](#residual-deviation)、[基準状態](#reference-state)

<a id="evaluation-gauge"></a>
### 計器（けいき）
- 英語版：[Evaluation Gauge](./NRA-IDE_Dictionary_EN.md#evaluation-gauge)
- 記号・固定名： $\mathsf{Gauge}^{(\mathrm{self})}$ ／ `evaluation_gauge`
- 型：計器の記録
- 意味：対象を測る基準状態・射影規則・閾値・形状変換関数・平滑係数・有効ゲート幅
- 使ってはならない先：同じ評価対象の評価出力による変更（逆導出B）
- 混同注意：以前は $\mathcal{K}^{(\mathrm{self})}$ と書いていた。FORMULA §5.5のknee値 $k$ と大小・装飾だけの区別だったため改めた（2026-09-29）
- 関連：[逆導出](#reverse-derivation)

<a id="event-history"></a>
### 経路履歴（けいろりれき）
- 英語版：[Event History](./NRA-IDE_Dictionary_EN.md#event-history)
- 記号・固定名： $\mathsf{History}_n$ ／ `event_history`
- 型：証言の記録
- 意味：事象 $\mathrm{Ev}_1,\dots,\mathrm{Ev}_n$ の記録列。常に伸び、書き換えない
- 書き方：追記は $\mathsf{History}_n=\mathsf{History}_{n-1}\oplus\mathrm{Ev}_n$ 。記録の個数は $\#\mathsf{History}_n$
- 混同注意：
  - 以前は $\mathcal{H}_n$ と書いていた。形状変換関数 $h$ と大小・字体だけの区別だったため改めた（2026-09-29）
  - 記録の個数を絶対値と同じ $\lvert\cdot\rvert$ で書いていた（2026-09-29）
  - 経路履歴（証言のための記録）と、物理状態・評価状態を混ぜない（2026-09-29）
- 関連：[判定用十分状態](#decision-sufficient-state)

<a id="active-elements"></a>
### 構成（こうせい）
- 英語版：[Active Elements](./NRA-IDE_Dictionary_EN.md#active-elements)
- 記号・固定名： $\mathsf{Active}_n$ ／ `active_elements`
- 型：集合
- 意味：時点 $n$ に評価対象に含まれている構造要素の集合（付加され、まだ除去されていない要素）。定義元：FORMULA §0.5.4
- 混同注意：
  - 瞬間分類 $C_0$ ・連結条件C1〜C4と字体・大小だけの区別になっていたので、分類と条件の側を改名した（2026-09-29）
  - 以前は $\mathcal{C}_n$ と書いていた。AXIOMS v2.4で制約 $C$ が正典の記号になり、装飾だけの区別になったため、構成の側を改名した（2026-09-29）
- 関連：[合成規則](#thickness-composition-rule)、[構造要素](#structural-element)

<a id="thickness-composition-rule"></a>
### 合成規則（ごうせいきそく）
- 英語版：[Thickness Composition Rule](./NRA-IDE_Dictionary_EN.md#thickness-composition-rule)
- 記号・固定名： $\mathrm{Comp}_\tau$ ／ `thickness_composition_rule`
- 型：写像（評価前に固定）
- 意味：要素の厚みから全体の実効厚みを定める規則。 $\tau_n=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_n)_{e\in\mathsf{Active}_n}\bigr)$ 。条件：各引数について非減少、有限・非負・単位を保つ、要素一つならその厚み、全要素0なら0、評価の中で除去を認める場合は要素を外しても値が増えない。定義元：FORMULA §0.5.4
- 書き方：並列なら和。直列（ $\min$ ）は要素を外すと全体が強くなるので、評価の中で除去を扱わず宣言の変更とする
- 混同注意：以前は $\Gamma$ と書いていた。FORMULA §5の減衰係数 $\gamma$ と大小だけの区別だったため改めた（2026-09-29）。「要素を外しても値は増えない」を全ての形に課すと直列の構造が表せないことを、条件を足す途中で見つけた（2026-09-29）
- 関連：[構成](#active-elements)、[構造要素の付加](#structural-element-addition)

<a id="structural-sensitivity"></a>
### 構造感度（こうぞうかんど）
- 英語版：[Structural Sensitivity](./NRA-IDE_Dictionary_EN.md#structural-sensitivity)
- 記号： $S=1/M_\tau$
- 型・単位：派生出力、 $u^{-1}$
- 意味：残存吸収余白の逆数。定義元：FORMULA §3
- 混同注意：エントロピー相当量 $\mathrm{entropy}$ と `entropy_export` を $S$ で書かない（AXIOMS §4.5、FORMULA §7）（2026-09-29）
- 関連：[残存吸収余白](#remaining-absorption-margin)、[エントロピー相当量](#entropy-quantity)

<a id="structural-testimony"></a>
### 構造証言（こうぞうしょうげん）
- 英語版：[Structural Testimony](./NRA-IDE_Dictionary_EN.md#structural-testimony)
- 意味：構造の状態を、固定の欄と形式で記録・報告し続けること。 $R<1.0$ の間は停止しない。 $R\ge1.0$ では破断後固定証言へ切り替える。定義元：AXIOMS §11
- 受け取り方の違い【未確認】：英語の testimony は法廷での証言と読まれやすい
- 関連：[経路履歴](#event-history)

<a id="structural-element"></a>
### 構造要素（こうぞうようそ）
- 英語版：[Structural Element](./NRA-IDE_Dictionary_EN.md#structural-element)
- 記号・固定名： $e$ ／ `element_id`
- 型：添字
- 意味：評価対象を構成する要素。 $e=0$ は宣言時の構造、 $e\ge1$ は付加した要素。要素ごとに宣言厚み $\tau^{[e]}_0$ と劣化度 $\lambda^{[e]}_n$ を持つ。定義元：FORMULA §0.5.4
- 関連：[構成](#active-elements)、[構造要素の付加](#structural-element-addition)

<a id="structural-element-removal"></a>
### 構造要素の除去（こうぞうようそのじょきょ）
- 英語版：[Removal of a Structural Element](./NRA-IDE_Dictionary_EN.md#structural-element-removal)
- 意味：壊れていない構造要素を計画的に外すこと。劣化ではないので劣化度に計上しない。厚みは減る。外した要素を戻すときは、改めて付加として扱う。定義元：AXIOMS §7
- 混同注意：サーバーの縮退のような「健全な要素を外す」場合の分類がなく、「壊れた」と記録するしかなかった（2026-09-29）
- 関連：[構造要素の付加](#structural-element-addition)

<a id="structural-element-addition"></a>
### 構造要素の付加（こうぞうようそのふか）
- 英語版：[Addition of a Structural Element](./NRA-IDE_Dictionary_EN.md#structural-element-addition)
- 意味：評価対象へ新しい構造要素を加えること。吸収厚みが増える唯一の経路。既存の要素の厚みを回復させない。加えた要素の厚みは加えた時点のCause-Side測定で定める。合わせる規則は評価前に固定する。主体は問わない（人の補強、生体の修復）。定義元：AXIOMS §7・§8
- 使ってはならない先： $R$ だけを根拠に「付加が済んだ」「厚みが増えた」と認めること（ $R$ を事前固定の補強操作の引き金にするのはよい）
- 混同注意：
  - 「外部補充」「外生補充」「外生的な補修事象」「外生的な復元操作」など6通りの言い方が混在し、既存のものが戻ると読めた（2026-09-29）
  - 肉盛り溶接を「劣化度が戻った」と読まない。補修材という要素の付加（2026-09-29）
  - 補強で全体の厚みが $\tau_0$ を上回っても、初期構造への復元ではない（2026-09-29）
- 受け取り方の違い【未確認】：日本語の「付加」は「付加価値」を連想させる。英語の addition は数の足し算と読まれやすい
- 関連：[吸収厚み](#absorption-thickness)、[構造要素の除去](#structural-element-removal)、[補充](#replenishment)、[補修](#repair)

<a id="structural-continuity"></a>
### 構造連続性（こうぞうれんぞくせい）
- 英語版：[Structural Continuity](./NRA-IDE_Dictionary_EN.md#structural-continuity)
- 記号・固定名： $\omega$ ／ `omega`
- 型：補助構造量（Cause-Side）
- 意味：構造が遷移を継続しているかを示す。ドメインが評価前に定めた連続観測または位相更新規則の下で継続が確認できるときに限り $\omega>0$ 。定義元：AXIOMS §1（凡例）・§4.5
- 出所：Cause-Side観測、評価前に固定した変換規則
- 使ってはならない先：評価出力（ $R$ 、正規状態、不可逆ラッチ、その集約）から得ること
- 書き方：評価の系列との対応づけは、評価宣言の任意要素として評価ごとに宣言する（一般規則は定めない。導出文書P0）
- 混同注意：観測が欠けていることを $\omega=0$ と書かない（AXIOMS §4.5）。docs 12章の用語集が「遷移継続量」と呼んでいた（2026-09-29）
- 関連：[遷移位相](#transition-phase)

<a id="confession"></a>
### 告白（こくはく）
- 英語版：[Confession](./NRA-IDE_Dictionary_EN.md#confession)
- 固定名：`CONFESSION`（出力 `status`）
- 型：分類（不明時の停止信号）
- 意味：必要変数・単位・時点・出所・対象・ドメイン規則が不明、値が不正・非有限、Cause-SideかEffect-Sideか判別できないときに出力する。定義元：AXIOMS §6・§10.6
- 使ってはならない先：既知の危険接近や既知の状態遷移の報告
- 受け取り方の違い【未確認】：英語の confession は宗教・法廷の告白と読まれやすい。ここでは不明を構造化して示す停止信号
- 関連：[観測不能](#not-observable)

<a id="applied-action"></a>
### 作用（さよう）
- 英語版：[Applied Action](./NRA-IDE_Dictionary_EN.md#applied-action)
- 記号・固定名： $a_n$ ／ `applied_action`
- 型：対象への入力（観測された物理的事象）
- 意味：その時点で構造に加わっている作用。受け止め幅を一時的に狭める条件の効果（一時的な可逆成分）もここに計上する。定義元：FORMULA §0.5.3
- 混同注意：
  - 命題2の事象の前後を $a$ 、 $b$ 、命題4の二つの構造を $\lambda_a$ 、 $\lambda_b$ と書いて、作用と同じ文字を使っていた（2026-09-29）
  - [制約](#external-constraint) $C$ （外部条件）と混同しない。 $C$ は計上先ではなく、その効果が $\Delta\lambda_n$ や計器にだけ現れる場合は $a_n$ に現れない（2026-09-30）
- 関連：[可逆成分](#reversible-deviation)、[制約](#external-constraint)

<a id="remaining-absorption-margin"></a>
### 残存吸収余白（ざんぞんきゅうしゅうよはく）
- 英語版：[Remaining Absorption Margin](./NRA-IDE_Dictionary_EN.md#remaining-absorption-margin)
- 記号・固定名： $M_\tau=\tau-\delta$ ／ `remaining_absorption_margin`（旧名 `remaining_slack` は非推奨）
- 型・単位：派生出力、 $u$
- 意味：厚みのうち、まだズレが入っていない残り。定義元：AXIOMS §5、FORMULA §2
- 混同注意：
  - 吸収厚み（総幅）と混同しない（2026-09-26）
  - 「残存吸収余裕」（AXIOMS §5）、「残存構造余裕」（AXIOMS §10.5、Thesis、docs）とも呼んでいた。余白に揃えた（2026-09-30）
- 受け取り方の違い【未確認】：英語の margin は利益率や安全率と読まれやすい
- 関連：[残存比率余白](#remaining-ratio-margin)

<a id="remaining-ratio-margin"></a>
### 残存比率余白（ざんぞんひりつよはく）
- 英語版：[Remaining Ratio Margin](./NRA-IDE_Dictionary_EN.md#remaining-ratio-margin)
- 記号・固定名： $M_R=1-R$ ／ `remaining_ratio_margin`
- 型・単位：派生出力、無次元
- 意味：定義元：AXIOMS §5、FORMULA §2。`remaining margin` という曖昧な単独名を使わない
- 書き方：「比率」は、境界接近比 $R$ の尺度で測った余白という意味である。値は $M_\tau/\tau$ に等しい（ $M_R=1-R=(\tau-\delta)/\tau$ ）
- 混同注意：AXIOMS §5では「無次元の境界余裕」と呼んでいた。「余裕」は総幅 $\tau$ の説明（AXIOMS §3・§4）にも使われるため、量の名前は「余白」に揃えた（2026-09-30）

<a id="residual-deviation"></a>
### 残留ズレ（ざんりゅうずれ）
- 英語版：[Residual Deviation](./NRA-IDE_Dictionary_EN.md#residual-deviation)
- 記号・固定名： $p_n$ ／ `residual_deviation`
- 型：対象状態
- 意味：蓄積ズレのうち、作用を除いても残る部分（不可逆成分）。評価中に減少しない。定義元：AXIOMS §4・§7、FORMULA §0.5.3
- 書き方：後退差分で $p_n=p_{n-1}+\Delta p_n$ 、 $p_n=p_0+\sum_{m=1}^{n}\Delta p_m$
- 混同注意：デモの residualDebt・ $D_{\mathrm{long}}$ は $R$ から作った量で、残留ズレではない（2026-09-29）
- 関連：[可逆成分](#reversible-deviation)、[矯正](#straightening)

<a id="work-quantity"></a>
### 仕事量（しごとりょう）
- 英語版：[Work](./NRA-IDE_Dictionary_EN.md#work-quantity)
- 記号・固定名： $W$ ／ `work_quantity`
- 型：補助構造量（任意、Cause-Side）
- 意味：ドメインが定義・単位・観測方法を明記した場合だけ使う任意量。定義元：AXIOMS §4.5。FORMULA §7の予約表には含めない
- 出所：Cause-Side観測、評価前に固定した変換規則
- 使ってはならない先：評価出力（ $R$ 、正規状態、不可逆ラッチ、その集約）から得ること
- 混同注意：対象状態の旧記号 $\mathcal{W}$ と装飾だけの区別になっていた。対象状態の側を $\mathsf{Phys}$ に改めた（2026-09-29）
- 受け取り方の違い【未確認】：物理の仕事（力×変位）とそのまま読まれやすい。定義はドメインが与える
- 関連：[対象状態](#target-physical-state)

<a id="subject-target"></a>
### 自構造（じこうぞう）
- 英語版：[Subject Target](./NRA-IDE_Dictionary_EN.md#subject-target)
- 記号・固定名： $(\mathrm{self})$ ／ `subject_target`
- 意味：いま評価している構造。他構造は $(i)$
- 混同注意：以前は構造名 $G$ と書いていた（FORMULA §5の $G(r)$ と字形が同じ）。案の $k$ はknee値 $k$ と衝突するため採らなかった（2026-09-29）
- 関連：[他構造](#other-target)

<a id="effective-thickness"></a>
### 実効厚み（じっこうあつみ）
- 英語版：[Effective Thickness](./NRA-IDE_Dictionary_EN.md#effective-thickness)
- 記号： $\tau_n$
- 意味：一次式で使う、時点 $n$ の構造全体の厚み。構造要素の付加がない限り増えない。定義元：FORMULA §0.5.4
- 関連：[吸収厚み](#absorption-thickness)、[側別有効ゲート幅](#side-specific-gate-width)

<a id="dominant-side"></a>
### 支配側（しはいがわ）
- 英語版：[Dominant Side](./NRA-IDE_Dictionary_EN.md#dominant-side)
- 記号・固定名： $D$ ／ `dominant_side`
- 型：補助出力
- 意味：側別比の大きい方。定義元：FORMULA §4.6
- 混同注意：評価宣言を $\mathcal{D}$ と書いて、字体だけで区別していた。評価宣言を $\mathsf{Decl}$ に改めた（2026-09-29）

<a id="projection"></a>
### 射影（しゃえい）
- 英語版：[Projection](./NRA-IDE_Dictionary_EN.md#projection)
- 記号： $\Pi$
- 意味：現在の境界状態で許されたEffect-Side内容だけを選ぶ操作。可逆な写像ではない。定義元：SANDWICH_ARCH §8.2
- 関連：[逆射影](#inverse-projection)、[射影規則](#observation-projection-rule)

<a id="observation-projection-rule"></a>
### 射影規則（しゃえいきそく）
- 英語版：[Observation Projection Rule](./NRA-IDE_Dictionary_EN.md#observation-projection-rule)
- 記号・固定名： $\sigma$ ／ `observation_projection_rule`
- 型：写像（評価前に固定）
- 意味：観測値を、基準状態から宣言した破断方向へ測ったズレへ移す規則。 $\delta_n=\sigma(o_n)$ 。定義元：FORMULA §0.5.2
- 混同注意：SANDWICHの射影 $\Pi$ とは別物（2026-09-29）
- 関連：[射影](#projection)

<a id="instantaneous-classification"></a>
### 瞬間分類（しゅんかんぶんるい）
- 英語版：[Instantaneous Classification](./NRA-IDE_Dictionary_EN.md#instantaneous-classification)
- 記号・固定名： $\mathrm{Class}(R)$ ／ `instantaneous_classification`
- 意味：有効な $R$ の区間による正典の分類（ラッチを反映する前）
- 混同注意：以前は $C_0(R)$ と書いていた（2026-09-29）
- 関連：[状態区分](#target-state)

<a id="target-state"></a>
### 状態区分（じょうたいくぶん）
- 英語版：[Target Boundary State](./NRA-IDE_Dictionary_EN.md#target-state)
- 記号・固定名： $\mathsf{State}_n$ ／ `target_state`（値：`PERMIT`・`BOUNDARY_WARNING`・`HANDOFF_REQUIRED`・`IRREVERSIBLE_TRANSITION`・`RUPTURE_BOUNDARY`）
- 型：正規状態
- 意味：有効な $R$ とラッチから決まる状態。定義元：AXIOMS §9〜§11.1
- 混同注意：以前は $Q_n$ と書いていた（可逆成分 $q_n$ と大小だけの区別）（2026-09-29）
- 関連：[瞬間分類](#instantaneous-classification)、[不可逆ラッチ](#irreversible-latch)

<a id="external-constraint"></a>
### 制約（せいやく）
- 英語版：[Constraint](./NRA-IDE_Dictionary_EN.md#external-constraint)
- 記号・固定名： $C$ ／ `external_constraint`
- 型：補助構造量（Cause-Side）
- 意味：対象構造へ外部から加わる負荷・拘束・環境条件。時点の値 $C_n$ を持つ量で、観測 $o_n$ の成分。何を $C$ とするか（種類・出所・単位・換算規則）は評価宣言に語で書く。定義元：AXIOMS §4.5、FORMULA §7
- 出所：Cause-Side観測、評価前に固定した変換規則
- 使ってはならない先：評価出力（ $R$ 、正規状態、不可逆ラッチ、その集約）から得ること。蓄積ズレ・吸収厚みへの直接の計上（計上は $a_n$ ・ $\Delta p_n$ ・ $\Delta\lambda_n$ のいずれか一つ）
- 混同注意：
  - 構成の旧記号 $\mathcal{C}_n$ と装飾だけの区別になっていた。構成の側を $\mathsf{Active}_n$ に改めた（2026-09-29）
  - 一般語の「制約（条件）」と区別する。例えば「 $\tau_{\mathrm{restored}}<\tau_0$ という制約」は条件の意味（2026-09-29）
  - $C$ は条件、[作用](#applied-action) $a_n$ は計上された作用。 $\delta$ ・ $\tau$ へ計上されるのは $a_n$ ・ $\Delta p_n$ ・ $\Delta\lambda_n$ のどれか一つで、 $C$ は計上先にならない。同じ因子（温度など）が $C$ と $a_n$ の両方に現れても二重計上ではない（2026-09-30）
- 受け取り方の違い【未確認】：英語の constraint は最適化の制約条件と読まれやすい。ここでは外部から加わる負荷
- 関連：[作用](#applied-action)、[構成](#active-elements)、[評価宣言](#evaluation-declaration)

<a id="transition-phase"></a>
### 遷移位相（せんいいそう）
- 英語版：[Transition Phase](./NRA-IDE_Dictionary_EN.md#transition-phase)
- 記号・固定名： $\mathrm{Phase}$ ／ `transition_phase`
- 型：補助構造量（Cause-Side、内部状態）
- 意味：対象構造が遷移のどの段階にあるかを示す内部状態。Cause-Sideに由来する遷移規則で更新する。定義元：AXIOMS §4.5
- 出所：Cause-Side観測、評価前に固定した変換規則
- 使ってはならない先：空間座標・モデルが生成した埋め込みとして読むこと。評価出力から得ること
- 書き方：綴りで $\mathrm{Phase}$ と書く。 $\varphi$ ・ $\phi$ は使わない
- 混同注意：案では $\varphi$ と書いていたが、FORMULA §5.1の補助計算項 $\Phi(x)$ と大小だけの区別になるため改めた（2026-09-29）
- 受け取り方の違い【未確認】：英語の phase は物質の相や波の位相と読まれやすい。ここでは遷移の段階
- 関連：[構造連続性](#structural-continuity)

<a id="declared-thickness"></a>
### 宣言厚み（せんげんあつみ）
- 英語版：[Declared Thickness](./NRA-IDE_Dictionary_EN.md#declared-thickness)
- 記号・固定名： $\tau_0$ ／ `initial_tau`（参照実装 `DynamicTauEngine` の引数）
- 型・単位：構造量（Cause-Side）、 $u$
- 意味：評価開始時（遷移前）の構造全体の吸収厚み。要素が複数なら $\tau_0=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_0)_{e\in\mathsf{Active}_0}\bigr)$ 。定義元：AXIOMS §7（初期吸収厚み）・§8（基準吸収厚み）、FORMULA §0.5.1・§0.5.4
- 混同注意：「要素が一つの場合だけの特殊形」と書いたのは正典と食い違っていた（2026-09-29）
- 関連：[吸収厚み](#absorption-thickness)、[復元後の吸収厚み](#restored-thickness)

<a id="side-specific-gate-width"></a>
### 側別有効ゲート幅（そくべつゆうこうげーとはば）
- 英語版：[Side-Specific Effective Gate Width](./NRA-IDE_Dictionary_EN.md#side-specific-gate-width)
- 記号・固定名： $\tau_{\mathrm{upper}}$ 、 $\tau_{\mathrm{lower}}$ ／ `tau_upper`・`tau_lower`
- 型：計器（二次式だけで使う）
- 意味：増減してよい。基礎吸収厚みの自然回復を意味しない。定義元：FORMULA §4.4
- 使ってはならない先：形状変換関数へ評価出力（ $R$ 系）を入れること
- 関連：[実効厚み](#effective-thickness)

<a id="target-physical-state"></a>
### 対象状態（たいしょうじょうたい）
- 英語版：[Target Physical State](./NRA-IDE_Dictionary_EN.md#target-physical-state)
- 記号・固定名： $\mathsf{Phys}^{(\mathrm{self})}_n$ ／ `target_physical_state`
- 型：状態の記録
- 意味：対象の物理状態 $(q_n,p_n,(\lambda^{[e]}_n)_{e\in\mathsf{Active}_n})$ 。評価状態（ラッチ）と経路履歴は含まない
- 出所：観測された物理的事象、対象の物理法則
- 使ってはならない先：評価出力の読み戻し（自構造・他構造とも）
- 混同注意：
  - 対象状態へ入るのは観測された物理的事象だけ。物理状態・評価状態・経路履歴を混ぜない（2026-09-29）
  - 以前は $\mathcal{W}^{(\mathrm{self})}_n$ と書いていた。AXIOMS v2.4の仕事量 $W$ と装飾だけの区別になったため改めた（2026-09-29）
- 関連：[評価状態](#evaluation-state)、[経路履歴](#event-history)

<a id="other-target"></a>
### 他構造（たこうぞう）
- 英語版：[Other Target](./NRA-IDE_Dictionary_EN.md#other-target)
- 記号・固定名： $(i)$ ／ `other_target_index`
- 意味：影響を与える他の構造、または部分構造。他構造の観測された物理状態は自構造の観測事象として入る。他構造の評価出力は、自構造の監査・構造証言での記録、安全側の計器入力、事前固定の物理制御の指令に使え、自構造の対象状態へは入らない
- 関連：[自構造](#subject-target)

<a id="accumulated-deviation"></a>
### 蓄積ズレ（ちくせきずれ）
- 英語版：[Accumulated Deviation](./NRA-IDE_Dictionary_EN.md#accumulated-deviation)
- 記号・固定名： $\delta$ ／ `delta`（出力 `observed_delta`）
- 型・単位：構造量（Cause-Side）、 $u$
- 意味：評価前に固定した基準状態から、宣言した破断方向へ測ったズレ。可逆成分と残留ズレから成る。基準を動かさずに測ることで履歴を伴う。定義元：AXIOMS §4・§5、FORMULA §1
- 使ってはならない先：Effect-Side由来の値による更新（逆導出A）
- 混同注意：「 $\delta$ は単なる瞬間値ではない」と「作用を除けば減る可逆成分を含む」の関係が正典になかった（v2.2で定めた。2026-09-28）
- 受け取り方の違い【未確認】：英語の deviation は統計の偏差（standard deviation）と読まれやすい。日本語の「ズレ」は日常の言葉として軽く読まれやすい
- 関連：[可逆成分](#reversible-deviation)、[残留ズレ](#residual-deviation)、[基準状態](#reference-state)

<a id="out-of-domain"></a>
### 定義域外（ていぎいきがい）
- 英語版：[Out of Domain](./NRA-IDE_Dictionary_EN.md#out-of-domain)
- 記号・固定名： $\emptyset$ ／ `OUT_OF_DESCRIPTION_DOMAIN`（出力 `status`）
- 意味： $\tau=0$ のとき。 $R$ は定義できない。定義元：AXIOMS §1・§6・§10.7
- 書き方： $\emptyset$ はこのリポジトリでは「定義域外」の意味。空集合の意味では使わず、「空」は語で書く
- 使ってはならない先： $R$ を無限大へ置き換えること、RUPTURE_BOUNDARYへの読み替え
- 混同注意：離散の更新では、 $\lambda$ が一度で1に達すると直前の $R$ が1未満でも定義域外になる（2026-09-28）
- 関連：[完全破断境界](#complete-rupture-boundary)

<a id="decision-sufficient-state"></a>
### 判定用十分状態（はんていようじゅうぶんじょうたい）
- 英語版：[Decision-Sufficient State](./NRA-IDE_Dictionary_EN.md#decision-sufficient-state)
- 記号・固定名： $Z_n$ ／ `decision_sufficient_state`
- 型：名前付きの欄を持つ記録
- 意味：次の分類を決めるのに十分な状態。欄は `residual_deviation`、`active_elements`（各要素の `declared_tau`・`degradation_fraction`・必要なら `domain_memory`）、`irreversible_latched`、必要なら `reversible_state`・`domain_global_memory`
- 書き方：位置で並べる組にしない。更新規則はラッチを除く物理状態だけを入力にする
- 混同注意： $(p,\lambda,\ell)$ の組では、要素を複数にしたときに足りなかった（2026-09-29）。更新規則の入力にラッチが入る形にしていた（2026-09-29）
- 関連：[経路履歴](#event-history)

<a id="evaluation-output"></a>
### 評価出力（ひょうかしゅつりょく）
- 英語版：[Evaluation Output](./NRA-IDE_Dictionary_EN.md#evaluation-output)
- 記号・固定名： $\mathsf{Out}^{(\mathrm{self})}_n$ ／ `evaluation_output`
- 意味： $R$ 、正規状態、不可逆ラッチ。Cause-Side観測でもEffect-Side生成物でもない。Cause-Side入力から事前固定規則で計算した出力。定義元：AXIOMS §14（側別比を含めるのは導出文書の読み）
- 使ってよい先：監査、構造証言、状態分類、事前固定された物理制御の指令。他の評価対象の閾値・有効ゲート幅へは安全側で閉路がない場合に限る
- 使ってはならない先：同じ評価対象の計器（逆導出B）、対象状態
- 書き方：以前は $\mathcal{Y}^{(\mathrm{self})}_n$ と書いていた。衝突はないが、P9の三区分（対象状態・計器・評価出力）の書き方を揃えるため改めた（2026-09-29）
- 混同注意：使ってよい先を「閾値・ゲートと物理制御にだけ」と狭く書いた（2026-09-29）
- 関連：[境界接近比](#boundary-approach-ratio)、[逆導出](#reverse-derivation)

<a id="evaluation-state"></a>
### 評価状態（ひょうかじょうたい）
- 英語版：[Evaluation State](./NRA-IDE_Dictionary_EN.md#evaluation-state)
- 意味：不可逆ラッチなど、評価出力として保持するもの。対象の物理状態とも経路履歴とも別
- 関連：[不可逆ラッチ](#irreversible-latch)、[対象状態](#target-physical-state)

<a id="evaluation-snapshot"></a>
### 評価スナップショット（ひょうかすなっぷしょっと）
- 英語版：[Evaluation Snapshot](./NRA-IDE_Dictionary_EN.md#evaluation-snapshot)
- 意味：一つの評価で固定する、対象・更新権限・出所・単位・時刻・変換規則・閾値規則の組。新しい権限あるCause-Side観測は、次のスナップショットを更新できる。定義元：FORMULA §6、AXIOMS §14
- 書き方：新しい観測で宣言厚みが変わる場合は、評価中の増加として扱わず、次の評価スナップショットとして宣言し直す
- 混同注意：「構造が変化した」と書くと「変質」、「測定し直し」と書くと「過去の訂正」と読まれる。「次の評価スナップショット」と書く（2026-09-29）
- 関連：[評価宣言](#evaluation-declaration)

<a id="evaluation-declaration"></a>
### 評価宣言（ひょうかせんげん）
- 英語版：[Evaluation Declaration](./NRA-IDE_Dictionary_EN.md#evaluation-declaration)
- 記号・固定名： $\mathsf{Decl}$ ／ `evaluation_declaration`
- 型：宣言（評価前に固定）
- 意味：計算開始前に固定する約束の組。必須要素は、評価対象と破断様式、単位、観測の種類と出所、閾値、欠測・観測不能の処理、基準状態、射影規則、分解規則、宣言厚み、合成規則。任意要素は、評価の系列と構造連続性 $\omega$ との対応づけ、外部条件（制約 $C$ ）の同定。定義元：FORMULA §0.5.1
- 混同注意：以前は $\mathcal{D}$ と書いていた（支配側 $D$ と字体だけの区別）（2026-09-29）
- 関連：[評価スナップショット](#evaluation-snapshot)

<a id="irreversible-threshold"></a>
### 不可逆遷移開始点（ふかぎゃくせんいかいしてん）
- 英語版：[Irreversible Transition Onset](./NRA-IDE_Dictionary_EN.md#irreversible-threshold)
- 記号・固定名： $R_{\mathrm{irrev}}$ ／ `r_irrev`（出力 `thresholds.R_irrev`）
- 型：計器（閾値）
- 意味：元の構造状態へ戻れない不可逆遷移へ入る点。 $R_{\mathrm{handoff}}<R_{\mathrm{irrev}}<1.0$ 。定義元：AXIOMS §9・§10.4

<a id="irreversible-latch"></a>
### 不可逆ラッチ（ふかぎゃくらっち）
- 英語版：[Irreversible Latch](./NRA-IDE_Dictionary_EN.md#irreversible-latch)
- 記号・固定名： $\ell_n$ ／ `irreversible_latched`
- 型：評価状態（真偽）
- 意味：一度 $R_{\mathrm{irrev}}$ に達したら、自動では解除しない。 $\ell_n=\ell_{n-1}\lor\mathbf{1}\{R_n\ge R_{\mathrm{irrev}}\}$ 。定義元：AXIOMS §10.4
- 書き方：固定名は `irreversible_latched`（`irreversible_latch` ではない）
- 混同注意：補修や付加で自動解除しない。宣言し直すときは、前の評価でラッチがかかっていたことを新しい宣言に書く（2026-09-29）。物理法則の入力にしない（2026-09-29）
- 受け取り方の違い【未確認】：英語の latch は電子回路のラッチ（リセットできる）と読まれやすい
- 関連：[不可逆遷移開始点](#irreversible-threshold)

<a id="restoration"></a>
### 復元（ふくげん）
- 英語版：[Restoration](./NRA-IDE_Dictionary_EN.md#restoration)
- 意味：初期構造への復帰を主張すること。比較可能性と $\tau_{\mathrm{restored}}<\tau_0$ の双方の立証が要る。定義元：AXIOMS §8
- 混同注意：「値の復帰」「物理状態の復帰」「履歴の同一」は別の問い（導出文書 命題2）（2026-09-29）
- 関連：[復元後の吸収厚み](#restored-thickness)

<a id="restored-thickness"></a>
### 復元後の吸収厚み（ふくげんごのきゅうしゅうあつみ）
- 英語版：[Restored Absorption Thickness](./NRA-IDE_Dictionary_EN.md#restored-thickness)
- 記号： $\tau_{\mathrm{restored}}$
- 意味：復元を目的とする操作の後に、同一対象・同一単位・同一測定規則で評価した後継構造のうち、付加した要素を除く既存の要素の厚み。定義元：AXIOMS §8
- 混同注意：付加した要素を含む全体の厚みと読むと、補強した橋で $\tau_{\mathrm{restored}}<\tau_0$ に反してしまう（2026-09-29）

<a id="event-allocation-rule"></a>
### 分解規則（ぶんかいきそく）
- 英語版：[Event Allocation Rule](./NRA-IDE_Dictionary_EN.md#event-allocation-rule)
- 記号・固定名： $\mathsf{Alloc}$ ／ `event_allocation_rule`
- 型：写像（評価前に固定）
- 意味：観測された一つの変化を、作用・残留ズレの増分・劣化度の増分の**ちょうど一つ**に計上する規則（一変化一計上）。文脈・権限・出所 $\mathrm{ctx}_n$ は計上先ではない。定義元：FORMULA §0.5.3
- 混同注意：以前は $\Lambda$ と書いていた（劣化度 $\lambda$ と大小だけの区別）（2026-09-29）
- 関連：[観測事象](#observation-event)

<a id="evaluation-archive"></a>
### 保管記録（ほかんきろく）
- 英語版：[Evaluation Archive](./NRA-IDE_Dictionary_EN.md#evaluation-archive)
- 記号・固定名： $\mathsf{Archive}$ ／ `evaluation_archive`
- 意味：終了した評価の記録の列。書き換えない
- 混同注意：以前は $\mathcal{A}$ と書いていた（例の光合成速度 $A$ と字体だけの区別）（2026-09-29）

<a id="repair"></a>
### 補修（ほしゅう）→ [構造要素の付加](#structural-element-addition)を見よ
- 英語版：[Repair](./NRA-IDE_Dictionary_EN.md#repair)
- 日常の言葉としては使ってよい。式の上では「補修材という要素の付加」として扱い、既存要素の劣化度は減らない
- 混同注意：「補修回復分 $\eta$ 」として劣化度を差し引く書き方をやめた（2026-09-29）

<a id="replenishment"></a>
### 補充（ほじゅう）→ [構造要素の付加](#structural-element-addition)を見よ
- 英語版：[Replenishment](./NRA-IDE_Dictionary_EN.md#replenishment)
- 正規語ではない。AXIOMS v2.2までの「外部補充」「外生補充」「外生的な補充操作」は、v2.3で「構造要素の付加」に改めた
- 混同注意：既存の厚みが戻ると読める（2026-09-29）

<a id="degradation-fraction"></a>
### 劣化度（れっかど）
- 英語版：[Degradation Fraction](./NRA-IDE_Dictionary_EN.md#degradation-fraction)
- 記号・固定名： $\lambda^{[e]}_n$ ／ `element_degradation_fraction`（要素が一つの場合は $\lambda_n$ ）
- 型：対象状態（無次元、 $0\le\lambda\le1$ ）
- 意味：要素の厚みが失われた割合。 $\tau^{[e]}_n=(1-\lambda^{[e]}_n)\tau^{[e]}_0$ 。評価中に減らない。定義元：FORMULA §0.5.4
- 書き方：一般の式では要素ごとの $\lambda^{[e]}_n$ を使い、 $\lambda_n$ は要素が一つの式だけで使う
- 混同注意：要素を複数にした後も、単一要素の $\lambda_n$ ・ $\tau_0$ を全体の状態として使い続け、一次式・補題・命題5へ波及した（2026-09-29）
- 関連：[構造要素](#structural-element)

---

## 2. 記号の部

### 2.1 ラテン文字

| 記号 | 見出し |
|---|---|
| $a_n$ | [作用](#applied-action) |
| $\mathsf{Active}_n$ | [構成](#active-elements) |
| $C$ 、 $C_n$ | [制約](#external-constraint) |
| $\mathrm{Class}(R)$ | [瞬間分類](#instantaneous-classification) |
| $\mathrm{Comp}_\tau$ | [合成規則](#thickness-composition-rule) |
| $\mathrm{ctx}_n$ | 文脈・権限・出所（[分解規則](#event-allocation-rule)） |
| $D$ | [支配側](#dominant-side) |
| $\mathsf{Decl}$ | [評価宣言](#evaluation-declaration) |
| $e$ | [構造要素](#structural-element) |
| $\mathrm{entropy}$ | [エントロピー相当量](#entropy-quantity) |
| $\mathrm{Ev}_n$ | [観測事象](#observation-event) |
| $\mathrm{EvalGraph}^{(j)}$ | 展開評価グラフ（導出文書 第3部） |
| $g_p$ 、 $g^{[e]}_\lambda$ | 残留ズレ・要素の劣化の増分則（物理法則。評価出力を入力にしない） |
| $\mathsf{Gauge}^{(\mathrm{self})}$ | [計器](#evaluation-gauge) |
| $\mathsf{History}_n$ | [経路履歴](#event-history) |
| $M_R$ 、 $M_\tau$ | [残存比率余白](#remaining-ratio-margin)、[残存吸収余白](#remaining-absorption-margin) |
| $o_n$ | [観測値](#observation-value) |
| $\mathsf{Out}^{(\mathrm{self})}_n$ | [評価出力](#evaluation-output) |
| $p_n$ | [残留ズレ](#residual-deviation) |
| $\mathrm{Phase}$ | [遷移位相](#transition-phase) |
| $\mathsf{Phys}^{(\mathrm{self})}_n$ | [対象状態](#target-physical-state) |
| $q_n$ 、 $q^{\mathrm{temp}}_n$ | [可逆成分](#reversible-deviation)、[一時的な可逆成分](#temporary-reversible-deviation) |
| $R$ 、 $R_{\mathrm{target}}$ | [境界接近比](#boundary-approach-ratio) |
| $R_{\mathrm{warn}}$ 、 $R_{\mathrm{handoff}}$ 、 $R_{\mathrm{irrev}}$ | [警告点](#warning-threshold)、[委譲点](#handoff-threshold)、[不可逆遷移開始点](#irreversible-threshold) |
| $R_{\mathrm{upper}}$ 、 $R_{\mathrm{lower}}$ 、 $R_{\mathrm{dir}}$ | 側別比・側別補助集約（補助。正規 $R$ ではない。FORMULA §4.5・§4.6） |
| $S$ | [構造感度](#structural-sensitivity) |
| $\mathsf{State}_n$ | [状態区分](#target-state) |
| $u$ | $\delta$ と $\tau$ に共通の単位 |
| $\mathsf{Update}$ | 更新規則（導出文書 第3部） |
| $W$ | [仕事量](#work-quantity) |
| $Z_n$ | [判定用十分状態](#decision-sufficient-state) |

### 2.2 ギリシャ文字

| 記号 | 見出し |
|---|---|
| $\alpha_u$ 、 $\alpha_l$ | 平滑係数（FORMULA §4.2。固定名 `alpha_upper`・`alpha_lower`） |
| $\gamma$ | 減衰係数（FORMULA §5） |
| $\delta$ 、 $\delta_{\mathrm{upper}}$ 、 $\delta_{\mathrm{lower}}$ | [蓄積ズレ](#accumulated-deviation)（側別は FORMULA §4.1） |
| $\epsilon$ | 最小閾値・ゼロ近傍（AXIOMS §1） |
| $\ell_n$ | [不可逆ラッチ](#irreversible-latch) |
| $\lambda^{[e]}_n$ 、 $\lambda_n$ | [劣化度](#degradation-fraction) |
| $\Pi$ 、 $\Pi^{-1}$ | [射影](#projection)、[逆射影](#inverse-projection) |
| $\rho$ | 可逆応答（導出文書 第3部） |
| $\sigma$ | [射影規則](#observation-projection-rule) |
| $\tau$ 、 $\tau_n$ 、 $\tau_0$ 、 $\tau^{[e]}_0$ 、 $\tau_{\mathrm{restored}}$ | [吸収厚み](#absorption-thickness)、[実効厚み](#effective-thickness)、[宣言厚み](#declared-thickness)、[復元後の吸収厚み](#restored-thickness) |
| $\tau_{\mathrm{upper}}$ 、 $\tau_{\mathrm{lower}}$ | [側別有効ゲート幅](#side-specific-gate-width) |
| $\Phi(x)$ | 補助計算項（FORMULA §5.1）。遷移位相 $\mathrm{Phase}$ とは別 |
| $\omega$ | [構造連続性](#structural-continuity) |

### 2.3 装飾文字

現在、装飾文字の記号はない。 $\mathcal{C}_n$ ・ $\mathcal{W}^{(\mathrm{self})}_n$ ・ $\mathcal{K}^{(\mathrm{self})}$ ・ $\mathcal{Y}^{(\mathrm{self})}_n$ は、2026-09-29に $\mathsf{Active}_n$ ・ $\mathsf{Phys}^{(\mathrm{self})}_n$ ・ $\mathsf{Gauge}^{(\mathrm{self})}$ ・ $\mathsf{Out}^{(\mathrm{self})}_n$ へ改め、2.1へ移した。

### 2.4 演算子・関係（規則の対象外）

| 表示 | 意味 | 注意 |
|---|---|---|
| $\sum$ | 和 | 添字の範囲を明記する |
| $\Delta$ | 差分・増分 | **後退差分**で書く： $\Delta x_n=x_n-x_{n-1}$ （FORMULA §4.7）。導出文書は2026-09-29に後退差分へ揃えた |
| $\mathrm{d}/\mathrm{d}t$ 、 $\partial$ | 微分、偏微分 | 微分の d は立体（0.5）。FORMULA §4.7は斜体（未反映） |
| $\int$ 、 $\lim$ | 積分、極限 | — |
| $\to$ | 文脈で意味が変わる：極限、写像の向き、計算の経路の辺 | 経路の辺では「どの量からどの量を計算するか」 |
| $\leadsto$ | 経路が存在する（何段かを経て届く） | — |
| $\Rightarrow$ 、 $\not\Rightarrow$ 、 $\iff$ | ならば、ならばとは限らない、同値 | — |
| $\land$ 、 $\lor$ | かつ、または | ラッチの式の $\lor$ は論理和 |
| $\in$ 、 $\subseteq$ 、 $\cup$ 、 $\exists$ | 属する、部分集合、和集合、存在する | — |
| $\emptyset$ | **定義域外**（AXIOMS §1） | 空集合の意味では使わない |
| $\max$ 、 $\min$ 、 $\arg\max$ | 最大、最小、最大を与えるもの | — |
| $\lvert x\rvert$ | 絶対値 | 記録の個数には使わない（→ $\#$ ） |
| $\#$ | 記録の個数 | $\#\mathsf{History}_n$ |
| $\mathbf{1}\{\cdot\}$ | 指示関数（真なら1、偽なら0） | — |
| $\approx$ 、 $\sim$ 、 $\ll$ 、 $\gg$ | 近似、漸近的に等しい、非常に小さい・大きい | — |
| $\oplus$ | **記録列の末尾への接続** | 加算・直和・排他的論理和ではない |
| $\mathbb{R}$ 、 $\mathbb{R}_{\mathrm{finite}}$ | 実数、有限な実数 | — |
| $\boxed{\ }$ | その節の結論の式 | — |
| ∎ | 証明の終わり | — |

### 2.5 次元の記号（規則の対象外）

| 表示 | 意味 | 注意 |
|---|---|---|
| $[x]$ | 量 $x$ の次元 | — |
| $\mathsf{L}$ 、 $\mathsf{M}$ 、 $\mathsf{T}$ 、 $\mathsf{I}$ 、 $\mathsf{\Theta}$ 、 $\mathsf{N}$ 、 $\mathsf{J}$ | ISQの基本次元 | サンセリフの立体大文字（0.5） |
| $X$ 、 $T$ （FORMULA §5.2） | 状態の次元、時間の次元 | 現在の正典は斜体（未反映） |
| $[R]=1$ | 無次元 | — |

---

## 3. 固定名の部（英字順）

| 固定名 | 見出し |
|---|---|
| `active_elements` | [構成](#active-elements) |
| `alpha_upper`・`alpha_lower` | 平滑係数（2.2） |
| `applied_action` | [作用](#applied-action) |
| `audit_log` | 非推奨の結合表示。正規は `structural_disclosure_log` と `input_exception_log` |
| `CONFESSION` | [告白](#confession) |
| `d_delta_dt`・`d_tau_dt` | ズレ・厚みの変化率（二重ゆらぎ。FORMULA §4.7） |
| `decision_sufficient_state` | [判定用十分状態](#decision-sufficient-state) |
| `declared_target` | 宣言対象（FORMULA §0） |
| `delta`・`observed_delta` | [蓄積ズレ](#accumulated-deviation) |
| `delta_upper`・`delta_lower`（引数 `current_delta_upper`・`current_delta_lower`） | 側別の蓄積ズレ（FORMULA §4.1） |
| `dominant_side` | [支配側](#dominant-side) |
| `element_declared_tau` | 要素の宣言厚み（[構造要素](#structural-element)） |
| `element_degradation_fraction` | [劣化度](#degradation-fraction) |
| `element_id` | [構造要素](#structural-element) |
| `entropy_export` | 離散遷移で持ち越さない残差（[エントロピー相当量](#entropy-quantity)の書き方） |
| `entropy_quantity` | [エントロピー相当量](#entropy-quantity) |
| `evaluation_archive` | [保管記録](#evaluation-archive) |
| `evaluation_declaration` | [評価宣言](#evaluation-declaration) |
| `evaluation_gauge` | [計器](#evaluation-gauge) |
| `evaluation_output` | [評価出力](#evaluation-output) |
| `event_allocation_rule` | [分解規則](#event-allocation-rule) |
| `event_history` | [経路履歴](#event-history) |
| `external_constraint` | [制約](#external-constraint) |
| `initial_tau` | [宣言厚み](#declared-thickness) |
| `instantaneous_classification` | [瞬間分類](#instantaneous-classification) |
| `irreversible_latched` | [不可逆ラッチ](#irreversible-latch) |
| `NOT_OBSERVABLE` | [観測不能](#not-observable) |
| `observation_event` | [観測事象](#observation-event) |
| `observation_projection_rule` | [射影規則](#observation-projection-rule) |
| `observation_value` | [観測値](#observation-value) |
| `omega` | [構造連続性](#structural-continuity) |
| `other_target_index` | [他構造](#other-target) |
| `OUT_OF_DESCRIPTION_DOMAIN` | [定義域外](#out-of-domain) |
| `R`・`R_upper`・`R_lower`・`R_dir` | [境界接近比](#boundary-approach-ratio)、側別比 |
| `r_warn`・`r_handoff`・`r_irrev`（出力 `thresholds.R_warn` など） | 閾値 |
| `R_op`・`Rop`・`rop`・`r_op` | 互換入力（→ `R_handoff`・`r_handoff`）。新しい文書では使わない |
| `remaining_absorption_margin`（旧 `remaining_slack`） | [残存吸収余白](#remaining-absorption-margin) |
| `remaining_ratio_margin` | [残存比率余白](#remaining-ratio-margin) |
| `residual_deviation` | [残留ズレ](#residual-deviation) |
| `reversible_deviation` | [可逆成分](#reversible-deviation) |
| `subject_target` | [自構造](#subject-target) |
| `target_physical_state` | [対象状態](#target-physical-state) |
| `target_state` | [状態区分](#target-state) |
| `tau`・`observed_tau` | [吸収厚み](#absorption-thickness) |
| `tau_upper`・`tau_lower` | [側別有効ゲート幅](#side-specific-gate-width) |
| `temporary_reversible_deviation` | [一時的な可逆成分](#temporary-reversible-deviation) |
| `thickness_composition_rule` | [合成規則](#thickness-composition-rule) |
| `transition_phase` | [遷移位相](#transition-phase) |
| `work_quantity` | [仕事量](#work-quantity) |

---

## 4. 添字とラベルの約束

### 4.1 添字・上付き

| 表示 | 意味 |
|---|---|
| $_n$ | 構造更新番号。事象 $\mathrm{Ev}_n$ が状態を $n-1$ から $n$ へ進める（時刻ではない） |
| $_t$ | 時刻（FORMULA・AXIOMS） |
| $_0$ | 評価開始時・遷移前 |
| $^{[e]}$ | 構造要素 $e$ |
| $^{(\mathrm{self})}$ 、 $^{(i)}$ | 自構造、他構造 $i$ |
| $^{(j)}$ | 評価番号 $j$ |
| $^{(-)}$ 、 $^{(+)}$ | 一つの事象の前と後 |
| $_{\mathrm{upper}}$ 、 $_{\mathrm{lower}}$ | 上側、下側（二次式） |
| $_{\mathrm{warn}}$ 、 $_{\mathrm{handoff}}$ 、 $_{\mathrm{irrev}}$ | 閾値の種類 |
| $^{\mathrm{temp}}$ | 一時的 |
| $_{\mathrm{low}}$ 、 $_{\mathrm{high}}$ | 比べる二つの対象（導出文書 命題4） |

### 4.2 ラベル（規則の対象外）

| ラベル | 意味 | 注意 |
|---|---|---|
| P0〜P9 | 導出文書の前提 | — |
| (i)〜(vi) | P9と第3部の条件（ローマ数字） | 他構造の添字 $i$ とは別 |
| 【1】〜【11】 | 導出文書 第1部の節 | — |
| 段1〜段7 | 導出の鎖の段 | — |
| 補題1〜3、命題0〜6（2a・2bを含む） | 導出文書の補題・命題 | — |
| LC-1〜LC-4 | 連結条件 | 以前のC1〜C4 |
| §n | 文書の節 | — |
| 逆導出A・B | 逆導出の区分 | — |
| 大文字の英語（PERMITなど） | 正規状態・分類の名前 | — |
| 表の中の「A」「B」 | 比べる対象の名前 | 記号ではない |

---

## 5. 混同の記録（日付順）

中身は各見出しの「混同注意」にある。ここは日付順の案内である。

| 日付 | 何と何を混同したか | 見出し |
|---|---|---|
| 2026-09-26 | 吸収厚み（総幅）と、残り（余白） | [吸収厚み](#absorption-thickness)、[残存吸収余白](#remaining-absorption-margin) |
| 2026-09-27 | 「逆導出」の語が少なくとも九つの意味で使われていた | [逆導出](#reverse-derivation) |
| 2026-09-27 | 方向性だけの指示を、正典の書き込みの許可と取り違えた（作業の進め方） | 経過の記録 4章 |
| 2026-09-28 | 蓄積ズレが減り得るか（可逆成分を含むか）が正典になかった | [蓄積ズレ](#accumulated-deviation) |
| 2026-09-28 | 「可逆進入」と正典の「可逆成分」 | [可逆成分](#reversible-deviation) |
| 2026-09-28 | 基準状態 $x_{\mathrm{ref}}$ と参照状態 $x_{\mathrm{exact}}$ | [基準状態](#reference-state) |
| 2026-09-28 | 観測不能とCONFESSION（両方向の誤り） | [観測不能](#not-observable) |
| 2026-09-28 | Π⁻¹（逆推論）と Π⁻¹（逆導出） | [逆推論](#reverse-inference) |
| 2026-09-29 | 補充・補修・復元と、構造要素の付加 | [構造要素の付加](#structural-element-addition)、[補充](#replenishment)、[補修](#repair) |
| 2026-09-29 | 測定し直し・構造の変化と、次の評価スナップショット | [評価スナップショット](#evaluation-snapshot) |
| 2026-09-29 | 矯正と補修（残留ズレは減るか） | [矯正](#straightening) |
| 2026-09-29 | 健全な要素を外すことと、破断 | [構造要素の除去](#structural-element-removal) |
| 2026-09-29 | 一時的に狭まる幅と、実効厚みの減少 | [一時的な可逆成分](#temporary-reversible-deviation) |
| 2026-09-29 | $\tau_{\mathrm{restored}}$ と、付加を含む全体の厚み | [復元後の吸収厚み](#restored-thickness) |
| 2026-09-29 | 他構造の評価出力と、観測された物理的事象 | [境界接近比](#boundary-approach-ratio)、[他構造](#other-target) |
| 2026-09-29 | 保存された評価出力 $R$ と、物理法則の中の比 | [逆導出](#reverse-derivation) |
| 2026-09-29 | 物理状態・評価状態・経路履歴 | [対象状態](#target-physical-state)、[経路履歴](#event-history) |
| 2026-09-29 | 単一要素の $\tau_0$ ・ $\lambda_n$ と、要素を複数にした一般形 | [劣化度](#degradation-fraction)、[宣言厚み](#declared-thickness) |
| 2026-09-29 | 字体・大小だけの区別（ $\mathcal{D}$ と $D$ 、 $\Gamma$ と $\gamma$ 、 $\Lambda$ と $\lambda$ 、 $Q$ と $q$ 、 $E$ と $e$ など） | 各見出し、0.5 |
| 2026-09-29 | 正典に加えた記号（制約 $C$ ・仕事量 $W$ ）と、導出文書の $\mathcal{C}_n$ ・ $\mathcal{W}_n$ （装飾だけの区別）。 $\mathcal{K}$ とknee値 $k$ | [構成](#active-elements)、[対象状態](#target-physical-state)、[計器](#evaluation-gauge) |
| 2026-09-29 | 評価出力の使い道を狭く書いた | [評価出力](#evaluation-output) |
| 2026-09-29 | 差分 $\Delta$ の向き（前進と後退） | 2.4 |
| 2026-09-29 | 記録の個数と絶対値（ $\lvert\cdot\rvert$ ） | [経路履歴](#event-history) |
| 2026-09-29 | 正典v2.4の補助構造量（ $\omega$ ・ $\mathrm{Phase}$ ・ $C$ ・ $W$ ・ $\mathrm{entropy}$ ）が辞書になかった。 $\omega$ を「遷移継続量」とも呼んでいた（docs 12章） | [構造連続性](#structural-continuity)、[遷移位相](#transition-phase)、[制約](#external-constraint)、[仕事量](#work-quantity)、[エントロピー相当量](#entropy-quantity) |
| 2026-09-30 | 余裕と余白（総幅 $\tau$ と残り $M_\tau$ が同じ「余裕」になっていた） | [残存吸収余白](#remaining-absorption-margin)、[残存比率余白](#remaining-ratio-margin) |
| 2026-09-30 | 制約 $C$ （条件）と作用 $a_n$ （計上された入力） | [制約](#external-constraint)、[作用](#applied-action) |

---

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
