/* ═══════════════════════════════════════════════════════════════════════
 * File:  10_Testbench_TypeA_Cases.v
 * Phase: 10 (Verification)
 * Date:  2026-07-29
 * 目的:  BioCalibrator_TypeA_Jamming を Phase 30 の7ケースで検証する。
 *
 * 期待値は 30_Test_Data/expected_results.json と同一である。
 *   expected = (error_code << 1) | is_jammed
 *
 * 入力の Q8.8 値は、ホスト側 _float_to_q8_8() と同じ「切り捨て」で求める。
 *   0.05 -> 0x000C (12)      0.6 -> 0x0099 (153)      200.0 -> 0xC800
 *
 * 実行:
 *   iverilog -o tb.vvp ../src/10_BioCalibrator_TypeA.v 10_Testbench_TypeA_Cases.v
 *   vvp tb.vvp
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module Testbench_TypeA_Cases;

    reg clk, rst_n, in_valid;
    reg [15:0] E, eta, D, d, dP, B, v;
    wire jammed, out_valid;
    wire [7:0] err;

    integer pass_count = 0;
    integer fail_count = 0;

    BioCalibrator_TypeA_Jamming dut (
        .clk(clk), .rst_n(rst_n),
        .i_in_valid(in_valid),
        .i_cell_stiffness(E),
        .i_cell_viscosity(eta),
        .i_cell_diameter(D),
        .i_pore_size(d),
        .i_flow_dp(dP),
        .i_drug_boost(B),
        .i_deform_velocity(v),
        .o_is_jammed(jammed),
        .o_error_code(err),
        .o_out_valid(out_valid)
    );

    // 100MHz
    always #5 clk = ~clk;

    // 1件を投入し、パイプライン完了を待って期待値と照合する
    task run_case;
        input [63:0] name;          // 8文字までのケース名
        input [15:0] i_E, i_eta, i_D, i_d, i_dP, i_B;
        input [7:0]  expected;
        reg   [7:0]  actual;
        integer guard;
        begin
            @(negedge clk);
            E = i_E; eta = i_eta; D = i_D; d = i_d; dP = i_dP; B = i_B;
            v = 16'hC800;           // 200.0 um/s (Phase 4 標準値)
            in_valid = 1'b1;
            @(negedge clk);
            in_valid = 1'b0;

            // o_out_valid は1クロックのパルス。取りこぼさないよう毎エッジ確認する
            guard = 0;
            while (out_valid !== 1'b1 && guard < 20) begin
                @(posedge clk);
                guard = guard + 1;
            end

            if (out_valid !== 1'b1) begin
                $display("  %0s : TIMEOUT (o_out_valid が立たない)", name);
                fail_count = fail_count + 1;
            end else begin
                actual = (err << 1) | (jammed ? 8'h01 : 8'h00);
                if (actual === expected) begin
                    $display("  %0s : [PASS] 0x%02h", name, actual);
                    pass_count = pass_count + 1;
                end else begin
                    $display("  %0s : [FAIL] actual=0x%02h expected=0x%02h (jammed=%b err=0x%02h)",
                             name, actual, expected, jammed, err);
                    fail_count = fail_count + 1;
                end
            end
            @(negedge clk);
        end
    endtask

    initial begin
        $display("--- BioCalibrator TypeA : Phase 30 Case Verification ---");
        clk = 0; rst_n = 0; in_valid = 0;
        E = 0; eta = 0; D = 0; d = 0; dP = 0; B = 0; v = 0;
        #20 rst_n = 1;
        #20;

        //        name        E        eta      D        d        dP       B        expected
        run_case("TC001", 16'h0180, 16'h000C, 16'h0C00, 16'h0800, 16'h0099, 16'h0000, 8'h00);
        run_case("TC002", 16'h0180, 16'h000C, 16'h0C00, 16'h0800, 16'h0099, 16'h0300, 8'h01);
        run_case("TC003", 16'h0300, 16'h000C, 16'h0C00, 16'h0800, 16'h0099, 16'h0000, 8'h01);
        run_case("TC004", 16'h0180, 16'h0000, 16'h0C00, 16'h0800, 16'h0099, 16'h0000, 8'h06);
        run_case("TC005", 16'h0180, 16'h000C, 16'h0600, 16'h0800, 16'h0099, 16'h0000, 8'h02);
        run_case("TC006", 16'h0080, 16'h000C, 16'h0C00, 16'h0800, 16'h0200, 16'h0000, 8'h00);
        run_case("TC007", 16'h0180, 16'h000C, 16'h0C00, 16'h0800, 16'h0099, 16'h0A00, 8'h01);

        $display("");
        $display("Summary: %0d / %0d cases passed.", pass_count, pass_count + fail_count);
        if (fail_count == 0)
            $display("[OK] RTL matches Phase 30 oracle.");
        else
            $display("[FAIL] RTL does NOT match the oracle.");
        $finish;
    end

endmodule
