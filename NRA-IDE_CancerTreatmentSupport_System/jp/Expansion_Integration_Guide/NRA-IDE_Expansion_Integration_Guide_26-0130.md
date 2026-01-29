# NRA-IDE 拡張実装パッケージ統合説明書
**生成日時:** 2026-01-30 05:30


---

## 📦 Package 概要

```
NRA-IDE_Expansion_Packages/
├── 1_Testbench_Parametric_Sweep_26-0130.v
│   └── 機能: 全パラメータ空間の総当たり探索
│       入力: Stiffness × Diameter × Pressure
│       出力: CSV統計ファイル + 最悪ケース抽出
│
├── 2_BioCalibrator_TypeB_Collective_26-0130.v
│   └── 機能: 集団力学（ジャミング）対応
│       対象: 子宮頸癌など「集団で押す」タイプ
│       計算: F = N × F_single × (1 + α√N)
│
└── 3_Clinical_Data_Pipeline_26-0130.py
    └── 機能: 病院DB → FPGA → レポート生成
        特徴: シリアル通信 + 安全マップ可視化
```

---

## 🎯 Package 1 詳細: パラメトリックスイープ

### **実装内容**
```
Parameter Space: 3D Grid Search
┌─────────────────────────────────┐
│ Stiffness: 0.1~2.0 kPa (Step 0.1)│
│ Diameter:  8~25 μm (Step 1.0)    │
│ Pressure:  100~1000 Pa (Step 50) │
└─────────────────────────────────┘
         ↓ 総当たり探索
┌─────────────────────────────────┐
│ Total Cases: ~20×18×19 = 6,840  │
│ 各条件で最小ブースト値を抽出    │
└─────────────────────────────────┘
```

### **出力ファイル**
- `calibration_results_26-0130.csv`
  ```csv
  Stiffness_kPa,Diameter_um,Pressure_Pa,DrugBoost_kPa
  0.100,8.0,100,0.012
  0.100,8.0,150,0.045
  ...
  2.000,25.0,1000,8.523
  ```

### **統計情報**
- 最大必要ブースト値（Max Boost Required）
- 最小必要ブースト値（Min Boost Required）
- 失敗ケース数（10 kPa超過で解なし）

### **使用方法**
```bash
# Verilogシミュレータ（Icarus Verilog等）
iverilog -o sweep_sim \
    BioCalibrator_Core_Logic_26-0130.v \
    Testbench_Parametric_Sweep_26-0130.v

vvp sweep_sim
# → calibration_results_26-0130.csv 生成
```

---

## 🎯 Package 2 詳細: Type B集団力学

### **物理モデル**
```
Type A (単体細胞) vs Type B (集団)

Type A:                Type B:
   ●  → Force F           ●●●
                          ●●● → Force ≈ 22.5F
                          ●●●

集団効果:
F_collective = N × F_individual × (1 + α × √N)

例: N=9, α=0.5
→ F = 9F × (1 + 0.5×3) = 9F × 2.5 = 22.5F
```

### **新規入力パラメータ**
```verilog
input wire [7:0] i_cell_count;         // 1~255個
input wire [7:0] i_cooperation_alpha;  // 協調係数 (Q4.4)
```

### **√N実装**
```verilog
// ハードウェアフレンドリーなルックアップテーブル
assign w_sqrt_N = (i_cell_count <= 4)  ? 2 :
                  (i_cell_count <= 9)  ? 3 :
                  (i_cell_count <= 16) ? 4 :
                  (i_cell_count <= 25) ? 5 : ...;
```

### **使用方法**
```verilog
// TypeAとTypeBの切り替え例
module Cancer_Treatment_Selector (
    input wire i_cancer_type, // 0=TypeA, 1=TypeB
    // ... 他のパラメータ
    output wire o_is_jammed
);
    wire o_jammed_A, o_jammed_B;
    
    BioCalibrator_Core_Logic typeA_module (...);
    BioCalibrator_TypeB_Collective typeB_module (...);
    
    assign o_is_jammed = i_cancer_type ? o_jammed_B : o_jammed_A;
endmodule
```

---

## 🎯 Package 3 詳細: 臨床データパイプライン

### **システムアーキテクチャ**
```
┌──────────────────┐
│ 病院設備         │
│ - 超音波診断装置 │
│ - 血圧計         │
│ - 病理検査       │
└────────┬─────────┘
         ↓
┌────────────────────┐
│ Python Validator   │
│ - 単位変換         │
│ - Q8.8エンコード   │
└────────┬───────────┘
         ↓
┌────────────────────┐
│ FPGA Interface     │
│ (UART/Serial通信)  │
└────────┬───────────┘
         ↓
┌────────────────────┐
│ Bio-Calibrator     │
│ → 適合値算出       │
└────────┬───────────┘
         ↓
┌────────────────────┐
│ Report Generator   │
│ - テキストレポート │
│ - 安全マップ画像   │
└────────────────────┘
```

### **通信プロトコル**
```python
# Host → FPGA (ASCII)
"STIFF:0x00CC,DIAM:0x0F00,PRESS:0x3F90\n"

# FPGA → Host
"BOOST:0x0B4D\n"  # = +2.852 kPa
```

### **Q8.8固定小数点エンコード**
```
例: 2.5 kPa をエンコード
→ 2.5 × 256 = 640 (10進) = 0x0280 (16進)

┌────────┬────────┐
│ 0x02   │ 0x80   │
│ Integer│Fraction│
│   2    │  0.5   │
└────────┴────────┘
```

### **出力例**
```
Report_{PatientID}_26-0130.txt
SafetyMap_{PatientID}_26-0130.png

[レポート内容]
╔═══════════════════════════════════╗
║  NRA-IDE Clinical Report          ║
╚═══════════════════════════════════╝
Patient: P12345
Measured:
  - Stiffness: 0.8 kPa
  - Pressure: 120 mmHg

★ Recommended: +2.852 kPa
```

### **使用方法**
```python
# 患者データ準備
patient = {
    'patient_id': 'P12345',
    'tumor_stiffness': 0.8,
    'tumor_diameter': 15.0,
    'blood_pressure': 120
}

# パイプライン実行
validator = PatientDataValidator()
fpga = FPGAInterface()
reporter = ClinicalReportGenerator()

encoded = validator.encode_patient_data(patient)
boost = fpga.query_calibration(encoded)
report = reporter.generate_report(patient, boost)
reporter.plot_safety_map(patient, boost, "map.png")
```

---

## 🔗 3パッケージの統合運用

### **完全ワークフロー**
```
[初期キャリブレーション]
1. Testbench Parametric Sweep 実行
   → 全パラメータ空間のマップ作成
   → CSV統計ファイル保存

[臨床運用開始]
2. 患者測定データ取得
   → Clinical Data Pipeline 起動
   → Q8.8エンコード

3. FPGA照会
   → Type A or Type B モジュール選択
   → 最適ブースト値取得

4. レポート生成
   → テキストレポート
   → 安全マップ可視化
   → 医師へ提示
```

### **ASCII統合図**
```
┌─────────────────────────────────────────────────────┐
│              NRA-IDE Complete System                │
└─────────────────────────────────────────────────────┘
         │
         ├─ [事前準備] Parametric Sweep
         │   └→ 全空間マップ生成（CSV）
         │
         ├─ [臨床適用] Clinical Pipeline
         │   ├→ 患者データ取得
         │   ├→ Validator → Q8.8変換
         │   └→ FPGA通信（UART）
         │
         └─ [FPGA判定] Type A/B Module
             ├→ Type A: 単体硬化
             ├→ Type B: 集団ジャミング
             └→ 最適ブースト出力
                 │
                 └→ Report Generator
                     ├→ テキストレポート
                     └→ 安全マップPNG
```

---

## 📋 ファイル一覧

| ファイル名 | 役割 | 出力 |
|-----------|------|------|
| `Testbench_Parametric_Sweep_26-0130.v` | 全パラメータ探索 | CSV統計 |
| `BioCalibrator_TypeB_Collective_26-0130.v` | 集団力学対応 | FPGA回路 |
| `Clinical_Data_Pipeline_26-0130.py` | 病院連携 | レポート+PNG |

---
