/* ═══════════════════════════════════════════════════════════════════════
 * File: 10_UART_Interface.v
 * Rev:  2.0 (2026-07-29) ビット周期の off-by-one を修正
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module UART_Interface # (
    parameter CLK_FREQ = 100_000_000,
    parameter BAUD_RATE = 115200
)(
    input wire clk, rst_n, uart_rx,
    output reg uart_tx,
    output reg [7:0] rx_data,
    output reg rx_valid,
    input wire [7:0] tx_data,
    input wire tx_start,
    output reg tx_busy
);
    localparam BIT_PERIOD = CLK_FREQ / BAUD_RATE;

    // RX Logic
    reg [15:0] rx_cnt;
    reg [3:0]  rx_bit_idx;
    reg [2:0]  rx_state;
    reg [7:0]  rx_shift;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin rx_state <= 0; rx_valid <= 0; rx_cnt <= 0; end
        else begin
            rx_valid <= 0;
            case (rx_state)
                // カウンタは 0 から始まるため、N クロック待つ条件は N-1 である。
                // BIT_PERIOD と比較すると 1 クロック余分に待ち、実効ボーレートが
                // CLK_FREQ/(BIT_PERIOD+1) になってビットごとに誤差が蓄積する。
                0: if (uart_rx == 0) begin rx_state <= 1; rx_cnt <= 0; end
                1: if (rx_cnt == (BIT_PERIOD/2) - 1) begin rx_state <= 2; rx_cnt <= 0; rx_bit_idx <= 0; end
                   else rx_cnt <= rx_cnt + 1;
                2: if (rx_cnt == BIT_PERIOD - 1) begin
                       rx_cnt <= 0; rx_shift[rx_bit_idx] <= uart_rx;
                       if (rx_bit_idx == 7) rx_state <= 3; else rx_bit_idx <= rx_bit_idx + 1;
                   end else rx_cnt <= rx_cnt + 1;
                3: if (rx_cnt == BIT_PERIOD - 1) begin rx_state <= 0; rx_data <= rx_shift; rx_valid <= 1; end
                   else rx_cnt <= rx_cnt + 1;
            endcase
        end
    end

    // TX Logic
    reg [15:0] tx_cnt;
    reg [3:0]  tx_bit_idx;
    reg [2:0]  tx_state;
    reg [7:0]  tx_shift;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin tx_state <= 0; uart_tx <= 1; tx_busy <= 0; tx_cnt <= 0; end
        else begin
            case (tx_state)
                0: if (tx_start) begin
                       tx_state <= 1; tx_shift <= tx_data; tx_busy <= 1; uart_tx <= 0; tx_cnt <= 0;
                   end else tx_busy <= 0;
                1: if (tx_cnt == BIT_PERIOD - 1) begin
                       tx_state <= 2; tx_cnt <= 0; tx_bit_idx <= 0; uart_tx <= tx_shift[0];
                   end else tx_cnt <= tx_cnt + 1;
                2: if (tx_cnt == BIT_PERIOD - 1) begin
                       tx_cnt <= 0;
                       if (tx_bit_idx == 7) begin tx_state <= 3; uart_tx <= 1; end
                       else begin tx_bit_idx <= tx_bit_idx + 1; uart_tx <= tx_shift[tx_bit_idx + 1]; end
                   end else tx_cnt <= tx_cnt + 1;
                3: if (tx_cnt == BIT_PERIOD - 1) begin tx_state <= 0; tx_busy <= 0; end
                   else tx_cnt <= tx_cnt + 1;
            endcase
        end
    end
endmodule