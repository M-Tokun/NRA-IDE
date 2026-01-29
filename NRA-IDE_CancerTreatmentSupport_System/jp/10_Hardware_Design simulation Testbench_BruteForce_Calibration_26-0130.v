/* Module: Testbench_BruteForce (2026-01-30) */
/* Description: 最悪条件に対し、適合値が見つかるまで薬剤濃度を上げ続ける総当たり試験機 */

`timescale 1ns / 1ps

module Testbench_BruteForce_Calibration;
    reg [15:0] t_cell_stiffness;
    reg [15:0] t_cell_diameter;
    reg [15:0] t_pore_size;
    reg [15:0] t_blood_pressure;
    reg [15:0] t_drug_boost;
    wire t_is_jammed;

    BioCalibrator_Core_Logic DUT (
        .i_cell_stiffness(t_cell_stiffness), .i_cell_diameter(t_cell_diameter),
        .i_pore_size(t_pore_size), .i_blood_pressure(t_blood_pressure),
        .i_drug_boost(t_drug_boost), .o_is_jammed(t_is_jammed)
    );

    initial begin
        // Worst Case Scenario Setup
        t_cell_stiffness = 16'h0080; // 0.5 kPa
        t_cell_diameter  = 16'h0C00; // 12.0 um
        t_pore_size      = 16'h0800; // 8.0 um
        t_blood_pressure = 16'h0258; // 600 Pa
        t_drug_boost     = 0;

        // Brute Force Loop
        while (t_drug_boost < 16'hFFFF) begin
            #1; // Wait 1ns
            if (t_is_jammed == 1'b1) begin
                $display(">> MATCH FOUND! Boost: +%1.3f kPa", t_drug_boost / 256.0);
                $finish;
            end
            t_drug_boost = t_drug_boost + 1; // Increment 0.004 kPa
        end
    end
endmodule