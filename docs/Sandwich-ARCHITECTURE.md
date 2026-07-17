# NRA-IDE: サンドイッチ構造（権限分離と多層配置）

## 0. 目的

NRA-IDEを実装へ配置するとき、Cause-Sideの構造権威、決定論的IDE評価、Effect-Sideの説明・生成を混同しないための多層構成を記述する。サンドイッチは配置パターンであり、各層へ別々の正規や判定権限を与えるものではない。

本書は公開用の下位説明文書であり、上位仕様[`theory/SANDWICH_ARCH.md`](../theory/SANDWICH_ARCH.md)およびそれより上位の正規文書に従う。競合時に本書、図、デモ、実装コメントを優先してはならない。

律環公理は「存在は生成である。」の一つだけであり、第二公理以降は存在しない。一次式と二次式（二重ゆらぎ式）は、公理ではなくIDEの二つの正規計算系である。その他の式は派生式、補助式または補完式である。

---

## 1. 構造の必然：なぜ分離するのか

構造観測、状態分類、自然言語生成を一つの変更可能なロジックへまとめると、Effect-Sideの評価や生成結果がCause-Sideの $\delta$ 、 $\tau$ 、閾値へ逆流する経路を作り得ます。そこで、権威とデータ経路を三つに分離します。

![NRA-IDE Sandwich Architecture](./TOP_sandwich.png)

---

## 2. 各層の役割

### 2.1 Cause-Side / Structural Input Gate

- **役割:** $\delta$ 、 $\tau$ 、`R_warn`、`R_handoff`、`R_irrev`の出所、単位、有限性、更新規則を検証する。
- **権限:** 宣言済みのCause-Side観測と、評価前に固定した変換・更新規則だけが構造入力を決める。
- **禁止:** LLM出力、自己評価、ランキング、ログなどのEffect-Side値を構造入力の更新根拠へ自動再投入しない。

### 2.2 IDE Structural Evaluation

- **役割:** 正規比 $R=\delta/\tau$ と固定済み閾値から正規状態を決定し、構造証言を作る。
- **境界:** `PERMIT`、`BOUNDARY_WARNING`、`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`を境界同値込みで分類する。
- **例外:** $\tau=0$ は`OUT_OF_DESCRIPTION_DOMAIN`、負値・非有限値・閾値不正は`CONFESSION`。
- **余白:** 無次元の残存比率余白 $M_R=1-R$ と、 $\delta$ ・ $\tau$ と同じ単位の残存吸収余白 $M_{\tau}=\tau-\delta$ を区別する。
- **証言:** 二重ゆらぎ欄は常時存在し、観測不能なら`NOT_OBSERVABLE`と理由を返す。不可逆ラッチは後のR低下で解除しない。
- **ログ:** 既知の数値的進行は`STRUCTURAL_DISCLOSURE_LOG`へ、`CONFESSION`と`OUT_OF_DESCRIPTION_DOMAIN`は`INPUT_EXCEPTION_LOG`へ分離して記録する。

### 2.3 Effect-Side / LLM and Delivery Gate

- **役割:** IDEが決定した状態と構造証言を、説明・翻訳・提示へ反映する。
- **制約:** 生成済みテキストの意味評価から $\delta$ 、 $\tau$ 、閾値、状態を再計算しない。既知の警告や委譲を通常説明へ弱めない。
- **証言切替:** $R<1$ は継続構造証言、 $R\ge1$ は最終固定証言。`RUPTURE_BOUNDARY`は自由形式生成で上書きしない。
- **警告:** `BOUNDARY_WARNING`だけでは、事前固定されたドメイン規則が要求しない限り、Effect-Side出力を全面抑止しない。

---

## 3. 配置上の注意

- `HANDOFF_REQUIRED`は $R\ge R_{\mathrm{handoff}}$ かつ $R<R_{\mathrm{irrev}}$ の運用状態であり、 $R=1$ の別名ではない。
- `IRREVERSIBLE_TRANSITION`は $R\ge R_{\mathrm{irrev}}$ かつ $R<1$ でラッチされる。
- `RUPTURE_BOUNDARY`は $R\ge1$ であり、最終固定証言へ切り替える。
- Fail-Closedは状態名ではない。`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`、`CONFESSION`、`OUT_OF_DESCRIPTION_DOMAIN`で、影響する新規自律判断と自律操作を抑止する運用原則である。
- Fail-Closedは完全沈黙を意味せず、必要な固定構造証言とログを抑止しない。`PERMIT`には適用せず、`BOUNDARY_WARNING`だけでは全面抑止しない。
- 多層配置は安全性を単独で保証しない。対象領域の観測、閾値根拠、故障経路、人間委譲を別途検証する。

---

## 4. 視覚的理解 (Interactive Module)
非正規の概念デモとして、**[M3: 生体模倣サンドイッチ](./figures/M3_NRA_biomimetic_sandwich_svg.html)** を参照できます。これは多層配置を説明する可視化であり、実装適合性、安全性、測定結果または特定ドメインでの有効性を立証しません。

---

### 主要コンポーネント（概念対応）

- **Structural Input Gate:** Cause-Side観測と更新規則を検証する境界。
- **Normative IDE evaluator:** [`nra-core/foundations/NRA-IDE_Architecture_public.py`](../nra-core/foundations/NRA-IDE_Architecture_public.py)。配置だけで適合性は決まらない。
- **Generated docs mirror:** [`docs/NRA-IDE_Architecture_public.py`](./NRA-IDE_Architecture_public.py)。正規ソースとSHA-256が一致しなければならない。
- **Conformance suite:** [`tests/test_nra_ide_reference.py`](../tests/test_nra_ide_reference.py)。現行17試験への合格が必要であり、特定ドメインの安全性までは立証しない。
- **LLM / presentation layer:** 構造証言を説明へ反映するEffect-Side。
- **Effect-Side discard record:** 採用しなかった生成値をEffect-Side監査用に保持し、自動的な構造入力へ戻さない。正規の二つの構造ログと混同しない。
- **Canonical structural logs:** 既知の数値進行用`STRUCTURAL_DISCLOSURE_LOG`と入力例外用`INPUT_EXCEPTION_LOG`を分離する。

---

### Copyright (c) 2026 M-Tokuni  
### SPDX-License-Identifier: MIT
