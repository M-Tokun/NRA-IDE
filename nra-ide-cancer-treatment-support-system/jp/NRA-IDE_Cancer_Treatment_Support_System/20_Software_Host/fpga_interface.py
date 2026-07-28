# ═══════════════════════════════════════════════════════════════════════
# File: fpga_interface.py
# Phase: 20 (Master Integration)
# Date: 26-0203-1740 JST
# ═══════════════════════════════════════════════════════════════════════

import serial
import struct
import time
from typing import Dict, Optional

import nra_core_model as core

class FPGAInterface:
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1.0)
            time.sleep(2.0) # FPGA Reset Grace Period
            print(f"[OK] FPGA Infrastructure Online: {port}")
        except Exception as e:
            print(f"[WARN] FPGA Offline (SIMULATION MODE ACTIVE): {e}")
            self.serial = None

    def _float_to_q8_8(self, value: float) -> int:
        return int(max(0.0, min(255.99, value)) * 256)

    def send_query(self, p: Dict[str, float], c_type: str = "Type A") -> Optional[Dict]:
        """
        14-byte Protocol with Dynamic Type Selection
        Header: 0xA5 (Type A), 0xA6 (Type B)
        """
        # 型名は 'Type A' / 'TypeA' 等の表記ゆれを吸収してから判定する
        is_type_a = core.normalize_type(c_type) == 'typea'

        if not self.serial:
            # シミュレーションモード: 参照実装（RTL のビット単位再現）で判定する。
            # 旧版は 0xFF を返していたため、FPGA 非接続では自己診断が必ず失敗した。
            return core.evaluate(p, c_type)

        # 1. Header selection based on Cancer Type
        header = b'\xA5' if is_type_a else b'\xA6'

        # 2. Construct Payload
        payload = struct.pack('>6H',
            self._float_to_q8_8(p['cell_stiffness']),
            self._float_to_q8_8(p['cell_viscosity']),
            self._float_to_q8_8(p['cell_diameter']),
            self._float_to_q8_8(p['pore_size']),
            self._float_to_q8_8(p['flow_dp']),
            self._float_to_q8_8(p['drug_boost'])
        )

        # 3. Checksum (XOR)
        checksum = 0
        for b in payload: checksum ^= b
        packet = header + payload + struct.pack('B', checksum)

        # 4. Transmission with Retry Logic
        for attempt in range(3):
            self.serial.reset_input_buffer()
            self.serial.write(packet)
            res = self.serial.read(3)

            if len(res) == 3:
                rx_h, rx_d, rx_s = struct.unpack('BBB', res)
                # 応答ヘッダは送信ヘッダと一致すること（Type B も受理する）
                if rx_h == header[0] and rx_s == (rx_h ^ rx_d):
                    return {'is_jammed': bool(rx_d & 0x01), 'error_code': (rx_d >> 1)}
            time.sleep(0.05)

        # 0x05 = ERR_COMM (Phase 4 §2)。0x04 は FPGA のオーバーフローに予約
        return {'is_jammed': False, 'error_code': core.ERR_COMM} # Fail-Closed
