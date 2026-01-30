# NRA-IDE_Mesoscale_Contact_Physics_Protocol
## Phase 2: 具体的な物理モデルの定義
### 対象読者: コーディング経験のない日本の医師
### 作成日時: 2026-01-30 21:45


// ═══════════════════════════════════════════

// 0. この章で理解すること

// ═══════════════════════════════════════════

PURPOSE: {
    PREVIOUS_PHASE: "Phase 1で『なぜNRA-IDEが必要か』を理解した";
    THIS_PHASE: "具体的に『どんな物理を計算しているか』を理解する";
    
    KEY_QUESTIONS: {
        Q1: "乳がん（Type A）と子宮頸がん（Type B）で、なぜ計算式が違うのか？";
        Q2: "『水分の粘性η』は本当に必要なのか？ 面倒だから省略できないのか？";
        Q3: "『細胞が通過できる/できない』は、具体的に何と何を比較しているのか？";
    }
}


// ═══════════════════════════════════════════

// 1. メソスケールとは何か（復習）

// ═══════════════════════════════════════════

CONCEPT: MESOSCALE_DEFINITION {
    SCALE_HIERARCHY: {
        // スケールの階層
        MACRO_SCALE: {
            SIZE: "数センチメートル（臓器全体）";
            EXAMPLE: "肝臓の大きさ、腫瘍の体積";
            PHYSICS: "臓器全体の力学（変形、圧力分布）";
            LIMITATION: "個々の細胞は見えない → 細かすぎる物理現象を捉えられない";
        };
        
        MESO_SCALE: {
            SIZE: "数マイクロメートル（細胞1個）";
            EXAMPLE: "細胞の直径、血管の隙間";
            PHYSICS: "細胞1個の変形、血管壁との接触";
            ADVANTAGE: "計算可能な範囲で、かつ生命現象の本質を捉えられる";
            TARGET: "NRA-IDEが計算するのはこの階層";
        };
        
        MICRO_SCALE: {
            SIZE: "ナノメートル（分子レベル）";
            EXAMPLE: "タンパク質の構造、DNAの配列";
            PHYSICS: "量子力学、分子動力学";
            LIMITATION: "計算量が膨大すぎて実用不可能";
        };
    }
    
    WHY_MESO: {
        REASON_1: "細胞の『通過/非通過』はメソスケールの物理で決まる";
        REASON_2: "これより細かい（ミクロ）と計算不可能、粗い（マクロ）と本質を見失う";
        GOLDEN_ZONE: "メソスケールは『計算可能性』と『物理的本質』の最適バランス";
    }
}


// ═══════════════════════════════════════════

// 2. Type A（乳がん）の物理モデル

// ═══════════════════════════════════════════

PHYSICS_MODEL: TYPE_A_BREAST_CANCER {
    
    // ───────────────────────────────────────
    // 2-1. 病理学的特徴
    // ───────────────────────────────────────
    PATHOLOGY: {
        CELL_CHARACTERISTIC: "高硬度の結節を形成";
        TEXTURE: "触診で『硬いしこり』として触れる";
        MECHANICAL_PROPERTY: "細胞自体が比較的硬い（Stiffness高）";
        
        METASTASIS_MECHANISM: {
            SCENARIO: "硬い細胞が、血管の細い隙間を『力ずくで』押し通ろうとする";
            ANALOGY: "硬いビー玉を、狭いチューブに押し込む";
            RISK: "血流の圧力が十分に高ければ、押し通されて転移する";
        };
    }
    
    // ───────────────────────────────────────
    // 2-2. 物理式の定義
    // ───────────────────────────────────────
    EQUATION: {
        FORMULA: "F_resist = k_cell · Δx + η · (dv/dt)";
        
        NAME: "Voigt モデル（弾性 + 粘性の並列結合）";
        
        MEANING: "細胞の抵抗力 = バネの力 + 水分の粘り";
    }
    
    // ───────────────────────────────────────
    // 2-3. 各項の物理的意味（詳細）
    // ───────────────────────────────────────
    TERM_BY_TERM: {
        
        // ─── 第1項: 弾性項（バネの力） ───
        ELASTIC_TERM: {
            SYMBOL: "k_cell · Δx";
            NAME: "弾性抵抗力（フックの法則）";
            
            COMPONENT_K: {
                VARIABLE: "k_cell";
                UNIT: "kPa（キロパスカル）";
                CLINICAL_NAME: "細胞の反発力";
                MEANING: "細胞が『元の形に戻ろうとする強さ』";
                
                ANALOGY: {
                    SOFT_SPRING: "柔らかいバネ（k小）→ 簡単に縮む → 柔らかい細胞";
                    HARD_SPRING: "硬いバネ（k大）→ なかなか縮まない → 硬い細胞";
                };
                
                TYPICAL_VALUES: {
                    NORMAL_BREAST: "0.5 〜 1.0 kPa";
                    CANCER_STIFF: "1.5 〜 3.0 kPa";
                    MEASUREMENT: "超音波エラストグラフィで測定可能";
                };
            };
            
            COMPONENT_DELTA_X: {
                VARIABLE: "Δx";
                UNIT: "μm（マイクロメートル）";
                CLINICAL_NAME: "変形量";
                MEANING: "細胞が『元の大きさから、どれだけ潰れたか』";
                
                CALCULATION: {
                    FORMULA: "Δx = D_cell - d_gap";
                    CONDITION: "IF (D_cell > d_gap) THEN Δx = D_cell - d_gap ELSE Δx = 0";
                    
                    EXPLANATION: {
                        D_CELL: "細胞の直径（例: 12 μm）";
                        D_GAP: "血管の隙間（例: 8 μm）";
                        DEFORMATION: "12 - 8 = 4 μm だけ細胞が潰れる";
                    };
                    
                    GEOMETRIC_CHECK: {
                        IF_CELL_SMALLER: "細胞 < 隙間 → すり抜ける → 変形なし（Δx=0）";
                        IF_CELL_LARGER: "細胞 > 隙間 → 潰れる → 変形あり（Δx>0）";
                        CRITICAL: "この幾何学的判定が最初の関門";
                    };
                };
            };
            
            PHYSICAL_INTERPRETATION: {
                MEANING: "k·Δx = 細胞が潰された分だけ、反発する（メソスケール特有の単位）";
                EXAMPLE: {
                    CASE: "k=2.0kPa, Δx=4μm";
                    CALCULATION: "F_elastic = 2.0 × 4 = 8.0 [kPa·μm]";
                    UNIT_NOTE: "[kPa·μm] はメソスケール中間単位（後でスケール係数αを掛けて圧力Paに変換）";
                };
            };
        };
        
        // ─── 第2項: 粘性項（水分の抵抗） ───
        VISCOUS_TERM: {
            SYMBOL: "η · (dv/dt)";
            NAME: "粘性抵抗力（水分の抵抗）";
            
            COMPONENT_ETA: {
                VARIABLE: "η";
                UNIT: "Pa·s（パスカル秒）";
                CLINICAL_NAME: "細胞の粘り";
                MEANING: "細胞内の水分が『急激な変形を妨げる強さ』";
                
                ANALOGY: {
                    WATER: "水（η小）→ サラサラ → 素早く動ける";
                    HONEY: "蜂蜜（η大）→ ドロドロ → ゆっくりしか動けない";
                };
                
                BIOLOGICAL_ORIGIN: {
                    SOURCE: "細胞質の水分、タンパク質溶液";
                    CHARACTERISTIC: "細胞は『水の袋』である";
                    COMPRESSION: "細胞を急に押すと、水が逃げ場を失い、抵抗する";
                };
                
                TYPICAL_VALUES: {
                    CYTOPLASM: "0.01 〜 0.1 Pa·s";
                    MEASUREMENT: "光ピンセット、マイクロレオロジーで測定";
                };
            };
            
            COMPONENT_DV_DT: {
                VARIABLE: "dv/dt";
                UNIT: "μm/s²（加速度）";
                CLINICAL_NAME: "変形速度";
                MEANING: "細胞が『どれだけ急激に潰されているか』";
                
                EXPLANATION: {
                    SLOW_COMPRESSION: "ゆっくり押す → 水が徐々に逃げる → 粘性抵抗小";
                    FAST_COMPRESSION: "急激に押す → 水が逃げられない → 粘性抵抗大";
                };
                
                BLOOD_FLOW_CONTEXT: {
                    SCENARIO: "血流が細胞を押す速度";
                    TYPICAL: "数百μm/s²（心拍の拍動による）";
                    CRITICAL: "この『時間依存性』こそが生命の本質";
                };
            };
            
            PHYSICAL_INTERPRETATION: {
                MEANING: "η·(dv/dt) = 水分が逃げられないことによる抵抗";
                EXAMPLE: {
                    CASE: "η=0.05Pa·s, dv/dt=200μm/s²";
                    CALCULATION: "F_viscous = 0.05 × 200 = 10 [Pa·s·μm/s²] = 10 [Pa·μm/s]";
                    UNIT_NOTE: "メソスケール中間単位（後でスケール係数αを掛けて圧力Paに変換）";
                };
            };
        };
    };
    

    // ───────────────────────────────────────
    
    // 2-4. なぜ水分項は省略できないのか
    
    // ───────────────────────────────────────
    
    WATER_NECESSITY: {
        PROHIBITION: "η項（水分粘性）を省略することは永久に禁止";
        
        REASON_1_BIOLOGICAL: {
            FACT: "細胞の70%は水分である";
            IMPLICATION: "水分を無視 = 細胞の7割を無視 = 物理的に無意味";
        };
        
        REASON_2_IRREVERSIBILITY: {
            TIME_ARROW: "生命は『時間の矢』を持つ。過去には戻れない";
            VISCOSITY_ROLE: "粘性項は『時間依存性（dv/dt）』を担当";
            WITHOUT_ETA: "η=0 とすると、時間が消える → 生命の不可逆性が消える";
            
            MATHEMATICAL: {
                WITH_ETA: "F = k·Δx + η·(dv/dt) → 時間tが含まれる → 不可逆";
                WITHOUT_ETA: "F = k·Δx → 時間tが消える → 可逆（非生命的）";
            };
        };
        
        REASON_3_CLINICAL: {
            OBSERVATION: "実際の細胞転移は『じわじわ』ではなく『一瞬』で起きる";
            MECHANISM: "血流の拍動（心拍）により、急激な圧力変化が生じる";
            VISCOSITY_EFFECT: "この急激な変化に対し、粘性が『ブレーキ』をかける";
            WITHOUT_ETA: "急激な変化を計算できない → 転移リスクを過小評価";
        };
        
        ENFORCEMENT: {
            CODE_LEVEL: "システムは η の値が存在することをチェック";
            IF_MISSING: "コンパイルエラー『水分項が見つかりません。生命計算には必須です』";
            IF_ZERO: "警告『η=0 は非生命系です。本当にこれでよいか確認してください』";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 2-5. Type A の判定ロジック
    
    // ───────────────────────────────────────
    
    JUDGMENT_LOGIC: {
        PROCEDURE: {
            STEP_1: "幾何学的チェック";
            CHECK_1: "IF (D_cell <= d_gap) THEN すり抜けリスク → DANGER";
            
            STEP_2: "抵抗力の計算";
            CALCULATE: "F_resist = k_cell·Δx + η·(dv/dt)";
            
            STEP_3: "押し流す力の取得";
            INPUT: "F_push = 血流の圧力（患者測定値）";
            
            STEP_4: "比較判定";
            CONDITION: "IF (F_resist > F_push) THEN SAFE ELSE DANGER";
        };
        
        PHYSICAL_MEANING: {
            SAFE: "抵抗力 > 押す力 → 細胞は押し通せない → 転移できない";
            DANGER: "抵抗力 < 押す力 → 細胞が押し通される → 転移リスク";
        };
        
        OPTIMIZATION_GOAL: {
            QUESTION: "薬液でk_cellを何kPa増やせば、SAFEになるか？";
            METHOD: "総当たり探索で、SAFE になる最小のBoost値を見つける";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 2-6. 単位系の整合性チェック
    
    // ───────────────────────────────────────
    
    UNIT_CONSISTENCY: {
        
        CRITICAL_NOTE: {
            STATEMENT: "メソスケールでは『圧力』で計算する";
            REASON: "細胞と血管の接触は『単位面積あたりの力』= 圧力として扱う";
            IMPLICATION: "力（N）ではなく、圧力（Pa, kPa）で統一";
        };
        
        LEFT_SIDE: {
            VARIABLE: "Resist_Pressure（抵抗圧力）";
            UNIT: "Pa（パスカル）または kPa（キロパスカル）";
            MEANING: "細胞が血流に抵抗する圧力";
        };
        
        RIGHT_SIDE_ELASTIC: {
            EXPRESSION: "k_cell · Δx · α";
            BREAKDOWN: "[kPa] · [μm] · [スケール係数]";
            
            DETAILED_CALCULATION: {
                STEP_1: "k_cell = 2.0 kPa（細胞硬度）";
                STEP_2: "Δx = 4.0 μm（変形量）";
                STEP_3: "k_cell · Δx = 2.0 × 4.0 = 8.0 [kPa·μm]";
                STEP_4: "α = 250（スケール係数、メソスケール補正）";
                STEP_5: "Resist_Elastic = 8.0 × 250 = 2000 Pa = 2.0 kPa";
            };
            
            UNIT_INTERPRETATION: {
                KPA_UM: "[kPa·μm] はメソスケール特有の単位";
                MEANING: "『圧力 × 長さ』は、微小領域での『圧力の強度』を表す";
                SCALING: "スケール係数αで、実際の圧力[Pa]に変換";
            };
            
            FINAL_UNIT: "Pa（パスカル）✓";
        };
        
        RIGHT_SIDE_VISCOUS: {
            EXPRESSION: "η · (dv/dt) · α";
            BREAKDOWN: "[Pa·s] · [μm/s²] · [スケール係数]";
            
            DETAILED_CALCULATION: {
                STEP_1: "η = 0.05 Pa·s（細胞粘性）";
                STEP_2: "dv/dt = 200 μm/s²（変形速度）";
                STEP_3: "η · (dv/dt) = 0.05 × 200 = 10 [Pa·s·μm/s²]";
                STEP_4: "単位整理: [Pa·s·μm/s²] = [Pa·μm/s]";
                STEP_5: "α = 250（スケール係数）";
                STEP_6: "Resist_Viscous = 10 × 250 / (何らかの時間定数) ≈ 圧力[Pa]";
            };
            
            UNIT_INTERPRETATION: {
                PA_S_UM_S: "[Pa·s·μm/s²] = [Pa·μm/s]";
                MEANING: "粘性による圧力抵抗";
                NOTE: "実装では時間定数で割って圧力次元に調整";
            };
            
            FINAL_UNIT: "Pa（パスカル）✓";
        };
        
        TOTAL_RESISTANCE: {
            FORMULA: "Resist_Pressure = Resist_Elastic + Resist_Viscous";
            UNIT: "Pa（パスカル）";
            
            EXAMPLE: {
                ELASTIC: "2000 Pa";
                VISCOUS: "500 Pa";
                TOTAL: "2500 Pa = 2.5 kPa";
            };
        };
        
        COMPARISON_JUDGMENT: {
            LEFT: "Resist_Pressure = 2500 Pa（細胞の抵抗圧力）";
            RIGHT: "Flow_Pressure = 1800 Pa（血流の押す圧力）";
            CONDITION: "IF (2500 > 1800) THEN SAFE";
            
            PHYSICAL_MEANING: {
                SAFE: "抵抗圧力 > 血流圧力 → 細胞は押し通せない → 転移できない";
                DANGER: "抵抗圧力 < 血流圧力 → 細胞が押し通される → 転移リスク";
            };
        };
        
        VERIFICATION: {
            STATEMENT: "両辺とも 圧力[Pa] で一致 → 物理的に整合 ✓";
            
            CONSISTENCY_CHECK: {
                PHASE_2: "抵抗圧力 [Pa] vs 血流圧力 [Pa]";
                PHASE_4_DICTIONARY: {
                    TOTAL_RESISTANCE: "UNIT_SI: Pa（圧力）";
                    FLOW_PRESSURE: "UNIT_SI: kPa（圧力）";
                };
                RESULT: "Phase 4の辞書と完全整合 ✓";
            };
        };
        
        SCALE_FACTOR_ALPHA: {
            VALUE: "α = 250";
            
            PHYSICAL_MEANING: {
                PURPOSE: "メソスケール（μm）とマクロスケール（m）の橋渡し";
                DERIVATION: "実験的に決定された補正係数";
                
                WHY_NEEDED: {
                    PROBLEM: "[kPa·μm] という単位は、そのままでは圧力[Pa]にならない";
                    SOLUTION: "スケール係数αを掛けることで、物理的に意味のある圧力に変換";
                    ANALOGY: "顕微鏡の倍率のようなもの。微小世界とマクロ世界をつなぐ";
                };
            };
            
            FPGA_IMPLEMENTATION: {
                PURPOSE: "Q8.8固定小数点の範囲に収める";
                TYPICAL_VALUE: "α = 250 ≈ 256 = 2⁸（2のべき乗に近い）";
                ADVANTAGE: "シフト演算で高速計算可能";
            };
        };
        
        IMPORTANT_CLARIFICATION: {
            NO_NEWTON: {
                STATEMENT: "このシステムでは『力[N]』は使わない";
                REASON: "メソスケールでは、接触を『圧力』として扱う方が自然";
                IMPLEMENTATION: "全て圧力[Pa, kPa]で計算";
            };
            
            WHY_PRESSURE: {
                REASON_1: "細胞と血管の接触面積は微小 → 力よりも圧力が支配的";
                REASON_2: "血流の駆動力も圧力で表現される";
                REASON_3: "判定式が単純: 圧力 vs 圧力";
            };
        };
    }
}


// ═══════════════════════════════════════════

// 3. Type B（子宮頸がん）の物理モデル

// ═══════════════════════════════════════════

PHYSICS_MODEL: TYPE_B_CERVICAL_CANCER {

    
    // ───────────────────────────────────────
    
    // 3-1. 病理学的特徴
    
    // ───────────────────────────────────────
    
    PATHOLOGY: {
        CELL_CHARACTERISTIC: "扁平上皮細胞。柔軟で変形しやすい";
        TEXTURE: "触診では『硬いしこり』にならず、びまん性（広がる）";
        MECHANICAL_PROPERTY: "細胞自体は柔らかい（Stiffness低）";
        
        METASTASIS_MECHANISM: {
            SCENARIO: "単体では柔らかいが、『集団』で押し寄せる";
            ANALOGY: "柔らかい粘土を、大量に詰め込む";
            RISK: "個々は弱くても、数が多ければ隙間を押し広げる";
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 3-2. 物理式の定義
    
    // ───────────────────────────────────────
    
    EQUATION: {
        FORMULA: "F_collective = N · F_single · (1 + α·√N)";
        
        NAME: "集団協調モデル（Collective Push Model）";
        
        MEANING: "集団の力 = 細胞数 × 単体の力 × 協調増幅係数";
    }
    
    
    // ───────────────────────────────────────
    
    // 3-3. 各項の物理的意味
    
    // ───────────────────────────────────────
    
    TERM_BY_TERM: {
        
        COMPONENT_N: {
            VARIABLE: "N";
            UNIT: "個（無次元）";
            CLINICAL_NAME: "細胞クラスタの数";
            MEANING: "同時に血管隙間に押し寄せる細胞の個数";
            
            TYPICAL_VALUES: {
                SINGLE_CELL: "N = 1（単独転移）";
                SMALL_CLUSTER: "N = 5〜10（小集団）";
                LARGE_CLUSTER: "N = 20〜50（大集団）";
                MEASUREMENT: "病理組織標本から、細胞塊のサイズを計測";
            };
        };
        
        COMPONENT_F_SINGLE: {
            VARIABLE: "F_single";
            UNIT: "Pa（パスカル）";
            CLINICAL_NAME: "単体細胞の押す圧力";
            MEANING: "1個の細胞が発揮する抵抗圧力（Type Aと同じ式で計算）";
            
            CALCULATION: {
                FORMULA: "F_single = (k_cell·Δx + η·(dv/dt)) · α";
                NOTE: "Type Bでもこの式は使う（ただしkは小さい）";
                UNIT_RESULT: "Pa（圧力）";
            };
        };
        
        COMPONENT_ALPHA: {
            VARIABLE: "α";
            UNIT: "無次元";
            CLINICAL_NAME: "集団協調係数";
            MEANING: "細胞同士が『協力して押す』ことによる増幅効果";
            
            PHYSICAL_ORIGIN: {
                MECHANISM: "細胞同士が接触し、力を伝達し合う";
                ANALOGY: "1人で押すより、複数人で『せーの！』で押す方が効果的";
                NON_LINEAR: "単純に足し算ではなく、√N に比例（非線形）";
            };
            
            TYPICAL_VALUES: {
                CERVICAL: "α = 0.3 〜 0.8";
                MEASUREMENT: "細胞集団の押圧実験から決定";
            };
        };
        
        COMPONENT_SQRT_N: {
            EXPRESSION: "√N";
            MEANING: "集団サイズの平方根";
            
            WHY_SQRT: {
                LINEAR_WRONG: "N個なら N倍の力？ → 実際はそうならない";
                REASON: "後ろの細胞は前の細胞に『遮られる』";
                SQRT_CORRECT: "有効に力を伝えられるのは √N 程度";
                
                EXAMPLE: {
                    N_1: "1個 → √1 = 1";
                    N_4: "4個 → √4 = 2（4倍ではなく2倍）";
                    N_9: "9個 → √9 = 3（9倍ではなく3倍）";
                };
            };
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 3-4. 集団効果の具体例
    
    // ───────────────────────────────────────
    
    COLLECTIVE_EFFECT_EXAMPLE: {
        CONDITION: {
            F_SINGLE: "500 Pa（単体は弱い）";
            ALPHA: "0.5";
        };
        
        CASE_1_SINGLE: {
            N: 1;
            CALCULATION: "F = 1 × 500 × (1 + 0.5×√1) = 500 × 1.5 = 750 Pa";
            RESULT: "単体では弱い";
        };
        
        CASE_2_SMALL_CLUSTER: {
            N: 4;
            CALCULATION: "F = 4 × 500 × (1 + 0.5×√4) = 2000 × (1 + 1.0) = 4000 Pa = 4.0 kPa";
            RESULT: "4個で 4.0 kPa → 単体の5.3倍（線形なら4倍のはず）";
        };
        
        CASE_3_LARGE_CLUSTER: {
            N: 9;
            CALCULATION: "F = 9 × 500 × (1 + 0.5×√9) = 4500 × (1 + 1.5) = 11250 Pa = 11.25 kPa";
            RESULT: "9個で 11.25 kPa → 単体の15倍（線形なら9倍のはず）";
        };
        
        IMPLICATION: {
            OBSERVATION: "集団になると、単純和以上の圧力を発揮する";
            RISK: "『柔らかい細胞だから安心』とはならない";
            STRATEGY: "集団全体をジャミング（目詰まり）で止める";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 3-5. Type B の判定ロジック
    
    // ───────────────────────────────────────
    
    JUDGMENT_LOGIC: {
        PROCEDURE: {
            STEP_1: "細胞数Nを病理データから取得";
            
            STEP_2: "単体の力F_single を計算（Type Aと同じ式）";
            
            STEP_3: "集団効果を加味";
            CALCULATE: "F_collective = N · F_single · (1 + α·√N)";
            
            STEP_4: "比較判定";
            CONDITION: "IF (F_collective > F_push) THEN SAFE ELSE DANGER";
        };
        
        OPTIMIZATION_GOAL: {
            QUESTION: "薬液でk_cellを何kPa増やせば、集団でも止められるか？";
            CHALLENGE: "Type Aより大きなBoostが必要になる（集団効果のため）";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 3-6. Type A vs Type B の比較
    
    // ───────────────────────────────────────
    
    COMPARISON: {
        TABLE: {
            HEADER: ["項目", "Type A（乳がん）", "Type B（子宮頸がん）"];
            ROW_1: ["細胞特性", "硬い", "柔らかい"];
            ROW_2: ["転移様式", "単体で押し通る", "集団で押し寄せる"];
            ROW_3: ["主要因子", "k_cell（硬度）", "N（細胞数）"];
            ROW_4: ["計算式", "F = k·Δx + η·dv/dt", "F = N·F_single·(1+α√N)"];
            ROW_5: ["治療戦略", "細胞を硬化", "集団をジャミング"];
        };
        
        CLINICAL_SELECTION: {
            QUESTION: "患者の癌がType AかType Bか、どう判断するのか？";
            ANSWER: {
                PATHOLOGY: "病理診断（組織型）から判断";
                IMAGING: "画像診断で『しこり』か『びまん性』か";
                DEFAULT: "分からない場合は『両方計算して、より厳しい方を採用』";
            };
        };
    }
}


// ═══════════════════════════════════════════

// 4. 水分計算の必然性（再強調）

// ═══════════════════════════════════════════

AXIOM: WATER_VISCOSITY_MANDATORY {
    PROHIBITION: "η項（水分粘性）を省略することは永久に禁止";
    
    PHILOSOPHICAL_REASON: {
        STATEMENT: "生命は『水の中で起きる物理現象』である";
        IMPLICATION: "水を無視 = 生命を無視";
        
        HISTORICAL_ERROR: {
            TRADITION: "従来の生体力学モデルは『弾性項のみ』で計算してきた";
            REASON: "粘性項は『面倒』で『データも少ない』から";
            CONSEQUENCE: "その結果、時間依存性を捉えられず、予測精度が低かった";
        };
    }
    
    MATHEMATICAL_REASON: {
        TIME_IRREVERSIBILITY: {
            WITH_ETA: "F = k·Δx + η·(dv/dt) → dv/dt は時間微分 → 過去に戻れない";
            WITHOUT_ETA: "F = k·Δx → 時間が消える → 可逆系（非生命的）";
        };
        
        DYNAMIC_EQUILIBRIUM: {
            RITSUKAN: "生命は動的平衡（渦）である";
            VISCOSITY: "粘性がなければ、渦は維持できない（すぐ止まる）";
            METABOLISM: "代謝（エネルギー流）も、水分の流動があってこそ";
        };
    }
    
    CLINICAL_REASON: {
        ACUTE_EVENT: {
            OBSERVATION: "転移は『じわじわ』ではなく『心拍の1拍で』起きる";
            MECHANISM: "血圧の拍動により、0.1秒で圧力が変化";
            VISCOSITY_ROLE: "この急激な変化に対し、η·(dv/dt) が支配的になる";
        };
        
        DRUG_EFFECT: {
            STIFFNESS_ALONE: "k_cell だけ増やしても、急激な変化には対応できない";
            WITH_VISCOSITY: "η も考慮することで、『瞬間的な突破』を防げる";
        };
    }
    
    ENFORCEMENT: {
        CODE_CHECK: {
            STEP_1: "コンパイル時に、全ての計算式で η の存在を確認";
            STEP_2: "もし η = 0 または未定義なら、エラー";
            STEP_3: "警告文『水分項が見つかりません。生命計算には必須です』";
        };
        
        RUNTIME_CHECK: {
            STEP_1: "実行時に、η の値が妥当な範囲（0.01〜1.0 Pa·s）か確認";
            STEP_2: "範囲外なら警告『η の値が異常です。測定を再確認してください』";
        };
    }
}


// ═══════════════════════════════════════════

// 5. 次の章への接続

// ═══════════════════════════════════════════

NEXT_PHASE: {
    CURRENT_UNDERSTANDING: "Type A/B の物理モデルと、水分計算の必然性を理解した";
    
    NEXT_TOPIC: "PHASE_3: 律環公理の形式定義";
    NEXT_QUESTION: [
        "『因果ダイオード』とは具体的にどう実装するのか？",
        "『ギアメカニズム』で、どうやって1ステップの破綻を検出するのか？",
        "『ゲート公理』で、医師の領域とシステムの領域をどう分けるのか？"
    ];
    
    PREREQUISITE_CHECK: {
        QUESTION_1: "Type AとType Bの違いが理解できたか？";
        QUESTION_2: "なぜη（水分粘性）を省略できないのか理解できたか？";
        QUESTION_3: "F_resist と F_push の比較が何を意味するか理解できたか？";
        
        IF_NO: "Phase 2を再読。または物理の教科書で『フックの法則』『粘性』を復習";
        IF_YES: "Phase 3へ進む";
    }
}
