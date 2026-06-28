# NRA-IDE / ground
<!-- FILE: ground/README.md 26-0628-1855 -->

## 定義

LLMの外部に置く接地判断エンジン。
変数の存在確定・FAIL-CLOSED発火基準・物理制約定義を保持する。
接続方式（API等）は未確定。`interface/README.md` を参照。

## 位置付け

```
NRA-IDE/core/   → 公理・理論定義の本体（定義権の所在）
NRA-IDE/ground/ → 接地判断の実装・ログ・インターフェース
```

内包しない。完全独立しない。`core/shared/` を両軸が参照する構造。

---

## 追記ゲートルール（必須）

追記前に以下4項目を全て確認する。
**④がひとつでも未解決な場合、追記禁止。`ground_Report/pending/` に置く。**

```
① この概念は既存公理に存在しないか
② 類似概念との差分を明示できるか
③ どの既存公理と接続するか
④ 矛盾する既存記述はないか
```

---

## ステータス管理

$$S \in \{\text{active},\ \text{pending},\ \text{archived}\}$$

- ステータス変更＝ディレクトリ移動
- タグの自由記述禁止
- `ground_Report/index.md` に2行以内のサマリーのみ記載

---

*©M-Tokuni 2026*
