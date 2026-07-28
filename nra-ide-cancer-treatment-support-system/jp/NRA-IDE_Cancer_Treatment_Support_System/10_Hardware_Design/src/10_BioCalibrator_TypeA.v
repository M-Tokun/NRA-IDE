/* ═══════════════════════════════════════════════════════════════════════
 * File:  10_BioCalibrator_TypeA.v
 * Phase: 10 (Compute Core)
 * Rev:   2.0  応力比較形へ改訂 (2026-07-28)
 * 目的:  単一細胞ジャミング判定（PHASE_2 Rev 2.0 準拠）
 *
 * 判定式（全項 kPa, PHASE_2 §1）:
 *   sigma_el = (E + B) * (D - d)/D            … 弾性抵抗応力
 *   sigma_v  = 12 * eta * v * D / (1000 * d^2) … 孔内粘性抵抗応力
 *   sigma_el + sigma_v > dP  =>  BLOCKED（細胞は通過できない）
 *
 * 旧版(Rev 1.0)は (E+B)*(D-d) を dP と直接比較していたため次元が閉じておらず、
 * 幾何エラー以外は常に BLOCKED へ張り付いていた。応力に乗じるべきは変位では
 * なく歪み (D-d)/D（無次元）である。
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module BioCalibrator_TypeA_Jamming (
    input  wire        clk, rst_n,
    input  wire        i_in_valid,           // 演算開始パルス
    input  wire [15:0] i_cell_stiffness,     // E    [kPa]   Q8.8
    input  wire [15:0] i_cell_viscosity,     // eta  [Pa*s]  Q8.8
    input  wire [15:0] i_cell_diameter,      // D    [um]    Q8.8
    input  wire [15:0] i_pore_size,          // d    [um]    Q8.8
    input  wire [15:0] i_flow_dp,            // dP   [kPa]   Q8.8
    input  wire [15:0] i_drug_boost,         // B    [kPa]   Q8.8
    input  wire [15:0] i_deform_velocity,    // v    [um/s]  Q8.8
    output reg         o_is_jammed,          // 1 = BLOCKED, 0 = PASSABLE
    output reg  [7:0]  o_error_code,
    output reg         o_out_valid           // i_in_valid から5クロック後
);

    // ── Phase 4 準拠の入力範囲 (Q8.8) ───────────────────────────────
    localparam [15:0] D_MIN = 16'h0500, D_MAX = 16'h1E00; //  5.0 - 30.0 um
    localparam [15:0] P_MIN = 16'h0500, P_MAX = 16'h0F00; //  5.0 - 15.0 um
    localparam [15:0] E_MIN = 16'h0019, E_MAX = 16'h0A00; //  0.1 - 10.0 kPa
    localparam [15:0] B_MAX = 16'h0A00;                   //  0.0 - 10.0 kPa
    localparam [15:0] N_MIN = 16'h0002, N_MAX = 16'h0100; // 0.01 -  1.0 Pa*s
    localparam [15:0] F_MAX = 16'h0500;                   //  0.0 -  5.0 kPa

    // ── Phase 4 エラーコード ────────────────────────────────────────
    localparam [7:0] ERR_NONE  = 8'h00,
                     ERR_GEOM  = 8'h01,   // D < d       すり抜け
                     ERR_RANGE = 8'h02,   // 範囲外入力
                     ERR_VISC0 = 8'h03,   // eta = 0     律環公理違反
                     ERR_OVF   = 8'h04;   // 演算オーバーフロー

    // ── 定数ROM (PHASE_6 §3) ────────────────────────────────────────
    // 添字 idx = X[12:6]（物理量を 0.25um 刻みに量子化, X = idx/4 [um]）
    //   rom_recip[idx] = 1/D          を Q0.16 で保持
    //   rom_kvisc[idx] = 0.012 / d^2  を Q0.24 で保持 (0.012 = 12/1000)
    // 添字 20 未満（5.0um 未満）は 0。抵抗応力を 0 = PASSABLE 側へ倒す。
    reg [15:0] rom_recip [0:127];
    reg [15:0] rom_kvisc [0:127];
    integer n;
    initial begin
        for (n = 0; n < 128; n = n + 1) begin
            rom_recip[n] = (n < 20) ? 16'd0 : (262144 / n);
            rom_kvisc[n] = (n < 20) ? 16'd0 : (3221225 / (n * n));
        end
    end

    // ── Stage 1: 入力ラッチ・妥当性判定・幾何 ───────────────────────
    // 全入力を同時にラッチする（Rev 1.0 のラッチ漏れによる段間食い違いを是正）
    reg        v1;
    reg [15:0] e1, n1, d1, f1, b1, u1;
    reg [15:0] dx1;
    reg [6:0]  idxD1, idxd1;
    reg [7:0]  err1;

    wire out_of_range =
        (i_cell_diameter  < D_MIN) || (i_cell_diameter  > D_MAX) ||
        (i_pore_size      < P_MIN) || (i_pore_size      > P_MAX) ||
        (i_cell_stiffness < E_MIN) || (i_cell_stiffness > E_MAX) ||
        (i_drug_boost     > B_MAX) ||
        (i_cell_viscosity < N_MIN) || (i_cell_viscosity > N_MAX) ||
        (i_flow_dp        > F_MAX);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            v1 <= 1'b0; err1 <= ERR_NONE; dx1 <= 16'd0;
            idxD1 <= 7'd0; idxd1 <= 7'd0;
            e1 <= 16'd0; n1 <= 16'd0; d1 <= 16'd0;
            f1 <= 16'd0; b1 <= 16'd0; u1 <= 16'd0;
        end else begin
            v1 <= i_in_valid;
            e1 <= i_cell_stiffness;  n1 <= i_cell_viscosity;
            d1 <= i_cell_diameter;   f1 <= i_flow_dp;
            b1 <= i_drug_boost;      u1 <= i_deform_velocity;

            idxD1 <= i_cell_diameter[12:6];
            idxd1 <= i_pore_size[12:6];

            // 判定順序は PHASE_4 §2.1 で固定: 0x03 -> 0x02 -> 0x01
            if (i_cell_viscosity == 16'd0)               err1 <= ERR_VISC0;
            else if (out_of_range)                       err1 <= ERR_RANGE;
            else if (i_cell_diameter < i_pore_size)      err1 <= ERR_GEOM;
            else                                         err1 <= ERR_NONE;

            dx1 <= (i_cell_diameter < i_pore_size)
                   ? 16'd0 : (i_cell_diameter - i_pore_size);
        end
    end

    // ── Stage 2: ROM参照・k_eff・eta*v ──────────────────────────────
    reg        v2;
    reg [15:0] dx2, d2, f2, recip2, kvis2;
    reg [16:0] keff2;            // E + B (最大 20.0 kPa = 17bit)
    reg [31:0] etav2;            // eta * v   Q16.16
    reg [7:0]  err2;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            v2 <= 1'b0; err2 <= ERR_NONE; dx2 <= 16'd0; d2 <= 16'd0;
            f2 <= 16'd0; recip2 <= 16'd0; kvis2 <= 16'd0;
            keff2 <= 17'd0; etav2 <= 32'd0;
        end else begin
            v2 <= v1; err2 <= err1; dx2 <= dx1; d2 <= d1; f2 <= f1;
            recip2 <= rom_recip[idxD1];
            kvis2  <= rom_kvisc[idxd1];
            keff2  <= {1'b0, e1} + {1'b0, b1};
            etav2  <= n1 * u1;
        end
    end

    // ── Stage 3: 歪み・粘性係数 ─────────────────────────────────────
    reg        v3;
    reg [15:0] strain3;          // (D-d)/D            Q0.8
    reg [15:0] q1_3;             // 0.012*eta*v/d^2    Q0.16
    reg [15:0] d3, f3;
    reg [16:0] keff3;
    reg [7:0]  err3;

    wire [31:0] strain_mul = dx2 * recip2;   // Q8.8 * Q0.16 = eps * 2^24
    wire [47:0] q1_mul     = etav2 * kvis2;  // Q16.16 * Q0.24 = val * 2^40

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            v3 <= 1'b0; err3 <= ERR_NONE; strain3 <= 16'd0; q1_3 <= 16'd0;
            d3 <= 16'd0; f3 <= 16'd0; keff3 <= 17'd0;
        end else begin
            v3 <= v2; err3 <= err2; d3 <= d2; f3 <= f2; keff3 <= keff2;
            strain3 <= strain_mul[31:16];    // -> Q0.8
            q1_3    <= q1_mul[39:24];        // -> Q0.16
        end
    end

    // ── Stage 4: 応力の各項 ─────────────────────────────────────────
    reg        v4, ovf4;
    reg [15:0] sig_el4, sig_v4, f4;
    reg [7:0]  err4;

    wire [32:0] el_mul = keff3 * strain3;    // Q8.8  * Q0.8 = sigma * 2^16
    wire [31:0] v_mul  = q1_3  * d3;         // Q0.16 * Q8.8 = sigma * 2^24

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            v4 <= 1'b0; err4 <= ERR_NONE; ovf4 <= 1'b0;
            sig_el4 <= 16'd0; sig_v4 <= 16'd0; f4 <= 16'd0;
        end else begin
            v4 <= v3; err4 <= err3; f4 <= f3;
            // いずれも Q8.8 へ戻す（弾性項は >>8、粘性項は >>16）
            sig_el4 <= el_mul[23:8];
            sig_v4  <= v_mul[31:16];
            // 弾性項のみオーバーフローしうる（sigma_el >= 256.0 kPa）
            ovf4    <= |el_mul[32:24];
        end
    end

    // ── Stage 5: 合算・比較・エラー確定 ─────────────────────────────
    wire [16:0] sig_total = {1'b0, sig_el4} + {1'b0, sig_v4};
    wire        overflow  = ovf4 | sig_total[16];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            o_is_jammed <= 1'b0; o_error_code <= ERR_NONE; o_out_valid <= 1'b0;
        end else begin
            o_out_valid <= v4;
            if (err4 != ERR_NONE) begin
                // Fail-Closed: 異常時は転移リスク側（PASSABLE）へ倒す
                o_error_code <= err4;
                o_is_jammed  <= 1'b0;
            end else if (overflow) begin
                o_error_code <= ERR_OVF;
                o_is_jammed  <= 1'b0;
            end else begin
                o_error_code <= ERR_NONE;
                o_is_jammed  <= (sig_total[15:0] > f4);
            end
        end
    end

endmodule
