# FileName: nra_crystallizer_JP_v2.py
# Timestamp: 26-0210-1425 (JST)
# Framework: NRA-IDE / Nomological Ring Axioms
# Logic: Adaptive Thickness (Breathing Tau) Implementation(サンドイッチ構造.ver)

import os
import sys
import re
import math
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional

# --- NRA-IDE Parameters ---
BASE_TAU = 0.35        # 基本の厚み（システムの許容範囲）
MOMENTUM_STEP = 0.2    # 吸気時の厚み増加量
DECAY_STEP = 0.05      # 呼気時の厚み減少量
MAX_MOMENTUM = 1.0     # 最大の厚み倍率
SPARK_WEIGHT = 2.0     # 特異点検知時の重力加算

@dataclass
class CrystalPoint:
    content: str
    delta: float       # ゆらぎ（重要度スコア）
    tau: float         # その瞬間の厚み
    r_ratio: float     # 通過比率 R = delta / tau
    is_spark: bool     # 直感回路による強制検知か

class NRACore:
    """NRA-IDEの因果通過ゲートを司るコアエンジン"""
    def __init__(self):
        self.base_tau = BASE_TAU
        self.momentum = 0.0
        self.intuition_keywords = ["結論", "しかし", "重要", "核心", "特異点", "！", "？"]

    def process_line(self, line: str) -> Optional[CrystalPoint]:
        # 1. Layer 01: Pre-Process (下のパン - 空間変数の排除)
        clean_content = line.strip()
        if not clean_content: return None

        # 2. Layer 02: Core Inference (具材 - ゆらぎと厚みの算出)
        # 基本的なゆらぎ(delta)の算出（構造的密度）
        delta = len(clean_content) / 100.0  # 簡易的な密度判定
        is_spark = any(k in clean_content for k in self.intuition_keywords)
        if is_spark:
            delta *= SPARK_WEIGHT

        # 動的な厚み(Adaptive Tau)の適用
        current_tau = self.base_tau * (1.0 + self.momentum)

        # 因果通過比率 R = delta / tau
        r = delta / current_tau

        # 3. Layer 03: Post-Process (上のパン - 通過判定)
        # Purity判定: Rが1.0に近いほど高純度な結晶となる
        if r >= 0.65 or is_spark:
            # 通過成功（結晶化）
            point = CrystalPoint(clean_content, delta, current_tau, r, is_spark)
            self._inhale() # 吸気: 厚みを増やす
            return point
        else:
            # 通過失敗（残滓として処理）
            self._exhale() # 呼気: 厚みを絞る
            return None

    def _inhale(self):
        """吸気: 文脈の厚みを増やし、周辺情報を吸い込む"""
        self.momentum = min(self.momentum + MOMENTUM_STEP, MAX_MOMENTUM)

    def _exhale(self):
        """呼気: 厚みを収縮させ、純度(R)の要求基準を上げる"""
        self.momentum = max(self.momentum - DECAY_STEP, 0.0)

def main():
    if len(sys.argv) < 2:
        print("Usage: python nra_crystallizer_JP_v2.py <input_file.md>")
        return

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    core = NRACore()
    crystallized_data = []

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            point = core.process_line(line)
            if point:
                crystallized_data.append(point)

    # 出力ファイル生成（スナップショットの固定）
    timestamp = datetime.now().strftime("%Y-%m%d-%H%M")
    output_path = f"{os.path.splitext(input_path)[0]}_Crystallized_{timestamp}.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# NRA Crystallization Report (v2: Adaptive Tau)\n")
        f.write(f"Generated: {timestamp} | Base Tau: {BASE_TAU}\n\n")
        f.write(f"## ⚡ INTUITION SPARKS (特異点)\n")
        for p in [x for x in crystallized_data if x.is_spark]:
            f.write(f"- {p.content}  *(R={p.r_ratio:.2f}, τ={p.tau:.2f})*\n")

        f.write(f"\n## ◆ CRYSTALLIZED KNOWLEDGE (文脈結晶)\n")
        for p in [x for x in crystallized_data if not x.is_spark]:
            f.write(f"- {p.content}  *(R={p.r_ratio:.2f})*\n")

    print(f"Crystallization Complete: {output_path}")

if __name__ == "__main__":
    main()
