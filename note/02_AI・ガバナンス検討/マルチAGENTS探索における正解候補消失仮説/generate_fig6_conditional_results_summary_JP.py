from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "Meiryo"
plt.rcParams["axes.unicode_minus"] = False


OUTPUT = Path(__file__).with_name("fig6_conditional_results_summary_v2_JP.png")


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
        "図6. 条件付き数学的結果とその適用範囲",
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
        "条件付き結果1 ― 非対称合意フィルタリング",
        "モデル：2つのサンプリングされた候補は同側ペアの場合のみ残存する；\n"
        "真側と誤り側の実効通過率は $0<a,b\\leq1$ である。\n\n"
        "$p_{t+1}=\\dfrac{ap_t^2}{ap_t^2+b(1-p_t)^2}$，$p_*=\\dfrac{b}{a+b}$\n"
        "$p_0<p_*\\;\\Longrightarrow\\;p_t\\to0$\n\n"
        "適用範囲：これは条件付きの最小写像であり、普遍的な合意法則ではない。\n"
        "真が外れ値であること自体は $a\\ll b$ を意味しない。",
        "#E5F0FA",
        "#5C91C7",
    )

    result_box(
        ax,
        9.4,
        6.6,
        8.0,
        4.2,
        "条件付き結果2 ― 特徴空間からの排除",
        "評価前に $\\phi:\\mathcal{A}\\to V$ を固定・検証し、$x_i=\\phi(A_i)$ とする。\n"
        "$\\mathcal{E}=\\operatorname{span}\\{x_2,\\ldots,x_N\\}\\subseteq V$\n\n"
        "$T\\perp\\mathcal{E}$ かつ $g(x_1,\\ldots,x_N)\\in\\mathcal{E}$\n"
        "$\\Longrightarrow\\;\\langle g(x_1,\\ldots,x_N),T\\rangle_V=0$\n\n"
        "適用範囲：概念的なエージェントのタプルは自動的にベクトルにはならない。\n"
        "特徴写像と内積解釈には別途の根拠が必要である。",
        "#FBE9E9",
        "#C56A6A",
    )

    result_box(
        ax,
        0.6,
        2.0,
        8.0,
        4.0,
        "条件付き結果3 ― 非単射圧縮",
        "$G:\\mathcal{D}\\to\\mathcal{C}$ が非単射である\n"
        "$\\Longrightarrow$ 元の入力 $A$ を全て復元する大域的な左逆写像は存在しない。\n\n"
        "保証される事項：完全な入力は $C=G(A)$ のみから一意に復元できない。\n\n"
        "条件付きフィールド損失：内容 $q$、出所 $(s,\\kappa)$、経路 $p$ のいずれかは、\n"
        "$C$にも別途保持された記録にも符号化されていない場合にのみ失われる。\n"
        "非単射性だけでは、これら3つのフィールドすべてが消失することは証明されない。",
        "#FFF4CC",
        "#D2A62D",
    )

    result_box(
        ax,
        9.4,
        2.0,
        8.0,
        4.0,
        "条件付き結果4 ― 再帰的誤差の期待値",
        "$e_{t+1}=\\alpha e_t+\\beta\\varepsilon_t$ ただし\n"
        "$0\\leq\\alpha<1$，$\\beta\\geq0$，$E[|\\varepsilon_t|]<\\infty$，$E[\\varepsilon_t]=\\mu$\n\n"
        "$E[e_t]=\\alpha^te_0+\\beta\\mu\\dfrac{1-\\alpha^t}{1-\\alpha}$\n"
        "$\\lim_{t\\to\\infty}E[e_t]=\\dfrac{\\beta\\mu}{1-\\alpha}$\n\n"
        "適用範囲：$\\alpha=1$ の場合、平均は $e_0+t\\beta\\mu$ となり、有限極限は成立しない。\n"
        "このスカラー漸化式だけでは情報の不可逆性は証明されない。",
        "#E8F3E5",
        "#659B62",
    )

    ax.text(
        9,
        0.8,
        "関連する条件が同時に成立する場合にのみ支持される\n"
        "非対称選択＋検証済みの特徴空間制限＋未保持フィールド＋未検証の再帰的再利用\n"
        "主張しないこと：全ての多エージェントシステムが真実を排除するわけではない。NRA-IDEはEffect-Side出力がCause-Side構造入力を書き換えることを防ぐものであり、失われた真実を復元するものではない。",
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
