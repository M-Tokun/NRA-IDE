# FileName: nra_crystallizer_EN_v2.py
# Timestamp: 26-0210-1458 (JST)
# Framework: NRA-IDE / Nomological Ring Axioms
# Logic: Adaptive Thickness (Breathing Tau) - Global Edition

import os
import sys
import datetime
from dataclasses import dataclass
from typing import List, Optional

# --- NRA-IDE Parameters (Optimized for English Token Density) ---
BASE_TAU = 0.45        # Higher base tau for English (sparse info density)
MOMENTUM_STEP = 0.25   # Slightly faster inhalation to capture long English sentences
DECAY_STEP = 0.08      # Slightly faster decay
MAX_MOMENTUM = 1.2
SPARK_WEIGHT = 2.5     # Higher weight for distinct English structural markers

@dataclass
class CrystalPoint:
    content: str
    delta: float       # Momentum / Fluctuation score
    tau: float         # Dynamic Thickness
    r_ratio: float     # Passability Ratio R = delta / tau
    is_spark: bool     # Intuition Circuit Triggered

class NRACoreEN:
    """NRA-IDE Causality Pass Gate Core"""
    def __init__(self):
        self.base_tau = BASE_TAU
        self.momentum = 0.0
        # Keywords for global intuition detection
        self.intuition_keywords = [
            "Conclusion", "However", "Important", "Critical",
            "Paradigm", "Singularity", "Structure", "Result"
        ]

    def process_line(self, line: str) -> Optional[CrystalPoint]:
        # 1. Layer 01: Pre-Process (Bottom Bread - Sanitization)
        clean_content = line.strip()
        if not clean_content: return None

        # 2. Layer 02: Core Inference (Filling - Dynamics)
        # Calculate Delta (Structural Density)
        delta = len(clean_content) / 150.0  # Normalized for English character count
        is_spark = any(k.lower() in clean_content.lower() for k in self.intuition_keywords)
        if is_spark:
            delta *= SPARK_WEIGHT

        # Adaptive Thickness (Breathing Tau)
        current_tau = self.base_tau * (1.0 + self.momentum)

        # Passability Ratio R = delta / tau
        r = delta / current_tau

        # 3. Layer 03: Post-Process (Top Bread - Verification)
        # Purity check: Optimized for technical documentation (0.75 threshold)
        if r >= 0.75 or is_spark:
            point = CrystalPoint(clean_content, delta, current_tau, r, is_spark)
            self._inhale()
            return point
        else:
            self._exhale()
            return None

    def _inhale(self):
        """Inhale: Expand Tau to capture deeper context"""
        self.momentum = min(self.momentum + MOMENTUM_STEP, MAX_MOMENTUM)

    def _exhale(self):
        """Exhale: Shrink Tau to increase purity requirements"""
        self.momentum = max(self.momentum - DECAY_STEP, 0.0)

def main():
    if len(sys.argv) < 2:
        print("Usage: python nra_crystallizer_EN_v2.py <input_file.md>")
        return

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    core = NRACoreEN()
    crystallized_data = []

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            point = core.process_line(line)
            if point:
                crystallized_data.append(point)

    # Generate Snapshot (Fixed Output)
    timestamp = datetime.datetime.now().strftime("%Y-%m%d")
    output_path = f"{os.path.splitext(input_path)[0]}_Crystallized_EN_{timestamp}.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# NRA Crystallization Report (v2: Global)\n")
        f.write(f"Generated: {timestamp} | Base Tau: {BASE_TAU}\n\n")
        f.write(f"## ⚡ INTUITION SPARKS\n")
        for p in [x for x in crystallized_data if x.is_spark]:
            f.write(f"- {p.content}  *(R={p.r_ratio:.2f}, τ={p.tau:.2f})*\n")

        f.write(f"\n## ◆ CRYSTALLIZED KNOWLEDGE\n")
        for p in [x for x in crystallized_data if not x.is_spark]:
            f.write(f"- {p.content}  *(R={p.r_ratio:.2f})*\n")

    print(f"Crystallization Complete: {output_path}")

if __name__ == "__main__":
    main()
