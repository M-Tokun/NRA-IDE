from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


OUTPUT = Path(__file__).with_name("fig4_recursive_error_expectation_v2.png")


def box(ax, x, y, width, height, text, face, edge, fontsize=10.5):
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
        linespacing=1.25,
    )


def main():
    alpha = 0.7
    beta = 0.15
    mu = 2 / 7
    e0 = 0.0
    rounds = list(range(21))
    expected = [
        alpha**t * e0 + beta * mu * (1 - alpha**t) / (1 - alpha)
        for t in rounds
    ]
    limit = beta * mu / (1 - alpha)

    fig = plt.figure(figsize=(16, 11))
    grid = fig.add_gridspec(2, 1, height_ratios=[1.05, 1.2], hspace=0.28)
    ax_flow = fig.add_subplot(grid[0])
    ax_plot = fig.add_subplot(grid[1])
    fig.suptitle(
        "Figure 4. Recursive premise contamination and a conditional expectation model",
        fontsize=20,
        fontweight="bold",
    )

    ax_flow.set_xlim(0, 16)
    ax_flow.set_ylim(0, 5)
    ax_flow.axis("off")
    flow = [
        (0.3, "Cause-Side\nobservation / source", "#E6F2E3", "#4C8A48"),
        (3.5, "Agent inference\nmultiple candidates", "#F7E6E6", "#B85C5C"),
        (6.7, "Agreement selection\nand compression", "#FFF0C9", "#C6951A"),
        (9.9, "BOUNDARY VIOLATION\noutput treated as if verified\nwhile type / provenance is erased", "#F9D9C8", "#C55B32"),
        (13.1, "Next round\nreuses the premise", "#F2D4D7", "#A94E57"),
    ]
    for x, text, face, edge in flow:
        box(ax_flow, x, 2.4, 2.6, 1.5, text, face, edge, fontsize=9.5)
    for x in [2.9, 6.1, 9.3, 12.5]:
        ax_flow.annotate(
            "",
            xy=(x + 0.6, 3.15),
            xytext=(x, 3.15),
            arrowprops=dict(arrowstyle="->", lw=2, color="#333333"),
        )
    ax_flow.text(
        8,
        1.25,
        "The boundary violation is not a canonical Cause-Side update.\n"
        "Information-structural loss comes from omitted candidates, provenance, type, and dependency paths.",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
    )
    ax_flow.text(
        8,
        0.35,
        r"$e_{t+1}=\alpha e_t+\beta\varepsilon_t$,  "
        r"$0\leq\alpha<1$,  $\beta\geq0$,  $E[\varepsilon_t]=\mu$",
        ha="center",
        fontsize=12,
    )

    ax_plot.plot(rounds, expected, marker="o", linewidth=2.5, label="theoretical expectation")
    ax_plot.axhline(limit, color="#D97706", linestyle="--", linewidth=2.5, label=f"limit = {limit:.6f}")
    ax_plot.set_xlabel("Recursive round $t$", fontsize=12)
    ax_plot.set_ylabel(r"Expected error-strength proxy $E[e_t]$", fontsize=12)
    ax_plot.set_title(
        r"Explicit example: $e_0=0$, $\alpha=0.7$, $\beta=0.15$, $\mu=2/7$",
        fontsize=14,
        fontweight="bold",
    )
    ax_plot.set_xticks(rounds)
    ax_plot.set_ylim(0, 0.16)
    ax_plot.grid(alpha=0.3)
    ax_plot.legend(loc="lower right", fontsize=11)
    ax_plot.text(
        0.02,
        0.92,
        "Expectation curve only; no random trials or confidence interval.\n"
        "This scalar recurrence does not prove information irreversibility.",
        transform=ax_plot.transAxes,
        va="top",
        fontsize=11,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#777777"),
    )

    fig.subplots_adjust(top=0.90, bottom=0.07, left=0.06, right=0.98, hspace=0.28)
    fig.savefig(OUTPUT, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(OUTPUT)


if __name__ == "__main__":
    main()
