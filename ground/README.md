# NRA-IDE / ground
<!-- FILE: ground/README.md 26-0824 -->

LLMの外部に置く IDE 側の接地・境界制御レイヤー。
変数が実行に使用可能か、FAIL-CLOSEDを発火すべきか、最低限の物理制約に反していないかを判定する。
接続方式（API等）は未確定。`interface/README.md` を参照。

```
NRA-IDE/core/   → NRA側の構造境界・理論定義（縦軸）
NRA-IDE/ground/ → IDE側の接地判断・境界制御・実行前ゲート（横軸）
```

`ground` はNRA公理を追加しない。真理や存在を決定する層ではなく、実行へ渡してよい入力かを判定する層である。
内包しない。完全独立しない。`core/shared/` を両軸が参照する構造。

作業契約・追記時の確認事項・ステータス管理は `AGENTS.md` に従う。ここでは独自ルールを設けない。

---

*©M-Tokuni 2026*
