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
# 【現行の非正典スコアについて】
#
#   chain_score = cooccurrence × dynamic_gain
#     cooccurrence = (retry/10) × (queue/500) × (dep_to/5)
#     dynamic_gain = GAIN_BASE × min(1 + EMA(cooccurrence), GAIN_AMPLIFY_LIMIT)
#
#   EMAはスコアの補助倍率を変えるだけです。正典の R=δ/τ、τ、状態分類ではありません。
#   同じテレメトリでも、スコープ別EMAの履歴によってスコアが変わります。

import requests
import time

GATE_URL = "http://localhost:8080/v1/decision"  # 実際の環境に合わせて変更


def test_decision(label: str, telemetry: dict, expected: str | None = None,
                  scope_name: str = "validation-test") -> dict | None:
    """
    1件の判定リクエストを送って結果を表示する共通関数。

    label    : テストの説明文
    telemetry: 送るテレメトリデータ
    expected : 期待する判定（"PASS" または "SILENCE"）
    scope_name: EMAとHOLDを区別するサービス名
    """
    payload = {
        "scope":     {"service": scope_name, "route": "/test"},
        "telemetry": telemetry,
    }

    print(f"\n--- {label} ---")
    try:
        start = time.time()
        resp     = requests.post(GATE_URL, json=payload, timeout=0.5)
        duration = (time.time() - start) * 1000
        result   = resp.json()

        decision = result.get("decision")
        chain_score = result.get("chain_score")
        score_text = "null" if chain_score is None else f"{chain_score:.6f}"
        print(f"  判定: {decision}  (chain_score={score_text})  応答時間: {duration:.1f}ms")
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
# 【計算の目安（このスコープで初回呼び出し時）】
#   cooccurrence = (0.1/10) × (5/500) × (0.1/5) = 0.000002
#   dynamic_gain ≈ 1.5 × (1 + 0.000002) ≈ 1.500003
#   chain_score ≈ 0.000003  → CHAIN_SCORE_LIMIT(1.0) 未満 → PASS
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
#   chain_score が CHAIN_SCORE_LIMIT(1.0) 以上で SILENCE になるはずです。
#
# 【計算の目安（このスコープで初回呼び出し時）】
#   cooccurrence = (15/10) × (600/500) × (8/5)
#         = 1.5 × 1.2 × 1.6 = 2.88
#   既存EMAがあるため、このスクリプトの実測スコアは 8.64 とは限りません。
#   EMAは前回の低負荷 0.000002 から更新され、約 0.8640014。
#   dynamic_gain ≈ 1.5 × (1 + 0.8640014) ≈ 2.7960021
#   chain_score ≈ 2.88 × 2.7960021 ≈ 8.052486  → SILENCE
#
#   ※ 独立した新規スコープで高負荷を初回入力すると 8.64 となります。
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


# テスト 5: スコア補助倍率（EMA）の蓄積効果
#
# 【狙い】
#   単独では SILENCE にならない「中程度の負荷」を複数回送り続けると、
#   専用スコープを低負荷で初期化してから中程度の負荷を反復します。
#   EMAとスコアが上昇することを確認します。
#
#   これが「山の尖りを丸める」効果です。
#   急な尖りではなく、じわじわと閾値に近づく挙動になります。
#
#   【注意】
#     専用スコープを使うため、先のテストのHOLDの影響は受けません。
print("\n" + "="*50)
print("【テスト 5】補助倍率 — 中程度の負荷が続くとスコアが変わるか")
print("="*50)
test_decision(
    "EMA初期化用の低負荷",
    {"retry_rate": 0.1, "queue_depth": 5, "dep_timeout_rate": 0.1},
    expected="PASS",
    scope_name="validation-ema-test",
)

print("  同じ中程度テレメトリを 5 回送ります。スコアの変化を観察してください。")
print("  EMA が蓄積されるにつれて補助倍率が変化します。\n")

mid_telemetry = {"retry_rate": 5.0, "queue_depth": 200, "dep_timeout_rate": 3.0}
# cooccurrence = (5/10)×(200/500)×(3/5) = 0.5×0.4×0.6 = 0.12
# 固定倍率版: chain_score = 0.12 × 1.5 = 0.18（PASS のまま）
# 低負荷で初期化した同一スコープのEMAが 0.12 に近づき、スコアが上昇する

for i in range(1, 6):
    result = test_decision(
        f"中程度負荷 ({i}回目)",
        mid_telemetry,
        scope_name="validation-ema-test",
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
