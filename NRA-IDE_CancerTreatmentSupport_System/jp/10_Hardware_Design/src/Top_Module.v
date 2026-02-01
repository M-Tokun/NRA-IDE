/* ═══════════════════════════════════════════════════════════════════════
 * File: Top_Module.v
 * Module: Top_Module
 * Date: 2026-02-01 (Final Fix)
 * Author: M-Tokuni & AI Architects
 * Project: NRA-IDE Cancer Treatment Support System
 * * 目的: システム全体の統合トップモジュール
 * * 通信プロトコル (Binary 14 Bytes):
 * [Header(0xA5)] [Stiff(2)] [Visc(2)] [Diam(2)] [Pore(2)] [Flow(2)] [Boost(2)] [CheckSum(1)]
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module Top_Module (
    input wire clk,            // 100MHz System Clock
    input wire rst_n,          // Reset (Active Low)
    input wire uart_rx,        // UART RX Pin
    output wire uart_tx,       // UART TX Pin
    output wire led_status,    // LED Green (SAFE)
    output wire led_error      // LED Red (ERROR)
);

    // ────────────────────────────────────
    // 内部レジスタ（Q8.8固定小数点）
    // ────────────────────────────────────
    reg [15:0] r_cell_stiffness;
    reg [15:0] r_cell_viscosity;
    reg [15:0] r_cell_diameter;
    reg [15:0] r_pore_size;
    reg [15:0] r_flow_dp;
    reg [15:0] r_drug_boost;
    
    // 定数・その他
    wire [15:0] w_deform_velocity = 16'h3200; // 仮固定 200.0 (dv/dt)
    wire [7:0]  w_cell_count = 8'd1;          // Type B用 (今回は1固定)
    wire        w_cancer_type = 1'b0;         // 0=TypeA, 1=TypeB (将来用)

    // ────────────────────────────────────
    // UART インターフェース接続
    // ────────────────────────────────────
    wire [7:0] rx_data;
    wire       rx_valid;
    wire [7:0] tx_data;
    reg        tx_start;
    wire       tx_busy;
    
    UART_Interface #(
        .CLK_FREQ(100_000_000),
        .BAUD_RATE(115200)
    ) uart_inst (
        .clk(clk),
        .rst_n(rst_n),
        .uart_rx(uart_rx),
        .uart_tx(uart_tx),
        .rx_data(rx_data),
        .rx_valid(rx_valid),
        .tx_data(tx_data),
        .tx_start(tx_start),
        .tx_busy(tx_busy)
    );

    // ────────────────────────────────────
    // バイナリ受信ステートマシン
    // ────────────────────────────────────
    reg [3:0] rx_counter;
    reg [7:0] rx_buffer [0:13]; // 14バイトバッファ
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_counter <= 0;
            r_cell_stiffness <= 0;
            r_cell_viscosity <= 0;
            // ... 他もリセット
        end else if (rx_valid) begin
            // 1. ヘッダ同期 (0xA5待ち)
            if (rx_counter == 0) begin
                if (rx_data == 8'hA5) begin
                    rx_buffer[0] <= rx_data;
                    rx_counter <= 1;
                end
            end
            // 2. データ受信
            else begin
                rx_buffer[rx_counter] <= rx_data;
                rx_counter <= rx_counter + 1;
                
                // 3. パケット完了 (14バイト目)
                if (rx_counter == 13) begin
                    rx_counter <= 0;
                    // チェックサム検証（簡易的にXOR総和が0になるか等）
                    // ここでは信頼して直接ロード（B4学生向け簡易実装）
                    r_cell_stiffness <= {rx_buffer[1], rx_buffer[2]};
                    r_cell_viscosity <= {rx_buffer[3], rx_buffer[4]};
                    r_cell_diameter  <= {rx_buffer[5], rx_buffer[6]};
                    r_pore_size      <= {rx_buffer[7], rx_buffer[8]};
                    r_flow_dp        <= {rx_buffer[9], rx_buffer[10]};
                    r_drug_boost     <= {rx_buffer[11], rx_buffer[12]};
                end
            end
        end
    end

    // ────────────────────────────────────
    // コアロジック接続
    // ────────────────────────────────────
    wire w_is_jammed;
    wire [7:0] w_error_code;
    
    Cancer_Treatment_Selector core (
        .clk(clk),
        .rst_n(rst_n),
        .i_cell_stiffness(r_cell_stiffness),
        .i_cell_viscosity(r_cell_viscosity),
        .i_cell_diameter(r_cell_diameter),
        .i_pore_size(r_pore_size),
        .i_flow_dp(r_flow_dp),
        .i_drug_boost(r_drug_boost),
        .i_deform_velocity(w_deform_velocity),
        .i_cell_count(w_cell_count),
        .i_cancer_type(w_cancer_type),
        .o_is_jammed(w_is_jammed),
        .o_error_code(w_error_code)
    );

    // ────────────────────────────────────
    // 結果送信ロジック（簡易版）
    // ────────────────────────────────────
    // ホストから受信完了直後に結果を返すエコーバック方式
    reg [2:0] tx_state;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx_state <= 0;
            tx_start <= 0;
        end else begin
            case (tx_state)
                0: begin // トリガー待ち（受信完了フラグで起動推奨）
                    if (rx_counter == 13 && rx_valid) tx_state <= 1;
                end
                1: begin // ヘッダ送信
                     // ... 実装省略（UART_Interfaceへ順次データを投げる）
                     tx_state <= 0; 
                end
            endcase
        end
    end
    
    // LED表示
    assign led_status = w_is_jammed;  // SAFEなら点灯
    assign led_error  = (w_error_code != 0); // エラーなら点灯

endmodule