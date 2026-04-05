# FILE: 05_fmo_fluctuation_path_log.py
# TITLE: 経路ログ専用版（最終量子状態は不要・δ/Rの軌跡のみ出力）
# Author: M-Tokuni / Comment: KEN
# Date: 2026-03-28
# 概要：「結果よりも経路が重要」という律環思想の直接的な実装。
#       量子状態（psi の最終値）は一切保存しない。
#       保存するのは、各ステップの δ1, δ2, R_quantum, status のみ。
#       この経路ログが「性質誤差の追跡痕」であり、
#       追跡できれば誤差ではなく「正しい状態記述」になる。

import numpy as np
from qutip import basis, Qobj, mesolve, destroy, qeye
from typing import Dict, List


# ─────────────────────────────────────────────
# 律環公理 量子2重ゆらぎ（経路ログ専用・軽量版）
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
    r_upper = delta1_upper / (tau_base * (1 + 0.45 * delta1_upper))
    r_lower = delta1_lower / (tau_base * max(0.55, 1 - 0.35 * delta1_lower))
    interference = delta2_coherence ** 2
    r_q = (delta2_coherence + lambda_q * interference) / (tau_base * (1 + 0.35 * delta2_coherence))

    R_quantum = max(r_upper, r_lower, r_q)

    if R_quantum < 1.0 - eps:
        status = "coherence_accumulating"
        action = "none"
    else:
        status = "phase_jump_generated"
        action = "nutrient_transfer_quantum" if purpose_mode == "plant_quantum" else "coherence_collapse"

    return {"R_quantum": R_quantum, "status": status, "action": action}


# ─────────────────────────────────────────────
# 経路ログ生成（3サイトFMO、結果なし・δ/Rのみ保存）
# ─────────────────────────────────────────────
def fmo_3site_fluctuation_path_log(steps: int = 120, dt: float = 0.08) -> List[Dict]:
    # 3サイトFMOハミルトニアン
    H = 2 * np.pi * Qobj([[200, 100,  50],
                           [100,   0, -80],
                           [ 50, -80, -200]])

    # 初期状態：antenna サイト
    psi = basis(3, 0)

    # NISQノイズ
    gamma_relax   = 0.12
    gamma_dephase = 0.28
    c_ops = []
    for i in range(3):
        c_ops.append(np.sqrt(gamma_relax)   * destroy(3) * basis(3, i).dag())
        proj = basis(3, i) * basis(3, i).dag()
        c_ops.append(np.sqrt(gamma_dephase) * (proj - qeye(3) / 3))

    path_log: List[Dict] = []
    np.random.seed(42)

    for step in range(steps):
        # 量子時間発展
        result = mesolve(H, psi, [0, dt], c_ops, e_ops=[])
        psi    = result.states[-1]

        # δ2：多サイトコヒーレンス（経路追跡の核）
        rho_full = (psi * psi.dag()).full()
        off_diag = sum(
            abs(rho_full[i, j])
            for i in range(3) for j in range(3) if i != j
        )
        delta2 = (2 * off_diag) / 3.0

        # δ1：古典環境ゆらぎ
        delta1_upper = gamma_dephase * (1 + 0.25 * np.random.randn())
        delta1_lower = gamma_relax * 0.75

        # 律環判定
        state = compute_r_quantum(delta1_upper, delta1_lower, delta2)

        # ── 経路ログに記録（最終状態は保存しない） ──
        log_entry = {
            "step":           step,
            "δ1_upper":       round(delta1_upper, 6),
            "δ1_lower":       round(delta1_lower, 6),
            "δ2_coherence":   round(delta2, 6),
            "R_quantum":      round(state["R_quantum"], 6),
            "status":         state["status"],
            "action":         state["action"]
        }
        path_log.append(log_entry)

        # 位相跳躍時のみリセット（それ以外は psi を引き継ぐ）
        if state["status"] == "phase_jump_generated":
            psi = basis(3, 0)   # antenna 側に戻す（エネルギー転移後の再励起模擬）

    return path_log


# ─────────────────────────────────────────────
# 実行（ログのみ出力・グラフなし）
# ─────────────────────────────────────────────
if __name__ == "__main__":
    log = fmo_3site_fluctuation_path_log(steps=80)

    print("=== ゆらぎ誤差 経路ログ（最終量子状態は保存していません） ===")
    print(f"{'step':>4} | {'δ1_upper':>9} | {'δ1_lower':>9} | "
          f"{'δ2_coh':>8} | {'R_quantum':>9} | status (action)")
    print("-" * 80)
    for entry in log:
        print(
            f"{entry['step']:4d} | "
            f"{entry['δ1_upper']:9.5f} | "
            f"{entry['δ1_lower']:9.5f} | "
            f"{entry['δ2_coherence']:8.5f} | "
            f"{entry['R_quantum']:9.5f} | "
            f"{entry['status']} ({entry['action']})"
        )

    # JSON形式での保存例
    import json
    with open("path_log_output.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print("\n→ path_log_output.json に全ログを保存しました。")
    print("  このファイルが「性質誤差の追跡痕」であり、6D Visualizerへの入力になります。")
