# 可視化18件の位置付けと操作 / Scope and operation of 18 visualizations

ここは研究・説明・履歴資料の置き場です。正規参照実装、測定器、安全証明、実運用の判断器ではありません。現行正典は[AXIOMS v2.4](../../theory/AXIOMS.md)、式の定義は[FORMULA](../../FORMULA.md)、正規参照ソースは[Architecture](../foundations/NRA-IDE_Architecture_public.py)に従います。

These are research, educational and historical assets, not calibrated instruments, safety proofs or operational decision systems. Canonical authority remains in AXIOMS; these pages do not replace the normative evaluator.

| ファイル / File | 位置付け・制限 / Scope and limits |
|---|---|
| [Axiom1](NRA_IDE_Axiom1_RigidityPlay_20260425.html) | 旧「公理1」の比較教材。有限Rと最初の破断到達記録を保持。厚み変更は新実験。Historical rigidity/play comparison; finite first-reach record; new thickness starts a separate evaluation. |
| [Axiom2](NRA_IDE_Axiom2_HistoricalAccumulation_20260425.html) | 合成蓄積・消耗・要素追加。追加要素の厚みと既存要素を分離し、既存厚み・残留ズレを回復しない。Synthetic accumulation and added-element model; no restoration of existing elements. |
| [AdaptiveGate](NRA_IDE_AdaptiveGate_20260425.html) | kの適応だけを比較。共通PD・固定刻み・相対速度を使用。β=0で左右一致。壁のクリップ回数を表示。Complementary controller comparison, not a stability proof. |
| [AIRisk filename](NRA_IDE_AIRisk_Layer5_20260416.html) | 実体は適応ゲート比較。ファイル名を履歴として維持。gateRatioは補助比で、正規R・構造厚み・実行権限を判定しない。Legacy filename; auxiliary gate ratio only. |
| [Basic](NRA_IDE_v2a_basic_20260408.html) | 作業者・橋・電池の概念比較。容量一定ならR=1−残量割合。従来技術全般の比較実験ではない。Illustrative normalized scenarios, not a general empirical comparison. |
| [Degradation](NRA_IDE_v2b_deg_v2_20260408.html) | 合成残留指数と可逆負荷の例。表示δ・τと比の入力を一致させ、不可逆・破断履歴を保持。物理校正なし。Synthetic residual-plus-reversible-load model; uncalibrated. |
| [Battery](NRA_IDE_Battery_Comparison_20260412_2054.html) | 同一消耗率で残量と消費比を比較。警告・終端は同時であり予測優位性を主張しない。Equal-drain display comparison; no predictive superiority claim. |
| [Classical AI comparison](NRA_IDE_ClassicalAI_vs_NRAIDE_20260416.html) | 比較演出。時刻演出と状態イベントを分離し、再描画・resizeは実験値を初期化しない。異なるモデルの優劣を実証しない。Illustrative comparison, no general AI-performance proof. |
| [Quantum uncertainty](NRA_IDE_Quantum_Error_20260416.html) | Δx·Δp≥ℏ/2とNRAのδを区別。量子波形は演出。境界線はRグラフと同じ座標変換。Separate quantum observables from structural deviation. |
| [Property error](NRA_IDE_PropertyError_20260416.html) | 熱粒子・層の完了は演出。残差、熱量、保存則、層出力の正しさは未検証。Heat and layer animation is conceptual, not measured or validated. |
| [Formula diagram](NRA_IDE_Formula_Diagram_20260416.html) | 補完式の図解。G(r)は小残差で二次的、大残差で漸近線形かつ非有界。Complementary formula explanation, not bounded saturation. |
| [Full paper](NRA_IDE_FullPaper_20260416.html) | 思想形成の説明。一般保証・熱排出・比較の主張は研究仮説であり、実証済み結果へ昇格しない。Historical explanation; unvalidated claims remain hypotheses. |
| [Water JP](nra_simulation_02_JP.html) | 旧BoundLaw。固定0.8→0.75補正、無限容量buffer。正規Rや物理保存則の証明ではない。Old BoundLaw toy model. |
| [Water EN](nra_simulation_02_EN.html) | 上記の日英対応版。外部Plotly依存を除きCanvas描画へ同期。Bilingual counterpart with native Canvas plotting. |
| [Water Canvas](nra_simulation_canvas.html) | 同じ旧モデルのCanvas版。タイマー停止・Reset世代管理を共通化。Same toy model with timer cancellation and reset-generation control. |
| [Audit JP](AI回答の違和感原因_判断経路確認ツール_26-0713-1628_final.html) | 表面語句の走査と監査prompt生成。非検出はUNKNOWN。入力版と記録を結合。[日本語説明](README_AI_Path_Audit_Tool_v2.md)。Lexical audit helper, not factual or canonical-R evaluation. |
| [Audit EN](AI_Response_Discomfort_Cause_and_Reasoning_Path_Audit_Tool_26-0718-0014_EN.html) | 英語文分割を使用し、記録規則はJPと同期。[English guide](README_AI_Path_Audit_Tool_v2_EN.md)。Locale-aware sentence segmentation and versioned audit records. |
| [ALL poster](Nra-Ide-ALL.html) | 旧図6件を原画像のまま保存。各図に旧記号・旧境界・保証範囲の注記。計算器ではない。Historical figures individually labelled; not an evaluator. |

## 操作とモデルの境界 / Operation versus model

RESETや初期厚みの再宣言は別の実験です。同じ評価中の不可逆履歴の解除・復元ではありません。例示の0.7/0.75/0.9は校正済み普遍値ではありません。現行正典の実行権限・観測・記録・通信の分離を完全実装した教材群ではありません。警告表示があることを、実機や外部APIの実行抑止の証明にしてはなりません。

RESET and a new initial thickness start independent runs. They do not restore an existing target or clear its history within one evaluation. Illustrative thresholds are not universal constants. A displayed warning does not prove suppression of real equipment or external APIs.

監査ツールでは入力変更で古い表示を無効化し、過去の記録は保持します。JSONLには入力スナップショットと生成prompt本文を含みます。端末保存は明示的なSave/Restoreで行います。

The audit helpers invalidate stale presentation on input changes, retaining previous records. JSONL includes input snapshots and generated prompt text. Device input storage uses explicit Save/Restore actions.
