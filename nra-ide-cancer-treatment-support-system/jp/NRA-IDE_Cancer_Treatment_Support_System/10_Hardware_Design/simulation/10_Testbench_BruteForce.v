/* ═══════════════════════════════════════════════════════════════════════
 * File: Testbench_BruteForce.v
 * Date: 2026-02-03 16:35 JST
 * 目的: 3段パイプライン遅延を考慮した Boost 最適値の自動探索
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module Testbench_BruteForce;
    // Signals
    reg clk, rst_n;
    reg i_in_valid;
    reg [15:0] stiff, visc, diam, pore, flow, boost, vel;
    wire jammed, o_out_valid;
    wire [7:0] err;

    // DUT Instance (Type A Revised)
    BioCalibrator_TypeA_Jamming dut (
        .clk(clk), .rst_n(rst_n),
        .i_in_valid(i_in_valid),
        .i_cell_stiffness(stiff),
        .i_cell_viscosity(visc),
        .i_cell_diameter(diam),
        .i_pore_size(pore),
        .i_flow_dp(flow),
        .i_drug_boost(boost),
        .i_deform_velocity(vel),
        .o_is_jammed(jammed),
        .o_error_code(err),
        .o_out_valid(o_out_valid)
    );

    // Clock Generation (100MHz)
    always #5 clk = ~clk;

    // Search Logic
    initial begin
        // 1. 初期化
        clk = 0; rst_n = 0; i_in_valid = 0;
        stiff = 16'h0180; // 1.5 (Q8.8)
        visc  = 16'h000D; // 0.05
        diam  = 16'h0C00; // 12.0
        pore  = 16'h0800; // 8.0
        flow  = 16'h0099; // 0.6
        vel   = 16'h3200; // 200.0
        boost = 16'h0000; // Start from 0.0
        
        #20 rst_n = 1; #20;

        $display("--- Starting Brute Force Search ---");

        // 2. 探索ループ (Boost を 0.01 刻みで増加)
        repeat (1000) begin
            // 入力パルスの生成
            @(posedge clk);
            i_in_valid = 1;
            @(posedge clk);
            i_in_valid = 0;

            // 3段パイプラインの完了待ち (o_out_valid が立ち上がるまで待機)
            wait(o_out_valid == 1);
            @(posedge clk); // 同期サンプリング

            // 判定評価
            if (jammed == 1) begin
                $display("✓ Solution Found! Boost = %h (Q8.8 representation)", boost);
                $display("  Physics: F_resist > F_flow confirmed.");
                #100;
                $finish;
            end

            // Boost 更新
            boost = boost + 16'h0003; // 約 +0.01
        end
        
        $display("✗ Solution Not Found within range.");
        $finish;
    end

endmodule