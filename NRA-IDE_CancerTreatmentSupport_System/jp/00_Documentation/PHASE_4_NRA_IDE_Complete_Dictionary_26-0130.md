# NRA-IDE_Complete_Terminology_Dictionary
### Phase 4: 完全用語辞書（統一基準）
* 対象読者: 医療関係者 + エンジニア
* 作成日時: 2026-01-30 22:15


// ═══════════════════════════════════════════

// 0. この辞書の目的

// ═══════════════════════════════════════════


PURPOSE: {
    FUNCTION: "NRA-IDEシステム内で使用される全ての変数・単位・命名を定義";
    AUDIENCE: [
        "医師（物理的意味を理解するため）",
        "エンジニア（実装時の参照として）",
        "研究者（論文執筆時の用語統一）"
    ];
    
    CRITICAL_RULE: {
        STATEMENT: "この辞書に載っていない変数名・単位は使用禁止";
        ENFORCEMENT: "コンパイル時に、辞書との照合チェックを実行";
        VIOLATION: "辞書にない名前が見つかったら、エラー";
    };
}


// ═══════════════════════════════════════════

// 1. 物理量定義表（全変数）

// ═══════════════════════════════════════════

DICTIONARY: PHYSICAL_VARIABLES {
    
    // ───────────────────────────────────────
    // 1-1. 細胞関連変数
    // ───────────────────────────────────────
    CATEGORY: CELL_PROPERTIES {
        
        ENTRY: CELL_STIFFNESS {
            CLINICAL_NAME_JP: "細胞の反発力（弾性係数）";
            CLINICAL_NAME_EN: "Cell Stiffness (Elastic Modulus)";
            REGISTER_NAME: "i_cell_stiffness";
            UNIT_SI: "kPa（キロパスカル）";
            UNIT_Q8_8: "0x0100 = 1.0 kPa";
            
            RANGE_VALID: {
                MIN: 0.1;  // kPa
                MAX: 10.0; // kPa
                TYPICAL: [0.5, 3.0]; // 正常〜癌細胞
            };
            
            RANGE_Q8_8: {
                MIN: 0x001A; // 26 (= 0.1 × 256)
                MAX: 0x0A00; // 2560 (= 10.0 × 256)
            };
            
            PHYSICS_MEANING: "細胞が変形した際に元に戻ろうとする力。乳がんのJamming判定の主軸";
            
            MEASUREMENT_METHOD: {
                TECHNIQUE: "超音波エラストグラフィ（Ultrasound Elastography）";
                PROCEDURE: "超音波で組織を押し、変形の度合いから硬さを推定";
                ACCURACY: "±0.2 kPa程度";
            };
            
            CLINICAL_INTERPRETATION: {
                SOFT: "0.1〜0.5 kPa → 柔らかい → すり抜けリスク高";
                MEDIUM: "0.5〜1.5 kPa → 正常範囲";
                HARD: "1.5〜3.0 kPa → 硬い → ジャミング可能性";
                VERY_HARD: "3.0〜 kPa → 異常に硬い → 石灰化の疑い";
            };
        };
        
        ENTRY: CELL_VISCOSITY {
            CLINICAL_NAME_JP: "細胞の粘り（水分抵抗係数）";
            CLINICAL_NAME_EN: "Cell Viscosity (Viscous Coefficient)";
            REGISTER_NAME: "i_cell_viscosity";
            UNIT_SI: "Pa·s（パスカル秒）";
            UNIT_Q8_8: "0x0100 = 1.0 Pa·s";
            
            RANGE_VALID: {
                MIN: 0.01;  // Pa·s
                MAX: 1.0;   // Pa·s
                TYPICAL: [0.03, 0.1]; // 細胞質の粘性
            };
            
            RANGE_Q8_8: {
                MIN: 0x0003; // 3 (= 0.01 × 256)
                MAX: 0x0100; // 256 (= 1.0 × 256)
            };
            
            PHYSICS_MEANING: "細胞内の水分が急激な変形を妨げる強さ。子宮頸がんのすり抜け阻止の生命線";
            
            PROHIBITION: {
                RULE: "この値を0にすることは永久に禁止";
                REASON: "水分無視 = 生命の時間依存性を無視 = 非物理的";
                ENFORCEMENT: "η = 0 なら即座にコンパイルエラー";
            };
            
            MEASUREMENT_METHOD: {
                TECHNIQUE: "マイクロレオロジー（Microrheology）、光ピンセット";
                PROCEDURE: "微小ビーズを細胞内に入れ、その動きから粘性を推定";
                ACCURACY: "±0.01 Pa·s程度";
            };
        };
        
        ENTRY: CELL_DIAMETER {
            CLINICAL_NAME_JP: "細胞の直径";
            CLINICAL_NAME_EN: "Cell Diameter";
            REGISTER_NAME: "i_cell_diameter";
            UNIT_SI: "μm（マイクロメートル）";
            UNIT_Q8_8: "0x0100 = 1.0 μm";
            
            RANGE_VALID: {
                MIN: 5.0;   // μm
                MAX: 30.0;  // μm
                TYPICAL: [8.0, 25.0]; // 一般的な上皮細胞
            };
            
            RANGE_Q8_8: {
                MIN: 0x0500;  // 1280 (= 5.0 × 256)
                MAX: 0x1E00;  // 7680 (= 30.0 × 256)
            };
            
            PHYSICS_MEANING: "細胞の大きさ。血管隙間との幾何学的比較に使用";
            
            MEASUREMENT_METHOD: {
                TECHNIQUE: "顕微鏡画像解析、超音波画像";
                PROCEDURE: "病理標本を顕微鏡で観察し、直径を測定";
                ACCURACY: "±1 μm程度";
            };
        };
        
        ENTRY: CELL_COUNT {
            CLINICAL_NAME_JP: "細胞クラスタの数（集団サイズ）";
            CLINICAL_NAME_EN: "Cell Cluster Count";
            REGISTER_NAME: "i_cell_count";
            UNIT_SI: "個（無次元）";
            UNIT_Q8_8: "整数のまま（8ビット）";
            
            RANGE_VALID: {
                MIN: 1;     // 個
                MAX: 50;    // 個
                TYPICAL: [1, 20]; // 単独〜中規模クラスタ
            };
            
            PHYSICS_MEANING: "Type B（子宮頸がん等）で、同時に押し寄せる細胞の個数";
            
            MEASUREMENT_METHOD: {
                TECHNIQUE: "病理組織標本の観察";
                PROCEDURE: "HE染色標本で、細胞塊のサイズを計数";
                ACCURACY: "±5個程度";
            };
        };
    };
    

    // ───────────────────────────────────────
    
    // 1-2. 血管関連変数
    
    // ───────────────────────────────────────
    
    CATEGORY: VESSEL_PROPERTIES {
        
        ENTRY: PORE_SIZE {
            CLINICAL_NAME_JP: "血管の隙間（微細孔直径）";
            CLINICAL_NAME_EN: "Vessel Pore Size (Gap Diameter)";
            REGISTER_NAME: "i_pore_size";
            UNIT_SI: "μm（マイクロメートル）";
            UNIT_Q8_8: "0x0100 = 1.0 μm";
            
            RANGE_VALID: {
                MIN: 5.0;   // μm
                MAX: 15.0;  // μm
                TYPICAL: 8.0; // 毛細血管の典型値
            };
            
            RANGE_Q8_8: {
                MIN: 0x0500;  // 1280 (= 5.0 × 256)
                MAX: 0x0F00;  // 3840 (= 15.0 × 256)
            };
            
            PHYSICS_MEANING: "細胞が通過しようとする血管の隙間の大きさ";
            
            MEASUREMENT_METHOD: {
                TECHNIQUE: "血管造影、電子顕微鏡";
                PROCEDURE: "造影剤を注入し、血管の内径を測定";
                ACCURACY: "±0.5 μm程度";
            };
            
            TYPICAL_VALUES: {
                CAPILLARY: "5〜10 μm（毛細血管）";
                VENULE: "10〜15 μm（細静脈）";
            };
        };
        
        ENTRY: FLOW_PRESSURE {
            CLINICAL_NAME_JP: "局所圧差（血流押圧力）";
            CLINICAL_NAME_EN: "Local Flow Pressure (Differential Pressure)";
            REGISTER_NAME: "i_flow_dp";
            UNIT_SI: "kPa（キロパスカル）";
            UNIT_Q8_8: "0x0100 = 1.0 kPa";
            
            RANGE_VALID: {
                MIN: 0.05;  // kPa
                MAX: 5.0;   // kPa
                TYPICAL: [0.5, 2.0]; // 毛細血管の圧力差
            };
            
            RANGE_Q8_8: {
                MIN: 0x000D;  // 13 (= 0.05 × 256)
                MAX: 0x0500;  // 1280 (= 5.0 × 256)
            };
            
            PHYSICS_MEANING: "微細孔を通過させようとする外部の力。血流が細胞を押す圧力";
            
            CAUTION: {
                STATEMENT: "全身血圧（mmHg）とは無関係";
                REASON: "局所の圧力差のみを考慮する";
                CONVERSION_NOTE: "血圧120mmHgは約16kPaだが、局所圧差は数kPa程度";
            };
            
            MEASUREMENT_METHOD: {
                TECHNIQUE: "カテーテル圧測定、数値流体力学（CFD）";
                PROCEDURE: "血管内にカテーテルを挿入し、圧力を直接測定";
                ACCURACY: "±0.1 kPa程度";
            };
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 1-3. 薬剤関連変数
    
    // ───────────────────────────────────────
   
    CATEGORY: DRUG_PARAMETERS {
        
        ENTRY: DRUG_BOOST {
            CLINICAL_NAME_JP: "薬剤補強（硬化ブースト）";
            CLINICAL_NAME_EN: "Drug-induced Stiffness Boost";
            REGISTER_NAME: "i_drug_boost";
            UNIT_SI: "kPa（キロパスカル）";
            UNIT_Q8_8: "0x0100 = 1.0 kPa";
            
            RANGE_VALID: {
                MIN: 0.0;   // kPa（薬剤なし）
                MAX: 10.0;  // kPa（最大投与）
                TYPICAL: [1.0, 5.0]; // 治療的範囲
            };
            
            RANGE_Q8_8: {
                MIN: 0x0000;  // 0
                MAX: 0x0A00;  // 2560 (= 10.0 × 256)
            };
            
            PHYSICS_MEANING: "薬剤により人為的に強化された細胞硬さ。最適化の制御変数";
            
            OPTIMIZATION_GOAL: "最小のBoost値で、SAFEを達成する値を総当たり探索で特定";
            
            CLINICAL_CONSIDERATION: {
                BENEFIT: "細胞を硬化させ、血管通過を防ぐ";
                RISK: "過剰投与で細胞破砕、副作用";
                BALANCE: "最小必要量を厳密計算で決定";
            };
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 1-4. 中間計算変数
    
    // ───────────────────────────────────────
    
    CATEGORY: INTERMEDIATE_VARIABLES {
        
        ENTRY: TOTAL_STIFFNESS {
            REGISTER_NAME: "w_total_stiffness";
            CALCULATION: "i_cell_stiffness + i_drug_boost";
            UNIT_SI: "kPa";
            UNIT_Q8_8: "0x0100 = 1.0 kPa";
            CLINICAL_ROLE: "細胞の固有硬度 + 薬剤による増強 = 総合硬度";
        };
        
        ENTRY: DEFORMATION {
            REGISTER_NAME: "w_deformation";
            CALCULATION: "MAX(0, i_cell_diameter - i_pore_size)";
            UNIT_SI: "μm";
            UNIT_Q8_8: "0x0100 = 1.0 μm";
            CLINICAL_ROLE: "細胞が血管隙間で押し潰される量";
            
            GEOMETRIC_CONDITION: {
                IF_CELL_SMALLER: "細胞 < 隙間 → Δx = 0（すり抜け）";
                IF_CELL_LARGER: "細胞 > 隙間 → Δx = 差分（潰れる）";
            };
        };
        
        ENTRY: ELASTIC_FORCE {
            REGISTER_NAME: "w_elastic_force";
            CALCULATION: "w_total_stiffness * w_deformation";
            UNIT_SI: "kPa·μm（力の次元）";
            UNIT_Q8_8: "Q16.16（32ビット中間結果）";
            CLINICAL_ROLE: "弾性項による抵抗力（バネの力）";
        };
        
        ENTRY: VISCOUS_FORCE {
            REGISTER_NAME: "w_viscous_force";
            CALCULATION: "i_cell_viscosity * deform_velocity";
            UNIT_SI: "Pa·μm/s（力の次元）";
            UNIT_Q8_8: "Q16.16（32ビット中間結果）";
            CLINICAL_ROLE: "粘性項による抵抗力（水分の抵抗）";
        };
        
        ENTRY: TOTAL_RESISTANCE {
            REGISTER_NAME: "w_resist_force";
            CALCULATION: "w_elastic_force + w_viscous_force + SCALING";
            UNIT_SI: "Pa（圧力）";
            UNIT_Q8_8: "0x0100 = 1.0 Pa";
            CLINICAL_ROLE: "細胞が発揮する総抵抗力";
            
            SCALING: {
                FACTOR: "α = 250（実験的に決定）";
                PURPOSE: "Q8.8固定小数点の範囲に収める";
            };
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 1-5. 出力変数
    
    // ───────────────────────────────────────
    
    CATEGORY: OUTPUT_VARIABLES {
        
        ENTRY: IS_JAMMED {
            REGISTER_NAME: "o_is_jammed";
            TYPE: "Boolean（1ビット）";
            VALUES: {
                SAFE: 1;   // 物理的封鎖成立
                DANGER: 0; // 通過リスクあり
            };
            
            JUDGMENT_LOGIC: {
                CONDITION: "IF (w_resist_force > i_flow_dp) THEN 1 ELSE 0";
                CLINICAL_ROLE: "抵抗力 > 押す力 なら SAFE";
            };
            
            CLINICAL_INTERPRETATION: {
                SAFE: "この条件下では、細胞は物理的に血管を通過できない";
                DANGER: "通過リスクあり。追加検査または薬液量増加が必要";
            };
        };
        
        ENTRY: OPTIMAL_BOOST {
            REGISTER_NAME: "o_optimal_boost";
            TYPE: "Q8.8固定小数点（16ビット）";
            UNIT_SI: "kPa";
            CLINICAL_ROLE: "SAFEを達成する最小の薬液量";
            
            CALCULATION_METHOD: {
                STEP_1: "Boost = 0 から開始";
                STEP_2: "o_is_jammed を判定";
                STEP_3: "IF (DANGER) THEN Boost += 0.01 kPa";
                STEP_4: "SAFE になるまで繰り返し";
                STEP_5: "その時のBoost値を記録";
            };
        };
    };
}


// ═══════════════════════════════════════════

// 2. 単位変換表

// ═══════════════════════════════════════════

DICTIONARY: UNIT_CONVERSION {
    

    // ───────────────────────────────────────
    
    // 2-1. 血圧の変換（mmHg → kPa）
    
    // ───────────────────────────────────────
    
    CONVERSION: BLOOD_PRESSURE_mmHg_to_kPa {
        FORMULA: "kPa = mmHg × 0.133322";
        
        EXAMPLES: {
            EXAMPLE_1: "120 mmHg → 16.0 kPa";
            EXAMPLE_2: "80 mmHg → 10.7 kPa";
            EXAMPLE_3: "140 mmHg → 18.7 kPa";
        };
        
        IMPLEMENTATION_Q8_8: {
            FORMULA: "kPa_Q8_8 = (mmHg × 34) >> 8";
            EXPLANATION: "0.133322 × 256 ≈ 34（整数近似）";
            EXAMPLE: "120 mmHg → (120 × 34) >> 8 = 4080 >> 8 = 15.9（約16.0 kPa）";
        };
        
        CAUTION: {
            NOTE: "全身血圧と局所圧差は別物";
            REASON: "血管の抵抗により、局所では圧力が低下する";
            USE: "この変換は参考値。実際は局所測定が望ましい";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 2-2. 長さの変換（μm → Q8.8）
    
    // ───────────────────────────────────────
    
    CONVERSION: LENGTH_um_to_Q8_8 {
        FORMULA: "Q8_8 = μm × 256";
        
        EXAMPLES: {
            EXAMPLE_1: "12.5 μm → 3200 (0x0C80)";
            EXAMPLE_2: "8.0 μm → 2048 (0x0800)";
            EXAMPLE_3: "0.5 μm → 128 (0x0080)";
        };
        
        RANGE_CHECK: {
            MAX_VALUE: "255.99 μm";
            REASON: "Q8.8は8ビット整数部なので、256以上は表現不可";
            IF_EXCEED: "エラー『長さが表現範囲を超えています』";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 2-3. 圧力の変換（kPa → Q8.8）
    
    // ───────────────────────────────────────
    
    CONVERSION: PRESSURE_kPa_to_Q8_8 {
        FORMULA: "Q8_8 = kPa × 256";
        
        EXAMPLES: {
            EXAMPLE_1: "2.5 kPa → 640 (0x0280)";
            EXAMPLE_2: "1.0 kPa → 256 (0x0100)";
            EXAMPLE_3: "0.1 kPa → 26 (0x001A)";
        };
        
        PRECISION: {
            RESOLUTION: "1 / 256 = 0.0039 kPa（約4 Pa）";
            NOTE: "医療測定の精度（±0.1 kPa程度）に対して十分";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 2-4. 粘性係数の変換（Pa·s → Q8.8）
    
    // ───────────────────────────────────────
    
    CONVERSION: VISCOSITY_Pas_to_Q8_8 {
        FORMULA: "Q8_8 = (Pa·s) × 256";
        
        EXAMPLES: {
            EXAMPLE_1: "0.05 Pa·s → 13 (0x000D)";
            EXAMPLE_2: "0.1 Pa·s → 26 (0x001A)";
            EXAMPLE_3: "1.0 Pa·s → 256 (0x0100)";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 2-5. Q8.8 → 実数の逆変換
    
    // ───────────────────────────────────────
    
    CONVERSION: Q8_8_to_FLOAT {
        FORMULA: "実数 = Q8_8 / 256.0";
        
        EXAMPLES: {
            EXAMPLE_1: "0x0280 (640) → 640 / 256 = 2.5";
            EXAMPLE_2: "0x0100 (256) → 256 / 256 = 1.0";
            EXAMPLE_3: "0x001A (26) → 26 / 256 = 0.1016";
        };
        
        USE_CASE: "表示用、レポート生成時に実数に戻す";
    };
}


// ═══════════════════════════════════════════

// 3. 命名規則

// ═══════════════════════════════════════════

DICTIONARY: NAMING_CONVENTION {
    

    // ───────────────────────────────────────
    
    // 3-1. プレフィックス（接頭辞）
    
    // ───────────────────────────────────────
    
    PREFIX: {
        I_: {
            CLINICAL_ROLE: "Input register（入力レジスタ）";
            USAGE: "外部から与えられるパラメータ";
            EXAMPLES: ["i_cell_stiffness", "i_pore_size", "i_drug_boost"];
        };
        
        O_: {
            CLINICAL_ROLE: "Output register（出力レジスタ）";
            USAGE: "外部に返す結果";
            EXAMPLES: ["o_is_jammed", "o_optimal_boost"];
        };
        
        W_: {
            CLINICAL_ROLE: "Wire（内部配線、組み合わせ回路）";
            USAGE: "内部の中間計算値（レジスタではない）";
            EXAMPLES: ["w_total_stiffness", "w_deformation", "w_resist_force"];
        };
        
        R_: {
            CLINICAL_ROLE: "Register（内部レジスタ、順序回路）";
            USAGE: "クロック同期で値が保持される内部レジスタ";
            EXAMPLES: ["r_state", "r_counter"];
        };
        
        T_: {
            CLINICAL_ROLE: "Testbench signal（テストベンチ信号）";
            USAGE: "シミュレーション用の信号";
            EXAMPLES: ["t_cell_stiffness", "t_is_jammed"];
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 3-2. サフィックス（接尾辞）
    
    // ───────────────────────────────────────
    
    SUFFIX: {
        _KPA: {
            CLINICAL_ROLE: "単位がキロパスカル（kPa）";
            EXAMPLES: ["cell_stiffness_kPa", "drug_boost_kPa"];
        };
        
        _UM: {
            CLINICAL_ROLE: "単位がマイクロメートル（μm）";
            EXAMPLES: ["cell_diameter_um", "pore_size_um"];
        };
        
        _PA_S: {
            CLINICAL_ROLE: "単位がパスカル秒（Pa·s）";
            EXAMPLES: ["cell_viscosity_Pa_s"];
        };
        
        _N: {
            CLINICAL_ROLE: "単位がニュートン（N）";
            EXAMPLES: ["resist_force_N", "push_force_N"];
        };
        
        _Q8_8: {
            CLINICAL_ROLE: "Q8.8固定小数点形式";
            EXAMPLES: ["stiffness_Q8_8", "boost_Q8_8"];
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 3-3. 禁止用語
    
    // ───────────────────────────────────────
    
    FORBIDDEN_WORDS: {
        DISTANCE_BASED: {
            WORDS: ["distance_force", "gap_to_force", "length_derived_tension"];
            REASON: "距離から力を導出する命名は因果ダイオード違反";
            ALTERNATIVE: "constraint_force, contact_tension";
        };
        
        AVERAGE: {
            WORDS: ["average_stiffness", "mean_boost", "typical_pressure"];
            REASON: "平均を示唆する命名は最悪ケース計算の原則に反する";
            ALTERNATIVE: "min_stiffness, max_boost, worst_case_pressure";
        };
        
        ESTIMATE: {
            WORDS: ["estimated_force", "approx_resistance", "guess_value"];
            REASON: "推定を示唆する命名は厳密計算の原則に反する";
            ALTERNATIVE: "calculated_force, exact_resistance, determined_value";
        };
        
        FUZZY: {
            WORDS: ["maybe_safe", "probably_jammed", "likely_blocked"];
            REASON: "曖昧さを示唆する命名はFail-Closed原則に反する";
            ALTERNATIVE: "is_safe (Boolean), is_jammed (Boolean)";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 3-4. 推奨される命名パターン
    
    // ───────────────────────────────────────
    
    RECOMMENDED_PATTERNS: {
        PHYSICAL_QUANTITIES: {
            PATTERN: "{prefix}_{substance}_{property}_{suffix}";
            EXAMPLES: {
                EXAMPLE_1: "i_cell_stiffness_kPa";
                EXAMPLE_2: "w_total_resistance_N";
                EXAMPLE_3: "o_optimal_boost_Q8_8";
            };
        };
        
        BOOLEAN_FLAGS: {
            PATTERN: "{prefix}_is_{state}";
            EXAMPLES: {
                EXAMPLE_1: "o_is_jammed";
                EXAMPLE_2: "w_is_contact";
                EXAMPLE_3: "r_is_overflow";
            };
        };
        
        CALCULATION_STEPS: {
            PATTERN: "{prefix}_{step_name}_{stage}";
            EXAMPLES: {
                EXAMPLE_1: "w_elastic_force_stage1";
                EXAMPLE_2: "w_viscous_resistance_stage2";
                EXAMPLE_3: "w_total_force_stage3";
            };
        };
    };
}


// ═══════════════════════════════════════════

// 4. 状態出力の定義

// ═══════════════════════════════════════════

DICTIONARY: STATUS_OUTPUT {
    

    // ───────────────────────────────────────
    
    // 4-1. 判定結果（Enum）
    
    // ───────────────────────────────────────
    
    ENUM: JUDGMENT_RESULT {
        SAFE: {
            VALUE: 0b1;
            CLINICAL_ROLE: "物理的封鎖成立。抵抗力 > 圧力";
            COLOR: "緑（Green）";
            UI_DISPLAY: "✓ SAFE";
            CLINICAL_ACTION: "この条件で治療継続可能";
        };
        
        DANGER: {
            VALUE: 0b0;
            CLINICAL_ROLE: "通過リスクあり。または幾何学的・力学的不成立";
            COLOR: "赤（Red）";
            UI_DISPLAY: "✗ DANGER";
            CLINICAL_ACTION: "追加検査、薬液量調整、または治療方針変更";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 4-2. 警告レベル（Enum）
    
    // ───────────────────────────────────────
    
    ENUM: ALERT_LEVEL {
        NORMAL: {
            VALUE: 0;
            CLINICAL_ROLE: "公理内動作。物理的保証あり";
            COLOR: "緑";
            UI_DISPLAY: "正常動作範囲";
        };
        
        CAUTION: {
            VALUE: 1;
            CLINICAL_ROLE: "閾値接近。注意が必要";
            COLOR: "黄";
            UI_DISPLAY: "⚠ 注意";
            TRIGGER: "RED ZONE まで 10%以内";
        };
        
        RED_ZONE: {
            VALUE: 2;
            CLINICAL_ROLE: "公理外領域。物理的保証なし";
            COLOR: "赤";
            UI_DISPLAY: "⚠⚠ RED ZONE";
            ACTION: "状態指示機械モードへ移行";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 4-3. エラーコード
    
    // ───────────────────────────────────────
    
    ENUM: ERROR_CODE {
        NO_ERROR: {
            VALUE: 0x00;
            CLINICAL_ROLE: "エラーなし";
        };
        
        GEOMETRIC_BYPASS: {
            VALUE: 0x01;
            CLINICAL_ROLE: "幾何学的すり抜けリスク（細胞 < 隙間）";
            MESSAGE: "細胞が血管隙間より小さいため、物理的封鎖不可能";
        };
        
        NEGATIVE_STIFFNESS: {
            VALUE: 0x02;
            CLINICAL_ROLE: "細胞硬度が負";
            MESSAGE: "細胞硬度が負の値です。データ入力を確認してください";
        };
        
        ZERO_VISCOSITY: {
            VALUE: 0x03;
            CLINICAL_ROLE: "水分粘性がゼロまたは未定義";
            MESSAGE: "水分粘性が未定義です。生命計算には必須です";
        };
        
        OVERFLOW: {
            VALUE: 0x04;
            CLINICAL_ROLE: "演算オーバーフロー";
            MESSAGE: "計算範囲を超えました。パラメータを見直してください";
        };
        
        PRESSURE_UNKNOWN: {
            VALUE: 0x05;
            CLINICAL_ROLE: "血流圧力データ欠落";
            MESSAGE: "血流圧力が未測定です。測定してから再計算してください";
        };
    };
}


// ═══════════════════════════════════════════

// 5. 辞書の使用方法

// ═══════════════════════════════════════════

USAGE_GUIDE: {
    
    // ───────────────────────────────────────
    // 5-1. 医師向け
    // ───────────────────────────────────────
    FOR_PHYSICIANS: {
        PURPOSE: "患者データ入力時、結果解釈時の参照";
        
        STEP_1_INPUT: {
            ACTION: "測定値を入力する";
            REFERENCE: "PHYSICAL_VARIABLESセクションで、各変数の意味と単位を確認";
            EXAMPLE: "細胞硬度1.5kPa → i_cell_stiffness = 1.5";
        };
        
        STEP_2_CONVERT: {
            ACTION: "単位変換（必要なら）";
            REFERENCE: "UNIT_CONVERSIONセクションで変換式を確認";
            EXAMPLE: "血圧120mmHg → 16.0kPa（参考）";
        };
        
        STEP_3_OUTPUT: {
            ACTION: "結果の解釈";
            REFERENCE: "STATUS_OUTPUTセクションで、SAFE/DANGERの意味を確認";
            EXAMPLE: "SAFE → 物理的封鎖成立。治療継続可能";
        };
    };
    

    // ───────────────────────────────────────
    
    // 5-2. エンジニア向け
    
    // ───────────────────────────────────────
    
    FOR_ENGINEERS: {
        PURPOSE: "実装時の命名統一、型チェック";
        
        STEP_1_VARIABLE: {
            ACTION: "変数を定義する";
            REFERENCE: "NAMING_CONVENTIONセクションでプレフィックスを選択";
            EXAMPLE: "入力なら i_, 中間なら w_, 出力なら o_";
        };
        
        STEP_2_TYPE: {
            ACTION: "データ型を決定";
            REFERENCE: "PHYSICAL_VARIABLESセクションでRANGE_Q8_8を確認";
            EXAMPLE: "i_cell_stiffness は Q8.8 (16bit)";
        };
        
        STEP_3_CHECK: {
            ACTION: "コンパイル時に辞書との照合";
            REFERENCE: "辞書にない名前が使われていたらエラー";
            ENFORCEMENT: "自動チェックスクリプトを実行";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 5-3. 研究者向け
    
    // ───────────────────────────────────────
    
    FOR_RESEARCHERS: {
        PURPOSE: "論文執筆時の用語統一";
        
        STEP_1_TERMINOLOGY: {
            ACTION: "用語を統一する";
            REFERENCE: "CLINICAL_NAME_ENセクションで英語名を確認";
            EXAMPLE: "Cell Stiffness (Elastic Modulus)";
        };
        
        STEP_2_UNIT: {
            ACTION: "単位を明記";
            REFERENCE: "UNIT_SIセクションでSI単位を確認";
            EXAMPLE: "Stiffness: 1.5 kPa";
        };
        
        STEP_3_CITE: {
            ACTION: "測定方法を引用";
            REFERENCE: "MEASUREMENT_METHODセクションで手法を確認";
            EXAMPLE: "Stiffness was measured using ultrasound elastography";
        };
    };
}


// ═══════════════════════════════════════════

// 6. 次の章への接続

// ═══════════════════════════════════════════

NEXT_PHASE: {
    CURRENT_UNDERSTANDING: "全ての変数・単位・命名規則を統一的に理解した";
    
    NEXT_TOPIC: "PHASE_5: システムアーキテクチャ";
    NEXT_QUESTION: [
        "なぜFPGAを選択したのか？ GPUではダメなのか？",
        "データフローはどうなっているのか？",
        "Type A/B の切り替えはどう実装するのか？"
    ];
    
    PREREQUISITE_CHECK: {
        QUESTION_1: "全ての変数名と単位が理解できたか？";
        QUESTION_2: "Q8.8固定小数点の変換方法が理解できたか？";
        QUESTION_3: "命名規則のプレフィックス（i_, o_, w_）の意味が理解できたか？";
        
        IF_NO: "Phase 4を再読。または辞書を印刷して手元に置く";
        IF_YES: "Phase 5へ進む";
    }
}
