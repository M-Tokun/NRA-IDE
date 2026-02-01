/* ═══════════════════════════════════════════════════════════════════════
 * File: BioCalibrator_TypeA.v
 * Module: BioCalibrator_TypeA_Jamming
 * Date: 2026-02-01
 * * 目的: Type A (Jamming) 物理演算コア (Q8.8 Pipeline)
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module BioCalibrator_TypeA_Jamming (
    input wire clk, rst_n,
    input wire [15:0] i_cell_stiffness,
    input wire [15:0] i_cell_viscosity,
    input wire [15:0] i_cell_diameter,
    input wire [15:0] i_pore_size,
    input wire [15:0] i_flow_dp,
    input wire [15:0] i_drug_boost,
    input wire [15:0] i_deform_velocity,
    output reg o_is_jammed,
    output reg [7:0] o_error_code
);

    // Stage 1: Geometry Check
    reg [15:0] r_delta_x_s1;
    reg r_geom_err_s1;
    
    always @(posedge clk) begin
        if (i_cell_diameter < i_pore_size) begin
            r_delta_x_s1 <= 0;
            r_geom_err_s1 <= 1; // すり抜け発生
        end else begin
            r_delta_x_s1 <= i_cell_diameter - i_pore_size;
            r_geom_err_s1 <= 0;
        end
    end

    // Stage 2: Physics Calculation (Q8.8 Mult)
    // F_elastic = (k + Boost) * dx
    // F_viscous = eta * velocity
    reg [31:0] r_elastic_s2; // Mult result needs 32bit
    reg [31:0] r_viscous_s2;
    
    always @(posedge clk) begin
        r_elastic_s2 <= (i_cell_stiffness + i_drug_boost) * r_delta_x_s1;
        r_viscous_s2 <= i_cell_viscosity * i_deform_velocity;
    end

    // Stage 3: Summation & Comparison
    // 結果を 256 で割って Q8.8 に戻す処理が必要だが、
    // 比較対象の FlowDP も 256倍すれば割らなくて済む（高速化）
    wire [31:0] w_total_resist = r_elastic_s2 + r_viscous_s2;
    wire [31:0] w_flow_force   = {16'b0, i_flow_dp} * 256; // Q8.8同士の比較用スケーリング

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            o_is_jammed <= 0;
            o_error_code <= 0;
        end else begin
            if (i_cell_viscosity == 0) o_error_code <= 8'h03; // Zero Viscosity
            else if (r_geom_err_s1)    o_error_code <= 8'h01; // Geometric Error
            else begin
                o_error_code <= 0;
                if (w_total_resist > w_flow_force) o_is_jammed <= 1; // SAFE
                else                               o_is_jammed <= 0; // DANGER
            end
        end
    end

endmodule