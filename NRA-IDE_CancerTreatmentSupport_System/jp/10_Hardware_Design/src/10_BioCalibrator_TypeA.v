/* 10_BioCalibrator_TypeA.v (Revised) 26-0203-1600 */
module BioCalibrator_TypeA_Jamming (
    input wire clk, rst_n, i_in_valid,
    input wire [15:0] i_cell_stiffness, i_cell_viscosity,
    input wire [15:0] i_cell_diameter, i_pore_size,
    input wire [15:0] i_flow_dp, i_drug_boost,
    input wire [15:0] i_deform_velocity,
    output reg o_is_jammed, output reg [7:0] o_error_code, output reg o_out_valid
);
    reg [1:0]  v_pipe; 
    reg [15:0] r_delta_x_s1, r_flow_dp_s1, r_flow_dp_s2;
    reg        r_geom_err_s1, r_geom_err_s2;
    reg [31:0] r_elastic_s2, r_viscous_s2;

    always @(posedge clk) begin
        v_pipe[0] <= i_in_valid; r_flow_dp_s1 <= i_flow_dp;
        if (i_cell_diameter < i_pore_size) begin r_delta_x_s1 <= 0; r_geom_err_s1 <= 1; end
        else begin r_delta_x_s1 <= i_cell_diameter - i_pore_size; r_geom_err_s1 <= 0; end
    end
    always @(posedge clk) begin
        v_pipe[1] <= v_pipe[0]; r_flow_dp_s2 <= r_flow_dp_s1; r_geom_err_s2 <= r_geom_err_s1;
        r_elastic_s2 <= (i_cell_stiffness + i_drug_boost) * r_delta_x_s1;
        r_viscous_s2 <= i_cell_viscosity * i_deform_velocity;
    end
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin o_is_jammed <= 0; o_error_code <= 0; o_out_valid <= 0; end
        else begin
            o_out_valid <= v_pipe[1];
            if (r_geom_err_s2) begin o_error_code <= 8'h01; o_is_jammed <= 0; end
            else begin
                o_error_code <= 0;
                if ((r_elastic_s2 + r_viscous_s2) > ({16'b0, r_flow_dp_s2} << 8)) o_is_jammed <= 1;
                else o_is_jammed <= 0;
            end
        end
    end
endmodule