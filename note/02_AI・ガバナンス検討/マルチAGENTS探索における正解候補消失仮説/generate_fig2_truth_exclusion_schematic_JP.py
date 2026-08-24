from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "Meiryo"
plt.rcParams["axes.unicode_minus"] = False


OUTPUT = Path(__file__).with_name("fig2_truth_exclusion_schematic_v2_JP.png")


def rounded_box(ax, x, y, width, height, text, face, edge, fontsize=11):
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.04",
        facecolor=face,
        edgecolor=edge,
        linewidth=2,
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2,
        y + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold",
        linespacing=1.35,
    )


def main():
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle(
        "図2. 合意選択による真の候補排除の模式図",
        fontsize=20,
        fontweight="bold",
    )

    # Left: one explicit geometry, without probabilistic interpretation.
    truth = 0.0
    shared_error_candidates = [0.78, 0.88, 0.97, 1.00, 1.03, 1.08, 1.18, 1.25, 1.35]
    ax_left.axvspan(-0.3, 0.3, color="#D8EAF6", alpha=0.9, label="真の基準帯（例示）")
    ax_left.axvspan(0.72, 1.40, color="#FCE3CF", alpha=0.7, label="高合意の共有誤り領域")
    ax_left.scatter([truth], [1.0], s=260, color="#1F77B4", label="真の候補 T", zorder=3)
    ax_left.scatter(
        shared_error_candidates,
        [1.0] * len(shared_error_candidates),
        s=150,
        marker="x",
        linewidths=3,
        color="#E26A18",
        label="共有誤り候補",
        zorder=3,
    )
    ax_left.annotate(
        "合意選択された領域",
        xy=(1.05, 1.0),
        xytext=(0.72, 1.28),
        arrowprops=dict(arrowstyle="->", lw=2, color="#9C4B11"),
        fontsize=11,
        color="#9C4B11",
        fontweight="bold",
    )
    ax_left.annotate(
        "別途保持経路がなければ\n少数派候補は除外される",
        xy=(truth, 1.0),
        xytext=(-0.35, 0.68),
        arrowprops=dict(arrowstyle="->", lw=2, color="#1F5F8A"),
        fontsize=11,
        color="#1F5F8A",
        fontweight="bold",
    )
    ax_left.set_xlim(-0.5, 1.6)
    ax_left.set_ylim(0.45, 1.45)
    ax_left.set_yticks([])
    ax_left.set_xlabel("例示的な1次元特徴空間における位置", fontsize=12)
    ax_left.set_title("一つの具体的な配置", fontsize=15, fontweight="bold")
    ax_left.grid(axis="x", alpha=0.25)
    ax_left.legend(loc="upper left", fontsize=10)

    # Right: conditions required for the exclusion statement.
    ax_right.set_xlim(0, 10)
    ax_right.set_ylim(0, 10)
    ax_right.axis("off")
    ax_right.set_title("確率推定ではなく条件", fontsize=15, fontweight="bold")
    rounded_box(
        ax_right,
        0.6,
        7.4,
        8.8,
        1.4,
        "1. 真の候補は発見されるが、\n選択された特徴表現では少数派のままである",
        "#E7F1FA",
        "#5E8FB5",
    )
    rounded_box(
        ax_right,
        0.6,
        5.3,
        8.8,
        1.4,
        "2. 集約ルールは全ての分岐を保持するのではなく、\n支配的な高合意領域を選択する",
        "#FFF0D9",
        "#D59A2B",
    )
    rounded_box(
        ax_right,
        0.6,
        3.2,
        8.8,
        1.4,
        "3. 除外された候補・出所・経路は、\n独立した監査経路を通じて保持されない",
        "#F9E2E2",
        "#C65A5A",
    )
    rounded_box(
        ax_right,
        0.6,
        1.0,
        8.8,
        1.5,
        "条件付き結果\n真の候補が選択された出力から欠落しうる。\n普遍的な回復率は推定されない。",
        "#E7F4E7",
        "#4D9A58",
        fontsize=12,
    )
    for start_y, end_y in [(7.4, 6.7), (5.3, 4.6), (3.2, 2.5)]:
        ax_right.annotate(
            "",
            xy=(5.0, end_y),
            xytext=(5.0, start_y),
            arrowprops=dict(arrowstyle="->", lw=2, color="#444444"),
        )

    fig.text(
        0.5,
        0.02,
        "本図はあくまで模式図であり、モンテカルロ試行・実証的な相関推定・一般的なエージェント数についての主張を含まない。",
        ha="center",
        fontsize=11,
        fontweight="bold",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 0.94))
    fig.savefig(OUTPUT, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(OUTPUT)


if __name__ == "__main__":
    main()
