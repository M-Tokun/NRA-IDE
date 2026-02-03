/* File: 10_Testbench_Integration.v 26-0203-1605 JST */
`timescale 1ns / 1ps
module Testbench_Integration;
    reg clk, rst_n, uart_rx; wire uart_tx, led_status, led_error;
    Top_Module dut (.clk(clk), .rst_n(rst_n), .uart_rx(uart_rx), .uart_tx(uart_tx), .led_status(led_status), .led_error(led_error));
    always #5 clk = ~clk;
    task send_uart(input [7:0] data);
        integer i; begin
            uart_rx = 0; #8681; // Start bit (115200 baud)
            for (i=0; i<8; i=i+1) begin uart_rx = data[i]; #8681; end
            uart_rx = 1; #8681; // Stop bit
        end
    endtask
    initial begin
        clk = 0; rst_n = 0; uart_rx = 1; #100 rst_n = 1; #100;
        send_uart(8'hA5); // Header
        send_uart(8'h01); send_uart(8'h80); // Stiff 1.5
        send_uart(8'h00); send_uart(8'h0D); // Visc 0.05
        send_uart(8'h0C); send_uart(8'h00); // Diam 12.0
        send_uart(8'h08); send_uart(8'h00); // Pore 8.0
        send_uart(8'h00); send_uart(8'h99); // Flow 0.6
        send_uart(8'h00); send_uart(8'h00); // Boost 0.0
        send_uart(8'h00); // Checksum
        #2000000; $display("Simulation Finished"); $finish;
    end
endmodule