/* ═══════════════════════════════════════════════════════════════════════
 * File: BioCalibrator_TypeA.v (Revised)
 * 26-0203-1500 JST
 * ═══════════════════════════════════════════════════════════════════════ */

module BioCalibrator_TypeA_Jamming (
    input wire clk, rst_n,
    input wire i_in_valid,            // 入力データ有効フラグ
    input wire [15:0] i_cell_stiffness, i_cell_viscosity,
    input wire [15:0] i_cell_diameter, i_pore_size,
    input wire [15:0] i_flow_dp, i_drug_boost,
    input wire [15:0] i_deform_velocity,
    output reg o_is_jammed,
    output reg [7:0] o_error_code,
    output reg o_out_valid            // 演算完了フラグ (3サイクル後)
);

    // Pipeline Registers
    reg [1:0]  v_pipe; 
    reg [15:0] r_delta_x_s1;
    reg [15:0] r_flow_dp_s1, r_flow_dp_s2; // 遅延調整用
    reg        r_geom_err_s1, r_geom_err_s2;
    reg [31:0] r_elastic_s2, r_viscous_s2;

    // Stage 1: Geometry & Sync
    always @(posedge clk) begin
        v_pipe[0]    <= i_in_valid;
        r_flow_dp_s1 <= i_flow_dp;
        if (i_cell_diameter < i_pore_size) begin
            r_delta_x_s1  <= 0;
            r_geom_err_s1 <= 1; [cite: 100]
        end else begin
            r_delta_x_s1  <= i_cell_diameter - i_pore_size; [cite: 100]
            r_geom_err_s1 <= 0; [cite: 101]
        end
    end

    // Stage 2: Multipliers (Q16.16)
    always @(posedge clk) begin
        v_pipe[1]     <= v_pipe[0];
        r_flow_dp_s2  <= r_flow_dp_s1;
        r_geom_err_s2 <= r_geom_err_s1;
        // (Q8.8 + Q8.8) * Q8.8 = Q16.16
        r_elastic_s2 <= (i_cell_stiffness + i_drug_boost) * r_delta_x_s1; [cite: 103]
        r_viscous_s2 <= i_cell_viscosity * i_deform_velocity; [cite: 104]
    end

    // Stage 3: Comparison
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            o_is_jammed <= 0; o_error_code <= 0; o_out_valid <= 0;
        end else begin
            o_out_valid <= v_pipe[1];
            if (r_geom_err_s2) begin
                o_error_code <= 8'h01; o_is_jammed <= 0;
            end else begin
                o_error_code <= 0;
                // Compare Q16.16 vs Q16.16 (FlowDP * 256)
                if ((r_elastic_s2 + r_viscous_s2) > ({16'b0, r_flow_dp_s2} << 8)) [cite: 105]
                    o_is_jammed <= 1;
                else
                    o_is_jammed <= 0;
            end
        end
    end
endmodule