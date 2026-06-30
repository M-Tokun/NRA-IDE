# 逆行接地方針（Inverse Grounding Policy）Rev.2.1
<!-- FILE: ground/policies/inverse_grounding_policy.md 26-0629 -->
<!-- 前版：26-0628-1855 → 型分離・FAIL-CLOSED精密化・ハード制約化 -->

ステータス：**active**

注：このファイルはIDE側の接地・境界制御方針であり、NRA公理を追加しない。
真理や存在を決定するものではなく、実行へ渡してよい入力かを判定する。

---

## Layer 0：接地セマンティクス（変更不可・最優先）

### 変数の型分離

$$e_i \in \{0,\ 1\}$$

$$x_i \in \mathcal{X}_i \cup \{\bot\}$$

$$e_i = 1 \Rightarrow x_i \in \mathcal{X}_i$$

$$e_i = 0 \Rightarrow x_i = \bot$$

- $e_i$：接地フラグ（変数 $i$ の観測・定義・出所が実行文脈で使用可能か）
- $x_i$：実際の物理値
- $\bot$：未観測・未定義・検証不能・未使用可能（数値補完を許さない状態）

**型の原則：二値性は物理値そのものではなく接地フラグに適用する。**

### FAIL-CLOSED条件

$$i \notin \Omega_{\mathrm{declared}} \Rightarrow x_i = \bot$$

$$\exists i \in M_{\mathrm{required}},\ x_i = \bot \Rightarrow \mathrm{FAIL\text{-}CLOSED}$$

- $M_{\mathrm{required}}$：当該逆算・行動判断に不可欠な必須変数集合
- $\Omega_{\mathrm{declared}}$：宣言済み変数空間

**FAIL-CLOSEDの意味：未知変数を不存在と断定しない。
ただし未知を含んだまま行動決定へ進む実行権限を停止する。**

**欠損変数への補完推論は無条件で禁止する。**

---

## Layer 1：要素計算式

### 実行可能集合の確定（ハード制約）

$$\mathcal{A} = \left\{x \mid x \in \mathcal{C}_{phys},\ \forall i \in M_{\mathrm{required}},\ e_i = 1\right\}$$

$$\mathcal{A} = \varnothing \Rightarrow \mathrm{FAIL\text{-}CLOSED}$$

- $\mathcal{C}_{phys}$：保存則・境界条件・因果順序を満たす物理的許容集合
- **$\mathcal{C}_{phys}$ はペナルティではなくハードゲート。最低限の物理制約に反する候補は実行候補外。**

### 逆算実行（$\mathcal{A} \neq \varnothing$ の場合のみ）

$$\hat{x} = \arg\min_{x \in \mathcal{A}}\ \mathcal{L}(F(x),\ R)$$

- $R$：現実観察値（物理直接計測値のみ有効）
- $\hat{x}$：物理制約内で観測値に最も近い原因状態

### 横軸スコア $\delta_{inv}$

$$\mathcal{I}_{phys}(R) = \left\{x \mid x \in \mathcal{C}_{phys},\ F(x) \approx R\right\}$$

$$\delta_{inv} = \inf_{x \in \mathcal{I}_{phys}(R)}\ d(\hat{x}_{AI},\ x)$$

- $\hat{x}_{AI}$：AIが提案する原因状態
- $\delta_{inv}$：AI案が物理的許容集合からどれだけ外れているか

**「もっともらしい説明」ではなく「物理的許容集合への距離」が横軸スコアの実体。**

---

## Layer 2：3パターン実行条件

```
Pattern A：全必須変数有効
　∀i ∈ M_required, e_i=1 かつ A ≠ ∅
　→ 逆算実行（hat_x 返却）

Pattern B：必須変数欠損
　∃i ∈ M_required, x_i=⊥
　→ FAIL-CLOSED発火（実行権限停止）

Pattern C：非必須変数欠損
　∃i ∉ M_required, x_i=⊥ かつ ∀i ∈ M_required, e_i=1
　→ 欠損を明示して継続（補完禁止）
```

**PatternCの欠損明示は補完ではない。不確定範囲を返すことが正常な出力。**

---

## Layer 3：適用条件・境界条件

### 適用可能ドメイン

$\mathcal{C}_{phys}$ が定義可能なドメイン。

```
例：気象・農業・構造力学・化学反応・水理学
```

### 適用境界（禁止ドメイン）

```
例：人間行動・市場価格・社会現象
　　→ C_phys が存在しない領域
```

### 観測台帳（必須付帯情報）

変数 $x_i$ に必ず付帯させるメタデータ：

```
取得時刻・場所・単位・機器・校正状態・測定誤差・出所
```

### 探索系と実行系の分離

```
探索（未知変数の候補化）：許可
実行（仮説を行動判断へ流入）：禁止
```

### 接地品質スコア（IDE内部の横軸運用指標）

$$P_{ground} = \frac{A_{valid} \cdot C_{trace}}{\kappa_{compute}}$$

- $A_{valid}$：必須変数の有効観測率
- $C_{trace}$：観測→制約→式→結論の追跡可能率
- $\kappa_{compute}$：計算・探索コスト
- **注：$\tau$ は NRA-IDE既存構造の吸収厚みと衝突するため $\kappa$ に変更**
- **$P_{ground}$ は $R=\delta/\tau$ と同型ではない。接地品質の運用指標として扱う。**

---

## NRA-IDE接続

| NRA-IDE原理 | 接続 |
|---|---|
| IDE | 接地判断・境界制御・実行前ゲート |
| FAIL-CLOSED | 実行権限停止（不存在断定ではない） |
| 横軸制御 | 事実・観測・出所・物理制約・閾値に基づく実行可否判定 |

---

## 変更履歴

| 版 | 日時 | 変更内容 |
|---|---|---|
| Rev.1 | 26-0628-1855 | 初版 |
| Rev.2 | 26-0628-1913 | 型分離・FAIL-CLOSED精密化・ハード制約化・τ→κ |
| Rev.2.1 | 26-0629 | 公理扱いを撤回し、IDE側の接地・境界制御方針として再定義 |

---

*©M-Tokuni 2026*
