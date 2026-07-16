# nra-core/quantum 整合性精査報告

- 精査日: 2026-07-14
- 対象: `nra-core/quantum/NRA-IDE_quantum_Python` 配下Markdown 2件、Python 6件
- 照合基準: `theory/AXIOMS.md`、`theory/axioms.json` v2.1、`theory/SANDWICH_ARCH.md`、papers配下量子対応文書
- 方針: 原資料は変更せず、後続の訂正・再設計に必要な事項を記録する。

## 1. 総合判定

量子サブディレクトリは「構想資料および未完成デモ」である。正典v2.1準拠、量子測定問題の解決、量子誤り訂正の代替、完成済み実装のいずれとも判定できない。

主要理由:

1. 2文書の結論と式が互いに矛盾する。
2. Python 6件すべてに実行を阻止するQuTiP APIまたはQobj次元上の問題がある。
3. コヒーレンス、人口、密度行列、測定、resetを混同する。
4. `max`式、R=1固定、reset、独自purpose_modeが正典v2.1と不整合。
5. 入力domain、単位、finite、非負性、量子状態の型を検証しない。
6. 「完成」「測定問題解消」「QECより事前制御」等の結論を支える試験・導出・実験がない。

## 2. 文書間の直接矛盾

### `NRA_IDE_Quantum_Measurement_Session_2026-03-28_1920.md`

この文書は、新しい式・原則は不要であり、外部系のδ・τを既存式へ加えるだけで量子測定問題が解消すると主張する。

### `NRA-IDE_量子拡張セッションサマリー_2026-03-28.md`

この文書は、`R_quantum`、δ2、lambda、interference、tau_q、purpose_modeという新しい式・変数・状態を導入する。

したがって「新設不要」と「量子拡張式を新設」は両立しない。

## 3. 量子測定問題文書

- 系と測定器を複合系へ含めるだけでは、Born則、単一結果、基底選択、デコヒーレンス後の混合状態を説明しない。
- 不確定性原理を「τが有限である帰結」とするが、非可換演算子・交換関係からの導出がない。
- 波動関数を「構造の影」とするのは哲学的主張で、計算定義ではない。
- `(delta_S+delta_external)/(tau_S+tau_external)`に単位、重み、相互作用、相関項がない。
- 外部tau追加によりRが低下し、測定が安定性を増す場合がある。
- 系境界を不要としながらdelta_Sとdelta_externalを区別し、自己矛盾する。
- 「哲学的結論ではなく計算構造の帰結」という結論に必要な状態空間・演算子・確率・予測がない。

## 4. 量子拡張サマリー

### 正典不整合

- 上下・量子チャネルを`max`で統合し、排他的原因チャネル選択と衝突する。
- R>=1でdelta reset、基底射影、階層resetを行い、不可逆ラッチと衝突する。
- 独自purpose_modeは現行正典状態と対応しない。
- OUT_OF_DESCRIPTION_DOMAIN、CONFESSION、領域別閾値、証言継続がない。
- 経路ログから原因を逆算する主張は因果ダイオードの逆推論禁止とも衝突する。

### 量子式

- tau_qをコヒーレンス時間、delta2をfidelity・entropy・行列要素候補とし、単位・意味が一致しない。
- fidelityそのものは偏差ではなく、`1-F`等の定義が必要。
- オフダイアゴナル要素は基底依存。
- interferenceは負になり得、delta・Rの非負性を保証しない。
- 高コヒーレンスほどRが増え、良好な状態を崩壊へ近づける可能性がある。
- R=1で決定論的に崩壊しても、測定結果の確率分布を導出しない。
- 測定閾値とデコヒーレンス時間を同じtauとして混同する。

### 固定小数点構想

- IEEE 754の指数部が勝手にdelta/tau比を変えるという説明は誤り。
- 固定小数点にも量子化、丸め、飽和、overflowがあり「丸めなし」は成立しない。
- 128bit packetに符号、scale、endianness、overflow、欠損値、時刻wrapが未定義。
- 16bit Step Indexは65536 stepで周回する。
- 8bit checksumは完全性を保証しない。
- 48bitで微細情報を全て記録できる根拠がない。
- 量子registerを毎step無擾乱で読み出すことはできない。
- 実現可能性85～95%に評価方法がない。

### 検証・文書品質

- 波形一致だけでモデルが現実を正しく追跡すると断定できない。
- 固定小数点logから原因を一意に逆算できない。
- 冒頭HTML commentが閉じていない。
- 推奨file名と実fileの`01_`～`06_`prefixが一致しない。
- Markdown tableの行間に空行がある。

## 5. Python 6件共通

- `compute_r_quantum`が複製され、係数・lambda・tau式がfileごとに異なる。
- `max`による三channel統合を使用する。
- R=1固定、reset、独自purpose_modeを使用する。
- 非負性、[0,1]、finite、tau正値、単位を検証しない。
- 高いcoherenceをdeltaとして加算し、崩壊riskを上げる。
- test、期待値、requirements、QuTiP対応version指定がない。

## 6. 実行不能箇所

### 01、02、03

次の呼出しは`expect`のstate引数が欠ける。

```python
e_ops=[expect(sigmaz())]
```

通常は`mesolve`へobservableを渡す形、例えば`e_ops=[sigmaz()]`が必要。

### 04、05、06

次のcollapse operator構築は3x3 operatorと1x3 braの積になり、QuTiP次元が適合しない。

```python
destroy(3) * basis(3, i).dag()
```

### 密度行列

collapse operator使用後の`mesolve`状態はdensity matrixになるが、03～06はさらに`psi*psi.dag()`を行い、density matrixを二乗する。

## 7. `01_rhizosphere_quantum_demo.py`

- `|0>`との重なり確率をcoherenceと呼ぶが、これは基底人口。
- delta1・delta2が負または範囲外になり得る。
- R_op引数は未使用。
- delta_nextを呼出側が使用せず、phase jump時のdelta resetが実装されない。
- 時間依存Hamiltonianの時刻を毎step 0へ戻し、外部位相が連続しない。
- psi resetだけを微生物から根へのenergy transferと解釈する根拠がない。

## 8. `02_rhizosphere_nested_quantum.py`

- R_op属性は未使用。
- classical layerでもdelta2_coherenceを乱数更新する。
- quantum layerでdelta2をresetしてもpsiをresetせず、次stepに元のpsiからdelta2が再生成される。
- child jump feedbackはparent R計算後に加算され、同stepのparent履歴へ反映されない。
- 「数百層」は100 sibling追加例であり、深いnestの検証ではない。
- 循環参照、再帰深度、計算量への防御がない。

## 9. `03_nisq_fmo_2site.py`

- 初期等重ね合わせは使用Hamiltonianの固有状態で、意図したsite間transferの観察条件として不適切。
- `expect(sigmaz())`引数不足で停止する。
- noise rateの単位とHamiltonian・dtの尺度対応がない。
- 「現実NISQ deviceに近い」根拠がなく、実装はgate型hardwareでなくQuTiP開放系simulation。
- collapse operator使用後のstate型を誤って扱う。
- R到達時のsite0 projectionはQECでも測定modelでもない。

## 10. `04_nisq_fmo_3site.py`

- collapse operatorがQobj次元不一致。
- density matrixを二乗してcoherenceを計算する。
- off-diagonal総和へ`2/3`を掛ける正規化は最大状態で1を超え得る。
- Hamiltonianの単位、出典、hbar、時間尺度がない。
- R到達時のsite2強制projectionはHamiltonianから導出されない。
- `nutrient_transfer_quantum`は光励起energy移動とnutrient移動を混同する。

## 11. `05_fmo_fluctuation_path_log.py`

- 04と同じcollapse operator次元不一致、density matrix二乗、coherence正規化問題がある。
- 「生log・丸めなし」に対し、値を6桁へroundする。
- Python floatであり固定小数点構想を実装しない。
- delta/R logだけではquantum pathや原因を一意に復元できない。
- `path_log_output.json`をcurrent directoryへ上書きする。
- 6D Visualizerとのschema・readerがない。

## 12. `06_quantum_error_control_demo.py`

- 04・05と同じ実行不能箇所がある。
- real-time hardware監視ではなくoffline numerical loop。
- syndrome測定、logical qubit、error correctionを実装せず、単に初期stateへresetする。
- resetは計算状態を破棄し、QECの代替にならない。
- 次stepから無条件に再開し、人間承認・latchがない。
- QECを単なる事後処理とする説明は不正確。

## 13. 修正優先順位

1. 「完成」「測定問題解消」「QEC代替」の表現を未検証仮説へ変更する。
2. QuTiP API、collapse operator、ket/density matrix処理を修正し、最小testを追加する。
3. coherence・population・fidelity・decoherence rateを別type・別単位で定義する。
4. compute_r_quantumを一箇所へ統合し、domain・単位・finiteを検証する。
5. v2.1状態機械、排他的channel、OOD、latchへ更新する。
6. reset・projectionを物理modelまたはcontrol actionとして明確に分離する。
7. fixed-point packetのscale、符号、overflow、checksum、versionを仕様化する。
8. raw logと丸め済みdisplay logを分離し、Visualizer schemaを定義する。
9. FMO modelの出典・単位・時間scale・観測量を明示する。
10. 再現可能な期待値、test fixture、QuTiP version、実行手順を追加する。
