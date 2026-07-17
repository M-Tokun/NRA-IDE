# NRA-IDE: 線形近似の限界と、非線形な「構造的境界」の再定義

## 律環公理 — 内包性動力学エンジン  
### Nomological Ring Axioms (NRA) - Intensional Dynamics Engine (IDE)

---

> [!IMPORTANT]
> 律環公理は「存在は生成である。」の一つだけであり、第二公理以降は存在しません。一次式と二次式（二重ゆらぎ式）は、公理ではなくIDEの二つの正規計算系です。その他の式は派生式、補助式または補完式です。
>
> このページと各体験モジュールは公開用の説明資料です。正規文書を上書きせず、測定器、適合証拠、安全証明、または特定ドメインでの有効性保証にはなりません。

> 「構造余裕を消耗する最適化は、不可逆な破断境界（ $R \ge 1$ ）へ接近し得る」

現代の安全設計の多くは、一つの重要な構造的見落としを抱えています。それは、「効率」の向上や「予測」の精密化が、必ずしもシステムの堅牢性に直結しないという事実です。むしろ、特定の境界条件下では、これらの努力が系の「残渣（Residue）」を削り取り、微小な変動に対していかにも脆弱な構造を作り出してしまうことがあります。

線形的な安全設計は、境界（Boundary）を固定的なものと見なし、切り捨てた残渣（Residue）を制御可能な誤差として扱うことがあります。NRA-IDE（律環公理）は、変位、残存許容量、切り捨てられた情報が構造状態の評価へ与える影響を検討するための枠組みです。固定された構造証言と委譲規則は安全志向のレビューを支援しますが、それだけで安全を保証するものではありません。

---

## インタラクティブ・体験モジュール (M1〜M5)

既存の線形近似の限界とNRA-IDEの構造語彙に関する、事前設定された概念シナリオを以下の非正規デモで確認できます。表示値は各デモの仮定から生成されたものであり、直接のCause-Side測定値または正規証拠ではありません。

1. **[M1: 線形 vs NRA 破断対比](./figures/M1_NRA_linear_breakdown_simulator.html)**
   - 線形近似が「想定外の変動」に直面した際の挙動の差異を確認してください。
2. **[M2: 残渣タンク (Residue Tank)](./figures/M2_NRA_residue_tank.html)**
   - システム内部に蓄積する「残渣」の減少と、臨界接近時の感度上昇を体験してください。
3. **[M3: 生体模倣サンドイッチ (Biomimetic Sandwich)](./figures/M3_NRA_biomimetic_sandwich_svg.html)**
   - 層間の権限分離を表す概念モデルです。図だけで安全性またはアーキテクチャ適合性は立証されません。
4. **[M4: 告白デバッガー (Confession Debugger)](./figures/M4_NRA_confession_debugger.html)**
   - 既知の構造開示、`CONFESSION`、`OUT_OF_DESCRIPTION_DOMAIN`、固定構造証言、影響する自律出力の抑止を区別します。
5. **[M5: 用語集フリップカード](./figures/M5_NRA_IDE_flip_glossary.html)**
   - NRAの世界観を支える、再定義された言語群を確認します。

---

## 唯一公理とIDE式分類

唯一の律環公理は次です。

> **存在は生成である。**
> **Existence is Generation.**

IDE一次式は次です。

$$
R=\frac{\delta}{\tau}
$$

これはIDEの第一の正規計算系であり、公理ではありません。二次式（二重ゆらぎ式）はIDEの第二の正規計算系であり、第二公理ではありません。

次の画像は現行式関係の説明図です。正規本文が優先され、画像の配置だけでは適合性を取得しません。

![NRA-IDE 基礎式](./nra_ide_formula_basic.jpg)

- **$\delta$ (Delta):** 宣言されたCause-Side観測または事前固定されたCause-Side変換から導く非負の蓄積ズレ。
- **$\tau$ (Tau):** 正の吸収厚み。時定数ではない。 $\tau=0$ は`OUT_OF_DESCRIPTION_DOMAIN`。
- **$R$:** 正規比 $\delta/\tau$ 。残渣そのものではない。 $R \ge 1$ は`RUPTURE_BOUNDARY`であり、構造証言は最終固定となる。不正値・非有限値は`CONFESSION`。

二つの残余余白は次です。

$$
M_R=1-R
$$

$$
M_{\tau}=\tau-\delta
$$

$M_R$ は無次元です。 $M_{\tau}$ は $\delta$ および $\tau$ と同じ単位を持ちます。

破断境界より前は、運用閾値によって`PERMIT`、`BOUNDARY_WARNING`、`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`を区別します。Effect-SideまたはLLM出力は、 $\delta$ 、 $\tau$ 、閾値、判定状態を書き換えられません。

正規7状態は、`PERMIT`、`BOUNDARY_WARNING`、`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`、`CONFESSION`、`OUT_OF_DESCRIPTION_DOMAIN`です。

Fail-Closedは、`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`、`CONFESSION`、`OUT_OF_DESCRIPTION_DOMAIN`で、影響する新規自律判断と自律操作を抑止します。完全沈黙を意味せず、必要な固定構造証言とログを抑止しません。`PERMIT`はFail-Closedではありません。`BOUNDARY_WARNING`だけでは、事前固定されたドメイン規則が要求しない限り全面抑止しません。

`BOUNDARY_WARNING`では、観測可能なら二重ゆらぎ判定を、観測不能なら`NOT_OBSERVABLE`と欠損理由を出します。既知の数値的進行は`STRUCTURAL_DISCLOSURE_LOG`へ、`CONFESSION`と`OUT_OF_DESCRIPTION_DOMAIN`は`INPUT_EXCEPTION_LOG`へ分離して記録します。

### 量子・古典応用に関する研究仮説図

次の応用図は非正規の研究資料です。誤差発散が起きないことを立証するものではなく、実装適合性も付与しません。

![NRA-IDE 応用式](./nra_ide_formula_applied.jpg)

本ドキュメントは、枠組みの前提・主張・限界を、検討と検証が可能な形で説明します。

正規参照先と実装証拠：

- [`theory/AXIOMS.md`](../theory/AXIOMS.md) — 最上位の正規定義
- [`theory/axioms.json`](../theory/axioms.json) — 機械可読な正規同期表現
- [`FORMULA.md`](../FORMULA.md) — IDEの式、定義域、分類
- [`llms.md`](../llms.md) — AI解釈・運用ゲート
- [`NRA-IDE_Architecture_public.py`](./NRA-IDE_Architecture_public.py) — 正規ソースから生成同期するdocsミラー
- [`nra-core/foundations/NRA-IDE_Architecture_public.py`](../nra-core/foundations/NRA-IDE_Architecture_public.py) — 正規参照実装ソース
- [`tests/test_nra_ide_reference.py`](../tests/test_nra_ide_reference.py) — 正規適合試験

---

## プロジェクト構造

次のアーキテクチャ図は説明用です。適合性には本文仕様と該当試験が必要であり、図だけでは安全性を立証しません。

![NRA-IDE サンドイッチ・アーキテクチャ](./TOP_sandwich.png)

- `ja-JP/ai/` : 日本語による詳細な技術解説
- `Sandwich-ARCHITECTURE.md` : Cause-SideとEffect-Sideの権限分離に関する説明
- `figures/` : 非正規の概念図およびデモンストレーションモデル

---

### Copyright (c) 2026 M-Tokuni  
### SPDX-License-Identifier: MIT
