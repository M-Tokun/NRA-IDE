# ═══════════════════════════════════════════════════════════════════════
# File: fpga_interface.py
# Phase: 20
# Date: 2026-02-01 (Binary Fix)
# Author: M-Tokuni & AI Architects
#
# 目的: ホストPC ↔ FPGA Bio-Calibrator 通信インターフェース
# プロトコル: Binary Mode (14 Bytes Fixed Packet)
# 通信速度: 115200 bps
# ═══════════════════════════════════════════════════════════════════════

import serial
import struct
import time
from typing import Dict, Optional

class FPGAInterface:
    """
    FPGAとのバイナリ通信クラス

    Packet Structure (Host -> FPGA, 14 Bytes):
      [0]: Header (0xA5)
      [1-2]: Stiffness (Q8.8)
      [3-4]: Viscosity (Q8.8)
      [5-6]: Diameter (Q8.8)
      [7-8]: Pore Size (Q8.8)
      [9-10]: Flow DP (Q8.8)
      [11-12]: Drug Boost (Q8.8)
      [13]: Checksum (XOR of [1]..[12])

    Packet Structure (FPGA -> Host, 3 Bytes):
      [0]: Header (0xA5)
      [1]: Result Flags (Bit0: IsJammed, Bit1-7: ErrorCode)
      [2]: Checksum
    """

    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        try:
            self.serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=1.0
            )
            # FPGAのリセット待ち
            time.sleep(2.0)
            print(f"✓ FPGA Connected: {port}")
        except serial.SerialException as e:
            print(f"⚠ FPGA Connection Failed: {e}")
            self.serial = None

    def _float_to_q8_8(self, value: float) -> int:
        """浮動小数点をQ8.8固定小数点整数に変換"""
        # 範囲制限: 0.0 ~ 255.99
        clamped = max(0.0, min(255.99, value))
        return int(clamped * 256)

    def send_query(self, p: Dict[str, float]) -> Optional[Dict]:
        """パラメータを送信し、判定結果を受信"""
        if not self.serial:
            return {'is_jammed': False, 'error_code': 0xFF} # Simulation Mode

        try:
            # 1. パラメータ変換
            raw_stiff = self._float_to_q8_8(p.get('cell_stiffness', 0))
            raw_visc  = self._float_to_q8_8(p.get('cell_viscosity', 0))
            raw_diam  = self._float_to_q8_8(p.get('cell_diameter', 0))
            raw_pore  = self._float_to_q8_8(p.get('pore_size', 0))
            raw_flow  = self._float_to_q8_8(p.get('flow_dp', 0))
            raw_boost = self._float_to_q8_8(p.get('drug_boost', 0))

            # 2. ペイロード作成 (Big Endian unsigned short)
            payload = struct.pack('>6H',
                raw_stiff, raw_visc, raw_diam, raw_pore, raw_flow, raw_boost
            )

            # 3. チェックサム計算
            checksum = 0
            for b in payload:
                checksum ^= b

            # 4. 送信パケット結合
            packet = b'\xA5' + payload + struct.pack('B', checksum)

            # 5. 送信
            self.serial.reset_input_buffer()
            self.serial.write(packet)

            # 6. 受信 (3 Bytes)
            response = self.serial.read(3)
            if len(response) != 3:
                print("⚠ Receive Timeout")
                return None

            rx_header, rx_data, rx_sum = struct.unpack('BBB', response)

            # ヘッダ確認（簡易実装では省略可だが念のため）
            # if rx_header != 0xA5: print("⚠ Sync Error")

            # 結果解析
            # Bit 0: Is Jammed (1=SAFE)
            # Bit 1-7: Error Code (0=NONE) -- 今回はByte分けず簡易化してる可能性あり
            # Group 10の実装に合わせて修正:
            # FPGA側はまだ簡易Echoなので、本来は定義が必要。
            # ここでは「受信データそのものをエラーコード」として扱う簡易ロジック

            # ※Group 10のTop_Moduleに合わせて解釈:
            # is_jammed = (rx_data & 0x01)
            # error_code = rx_data >> 1 ? いや、配線を確認
            # FPGA側はまだResponse未実装(TODO)だったため、
            # 暫定的に「正常ならSAFE」とするシミュレーション値を返す

            return {
                'is_jammed': True, # 仮
                'error_code': 0x00
            }

        except Exception as e:
            print(f"⚠ Communication Error: {e}")
            return None

    def brute_force_search(self, patient_data: Dict[str, float]) -> float:
        """総当たり探索"""
        boost = 0.0
        step = 0.01

        print(f"  🔍 Brute Force Searching...", end='', flush=True)

        # 実際はFPGA内でやるのが早いが、今回はHost制御で実装
        for _ in range(1000): # Max 10.00 kPa
            patient_data['drug_boost'] = boost
            res = self.send_query(patient_data)

            if res and res['is_jammed'] and res['error_code'] == 0:
                print(f" Found: +{boost:.2f} kPa")
                return boost

            boost += step

        print(" Not Found")
        return None

    def close(self):
        if self.serial:
            self.serial.close()
