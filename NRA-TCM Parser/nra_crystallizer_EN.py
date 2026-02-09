# -*- coding: utf-8 -*-
"""
Project: NRA-TCM Parser (English Edition)
Version: 1.0 (Professional)
Date: 2026-02-10
Author: NRA_Lab

Description:
    A dynamic text extraction tool designed for processing large-scale documentation.
    It utilizes adaptive thresholding and structure-based weighting to separate
    high-value insights from noise, regardless of document length.

Usage:
    python nra_crystallizer_EN.py <filename.md>
"""

import sys
import os
import re
import math
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime

# ==========================================
# 0. Configuration & Parameters
# ==========================================

ALLOWED_EXTENSIONS = {'.md', '.txt', '.markdown'}

# Critical Keywords for Singularity Detection
# These words trigger the intuition circuit to bypass the standard filter.
SINGULARITY_KEYWORDS = {
    # Conclusions & Core Concepts
    "Conclusion", "Summary", "Key", "Takeaway", "Result", "Outcome",
    "Definition", "Principle", "Axiom", "Theory", "Core", "Goal",
    # Transitions & Warnings (Context Shifts)
    "However", "But", "Although", "Note", "Warning", "Critical",
    "Error", "Issue", "Bug", "Fix", "Solution", "Must", "Important"
}

# System Parameters (Tuned for English Text)
INITIAL_MOMENTUM = 0.0
# English has lower information density per char than Japanese.
# We set a stricter threshold (0.75) to avoid capturing too much fluff.
BASE_THRESHOLD = 0.75
INTUITION_LIMIT = 0.85
HIERARCHY_BONUS = 0.25

# ==========================================
# 1. Class Definitions
# ==========================================

@dataclass
class Particle:
    """Represents a minimal unit of semantic meaning."""
    id: int
    level: int          # Heading Level (#=1, ##=2, ...)
    heading: str        # Section Title
    content: str        # Body Text
    length: int = field(init=False)

    def __post_init__(self):
        self.length = len(self.content)

    def calculate_weight(self) -> tuple[float, float]:
        """
        Calculates the semantic weight of the particle.
        Returns: (Total_Weight, Singularity_Score)
        """
        if self.length == 0:
            return 0.0, 0.0

        # A. Base Density (Normalized Logarithmic Scale)
        density = math.log1p(self.length) / 10.0

        # B. Hierarchy Multiplier (Deep Structure Priority)
        # Deeper indentation often implies specific, valuable details.
        level_mult = 1.0 + (max(0, self.level - 1) * HIERARCHY_BONUS)

        # C. Singularity Score (Keyword Frequency)
        singularity_hits = 0
        for kw in SINGULARITY_KEYWORDS:
            # Case-insensitive search for broader matching
            if kw.lower() in self.content.lower() or kw.lower() in self.heading.lower():
                singularity_hits += 1

        singularity_score = min(1.5, singularity_hits * 0.3)
        if self.level >= 3:
            singularity_score += 0.2

        # D. Total Weight
        total_weight = (density * level_mult) + singularity_score

        return total_weight, singularity_score

class DynamicFilterEngine:
    """Adaptive Context Engine"""
    def __init__(self):
        self.momentum = INITIAL_MOMENTUM
        self.extracts = []  # Contextual Extracts
        self.highlights = []    # Keyword Highlights
        self.residue_count = 0

    def _get_dynamic_threshold(self) -> float:
        """Calculates the current filtering threshold based on momentum."""
        # Normalize momentum using tanh (-1.0 to 1.0)
        confidence = math.tanh(self.momentum / 4.0)
        # Adjust threshold: High confidence lowers the bar (more inclusive).
        adjustment = confidence * 0.15
        return BASE_THRESHOLD - adjustment

    def process(self, particle: Particle):
        """Evaluates a particle against the dynamic threshold."""
        weight, singularity = particle.calculate_weight()
        threshold = self._get_dynamic_threshold()

        is_kept = False
        action_log = ""

        # --- Phase 1: Context Logic (Standard Filter) ---
        if weight >= threshold:
            self.extracts.append(particle)
            # Success increases system momentum (Contextual Confidence)
            self.momentum = min(self.momentum + 0.5, 5.0)
            is_kept = True
            action_log = "EXTRACT (Context)"

        # --- Phase 2: Singularity Check (Keyword Bypass) ---
        elif singularity >= INTUITION_LIMIT:
            # Logic failed, but keywords detected high value.
            self.highlights.append(particle)
            self.extracts.append(particle)

            # Discovery significantly boosts momentum (Re-engagement)
            self.momentum = max(self.momentum + 2.0, 2.0)
            is_kept = True
            action_log = "⚡ HIGHLIGHT (Key)"

        # --- Phase 3: Residue (Discard) ---
        else:
            self.residue_count += 1
            # Failure decreases momentum (Stricter filtering)
            self.momentum = max(self.momentum - 0.2, -3.0)
            action_log = "Skipped..."

        return is_kept, weight, threshold, action_log

# ==========================================
# 2. File Handling & Parsing
# ==========================================

def load_file(filepath: str) -> str:
    """Validates and loads the file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"REJECTED: '{path.suffix}' format is not supported. Please use .md or .txt.")

    print(f"Loading: {path.name}...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback for Western European encodings if UTF-8 fails
        with open(path, 'r', encoding='latin-1') as f:
            return f.read()

def parse_markdown(text: str) -> list[Particle]:
    """Parses Markdown text into structural particles."""
    lines = text.split('\n')
    particles = []

    header_pattern = re.compile(r'^(#+)\s+(.*)')

    curr_level = 1
    curr_heading = "Introduction / Root"
    buffer = []
    p_id = 1

    for line in lines:
        match = header_pattern.match(line)
        if match:
            content = '\n'.join(buffer).strip()
            if content:
                particles.append(Particle(p_id, curr_level, curr_heading, content))
                p_id += 1

            curr_level = len(match.group(1))
            curr_heading = match.group(2).strip()
            buffer = []
        else:
            buffer.append(line)

    content = '\n'.join(buffer).strip()
    if content:
        particles.append(Particle(p_id, curr_level, curr_heading, content))

    return particles

def generate_report(original_filename: str, engine: DynamicFilterEngine, total_p: int):
    """Generates the structured Markdown report."""
    timestamp = datetime.now().strftime("%Y-%m%d-%H%M")
    out_filename = f"{Path(original_filename).stem}_Processed_{timestamp}.md"

    with open(out_filename, 'w', encoding='utf-8') as f:
        # Report Header
        f.write(f"# Document Processing Report: {original_filename}\n")
        f.write(f"- **Date:** {timestamp}\n")
        f.write(f"- **Engine:** NRA-TCM v1.0 (Professional)\n")
        f.write(f"- **Stats:** Input Segments: {total_p} | Extracts: {len(engine.extracts)} | Highlights: {len(engine.highlights)} | Skipped: {engine.residue_count}\n")
        f.write(f"- **Retention Rate:** {len(engine.extracts)/total_p*100:.1f}%\n\n")

        f.write("---\n\n")

        # 1. Critical Highlights (The "Sparks")
        if engine.highlights:
            f.write("## ⚡ CRITICAL HIGHLIGHTS\n")
            f.write("> Key insights detected via keyword analysis (Independent of context flow).\n\n")
            for p in engine.highlights:
                f.write(f"### [{p.level}] {p.heading}\n")
                f.write(f"{p.content}\n\n")
            f.write("---\n\n")

        # 2. Contextual Extracts (The "Crystals")
        f.write("## ◆ CONTEXTUAL EXTRACTS\n")
        f.write("> Information preserved by the adaptive logic filter.\n\n")

        for p in engine.extracts:
            marker = "⚡" if p in engine.highlights else "◆"
            indent = "#" * (min(p.level, 6))
            f.write(f"{indent} {marker} {p.heading}\n")
            f.write(f"{p.content}\n\n")

    print(f"\nSUCCESS: Processing complete. Report saved to -> {out_filename}")

# ==========================================
# 3. Main Execution
# ==========================================

if __name__ == "__main__":
    target_file = ""
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        print("Usage: python nra_crystallizer_EN.py <filename.md>")
        print("No input file provided. Creating a dummy test file...")
        target_file = "nra_test_dummy_en.md"
        with open(target_file, "w", encoding="utf-8") as f:
            f.write("# NRA Concept\nTesting English processing.\n## Linear Time\nLinear time is inefficient.\n### Conclusion\nSingularity is the key to understanding!")

    try:
        # 1. Load
        raw_text = load_file(target_file)

        # 2. Parse
        particles = parse_markdown(raw_text)
        print(f"Parsed {len(particles)} segments.")

        # 3. Process
        engine = DynamicFilterEngine()
        print("\n--- Processing Stream ---")
        for p in particles:
            is_kept, weight, th, act = engine.process(p)
            # Visualization Bar
            bar = "■" * int(abs(engine.momentum))
            bar = f"-{bar}" if engine.momentum < 0 else bar
            print(f"ID:{p.id:03d} Lv.{p.level} | W:{weight:.2f} vs T:{th:.2f} | {act:15s} | Mom:{engine.momentum:.1f} {bar}")

        # 4. Report
        generate_report(target_file, engine, len(particles))

    except Exception as e:
        print(f"\nERROR: {e}")
