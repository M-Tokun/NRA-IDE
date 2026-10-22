# 訳語の対応表（量子ハイブリッド用語集）

日本語と英語のすり合わせを記録する。英語は日本語の直訳ではなく、この表に従って書く。食い違いを見つけたら、片方だけを直して終わらせず、両方を直し、理由を日付つきで下の「経過」に残す。

| 見出しID | 日本語名 | 英語名 | 選んだ理由 | 避けた訳語と理由 | 状態 |
|---|---|---|---|---|---|
| `qh-spsa` | 同時摂動確率近似（SPSA） | Simultaneous Perturbation Stochastic Approximation (SPSA) | 略称SPSAは原語のまま通用し、日本語の正式名は原題の語順に沿う | 「同時」を「同期」と取り違える訳（非同期の議論と混ざる） | 【草稿】英日未確認 |
| `qh-barren-plateau` | バレンプラトー（勾配消失の台地） | Barren plateau | カタカナを主とし、意味は説明で補う。分野で定着した呼び方 | 「不毛の台地」（直訳。用語として使わない）、「勾配消失」だけ（より広い語で、バレンプラトーはその一種。量子回路に特有の指数的な消失を表せない） | 【草稿】英日未確認 |
| `qh-vqe` | 変分量子固有値ソルバ（VQE） | Variational Quantum Eigensolver (VQE) | 未記入 | 未記入 | 【骨格】 |
| `qh-nisq` | NISQ（ノイズのある中規模量子） | Noisy Intermediate-Scale Quantum (NISQ) | 未記入 | 未記入 | 【骨格】 |
| `qh-shot` | ショット | Shot | 未記入 | 未記入 | 【骨格】 |
| `qh-parameter-shift-rule` | パラメータシフト則 | Parameter-shift rule | 未記入 | 未記入 | 【骨格】 |
| `qh-lindblad-equation` | リンドブラッド方程式（GKSL形式） | Lindblad (GKSL) equation | 未記入 | 未記入 | 【骨格】 |
| `qh-observable-expectation-vector` | 観測量期待値ベクトル | Observable expectation-value vector | 未記入 | 未記入 | 【骨格】 |
| `qh-rate-limiting-stage` | 律速段原則 | Rate-limiting-stage principle | 未記入 | 未記入 | 【骨格】 |
| `qh-delayed-reference-residual` | 遅延参照残差（4月の旧称は残渣 r_t。正典の残差 ξ とは別） | Delayed-reference residual (r_t of April; distinct from the canonical residual ξ) | 英語の residual は「残差」に当たる。正典の残差（ξ）と区別するため、「遅延参照」を付ける。4月の「残渣」は旧称として残す | 「残渣」（残りかすの語で、差の意味と合わない。読みが同じ「ざんさ」で取り違える）、単独の「残差」「residual」（正典の ξ と混ざる） | 【草稿】英日未確認 |
| `qh-fractional-carry` | 端数持ち越し | Fractional carry-over | 未記入 | 未記入 | 【骨格】 |
| `qh-quantization-lock` | 量子化ロック | Quantization lock (underflow freeze) | 未記入 | 未記入 | 【骨格】 |
| `qh-lfsr` | 線形帰還シフトレジスタ（LFSR） | Linear-feedback shift register (LFSR) | 未記入 | 未記入 | 【骨格】 |
| `qh-pair-skip` | ペア見送り | Pairwise skip of an update | 未記入 | 未記入 | 【骨格】 |
| `qh-discard-vault` | DiscardVault（見送り・境界越えの保管庫） | DiscardVault | 未記入 | 未記入 | 【骨格】 |
| `qh-update-authority` | 更新権限 | Update authority | 未記入 | 未記入 | 【骨格】 |
| `qh-few-shot-spsa-nominal-calculation` | 少数ショットSPSA名目計算 | Few-shot SPSA nominal calculation | 未記入 | 未記入 | 【骨格】 |
| `qh-cryo-cmos-4k-stage` | 4Kステージ（Cryo-CMOS） | 4 K stage (Cryo-CMOS) | 未記入 | 未記入 | 【骨格】 |
| `qh-qec` | 量子誤り訂正（QEC） | Quantum error correction (QEC) | 未記入 | 未記入 | 【骨格】 |
| `qh-union-find-decoder` | Union-Find復号器 | Union-Find decoder | 未記入 | 未記入 | 【骨格】 |

## 経過

| 日付 | 見出しID | 内容 |
|---|---|---|
| 2026-10-22 | （全体） | 骨格を作成。名称は仮置きで、すり合わせは未了 |
| 2026-10-22 | `qh-spsa`、`qh-barren-plateau`、`qh-delayed-reference-residual` | 草稿を作成（日英同時）。`qh-barren-plateau` の見出しは、いったん「勾配消失の台地」を外したが、利用者の指摘（本質を突いた正しい説明。バレンプラトーは勾配消失の一種）で同日に戻した。IDは変えていない |
| 2026-10-23 | `qh-delayed-reference-residual` | 見出しを「遅延参照残渣」から「遅延参照残差」へ変更（案B）。理由：4月の r_t は予測と参照の差で、意味は残差。英語の residual と対応し、正典の残差 ξ とも語が揃う。「残渣」は旧称（差の意味と、浮動小数点の端数＝余り物の意味の二つがあった）として残す。IDは変えていない |
