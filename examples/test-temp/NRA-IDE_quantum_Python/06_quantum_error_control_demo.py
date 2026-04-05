# FILE: 06_quantum_error_control_demo.py
# TITLE: 量子誤差制御デモ（R_quantumによるリアルタイム構造監視）
# Author: M-Tokuni / Comment: KEN
# Date: 2026-03-28
# 概要：従来の量子誤差訂正（QEC）は「誤差が出てから修正する」事後処理。
#       律環公理は「誤差が爆発する前に構造破断を検知して環を閉じる」事前制御。
#       ただし注意：このコードはまだ「誤差を出さないようにする」方向の実装。
#       →「遊び幅の中のゆらぎを追跡する」思想への移行は次フェーズ（07以降）。
#       NISQノイズを強めに設定し、R_quantum ≥ 1.0 で即座に安全リセットする。

import numpy as np
from qutip import basis, Qobj, mesolve, destroy, qeye
from typing import Dict, List


# ─────────────────────────────────────────────
# 律環公理 量子誤差制御用2重ゆらぎ
# purpose_mode="quantum_error_control" のみ定義
# ─────────────────────────────────────────────
def compute_r_quantum(
    delta1_upper: float,
    delta1_lower: float,
    delta2_coherence: float,
    tau_base: float = 1.0,
    lambda_q: float = 0.75,
    eps: float = 1e-9,
    purpose_mode: str = "quantum_error_control"
) -> Dict:
    # 動的τ（NISQの現実的なノイズ強度に合わせて係数を調整）
    r_upper = delta1_upper / (tau_base * (1 + 0.45 * delta1_upper))
    r_lower = delta1_lower / (tau_base * max(0.55, 1 - 0.35 * delta1_lower))
    interference = delta2_coherence ** 2
    r_q = (delta2_coherence + lambda_q * interference) / (tau_base * (1 + 0.35 * delta2_coherence))

    R_quantum = max(r_upper, r_lower, r_q)

    if R_quantum < 1.0 - eps:
        # 閾値内：コヒーレンス維持中
        return {"R_quantum": R_quantum, "status": "coherence_accumulating", "action": None}
    else:
        # 閾値超過：purpose_mode に応じた制御行動
        action = "error_controlled_reset" if purpose_mode == "quantum_error_control" else "fail_closed"
        return {"R_quantum": R_quantum, "status": "phase_jump_generated", "action": action}


# ─────────────────────────────────────────────
# 量子誤差制御デモ（3サイトFMO・ノイズ強め設定）
# ─────────────────────────────────────────────
def quantum_error_control_demo(steps: int = 120, dt: float = 0.08):
    # 3サイトFMOハミルトニアン
    H = 2 * np.pi * Qobj([[200, 100,  50],
                           [100,   0, -80],
                           [ 50, -80, -200]])

    # 初期状態：antenna サイト
    psi = basis(3, 0)

    # NISQノイズ：意図的に強めに設定して誤差制御が頻繁に発動するようにする
    gamma_relax   = 0.18   # 通常より強い振幅減衰
    gamma_dephase = 0.32   # 通常より強い位相減衰
    c_ops = []
    for i in range(3):
        c_ops.append(np.sqrt(gamma_relax)   * destroy(3) * basis(3, i).dag())
        proj = basis(3, i) * basis(3, i).dag()
        c_ops.append(np.sqrt(gamma_dephase) * (proj - qeye(3) / 3))

    path_log: List[Dict] = []
    np.random.seed(42)
    control_events = 0   # 誤差制御発動回数カウンタ

    for step in range(steps):
        # 1ステップ時間発展（強ノイズ込み）
        result = mesolve(H, psi, [0, dt], c_ops, e_ops=[])
        psi    = result.states[-1]

        # δ2：多サイトコヒーレンス
        rho_full = (psi * psi.dag()).full()
        off_diag = sum(
            abs(rho_full[i, j])
            for i in range(3) for j in range(3) if i != j
        )
        delta2 = (2 * off_diag) / 3.0

        # δ1：強ノイズ環境を反映した古典ゆらぎ
        delta1_upper = gamma_dephase * (1 + 0.3 * np.random.randn())
        delta1_lower = gamma_relax * 0.9

        # 律環判定（quantum_error_control モード）
        state = compute_r_quantum(delta1_upper, delta1_lower, delta2,
                                  purpose_mode="quantum_error_control")

        # 経路ログ記録
        path_log.append({
            "step":         step,
            "δ1_upper":     round(delta1_upper, 5),
            "δ1_lower":     round(delta1_lower, 5),
            "δ2_coherence": round(delta2, 5),
            "R_quantum":    round(state["R_quantum"], 5),
            "status":       state["status"],
            "action":       state["action"]
        })

        if state["status"] == "phase_jump_generated":
            control_events += 1
            # error_controlled_reset：安全リセット（antenna 側に戻す）
            # ここが従来QECの「事後訂正」ではなく「構造閾値到達時の即時制御」
            psi = basis(3, 0)
            print(f"【量子誤差制御発動！ step={step:3d}】 R={state['R_quantum']:.4f} → リセット")

    return path_log, control_events


# ─────────────────────────────────────────────
# 実行
# ─────────────────────────────────────────────
if __name__ == "__main__":
    log, events = quantum_error_control_demo()

    print(f"\n=== 量子誤差制御 結果 ===")
    print(f"制御発動回数: {events} 回（{len(log)} ステップ中）")
    print(f"発動率: {events / len(log) * 100:.1f}%")

    print("\n最初の15ステップの経路ログ:")
    print(f"{'step':>4} | {'δ1_upper':>9} | {'δ1_lower':>9} | "
          f"{'δ2_coh':>8} | {'R_quantum':>9} | status (action)")
    print("-" * 75)
    for entry in log[:15]:
        print(
            f"{entry['step']:4d} | "
            f"{entry['δ1_upper']:9.4f} | "
            f"{entry['δ1_lower']:9.4f} | "
            f"{entry['δ2_coherence']:8.4f} | "
            f"{entry['R_quantum']:9.4f} | "
            f"{entry['status']} ({entry['action']})"
        )

    print("\n【設計上の注意】")
    print("このコードは「誤差が広がる前にリセット」という方向性（力技寄り）。")
    print("本来の律環思想は「τの中でδがどう動いたかを追跡する」こと。")
    print("→ 05_fmo_fluctuation_path_log.py が思想的により正確な実装。")
