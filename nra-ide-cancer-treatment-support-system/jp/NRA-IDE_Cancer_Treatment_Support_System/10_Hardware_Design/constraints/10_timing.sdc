# ═══════════════════════════════════════════════════════════════════════
# File: timing.sdc
# Phase: 10
# 目的: タイミング制約 (100MHz)
# ═══════════════════════════════════════════════════════════════════════

# System Clock 100MHz (10ns)
create_clock -name sys_clk -period 10.0 [get_ports clk]

# UART Input Delay
set_input_delay -clock sys_clk -max 2.0 [get_ports uart_rx]
set_input_delay -clock sys_clk -min 0.5 [get_ports uart_rx]

# UART Output Delay
set_output_delay -clock sys_clk -max 2.0 [get_ports uart_tx]
set_output_delay -clock sys_clk -min 0.5 [get_ports uart_tx]

# False Paths (LEDs, Reset)
set_false_path -from [get_ports rst_n]
set_false_path -to [get_ports led_status]
set_false_path -to [get_ports led_error]