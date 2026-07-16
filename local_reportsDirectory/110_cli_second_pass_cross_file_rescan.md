# NRA-IDE 第2次CLI精査 継続Report — AI文書26件 横断再集計

- 実施日: 2026-07-16 JST
- 対象: `docs/en-US/ai`および`docs/ja-JP/ai`のMarkdown 26件
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 構造検査

```text
FILES=26
ODD_FENCES=0
TRAILING_WHITESPACE_FILES=0
REPLACEMENT_CHARACTER_FILES=0
INVALID_FIRST_HEADING_FILES=0
```

構造破損は検出しなかった。

## 2. 旧表現の確定残存

直接的な状態・ラッチ混同は次の2件だった。

- `docs/en-US/ai/12_glossary_EN.md:148`: `latch state`
- `docs/ja-JP/ai/12_glossary_JP.md:133`: `正規状態`、`ラッチ状態`、末尾の`正規状態`

## 3. 不完全列挙候補の扱い

機械抽出は、具体的な列挙だけでなく「旧経路を継続しない」「Cause-Side権限にならない」という包括的な禁止文も候補化した。包括文は対象集合を限定する列挙ではないため、欠落判定を自動確定しない。

既に同一ファイル内で完全な禁止集合が明示され、候補文が特定目的の包括文または特定閾値だけの説明である場合は、偽陽性として保持する。今後は直接的な旧用語、または列挙形式で一部だけを権限対象として示す文を優先する。

## 4. 次の作業位置

次の直接対象は`docs/en-US/ai/12_glossary_EN.md`とする。英語版を1ファイル質疑形式で判定した後、日本語対訳を別ファイルとして扱う。

このReport作成時点で対象本文は編集していない。
