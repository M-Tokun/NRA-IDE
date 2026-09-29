# NRA-IDE 記号・名前索引 / NRA-IDE Symbol and Name Index

**Version:** 1.0（名前を確定。2026-09-29） / 1.0 (names fixed, 2026-09-29)  
**Author:** M-Tokuni  
**Document role:** 記号・正規の固定名・API名・型・出所・使用先・定義元を対応づける索引 / An index mapping symbols to fixed names, API names, types, origins, permitted uses, and defining sources

---

## 0. 位置付け / Role

本書は、NRA-IDEで使用される数学記号、正規の固定名、API名、実装名、型、出所、許可された使用先、および定義元を対応づける索引である。本書は正典の定義を作らず、変更しない。意味または記号予約が競合する場合は、`theory/AXIOMS.md` §16の優先順位と `FORMULA.md` §7に従う。本書は独自の予約権限を持たない。

This document is an index that maps the mathematical symbols, canonical fixed names, API names, implementation names, types, origins, permitted uses, and defining sources used in NRA-IDE. It neither creates nor changes canonical definitions. Where meanings or symbol reservations conflict, the precedence order of `theory/AXIOMS.md` §16 and `FORMULA.md` §7 govern. This document holds no reservation authority of its own.

### 0.1 名前の採用順 / Naming precedence

名前は次の順で採用する。既存の名前があるものは、それを採り、本書で新しい名前を作らない。

1. `theory/AXIOMS.md` の正規表記
2. `theory/axioms.json` の機械可読名
3. 正規参照実装（`nra-core/foundations/NRA-IDE_Architecture_public.py`）の公開引数・出力フィールド
4. `FORMULA.md` の記号予約
5. 既存の名前がない場合だけ、新しい固定名を提案する

Names are adopted in the order above. Where a name already exists, it is adopted and this document does not create a new one. Temporary variables used only inside an implementation are distinguished from public fixed names (for example, the internal `ratio` in the reference implementation is not an alternative name for the public output `R`).

### 0.2 列の意味 / Columns

| 列 | 意味 |
|---|---|
| 型 | 構造量（Cause-Side）、評価出力、評価状態、計器、対象状態、宣言、写像、添字、記録 のいずれか |
| 出所 | その値がどこから得られるか |
| 使ってよい先 | その値を入力にしてよい計算・出力 |
| 使ってはならない先 | その値を入力にしてはならない先（逆導出・物理的事象の原則による） |

---

## 1. 正典に定義がある記号 / Symbols defined in the canon

### 1.1 一次式・余白・閾値・状態 / Primary formula, margins, thresholds, states

| 日本語名 | English | 表示 | 固定名（API・出力） | 型 | 単位 | 出所 | 使ってよい先 | 使ってはならない先 | 定義元 |
|---|---|---|---|---|---|---|---|---|---|
| 蓄積ズレ | Accumulated Deviation | $\delta$ | `delta`（出力 `observed_delta`） | 構造量（Cause-Side） | $u$ | Cause-Side観測、評価前に固定した変換規則 | $R$ の計算、対象の物理法則、構造証言、監査 | Effect-Side由来の値による更新（逆導出A） | AXIOMS §4・§5、FORMULA §1 |
| 吸収厚み | Absorption Thickness | $\tau$ | `tau`（出力 `observed_tau`） | 構造量（Cause-Side） | $u$ | Cause-Side観測、評価前に固定した変換規則、構造要素の付加（加えた時点の測定） | $R$ の計算、対象の物理法則、構造証言、監査 | 自然回復としての増加、評価出力による更新 | AXIOMS §4・§7、FORMULA §1 |
| 境界接近比 | Boundary Approach Ratio | $R$ | `R` | 評価出力 | 無次元 | $\delta/\tau$ （同一スナップショット） | 状態分類、不可逆ラッチ、監査、構造証言、事前固定された物理制御の指令。他の評価対象の閾値・有効ゲート幅へは、安全側の向きで閉路がない場合に限る | 同じ評価対象の計器（逆導出B）、対象状態 | AXIOMS §5・§14、FORMULA §1 |
| 境界接近警告点 | Boundary Warning Point | $R_{\mathrm{warn}}$ | `r_warn`（出力 `thresholds.R_warn`） | 計器（閾値） | 無次元 | 評価前の宣言 | 状態分類 | 評価出力による変更 | AXIOMS §9・§10.2 |
| 境界前人間委譲点 | Pre-Boundary Human Handoff Point | $R_{\mathrm{handoff}}$ | `r_handoff`（出力 `thresholds.R_handoff`） | 計器（閾値） | 無次元 | 評価前の宣言 | 状態分類 | 評価出力による変更 | AXIOMS §1・§9・§10.3 |
| 不可逆遷移開始点 | Irreversible Transition Onset | $R_{\mathrm{irrev}}$ | `r_irrev`（出力 `thresholds.R_irrev`） | 計器（閾値） | 無次元 | 評価前の宣言 | 状態分類、不可逆ラッチ | 評価出力による変更 | AXIOMS §9・§10.4 |
| 完全破断境界 | Complete Rupture Boundary | $R=1.0$ | — | 不変の境界 | 無次元 | 正典 | 状態分類 | 領域ごとの変更 | AXIOMS §9・§10.5 |
| 不可逆ラッチ | Irreversible Latch | $\ell_n$ | `irreversible_latched` | 評価状態 | 真偽 | $R$ と以前のラッチ | 状態分類、構造証言 | 自動解除 | AXIOMS §10.4 |
| 残存比率余白 | Remaining Ratio Margin | $M_R$ | `remaining_ratio_margin` | 派生出力 | 無次元 | $1-R$ | 構造証言、監査 | — | AXIOMS §5、FORMULA §2 |
| 残存吸収余白 | Remaining Absorption Margin | $M_\tau$ | `remaining_absorption_margin` | 派生出力 | $u$ | $\tau-\delta$ | 構造証言、監査、構造感度 | — | AXIOMS §5、FORMULA §2 |
| 構造感度 | Structural Sensitivity | $S$ | — | 派生出力 | $u^{-1}$ | $1/M_\tau$ | 構造証言、監査 | — | FORMULA §3 |
| 対象の境界接近比 | Target Boundary Approach Ratio | $R_{\mathrm{target}}$ | `R` | 評価出力 | 無次元 | 評価前に一意に宣言した対象の $\delta/\tau$ | $R$ と同じ | $R$ と同じ | AXIOMS §10.5、FORMULA §0 |
| 初期（基準）吸収厚み | Initial (Baseline) Absorption Thickness | $\tau_0$ | `initial_tau`（参照実装 `DynamicTauEngine` の引数） | 構造量（Cause-Side） | $u$ | 評価開始前・遷移前に固定した構造全体の吸収厚み | τ状態遷移式、復元劣化の比較 | 評価中の付け直し | AXIOMS §7・§8 |
| 復元後の吸収厚み | Restored Absorption Thickness | $\tau_{\mathrm{restored}}$ | — | 構造量（Cause-Side） | $u$ | 復元を目的とする操作の後に、同一対象・同一単位・同一測定規則で評価した後継構造のうち、付加した要素を除く既存の要素の厚み | 復元劣化の立証 | 付加した要素を含む全体の厚みとしての使用 | AXIOMS §8 |
| 消耗率関数 | Depletion Rate Function | $f(\delta)$ | — | 補助モデル（写像） | $u$ /時間 | 領域ごとの補助モデル | τ状態遷移式 | 評価出力を入力にすること | AXIOMS §7 |
| 対象状態区分 | Target Boundary State | — | `target_state`（値：`PERMIT`・`BOUNDARY_WARNING`・`HANDOFF_REQUIRED`・`IRREVERSIBLE_TRANSITION`・`RUPTURE_BOUNDARY`） | 正規状態 | — | 有効な $R$ とラッチ | 実行権限の制約、構造証言、監査 | — | AXIOMS §9〜§11.1 |
| 定義域外 | Out of domain | $\emptyset$ | `OUT_OF_DESCRIPTION_DOMAIN`（出力 `status`） | 分類 | — | $\tau=0$ | 構造証言 | $R$ を無限大へ置き換えること | AXIOMS §1・§6・§10.7 |
| 告白 | Confession | — | `CONFESSION`（出力 `status`） | 分類（不明時の停止信号） | — | 不明・不正・非有限な入力 | 構造証言 | 既知の危険接近の報告に使うこと | AXIOMS §6・§10.6 |
| 観測不能 | Not Observable | — | `NOT_OBSERVABLE` | 観測チャネル状態 | — | 観測経路から値が得られない | 欠損理由の出力 | CONFESSIONへの読み替え、0・安定・回復としての補完 | AXIOMS §10.2・§11.1・§11.2 |
| 構造連続性 | Structural Continuity | $\omega$ | — | 構造概念 | — | 正典 | — | — | AXIOMS §1 |
| 最小閾値・ゼロ近傍 | Minimum Threshold / Near-Zero | $\epsilon$ | — | 数値条件 | — | 正典 | — | — | AXIOMS §1 |
| 宣言対象 | Declared Target | — | `declared_target` | 宣言 | — | 評価前の固定 | 対象の同定 | — | FORMULA §0、AXIOMS §10.5 |

### 1.2 二次式（二重ゆらぎ式） / Secondary Formula

| 日本語名 | English | 表示 | 固定名（API・出力） | 型 | 出所 | 使ってはならない先 | 定義元 |
|---|---|---|---|---|---|---|---|
| 上側・下側蓄積ズレ | Upper/Lower-Side Accumulated Deviation | $\delta_{\mathrm{upper}}$ 、 $\delta_{\mathrm{lower}}$ | `delta_upper`・`delta_lower`（引数 `current_delta_upper`・`current_delta_lower`） | 構造量（Cause-Side） | Cause-Side観測 | Effect-Side由来の値による更新 | FORMULA §4.1 |
| 側別有効ゲート幅 | Side-Specific Effective Gate Width | $\tau_{\mathrm{upper}}$ 、 $\tau_{\mathrm{lower}}$ | `tau_upper`・`tau_lower` | 計器 | $\tau$ と側別EMAの形状変換 | 評価出力（ $R$ 系）を形状変換の入力にすること | FORMULA §4.4 |
| 側別境界接近比 | Side-Specific Boundary-Approach Ratio | $R_{\mathrm{upper}}$ 、 $R_{\mathrm{lower}}$ | `R_upper`・`R_lower` | 評価出力（補助） | 側別の比 | 正規 $R$ としての使用 | FORMULA §4.5 |
| 側別補助集約 | Directional Auxiliary Aggregate | $R_{\mathrm{dir}}$ | `R_dir` | 評価出力（補助） | 側別比の最大 | 正規 $R$ としての使用、正規状態の直接分類 | FORMULA §4.6 |
| 支配側 | Dominant Side | $D$ | `dominant_side` | 補助出力 | 側別比の比較 | 他の意味での使用 | FORMULA §4.6 |
| 平滑係数 | Smoothing Coefficients | $\alpha_u$ 、 $\alpha_l$ | `alpha_upper`・`alpha_lower` | 計器 | 評価前の固定 | 評価出力による変更 | FORMULA §4.2 |
| 形状変換関数 | Shape-Transformation Functions | $h_{\mathrm{upper}}$ 、 $h_{\mathrm{lower}}$ | — | 計器（写像） | 評価前の固定 | 評価出力を入力にすること | FORMULA §4.4 |
| ズレ・厚みの変化率 | Rates of Change | $d\delta/dt$ 、 $d\tau/dt$ | `d_delta_dt`・`d_tau_dt`（出力 `double_fluctuation`） | Cause-Side派生量 | 観測、事前固定の差分規則 | — | FORMULA §4.7 |

### 1.3 補完式 / Complementary Formula（FORMULA §5）

FORMULA §5の記号（ $x$ 、 $x_{\mathrm{exact}}$ 、 $r$ 、 $\gamma$ 、 $k$ 、 $F_{\mathrm{IDE}}$ 、 $\Phi$ 、 $G(r)$ ）は同節の定義による。他の文書でこれらと同じ基底名を別の意味に使わない（5章の衝突の解消を参照）。

### 1.4 射影 / Projection（SANDWICH_ARCH）

| 日本語名 | English | 表示 | 型 | 注意 | 定義元 |
|---|---|---|---|---|---|
| 射影 | Projection | $\Pi$ | 操作（Effect-Side内容の選別） | 可逆な写像ではない | SANDWICH_ARCH §8.2 |
| 逆射影 | Inverse Projection | $\Pi^{-1}$ | 禁止された逆向き経路の名前 | $\Pi$ の数学的な逆写像ではない | SANDWICH_ARCH §8.3・§8.4 |

### 1.5 互換名（新しい文書では使わない） / Compatibility aliases (not used in new documents)

| 互換名 | 正規名 | 定義元 |
|---|---|---|
| `R_op`、`Rop`、`rop`（表記）、`r_op`、`rop`（実装引数） | `R_handoff` ／ `r_handoff` | AXIOMS §1、参照実装 |
| `remaining_slack` | `remaining_absorption_margin` | 参照実装（非推奨の別名） |
| `audit_log`（結合表示） | `structural_disclosure_log` と `input_exception_log` | 参照実装（非推奨の結合表示） |

---

## 2. 導出文書の記号 / Symbols of the derivation document

`theory/NRA-IDE_Primary_Formula_Derivation_Bilingual.md` で使う記号。評価宣言・射影・分解・合成などは、現時点では導出文書が置く前提であり、FORMULA.md §0.5への反映を予定している。「表示」は、5章の規則による名前であり、2026-09-29に確定し（6章）、同日に導出文書へ反映した。「旧表示」は反映前の表示である。

| 日本語名 | English | 旧表示 | 表示 | 固定名 | 型 | 出所 | 使ってよい先 | 状態 |
|---|---|---|---|---|---|---|---|---|
| 評価宣言 | Evaluation Declaration | $\mathcal{D}$ | $\mathsf{Decl}$ | `evaluation_declaration` | 宣言 | 評価前の固定 | 当該評価の全体 | 改名（ $D$ との字体だけの区別をやめる） |
| 構造更新番号 | Update Index | $n$ | $n$ | `update_index` | 添字 | 更新の順序 | 各状態量 | 維持 |
| 評価番号 | Evaluation Index | $j$ | $j$ | `evaluation_index` | 添字 | 評価間の遷移 | 宣言、保管記録 | 維持 |
| 自構造 | Subject Target | $G$ | $(\mathrm{self})$ | `subject_target` | 添字（ラベル） | 評価宣言 | 自構造の状態・計器・出力 | 改名（3章） |
| 他構造 | Other Target | $i$ | $i$ | `other_target_index` | 添字 | 外部の構造 | 連結経路 | 維持 |
| 構造要素 | Structural Element | $e$ | $e$ | `element_id` | 添字 | 付加の時点で確定 | 要素ごとの状態 | 維持 |
| 観測値 | Observation Value | $o_n$ | $o_n$ | `observation_value` | Cause-Side入力 | 観測 | 射影規則 | 維持 |
| 観測事象 | Observation Event | $E_n$ | $\mathrm{Ev}_n$ | `observation_event` | 事象記録 | 観測 | 分解規則、経路履歴 | 改名（ $e$ との大小だけの区別をやめる） |
| 射影規則 | Observation Projection Rule | $\sigma$ | $\sigma$ | `observation_projection_rule` | 写像 | 評価前の固定 | $\delta$ | 維持 |
| 分解規則 | Event Allocation Rule | $\Lambda$ | $\mathsf{Alloc}$ | `event_allocation_rule` | 写像 | 評価前の固定 | $a$ 、 $p$ 、要素ごとの劣化度 | 改名（ $\lambda$ との大小だけの区別をやめる） |
| 作用 | Applied Action | $a_n$ | $a_n$ | `applied_action` | 対象への入力 | 観測された物理的事象 | 可逆応答、劣化の法則 | 維持 |
| 文脈・権限・出所 | Event Context | $c_n$ | $\mathrm{ctx}_n$ | `event_context` | 付随情報 | 観測事象 | 記録（計上先ではない） | 改名（ $\mathcal{C}_n$ との大小・字体だけの区別をやめる） |
| 可逆成分 | Reversible Deviation | $q_n$ | $q_n$ | `reversible_deviation` | 対象状態 | 物理法則、射影との整合 | $\delta$ | 維持 |
| 一時的な可逆成分 | Temporary Reversible Deviation | $\mu_n$ | $q^{\mathrm{temp}}_n$ | `temporary_reversible_deviation` | 対象状態（ $q_n$ の一部） | 一時的な作用・条件の観測 | $q_n$ | 改名（「厚みの減少」という名前をやめる） |
| 残留ズレ | Residual Deviation | $p_n$ | $p_n$ | `residual_deviation` | 対象状態 | 観測された物理的事象 | $\delta$ | 維持 |
| 構成 | Active Elements | $\mathcal{C}_n$ | $\mathcal{C}_n$ | `active_elements` | 集合 | 付加・除去の事象 | 厚みの合成 | 維持（分類・条件の側を改名） |
| 要素の宣言厚み | Element Declared Thickness | $\tau^{[e]}_0$ | $\tau^{[e]}_0$ | `element_declared_tau` | 要素の状態 | 付加の時点のCause-Side測定 | 厚みの合成 | 一般形 |
| 要素の劣化度 | Element Degradation Fraction | $\lambda^{[e]}_n$ | $\lambda^{[e]}_n$ | `element_degradation_fraction` | 要素の状態 | 物理的な劣化の法則 | 要素の厚み | 一般形 |
| 単一要素の劣化度 | Single-Element Degradation Fraction | $\lambda_n$ | $\lambda_n$ | `single_element_degradation_fraction` | 特殊形 | 要素が一つのモデル | 要素が一つの式だけ | 使用範囲を限定 |
| 宣言厚み | Declared Thickness | $\tau_0$ | $\tau_0$ | — | 構造量（評価開始時の構造全体） | 評価宣言 | 正典（AXIOMS §7・§8）の $\tau_0$ と同じ意味で使う。一般には $\tau_0=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_0)_{e\in\mathcal{C}_0}\bigr)$ 、要素が一つなら $\tau_0=\tau^{[0]}_0$ | 意味を正典に合わせる（要素が一つの式だけの特殊形としない） |
| 厚みの合成規則 | Thickness Composition Rule | $\Gamma$ | $\mathrm{Comp}_\tau$ | `thickness_composition_rule` | 写像 | 評価前の固定 | $\tau$ | 改名（ $\gamma$ との大小だけの区別をやめる） |
| 更新規則 | State Update Rule | $\mathcal{U}$ | $\mathsf{Update}$ | `state_update_rule` | 写像 | 物理法則 | 対象状態 | 改名（引用中の $U$ との字体だけの区別をやめる） |
| 可逆応答 | Reversible Response Rule | $\rho$ | $\rho$ | `reversible_response_rule` | 写像 | 物理法則 | $q$ | 維持 |
| 残留ズレの増分則 | Residual Deviation Increment Rule | $g_p$ | $g_p$ | `residual_deviation_increment_rule` | 写像 | 物理法則 | $p$ | 維持 |
| 要素の劣化増分則 | Element Degradation Increment Rule | $g_\lambda$ | $g^{[e]}_\lambda$ | `element_degradation_increment_rule` | 写像 | 要素ごとの物理法則 | $\lambda^{[e]}$ | 要素ごとへ変更 |
| 対象の物理状態 | Target Physical State | $\mathcal{W}^{(G)}_n$ | $\mathcal{W}^{(\mathrm{self})}_n$ | `target_physical_state` | 状態記録 | Cause-Side | 物理法則、評価の計算 | `target_state`（正規状態）とは別 |
| 評価の計器 | Evaluation Gauge | $\mathcal{K}^{(G)}$ | $\mathcal{K}^{(\mathrm{self})}$ | `evaluation_gauge` | 計器の記録 | 評価前の固定 | 評価の計算 | 維持 |
| 評価出力 | Evaluation Output | $\mathcal{Y}^{(G)}_n$ | $\mathcal{Y}^{(\mathrm{self})}_n$ | `evaluation_output` | 出力の記録 | 対象状態と計器 | 状態分類、構造証言、監査、事前固定の物理制御の指令 | 維持 |
| 経路履歴 | Event History | $\mathcal{H}_n$ | $\mathsf{History}_n$ | `event_history` | 証言の記録 | 観測事象 | 監査、構造証言 | 改名（形状変換関数 $h$ との大小・字体だけの区別をやめる） |
| 繰返し回数 | Cycle Count | $N$ （命題5） | 語で書く（「繰返し回数」） | `cycle_count` | 領域の追加状態 | 観測 | 劣化の法則 | 改名（ $n$ との大小だけの区別をやめる） |
| 状態区分 | Latched Boundary State | $Q_n$ | $\mathsf{State}_n$ | `target_state` | 正規状態 | 有効な $R$ とラッチ | 構造証言、監査 | 改名（ $q$ との大小だけの区別をやめる） |
| 瞬間分類 | Instantaneous Classification | $C_0(R)$ | $\mathrm{Class}(R)$ | `instantaneous_classification` | 分類関数 | 有効な $R$ | 状態区分 | 改名（ $\mathcal{C}_n$ との区別） |
| 連結条件 | Link Conditions | C1〜C4 | LC-1〜LC-4 | `link_condition_1`〜`4` | 条件ラベル | P9の帰結 | 連結の検査 | 改名（ $\mathcal{C}_n$ との区別） |
| 評価の保管記録 | Evaluation Archive | $\mathcal{A}$ | $\mathsf{Archive}$ | `evaluation_archive` | 保管記録 | 終了した評価 | 監査、次の評価の来歴 | 改名（例の $A$ との字体だけの区別をやめる） |
| 展開評価グラフ | Expanded Evaluation Graph | $\mathcal{G}^{(j)}$ | $\mathrm{EvalGraph}^{(j)}$ | `expanded_evaluation_graph` | 有向グラフ | 宣言した計算経路 | 逆導出の検査 | 改名（ $G(r)$ との区別） |
| 判定用十分状態 | Decision-Sufficient State | $Z_n$ | $Z_n$ | `decision_sufficient_state` | 名前付きの状態記録（4章） | 更新規則が必要とする状態 | 次の更新 | 位置で並べる組から、名前付きの欄へ変更 |
| 前・後（事象の） | Before / After | $a$ 、 $b$ （命題2） | $(-)$ 、 $(+)$ | — | 添字 | — | — | 改名（作用 $a_n$ との衝突をやめる） |

物理法則の中で使う比 $\delta/\tau$ には、新しい記号（例：r_phys）を割り当てない。物理法則は $\Delta\lambda^{[e]}_n=g^{[e]}_\lambda(\delta_n,\tau_n,\dots)$ のように、Cause-Side由来の引数を直接示す。保存された評価出力 $R$ （その平均・集約・状態区分）を読み戻して対象状態を更新しない。

---

## 3. 添字の固定 / Fixed indices

| 添字 | 意味 | 注意 |
|---|---|---|
| $n$ | 構造更新番号（事象の順序。時刻ではない） | — |
| $j$ | 評価番号 | — |
| $(\mathrm{self})$ | 現在評価している自構造 | $k$ は使わない。FORMULA §5のknee値 $k$ 、導出文書6.2の係数 $k$ と衝突するため |
| $i$ | 影響を与える他構造、または部分構造 | 部分構造の個数に別の文字（ $m$ など）を使わず、「有限個」と書く（ $m$ は和の添字に使っているため） |
| $e$ | 自構造に含まれる構造要素 | 観測事象は $\mathrm{Ev}_n$ と書き、 $E$ を使わない |

したがって、 $\mathcal{W}^{(\mathrm{self})}_n$ と $\mathcal{W}^{(i)}_n$ （自構造と他構造の物理状態）、 $\mathcal{Y}^{(\mathrm{self})}_n$ と $\mathcal{Y}^{(i)}_n$ （自構造と他構造の評価出力）を区別できる。他構造の $\mathcal{Y}^{(i)}$ を自構造の $\mathcal{W}^{(\mathrm{self})}$ へ直接入れてはならない。他構造の物理的事象をCause-Sideで観測したものは、自構造の観測事象 $\mathrm{Ev}^{(\mathrm{self})}_n$ として扱える。

---

## 4. 判定用十分状態の欄 / Fields of the decision-sufficient state

$Z_n$ は、位置で並べる組ではなく、名前付きの欄を持つ記録とする。新しい状態を加えたときに、要約の更新漏れを欄の有無で検査できるようにするためである。

```text
decision_sufficient_state:
  residual_deviation              # p_n
  reversible_state                # q_n（更新規則が q_n に依存する場合）
  active_elements:                # 構成 C_n
    element_id:                   # e
      declared_tau                # τ0^[e]（付加の時点の測定値）
      degradation_fraction        # λ^[e]_n
      domain_memory               # 疲労回数・温度履歴など（必要な場合）
  irreversible_latched            # ℓ_n
  domain_global_memory            # 構造全体の追加状態（必要な場合）
```

---

## 5. 衝突の解消と規則 / Resolved collisions and rules

### 5.1 解消する衝突 / Collisions to resolve

導出文書の中で、字体・大小・書体・装飾の違いだけで別の意味を区別していた組、または同じ文字を別の意味に使っていた組。FORMULA.md の記号との組は、導出文書の記号をFORMULA.md §0.5へ反映したときに同一文書の中の衝突になるので、ここに含める。

| 組 | 衝突の内容 | 解消 |
|---|---|---|
| $\mathcal{D}$ と $D$ | 評価宣言と支配側（FORMULA §4.6） | $\mathsf{Decl}$ |
| $\Gamma$ と $\gamma$ | 合成規則と減衰係数（FORMULA §5） | $\mathrm{Comp}_\tau$ |
| 構造名 $G$ と $G(r)$ | 自構造と残差ゲート（FORMULA §5） | $(\mathrm{self})$ |
| $\mathcal{G}^{(j)}$ と $G(r)$ | 展開評価グラフと残差ゲート | $\mathrm{EvalGraph}^{(j)}$ |
| $\mathcal{C}_n$ と $C_0$ 、C1〜C4 | 構成と瞬間分類、連結条件 | $\mathrm{Class}$ 、LC-1〜LC-4 |
| $\Lambda$ と $\lambda$ | 分解規則と劣化度 | $\mathsf{Alloc}$ |
| $Q_n$ と $q_n$ | 状態区分と可逆成分 | $\mathsf{State}_n$ |
| $E_n$ と $e$ | 観測事象と構造要素 | $\mathrm{Ev}_n$ |
| $\mathcal{A}$ と例の $A$ | 保管記録と光合成速度（段1の例） | $\mathsf{Archive}$ |
| 例の $A$ と作用 $a_n$ | 光合成速度と作用 | 例の $A$ を語で書く（「光合成速度」） |
| $\mathcal{U}$ と引用中の $U$ | 更新規則と未観測の割合（6.3の先行草案の引用） | $\mathsf{Update}$ |
| $c_n$ と $\mathcal{C}_n$ | 文脈・権限・出所と構成 | $\mathrm{ctx}_n$ |
| $\mathcal{H}_n$ と $h_{\mathrm{upper}}$ 、 $h_{\mathrm{lower}}$ | 経路履歴と形状変換関数（FORMULA §4.4） | $\mathsf{History}_n$ |
| 命題5の $N$ と $n$ | 繰返し回数と構造更新番号 | 語で書く（「繰返し回数」） |
| 段7の $i=1,\dots,m$ の $m$ と和の添字 $m$ | 部分構造の個数と和の添字 | 語で書く（「有限個」） |
| 引用中の先行草案の記号（ $D_T$ 、 $\Phi$ 、 $T$ 、 $J_t$ 、 $G_{\max}$ 、 $h_t$ 、 $U$ ） | それぞれ $D$ 、FORMULA §5の $\Phi$ 、 $G(r)$ 、 $h_{\mathrm{upper}}$ 、単位 $u$ などと衝突する | 引用は語で言い換え、式は元の文書（先行草案）を参照する |
| 命題2の $a$ 、 $b$ と作用 $a_n$ | 事象の前後と作用 | $(-)$ 、 $(+)$ |
| 命題4の $\lambda_a$ 、 $\lambda_b$ と作用 $a_n$ | 二つの構造のラベルと作用 | $\lambda_{\mathrm{low}}$ 、 $\lambda_{\mathrm{high}}$ （導出文書の反映時に追加） |
| 自構造の添字 $k$ （案）と knee値 $k$ | 添字とFORMULA §5の係数、導出文書6.2の係数 | $(\mathrm{self})$ |
| $\lambda_n$ と $\lambda^{[e]}_n$ | 単一要素の特殊形と要素ごとの一般形 | $\lambda_n$ は要素が一つの式だけで使う |
| 名前「一時的な厚みの減少」 $\mu_n$ | 厚みの名前なのにズレの側に数える | $q^{\mathrm{temp}}_n$ |

### 5.2 規則（FORMULA.md §7へ提示予定。現時点では規範ではない） / Rule (to be proposed for FORMULA.md §7; not normative yet)

> 同一文書または同一実装内では、字体、大小文字、書体または装飾の違いだけによって、異なる意味の記号を区別してはならない。異なる意味には異なる基底名を使用する。

> Within the same document or implementation, distinct meanings must not be distinguished solely by font, letter case, typeface, or decoration. Distinct meanings must use distinct base names.

適用の範囲（提示時に確認する）：標準の数学演算子（ $\sum$ 、差分の $\Delta$ 、 $\partial$ 、 $d$ ）と、前提・節のラベル（P0〜P9、第1部の【1】〜【11】）は記号の割当に含めない。例えば $\Delta\delta_n$ の $\Delta$ は差分の演算子であり、 $\delta$ と別の意味の記号としては扱わない。

**正典自身の中の衝突**：この規則をそのままFORMULA.md §7へ入れると、FORMULA.md自身の中に規則に反する組が残る。

| 組 | 箇所 | 内容 |
|---|---|---|
| $R$ と $r$ | FORMULA §1（境界接近比）と §5（参照状態との差、残差） | 大小だけの区別 |
| $x$ と $X$ 、 $t$ と $T$ | FORMULA §5.1（計算状態、時間）と §5.2（次元の記号 $[x]=X$ 、 $[t]=T$ ） | 大小だけの区別 |

次元の記号は、次元解析の標準の表記として規則の対象から外すことができる。残差 $r$ は、外すか、FORMULA §5の記号を改めるか（正典の変更）を決める必要がある（6章 N5）。

---

## 6. 確定した事項 / Fixed items

2026-09-29、N1〜N6を下表のとおり確定した。

| # | 内容 | 確定した内容 |
|---|---|---|
| N1 | 自構造の表示 | $(\mathrm{self})$ 。 $k$ は既存の係数と衝突する |
| N2 | 5.1のうち、他の精査の一覧になかった追加の改名（ $\mathsf{Alloc}$ 、 $\mathsf{State}_n$ 、 $\mathrm{Ev}_n$ 、 $\mathsf{Archive}$ 、 $\mathsf{Update}$ 、 $\mathrm{ctx}_n$ 、 $\mathsf{History}_n$ 、 $(-)$ ・ $(+)$ 、語で書くもの（例の $A$ 、 $N$ 、 $m$ 、先行草案の引用）） | 改名する |
| N3 | 5.2の規則の適用の範囲（標準の数学演算子、ラベル、次元の記号を除く） | 除く |
| N4 | 本書の版表記 | 1.0とした |
| N5 | FORMULA §5の残差 $r$ と境界接近比 $R$ の大小だけの区別 | 規則をFORMULA §7へ提示するときに、残差の記号を改める案（他のどの記号とも衝突しない名前の候補を、提示時に示す）と、規則の対象から外す案の両方を示し、判断を仰ぐ |
| N6 | 宣言厚み $\tau_0$ の意味 | 正典（AXIOMS §7・§8）と同じく構造全体の初期（基準）吸収厚みとし、要素が複数のときは $\tau_0=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_0)_{e\in\mathcal{C}_0}\bigr)$ と読む。導出文書の「要素が一つの場合の式」はこの特別な場合 |

---

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
