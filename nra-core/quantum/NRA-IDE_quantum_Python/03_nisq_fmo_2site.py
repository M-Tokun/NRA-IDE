# FILE: 03_nisq_fmo_2site.py
# TITLE: 2サイトFMO NISQシミュレーション（光合成光収穫複合体 簡易版）
# Author: M-Tokuni / Comment: KEN
# Date: 2026-03-28
# 概要：植物の光合成における量子コヒーレンス（励起エネルギー伝達）を
#       最小構成（2サイト）で模擬する。
#       サイト0 = antenna（光を受ける側）
#       サイト1 = reaction center 方向（エネルギー転移先）
#       NISQノイズ（振幅減衰・位相減衰）を入れた現実的な設定。

import numpy as np
from qutip import basis, Qobj, mesolve, expect, destroy, sigmaz, sigmay
import matplotlib.pyplot as plt
from typing import Dict


# ─────────────────────────────────────────────
# 律環公理 量子2重ゆらぎ（NISQ版）
# EMAを省略し直近値で近似（軽量・高速評価用）
# ─────────────────────────────────────────────
def compute_r_quantum(
    delta1_upper: float,
    delta1_lower: float,
    delta2_coherence: float,
    tau_base: float = 1.0,
    lambda_q: float = 0.7,
    eps: float = 1e-9,
    purpose_mode: str = "quantum_coherence"
) -> Dict:
    # 動的τ（簡易版）
    r_upper = delta1_upper / (tau_base * (1 + 0.4 * delta1_upper))
    r_lower = delta1_lower / (tau_base * max(0.6, 1 - 0.3 * delta1_lower))

    # 量子干渉項（δ2の2乗）
    interference = delta2_coherence ** 2
    r_q = (delta2_coherence + lambda_q * interference) / (tau_base * (1 + 0.3 * delta2_coherence))

    R_quantum = max(r_upper, r_lower, r_q)

    if R_quantum < 1.0 - eps:
        status = "coherence_accumulating"
        action = None
    else:
        status = "phase_jump_generated"
        # purpose_mode で跳躍時の行動を切り替える
        if purpose_mode == "quantum_coherence":
            action = "coherence_collapse"          # 重ね合わせ崩壊
        elif purpose_mode == "plant_quantum":
            action = "nutrient_transfer_quantum"   # 植物エネルギー転移
        else:
            action = "fail_closed"

    return {
        "R_quantum": R_quantum,
        "status":    status,
        "action":    action
    }


# ─────────────────────────────────────────────
# 2サイトFMO NISQシミュレーション
# ─────────────────────────────────────────────
def nisq_fmo_simulation(steps: int = 50, dt: float = 0.1):
    # 2サイトハミルトニアン（結合項のみのシンプル版）
    H = 2 * np.pi * Qobj([[0.0, 1.0],
                           [1.0, 0.0]])

    # 初期状態：重ね合わせ（antenna側とreaction center側が均等）
    psi0 = (basis(2, 0) + basis(2, 1)).unit()

    # NISQノイズ：現実のデバイスに近い緩和率・脱相率を設定
    gamma_relax   = 0.15   # 振幅減衰（エネルギー散逸）
    gamma_dephase = 0.25   # 位相減衰（コヒーレンス消失）

    # Lindblad 演算子（ノイズのモデル）
    c_ops = [
        np.sqrt(gamma_relax)       * destroy(2),   # 振幅減衰
        np.sqrt(2 * gamma_dephase) * sigmaz()       # 位相減衰
    ]

    results           = []
    coherence_history = []
    R_history         = []

    psi = psi0
    for step in range(steps):
        # qutip で1ステップ時間発展（ノイズ込み）
        result = mesolve(H, psi, [0, dt], c_ops, e_ops=[expect(sigmaz())])
        psi    = result.states[-1]

        # δ2：密度行列のオフダイアゴナル要素（コヒーレンス強度）
        rho = psi * psi.dag()
        delta2_coherence = abs(rho.full()[0, 1]) * 2.0   # [0,1] 要素 × 2 で正規化

        # δ1：デコヒーレンスノイズ強度を古典ゆらぎとして使用
        delta1_upper = gamma_dephase * (1 + 0.2 * np.random.randn())
        delta1_lower = gamma_relax * 0.8

        # 律環判定
        state = compute_r_quantum(
            delta1_upper, delta1_lower, delta2_coherence,
            purpose_mode="quantum_coherence"
        )

        # sigmay の期待値をコヒーレンス指標として記録
        coherence = abs(expect(sigmay(), psi))
        coherence_history.append(coherence)
        R_history.append(state["R_quantum"])

        results.append({
            "step":      step,
            "coherence": coherence,
            "R_quantum": state["R_quantum"],
            "status":    state["status"],
            "action":    state["action"]
        })

        if state["status"] == "phase_jump_generated":
            print(f"【位相跳躍発生！ step={step}】 action={state['action']} | R={state['R_quantum']:.3f}")
            # coherence_collapse：測定崩壊を模擬してsite0（antenna）に射影
            if state["action"] == "coherence_collapse":
                psi = basis(2, 0)

    return results, coherence_history, R_history


# ─────────────────────────────────────────────
# 実行・可視化
# ─────────────────────────────────────────────
if __name__ == "__main__":
    np.random.seed(42)
    sim_results, coh_hist, R_hist = nisq_fmo_simulation(steps=80)

    # ログ表示（10ステップごと）
    for r in sim_results[::10]:
        print(f"step {r['step']:2d} | coh={r['coherence']:.3f} | "
              f"R={r['R_quantum']:.3f} | {r['status']}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(coh_hist, label='Quantum Coherence (δ₂)', color='#aaff44')
    ax1.axhline(0, color='gray', linestyle='--')
    ax1.set_title('2サイトFMO NISQ - コヒーレンス時間発展')
    ax1.set_xlabel('時間ステップ')
    ax1.set_ylabel('Coherence')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(R_hist, label='R_quantum（構造安定度）', color='#ff4060')
    ax2.axhline(1.0, color='red', linestyle='--', label='閾値（位相跳躍）')
    ax2.set_title('律環公理監視 - R_quantum')
    ax2.set_xlabel('時間ステップ')
    ax2.set_ylabel('R_quantum')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
