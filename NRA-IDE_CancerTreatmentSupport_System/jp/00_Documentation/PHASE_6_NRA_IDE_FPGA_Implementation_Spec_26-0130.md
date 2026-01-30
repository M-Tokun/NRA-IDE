# NRA-IDE_FPGA_Implementation_Spec_Protocol
### Phase 6: FPGA実装仕様（レジスタレベル設計）
* 対象読者: エンジニア + 
* 作成日時: 2026-01-30 22:45

// ═══════════════════════════════════════════
// 0. この章で理解すること
// ═══════════════════════════════════════════
PURPOSE: {
    PREVIOUS_PHASE: "Phase 5でシステム全体構造と計算資源要件を理解した";
    THIS_PHASE: "FPGAレジスタレベルの詳細設計を理解する";
    
    KEY_QUESTIONS: {
        Q1: "Q8.8固定小数点演算をどう実装するのか？";
        Q2: "レジスタマップの詳細は？";
        Q3: "5段パイプラインの各ステージで何をするのか？";
        Q4: "タイミング解析でクリティカルパスは？";
    }
}

// ═══════════════════════════════════════════
// 1. Q8.8固定小数点演算
// ═══════════════════════════════════════════
FIXED_POINT_Q8_8: {
    
    // ───────────────────────────────────────
    // 1-1. なぜ浮動小数点を禁止するのか
    // ───────────────────────────────────────
    WHY_NO_FLOAT: {
        
        FLOATING_POINT_PROBLEM: {
            FORMAT: "IEEE 754 単精度（32ビット）";
            
            PRECISION_LOSS: {
                EXAMPLE: "0.1 + 0.2 = 0.30000000000000004";
                REASON: "10進数を2進数で正確に表現できない";
                ACCUMULATION: "数千回計算すると、誤差が蓄積";
            };
            
            NON_DETERMINISM: {
                PHENOMENON: "同じ計算でも、処理順序で結果が微妙に変わる";
                EXAMPLE: "(a + b) + c ≠ a + (b + c)（理論上は等しいはず）";
                MEDICAL_IMPACT: "再現性なし → 医療機器認証不可";
            };
            
            HARDWARE_COMPLEXITY: {
                CIRCUIT: "浮動小数点演算器は複雑（数千Logic Elements）";
                LATENCY: "数クロックサイクル必要";
                POWER: "消費電力大";
            };
        };
        
        MEDICAL_REQUIREMENT: {
            STAKES: "SAFE/DANGERの境界は 0.1 kPa の差";
            PRECISION: "10⁻⁷ の丸め誤差でも、積み重なれば致命的";
            DETERMINISM: "同じ入力 → 必ず同じ出力（検証可能性）";
            
            CONCLUSION: "浮動小数点は医療判定に不適";
        };
    };
    
    // ───────────────────────────────────────
    // 1-2. Q8.8形式の定義
    // ───────────────────────────────────────
    Q8_8_FORMAT: {
        
        BIT_LAYOUT: {
            TOTAL: "16 ビット";
            INTEGER_PART: "上位8ビット（ビット15〜8）";
            FRACTIONAL_PART: "下位8ビット（ビット7〜0）";
            
            DIAGRAM: "
┌─────────────┬─────────────┐
│  Integer    │  Fraction   │
│  8 bits     │  8 bits     │
│  [15:8]     │  [7:0]      │
└─────────────┴─────────────┘
Bit: 15 14 13 12 11 10 9  8  7  6  5  4  3  2  1  0
     2⁷ 2⁶ 2⁵ 2⁴ 2³ 2² 2¹ 2⁰ 2⁻¹ 2⁻² ... 2⁻⁸
";
        };
        
        RANGE: {
            MIN: "0.00390625（1/256 = 2⁻⁸）";
            MAX: "255.99609375（256 - 1/256）";
            PRECISION: "1/256 ≈ 0.0039";
        };
        
        EXAMPLES: {
            EXAMPLE_1: {
                VALUE: "2.5 kPa";
                CALCULATION: "2.5 × 256 = 640";
                BINARY: "0000 0010 1000 0000";
                HEX: "0x0280";
                BREAKDOWN: "0x02（整数部=2） + 0x80（小数部=0.5）";
            };
            
            EXAMPLE_2: {
                VALUE: "0.1 kPa";
                CALCULATION: "0.1 × 256 = 25.6 → 26（四捨五入）";
                BINARY: "0000 0000 0001 1010";
                HEX: "0x001A";
                ACTUAL: "26 / 256 = 0.1015625 kPa";
                ERROR: "誤差 = 0.0015625 kPa（許容範囲）";
            };
            
            EXAMPLE_3: {
                VALUE: "12.0 μm";
                CALCULATION: "12.0 × 256 = 3072";
                BINARY: "0000 1100 0000 0000";
                HEX: "0x0C00";
            };
        };
    };
    
    // ───────────────────────────────────────
    // 1-3. Q8.8演算ルール
    // ───────────────────────────────────────
    ARITHMETIC_RULES: {
        
        ADDITION: {
            RULE: "そのまま加算（シフト不要）";
            
            EXAMPLE: {
                A: "2.5 kPa = 0x0280 (640)";
                B: "1.5 kPa = 0x0180 (384)";
                CALC: "640 + 384 = 1024";
                RESULT: "0x0400 = 4.0 kPa ✓";
            };
            
            VERILOG: "result = a + b; // 16ビット加算";
        };
        
        SUBTRACTION: {
            RULE: "そのまま減算（シフト不要）";
            
            EXAMPLE: {
                A: "12.0 μm = 0x0C00 (3072)";
                B: "8.0 μm = 0x0800 (2048)";
                CALC: "3072 - 2048 = 1024";
                RESULT: "0x0400 = 4.0 μm ✓";
            };
            
            VERILOG: "result = a - b; // 16ビット減算";
        };
        
        MULTIPLICATION: {
            RULE: "乗算後、8ビット右シフト（÷256）";
            
            WHY_SHIFT: {
                Q8_8_x_Q8_8: "小数部が2回掛かる → Q8.16になる";
                CORRECTION: "8ビット右シフトで Q8.8 に戻す";
            };
            
            EXAMPLE: {
                A: "2.0 kPa = 0x0200 (512)";
                B: "4.0 μm = 0x0400 (1024)";
                CALC: "512 × 1024 = 524,288";
                BINARY: "32ビット結果 = 0x0008_0000";
                SHIFT: "524,288 >> 8 = 2048";
                RESULT: "0x0800 = 8.0 [kPa·μm] ✓";
            };
            
            VERILOG: {
                CODE: "
wire [31:0] product;
wire [15:0] result;
assign product = a * b;       // 32ビット乗算
assign result = product[23:8]; // 上位16ビット取得（=8ビット右シフト）
";
            };
        };
        
        DIVISION: {
            RULE: "8ビット左シフト（×256）してから除算";
            
            WHY_SHIFT: {
                Q8_8_div_Q8_8: "小数部が打ち消される → 整数になる";
                CORRECTION: "事前に256倍して補正";
            };
            
            EXAMPLE: {
                A: "8.0 kPa = 0x0800 (2048)";
                B: "2.0 kPa = 0x0200 (512)";
                SHIFT: "2048 << 8 = 524,288";
                CALC: "524,288 / 512 = 1024";
                RESULT: "0x0400 = 4.0 ✓";
            };
            
            VERILOG: {
                CODE: "
wire [31:0] dividend;
wire [15:0] result;
assign dividend = {a, 16'h0000}; // 8ビット左シフト（下位16ビットを0埋め）
assign result = dividend / b;     // 除算
";
            };
            
            NOTE: "除算はハードウェアコスト大 → なるべく避ける";
        };
    };
    
    // ───────────────────────────────────────
    // 1-4. オーバーフロー対策
    // ───────────────────────────────────────
    OVERFLOW_HANDLING: {
        
        ADDITION_OVERFLOW: {
            DETECTION: "キャリーフラグ（17ビット目）をチェック";
            
            EXAMPLE: {
                A: "200.0 kPa = 0xC800 (51200)";
                B: "100.0 kPa = 0x6400 (25600)";
                CALC: "51200 + 25600 = 76800 = 0x12C00（17ビット）";
                OVERFLOW: "ビット16が1 → オーバーフロー";
            };
            
            ACTION: "即座に DANGER出力 + エラーフラグ";
            
            VERILOG: "
wire [16:0] sum;
assign sum = {1'b0, a} + {1'b0, b}; // 17ビット加算
assign overflow = sum[16];          // 最上位ビット
if (overflow) assign o_is_jammed = 1'b0; // DANGER
";
        };
        
        MULTIPLICATION_OVERFLOW: {
            DETECTION: "上位16ビット（[31:24]）が非ゼロ";
            
            EXAMPLE: {
                A: "200.0 kPa = 0xC800";
                B: "200.0 μm = 0xC800";
                CALC: "51200 × 51200 = 2,621,440,000";
                BINARY: "32ビット結果 = 0x9C40_0000";
                CHECK: "上位8ビット [31:24] = 0x9C（非ゼロ）";
                OVERFLOW: "検出！";
            };
            
            ACTION: "DANGER出力 + エラーコード";
            
            VERILOG: "
wire [31:0] product;
assign product = a * b;
assign overflow = |product[31:24]; // OR reduction（1つでも1なら1）
if (overflow) assign o_is_jammed = 1'b0;
";
        };
    };
}

// ═══════════════════════════════════════════
// 2. レジスタマップ定義
// ═══════════════════════════════════════════
REGISTER_MAP: {
    
    // ───────────────────────────────────────
    // 2-1. 入力レジスタ群
    // ───────────────────────────────────────
    INPUT_REGISTERS: {
        
        I_CELL_STIFFNESS: {
            ADDRESS: "0x00";
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            UNIT: "kPa";
            RANGE: "[0x001A, 0x0A00] = [0.1, 10.0] kPa";
            RESET: "0x0000";
            DESCRIPTION: "細胞の反発力（弾性係数）";
        };
        
        I_CELL_VISCOSITY: {
            ADDRESS: "0x02";
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            UNIT: "Pa·s";
            RANGE: "[0x0003, 0x0100] = [0.01, 1.0] Pa·s";
            RESET: "0x000D"; // 0.05 Pa·s（デフォルト）
            PROHIBITION: "0x0000は禁止（水分項必須）";
            DESCRIPTION: "細胞の粘り（水分抵抗係数）";
        };
        
        I_CELL_DIAMETER: {
            ADDRESS: "0x04";
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            UNIT: "μm";
            RANGE: "[0x0500, 0x1E00] = [5.0, 30.0] μm";
            RESET: "0x0000";
            DESCRIPTION: "細胞の直径";
        };
        
        I_PORE_SIZE: {
            ADDRESS: "0x06";
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            UNIT: "μm";
            RANGE: "[0x0500, 0x0F00] = [5.0, 15.0] μm";
            RESET: "0x0800"; // 8.0 μm（典型的毛細血管）
            DESCRIPTION: "血管の隙間（微細孔直径）";
        };
        
        I_FLOW_DP: {
            ADDRESS: "0x08";
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            UNIT: "kPa";
            RANGE: "[0x000D, 0x0500] = [0.05, 5.0] kPa";
            RESET: "0x0000";
            DESCRIPTION: "局所圧差（血流押圧力）";
        };
        
        I_DRUG_BOOST: {
            ADDRESS: "0x0A";
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            UNIT: "kPa";
            RANGE: "[0x0000, 0x0A00] = [0.0, 10.0] kPa";
            RESET: "0x0000";
            DESCRIPTION: "薬剤補強（硬化ブースト）";
        };
        
        I_CELL_COUNT: {
            ADDRESS: "0x0C";
            WIDTH: "8 bit";
            FORMAT: "整数";
            UNIT: "個";
            RANGE: "[1, 50]";
            RESET: "0x01"; // デフォルト1個（Type A想定）";
            DESCRIPTION: "細胞クラスタの数（Type B用）";
        };
        
        I_CANCER_TYPE: {
            ADDRESS: "0x0E";
            WIDTH: "1 bit";
            FORMAT: "Boolean";
            VALUES: "0=Type A, 1=Type B";
            RESET: "0"; // デフォルトType A
            DESCRIPTION: "癌タイプ選択";
        };
    };
    
    // ───────────────────────────────────────
    // 2-2. 中間演算レジスタ（ワイヤ）
    // ───────────────────────────────────────
    INTERMEDIATE_WIRES: {
        
        W_TOTAL_STIFFNESS: {
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            CALCULATION: "i_cell_stiffness + i_drug_boost";
            DESCRIPTION: "総合硬度";
        };
        
        W_DEFORMATION: {
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            CALCULATION: "MAX(0, i_cell_diameter - i_pore_size)";
            DESCRIPTION: "変形量";
        };
        
        W_ELASTIC_FORCE: {
            WIDTH: "32 bit";
            FORMAT: "Q16.16（中間結果）";
            CALCULATION: "w_total_stiffness * w_deformation";
            DESCRIPTION: "弾性項（乗算後、未シフト）";
        };
        
        W_ELASTIC_SCALED: {
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            CALCULATION: "w_elastic_force[23:8]";
            DESCRIPTION: "弾性項（8ビット右シフト後）";
        };
        
        W_VISCOUS_FORCE: {
            WIDTH: "32 bit";
            FORMAT: "Q16.16";
            CALCULATION: "i_cell_viscosity * deform_velocity";
            DESCRIPTION: "粘性項（乗算後、未シフト）";
        };
        
        W_RESIST_FORCE: {
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            CALCULATION: "(w_elastic_scaled + w_viscous_scaled) * ALPHA";
            DESCRIPTION: "総抵抗圧力";
        };
    };
    
    // ───────────────────────────────────────
    // 2-3. 出力レジスタ群
    // ───────────────────────────────────────
    OUTPUT_REGISTERS: {
        
        O_IS_JAMMED: {
            ADDRESS: "0x10";
            WIDTH: "1 bit";
            VALUES: "1=SAFE, 0=DANGER";
            DESCRIPTION: "判定結果";
            
            LOGIC: "IF (w_resist_force > i_flow_dp) THEN 1 ELSE 0";
        };
        
        O_OPTIMAL_BOOST: {
            ADDRESS: "0x12";
            WIDTH: "16 bit";
            FORMAT: "Q8.8";
            UNIT: "kPa";
            DESCRIPTION: "最適薬液量（総当たり結果）";
        };
        
        O_ERROR_CODE: {
            ADDRESS: "0x14";
            WIDTH: "8 bit";
            FORMAT: "Enum（Phase 4 辞書参照）";
            DESCRIPTION: "エラーコード";
            
            CODES: {
                NO_ERROR: "0x00";
                GEOMETRIC_BYPASS: "0x01";
                NEGATIVE_STIFFNESS: "0x02";
                ZERO_VISCOSITY: "0x03";
                OVERFLOW: "0x04";
                PRESSURE_UNKNOWN: "0x05";
            };
        };
        
        O_ALERT_LEVEL: {
            ADDRESS: "0x16";
            WIDTH: "2 bit";
            FORMAT: "Enum";
            DESCRIPTION: "警告レベル";
            
            VALUES: {
                NORMAL: "0b00";
                CAUTION: "0b01";
                RED_ZONE: "0b10";
            };
        };
    };
}

// ═══════════════════════════════════════════
// 3. パイプライン設計
// ═══════════════════════════════════════════
PIPELINE_DESIGN: {
    
    // ───────────────────────────────────────
    // 3-1. 5段パイプライン概要
    // ───────────────────────────────────────
    PIPELINE_OVERVIEW: {
        STAGES: 5;
        THROUGHPUT: "1判定 / 5 cycles";
        LATENCY: "5 cycles（初回のみ）";
        
        DIAGRAM: "
Clock:    1      2      3      4      5      6      7
Stage 1: [A]    [B]    [C]    [D]    [E]    [F]    ...
Stage 2:        [A]    [B]    [C]    [D]    [E]    ...
Stage 3:               [A]    [B]    [C]    [D]    ...
Stage 4:                      [A]    [B]    [C]    ...
Stage 5:                             [A]    [B]    ...

A,B,C... = 異なる判定タスク
初回は5サイクル、以降は1サイクル/判定
";
    };
    
    // ───────────────────────────────────────
    // 3-2. 各ステージの詳細
    // ───────────────────────────────────────
    STAGE_1_DEFORMATION: {
        NAME: "変形量計算";
        
        OPERATIONS: {
            OP_1: "幾何学的チェック: IF (D_cell <= d_gap)";
            OP_2: "減算: Δx = D_cell - d_gap";
            OP_3: "MAX: Δx = MAX(0, Δx)";
        };
        
        VERILOG: "
always @(posedge clk) begin
    if (i_cell_diameter <= i_pore_size) begin
        r_deformation <= 16'h0000;
        r_bypass_flag <= 1'b1; // すり抜けリスク
    end else begin
        r_deformation <= i_cell_diameter - i_pore_size;
        r_bypass_flag <= 1'b0;
    end
end
";
        
        TIMING: "1 cycle";
    };
    
    STAGE_2_ELASTIC: {
        NAME: "弾性力計算";
        
        OPERATIONS: {
            OP_1: "加算: k_total = k_cell + Boost";
            OP_2: "乗算: F_elastic = k_total × Δx";
        };
        
        VERILOG: "
always @(posedge clk) begin
    r_total_stiffness <= i_cell_stiffness + i_drug_boost;
    r_elastic_raw <= r_total_stiffness * r_deformation; // 32ビット
end
";
        
        TIMING: "1 cycle";
    };
    
    STAGE_3_VISCOUS: {
        NAME: "粘性抵抗計算";
        
        OPERATIONS: {
            OP_1: "粘性力: F_viscous = η × (dv/dt)";
            NOTE: "dv/dt は外部から与えられる（または固定値）";
        };
        
        VERILOG: "
always @(posedge clk) begin
    r_viscous_raw <= i_cell_viscosity * i_deform_velocity; // 32ビット
end
";
        
        TIMING: "1 cycle";
    };
    
    STAGE_4_TOTAL_RESISTANCE: {
        NAME: "総合抵抗力算出";
        
        OPERATIONS: {
            OP_1: "右シフト: F_elastic_scaled = F_elastic_raw >> 8";
            OP_2: "右シフト: F_viscous_scaled = F_viscous_raw >> 8";
            OP_3: "加算: F_resist = (F_elastic + F_viscous) × α";
        };
        
        VERILOG: "
localparam ALPHA = 250;

always @(posedge clk) begin
    r_elastic_scaled <= r_elastic_raw[23:8];
    r_viscous_scaled <= r_viscous_raw[23:8];
    r_resist_force <= (r_elastic_scaled + r_viscous_scaled) * ALPHA;
end
";
        
        TIMING: "1 cycle";
    };
    
    STAGE_5_JUDGMENT: {
        NAME: "比較判定";
        
        OPERATIONS: {
            OP_1: "比較: Resist > Pressure ?";
            OP_2: "Fail-Closed: 不確かさは DANGER側";
        };
        
        VERILOG: "
always @(posedge clk) begin
    if (r_bypass_flag) begin
        o_is_jammed <= 1'b0; // 幾何学的すり抜け → DANGER
    end else if (r_overflow_flag) begin
        o_is_jammed <= 1'b0; // オーバーフロー → DANGER
    end else if (r_resist_force > i_flow_dp) begin
        o_is_jammed <= 1'b1; // SAFE
    end else begin
        o_is_jammed <= 1'b0; // DANGER
    end
end
";
        
        TIMING: "1 cycle";
    };
}

// ═══════════════════════════════════════════
// 4. タイミング解析
// ═══════════════════════════════════════════
TIMING_ANALYSIS: {
    
    // ───────────────────────────────────────
    // 4-1. クリティカルパス特定
    // ───────────────────────────────────────
    CRITICAL_PATH: {
        
        CANDIDATES: {
            PATH_1: {
                ROUTE: "乗算器 → シフト → 加算 → 比較";
                DELAY: "約8 ns（100MHz想定）";
                STAGE: "Stage 4（総合抵抗力）";
            };
            
            PATH_2: {
                ROUTE: "レジスタ → 乗算器 → レジスタ";
                DELAY: "約7 ns";
                STAGE: "Stage 2（弾性力乗算）";
            };
        };
        
        WORST_CASE: "PATH_1（約8 ns）";
        
        MARGIN: {
            CLOCK_PERIOD: "10 ns（100MHz）";
            PATH_DELAY: "8 ns";
            SLACK: "2 ns（余裕あり）";
        };
    };
    
    // ───────────────────────────────────────
    // 4-2. タイミング制約
    // ───────────────────────────────────────
    TIMING_CONSTRAINTS: {
        
        SETUP_TIME: {
            DEFINITION: "クロック立ち上がり前に、データが安定している時間";
            TYPICAL: "1 ns";
        };
        
        HOLD_TIME: {
            DEFINITION: "クロック立ち上がり後も、データが保持される時間";
            TYPICAL: "0.5 ns";
        };
        
        CLOCK_SKEW: {
            DEFINITION: "クロック信号の到達時間のばらつき";
            BUDGET: "±0.5 ns以内";
        };
    };
    
    // ───────────────────────────────────────
    // 4-3. 最適化戦略
    // ───────────────────────────────────────
    OPTIMIZATION: {
        
        STRATEGY_1_RETIMING: {
            TECHNIQUE: "レジスタを最適配置し直す";
            GOAL: "クリティカルパスを短縮";
            TOOL: "FPGAツール（Quartus, Vivado）が自動実行";
        };
        
        STRATEGY_2_PIPELINING: {
            TECHNIQUE: "長い組み合わせ回路をさらに分割";
            EXAMPLE: "Stage 4 を 2つに分割 → 6段パイプライン";
            TRADEOFF: "レイテンシ増加、スループット不変";
        };
        
        STRATEGY_3_RESOURCE_SHARING: {
            TECHNIQUE: "乗算器を時分割で共有";
            BENEFIT: "Logic Elements削減";
            TRADEOFF: "スループット低下";
            USE_CASE: "並列度を下げる場合";
        };
    };
}

// ═══════════════════════════════════════════
// 5. リソース見積もり
// ═══════════════════════════════════════════
RESOURCE_ESTIMATION: {
    
    // ───────────────────────────────────────
    // 5-1. Logic Elements（LE）
    // ───────────────────────────────────────
    LOGIC_ELEMENTS: {
        
        SINGLE_UNIT: {
            REGISTERS: "約200 LE";
            MULTIPLIERS: "4個 × 200 LE = 800 LE";
            COMPARATORS: "約50 LE";
            CONTROL: "約100 LE";
            TOTAL: "約1,150 LE / ユニット";
        };
        
        PARALLEL_16_UNITS: {
            CALCULATION: "1,150 × 16 = 18,400 LE";
            TARGET_FPGA: "Intel Cyclone V（約25K LE）";
            UTILIZATION: "約75%（適正範囲）";
        };
    };
    
    // ───────────────────────────────────────
    // 5-2. DSPブロック
    // ───────────────────────────────────────
    DSP_BLOCKS: {
        
        USAGE: {
            MULTIPLIERS: "4個 / ユニット（弾性×2, 粘性×1, スケール×1）";
            PARALLEL_16: "64個のDSPブロック";
        };
        
        AVAILABILITY: {
            CYCLONE_V: "約80 DSPブロック";
            UTILIZATION: "64 / 80 = 80%（やや高い）";
        };
        
        OPTIMIZATION: {
            OPTION: "一部の乗算を Logic Elementsで実装";
            TRADEOFF: "LE消費増、DSP節約";
        };
    };
    
    // ───────────────────────────────────────
    // 5-3. メモリ（RAM）
    // ───────────────────────────────────────
    MEMORY: {
        
        INTERNAL: {
            REGISTERS_ONLY: "約500 bit / ユニット";
            NO_RAM: "外部RAMは不要";
            ADVANTAGE: "アクセス遅延ゼロ";
        };
        
        LOOKUP_TABLES: {
            EXAMPLE: "√N テーブル（Type B用）";
            SIZE: "50エントリ × 8bit = 400 bit";
            IMPLEMENTATION: "ROM（Logic Elementsで実装）";
        };
    };
}

// ═══════════════════════════════════════════
// 6. 次の章への接続
// ═══════════════════════════════════════════
NEXT_PHASE: {
    CURRENT_UNDERSTANDING: "FPGA実装の詳細（Q8.8演算、レジスタマップ、パイプライン）を理解した";
    
    NEXT_TOPIC: "PHASE_7: 実装コード（冗長コメント版Verilog + Python）";
    NEXT_QUESTION: [
        "実際のVerilogコードはどう書くのか？",
        "Pythonホスト側のコードは？",
        "Testbenchでどう検証するのか？"
    ];
    
    PREREQUISITE_CHECK: {
        QUESTION_1: "Q8.8固定小数点の演算ルールが理解できたか？";
        QUESTION_2: "5段パイプラインの各ステージが理解できたか？";
        QUESTION_3: "タイミング解析とクリティカルパスが理解できたか？";
        
        IF_NO: "Phase 6を再読";
        IF_YES: "Phase 7へ進む";
    }
}
