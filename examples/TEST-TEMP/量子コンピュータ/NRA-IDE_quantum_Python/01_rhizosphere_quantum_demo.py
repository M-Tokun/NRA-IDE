# FILE: 01_rhizosphere_quantum_demo.py
# TITLE: 単層根圏量子シミュレーション（律環公理 2重ゆらぎ量子拡張）
# Author: M-Tokuni / Comment: KEN
# Date: 2026-03-28

import numpy as np
from qutip import basis, sigmaz, sigmax, mesolve, expect
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# 律環公理 量子2重ゆらぎ計算関数
# 入力: δ1(古典ゆらぎ上下)、δ2(量子コヒーレンス)
# 出力: R_quantum と状態判定（蓄積中・位相跳躍・遷移帯）
# ─────────────────────────────────────────────
def compute_quantum_dual_fluctuation(
    delta1_upper, delta1_lower, delta2_coherence,
    tau_base=1.0, lambda_q=0.8, eps=1e-9, R_op=1.2,
    ema_upper=0.0, ema_lower=0.0, ema_q=0.0,
    alpha_u=0.3, alpha_l=0.3, alpha_q=0.2
):
    # EMA（指数移動平均）で単発ノイズを平滑化。過去のゆらぎを記憶する
    ema_upper = alpha_u * delta1_upper + (1 - alpha_u) * ema_upper
    ema_lower = alpha_l * delta1_lower + (1 - alpha_l) * ema_lower
    ema_q     = alpha_q * delta2_coherence + (1 - alpha_q) * ema_q

    # 動的τ：拡大ストレスは厚みを増やし、縮小ストレスには敏感になる（非対称）
    tau_upper = tau_base * (1 + 0.5 * ema_upper)
    tau_lower = tau_base * max(0.5, 1 - 0.3 * ema_lower)
    tau_q     = tau_base * (1 + 0.4 * ema_q)

    # 量子干渉項：コヒーレンスの2乗で近似
    interference = delta2_coherence ** 2

    # R_quantum = max(上側, 下側, 量子層) で非対称に判定
    r_upper = delta1_upper / tau_upper
    r_lower = delta1_lower / tau_lower
    r_q     = (delta2_coherence + lambda_q * interference) / tau_q
    R_quantum = max(r_upper, r_lower, r_q)

    # 脱進機型状態判定
    if R_quantum < 1.0 - eps:
        # τ内に収まっている → コヒーレンス蓄積継続
        status = "coherence_accumulating"
        delta_next = {"delta1_upper": delta1_upper + 0.01, "delta2": delta2_coherence}
    elif R_quantum >= 1.0:
        # τを超えた → 位相跳躍（エネルギー転移）発生、δをリセット
        status = "phase_jump_generated"
        delta_next = {"delta1_upper": 0.0, "delta2": 0.0}
    else:
        # 遷移帯（transition band）
        status = "transition_band"
        delta_next = {"delta1_upper": max(0, delta1_upper - tau_upper), "delta2": delta2_coherence}

    return {
        "R_quantum": R_quantum,
        "status": status,
        "ema_upper": ema_upper,
        "ema_lower": ema_lower,
        "ema_q": ema_q,
        "delta_next": delta_next
    }


# ─────────────────────────────────────────────
# qutip を使った根圏1層シミュレーション
# 対象：根圏バクテリアの量子コヒーレンス（2レベル系）
#       δ2 = 量子重ね合わせ強度、δ1 = 土壌環境ゆらぎ
# ─────────────────────────────────────────────
def simulate_rhizosphere_quantum_layer(steps=20, dt=0.1):
    # 初期量子状態：基底状態 |0⟩（未励起）
    psi0 = basis(2, 0)

    # ハミルトニアン：sigmax でRabi振動（量子コヒーレンス駆動）
    H0 = 2 * np.pi * sigmax()

    # 時間依存ノイズ：土壌ゆらぎ（δ1）をsigmazで古典ノイズとして重畳
    def H_t(t, args):
        noise = args['delta1'] * np.sin(2 * np.pi * t)
        return H0 + noise * sigmaz()

    results = []
    ema_u, ema_l, ema_q = 0.0, 0.0, 0.0
    delta1_upper, delta1_lower, delta2 = 0.1, 0.05, 0.3  # 初期ゆらぎ値

    for step in range(steps):
        # 1ステップ時間発展（ノイズあり）
        args = {'delta1': delta1_upper}
        result = mesolve(H_t, psi0, [0, dt], [], e_ops=[expect(sigmaz())], args=args)

        # δ2：基底状態との重なり合いをコヒーレンス強度として抽出
        coherence = abs(result.states[-1].overlap(basis(2, 0))) ** 2

        # δ1 更新：土壌・肥料・微生物拮抗を乱数で模擬
        delta1_upper += 0.02 * np.random.randn()
        delta1_lower += 0.01 * np.random.randn()
        delta2 = coherence + 0.05 * np.random.randn()

        # 律環公理で構造安定度を評価
        state = compute_quantum_dual_fluctuation(
            delta1_upper, delta1_lower, delta2,
            ema_upper=ema_u, ema_lower=ema_l, ema_q=ema_q
        )
        ema_u, ema_l, ema_q = state["ema_upper"], state["ema_lower"], state["ema_q"]

        results.append({
            "step": step,
            "coherence": coherence,
            "R_quantum": state["R_quantum"],
            "status": state["status"]
        })

        if state["status"] == "phase_jump_generated":
            # 位相跳躍：微生物→根へのエネルギー転移を模擬してリセット
            psi0 = basis(2, 0)
            print(f"【位相跳躍発生！ step={step}】 微生物→根への情報/エネルギー転移")
        else:
            psi0 = result.states[-1]

    return results


# ─────────────────────────────────────────────
# 実行・可視化
# ─────────────────────────────────────────────
if __name__ == "__main__":
    np.random.seed(42)
    sim_results = simulate_rhizosphere_quantum_layer(steps=30)

    # ログ表示
    for r in sim_results:
        print(f"step {r['step']:2d} | coherence={r['coherence']:.3f} | "
              f"R={r['R_quantum']:.3f} | status={r['status']}")

    # グラフ：R_quantum とコヒーレンスの時系列
    steps      = [r['step']      for r in sim_results]
    Rs         = [r['R_quantum'] for r in sim_results]
    coherences = [r['coherence'] for r in sim_results]

    plt.plot(steps, Rs,         label='R_quantum (構造安定度)')
    plt.plot(steps, coherences, label='量子コヒーレンス (δ₂)')
    plt.axhline(1.0, color='r', linestyle='--', label='位相跳躍閾値')
    plt.xlabel('時間ステップ（根圏ストレス蓄積）')
    plt.ylabel('値')
    plt.title('律環公理 × qutip 根圏微生物量子層シミュレーション（単層）')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
