# 訳語の対応表（量子ハイブリッド用語集）

日本語と英語のすり合わせを記録する。英語は日本語の直訳ではなく、この表に従って書く。食い違いを見つけたら、片方だけを直して終わらせず、両方を直し、理由を日付つきで下の「経過」に残す。

| 見出しID | 日本語名 | 英語名 | 選んだ理由 | 避けた訳語と理由 | 状態 |
|---|---|---|---|---|---|
| `qh-spsa` | 同時摂動確率近似（SPSA） | Simultaneous Perturbation Stochastic Approximation (SPSA) | 略称SPSAは原語のまま通用し、日本語の正式名は原題の語順に沿う | 「同時」を「同期」と取り違える訳（非同期の議論と混ざる） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-barren-plateau` | バレンプラトー（勾配消失の台地） | Barren plateau | カタカナを主とし、意味は説明で補う。分野で定着した呼び方 | 「不毛の台地」（直訳。用語として使わない）、「勾配消失」だけ（より広い語で、バレンプラトーはその一種。量子回路に特有の指数的な消失を表せない） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-vqe` | 変分量子固有値ソルバ（VQE） | Variational Quantum Eigensolver (VQE) | 略称VQEが定着。「固有値ソルバ」は eigensolver の訳 | 「求解器」 | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-nisq` | NISQ（ノイズのある中規模量子） | Noisy Intermediate-Scale Quantum (NISQ) | 略称NISQが定着。説明で補う | 「雑音つき」だけ（中規模の意味が落ちる） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-shot` | ショット | Shot | 実装資料の語をそのまま使う | 「試行」「照射」 | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-parameter-shift-rule` | パラメータシフト則 | Parameter-shift rule | shift は値をずらす意味 | 「パラメータ移動」 | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-lindblad-equation` | リンドブラッド方程式（GKSL形式） | Lindblad (GKSL) equation | GKSL形式と併記して由来を示す | 「主方程式」だけ（別の方程式も指すため） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-observable-expectation-vector` | 観測量期待値ベクトル | Observable expectation-value vector | observable は物理量。観測された値ではない | 「観測値ベクトル」（observationと混ざる） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-rate-limiting-stage` | 律速段原則 | Rate-limiting-stage principle | 化学工学の「律速段階」と同じ考え方 | 「ボトルネック原則」 | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-delayed-reference-residual` | 遅延参照残差（4月の旧称は残渣 r_t。正典の残差 ξ とは別） | Delayed-reference residual (r_t of April; distinct from the canonical residual ξ) | 英語の residual は「残差」に当たる。正典の残差（ξ）と区別するため、「遅延参照」を付ける。4月の「残渣」は旧称として残す | 「残渣」（残りかすの語で、差の意味と合わない。読みが同じ「ざんさ」で取り違える）、単独の「残差」「residual」（正典の ξ と混ざる） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-fractional-carry` | 端数持ち越し | Fractional carry-over | 日本語の「端数」に対応し、誤差帰還と近い | 「残渣持ち越し」（差の意味と混ざる） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-quantization-lock` | 量子化ロック | Quantization lock (underflow freeze) | quantization は数値の離散化で、量子力学の quantum とは別 | 「量子ロック」（量子計算の現象と誤解される） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-lfsr` | 線形帰還シフトレジスタ（LFSR） | Linear-feedback shift register (LFSR) | 略称が定着。疑似乱数と明記 | 「乱数生成器」だけ（疑似乱数でない意味に読める） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-pair-skip` | ペア見送り | Pairwise skip of an update | 観測値を捨てずに記録する意味で skip | 「破棄」（discard） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-discard-vault` | DiscardVault（見送り・境界越えの保管庫） | DiscardVault | 参照実装の固定名 | 日本語への訳（固定名のため） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-update-authority` | 更新許可 | Update permission | 最適化の更新の許可。正典の「更新権限」と同名を避けて改名（2026-10-23） | 未定（正典側の英訳が未確認） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-few-shot-spsa-nominal-calculation` | 少数ショットSPSA名目計算 | Few-shot SPSA nominal calculation | 旧称の「二重揺らぎ」が正典語と同名だったため改名 | 「二重揺らぎ名目計算」（旧称） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-cryo-cmos-4k-stage` | 4Kステージ | 4 K stage | 冷却段（場所）を指す語として、Cryo-CMOS（回路）から分けた | 「4Kステージ（Cryo-CMOS）」（二つの概念の合成） | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-cryo-cmos` | Cryo-CMOS（極低温CMOS） | Cryo-CMOS (cryogenic CMOS) | Cryo-CMOS は原語のまま通用する | 「極低温半導体」（回路の意味が落ちる） | 【草稿】概念未照合（全文対訳未確認） |
| `qh-qec` | 量子誤り訂正（QEC） | Quantum error correction (QEC) | 略称QECが定着 | 「エラー補正」 | 【草稿】概念照合済み（全文対訳未確認） |
| `qh-union-find-decoder` | Union-Find復号器 | Union-Find decoder | 手法名として原語のまま | 「併合探索」 | 【草稿】概念照合済み（全文対訳未確認） |

## 経過

| 日付 | 見出しID | 内容 |
|---|---|---|
| 2026-10-22 | （全体） | 骨格を作成。名称は仮置きで、すり合わせは未了 |
| 2026-10-22 | `qh-spsa`、`qh-barren-plateau`、`qh-delayed-reference-residual` | 草稿を作成（日英同時）。`qh-barren-plateau` の見出しは、いったん「勾配消失の台地」を外したが、「勾配消失の台地」の説明が概念として妥当で、バレンプラトーが勾配消失の一種であることから、同日に戻した。IDは変えていない |
| 2026-10-23 | `qh-delayed-reference-residual` | 見出しを「遅延参照残渣」から「遅延参照残差」へ変更（案B）。理由：4月の r_t は予測と参照の差で、意味は残差。英語の residual と対応し、正典の残差 ξ とも語が揃う。「残渣」は旧称（差の意味と、浮動小数点の端数＝余り物の意味の二つがあった）として残す。IDは変えていない |
| 2026-10-23 | 残りの17語 | 草稿を作成（日英同時）。確認済みの印は付けていない。`qh-update-authority` は正典の「更新権限」と同名で、判断が要る（2026-10-23に「更新許可」へ改名） |
| 2026-10-23 | `qh-update-authority` | 見出しを「更新権限」から「更新許可」（英：Update permission）へ変更。理由：正典 AXIOMS §14 の「更新権限」と同名になるため。IDは変えていない |
| 2026-10-23 | （全20語） | 日英のすり合わせを、対応表の案どおりに確認。`qh-update-authority` は、見出し「更新許可」を確認し、正典側の英訳は update authority と確認。出典の書誌は照合済み（Spall の DOI を含む） |
| 2026-10-23 | `qh-update-authority` | 正典側の「更新権限」の英語表記を確認：update authority（FORMULA §6、THEORY、SANDWICH_ARCH、基礎論文、辞書の評価スナップショット、axioms.json）。英語でも同名になるため、「更新許可（Update permission）」への改名は妥当。未了の項目は解消 |
| 2026-10-23 | 全体 | 外部レビューの指摘を検討して修正（SPSAの由来、バレンプラトーの条件、VQE・NISQの限定、ショットの独立性、ℏ=1、律速段原則の比較可能性、端数持ち越しの前提、量子化ロックの限定、LFSRの再現条件、ペア見送りの限定、名目の用語、Union-Findのノイズ条件）。4Kステージの冷却能力は、メーカー資料で確認した値に更新し、Cryo-CMOS を別項目 `qh-cryo-cmos` に分けた |
| 2026-10-23 | （状態欄） | 状態欄の「英日確認済み／未確認」を、「概念照合済み／未照合」と「全文対訳（未）確認」に分けた。これまでの確認は、意味と訳語の対応の照合であり、全欄の英訳の一対一の確認ではないため |
