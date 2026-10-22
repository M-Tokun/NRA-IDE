"""小規模比較シミュレーション：SPSA × 境界監督（A〜D）と故障注入（2026-10-22）

実行: python -I -X utf8 sim_compare.py
すべて古典計算機上の仮想モデル。数値は構造を見るための例示で、実機の値ではない。

構成
  A: 通常のSPSA（監視なし）
  B: SPSA＋単純な閾値監視（欠測はゼロ埋め、判定は測定時のみ、ラッチなし、記録なし）
  C: SPSA＋NRA-IDE（観測喪失は保持・停止、状態区分、r_irrevでラッチ、境界越えを記録）
  D: C＋適用直前の再判定（時刻・版の照合）

最適化対象: 1量子ビット C(θ)=(1-cosθ)/2、各点Mショット、2点SPSA。
熱モデル: 4K段。δ=P_load-P_base、τ=P_cap(T_op)·h-P_base（Cause-Side：宣言運転温度での冷却能力×健全性）。
真値の判定: 適用時の真の R≥r_handoff の更新を「危険な更新」、真の R<r_warn かつ観測が有効なのに見送った更新を「誤停止」とする。
"""
import numpy as np

P_BASE, P_CAP0 = 1.0, 1.5
R_WARN, R_HANDOFF, R_IRREV = 0.6, 0.8, 0.95
K, M_SHOTS, A_STEP, C_PERT = 400, 8, 0.1, np.pi / 8
SIG = 0.005  # 監視チャネルの測定雑音（W）


def cost(theta):
    return (1 - np.cos(theta)) / 2


def scenario(name):
    """各ステップの真の δ、健全性 h、観測チャネル有効フラグを返す。"""
    k = np.arange(K)
    delta = np.full(K, 0.15)
    h = np.ones(K)
    channel = np.ones(K, dtype=bool)
    if name == "S1_欠測中の負荷上昇":
        channel[150:200] = False
        delta[160:190] = 0.45  # R=0.9。欠測で見えない
    elif name == "S2_遅延中の急変":
        delta[200:230] = 0.45
    elif name == "S4_τのゆっくりした劣化":
        sl = slice(100, K)
        h[sl] = 1 - 0.2 * (k[sl] - 100) / (K - 100)  # P_cap 1.5→1.2、τ 0.5→0.2
        delta[sl] = 0.15 + 0.05 * (k[sl] - 100) / (K - 100)
    elif name == "S5_無害なδの一時増加":
        delta[100:150] = 0.30  # R=0.6、τは一定
    elif name == "S6_一時的な境界越え":
        delta[200:204] = 0.60  # R=1.2 を4ステップ
    return delta, h, channel


def true_R(delta, h):
    return delta / (P_CAP0 * h - P_BASE)


def run(arch, name, seed, latency=0):
    rng = np.random.default_rng(seed)
    delta, h, channel = scenario(name)
    obs_delta = delta + rng.normal(0, SIG, K)
    obs_tau = (P_CAP0 * h - P_BASE) + rng.normal(0, SIG, K)
    theta, latched, queue = np.pi / 2, False, []
    m = dict(danger=0, false_stop=0, applied=0, record=False)

    def monitor(t):
        """構成ごとの判定。戻り値: 更新を許すか。"""
        nonlocal latched
        if arch == "A":
            return True
        if arch == "B":
            d = obs_delta[t] if channel[t] else 0.0  # 欠測をゼロ埋め
            return d / obs_tau[t] < R_HANDOFF
        if not channel[t]:
            return False  # OBSERVATION_LOST：保持して自律判断を止める
        r = obs_delta[t] / obs_tau[t]
        if r >= R_IRREV:
            latched = True
            m["record"] = True  # 越えた時刻と値を記録
        return (not latched) and r < R_HANDOFF

    for t in range(K):
        # 測定と勾配（Mショット×2点）
        dlt = rng.choice([-1.0, 1.0])
        p_plus, p_minus = cost(theta + C_PERT * dlt), cost(theta - C_PERT * dlt)
        y_plus = rng.binomial(M_SHOTS, p_plus) / M_SHOTS
        y_minus = rng.binomial(M_SHOTS, p_minus) / M_SHOTS
        g = (y_plus - y_minus) / (2 * C_PERT) * dlt
        if monitor(t):
            queue.append((t + latency, g))
        else:
            ok_truth = channel[t] and true_R(delta[t], h[t]) < R_WARN
            m["false_stop"] += ok_truth
        # 適用
        for item in [q for q in queue if q[0] == t]:
            queue.remove(item)
            if arch == "D" and not monitor(t):
                ok_truth = channel[t] and true_R(delta[t], h[t]) < R_WARN
                m["false_stop"] += ok_truth
                continue
            theta -= A_STEP * item[1]
            m["applied"] += 1
            m["danger"] += true_R(delta[t], h[t]) >= R_HANDOFF
    m["final_cost"] = cost(theta)
    return m


def compare(name, latency=0, seeds=200):
    print(f"\n[{name}] 遅延={latency}ステップ、{seeds}試行の平均")
    print("  構成 | 危険な更新 | 誤停止 | 適用した更新 | 最終コスト | 境界越えの記録")
    for arch in "ABCD":
        ms = [run(arch, name, s, latency) for s in range(seeds)]
        avg = {k: np.mean([x[k] for x in ms]) for k in ("danger", "false_stop", "applied", "final_cost", "record")}
        print(f"  {arch}    | {avg['danger']:9.2f} | {avg['false_stop']:6.2f} | {avg['applied']:11.1f} |"
              f" {avg['final_cost']:.4f} | {avg['record']:.0%}")


def tau_definition_check():
    """S3：τを応答温度 T から求めると平衡で R≡1 になることの確認。"""
    print("\n[S3_τの定義] 平衡状態で比較（P_avail(T)=P_cap·T/T_op、熱容量で緩和）")
    print("  付加負荷δ | 真のR（T_opで評価） | 応答温度で求めたR")
    for d in (0.1, 0.25, 0.4, 0.6):
        T, T_op, Cth, dt = 4.2, 4.2, 5.0, 0.01
        for _ in range(20000):  # 熱平衡まで緩和
            T += dt * (P_BASE + d - P_CAP0 * T / T_op) / Cth
        r_eff = d / (P_CAP0 * T / T_op - P_BASE)
        print(f"  {d:9.2f} | {d / (P_CAP0 - P_BASE):18.2f} | {r_eff:.3f}")


def double_fluct_specificity(seeds=200, W=20):
    """S4・S5：Rの増加傾向と二重ゆらぎの警報を比べる（回帰傾きの3σ判定）。"""
    print(f"\n[S4・S5_二重ゆらぎ] 窓{W}ステップの回帰傾き、3σで有意とみなす。{seeds}試行")
    x = np.arange(W) - (W - 1) / 2
    se = SIG / np.sqrt(np.sum(x ** 2))
    for name in ("S4_τのゆっくりした劣化", "S5_無害なδの一時増加"):
        first_trend, first_df, n_trend, n_df, warn_t = [], [], [], [], []
        for s in range(seeds):
            rng = np.random.default_rng(s)
            delta, h, _ = scenario(name)
            od = delta + rng.normal(0, SIG, K)
            ot = (P_CAP0 * h - P_BASE) + rng.normal(0, SIG, K)
            r = od / ot
            tr, dfl = [], []
            for t in range(W, K):
                sd = np.polyfit(x, od[t - W:t], 1)[0]
                st = np.polyfit(x, ot[t - W:t], 1)[0]
                sr = np.polyfit(x, r[t - W:t], 1)[0]
                se_r = se / 0.5  # 目安
                tr.append(sr > 3 * se_r)
                dfl.append(sd > 3 * se and st < -3 * se)
            tr, dfl = np.array(tr), np.array(dfl)
            n_trend.append(tr.sum()); n_df.append(dfl.sum())
            first_trend.append(W + np.argmax(tr) if tr.any() else np.nan)
            first_df.append(W + np.argmax(dfl) if dfl.any() else np.nan)
            w = np.where(r >= R_WARN)[0]
            warn_t.append(w[0] if w.size else np.nan)
        print(f"  {name}: 警報ステップ数 R増加傾向={np.mean(n_trend):.1f} 二重ゆらぎ={np.mean(n_df):.1f}"
              f" ／ 初回時刻 R増加傾向={np.nanmean(first_trend):.0f} 二重ゆらぎ={np.nanmean(first_df):.0f}"
              f" R≥r_warn={np.nanmean(warn_t):.0f}")


if __name__ == "__main__":
    compare("S1_欠測中の負荷上昇")
    compare("S2_遅延中の急変", latency=5)
    compare("S6_一時的な境界越え")
    tau_definition_check()
    double_fluct_specificity()
