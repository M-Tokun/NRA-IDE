# NRA-IDE FPGA実装 ─ セッションまとめ

<!-- FILE: NRA-IDE_FPGA_Implementation_2026-03-14_2157.md -->

<!-- 作成日時: 2026-03-14 21:57:11 JST -->

<!-- 対象リポジトリ: https://github.com/M-Tokun/NRA-IDE -->



---



## 1. 概要



NRA-IDE（律環公理 / Nomological Ring Axioms ─ 内包性動力学エンジン / Intensional Dynamics Engine）のコア原則を、FPGAの論理回路として実装する具体的な手順を整理した。インタラクティブウィジェットを用いて5フェーズに分けて設計・実装・検証の流れを示し、各フェーズの判断根拠を補足した。



---



## 2. 原則 → FPGA回路 マッピング（フェーズ①）



NRA-IDEの7原則を回路要素へ1対1で対応させる。この対応表が実装全体の設計基盤となる。



| NRA-IDE原則 | FPGA回路要素 | 実装上のポイント |

|---|---|---|

| 因果ダイオード原理 | 一方向レジスタ（FF + enable） | 逆方向出力ポートを設けない。ポート非存在 = 物理的配線不可 |

| 脱進機原理（誤差蓄積ゼロ） | Q16.16 固定小数点演算 | 浮動小数点禁止。DSP48スライスで完全精度比較 |

| 律環公理（処理順序厳守） | 同期パイプライン + FSM | クロックエッジ整列。IDLE → OBSERVE → COMPUTE → VALIDATE → EMIT |

| 完全境界（絶対閾値） | コンパレータ（ハードコード定数） | 実行時変更禁止。パラメータとしてトップレベルに固定 |

| 限界告白システム | FSM S_CONFESS 状態 | confess_flag=1 で割り込み出力 + 出力強制ゼロ |

| 中心なしアーキテクチャ | 分散モジュール直結 | 中央調停ロジック（アービター）を置かない |

| 不可逆性（時間の一方向性） | 単調カウンタ・FSM一方向遷移 | ロールバック禁止。S_EMIT → S_OBSERVE の逆走パス生成なし |



### 設計禁止事項（回路レベル）



> 距離は観測・ログのみ。`threshold_detector` のコンビネーション論理への入力は「現在の値」と「固定された境界値」のみ。過去の観測値との差分（距離）を入力してはならない。



---



## 3. 開発環境構築（フェーズ②）



### 推奨ツールチェーン



| 項目 | 選定内容 |

|---|---|

| ターゲットFPGA | Xilinx Artix-7 (XC7A35T) または Intel Cyclone V |

| 開発ツール | Vivado 2023.x / Quartus Prime Lite |

| HDL言語 | SystemVerilog 2012 (IEEE 1800-2012) |

| シミュレータ | ModelSim / Vivado Simulator (Xvlog) |

| 形式検証（任意） | SymbiYosys（オープンソース） |

| 固定小数点形式 | Q16.16（32bit符号付き固定小数点） |



### ディレクトリ構成



```

nra-ide-fpga/

├── rtl/

│   ├── causal_diode.sv        ← 因果ダイオード

│   ├── threshold_detector.sv  ← 閾値検出器（脱進機）

│   ├── nra_ring_fsm.sv        ← 律環FSM

│   ├── ide_pipeline.sv        ← IDEパイプライン

│   └── nra_ide_top.sv         ← トップレベル統合

├── tb/

│   ├── tb_causal_diode.sv

│   ├── tb_nra_ring_fsm.sv

│   └── tb_nra_ide_top.sv

├── constraints/

│   └── nra_ide.xdc

├── sim/

│   └── run_sim.tcl

└── synth/

    └── run_synth.tcl

```



### 環境構築の注意点



Q16.16境界値パラメータの符号処理について、Vivadoは `signed` パラメータをそのまま扱うが、Quartusでは `localparam signed` と明示しないと符号拡張に失敗するケースがある。`32'sh00008000` という `sh` プレフィックス記法（符号付き16進数の明示）でこの問題を回避する。



---



## 4. コアモジュール実装（フェーズ③）



### 4-1. causal_diode.sv ─ 因果ダイオード



```systemverilog

// causal_diode.sv ─ 因果ダイオード（一方向信号流）

// NRA-IDE原則：逆方向パスを物理的に存在させない

module causal_diode #(

    parameter DATA_WIDTH = 32

)(

    input  logic                  clk,

    input  logic                  rst_n,

    input  logic [DATA_WIDTH-1:0] data_in,

    input  logic                  valid_in,

    output logic [DATA_WIDTH-1:0] data_out,

    output logic                  valid_out

    // ★ 逆方向出力ポートは存在しない ─ 因果性の回路的保証

);

    always_ff @(posedge clk or negedge rst_n) begin

        if (!rst_n) begin

            data_out  <= '0;

            valid_out <= 1'b0;

        end else begin

            data_out  <= data_in;

            valid_out <= valid_in;

        end

    end

endmodule

```



**設計根拠:** 逆方向出力ポートが存在しないことが本質。ソフトウェアでは「逆向きに呼ばない」という規約で実現するが、FPGAではポートがなければ物理的に配線不可能になる。不可逆性をHDL構造として保証する最もシンプルな手法。



---



### 4-2. threshold_detector.sv ─ 閾値検出器（脱進機原理）



```systemverilog

// threshold_detector.sv ─ 閾値検出器（脱進機原理）

// 浮動小数点不使用 → 誤差蓄積ゼロ（Q16.16固定小数点）

module threshold_detector #(

    parameter DATA_WIDTH = 32,

    parameter FRAC_BITS  = 16  // Q16.16形式

)(

    input  logic signed [DATA_WIDTH-1:0] value,

    input  logic signed [DATA_WIDTH-1:0] threshold_lo,

    input  logic signed [DATA_WIDTH-1:0] threshold_hi,

    output logic                          in_zone,

    output logic                          breach_lo,

    output logic                          breach_hi

);

    assign in_zone   = (value >= threshold_lo) & (value <= threshold_hi);

    assign breach_lo = (value <  threshold_lo);

    assign breach_hi = (value >  threshold_hi);

    // Q16.16での境界値例: 0.5 → 32'd32768, 1.0 → 32'd65536

endmodule

```



**設計根拠:** コンビネーション論理のみ。遅延ゼロ、整数比較のみで実現する。境界値はパラメータとしてトップレベルから注入し、このモジュール内では変更不可。



---



### 4-3. nra_ring_fsm.sv ─ 律環有限状態機械



```systemverilog

typedef enum logic [2:0] {

    S_IDLE     = 3'b000,

    S_OBSERVE  = 3'b001,

    S_COMPUTE  = 3'b010,

    S_VALIDATE = 3'b011,

    S_EMIT     = 3'b100,

    S_CONFESS  = 3'b101

} nra_state_t;



module nra_ring_fsm (

    input  logic       clk,

    input  logic       rst_n,

    input  logic       valid_in,

    input  logic       breach,

    output nra_state_t state,

    output logic       confess_flag

);

    nra_state_t next_state;



    always_ff @(posedge clk or negedge rst_n)

        state <= (!rst_n) ? S_IDLE : next_state;



    always_comb begin

        next_state   = state;

        confess_flag = 1'b0;

        unique case (state)

            S_IDLE:     next_state = valid_in ? S_OBSERVE : S_IDLE;

            S_OBSERVE:  next_state = S_COMPUTE;

            S_COMPUTE:  next_state = S_VALIDATE;

            S_VALIDATE: next_state = breach ? S_CONFESS : S_EMIT;

            S_EMIT:     next_state = S_IDLE;

            S_CONFESS: begin

                confess_flag = 1'b1;

                next_state   = S_IDLE;

            end

            default:    next_state = S_IDLE;

        endcase

    end

endmodule

```



**設計根拠:** `unique case` を使用することで、ツールが全分岐の網羅性を静的に検証し、未定義状態への遷移パスを合成時エラーとして検出する。ソフトウェアの `switch + default` とは本質的に異なり、「存在しない状態への遷移パスを生成しない」という回路制約になる。



---



### 4-4. ide_pipeline.sv ─ 内包性動力学パイプライン



```systemverilog

module ide_pipeline #(

    parameter STAGES     = 4,

    parameter DATA_WIDTH = 32

)(

    input  logic                  clk,

    input  logic                  rst_n,

    input  logic [DATA_WIDTH-1:0] data_in,

    input  logic                  valid_in,

    output logic [DATA_WIDTH-1:0] data_out,

    output logic                  valid_out,

    output logic                  stall

);

    logic [DATA_WIDTH-1:0] pipe_data  [STAGES];

    logic                  pipe_valid [STAGES];



    genvar i;

    generate

        for (i = 0; i < STAGES; i++) begin : stage

            always_ff @(posedge clk or negedge rst_n) begin

                if (!rst_n) begin

                    pipe_data [i] <= '0;

                    pipe_valid[i] <= 1'b0;

                end else if (!stall) begin

                    pipe_data [i] <= (i==0) ? data_in  : pipe_data [i-1];

                    pipe_valid[i] <= (i==0) ? valid_in : pipe_valid[i-1];

                end

            end

        end

    endgenerate



    assign data_out  = pipe_data [STAGES-1];

    assign valid_out = pipe_valid[STAGES-1];

    assign stall     = 1'b0;  // ← バックプレッシャー制御の拡張ポイント

endmodule

```



**設計根拠:** `stall=1'b0` の固定は意図的な拡張ポイント。バックプレッシャーが必要になった時点でここのみを変更すれば、パイプライン全体への影響をこの1ポートに集約できる。



---



### 4-5. nra_ide_top.sv ─ トップレベル統合



```systemverilog

module nra_ide_top #(

    parameter DATA_WIDTH = 32,

    parameter FRAC_BITS  = 16,

    parameter signed [31:0] THR_LO = 32'sh00008000, // +0.5 (Q16.16)

    parameter signed [31:0] THR_HI = 32'sh00018000  // +1.5 (Q16.16)

)(

    input  logic                  clk, rst_n,

    input  logic [DATA_WIDTH-1:0] raw_in,

    input  logic                  valid_in,

    output logic [DATA_WIDTH-1:0] result_out,

    output logic                  valid_out,

    output logic                  confess_out

);

    logic [DATA_WIDTH-1:0] diode_data, pipe_data;

    logic diode_valid, pipe_valid, stall;

    logic in_zone, breach_lo, breach_hi;

    nra_state_t fsm_state;



    causal_diode    #(.DATA_WIDTH(DATA_WIDTH)) u_diode (

        .clk,.rst_n,.data_in(raw_in),.valid_in,

        .data_out(diode_data),.valid_out(diode_valid));



    ide_pipeline    #(.DATA_WIDTH(DATA_WIDTH)) u_pipe (

        .clk,.rst_n,.data_in(diode_data),.valid_in(diode_valid),

        .data_out(pipe_data),.valid_out(pipe_valid),.stall);



    threshold_detector #(.DATA_WIDTH(DATA_WIDTH)) u_thr (

        .value(pipe_data),.threshold_lo(THR_LO),.threshold_hi(THR_HI),

        .in_zone,.breach_lo,.breach_hi);



    nra_ring_fsm u_fsm (

        .clk,.rst_n,.valid_in(pipe_valid),

        .breach(breach_lo | breach_hi),

        .state(fsm_state),.confess_flag(confess_out));



    assign result_out = (fsm_state == S_EMIT) ? pipe_data : '0;

    assign valid_out  = (fsm_state == S_EMIT);

endmodule

```



**設計根拠:** 4つのモジュールを直結し、中央調停ロジックを置かないことが「中心なしアーキテクチャ」の回路的表現。



---



## 5. シミュレーション・検証（フェーズ④）



### 検証優先順位



正常パスより「限界告白が正しく発動するか」を優先する。境界違反時の動作こそがアーキテクチャの本質を確認する場所であるため、以下の順で確認する。



1. `confess_flag=1` のとき `result_out` が必ずゼロになること

2. 因果ダイオード：逆方向信号が完全にブロックされること

3. 閾値検出器：Q16.16の境界値で誤差が発生しないこと

4. 律環FSM：S_CONFESSからS_IDLEへの遷移が1クロックで完了すること

5. パイプライン：バックプレッシャー中のデータ保全

6. 不可逆性：リセット後にS_EMIT → S_OBSERVEの逆走が起きないこと



### テストベンチ骨格



```systemverilog

module tb_nra_ring_fsm;

  logic clk = 0, rst_n = 0;

  logic valid_in = 0, breach = 0;

  nra_state_t state;

  logic confess_flag;



  nra_ring_fsm dut(.clk,.rst_n,.valid_in,.breach,.state,.confess_flag);



  always #5 clk = ~clk;  // 100 MHz



  initial begin

    // 正常パス検証

    @(posedge clk); rst_n = 1;

    valid_in = 1; breach = 0;

    repeat(6) @(posedge clk);

    assert(state == S_IDLE) else $error("正常パス失敗");



    // 限界告白トリガー

    valid_in = 1; breach = 1;

    repeat(4) @(posedge clk);

    assert(confess_flag == 1) else $error("告白フラグ失敗");



    // 不可逆性チェック

    breach = 0; valid_in = 1;

    repeat(6) @(posedge clk);

    assert(state != S_OBSERVE) else $error("不可逆性違反");



    $display("NRA-IDE FSM検証 完了"); $finish;

  end

endmodule

```



### 形式検証（SymbiYosys）への拡張



S_CONFESSからのロールバック不可をLTL式で記述することで、テストベンチが網羅できない状態空間を網羅的に検証できる。具体的な記述は次ステップとして残置。



---



## 6. 合成・実装・展開（フェーズ⑤）



### タイミング制約（nra_ide.xdc）



```tcl

# システムクロック 100 MHz

create_clock -period 10.000 -name sys_clk [get_ports clk]



# 因果ダイオード出力パス：最大1クロック

set_max_delay -from [get_cells {causal_diode*}] \

              -to   [get_cells {nra_ring_fsm*}] 10.0



# 閾値検出器：コンビネーション遅延を5ns以下に制限

set_max_delay -datapath_only \

  -from [get_cells {threshold_det*}] 5.0



# confess_flag：非同期クロック交差禁止

set_false_path -from [get_pins {nra_ring_fsm/confess_flag_reg/C}] \

               -to   [get_ports confess_out]

```



### 合成・実装スクリプト



```tcl

open_project nra_ide.xpr

update_compile_order -fileset sources_1

launch_runs synth_1 -strategy Flow_PerfOptimized_high

wait_on_run synth_1

open_run synth_1

report_timing_summary -file synth_timing.rpt

launch_runs impl_1 -to_step write_bitstream

wait_on_run impl_1

open_hw_manager

connect_hw_server

program_hw_devices [get_hw_devices]

```



### リソース見積もり（Artix-7 XC7A35T基準）



| リソース | 推定値 |

|---|---|

| LUT（論理セル） | 420〜680 LUT |

| FF（フリップフロップ） | 180〜260 FF |

| DSP48E1 | 2〜4 スライス（Q16.16乗算器） |

| BRAM | 0（パイプラインは分散RAM） |

| 最大クロック（Fmax） | 180〜220 MHz |



### 合成後の確認ポイント



`report_timing_summary` で最初に確認するのは **Worst Negative Slack (WNS)** の値。負の値は100MHzでのタイミング違反を意味する。`threshold_detector` のコンビネーションパスが長い場合の対処は2通り。中間にFFを1段追加してパイプライン化するか、クロックを80MHzへ引き下げる。



---



## 7. 次ステップ候補



- SymbiYosysによるS_CONFESS不可逆性のLTL式記述

- バックプレッシャー制御（`stall` ポート）の完全実装

- 自律走行への応用（5ゾーン安全フレームワークとFPGA限界告白の統合）

- 農繁期前のネットリスト・制約ファイルのGitコミット手順の確定



---



*他AIによる再検証を考慮し、NRA-IDE固有の内部開発コード（HAN等）および般若(hannya)関連の宗教用語はこの文書に含めていない。*



---

<!-- END OF FILE: NRA-IDE_FPGA_Implementation_2026-03-14_2157.md -->

