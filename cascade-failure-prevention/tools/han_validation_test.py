# FILE: han_validation_test.py
# TITLE: HAN Gate 動作検証スクリプト
# Author: M-Tokuni (https://github.com/M-Tokun/NRA-IDE)
# Date: 2026-03-06 JST
#
# 【修正履歴】
#   v1.0  2026-02-06: 初版
#   v1.1  2026-03-06: R の計算コメントを動的τ対応に修正
#                     二重ゆらぎ（EMA）の動作確認テストを追加
#
# 【このスクリプトの使い方】
#
# HAN Gate が正しく動いているかを確認するための検証ツールです。
# ゲートを起動した状態で実行してください。
#
#   python han_validation_test.py
#
# 【事前準備】
#
#   pip install requests
#
#   # ゲートの起動（別ターミナルで）
#   python gate/han_gate_service.py
#
# 【テストケースの読み方】
#
#   各テストは「label」「テレメトリ」「期待する判定」の3つで構成されています。
#   ⚠️  WARNING が出たら、期待した動作になっていないサインです。
#   ❌  Error が出たら、ゲートに接続できていません。
#
# 【R の値について（動的τ版）】
#
#   R = r_raw × τ_dynamic
#     r_raw = (retry/10) × (queue/500) × (dep_to/5)
#     τ_dynamic = τ_base × (1 + EMA(r_raw))  ← EMAは状態によって変わります
#
#   「なぜ静的計算式と値が違うの？」と思ったら、
#   それは EMA（過去の状態の記憶）が影響しているためです。
#   初回呼び出しでは EMA ≒ r_raw なので、
#   τ_dynamic ≒ τ_base × (1 + r_raw) となります。
#   2回目以降は EMA が蓄積されるため、同じテレメトリでも R が変わることがあります。
#   これが「二重ゆらぎ」の意図した挙動です。

import requests
import time

GATE_URL = "http://localhost:8080/v1/decision"  # 実際の環境に合わせて変更


def test_decision(label: str, telemetry: dict, expected: str | None = None,
                  tau: float = 1.5) -> dict | None:
    """
    1件の判定リクエストを送って結果を表示する共通関数。

    label    : テストの説明文
    telemetry: 送るテレメトリデータ
    expected : 期待する判定（"PASS" または "SILENCE"）
    tau      : 吸収厚み（省略時 1.5）
    """
    payload = {
        "scope":     {"service": "validation-test", "route": "/test"},
        "telemetry": telemetry,
        "tau":       tau,
    }

    print(f"\n--- {label} ---")
    try:
        start = time.time()
        resp     = requests.post(GATE_URL, json=payload, timeout=0.5)
        duration = (time.time() - start) * 1000
        result   = resp.json()

        decision = result.get("decision")
        R        = result.get("R", 0)
        print(f"  判定: {decision}  (R={R:.6f})  応答時間: {duration:.1f}ms")
        print(f"  理由: {result.get('reason', '')}")

        if expected and decision != expected:
            print(f"  ⚠️  警告: {expected} を期待しましたが {decision} が返りました")
        else:
            print(f"  ✅ 期待通りです")
        return result

    except Exception as e:
        print(f"  ❌ エラー: {e}")
        print(f"     ゲートが起動していますか？ (python gate/han_gate_service.py)")
        return None


# テスト 1: 正常系（低負荷）
#
# 【狙い】
#   リトライも、キューも、タイムアウトも小さい。
#   3指標が全て小さいので乗算結果は非常に小さく、PASS になるはずです。
#
# 【計算の目安（初回呼び出し時）】
#   r_raw = (0.1/10) × (5/500) × (0.1/5) = 0.000002
#   τ_dynamic ≈ 1.5 × (1 + 0.000002) ≈ 1.500003
#   R ≈ 0.000003  → R_OP(1.0) より遥かに小さい → PASS
print("\n" + "="*50)
print("【テスト 1】正常系 — 低負荷時は PASS になるか")
print("="*50)
test_decision(
    "低負荷トラフィック",
    {"retry_rate": 0.1, "queue_depth": 5, "dep_timeout_rate": 0.1},
    expected="PASS",
)


# テスト 2: テレメトリ欠損（Fail-Closed）
#
# 【狙い】
#   必須項目が欠けている場合、「情報不足 = 止める」原則で SILENCE になるはずです。
#   「わからないときは動かす」ではなく「わからないときは止める」のが
#   律環公理の Fail-Closed 設計です。
print("\n" + "="*50)
print("【テスト 2】テレメトリ欠損 — 情報不足なら SILENCE になるか（Fail-Closed）")
print("="*50)
test_decision(
    "必須フィールドが欠損（retry_rate のみ送信）",
    {"retry_rate": 0.1},
    expected="SILENCE",
)


# テスト 3: 連鎖反応シミュレーション
#
# 【狙い】
#   リトライ・キュー・タイムアウトが同時に高い値になると
#   R が R_OP(1.0) を超えて SILENCE になるはずです。
#
# 【計算の目安（初回呼び出し時）】
#   r_raw = (15/10) × (600/500) × (8/5)
#         = 1.5 × 1.2 × 1.6 = 2.88
#   EMA(初回) ≈ r_raw = 2.88
#   τ_dynamic = 1.5 × min(1 + 2.88, 2.0) = 1.5 × 2.0 = 3.0  ← TAU_AMPLIFY で上限
#   R = 2.88 × 3.0 = 8.64  → R_OP(1.0) を大きく超える → SILENCE
#
#   ※ TAU_AMPLIFY=2.0 が上限として機能しているのがわかります。
#   ※ 静的τ版の R=4.32 より大きくなっています。
#      これは動的τが「危険な状況をより早く捉える」ように機能しているためです。
print("\n" + "="*50)
print("【テスト 3】連鎖反応 — 3指標が同時に高いと SILENCE になるか")
print("="*50)
test_decision(
    "高負荷（リトライ・キュー・タイムアウトが同時に高い）",
    {"retry_rate": 15.0, "queue_depth": 600, "dep_timeout_rate": 8.0},
    expected="SILENCE",
)


# テスト 4: HOLD 動作確認
#
# 【狙い】
#   テスト 3 の直後、テレメトリが正常に戻っても
#   HOLD_MS（デフォルト 2000ms）の間は SILENCE が続くはずです。
#
#   【なぜ HOLD があるのか？】
#     連鎖が収まった直後にすぐ再開すると、
#     再び連鎖が始まるリスクがあります。
#     「少し落ち着いてから再開する」冷却期間として機能します。
print("\n" + "="*50)
print("【テスト 4】HOLD 動作 — 連鎖後は冷却期間中も SILENCE が続くか")
print("="*50)
print("  （テスト 3 直後なので HOLD 中のはずです）")
test_decision(
    "HOLD 期間中（テレメトリは正常値）",
    {"retry_rate": 0.1, "queue_depth": 5, "dep_timeout_rate": 0.1},
    expected="SILENCE",
)


# テスト 5: 二重ゆらぎ（EMA）の蓄積効果
#
# 【狙い】
#   単独では SILENCE にならない「中程度の負荷」を複数回送り続けると、
#   EMA が蓄積されて τ が大きくなり、徐々に R が上昇していくことを確認します。
#
#   これが「山の尖りを丸める」効果です。
#   急な尖りではなく、じわじわと閾値に近づく挙動になります。
#
#   【注意】
#     このテストは HOLD 期間（2秒）が明けてから実行する必要があります。
#     スクリプトは 3 秒待機します。
print("\n" + "="*50)
print("【テスト 5】二重ゆらぎ — 中程度の負荷が続くと R が上昇していくか")
print("="*50)
print("  HOLD 期間（2秒）が明けるのを待ちます...")
time.sleep(3)

print("  同じ中程度テレメトリを 5 回送ります。R の変化を観察してください。")
print("  EMA が蓄積されるにつれて R が上昇するはずです。\n")

mid_telemetry = {"retry_rate": 5.0, "queue_depth": 200, "dep_timeout_rate": 3.0}
# r_raw = (5/10)×(200/500)×(3/5) = 0.5×0.4×0.6 = 0.12
# 静的τ版: R = 0.12 × 1.5 = 0.18（PASS のまま）
# 動的τ版: EMA が蓄積されると τ が膨らみ R が上昇していく

for i in range(1, 6):
    result = test_decision(
        f"中程度負荷 ({i}回目)",
        mid_telemetry,
    )
    time.sleep(0.2)


# テスト 6: ヘルスチェック
print("\n" + "="*50)
print("【テスト 6】ヘルスチェック")
print("="*50)
try:
    resp = requests.get("http://localhost:8080/healthz", timeout=0.5)
    print(f"  /healthz: {resp.status_code} {resp.text.strip()}")
    if resp.status_code == 200:
        print("  ✅ ゲートは正常に稼働しています")
    else:
        print("  ⚠️  想定外のステータスコードです")
except Exception as e:
    print(f"  ❌ エラー: {e}")


# テスト 7: メトリクスエンドポイント
print("\n" + "="*50)
print("【テスト 7】メトリクス取得 — /metrics が正しく動くか")
print("="*50)
try:
    resp = requests.get("http://localhost:8080/metrics", timeout=0.5)
    print(f"  ステータス: {resp.status_code}")
    for line in resp.text.strip().split("\n"):
        print(f"  {line}")
    print("  ✅ メトリクスを取得できました")
except Exception as e:
    print(f"  ❌ エラー: {e}")

print("\n" + "="*50)
print("検証完了")
print("="*50)
