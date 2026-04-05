/* ═══════════════════════════════════════════════════════════════════════
 * File: 10_Cancer_Treatment_Selector.v
 * Date: 2026-02-03 16:15 JST
 * 目的: Type A/B 演算器の同期信号（Valid）を含む完全統合
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module Cancer_Treatment_Selector (
    input wire clk, rst_n,
    input wire i_in_valid,            // Top_Moduleからの計算開始信号 
    input wire [15:0] i_cell_stiffness, i_cell_viscosity,
    input wire [15:0] i_cell_diameter, i_pore_size,
    input wire [15:0] i_flow_dp, i_drug_boost,
    input wire [15:0] i_deform_velocity,
    input wire [7:0]  i_cell_count,
    input wire        i_cancer_type,  // 0:TypeA, 1:TypeB [cite: 201]
    output wire       o_is_jammed,
    output wire [7:0] o_error_code,
    output wire       o_out_valid     // Top_Moduleへの計算完了通知 
);
    wire jam_a, jam_b, val_a, val_b;
    wire [7:0] err_a, err_b;

    // Type A: Jamming Model (10_BioCalibrator_TypeA.v) [cite: 174]
    BioCalibrator_TypeA_Jamming mod_a (
        .clk(clk), .rst_n(rst_n), .i_in_valid(i_in_valid),
        .i_cell_stiffness(i_cell_stiffness), .i_cell_viscosity(i_cell_viscosity),
        .i_cell_diameter(i_cell_diameter), .i_pore_size(i_pore_size),
        .i_flow_dp(i_flow_dp), .i_drug_boost(i_drug_boost),
        .i_deform_velocity(i_deform_velocity),
        .o_is_jammed(jam_a), .o_error_code(err_a), .o_out_valid(val_a)
    );

    // Type B: Collective Model (10_BioCalibrator_TypeB.v) [cite: 186]
    BioCalibrator_TypeB_Collective mod_b (
        .clk(clk), .rst_n(rst_n), .i_in_valid(i_in_valid),
        .i_cell_stiffness(i_cell_stiffness), .i_cell_viscosity(i_cell_viscosity),
        .i_cell_diameter(i_cell_diameter), .i_pore_size(i_pore_size),
        .i_flow_dp(i_flow_dp), .i_drug_boost(i_drug_boost),
        .i_deform_velocity(i_deform_velocity), .i_cell_count(i_cell_count),
        .o_is_jammed(jam_b), .o_error_code(err_b), .o_out_valid(val_b)
    );

    // MUX: 癌腫タイプによる出力の切り替え [cite: 206]
    assign o_is_jammed  = (i_cancer_type == 0) ? jam_a : jam_b;
    assign o_error_code = (i_cancer_type == 0) ? err_a : err_b;
    assign o_out_valid  = (i_cancer_type == 0) ? val_a : val_b;

endmodule