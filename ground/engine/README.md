# ground/engine/
<!-- FILE: ground/engine/README.md 26-0629 -->

## 位置付け

`ground/engine/grounding.py` は、IDE側の接地・境界制御ロジックである。
NRA公理を追加しない。真理や存在を決定しない。

この engine が判定するのは、観測・定義・出所・物理制約に照らして、変数を現在の実行文脈で使用してよいかである。

---

## 基本状態

### `BOTTOM`

`BOTTOM` は Python 上では `None` で表現する。
ただし、通常の null や不存在断定ではない。

`BOTTOM` は次の状態を表す。

```text
未観測
未定義
検証不能
現在の実行文脈で未使用可能
```

`BOTTOM` を数値補完してはならない。

### `e`

`e` は存在フラグではない。
現在の実行文脈で、その変数を使用可能な値として扱えるかを示す接地フラグである。

```text
e = 1 → x は BOTTOM ではなく、使用可能な値でなければならない
e = 0 → x は BOTTOM として扱う
```

---

## 観測台帳

`GroundedVariable` は次の観測台帳フィールドを持つ。

```text
取得時刻
場所
単位
機器
校正状態
測定誤差
出所
```

方針上、観測台帳は必須である。
ただし現実装では、空文字を許容して構造フィールドを保持する段階に留めている。

厳格な台帳検証は、ドメイン別 validator または後続実装で行う。

---

## 判定フロー

`GroundingEngine.classify()` は、入力変数を次の3パターンに分類する。

```text
Pattern A:
  全必須変数が使用可能
  → domain inverse compute へ進む

Pattern B:
  必須変数が欠損または未使用可能
  → FAIL-CLOSED

Pattern C:
  必須変数は使用可能だが、非必須変数が欠損または未使用可能
  → 欠損を明示して domain inverse compute へ進む
```

Pattern C は補完許可ではない。
欠損を明示したうえで、不確定範囲を含む結果として扱う。

---

## 実行境界

`GroundingEngine.execute()` は、Pattern B を実行停止する。
Pattern A と Pattern C は `_inverse_compute()` へ渡す。

基底クラスの `_inverse_compute()` は未実装である。
実際の逆算処理は、ドメイン別サブクラスが実装する。

そのため、基底クラスのままでは Pattern A / Pattern C は `NotImplementedError` になる。
Pattern C の warning 返却は、ドメイン別 `_inverse_compute()` が成功した後に成立する。

---

## 物理制約

`c_phys_validator` は、ドメイン別の物理制約チェック関数である。

これはペナルティではなくハードゲートとして扱う。
物理制約に反する候補は、実行候補に入れず FAIL-CLOSED とする。

---

## 実装上の未決事項

```text
宣言済み変数空間 Ω_declared の明示モデル
観測台帳の厳格検証
Pattern C の不確定範囲返却形式
ドメイン別 _inverse_compute()
```

これらは `ground` の方針と矛盾しない。
現実装は、IDE側の接地・境界制御ロジックの最小骨格である。

---

*©M-Tokuni 2026*
