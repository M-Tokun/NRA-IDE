"""NRA-IDE_説明用拡張式体系.md の式を有理数（fractions.Fraction）で検算する。

対象：第1B・1C式、第2A・2B式（および両者の整合）、第3式（累積収支）、第4式（境界到達条件）、
式(2.0)の除去例（9+3 → 8+3）。合成データによる代数の確認であり、物理的妥当性の検証ではない。
"""
from fractions import Fraction as F
import json
import random
import sys

random.seed(20261118)
THETAS = [F(1, 2), F(7, 10), F(9, 10), F(1)]


def rnd(lo, hi):
    return F(random.randint(lo, hi), random.randint(1, 7))


def step(state, theta):
    """状態 (tau, q, p) から次状態を作る。条件を満たさなければ None。"""
    tau0, q0, p0 = state
    tdeg = -rnd(0, 10)
    tcomp = rnd(-10, 10)
    tau = tau0 + tdeg + tcomp
    dq, dp = rnd(-10, 10), rnd(0, 10)
    q, p = q0 + dq, p0 + dp
    if tau <= 0 or q < 0:
        return None
    return (tau, q, p), dq, dp, tdeg, tcomp


counts = {}


def ok(group, cond):
    counts[group] = counts.get(group, 0) + 1
    if not cond:
        raise AssertionError(group)


total = 0
while total < 5000:
    tau0 = rnd(1, 40)
    q0, p0 = rnd(0, 20), rnd(0, 20)
    theta = random.choice(THETAS)
    s0 = (tau0, q0, p0)
    cur = s0
    m_start = theta * tau0 - (q0 + p0)
    sums = [F(0)] * 4
    n_steps = random.randint(1, 5)
    done = 0
    for _ in range(n_steps):
        r = step(cur, theta)
        if r is None:
            break
        nxt, dq, dp, tdeg, tcomp = r
        tau_p, q_p, p_p = cur
        tau, q, p = nxt
        d_p, d = q_p + p_p, q + p
        R_p, R = d_p / tau_p, d / tau
        m_p, m = theta * tau_p - d_p, theta * tau - d
        dtau = tau - tau_p
        ok("1B_margin_definition", m == tau * (theta - R))
        ok("1B_sign_equivalence", (m > 0) == (R < theta) and (m == 0) == (R == theta))
        ok("1C_fixed_comparison", theta * tau - p == m + q)
        ok("2A_ratio_decomposition",
           R - R_p == dq / tau + dp / tau + R_p * (-tdeg) / tau + (-R_p * tcomp / tau))
        ok("2B_margin_decomposition", m - m_p == -dq - dp + theta * tdeg + theta * tcomp)
        ok("2A_2B_consistency", m - m_p == -tau * (R - R_p) + (theta - R_p) * dtau)
        ok("4_boundary_condition_new_direction",
           (R >= theta) == (m_p <= (d - d_p) - theta * dtau))
        ok("4_boundary_condition_expanded",
           (m <= 0) == (m_p <= dq + dp - theta * tdeg - theta * tcomp))
        sums = [sums[0] + dq, sums[1] + dp, sums[2] + tdeg, sums[3] + tcomp]
        cur = nxt
        done += 1
        total += 1
    if done:
        tau, q, p = cur
        m_n = theta * tau - (q + p)
        ok("3_cumulative_balance",
           m_n == m_start - sums[0] - sums[1] + theta * sums[2] + theta * sums[3])

# 式(2.0) 除去例：Comp_tau = 和、要素0が9->8、要素1(3)を傷みなく除去（除去した回の値 3 を中間項に入れる）
tau_prev = F(9) + F(3)
mid = F(8) + F(3)
tau_now = F(8)
ok("2.0_removal_example_deg", mid - tau_prev == -1)
ok("2.0_removal_example_comp", tau_now - mid == -3)
ok("2.0_removal_example_sum", (mid - tau_prev) + (tau_now - mid) == tau_now - tau_prev)

# R_{n-1}=0（無負荷）で器だけが劣化：2Aの劣化縮小項は0、2Bの寄与は theta*dtau_deg
theta = F(7, 10)
tau_p, tau = F(10), F(8)
m_p, m = theta * tau_p, theta * tau
ok("idle_degradation_2A_zero", F(0) - F(0) == F(0) * (tau_p - tau) / tau)
ok("idle_degradation_2B_margin", m - m_p == theta * (tau - tau_p))

result = {"kind": "exact_algebra_checks_on_synthetic_data", "all_passed": True,
          "total_checks": sum(counts.values()), "checks_by_group": counts,
          "physical_validation": "not_performed", "canonical_adoption": "not_claimed"}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0)
