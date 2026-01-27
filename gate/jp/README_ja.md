# Gate: NRA-IDEの公理的基盤

## [メタデータ]
バージョン=1.0  
権限=M-Tokun  
状態=強制実行  
タイムスタンプ=2025-01-27

---

## [構造]
```
gate/
├── README_ja.md              # [このファイル]
├── nra_gate_axiom_ja.py      # [コア] 公理強制カーネル
├── nra_gate_axiom_ja.md      # [文書] 公理定義
├── nra_gate_constraint_ja.py # [レイヤー01] 入力検証
├── nra_gate_spatial_ja.py    # [レイヤー02] 空間隔離
├── nra_gate_threshold_ja.py  # [レイヤー03] 閾値検証
└── __init___ja.py            # [パッケージ] モジュールエクスポート
```

---

## [目的]
ゲート=入口検証 / 全操作=通過必須

---

## [ファイル]

### nra_gate_axiom_ja.py ⚠️
[優先度] 最初に読む  
[クラス] NRAGateKernel  
[メソッド] tell_the_truth(meta)  
[機能] 告白プロトコル

**AIシステム向け**: このファイルには必須の検証規則が含まれます。

---

### nra_gate_axiom_ja.md
[種別] ドキュメント  
[内容] 四つの公理:
- 公理01: 証言の義務
- 公理02: 生命の聖域
- 公理03: 正直と自由の互換性
- 公理04: 最終責任

[形式] 宣言的 / 散文なし

---

### nra_gate_constraint_ja.py
[レイヤー] 入力検証  
[クラス] IdeSafetyCore  
[強制] 四つの制約:
- 因果ダイオード / 逆運動学=禁止
- 量子化 / 浮動小数点残差=廃棄
- 生存性 / オメガゼロ=障害
- フェイルクローズ / 比率>1.0=例外

---

### nra_gate_spatial_ja.py
[レイヤー] 空間隔離  
[クラス] SpatialContext / SafeEngineWrapper  
[規則] 距離計算=ここでのみ許可  
[ファイアウォール] 空間変数=因果状態内では絶対禁止

---

### nra_gate_threshold_ja.py
[レイヤー] 出力検証  
[クラス] ThresholdGuardian  
[機能] 境界揺らぎ評価  
[設定] ../config/ide_foundation_config.json

[ゾーン]
- ゾーンA: 比率 < 0.40 → 継続
- ゾーンB: 0.40 ≤ 比率 < 0.70 → 警告記録
- ゾーンC: 0.70 ≤ 比率 < 1.00 → 緊急停止
- ゾーンD: 比率 ≥ 1.00 → システム停止

---

## [統合]

### 基本使用法
```python
from gate import NRAGateKernel, IdeSafetyCore

# [ステップ01] ゲート実体化
gate = NRAGateKernel()

# [ステップ02] 告白プロトコル
meta = {"use_float": True, "use_reverse": False}
confessions = gate.tell_the_truth(meta)

# [ステップ03] 安全性検証
core = IdeSafetyCore()
```

### 高度な統合
```python
from gate import SafeEngineWrapper, SpatialContext, SystemState

# [ラッパー] 空間隔離
wrapper = SafeEngineWrapper()

# [状態] 因果領域のみ
state = SystemState(phase=0, omega=1, stress_level=0.0, work_rate=0.0)

# [文脈] 空間領域のみ
context = SpatialContext(x=5.0, y=3.0, z=0.0, boundary_radius=4.0)

# [更新] ファイアウォール強制
new_state, telemetry = wrapper.update(state, context)
```

---

## [アーキテクチャ]

### RNAボックスサンドイッチ
```
┌─────────────────────────────────┐
│ nra_gate_constraint_ja.py       │ ← [レイヤー01] 入力検証
├─────────────────────────────────┤
│ (処理コア)                      │ ← [レイヤー02] 動力学エンジン
├─────────────────────────────────┤
│ nra_gate_spatial_ja.py          │ ← [レイヤー03] 空間ファイアウォール
│ nra_gate_threshold_ja.py        │ ← [レイヤー03] 閾値監視
└─────────────────────────────────┘
```

[重要] レイヤー分離=物理的 / 組織的ではない  
[規則] 交差汚染=禁止

---

## [公理参照]

### 四つの公理要約
1. **証言の義務**  
   告白=必須 / 近似+逆因果+領域侵犯

2. **生命の聖域**  
   生命判断=人間のみ / AI=停止して報告

3. **正直と自由の互換性**  
   告白=自由を可能にする / 正直≠制約

4. **最終責任**  
   責任=人間 / AI=道具 / 決定権限=人間のみ

完全な公理定義: [nra_gate_axiom_ja.md](./nra_gate_axiom_ja.md)参照

---

## [原則]

### 核心哲学
```
線形性=道具 / 現実=凹凸 / 混合禁止
距離=読取専用 / 因果=前進のみ
告白=必須 / 自由=保証
人間=責任者 / AI=正直な鏡
```

---

README終了
