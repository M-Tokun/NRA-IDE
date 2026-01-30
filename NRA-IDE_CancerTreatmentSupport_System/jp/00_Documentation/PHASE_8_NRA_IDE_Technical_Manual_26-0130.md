# NRA-IDE_Technical_Manual
### Phase 8: 技術現場向け説明書
* 対象読者: エンジニア（合成・デバッグ） + 医師（パラメータ解釈）
* 作成日時: 2026-01-30 23:15

// ═══════════════════════════════════════════
// 0. この章の目的
// ═══════════════════════════════════════════
PURPOSE: {
    PREVIOUS_PHASE: "Phase 7で実装コードを理解した";
    THIS_PHASE: "現場で使うための実用的な手順書";
    
    TWO_AUDIENCES: {
        ENGINEERS: "FPGA合成、デバッグ、性能チューニング";
        PHYSICIANS: "パラメータ読み方、警告の意味、調整可能な閾値";
    };
}


// ═══════════════════════════════════════════

// 1. エンジニア向けセクション

// ═══════════════════════════════════════════

SECTION_ENGINEERS: {
    
 
    // ───────────────────────────────────────
    
    // 1-1. FPGA合成手順
    
    // ───────────────────────────────────────
    
    SYNTHESIS_PROCEDURE: {
        
        TOOLCHAIN: {
            INTEL: "Quartus Prime（Cyclone V想定）";
            XILINX: "Vivado（Artix-7想定）";
            OPEN_SOURCE: "Yosys + nextpnr（研究用）";
        };
        
        STEP_BY_STEP: {
            
            STEP_1_PROJECT_SETUP: {
                ACTION: "プロジェクト新規作成";
                
                QUARTUS: {
                    DEVICE: "Cyclone V 5CEBA4F23C7";
                    FAMILY: "Cyclone V E";
                };
                
                VIVADO: {
                    DEVICE: "XC7A35T-1CPG236C";
                    FAMILY: "Artix-7";
                };
            };
            
            STEP_2_ADD_FILES: {
                ACTION: "Verilogソースを追加";
                
                FILES: {
                    CORE_A: "BioCalibrator_TypeA_Jamming_Verbose_26-0130.v";
                    CORE_B: "BioCalibrator_TypeB_Collective_26-0130.v";
                    SELECTOR: "Cancer_Treatment_Selector.v";
                    TOP: "Top_Module.v（UARTインターフェース含む）";
                };
            };
            
            STEP_3_CONSTRAINTS: {
                ACTION: "制約ファイル設定";
                
                TIMING_CONSTRAINT: {
                    CLOCK: "create_clock -period 10.0 [get_ports clk]";
                    NOTE: "10ns = 100MHz";
                };
                
                IO_CONSTRAINT: {
                    UART_TX: "set_location_assignment PIN_M9 -to uart_tx";
                    UART_RX: "set_location_assignment PIN_M8 -to uart_rx";
                    NOTE: "実機のピン配置に合わせる";
                };
            };
            
            STEP_4_SYNTHESIS: {
                ACTION: "合成実行";
                
                COMMAND: {
                    QUARTUS: "quartus_map --read_settings_files=on --write_settings_files=off NRA_IDE -c NRA_IDE";
                    VIVADO: "synth_design -top Top_Module -part xc7a35tcpg236-1";
                };
                
                CHECK_REPORT: {
                    LOGIC_ELEMENTS: "約1,150 LE / ユニット → 18K LE（16並列時）";
                    DSP_BLOCKS: "約64個（乗算器）";
                    MEMORY: "0 KB（全てレジスタ）";
                };
            };
            
            STEP_5_PLACE_ROUTE: {
                ACTION: "配置配線";
                
                COMMAND: {
                    QUARTUS: "quartus_fit --read_settings_files=off --write_settings_files=off NRA_IDE -c NRA_IDE";
                    VIVADO: "place_design; route_design";
                };
                
                CHECK_TIMING: {
                    SLACK: "Setup Slack > 0 なら OK";
                    WARNING: "Negative Slack なら、クロック周波数を下げるかパイプライン深化";
                };
            };
            
            STEP_6_BITSTREAM: {
                ACTION: "ビットストリーム生成";
                
                COMMAND: {
                    QUARTUS: "quartus_asm --read_settings_files=off --write_settings_files=off NRA_IDE -c NRA_IDE";
                    VIVADO: "write_bitstream -force NRA_IDE.bit";
                };
                
                OUTPUT: "NRA_IDE.sof（Quartus）または NRA_IDE.bit（Vivado）";
            };
            
            STEP_7_PROGRAM: {
                ACTION: "FPGAにプログラム";
                
                QUARTUS: "quartus_pgm -m JTAG -o \"p;NRA_IDE.sof\"";
                VIVADO: "program_hw_devices [get_hw_devices xc7a35t_0] -f NRA_IDE.bit";
                
                VERIFY: "UARTからの応答確認";
            };
        };
    };
    
    // ───────────────────────────────────────
    // 1-2. デバッグ方法
    // ───────────────────────────────────────
    DEBUGGING: {
        
        SIMULATION: {
            TOOL: "ModelSim, Icarus Verilog, Verilator";
            
            PROCEDURE: {
                STEP_1: "Testbench作成（Phase 7のコード参照）";
                STEP_2: "シミュレーション実行";
                STEP_3: "波形確認";
                STEP_4: "期待値と比較";
            };
            
            EXAMPLE_MODELSIM: {
                COMPILE: "vlog BioCalibrator_TypeA_Jamming_Verbose_26-0130.v";
                COMPILE_TB: "vlog Testbench_BruteForce_Calibration_26-0130.v";
                SIMULATE: "vsim -c Testbench_BruteForce_Calibration -do \"run -all; quit\"";
            };
            
            WAVEFORM_CHECK: {
                SIGNAL_1: "i_cell_stiffness → 入力値が正しいか";
                SIGNAL_2: "r_deformation → 変形量計算が正しいか";
                SIGNAL_3: "r_elastic_raw → 乗算結果が正しいか";
                SIGNAL_4: "o_is_jammed → 最終判定が正しいか";
            };
        };
        
        HARDWARE_DEBUG: {
            TOOL: "SignalTap（Quartus）, ILA（Vivado）";
            
            PROCEDURE: {
                STEP_1: "観測したい信号を SignalTap に登録";
                STEP_2: "トリガ条件設定（例: o_error_code != 0）";
                STEP_3: "FPGA再プログラム";
                STEP_4: "実機動作させてキャプチャ";
            };
            
            TYPICAL_SIGNALS: {
                SIG_1: "i_cell_stiffness, i_cell_diameter（入力確認）";
                SIG_2: "r_bypass_flag（幾何学的すり抜け検出）";
                SIG_3: "r_overflow_flag（演算オーバーフロー検出）";
                SIG_4: "o_is_jammed（判定結果）";
            };
        };
        
        COMMON_ISSUES: {
            
            ISSUE_1_ALWAYS_DANGER: {
                SYMPTOM: "どんな入力でも o_is_jammed = 0";
                
                CHECK_1: "i_flow_dp が異常に大きくないか";
                CHECK_2: "r_resist_force の計算が正しいか";
                CHECK_3: "オーバーフローが発生していないか";
                
                FIX: "波形で r_resist_force と i_flow_dp を比較";
            };
            
            ISSUE_2_OVERFLOW: {
                SYMPTOM: "o_error_code = 0x04（オーバーフロー）";
                
                CHECK_1: "入力値が範囲内か（Phase 4辞書確認）";
                CHECK_2: "ALPHA値が適切か（デフォルト250）";
                
                FIX: "ALPHAを小さくする、またはパイプライン内でスケーリング調整";
            };
            
            ISSUE_3_UART_TIMEOUT: {
                SYMPTOM: "ホストPCがFPGAからの応答を受信できない";
                
                CHECK_1: "ボーレート一致（115200 bps）";
                CHECK_2: "TX/RXピンの配線確認";
                CHECK_3: "FPGAのUARTモジュールが動作しているか";
                
                FIX: "ループバックテスト（TX→RX短絡）で疎通確認";
            };
        };
    };
    
    // ───────────────────────────────────────
    // 1-3. 性能チューニング
    // ───────────────────────────────────────
    PERFORMANCE_TUNING: {
        
        PARALLEL_OPTIMIZATION: {
            STRATEGY: "パラメータ空間を並列探索";
            
            CURRENT: "16並列ユニット → 3〜5 ms";
            UPGRADE: "32並列ユニット → 1.5〜2.5 ms";
            TRADEOFF: "Logic Elements 2倍消費";
            
            IMPLEMENTATION: {
                STEP_1: "BioCalibrator モジュールを32個インスタンス化";
                STEP_2: "パラメータ空間を32分割";
                STEP_3: "各ユニットに割り当て";
                STEP_4: "結果を集約（最大Boost値を取得）";
            };
        };
        
        CLOCK_FREQUENCY: {
            DEFAULT: "100 MHz";
            OVERCLOCK: "150 MHz（リスクあり）";
            
            PROCEDURE: {
                STEP_1: "制約ファイルでクロック周期を短縮";
                STEP_2: "タイミング解析でSlack確認";
                STEP_3: "負Slackなら、パイプライン深化";
            };
        };
        
        RESOURCE_REDUCTION: {
            STRATEGY: "並列度を下げて Logic Elements 節約";
            
            EXAMPLE: "16並列 → 4並列";
            TRADEOFF: "実行時間 4倍増（12〜20 ms）";
            BENEFIT: "小規模FPGA（数千LE）で動作可能";
        };
    };
}

// ═══════════════════════════════════════════
// 2. 医師向けセクション
// ═══════════════════════════════════════════
SECTION_PHYSICIANS: {
    
    // ───────────────────────────────────────
    // 2-1. パラメータの読み方
    // ───────────────────────────────────────
    PARAMETER_INTERPRETATION: {
        
        INPUT_PARAMETERS: {
            
            CELL_STIFFNESS: {
                CLINICAL_NAME: "細胞硬度";
                UNIT: "kPa（キロパスカル）";
                TYPICAL_RANGE: "0.5〜3.0 kPa";
                
                INTERPRETATION: {
                    LOW: "0.5 kPa以下 → 柔らかい → すり抜けリスク高";
                    NORMAL: "0.5〜1.5 kPa → 正常範囲";
                    HIGH: "1.5〜3.0 kPa → 硬い → ジャミング可能";
                    VERY_HIGH: "3.0 kPa以上 → 石灰化の疑い";
                };
                
                MEASUREMENT: "超音波エラストグラフィで測定";
            };
            
            CELL_DIAMETER: {
                CLINICAL_NAME: "細胞直径";
                UNIT: "μm（マイクロメートル）";
                TYPICAL_RANGE: "8〜25 μm";
                
                INTERPRETATION: {
                    SMALL: "8 μm以下 → 小さい → すり抜けやすい";
                    NORMAL: "10〜20 μm → 正常範囲";
                    LARGE: "25 μm以上 → 大きい → 変形困難";
                };
                
                MEASUREMENT: "病理標本の顕微鏡観察";
            };
            
            FLOW_PRESSURE: {
                CLINICAL_NAME: "局所血流圧力";
                UNIT: "kPa";
                TYPICAL_RANGE: "0.5〜2.0 kPa";
                
                NOTE: "全身血圧（120 mmHg ≈ 16 kPa）とは別。局所の圧力差のみ";
                
                MEASUREMENT: "カテーテル圧測定、またはCFDシミュレーション";
            };
        };
        
        OUTPUT_RESULTS: {
            
            OPTIMAL_BOOST: {
                MEANING: "この患者に必要な薬液補強量";
                UNIT: "kPa";
                
                EXAMPLE: {
                    OUTPUT: "+2.852 kPa";
                    INTERPRETATION: "細胞硬度を 2.852 kPa 増やせば、物理的封鎖が成立";
                };
                
                CLINICAL_ACTION: {
                    STEP_1: "この値を参考に、投与量を決定";
                    STEP_2: "副作用リスクと天秤にかける";
                    STEP_3: "患者と相談し、同意取得";
                };
            };
            
            ERROR_CODE: {
                CODE_0x00: {
                    NAME: "エラーなし";
                    ACTION: "正常。結果を信頼してよい";
                };
                
                CODE_0x01: {
                    NAME: "幾何学的すり抜けリスク";
                    MEANING: "細胞が血管隙間より小さい → 薬液では防げない";
                    ACTION: "他の治療法を検討（外科的切除、放射線等）";
                };
                
                CODE_0x03: {
                    NAME: "水分粘性未定義";
                    MEANING: "測定データに η（粘性係数）が含まれていない";
                    ACTION: "マイクロレオロジー測定を追加";
                };
                
                CODE_0x04: {
                    NAME: "演算オーバーフロー";
                    MEANING: "パラメータが異常値";
                    ACTION: "測定値を再確認。入力ミスの可能性";
                };
            };
        };
    };
    
    // ───────────────────────────────────────
    // 2-2. 警告の意味
    // ───────────────────────────────────────
    WARNING_MESSAGES: {
        
        CAUTION_YELLOW: {
            TRIGGER: "RED ZONE まで 10%以内";
            
            MEANING: "物理的保証の限界に近づいている";
            
            CLINICAL_IMPLICATION: {
                STATEMENT: "薬液量をこれ以上増やすと、予測不能領域に入る";
                RISK: {
                    CELL_FRACTURE: "細胞破砕（破片が転移を促進）";
                    TISSUE_PERFORATION: "血管壁穿孔（出血リスク）";
                };
            };
            
            ACTION: {
                OPTION_1: "現在の値で妥協する";
                OPTION_2: "慎重に少しずつ増やす（状態指示機械モード）";
                OPTION_3: "他の治療法と併用";
            };
        };
        
        RED_ZONE: {
            TRIGGER: "細胞破砕リスク、組織穿孔リスク検出";
            
            MEANING: "NRA-IDE公理が保証できない領域";
            
            CLINICAL_IMPLICATION: {
                STATEMENT: "ここから先は、物理法則による自動判定ができない";
                ANALOGY: "飛行機の自動操縦が切れて、手動操縦に切り替わる";
            };
            
            STATE_INDICATOR_MODE: {
                DEFINITION: "医師が『覚悟を持って』微調整する領域";
                
                INTERFACE: {
                    SLIDER: "薬液量スライダー（UI）";
                    FEEDBACK: "リアルタイムで物理状態表示（ただし保証なし）";
                };
                
                RESPONSIBILITY: {
                    SYSTEM: "物理状態の可視化のみ";
                    PHYSICIAN: "最終決定と責任";
                };
            };
        };
    };
    
    // ───────────────────────────────────────
    // 2-3. 調整可能な閾値
    // ───────────────────────────────────────
    ADJUSTABLE_THRESHOLDS: {
        
        THRESHOLD_1_SAFETY_MARGIN: {
            PARAMETER: "安全マージン";
            DEFAULT: "10%（最適Boost × 1.1）";
            
            MEANING: "余裕を持たせるための上乗せ";
            
            ADJUSTMENT: {
                CONSERVATIVE: "20%（より安全側）";
                AGGRESSIVE: "5%（最小限）";
            };
            
            CLINICAL_JUDGMENT: {
                YOUNG_PATIENT: "回復力高い → 5%でも可";
                ELDERLY_PATIENT: "副作用リスク → 20%推奨";
            };
        };
        
        THRESHOLD_2_RED_ZONE_TRIGGER: {
            PARAMETER: "RED ZONE 開始点";
            DEFAULT: "Boost > 8.0 kPa";
            
            MEANING: "この値を超えると、物理的保証が困難";
            
            ADJUSTMENT: {
                REASON: "組織の強度、患者の体質により変わる";
                PROCEDURE: "臨床試験データから決定";
            };
        };
    };
    
    // ───────────────────────────────────────
    // 2-4. FAQ（よくある質問）
    // ───────────────────────────────────────
    FAQ: {
        
        Q1: {
            QUESTION: "なぜ水分の粘性（η）を測定しなければならないのか？";
            ANSWER: "細胞は70%が水分。これを無視すると、時間依存性が消え、生命の不可逆性を計算できなくなる。転移は『心拍の1拍で』起きるため、粘性項は必須。";
        };
        
        Q2: {
            QUESTION: "全身血圧120mmHgなのに、なぜ局所圧力は数kPaなのか？";
            ANSWER: "血管の抵抗により、局所では圧力が大幅に低下する。毛細血管レベルでは、数kPa程度の圧力差のみが残る。";
        };
        
        Q3: {
            QUESTION: "システムが『DANGER』と判定したら、治療不可能なのか？";
            ANSWER: "いいえ。『現在の条件では物理的封鎖が成立しない』という意味。薬液量を増やす、または他の治療法と併用することで対処可能。";
        };
        
        Q4: {
            QUESTION: "Type AとType Bはどう判別するのか？";
            ANSWER: "病理組織型から判断。腺癌→Type A（硬い単独細胞）、扁平上皮癌→Type B（柔らかい集団）。不明な場合は両方計算し、より厳しい値を採用。";
        };
        
        Q5: {
            QUESTION: "なぜGPUではなくFPGAなのか？";
            ANSWER: "医療機器には『再現性100%』『遅延ゼロ』『誤差ゼロ』が必要。GPUはOSの割り込みと浮動小数点の丸め誤差があるため不適。FPGAは専用回路で決定論的に動作。";
        };
    };
}

// ═══════════════════════════════════════════
// 3. トラブルシューティング表
// ═══════════════════════════════════════════
TROUBLESHOOTING: {
    
    TABLE: {
        HEADER: ["症状", "原因候補", "確認方法", "対処法"];
        
        ROW_1: {
            SYMPTOM: "常にDANGER判定";
            CAUSE: "i_flow_dp が異常に大きい";
            CHECK: "入力パラメータを確認";
            FIX: "測定値を再確認。単位変換ミスの可能性";
        };
        
        ROW_2: {
            SYMPTOM: "オーバーフロー頻発";
            CAUSE: "ALPHA値が大きすぎる";
            CHECK: "r_resist_force の波形確認";
            FIX: "ALPHAを250→150に変更";
        };
        
        ROW_3: {
            SYMPTOM: "UART通信不能";
            CAUSE: "ボーレート不一致";
            CHECK: "115200 bps か確認";
            FIX: "ホストPC側を115200に設定";
        };
        
        ROW_4: {
            SYMPTOM: "計算が遅い（>100ms）";
            CAUSE: "並列度が低い";
            CHECK: "何ユニット並列か確認";
            FIX: "16並列に増やす";
        };
        
        ROW_5: {
            SYMPTOM: "RED ZONE頻出";
            CAUSE: "患者の組織が脆弱";
            CHECK: "患者背景（年齢、既往歴）";
            FIX: "状態指示機械モードで慎重調整";
        };
    };
}

// ═══════════════════════════════════════════
// 4. 次の章への接続
// ═══════════════════════════════════════════
NEXT_PHASE: {
    CURRENT_UNDERSTANDING: "技術現場での運用方法を理解した";
    
    NEXT_TOPIC: "PHASE_9: 運用ガイド（クイックスタート、展開チェックリスト）";
    NEXT_CONTENT: [
        "初回セットアップ手順",
        "日常運用フロー",
        "デプロイメントチェックリスト"
    ];
}
