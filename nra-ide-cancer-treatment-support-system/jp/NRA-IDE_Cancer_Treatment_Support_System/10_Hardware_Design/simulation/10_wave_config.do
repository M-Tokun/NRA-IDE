# ═══════════════════════════════════════════════════════════════════════
# File: wave_config.do
# Phase: 10 (Synchronous Update)
# Rev:  2.0 (2026-07-29) 5段パイプラインの実信号名へ更新
# 目的: パイプライン同期（Valid/Ready）の可視化
# ═══════════════════════════════════════════════════════════════════════

onerror {resume}
quietly WaveActivateNextPane {} 0

add wave -noupdate -divider "System"
add wave -noupdate /Testbench_BruteForce/clk
add wave -noupdate /Testbench_BruteForce/rst_n

add wave -noupdate -divider "Sync Control"
add wave -noupdate -color {Cyan} /Testbench_BruteForce/i_in_valid
add wave -noupdate -color {Orange} /Testbench_BruteForce/o_out_valid

add wave -noupdate -divider "Input Parameters"
add wave -noupdate -radix hexadecimal /Testbench_BruteForce/stiff
add wave -noupdate -radix hexadecimal /Testbench_BruteForce/boost
add wave -noupdate -radix hexadecimal /Testbench_BruteForce/visc

add wave -noupdate -divider "Stage 4: Stress Terms (Q8.8)"
add wave -noupdate -radix decimal /Testbench_BruteForce/dut/sig_el4
add wave -noupdate -radix decimal /Testbench_BruteForce/dut/sig_v4

add wave -noupdate -divider "Final Decision"
add wave -noupdate -color {Green} /Testbench_BruteForce/jammed
add wave -noupdate -color {Red}   /Testbench_BruteForce/err

TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {0 ns} 0}
configure wave -namecolwidth 250
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 1
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2