# FILE: 04_nisq_fmo_3site.py
# TITLE: 3サイトFMO NISQシミュレーション（植物光合成 拡張版）
# Author: M-Tokuni / Comment: KEN
# Date: 2026-03-28
# 概要：2サイト版から3サイトに拡張。
#       実際のFMO（Fenna-Matthews-Olson）複合体は7サイトだが
#       NISQの現行規模では2〜4サイトが現実的。
#       サイト0 = antenna、サイト2 = reaction center 方向
#       δ2 = 全オフダイアゴナル要素の平均（多サイトコヒーレンス）
#       purpose_mode="plant_quantum" でエネルギー転移を模擬。

import numpy as np
from qutip import basis, Qobj, mesolve, destroy, qeye
import matplotlib.pyplot as plt
from typing import Dict


# ─────────────────────────────────────────────
# 律環公理 量子2重ゆらぎ（3サイト向け・plant_quantum 対応）
# ─────────────────────────────────────────────
def compute_r_quantum(
    delta1_upper: float,
    delta1_lower: float,
    delta2_coherence: float,
    tau_base: float = 1.0,
    lambda_q: float = 0.75,
    eps: float = 1e-9,
    purpose_mode: str = "plant_quantum"
) -> Dict:
    # 動的τ
    r_upper = delta1_upper / (tau_base * (1 + 0.45 * delta1_upper))
    r_lower = delta1_lower / (tau_base * max(0.55, 1 - 0.35 * delta1_lower))
    interference = delta2_coherence ** 2
    r_q = (delta2_coherence + lambda_q * interference) / (tau_base * (1 + 0.35 * delta2_coherence))

    R_quantum = max(r_upper, r_lower, r_q)

    if R_quantum < 1.0 - eps:
        status = "coherence_accumulating"
        action = None
    else:
        status = "phase_jump_generated"
        if purpose_mode == "plant_quantum":
            action = "nutrient_transfer_quantum"   # 光合成エネルギー転移
        elif purpose_mode == "quantum_coherence":
            action = "coherence_collapse"
        else:
            action = "fail_closed"

    return {
        "R_quantum": R_quantum,
        "status":    status,
        "action":    action
    }


# ─────────────────────────────────────────────
# 3サイトFMO NISQシミュレーション
# ─────────────────────────────────────────────
def fmo_3site_nisq_simulation(steps: int = 120, dt: float = 0.08):
    # 3サイトFMOハミルトニアン（文献典型値ベース・2π倍で周波数単位に変換）
    # 対角：各サイトのエネルギー準位（antenna側 > 中間 > reaction center 側）
    # 非対角：サイト間の結合強度
    eps_vals = np.array([200, 0, -200])     # サイトエネルギー [任意スケール]
    V12, V13, V23 = 100, 50, -80           # 結合強度

    H_matrix = np.array([
        [eps_vals[0], V12,         V13],
        [V12,         eps_vals[1], V23],
        [V13,         V23,         eps_vals[2]]
    ])
    H = 2 * np.pi * Qobj(H_matrix)

    # 初期状態：サイト0（antenna側）に励起を集中
    psi0 = basis(3, 0)

    # NISQノイズ：各サイトに振幅減衰・位相減衰を適用
    gamma_relax   = 0.12
    gamma_dephase = 0.28
    c_ops = []
    for i in range(3):
        # 振幅減衰：|i⟩ → 基底状態への遷移（エネルギー散逸）
        c_ops.append(np.sqrt(gamma_relax) * destroy(3) * basis(3, i).dag())
        # 位相減衰：コヒーレンスの消失（dephasing）
        proj = basis(3, i) * basis(3, i).dag()
        c_ops.append(np.sqrt(gamma_dephase) * (proj - qeye(3) / 3))

    results           = []
    coherence_history = []
    R_history         = []

    psi = psi0
    for step in range(steps):
        # 1ステップ時間発展（NISQノイズ込み）
        result = mesolve(H, psi, [0, dt], c_ops, e_ops=[])
        psi    = result.states[-1]

        # δ2：多サイトコヒーレンス（全オフダイアゴナル要素の平均絶対値）
        rho_full = (psi * psi.dag()).full()
        off_diag = sum(
            abs(rho_full[i, j])
            for i in range(3) for j in range(3) if i != j
        )
        delta2_coherence = (2 * off_diag) / 3.0   # 3サイト対応に正規化

        # δ1：デコヒーレンスノイズを古典ゆらぎとして扱う
        delta1_upper = gamma_dephase * (1 + 0.25 * np.random.randn())
        delta1_lower = gamma_relax * 0.75

        # 律環判定（plant_quantum モード）
        state = compute_r_quantum(
            delta1_upper, delta1_lower, delta2_coherence,
            purpose_mode="plant_quantum"
        )

        # 全コヒーレンス量（対角以外の総和）を記録
        coh = sum(
            abs(rho_full[i, j])
            for i in range(3) for j in range(3) if i != j
        )
        coherence_history.append(coh)
        R_history.append(state["R_quantum"])

        results.append({
            "step":      step,
            "coherence": coh,
            "R_quantum": state["R_quantum"],
            "status":    state["status"],
            "action":    state["action"]
        })

        if state["status"] == "phase_jump_generated":
            print(f"【位相跳躍発生！ step={step:3d}】 action={state['action']} | "
                  f"R={state['R_quantum']:.3f} | δ2={delta2_coherence:.3f}")
            # plant_quantum：光合成エネルギー転移を模擬してサイト2（reaction center）に射影
            if state["action"] == "nutrient_transfer_quantum":
                psi = basis(3, 2)

    return results, coherence_history, R_history


# ─────────────────────────────────────────────
# 実行・可視化
# ─────────────────────────────────────────────
if __name__ == "__main__":
    np.random.seed(42)
    sim_results, coh_hist, R_hist = fmo_3site_nisq_simulation(steps=150)

    # ログ表示（15ステップごと）
    for r in sim_results[::15]:
        print(f"step {r['step']:3d} | coh={r['coherence']:.3f} | "
              f"R={r['R_quantum']:.3f} | {r['status']}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(coh_hist, label='Multi-site Coherence (δ₂)', color='#aaff44', lw=2)
    ax1.axhline(0, color='gray', linestyle='--')
    ax1.set_title('3サイトFMO NISQ - 量子コヒーレンス時間発展')
    ax1.set_xlabel('時間ステップ')
    ax1.set_ylabel('Coherence')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(R_hist, label='R_quantum（構造安定度）', color='#ff4060', lw=2)
    ax2.axhline(1.0, color='red', linestyle='--', label='閾値（位相跳躍）')
    ax2.set_title('律環公理監視 - R_quantum（purpose_mode=plant_quantum）')
    ax2.set_xlabel('時間ステップ')
    ax2.set_ylabel('R_quantum')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
