# NRA-IDE AUTOSAR 統合パターン
## AUTOSAR Integration Patterns

**FILE: NRA-IDE_AUTOSAR_Integration_0224_v02.md**  
**Author: M-Tokuni / KEN**  
**Version: 0.2**  
**Date: 2026-02-24**  
**変更点 v0.2:** ポート禁止粒度の修正（禁止すべきは「方向」ではなく「目的」）  
**依存文書 / Depends on:**  
- `NRA-IDE_Automotive_Scope_0224_v02.md`  
- `NRA-IDE_OTA_Gate_Verification_0224_v01.md`

---

## 0. 本文書の目的 / Purpose

本文書は NRA-IDE Gate を AUTOSAR（AUTomotive Open System ARchitecture）環境に  
統合する際の**配置・ポート定義・実装制約・τ 保護方法**を定義する。

AUTOSAR には2系統が存在し、NRA-IDE の配置戦略が異なる。

```
Classic Platform   → ECU 組み込み・リアルタイム制御
Adaptive Platform  → 高性能 ECU・自動運転・OTA 対応
```

> **前提原則 / Prerequisite**  
> AUTOSAR の層構造は NRA-IDE の「接続（OK）・混用（NG）」原則と  
> 構造的に整合する。層の境界が Gate の境界になる。

---

## 1. AUTOSAR における NRA-IDE の位置づけ
## Positioning NRA-IDE within AUTOSAR

### 1.1 Classic Platform における配置

```
┌─────────────────────────────────────┐
│  Application Layer                   │
│  ┌─────────────┐  ┌──────────────┐  │
│  │ 制御 SWC     │  │ NRA-IDE Gate │  │
│  │ Control SWC  │  │ SWC          │  │ ← Gate はここに配置
│  └──────┬──────┘  └──────┬───────┘  │
│         │  RTE           │           │
│  ┌──────▼────────────────▼───────┐  │
│  │  RTE（Runtime Environment）   │  │ ← ポート経由で接続
│  └──────────────┬────────────────┘  │
└─────────────────┼───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│  BSW（Basic Software）               │
│  COM / MCAL / OS / NvM / WDG        │ ← τ は NvM に格納
└─────────────────────────────────────┘
```

**Gate SWC の役割：**
- センサー値を R-Port で受信（読み取り専用）
- R = δ / τ を計算
- R ≥ 1.0 → FAIL-CLOSED 指令を P-Port で送信
- 制御 SWC からの書き込みを構造的に受け付けない

### 1.2 Adaptive Platform における配置

```
┌────────────────────────────────────────┐
│  Adaptive Applications                  │
│  ┌──────────────┐  ┌────────────────┐  │
│  │ 自動運転 AA   │  │ NRA-IDE Gate   │  │
│  │ Autonomy App │  │ Adaptive App   │  │ ← 独立した AA として配置
│  └──────┬───────┘  └───────┬────────┘  │
└─────────┼──────────────────┼───────────┘
          │  ARA（AUTOSAR    │
          │  Runtime for     │
┌─────────▼──────────────────▼───────────┐
│  Adaptive）                             │
│  Service Interface / Communication     │ ← サービス経由で接続
│  Execution Management / State Manager  │
└────────────────────────────────────────┘
```

**Adaptive Application としての Gate の特徴：**
- Service として登録、他の AA からは Read-Only でアクセス
- Execution Management による起動・停止管理
- State Manager との連携で FAIL-CLOSED 状態を伝播

---

## 2. ポート定義 / Port Definitions

### 2.1 Classic Platform — SWC ポート設計

```
NRA-IDE Gate SWC
┌────────────────────────────────────┐
│                                    │
│  入力 R-Port（受信専用）            │
│  ├─ SensorData_SpeedKmh   [float] │ ← 速度
│  ├─ SensorData_DistanceM  [float] │ ← 車間距離
│  ├─ SensorData_TorqueNm   [float] │ ← トルク（ロボットアーム等）
│  └─ SensorData_PowerW     [float] │ ← 消費電力
│                                    │
│  出力 P-Port（送信専用）            │
│  ├─ GateDecision_R        [float] │ ← R 値（外部から読み取り可）
│  ├─ GateDecision_Zone     [uint8] │ ← Zone A/B/C/D（外部から読み取り可）
│  ├─ GateDecision_FailCmd  [bool]  │ ← FAIL-CLOSED 指令
│  └─ GateDecision_PrevR    [float] │ ← 前周期 R 値（時系列継続用）
│                                    │
│  【書き込み禁止領域】               │
│  ✗ τ への外部書き込みポートは存在しない         │
│  ✗ Gate ロジックへの外部書き込みは存在しない    │
│  ✓ R 値・Zone・状態の読み取りは許可            │
└────────────────────────────────────┘
```

**ポート接続ルール（v0.2 修正版）：**

> **原則：禁止すべきは「方向」ではなく「目的」**  
> τ・ロジックへの**書き込み**は禁止。R値・状態の**読み取り**は許可。

| 接続 | 方向 | 許可 / 禁止 | 理由 |
|------|------|------------|------|
| センサー SWC → Gate R-Port | 書き込み | ✓ 許可 | センサー値の受信は必須 |
| Gate P-Port → アクチュエーター SWC | 書き込み | ✓ 許可 | FAIL-CLOSED 指令の送信 |
| Gate P-Port → 制御 SWC | 読み取り | ✓ 許可 | R値・Zone の観測は問題なし |
| Gate P-Port → OBD 診断 | 読み取り | ✓ 許可 | 診断に必要・推奨 |
| Gate 前周期R → Gate 今周期計算 | 内部時系列 | ✓ 許可 | 逆流ではなく時系列継続 |
| 制御 SWC → Gate τ 値 | **書き込み** | ✗ **禁止** | 保証の破壊 |
| 制御 SWC → Gate ロジック | **書き込み** | ✗ **禁止** | 保証の破壊 |
| 開発ツール → Gate τ 値 | **書き込み** | △ **条件付き** | 開発環境のみ・NvM経由・ログ必須 |

### 2.2 Adaptive Platform — Service Interface 設計

```
NRA-IDE Gate Service
  Service Name:  nra_ide.gate.v1
  Instance ID:   domain固有（例: automotive.adas.gate）

  Provided Methods（外部から呼び出し可能）:
    GetGateStatus() → { R: float, zone: enum, failCmd: bool }
    GetTauValue()   → { tau: float, basis: string }  ← 読み取り専用
    GetGateHistory() → { prevR: float[], timestamps: uint64[] } ← 診断用

  Subscribed Events（Gate が受信）:
    SensorUpdate → { speed, distance, torque, power }

  書き込み系メソッドの方針:
    SetTauValue()   ← 本番環境では存在しない
                       開発環境のみ・NvM 経由・ログ必須で条件付き許可
    SetGateLogic()  ← 存在しない（全環境で禁止）
```

### 2.3 開発環境での条件付き τ 書き込み許可
### Conditional τ Write Permission in Development Environment

本番環境では τ への書き込みは構造的に禁止されるが、  
キャリブレーション・デバッグ・出荷前調整の現実的な需要を考慮し、  
**開発環境に限り条件付きで許可する。**

```
【条件付き許可の要件】

環境条件:
  □ 開発専用ビルド（DEVELOPMENT_BUILD フラグが有効）
  □ 本番 ECU フラッシュ前のステージング環境のみ
  □ 本番フラッシュ時に開発専用ポートをコンパイル除外

手順条件:
  □ NvM Manager 経由のみ（直接メモリ書き込み禁止）
  □ 変更前後の τ 値をログに記録
  □ 変更根拠（測定値・試験レポート番号）を同時記録
  □ 承認者の電子署名が必要

本番への昇格:
  □ 開発環境で確定した τ 値は OTA クラス A プロセスで本番に反映
  □ 開発環境での変更を直接本番に適用することは禁止
```

> **境界の明確化：**  
> 「開発で触れる = 本番でも触れる」ではない。  
> 開発環境の条件付き許可は本番環境の禁止を緩めるものではない。

---

## 3. 実装上の制約 / Implementation Constraints

### 3.1 OS タスク優先度

```
【Classic Platform — OSEK/AUTOSAR OS】

タスク優先度（高 → 低）:
  Priority 1（最高）: NRA-IDE Gate タスク  ← ここ
  Priority 2        : アクチュエーター制御
  Priority 3        : 制御 AI / 最適化
  Priority 4        : ログ・通信
  Priority 5（最低）: UI・表示

理由:
  Gate が制御 AI に CPU を奪われると
  FAIL-CLOSED の応答遅延が発生する
  Gate は常に最優先で実行される必要がある
```

### 3.2 実行周期（タスク周期）

```
Gate タスクの実行周期:
  推奨: 1ms 以下（自動車安全領域）
  最大: 10ms（これを超えると応答遅延が危険）

  理由:
    R ≥ 1.0 を検知してから FAIL-CLOSED 指令を
    出すまでの時間が長いほど危険が増す

固定周期の義務:
  Gate のタスク周期は実行時に変更禁止
  「負荷が高いから Gate の周期を下げる」は禁止
  → これは Gate の弱体化であり混用に相当する
```

### 3.3 メモリ保護（MPU 設定）

```
【Classic Platform — MemMap / MPU 設定】

Gate SWC のメモリ領域:
  .gate_config セクション:
    τ 値の格納領域
    アクセス権: Gate SWC のみ READ/WRITE
               他 SWC は READ 禁止（存在を知らせない）

  .gate_logic セクション:
    R 計算ロジック
    アクセス権: READ-ONLY（自己書き換え禁止）

  .gate_output セクション:
    R 値・Zone・FAIL-CLOSED 指令
    アクセス権: Gate SWC が WRITE
               他 SWC は READ ONLY

MPU 設定例（AUTOSAR MemMap）:
  #pragma ghs section data=".gate_config"
  static volatile float32 tau_value = 8.0f;  /* τ 固定値 */
  #pragma ghs section

  /* τ への外部書き込みは MPU ハードウェアで遮断 */
```

---

## 4. τ の保護方法 / τ Protection Mechanism

τ の無断変更は Gate の保証を破壊する最大のリスクである。  
AUTOSAR では以下の3層で τ を保護する。

### 4.1 NvM（不揮発メモリ）への格納

```
【Classic Platform — NvM 設定】

NvM ブロック定義:
  Block ID:       NRA_GATE_TAU_BLOCK
  サイズ:         4 bytes（float32）
  アクセス権:     読み取り: Gate SWC のみ
                  書き込み: NvM Manager 経由のみ
                            （OTA 更新クラス A のプロセスのみ許可）
  CRC チェック:   有効（破損検出）
  書き込みログ:   有効（変更履歴を NvM に記録）

起動時シーケンス:
  1. NvM から τ 値を読み込む
  2. CRC 検証
  3. 値が設計範囲内か確認（範囲外 → FAIL-CLOSED で起動禁止）
  4. Gate 初期化完了
```

### 4.2 ソフトウェア的保護

```
C 実装例（AUTOSAR Classic SWC）:

/* FILE: NRA_IDE_Gate.c  2026-02-24 */

/* τ は const で宣言 — コンパイル時点で書き込み禁止 */
/* 実行時の変更は構造的に不可能 */
static const float32 NRA_GATE_TAU = 8.0f;  /* 単位: m  根拠: NvM から読込 */

/* R 計算関数 — 入力のみ受け取り、τ は内部定数を使用 */
static float32 NRA_Gate_ComputeR(float32 delta)
{
    /* NRA_GATE_TAU は外部から変更不可 */
    if (NRA_GATE_TAU <= 0.0f)
    {
        /* τ 異常 → 即時 FAIL-CLOSED */
        return NRA_GATE_R_MAX;
    }
    return delta / NRA_GATE_TAU;
}

/* Gate メイン関数 — 最高優先度タスクから呼び出し */
void NRA_Gate_MainFunction(void)
{
    float32 speed    = Rte_IRead_Gate_SensorData_SpeedKmh();
    float32 distance = Rte_IRead_Gate_SensorData_DistanceM();
    float32 delta    = NRA_Gate_ComputeDelta(speed, distance);
    float32 R        = NRA_Gate_ComputeR(delta);

    /* FAIL-CLOSED 判定 */
    if (R >= 1.0f)
    {
        Rte_IWrite_Gate_GateDecision_FailCmd(TRUE);
    }
    else
    {
        Rte_IWrite_Gate_GateDecision_FailCmd(FALSE);
    }

    Rte_IWrite_Gate_GateDecision_R(R);
}
```

### 4.3 OTA 更新との連動

`NRA-IDE_OTA_Gate_Verification_0224_v01.md` のクラス A プロセスを通過した場合のみ  
τ の NvM 書き込みが許可される。

```
τ 更新シーケンス（OTA クラス A）:

  OTA Manager
      ↓ 更新パッケージ（τ 新値 + 根拠ハッシュ）
  Gate 検証プロセス（ステージング確認済み）
      ↓ 承認済みフラグ
  NvM Manager
      ↓ NRA_GATE_TAU_BLOCK への書き込み
  Gate SWC 再起動
      ↓ NvM から新 τ 値を読み込み
  Gate 再初期化完了

  承認済みフラグなしの NvM 書き込み → MPU がハードウェアで遮断
```

---

## 5. Watchdog との連携 / Watchdog Integration

Gate が停止した場合（デッドロック・例外等）の安全動作を定義する。

```
【Classic Platform — WDG Manager との連携】

Gate タスクは毎周期 WDG にアライブ信号を送信:
  NRA_Gate_MainFunction() の末尾で
  Wdg_SetTriggerCondition(NRA_GATE_WDG_CYCLE);

WDG がタイムアウトを検知した場合:
  → ハードウェアリセット OR
  → FAIL-CLOSED 指令をハードウェアレベルで強制送信

理由:
  Gate が止まった = Gate が存在しない
  Gate が存在しない = 保証がない
  → FAIL-CLOSED と同等の危険状態
  → 止まったまま走行継続は禁止
```

---

## 6. Classic vs Adaptive 比較
## Classic vs Adaptive — Comparison for NRA-IDE

| 観点 | Classic Platform | Adaptive Platform |
|------|-----------------|------------------|
| Gate 形態 | SWC（ソフトウェアコンポーネント） | Adaptive Application |
| 接続方式 | RTE ポート | ARA Service Interface |
| τ 保護 | NvM + MPU + const 宣言 | Persistent Storage + Access Control |
| タスク管理 | OSEK/AUTOSAR OS（固定周期） | Execution Management（動的だが Gate は固定） |
| OTA 対応 | NvM Manager 経由で制御 | Update & Config Management |
| 推奨用途 | パワートレイン・ブレーキ系 | ADAS・自動運転判断系 |
| リアルタイム性 | 1ms 以下対応 | 数 ms 程度（Classic より低い） |

> **選択基準：**  
> ブレーキ・エンジン等の安全クリティカルな物理系 → Classic  
> ADAS・自動運転等の判断系 → Adaptive  
> 両系統が混在する場合 → Gate を Classic に配置し Adaptive へ FAIL-CLOSED 指令を伝達

---

## 7. まとめ / Summary

```
AUTOSAR における NRA-IDE 統合の原則（v0.2 修正版）:

禁止すべきは「方向」ではなく「目的」:
  τ・ロジックへの書き込み       → 全環境で禁止
  R値・状態の読み取り           → 全環境で許可（診断に必要）
  開発ツールからの τ 書き込み   → 開発環境のみ条件付き許可
  Gate 前周期R の内部利用       → 許可（逆流ではなく時系列継続）

Rule A: Gate は独立した SWC / Adaptive Application として配置
        他の SWC と一体化させない

Rule B: τ・Gate ロジックへの書き込みポートは本番環境に存在させない
        R値・状態の読み取りは許可する（観測は歓迎）

Rule C: Gate タスクは最高優先度
        負荷状況に関わらず周期を変更しない

Rule D: τ は NvM + MPU + const の3層で保護
        本番環境での変更はハードウェアレベルで禁止
        開発環境での変更は NvM 経由・ログ必須

Rule E: Gate が停止したら Watchdog が FAIL-CLOSED を代行
        「Gate が止まった状態での走行継続」は禁止

AUTOSAR の層構造は NRA-IDE の設計原則と整合する。
層の境界 = Gate の境界
τ・ロジックへの外部書き込み = 混用（NG）
R値の外部読み取り = 接続（OK）
```

---

## 参照 / References

- `NRA-IDE_Automotive_Scope_0224_v02.md` — 適用範囲定義書
- `NRA-IDE_OTA_Gate_Verification_0224_v01.md` — OTA 検証プロセス
- `NRA-IDE_AutoDrive_POC_02_JP.html` / `_EN.html` — 自動運転 Gate POC
- AUTOSAR Classic Platform Specification R22-11
- AUTOSAR Adaptive Platform Specification R22-11
- AUTOSAR SWS MemoryStack (NvM)
- ISO 26262: Road vehicles — Functional safety
- GitHub: https://github.com/M-Tokun/NRA-IDE

---

*FILE: NRA-IDE_AUTOSAR_Integration_0224_v02.md*  
*© M-Tokuni — MIT License (非商用・教育・研究目的)*
