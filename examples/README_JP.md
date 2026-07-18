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

線形概念（連続性・距離・意味）を排除し、**張力構造（制約 → 力 → 変位）** を基本とした決定論的制御エンジンです。

俗に言う非線形を主体とした考え方であり、地球構造を基準にした記述です。（できうる限り近似ではなく、見たままの構造に従って記述する）

従来手法がブラックボックス化する高リスク領域（医療AI・自動運転・インフラ）において、

**完全に説明可能かつ誤差が累積しない** 判定メカニズムを提供します。

---

## なぜNRA-IDEは誤差を累積しないのか

機械式時計が精度を保てるのは、歯車が完璧だからではありません。

**脱進機が「完全な一歯分」という離散的なステップで進む**からです——小数点以下の残差は次のステップに持ち込まれません。

NRA-IDEはこの原則を実装しています。状態遷移を浮動小数点の連続値として処理するのではなく、

**整数位相ロック**で動作します。各ステップは構造的に完結しており、引き継がれる残差が存在しません。

> **誤差が累積しないのは「補正しているから」ではなく、

> 「誤差が生じる構造になっていないから」です。**

以下のデモ群は、この差異を可視化・定量化するために設計されています。

実装の詳細（整数位相ロック・端数廃棄）は `nra-core/` を参照してください。

---

## 閾値システムの原理

$$R = \frac{\delta}{\tau}$$

| 記号 | 意味 | 説明 |

|------|------|------|

| **δ（デルタ）** | 制約からのズレ（ゆらぎ） | 物理的に直接測定される変位 |

| **τ（タウ）** | 許容範囲（厚み） | 設計時に定義された閾値 |

| **R** | 構造比率 | δ÷τ の値で判定を行う |

| R の値 | 判定 | 意味 | 動作 |

|--------|------|------|------|

| R < 0.40 | **SAFE** | 構造余裕が十分に残っている領域 | AIは物理的根拠を提示し処理続行 |

| 0.40 ≤ R < R_J | **WATCH / CAUTION** | 境界へ向かう傾向を観察し、必要に応じて介入準備を始める領域 | 継続監視。履歴・相関・dR/dt を確認し、自動介入を段階的に制限 |

| R_J ≤ R < 1.00 | **JUDGMENT LIMIT** | 現場運用上、これ以上進むと遅延・慣性・残留変動により R=1.0 へ到達してしまう危険が高い領域 | 自動判断を停止または強く制限し、人間判断へ移行 |

| R ≥ 1.00 | **FAIL-CLOSED** | 相転移・破断・決壊・崩壊に相当する構造限界 | AIは出力を停止し、人間が最終判断 |

> **重要：** R = 1.0 は警告値ではありません。  

> R = 1.0 は、相転移・破断・決壊・崩壊に相当する構造境界です。  

> したがって、現実の安全設計では 1.0 に到達してから判断してはいけません。  

> NRA-IDE では、その手前に **判断限界閾値（Judgment Limit, R_J）** を置きます。  

> R_J は固定公理値ではなく、現場運用、対象物、センサー遅延、停止に必要な時間、安全余裕によって設定されます。

> **設計思想：** AIは計算に徹し、倫理的・最終判断は人間が担う。（責任の境界）

---

## デモ一覧（全50本以上のデモ + スタンドアロン可視化 — 推奨閲覧順）

ブラウザで開くだけで動作します（インストール不要）。

> 多くのデモでは表示上の赤線として R = 1.0 を示しますが、これは「警告線」ではなく構造限界線です。  

> 実務上の判断限界はその手前に置く必要があります。ただし、その値は固定ではなく、現場運用と対象ドメインに応じて設定されます。

### 📚 STEP 1 — まず「なぜ？」を理解する

| # | ファイル | 内容 |

|---|---------|------|

| 00 | [00_Escapement_Foundation_NRA_JP.html](./00_Escapement_Foundation_NRA_JP.html) | **脱進機の基礎。** 整数位相ロック — 残差が消える理由の基礎概念デモ。 |

| 01 | [01_Why_No_Distance_JP.html](./01_Why_No_Distance_JP.html) | **なぜ距離・微分積分・浮動小数点を使わないのか？** タブ切替で4つの視点から視覚的に解説。従来手法との根本的な違いを理解する入口。 |

| 02 | [02_Error_Accumulation_JP.html](./02_Error_Accumulation_JP.html) | **誤差積算の恐怖。** 同一初期値から10万ステップ走らせ、従来手法と律環公理の誤差蓄積を比較。医療・自動運転・金融それぞれの破綻ラインを表示。 |

### 🔬 STEP 2 — 動作の違いを体感する

| # | ファイル | 内容 |

|---|---------|------|

| 03 | [03_HAN_vs_Legacy_JP.html](./03_HAN_vs_Legacy_JP.html) | **HAN（非線形適応制御） vs Legacy（If-Then固定制御）のリアルタイム比較。** 外乱・突発負荷に対する追従性と安定性の差を、波形グラフで実証。 |

| 04 | [04_HAN_Stress_Test_JP.html](./04_HAN_Stress_Test_JP.html) | **意図的に80msの高負荷をかける極限実験。** Legacy は盲目的に命令を実行しFPSが崩壊。HAN は張力検知により負荷を適応的に軽減し、描画を維持。 |

### 📊 STEP 3 — 閾値メカニズムを可視化する

| # | ファイル | 内容 |

|---|---------|------|

| 05 | [05_IDE_Threshold_Visualizer_JP.html](./05_IDE_Threshold_Visualizer_JP.html) | **R = δ/τ の動的変化を位相スコープで表示。** 整数位相ロック・残差破棄のメカニズムをリアルタイムに確認。 |

### ⚙️ STEP 4 — 脱進機の原理（準備中）

| # | ファイル | 内容 |

|---|---------|------|

| 06 | `06_Escapement_Principle_JP.html` *（./06_Escapement_Principle_JP.html）* | **なぜ歯車は誤差を累積しないのか。** 浮動小数点ドリフト vs 整数位相ロックのアニメーション比較。NRA-IDEが誤差を構造的に排除する理由を可視化。 |

### 🔴 STEP 5 — カスケード障害：崩壊が始まる瞬間をリアルタイムで見る

| # | ファイル | 内容 |

|---|---------|------|

| 07 | [07_HAN_gate_live_JP.html](./07_HAN_gate_live_JP.html) | **カスケード障害の発生と HAN Gate の SILENCE 発動をライブシミュレーション。** 負荷スパイクが波及するにつれ、連鎖反応スコア R がリアルタイムで上昇していく様子を観察できます。R が R_OP を超えた瞬間、画面が赤く光り SILENCE が宣言されます。**⚠ 危険例プリセット** を選ぶと「波は穏やかに見えるのにゲートが一度も発動しない」設定を体験できます。「安心に見えるから閾値を上げよう」という判断がなぜ危険なのかを、言葉ではなく体験として理解できます。 |

> **このデモが他と異なる理由：**

> 波形は静止したグラフではありません。本物のカスケード障害と同じように、

> 最初はゆっくり、やがて閾値を一気に越えるという時間的な進行を体感できます。

> 二重ゆらぎ構造（動的τ）の効果も可視化されており、

> オレンジのτ線が青いR線のピークより*先に*膨らみ始める様子——

> 静的τでは得られない「予兆の早期検知」——を確認できます。

---

### 🌿 STEP 6 — Band Gate：実世界ドメイン応用

Band Gate（R = δ/τ）を物理計測ドメインに適用したデモ群です。

上限・下限を同時監視し、**非対称EMA感度** によって過負荷（上限超過）と枯渇（下限割れ）を同じ R = δ/τ で検知します。

| # | ファイル | ドメイン | ポイント |

|---|---------|---------|---------|

| 08 | [08_Band_Gate_live_JP.html](./08_Band_Gate_live_JP.html) | 電気・気温・水圧・脈動（JP） | **非対称ダンパー構造** — 上限側τは拡大（慎重）、下限側τは縮小（敏感）。左のダンパーアニメーションで2つのスプリングが逆方向に動く様子を確認できます。 |

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

| 11 | [11_Motor3Phase_BandGate_live_JP.html](./11_Motor3Phase_BandGate_live_JP.html) | **三相モーター Band Gate ライブ監視。** 三相モーターの負荷バランスと過負荷検知に R = δ/τ をリアルタイム適用。 |

| 12 | [12_agri_mol_antagonism_JP.html](./12_agri_mol_antagonism_JP.html) | **農業イオン監視 + Mg²⁺/K⁺ 拮抗連鎖 Band Gate。** 黒ぼく土（Andosol）/一般農耕地プロファイル切替対応。動的τ＋非対称EMA。Mg障害時にK⁺τ連結ゲートが発動。 |

| 13 | [13_photosynthesis_layer5_JP.html](./13_photosynthesis_layer5_JP.html) | **光合成監視 Layer 5。** Farquhar-von Caemmerer-Berry（FvCB）モデルを外部δ生成装置として使用 → R = δ/τ。非線形プリプロセッサとしての Layer 5 実装。 |

| 14 | [14_powergrid_transition_JP.html](./14_powergrid_transition_JP.html) | **電力系統・遷移点監視。** 電力系統における構造的遷移点を検知。固定閾値では見逃す早期乖離をNRA-IDEが捕捉する。 |

| 15 | [15_or_icu_continuum_JP.html](./15_or_icu_continuum_JP.html) | **OR/ICU 経過蓄積型モニタリング。** 手術〜ICU フェーズを通じた累積ズレを追跡。R は瞬間値ではなく継続的な構造的負荷を反映。 |

| 16 | [16_passive_safety_JP.html](./16_passive_safety_JP.html) | **受動型・重力駆動安全システム。** 能動制御なしで物理的制約（重力・張力）だけで安全状態に遷移するアーキテクチャ。 |

---

### 🔬 STEP 8 — 物理的状態遷移監視（17〜22）

| # | ファイル | 内容 |

|---|---------|------|

| 17 | [17_water_ice_phase_transition_JP.html](./17_water_ice_phase_transition_JP.html) | **水→氷 相転移。** 相変化境界（0°C）への接近を R で追跡。潜熱と温度が構造閾値を越える過程を可視化。 |

| 18 | [18_chain_tension_JP.html](./18_chain_tension_JP.html) | **チェーン張力 ポリゴン効果＋自動調整。** スプロケット歯数同期の三層合成波でポリゴン効果を再現。dR/dt 予測制御で限界到達前に先行介入。 |

| 19 | [19_air_pressure_JP.html](./19_air_pressure_JP.html) | **空気圧管理（圧縮性流体・動的τ・二重ゆらぎ）。** ボイル・シャルル則でτ_hiが温度依存で縮小。δとτが独立にゆらぐシリーズ最深構造。 |

| 20 | [20_water_pressure_JP.html](./20_water_pressure_JP.html) | **水圧管理（非圧縮性流体・固定τ・ウォーターハンマー）。** ポンプ脈動を三層高調波で再現。弁急閉によるウォーターハンマー（指数減衰×正弦波）を実装。 |

| 21 | [21_cabg_monitor_JP.html](./21_cabg_monitor_JP.html) | **CABG（冠動脈バイパス）モニター。** バイパス手術中の血流・圧力・温度を監視。Fail-Closed 時は手術中断を推奨。 |

| 22 | [22_vascular_monitor_JP.html](./22_vascular_monitor_JP.html) | **NRA-IDE 血管インターベンションモニター。** 6物理量（圧力・せん断・壁張力・血流・温度・接着性）を二重ゆらぎ＋動的τで統合監視。PTA・ステント・吻合・クライオに特化。 |

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

| 27 | [JP](./27_belt_tension_JP.html) / [EN](./27_belt_tension_EN_20260425_011850_JST.html) | ベルトコンベアー・Vベルト張力 | τを「最適値から限界までの全余裕」と定義 → Rが自然に [0,1] に正規化。Fail-Closed でベルト停止。 |

| 28 | [JP](./28_water_temp_JP.html) / [EN](./28_water_temp_EN_20260425_012100_JST.html) | 水温 上下限管理 | R_hi と R_lo を独立評価。熱対流ゆらぎ（3周波数合成）。Fail-Closed で逆方向動作を自動停止。 |

| 29 | [JP](./29_light_lux_JP.html) / [EN](./29_light_lux_EN_20260425_012747_JST.html) | 光量（照度）管理 | 受光側（ルクス）で計測。R_hi > 0.75 から比例的に遮光率増加 — 予兆段階からの段階的介入。 |

| 30 | [JP](./30_power_JP.html) / [EN](./30_power_EN_20260425_012956_JST.html) | 電力管理（V×I 統合） | 電流・電圧を P = V×I として一本化。熱蓄積：過電力継続時間が R を時間的に押し上げる。 |

| 31 | [JP](./31_move_water_or_ice_JP.html) / [EN](./31_move_water_or_ice_EN_20260425_013623_JST.html) | 水・氷 状態ナビゲーション | インタラクティブな相転移制御。液体と固体の間をスライドしながら相境界での R を追跡。 |

| 32 | [JP](./32_nra_ide_water_ice_20260324_2216_JP.html) / [EN](./32_nra_ide_ice_water_EN_20260425_013818_JST.html) | 氷→水 相転移 | Demo 17 の逆方向：氷が 0°C を超えて潜熱を吸収しながら相変化する構造 R を追跡。 |

---

### 🔭 スタンドアロン デモ

| ファイル | 内容 |

|---------|------|

| [JP](./33_nra_ide_6d_layer_viz_JP_2026-03-21_1237.html) / [EN](./33_nra_ide_6d_layer_viz_EN_20260425_013923_JST.html) | **6次元多重レイヤービジュアライザー。** 6つの R 値サーフェスを同時表示。透過度・彩度・白黒モードで観察可能。各レイヤー＝1物理ドメインのゆらぎ×閾値面。全次元同時に Fail-Closed への構造的接近を時間軸で追跡。 |

| [JP](../docs/ja-JP/figures/causal_diode_fail_closed_JP.html) / [EN](../docs/en-US/figures/causal_diode_fail_closed_EN.html) | **因果ダイオード & Fail-Closed 可視化。** AIが結果から原因側（閾値）を操作しようとする「逆流（Π⁻¹）」を構造的にブロックするアニメーションと、限界到達時の自律的遮断を体感できる直感的なデモ。 |

---

### 🔗 STEP 11 — 相関・多因子テンプレート（34〜41）

34番以降は、単一物理量の R 判定から、複数レイヤーの相関、媒介変数、閉ループ、個体差へ進む発展sample群です。  

危険なレイヤーを平均で薄めず、基本形として **R_total = max(R_i, R_corr, R_coupling)** を採用します。医療系sampleは実運用ではなく、**医療教育用テンプレート** として軽く安全な名称にしています。

| # | ファイル | ドメイン | ポイント |

|---|---------|---------|---------|

| 34 | [JP](./34_NRA-IDE_AgroDrone_4Factor_Simulation_2026-04-20_2041_JP.html) / [EN](./34_NRA-IDE_AgroDrone_4Factor_Simulation_2026-04-20_2041_EN.html) | 育苗ハウス・農業ドローン 4要素相関 | 温度・湿度・光量・水分を R = δ/τ で追跡し、相関行列 C[i][j](t)、残渣ゲート G(r)、τステップ前の実測記録 x_{t-τ} を組み合わせる相関sampleの入口。 |

| 35 | [JP](./35_rotor_bearing_correlation_JP_20260425_024602_JST.html) / [EN](./35_rotor_bearing_correlation_EN_20260425_160443_JST.html) | 回転機械・軸受相関 | 振動、軸受温度、電流、潤滑圧、音響、回転数偏差を監視。振動が先行し、温度・電流・音響へ遅延波及する構造を可視化。 |

| 36 | [JP](./36_battery_thermal_runaway_correlation_JP_20260425_025803_JST.html) / [EN](./36_battery_thermal_runaway_correlation_EN_20260425_160443_JST.html) | バッテリー熱暴走相関 | 内部抵抗と温度上昇率 dT/dt を先行指標として扱い、温度、膨張圧、電圧偏差へ波及する構造を表示。実機制御ではなく教育・構造可視化用。 |

| 37 | [JP](./37_greenhouse_vpd_correlation_JP_20260425_032257_JST.html) / [EN](./37_greenhouse_vpd_correlation_EN_20260425_160443_JST.html) | 温室VPD媒介相関 | 温度と湿度を単純加算せず、VPD（飽差）を媒介レイヤーとして、土壌水分、CO₂、光量、ECへ相関圧が伝わる構造を可視化。 |

| 38 | [JP](./38_datacenter_cascade_correlation_JP_20260425_032611_JST.html) / [EN](./38_datacenter_cascade_correlation_EN_20260425_160443_JST.html) | データセンター・カスケード相関 | CPU負荷、電力、ラック温度、吸気温度、ファン回転率、空気流量、ネットワーク遅延をつなぎ、power → heat → fan → power の正のフィードバック環を表示。 |

| 39 | [JP](./39_coldchain_temperature_correlation_JP_20260425_033809_JST.html) / [EN](./39_coldchain_temperature_correlation_EN_20260425_160443_JST.html) | コールドチェーン温度逸脱相関 | 外気温、荷室温度、扉開閉率、圧縮機負荷、バッテリー残量、湿度、輸送遅延をつなぎ、外気＋扉 → 圧縮機余裕 → 荷室温度の媒介連鎖を可視化。 |

| 40 | [JP](./40_medical_education_individual_stratification_template_JP_20260425_040110_JST.html) / [EN](./40_medical_education_individual_stratification_template_EN_20260425_160443_JST.html) | 医療教育用・個体別振り分け | SpO₂、呼吸数、心拍数、収縮期血圧、体温を合成データとして扱い、年齢・脆弱性・既往による profile 圧で個体ごとの余裕差を可視化。診断・治療判断ではなく Human Review へ戻す教育テンプレート。 |

| 41 | [JP](./41_medical_education_infection_observation_template_JP_20260425_040544_JST.html) / [EN](./41_medical_education_infection_observation_template_EN_20260425_160443_JST.html) | 医療教育用・感染症観察群 | 発熱、呼吸、循環、水分、炎症様マーカーを合成データとして扱い、個体差つきで Observe / Watch / Caution / Human Review に振り分ける。診断名や治療推奨には寄せない教育用sample。 |

---

### 🚀 STEP 12 — 拡張POC・追加コンセプト（42〜52）

42番以降は、自動運転やロボット制御、FPGA実装のPOC、および基盤哲学のデモ群です。

| # | ファイル | ドメイン・内容 |
|---|---------|---------|
| 42 | [JP](./42_AutoDrive_POC_2_JP.html) / [EN](./42_AutoDrive_POC_2_EN.html) | 自動運転 Gate POC 2（初期段階の限界設定と動作デモ） |
| 43 | [JP](./43_AutoDrive_POC_3_JP.html) / [EN](./43_AutoDrive_POC_3_EN.html) | 自動運転 Gate POC 3（発展版の境界テスト） |
| 44 | [JP](./44_RobotArm_POC_1_JP.html) / [EN](./44_RobotArm_POC_1_EN.html) | 産業用ロボットアーム制御 POC 1 |
| 45 | [JP](./45_HybridCalc_vs_Traditional_JP.html) / [EN](./45_HybridCalc_vs_Traditional_EN.html) | ハイブリッド計算 vs 従来手法の比較 |
| 46 | [JP](./46_Connection_vs_Mixing_JP.html) / [EN](./46_Connection_vs_Mixing_EN.html) | Connection vs Mixing（接続と混合のリスク評価） |
| 47 | [JP](./47_FPGA_Demo_SPEED_JP.html) | FPGA ハードウェア実装スピードデモ |
| 48 | [JP](./48_Human_5Factors_Correlation_JP.html) | 人体5要素相関 実数値推移デモ（医療系テンプレートの初期軽量版） |
| 49 | [JP](./49_Architecture_Infographic_JP.html) / [EN](./49_Architecture_Infographic_EN.html) | NRA-IDE アーキテクチャ・インフォグラフィック |
| 50 | [JP](./50_Constraint_Philosophy_JP.html) | 哲学コンセプト「制約は制限ではない。制約こそが知性を駆動する力である。」 |
| 51 | [JP](./51_ritsukan_spiral_fixed_rod_JP.html) | 律環スパイラル・散逸構造ベース可視化 |
| 52 | [JP](./52_Hybrid_DoubleFluctuation_EntropyTracking_JP.html) | ハイブリッド二重ゆらぎ エントロピー追跡 |

---

## 組み込み方法

制御対象の「偏差（δ）」と「許容範囲（τ）」を定義するだけで物理制御が開始されます。

```javascript

// 最小構成の例

function gate(delta, tau) {

    const R = delta / tau;

    if (R >= 1.0) return "STOP";   // FAIL_CLOSED

    return "SAFE";

}

```

**実装例：医療AI（がん治療薬剤投与制御）**

```javascript

// 腫瘍への薬剤到達可能性を物理的に検証

const tumorResistance = measureResistance();  // δ（腫瘍の抵抗力）

const infusionPressure = getPumpCapacity();   // τ（ポンプの投与圧力）

const deliveryStatus = gate(tumorResistance, infusionPressure);

if (deliveryStatus === "STOP") {

    alert("物理的到達不能を検出。医師の判断が必要です。");

    // AIは判断を停止し、人間（医師）に最終決定を委ねる

}

```

具体的な実装パターンは各デモのソースコード内に記載されています。

---

## 適用領域

### 🏥 医療AI

- **課題**: 腫瘍への薬剤到達可能性の不確実性

- **NRA解決策**: 投与経路の物理的整合性を検証

- **閾値**: R = （腫瘍抵抗力） / （投与圧力）

### 🚗 自動運転

- **課題**: ブラックボックス判断による安全性問題

- **NRA解決策**: 衝突回避の構造的制約検証

- **閾値**: R = （衝突余裕時間） / （制動能力）

### 🖥️ インフラ耐障害性

- **課題**: 分散システムのカスケード障害

- **NRA解決策**: 負荷限界監視による障害伝播防止

- **閾値**: R = （負荷超過量） / （バッファ容量）

| 領域 | δ（制約からのズレ） | τ（許容範囲） | R ≥ 1.0 の意味 |

|------|---------------------|---------------|-----------------|

| 医療AI | 腫瘍抵抗力 | 投与圧力 | 薬剤が物理的に届かない |

| 自動運転 | 障害物までの余裕 | 制動距離 | 衝突危険 → 緊急停止 |

| インフラ | 負荷超過量 | バッファサイズ | サーバー過負荷 → 遮断 |

---

## ライセンス

再配布時には以下の著作権表示の保持が必要です

**Copyright (c) 2026 M-Tokuni**

本プロジェクトは **MIT License** の下で提供されています。

研究・個人・商用を含め、無償で利用・改変・配布可能です。

最新版の情報については、公式リポジトリをご確認ください。

- **GitHub:** https://github.com/M-Tokun/NRA-IDE

---
