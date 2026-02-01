/* ═══════════════════════════════════════════════════════════════════════
 * File: Cancer_Treatment_Selector.v
 * Module: Cancer_Treatment_Selector
 * Date: 2026-02-01
 * * 目的: Type A/B 切り替えモジュール
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module Cancer_Treatment_Selector (
    input wire clk, rst_n,
    input wire [15:0] i_cell_stiffness,
    input wire [15:0] i_cell_viscosity,
    input wire [15:0] i_cell_diameter,
    input wire [15:0] i_pore_size,
    input wire [15:0] i_flow_dp,
    input wire [15:0] i_drug_boost,
    input wire [15:0] i_deform_velocity,
    input wire [7:0]  i_cell_count,
    input wire        i_cancer_type, // 0:TypeA, 1:TypeB
    output wire       o_is_jammed,
    output wire [7:0] o_error_code
);

    wire w_jam_a, w_jam_b;
    wire [7:0] w_err_a, w_err_b;

    // Type A Instance
    BioCalibrator_TypeA_Jamming mod_a (
        .clk(clk), .rst_n(rst_n),
        .i_cell_stiffness(i_cell_stiffness),
        .i_cell_viscosity(i_cell_viscosity),
        .i_cell_diameter(i_cell_diameter),
        .i_pore_size(i_pore_size),
        .i_flow_dp(i_flow_dp),
        .i_drug_boost(i_drug_boost),
        .i_deform_velocity(i_deform_velocity),
        .o_is_jammed(w_jam_a),
        .o_error_code(w_err_a)
    );
    
    // Type B Instance (Dummy for now, assumes exists)
    // BioCalibrator_TypeB_Collective mod_b (...);
    assign w_jam_b = 0; // Placeholder
    assign w_err_b = 0; // Placeholder

    // MUX
    assign o_is_jammed  = (i_cancer_type == 0) ? w_jam_a : w_jam_b;
    assign o_error_code = (i_cancer_type == 0) ? w_err_a : w_err_b;

endmodule