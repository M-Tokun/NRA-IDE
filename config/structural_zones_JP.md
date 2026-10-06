# 現行NRA-IDE境界設定

定義は[AXIOMS.md](../theory/AXIOMS.md)と[axioms.json](../theory/axioms.json)による。照合時点はv2.4。[参照実装](../nra-core/foundations/NRA-IDE_Architecture_public.py)を分類に用い、[gateアダプター](../gate/_canonical_threshold.py)が呼出し間の対象履歴を保持する。

`R = delta / tau`の定義域は有限のdelta >= 0、有限のtau > 0。負値を絶対値で補正しない。tau=0はOUT_OF_DESCRIPTION_DOMAINである。ドメインごとに評価前に定める閾値は`0 <= R_warn < R_handoff < R_irrev < 1`。旧来の共通0.40/0.99閾値とZone A/B/Cを現行モデルへ流用しない。

| 正規状態 | 条件 | 運用動作 |
|---|---|---|
| PERMIT | 0 <= R < R_warn | CONTINUE |
| BOUNDARY_WARNING | R_warn <= R < R_handoff | LOG_WARN |
| HANDOFF_REQUIRED | R_handoff <= R < R_irrev | FAIL_CLOSED |
| IRREVERSIBLE_TRANSITION | R_irrev <= R < 1, または不可逆ラッチ保持 | FAIL_CLOSED |
| RUPTURE_BOUNDARY | R >= 1, または対象破断保持 | FAIL_CLOSED |
| CONFESSION | 入力・宣言・閾値が不正または不明 | FAIL_CLOSED |
| OUT_OF_DESCRIPTION_DOMAIN | tau = 0 （他の必要条件を満たす入力） | FAIL_CLOSED |

FAIL_CLOSEDは運用動作であり、8番目の正規状態や完全沈黙ではない。Handoffで移るのは実行権限だけである。観測・記録・通信は別次元として保持する。対象破断後は、生存経路でPOST_RUPTURE_FIXEDの構造証言を継続する。後続Rの低下や入力異常によって破断を解除せず、不正サンプルはCONFESSIONとして対象破断とは別に報告する。

既定JSONの宣言・閾値はnullであり、未設定の評価はCONFESSIONとなる。対象・単位・出所・delta/tau構成規則・適用領域・閾値根拠をドメイン担当者が評価前に設定し、各呼出しに観測時点を渡す。実装が検証するのは入力構造であり、物理測定・支配方程式の真実性や安全性を保証しない。

ide_presets.jsonは0.4/0.6/0.8の例示閾値を使うSOFTWARE_DEMOだけを持つ。未検証のソフトウェアデモであり、物理的・臨床的安全性の根拠はない。旧DOMAIN_A/B/C、no_history、JSON actionは[legacy/v1](legacy/v1/structural_zones_JP.md)へ保存し、自動変換しない。

残存余白は`remaining_ratio_margin = 1 - R`と`remaining_absorption_margin = tau - delta`を区別する。出力や設定コピーの変更、R低下で不可逆・破断履歴を解除しない。プロセス再起動をまたぐ履歴保存は呼出し側の責任であり、新規instanceの生成は回復の根拠にならない。
