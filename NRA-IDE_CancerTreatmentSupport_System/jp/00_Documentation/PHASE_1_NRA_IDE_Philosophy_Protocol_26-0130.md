# NRA-IDE_Philosophy_Protocol
## Phase 1: なぜこのシステムが必要なのか
* 対象読者: コーディング経験のない医療関係者の方
### 作成日時: 2026-01-30 21:30

// ═══════════════════════════════════════════

// 0. この文書の目的

// ═══════════════════════════════════════════

PURPOSE: {
    TARGET_READER: "コーディングを知らない日本の臨床医";
    GOAL: "なぜNRA-IDEが既存の医療統計手法では解決できない問題を扱えるのか、物理的直感で理解する";
    NOTE: "この文書は論文ではなく、現場で使うための『取扱説明書の哲学編』である";
}

// ═══════════════════════════════════════════

// 1. プロジェクトの原点（なぜ生まれたか）

// ═══════════════════════════════════════════

AXIOM: PROJECT_ORIGIN {
    DEFINITION: "既存の数学が『誤差』『ノイズ』として切り捨ててきた領域にこそ、解決の鍵がある";
    
    BACKGROUND: {
        // 従来の科学：「平均」を求め、「ばらつき」を無視する
        TRADITIONAL_APPROACH: "大量のデータを集め、統計的な『平均的傾向』を導き出す";
        PROBLEM: "しかし、患者Aさんの細胞は『平均』ではない。Aさん固有の物理状態がある";
        
        EXAMPLE_TRADITIONAL: {
            CASE: "乳がん患者1000人のデータから『5年生存率70%』を算出";
            LIMITATION: "しかし、目の前のAさんが70%側なのか30%側なのかは分からない";
            REASON: "統計は『集団の傾向』であって、『個体の物理状態』ではない";
        }
    }
    
    BREAKTHROUGH: {
        INSIGHT: "癌細胞の転移は『確率』ではなく『物理現象』である";
        PHYSICS: "細胞が血管の隙間を通過できるか = 力と変形の物理法則で決まる";
        
        ANALOGY: {
            // 日常例：ボールが穴を通過できるか
            SCENARIO: "直径10cmのボールを、直径8cmの穴に押し込もうとする";
            QUESTION: "『統計的に何%通過できるか』ではなく、『物理的に通過できるか・できないか』が決まる";
            NRA_IDE_APPROACH: "この物理的成否を、細胞1つ1つについて厳密に計算する";
        }
    }
}


// ═══════════════════════════════════════════

// 1-B. 転移位相構造の世界観

// ═══════════════════════════════════════════

AXIOM: PHASE_TRANSITION_WORLDVIEW {
    PRINCIPLE: "人体も自然も世界構造も、転移位相構造（離散的階段）でできている";
    
    CONTINUOUS_VS_DISCRETE: {
        FALSE_VIEW: {
            MODEL: "連続的な変化";
            ASSUMPTION: "『だんだん悪化する』『徐々に進行する』";
            GRAPH: "なだらかな坂道";
            EXAMPLE: "腫瘍が1mm→2mm→3mmと『連続的に』大きくなる";
        };
        
        TRUE_VIEW: {
            MODEL: "離散的な階段（相転移）";
            REALITY: "臨界点を超えた瞬間に、突然状態が変わる";
            GRAPH: "階段状のジャンプ";
            EXAMPLE: "抵抗力=圧力の瞬間に、封鎖→突破が一瞬で切り替わる";
        };
    };
    
    EXAMPLES_IN_NATURE: {
        PHYSICS: {
            PHENOMENON: "水 → 氷（凝固）";
            CRITICAL_POINT: "0℃（273.15 K）";
            OBSERVATION: "0.01℃下がっただけで、液体が固体に突然変わる";
            MEANING: "『だんだん固まる』のではなく、臨界点で一気に相転移";
        };
        
        BIOLOGY: {
            PHENOMENON: "正常細胞 → 癌化";
            CRITICAL_POINT: "遺伝子変異の閾値";
            OBSERVATION: "ある変異が蓄積した瞬間、制御不能な増殖が始まる";
            MEANING: "『だんだん癌になる』のではなく、閾値を超えた瞬間にスイッチが入る";
        };
        
        MEDICINE: {
            PHENOMENON: "封鎖成立 → 突破（転移）";
            CRITICAL_POINT: "抵抗圧力 = 血流圧力";
            OBSERVATION: "0.1 kPa の差で、SAFE ⇄ DANGER が切り替わる";
            MEANING: "『だんだん通過しやすくなる』のではなく、臨界点で一瞬で突破される";
        };
    };
    
    NRA_IDE_MISSION: {
        GOAL: "この臨界点（閾値）を厳密に計算する";
        
        TRADITIONAL_FAILURE: {
            METHOD: "平均値やトレンド分析";
            PROBLEM: "臨界点を『通過する前後』が見えない";
            RESULT: "『だいたいこのくらい』という曖昧な予測";
        };
        
        NRA_IDE_SUCCESS: {
            METHOD: "パラメータ空間の総当たり探索";
            ADVANTAGE: "臨界点（抵抗力=圧力）を正確に特定";
            RESULT: "『この条件で突破される』という決定論的判定";
        };
    };
    
    MATHEMATICAL_FORMULATION: {
        THRESHOLD_FUNCTION: {
            FORMULA: "Status = Heaviside(Resist - Pressure)";
            MEANING: "抵抗 > 圧力 なら 1（SAFE）、そうでなければ 0（DANGER）";
            
            HEAVISIDE: {
                DEFINITION: "階段関数（ステップ関数）";
                PROPERTY: "x=0で不連続に0→1へジャンプ";
                INTERPRETATION: "なだらかな遷移ではなく、一瞬で切り替わる";
            };
        };
        
        RED_ZONE_AS_CRITICAL_POINT: {
            STATEMENT: "RED ZONEは相転移の臨界点そのもの";
            PHYSICS: "細胞破砕、組織穿孔は『系の相転移』";
            WARNING: "臨界点では、微小な摂動で系が崩壊する";
            CLINICAL: "だからRED ZONEでは医師が慎重に調整する";
        };
    };
    
    IMPLICATION_FOR_TREATMENT: {
        INSIGHT: "『少しずつ薬を増やす』は、臨界点を見逃す危険がある";
        STRATEGY: "総当たりで臨界点を事前計算し、一発で最適値を投与";
        SAFETY: "臨界点の手前で確実に止める（余裕を持たせる）";
    };
}


// ═══════════════════════════════════════════

// 2. 既存医療システムの3つの限界

// ═══════════════════════════════════════════

PROBLEM: EXISTING_MEDICINE_LIMIT {
    
    // ───────────────────────────────────────
    // 限界1: 統計的予測は個体の物理を無視する
    // ───────────────────────────────────────
    ISSUE_1: STATISTICAL_AVERAGING {
        DESCRIPTION: "『平均的な患者』は存在しない";
        
        EXAMPLE: {
            CASE: "乳がん細胞の硬さ(Stiffness)";
            STATISTICAL_REPORT: "平均 1.2 kPa、標準偏差 0.5 kPa";
            REALITY: {
                PATIENT_A: "細胞硬度 0.5 kPa（柔らかい）→ 血管をすり抜けやすい";
                PATIENT_B: "細胞硬度 2.0 kPa（硬い）→ 血管で詰まりやすい";
                CRITICAL: "この2人に同じ薬液濃度を投与するのは物理的に誤り";
            }
        }
        
        WHY_PROBLEM: {
            REASON_1: "統計は『どちらの患者が多いか』は教えてくれる";
            REASON_2: "しかし『目の前の患者Aさんに必要な薬液量』は教えてくれない";
            REASON_3: "物理的封鎖には『平均的な力』ではなく『最悪ケースでも耐える力』が必要";
        }
    }
    
    // ───────────────────────────────────────
    // 限界2: 距離ベースの判断は因果を逆転させる
    // ───────────────────────────────────────
    ISSUE_2: DISTANCE_BASED_FALLACY {
        DESCRIPTION: "『距離が近いから力が強い』という逆算は物理的に誤り";
        
        CORRECT_CAUSALITY: {
            // 正しい因果の流れ
            STEP_1: "細胞が血管壁に接触する（制約が発生）";
            STEP_2: "接触により反発力が発生する（力が生まれる）";
            STEP_3: "力により細胞が変形する（結果として距離が変わる）";
            SUMMARY: "制約 → 力 → 距離（この順序は絶対）";
        }
        
        WRONG_APPROACH: {
            // 間違った従来手法
            MEASUREMENT: "CTスキャンで『腫瘍と血管の距離が2mm』と測定";
            WRONG_INFERENCE: "距離が近い → だから強い力がかかっている（逆算）";
            WHY_WRONG: "距離は『結果』であって『原因』ではない";
            
            ANALOGY: {
                SCENARIO: "2人の人間の距離が1mだとする";
                WRONG_Q: "『距離が1mだから、2人の間に何Nの力が働いているか？』";
                CORRECT_Q: "『2人が押し合っているか（制約）？ なら力がある。離れて立っているだけ？ なら力はゼロ』";
                MORAL: "距離だけ見ても、力は分からない。接触状態（制約）を見なければならない";
            }
        }
        
        NRA_IDE_SOLUTION: {
            PRINCIPLE: "距離は計算しない。制約（接触）と張力（反発）のみを計算する";
            IMPLEMENTATION: "細胞直径 > 血管隙間 → 接触あり → 反発力を計算";
            RESULT: "『距離から力を逆算する』という誤りを構造的に排除";
        }
    }
    
    // ───────────────────────────────────────
    // 限界3: 計算資源の浪費（不要な汎用性）
    // ───────────────────────────────────────
    ISSUE_3: COMPUTATIONAL_WASTE {
        DESCRIPTION: "GPUやCUDAは『何でも計算できる』が、それゆえに遅い";
        
        ANALOGY: {
            GENERAL_PURPOSE_CPU: "スイスアーミーナイフ（何でもできるが、どれも中途半端）";
            FPGA_SPECIALIZED: "外科用メス（切ることに特化、他はできないが圧倒的に鋭い）";
        }
        
        WHY_GPU_IS_SLOW: {
            REASON_1: "OSのスケジューラが割り込む（ジッタ）";
            REASON_2: "浮動小数点演算の丸め誤差が蓄積する";
            REASON_3: "メモリアクセスのレイテンシ（遅延）が避けられない";
            
            MEDICAL_ANALOGY: {
                GPU_APPROACH: "救急車で患者を運び、病院で手術（移動時間がかかる）";
                FPGA_APPROACH: "手術室を患者のベッドサイドに持ってくる（移動ゼロ）";
            }
        }
        
        NRA_IDE_SOLUTION: {
            HARDWARE: "FPGA（Field-Programmable Gate Array）専用回路";
            ADVANTAGE_1: "レジスタ直接叩き → メモリ遅延ゼロ";
            ADVANTAGE_2: "組み合わせ回路のみ → OS割り込みゼロ";
            ADVANTAGE_3: "固定小数点演算 → 丸め誤差ゼロ";
            RESULT: "1患者あたり1ミリ秒未満で最適薬液量を算出";
        }
    }
}


// ═══════════════════════════════════════════

// 3. NRA-IDEが解決する3つの物理問題

// ═══════════════════════════════════════════

SOLUTION: NRA_IDE_APPROACH {
    
    CONTEXT: {
        NOTE: "このシステムは元々、物理学の『誤差切り捨て問題』から生まれた";
        ORIGIN_PROBLEMS: [
            "超伝導（原子格子の歪みが主役）",
            "プラズマ（崩壊直前のノイズが主役）",
            "癌転移（細胞の柔らかさが主役）"
        ];
        COMMON_PATTERN: "従来理論が『無視してよい』とした微細な物理こそが決定的";
    }
    
    // ───────────────────────────────────────
    // 解決策1: メソスケール物理の厳密計算
    // ───────────────────────────────────────
    SOLUTION_1: MESOSCALE_PRECISION {
        DEFINITION: "メソスケール = 細胞1個（10〜20マイクロメートル）レベルの物理";
        
        TARGET_SCALE: {
            MACRO_SCALE: "臓器全体（数センチ）→ 粗すぎて個々の細胞が見えない";
            MICRO_SCALE: "分子レベル（ナノメートル）→ 細かすぎて計算不可能";
            MESO_SCALE: "細胞1個（マイクロメートル）→ 物理法則が明確で計算可能";
        }
        
        PHYSICS_DETAIL: {
            ELEMENT_1: "細胞の硬さ（弾性係数 k）";
            ELEMENT_2: "細胞内の水分（粘性係数 η）";
            ELEMENT_3: "血管の隙間（幾何学的制約）";
            ELEMENT_4: "血流の圧力（押し流す力）";
            
            EQUATION: {
                FORMULA: "F_resist = k·Δx + η·(dv/dt)";
                MEANING: "抵抗力 = 細胞の硬さ × 変形量 + 水分の粘り × 変形速度";
                
                PHYSICAL_INTERPRETATION: {
                    TERM_1_ELASTIC: {
                        SYMBOL: "k·Δx";
                        NAME: "弾性項（バネの力）";
                        ANALOGY: "バネを押し縮めると、元に戻ろうとする力が発生";
                        MEDICAL: "細胞が血管に押し込まれると、元の形に戻ろうと抵抗する";
                    };
                    
                    TERM_2_VISCOUS: {
                        SYMBOL: "η·(dv/dt)";
                        NAME: "粘性項（水分の抵抗）";
                        ANALOGY: "蜂蜜の中で物を動かすと、ゆっくりしか動けない";
                        MEDICAL: "細胞内の水分が逃げ場を失い、急激な変形を妨げる";
                        
                        CRITICAL_NOTE: {
                            WARNING: "この項を『面倒だから無視』することは絶対に禁止";
                            REASON: "水分こそが生命の本質。これを飛ばせば『生きた細胞』ではなくなる";
                            ENFORCEMENT: "システムは水分計算の省略を検出したら、即座にエラーを出す";
                        };
                    };
                }
            }
        }
    }
    
    // ───────────────────────────────────────
    // 解決策2: 総当たり探索で最悪ケースを特定
    // ───────────────────────────────────────
    SOLUTION_2: BRUTE_FORCE_WORST_CASE {
        PRINCIPLE: "『平均的なケース』ではなく『最も危険なケース』を計算する";
        
        WHY_WORST_CASE: {
            SCENARIO: "薬液を投与して細胞を硬化させ、血管通過を防ぐ";
            
            AVERAGE_APPROACH: {
                LOGIC: "平均的な細胞硬度1.2kPa → 平均的な薬液量2.0kPaで十分";
                PROBLEM: "しかし患者の細胞に『最も柔らかい細胞0.5kPa』が1個でもあれば？";
                RESULT: "その1個がすり抜けて転移する → 治療失敗";
            };
            
            WORST_CASE_APPROACH: {
                LOGIC: "患者の細胞の中で『最も柔らかい細胞』を想定";
                CALCULATION: "その最悪細胞でも通過できないだけの薬液量を算出";
                RESULT: "全ての細胞が確実に封鎖される → 物理的保証";
            };
        }
        
        IMPLEMENTATION: {
            METHOD: "総当たり探索（Brute-Force Search）";
            
            PARAMETER_SPACE: {
                // 探索する変数の範囲
                CELL_STIFFNESS: "0.1 〜 2.0 kPa（0.1刻み）→ 20通り";
                CELL_DIAMETER: "8 〜 25 μm（1刻み）→ 18通り";
                BLOOD_PRESSURE: "100 〜 1000 Pa（50刻み）→ 19通り";
                TOTAL_CASES: "20 × 18 × 19 = 6,840通り";
            };
            
            SEARCH_PROCESS: {
                STEP_1: "各ケースについて、薬液量0から開始";
                STEP_2: "物理計算で『通過できるか？』を判定";
                STEP_3: "通過できるなら、薬液量を0.01kPa増やして再計算";
                STEP_4: "通過できなくなったら、その薬液量を記録";
                STEP_5: "6,840ケース全てで繰り返し";
                RESULT: "『最も多くの薬液が必要だったケース』= 最悪ケース";
            };
            
            TIME_COST: {
                TRADITIONAL_CPU: "数時間（逐次計算）";
                GPU_PARALLEL: "数分（並列だが遅延あり）";
                FPGA_CUSTOM: "数ミリ秒（専用回路、遅延ゼロ）";
                MEDICAL_IMPACT: "手術室で患者を待たせずに、その場で最適投薬量が分かる";
            };
        }
    }
    
    // ───────────────────────────────────────
    // 解決策3: FPGA専用回路で瞬時判定
    // ───────────────────────────────────────
    SOLUTION_3: FPGA_ZERO_LATENCY {
        DEFINITION: "FPGA = 書き換え可能な専用ハードウェア回路";
        
        ANALOGY: {
            GENERAL_COMPUTER: "楽譜を読んで演奏する音楽家（柔軟だが演奏に時間がかかる）";
            FPGA: "特定の曲だけ演奏するオルゴール（他は弾けないが、瞬時に鳴る）";
        };
        
        HARDWARE_ADVANTAGE: {
            NO_MEMORY: {
                TRADITIONAL: "計算結果をメモリに書き込み、また読み出す（往復の遅延）";
                FPGA: "レジスタ間で直接転送（遅延ゼロ）";
                ANALOGY: "リレー競技で、バトンを地面に置かず直接手渡し";
            };
            
            NO_OS: {
                TRADITIONAL: "OS（Windows等）が『ちょっと待って、他の仕事もあるから』と割り込む";
                FPGA: "OSなし。この計算専用（割り込みゼロ）";
                ANALOGY: "救急患者専用の手術室（他の予約で中断されない）";
            };
            
            NO_FLOAT: {
                TRADITIONAL: "浮動小数点（0.123456789...）で計算 → 丸め誤差が蓄積";
                FPGA: "固定小数点（Q8.8形式）で計算 → 誤差ゼロ";
                
                Q8_8_EXPLANATION: {
                    FORMAT: "16ビット整数を『整数部8ビット + 小数部8ビット』に分割";
                    EXAMPLE: {
                        VALUE: "2.5 kPa";
                        BINARY: "0x0280";
                        BREAKDOWN: "0x02（整数部=2） + 0x80（小数部=0.5）";
                    };
                    ADVANTAGE: "整数演算だけで小数を扱える → 誤差ゼロ、高速";
                };
            };
        }
        
        MEDICAL_JUSTIFICATION: {
            STAKES: "細胞1個の通過判定 = 患者の生死";
            PRECISION: "『だいたい合ってる』では許されない";
            REQUIREMENT: "丸め誤差ゼロ、遅延ゼロ、割り込みゼロ → FPGAが唯一の解";
        }
    }
}


// ═══════════════════════════════════════════

// 4. 律環公理（Ritsukan Circular Axiom）

// ═══════════════════════════════════════════

AXIOM: RITSUKAN_FOUNDATION {
    DEFINITION: "生命は動的平衡（涅槃）にある渦である";
    
    PHILOSOPHY: {
        STATIC_EQUILIBRIUM: {
            EXAMPLE: "石ころ（動かない、エネルギー不要）";
            CHARACTERISTIC: "死んだ系。外部から力を加えない限り変化しない";
        };
        
        DYNAMIC_EQUILIBRIUM: {
            EXAMPLE: "渦巻き、炎、生命（常に動いているが、形は保たれる）";
            CHARACTERISTIC: "エネルギーを流し続けることで『形』を維持";
            MEDICAL: "細胞は常に代謝（エネルギー消費）している。止まれば死ぬ";
        };
    }
    
    MATHEMATICAL_CONSTRAINT: {
        ROTATION: "ω > 0（回転がある）";
        WORK: "Work > 0（仕事を維持し続ける）";
        
        MEANING: {
            IF_OMEGA_ZERO: "回転が止まる = 系の崩壊（死）";
            IF_WORK_ZERO: "エネルギー供給が止まる = 系の消滅（壊死）";
        };
        
        CANCER_APPLICATION: {
            NORMAL_CELL: "ω > 0, Work > 0 → 正常な動的平衡";
            CANCER_CELL: "ω ≫ 0, Work ≫ 0 → 異常に高い代謝（増殖）";
            TREATMENT_GOAL: "物理的封鎖により、癌細胞の『渦』を止める";
        };
    }
    
    UNIT_PRINCIPLE: {
        ABOLISH_DISTANCE: "『距離』を計算の基準にしない";
        USE_CONSTRAINT: "『制約』と『張力』で計算する";
        
        REASON: {
            DISTANCE_IS_RESULT: "距離は物理過程の『結果』であって『原因』ではない";
            CONSTRAINT_IS_CAUSE: "制約（接触）こそが力を生む『原因』";
            
            ENFORCEMENT: {
                CODE_LEVEL: "システム内で『距離から力を導出する』コードは書けない構造";
                COMPILER_CHECK: "もし書こうとしたら、コンパイル時にエラー";
                GUARANTEE: "構造的に因果逆転を防止";
            };
        }
    }
}


// ═══════════════════════════════════════════

// 5. 医師が理解すべき核心メッセージ

// ═══════════════════════════════════════════

CORE_MESSAGE: FOR_CLINICIANS {
    
    MESSAGE_1: {
        STATEMENT: "このシステムは『AIによる診断支援』ではありません";
        CLARIFICATION: "物理法則に基づく『計算機』です";
        
        DIFFERENCE: {
            AI_DIAGNOSIS: {
                METHOD: "過去の症例データから『似たパターン』を探す";
                OUTPUT: "『この患者は70%の確率でこうなる』という統計的推測";
                LIMITATION: "なぜそうなるかの物理的根拠は不明";
            };
            
            NRA_IDE: {
                METHOD: "患者固有の物理パラメータから『力学的成否』を計算";
                OUTPUT: "『この患者の細胞は物理的に通過できる/できない』という決定論的判定";
                STRENGTH: "物理法則が根拠なので、説明可能";
            };
        }
    }
    
    MESSAGE_2: {
        STATEMENT: "『平均的な患者』のための薬液量ではありません";
        CLARIFICATION: "『あなたの目の前の患者さん』のための薬液量です";
        
        PERSONALIZATION: {
            TRADITIONAL: "ガイドライン『標準投与量は○○mg/kg』";
            NRA_IDE: "この患者さんの細胞硬度、血管径、血圧から逆算した『この人だけの最適量』";
            
            ANALOGY: {
                CLOTHING: "既製服（S/M/L）vs オーダーメイド（採寸して作る）";
                MEDICINE: "標準投薬 vs 物理的最適化";
            };
        }
    }
    
    MESSAGE_3: {
        STATEMENT: "このシステムは『最終決定』をしません";
        CLARIFICATION: "医師が判断するための『物理的根拠』を提示します";
        
        ROLE_SEPARATION: {
            SYSTEM_ROLE: {
                INSIDE_GATE: "物理的封鎖の成否判定";
                WHAT: "『薬液○○kPaで細胞通過を防げる』という計算";
                LIMIT: "ここまで";
            };
            
            PHYSICIAN_ROLE: {
                OUTSIDE_GATE: "治療方針の最終決定";
                WHAT: "『その薬液量を実際に投与するか』『副作用とのバランスは』";
                RESPONSIBILITY: "医師と患者が責任を持つ領域";
            };
            
            BOUNDARY: "ゲート公理（Gate Axiom）で明確に分離";
        }
    }
    
    MESSAGE_4: {
        STATEMENT: "不確かさは隠蔽しません";
        CLARIFICATION: "『分からない』『物理的に保証できない』は正直に報告します";
        
        FAIL_CLOSED_PRINCIPLE: {
            SAFE_OUTPUT: "抵抗力 > 圧力 → 確実に封鎖できる → 緑";
            DANGER_OUTPUT: "少しでも不確かさがあれば → 即座に赤";
            
            NO_YELLOW: {
                PRINCIPLE: "『たぶん大丈夫』という中間状態は存在しない";
                REASON: "生命の判定に『曖昧』は許されない";
            };
        }
        
        RED_ZONE: {
            DEFINITION: "物理公理が保証できない領域";
            TRIGGER: [
                "細胞破砕（Fracture）のリスク",
                "組織穿孔（Perforation）のリスク",
                "代謝崩壊による系の不安定化"
            ];
            ACTION: "医師に『状態指示機械モード』への移行を促す";
            MEANING: "ここから先は、医師と患者が覚悟を持ってダイヤルを回す領域";
        }
    }
}


// ═══════════════════════════════════════════

// 6. 次の章への接続

// ═══════════════════════════════════════════

NEXT_PHASE: {
    CURRENT_UNDERSTANDING: "なぜNRA-IDEが必要か、何を解決するかを理解した";
    
    NEXT_TOPIC: "PHASE_2: 具体的な物理モデルの定義";
    NEXT_QUESTION: [
        "Type A（乳がん）とType B（子宮頸がん）で何が違うのか？",
        "水分の粘性η を具体的にどう計算するのか？",
        "『細胞が通過できる/できない』の物理的境界はどこか？"
    ];
    
    PREREQUISITE_CHECK: {
        QUESTION_1: "『距離ではなく制約で計算する』の意味が理解できたか？";
        QUESTION_2: "『平均ではなく最悪ケース』の重要性が理解できたか？";
        QUESTION_3: "『FPGAがなぜ必要か』が理解できたか？";
        
        IF_NO: "Phase 1を再読。または医師仲間と議論して理解を深める";
        IF_YES: "Phase 2へ進む";
    }
}


// ═══════════════════════════════════════════

// 医師への最終メッセージ

// ═══════════════════════════════════════════

EPILOGUE: {
    TO_PHYSICIANS: {
        MESSAGE: "このシステムは、あなたの『勘』を否定するものではありません";
        INTENT: "あなたの臨床経験に、『物理的根拠』という道具を追加するものです";
        
        ANALOGY: {
            PAST: "聴診器が発明される前、医師は耳を直接患者の胸に当てていた";
            PRESENT: "聴診器は医師の聴覚を『増幅』した。診断を機械に任せたわけではない";
            NRA_IDE: "同様に、医師の判断を『物理的根拠で補強』する道具";
        };
        
        COLLABORATION: {
            PHYSICIAN_STRENGTH: "臨床経験、患者との対話、全体的判断";
            SYSTEM_STRENGTH: "物理計算、最悪ケース特定、瞬時判定";
            SYNERGY: "両者が協力することで、より確実な治療が可能になる";
        };
    }
    
    NEXT_STEP: {
        ACTION: "Phase 2（物理モデル詳細）を読み、具体的な計算の流れを理解する";
        GOAL: "最終的に、自分の患者さんのデータを入力し、結果を解釈できるようになる";
    }
}
