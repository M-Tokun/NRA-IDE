/* Module: Testbench_Parametric_Sweep (2026-01-30 20:45)
 * Description: N×M×K 全パラメータ空間を総当たりし、最悪ケースの適合値を抽出
 * Architecture:
 *   ┌─────────────────────────────────────────┐
 *   │  Parameter Space Explorer (3D Sweep)   │
 *   │  ┌───────┐  ┌───────┐  ┌───────┐      │
 *   │  │Stiff  │→ │Diam   │→ │Press  │→DUT  │
 *   │  │0.1~2.0│  │8~25μm │  │100~1k │      │
 *   │  └───────┘  └───────┘  └───────┘      │
 *   └─────────────────────────────────────────┘
 *                  ↓
 *         ┌────────────────┐
 *         │ Statistics     │
 *         │ - Max Boost    │
 *         │ - Min Boost    │
 *         │ - Coverage %   │
 *         └────────────────┘
 */

`timescale 1ns / 1ps

module Testbench_Parametric_Sweep;
    // ============================================
    // 1. DUT Interface
    // ============================================
    reg [15:0] t_cell_stiffness;
    reg [15:0] t_cell_diameter;
    reg [15:0] t_pore_size;
    reg [15:0] t_blood_pressure;
    reg [15:0] t_drug_boost;
    wire t_is_jammed;

    BioCalibrator_Core_Logic DUT (
        .i_cell_stiffness(t_cell_stiffness),
        .i_cell_diameter(t_cell_diameter),
        .i_pore_size(t_pore_size),
        .i_blood_pressure(t_blood_pressure),
        .i_drug_boost(t_drug_boost),
        .o_is_jammed(t_is_jammed)
    );

    // ============================================
    // 2. Parameter Space Definition (Q8.8 Format)
    // ============================================
    // Stiffness: 0.1~2.0 kPa (Step: 0.1 kPa)
    localparam STIFF_MIN  = 16'h001A; // 0.1 kPa
    localparam STIFF_MAX  = 16'h0200; // 2.0 kPa
    localparam STIFF_STEP = 16'h001A; // 0.1 kPa

    // Diameter: 8~25 μm (Step: 1 μm)
    localparam DIAM_MIN  = 16'h0800;  // 8.0 μm
    localparam DIAM_MAX  = 16'h1900;  // 25.0 μm
    localparam DIAM_STEP = 16'h0100;  // 1.0 μm

    // Blood Pressure: 100~1000 Pa (Step: 50 Pa)
    localparam PRESS_MIN  = 16'h0064; // 100 Pa
    localparam PRESS_MAX  = 16'h03E8; // 1000 Pa
    localparam PRESS_STEP = 16'h0032; // 50 Pa

    // Pore Size: Fixed at 8.0 μm (Typical Capillary)
    localparam PORE_FIXED = 16'h0800;

    // ============================================
    // 3. Result Storage
    // ============================================
    reg [15:0] result_boost [0:9999];  // Store optimal boost for each case
    reg [15:0] result_stiff [0:9999];
    reg [15:0] result_diam  [0:9999];
    reg [15:0] result_press [0:9999];
    integer result_count;
    integer failed_count;

    // Statistics
    reg [15:0] max_boost_required;
    reg [15:0] min_boost_required;
    integer total_cases;

    // ============================================
    // 4. Main Test Procedure
    // ============================================
    integer i_stiff, i_diam, i_press;
    integer boost_search;

    initial begin
        $display("========================================");
        $display(" NRA-IDE Parametric Sweep Test Start");
        $display(" Timestamp: 2026-01-30 20:45:00");
        $display("========================================");
        $display("");

        // Initialize
        result_count = 0;
        failed_count = 0;
        total_cases = 0;
        max_boost_required = 0;
        min_boost_required = 16'hFFFF;
        t_pore_size = PORE_FIXED;

        // ┌─────────────────────────────────┐
        // │  3D Parameter Space Sweep       │
        // │                                 │
        // │   for Stiffness:                │
        // │     for Diameter:               │
        // │       for Pressure:             │
        // │         → Find Min Boost        │
        // └─────────────────────────────────┘

        for (i_stiff = STIFF_MIN; i_stiff <= STIFF_MAX; i_stiff = i_stiff + STIFF_STEP) begin
            for (i_diam = DIAM_MIN; i_diam <= DIAM_MAX; i_diam = i_diam + DIAM_STEP) begin
                for (i_press = PRESS_MIN; i_press <= PRESS_MAX; i_press = i_press + PRESS_STEP) begin
                    
                    total_cases = total_cases + 1;
                    t_cell_stiffness = i_stiff;
                    t_cell_diameter  = i_diam;
                    t_blood_pressure = i_press;
                    t_drug_boost = 0;

                    // ─────────────────────────────
                    // Inner Loop: Boost Search
                    // ─────────────────────────────
                    boost_search = 0;
                    while (t_drug_boost < 16'h2800) begin // Max 10 kPa
                        #1; // Wait 1ns for combinational logic
                        
                        if (t_is_jammed == 1'b1) begin
                            // ✓ Found minimum boost for this condition
                            result_boost[result_count] = t_drug_boost;
                            result_stiff[result_count] = t_cell_stiffness;
                            result_diam[result_count]  = t_cell_diameter;
                            result_press[result_count] = t_blood_pressure;
                            
                            // Update statistics
                            if (t_drug_boost > max_boost_required) 
                                max_boost_required = t_drug_boost;
                            if (t_drug_boost < min_boost_required) 
                                min_boost_required = t_drug_boost;
                            
                            result_count = result_count + 1;
                            boost_search = 1; // Mark as found
                            break;
                        end
                        
                        t_drug_boost = t_drug_boost + 8; // Step: 0.03 kPa
                    end

                    if (boost_search == 0) begin
                        // ✗ No solution found (exceeds 10 kPa limit)
                        failed_count = failed_count + 1;
                        $display("[WARN] No solution: Stiff=%.2f, Diam=%.1f, Press=%d", 
                                 i_stiff/256.0, i_diam/256.0, i_press);
                    end

                end
            end
        end

        // ============================================
        // 5. Results Summary
        // ============================================
        $display("");
        $display("========================================");
        $display(" Sweep Complete - Results Summary");
        $display("========================================");
        $display("Total Cases Tested:    %d", total_cases);
        $display("Successful Calibrations: %d (%.1f%%)", 
                 result_count, 100.0 * result_count / total_cases);
        $display("Failed Cases:          %d", failed_count);
        $display("");
        $display("--- Boost Statistics ---");
        $display("Max Boost Required:    +%.3f kPa", max_boost_required / 256.0);
        $display("Min Boost Required:    +%.3f kPa", min_boost_required / 256.0);
        $display("");

        // ============================================
        // 6. Export to CSV
        // ============================================
        integer fd, idx;
        fd = $fopen("calibration_results_26-0130.csv", "w");
        $fwrite(fd, "Stiffness_kPa,Diameter_um,Pressure_Pa,DrugBoost_kPa\n");
        
        for (idx = 0; idx < result_count; idx = idx + 1) begin
            $fwrite(fd, "%.3f,%.1f,%d,%.3f\n",
                    result_stiff[idx] / 256.0,
                    result_diam[idx] / 256.0,
                    result_press[idx],
                    result_boost[idx] / 256.0);
        end
        $fclose(fd);
        $display(">> CSV Export: calibration_results_26-0130.csv");
        $display("");

        // ============================================
        // 7. Worst Case Extraction
        // ============================================
        $display("--- Worst Case Scenario ---");
        for (idx = 0; idx < result_count; idx = idx + 1) begin
            if (result_boost[idx] == max_boost_required) begin
                $display("Condition:");
                $display("  Cell Stiffness:  %.3f kPa", result_stiff[idx] / 256.0);
                $display("  Cell Diameter:   %.1f μm", result_diam[idx] / 256.0);
                $display("  Blood Pressure:  %d Pa", result_press[idx]);
                $display("  Required Boost:  +%.3f kPa", result_boost[idx] / 256.0);
                break;
            end
        end

        $display("========================================");
        $finish;
    end

endmodule

/*
 * ASCII Art: Parameter Space Visualization
 *
 *        Blood Pressure (Pa)
 *              ↑
 *           1000├─┐
 *                │ │ ← High Risk Zone
 *            600├─┼─┐
 *                │ │ │
 *            100├─┴─┴─→ Cell Stiffness (kPa)
 *               0.1  2.0
 *
 *   Each point in this 3D space gets a "minimum boost" value
 *   The testbench finds ALL these values through brute force
 */
