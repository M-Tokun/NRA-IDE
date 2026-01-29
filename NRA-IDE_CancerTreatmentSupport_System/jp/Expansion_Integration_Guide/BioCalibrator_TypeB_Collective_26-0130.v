/* Module: BioCalibrator_TypeB_Collective (2026-01-30 20:50)
 * Description: 子宮頸癌など「集団で押す」タイプの転移メカニズムに対応
 * Physics Model:
 *   F_collective = N × F_individual × (1 + α × √N)
 *   ※ α: Cooperative Enhancement Factor (集団協調係数)
 *
 * Architecture Comparison:
 *
 *   Type A (Softness Bypass)     Type B (Collective Push)
 *   ┌───────────┐                ┌───────────────────┐
 *   │ Single    │                │ Cell Cluster      │
 *   │ Soft Cell │──→ Gap         │ ●●●               │
 *   │     ●     │                │ ●●●  ──→ Gap      │
 *   └───────────┘                │ ●●●               │
 *   Strategy: Harden              └───────────────────┘
 *   (Increase k)                 Strategy: Jam Entire Front
 *                                (Increase Total Resistance)
 */

`timescale 1ns / 1ps

module BioCalibrator_TypeB_Collective (
    // ============================================
    // Input Parameters
    // ============================================
    input wire [15:0] i_cell_stiffness,    // Individual cell stiffness (Q8.8)
    input wire [15:0] i_cell_diameter,     // Individual cell size (Q8.8)
    input wire [15:0] i_pore_size,         // Gap size (Q8.8)
    input wire [15:0] i_blood_pressure,    // Flow pressure (Pa)
    input wire [15:0] i_drug_boost,        // Drug-induced stiffness boost (Q8.8)
    input wire [7:0]  i_cell_count,        // Number of cells in cluster (1~255)
    input wire [7:0]  i_cooperation_alpha, // α × 16 (Q4.4 fixed point)

    // ============================================
    // Output
    // ============================================
    output wire o_is_jammed                // 1=Blocked, 0=Penetrates
);

    // ============================================
    // Stage 1: Individual Cell Physics
    // ============================================
    wire [15:0] w_total_stiffness;
    wire [15:0] w_deformation;
    wire [31:0] w_single_force_calc;
    wire [15:0] w_single_force;

    assign w_total_stiffness = i_cell_stiffness + i_drug_boost;
    assign w_deformation = (i_cell_diameter > i_pore_size) 
                           ? (i_cell_diameter - i_pore_size) : 16'd0;
    assign w_single_force_calc = w_total_stiffness * w_deformation;
    assign w_single_force = w_single_force_calc[23:8]; // Scale to Q8.8

    // ============================================
    // Stage 2: Cooperative Enhancement
    // ============================================
    // F_coop = F_single × (1 + α × √N)
    //
    // ASCII Visualization:
    //   Individual:  ●  → Force = F
    //   Pair:        ●● → Force = 2F × (1 + α×√2) ≈ 2.6F
    //   Cluster(9):  ●●● 
    //                ●●● → Force = 9F × (1 + α×3) ≈ 13.5F
    //                ●●●

    wire [7:0] w_sqrt_N;           // √N approximation
    wire [15:0] w_coop_factor;     // (1 + α × √N) in Q8.8
    wire [31:0] w_enhanced_force;
    
    // √N Lookup Table (Hardware-friendly approximation)
    assign w_sqrt_N = (i_cell_count <= 8'd4)  ? 8'd2 :
                      (i_cell_count <= 8'd9)  ? 8'd3 :
                      (i_cell_count <= 8'd16) ? 8'd4 :
                      (i_cell_count <= 8'd25) ? 8'd5 :
                      (i_cell_count <= 8'd36) ? 8'd6 :
                      (i_cell_count <= 8'd49) ? 8'd7 : 8'd8;

    // Cooperation Factor = 256 + (alpha × sqrt_N × 16)
    // Example: α=0.5(Q4.4=8), N=9 → 256 + (8×3×16) = 640 (=2.5 in Q8.8)
    assign w_coop_factor = 16'd256 + (i_cooperation_alpha * w_sqrt_N * 16);

    // Enhanced Force = Single × Count × Coop_Factor
    assign w_enhanced_force = (w_single_force * i_cell_count * w_coop_factor) >> 8;

    // ============================================
    // Stage 3: Final Judgment
    // ============================================
    wire [15:0] w_collective_resistance;
    assign w_collective_resistance = w_enhanced_force[15:0];
    assign o_is_jammed = (w_collective_resistance > i_blood_pressure) ? 1'b1 : 1'b0;

    // ============================================
    // Debug Monitoring (Simulation Only)
    // ============================================
    `ifdef SIMULATION
        always @(*) begin
            if (w_deformation > 0) begin
                $display("[TypeB] Count=%d, Single=%d, Coop=%.2f, Total=%d, Jammed=%b",
                         i_cell_count, 
                         w_single_force,
                         w_coop_factor / 256.0,
                         w_collective_resistance,
                         o_is_jammed);
            end
        end
    `endif

endmodule

/*
 * ============================================
 * Testbench for Type B Module
 * ============================================
 */
module Testbench_TypeB;
    reg [15:0] t_stiffness, t_diameter, t_pore, t_pressure, t_boost;
    reg [7:0]  t_count, t_alpha;
    wire t_jammed;

    BioCalibrator_TypeB_Collective DUT (
        .i_cell_stiffness(t_stiffness),
        .i_cell_diameter(t_diameter),
        .i_pore_size(t_pore),
        .i_blood_pressure(t_pressure),
        .i_drug_boost(t_boost),
        .i_cell_count(t_count),
        .i_cooperation_alpha(t_alpha),
        .o_is_jammed(t_jammed)
    );

    initial begin
        $display("========================================");
        $display(" Type B (Collective Push) Test");
        $display("========================================");

        // Fixed geometry
        t_stiffness = 16'h0080; // 0.5 kPa (soft cervical cancer)
        t_diameter  = 16'h0A00; // 10.0 μm
        t_pore      = 16'h0800; // 8.0 μm
        t_pressure  = 16'h0258; // 600 Pa
        t_alpha     = 8'd8;     // α = 0.5

        // Test: Increasing cluster size
        $display("\n--- Cluster Size Effect (No Drug) ---");
        t_boost = 0;
        for (t_count = 1; t_count <= 20; t_count = t_count + 1) begin
            #10;
            $display("N=%2d → Jammed=%b", t_count, t_jammed);
        end

        // Test: Drug boost requirement
        $display("\n--- Drug Boost Search (N=10) ---");
        t_count = 10;
        t_boost = 0;
        while (t_boost < 16'h1000) begin
            #10;
            if (t_jammed == 1'b1) begin
                $display(">> Required Boost: +%.3f kPa", t_boost / 256.0);
                break;
            end
            t_boost = t_boost + 16; // Step 0.06 kPa
        end

        $display("========================================");
        $finish;
    end
endmodule

/*
 * ASCII Art: Collective Force Visualization
 *
 *   Single Cell (N=1):
 *   ●─────→ F
 *
 *   Small Cluster (N=4):
 *   ●●
 *   ●●─────→ 4F × 1.4 ≈ 5.6F
 *
 *   Large Cluster (N=9):
 *   ●●●
 *   ●●●─────→ 9F × 2.5 ≈ 22.5F
 *   ●●●
 *
 *   The gap can withstand individual cells
 *   but collapses under collective pressure!
 */
