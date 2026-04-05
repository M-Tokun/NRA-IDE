# ═══════════════════════════════════════════════════════════════════════
# File: fpga_interface.py
# Phase: 20 (Master Integration)
# Date: 26-0203-1740 JST
# ═══════════════════════════════════════════════════════════════════════

import serial
import struct
import time
from typing import Dict, Optional

class FPGAInterface:
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1.0)
            time.sleep(2.0) # FPGA Reset Grace Period
            print(f"✓ FPGA Infrastructure Online: {port}")
        except Exception as e:
            print(f"⚠ FPGA Offline (SIMULATION MODE ACTIVE): {e}")
            self.serial = None

    def _float_to_q8_8(self, value: float) -> int:
        return int(max(0.0, min(255.99, value)) * 256)

    def send_query(self, p: Dict[str, float], c_type: str = "Type A") -> Optional[Dict]:
        """
        14-byte Protocol with Dynamic Type Selection
        Header: 0xA5 (Type A), 0xA6 (Type B)
        """
        if not self.serial:
            return {'is_jammed': False, 'error_code': 0xFF} # Sim Default

        # 1. Header selection based on Cancer Type
        header = b'\xA5' if c_type == "Type A" else b'\xA6'

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
                if rx_h == 0xA5 and rx_s == (rx_h ^ rx_d):
                    return {'is_jammed': bool(rx_d & 0x01), 'error_code': (rx_d >> 1)}
            time.sleep(0.05)

        return {'is_jammed': False, 'error_code': 0x04} # Comm Error (Fail-Closed)
