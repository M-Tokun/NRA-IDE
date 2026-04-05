# FileName: nra_crystallizer_JP_v3.1.py
# バージョン: 3.1　著作権者　M-Tokuni
# 作った日: 2026年2月11日
# 何をするプログラム？ → AIが長い文章を読み込んで、「密度判定」で重要な部分だけを残す要約マシンです。
# 難しい言葉は使わず、誰でも調整できるようにコメントを書きました
# 原文のカジュアル度合いが大きすぎると役に立ちません。コード改変が簡単で実装可能ですが激重になるだけです。
# 今回は汎用版ですが、面倒でなければパラメータを参考に小説/論文/会議録などpy分けが実用的です。

import os
import sys
import re
import math
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# ── ここを変えると要約の厳しさが変わります ──(AIの注目度合い判定)
BASE_TAU = 0.41          # 基本の「許容の広さ」。小さいほど厳しくなる（おすすめ: 0.35〜0.50）
MOMENTUM_STEP = 0.2      # 良い部分を見つけたらどれだけ「集中モード」になるか
DECAY_STEP = 0.1        # つまらない部分が続くとどれだけ集中が戻るか
MAX_MOMENTUM = 0.8       # 集中モードの最大値（1.0で止まる）
SPARK_WEIGHT = 2.0       # 「これは大事！」と思ったときの特別ボーナス（大きくしすぎると雑になる）

# 重要な言葉リスト（これが入っていると「大事かも！」と考える）
IMPORTANT_WORDS = ["結論", "しかし", "重要", "核心", "特異点", "つまり", "要するに", "結局", "まとめると"]

@dataclass
class CrystalPoint:
    content: str     # 残した文章
    delta: float     # この行の「濃さ」（数字が大きいほど濃い）
    tau: float       # 今の「許容の広さ」
    r_ratio: float   # 濃さ ÷ 許容の広さ（これが大きいと通過しやすい）
    is_spark: bool   # 「これは大事！」と特別に思った行か？
class NRACore:
    def __init__(self):
        self.base_tau = BASE_TAU
        self.momentum = 0.0               # 集中度（0〜1.0）
        self.spark_streak = 0             # 大事な行が続いた回数
        self.intuition_keywords = IMPORTANT_WORDS
        self.momentum_history: List[float] = []  # 集中度の変化を記録
        self.prev_deltas: List[float] = []       # 最近の濃さを覚えておく

    def process_line(self, line: str) -> Optional[CrystalPoint]:
        clean_content = line.strip()
        if not clean_content:
            return None

        # 見出し（#）のレベルを調べる
        header_level = self._get_header_level(clean_content)

        # 見出しのレベルでボーナス（ほとんど変えない。1.6とか入れると挙動が凄く変化）
        if header_level == 1:
            bonus = 0.95
        elif header_level == 3:
            bonus = 1.05
        elif header_level >= 4:
            bonus = 1.10
        else:
            bonus = 1.00

        # この行の濃さ（長さで計算）
        delta_base = math.log1p(len(clean_content)) / 5.0
        delta = delta_base * bonus

        # 「大事な言葉」が入っているかチェック
        has_important_word = any(word in clean_content for word in self.intuition_keywords)

        # 最近5行の平均濃さと比べて、急に濃くなったか？
        avg_prev = sum(self.prev_deltas[-5:]) / len(self.prev_deltas[-5:]) if self.prev_deltas else 1.0
        sudden_jump = delta / avg_prev if avg_prev > 0 else 0
        is_spark = has_important_word and (sudden_jump > 1.8 or len(self.prev_deltas) < 3)

        if is_spark:
            delta *= SPARK_WEIGHT

        # 今の許容の広さ
        current_tau = self.base_tau * (1.0 + self.momentum)

        # 濃さ ÷ 許容の広さ
        r = delta / current_tau

        self.prev_deltas.append(delta)

        # 通過できるか判定
        if r >= 0.65 or is_spark:
            content = clean_content

            # 感嘆符（！）があったら、後ろの余分な部分を切る（感情部分を消す）
            if is_spark and '！' in content:
                last_pos = content.rfind('！')
                if last_pos != -1:
                    trimmed = content[:last_pos].rstrip(' ？！')
                    if trimmed.strip():
                        content = trimmed

            point = CrystalPoint(content, delta, current_tau, r, is_spark)
            self._inhale(is_spark)
            self.momentum_history.append(self.momentum)
            return point
        else:
            self._exhale()
            self.momentum_history.append(self.momentum)
            return None

    def _get_header_level(self, line: str) -> int:
        match = re.match(r'^(#{1,6})\s', line)
        return len(match.group(1)) if match else 0

    def _inhale(self, is_spark: bool = False):
        if is_spark:
            add = MOMENTUM_STEP / (1.0 + math.log1p(self.spark_streak))
            self.momentum = min(self.momentum + add, MAX_MOMENTUM)
            self.spark_streak += 1
        else:
            self.momentum = min(self.momentum + MOMENTUM_STEP, MAX_MOMENTUM)
            self.spark_streak = 0

    def _exhale(self):
        self.momentum = max(self.momentum - DECAY_STEP, 0.0)
        self.spark_streak = max(self.spark_streak - 1, 0)

    def process_paragraph(self, lines: List[str]) -> List[CrystalPoint]:
        crystals = []
        has_crystal = False

        for line in lines:
            point = self.process_line(line)
            if point:
                crystals.append(point)
                has_crystal = True

        # 段落が良かったら、次の段落も少し集中しやすくする
        if has_crystal:
            self.momentum *= 0.7
        else:
            self.momentum = max(self.momentum * 0.3, 0.0)

        return crystals

def main():
    if len(sys.argv) < 2:
        print("使い方: python nra_crystallizer_JP_v3.1.py ファイル名.md")
        return

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"ファイルが見つかりません: {input_path}")
        return

    core = NRACore()
    crystallized = []

    with open(input_path, 'r', encoding='utf-8') as f:
        paragraph = []
        for line in f:
            if line.strip() == '':
                if paragraph:
                    crystallized.extend(core.process_paragraph(paragraph))
                    paragraph = []
            else:
                paragraph.append(line)
        if paragraph:
            crystallized.extend(core.process_paragraph(paragraph))

    timestamp = datetime.now().strftime("%Y-%m%d-%H%M")
    output_path = f"{os.path.splitext(input_path)[0]}_要約_{timestamp}.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# 要約レポート（v3.1）\n")
        f.write(f"作った日時: {timestamp} | 基本の許容: {BASE_TAU}\n\n")
        f.write(f"## 大事なポイント（特別ピックアップ）\n")
        for p in [x for x in crystallized if x.is_spark]:
            f.write(f"- {p.content}  *(スコア={p.r_ratio:.2f})*\n")

        f.write(f"\n## 残った大事な文\n")
        for p in [x for x in crystallized if not x.is_spark]:
            f.write(f"- {p.content}  *(スコア={p.r_ratio:.2f})*\n")

        f.write("\n## 集中度の変化グラフ（テキスト版）\n")
        if core.momentum_history:
            max_m = max(core.momentum_history)
            n = len(core.momentum_history)
            for i in range(0, n, max(1, n // 30)):
                pos = (i / n) * 100
                m = core.momentum_history[i]
                bar = "█" * int(30 * (m / max_m)) if max_m > 0 else ""
                f.write(f"{pos:>4.0f}% | {bar:<30}  集中={m:.2f}\n")

    print(f"要約ができました！ → {output_path}")

if __name__ == "__main__":
    main()
