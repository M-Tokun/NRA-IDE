# ═══════════════════════════════════════════════════════════════════════
# File: wave_config.do
# Phase: 10
# 目的: ModelSimでの波形表示設定
# ═══════════════════════════════════════════════════════════════════════

onerror {resume}
quietly WaveActivateNextPane {} 0

add wave -noupdate -divider "Clock & Reset"
add wave -noupdate /Testbench_BruteForce/clk
add wave -noupdate /Testbench_BruteForce/rst_n

add wave -noupdate -divider "Inputs (Q8.8)"
add wave -noupdate -radix hexadecimal /Testbench_BruteForce/stiff
add wave -noupdate -radix hexadecimal /Testbench_BruteForce/boost
add wave -noupdate -radix hexadecimal /Testbench_BruteForce/visc

add wave -noupdate -divider "Outputs"
add wave -noupdate -color {Green} /Testbench_BruteForce/jammed
add wave -noupdate -color {Red}   /Testbench_BruteForce/err

TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {0 ns} 0}
configure wave -namecolwidth 200
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 1
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2