# 熱波インフラカスケード — 物理根拠足場
<!-- FILE: ground/ground_Report/pending/heatwave_cascade_foundation.md 26-0629 -->

ステータス：**pending**

注：本文書は例示設問（2026年6月ヨーロッパ熱波）を題材に、
ground/ フレームワークの適用方法論を示す足場である。
実観測データが充当された時点で active 移行を検討する。

---

## 方法論

式を先に決めず、観測から出す。

```
観測された事象
    ↓
その事象が示す物理量を特定
    ↓
次の観測事象との接続を問う
    ↓
式は後から出てくる
```

「式を先に立てて事象をはめ込む」は補完推論と同型のため禁止。
必須変数が ⊥ の場合は Pattern B → FAIL-CLOSED。

---

## 変数セット

### 気温（全系統共通の駆動変数）

$$x_1 = T_{max}(t) \quad \text{[日最高気温]}$$

$$x_2 = T_{min}(t) \quad \text{[日最低気温]}$$

$$x_3 = \Sigma_{heat}(t) = \sum_{\tau=0}^{t} \max\!\left(T(\tau) - T_{base},\ 0\right) \quad \text{[積算気温]}$$

$T_{max}$ と $T_{min}$ の両方が必要な理由：$T_{min}$ が高止まりすると夜間回復窓が閉じ、
各系統の $\delta$ が翌日開始時点ですでに削られた状態になる。

$\Sigma_{heat}$ は瞬間値が閾値未満でも累積で $\delta$ を削る。
河川水温・地中温度・構造物熱疲労はこの変数に支配される。

$T_{base}$ はドメインごとに異なる。決め打てない。

---

## 各系統の δ

### 電力

$$x_4 = P_{supply}(t), \quad x_5 = P_{demand}(t)$$

$$\delta_{power}(t) = P_{supply}(t) - P_{demand}(t)$$

| 側 | 変数 | 熱波下での方向 |
|---|---|---|
| 供給 | 原発出力（河川水温制限）、火力効率 | ↓ |
| 需要 | 冷房負荷（$T_{max}$ に対して非線形増加） | ↑ |

両側から同時に削られる。

---

### 水

$$x_6 = Q_{river}(t), \quad x_7 = Q_{demand}(t), \quad x_{11} = Q_{eco,min}$$

$$x_{12} = q_{nuclear}(t), \quad x_{13} = q_{agri}(t), \quad x_{14} = q_{city}(t)$$

$$\delta_{water,shared}(t) = Q_{river}(t) - Q_{eco,min} - \sum_i q_i(t)$$

$Q_{eco,min}$（環境基準流量）は法定固定値。差し引き後の残量に複数需要が競合する。

熱波下では $q_{nuclear}$・$q_{agri}$・$q_{city}$ が全項目同時に増加する。

$$x_{15} = \text{上下流位置} \quad \text{[構造変数・固定]}$$

水は上流→下流の一方向。地理的優位が法的優先順位に先行する。
電力と異なり「融通」が構造的に非対称。

---

### 電力網（融通・調整範囲）

$$x_8 = C_{interconnect}(i,j,t), \quad x_9 = \delta_{neighbor}(t), \quad x_{10} = \Omega_{balance}(t)$$

$$\Delta P_{import} = \min\!\left(\delta_{neighbor},\ C_{interconnect}\right)$$

$$\Omega_{balance}(t+1) = \Omega_{balance}(t)\ \cup\ \left\{j \mid \delta_j(t) \leq \epsilon,\ C_{interconnect}(i,j) < \text{要求量}\right\}$$

$\delta \to 0$ の地点が増えるにつれ、融通不可能ゾーンがネットワークトポロジーに沿って拡大する。
拡大は線形ではなく、連系線の構造に依存する。

---

### 物流

$$x_{16} = Q_{freight,river}(t), \quad x_{17} = \delta_{geo}(t), \quad x_{18} = C_{repair}(t)$$

$$\delta_{logistics}(t) = \delta_{design} - \delta_{geo}(t) - \delta_{heat}(t)$$

| 項 | 内容 |
|---|---|
| $\delta_{design}$ | 設計上の余裕（固定） |
| $\delta_{geo}(t)$ | 地政学的再ルーティングが熱波以前に消費済みの余裕（背景条件） |
| $\delta_{heat}(t)$ | 熱波による物理制約で削られる余裕 |

$\delta_{geo}$ は熱波が来た時点で確定済みの値。設計余裕の先食い。

$C_{repair}(t)$：物流依存の復旧到達可能性。
物流寸断が復旧機能そのものを止める。

---

## 電力・水の結合ループ

```
Q_river↓
  ↓
原発冷却水不足 → P_supply↓
  ↓
ポンプ停止 → Q_city↓
  ↓
農業が地下水に切替 → 揚水ポンプ電力需要↑
  ↓
P_demand↑ → δ_power↓（さらに削られる）
```

水と電力の $\delta$ が互いを削り合うループ。

---

## カスケード完成の構造

```
δ_power    → 0
δ_water    → 0
δ_logistics→ 0
C_repair   → 0
    ↓
復旧不能
```

$\delta_{geo}$ が設計余裕を先食いしているため、
熱波到達時点の実効余裕は $\delta_{design}$ より小さい。

---

## 変数セット一覧

| No. | 変数 | 内容 | 種別 |
|---|---|---|---|
| $x_1$ | $T_{max}(t)$ | 日最高気温 | 時系列 |
| $x_2$ | $T_{min}(t)$ | 日最低気温 | 時系列 |
| $x_3$ | $\Sigma_{heat}(t)$ | 積算気温 | 時系列 |
| $x_4$ | $P_{supply}(t)$ | 電力供給量 | 時系列 |
| $x_5$ | $P_{demand}(t)$ | 電力需要量 | 時系列 |
| $x_6$ | $Q_{river}(t)$ | 河川流量 | 時系列 |
| $x_7$ | $Q_{demand}(t)$ | 水需要量 | 時系列 |
| $x_8$ | $C_{interconnect}(i,j,t)$ | 連系線転送容量 | 構造＋時系列 |
| $x_9$ | $\delta_{neighbor}(t)$ | 隣接ゾーン余裕 | 時系列 |
| $x_{10}$ | $\Omega_{balance}(t)$ | 調整が閉じている地理的範囲 | 時系列 |
| $x_{11}$ | $Q_{eco,min}$ | 環境基準流量（法定） | 固定 |
| $x_{12}$ | $q_{nuclear}(t)$ | 原発冷却取水量 | 時系列 |
| $x_{13}$ | $q_{agri}(t)$ | 農業取水量 | 時系列 |
| $x_{14}$ | $q_{city}(t)$ | 都市用水量 | 時系列 |
| $x_{15}$ | 上下流位置 | 地理的トポロジー | 構造変数 |
| $x_{16}$ | $Q_{freight,river}(t)$ | 河川貨物可能積載量 | 時系列 |
| $x_{17}$ | $\delta_{geo}(t)$ | 地政学的既消費余裕 | 背景条件 |
| $x_{18}$ | $C_{repair}(t)$ | 復旧到達可能性 | 時系列 |

---

## Pattern 判定（現時点）

| 変数 | 状態 |
|---|---|
| $T_{max}(t)$, $T_{min}(t)$ | 気象記録から取得可能 |
| $\Sigma_{heat}(t)$ | 上記から算出可能 |
| $Q_{river}(t)$ | 水管理局データ（入手可否による） |
| $\delta_{geo}(t)$ | 推計値・観測値混在 → Pattern C |
| 2026年6月実イベント観測値 | 現時点 ⊥ → Pattern B |

---

## 未着手

```
鉄道・道路系統の δ
各変数間の時定数の違い（電力：秒〜分 / 水：日〜週）
Ω_balance 拡大の止まり条件
T_base のドメイン別決定
実観測値の充当
```

---

*©M-Tokuni 2026*
