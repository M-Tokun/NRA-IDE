from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


OUTPUT = Path(__file__).with_name("fig2_truth_exclusion_schematic_v2.png")


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
        "Figure 2. Illustrative truth-candidate exclusion by agreement selection",
        fontsize=20,
        fontweight="bold",
    )

    # Left: one explicit geometry, without probabilistic interpretation.
    truth = 0.0
    shared_error_candidates = [0.78, 0.88, 0.97, 1.00, 1.03, 1.08, 1.18, 1.25, 1.35]
    ax_left.axvspan(-0.3, 0.3, color="#D8EAF6", alpha=0.9, label="illustrative truth-reference band")
    ax_left.axvspan(0.72, 1.40, color="#FCE3CF", alpha=0.7, label="high-agreement shared-error region")
    ax_left.scatter([truth], [1.0], s=260, color="#1F77B4", label="truth candidate T", zorder=3)
    ax_left.scatter(
        shared_error_candidates,
        [1.0] * len(shared_error_candidates),
        s=150,
        marker="x",
        linewidths=3,
        color="#E26A18",
        label="shared-error candidates",
        zorder=3,
    )
    ax_left.annotate(
        "agreement-selected region",
        xy=(1.05, 1.0),
        xytext=(0.72, 1.28),
        arrowprops=dict(arrowstyle="->", lw=2, color="#9C4B11"),
        fontsize=11,
        color="#9C4B11",
        fontweight="bold",
    )
    ax_left.annotate(
        "minority candidate omitted\nif no separate retention path exists",
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
    ax_left.set_xlabel("Position in an illustrative one-dimensional feature space", fontsize=12)
    ax_left.set_title("One explicit configuration", fontsize=15, fontweight="bold")
    ax_left.grid(axis="x", alpha=0.25)
    ax_left.legend(loc="upper left", fontsize=10)

    # Right: conditions required for the exclusion statement.
    ax_right.set_xlim(0, 10)
    ax_right.set_ylim(0, 10)
    ax_right.axis("off")
    ax_right.set_title("Conditions, not a probability estimate", fontsize=15, fontweight="bold")
    rounded_box(
        ax_right,
        0.6,
        7.4,
        8.8,
        1.4,
        "1. A truth candidate is discovered and remains a minority\nin the selected feature representation",
        "#E7F1FA",
        "#5E8FB5",
    )
    rounded_box(
        ax_right,
        0.6,
        5.3,
        8.8,
        1.4,
        "2. The aggregation rule selects the dominant\nhigh-agreement region rather than preserving every branch",
        "#FFF0D9",
        "#D59A2B",
    )
    rounded_box(
        ax_right,
        0.6,
        3.2,
        8.8,
        1.4,
        "3. The omitted candidate, provenance, and path\nare not retained through an independent audit route",
        "#F9E2E2",
        "#C65A5A",
    )
    rounded_box(
        ax_right,
        0.6,
        1.0,
        8.8,
        1.5,
        "CONDITIONAL RESULT\nThe truth candidate can be absent from the selected output.\nNo universal recovery rate is inferred.",
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
        "Illustrative schematic only: no Monte Carlo trial, empirical correlation estimate, or general agent-count claim.",
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
