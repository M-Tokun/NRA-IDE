# ═══════════════════════════════════════════════════════════════════════
# File: pinout_artix_7.xdc
# Phase: 10
# Target: Basys 3 (Artix-7)
# ═══════════════════════════════════════════════════════════════════════

# Clock (100MHz)
set_property PACKAGE_PIN W5 [get_ports clk]
set_property IOSTANDARD LVCMOS33 [get_ports clk]
create_clock -period 10.000 -name sys_clk [get_ports clk]

# Reset (BtnC)
set_property PACKAGE_PIN U18 [get_ports rst_n]
set_property IOSTANDARD LVCMOS33 [get_ports rst_n]

# UART
set_property PACKAGE_PIN B18 [get_ports uart_rx]
set_property IOSTANDARD LVCMOS33 [get_ports uart_rx]
set_property PACKAGE_PIN A18 [get_ports uart_tx]
set_property IOSTANDARD LVCMOS33 [get_ports uart_tx]

# LEDs
set_property PACKAGE_PIN U16 [get_ports led_status]
set_property IOSTANDARD LVCMOS33 [get_ports led_status]
set_property PACKAGE_PIN E19 [get_ports led_error]
set_property IOSTANDARD LVCMOS33 [get_ports led_error]