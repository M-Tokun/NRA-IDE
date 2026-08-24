from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


OUTPUT = Path(__file__).with_name("fig3_noninjective_compression_conditional_v2_EN.png")


def box(ax, x, y, width, height, text, face, edge, fontsize=11, weight="normal"):
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
        fontweight=weight,
        linespacing=1.35,
    )


def arrow(ax, start, end):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="->", color="black", lw=2),
    )


def main():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title(
        "Figure 3. Non-injective consensus compression: guaranteed and conditional consequences",
        fontsize=20,
        fontweight="bold",
        pad=18,
    )

    box(
        ax,
        0.6,
        6.5,
        4.1,
        2.3,
        "STRUCTURED AGENT STATE\n\n$A=(A_1,\\ldots,A_N)$\ncontent $q$ | provenance $s$\nreasoning path $p$ | epistemic type $\\kappa$",
        "#EAF4E4",
        "#4F8A4C",
        fontsize=11,
        weight="bold",
    )
    box(
        ax,
        5.9,
        6.5,
        4.2,
        2.3,
        "CONSENSUS / COMPRESSION\n\n$G:\\mathcal{D}\\rightarrow\\mathcal{C}$\n$C=G(A)$\n\nNon-injective if $A\\ne A'$ and $G(A)=G(A')$",
        "#FFF3CD",
        "#C99700",
        fontsize=11,
        weight="bold",
    )
    box(
        ax,
        11.3,
        6.5,
        4.1,
        2.3,
        "GUARANTEED BY\nNON-INJECTIVITY\n\nAt least two distinct inputs share $C$\nNo global left inverse recovers every $A$",
        "#E7F0FA",
        "#5B8DB8",
        fontsize=11,
        weight="bold",
    )
    arrow(ax, (4.7, 7.65), (5.9, 7.65))
    arrow(ax, (10.1, 7.65), (11.3, 7.65))

    ax.text(
        8,
        5.8,
        "Non-injectivity does not identify which semantic fields were omitted.\nAudit the saved output and every separate retention channel.",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#7A4D00",
    )

    box(
        ax,
        0.6,
        2.5,
        4.1,
        2.2,
        "CONDITIONAL CONTENT LOSS\n\nIf candidate content $q$ is encoded\nin neither $C$ nor a retained record,\nthe original candidate is unavailable downstream.",
        "#FBE7E7",
        "#C75B5B",
        fontsize=10.5,
        weight="bold",
    )
    box(
        ax,
        5.95,
        2.5,
        4.1,
        2.2,
        "CONDITIONAL PROVENANCE LOSS\n\nIf source $s$ and type $\\kappa$ are encoded\nin neither $C$ nor a retained record,\norigin and epistemic type cannot be recovered.",
        "#FFF0DD",
        "#C98434",
        fontsize=10.5,
        weight="bold",
    )
    box(
        ax,
        11.3,
        2.5,
        4.1,
        2.2,
        "CONDITIONAL STRUCTURAL LOSS\n\nIf dependency path $p$ is encoded\nin neither $C$ nor a retained record,\nthe original support path cannot be recovered.",
        "#E8F3E5",
        "#5B9555",
        fontsize=10.5,
        weight="bold",
    )
    arrow(ax, (2.65, 5.15), (2.65, 4.7))
    arrow(ax, (8, 5.15), (8, 4.7))
    arrow(ax, (13.35, 5.15), (13.35, 4.7))

    ax.text(
        8,
        1.2,
        "Exact conclusion: $G$ being non-injective proves non-unique recoverability of the full input.\n"
        "A specific content, provenance, or path loss requires evidence that the corresponding field was not retained elsewhere.",
        ha="center",
        va="center",
        fontsize=11.5,
        fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.45",
            facecolor="#EEF2F7",
            edgecolor="#7186A0",
            linewidth=2,
        ),
    )

    fig.subplots_adjust(top=0.91, bottom=0.04, left=0.03, right=0.97)
    fig.savefig(OUTPUT, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(OUTPUT)


if __name__ == "__main__":
    main()
