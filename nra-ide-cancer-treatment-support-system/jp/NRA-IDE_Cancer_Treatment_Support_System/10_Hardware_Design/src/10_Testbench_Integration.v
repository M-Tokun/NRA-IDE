/* ═══════════════════════════════════════════════════════════════════════
 * File:  10_Testbench_Integration.v
 * Phase: 10 (Verification)
 * Rev:   2.0 (2026-07-29)
 * 目的:  UART を含む全系を Phase 30 の7ケースで検証する。
 *
 * 14バイトを送信し、3バイトの応答を受信して照合する。
 * チェックサムはタスク内で計算する（Rev 1.0 は 0x00 を直書きしており、
 * 正しくは 0x11 であった。Fail-Closed が働けば必ず破棄される値だった）。
 *
 * 実行:
 *   iverilog -o itb.vvp 10_Top_Module.v 10_Cancer_Treatment_Selector.v \
 *       10_BioCalibrator_TypeA.v 10_BioCalibrator_TypeB.v \
 *       10_UART_Interface.v 10_Testbench_Integration.v
 *   vvp itb.vvp
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module Testbench_Integration;

    // シミュレーション時間短縮のためボーレートを加速する。
    // 実機は BAUD_RATE = 115200 だが、その場合 1ビット 8681 ns となり
    // 8ケースで約12 ms、100MHz クロックで240万エッジを要して現実的でない。
    // UART のビット周期は CLK_FREQ / BAUD_RATE で決まるので、比を保てば
    // 論理の検証としては等価である。
    parameter CLK_FREQ  = 100_000_000;      // 100 MHz
    parameter BAUD_RATE = 1_000_000;        // 実機は 115_200（ビット周期100クロック）
    localparam CLK_NS   = 1_000_000_000 / CLK_FREQ;             // 10 ns
    localparam BIT_NS   = CLK_NS * (CLK_FREQ / BAUD_RATE);      // 100 ns

    reg  clk, rst_n, uart_rx;
    wire uart_tx, led_status, led_error;

    integer pass_count = 0;
    integer fail_count = 0;

    Top_Module #(
        .CLK_FREQ(CLK_FREQ), .BAUD_RATE(BAUD_RATE)
    ) dut (
        .clk(clk), .rst_n(rst_n), .uart_rx(uart_rx), .uart_tx(uart_tx),
        .led_status(led_status), .led_error(led_error)
    );

    always #(CLK_NS/2) clk = ~clk;

    // ── 1バイト送信 (8N1, LSB first) ────────────────────────────────
    task send_uart(input [7:0] data);
        integer i;
        begin
            uart_rx = 0; #BIT_NS;                       // start bit
            for (i = 0; i < 8; i = i + 1) begin
                uart_rx = data[i]; #BIT_NS;
            end
            uart_rx = 1; #BIT_NS;                       // stop bit
        end
    endtask

    // ── 1バイト受信 (uart_tx を監視) ────────────────────────────────
    task recv_uart(output [7:0] data);
        integer i;
        begin
            @(negedge uart_tx);                         // start bit
            #(BIT_NS + BIT_NS/2);                       // 最初のデータビット中央へ
            for (i = 0; i < 8; i = i + 1) begin
                data[i] = uart_tx; #BIT_NS;
            end
        end
    endtask

    // ── 14バイト送信（チェックサムは自動計算） ──────────────────────
    task send_packet(
        input [7:0]  header,
        input [15:0] stiff, visc, diam, pore, flow, boost
    );
        reg [7:0] cs;
        begin
            cs = stiff[15:8] ^ stiff[7:0] ^ visc[15:8] ^ visc[7:0]
               ^ diam[15:8]  ^ diam[7:0]  ^ pore[15:8] ^ pore[7:0]
               ^ flow[15:8]  ^ flow[7:0]  ^ boost[15:8] ^ boost[7:0];

            send_uart(header);
            send_uart(stiff[15:8]); send_uart(stiff[7:0]);
            send_uart(visc[15:8]);  send_uart(visc[7:0]);
            send_uart(diam[15:8]);  send_uart(diam[7:0]);
            send_uart(pore[15:8]);  send_uart(pore[7:0]);
            send_uart(flow[15:8]);  send_uart(flow[7:0]);
            send_uart(boost[15:8]); send_uart(boost[7:0]);
            send_uart(cs);
        end
    endtask

    // ── 1ケースの実行と照合 ─────────────────────────────────────────
    task run_case(
        input [63:0] name,
        input [15:0] stiff, visc, diam, pore, flow, boost,
        input [7:0]  expected
    );
        reg [7:0] h, d, c;
        begin
            // FPGA は最終バイトのストップビット送出中に応答を開始する。
            // 送信完了を待ってから受信を始めると立ち下がりを取りこぼすため、
            // 送信と受信を並行させる。
            fork
                send_packet(8'hA5, stiff, visc, diam, pore, flow, boost);
                begin
                    recv_uart(h);
                    recv_uart(d);
                    recv_uart(c);
                end
            join

            if (h !== 8'hA5)
                $display("  %0s : [FAIL] header=0x%02h (expected 0xA5)", name, h);
            else if (c !== (h ^ d))
                $display("  %0s : [FAIL] checksum=0x%02h (expected 0x%02h)", name, c, h ^ d);
            else if (d !== expected)
                $display("  %0s : [FAIL] data=0x%02h expected=0x%02h", name, d, expected);
            else begin
                $display("  %0s : [PASS] 0x%02h", name, d);
                pass_count = pass_count + 1;
                disable run_case;
            end
            fail_count = fail_count + 1;
        end
    endtask

    // ── チェックサム不一致時の挙動確認 ──────────────────────────────
    task run_bad_checksum;
        integer waited;
        begin
            send_uart(8'hA5);
            send_uart(8'h01); send_uart(8'h80);
            send_uart(8'h00); send_uart(8'h0C);
            send_uart(8'h0C); send_uart(8'h00);
            send_uart(8'h08); send_uart(8'h00);
            send_uart(8'h00); send_uart(8'h99);
            send_uart(8'h00); send_uart(8'h00);
            send_uart(8'h00);                       // 誤ったチェックサム（正: 0x10）

            // 応答が返らないことを確認する（Fail-Closed）
            waited = 0;
            while (uart_tx === 1'b1 && waited < 40) begin
                #BIT_NS; waited = waited + 1;
            end
            if (uart_tx === 1'b1) begin
                $display("  BADSUM : [PASS] 応答なし（パケット破棄）");
                pass_count = pass_count + 1;
            end else begin
                $display("  BADSUM : [FAIL] 誤パケットに応答した");
                fail_count = fail_count + 1;
            end
        end
    endtask

    initial begin
        $display("--- Top_Module Integration : Phase 30 Case Verification ---");
        clk = 0; rst_n = 0; uart_rx = 1;
        #100 rst_n = 1;
        #100;

        //        name        stiff     visc      diam      pore      flow      boost     expected
        run_case("TC001", 16'h0180, 16'h000C, 16'h0C00, 16'h0800, 16'h0099, 16'h0000, 8'h00);
        run_case("TC002", 16'h0180, 16'h000C, 16'h0C00, 16'h0800, 16'h0099, 16'h0300, 8'h01);
        run_case("TC003", 16'h0300, 16'h000C, 16'h0C00, 16'h0800, 16'h0099, 16'h0000, 8'h01);
        run_case("TC004", 16'h0180, 16'h0000, 16'h0C00, 16'h0800, 16'h0099, 16'h0000, 8'h06);
        run_case("TC005", 16'h0180, 16'h000C, 16'h0600, 16'h0800, 16'h0099, 16'h0000, 8'h02);
        run_case("TC006", 16'h0080, 16'h000C, 16'h0C00, 16'h0800, 16'h0200, 16'h0000, 8'h00);
        run_case("TC007", 16'h0180, 16'h000C, 16'h0C00, 16'h0800, 16'h0099, 16'h0A00, 8'h01);

        run_bad_checksum;

        $display("");
        $display("Summary: %0d / %0d checks passed.", pass_count, pass_count + fail_count);
        if (fail_count == 0)
            $display("[OK] Full-path integration verified.");
        else
            $display("[FAIL] Integration mismatch.");
        $finish;
    end

endmodule
