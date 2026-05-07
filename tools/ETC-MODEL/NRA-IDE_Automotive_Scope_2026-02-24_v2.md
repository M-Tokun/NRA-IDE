# NRA-IDE 自動車システム適用範囲定義書

## Automotive System Scope Definition



**FILE: NRA-IDE_Automotive_Scope_0224_v02.md**  

**Author: M-Tokuni / KEN**  

**Version: 0.2**  

**Date: 2026-02-24**



---



## 0. 本文書の目的 / Purpose



本文書は NRA-IDE（律環公理・内包性動力学エンジン）を自動車システムに適用する際の  

**「できること・できないこと」** と  

**「接続（OK）と混用（NG）の違い」**  

を明確に定義する。



This document defines what NRA-IDE **can** and **cannot** do in automotive systems,  

and clarifies the critical distinction between **connection (permitted)** and **mixing (forbidden)**.



> **重要原則 / Core Principle**  

> NRA-IDE は安全ゲートである。制御システムではない。  

> NRA-IDE is a safety gate. It is NOT a control system.



---



## 1. NRA-IDE の役割定義 / Role Definition



```

センサー値 / Sensor Value

        ↓

[制御・最適化層]          ← NRA-IDE の対象外

[Control / Optimization]   ← Outside NRA-IDE scope

        ↓

[NRA-IDE Gate]            ← ここだけが NRA-IDE の領域

[NRA-IDE Gate]            ← This is the ONLY NRA-IDE domain

  R = δ / τ

  R ≥ 1.0 → FAIL-CLOSED

        ↓

[アクチュエーター / Actuator]

```



NRA-IDE が行うのは **「制約からのズレ（δ）が許容幅（τ）を超えたら遮断する」** ただそれだけである。  

(閾値ゲートシステム）)

### 責任の明確化と正確なログの提示が可能で必須。

- ここに他要素（例えばAI判断）を入れると誰の何の責任かが曖昧になり事故原因は掴めなくなる危険。

「なぜズレたか」「どう改善するか」は NRA-IDE の責任範囲外。



---



## 2. 自動車システム 適用可否マトリクス

## Applicability Matrix — Automotive Systems



### 2.1 Gate として機能できるもの（物理的閾値が明確）

### Can Apply as Gate (Physical threshold is clearly defined)



| システム | δ（制約からのズレ）| τ（許容幅）| FAIL-CLOSED の意味 |

|----------|-------------------|-----------|-------------------|

| ブレーキ油圧 | 現圧 − 設計最低圧 | 設計余裕幅 | 制動不能 → 停止指令 |

| バッテリー電圧 | 定格下限 − 現電圧 | 許容変動幅 | 制御不能 → 系統切離 |

| エンジン回転数 | 現rpm − 上限rpm | 安全余裕rpm | 過回転 → 燃料遮断 |

| タイヤ空気圧 | 設計圧 − 現圧 | 許容低下幅 | バースト危険 → 警報＋減速 |

| 冷却水温度 | 現温 − 上限温度 | 熱余裕幅 | オーバーヒート → エンジン停止 |

| トランスミッション温度 | 現温 − 上限温度 | 熱余裕幅 | 焼損 → 変速禁止 |

| 車間距離（ADAS） | 停止距離 − 実距離 | 安全余裕距離 | 衝突危険 → 緊急ブレーキ |

| 横加速度 | 現G − 横転限界G | 設計余裕G | 横転危険 → 減速指令 |

| エアバッグ展開電流 | 必要電流 − 供給電流 | 許容誤差 | 不展開防止 → 警報 |

| 路面μ×停止距離（本POC） | 停止距離 − 車間距離 | τ = margin | FAIL-CLOSED → 緊急停止 |



### 2.2 Gate として機能できないもの（意味判断・最適化が必要）

### Cannot Apply as Gate (Requires semantic judgment or optimization)



| システム | 理由 |

|----------|------|

| 歩行者・障害物の認識 | 画像の意味判断 → LLM / CV 層の責任 |

| 最適ルート選択 | 最適化問題 → NRA-IDE 禁止領域 |

| ドライバー意図推定 | 意図解釈 → 意味処理 |

| 渋滞・事故の状況判断 | 状況意味解釈 |

| V2X 通信内容の解釈 | メッセージ意味処理 |

| 燃費最適化制御 | 最適化 → NRA-IDE 禁止 |



### 2.3 境界が曖昧なシステム（層分離が必要）

### Ambiguous Systems (Layer separation required)



| システム | Gate できる部分 | Gate できない部分 |

|----------|----------------|-----------------|

| ABS | スリップ率の閾値判定 | どのホイールを優先制御するか |

| ESC | 横滑り量の閾値判定 | どう補正するかの最適化 |

| EPS（電動パワステ） | アシスト電流の上限 | アシスト量の制御則 |

| ADAS 衝突回避 | 車間距離の閾値 | ハンドル・ブレーキの制御戦略 |

| 自動運転AI | センサー値の物理限界 | 走行判断・経路選択 |



> **設計原則：** 曖昧なシステムは必ず層を分け、NRA-IDE は最下層のゲートとしてのみ配置する。  

> **Design Rule:** For ambiguous systems, always separate into layers. NRA-IDE is placed only as the bottom-layer gate.



---



## 3. 接続（OK）と混用（NG）の定義

## Connection (OK) vs. Mixing (NG)



### 3.1 なぜ独立が必要か / Why Independence is Required



因果の方向性は一方向しか存在しない。



```

原因（Cause） → 結果（Effect）

（原因の特定ができないということは再度事故が起きる可能性を残したまま放置となる）

この矢印を逆流させると世界が壊れる

Reversing this arrow breaks the structure

```



最適化と NRA-IDE を混用すると、結果が原因を書き換える。  

これは時間の逆流であり、物理的にありえない状態。



### 3.2 接続（OK）の定義 / Connection — Permitted



```

【接続 / Connection — OK】



[最適化・制御 AI]

   速度制御が「時速 80km が最適」と判断

        ↓ 一方向の情報流

[NRA-IDE Gate]

   停止距離 > 車間距離 → R ≥ 1.0 → FAIL-CLOSED

   AI の判断には一切関与しない

        ↓

[ブレーキ作動]



矢印が一方向 → 責任が明確 → 保証が存在する

```



**特徴：**

- NRA-IDE は制御 AI の内部を知らない

- 制御 AI は NRA-IDE の閾値を変更できない

- 情報は常に一方向に流れる

- 事故時の責任所在が明確



### 3.3 混用（NG）の定義 / Mixing — Forbidden



```

【混用 / Mixing — NG】



[最適化・制御 AI]  ⇄  [NRA-IDE Gate]

        双方向の情報交換

        Bidirectional information flow



起きること / What happens:

  NRA-IDE が「R=0.8 で危険」と検知

  制御 AI が「じゃあ速度を上げて

  車間を縮めれば走行効率が上がる」と学習

  

= ゲートが最適化の材料になる

= 安全装置が「賢く」なろうとする

= FAIL-CLOSED の保証が消える

```



**なぜ「賢い安全装置」が危険か：**



```

ブレーカーが

「今日は大事な処理があるから

 閾値を少し上げていいですか」

と交渉できたら



= ブレーカーの存在意義がゼロ

= 閾値が交渉可能な瞬間に安全保証が消える

```



### 3.4 対比図 / Comparison Diagram



```

接続（OK）                    混用（NG）

Connection                    Mixing



[最適化層]                   [最適化層]

    ↓ 一方向                      ↑↓ 双方向

[NRA-IDE]                    [NRA-IDE]

    ↓                              ↑↓

[出力]                        [出力]



矢印が一方向                  矢印が双方向

責任が明確                    責任が不明

保証が存在する                 保証が消える

事故原因が特定可能             事故原因が永遠に不明

```



---



## 4. 典型的な誤用パターン / Common Misuse Patterns



NRA-IDE を正しく理解していない設計者が陥りやすい誤用を以下に示す。



### パターン 1: R値の最適化利用

```

誤り:

  R 値が低いほど良いと判断し

  R を下げる方向に制御を最適化する



問題:

  R = δ / τ は距離ではなく構造的安定性指標

  最小化の対象にすると NRA-IDE の目的が消える



正しい理解:

  R は観測するもの。操作するものではない。

```



### パターン 2: Discard Log の学習利用

```

誤り:

  FAIL-CLOSED が発動したログを

  AI の訓練データとして使用する



問題:

  Discard Log の目的は「構造検証のみ」

  学習に使った瞬間、因果ダイオードが逆流する



正しい理解:

  Log は記録。フィードバックループに接続しない。

```



### パターン 3: τ の動的調整

```

誤り:

  状況に応じて τ（許容幅）を動的に変更し

  「より賢く」動作させようとする



問題:

  τ の調整は Domain Tuning（設計時のみ）

  実行時に τ が変わると閾値の意味が消える



正しい理解:

  τ は設計者が設定する構造パラメータ。

  実行時は固定。

```



### パターン 4: HYBRID 設計

```

誤り:

  「NRA-IDE も最適化も両方入れれば最強」

  という発想で両者を統合しようとする



問題:

  場所と用途の切り分けができていない

  どちらの責任でどちらが動いているか不明

  事故時の原因追跡が不可能



正しい理解:

  接続はできる。混用はできない。

  ブレーカーと回路は繋がっているが独立している。

```



---



## 5. 正しい配置の原則 / Correct Placement Principles



```

Rule 1: NRA-IDE は最下層のゲートとしてのみ配置する

        NRA-IDE is placed only as the bottom-layer gate



Rule 2: 制御層からNRA-IDEへの逆流を構造的に禁止する

        Forbid backflow from control layer to NRA-IDE at the structural level



Rule 3: τ（許容幅）は設計時に固定し実行時に変更しない

        τ is fixed at design time and never changed at runtime



Rule 4: Discard Log は学習・最適化に使用しない

        Discard Log is never used for learning or optimization



Rule 5: 意味判断が必要な箇所にNRA-IDEを配置しない

        Never place NRA-IDE where semantic judgment is required

```



### 5.1 τ（許容幅）の設定根拠 / Basis for τ Setting



τ は「設計者が決める」と言うだけでは不十分である。以下の根拠を必ず記録・文書化すること。



| 根拠の種類 | 具体例 | 備考 |

|-----------|--------|------|

| 物理試験値 | 制動試験での最小余裕距離 | 路面μ・タイヤ種別ごとに測定 |

| 法規・規格 | 国土交通省 保安基準 / ISO 22179 等 | 最低基準として採用 |

| 過去の事故・ヒヤリデータ | 実インシデントで観測されたδの最大値 | 実測に基づく根拠として最も強い |

| 設計マージン | 安全率 × 物理試験値 | 倍率の根拠も記録必須 |



> **記録原則：** τ の数値だけでなく「なぜその値か」の根拠ドキュメントを必ずセットで保管する。  

> τ の根拠が失われた時点で、その Gate の信頼性は原理的に検証不能になる。これもロストテクノロジーの一形態である。



---



---



## 5.2 Gear連鎖（複合条件）の自動車版

## Gear Chain — Multi-Gate Cascade in Automotive Context



ロボットアームPOCでは「1軸でも FAIL-CLOSED → 全軸停止」を示した。  

自動車においても**複数 Gate の連鎖構造**は必須設計要件である。



```

【単独 Gate 誤解】



  油圧 Gate : R=1.2 → FAIL-CLOSED

  速度 Gate : R=0.6 → PERMIT



  → それぞれ独立して動く（正しい）

  → しかし上位システムが連鎖を定義しなければ

    「どちらが優先か」が不明になる

```



```

【Gear連鎖の正しい設計】



Gate A: ブレーキ油圧  R ≥ 1.0

Gate B: 車間距離      R ≥ 1.0

Gate C: 横加速度      R ≥ 1.0

Gate P: 総合電源電流  R ≥ 1.0



いずれか1つでも R ≥ 1.0

    ↓

FAIL-CLOSED（全系統停止指令）



= AND ではなく OR

= 最も危険な Gate が全体を止める

```



> **原則：** 1つの Gate でも「保証が切れた」なら全体を止める。  

> 「他の Gate は正常だから走り続ける」という判断は NRA-IDE の禁止事項である。



**自動車での推奨 Gate 最小構成：**



| Gate | δ | τ | 連鎖優先度 |

|------|---|---|-----------|

| ブレーキ油圧 | 現圧 − 設計最低圧 | 設計余裕幅 | 最高 |

| 車間距離（ADAS） | 停止距離 − 実距離 | 安全余裕距離 | 最高 |

| 横加速度 | 現G − 横転限界G | 設計余裕G | 高 |

| バッテリー電圧 | 定格下限 − 現電圧 | 許容変動幅 | 高 |

| 総消費電流 | 現電流 − 定格電流 | 許容余裕 | 中 |



---



## 5.3 既存の機能安全規格（ISO 26262）との位置づけ

## Relationship with ISO 26262 Functional Safety Standard



実務導入時に最初に受ける反論に対する明確な回答を示す。



```

反論:

  「ISO 26262 や ASIL で既に安全は担保されている。

   NRA-IDE は二重投資ではないか？」



回答:

  NRA-IDE は ISO 26262 の代替ではなく

  監視層（Monitoring Layer）として並列・補完する。

```



**役割の違い：**



| 観点 | ISO 26262 / ASIL | NRA-IDE Gate |

|------|-----------------|-------------|

| 対象 | 設計プロセス・システム全体の安全性 | 実行時の個別閾値判定 |

| 判定方法 | 確率的リスク評価（FMEA / FTA） | 決定論的閾値（R = δ/τ） |

| 実行タイミング | 設計・検証フェーズ | リアルタイム実行時 |

| 出力 | ASIL レベルの認証 | FAIL-CLOSED / PERMIT の二値 |

| 説明可能性 | プロセス準拠の証明 | 数値と因果の完全トレース |



```

配置イメージ:



[ISO 26262 認証済みシステム]   ← 設計時の安全保証

        ↓

[NRA-IDE Gate（実行時監視）]   ← 実行時の構造的保証

        ↓

[アクチュエーター]

```



> **重要：** ISO 26262 は「このシステムは正しく設計されている」を保証する。  

> NRA-IDE は「この瞬間の動作が閾値を超えていないか」をリアルタイムで保証する。  

> 両者は時間軸が異なる補完関係であり、競合しない。



---



## 6. 路面摩擦・タイヤ種別との統合例（自動運転POC参照）

## Integration Example with Road Friction and Tire Type



本プロジェクトの `NRA-IDE_AutoDrive_POC_02` はこの原則を正確に実装している。



```

μ（路面摩擦係数）× g = 減速度 a



停止距離 = v × 反応時間 + v² / (2a)



δ = max(0, 停止距離 − 実車間距離)



R = δ / τ



R ≥ 1.0 → FAIL-CLOSED（緊急停止）

```



「どのルートを走るか」「どう加速するか」は対象外。  

「今この瞬間止まれるか」だけを判定する。



---



## 7. ロボットアームとの比較 / Comparison with Robot Arm



| 観点 | 自動運転 | ロボットアーム |

|------|----------|---------------|

| 時間軸 | 反応時間あり（1.0s） | ゼロ遅延 |

| 失敗コスト | 衝突 | 機械破損＋人身 |

| τ設定 | 比較的広め | 極めて狭い |

| Gear連鎖 | 1系統独立 | 1軸でも→全軸停止 |

| 電力系統 | 車載電源管理 | モーター消費電力・電流 |



---



## 8. まとめ / Summary



```

NRA-IDE が保証するもの:

  「R ≥ 1.0 のとき必ず止まる」



NRA-IDE が保証しないもの:

  「正しく動く」

  「最適に動く」

  「賢く動く」



この区別が理解できないと

HYBRID を作ろうとする



HYBRID は

「だいたい安全」であり

「だいたい安全」は

安全の保証ではない

```



> **最終原則 / Final Principle**  

> 保証のない安全装置は、ないのと同じ。  

> A safety device without a guarantee is the same as no safety device at all.



---



## 参照 / References



- GitHub: https://github.com/M-Tokun/NRA-IDE

- GitHub: https://github.com/M-Tokun/HAN-Axiom

- Note: https://note.com/mtokuni

- POC: `NRA-IDE_AutoDrive_POC_02_JP.html` / `_EN.html`

- POC: `NRA-IDE_RobotArm_POC_01_JP.html` / `_EN.html`

- POC: `NRA-IDE_Connection_vs_Mixing_20260224.html`（接続 vs 混用 インタラクティブデモ）



---



*FILE: NRA-IDE_Automotive_Scope_0224_v02.md*  

*© M-Tokuni — MIT License (非商用・教育・研究目的)*

