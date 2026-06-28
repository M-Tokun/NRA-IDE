# NRA-IDE / ground ディレクトリ構造
<!-- FILE: ground/DIRECTORY_STRUCTURE_26-0628-1919.md -->

---

## 構造図

```
NRA-IDE/
└── ground/
    │
    ├── DIRECTORY_STRUCTURE.md   ← 本ファイル
    │
    ├── README.md
    │   └── 定義・目的・追記ゲートルール（4項目チェック）
    │
    ├── policies/
    │   └── inverse_grounding_policy.md        [active / Rev.2.1]
    │       └── 逆行接地方針 Layer 0〜3
    │           ├── Layer 0：接地セマンティクス
    │           │   ├── e_i ∈ {0,1}（接地フラグ）
    │           │   ├── x_i ∈ X_i ∪ {⊥}（物理値）
    │           │   └── FAIL-CLOSED＝実行権限停止
    │           ├── Layer 1：要素計算式
    │           │   ├── 実行可能集合 A（ハード制約）
    │           │   ├── 逆算式 hat_x
    │           │   └── 横軸スコア δ_inv
    │           ├── Layer 2：3パターン実行条件
    │           │   ├── Pattern A：全必須変数有効 → 逆算実行
    │           │   ├── Pattern B：必須変数欠損  → FAIL-CLOSED
    │           │   └── Pattern C：非必須変数欠損 → 欠損明示継続
    │           └── Layer 3：適用条件・境界条件
    │               ├── 適用可能ドメイン（気象・農業・構造力学等）
    │               ├── 適用禁止ドメイン（人間行動・市場価格等）
    │               ├── 観測台帳（必須付帯メタデータ定義）
    │               ├── 探索系と実行系の分離
    │               └── P_ground（IDE内部の接地品質指標）
    │
    ├── engine/
    │   └── grounding.py                       [Rev.2 / 分岐確認用テストあり]
    │       ├── GroundedVariable（接地済み変数・観測台帳付帯）
    │       ├── GroundingEngine
    │       │   ├── classify()   → Pattern A/B/C 判定
    │       │   ├── execute()    → パターン分岐実行
    │       │   └── _inverse_compute()  → ドメイン別実装待ち
    │       └── _run_tests()     → 3パターン分岐確認用
    │
    ├── interface/
    │   └── README.md                          [pending]
    │       └── 接続方式未確定・note記述のみ
    │           └── API/ライブラリ等・whatが確定後にhowを決定
    │
    └── ground_Report/
        ├── index.md                           ← 2行サマリー一覧
        │   ├── 逆行接地方針 Rev.2.1  [active]
        │   ├── 接続方式              [pending]
        │   └── ground名称整理        [active]
        │
        ├── active/
        │   └── inverse_grounding_policy.md
        │       └── 確定根拠（追記ゲート記録付き）
        │
        ├── pending/
        │   └── interface_connection.md
        │       └── active移動条件：inverse_compute実装完了後
        │
        ├── archived/                          ← 現在空
        │
        └── 変更履歴.md
            └── ground配下の設計判断・名称変更理由
```

---

## ステータス凡例

| ステータス | 意味 | ディレクトリ |
|---|---|---|
| active | 確定・有効 | `ground_Report/active/` |
| pending | 検討中・未確定 | `ground_Report/pending/` |
| archived | 削除・統合済み | `ground_Report/archived/` |

**ステータス変更 = ディレクトリ移動（タグ自由記述禁止）**

---

## 追記ゲートルール（再掲）

```
① この概念は既存方針・既存仕様に存在しないか
② 類似概念との差分を明示できるか
③ どの既存方針・既存仕様と接続するか
④ 矛盾する既存記述はないか

④が未解決な場合 → 追記禁止・pending へ
```

---

## 名称変更履歴

```
ground/axioms/ → ground/policies/
```

`ground` はNRA公理を追加する場所ではなく、IDE側の接地・境界制御方針を保持するため、ディレクトリ名を実態に合わせた。

---

## 未着手（実装待ち）

```
engine/grounding.py
　└── _inverse_compute()
　　　└── ドメイン別サブクラス実装
　　　　　→ 最初のドメイン確定後に着手
```

---

*©M-Tokuni 2026*
