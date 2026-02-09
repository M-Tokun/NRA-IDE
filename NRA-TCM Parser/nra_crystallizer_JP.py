# -*- coding: utf-8 -*-
"""
Project: NRA-TCM Parser (Text Crystallization Method)
Version: 1.0 (Genesis)
Date: 26-0210
Author: NRA_Lab (M-Tokuni & Gemini)

Description:
    律環公理に基づき、線形なテキストデータを「意味的重力」によって再配置・結晶化させるツール。
    1500ページ級のMarkdown/Textファイルを「粒子」に分解し、動的フィルタリングと
    直感回路（Singularity Detection）を用いて重要な情報のみを抽出する。

Usage:
    python nra_crystallizer.py <filename.md>
"""

import sys
import os
import re
import math
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime

# ==========================================
# 0. Constants & Configuration (律の設定)
# ==========================================

# 許可された拡張子（これ以外はノイズとして拒絶）
ALLOWED_EXTENSIONS = {'.md', '.txt', '.markdown'}

# 特異点検知用キーワード（直感回路を刺激する言葉）
SINGULARITY_KEYWORDS = {
    # 核心・結論
    "結論", "重要", "核心", "要点", "つまり", "したがって", "結果",
    "Conclusion", "Important", "Key", "Result", "Summary",
    # 逆接・警句（文脈の転換点）
    "しかし", "ただし", "注意", "警告", "欠陥", "問題", "Error",
    "But", "However", "Note", "Warning", "Critical", "Fix",
    # 新概念・定義
    "定義", "概念", "法則", "公理", "Axiom", "Theory", "Define"
}

# システムパラメータ （文章おおよそ文字数/要点/切れ味を調整しま。す）

INITIAL_MOMENTUM = 0.0      # 初期の厚み
BASE_THRESHOLD = 0.65       # 論理ゲートの基準高さ
INTUITION_LIMIT = 0.85      # 直感ゲートの発動ライン（絶対値）
HIERARCHY_BONUS = 0.25      # 階層が1深くなるごとの重力加算係数（逆転ポテンシャル）

# ==========================================
# 1. Class Definitions (構成要素)
# ==========================================

@dataclass
class Particle:
    """意味の最小単位（粒子）"""
    id: int
    level: int          # 階層レベル (#=1, ##=2, ###=3...)
    heading: str        # 見出し
    content: str        # 本文
    length: int = field(init=False)

    def __post_init__(self):
        self.length = len(self.content)

    def calculate_gravity(self) -> tuple[float, float]:
        """
        粒子の重力を計算する。
        Returns: (Total_Gravity, Singularity_Score)
        """
        if self.length == 0:
            return 0.0, 0.0

        # A. 基礎密度 (対数スケールで正規化)
        density = math.log1p(self.length) / 10.0 # 0.0 ~ 1.0程度に収める

        # B. 階層係数 (逆転ポテンシャル: 深いほど重い)
        # Lv.1 -> 1.0, Lv.3 -> 1.5, Lv.5 -> 2.0
        level_mult = 1.0 + (max(0, self.level - 1) * HIERARCHY_BONUS)

        # C. 特異点スコア (キーワード含有率)
        singularity_hits = 0
        for kw in SINGULARITY_KEYWORDS:
            if kw in self.content or kw in self.heading:
                singularity_hits += 1

        # 特異点スコア計算 (0.0 ~ 1.0+)
        singularity_score = min(1.5, singularity_hits * 0.3)
        if self.level >= 3: # 深層階層ボーナス
            singularity_score += 0.2

        # D. 最終重力 (密度 × 階層) + 特異点
        # 特異点は加算項として働き、密度が低くても値を押し上げる
        total_gravity = (density * level_mult) + singularity_score

        return total_gravity, singularity_score

class NRA_Engine:
    """動的解析エンジン"""
    def __init__(self):
        self.momentum = INITIAL_MOMENTUM
        self.crystals = []  # 結晶化された粒子
        self.sparks = []    # 直感で拾った粒子
        self.residue_count = 0

    def _get_dynamic_threshold(self) -> float:
        """厚みに基づく動的閾値計算"""
        # tanhで -1.0 ~ 1.0 に正規化
        confidence = math.tanh(self.momentum / 4.0)
        # 閾値を ±0.15 変動させる
        # 自信がある(Pos) -> 閾値下がる(-), 自信がない(Neg) -> 閾値上がる(+)
        adjustment = confidence * 0.15
        return BASE_THRESHOLD - adjustment

    def process(self, particle: Particle):
        """粒子を判定・分類する"""
        gravity, singularity = particle.calculate_gravity()
        threshold = self._get_dynamic_threshold()

        is_crystallized = False
        action_log = ""

        # --- Phase 1: Logic Gate (文脈依存) ---
        if gravity >= threshold:
            self.crystals.append(particle)
            # 論理的成功: 厚みを少し増す
            self.momentum = min(self.momentum + 0.5, 5.0)
            is_crystallized = True
            action_log = "CRYSTAL (Logic)"

        # --- Phase 2: Intuition Gate (特異点バイパス) ---
        elif singularity >= INTUITION_LIMIT:
            # 論理では弾かれたが、直感が反応した
            self.sparks.append(particle) # Sparksリストにも保存
            self.crystals.append(particle) # 結果的には結晶として残す

            # 直感的成功: 厚みを劇的に回復（覚醒）
            self.momentum = max(self.momentum + 2.0, 2.0)
            is_crystallized = True
            action_log = "⚡ SPARK (Intuition)"

        # --- Phase 3: Residue (廃棄) ---
        else:
            self.residue_count += 1
            # 失敗: 厚みを減衰させる
            self.momentum = max(self.momentum - 0.2, -3.0)
            action_log = "Residue..."

        return is_crystallized, gravity, threshold, action_log

# ==========================================
# 2. File Handling & Parsing (入出力)
# ==========================================

def load_file(filepath: str) -> str:
    """入力ゲートキーパー"""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"REJECTED: '{path.suffix}' is not allowed. Use .md or .txt only.")

    print(f"Loading: {path.name}...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='cp932') as f: # Legacy fallback
            return f.read()

def atomize_markdown(text: str) -> list[Particle]:
    """Markdownを粒子に分解"""
    lines = text.split('\n')
    particles = []

    # Header regex: # Title, ## Section...
    header_pattern = re.compile(r'^(#+)\s+(.*)')

    curr_level = 1 # Default level
    curr_heading = "Introduction / Root"
    buffer = []
    p_id = 1

    for line in lines:
        match = header_pattern.match(line)
        if match:
            # Save previous buffer
            content = '\n'.join(buffer).strip()
            if content:
                particles.append(Particle(p_id, curr_level, curr_heading, content))
                p_id += 1

            # Start new section
            curr_level = len(match.group(1))
            curr_heading = match.group(2).strip()
            buffer = []
        else:
            buffer.append(line)

    # Last buffer
    content = '\n'.join(buffer).strip()
    if content:
        particles.append(Particle(p_id, curr_level, curr_heading, content))

    return particles

def generate_report(original_filename: str, engine: NRA_Engine, total_p: int):
    """結晶化レポート(.md)を出力"""
    timestamp = datetime.now().strftime("%Y-%m%d-%H%M")
    out_filename = f"{Path(original_filename).stem}_Crystallized_{timestamp}.md"

    with open(out_filename, 'w', encoding='utf-8') as f:
        # Header
        f.write(f"# NRA Crystallization Report: {original_filename}\n")
        f.write(f"- **Date:** {timestamp}\n")
        f.write(f"- **Engine:** NRA-TCM v1.0\n")
        f.write(f"- **Stats:** Total Particles: {total_p} | Crystals: {len(engine.crystals)} | Sparks: {len(engine.sparks)} | Residue: {engine.residue_count}\n")
        f.write(f"- **Efficiency:** {len(engine.crystals)/total_p*100:.1f}% retention\n\n")

        f.write("---\n\n")

        # 1. Sparks (Priority Insights)
        if engine.sparks:
            f.write("## ⚡ INTUITION SPARKS (Critical Insights)\n")
            f.write("> 直感回路が捕捉した特異点（文脈を無視した重要事項）\n\n")
            for p in engine.sparks:
                f.write(f"### [{p.level}] {p.heading}\n")
                f.write(f"{p.content}\n\n")
            f.write("---\n\n")

        # 2. Crystals (Contextual Logic)
        f.write("## ◆ CRYSTALLIZED KNOWLEDGE (Contextual)\n")
        f.write("> 論理ゲートを通過した文脈的知識\n\n")

        for p in engine.crystals:
            # Sparkと重複していても、文脈順に並べるために再度記載（ただしマークをつける）
            marker = "⚡" if p in engine.sparks else "◆"
            indent = "#" * (min(p.level, 6)) # Markdown header formatting
            f.write(f"{indent} {marker} {p.heading}\n")
            f.write(f"{p.content}\n\n")

    print(f"\nSUCCESS: Crystallization complete. Output saved to -> {out_filename}")

# ==========================================
# 3. Main Execution
# ==========================================

if __name__ == "__main__":
    # 引数処理（なければデフォルト動作）
    target_file = ""
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        print("Usage: python nra_crystallizer.py <filename.md>")
        # テスト用ダミー作成
        print("No input file. Creating dummy test file...")
        target_file = "nra_test_dummy.md"
        with open(target_file, "w", encoding="utf-8") as f:
            f.write("# NRA Concept\nThis is a test.\n## Linear Time\nLinear time is obsolete.\n### 結論\nSingularity is Key!")

    try:
        # 1. Load
        raw_text = load_file(target_file)

        # 2. Atomize
        particles = atomize_markdown(raw_text)
        print(f"Atomized into {len(particles)} particles.")

        # 3. Process (Crystallize)
        engine = NRA_Engine()
        print("\n--- Processing Stream ---")
        for p in particles:
            is_cryst, grav, th, act = engine.process(p)
            # ログ出力（進行状況）
            bar = "■" * int(abs(engine.momentum))
            bar = f"-{bar}" if engine.momentum < 0 else bar
            print(f"ID:{p.id:03d} Lv.{p.level} | G:{grav:.2f} vs T:{th:.2f} | {act:15s} | Mom:{engine.momentum:.1f} {bar}")

        # 4. Report
        generate_report(target_file, engine, len(particles))

    except Exception as e:
        print(f"\nERROR: {e}")
