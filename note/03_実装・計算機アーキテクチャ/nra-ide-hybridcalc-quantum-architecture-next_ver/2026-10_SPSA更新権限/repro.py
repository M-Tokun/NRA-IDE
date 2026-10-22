"""再現スクリプト：論文「二重揺らぎ名目計算と内包性動力学境界…」精査（2026-10-22）

実行: python -I repro.py
各テストは「入力・操作・期待値（論文の主張）・実測値」を出力する。
"""
import numpy as np

rng = np.random.default_rng(20261022)


def t1_barren_plateau_shots():
    # 論文§2.1: Var[∂C] ≤ O(2^-n) から「勾配の大きさ 2^-n」→ M ∈ O(2^{2n}) と主張。
    # 分散が 2^-n なら典型的な勾配の大きさ（標準偏差）は 2^{-n/2}。
    print("T1 バレンプラトーのショット数")
    for n in (10, 20, 30):
        grad_std = np.sqrt(2.0 ** -n)
        m_needed = (1.0 / grad_std) ** 2  # sigma0=1, sigma0/sqrt(M) < grad_std
        print(f"  n={n}: 勾配の典型値={grad_std:.2e}  必要M≈{m_needed:.2e} (=2^n)  論文の2^(2n)={2.0**(2*n):.2e}")


def spsa_samples(g, c, n_samples, noise):
    p = g.size
    delta = rng.choice([-1.0, 1.0], size=(n_samples, p))
    signal = 2 * c * (delta @ g)  # L(θ+cΔ)-L(θ-cΔ) for linear L
    eps_p, eps_m = noise(n_samples), noise(n_samples)
    diff = signal + eps_p - eps_m
    ghat = (diff / (2 * c))[:, None] * delta
    return diff, ghat


def asym_spike_noise(n):
    # 正規ノイズ + 片側（正方向）の稀な大スパイク
    base = rng.normal(0, 0.05, n)
    spike = (rng.random(n) < 0.03) * rng.exponential(2.0, n)
    return base + spike


def report(name, est, g):
    cos = est @ g / (np.linalg.norm(est) * np.linalg.norm(g))
    ratio = est / g
    print(f"  {name:28s} cos={cos:.4f}  成分比 E[ĝ_i]/g_i = {np.array2string(ratio, precision=2)}")


def t2_gate_bias():
    # 論文§4.1: クリップは非対称ノイズでバイアスを生む（破棄なら生じない、§5.1で収束条件が厳密に保たれる）
    # 操作: 線形コスト、勾配 g、片側スパイクノイズ。補正なし・クリップ・ペア破棄（|Δy|ゲート）を比較。
    print("T2 クリップと破棄のバイアス（N=2,000,000）")
    g = np.array([5.0, 2.0, 1.0, 0.5, 0.2, 0.1])
    c, N = 0.05, 2_000_000
    diff, ghat = spsa_samples(g, c, N, asym_spike_noise)
    report("補正なし", ghat.mean(0), g)
    C = np.quantile(np.abs(ghat), 0.95)
    report(f"クリップ ±{C:.1f}", np.clip(ghat, -C, C).mean(0), g)
    ad = np.abs(diff)
    mu, mad = ad.mean(), np.mean(np.abs(ad - ad.mean()))
    for m in (1, 2):
        thr = mu + mad * (2 ** m)  # 論文§4.3: μ + (σ << m)
        keep = ad <= thr
        report(f"ペア破棄 m={m} 残存{keep.mean():.1%}", ghat[keep].mean(0), g)


def t3_adaptive_threshold_drift():
    # 論文§4.3: 閾値 μ_k + (σ_k<<m) を差分の指数移動平均から作る。
    # 操作: 差分が毎ステップ0.2%ずつ増える（ゆっくりした真の悪化）。EMAが追従し、破棄が起きるかを見る。
    print("T3 適応閾値の追従（ゆっくり増える偏差）")
    alpha, m = 0.05, 2
    mu, sig, discards = 1.0, 0.1, 0
    for k in range(3000):
        d = 1.0 * (1.002 ** k) + rng.normal(0, 0.05)
        if d > mu + sig * (2 ** m):
            discards += 1
        else:
            mu = (1 - alpha) * mu + alpha * d
            sig = (1 - alpha) * sig + alpha * abs(d - mu)
    print(f"  3000ステップで偏差は約{1.002**3000:.0f}倍に増加。破棄回数={discards}（閾値は最終 {mu + sig*4:.1f}）")


def t4_shift_then_feedback():
    # 論文§5.2: ũ = (ĝ >> s) + r。整数で先にシフトすると端数は r に入らない。
    print("T4 右シフト後のエラーフィードバック")
    g_int, s, steps = 3, 4, 64  # 3/16 = 0.1875 LSB/step
    theta_a, r = 0, 0
    for _ in range(steps):  # 論文の式どおり（整数シフト後に加算）
        u = (g_int >> s) + r
        theta_a += int(np.floor(u)); r = u - np.floor(u)
    acc, theta_b = 0, 0
    for _ in range(steps):  # 拡張精度アキュムレータ（シフト前の端数を保持）
        acc += g_int
        step = acc >> s
        theta_b += step; acc -= step << s
    print(f"  期待される総更新量={g_int*steps/2**s:.1f}  論文式どおり={theta_a}  拡張精度={theta_b}")


def t5_variable_shift():
    # v2の式（勾配のまま積算→その時点のsでシフト）と、v3の式（共通の高精度単位で積算）を、
    # 途中でシフト量sが変わる場合に比べる。理想値は Σ g_k / 2^{s_k}（実数）。
    print("T5 シフト量が変わるときの端数持ち越し（v2の式とv3の式）")
    g = [7] * 50 + [7] * 50
    s = [3] * 50 + [6] * 50
    ideal = sum(gi / 2 ** si for gi, si in zip(g, s))
    acc, upd_v2 = 0, 0
    for gi, si in zip(g, s):
        acc += gi; u = acc >> si; acc -= u << si; upd_v2 += u
    F, acc3, upd_v3 = 8, 0, 0
    for gi, si in zip(g, s):
        acc3 += gi << (F - si); u = acc3 >> F; acc3 -= u << F; upd_v3 += u
    print(f"  理想値={ideal:.3f}  v2の式={upd_v2}  v3の式={upd_v3}"
          f"（v2はsが変わる時点の残差{(7*50) % 8}を新しいsで扱う）")


if __name__ == "__main__":
    t1_barren_plateau_shots(); t2_gate_bias(); t3_adaptive_threshold_drift(); t4_shift_then_feedback(); t5_variable_shift()
