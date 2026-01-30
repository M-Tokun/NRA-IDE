# NRA-IDE_System_Architecture_Protocol
### Phase 5: システムアーキテクチャ
* 対象読者: 医師 + エンジニア
* 作成日時: 2026-01-30 22:30


// ═══════════════════════════════════════════

// 0. この章で理解すること

// ═══════════════════════════════════════════

PURPOSE: {
    PREVIOUS_PHASE: "Phase 4で全変数・単位・命名規則を統一的に理解した";
    THIS_PHASE: "なぜFPGAなのか、システム全体の構造、計算資源要件を理解する";
    
    KEY_QUESTIONS: {
        Q1: "なぜGPU/CUDAではなくFPGAを選択したのか？";
        Q2: "患者データから結果までのデータフローは？";
        Q3: "総当たり探索は何回計算するのか？ 時間はかかるのか？";
        Q4: "Type A/B の切り替えはどう実装するのか？";
    }
}

// ═══════════════════════════════════════════
// 1. なぜFPGAか（ハードウェア選択の根拠）
// ═══════════════════════════════════════════
HARDWARE_SELECTION: WHY_FPGA {
    
    // ───────────────────────────────────────
    // 1-1. 選択肢の比較
    // ───────────────────────────────────────
    COMPARISON_TABLE: {
        HEADER: ["項目", "CPU", "GPU/CUDA", "FPGA"];
        
        ROW_FLEXIBILITY: {
            CPU: "◎ 何でもできる";
            GPU: "○ 並列計算得意";
            FPGA: "△ 専用計算のみ";
        };
        
        ROW_LATENCY: {
            CPU: "△ OSジッタあり（数ms）";
            GPU: "△ メモリ転送遅延（数百μs）";
            FPGA: "◎ ゼロレイテンシ（数十ns）";
        };
        
        ROW_PRECISION: {
            CPU: "○ 浮動小数点（丸め誤差）";
            GPU: "○ 浮動小数点（丸め誤差）";
            FPGA: "◎ 固定小数点（誤差ゼロ）";
        };
        
        ROW_DETERMINISM: {
            CPU: "× OS割り込みで不確定";
            GPU: "× スケジューラで不確定";
            FPGA: "◎ 完全決定論的";
        };
        
        ROW_POWER: {
            CPU: "△ 数十W";
            GPU: "× 数百W";
            FPGA: "◎ 数W";
        };
        
        ROW_COST: {
            CPU: "◎ 安い";
            GPU: "△ 高い";
            FPGA: "○ 中程度";
        };
    };
    
    // ───────────────────────────────────────
    // 1-2. FPGAが必要な理由
    // ───────────────────────────────────────
    FPGA_NECESSITY: {
        
        REASON_1_ZERO_LATENCY: {
            REQUIREMENT: "細胞1個の判定に、遅延ゼロが必要";
            
            WHY: {
                LIFE_STAKES: "細胞1個の通過 = 患者の転移リスク";
                NO_DELAY: "OSの割り込み待ちなど許されない";
                REAL_TIME: "測定→計算→結果を瞬時に完結";
            };
            
            CPU_GPU_PROBLEM: {
                OS_JITTER: {
                    PHENOMENON: "OSが『ちょっと待って、他の仕事もあるから』と割り込む";
                    DELAY: "数ミリ秒〜数十ミリ秒の不確定遅延";
                    MEDICAL_IMPACT: "手術室で待たされる = 許容不可";
                };
                
                MEMORY_TRANSFER: {
                    PHENOMENON: "GPU: CPU↔GPUメモリ間の転送";
                    DELAY: "数百マイクロ秒";
                    MEDICAL_IMPACT: "リアルタイム判定には遅すぎる";
                };
            };
            
            FPGA_SOLUTION: {
                MECHANISM: "レジスタ間直接転送";
                DELAY: "数十ナノ秒（OSなし、メモリなし）";
                ANALOGY: "リレー競技で、バトンを地面に置かず直接手渡し";
            };
        };
        
        REASON_2_FIXED_POINT: {
            REQUIREMENT: "丸め誤差ゼロの厳密計算";
            
            WHY: {
                LIFE_JUDGMENT: "SAFE/DANGERの境界は、0.1 kPa の差";
                NO_ERROR: "浮動小数点の丸め誤差（10⁻⁷程度）でも蓄積すれば致命的";
                GUARANTEE: "厳密な物理保証には、誤差ゼロが必須";
            };
            
            CPU_GPU_PROBLEM: {
                FLOATING_POINT: {
                    FORMAT: "IEEE 754 浮動小数点";
                    ERROR: "0.1 + 0.2 = 0.30000000000000004（誤差）";
                    ACCUMULATION: "数千回計算すると、誤差が無視できなくなる";
                };
            };
            
            FPGA_SOLUTION: {
                FORMAT: "Q8.8 固定小数点（16ビット整数）";
                ERROR: "ゼロ（整数演算のみ）";
                EXAMPLE: "2.5 kPa = 640（整数） → 誤差なし";
            };
        };
        
        REASON_3_DETERMINISM: {
            REQUIREMENT: "完全決定論的動作（再現性100%）";
            
            WHY: {
                MEDICAL_DEVICE: "医療機器認証には再現性が必須";
                AUDIT: "同じ入力 → 必ず同じ出力（検証可能）";
                TRUST: "医師が信頼できる根拠";
            };
            
            CPU_GPU_PROBLEM: {
                SCHEDULER: {
                    PHENOMENON: "OSのタスクスケジューラが動的に変化";
                    RESULT: "同じ入力でも、実行順序が変わる → 結果が微妙に変わる";
                    MEDICAL_IMPACT: "再現性なし → 認証不可";
                };
            };
            
            FPGA_SOLUTION: {
                MECHANISM: "OSなし、ハードウェア回路のみ";
                GUARANTEE: "同じ入力 → 必ず同じクロックサイクルで同じ出力";
                VERIFICATION: "回路図レベルで検証可能";
            };
        };
    };
    
    // ───────────────────────────────────────
    // 1-3. FPGAの制約と対策
    // ───────────────────────────────────────
    FPGA_LIMITATIONS: {
        
        LIMITATION_1_INFLEXIBILITY: {
            PROBLEM: "一度回路を焼くと、変更が困難";
            MITIGATION: {
                SOLUTION: "パラメータは外部から変更可能にする";
                EXAMPLE: "薬液量Boostは入力レジスタ経由で動的変更";
                FIXED_PART: "物理式（k·Δx + η·dv/dt）は回路に固定";
            };
        };
        
        LIMITATION_2_RESOURCE: {
            PROBLEM: "Logic Elementsに限りがある";
            MITIGATION: {
                SOLUTION: "パイプライン最適化、リソース共有";
                REQUIREMENT: "最小 10K Logic Elements（中規模FPGA）";
                EXAMPLE: "Intel Cyclone V, Xilinx Artix-7";
            };
        };
        
        LIMITATION_3_DEBUGGING: {
            PROBLEM: "CPUほどデバッグが容易ではない";
            MITIGATION: {
                SOLUTION: "Testbench（シミュレーション）で事前検証";
                TOOLS: "ModelSim, Icarus Verilog";
                STRATEGY: "実機実装前に、全ケースをシミュレーション";
            };
        };
    };
}

// ═══════════════════════════════════════════
// 2. システム全体のデータフロー
// ═══════════════════════════════════════════
SYSTEM_DATAFLOW: {
    
    // ───────────────────────────────────────
    // 2-1. 全体図（ASCII）
    // ───────────────────────────────────────
    ARCHITECTURE_DIAGRAM: {
        ASCII_ART: "
┌─────────────────────────────────────────────────────────┐
│                  Hospital Floor                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │Ultrasound│  │  BP Cuff │  │ Pathology│              │
│  │  (kPa)   │  │  (mmHg)  │  │  (μm)    │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       └─────────────┴──────────────┘                    │
└─────────────────────┼───────────────────────────────────┘
                      ↓
        ┌─────────────────────────┐
        │  Host Computer (PC)     │
        │  ┌───────────────────┐  │
        │  │ Python Validator  │  │  ← Phase 4 辞書で単位チェック
        │  │ - Range Check     │  │
        │  │ - Unit Convert    │  │
        │  │ - Q8.8 Encode     │  │
        │  └─────────┬─────────┘  │
        └────────────┼─────────────┘
                     ↓ UART/PCIe
        ┌─────────────────────────┐
        │  FPGA Bio-Calibrator    │
        │  ┌───────────────────┐  │
        │  │ Type A Module     │←─┼─ i_cell_stiffness
        │  │ (Jamming)         │  │   i_cell_diameter
        │  ├───────────────────┤  │   i_pore_size
        │  │ Type B Module     │  │   i_flow_dp
        │  │ (Collective)      │  │   i_drug_boost
        │  ├───────────────────┤  │
        │  │ Brute-Force       │  │
        │  │ Optimizer         │  │
        │  └─────────┬─────────┘  │
        └────────────┼─────────────┘
                     ↓ UART/PCIe
        ┌─────────────────────────┐
        │  Host Computer (PC)     │
        │  ┌───────────────────┐  │
        │  │ Report Generator  │  │
        │  │ - Text Report     │  │
        │  │ - Safety Map PNG  │  │
        │  └───────────────────┘  │
        └─────────────────────────┘
                     ↓
        ┌─────────────────────────┐
        │  Physician Workstation  │
        │  (Treatment Decision)   │
        └─────────────────────────┘
";
    };
    
    // ───────────────────────────────────────
    // 2-2. ステージ別の詳細
    // ───────────────────────────────────────
    STAGE_1_MEASUREMENT: {
        LOCATION: "Hospital Floor（病院検査室）";
        
        DEVICES: {
            ELASTOGRAPHY: {
                DEVICE: "超音波エラストグラフィ";
                MEASURES: "細胞硬度 i_cell_stiffness [kPa]";
                OUTPUT: "1.5 kPa";
            };
            
            ULTRASOUND: {
                DEVICE: "超音波画像診断";
                MEASURES: "細胞直径 i_cell_diameter [μm]";
                OUTPUT: "12.0 μm";
            };
            
            BP_CUFF: {
                DEVICE: "血圧計";
                MEASURES: "全身血圧 [mmHg]（参考値）";
                OUTPUT: "120 mmHg";
                NOTE: "局所圧差ではないので、あくまで参考";
            };
            
            PATHOLOGY: {
                DEVICE: "病理組織検査";
                MEASURES: "細胞数 i_cell_count（Type B用）";
                OUTPUT: "10 個";
            };
        };
        
        OUTPUT_FORMAT: {
            EXAMPLE: {
                STIFFNESS: "1.5 kPa";
                DIAMETER: "12.0 μm";
                PRESSURE_REF: "120 mmHg";
                CELL_COUNT: "10";
            };
        };
    };
    
    STAGE_2_VALIDATION: {
        LOCATION: "Host Computer（ホストPC）";
        
        RESPONSIBILITIES: {
            RANGE_CHECK: {
                ACTION: "Phase 4 辞書のRANGE_VALIDと照合";
                EXAMPLE: "stiffness 1.5 kPa は [0.1, 10.0] 内 → OK";
                IF_ERROR: "範囲外なら警告『測定値が異常です』";
            };
            
            UNIT_CONVERT: {
                ACTION: "SI単位に統一";
                EXAMPLE: "120 mmHg → 16.0 kPa（参考）";
                NOTE: "実際は局所圧差を別途測定するのが理想";
            };
            
            Q8_8_ENCODE: {
                ACTION: "FPGA用に固定小数点へ変換";
                EXAMPLE: "1.5 kPa → 0x0180 (384)";
                FORMULA: "Q8_8 = value × 256";
            };
        };
        
        OUTPUT_FORMAT: {
            PACKET: {
                i_cell_stiffness: "0x0180";
                i_cell_diameter: "0x0C00";
                i_pore_size: "0x0800"; // 固定値 8.0μm
                i_flow_dp: "0x0258"; // 600 Pa（仮定）
                i_drug_boost: "0x0000"; // 初期値0
            };
        };
    };
    
    STAGE_3_FPGA_COMPUTATION: {
        LOCATION: "FPGA Bio-Calibrator";
        
        INTERFACE: {
            INPUT: "UART または PCIe経由でパケット受信";
            PROTOCOL: "例: STIFF:0x0180,DIAM:0x0C00,... （ASCII形式）";
        };
        
        COMPUTATION: {
            TYPE_SELECTION: {
                IF_TYPE_A: "Jamming Module 起動";
                IF_TYPE_B: "Collective Module 起動";
                AUTO_SELECT: "病理データから自動判別（または医師が指定）";
            };
            
            BRUTE_FORCE: {
                LOOP: "i_drug_boost = 0 から開始";
                STEP: "0.01 kPa ずつ増加";
                CHECK: "各ステップで o_is_jammed を判定";
                TERMINATE: "SAFE になったら終了";
                RECORD: "その時のBoost値を記録";
            };
        };
        
        OUTPUT: {
            RESULT: "o_optimal_boost = 0x0B4D（例: 2.852 kPa）";
            PROTOCOL: "BOOST:0x0B4D （UART/PCIe経由でホストへ返送）";
        };
    };
    
    STAGE_4_REPORT_GENERATION: {
        LOCATION: "Host Computer（ホストPC）";
        
        RESPONSIBILITIES: {
            DECODE: {
                ACTION: "Q8.8 → 実数へ逆変換";
                EXAMPLE: "0x0B4D (2893) → 2893 / 256 = 11.3 kPa";
            };
            
            TEXT_REPORT: {
                GENERATE: "Phase 4 辞書の用語で臨床レポート作成";
                EXAMPLE: "
╔═══════════════════════════════════╗
║  NRA-IDE Clinical Report          ║
╚═══════════════════════════════════╝
Patient: P12345
Measured: Stiffness 1.5 kPa
★ Recommended Boost: +2.85 kPa
";
            };
            
            SAFETY_MAP: {
                GENERATE: "matplotlib で安全域可視化";
                OUTPUT: "SafetyMap_P12345.png";
            };
        };
    };
    
    STAGE_5_PHYSICIAN_DECISION: {
        LOCATION: "Physician Workstation（医師端末）";
        
        PHYSICIAN_REVIEW: {
            RECEIVE: "テキストレポート + 安全マップ画像";
            INTERPRET: "物理的根拠を理解";
            INTEGRATE: "臨床所見、患者背景と統合";
            DECIDE: "最終治療方針を決定";
            EXPLAIN: "患者に説明、同意取得";
        };
        
        GATE_AXIOM: {
            SYSTEM_ROLE: "物理的根拠の提示（ここまで）";
            PHYSICIAN_ROLE: "最終決定（ここから）";
            BOUNDARY: "ゲート公理で明確に分離";
        };
    };
}

// ═══════════════════════════════════════════
// 3. 計算資源要件（総当たり回数）
// ═══════════════════════════════════════════
COMPUTATIONAL_RESOURCES: {
    
    // ───────────────────────────────────────
    // 3-1. 総当たり計算回数の詳細
    // ───────────────────────────────────────
    BRUTE_FORCE_COMPLEXITY: {
        
        OUTER_LOOP_PARAMETER_SPACE: {
            STIFFNESS: {
                RANGE: "0.1 〜 2.0 kPa";
                STEP: "0.1 kPa";
                COUNT: 20;
                REASON: "患者の細胞硬度のばらつきを網羅";
            };
            
            DIAMETER: {
                RANGE: "8 〜 25 μm";
                STEP: "1.0 μm";
                COUNT: 18;
                REASON: "細胞サイズの個体差を網羅";
            };
            
            PRESSURE: {
                RANGE: "100 〜 1000 Pa";
                STEP: "50 Pa";
                COUNT: 19;
                REASON: "血流圧力の生理的範囲を網羅";
            };
            
            TOTAL_CASES: "20 × 18 × 19 = 6,840 ケース";
            
            MEANING: {
                WHAT: "患者が持ちうる『全ての可能な物理状態』を列挙";
                WHY: "最悪ケース（最も危険な組み合わせ）を見逃さないため";
            };
        };
        
        INNER_LOOP_BOOST_SEARCH: {
            BOOST_RANGE: "0.0 〜 10.0 kPa";
            BOOST_STEP: "0.01 kPa（Q8.8で 0x0003）";
            MAX_ITERATIONS: 1000; // 10.0 / 0.01 = 1000
            
            EARLY_TERMINATION: {
                CONDITION: "SAFE判定が出たら即終了";
                TYPICAL: "100〜200回で終了（平均150回と仮定）";
                REASON: "ほとんどのケースは、数kPa以下で封鎖できる";
            };
        };
        
        TOTAL_CALCULATIONS: {
            WORST_CASE: {
                VALUE: "6,840 × 1,000 = 6,840,000 回";
                SCENARIO: "全てのケースで10kPaまで探索";
                PROBABILITY: "ほぼ起きない（非現実的）";
            };
            
            TYPICAL_CASE: {
                VALUE: "6,840 × 150 = 1,026,000 回";
                SCENARIO: "平均150回で SAFE 到達";
                PROBABILITY: "実際の臨床でよくあるケース";
            };
            
            BEST_CASE: {
                VALUE: "6,840 × 10 = 68,400 回";
                SCENARIO: "ほとんど即座に SAFE";
                PROBABILITY: "細胞が既に硬い場合";
            };
        };
    };
    
    // ───────────────────────────────────────
    // 3-2. FPGA実行時間の見積もり
    // ───────────────────────────────────────
    FPGA_PERFORMANCE: {
        
        CLOCK_SPECIFICATION: {
            FREQUENCY: "100 MHz";
            PERIOD: "10 ns / cycle";
            JUSTIFICATION: "中規模FPGAで容易に達成可能";
        };
        
        PIPELINE_DESIGN: {
            DEPTH: "5 stage";
            
            STAGES: {
                STAGE_1: "変形量計算（Δx = D - d）";
                STAGE_2: "弾性力計算（k·Δx）";
                STAGE_3: "粘性力計算（η·dv/dt）";
                STAGE_4: "総合抵抗力（Elastic + Viscous）";
                STAGE_5: "比較判定（Resist > Pressure ?）";
            };
            
            THROUGHPUT: "1判定 / 5 cycles = 50 ns / 判定";
        };
        
        EXECUTION_TIME: {
            WORST_CASE: {
                CALCULATION: "6,840,000 × 50 ns = 342,000,000 ns = 342 ms";
                ASSESSMENT: "約0.3秒（十分速い）";
            };
            
            TYPICAL_CASE: {
                CALCULATION: "1,026,000 × 50 ns = 51,300,000 ns = 51.3 ms";
                ASSESSMENT: "約50ミリ秒（実用的）";
            };
            
            BEST_CASE: {
                CALCULATION: "68,400 × 50 ns = 3,420,000 ns = 3.42 ms";
                ASSESSMENT: "約3ミリ秒（瞬時）";
            };
        };
        
        CLINICAL_CONTEXT: {
            COMPARISON: {
                CT_SCAN: "数分〜数十分";
                BLOOD_TEST: "数時間";
                NRA_IDE: "数ミリ秒〜数十ミリ秒";
            };
            
            IMPLICATION: "検査結果が出た瞬間に、最適薬液量が分かる";
        };
    };
    
    // ───────────────────────────────────────
    // 3-3. 並列化による高速化
    // ───────────────────────────────────────
    PARALLEL_OPTIMIZATION: {
        
        STRATEGY: "外側ループ（パラメータ空間）を並列化";
        
        FPGA_UNITS: {
            COUNT: 16; // 並列実行ユニット
            PARTITION: "6,840 ケースを 16分割（428ケース/ユニット）";
        };
        
        SPEEDUP: {
            WORST_CASE: "342 ms / 16 = 21.4 ms";
            TYPICAL_CASE: "51.3 ms / 16 = 3.2 ms";
            
            ASSESSMENT: "典型的には 3〜5 ミリ秒で全探索完了";
        };
        
        RESOURCE_TRADEOFF: {
            BENEFIT: "16倍高速化";
            COST: "Logic Elements も 16倍必要";
            FEASIBILITY: "大規模FPGA（例: Xilinx Virtex-7）なら可能";
        };
    };
    
    // ───────────────────────────────────────
    // 3-4. メモリ要件
    // ───────────────────────────────────────
    MEMORY_REQUIREMENTS: {
        
        FPGA_INTERNAL: {
            REGISTERS_ONLY: {
                INPUT_REGS: "5変数 × 16bit = 80 bit";
                INTERMEDIATE: "10変数 × 32bit = 320 bit";
                OUTPUT_REGS: "2変数 × 16bit = 32 bit";
                TOTAL: "約500 bit（極小）";
            };
            
            NO_EXTERNAL_RAM: {
                STATEMENT: "外部DRAMは不要";
                REASON: "全てレジスタ内で完結";
                ADVANTAGE: "メモリアクセス遅延ゼロ";
            };
        };
        
        HOST_PC: {
            PYTHON_PROCESS: "数十MB（通常のPythonプログラム）";
            DATA_STORAGE: "患者データ + 結果 = 数KB / 患者";
        };
    };
    
    // ───────────────────────────────────────
    // 3-5. 消費電力
    // ───────────────────────────────────────
    POWER_CONSUMPTION: {
        
        FPGA_CHIP: {
            TYPICAL: "5 W 以下";
            COMPARISON: {
                GPU: "200〜400 W";
                ADVANTAGE: "FPGAは GPU の 1/40 の消費電力";
            };
        };
        
        SYSTEM_TOTAL: {
            FPGA_BOARD: "約10 W";
            HOST_PC: "約50 W";
            TOTAL: "約60 W";
            
            CLINICAL_IMPACT: "バッテリー駆動可能 → ポータブル機器化も視野";
        };
    };
}

// ═══════════════════════════════════════════
// 4. Type A/B 切り替え戦略
// ═══════════════════════════════════════════
TYPE_SELECTION_STRATEGY: {
    
    // ───────────────────────────────────────
    // 4-1. ハードウェア実装
    // ───────────────────────────────────────
    HARDWARE_ARCHITECTURE: {
        
        DUAL_MODULE: {
            MODULE_A: "Type A（Jamming）専用回路";
            MODULE_B: "Type B（Collective）専用回路";
            SELECTOR: "マルチプレクサ（MUX）で切り替え";
        };
        
        VERILOG_EXAMPLE: {
            CODE: "
module Cancer_Treatment_Selector (
    input wire i_cancer_type,  // 0=TypeA, 1=TypeB
    input wire [15:0] i_cell_stiffness,
    input wire [15:0] i_cell_diameter,
    // ... 他のパラメータ
    output wire o_is_jammed
);
    wire o_jammed_A, o_jammed_B;
    
    // Type A モジュール（Jamming）
    BioCalibrator_TypeA typeA (
        .i_cell_stiffness(i_cell_stiffness),
        .i_cell_diameter(i_cell_diameter),
        // ...
        .o_is_jammed(o_jammed_A)
    );
    
    // Type B モジュール（Collective）
    BioCalibrator_TypeB typeB (
        .i_cell_stiffness(i_cell_stiffness),
        .i_cell_count(i_cell_count),
        // ...
        .o_is_jammed(o_jammed_B)
    );
    
    // セレクタ
    assign o_is_jammed = i_cancer_type ? o_jammed_B : o_jammed_A;
    
endmodule
";
        };
    };
    
    // ───────────────────────────────────────
    // 4-2. 臨床判断基準
    // ───────────────────────────────────────
    CLINICAL_DECISION: {
        
        PATHOLOGY_BASED: {
            TYPE_A_INDICATORS: {
                TISSUE: "腺癌（Adenocarcinoma）";
                TEXTURE: "硬いしこり";
                MICROSCOPY: "単独細胞が多い";
                AUTO_SELECT: "病理レポートから自動判別可能";
            };
            
            TYPE_B_INDICATORS: {
                TISSUE: "扁平上皮癌（Squamous Cell Carcinoma）";
                TEXTURE: "びまん性";
                MICROSCOPY: "細胞集団が多い";
                AUTO_SELECT: "病理レポートから自動判別可能";
            };
        };
        
        UNKNOWN_CASE: {
            STRATEGY: "両方計算して、より厳しい方（高いBoost値）を採用";
            SAFETY: "Fail-Closed原則（安全側に倒す）";
            
            EXAMPLE: {
                TYPE_A_RESULT: "Boost = 2.5 kPa";
                TYPE_B_RESULT: "Boost = 3.8 kPa";
                FINAL: "3.8 kPa を採用（より厳しい条件）";
            };
        };
    };
    
    // ───────────────────────────────────────
    // 4-3. 将来拡張（Type C, D, ...）
    // ───────────────────────────────────────
    FUTURE_EXPANSION: {
        EXTENSIBILITY: "新しい癌タイプのモジュールを追加可能";
        
        TYPE_C_EXAMPLE: {
            HYPOTHESIS: "Type C: 血管新生を伴う転移";
            PHYSICS: "血管壁の弾性も考慮した複雑モデル";
            IMPLEMENTATION: "Module C を追加し、セレクタを拡張";
        };
        
        MODULARITY: {
            ADVANTAGE: "既存のType A/B モジュールはそのまま";
            MAINTENANCE: "各モジュールが独立 → 保守性高い";
        };
    };
}

// ═══════════════════════════════════════════
// 5. 安全機構の階層
// ═══════════════════════════════════════════
SAFETY_MECHANISMS: {
    
    // ───────────────────────────────────────
    // 5-1. Hardware層（FPGA回路）
    // ───────────────────────────────────────
    LAYER_HARDWARE: {
        
        FAIL_CLOSED_CIRCUIT: {
            PRINCIPLE: "演算器レベルでオーバーフローを検出";
            
            OVERFLOW_DETECTION: {
                ADDER: "加算器にキャリー検出回路";
                MULTIPLIER: "乗算器に上位ビット監視";
                IF_OVERFLOW: "即座に o_is_jammed = 0（DANGER）";
            };
            
            EXAMPLE: {
                SCENARIO: "k·Δx の計算で32ビットを超える";
                DETECTION: "上位16ビットが非ゼロ";
                ACTION: "DANGER出力 + エラーフラグセット";
            };
        };
        
        GEOMETRIC_CHECK: {
            CIRCUIT: "比較器（Comparator）で即座に判定";
            CONDITION: "IF (D_cell <= d_gap) THEN DANGER";
            TIMING: "1クロックサイクルで完了";
        };
    };
    
    // ───────────────────────────────────────
    // 5-2. Firmware層（制御ロジック）
    // ───────────────────────────────────────
    LAYER_FIRMWARE: {
        
        RANGE_VALIDATION: {
            CHECK: "入力値がQ8.8範囲内か";
            IF_EXCEED: "エラーフラグ + DANGER出力";
            MESSAGE: "HOST PCへエラーコード送信";
        };
        
        WATER_TERM_CHECK: {
            CHECK: "η（粘性係数）がゼロでないか";
            IF_ZERO: "即座にエラー";
            MESSAGE: "水分項が未定義です";
        };
    };
    
    // ───────────────────────────────────────
    // 5-3. Software層（ホストPC）
    // ───────────────────────────────────────
    LAYER_SOFTWARE: {
        
        INPUT_SANITIZATION: {
            CHECK: "Phase 4 辞書のRANGE_VALIDと照合";
            REJECT: "範囲外の入力は送信しない";
            WARNING: "医師へ警告表示";
        };
        
        RESULT_VERIFICATION: {
            CHECK: "FPGAからの結果が妥当か";
            SANITY: "Boost > 10 kPa なら警告";
            CROSS_CHECK: "可能なら別アルゴリズムで検算";
        };
    };
    
    // ───────────────────────────────────────
    // 5-4. 階層全体の連携
    // ───────────────────────────────────────
    LAYERED_DEFENSE: {
        CONCEPT: "多層防御（Defense in Depth）";
        
        EXAMPLE_SCENARIO: {
            ERROR: "測定ミスで、細胞硬度 -1.0 kPa（負の値）";
            
            LAYER_1_SOFTWARE: "入力段階で検出 → 送信拒否";
            LAYER_2_FIRMWARE: "もし通過しても、FPGAで検出 → DANGER";
            LAYER_3_HARDWARE: "演算時にも異常検出 → Fail-Closed";
            
            RESULT: "どの層でも捕捉 → 確実に安全側へ";
        };
    };
}

// ═══════════════════════════════════════════
// 6. 次の章への接続
// ═══════════════════════════════════════════
NEXT_PHASE: {
    CURRENT_UNDERSTANDING: "システム全体構造、FPGA選択理由、計算資源要件を理解した";
    
    NEXT_TOPIC: "PHASE_6: FPGA実装仕様（レジスタマップ、パイプライン詳細）";
    NEXT_QUESTION: [
        "Q8.8固定小数点演算の具体的な実装方法は？",
        "レジスタマップの詳細は？",
        "タイミング解析とクリティカルパスは？"
    ];
    
    PREREQUISITE_CHECK: {
        QUESTION_1: "なぜFPGAが必要か理解できたか？";
        QUESTION_2: "総当たり回数（最大684万回）と実行時間（数ms）が理解できたか？";
        QUESTION_3: "データフロー全体が理解できたか？";
        
        IF_NO: "Phase 5を再読";
        IF_YES: "Phase 6へ進む";
    }
}
