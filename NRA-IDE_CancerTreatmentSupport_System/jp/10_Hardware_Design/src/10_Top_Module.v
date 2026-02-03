// ... (前略)
    reg r_cancer_type; // 0:TypeA, 1:TypeB

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin 
            rx_cnt <= 0; r_cancer_type <= 0;
        end else begin
            if (rx_valid) begin
                if (rx_cnt == 0) begin
                    if (rx_data == 8'hA5) begin 
                        r_cancer_type <= 0; // Type A
                        rx_cnt <= 1;
                    end else if (rx_data == 8'hA6) begin
                        r_cancer_type <= 1; // Type B
                        rx_cnt <= 1;
                    end
                end
                // ... (チェックサム・バッファ処理)
            end
        end
    end

    // Selectorへの接続
    Cancer_Treatment_Selector core (
        // ... (他のポート)
        .i_cancer_type(r_cancer_type),
        // ...
    );