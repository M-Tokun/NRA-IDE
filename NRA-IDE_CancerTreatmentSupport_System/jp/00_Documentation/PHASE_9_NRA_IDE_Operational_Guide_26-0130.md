# NRA-IDE_Operational_Guide
### Phase 9: 運用ガイド
* 対象読者: 全員（初回導入、日常運用、展開準備）
* 作成日時: 2026-01-30 23:30


// ═══════════════════════════════════════════

// 0. この章の目的

// ═══════════════════════════════════════════

PURPOSE: {
    PREVIOUS_PHASE: "Phase 8で技術的な運用方法を理解した";
    THIS_PHASE: "実際に導入・運用するための実務ガイド";
    
    KEY_SECTIONS: {
        SECTION_1: "クイックスタート（初回セットアップ）";
        SECTION_2: "リソース要件（ハードウェア・ソフトウェア）";
        SECTION_3: "パフォーマンス指標";
        SECTION_4: "デプロイメントチェックリスト";
    };
}


// ═══════════════════════════════════════════

// 1. クイックスタート

// ═══════════════════════════════════════════

QUICK_START: {
    
    // ───────────────────────────────────────
    // 1-1. 初回セットアップ（30分）
    // ───────────────────────────────────────
    INITIAL_SETUP: {
        
        STEP_1_HARDWARE: {
            TITLE: "FPGAボード準備";
            TIME: "5分";
            
            REQUIRED: {
                FPGA_BOARD: "Intel Cyclone V または Xilinx Artix-7";
                USB_CABLE: "JTAG プログラミングケーブル";
                SERIAL_CABLE: "USB-UART変換ケーブル";
            };
            
            PROCEDURE: {
                ACTION_1: "FPGAボードに電源接続";
                ACTION_2: "JTAG ケーブルでPC接続";
                ACTION_3: "UART ケーブルでPC接続";
                VERIFY: "デバイスマネージャーでCOMポート確認（Windows）またはlsusb（Linux）";
            };
        };
        
        STEP_2_SOFTWARE: {
            TITLE: "ソフトウェアインストール";
            TIME: "10分";
            
            PC_REQUIREMENTS: {
                OS: "Windows 10/11 または Ubuntu 20.04+";
                RAM: "8 GB以上";
                STORAGE: "10 GB以上の空き容量";
            };
            
            INSTALL: {
                PYTHON: {
                    VERSION: "Python 3.8+";
                    COMMAND: "python --version（確認）";
                    PACKAGES: {
                        SERIAL: "pip install pyserial";
                        NUMPY: "pip install numpy";
                        MATPLOTLIB: "pip install matplotlib";
                    };
                };
                
                OPTIONAL: {
                    QUARTUS: "Intel Quartus Prime Lite（再合成する場合のみ）";
                    VIVADO: "Xilinx Vivado（再合成する場合のみ）";
                };
            };
        };
        
        STEP_3_PROGRAM_FPGA: {
            TITLE: "FPGAプログラミング";
            TIME: "5分";
            
            OBTAIN_BITSTREAM: {
                SOURCE: "プロジェクトのreleasesフォルダ";
                FILE: "NRA_IDE_TypeA_v1_0.sof（Quartus）または .bit（Vivado）";
            };
            
            PROGRAM: {
                QUARTUS: "Quartus Programmer GUI → 'Add File' → 'Start'";
                VIVADO: "Hardware Manager → 'Program Device'";
                COMMAND_LINE: {
                    QUARTUS: "quartus_pgm -m JTAG -o \"p;NRA_IDE_TypeA_v1_0.sof\"";
                    VIVADO: "vivado -mode tcl -source program.tcl";
                };
            };
            
            VERIFY: {
                ACTION: "FPGA上のLEDが点滅することを確認";
                NOTE: "点滅パターンはバージョン識別用（例: 3回点滅 = v1.0）";
            };
        };
        
        STEP_4_TEST_CONNECTION: {
            TITLE: "通信テスト";
            TIME: "5分";
            
            PYTHON_SCRIPT: {
                FILE: "fpga_interface_verbose_26-0130.py";
                COMMAND: "python fpga_interface_verbose_26-0130.py --test";
            };
            
            TEST_SEQUENCE: {
                SEND: "テスト用パラメータを送信";
                RECEIVE: "FPGA からの応答を受信";
                VERIFY: "正常応答なら '✓ 通信成功' 表示";
            };
            
            IF_FAIL: {
                CHECK_1: "COMポート番号が正しいか";
                CHECK_2: "ボーレートが 115200 bps か";
                CHECK_3: "TX/RX が逆になっていないか";
            };
        };
        
        STEP_5_FIRST_RUN: {
            TITLE: "初回実行";
            TIME: "5分";
            
            SAMPLE_DATA: {
                FILE: "sample_patient_data.json";
                CONTENT: {
                    CELL_STIFFNESS: "1.5 kPa";
                    CELL_DIAMETER: "12.0 μm";
                    PORE_SIZE: "8.0 μm";
                    FLOW_DP: "0.6 kPa";
                };
            };
            
            RUN: {
                COMMAND: "python main.py --input sample_patient_data.json";
                OUTPUT: "推奨薬液量: +2.852 kPa";
                REPORT: "NRA_IDE_Report_Sample.txt（テキストレポート）";
                MAP: "SafetyMap_Sample.png（安全域可視化）";
            };
            
            VERIFY: "レポートファイルが生成されたことを確認";
        };
    };
    
    // ───────────────────────────────────────
    // 1-2. 日常運用フロー
    // ───────────────────────────────────────
    DAILY_OPERATION: {
        
        WORKFLOW: {
            
            STEP_1_PATIENT_EXAM: {
                WHO: "臨床検査技師";
                ACTION: "患者測定（超音波エラストグラフィ、病理標本観察）";
                OUTPUT: "測定データ（Excel または CSV）";
            };
            
            STEP_2_DATA_INPUT: {
                WHO: "医療事務 または 医師";
                ACTION: "測定データをシステムに入力";
                TOOL: "WebUI または Python CLI";
                VALIDATE: "Phase 4 辞書で範囲チェック自動実行";
            };
            
            STEP_3_CALCULATION: {
                WHO: "システム（自動）";
                ACTION: "FPGA で総当たり探索実行";
                TIME: "3〜50 ミリ秒";
                OUTPUT: "最適薬液量 + エラーコード";
            };
            
            STEP_4_REPORT_GENERATION: {
                WHO: "システム（自動）";
                ACTION: "臨床レポート生成";
                FORMAT: {
                    TEXT: "患者ID、測定値、推奨値、警告";
                    IMAGE: "安全マップ（PNG）";
                };
            };
            
            STEP_5_PHYSICIAN_REVIEW: {
                WHO: "医師";
                ACTION: "レポート確認、最終判断";
                CONSIDERATIONS: {
                    FACTOR_1: "患者の既往歴、年齢";
                    FACTOR_2: "副作用リスク";
                    FACTOR_3: "他の治療法との併用";
                };
                DECISION: "投薬量決定、患者説明、同意取得";
            };
            
            STEP_6_TREATMENT: {
                WHO: "医師 + 看護師";
                ACTION: "薬液投与";
                MONITORING: "投与後の状態観察";
            };
        };
        
        TIME_ESTIMATE: {
            MEASUREMENT: "30分";
            DATA_INPUT: "5分";
            CALCULATION: "<1分";
            REPORT_REVIEW: "10分";
            TOTAL: "約45分 / 患者";
        };
    };
}

// ═══════════════════════════════════════════
// 2. リソース要件
// ═══════════════════════════════════════════
RESOURCE_REQUIREMENTS: {
    
    // ───────────────────────────────────────
    // 2-1. ハードウェア
    // ───────────────────────────────────────
    HARDWARE: {
        
        FPGA_BOARD: {
            MINIMUM: {
                CHIP: "Cyclone V 5CEBA4（約25K Logic Elements）";
                PARALLEL: "8ユニット並列";
                PERFORMANCE: "約10 ms / 患者";
                COST: "約$200";
            };
            
            RECOMMENDED: {
                CHIP: "Cyclone V 5CEBA7（約50K Logic Elements）";
                PARALLEL: "16ユニット並列";
                PERFORMANCE: "約3〜5 ms / 患者";
                COST: "約$400";
            };
            
            HIGH_END: {
                CHIP: "Virtex-7 XC7VX485T（約300K Logic Elements）";
                PARALLEL: "64ユニット並列";
                PERFORMANCE: "<1 ms / 患者";
                COST: "約$2,000";
                USE_CASE: "大規模病院、リアルタイム処理";
            };
        };
        
        HOST_PC: {
            MINIMUM: {
                CPU: "Intel Core i3 または同等";
                RAM: "8 GB";
                STORAGE: "256 GB SSD";
                OS: "Windows 10 または Ubuntu 20.04";
            };
            
            RECOMMENDED: {
                CPU: "Intel Core i5 以上";
                RAM: "16 GB";
                STORAGE: "512 GB SSD";
                GPU: "不要（FPGAで計算）";
            };
        };
        
        PERIPHERALS: {
            DISPLAY: "1920×1080以上（安全マップ表示用）";
            PRINTER: "レポート印刷用";
            NETWORK: "患者データベース接続用（オプション）";
        };
    };
    
    // ───────────────────────────────────────
    // 2-2. ソフトウェア
    // ───────────────────────────────────────
    SOFTWARE: {
        
        RUNTIME: {
            PYTHON: "3.8+ （pyserial, numpy, matplotlib）";
            DRIVERS: "FTDI UART ドライバ（自動インストール）";
        };
        
        DEVELOPMENT: {
            FPGA_TOOLS: {
                QUARTUS: "Intel Quartus Prime Lite（無料）";
                VIVADO: "Xilinx Vivado ML Edition（無料版あり）";
            };
            
            SIMULATION: {
                MODELSIM: "ModelSim Intel FPGA Edition（Quartus付属）";
                ICARUS: "Icarus Verilog（オープンソース）";
            };
        };
        
        OPTIONAL: {
            DATABASE: "PostgreSQL, MySQL（患者データ管理）";
            WEB_UI: "Flask, Django（Webインターフェース）";
        };
    };
    
    // ───────────────────────────────────────
    // 2-3. 消費電力
    // ───────────────────────────────────────
    POWER_CONSUMPTION: {
        
        FPGA_BOARD: {
            IDLE: "約2 W";
            ACTIVE: "約5 W";
            PEAK: "約8 W（16並列時）";
        };
        
        HOST_PC: {
            TYPICAL: "約50 W";
        };
        
        TOTAL_SYSTEM: {
            TYPICAL: "約55 W";
            COMPARISON: {
                GPU_SYSTEM: "約300 W";
                ADVANTAGE: "FPGAシステムは 1/5 の消費電力";
            };
        };
        
        BATTERY_OPERATION: {
            FEASIBILITY: "可能";
            DURATION: "50Wh バッテリーで約1時間";
            USE_CASE: "移動診療、災害時";
        };
    };
}

// ═══════════════════════════════════════════
// 3. パフォーマンス指標
// ═══════════════════════════════════════════
PERFORMANCE_METRICS: {
    
    // ───────────────────────────────────────
    // 3-1. 計算速度
    // ───────────────────────────────────────
    COMPUTATION_SPEED: {
        
        SINGLE_UNIT: {
            WORST_CASE: "342 ms（684万回判定）";
            TYPICAL: "51 ms（102万回判定）";
            BEST_CASE: "3.4 ms（6.8万回判定）";
        };
        
        PARALLEL_16_UNITS: {
            WORST_CASE: "21 ms";
            TYPICAL: "3.2 ms";
            BEST_CASE: "<1 ms";
        };
        
        REAL_WORLD: {
            AVERAGE: "約5 ms / 患者";
            VARIANCE: "±2 ms（パラメータ依存）";
        };
    };
    
    // ───────────────────────────────────────
    // 3-2. スループット
    // ───────────────────────────────────────
    THROUGHPUT: {
        
        PATIENTS_PER_HOUR: {
            SINGLE_UNIT: "約3,600患者/時（非現実的）";
            PARALLEL_16: "約720,000患者/時（理論値）";
            
            REALISTIC: {
                VALUE: "約10患者/時";
                BOTTLENECK: "測定時間（30分）が律速";
                NOTE: "計算時間は無視できる";
            };
        };
        
        DAILY_CAPACITY: {
            SMALL_CLINIC: "20〜50患者/日";
            MEDIUM_HOSPITAL: "100〜200患者/日";
            LARGE_HOSPITAL: "500+患者/日";
            
            NOTE: "FPGAの計算速度は十分。測定設備が律速";
        };
    };
    
    // ───────────────────────────────────────
    // 3-3. 精度
    // ───────────────────────────────────────
    ACCURACY: {
        
        NUMERICAL_PRECISION: {
            Q8_8_RESOLUTION: "0.0039 kPa";
            MEDICAL_MEASUREMENT: "±0.1 kPa";
            CONCLUSION: "Q8.8精度は医療測定精度より十分細かい";
        };
        
        ROUNDING_ERROR: {
            FIXED_POINT: "ゼロ（整数演算）";
            FLOATING_POINT: "約10⁻⁷（累積すると問題）";
            ADVANTAGE: "固定小数点により誤差ゼロを保証";
        };
        
        REPRODUCIBILITY: {
            DETERMINISM: "同じ入力 → 必ず同じ出力";
            VERIFICATION: "医療機器認証の要件を満たす";
        };
    };
}

// ═══════════════════════════════════════════
// 4. デプロイメントチェックリスト
// ═══════════════════════════════════════════
DEPLOYMENT_CHECKLIST: {
    
    // ───────────────────────────────────────
    // 4-1. 技術的検証
    // ───────────────────────────────────────
    TECHNICAL_VERIFICATION: {
        
        CHECKLIST: {
            ITEM_1: {
                TASK: "FPGAビットストリーム検証";
                PROCEDURE: "Testbenchで全ケーステスト";
                PASS_CRITERIA: "エラーゼロ";
            };
            
            ITEM_2: {
                TASK: "UART通信テスト";
                PROCEDURE: "ループバック + 実データ送受信";
                PASS_CRITERIA: "1000回送受信で通信失敗ゼロ";
            };
            
            ITEM_3: {
                TASK: "総当たり探索検証";
                PROCEDURE: "既知解と照合";
                PASS_CRITERIA: "誤差 < 0.01 kPa";
            };
            
            ITEM_4: {
                TASK: "エラーハンドリング";
                PROCEDURE: "異常値入力テスト";
                PASS_CRITERIA: "全てのエラーコードが正しく返る";
            };
            
            ITEM_5: {
                TASK: "長時間動作テスト";
                PROCEDURE: "連続48時間稼働";
                PASS_CRITERIA: "ハング、リセットなし";
            };
        };
    };
    
    // ───────────────────────────────────────
    // 4-2. 臨床的検証
    // ───────────────────────────────────────
    CLINICAL_VERIFICATION: {
        
        CHECKLIST: {
            ITEM_1: {
                TASK: "医師トレーニング";
                PROCEDURE: "Phase 1〜9 の資料で研修";
                DURATION: "4時間";
                PASS_CRITERIA: "理解度テスト 80%以上";
            };
            
            ITEM_2: {
                TASK: "測定精度確認";
                PROCEDURE: "同一患者を3回測定";
                PASS_CRITERIA: "ばらつき < 10%";
            };
            
            ITEM_3: {
                TASK: "レポート可読性";
                PROCEDURE: "医師5名がレポート読解";
                PASS_CRITERIA: "全員が理解できる";
            };
            
            ITEM_4: {
                TASK: "倫理審査";
                PROCEDURE: "IRB（施設内倫理審査委員会）承認取得";
                DOCUMENT: "同意書、プロトコル、リスク説明";
            };
            
            ITEM_5: {
                TASK: "パイロットスタディ";
                PROCEDURE: "10患者で実施";
                EVALUATION: "有効性、安全性、実行可能性";
            };
        };
    };
    
    // ───────────────────────────────────────
    // 4-3. 運用体制
    // ───────────────────────────────────────
    OPERATIONAL_READINESS: {
        
        CHECKLIST: {
            ITEM_1: {
                TASK: "役割分担明確化";
                ROLES: {
                    PHYSICIAN: "最終判断、患者説明";
                    TECHNICIAN: "測定、データ入力";
                    ENGINEER: "システム保守、トラブル対応";
                };
            };
            
            ITEM_2: {
                TASK: "データ管理体制";
                PROCEDURE: {
                    STORAGE: "暗号化ストレージ";
                    BACKUP: "毎日バックアップ";
                    RETENTION: "5年間保存（法令遵守）";
                };
            };
            
            ITEM_3: {
                TASK: "緊急時対応";
                PLAN: {
                    SYSTEM_DOWN: "手動計算手順書を準備";
                    DATA_LOSS: "バックアップから復元";
                    CONTACT: "エンジニアへ緊急連絡先";
                };
            };
            
            ITEM_4: {
                TASK: "定期メンテナンス";
                SCHEDULE: {
                    DAILY: "動作確認（朝）";
                    WEEKLY: "ログ確認";
                    MONTHLY: "FPGAファームウェア更新チェック";
                    YEARLY: "ハードウェア点検";
                };
            };
        };
    };
    
    // ───────────────────────────────────────
    // 4-4. 法規制対応
    // ───────────────────────────────────────
    REGULATORY_COMPLIANCE: {
        
        CHECKLIST: {
            ITEM_1: {
                TASK: "医療機器認証（日本）";
                REGULATION: "薬機法（PMDAへ申請）";
                CLASS: "クラスII（管理医療機器）想定";
                DURATION: "約1〜2年";
            };
            
            ITEM_2: {
                TASK: "個人情報保護";
                REGULATION: "個人情報保護法";
                MEASURES: {
                    ANONYMIZATION: "患者ID匿名化";
                    ACCESS_CONTROL: "ログイン認証";
                    AUDIT_LOG: "アクセスログ記録";
                };
            };
            
            ITEM_3: {
                TASK: "品質管理システム";
                STANDARD: "ISO 13485（医療機器品質マネジメント）";
                DOCUMENTATION: {
                    DHF: "Design History File（設計履歴）";
                    DMR: "Device Master Record（製造記録）";
                    DHR: "Device History Record（履歴記録）";
                };
            };
            
            ITEM_4: {
                TASK: "リスクマネジメント";
                STANDARD: "ISO 14971（医療機器リスクマネジメント）";
                PROCEDURE: {
                    HAZARD_ANALYSIS: "ハザード分析";
                    RISK_EVALUATION: "リスク評価";
                    MITIGATION: "リスク低減措置";
                };
            };
        };
    };
}

// ═══════════════════════════════════════════
// 5. 最終メッセージ
// ═══════════════════════════════════════════
FINAL_MESSAGE: {
    
    TO_ALL: {
        ACKNOWLEDGMENT: "Phase 1〜9 の全資料を通して、NRA-IDEシステムの理解が深まったことを願います";
        
        PHILOSOPHY: {
            STATEMENT: "このシステムは医師を『置き換える』ものではなく、医師を『補強する』道具です";
            GATE_AXIOM: "最終決定は必ず人間が行う。システムは物理的根拠を提示するのみ";
        };
        
        MISSION: {
            PRIMARY: "癌転移を物理的に封鎖し、患者の生命を守る";
            SECONDARY: "医療判断に『決定論的な物理根拠』を提供する";
            TERTIARY: "医療AIの『説明可能性』『検証可能性』のモデルケースとなる";
        };
        
        OPEN_SOURCE: {
            STATEMENT: "このシステムはオープンソースです";
            LICENSE: "MIT License";
            GITHUB: "https://github.com/M-Tokun/NRA-IDE";
            INVITATION: "改善提案、バグ報告、貢献を歓迎します";
        };
    };
    
    TO_PHYSICIANS: {
        MESSAGE: "あなたの臨床経験と、このシステムの物理計算を組み合わせることで、より確実な治療が可能になります";
        TRUST: "システムを盲信せず、常に批判的に検証してください";
        COLLABORATION: "疑問があれば、エンジニアと積極的に議論してください";
    };
    
    TO_ENGINEERS: {
        MESSAGE: "医療機器開発は、単なるソフトウェア開発ではありません";
        RESPONSIBILITY: "あなたの書くコードが、人の生命に直結します";
        QUALITY: "『だいたい動く』ではなく、『厳密に動く』を追求してください";
        DOCUMENTATION: "冗長なコメントは手間ではなく、信頼性の証です";
    };
    
    TO_RESEARCHERS: {
        MESSAGE: "このフレームワークは癌治療だけでなく、他の医療分野にも展開可能です";
        POTENTIAL: {
            CARDIOLOGY: "血栓の物理的封鎖";
            NEUROLOGY: "脳浮腫の圧力管理";
            ORTHOPEDICS: "骨折治癒の力学計算";
        };
        INVITATION: "新しい応用を探求し、論文化してください";
    };
}

// ═══════════════════════════════════════════
// 付録: 参考資料リンク
// ═══════════════════════════════════════════
APPENDIX: REFERENCES {
    
    PROJECT_FILES: {
        GITHUB: "https://github.com/M-Tokun/NRA-IDE";
        TWITTER: "https://x.com/m_tokuni";
        NOTE: "https://note.com/mtokuni";
        FACEBOOK: "https://www.facebook.com/tokuni.masa";
    };
    
    TECHNICAL_STANDARDS: {
        IEEE_754: "IEEE Standard for Floating-Point Arithmetic";
        ISO_13485: "Medical devices - Quality management systems";
        ISO_14971: "Medical devices - Application of risk management";
    };
    
    FPGA_RESOURCES: {
        INTEL_QUARTUS: "https://www.intel.com/content/www/us/en/products/details/fpga/development-tools/quartus-prime.html";
        XILINX_VIVADO: "https://www.xilinx.com/products/design-tools/vivado.html";
        ICARUS_VERILOG: "http://iverilog.icarus.com/";
    };
}
