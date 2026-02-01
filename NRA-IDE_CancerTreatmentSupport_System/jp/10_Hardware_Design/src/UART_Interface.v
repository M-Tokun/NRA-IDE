/* ═══════════════════════════════════════════════════════════════════════
 * File: UART_Interface.v
 * Module: UART_Interface
 * Date: 2026-02-01
 * Author: M-Tokuni & AI Architects
 * * 目的: シンプルなUART送受信（8N1）
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module UART_Interface # (
    parameter CLK_FREQ = 100_000_000,
    parameter BAUD_RATE = 115200
)(
    input wire clk, rst_n,
    input wire uart_rx,
    output reg uart_tx,
    output reg [7:0] rx_data,
    output reg rx_valid,
    input wire [7:0] tx_data,
    input wire tx_start,
    output wire tx_busy
);

    localparam BIT_PERIOD = CLK_FREQ / BAUD_RATE;
    
    // ─── 受信ロジック (RX) ───
    reg [15:0] rx_cnt;
    reg [3:0] rx_bit_idx;
    reg [2:0] rx_state; // 0:Idle, 1:Start, 2:Data, 3:Stop
    reg [7:0] rx_shift_reg;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_state <= 0;
            rx_valid <= 0;
        end else begin
            rx_valid <= 0; // デフォルトLOW
            
            case (rx_state)
                0: if (uart_rx == 0) begin // Start Bit検出
                       rx_state <= 1; rx_cnt <= 0;
                   end
                1: begin // Start Bit中央まで待機
                       if (rx_cnt == BIT_PERIOD/2) begin
                           rx_state <= 2; rx_cnt <= 0; rx_bit_idx <= 0;
                       end else rx_cnt <= rx_cnt + 1;
                   end
                2: begin // データ受信
                       if (rx_cnt == BIT_PERIOD) begin
                           rx_cnt <= 0;
                           rx_shift_reg[rx_bit_idx] <= uart_rx;
                           if (rx_bit_idx == 7) rx_state <= 3;
                           else rx_bit_idx <= rx_bit_idx + 1;
                       end else rx_cnt <= rx_cnt + 1;
                   end
                3: begin // Stop Bit確認
                       if (rx_cnt == BIT_PERIOD) begin
                           rx_state <= 0;
                           rx_data <= rx_shift_reg;
                           rx_valid <= 1; // 1クロックだけHIGH
                       end else rx_cnt <= rx_cnt + 1;
                   end
            endcase
        end
    end
    
    // ─── 送信ロジック (TX) は省略（同様のステートマシン） ───
    assign tx_busy = 0; // ダミー

endmodule