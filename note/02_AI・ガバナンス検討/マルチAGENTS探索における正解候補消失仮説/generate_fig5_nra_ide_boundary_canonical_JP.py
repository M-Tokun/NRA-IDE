from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "Meiryo"
plt.rcParams["axes.unicode_minus"] = False


OUTPUT = Path(__file__).with_name("fig5_nra_ide_boundary_canonical_v2_JP.png")


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
        "図5. NRA-IDE正典的境界：構造的入力・状態・権限",
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
        "CAUSE-SIDE 入力権限\n\n直接観測\n事前固定された変換規則\n宣言された対象／単位／時刻／情報源\n認可された更新経路とスナップショット",
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
        "NRA-IDE 正典的評価\n\n$R=\\delta/\\tau$\n\n$0\\leq R<R_{warn}$ : PERMIT\n$R_{warn}\\leq R<R_{handoff}$ : BOUNDARY_WARNING\n$R_{handoff}\\leq R<R_{irrev}$ : HANDOFF_REQUIRED\n$R_{irrev}\\leq R<1$ : IRREVERSIBLE_TRANSITION\n$R\\geq1$ : RUPTURE_BOUNDARY\n\n入力例外\n$\\tau=0$ : OUT_OF_DESCRIPTION_DOMAIN\nunknown／invalid／non-finite : CONFESSION",
        "#FFF3CD",
        "#C99700",
        fontsize=9.2,
        weight="bold",
    )
    arrow(ax, (4.8, 7.3), (5.8, 7.3), "")
    ax.text(5.3, 7.55, "有効な構造的入力のみ", ha="center", fontsize=10)

    # Effect-Side remains outside structural-input authority.
    box(
        ax,
        11.3,
        5.7,
        4.3,
        3.2,
        "EFFECT-SIDE 生成物\n\nマルチエージェント合意\n推論出力\n合成／生成データ\n自己整合性フィルタ\n過去の生成出力",
        "#FDECEC",
        "#D05C5C",
        fontsize=11,
        weight="bold",
    )
    arrow(ax, (10.4, 7.8), (11.3, 7.8), "")
    ax.text(10.85, 8.05, "スナップショットへの読み取り専用アクセス", ha="center", fontsize=10)

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
        "禁止される逆方向入力\n$\\delta$、$\\tau$、$R$、閾値、状態、ラッチのいずれも更新しない",
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
        "生存チャネル\n\n観測状態\nロギング状態\n通信状態\n監査系譜",
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
        "境界出力\n\n対象状態\n実行権限\n証言モード\n不可逆ラッチ状態",
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
        "フェイルクローズド\n運用原則\n\n未認可の自律処理を抑止する；\n観測・ログ・証言は消去しない",
        "#F3E5F5",
        "#8E5AA9",
        fontsize=10.5,
        weight="bold",
    )
    arrow(ax, (8.1, 4.8), (8.1, 4.2), "")
    ax.text(8.1, 4.48, "分類と権限制御", ha="center", fontsize=9.5)
    arrow(ax, (10.4, 3.1), (11.3, 3.1), "運用上の効果")

    ax.text(
        8,
        0.8,
        "新しい認可されたCause-Side観測は、次のスナップショットを更新しうる；検証はAI出力を再入力しない。\n"
        "$R$は構造的境界の分類と実行権限を制御するものであり、真実の復元や$p_t$の回復を行うものではない。",
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
