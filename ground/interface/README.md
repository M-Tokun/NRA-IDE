# ground/interface/
<!-- FILE: ground/interface/README.md 26-0628-1855 -->

ステータス：**pending**

---

## 接続方式：未確定

whatが確定する前にhowを決定しない。
NRA-IDE FAIL-CLOSED原則と同型。

## 検討中の方向性（note）

- API軸（HTTP）：外部LLMから呼び出し可能・切り分け明確
- ライブラリ直接参照：同一実行環境前提・低レイテンシ
- その他：未検討

## 決定条件

`grounding.py` の `_inverse_compute()` が
ドメイン別に実装完了した後に接続方式を確定する。

**現時点での記述禁止事項：**
接続プロトコル・エンドポイント設計・認証方式の確定記述。

---

*©M-Tokuni 2026*
