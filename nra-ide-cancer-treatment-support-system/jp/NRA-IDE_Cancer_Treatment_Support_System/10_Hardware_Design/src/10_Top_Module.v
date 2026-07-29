/* ═══════════════════════════════════════════════════════════════════════
 * File:  10_Top_Module.v
 * Phase: 10 (System Integration)
 * Rev:   2.0  新規実装 (2026-07-29)
 * 目的:  UART 受信 → 演算 → UART 送信のシーケンス制御
 *
 * プロトコル (PHASE_5 §3):
 *   Host -> FPGA : 14 bytes
 *     [00]    Header    0xA5 (Type A) / 0xA6 (Type B)
 *     [01-12] Payload   6 パラメータ × 2 バイト (Q8.8, Big Endian)
 *     [13]    Checksum  ペイロード12バイトの XOR
 *
 *   FPGA -> Host : 3 bytes
 *     [00] Header    受信したヘッダと同一
 *     [01] Data      (Error << 1) | Jammed
 *     [02] Checksum  Header ^ Data
 *
 * チェックサム不一致時はパケットを破棄し、応答しない（Fail-Closed）。
 * ホストは3回まで再送し、それでも応答が得られなければ 0x05 ERR_COMM と
 * して扱う（fpga_interface.py と同じ設計）。誤った判定を返すより、
 * 何も返さない方が安全側である。
 *
 * 変形速度 v はプロトコルに含まれないため、Phase 4 の標準値
 * 200.0 um/s (0xC800) を定数として与える。cell_count も搬送されないため
 * Type B は動作しない（BioCalibrator_TypeB_Collective が 0x06 を返す）。
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module Top_Module #(
    parameter CLK_FREQ  = 100_000_000,
    parameter BAUD_RATE = 115200
)(
    input  wire clk,
    input  wire rst_n,
    input  wire uart_rx,
    output wire uart_tx,
    output wire led_status,   // 1 = BLOCKED
    output wire led_error     // 1 = エラーコードあり
);

    // Phase 4 標準値: 変形速度 200.0 um/s (Q8.8)
    localparam [15:0] DEFAULT_DEFORM_VELOCITY = 16'hC800;
    // cell_count は未搬送。Type B は未実装のため値は使われない
    localparam [7:0]  DEFAULT_CELL_COUNT      = 8'd1;

    // ── UART ────────────────────────────────────────────────────────
    wire [7:0] rx_data;
    wire       rx_valid;
    reg  [7:0] tx_data;
    reg        tx_start;
    wire       tx_busy;

    UART_Interface #(
        .CLK_FREQ(CLK_FREQ), .BAUD_RATE(BAUD_RATE)
    ) uart (
        .clk(clk), .rst_n(rst_n), .uart_rx(uart_rx), .uart_tx(uart_tx),
        .rx_data(rx_data), .rx_valid(rx_valid),
        .tx_data(tx_data), .tx_start(tx_start), .tx_busy(tx_busy)
    );

    // ── 受信シーケンス ──────────────────────────────────────────────
    reg [3:0]  rx_cnt;          // 0..13
    reg [7:0]  r_header;
    reg [7:0]  r_buf [0:11];    // ペイロード12バイト
    reg [7:0]  r_xor;           // ペイロードの running XOR
    reg        calc_trigger;
    reg        r_cancer_type;   // 0:TypeA, 1:TypeB

    reg [15:0] p_stiff, p_visc, p_diam, p_pore, p_flow, p_boost;

    integer i;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_cnt        <= 4'd0;
            r_header      <= 8'h00;
            r_xor         <= 8'h00;
            calc_trigger  <= 1'b0;
            r_cancer_type <= 1'b0;
            p_stiff <= 16'd0; p_visc  <= 16'd0; p_diam  <= 16'd0;
            p_pore  <= 16'd0; p_flow  <= 16'd0; p_boost <= 16'd0;
            for (i = 0; i < 12; i = i + 1) r_buf[i] <= 8'h00;
        end else begin
            calc_trigger <= 1'b0;   // 既定は1クロックパルス

            if (rx_valid) begin
                if (rx_cnt == 4'd0) begin
                    // ヘッダ待ち。0xA5 / 0xA6 以外は読み捨てて同期を保つ
                    if (rx_data == 8'hA5 || rx_data == 8'hA6) begin
                        r_header      <= rx_data;
                        r_cancer_type <= (rx_data == 8'hA6);
                        r_xor         <= 8'h00;
                        rx_cnt        <= 4'd1;
                    end
                end else if (rx_cnt <= 4'd12) begin
                    // ペイロード
                    r_buf[rx_cnt - 4'd1] <= rx_data;
                    r_xor                <= r_xor ^ rx_data;
                    rx_cnt               <= rx_cnt + 4'd1;
                end else begin
                    // チェックサム
                    if (rx_data == r_xor) begin
                        // アトミックに演算部へ転送する（PHASE_6 §4）
                        p_stiff <= {r_buf[0],  r_buf[1]};
                        p_visc  <= {r_buf[2],  r_buf[3]};
                        p_diam  <= {r_buf[4],  r_buf[5]};
                        p_pore  <= {r_buf[6],  r_buf[7]};
                        p_flow  <= {r_buf[8],  r_buf[9]};
                        p_boost <= {r_buf[10], r_buf[11]};
                        calc_trigger <= 1'b1;
                    end
                    // 不一致なら破棄。応答しない（ホストが再送する）
                    rx_cnt <= 4'd0;
                end
            end
        end
    end

    // ── 演算コア ────────────────────────────────────────────────────
    wire       core_jammed;
    wire [7:0] core_err;
    wire       core_valid;

    Cancer_Treatment_Selector core (
        .clk(clk), .rst_n(rst_n),
        .i_in_valid(calc_trigger),
        .i_cell_stiffness(p_stiff),
        .i_cell_viscosity(p_visc),
        .i_cell_diameter(p_diam),
        .i_pore_size(p_pore),
        .i_flow_dp(p_flow),
        .i_drug_boost(p_boost),
        .i_deform_velocity(DEFAULT_DEFORM_VELOCITY),
        .i_cell_count(DEFAULT_CELL_COUNT),
        .i_cancer_type(r_cancer_type),
        .o_is_jammed(core_jammed),
        .o_error_code(core_err),
        .o_out_valid(core_valid)
    );

    // ── 判定結果の保持 ──────────────────────────────────────────────
    reg       r_jammed;
    reg [7:0] r_err;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            r_jammed <= 1'b0;
            r_err    <= 8'h00;
        end else if (core_valid) begin
            r_jammed <= core_jammed;
            r_err    <= core_err;
        end
    end

    assign led_status = r_jammed;
    assign led_error  = |r_err;

    // ── 送信シーケンス（3バイト） ───────────────────────────────────
    localparam TX_IDLE = 2'd0, TX_LOAD = 2'd1, TX_BUSY = 2'd2, TX_DONE = 2'd3;

    reg [1:0] tx_state;
    reg [1:0] tx_idx;
    wire [7:0] resp_data = (r_err << 1) | (r_jammed ? 8'h01 : 8'h00);

    reg [7:0] tx_byte;
    always @(*) begin
        case (tx_idx)
            2'd0:    tx_byte = r_header;
            2'd1:    tx_byte = resp_data;
            default: tx_byte = r_header ^ resp_data;
        endcase
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx_state <= TX_IDLE;
            tx_idx   <= 2'd0;
            tx_start <= 1'b0;
            tx_data  <= 8'h00;
        end else begin
            tx_start <= 1'b0;
            case (tx_state)
                TX_IDLE: begin
                    if (core_valid) begin
                        tx_idx   <= 2'd0;
                        tx_state <= TX_LOAD;
                    end
                end
                TX_LOAD: begin
                    tx_data  <= tx_byte;
                    tx_start <= 1'b1;
                    tx_state <= TX_BUSY;
                end
                TX_BUSY: begin
                    // tx_start の1クロック後に tx_busy が立つ
                    if (tx_busy) tx_state <= TX_DONE;
                end
                TX_DONE: begin
                    if (!tx_busy) begin
                        if (tx_idx == 2'd2) begin
                            tx_state <= TX_IDLE;
                        end else begin
                            tx_idx   <= tx_idx + 2'd1;
                            tx_state <= TX_LOAD;
                        end
                    end
                end
            endcase
        end
    end

endmodule
