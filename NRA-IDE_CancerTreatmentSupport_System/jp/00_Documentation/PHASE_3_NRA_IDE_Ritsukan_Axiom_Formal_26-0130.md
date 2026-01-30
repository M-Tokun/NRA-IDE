# NRA-IDE_Ritsukan_Circular_Axiom_Formal
### Phase 3: 律環公理（RCA）の形式定義
* 対象読者: コーディング経験のない両関係者の方
### 作成日時: 2026-01-30 22:00


// ═══════════════════════════════════════════

// 0. この章で理解すること

// ═══════════════════════════════════════════

PURPOSE: {
    PREVIOUS_PHASE: "Phase 2で『どんな物理を計算するか』を理解した";
    THIS_PHASE: "その計算を『どうやって安全に実行するか』の原理を理解する";
    
    KEY_QUESTIONS: {
        Q1: "『因果ダイオード』とは何か？ なぜ逆推論を禁止するのか？";
        Q2: "『ギアメカニズム』で、計算の破綻をどう検出するのか？";
        Q3: "『ゲート公理』で、医師の責任範囲とシステムの責任範囲をどう分けるのか？";
        Q4: "なぜ『距離ではなく制約』で計算するのか？";
    }
}


// ═══════════════════════════════════════════

// 1. 律環公理とは何か（復習と深掘り）

// ═══════════════════════════════════════════

AXIOM: RITSUKAN_FOUNDATION {
    
    // ───────────────────────────────────────
    // 1-1. 律環（Ritsukan）の語源と意味
    // ───────────────────────────────────────
    ETYMOLOGY: {
        RITSUKAN_JP: "律環（りつかん）";
        RITSU: "律 = 法則、規則";
        KAN: "環 = 循環、渦";
        COMBINED: "法則に従って循環する系";
    }
    

    // ───────────────────────────────────────
    
    // 1-2. 哲学的定義
    
    // ───────────────────────────────────────
    
    PHILOSOPHY: {
        DEFINITION: "生命は動的平衡（涅槃）にある渦である";
        
        STATIC_VS_DYNAMIC: {
            STATIC_EQUILIBRIUM: {
                EXAMPLE: "石ころ、死んだ系";
                CHARACTERISTIC: "外部から力を加えない限り、永遠に動かない";
                ENERGY: "エネルギー流入ゼロ";
                ENTROPY: "エントロピー増大が止まる（熱平衡）";
            };
            
            DYNAMIC_EQUILIBRIUM: {
                EXAMPLE: "渦巻き、炎、生命";
                CHARACTERISTIC: "常に動いているが、『形』は保たれる";
                ENERGY: "エネルギーを流し続けることで形を維持";
                ENTROPY: "エントロピーを外部に捨て続ける（散逸構造）";
                
                ANALOGY: {
                    WHIRLPOOL: "川の渦：水は流れているが、渦の形は同じ場所にある";
                    FLAME: "ロウソクの炎：分子は入れ替わるが、炎の形は保たれる";
                    CELL: "細胞：分子は代謝で入れ替わるが、細胞の形は維持される";
                };
            };
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 1-3. 数学的制約
    
    // ───────────────────────────────────────
    
    MATHEMATICAL_CONSTRAINT: {
        ROTATION: {
            SYMBOL: "ω > 0";
            MEANING: "回転（angular velocity）が正";
            IMPLICATION: "系が『動いている』ことの証";
            
            IF_OMEGA_ZERO: {
                STATE: "ω = 0";
                MEANING: "回転が止まる";
                CONSEQUENCE: "系の崩壊（死）";
                MEDICAL: "代謝が止まる = 細胞死";
            };
        };
        
        WORK: {
            SYMBOL: "Work > 0";
            MEANING: "仕事（energy input）が正";
            IMPLICATION: "系が『エネルギーを消費している』ことの証";
            
            IF_WORK_ZERO: {
                STATE: "Work = 0";
                MEANING: "エネルギー供給が止まる";
                CONSEQUENCE: "系の消滅（壊死）";
                MEDICAL: "栄養・酸素供給が止まる = 組織壊死";
            };
        };
        
        COMBINED_CONDITION: {
            FORMULA: "ω > 0 AND Work > 0";
            MEANING: "この2つが同時に満たされている = 生命";
            MEDICAL_INTERPRETATION: {
                NORMAL_CELL: "ω > 0, Work > 0 → 正常な動的平衡";
                CANCER_CELL: "ω ≫ 0, Work ≫ 0 → 異常に高い代謝（増殖）";
                TREATMENT_GOAL: "物理的封鎖により、癌細胞の『渦』を止める";
            };
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 1-4. 単位原理（距離の廃止）
    
    // ───────────────────────────────────────
    
    UNIT_PRINCIPLE: {
        ABOLISH_DISTANCE: "『距離(Distance)』を計算の基準にしない";
        USE_CONSTRAINT: "『制約(Constraint)』と『張力(Tension)』で計算する";
        
        REASON: {
            DISTANCE_IS_RESULT: "距離は物理過程の『結果』であって『原因』ではない";
            CONSTRAINT_IS_CAUSE: "制約（接触）こそが力を生む『原因』";
            
            ANALOGY: {
                WRONG_THINKING: "『2人の距離が1mだから、2人の間に力がある』";
                CORRECT_THINKING: "『2人が押し合っている（制約）から、力がある。その結果、距離が1mになった』";
            };
        };
        
        ENFORCEMENT: {
            CODE_STRUCTURE: "システム内で『距離から力を導出する』コードは書けない構造";
            COMPILER_CHECK: "もし書こうとしたら、コンパイル時にエラー";
            GUARANTEE: "構造的に因果逆転を防止";
        };
    }
}


// ═══════════════════════════════════════════

// 2. 因果ダイオード（Causal Diode）

// ═══════════════════════════════════════════

AXIOM: CAUSAL_DIODE {
    

    // ───────────────────────────────────────
    
    // 2-1. 定義
    
    // ───────────────────────────────────────
    
    DEFINITION: "因果は一方向のみ伝播。逆推論を構造的に禁止";
    
    
    // ───────────────────────────────────────
    
    // 2-2. ダイオードの比喩
    
    // ───────────────────────────────────────
    
    ANALOGY: {
        ELECTRICAL_DIODE: {
            FUNCTION: "電流を一方向にしか流さない電子部品";
            FORWARD: "順方向：電流が流れる";
            BACKWARD: "逆方向：電流が流れない（遮断）";
            APPLICATION: "交流を直流に変換（整流）";
        };
        
        CAUSAL_DIODE: {
            FUNCTION: "因果関係を一方向にしか流さない論理構造";
            FORWARD: "順方向：制約 → 力 → 距離（計算OK）";
            BACKWARD: "逆方向：距離 → 力（計算NG、エラー）";
            APPLICATION: "因果逆転の防止";
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 2-3. 正しい因果の流れ
    
    // ───────────────────────────────────────
    
    CORRECT_CAUSALITY: {
        STEP_1: "制約（Constraint）の発生";
        EXAMPLE_1: "細胞が血管壁に接触する";
        CONDITION_1: "細胞直径 > 血管隙間";
        
        STEP_2: "張力（Tension）の発生";
        EXAMPLE_2: "接触により反発力が発生する";
        PHYSICS_2: "F = k·Δx（フックの法則）";
        
        STEP_3: "距離（Distance）の変化";
        EXAMPLE_3: "力により細胞が変形する";
        RESULT_3: "変形量 Δx が観測される";
        
        SUMMARY: "制約 → 力 → 距離（この順序は絶対）";
    }
    
    
    // ───────────────────────────────────────
    
    // 2-4. 間違った逆推論（禁止）
    
    // ───────────────────────────────────────
    
    WRONG_INFERENCE: {
        STEP_1_WRONG: "距離の測定";
        EXAMPLE_1_WRONG: "CTスキャンで『腫瘍と血管の距離が2mm』と測定";
        
        STEP_2_WRONG: "力の逆算（誤り）";
        EXAMPLE_2_WRONG: "距離が2mmだから、力が○○Nかかっているはず";
        WHY_WRONG: "距離だけでは、『接触しているか』『押し合っているか』が分からない";
        
        ANALOGY: {
            SCENARIO: "2人の人間の距離が1mだとする";
            WRONG_Q: "『距離が1mだから、2人の間に何Nの力が働いているか？』";
            CORRECT_A: "分からない。押し合っているなら力がある。離れて立っているだけなら力はゼロ";
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 2-5. 実装方法
    
    // ───────────────────────────────────────
    
    IMPLEMENTATION: {
        CODE_STRUCTURE: {
            ALLOWED: {
                STEP_1: "IF (D_cell > d_gap) THEN contact = TRUE";
                STEP_2: "IF (contact) THEN F = k·Δx";
                STEP_3: "OBSERVE: Δx (結果として測定)";
                NOTE: "制約 → 力 → 距離の順";
            };
            
            FORBIDDEN: {
                STEP_1_BAD: "MEASURE: distance = 2mm";
                STEP_2_BAD: "INFER: F = some_function(distance)";
                ERROR: "距離から力を逆算しようとしている → コンパイルエラー";
            };
        };
        
        COMPILER_ENFORCEMENT: {
            RULE: "変数の依存関係を型システムで管理";
            CHECK: "もし『Distance型』から『Force型』への関数が定義されていたら、エラー";
            MESSAGE: "『因果ダイオード違反：距離から力を導出できません』";
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 2-6. 医学的意義
    
    // ───────────────────────────────────────
    
    MEDICAL_SIGNIFICANCE: {
        TRADITIONAL_IMAGING: {
            PRACTICE: "画像診断で『腫瘍のサイズ』『リンパ節との距離』を測定";
            INFERENCE: "『距離が近いから転移リスクが高い』と推測";
            LIMITATION: "しかし、距離だけでは物理的成否は分からない";
        };
        
        NRA_IDE_APPROACH: {
            MEASUREMENT: "細胞の硬さ、血管の隙間、血流の圧力を測定";
            CALCULATION: "制約（接触）→ 力（反発）→ 判定（通過可否）";
            ADVANTAGE: "物理的根拠に基づく判定";
        };
        
        CLINICAL_IMPACT: {
            BEFORE: "『この患者は転移リスクが高そう』（経験的推測）";
            AFTER: "『この患者の細胞は物理的に通過できない』（計算的保証）";
        };
    }
}


// ═══════════════════════════════════════════

// 3. ギアメカニズム（Gear Mechanism）

// ═══════════════════════════════════════════

AXIOM: GEAR_MECHANISM {
    

    // ───────────────────────────────────────
    
    // 3-1. 定義
    
    // ───────────────────────────────────────
    
    DEFINITION: "因果連鎖の1ステップでも破綻すれば全体停止";
    
    
    // ───────────────────────────────────────
    
    // 3-2. 歯車の比喩
    
    // ───────────────────────────────────────
    
    ANALOGY: {
        MECHANICAL_GEARS: {
            FUNCTION: "複数の歯車が噛み合って動力を伝達";
            NORMAL: "全ての歯車が正常なら、動力が伝わる";
            BROKEN: "1つでも歯車が欠けたら、全体が止まる";
            NO_BYPASS: "欠けた歯車を『飛ばして』次に伝えることはできない";
        };
        
        CAUSAL_GEARS: {
            FUNCTION: "因果のステップが順次つながる";
            NORMAL: "全てのステップが成立すれば、最終判定が出る";
            BROKEN: "1つでもステップが破綻したら、即座に停止（DANGER）";
            NO_BYPASS: "破綻したステップを『無視して』先に進むことはできない";
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 3-3. 因果連鎖のステップ
    
    // ───────────────────────────────────────
    
    CAUSAL_CHAIN: {
        STEP_1: "幾何学的接触チェック";
        STEP_2: "弾性力の計算";
        STEP_3: "粘性抵抗の追加";
        STEP_4: "総合抵抗力の算出";
        STEP_5: "押し流す力との比較";
        STEP_6: "最終判定";
        
        REQUIREMENT: "この6ステップ全てが成立して初めて、SAFEと判定できる";
    }
    
    
    // ───────────────────────────────────────
    
    // 3-4. 各ステップの破綻条件
    
    // ───────────────────────────────────────
    
    FAILURE_CONDITIONS: {
        
        STEP_1_GEOMETRIC_CHECK: {
            CONDITION: "IF (D_cell <= d_gap) THEN 幾何学的すり抜けリスク";
            ACTION: "即座にDANGER → 後続ステップは実行しない";
            REASON: "細胞が隙間より小さければ、力を計算する意味がない（素通り）";
        };
        
        STEP_2_ELASTIC_CALC: {
            CONDITION: "IF (k_cell < 0) OR (Δx < 0) THEN 物理パラメータ異常";
            ACTION: "即座にDANGER → エラーメッセージ『細胞硬度が負です』";
            REASON: "負の硬度は物理的にあり得ない → データ入力ミスの可能性";
        };
        
        STEP_3_VISCOUS_CALC: {
            CONDITION: "IF (η = 0) THEN 水分項欠落";
            ACTION: "即座にDANGER → エラーメッセージ『水分粘性が未定義です』";
            REASON: "水分を無視した計算は禁止（生命の不可逆性を無視）";
        };
        
        STEP_4_OVERFLOW_CHECK: {
            CONDITION: "IF (F_resist > MAX_VALUE) THEN 演算オーバーフロー";
            ACTION: "即座にDANGER → エラーメッセージ『計算範囲を超えました』";
            REASON: "Q8.8固定小数点の範囲を超える → 計算結果が信頼できない";
        };
        
        STEP_5_COMPARISON: {
            CONDITION: "IF (F_push = UNKNOWN) THEN 圧力データ欠落";
            ACTION: "即座にDANGER → エラーメッセージ『血流圧力が未測定です』";
            REASON: "比較対象が不明では判定できない";
        };
        
        STEP_6_FINAL_JUDGMENT: {
            CONDITION: "IF (F_resist <= F_push) THEN 物理的封鎖不成立";
            ACTION: "DANGER";
            REASON: "抵抗力が押す力を下回る → 通過リスクあり";
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 3-5. Fail-Closed 原則
    
    // ───────────────────────────────────────
    
    FAIL_CLOSED_PRINCIPLE: {
        DEFINITION: "不確かさは必ず『安全側（DANGER）』に倒す";
        
        CONTRAST: {
            FAIL_OPEN: {
                MEANING: "不確かなら『通す（SAFE）』";
                EXAMPLE: "セキュリティゲート故障時、開けっ放し";
                RISK: "危険を見逃す";
            };
            
            FAIL_CLOSED: {
                MEANING: "不確かなら『止める（DANGER）』";
                EXAMPLE: "セキュリティゲート故障時、閉鎖";
                SAFETY: "誤検知はあっても、見逃しはない";
            };
        };
        
        MEDICAL_JUSTIFICATION: {
            STATEMENT: "生命の判定では『たぶん大丈夫』は許されない";
            POLICY: "少しでも疑わしければ、DANGERを出す";
            CONSEQUENCE: "医師が追加検査・慎重判断を行う";
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 3-6. 実装例
    
    // ───────────────────────────────────────
    
    IMPLEMENTATION_EXAMPLE: {
        PSEUDOCODE: {
            LINE_1: "FUNCTION Judge_Safety(cell_data, vessel_data):";
            LINE_2: "    // Gear 1: Geometric Check";
            LINE_3: "    IF (cell_data.diameter <= vessel_data.gap) THEN";
            LINE_4: "        RETURN(STATUS=DANGER, REASON='幾何学的すり抜けリスク');";
            LINE_5: "    END IF";
            LINE_6: "";
            LINE_7: "    // Gear 2: Elastic Force";
            LINE_8: "    IF (cell_data.stiffness < 0) THEN";
            LINE_9: "        RETURN(STATUS=DANGER, REASON='細胞硬度が負です');";
            LINE_10: "    END IF";
            LINE_11: "    F_elastic = cell_data.stiffness * (cell_data.diameter - vessel_data.gap);";
            LINE_12: "";
            LINE_13: "    // Gear 3: Viscous Resistance";
            LINE_14: "    IF (cell_data.viscosity = 0) THEN";
            LINE_15: "        RETURN(STATUS=DANGER, REASON='水分粘性が未定義です');";
            LINE_16: "    END IF";
            LINE_17: "    F_viscous = cell_data.viscosity * cell_data.deform_velocity;";
            LINE_18: "";
            LINE_19: "    // Gear 4: Total Resistance";
            LINE_20: "    F_resist = F_elastic + F_viscous;";
            LINE_21: "    IF (F_resist > MAX_FORCE) THEN";
            LINE_22: "        RETURN(STATUS=DANGER, REASON='計算範囲を超えました');";
            LINE_23: "    END IF";
            LINE_24: "";
            LINE_25: "    // Gear 5: Comparison";
            LINE_26: "    IF (vessel_data.flow_pressure = UNKNOWN) THEN";
            LINE_27: "        RETURN(STATUS=DANGER, REASON='血流圧力が未測定です');";
            LINE_28: "    END IF";
            LINE_29: "";
            LINE_30: "    // Gear 6: Final Judgment";
            LINE_31: "    IF (F_resist > vessel_data.flow_pressure) THEN";
            LINE_32: "        RETURN(STATUS=SAFE);";
            LINE_33: "    ELSE";
            LINE_34: "        RETURN(STATUS=DANGER);";
            LINE_35: "    END IF";
            LINE_36: "END FUNCTION";
        };
        
        NOTE: "どのステップでも破綻したら、即座にRETURN（DANGER）→ 後続は実行しない";
    }
}


// ═══════════════════════════════════════════

// 4. ゲート公理（Gate Axiom）

// ═══════════════════════════════════════════

AXIOM: GATE_AXIOM {
    
    // ───────────────────────────────────────
    // 4-1. 定義
    // ───────────────────────────────────────
    DEFINITION: "人間の尊厳・生命に関わる決定には不可侵の境界がある";
    
    // ───────────────────────────────────────
    // 4-2. 境界の設定
    // ───────────────────────────────────────
    BOUNDARY_DEFINITION: {
        INSIDE_GATE: {
            DOMAIN: "物理的封鎖の成否判定";
            WHAT: "『この条件で細胞は通過できるか/できないか』という計算";
            RESPONSIBILITY: "システムが決定（物理法則に基づく）";
            LIMIT: "ここまで";
        };
        
        OUTSIDE_GATE: {
            DOMAIN: "治療方針の最終決定";
            WHAT: "『その薬液量を実際に投与するか』『副作用とのバランス』『患者のQOL』";
            RESPONSIBILITY: "医師と患者が決定（倫理・価値判断）";
            AUTONOMY: "ここはシステムが侵入してはならない領域";
        };
    }
    

    // ───────────────────────────────────────
    
    // 4-3. システムの役割
    
    // ───────────────────────────────────────
    
    SYSTEM_ROLE: {
        PROVIDE: "物理的根拠を提示する";
        EXAMPLE: "『薬液2.5kPaで、細胞通過を物理的に防げます』";
        
        NOT_PROVIDE: "最終決定を下す";
        EXAMPLE_WRONG: "『この患者には薬液2.5kPaを投与すべきです』（これは言わない）";
        
        RATIONALE: {
            SYSTEM_STRENGTH: "物理計算、最悪ケース特定";
            SYSTEM_WEAKNESS: "患者の背景、副作用リスク、価値判断は不得手";
            PHYSICIAN_STRENGTH: "臨床経験、全体的判断、患者との対話";
            SYNERGY: "両者が協力して、より良い治療を実現";
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 4-4. 医師の役割
    
    // ───────────────────────────────────────
    
    PHYSICIAN_ROLE: {
        RECEIVE: "システムからの物理的根拠を受け取る";
        INTEGRATE: "臨床所見、患者背景、副作用リスクと統合";
        DECIDE: "最終的な治療方針を決定";
        EXPLAIN: "患者に説明し、同意を得る";
        
        AUTONOMY: {
            STATEMENT: "医師は常に、システムの判定を『覆す』権利がある";
            EXAMPLE: "システムが『SAFE』でも、医師が『追加検査が必要』と判断すれば、それが優先";
            REASON: "システムは『物理』を見る。医師は『人間』を見る";
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 4-5. RED ZONE（公理外領域）
    
    // ───────────────────────────────────────
    
    RED_ZONE: {
        DEFINITION: "物理公理が保証できない領域";
        
        TRIGGER_CONDITIONS: {
            CELL_FRACTURE: {
                CONDITION: "細胞破砕（Fracture）のリスク";
                SCENARIO: "薬液濃度を上げすぎて、細胞が物理的に破壊される";
                RISK: "破片が血流に乗って、かえって転移が増える";
                ANALOGY: "風船を膨らませすぎて、爆発する";
            };
            
            TISSUE_PERFORATION: {
                CONDITION: "組織穿孔（Perforation）のリスク";
                SCENARIO: "圧力が高すぎて、血管壁が破れる";
                RISK: "出血、組織壊死";
                ANALOGY: "水道管に高圧をかけすぎて、破裂する";
            };
            
            METABOLIC_COLLAPSE: {
                CONDITION: "代謝崩壊による系の不安定化";
                SCENARIO: "細胞の動的平衡（ω, Work）が維持できなくなる";
                RISK: "予測不能な挙動";
                ANALOGY: "コマの回転が止まりそうになると、軌道が予測不能になる";
            };
        };
        
        SYSTEM_ACTION: {
            DETECTION: "上記の条件に近づいたことを検出";
            WARNING: "『警告：RED ZONE接近。物理的保証の限界です』";
            MODE_CHANGE: "『状態指示機械モード』への移行を促す";
        };
        
        STATE_INDICATOR_MODE: {
            DEFINITION: "医師が『覚悟を持って』ダイヤルを回す領域";
            INTERFACE: "スライダーUIで、医師が微調整";
            FEEDBACK: "リアルタイムで物理状態を表示（ただし保証はなし）";
            RESPONSIBILITY: "医師と患者が共有";
            
            ANALOGY: {
                AUTOPILOT: "通常モード = 自動操縦（物理法則に従う）";
                MANUAL: "RED ZONEモード = 手動操縦（医師が責任を持つ）";
            };
        };
    }
    
    
    // ───────────────────────────────────────
    
    // 4-6. 倫理的配慮
    
    // ───────────────────────────────────────
    
    ETHICAL_CONSIDERATION: {
        AI_ETHICS: {
            CONCERN: "AIが医療判断を『支配』してしまう懸念";
            NRA_IDE_STANCE: "このシステムはAIではなく『物理計算機』";
            GUARANTEE: "ゲート公理により、最終決定は必ず人間が行う";
        };
        
        INFORMED_CONSENT: {
            REQUIREMENT: "患者への説明義務";
            CONTENT: [
                "システムが何を計算しているか",
                "その結果が何を意味するか",
                "最終判断は医師が行うこと",
                "RED ZONEのリスク"
            ];
            DOCUMENT: "同意書に明記";
        };
        
        ACCOUNTABILITY: {
            SYSTEM: "計算ロジックの透明性（オープンソース）";
            PHYSICIAN: "臨床判断の責任";
            HOSPITAL: "システム運用の責任";
            SEPARATION: "各主体の責任範囲を明確に分離";
        };
    }
}


// ═══════════════════════════════════════════

// 5. 距離vs制約の優先順位

// ═══════════════════════════════════════════

PRINCIPLE: CONSTRAINT_PRIORITY {
    

    // ───────────────────────────────────────
    
    // 5-1. 原則
    
    // ───────────────────────────────────────
    
    RULE: "距離(Distance)は結果、制約(Constraint)が原因";
    
    
    // ───────────────────────────────────────
    
    // 5-2. 計算の優先順位
    
    // ───────────────────────────────────────
    
    ORDER: {
        PRIORITY_1: {
            ELEMENT: "制約（細胞と血管の接触条件）";
            QUESTION: "細胞は血管壁に当たっているか？";
            CHECK: "IF (D_cell > d_gap) THEN 接触あり";
        };
        
        PRIORITY_2: {
            ELEMENT: "張力（接触による反発力）";
            QUESTION: "接触によって、どれだけの力が発生するか？";
            CALCULATE: "F = k·Δx + η·(dv/dt)";
        };
        
        PRIORITY_3: {
            ELEMENT: "距離（結果としての変形量）";
            QUESTION: "その力により、細胞はどれだけ変形したか？";
            OBSERVE: "Δx（計算結果として得られる）";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 5-3. 距離から力を導出することの禁止
    
    // ───────────────────────────────────────
    
    PROHIBITION: {
        FORBIDDEN_LOGIC: "距離が○○だから、力が△△である";
        WHY_FORBIDDEN: "距離だけでは、接触状態（制約）が分からない";
        
        COUNTER_EXAMPLE: {
            CASE_A: "2人の距離が1m → 押し合っている → 力あり";
            CASE_B: "2人の距離が1m → 離れて立っている → 力なし";
            CONCLUSION: "同じ距離でも、制約の有無で力が変わる";
        };
    };
    
    
    // ───────────────────────────────────────
    
    // 5-4. 実装上の強制
    
    // ───────────────────────────────────────
    
    ENFORCEMENT: {
        TYPE_SYSTEM: {
            CONSTRAINT_TYPE: "接触あり/なしのBoolean型";
            FORCE_TYPE: "力の値（kPa·μm）";
            DISTANCE_TYPE: "距離の値（μm）";
            
            ALLOWED_CONVERSION: "Constraint → Force → Distance";
            FORBIDDEN_CONVERSION: "Distance → Force（コンパイルエラー）";
        };
        
        FUNCTION_SIGNATURE: {
            CORRECT: "calculate_force(constraint: Constraint, stiffness: kPa) -> Force";
            WRONG: "calculate_force(distance: Distance) -> Force （定義不可）";
        };
    };
}


// ═══════════════════════════════════════════

// 6. 次の章への接続

// ═══════════════════════════════════════════

NEXT_PHASE: {
    CURRENT_UNDERSTANDING: "律環公理（因果ダイオード、ギアメカニズム、ゲート公理）を理解した";
    
    NEXT_TOPIC: "PHASE_4: 完全用語辞書";
    NEXT_QUESTION: [
        "全ての変数の名前、単位、定義域は？",
        "単位変換（mmHg → Pa等）はどう行うのか？",
        "命名規則（i_, o_, w_等）の意味は？"
    ];
    
    PREREQUISITE_CHECK: {
        QUESTION_1: "因果ダイオードの意味が理解できたか？";
        QUESTION_2: "ギアメカニズムのFail-Closed原則が理解できたか？";
        QUESTION_3: "ゲート公理で、医師とシステムの役割分担が理解できたか？";
        
        IF_NO: "Phase 3を再読。または同僚と議論して理解を深める";
        IF_YES: "Phase 4へ進む";
    }
}


// ═══════════════════════════════════════════

// 医師への補足メッセージ

// ═══════════════════════════════════════════

EPILOGUE: {
    TO_PHYSICIANS: {
        REASSURANCE: {
            STATEMENT: "このシステムは、医師の判断を『置き換える』ものではありません";
            INTENT: "医師の判断を『物理的根拠で補強する』道具です";
        };
        
        GATE_AXIOM_GUARANTEE: {
            PROMISE: "最終決定は必ず医師が行います";
            SYSTEM_LIMIT: "システムは『物理的成否』を計算するだけ";
            PHYSICIAN_AUTONOMY: "治療方針は、医師と患者が決めます";
        };
        
        RED_ZONE_AWARENESS: {
            WARNING: "物理法則にも限界があります";
            HONESTY: "限界を超えたら、正直に『保証できません』と伝えます";
            COLLABORATION: "そこから先は、医師と患者が一緒に決める領域です";
        };
    }
}
