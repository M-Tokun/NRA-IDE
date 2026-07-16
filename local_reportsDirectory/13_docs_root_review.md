# docs 直下精査報告

- 検査日: 2026-07-14 JST
- 対象: `docs` 直下11ファイル
- 基準: 現行v2.1正典、ルート、theory、nra-core、noteの既精査結果
- 総合判定: **不合格**

## ファイル別判定

| ファイル | 判定 | 主な指摘 |
|---|---|---|
| `TOP_sandwich.png` | 不合格・重複 | `theory/figures/TOP_sandwich.png` と完全一致。CONFESSION、OUT_OF_DESCRIPTION_DOMAIN、`tau<=0`、現行境界を欠く旧図。 |
| `nra_ide_residue_base_delay_precision.png` | 不合格 | 正規比Rを残差関数名へ、tauを遅延へ再利用。「精度確保」の安定条件・誤差上界なし。 |
| `NRA-IDE_Architecture_public.py` | 不合格・重複 | nra-core版と完全一致。非正値tauをFAIL扱いしinfinity化、旧状態のみ、v2.1未実装。 |
| `Sandwich-ARCHITECTURE.md` | 不合格・legacy | tauを時間スケールとして扱い、Post-NRAを全面沈黙とする。現行 `SANDWICH_ARCH.md` とは別仕様。記載する`gate/`、`src/`対応も現構成と不一致。 |
| `nra_ide_sandwich_architecture.svg` | 不合格・legacy | `R<1 PERMIT / R>=1 FAIL-CLOSED`の二分のみ。三境界、5状態、領域外、ラッチなし。 |
| `README.md` | 不合格 | RをResidueと誤定義し、Honest Silenceを安全原理とする。量子IDEが誤差発散を避けるとの未証明断定。 |
| `README_JP.md` | 不合格 | 英語版と同じ旧仕様。Rを残渣とし、R>=1で一律出力停止。 |
| `FORMULA.pdf` | legacy | Ver 1.00系列の閲覧用資料。現行正本はMarkdownであり、旧定義・飽和語彙問題を継承するため正典利用不可。 |
| `nra_ide_formula_applied.jpg` | 不合格 | `F_IDE`を量子根本、`G(r)Phi(x)`を古典補助と断定するが、量・次元・結合・安定条件なし。 |
| `nra_ide_formula_basic.jpg` | 不合格・重複 | theoryのVer 1.00旧式図と完全一致。側別max、固定境界、出力停止等が現行不整合。 |
| `NRA-IDE_git.jpg` | 合格・ブランド資産 | 正式英語名称は正しい。理論主張を含まない。 |

## 横断問題

- docs公開入口が現行v2.1ではなく旧沈黙モデルを案内する。
- theory/nra-coreで不合格となったファイルを同一ハッシュで再掲し、正典・legacy表示がない。
- Rとtauの予約記号を残差・遅延・時間スケールへ多重使用する。
- 量子層、古典層、安全保証の主張を実装・試験なしで公開する。

## 最終判定

ブランド画像以外は現行公開入口として採用できない。README、図、公開Pythonをv2.1へ同期するか、docs全体をlegacy表示する必要がある。
