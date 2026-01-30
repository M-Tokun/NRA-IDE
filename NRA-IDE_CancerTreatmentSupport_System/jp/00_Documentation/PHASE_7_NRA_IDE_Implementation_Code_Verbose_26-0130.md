# NRA-IDE_Implementation_Code_Verbose
# Phase 7: 実装コード（冗長コメント版）
# 対象読者: エンジニア + コードを読みたい医師
# 作成日時: 2026-01-30 23:00

// ═══════════════════════════════════════════
// 0. この章の方針
// ═══════════════════════════════════════════
PURPOSE: {
    GUIDELINE: "コメント比率 > 50%（理解優先）";
    STYLE: "各行に物理的意味を記載";
    TARGET: "コーディング初心者でも読める";
    
    FILE_STRUCTURE: {
        SECTION_1: "Verilog FPGA Core（Type A）";
        SECTION_2: "Verilog FPGA Core（Type B）";
        SECTION_3: "Verilog Testbench（総当たり検証）";
        SECTION_4: "Python Host Interface";
        SECTION_5: "Python Report Generator";
    };
}

// ═══════════════════════════════════════════
// 1. Verilog FPGA Core（Type A - Jamming）
// ═══════════════════════════════════════════
VERILOG_CODE_TYPE_A: {
    
    FILE_NAME: "BioCalibrator_TypeA_Jamming_Verbose_26-0130.v";
    
    CONTENT: "
/* ═══════════════════════════════════════════════════════════════════════
 * Module: BioCalibrator_TypeA_Jamming
 * Date: 2026-01-30 23:00
 * Author: M-Tokuni & KEN
 * 
 * 目的: Type A（乳がん）の物理的封鎖判定
 * 物理式: F_resist = k·Δx + η·(dv/dt)
 * 判定: IF (F_resist > F_push) THEN SAFE ELSE DANGER
 * 
 * 重要原則:
 * - 水分粘性η を絶対に省略しない
 * - 距離ではなく制約（接触）から計算
 * - Fail-Closed: 不確かさは DANGER側へ
 * ═══════════════════════════════════════════════════════════════════════ */

`timescale 1ns / 1ps

module BioCalibrator_TypeA_Jamming (
    // ────────────────────────────────────
    // クロック・リセット
    // ────────────────────────────────────
    input wire clk,          // システムクロック（例: 100MHz）
    input wire rst_n,        // リセット（負論理、0でリセット）
    
    // ────────────────────────────────────
    // 入力: 患者パラメータ（全てQ8.8固定小数点）
    // ────────────────────────────────────
    input wire [15:0] i_cell_stiffness,  // 細胞硬度 [kPa]
    input wire [15:0] i_cell_viscosity,  // 水分粘性 [Pa·s]（絶対に0禁止）
    input wire [15:0] i_cell_diameter,   // 細胞直径 [μm]
    input wire [15:0] i_pore_size,       // 血管隙間 [μm]
    input wire [15:0] i_flow_dp,         // 血流圧力 [kPa]
    input wire [15:0] i_drug_boost,      // 薬剤ブースト [kPa]（制御変数）
    input wire [15:0] i_deform_velocity, // 変形速度 [μm/s²]
    
    // ────────────────────────────────────
    // 出力: 判定結果
    // ────────────────────────────────────
    output reg o_is_jammed,       // 1=SAFE（封鎖成立）, 0=DANGER（通過リスク）
    output reg [7:0] o_error_code // エラーコード（Phase 4辞書参照）
);

// ═══════════════════════════════════════════
// 定数定義
// ═══════════════════════════════════════════
localparam ALPHA = 250;  // スケール係数（実験的に決定）

// エラーコード（Phase 4辞書と一致）
localparam ERR_NONE = 8'h00;           // エラーなし
localparam ERR_GEOMETRIC = 8'h01;      // 幾何学的すり抜けリスク
localparam ERR_NEGATIVE_STIFF = 8'h02; // 細胞硬度が負
localparam ERR_ZERO_VISCOSITY = 8'h03; // 水分粘性ゼロ（禁止）
localparam ERR_OVERFLOW = 8'h04;       // 演算オーバーフロー

// ═══════════════════════════════════════════
// Stage 1: 変形量計算
// 目的: 細胞が血管隙間で潰される量を計算
// 物理: Δx = MAX(0, D_cell - d_gap)
// ═══════════════════════════════════════════
reg [15:0] r_deformation;      // 変形量 [μm]（Q8.8）
reg r_bypass_flag;             // 幾何学的すり抜けフラグ

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // リセット時: 全て0に初期化
        r_deformation <= 16'h0000;
        r_bypass_flag <= 1'b0;
    end else begin
        // ─── 幾何学的チェック ───
        // 細胞が隙間より小さい → すり抜ける → 封鎖不可能
        if (i_cell_diameter <= i_pore_size) begin
            r_deformation <= 16'h0000;  // 変形なし
            r_bypass_flag <= 1'b1;      // すり抜けリスク検出
        end else begin
            // 細胞が隙間より大きい → 潰れる
            r_deformation <= i_cell_diameter - i_pore_size;
            r_bypass_flag <= 1'b0;
        end
    end
end

// ═══════════════════════════════════════════
// Stage 2: 弾性力計算
// 目的: バネの力（フックの法則）を計算
// 物理: F_elastic = (k_cell + Boost) × Δx
// ═══════════════════════════════════════════
reg [15:0] r_total_stiffness;  // 総合硬度 [kPa]（Q8.8）
reg [31:0] r_elastic_raw;      // 弾性力（乗算後、未シフト）

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        r_total_stiffness <= 16'h0000;
        r_elastic_raw <= 32'h00000000;
    end else begin
        // ─── 総合硬度 = 細胞固有 + 薬剤ブースト ───
        r_total_stiffness <= i_cell_stiffness + i_drug_boost;
        
        // ─── 弾性力 = k × Δx ───
        // Q8.8 × Q8.8 = Q16.16 （32ビット結果）
        r_elastic_raw <= r_total_stiffness * r_deformation;
    end
end

// ═══════════════════════════════════════════
// Stage 3: 粘性抵抗計算
// 目的: 水分の抵抗（時間依存性）を計算
// 物理: F_viscous = η × (dv/dt)
// 重要: この項を省略することは永久に禁止
// ═══════════════════════════════════════════
reg [31:0] r_viscous_raw;      // 粘性力（乗算後、未シフト）
reg r_zero_viscosity_flag;     // η=0 検出フラグ

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        r_viscous_raw <= 32'h00000000;
        r_zero_viscosity_flag <= 1'b0;
    end else begin
        // ─── 水分粘性のゼロチェック（禁止） ───
        if (i_cell_viscosity == 16'h0000) begin
            r_viscous_raw <= 32'h00000000;
            r_zero_viscosity_flag <= 1'b1; // エラー検出
        end else begin
            // ─── 粘性力 = η × (dv/dt) ───
            // Q8.8 × Q8.8 = Q16.16
            r_viscous_raw <= i_cell_viscosity * i_deform_velocity;
            r_zero_viscosity_flag <= 1'b0;
        end
    end
end

// ═══════════════════════════════════════════
// Stage 4: 総合抵抗力算出
// 目的: 弾性 + 粘性 をスケーリングして圧力次元へ
// 物理: F_resist = (F_elastic + F_viscous) × α
// ═══════════════════════════════════════════
reg [15:0] r_elastic_scaled;   // 弾性力（右シフト後、Q8.8）
reg [15:0] r_viscous_scaled;   // 粘性力（右シフト後、Q8.8）
reg [31:0] r_resist_force_raw; // 総抵抗力（スケール前）
reg [15:0] r_resist_force;     // 総抵抗力 [Pa]（Q8.8）
reg r_overflow_flag;           // オーバーフロー検出

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        r_elastic_scaled <= 16'h0000;
        r_viscous_scaled <= 16'h0000;
        r_resist_force_raw <= 32'h00000000;
        r_resist_force <= 16'h0000;
        r_overflow_flag <= 1'b0;
    end else begin
        // ─── 右シフト（8ビット）: Q16.16 → Q8.8 ───
        // [31:24][23:8][7:0] → [23:8] を取得
        r_elastic_scaled <= r_elastic_raw[23:8];
        r_viscous_scaled <= r_viscous_raw[23:8];
        
        // ─── オーバーフローチェック ───
        // 上位8ビット [31:24] が非ゼロ → オーバーフロー
        if (|r_elastic_raw[31:24] || |r_viscous_raw[31:24]) begin
            r_overflow_flag <= 1'b1;
            r_resist_force <= 16'h0000; // エラー時は0
        end else begin
            r_overflow_flag <= 1'b0;
            
            // ─── 総抵抗力 = (弾性 + 粘性) × α ───
            r_resist_force_raw <= (r_elastic_scaled + r_viscous_scaled) * ALPHA;
            r_resist_force <= r_resist_force_raw[23:8]; // 再度右シフト
        end
    end
end

// ═══════════════════════════════════════════
// Stage 5: 最終判定
// 目的: 抵抗力 vs 血流圧力 を比較
// 原則: Fail-Closed（不確かさは DANGER側）
// ═══════════════════════════════════════════
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        o_is_jammed <= 1'b0;   // リセット時は DANGER
        o_error_code <= ERR_NONE;
    end else begin
        // ─── エラー判定（優先順位順） ───
        
        // 1. 幾何学的すり抜け
        if (r_bypass_flag) begin
            o_is_jammed <= 1'b0;
            o_error_code <= ERR_GEOMETRIC;
        
        // 2. 水分粘性ゼロ（禁止）
        end else if (r_zero_viscosity_flag) begin
            o_is_jammed <= 1'b0;
            o_error_code <= ERR_ZERO_VISCOSITY;
        
        // 3. 演算オーバーフロー
        end else if (r_overflow_flag) begin
            o_is_jammed <= 1'b0;
            o_error_code <= ERR_OVERFLOW;
        
        // 4. 正常判定
        end else begin
            o_error_code <= ERR_NONE;
            
            // ─── 比較: 抵抗圧力 > 血流圧力 ? ───
            if (r_resist_force > i_flow_dp) begin
                o_is_jammed <= 1'b1;  // SAFE（封鎖成立）
            end else begin
                o_is_jammed <= 1'b0;  // DANGER（通過リスクあり）
            end
        end
    end
end

endmodule

/* ═══════════════════════════════════════════════════════════════════════
 * 使用例:
 * 
 * BioCalibrator_TypeA_Jamming calibrator (
 *     .clk(sys_clk),
 *     .rst_n(sys_rst_n),
 *     .i_cell_stiffness(16'h0180),  // 1.5 kPa
 *     .i_cell_viscosity(16'h000D),  // 0.05 Pa·s
 *     .i_cell_diameter(16'h0C00),   // 12.0 μm
 *     .i_pore_size(16'h0800),       // 8.0 μm
 *     .i_flow_dp(16'h0258),         // 600 Pa
 *     .i_drug_boost(16'h0B4D),      // 2.852 kPa（総当たり結果）
 *     .i_deform_velocity(16'h3200), // 200 μm/s²
 *     .o_is_jammed(status),
 *     .o_error_code(error)
 * );
 * 
 * if (status == 1'b1) begin
 *     $display(\"SAFE: 細胞は物理的に封鎖されました\");
 * end else begin
 *     $display(\"DANGER: 通過リスクあり。エラーコード = %02X\", error);
 * end
 * ═══════════════════════════════════════════════════════════════════════ */
";
}

// ═══════════════════════════════════════════
// 2. Python Host Interface（シリアル通信）
// ═══════════════════════════════════════════
PYTHON_CODE_INTERFACE: {
    
    FILE_NAME: "fpga_interface_verbose_26-0130.py";
    
    CONTENT: "
# ═══════════════════════════════════════════════════════════════════════
# File: fpga_interface_verbose_26-0130.py
# Date: 2026-01-30 23:10
# Author: M-Tokuni & KEN
# 
# 目的: ホストPC ↔ FPGA Bio-Calibrator 間の通信
# プロトコル: UART シリアル通信（115200 bps）
# 形式: ASCII（人間が読める形式、デバッグ容易）
# ═══════════════════════════════════════════════════════════════════════

import serial
import struct
from typing import Dict, Optional

class FPGAInterface:
    \"\"\"
    FPGA Bio-Calibratorとの通信インターフェース
    
    通信プロトコル（例）:
    Host → FPGA: \"STIFF:0x0180,DIAM:0x0C00,PORE:0x0800,PRESS:0x0258,BOOST:0x0000\\n\"
    FPGA → Host: \"JAMMED:1,ERROR:0x00\\n\"
    \"\"\"
    
    def __init__(self, port: str = \"/dev/ttyUSB0\", baudrate: int = 115200):
        \"\"\"
        コンストラクタ
        
        Args:
            port: シリアルポート（Linux: /dev/ttyUSB0, Windows: COM3）
            baudrate: 通信速度（115200 bps推奨）
        \"\"\"
        try:
            # シリアルポート開く
            self.serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=2.0,  # 2秒タイムアウト
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            print(f\"✓ FPGA接続成功: {port} @ {baudrate} bps\")
        except serial.SerialException as e:
            print(f\"✗ FPGA接続失敗: {e}\")
            self.serial = None
    
    def q8_8_encode(self, value: float) -> int:
        \"\"\"
        実数 → Q8.8固定小数点へ変換
        
        Args:
            value: 実数値（例: 2.5）
        
        Returns:
            Q8.8整数値（例: 640 = 0x0280）
        
        Examples:
            >>> q8_8_encode(2.5)
            640  # = 2.5 × 256
            >>> q8_8_encode(0.1)
            26   # ≈ 0.1 × 256 = 25.6 → 26（四捨五入）
        \"\"\"
        # 範囲チェック
        if value < 0 or value > 255.99:
            raise ValueError(f\"Q8.8範囲外: {value}（0〜255.99のみ）\")
        
        # 256倍して整数化
        q8_8 = int(round(value * 256))
        return q8_8
    
    def q8_8_decode(self, q8_8: int) -> float:
        \"\"\"
        Q8.8固定小数点 → 実数へ変換
        
        Args:
            q8_8: Q8.8整数値（例: 640）
        
        Returns:
            実数値（例: 2.5）
        \"\"\"
        return q8_8 / 256.0
    
    def send_query(self, patient_data: Dict[str, float]) -> Optional[Dict]:
        \"\"\"
        患者データをFPGAに送信し、判定結果を受信
        
        Args:
            patient_data: 患者パラメータ辞書
                {
                    'cell_stiffness': 1.5,  # kPa
                    'cell_viscosity': 0.05, # Pa·s
                    'cell_diameter': 12.0,  # μm
                    'pore_size': 8.0,       # μm
                    'flow_dp': 0.6,         # kPa
                    'drug_boost': 2.852     # kPa（制御変数）
                }
        
        Returns:
            判定結果辞書 or None（通信失敗時）
                {
                    'is_jammed': True,      # SAFE/DANGER
                    'error_code': 0x00      # エラーコード
                }
        \"\"\"
        if self.serial is None:
            print(\"[ERROR] FPGA未接続\")
            return None
        
        # ─── Phase 4 辞書で範囲チェック ───
        # （省略: 実際は Phase 4 のRANGE_VALIDと照合）
        
        # ─── Q8.8エンコード ───
        stiff_q8 = self.q8_8_encode(patient_data['cell_stiffness'])
        visc_q8 = self.q8_8_encode(patient_data['cell_viscosity'])
        diam_q8 = self.q8_8_encode(patient_data['cell_diameter'])
        pore_q8 = self.q8_8_encode(patient_data['pore_size'])
        press_q8 = self.q8_8_encode(patient_data['flow_dp'])
        boost_q8 = self.q8_8_encode(patient_data['drug_boost'])
        
        # ─── コマンドパケット作成 ───
        # 形式: \"KEY:0xVALUE,KEY:0xVALUE,...\\n\"
        cmd = (
            f\"STIFF:0x{stiff_q8:04X},\"
            f\"VISC:0x{visc_q8:04X},\"
            f\"DIAM:0x{diam_q8:04X},\"
            f\"PORE:0x{pore_q8:04X},\"
            f\"PRESS:0x{press_q8:04X},\"
            f\"BOOST:0x{boost_q8:04X}\\n\"
        )
        
        # ─── 送信 ───
        self.serial.write(cmd.encode('utf-8'))
        print(f\"[SEND] {cmd.strip()}\")
        
        # ─── 受信 ───
        try:
            response = self.serial.readline().decode('utf-8').strip()
            print(f\"[RECV] {response}\")
        except UnicodeDecodeError:
            print(\"[ERROR] 受信データが不正\")
            return None
        
        # ─── パース ───
        # 形式: \"JAMMED:1,ERROR:0x00\"
        result = {}
        for item in response.split(','):
            key, value = item.split(':')
            if key == 'JAMMED':
                result['is_jammed'] = (int(value) == 1)
            elif key == 'ERROR':
                result['error_code'] = int(value, 16)
        
        return result
    
    def brute_force_optimize(self, patient_data: Dict[str, float]) -> float:
        \"\"\"
        総当たり探索で最適薬液量を特定
        
        Args:
            patient_data: 患者パラメータ（drug_boost以外）
        
        Returns:
            最適Boost値 [kPa]
        
        Strategy:
            Boost = 0 から開始
            0.01 kPa ずつ増やしながら判定
            SAFE になったら終了
        \"\"\"
        boost = 0.0
        step = 0.01  # kPa
        max_boost = 10.0  # kPa
        
        print(\"\\n[総当たり探索開始]\")
        
        while boost <= max_boost:
            # 現在のBoost値で判定
            patient_data['drug_boost'] = boost
            result = self.send_query(patient_data)
            
            if result is None:
                print(\"[ERROR] 通信失敗\")
                return None
            
            # SAFE 判定が出たら終了
            if result['is_jammed']:
                print(f\"\\n✓ 最適Boost発見: +{boost:.3f} kPa\")
                return boost
            
            # 次のステップへ
            boost += step
            if boost % 1.0 < step:  # 1 kPa ごとに進捗表示
                print(f\"  探索中: {boost:.2f} kPa ...\")
        
        # 見つからなかった
        print(\"\\n✗ 最適Boostが見つかりません（10 kPa 超）\")
        return None
    
    def close(self):
        \"\"\"シリアルポートを閉じる\"\"\"
        if self.serial:
            self.serial.close()
            print(\"✓ FPGA接続を閉じました\")


# ═══════════════════════════════════════════
# 使用例
# ═══════════════════════════════════════════
if __name__ == \"__main__\":
    # FPGA接続
    fpga = FPGAInterface(port=\"/dev/ttyUSB0\")
    
    # 患者データ（例）
    patient = {
        'cell_stiffness': 1.5,   # kPa（測定値）
        'cell_viscosity': 0.05,  # Pa·s（測定値）
        'cell_diameter': 12.0,   # μm（測定値）
        'pore_size': 8.0,        # μm（固定値）
        'flow_dp': 0.6,          # kPa（測定値）
        'drug_boost': 0.0        # 初期値
    }
    
    # 総当たりで最適Boost探索
    optimal_boost = fpga.brute_force_optimize(patient)
    
    if optimal_boost is not None:
        print(f\"\\n【結果】推奨薬液量: +{optimal_boost:.3f} kPa\")
    
    # 接続終了
    fpga.close()
";
}

// ═══════════════════════════════════════════
// 3. 次の章への接続
// ═══════════════════════════════════════════
NEXT_PHASE: {
    NOTE: "Phase 7 は実装コードのため、ここまで";
    
    NEXT_TOPIC: "PHASE_8: 技術現場向け説明書";
    NEXT_CONTENT: [
        "エンジニア向け: FPGA合成手順、デバッグ方法",
        "医師向け: パラメータの読み方、警告の意味",
        "FAQ: よくある質問と回答"
    ];
}
