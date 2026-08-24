from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


OUTPUT = Path(__file__).with_name("fig6_conditional_results_summary_v2_EN.png")


def result_box(ax, x, y, width, height, title, text, face, edge):
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.05",
        facecolor=face,
        edgecolor=edge,
        linewidth=2.2,
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2,
        y + height - 0.36,
        title,
        ha="center",
        va="top",
        fontsize=14,
        fontweight="bold",
    )
    ax.text(
        x + width / 2,
        y + height / 2 - 0.12,
        text,
        ha="center",
        va="center",
        fontsize=10.2,
        linespacing=1.35,
    )


def main():
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis("off")
    ax.set_title(
        "Figure 6. Conditional mathematical results and their scope",
        fontsize=22,
        fontweight="bold",
        pad=18,
    )

    result_box(
        ax,
        0.6,
        6.6,
        8.0,
        4.2,
        "CONDITIONAL RESULT 1 — Asymmetric agreement filtering",
        "Model: two sampled candidates are retained only for same-side pairs;\n"
        "truth-side and error-side effective pass rates are $0<a,b\\leq1$.\n\n"
        "$p_{t+1}=\\dfrac{ap_t^2}{ap_t^2+b(1-p_t)^2}$,  $p_*=\\dfrac{b}{a+b}$\n"
        "$p_0<p_*\\;\\Longrightarrow\\;p_t\\to0$\n\n"
        "Scope: this is a conditional minimal map, not a universal consensus law.\n"
        "Truth being an outlier does not itself imply $a\\ll b$.",
        "#E5F0FA",
        "#5C91C7",
    )

    result_box(
        ax,
        9.4,
        6.6,
        8.0,
        4.2,
        "CONDITIONAL RESULT 2 — Feature-space exclusion",
        "Fix and validate $\\phi:\\mathcal{A}\\to V$ before evaluation; let $x_i=\\phi(A_i)$.\n"
        "$\\mathcal{E}=\\operatorname{span}\\{x_2,\\ldots,x_N\\}\\subseteq V$\n\n"
        "$T\\perp\\mathcal{E}$ and $g(x_1,\\ldots,x_N)\\in\\mathcal{E}$\n"
        "$\\Longrightarrow\\;\\langle g(x_1,\\ldots,x_N),T\\rangle_V=0$\n\n"
        "Scope: the conceptual agent tuple is not automatically a vector.\n"
        "The feature map and inner-product interpretation require separate evidence.",
        "#FBE9E9",
        "#C56A6A",
    )

    result_box(
        ax,
        0.6,
        2.0,
        8.0,
        4.0,
        "CONDITIONAL RESULT 3 — Non-injective compression",
        "$G:\\mathcal{D}\\to\\mathcal{C}$ is non-injective\n"
        "$\\Longrightarrow$ no global left inverse recovers every original input $A$.\n\n"
        "Guaranteed: the complete input is not uniquely recoverable from $C=G(A)$ alone.\n\n"
        "Conditional field loss: content $q$, provenance $(s,\\kappa)$, or path $p$\n"
        "is lost only if it is encoded in neither $C$ nor a separate retained record.\n"
        "Non-injectivity alone does not prove that all three fields disappear.",
        "#FFF4CC",
        "#D2A62D",
    )

    result_box(
        ax,
        9.4,
        2.0,
        8.0,
        4.0,
        "CONDITIONAL RESULT 4 — Recursive error expectation",
        "$e_{t+1}=\\alpha e_t+\\beta\\varepsilon_t$ with\n"
        "$0\\leq\\alpha<1$, $\\beta\\geq0$, $E[|\\varepsilon_t|]<\\infty$, $E[\\varepsilon_t]=\\mu$\n\n"
        "$E[e_t]=\\alpha^te_0+\\beta\\mu\\dfrac{1-\\alpha^t}{1-\\alpha}$\n"
        "$\\lim_{t\\to\\infty}E[e_t]=\\dfrac{\\beta\\mu}{1-\\alpha}$\n\n"
        "Scope: for $\\alpha=1$, the mean is $e_0+t\\beta\\mu$; no finite-limit claim follows.\n"
        "The scalar recurrence alone does not prove information irreversibility.",
        "#E8F3E5",
        "#659B62",
    )

    ax.text(
        9,
        0.8,
        "SUPPORTED ONLY WHEN THE RELEVANT CONDITIONS CO-OCCUR\n"
        "asymmetric selection + validated feature-space restriction + unretained fields + unvalidated recursive reuse\n"
        "NOT CLAIMED: every multi-agent system excludes truth.  NRA-IDE prevents Effect-Side output from rewriting Cause-Side structural inputs; it does not reconstruct lost truth.",
        ha="center",
        va="center",
        fontsize=11.3,
        fontweight="bold",
        linespacing=1.4,
        bbox=dict(
            boxstyle="round,pad=0.55",
            facecolor="#E7EFF9",
            edgecolor="#6D8EB5",
            linewidth=2.2,
        ),
    )

    fig.subplots_adjust(top=0.91, bottom=0.03, left=0.03, right=0.97)
    fig.savefig(OUTPUT, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(OUTPUT)


if __name__ == "__main__":
    main()
