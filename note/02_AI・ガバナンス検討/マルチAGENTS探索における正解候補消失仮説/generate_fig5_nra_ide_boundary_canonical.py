from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


OUTPUT = Path(__file__).with_name("fig5_nra_ide_boundary_canonical_v2.png")


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


def arrow(ax, start, end, label, color="black", style="->", width=2):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle=style, color=color, lw=width),
    )
    ax.text(
        (start[0] + end[0]) / 2,
        (start[1] + end[1]) / 2 + 0.18,
        label,
        ha="center",
        va="bottom",
        fontsize=10,
        color=color,
        fontweight="bold" if color != "black" else "normal",
    )


def main():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title(
        "Figure 5. NRA-IDE canonical boundary: structural inputs, states, and authority",
        fontsize=20,
        fontweight="bold",
        pad=18,
    )

    # Cause-Side authority and inputs.
    box(
        ax,
        0.4,
        5.7,
        4.4,
        3.2,
        "CAUSE-SIDE INPUT AUTHORITY\n\nDirect observations\nPre-fixed transformation rules\nDeclared target / unit / time / source\nAuthorized update route and snapshot",
        "#E8F5E9",
        "#43A047",
        fontsize=11,
        weight="bold",
    )

    # Canonical evaluator and complete numeric state ladder.
    box(
        ax,
        5.8,
        4.8,
        4.6,
        4.1,
        "NRA-IDE CANONICAL EVALUATION\n\n$R=\\delta/\\tau$\n\n$0\\leq R<R_{warn}$ : PERMIT\n$R_{warn}\\leq R<R_{handoff}$ : BOUNDARY_WARNING\n$R_{handoff}\\leq R<R_{irrev}$ : HANDOFF_REQUIRED\n$R_{irrev}\\leq R<1$ : IRREVERSIBLE_TRANSITION\n$R\\geq1$ : RUPTURE_BOUNDARY\n\nINPUT EXCEPTIONS\n$\\tau=0$ : OUT_OF_DESCRIPTION_DOMAIN\nunknown / invalid / non-finite : CONFESSION",
        "#FFF3CD",
        "#C99700",
        fontsize=9.2,
        weight="bold",
    )
    arrow(ax, (4.8, 7.3), (5.8, 7.3), "")
    ax.text(5.3, 7.55, "only valid structural inputs", ha="center", fontsize=10)

    # Effect-Side remains outside structural-input authority.
    box(
        ax,
        11.3,
        5.7,
        4.3,
        3.2,
        "EFFECT-SIDE ARTIFACTS\n\nMulti-agent consensus\nReasoning outputs\nSynthetic / generated data\nSelf-consistency filters\nPrior generated outputs",
        "#FDECEC",
        "#D05C5C",
        fontsize=11,
        weight="bold",
    )
    arrow(ax, (10.4, 7.8), (11.3, 7.8), "")
    ax.text(10.85, 8.05, "read-only access to snapshot", ha="center", fontsize=10)

    # No reverse input path from Effect-Side.
    arrow(
        ax,
        (11.3, 6.2),
        (10.4, 6.2),
        "",
        color="#C62828",
        style="-[",
        width=2.5,
    )
    ax.text(
        13.45,
        5.1,
        "FORBIDDEN REVERSE INPUT\nNo update of $\\delta$, $\\tau$, $R$, thresholds, state, or latch",
        ha="center",
        va="center",
        fontsize=9.5,
        color="#C62828",
        fontweight="bold",
    )

    # Keep target state, execution authority, and surviving channels distinct.
    box(
        ax,
        0.5,
        2.0,
        4.5,
        2.2,
        "SURVIVING CHANNELS\n\nObservation state\nLogging state\nCommunication state\nAudit lineage",
        "#EAF2F8",
        "#5B8DB8",
        fontsize=11,
        weight="bold",
    )
    box(
        ax,
        5.8,
        2.0,
        4.6,
        2.2,
        "BOUNDARY OUTPUT\n\nTarget state\nExecution authority\nTestimony mode\nIrreversible-latch state",
        "#EEF1F8",
        "#6677A8",
        fontsize=11,
        weight="bold",
    )
    box(
        ax,
        11.3,
        2.0,
        4.3,
        2.2,
        "FAIL-CLOSED\nOPERATIONAL PRINCIPLE\n\nSuppress unauthorized autonomous processing;\ndo not erase observation, logs, or testimony",
        "#F3E5F5",
        "#8E5AA9",
        fontsize=10.5,
        weight="bold",
    )
    arrow(ax, (8.1, 4.8), (8.1, 4.2), "")
    ax.text(8.1, 4.48, "classification and authority control", ha="center", fontsize=9.5)
    arrow(ax, (10.4, 3.1), (11.3, 3.1), "operational effect")

    ax.text(
        8,
        0.8,
        "A new authorized Cause-Side observation may update the next snapshot; verification does not retype an AI output.\n"
        "$R$ controls structural boundary classification and execution authority, not truth reconstruction or $p_t$ recovery.",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#E7F0FA", edgecolor="#7295BE", linewidth=2),
    )

    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(OUTPUT)


if __name__ == "__main__":
    main()
