/* ═══════════════════════════════════════════════════════════════════════
 * File: BioCalibrator_TypeB.v
 * Module: BioCalibrator_TypeB_Collective
 * Date: 2026-02-01
 * * 目的: Type B (Collective) 集団力学封鎖判定
 * * 物理式: F_total = N * F_single * (1 + α√N)
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module BioCalibrator_TypeB_Collective (
    input wire clk, rst_n,
    input wire [15:0] i_cell_stiffness,
    input wire [15:0] i_cell_viscosity,
    input wire [15:0] i_cell_diameter,
    input wire [15:0] i_pore_size,
    input wire [15:0] i_flow_dp,
    input wire [15:0] i_drug_boost,
    input wire [15:0] i_deform_velocity,
    input wire [7:0]  i_cell_count,       // 集団サイズ N
    output reg o_is_jammed,
    output reg [7:0] o_error_code
);

    // Stage 1: Geometry Check & Single Cell Force
    // Type Aと同じ計算を行う
    reg [15:0] r_delta_x;
    reg [31:0] r_f_single;
    reg r_err_geom;
    
    always @(posedge clk) begin
        if (i_cell_diameter < i_pore_size) begin
            r_delta_x <= 0;
            r_err_geom <= 1;
        end else begin
            r_delta_x <= i_cell_diameter - i_pore_size;
            r_err_geom <= 0;
            
            // F_single = (k + Boost) * dx + eta * v
            // 簡易化: 1クロックで計算（実際はパイプライン推奨）
            r_f_single <= (i_cell_stiffness + i_drug_boost) * (i_cell_diameter - i_pore_size) 
                        + (i_cell_viscosity * i_deform_velocity);
        end
    end

    // Stage 2: Collective Effect
    // F_total = F_single * N (簡易版: α項は省略または定数倍)
    // Q8.8における N倍
    reg [31:0] r_f_total;
    
    always @(posedge clk) begin
        r_f_total <= r_f_single * i_cell_count; 
    end

    // Stage 3: Comparison
    wire [31:0] w_flow_force = {16'b0, i_flow_dp} * 256;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            o_is_jammed <= 0;
            o_error_code <= 0;
        end else begin
            if (i_cell_viscosity == 0) o_error_code <= 8'h03;
            else if (r_err_geom)       o_error_code <= 8'h01;
            else begin
                o_error_code <= 0;
                // 集団効果で抵抗力が勝るか？
                if (r_f_total > w_flow_force) o_is_jammed <= 1;
                else                          o_is_jammed <= 0;
            end
        end
    end

endmodule