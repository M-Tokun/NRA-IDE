"""二重ゆらぎとRの増加傾向を、誤警報率を揃えて比べる（2026-10-22）

実行: python -I -X utf8 sim_double_fluct.py
古典計算機上の仮想モデル。数値は例示で、実機の値ではない。

方法
  1. 変化のない状態（δ=0.15、τ=0.5、測定雑音のみ）で、各判定の1ステップあたりの誤警報率が
     同じ値（既定0.1%）になるよう閾値を較正する。
  2. 同じ閾値で、原因の異なる場面を比べる。S4cはS4aとRの経路が同じになるよう作る。
判定（窓Wステップの回帰傾きを標準誤差で割ったz値）
  R増加傾向: z_R > 閾値
  二重ゆらぎ: min(z_δ, -z_τ) > 閾値（δ増加とτ減少が同時に有意）
"""
import numpy as np

K, ONSET, W, SIG = 400, 100, 20, 0.005
D0, T0, FAR = 0.15, 0.5, 0.001
X = np.arange(W) - (W - 1) / 2
KER = X[::-1] / np.sum(X ** 2)  # 回帰傾きの畳み込み核
SE = SIG / np.sqrt(np.sum(X ** 2))


def slopes(y):
    return np.convolve(y, KER, mode="valid")  # 長さ K-W+1、窓の終端はインデックス W-1 から


def paths(name):
    k = np.arange(K)
    ramp = np.clip((k - ONSET) / (K - ONSET), 0, 1)
    d, t = np.full(K, D0), np.full(K, T0)
    if name == "S4a 両側が悪化（δ微増・τ劣化）":
        d, t = D0 + 0.05 * ramp, T0 - 0.3 * ramp
    elif name == "S4b τだけ劣化":
        t = T0 - 0.3 * ramp
    elif name == "S4c δだけ増加（S4aと同じRの経路）":
        r_a = (D0 + 0.05 * ramp) / (T0 - 0.3 * ramp)
        d = r_a * T0
    elif name == "S5 δの一時増加（τ一定）":
        d = np.where((k >= 100) & (k < 150), 0.30, D0)
    return d, t


def stats(name, rng):
    d, t = paths(name)
    od, ot = d + rng.normal(0, SIG, K), t + rng.normal(0, SIG, K)
    r = od / ot
    zd, zt = slopes(od) / SE, slopes(ot) / SE
    zr = slopes(r)
    return zr, np.minimum(zd, -zt), d / t


def calibrate(seeds=300):
    rng = np.random.default_rng(1)
    zr_all, df_all = [], []
    for _ in range(seeds):
        zr, df, _ = stats("null", rng)
        zr_all.append(zr); df_all.append(df)
    zr_all, df_all = np.concatenate(zr_all), np.concatenate(df_all)
    return np.quantile(zr_all, 1 - FAR), np.quantile(df_all, 1 - FAR)


def evaluate(name, thr_r, thr_df, seeds=300):
    rng = np.random.default_rng(2)
    first_r, first_df, rate_r, rate_df = [], [], [], []
    warn = None
    for _ in range(seeds):
        zr, df, r_true = stats(name, rng)
        ar, adf = zr > thr_r, df > thr_df
        after = slice(ONSET - (W - 1), None)  # 変化開始以降の窓
        rate_r.append(ar[after].mean()); rate_df.append(adf[after].mean())
        idx = np.arange(W - 1, K)
        fr = idx[(idx >= ONSET) & ar]; fd = idx[(idx >= ONSET) & adf]
        first_r.append(fr[0] if fr.size else np.nan); first_df.append(fd[0] if fd.size else np.nan)
        w = np.where(r_true >= 0.6)[0]
        warn = w[0] if w.size else None
    det = lambda a: f"{np.mean(~np.isnan(a)):.0%}"
    med = lambda a: "—" if np.all(np.isnan(a)) else f"{np.nanmedian(a):.0f}"
    print(f"  {name}")
    print(f"    検出した試行: R増加傾向 {det(np.array(first_r))} ／ 二重ゆらぎ {det(np.array(first_df))}")
    print(f"    初回検出（中央値）: R増加傾向 {med(np.array(first_r))} ／ 二重ゆらぎ {med(np.array(first_df))}"
          f" ／ 真のR≥0.6 {warn if warn is not None else '到達せず'}")
    print(f"    変化開始後の警報率: R増加傾向 {np.mean(rate_r):.1%} ／ 二重ゆらぎ {np.mean(rate_df):.1%}")


if __name__ == "__main__":
    thr_r, thr_df = calibrate()
    print(f"較正：変化なしで1ステップあたり誤警報率 {FAR:.1%}。閾値 R増加傾向={thr_r:.3g}、二重ゆらぎ={thr_df:.2f}σ")
    for name in ("S4a 両側が悪化（δ微増・τ劣化）", "S4b τだけ劣化",
                 "S4c δだけ増加（S4aと同じRの経路）", "S5 δの一時増加（τ一定）"):
        evaluate(name, thr_r, thr_df)
