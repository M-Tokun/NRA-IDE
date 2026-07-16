# nra-core 全体整合検査報告

- 検査日: 2026-07-14 JST
- 対象: nra-core配下の基礎文書、papers、implementation、quantum、visualization、ローカル設定
- 参照報告: `03_nra_core_papers_review.md`、`04_nra_core_implementation_review.md`、`05_nra_core_quantum_review.md`、`06_nra_core_visualization_review.md`
- 総合判定: **不合格**

## 1. 結論

nra-coreは、現行v2.1正典に整合する記述と、v1.x以前の固定閾値・直接復元・全面沈黙モデルが同一階層に混在している。さらに、公開Python、量子コード、visualizationに実行不能・算術矛盾・表示と内部値の不一致がある。このため、ディレクトリ名が示す「core」として一貫した実装・説明集合にはなっていない。

## 2. 分野別判定

### 基礎文書・アーキテクチャ

- 現行のSandwich Architectureにある「自由生成停止後も独立した証言を継続」はv2.1と整合する。
- 一方、旧解説・旧語彙・固定境界・Pre-NRA/Post-NRA表現を含む資料が残る。
- `NRA-IDE_Architecture_public.py` は旧版と同一で、tau<=0をFAIL_CLOSED扱いし、非正値tauをinfinityへ変換し、旧状態語彙だけを持つ。OUT_OF_DESCRIPTION_DOMAIN分離およびinfinity変換禁止と不整合。

### papers

- 数式・概念の一部は現行正典と重なるが、版・語彙・境界・沈黙仕様が統一されていない。
- PDFとMarkdown、和文と英文、旧稿と現行稿の位置付けが明示されず、正典・参考・廃止資料の区別が困難。
- 詳細は `03_nra_core_papers_review.md` に記録。

### implementation

- 現行正典の状態集合・多段閾値・不可逆ラッチ・証言継続を一貫実装していない。
- 旧固定閾値、直接補正、状態の復元、非正値tauの不適切処理が残る。
- ドキュメントとコードの意味が一致せず、実装を正典準拠の参照実装として扱えない。
- 詳細は `04_nra_core_implementation_review.md` に記録。

### quantum

- 01/02/03系コードは `expect(sigmaz())` に状態引数がなく、想定どおり実行できない。
- 04/05/06系コードは `destroy(3) * basis(3,i).dag()` の次元が非整合。
- 密度行列の二重適用等、量子状態の扱いにも問題がある。
- 不確定性原理をNRAの蓄積偏差deltaへ直接同一視する説明は物理的・次元的に成立しない。
- 詳細は `05_nra_core_quantum_review.md` に記録。

### visualization

- 検査対象は全体として旧版仕様に基づき、現行正典の説明・実証資料として不合格。
- G(r)の飽和誤認、`R=delta/tau`の算術矛盾、表示tauと計算tauの相違、固定時刻での破綻演出、熱粒子だけの排出演出等がある。
- 複数のAuto Run停止不備、遅延補正競合、外部CDN依存、壊れたHTML構造を確認した。
- 詳細は `06_nra_core_visualization_review.md` に記録。

## 3. 全体を横断する不整合

1. **状態語彙の混在**: NIRVANA、ELASTIC、CRITICAL、ABSTAIN、FAIL_CLOSED等の旧語彙と、v2.1のWARNING、CONFESSION、OUT_OF_DESCRIPTION_DOMAIN、IRREVERSIBLE_BOUNDARY、RUPTUREが混在する。
2. **境界仕様の混在**: 0.4、0.7、0.75、0.8、1.0等の任意固定値と、正典の `R_warn/R_op/R_irrev` が整理されていない。
3. **沈黙仕様の衝突**: 全面沈黙を正直な出力とする旧資料と、独立した証言を継続する現行Sandwich原則が衝突する。
4. **不可逆性の衝突**: 破断・境界超過後にreset、直接補正、tau回復、delta減少を許す実装があり、不可逆ラッチと衝突する。
5. **delta/tau/Rの意味混線**: deltaが累積偏差、瞬時ゆらぎ、遊び、量子不確定性、消費量として使い分けられ、tauも固定容量、動的厚み、指数増幅量として混在する。
6. **熱・バッファの未定義**: 残差の熱排出、バッファ移送、エネルギー保存を称するが、共通の保存量・単位・更新則がない。
7. **証拠と演出の混同**: 期待する結論を描画分岐・固定時刻・別入力へ埋め込み、それをProofまたは構造的帰結と呼ぶ資料がある。

## 4. 優先修正順

1. nra-core直下にmanifestを置き、各ファイルを `canonical / normative implementation / explanatory / experimental / legacy / invalid` に分類する。
2. `NRA-IDE_Architecture_public.py` をv2.1準拠へ更新し、非正値tauをOUT_OF_DESCRIPTION_DOMAINへ分離し、infinity変換を除去する。
3. 正典状態機械を単一の参照実装として作り、papers・quantum・visualizationが独自の閾値・語彙を再定義しない構造にする。
4. 旧HTML、旧PNG、旧論文、実行不能な量子コードを現行coreから隔離する。
5. G(r)の「飽和」表現を全媒体で訂正し、非有界性を明記する。
6. 全コードに最小実行テスト、状態遷移テスト、境界値テスト、ラッチテスト、tau非正値テスト、証言継続テストを追加する。
7. 公開資料の「証明」「物理法則」「唯一」「常に」等の表現を、実証・導出できる範囲へ限定する。

## 5. nra-coreの最終判定

- 正典と整合する部分資料: 存在する。
- ディレクトリ全体の語彙・数式・状態遷移・実装整合: 不成立。
- 参照実装としての実行可能性: 不成立。
- 公開説明資料としての再現性: 不成立。
- 現行coreとしての採用可否: **現状不可。旧版隔離と参照実装の再構築が必要。**

