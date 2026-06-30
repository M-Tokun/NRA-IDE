# ground data collection protocol
<!-- FILE: ground/ground_Report/pending/data_collection_protocol.md 26-0630 -->

ステータス：**pending**

注：本文書は、熱波・水不足・ヒートアイランド・インフラ障害などの実態事例から、`ground/` の横軸変数、観測台帳、採用判定、警告表記を育てるためのデータ集積方針である。後から削ることを前提に、初期段階では簡易化せず、判断理由を最大限残す。

---

## 0. 位置付け

`ground/` は NRA 公理を追加しない。真理や存在を決定しない。観測・定義・出所・単位・物理制約・欠損状態に基づき、入力を実行へ渡してよいかを判定する IDE 側の接地・境界制御レイヤーである。

本プロトコルは、その前段として、事例から得られたデータをどのように集め、どの変数に接続し、どの状態なら計算に使えるかを管理する。

---

## 1. 基本方針

### 1.1 事例から追う

式を先に決めない。事例から観測事象を拾い、その事象が要求する物理量・社会量・制約量を特定する。式・指標・分類は、観測された接続が十分に見えた後に整理する。

```text
観測された事象
  ↓
その事象が示す量を特定
  ↓
既存変数または新規候補へ接続
  ↓
単位・時点・地域・出所・信頼度を確認
  ↓
採用・保留・除外を判定
  ↓
必要な場合のみ計算へ渡す
```

### 1.2 固定する部分と固定しない部分

固定する部分：

- 欠損値を補完しない。
- 単位不明値を計算へ使わない。
- 出所不明値を計算へ使わない。
- 計算に使えるのは `adoption_status = adopted` のみ。
- `verified` は確認済みであって、採用済みではない。
- 最終警告に確率 `%` を表示しない。
- 警告表記は、根拠・欠損・不確実性とセットにする。
- `ground` は NRA 公理を追加しない。

固定しない部分：

- ドメイン別の最終式。
- Pattern C の詳細な返却形式。
- 接続方式 API / library / other。
- 変数の最終採否。
- 分布データの最終表現形式。
- ドメイン別閾値。
- 警告段階の最終ラベル。

理由：熱波や広域災害では、ドメインごとに支配変数が変わる。早期に様式を固定すると、観測から出すのではなく、既存様式へ事象を押し込む危険がある。一方で、単位・出所・採用判定・欠損処理は、後から揺らすと計算全体が崩れる。

---

## 2. ファイル構成

初期段階では、次の3ファイルを想定する。

```text
ground/ground_Report/pending/data_collection_protocol.md
ground/ground_Report/pending/variable_registry.csv
ground/ground_Report/pending/observation_ledger.csv
```

### 2.1 `data_collection_protocol.md`

人間向けの運用説明。なぜその列が必要か、なぜ採用・不採用を分けるか、なぜ確率 `%` を出さないかを記録する。

### 2.2 `variable_registry.csv`

変数そのものの登録表。変数名、ドメイン、物理量、単位、欠損時の扱い、接続先を管理する。

### 2.3 `observation_ledger.csv`

実データの観測台帳。値、単位、時点、地域、出所、信頼度、採用状態、採用・除外理由を管理する。

---

## 3. データ状態

### 3.1 reliability level

`reliability_level` は、値そのものの信頼度と出所の性質を表す。

| 値 | 意味 | 計算使用 |
|---|---|---|
| `primary_observed` | 一次観測値。気象機関、観測局、電力事業者、水管理機関などの直接値。 | 採用判定後のみ可 |
| `official_estimate` | 公的機関による推定値。死亡超過、被害推定など。 | 採用判定後のみ可 |
| `derived_calculation` | 一次値または採用値から計算した値。 | 入力値が adopted の場合のみ可 |
| `secondary_report` | 報道、解説記事、二次資料。 | 原則不可。候補探索のみ |
| `model_estimate` | モデル出力。定義・入力・検証条件が必要。 | 原則 pending |
| `unclear` | 出所・単位・定義・時点のいずれかが不明。 | 不可 |

理由：報道値は探索の入口として有用だが、計算にそのまま入れると、定義差・時点差・引用誤差が混入する。一次観測でも、今回の計算目的に合わなければ採用しない。

### 3.2 adoption status

`adoption_status` は、今回の `ground` 計算または判断に使えるかを表す。

| 値 | 意味 | 計算使用 |
|---|---|---|
| `adopted` | 今回の目的・単位・時点・地域・定義に適合し、計算使用を承認した値。 | 可 |
| `verified` | 出所・単位・時点などは確認済みだが、今回の計算採用は未決。 | 不可 |
| `candidate` | 見つけた候補。追加確認が必要。 | 不可 |
| `pending` | 定義・単位・接続先・扱いが未確定。 | 不可 |
| `excluded` | 不採用。理由を必ず記録する。 | 不可 |

理由：`verified` と `adopted` を分けないと、確認済みの値が自動的に計算へ流入する。確認済みであることと、今回の計算目的に適合することは別である。

---

## 4. 参入条件

変数・値・事例・警告は、見合うだけの根拠がある場合のみ `ground` に参入できる。根拠が薄いものは、重要そうでも `candidate` または `pending` に留める。

### 4.1 参入可能

```text
観測または一次情報がある
単位が分かる
対象時点が分かる
対象地域が分かる
出所が分かる
どの変数に接続するか説明できる
欠損と不確実性を明示できる
既存方針と矛盾しない
```

### 4.2 参入不可

```text
印象
単発の噂
出所不明の数値
単位不明の比較
地域・期間が混ざった値
根拠なしの因果断定
未観測変数の補完
定義差を無視した比較
```

理由：`ground` は警告を強く出すための層ではなく、実行へ渡してよい入力を判定する層である。薄弱な値が混入すると、後続の計算・警告・FAIL-CLOSED 判定が見かけ上だけ精密になる。

---

## 5. 変数命名

### 5.1 命名方針

変数名は、できるだけ次の順で構成する。

```text
domain_quantity_modifier
```

例：

```text
meteo_air_temp_max
meteo_air_temp_min
meteo_air_temp_anomaly
meteo_humidity_rel
meteo_dew_point
meteo_wind_speed
meteo_wind_direction
meteo_rain_amount_daily
meteo_rain_amount_cumulative
meteo_rain_intensity_peak
meteo_dry_days_count

surface_temp_road
surface_temp_rail
surface_temp_roof
surface_temp_water

hydro_river_flow
hydro_river_temp
hydro_river_level
hydro_reservoir_level
hydro_soil_moisture

power_supply
power_demand
power_cooling_demand
power_import_capacity

water_available
water_demand_city
water_demand_agri
water_demand_cooling
water_ecological_min

transport_capacity_rail
transport_capacity_road
transport_disruption_count

health_excess_mortality
health_emergency_calls
health_cooling_access

fire_risk_index
fire_event_count
fire_area_burned
fire_evacuated_count

geo_background_constraint
repair_access_capacity
```

理由：`rain`、`temp`、`water` のような短い名前は、日量・累積・強度・平年差・需要・供給が混ざる。変数名だけで全定義を背負わせないが、最低限、何の量かが読める名前にする。

### 5.2 記号衝突の注意

`δ` は NRA-IDE 本体の構造変数と衝突しやすい。横軸研究で余裕量を扱う場合は、可能な限り `slack_*`、`margin_*`、`capacity_*` などを用いる。

例：

```text
power_margin = power_supply - power_demand
water_remaining_flow = river_flow - ecological_min_flow - total_withdrawal
transport_capacity_remaining
```

理由：`δ_power` のような表記は直感的だが、NRA 本体の `δ/τ/R` と混同される危険がある。`ground` は横軸接地レイヤーであり、NRA 公理を増やさない。

---

## 6. 単位

単位が分かる部分のみ統一する。単位が不明な値は計算に使わない。単位はあるが定義差が大きいものは `pending` とする。

### 6.1 固定しやすい単位

| variable_name | unit | note |
|---|---|---|
| `meteo_air_temp_max` | `C` | 日最高気温 |
| `meteo_air_temp_min` | `C` | 日最低気温 |
| `meteo_air_temp_mean` | `C` | 平均気温。主変数ではなく補助扱い |
| `meteo_air_temp_anomaly` | `C` | 平年差 |
| `meteo_humidity_rel` | `%` | 相対湿度 |
| `meteo_dew_point` | `C` | 露点温度 |
| `meteo_wind_speed` | `m/s` | 平均または最大の定義を要記録 |
| `meteo_wind_direction` | `degree` | 方位角 |
| `meteo_rain_amount_daily` | `mm/day` | 日界定義を要記録 |
| `meteo_rain_amount_cumulative` | `mm` | 対象期間を要記録 |
| `meteo_rain_intensity_peak` | `mm/hour` | 最大時間雨量など |
| `meteo_dry_days_count` | `days` | 無降水日の定義を要記録 |
| `surface_temp_road` | `C` | 路面温度 |
| `surface_temp_rail` | `C` | レール温度 |
| `surface_temp_water` | `C` | 水面または河川水温 |
| `hydro_river_flow` | `m3/s` | 河川流量 |
| `hydro_river_level` | `m` | 観測基準面を要記録 |
| `hydro_reservoir_level` | `m` or `%` | 定義差あり |
| `hydro_soil_moisture` | `m3/m3` or `%` | 定義差あり |
| `power_supply` | `MW` | 電力供給 |
| `power_demand` | `MW` | 電力需要 |
| `power_import_capacity` | `MW` | 連系線・輸入容量 |
| `water_available` | `m3/s` or `m3/day` | 対象により異なる |
| `water_demand_city` | `m3/day` | 都市用水需要 |
| `water_demand_agri` | `m3/day` | 農業用水需要 |
| `water_demand_cooling` | `m3/day` | 冷却水需要 |
| `water_ecological_min` | `m3/s` | 環境基準流量 |
| `transport_disruption_count` | `count/day` | 障害件数 |
| `health_excess_mortality` | `deaths/day` | 推定値の場合は方法を要記録 |
| `health_emergency_calls` | `calls/day` | 対象分類を要記録 |
| `fire_event_count` | `count/day` | 火災件数 |
| `fire_area_burned` | `ha` or `km2` | 換算可。ただし元単位を保持 |
| `fire_evacuated_count` | `persons` | 避難人数 |

### 6.2 `%` の注意

`%` は乱用しない。相対湿度、貯水率、土壌水分率、冷房普及率、稼働率、観測充足率は、すべて `%` でも意味が異なる。

理由：同じ `%` でも分母が異なる。分母が不明な `%` は物理制約や地域比較に接続できない。

---

## 7. 面積・分布

面積と分布は、熱波・水不足・火災・ヒートアイランド・曝露人口の理解に不可欠である。ただし、分布の表現形式はデータ源に依存するため、初期段階では形を固定しない。

### 7.1 固定しやすい面積・人口単位

| variable_name | unit | note |
|---|---|---|
| `area_affected` | `km2` | 影響範囲 |
| `area_alert` | `km2` | 警報範囲 |
| `area_heatwave` | `km2` | 熱波範囲 |
| `area_drought` | `km2` | 干ばつ範囲 |
| `area_fire_burned` | `ha` or `km2` | 焼失面積 |
| `area_urban_impervious` | `km2` | 不透水・舗装面積 |
| `area_vegetation_cover` | `km2` | 植生面積 |
| `area_water_surface` | `km2` | 水面面積 |
| `population_exposed` | `persons` | 閾値曝露人口 |
| `population_density` | `persons/km2` | 人口密度 |

### 7.2 分布データに必要な台帳

```text
spatial_scope
spatial_resolution
geometry_type
area_km2
distribution_source
aggregation_method
projection_or_grid
time_scope
```

`geometry_type` の例：

```text
station_points
admin_area
grid
polygon
line_network
river_basin
```

理由：平均値だけでは、局所的な破綻、人口集中、高温域と水不足域の重なりが見えない。一方で、分布データを無理に一つの代表値へ潰すと、横軸の意味が失われる。

---

## 8. 概要・傾向・推定

概要と傾向は重要である。個別観測だけでは、広域性、持続性、複数系統の重なり、どの余裕が先に削られているかが見えない。ただし、憶測は排除し、推定までに留める。

### 8.1 出力区分

| 区分 | 意味 | 許可 |
|---|---|---|
| `observation` | 実測値、公的発表、事故件数、警報範囲。 | 可 |
| `aggregation` | 面積、件数、期間、重なり、分布の集計。 | 入力条件明示で可 |
| `trend` | 増加、減少、集中、拡大、持続。 | 根拠付きで可 |
| `estimate` | 観測と物理制約から見て妥当な範囲の解釈。 | 条件付きで可 |
| `speculation` | 根拠不足の原因断定、未来予測、未観測補完。 | 禁止 |

### 8.2 推定に必要な添付情報

```text
観測値
比較対象
物理制約
欠損変数
不確実性
採用不可条件
```

理由：警告には概要と傾向が必要だが、未観測変数を埋めた断定は `ground` の欠損補完禁止に反する。

---

## 9. 警告表記

警告文脈では「可能性」という言い方を許容する。ただし、根拠が見合う場合に限る。最終表記に確率 `%` を出さない。

### 9.1 許容表記

```text
可能性あり
可能性が高い
注意
警戒
重大警戒
判定保留
観測不足
接続未確定
```

### 9.2 禁止表記

```text
37% の確率で発生
ほぼ確実
必ず起きる
原因はこれである
この値から被害が確定する
```

理由：内部計算でスコア、比率、重なり面積、観測充足率を使うことはあり得る。しかし最終表示に `%` を出すと、欠損・定義差・観測密度差があるにもかかわらず、根拠以上の精度を装う。

### 9.3 内部スコアの扱い

内部では、次のような計算を行う可能性がある。

```text
観測充足率
面積重なり率
閾値距離
データ信頼度スコア
接地品質スコア
```

ただし、最終出力では段階表記に変換する。段階名・閾値はドメイン別に確定するまで pending とする。

---

## 10. CSV テンプレート

### 10.1 `variable_registry.csv`

```csv
variable_name,domain,quantity,unit,definition_status,required_default,missing_pattern,description,connected_variables,note
meteo_air_temp_max,meteo,temperature,C,fixed,true,B,Daily maximum air temperature,meteo_air_temp_min;meteo_heat_duration,
meteo_rain_amount_daily,meteo,precipitation,mm/day,fixed,false,C,Daily precipitation amount,meteo_rain_amount_cumulative;meteo_dry_days_count,
hydro_soil_moisture,hydro,soil_water,%,pending,false,C,Soil moisture; definition differs by source,water_demand_agri;fire_risk_index,unit may vary
```

列の意味：

| 列 | 意味 |
|---|---|
| `variable_name` | 変数名 |
| `domain` | meteo / surface / hydro / power / water / transport / health / fire / geo / repair など |
| `quantity` | 温度、流量、面積、人数などの量 |
| `unit` | 単位。不明なら空欄ではなく `BOTTOM` または `pending` 扱いを検討 |
| `definition_status` | fixed / pending / excluded |
| `required_default` | 初期既定で必須か |
| `missing_pattern` | 欠損時に Pattern B / C のどちらに入るか |
| `description` | 短い説明 |
| `connected_variables` | 接続候補 |
| `note` | 注意点 |

### 10.2 `observation_ledger.csv`

```csv
data_id,variable_name,value,unit,time_scope,spatial_scope,source_name,source_url,source_type,definition,uncertainty,traceability,reliability_level,adoption_status,adoption_reason,exclusion_reason,note
obs_0001,meteo_air_temp_max,40.5,C,2026-06-XX,Poland,unknown,,secondary_report,reported maximum temperature,unknown,partial,secondary_report,candidate,,,
```

列の意味：

| 列 | 意味 |
|---|---|
| `data_id` | 観測値の一意ID |
| `variable_name` | 接続する変数名 |
| `value` | 値 |
| `unit` | 単位 |
| `time_scope` | 対象時点または期間 |
| `spatial_scope` | 対象地域 |
| `source_name` | 発行主体・資料名 |
| `source_url` | URL。URLだけを証跡にしない |
| `source_type` | primary / official / secondary / model など |
| `definition` | 値の定義 |
| `uncertainty` | 誤差、速報、推定幅、欠損など |
| `traceability` | full / partial / weak / none |
| `reliability_level` | 3.1 の値 |
| `adoption_status` | 3.2 の値 |
| `adoption_reason` | 採用理由 |
| `exclusion_reason` | 除外理由 |
| `note` | 補足 |

---

## 11. 欠損と FAIL-CLOSED

欠損は欠損のまま扱う。未知変数を不存在と断定しない。ただし、必須変数が欠損している場合は、実行権限を停止する。

```text
Pattern A:
  全必須変数が採用済みで使用可能
  → 実行可能

Pattern B:
  必須変数が欠損、未採用、単位不明、出所不明、定義不一致
  → FAIL-CLOSED

Pattern C:
  非必須変数が欠損
  → 欠損を明示して継続。補完しない
```

理由：欠損補完は、見かけ上の連続性を作るが、実行判断へ未確認値を混入させる。`ground` の目的は、未知を埋めることではなく、未知を含む実行を止めることである。

---

## 12. 熱波事例で優先して見る変数群

### 12.1 気象基礎

```text
meteo_air_temp_max
meteo_air_temp_min
meteo_air_temp_mean
meteo_air_temp_anomaly
meteo_humidity_rel
meteo_dew_point
meteo_wind_speed
meteo_wind_direction
meteo_rain_amount_daily
meteo_rain_amount_cumulative
meteo_rain_intensity_peak
meteo_dry_days_count
meteo_solar_radiation
```

理由：熱波では気温だけでなく、湿度、夜間回復、風、日射、降水推移が被害構造を分ける。

### 12.2 地表・構造物

```text
surface_temp_road
surface_temp_rail
surface_temp_roof
surface_temp_water
surface_albedo
surface_impervious_ratio
shade_ratio
ventilation_index
material_expansion_allowance
```

理由：ヒートアイランドや構造物事故では、外気温よりも表面温度・部材温度・直射・蓄熱が効く場合がある。

### 12.3 水・農業・火災

```text
hydro_river_flow
hydro_river_temp
hydro_river_level
hydro_reservoir_level
hydro_soil_moisture
water_available
water_demand_city
water_demand_agri
water_demand_cooling
water_ecological_min
fire_risk_index
fire_event_count
fire_area_burned
```

理由：熱波は水不足、冷却水制約、農業取水、火災リスクを同時に動かす。

### 12.4 電力・交通・復旧

```text
power_supply
power_demand
power_cooling_demand
power_import_capacity
power_grid_restriction
transport_capacity_rail
transport_capacity_road
transport_disruption_count
repair_access_capacity
geo_background_constraint
```

理由：冷房普及率が低い地域では電力需要が跳ねにくい一方、人体側の被害が残る。一方で、既損傷グリッドや冷却水制約がある地域では、熱波が電力・復旧能力へ接続する。

### 12.5 人体・社会曝露

```text
health_excess_mortality
health_emergency_calls
health_cooling_access
population_exposed
population_density
ac_penetration
water_incident_count
```

理由：エアコン普及率が低い地域では、熱ストレスが電力系へ移らず人体側へ残る可能性がある。暑熱時には水不足だけでなく、水辺利用増加による水難事故も別系統として見る必要がある。

---

## 13. 採用・不採用理由の例

### 13.1 採用理由

```text
primary source with unit and date
official estimate with method
same spatial scope as target calculation
same time window as target calculation
definition matches variable registry
uncertainty stated and acceptable for this use
```

### 13.2 除外理由

```text
source_unclear
unit_missing
definition_mismatch
time_scope_mismatch
spatial_scope_mismatch
duplicate_weaker_source
insufficient_evidence
not_connected_to_variable
mixed_region
mixed_period
speculative_causality
```

理由：不採用理由を残さないと、後から同じ弱い値が再流入する。除外は失敗ではなく、接地品質を守る操作である。

---

## 14. 信頼できる過去事例の参照・照合

新しい事例を扱うときは、可能な限り信頼できる過去事例を参照し、今回の観測との共通点と差分を照合する。ただし、過去事例は類推による穴埋めに使わない。参照できるのは、変数候補、観測項目、欠損項目、照合すべき制約を見つける目的に限る。

### 14.1 参照対象

```text
公的調査報告
気象機関・水管理機関・電力事業者・交通事業者の記録
査読論文
行政・規制機関の事故報告
公式統計
一次資料に接続できる報道
```

### 14.2 照合項目

```text
対象地域
対象期間
気象条件
インフラ条件
人口曝露条件
既存損傷・背景制約
観測変数
単位
データ密度
欠損変数
事故・被害の発生経路
```

### 14.3 禁止事項

```text
過去事例が似ているという理由だけで未観測値を補完する
過去事例の被害率を今回へ直接移植する
地域差・時代差・インフラ差を無視して比較する
二次資料だけで因果を確定する
過去事例を adopted 扱いして今回の計算値へ混入する
```

### 14.4 使い方

過去事例は、次の用途に使う。

```text
見落としている変数候補を探す
観測台帳に必要な列を確認する
今回の事例で欠けているデータを明示する
物理制約または運用制約の接続候補を探す
警告表記に必要な根拠の厚みを確認する
```

理由：信頼できる過去事例は、今回の事例を解釈するための参照軸になる。しかし、過去事例は今回の観測値ではない。したがって、過去事例は照合と設計のために使い、欠損補完や確率移植には使わない。

---
## 15. 更新ルール

### 15.1 新規変数を追加する前の確認

```text
1. 既存変数で表現できないか
2. 類似変数との差分を説明できるか
3. 単位または定義状態を記録できるか
4. どの観測事象から必要になったか
5. どの既存方針と接続するか
6. 矛盾する既存記述はないか
```

### 15.2 新規観測値を追加する前の確認

```text
1. 出所は何か
2. 対象時点は何か
3. 対象地域は何か
4. 単位は何か
5. 定義は何か
6. どの変数に接続するか
7. reliability_level は何か
8. adoption_status は何か
9. 採用・保留・除外理由は何か
```

---

## 16. 未決事項

```text
variable_registry.csv の正式配置
observation_ledger.csv の正式配置
CSV の文字コードと改行規則
adopted への昇格手順
複数資料が矛盾した場合の優先規則
分布データの保存形式
GIS データとの接続方法
内部スコアから警告段階への変換方法
Pattern C の不確定範囲返却形式
```

これらは未決であり、現時点で固定しない。

---

## 17. まとめ

本プロトコルの最小原則は次の通りである。

```text
見合う根拠なき参入なし。
単位不明値を計算に入れない。
verified と adopted を分ける。
計算に使うのは adopted のみ。
欠損は補完しない。
推定は許すが、憶測は入れない。
警告に確率 % を表示しない。
なぜそうするのかを記録する。
```

---

*©M-Tokuni 2026*
