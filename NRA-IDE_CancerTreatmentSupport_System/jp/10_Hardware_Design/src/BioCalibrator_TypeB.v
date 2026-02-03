/* 10_BioCalibrator_TypeB.v (Non-Linear SCRUM Version) 26-0203-1714 */

module BioCalibrator_TypeB_Collective (
    // ... (ポート定義は前回同様)
);
    // スクラム効果係数 (1 + alpha * sqrt(N)) Q8.8形式
    // alpha = 0.5 と仮定した LUT (N=1..8)
    reg [15:0] r_scrum_lut;
    always @(*) begin
        case (i_cell_count)
            8'd1:    r_scrum_lut = 16'h0100; // 1.00
            8'd2:    r_scrum_lut = 16'h016A; // 1.00 + 0.5*1.41 = 1.70
            8'd3:    r_scrum_lut = 16'h01BB; // 1.00 + 0.5*1.73 = 1.86
            8'd4:    r_scrum_lut = 16'h0200; // 1.00 + 0.5*2.00 = 2.00
            default: r_scrum_lut = 16'h0280; // N>4 は 2.50 で飽和
        endcase
    end

    // Stage 3: 非線形スケーリング演算 (40bit)
    always @(posedge clk) begin
        // F_total = (F_single * N) * Scrum_Factor / 256
        r_f_total_s3 <= (r_f_single_s2 * r_n_s1 * r_scrum_lut) >> 8;
    end
    // ... (以下比較ロジック)
endmodule
