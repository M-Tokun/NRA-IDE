from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Meiryo"
plt.rcParams["axes.unicode_minus"] = False


OUTPUT = Path(__file__).with_name("fig1_asymmetric_filter_readable_v2_JP.png")


def update(p, truth_pass, error_pass):
    truth_mass = truth_pass * p**2
    error_mass = error_pass * (1 - p) ** 2
    return truth_mass / (truth_mass + error_mass)


def trajectory(p0, truth_pass, error_pass, rounds):
    values = [p0]
    for _ in range(rounds):
        values.append(update(values[-1], truth_pass, error_pass))
    return np.asarray(values)


def main():
    truth_pass = 0.05
    error_pass = 0.95
    threshold = error_pass / (truth_pass + error_pass)
    rounds = 8
    initial_values = [0.10, 0.40, 0.80, 0.90, 0.95, 0.97]

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(18, 7.5))
    fig.suptitle(
        "図1. 明示的な二標本モデルにおける非対称合意フィルタリング",
        fontsize=21,
        fontweight="bold",
        y=0.98,
    )

    generations = np.arange(rounds + 1)
    for p0 in initial_values:
        values = trajectory(p0, truth_pass, error_pass, rounds)
        width = 3.0 if p0 in (0.90, 0.95, 0.97) else 2.0
        ax_left.plot(
            generations,
            values,
            marker="o",
            linewidth=width,
            markersize=5,
            label=f"$p_0={p0:.2f}$",
        )

    ax_left.axhline(
        threshold,
        color="black",
        linestyle="--",
        linewidth=2,
        label=f"不安定固定点 $p_*={threshold:.2f}$",
    )
    ax_left.set_xlim(0, rounds)
    ax_left.set_ylim(-0.02, 1.02)
    ax_left.set_xlabel("世代 $t$", fontsize=13)
    ax_left.set_ylabel("真の候補の残存割合 $p_t$", fontsize=13)
    ax_left.set_title(
        "$a=0.05$, $b=0.95$：両方の吸引域が線形スケールで確認できる",
        fontsize=14,
        pad=12,
    )
    ax_left.grid(True, alpha=0.3)
    ax_left.legend(loc="center left", fontsize=10, framealpha=0.95)
    ax_left.text(
        4.15,
        0.29,
        "$p_0=0.90$:\n$0.90\\to0.81\\to0.4889\\to0.04595$\n$\\to1.22\\times10^{-4}\\to0$",
        fontsize=10.5,
        ha="left",
        va="center",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#777777", alpha=0.95),
    )

    a_values = np.linspace(0.01, 1.0, 240)
    b_values = np.linspace(0.01, 1.0, 240)
    a_grid, b_grid = np.meshgrid(a_values, b_values)
    boundary = b_grid / (a_grid + b_grid)
    levels = np.linspace(0, 1, 11)
    contour = ax_right.contourf(
        a_grid,
        b_grid,
        boundary,
        levels=levels,
        cmap="viridis",
        vmin=0,
        vmax=1,
    )
    ax_right.scatter(
        [truth_pass],
        [error_pass],
        s=130,
        color="#D62728",
        edgecolor="white",
        linewidth=1.5,
        zorder=3,
        label="例 $(a,b)=(0.05,0.95)$",
    )
    ax_right.set_xlabel("真側の実効通過率 $a$", fontsize=13)
    ax_right.set_ylabel("誤り側の実効通過率 $b$", fontsize=13)
    ax_right.set_title(
        "本モデルにおける崩壊境界 $p_*=b/(a+b)$",
        fontsize=14,
        pad=12,
    )
    ax_right.legend(loc="upper right", fontsize=10, framealpha=0.95)
    colorbar = fig.colorbar(contour, ax=ax_right, fraction=0.046, pad=0.04)
    colorbar.set_label("不安定固定点 $p_*$", fontsize=12)

    fig.text(
        0.5,
        0.02,
        "モデルの前提：独立な二候補サンプリング、同側ペアのみを率$a$と$b$で残存させ、異側ペアは破棄した後に再正規化する。"
        "外れ値であること自体は$a/b$を決定しない。",
        ha="center",
        va="bottom",
        fontsize=11.5,
        fontweight="bold",
    )
    fig.subplots_adjust(top=0.87, bottom=0.12, left=0.07, right=0.94, wspace=0.23)
    fig.savefig(OUTPUT, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(OUTPUT)


if __name__ == "__main__":
    main()
