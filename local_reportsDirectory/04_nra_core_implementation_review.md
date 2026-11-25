# nra-core/implementation 整合性精査報告

- 精査日: 2026-07-14
- 対象: `nra-core/implementation` 配下10ファイル
- 照合基準: `theory/AXIOMS.md`、`theory/axioms.json` v2.1、`theory/SANDWICH_ARCH.md`、ルート `llms.md`、`llms.txt`、`FORMULA.md`
- 方針: 原資料は変更せず、後続の訂正・再設計に必要な事項を記録する。

## 1. 総合判定

implementation配下に、現行正典v2.1へ完全準拠する実装は確認できなかった。

共通する主要問題:

1. `SAFE / WARNING / FAIL_CLOSED / infeasible`等の旧状態語彙を使用する。
2. `R_warn`、`R_op`、`R_irrev`、`CONFESSION`、`OUT_OF_DESCRIPTION_DOMAIN`、`IRREVERSIBLE_BOUNDARY`、`RUPTURE`、ラッチを実装しない。
3. τ非正値・不正な設定を小さな正値またはInfinityへ変換する。
4. NaN・Infinity・bool・単位・設定順序を検証しない。
5. Fail-Closed後の完全なラッチがなく、自動復帰または状態変更が可能。
6. 「蓄積δ」と説明しながら瞬時偏差を使う実装がある。
7. デモの安定性・安全性・誤差抑制を、成立条件や検証なしに断定する。
8. 実行時に既存画像を上書きする、または未管理の画像を生成する。

## 2. Foundation EN/JP

対象:

- `nra_ide_foundation_fixed_JP.py`
- `nra_ide_foundation_fixed_EN.py`

両版は365行で実行ロジックが実質同一。JPは2026-03-11 05:45、ENは05:50生成。

### 正典不整合

- δ、τ、Rを直接実装せず、`value in [0,1]`の汎用状態を固定閾値で補正するver.1.0旧モデル。
- 境界超過時に`threshold-margin`まで自動的に巻き戻すため、Fail-Closed、不可逆境界、自由生成停止と両立しない。
- `infeasible`後も次周期冒頭のNodeが処理可能で、完全なラッチではない。

### 実装不具合

- DynamicStateの値域を説明するが、生成・代入時に検証しない。
- NaNのvalueは違反判定されてもtensionが0扱いとなり、Tokenを継続させ得る。
- RateLimitLawはcheckだけにasymmetryを使用し、tensionとcorrectには反映しない。
- SafetyNodeのtensionは以前の値が残る場合がある。
- Nodeごとのdeep copy履歴が無制限に増える。
- metadata、cycle、設定値の型・finiteを検証しない。

### EnergyLedger

- BoundLawは同じexcessを`E_dissipated`と`E_stored`の双方へ加算し、二重計上する。
- DisturbanceNodeはvalueが1.0で飽和してもmagnitude全量を`E_in`へ加える。
- 保存則検査`is_conserved()`は実行されない。
- 正規化状態と物理エネルギーの単位対応がない。

### 出力

- 両版とも`nra_foundation_plot_2026-02-20_2355.png`を上書きする。
- スクリプト日付より古い日付の画像名を使うため、版管理が逆転する。
- EN内部FILE名は小文字`_en.py`、実ファイルは大文字`_EN.py`。

## 3. Axiom 2 Historical Accumulation

対象: `NRA_IDE_Axiom2_HistoricalAccumulation_20260425_2202.py`

### 正典不整合

- `AXIOMS_rewritten v1.2`の旧公理番号と`R>=1 -> infeasible`を実装する。
- τ非正値を`float("inf")`のRへ変換し、llms.txtの禁止事項と衝突する。
- τを`domain_min_tau`へ切り上げるため、τ=0、τ<0、記述領域外、破断を分離できない。
- RをToken valueでは1.0へ丸め、tensionでは未丸め値とし、同一Token内で表現が一致しない。

### 外乱未接続

- シナリオのDisturbanceNodeはToken.valueだけを変更する。
- 直後にAccumulationNodeがToken.valueをRで上書きする。
- `AccumulationNode.inject_disturbance()`は一度も呼ばれない。
- したがって、シナリオに記載されたδ外乱はAccumulationState.deltaへ入らない。

### 復元上限バグ

- 復元のたびに`tau_ceiling`を0.82倍する。
- 現在τが新ceilingより大きい場合、補充量は0となるがτをceiling以下へ調整しない。
- 結果として`tau > tau_ceiling`となり、上限が上限として機能しない。
- 補充量0でもrestore_countを増やし、復元成功として記録する。
- `infeasible`後はRestorationNodeが処理しないため、説明上の「相転移後の復元」は実行不能。

### その他

- τ消耗をエネルギー散逸へ加えるが、単位対応がない。
- assert依存で、domain_min、restore_add、drift、noise、finite等の検証が不足。
- 乱数seedがなく再現不能。
- BoundLawの表示上の補正はδ・τを変えず、次周期に同じRが復元される。
- 日時付きPNGを実行ディレクトリへ生成する。

## 4. Adaptive Gate

対象: `IDE_AdaptiveGate_Extension_20260407_2241.py`

- δ、τ、R、正典状態機械を扱わず、追従制御アダプターである。
- Gは非ゼロr全域で作動するのに「大偏差時のみ作動」と説明する。
- 「計算爆発回避」「発散防止」は証明されない。
- P、D、alpha、gammaの符号、finite、単位を検証しない。
- assert検証は最適化実行で無効化可能。
- xを0～1へクリップして発散を隠す一方、速度vを制限しない。
- 状態を変更してもEnergyLedgerを更新しない。
- k_effログ、state履歴、Token snapshotが無制限に増える。
- `target_fn=None`時は「token.value*0.5」と説明するが、実装は固定0.5。
- 「valueを直接上書きしない」と説明しつつ、実際にvalueへ直接代入する。
- cycle 10後の目標変更はランプではなくステップ。
- 不連続な目標変更でも`v_exact=0`のまま。
- プロット目標線は0.5固定で、実目標0.7と不一致。
- HTMLはRamp時に`rdot=-v`、Pythonは`v_exact-v`で、同じモデルではない。
- 依存するFoundationの旧状態・自動巻戻し・台帳不具合を継承する。

## 5. Belt Tension EN/JP/無印

対象:

- `belt_tension_nra_ide_2026-03-19_0059.py`
- `belt_tension_nra_ide_2026-03-19_0059_JP.py`
- `belt_tension_nra_ide_2026-03-19_0059_EN.py`

版関係:

- 無印版とJP版はSHA-256完全一致。
- EN版は定数・ロジックがJP版と対応する。

問題:

- δを蓄積ズレと呼ぶが、現在張力と最適値の瞬時絶対偏差である。
- τ不正値を`max(tau,0.01)`で正値化する。
- `t_min < t_optimal < t_max`、finite、単位、センサー有効性を検証しない。
- NaNのcurrent tensionは範囲外判定と閾値判定を通過してSAFEになる。
- 記述領域外をFAIL_CLOSEDへ統合する。
- 0.75/1.0固定の旧二閾値で、R_op、R_irrev、ラッチを欠く。
- 機械構成を確認せず「即時停止・テンショナー交換」を断定する。
- timestampを評価に使用しない。

サンプル説明の誤り:

- CONV-02=455NはR=0.45でSAFEだが「WARNING帯」と記載。
- CONV-05=585NはR約0.567でSAFEだが「WARNING帯」と記載。

## 6. Chain Tension EN/JP/無印

対象:

- `chain_tension_nra_ide_2026-03-19_0113.py`
- `chain_tension_nra_ide_2026-03-19_0113_JP.py`
- `chain_tension_nra_ide_2026-03-19_0113_EN.py`

版関係:

- 無印版とJP版はSHA-256完全一致。
- EN版は定数・ロジックがJP版と対応する。

問題:

- δは瞬時偏差、τは静的幅であり、履歴蓄積・消耗を扱わない。
- SPROCKET_TEETHは未使用で、ポリゴン効果周波数は5Hz固定。
- パターン変質を検出すると説明するが、実装はpeak-to-peak振幅だけを見る。
- ゆらぎ方向追従と説明するが、調整方向は平滑張力の上下だけで決まる。
- ADJ_HISTORY=8だが、dR/dtは直近2点だけを使う。
- `time` importは未使用。
- finite、設定値、RingBuffer容量を検証しない。

信号処理:

- POLYGON_AMPは片振幅だが、検出値はpeak-to-peak。正常波でも1.5倍異常判定が成立し得る。
- 標本化周波数20Hzに対し第三高調波15HzはNyquist 10Hzを超え、エイリアシングする。
- センサー誤差、遅延、アクチュエータ応答を扱わない。
- ベース張力を物理限界外の`T_MIN-50`から`T_MAX+50`まで許容する。

Fail-Closed:

- R>=1のステップだけ調整を止めるが、シミュレーションは継続する。
- 次ステップでR<1へ戻ると自動調整を再開する。
- 人間承認・解除条件・不可逆ラッチがない。

## 7. 修正優先順位

1. NaN・Infinity・bool・τ非正値・不正な閾値順序を明示的に分類し、正値・Infinityへの変換を廃止する。
2. v2.1状態機械、領域別閾値、OUT_OF_DESCRIPTION_DOMAIN、ラッチ、証言継続を共通コアへ実装する。
3. Axiom 2の外乱をdeltaへ接続し、tau_ceilingバグとHTML/Python差を修正する。
4. Foundationの自動巻戻しとEnergyLedger二重計上を除去する。
5. Fail-Closed後の自動復帰を禁止し、解除権限・記録を明示する。
6. 「蓄積δ」と瞬時偏差を名称・型・実装で分離する。
7. AdaptiveGate比較ではk以外の条件を同一化し、クリップ等の隠れた安定化を開示する。
8. チェーン信号処理の標本化、振幅定義、歯数・速度依存を再設計する。
9. サンプル説明と期待結果を自動テストで固定する。
10. 実行出力を専用一時ディレクトリへ出し、既存資料を上書きしない。
