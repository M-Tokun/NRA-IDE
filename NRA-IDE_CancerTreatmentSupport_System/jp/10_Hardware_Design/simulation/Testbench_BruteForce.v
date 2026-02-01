/* ═══════════════════════════════════════════════════════════════════════
 * File: Testbench_BruteForce.v
 * Date: 2026-02-01
 * * 目的: 薬液濃度（Boost）をスイープして最適値を探索するシミュレーション
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module Testbench_BruteForce;

    reg clk, rst_n;
    reg [15:0] stiff, visc, diam, pore, flow, boost, vel;
    wire jammed;
    wire [7:0] err;

    // DUT接続 (Type A)
    BioCalibrator_TypeA_Jamming dut (
        .clk(clk), .rst_n(rst_n),
        .i_cell_stiffness(stiff), .i_cell_viscosity(visc),
        .i_cell_diameter(diam), .i_pore_size(pore),
        .i_flow_dp(flow), .i_drug_boost(boost),
        .i_deform_velocity(vel),
        .o_is_jammed(jammed), .o_error_code(err)
    );

    // Clock Gen
    always #5 clk = ~clk;

    initial begin
        // Init
        clk = 0; rst_n = 0;
        stiff = 16'h0180; // 1.5
        visc  = 16'h000D; // 0.05
        diam  = 16'h0C00; // 12.0
        pore  = 16'h0800; // 8.0
        flow  = 16'h0099; // 0.6
        vel   = 16'h3200; // 200.0
        boost = 0;
        
        #20 rst_n = 1;

        // Brute Force Search Loop
        // Boostを 0.00 から 10.00 まで増加
        repeat (1000) begin
            #10; // Wait for pipeline
            if (jammed == 1) begin
                $display("✓ Solution Found! Boost = %h (Q8.8)", boost);
                $finish;
            end
            boost = boost + 16'h0003; // +0.01 (approx)
        end
        
        $display("✗ Solution Not Found within range.");
        $finish;
    end

endmodule