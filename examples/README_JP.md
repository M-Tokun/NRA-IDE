# NRA-IDE Examples — Japanese Edition

<!-- README_JP.md | examples/ | updated 20260425_162324_JST -->

---

## 正規参照 Quick Demo

リポジトリルートで、現行の正規参照実装を実行します。

```powershell
python examples/nra_ide_reference_quick_demo.py
```

このデモは[`nra-core/foundations/NRA-IDE_Architecture_public.py`](../nra-core/foundations/NRA-IDE_Architecture_public.py)を直接呼び出し、`PERMIT`、`BOUNDARY_WARNING`、`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`、`CONFESSION`、`OUT_OF_DESCRIPTION_DOMAIN`の7状態を確認します。

閾値は説明用に明示した値であり、推論された既定値ではありません。このデモは独立した正規判定器ではなく、医療、自律制御、その他の運用判断には使用できません。

このディレクトリのその他の例は、研究・説明・例示・ドメイン固有・履歴資料を保存しており、旧状態名を使用する場合があります。

---

## NRA-IDE とは

**律環公理 — 内包性動力学エンジン（Nomological Ring Axioms — Intensional Dynamics Engine）**

NRA-IDEは、Cause-Sideの蓄積ズレと吸収厚みから、宣言された対象の現在の境界状態を記述します。変数はドメイン固有の観測と構成規則によって定めます。この評価構造は万能な物理モデルや安全保証を提供するものではありません。[ルートの概要](../README_JP.md)と[正典定義](../theory/AXIOMS.md)を参照してください。

---

## 数値残差と整数位相ロック

整数位相ロックは、丸め誤差や残差を監査せず次状態へ引き継がないための設計原則です。物理的・数値的な誤差がすべて存在しないことを意味せず、個々のデモには独立した検証が必要です。

値と出所が確定した既知の丸め、近似、廃棄残差は`STRUCTURAL_DISCLOSURE_LOG`へ記録します。未知、不正、曖昧、非有限、未対応の構造情報は`CONFESSION`とし、既知の数値進行と分けて`INPUT_EXCEPTION_LOG`へ記録します。

---

## 現行の正規閾値体系

`R = delta / tau`において、deltaは蓄積ズレ、tauは吸収厚み、Rは境界接近比です。有限のdelta >= 0、有限のtau > 0を必要とします。事前宣言したドメイン閾値は`0 <= R_warn < R_handoff < R_irrev < 1`を満たします。

| 正規状態 | 条件 | アダプターの運用動作 |
|---|---|---|
| `PERMIT` | 0 <= R < R_warn | CONTINUE |
| `BOUNDARY_WARNING` | R_warn <= R < R_handoff | LOG_WARN |
| `HANDOFF_REQUIRED` | R_handoff <= R < R_irrev | Fail-Closed |
| `IRREVERSIBLE_TRANSITION` | R_irrev <= R < 1, または不可逆ラッチ保持 | Fail-Closed |
| `RUPTURE_BOUNDARY` | R >= 1, または対象破断保持 | Fail-Closed |
| `CONFESSION` | 不正または未知の構造入力・宣言 | Fail-Closed |
| `OUT_OF_DESCRIPTION_DOMAIN` | その他の構造が有効でtau = 0 | Fail-Closed |

アダプターは呼出し間で不可逆・対象破断の履歴を保持し、Rの低下で解除しません。不正な新入力は対象履歴を解除せず別に開示します。Fail-Closedは影響する新規自律判断と自律操作を抑止する運用原則であり、第八の状態や完全沈黙ではありません。生存する観測・記録・通信は独立に継続し、対象破断後は`POST_RUPTURE_FIXED`の固定証言を継続します。

残余は別量です。`M_R = 1 - R`は無次元、`M_tau = tau - delta`はdeltaとtauと同じ単位です。具体的な閾値にはドメインの根拠が必要です。SOFTWARE_DEMOの0.4/0.6/0.8は未検証の説明値です。

以下の表は、履歴的・ドメイン固有デモのローカル挙動を説明するものです。SAFE/WATCH/CAUTION/R_Jの表示やreset操作は、現行の正規状態・閾値・回復権限を定義しません。

---

## デモ一覧（全50本以上のデモ + スタンドアロン可視化 — 推奨閲覧順）

ブラウザで開くだけで動作します（インストール不要）。

> 多くのデモでは表示上の赤線として R = 1.0 を示しますが、これは「警告線」ではなく構造限界線です。  

> 実務上の判断限界はその手前に置く必要があります。ただし、その値は固定ではなく、現場運用と対象ドメインに応じて設定されます。

### デモごとの判断限界（R_J）の一覧

**履歴デモの表示慣行：** 比率を用いる多くのデモは、R = 1.0をローカルな破断・抑止境界に使います。非正典スコアやその他の例外は各ソースで説明しています。0.4 は多くのデモで WATCH の開始です。その間の警告閾値（判断限界 R_J）は、デモごとに宣言した値で、固定の公理値ではありません（上の注記のとおり）。

| デモ | 警告・判断限界の値 | 備考 |
|---|---|---|
| #08〜#11 | WARN 0.65（ログ）／色は 0.7 | 上下別々に評価。SILENCE は R ≥ 1.0 |
| #12・#13・#17・#18〜#20・#27〜#32・#36〜#39 | WARN 0.75 | #36 は WATCH 0.4 も使う |
| #14 | CAVEAT 0.4 | R ≥ 1.0 または負債 > 0.8 で破断 |
| #15 | CAVEAT 0.35、CRITICAL 0.6 | R_eff（R_total ＋ 負債×0.4）で判定 |
| #23・#24 | DAMP 0.72 | 破断（SILENCE / FALLBACK）は 1.0 |
| #34・#35 JP・#48 | WARNING 0.7 | #35 EN は WATCH 0.40 / WARN 0.75（別実装） |
| #40・#41 | Watch 0.40、Caution 0.75 | Human Review は 1.0 |
| #42・#46 | ZONE B 0.40、C 0.70 | D（RUPTURE_BOUNDARY、運用動作はFail-Closed）は 1.0 |
| #43 | ZONE B 0.40、C 0.70、D 0.85 | E（RUPTURE_BOUNDARY、運用動作はFail-Closed）は 1.0 |

閾値の根拠はいずれもデモ用の宣言値で、実運用では対象・センサー遅延・停止に必要な時間から設定します。

> RUPTURE_BOUNDARY・FAIL・FALLBACK に入ったデモは、「新しい評価」（#23 は「初期化」）を押すまで状態を固定します（不可逆ラッチ）。R の値は現在値を表示し続けます。  

> 08〜11 の SILENCE は HOLD 時間が過ぎると解ける一時遮断であり、破断境界の固定とは別の概念です。

### 📚 STEP 1 — まず「なぜ？」を理解する

| # | ファイル | 内容 |
|---|---------|------|
| 00 | [00_Escapement_Foundation_NRA_JP.html](./00_Escapement_Foundation_NRA_JP.html) | **脱進機の基礎。** 整数位相ロック — 残差が消える理由の基礎概念デモ。 |
| 01 | [01_Why_No_Distance_JP.html](./01_Why_No_Distance_JP.html) | **なぜ距離・微分積分・浮動小数点を使わないのか？** タブ切替で4つの視点から視覚的に解説。従来手法との根本的な違いを理解する入口。 |
| 02 | [02_Error_Accumulation_JP.html](./02_Error_Accumulation_JP.html) | **誤差積算の恐怖。** 同一初期値から10万ステップ走らせ、従来手法と律環公理の誤差蓄積を比較。医療・自動運転・金融それぞれの破綻ラインを表示。 |

### 🔬 STEP 2 — 動作の違いを体感する

| # | ファイル | 内容 |
|---|---------|------|
| 03 | [03_HAN_vs_Legacy_JP.html](./03_HAN_vs_Legacy_JP.html) | **HAN（非線形適応制御） vs Legacy（If-Then固定制御）のリアルタイム比較。** 外乱・突発負荷に対する追従性と安定性の差を波形グラフで比較（簡易モデルによる例示。比を0.99、力を±20で打ち切っており、限界超過の完全な防止を保証するものではない）。 |
| 04 | [04_HAN_Stress_Test_JP.html](./04_HAN_Stress_Test_JP.html) | **意図的に80msの高負荷をかける極限実験。** Legacy は盲目的に命令を実行しFPSが崩壊。HAN は張力検知により負荷を適応的に軽減し、描画を維持。 |

### 📊 STEP 3 — 閾値メカニズムを可視化する

| # | ファイル | 内容 |
|---|---------|------|
| 05 | [05_IDE_Threshold_Visualizer_JP.html](./05_IDE_Threshold_Visualizer_JP.html) | **位相スコープで整数位相ロック・残差破棄の仕組みを表示。** R・δ・τ そのものは計算せず、離散化の様子を示す図。 |

### ⚙️ STEP 4 — 脱進機の原理

| # | ファイル | 内容 |
|---|---------|------|
| 06 | [06_Escapement_Principle_JP.html](./06_Escapement_Principle_JP.html) | **なぜ歯車は誤差を累積しないのか。** 浮動小数点ドリフト vs 整数位相ロックのアニメーション比較。NRA-IDEが誤差を構造的に排除する理由を可視化。 |

### 🔴 STEP 5 — カスケード障害：崩壊が始まる瞬間をリアルタイムで見る

| # | ファイル | 内容 |
|---|---------|------|
| 07 | [07_HAN_gate_live_JP.html](./07_HAN_gate_live_JP.html) | **カスケード障害の発生と HAN Gate の SILENCE 発動をライブシミュレーション。** 負荷スパイクとともに非正典の連鎖予兆スコアが上昇し、ローカル閾値に達すると SILENCE が発動します。正規 R = δ/τ の実装ではありません。**⚠ 危険例プリセット** では「波は穏やかに見えるのにゲートが一度も発動しない」設定を体験できます。 |

> **このデモが他と異なる理由：**

> 波形は静止したグラフではありません。本物のカスケード障害と同じように、

> 最初はゆっくり、やがて閾値を一気に越えるという時間的な進行を体感できます。

> オレンジの線はEMAによるスコア補助倍率であり、正典の吸収厚みτではありません。

> デモの正規化定数とEMA入力は配備用HAN Gateコードとは異なり、挙動の例示です。

> 固定倍率との違いを観察できます。

---

### 🌿 STEP 6 — Band Gate：実世界ドメイン応用

Band Gate（R = δ/τ）を物理計測ドメインに適用したデモ群です。

上限・下限を同時監視し、**非対称EMA感度** によって過負荷（上限超過）と枯渇（下限割れ）を同じ R = δ/τ で検知します。

| # | ファイル | ドメイン | ポイント |
|---|---------|---------|---------|
| 08 | [08_Band_Gate_live_JP.html](./08_Band_Gate_live_JP.html) | 電気・気温・水圧・脈動（JP） | **非対称ダンパー構造** — δは基準値からのズレ、R = 1.0 が宣言上下限。ズレが続くとτを縮めて検知を早める（広げない）。上限側は縮みにくく（慎重）、下限側は大きく縮む（敏感）。左のダンパーアニメーションで2つのスプリングが逆方向に動く様子を確認できます。 |
| 08 | [08_Band_Gate_live_EN.html](./08_Band_Gate_live_EN.html) | 同上 — 英語版 | English labels and explanations. |
| 09 | [09_Greenhouse_BandGate_live_JP.html](./09_Greenhouse_BandGate_live_JP.html) | 温室農業 4指標同時監視（JP） | 灌漑水圧・気温・CO₂・養液ECを同時監視。**🏜 干ばつシミュレーション**で複数指標が同時低下する様子を観察できます。 |
| 09 | [09_Greenhouse_BandGate_live_EN.html](./09_Greenhouse_BandGate_live_EN.html) | 同上 — 英語版 | English labels and explanations. |
| 10 | [10_Field_DroughtGate_live_JP.html](./10_Field_DroughtGate_live_JP.html) | 屋外畑 干ばつ進行ゲージ（JP） | 土壌水分・地温・日射量・風速を監視。加重複合Rスコアから干ばつレベル **Lv.0〜4** を算出。**⛈ 嵐後急乾燥**シナリオでは、値が閾値を割る前にEMAが「乾き始めの勢い」を先読みする様子が体験できます——これが現在の農業IoT製品にない機能です。 |

> **現行の農業IoTにできないこと：**

> 市販の土壌センサーシステムのほとんどは、値が固定閾値を下回ったときにアラートを出すだけです。

> 「境界に向かう勢い」という概念を持ちません。

> ここで示すEMA先読み検知は、閾値だけの設計には構造的に存在しない機能です。

> これがNRA-IDEが埋めるギャップです。

---

### ⚙️ STEP 7 — 高度ドメイン応用（11〜16）

| # | ファイル | 内容 |
|---|---------|------|
| 11 | [JP](./11_Motor3Phase_BandGate_live_JP.html) / [EN](./11_Motor3Phase_BandGate_live_EN.html) | **三相モーター Band Gate ライブ監視。** 三相モーターの負荷バランスと過負荷検知に R = δ/τ をリアルタイム適用。 |
| 12 | [JP](./12_agri_mol_antagonism_JP.html) / [EN](./12_agri_mol_antagonism_EN.html) | **農業イオン監視 + Mg²⁺/K⁺ 拮抗連鎖 Band Gate。** 黒ぼく土（Andosol）/一般農耕地プロファイル切替対応。動的τ＋非対称EMA。Mg障害時にK⁺τ連結ゲートが発動。 |
| 13 | [JP](./13_photosynthesis_layer5_JP.html) / [EN](./13_photosynthesis_layer5_EN.html) | **光合成監視 Layer 5。** Farquhar-von Caemmerer-Berry（FvCB）モデルを外部δ生成装置として使用 → R = δ/τ。非線形プリプロセッサとしての Layer 5 実装。 |
| 14 | [JP](./14_powergrid_transition_JP.html) / [EN](./14_powergrid_transition_EN.html) | **電力系統・遷移点監視。** 電力系統における構造的遷移点を検知。固定閾値では見逃す早期乖離をNRA-IDEが捕捉する。 |
| 15 | [JP](./15_or_icu_continuum_JP.html) / [EN](./15_or_icu_continuum_EN.html) | **OR/ICU 経過蓄積型モニタリング。** 手術〜ICU フェーズを通じた累積ズレを追跡。R は瞬間値ではなく継続的な構造的負荷を反映。 |
| 16 | [JP](./16_passive_safety_JP.html) / [EN](./16_passive_safety_EN.html) | **受動型・重力駆動安全システム。** 能動制御なしで物理的制約（重力・張力）だけで安全状態に遷移するアーキテクチャ。 |

---

### 🔬 STEP 8 — 物理的状態遷移監視（17〜22）

| # | ファイル | 内容 |
|---|---------|------|
| 17 | [JP](./17_water_ice_phase_transition_JP.html) / [EN](./17_water_ice_phase_transition_EN.html) | **水→氷 相転移。** 取り出した熱量 Q を入力に、0°C で潜熱（334 kJ/kg）の間だけ温度が止まる様子を再現。R = 1.0 は凝固の始まり（0°C）に一致し、その後は「境界到達・相転移進行中」。動的τモデルの R ≥ 1 は、モデル上の警戒境界であり物理的な相転移ではない。 |
| 18 | [JP](./18_chain_tension_JP.html) / [EN](./18_chain_tension_EN.html) | **チェーン張力 ポリゴン効果＋自動調整。** スプロケット歯数同期の三層合成波でポリゴン効果を再現。dR/dt 予測制御で限界到達前に先行介入。 |
| 19 | [JP](./19_air_pressure_JP.html) / [EN](./19_air_pressure_EN.html) | **空気圧管理（圧縮性流体・動的τ・二重ゆらぎ）。** 温度上昇は圧力上昇（δ側）として計上し、τ_hi は材料強度の温度低下を仮定して縮小（デモ用の仮定）。δとτが独立にゆらぐシリーズ最深構造。 |
| 20 | [JP](./20_water_pressure_JP.html) / [EN](./20_water_pressure_EN.html) | **水圧管理（非圧縮性流体・固定τ・ウォーターハンマー）。** ポンプ脈動を三層高調波で再現。弁急閉によるウォーターハンマー（指数減衰×正弦波）を実装。 |
| 21 | [JP](./21_cabg_monitor_JP.html) / [EN](./21_cabg_monitor_EN.html) | **CABG（冠動脈バイパス）モニター。** バイパス手術中のグラフト血流（MGF）・拍動指数（PI）・拡張期充満（DF）を監視し、温度と血流量で許容幅を補正。Fail-Closed 時は手術中断を推奨。 |
| 22 | [JP](./22_vascular_monitor_JP.html) / [EN](./22_vascular_monitor_EN.html) | **NRA-IDE 血管インターベンションモニター。** 6物理量（圧力・せん断・壁張力・血流・温度・接着性）を、基準値からのズレ／限界までの距離で上下別々に評価し、温度でτを縮める（二重ゆらぎ）。最大値で合成し、破断は固定。バルーン展開・血流停滞・冷却の操作ボタン付き。教育用で、基準値は臨床基準ではありません。 |

---

### 🧩 STEP 9 — 高度機能・特定ドメイン（23〜26）

| # | ファイル | 内容 |
|---|---------|------|
| 23 | [23_sample_demo_JP.html](./23_sample_demo_JP.html) / [EN](./23_sample_demo_EN.html) | **状態境界・短期ログ・長期再構成。** 短期ゆらぎ追跡と長期構造傾向の再構成をNRA-IDEがどう分離するかを実証。 |
| 24 | [24_vehicle_mandatory_boundary_JP.html](./24_vehicle_mandatory_boundary_JP.html) / [EN](./24_vehicle_mandatory_boundary_EN.html) | **自動運転 必須限界構成デモ。** 衝突余裕時間・制動距離・横方向余裕を物理量監視。R ≥ 1.0 で上書き不可の強制 Fail-Closed。 |
| 25 | [25_dam_degradation_JP.html](./25_dam_degradation_JP.html) / [EN](./25_dam_degradation_EN.html) | **ダム管理比較 + τ劣化曲線。** 固定閾値監視 vs NRA-IDE τ劣化追跡を比較。構造余裕の侵食によるτ縮小を時系列で可視化。 |
| 26 | [JP](./26_escapement_contactpoint_JP.html) | **Phase-Gap エンジン — 接触点のみ熱排出。** 誤差・熱は連続計算全体ではなく位相境界の接触点のみで発生することを実証。 |

---

### 🛠️ STEP 10 — 設備監視の基礎（27〜32）

R = δ/τ を産業設備・施設監視の一般的ドメインに適用したデモ群です。

6本を通じてNRA-IDEの**単位非依存性**——同一の式構造で根本的に異なる物理量を管理できること——を実証します。

| # | ファイル | ドメイン | ポイント |
|---|---------|---------|---------|
| 27 | [JP](./27_belt_tension_JP.html) / [EN](./27_belt_tension_EN.html) | ベルトコンベアー・Vベルト張力 | τを「最適値から限界までの全余裕」と定義 → Rが自然に [0,1] に正規化。Fail-Closed でベルト停止。 |
| 28 | [JP](./28_water_temp_JP.html) / [EN](./28_water_temp_EN.html) | 水温 上下限管理 | R_hi と R_lo を独立評価。熱対流ゆらぎ（3周波数合成）。Fail-Closed で逆方向動作を自動停止。 |
| 29 | [JP](./29_light_lux_JP.html) / [EN](./29_light_lux_EN.html) | 光量（照度）管理 | 受光側（ルクス）で計測。R_hi > 0.75 から比例的に遮光率増加 — 予兆段階からの段階的介入。 |
| 30 | [JP](./30_power_JP.html) / [EN](./30_power_EN.html) | 電力管理（V×I 統合） | 電流・電圧を P = V×I として一本化。熱蓄積：過電力継続時間が R を時間的に押し上げる。 |
| 31 | [JP](./31_move_water_or_ice_JP.html) / [EN](./31_move_water_or_ice_EN.html) | 水・氷 状態ナビゲーション | インタラクティブな相転移制御。熱量 Q を取り出す（凝固系）／加える（融解系）操作で、潜熱の区間を含めて相境界での R を追跡。 |
| 32 | [JP](./32_nra_ide_water_ice_JP.html) / [EN](./32_nra_ide_ice_water_EN.html) | 氷→水 相転移 | Demo 17 の逆方向：加えた熱量 Q で氷が 0°C に達し、潜熱を吸収しながら融解する間の R を追跡（R = 1.0 は融解の始まり）。 |

---

### 🔭 スタンドアロン デモ

| ファイル | 内容 |
|---------|------|
| [JP](./33_nra_ide_6d_layer_viz_JP.html) / [EN](./33_nra_ide_6d_layer_viz_EN.html) | **6次元多重レイヤービジュアライザー。** 6つの R 値サーフェスを同時表示。透過度・彩度・白黒モードで観察可能。各レイヤー＝1物理ドメインのゆらぎ×閾値面。全次元同時に Fail-Closed への構造的接近を時間軸で追跡。 |
| [JP](../docs/ja-JP/figures/causal_diode_fail_closed_JP.html) / [EN](../docs/en-US/figures/causal_diode_fail_closed_EN.html) | **因果ダイオード & Fail-Closed 可視化。** AIが結果から原因側（閾値）を操作しようとする「逆流（Π⁻¹）」を構造的にブロックするアニメーションと、限界到達時の自律的遮断を体感できる直感的なデモ。 |

---

### 🔗 STEP 11 — 相関・多因子テンプレート（34〜41）

34番以降は、単一物理量の R 判定から、複数レイヤーの相関、媒介変数、閉ループ、個体差へ進む発展sample群です。  

> **JP 版と EN 版は別の実装です（#35〜#41、#49）。** 要素の構成・警告閾値・相関の正規化幅・状態名が異なります（例：#35 は JP が WARNING 0.70、EN が WATCH 0.40 / WARN 0.75）。日英を同じ入力で比べた結果は一致しません。違いは各ページのコード冒頭のコメントに記載しています。  

危険なレイヤーを平均で薄めず、基本形として **R_total = max(R_i, R_corr, R_coupling)** を採用します。医療系sampleは実運用ではなく、**医療教育用テンプレート** として軽く安全な名称にしています。

| # | ファイル | ドメイン | ポイント |
|---|---------|---------|---------|
| 34 | [JP](./34_NRA-IDE_AgroDrone_4Factor_Simulation_JP.html) / [EN](./34_NRA-IDE_AgroDrone_4Factor_Simulation_EN.html) | 育苗ハウス・農業ドローン 4要素相関 | 温度・湿度・光量・水分を R = δ/τ で追跡し、相関行列 C[i][j](t)、残渣ゲート G(r)、τステップ前の実測記録 x_{t-τ} を組み合わせる相関sampleの入口。 |
| 35 | [JP](./35_rotor_bearing_correlation_JP.html) / [EN](./35_rotor_bearing_correlation_EN.html) | 回転機械・軸受相関 | 振動、軸受温度、電流、潤滑圧、音響、回転数偏差を監視。振動が先行し、温度・電流・音響へ遅延波及する構造を可視化。 |
| 36 | [JP](./36_battery_thermal_runaway_correlation_JP.html) / [EN](./36_battery_thermal_runaway_correlation_EN.html) | バッテリー熱暴走相関 | 内部抵抗と温度上昇率 dT/dt を先行指標として扱い、温度、膨張圧、電圧偏差へ波及する構造を表示。実機制御ではなく教育・構造可視化用。 |
| 37 | [JP](./37_greenhouse_vpd_correlation_JP.html) / [EN](./37_greenhouse_vpd_correlation_EN.html) | 温室VPD媒介相関 | 温度と湿度を単純加算せず、VPD（飽差）を媒介レイヤーとして、土壌水分、CO₂、光量、ECへ相関圧が伝わる構造を可視化。 |
| 38 | [JP](./38_datacenter_cascade_correlation_JP.html) / [EN](./38_datacenter_cascade_correlation_EN.html) | データセンター・カスケード相関 | CPU負荷、電力、ラック温度、吸気温度、ファン回転率、空気流量、ネットワーク遅延をつなぎ、power → heat → fan → power の正のフィードバック環を表示。 |
| 39 | [JP](./39_coldchain_temperature_correlation_JP.html) / [EN](./39_coldchain_temperature_correlation_EN.html) | コールドチェーン温度逸脱相関 | 外気温、荷室温度、扉開閉率、圧縮機負荷、バッテリー残量、湿度、輸送遅延をつなぎ、外気＋扉 → 圧縮機余裕 → 荷室温度の媒介連鎖を可視化。 |
| 40 | [JP](./40_medical_education_individual_stratification_template_JP.html) / [EN](./40_medical_education_individual_stratification_template_EN.html) | 医療教育用・個体別振り分け | SpO₂、呼吸数、心拍数、収縮期血圧、体温を合成データとして扱い、年齢・脆弱性・既往による profile 圧で個体ごとの余裕差を可視化。診断・治療判断ではなく Human Review へ戻す教育テンプレート。 |
| 41 | [JP](./41_medical_education_infection_observation_template_JP.html) / [EN](./41_medical_education_infection_observation_template_EN.html) | 医療教育用・感染症観察群 | 発熱、呼吸、循環、水分、炎症様マーカーを合成データとして扱い、個体差つきで Observe / Watch / Caution / Human Review に振り分ける。診断名や治療推奨には寄せない教育用sample。 |

---

### 🚀 STEP 12 — 拡張POC・追加コンセプト（42〜53）

42番以降は、自動運転やロボット制御、FPGA実装のPOC、および基盤哲学のデモ群です。

| # | ファイル | ドメイン・内容 |
|---|---------|---------|
| 42 | [JP](./42_AutoDrive_POC_2_JP.html) / [EN](./42_AutoDrive_POC_2_EN.html) | 自動運転 Gate POC 2（初期段階の限界設定と動作デモ） |
| 43 | [JP](./43_AutoDrive_POC_3_JP.html) / [EN](./43_AutoDrive_POC_3_EN.html) | 自動運転 Gate POC 3（発展版の境界テスト） |
| 44 | [JP](./44_RobotArm_POC_1_JP.html) / [EN](./44_RobotArm_POC_1_EN.html) | 産業用ロボットアーム制御 POC 1 |
| 45 | [JP](./45_HybridCalc_vs_Traditional_JP.html) / [EN](./45_HybridCalc_vs_Traditional_EN.html) | ハイブリッド計算 vs 従来手法の比較 |
| 46 | [JP](./46_Connection_vs_Mixing_JP.html) / [EN](./46_Connection_vs_Mixing_EN.html) | Connection vs Mixing（接続と混合のリスク評価） |
| 47 | [JP](./47_FPGA_Demo_SPEED_JP.html) / [EN](./47_FPGA_Demo_SPEED_EN.html) | FPGA ハードウェア実装スピードデモ |
| 48 | [JP](./48_Human_5Factors_Correlation_JP.html) / [EN](./48_Human_5Factors_Correlation_EN.html) | 人体5要素相関 実数値推移デモ（医療系テンプレートの初期軽量版） |
| 49 | [JP](./49_Architecture_Infographic_JP.html) / [EN](./49_Architecture_Infographic_EN.html) | NRA-IDE アーキテクチャ・インフォグラフィック |
| 50 | [JP](./50_Constraint_Philosophy_JP.html) / [EN](./50_Constraint_Philosophy_EN.html) | 哲学コンセプト「制約は制限ではない。制約こそが知性を駆動する力である。」 |
| 52 | [JP](./52_Hybrid_DoubleFluctuation_EntropyTracking_JP.html) | ハイブリッド二重ゆらぎ エントロピー追跡 |
| 53 | [JP](./53_Formula_Lab_JP.html) | Formula Lab — 基礎式（R = δ/τ）と二次式（二重ゆらぎ、R_upper / R_lower）を境界の動きとして可視化するインタラクティブなプロトタイプ。説明文と連動。（日本語のみ） |

---

## 組み込み方法

リポジトリルートで実行する未検証のソフトウェア例です。二状態だけの独立判定器ではなく、現行アダプターを使います。

```python
import json
from pathlib import Path
from gate.jp import ThresholdGuardian

demo = json.loads(Path('config/ide_presets.json').read_text(encoding='utf-8'))['presets']['SOFTWARE_DEMO']
gate = ThresholdGuardian(config=demo)
notice = gate.evaluate(0.995, 1.0, timestamp='DEMO_T0').as_dict()
assert notice['status'] == 'IRREVERSIBLE_TRANSITION'
assert notice['fail_closed'] is True
```

既定設定は意図的に宣言未設定とし、`CONFESSION`を返します。実評価には、事前宣言した対象、単位、情報源、delta/tau構成規則、適用領域、閾値根拠と、呼出しごとの観測時点が必要です。同一インスタンスを保持し、再起動をまたぐ履歴を保存してください。新しいインスタンスの作成は回復の証明になりません。[現行gate文書](../gate/jp/README_JP.md)を参照してください。この例によって物理制御やドメインの安全性が確立されるわけではありません。

---

## 適用領域

### 🚗 自動運転

- **課題**: ブラックボックス判断による安全性問題

- **NRA解決策**: 衝突回避の構造的制約検証

- **閾値**: R = （停止距離が安全余裕帯へ入り込んだ量） / （安全余裕距離）。R = 1.0 は停止距離＝車間距離

### 🖥️ インフラ耐障害性

- **課題**: 分散システムのカスケード障害

- **NRA解決策**: 負荷限界監視による障害伝播防止

- **閾値**: R = （基準負荷からの増加分） / （基準負荷から許容上限までの余裕）。R = 1.0 は負荷＝許容上限

| 領域 | δ（制約からのズレ） | τ（許容範囲） | R ≥ 1.0 の意味 |
|------|---------------------|---------------|-----------------|
| 自動運転 | 停止距離が安全余裕帯（車間距離の手前 τ）へ入り込んだ量 | 安全余裕距離（設計時固定） | 停止距離 ≥ 車間距離：衝突危険 → 緊急停止 |
| インフラ | max(0, 負荷 − 基準負荷) | 許容上限 − 基準負荷 | 負荷＝許容上限：サーバー過負荷 → 遮断 |

---

## ライセンス

再配布時には以下の著作権表示の保持が必要です

**Copyright (c) 2026 M-Tokuni**

本プロジェクトは **MIT License** の下で提供されています。

研究・個人・商用を含め、無償で利用・改変・配布可能です。

最新版の情報については、公式リポジトリをご確認ください。

- **GitHub:** https://github.com/M-Tokun/NRA-IDE

---
