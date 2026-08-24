from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "Meiryo"
plt.rcParams["axes.unicode_minus"] = False


OUTPUT = Path(__file__).with_name("fig4_recursive_error_expectation_v2_JP.png")


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
        "図4. 再帰的な前提汚染と条件付き期待値モデル",
        fontsize=20,
        fontweight="bold",
    )

    ax_flow.set_xlim(0, 16)
    ax_flow.set_ylim(0, 5)
    ax_flow.axis("off")
    flow = [
        (0.3, "Cause-Side\n観測／情報源", "#E6F2E3", "#4C8A48"),
        (3.5, "エージェント推論\n複数候補", "#F7E6E6", "#B85C5C"),
        (6.7, "合意選択\nと圧縮", "#FFF0C9", "#C6951A"),
        (9.9, "境界違反\n型／出所が消去されたまま\n出力が検証済みとして扱われる", "#F9D9C8", "#C55B32"),
        (13.1, "次ラウンド\nで前提が再利用される", "#F2D4D7", "#A94E57"),
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
        "この境界違反は正典的なCause-Side更新ではない。\n"
        "情報構造上の損失は、省略された候補・出所・型・依存経路に起因する。",
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

    ax_plot.plot(rounds, expected, marker="o", linewidth=2.5, label="理論的期待値")
    ax_plot.axhline(limit, color="#D97706", linestyle="--", linewidth=2.5, label=f"極限値 = {limit:.6f}")
    ax_plot.set_xlabel("再帰ラウンド $t$", fontsize=12)
    ax_plot.set_ylabel(r"誤差強度プロキシの期待値 $E[e_t]$", fontsize=12)
    ax_plot.set_title(
        r"具体例：$e_0=0$, $\alpha=0.7$, $\beta=0.15$, $\mu=2/7$",
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
        "期待値曲線のみを示す。乱数試行や信頼区間は含まない。\n"
        "このスカラー漸化式は情報の不可逆性を証明しない。",
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
