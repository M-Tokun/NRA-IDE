# NRA-IDE リポジトリ構成およびリンクチェック・レポート (2026/04/26)

## 1. ディレクトリ構成の全体評価とアドバイス

全体として、NRA-IDEは「モノレポ（Monorepo）」的な構成を取っており、共通のドキュメント・理論定義と、各種サブプロジェクト（`gate`, `nra-core`, `nra-ide-cancer-treatment-support-system` 等）が混在している形です。プロジェクトの性質上、様々なモジュールや適用事例が含まれているため妥当な構造ですが、いくつか整理できるポイントがあります。

### 構成上のアドバイス
- **トップレベルドキュメントの整理**:
  ルートに `FORMULA.md` や `GOVERNANCE.md` が配置されていますが、`THEORY.md` や `ETHICS.md` は `theory/` フォルダ配下にあります。どちらかに統一するか、あるいは「中核となる憲章」のみルートに残し、各論は `theory/` や `docs/` に集約すると見通しが良くなります。
- **`note/` フォルダの扱い**:
  雑多なメモやセッション記録が `note/` 配下に蓄積されています。これらが公式なドキュメントでない場合は `.gitignore` で管理外にするか、あるいは `docs/archived_sessions/` のように整理して配置することをおすすめします。
- **サブプロジェクト名が長い**:
  `nra-ide-cancer-treatment-support-system` や `cascade-failure-prevention` など、非常に長いフォルダ名が存在します。コマンドラインでの操作性や視認性を考慮し、`cancer-treatment` や `han-gate` のように簡潔な名前にリネームすることも一案です。

---

## 2. リンク切れ (Broken Links) レポート

スクリプトを用いてリポジトリ内のすべての Markdown ファイルを走査し、相対リンクが正しく機能しているかをチェックしました。以下のファイルにおいて、存在しないファイルへのリンク切れが検出されています。

### `examples/README.md` および `examples/README_JP.md`
- ❌ `./26_escapement_contactpoint_EN_20260425_014259_JST.html`
- ❌ `./NRA-IDE_AgroDrone_4Factor_Simulation_2026-04-20_2041_EN.html`
- ❌ `./37_greenhouse_vpd_correlation_JP_FIXED_20260425_032257_JST.html`
  **【所見】**: 該当する HTML デモファイルが削除されたか、ファイル名が変更されています。

### `GOVERNANCE.md` (ルートディレクトリ)
- ❌ `./ETHICS.md` (2箇所)
  **【所見】**: `ETHICS.md` は現在 `theory/ETHICS.md` に移動されているため、パスを `./theory/ETHICS.md` に修正する必要があります。

### `universal-definition/jp/README_JP.md`
- ❌ `./jp/` への参照、および `./jp/NRA-IDE_Universal_Definition_v1_0_...` など
- ❌ `../LICENSE.txt`
  **【所見】**: ファイル自体がすでに `jp/` ディレクトリの中にあるにも関わらず、さらに `./jp/` を参照しています。親ディレクトリの `README.md` をコピーしてそのまま使っていることが原因と思われます。また、ライセンスファイルも正しくは `../../LICENSE` となります。

### `src/README.md` および `src/README_JP.md`
- ❌ `./LICENSE.md`
  **【所見】**: `src/` ディレクトリ内にローカルのライセンスファイルはありません。ルートの `../LICENSE` を参照するように修正が必要です。

### `gate/jp/README_JP.md`
- ❌ `./nra_gate_axiom_ja.md`
  **【所見】**: 同階層に該当するファイルが存在しません。

### `nra-ide-cancer-treatment-support-system/README_JP.md`
- ❌ `./README_EN.md`
  **【所見】**: 英語版のREADMEがまだ作成されていないか、別階層に存在します。

---

## 3. リポジトリ全体についての所見

1. **品質と意図の明確さ**:
   `README_JP.md` に「存在は生成である」という核公理や、「R = δ/τ」の計算式など、プロジェクトの根本思想が非常に丁寧に記載されています。またGitHub Actions (`nra_check.yml`) が設定されているなど、開発環境の維持に対する意識の高さが伺えます。
2. **階層の深さと参照エラーの多発**:
   Markdownのリンク切れを見てもわかる通り、「ファイルを新しいフォルダへ整理した際に、旧ファイルからのリンクパスを更新し忘れている」ケースが散見されます（例: `ETHICS.md` や `universal-definition` の相対パス）。
3. **今後の推奨アクション**:
   - 上記の「リンク切れリスト」に挙げたファイルのパスを修正する。
   - 今後もファイル移動の際は、依存する `README.md` の相対パス修正を忘れないよう、VSCodeの拡張機能（Markdown Link Checkなど）を活用する。

以上、NRA-IDE リポジトリのディレクトリ構成確認およびリンク切れ精査レポートとなります。
