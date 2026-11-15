# 開放系 R 増分分解 論文草案の数値例の検算（デモ用の値。実測値ではない）
# 実行: python nra-core/foundations/open_system_R_decomposition_check_20261116.py
from fractions import Fraction as F


def state(q, p, taus):
    """Comp_tau は和（デモ用の宣言）。"""
    tau = sum(taus)
    delta = q + p
    return delta, tau, delta / tau


# n-1 : 要素1つ, tau0=10, lambda=0.1
tau0 = F(10)
q0, p0, lam0 = F(2), F(1), F(1, 10)
d0, t0, R0 = state(q0, p0, [(1 - lam0) * tau0])

# n : dq=+1.5, dp=+0.5, dlambda=+0.1（構成は不変）
dq, dp, dlam = F(3, 2), F(1, 2), F(1, 10)
q1, p1, lam1 = q0 + dq, p0 + dp, lam0 + dlam
d1, t1, R1 = state(q1, p1, [(1 - lam1) * tau0])

t_wear = (1 - lam1) * tau0          # 構成を n-1 のままにした厚み
d_tau_wear = t_wear - t0            # <= 0
d_tau_comp = t1 - t_wear            # 構成変化分（ここでは 0）

terms1 = [dq / t1, dp / t1, R0 * (-d_tau_wear) / t1, -R0 * d_tau_comp / t1]
assert sum(terms1) == R1 - R0, "増分分解が一致しない"
assert p1 / t1 + q1 / t1 == R1, "R = R_rev + R_res が一致しない"

thetas = {"warn": F(1, 2), "handoff": F(7, 10), "irrev": F(9, 10), "rupture": F(1)}
margins1 = {k: th * t1 - d1 for k, th in thetas.items()}

# 余白の同値: d_delta - theta*d_tau >= m_theta  <=>  R_next >= theta
for th in thetas.values():
    m = th * t1 - d1
    for dd in [F(0), F(1, 2), F(1), F(3)]:
        for dt in [F(0), F(-1, 2), F(-1), F(-2)]:
            if t1 + dt > 0:
                assert ((d1 + dd) / (t1 + dt) >= th) == (dd - th * dt >= m)

# n+1 : 要素 e=1（宣言厚み 4）の付加だけ。q, p, lambda は不変
d2, t2, R2 = state(q1, p1, [(1 - lam1) * tau0, F(4)])
d_tau_comp2 = t2 - t1
terms2 = [F(0), F(0), F(0), -R1 * d_tau_comp2 / t2]
assert sum(terms2) == R2 - R1

for name, v in [
    ("R_{n-1}", R0), ("R_n", R1), ("dR_n", R1 - R0),
    ("作用進入項", terms1[0]), ("残留進入項", terms1[1]),
    ("劣化縮小項", terms1[2]), ("構成変化項", terms1[3]),
    ("R_rev,n", q1 / t1), ("R_res,n", p1 / t1),
    ("R_{n+1}", R2), ("構成変化項(n+1)", terms2[3]), ("R_res,n+1", p1 / t2),
]:
    print(f"{name:<18} = {v}  ({float(v):.6f})")
for k, m in margins1.items():
    print(f"m_theta[{k}] at n   = {m}  ({float(m):.4f})")
print("OK: すべての恒等式が厳密に一致")
