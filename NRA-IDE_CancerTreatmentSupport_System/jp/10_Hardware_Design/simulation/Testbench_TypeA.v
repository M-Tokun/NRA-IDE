/* ═══════════════════════════════════════════════════════════════════════
 * File: Testbench_TypeA.v
 * Date: 2026-02-01
 * * 目的: Type A モジュールの境界値テスト（Fail-Closed確認）
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module Testbench_TypeA;
    // ... (信号定義はBruteForceと同様)
    reg clk, rst_n;
    reg [15:0] stiff, visc, diam, pore, flow, boost, vel;
    wire jammed;
    wire [7:0] err;

    BioCalibrator_TypeA_Jamming dut (
        .clk(clk), .rst_n(rst_n),
        .i_cell_stiffness(stiff), .i_cell_viscosity(visc),
        .i_cell_diameter(diam), .i_pore_size(pore),
        .i_flow_dp(flow), .i_drug_boost(boost),
        .i_deform_velocity(vel),
        .o_is_jammed(jammed), .o_error_code(err)
    );
    
    always #5 clk = ~clk;

    initial begin
        clk = 0; rst_n = 0;
        #20 rst_n = 1;
        
        // Case 1: Viscosity Zero (Should fail)
        visc = 0;
        #20;
        if (err == 8'h03) $display("✓ PASS: Zero Viscosity Detected");
        else              $display("✗ FAIL: Zero Viscosity Missed");

        // Case 2: Geometric Error (Diameter < Pore)
        visc = 16'h000D;
        diam = 16'h0500; // 5.0
        pore = 16'h0800; // 8.0
        #20;
        if (err == 8'h01) $display("✓ PASS: Geometric Error Detected");
        else              $display("✗ FAIL: Geometric Error Missed");
        
        $finish;
    end
endmodule