from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "Meiryo"
plt.rcParams["axes.unicode_minus"] = False


OUTPUT = Path(__file__).with_name("fig3_noninjective_compression_conditional_v2_JP.png")


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
        "図3. 非単射な合意圧縮：保証される帰結と条件付きの帰結",
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
        "構造化されたエージェント状態\n\n$A=(A_1,\\ldots,A_N)$\n内容 $q$ ｜ 出所 $s$\n推論経路 $p$ ｜ 認識論的型 $\\kappa$",
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
        "合意／圧縮\n\n$G:\\mathcal{D}\\rightarrow\\mathcal{C}$\n$C=G(A)$\n\n$A\\ne A'$ かつ $G(A)=G(A')$ のとき非単射",
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
        "非単射性により\n保証される事項\n\n少なくとも2つの異なる入力が同一の$C$を共有する\nすべての$A$を復元する大域的な左逆写像は存在しない",
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
        "非単射性は、どの意味的フィールドが省略されたかを特定しない。\n保存された出力と、それとは別の全ての保持経路を監査すること。",
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
        "条件付き内容の損失\n\n候補内容$q$が$C$にも\n保持記録にも符号化されていない場合、\n元の候補は下流で利用できなくなる。",
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
        "条件付き出所の損失\n\n出所$s$と型$\\kappa$が$C$にも\n保持記録にも符号化されていない場合、\n起源と認識論的型は復元できない。",
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
        "条件付き構造の損失\n\n依存経路$p$が$C$にも\n保持記録にも符号化されていない場合、\n元の裏付け経路は復元できない。",
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
        "厳密な結論：$G$が非単射であることは、完全な入力を一意に復元できないことを証明する。\n"
        "特定の内容・出所・経路の損失を主張するには、当該フィールドが他の場所に保持されていないという証拠が必要である。",
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
