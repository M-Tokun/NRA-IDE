# XML 記述マニュアル

**作成日:** 2026年10月19日（修正版）  
**対象:** XML Viewer で扱うXML文書の基本的な書き方とXPathの使い方

## 1. XMLの基本構造

XML文書は以下の要素で構成されます。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <item id="1" type="example">
    <title>タイトル</title>
    <description>説明文</description>
  </item>
  <!-- コメント -->
</root>
```

### 主な規則
- ルート要素は1つだけ。
- 開始タグと終了タグは必ず対になる（空要素は `<tag/>` も可）。
- 属性値は引用符で囲む。
- 大文字・小文字を区別する。
- 特殊文字は実体参照へエスケープする:
  - `<` → `&lt;`
  - `>` → `&gt;`
  - `&` → `&amp;`
  - `"` → `&quot;`
  - `'` → `&apos;` または `&#39;`

## 2. よく使う要素・属性の書き方

### テキストとCDATA
```xml
<text>通常のテキスト</text>
<raw><![CDATA[<html>タグをそのまま書きたい場合</html>]]></raw>
```

### 属性
```xml
<item id="abc" count="10" active="true"/>
```

### 名前空間
```xml
<root xmlns:ns="http://example.com/ns">
  <ns:item>名前空間付き要素</ns:item>
</root>
```

## 3. XPathの基本

XPathはXML内のノードを選択する式言語です。XML ViewerのXPath欄で使用できます（XPath 1.0）。

### 基本記法

| 記法 | 意味 | 例 |
| --- | --- | --- |
| `/` | ルートからの絶対パス | `/root/item` |
| `//` | 任意の位置 | `//item` |
| `@` | 属性 | `@id` |
| `[]` | 条件（述語） | `//item[@id='1']` |
| `*` | 任意の要素 | `//item/*` |

### 述語の例
```xpath
//item[@type='example']
//item[position()=1]
//item[last()]
//*[contains(text(),'検索語')]
//item[count(child::*) > 2]
```

### 名前空間を無視する書き方
ビューアでは名前空間接頭辞が解決されないため、以下を推奨します。

```xpath
//*[local-name()='item']
//*[local-name()='item' and @id='1']
```

### 軸の例
```xpath
//item/child::title
//item/parent::*
//item/following-sibling::item
```

## 4. 実践例

```xpath
/bookstore/book[price>30]/title
//book[@category='web']/author
//*[not(@hidden)]
(//section)[1]//p
```

## 5. XPath評価時の注意事項

- XPathは大文字・小文字を厳密に区別します。
- テキストノード（`//text()`）や属性（`//@id`）を指定した場合、ビューア上ではそのノードを内包する親要素がハイライトされます。
- 非常に複雑な式や大量の結果は、ブラウザの描画性能によって表示に時間がかかる場合があります。
- 式のエラーはビューア上で「XPath エラー」と表示されます。

## 6. ビューアで特別扱いされる記法

### LaTeX数式
```xml
<formula latex="\frac{a}{b}"/>
<equation tex="E = mc^2"/>
<math>$$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$$</math>
```
※ `latex` または `tex` 属性を持つ要素、もしくは `formula`, `equation`, `math` 要素内のテキストが KaTeX で描画されます。

### コード
```xml
<code lang="python"><![CDATA[
def f(x):
    return x * 2
]]></code>
```
※ `code`, `source`, `pre`, `script` 要素に `lang` または `language` 属性（`python`, `javascript`, `verilog` 等）を指定するとシンタックスハイライトされます。

### リンク・画像
```xml
<link href="https://example.com"/>
<img src="diagram.png"/>
<ref file="other.xml#section1"/>
```
フォルダを開いて閲覧すると、相対パスの画像や他のXML文書へのリンクが自動解決されます。


## 7. 同梱サンプルと仕様上の注意

- `サンプル/01_操作ガイド.xml` は属性、階層、CDATA、コメント、名前空間、数式、コード、リンク、画像をまとめた教材です。
- `サンプル/chapters/advanced.xml` はフォルダ内相対パスの練習用です。
- XML本文では `&` と `<` のエスケープが必須です。`>` は多くの文脈でそのまま使えますが `]]>` は通常の文字データに直接書けません。引用符は属性値の区切り文字と一致するときエスケープが必要です。
- CDATAの中には `]]>` をそのまま含められません。
- XPath 1.0自体は文字列・数値・真偽値も返せますが、このビューアのXPath欄は**ノード集合**を結果として扱います。例: `count(//item)` は非対応です。件数は `//item` で検索した結果一覧で確認してください。
- 名前空間の接頭辞を解決するXPathリゾルバが未実装なので、名前空間要素には `//*[local-name()='item']` などを利用します。
- 数式描画はKaTeXでサポートされるLaTeX記法の範囲に限られます。
- このビューアは表示・検索ツールであり、XMLのDTD/XSD妥当性検証、XSLT実行、編集保存はできません。
- 「コピー」はXML文書のルート要素を直列化します。XML宣言、DOCTYPE、ルート外のコメントや処理命令は含めません。元ファイルを完全複製する操作ではありません。
