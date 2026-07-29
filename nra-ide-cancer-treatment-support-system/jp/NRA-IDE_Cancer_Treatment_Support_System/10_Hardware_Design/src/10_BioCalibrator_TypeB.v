/* ═══════════════════════════════════════════════════════════════════════
 * File:  10_BioCalibrator_TypeB.v
 * Phase: 10 (Compute Core)
 * Rev:   2.0  未実装を明示するスタブ (2026-07-29)
 *
 * Type B（細胞集団のスクラム効果）は実装しない。ERR_UNSUPPORTED (0x06) を
 * 返し、判定は行わない。理由は3つある。
 *
 *   1. モデルが未検証である。PHASE_2 §3 の sqrt(N) 則は現象論であり、
 *      増幅係数 alpha も 60_Research の文献では裏付けられていない。
 *      検証プロトコル（マイクロ流路試験）も Type A のみを対象としている。
 *
 *   2. 入力が届かない。現行の14バイトプロトコルは cell_count (N) を
 *      搬送しない（PHASE_5 §3.3）。N なしにクラスター判定はできない。
 *
 *   3. 未検証の物理式を回路にすると、判定が出てしまう。出た判定は
 *      読まれる。根拠のない数値を出すより、出さない方が安全側である。
 *
 * ホスト側 nra_core_model.evaluate() も Type B に対して同じ 0x06 を返す。
 * ハードウェアとホストで挙動を一致させてある。
 *
 * 【実装する場合】
 *   PHASE_2 §3 の検証を先に済ませること。式を実装した時点で
 *   nra_core_model.py の MODEL_VERSION と VALIDATION_STATUS、および
 *   本ファイルの Rev を必ず更新すること。
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module BioCalibrator_TypeB_Collective (
    input  wire        clk, rst_n,
    input  wire        i_in_valid,
    input  wire [15:0] i_cell_stiffness, i_cell_viscosity,
    input  wire [15:0] i_cell_diameter, i_pore_size,
    input  wire [15:0] i_flow_dp, i_drug_boost,
    input  wire [15:0] i_deform_velocity,
    input  wire [7:0]  i_cell_count,
    output reg         o_is_jammed,
    output reg  [7:0]  o_error_code,
    output reg         o_out_valid
);

    localparam [7:0] ERR_UNSUPPORTED = 8'h06;

    // Type A と同じ5段の遅延で応答する（上位のシーケンスを共通化するため）
    reg [4:0] v_pipe;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            v_pipe      <= 5'b0;
            o_is_jammed <= 1'b0;
            o_error_code<= 8'h00;
            o_out_valid <= 1'b0;
        end else begin
            v_pipe      <= {v_pipe[3:0], i_in_valid};
            o_out_valid <= v_pipe[4];
            // Fail-Closed: 判定せず、転移リスク側（PASSABLE）へ倒す
            o_is_jammed <= 1'b0;
            o_error_code<= ERR_UNSUPPORTED;
        end
    end

endmodule
