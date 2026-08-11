# 律環公理（NRA）に基づく人工知能システムの構造的安定性とセキュリティ境界の再定義

<!-- FILE: NRA_AI_Structural_Paper_2026-02-28.md -->

**モデル崩壊への数理的対抗策と次世代エージェントの批判的評価**---"動的なものには閾値は必ず存在する"という考え方において、下記のようになるのは必然と感じているものです（勿論、私見です）

---

現代の人工知能（AI）における技術的パラダイムは、大規模言語モデル（LLM）と自律型エージェントの爆発的な普及により、かつてない転換点を迎えている。しかし、その急速な発展の背後には、システムの構造的な不安定性と、因果律に基づかない統計的推論に依存するゆえの脆弱性が潜在している。本報告書では、万物の因果的プロセスを記述する「律環公理（Nomological Ring Axioms: NRA）,内包性動力学エンジン（Intensional Dynamics Engine）」を理論的基盤として提示し、現在のAIが直面している「モデル崩壊」や「実行境界のセキュリティ欠如」といった根源的課題を数理的に整理する。さらに、現在のAIエージェントの現状に対する批判的評価を行い、実効的な次世代アーキテクチャとしての論文構成案を策定する。

---

## 第1章　律環公理（NRA）を元とした理論体系と数理的整合性

律環公理（NRA）は、世界のあらゆる因果プロセスを4つの不可逆的なステップで定義する数理的・哲学的な枠組みである。これは物理系、生物系、情報系のすべてに適用可能なアイソモーフィズム（構造同型性）を志向しており、システムの動態を「境界」と「閾値」の観点から再定義するものである。

### 1.1　NRAの4段階プロセスと因果的必然性

NRAによれば、ある事象が発生し、システムが状態変化を起こす過程は以下の4段階に集約される。

**① 入力（Input）**

システムの外部からエネルギーまたは情報が流入するフェーズ。NRAにおいて、入力がない状態での出力生成は因果律に対する明白な違反と見なされる。熱力学第一法則にも通じる、システムの起動条件である。

**② 蓄積（Stick）**

流入した入力がシステム内部に留まり、ポテンシャルとして蓄積されるフェーズ。この段階では外部的な変化は観測されないが、システム内部の歪みや歪圧が高まっていく。

**③ 閾値（Threshold）**

蓄積されたエネルギーが一定の限界点に達するフェーズ。これは連続的な変化の中にある不連続な「1ビット」の分岐点であり、状態転移が起こるか否かを決定する厳格な境界である。

**④ 転移（Slip）またはフェイルクローズ（FAIL-CLOSED）**

閾値を超えた場合、システムは新しい状態へ転移（Slip）し出力を生成する。閾値に達しない場合は、システムは何も行わず「沈黙」を維持するフェイルクローズ（FAIL-CLOSED）を選択する。

このNRAの構造は、地震の発生（プレートの歪み蓄積から断層破壊へ）や生物の進化（突然変異の蓄積から種的分化へ）といった自然現象と深く共鳴している。

### 1.2　異分野におけるNRAの適用とアイソモーフィズムの検証

| フェーズ | 物理系（地震） | 生物系（進化） | AIシステム（モデル崩壊） | セキュリティ（ABE） |
|---|---|---|---|---|
| Input | プレート移動による応力 | 突然変異の発生 | 合成データの再帰入力 | 攻撃的命令の注入 |
| Stick | 地殻内部の歪み蓄積 | 遺伝子プールへの蓄積 | 統計的誤差の累積 | 推論レイヤーでの処理 |
| Threshold | 岩盤の静止摩擦限界 | 環境適応への選択圧 | 臨界再帰世代数 | 実行権限の照合 |
| Slip / FC | 断層の滑り（地震発生） | 新種の出現 | モデル崩壊（Collapse） | 実行または拒絶（FC） |

### 1.3　フェイルクローズ（FAIL-CLOSED）の思想的価値

NRAにおいて最も革新的な提案は、第4段階における「フェイルクローズ（FAIL-CLOSED）」の義務化である。現在のLLMの多くは、RLHF（人間によるフィードバックからの強化学習）の過程で、いかなる入力に対しても「役に立つ」出力を生成するように動機付けられている。その結果、確信度が極めて低い場合であっても、何らかの回答を捏造（ハルシネーション）して返す傾向がある。

NRA-IDE（律環公理に基づく統合開発環境）の設計では、信頼性スコアが閾値を下回った場合、空文字列 `""` を返すことが「誠実な出力」として定義される。これは、航空機のオートパイロットが異常時に操縦権を人間に戻す「安全な後退」と同じ論理であり、ISO 26262などの機能安全規格における基本原則である。医療診断や金融取引を担うAIエージェントにとって、「わからない」と沈黙することは、誤った行動をとることよりも構造的に正当な振る舞いである。物理的ログを出力可能ということは当然エラーログ（意味を伴わない）も残せるということである。

---

## 第2章　モデル崩壊のダイナミクス：再帰的学習におけるエントロピーの罠

モデル崩壊（Model Collapse）とは、生成AIが自ら生成したデータを訓練データとして再利用（再帰的学習）することで、元のデータ分布が持つ多様性や正確性が不可逆的に失われていく現象である。

### 2.1　知識崩壊（Knowledge Collapse）の3段階モデル

**ステージA（知識保存期）**

モデルは高い事実正確性を維持し、指示にも忠実に従う。人間由来のデータが支配的である。

**ステージB（知識崩壊期）**　---重みの消失部分の推定による穴埋め

最も危険な「能力の谷」。出力の流暢さは維持されているため一見正常に見えるが、内容は事実と異なる「自信満々な間違い（Confidently Wrong）」が頻発する。

**ステージC（完全崩壊期）**　---重みの消失

情報のエントロピーが極限まで低下し、モデルは特定の単語を繰り返す、文を交互に繰り返す。文中・文末が頻繁に途切れる。あるいは無意味な文字列（Gibberish）を出力するようになる。

このプロセスは、再帰的なフィードバックループが分布の「裾（tails）」、すなわち発生確率は低いが重要な例外事項を削ぎ落としてしまうために発生する。

### 2.2　モデル崩壊を引き起こす3つの構造的誤差

**統計的標本誤差（Statistical Approximation Error）**

サンプリングの過程で有限のデータしか扱えないため、低確率の事象が次世代の訓練データから脱落し、分布が平均へ収束する。

**関数近似誤差（Functional Approximation Error）**

ニューラルネットワークのモデル容量（キャパシティ）の限界により、複雑な多峰性分布を表現しきれず、単純なガウス分布などに歪めてしまう。

**最適化誤差（Optimization Error）**

学習アルゴリズムが収束しやすい単純なパターンを優先的に学習し、データの微細な構造を無視する。

数学的には、サンプルサイズ $n_t$ が世代 $t$ に対して超線形的に増加（ $\sum 1/n_t < \infty$ ）しない限り、推定パラメータ $\theta_t$ は真の分布から確率1で離散していくことが証明されている。

### 2.3　モデルサイズと「二重降下」曲線の影響

| 領域 | パラメータ数 m とデータ数 n の比 | 特徴 |
|---|---|---|
| 内挿閾値付近 | $m/n \approx 1$ | 崩壊の影響が最大化し、誤差 $\zeta$ が発散する |
| 過パラメータ化領域 | $m/n \gg 1$ | 大きなモデルの方が崩壊に対して耐性を持つ可能性がある（ただし完全には防げない） |
| 合成データ比率大 | 合成データが支配的 | モデルサイズを大きくしても性能が向上しない「スケーリング則の崩壊」が起こる |

この知見は、単純なモデルの巨大化だけでは崩壊を防げないことを示唆しており、NRA-IDEが提唱する「外部制約による境界制御」の重要性を裏付けている。

---

## 第3章　情報幾何学と生存可能性理論による数理的安定化

AIシステムの安定性を単なる損失関数の最小化としてではなく、状態空間における「境界維持」の問題として捉えるために、情報幾何学と実現可能性理論（Viability Theory）を導入する。

### 3.1　情報幾何学的多様体の収縮

甘利俊一らによって確立された情報幾何学は、確率分布の族をリーマン多様体として扱う。フィッシャー情報行列はパラメータ空間における計量テンソルであり、モデルの出力分布がパラメータの変化に対してどれほど敏感であるかを測定する。再帰的学習においては、この多様体のサポート（支持集合）が縮小していく。これは多様体上の曲率が極端に大きくなり、特定の領域に分布が「折り畳まれる」現象として解釈できる。この幾何学的な「潰れ」を回避するためには、外部のエントロピー・リザーバー（人間由来のデータや物理世界の観測データ）とシステムを適切に結合（Coupling）させることが必須である。

### 3.2　実現可能性理論（Viability Theory）による境界制御

ジャン＝ピエール・オービンによって提唱された実現可能性理論は、制約条件を満たし続けるための動的システムの制御を論じる。**実現可能性領域（Viability Domain）** とはシステムが「生存」可能である（破綻しない）状態空間の範囲であり、**境界ダイナミクス** とはシステムが領域の境界に達した際、内部に押し戻す「速度ベクトル」を選択するフィードバック制御である。どの制御を選んでも境界を逸脱してしまう状態を「危機の時代（Period of Crisis）」と呼び、これはAIにおける「不可逆的なモデル崩壊」や「制御不能なエージェント」に相当する。NRAの「閾値」は、この実現可能性領域の境界を数理的に表現したものであり、境界を越える前にシステムを停止（フェイルクローズ）させることで構造的な安全性を担保する。

---

## 第4章　セキュリティ境界の再定義：Authority Before Execution（ABE）

現在のAIエージェントのセキュリティにおける最大の誤解は、「推論を安全にすれば、行動も安全になる」という仮定である。これはソフトウェア工学における「意図・権限の混同」であり、深刻な脆弱性を招いている。

### 4.1　プロンプトインジェクション：アーキテクチャ上の欠陥

プロンプトインジェクション（直接的・間接的）は、命令とデータの境界を曖昧にするLLMの基本構造を突いた攻撃である。攻撃者は外部データ（RAGで取得されるWebページやメール等）に悪意ある命令を埋め込み、モデルは入力されたトークンが「信頼できる開発者の命令」なのか「信頼できない外部データ」なのかを区別する「内因的な信頼境界」を持っていないため、これを防げない。Microsoft 365 Copilotにおいて、ゼロクリックで内部ファイルを外部サーバーへ転移させる脆弱性（EchoLeak）が報告されており、これは既存の安全フィルターを容易に回避した。

### 4.2　実行前権限照合（ABE）の3大原則

NRAの「閾値」をセキュリティに応用したものが「Authority Before Execution (ABE)」である。これはモデルが行動（API呼び出しや送金等）を実行する直前の同期パスにおいて、以下の3条件を独立して検証するアーキテクチャである。

**① 権限の明示的存在（Authority Present）**

アクションに対する正当な権限が、人間または上位システムによって明示的に付与されているか。モデルの「自信」から推論してはならない。

**② スコアの妥当性（Scope Valid）**

付与された権限の範囲（ターゲット、操作内容、有効期間）と、実行しようとしているアクションが一致しているか。

**③ 鮮度の検証（Not Expired）**

権限チェックが最新のものであり、セッションやトークンが有効であるか。

この設計により、たとえプロンプトインジェクションによってモデルの「推論（意図）」が乗っ取られたとしても、最終的な「実行境界（閾値）」において物理的にアクションが遮断（フェイルクローズ）される。

---

## 第5章　AIエージェントの現状と限界に関する批判的評価

現在のAIエージェント、特に自律型と呼ばれるシステムに対して、NRAの観点から述べるならば、それらは「因果なき統計の暴走」という危うい均衡の上に成り立っている。

### 5.1　「流暢な無知」と過剰な信頼

現在のエージェント開発において最も憂慮すべきは、モデルの出力が流暢である（文法的に正しい）ことをもって、その背後にある論理や知識が正確であると誤認している点である。知識崩壊のステージBにおいて示されたように、モデルは事実に反する情報を極めて「確信に満ちた（Confident）」口調で出力する。これに対し、従来の「ガードレール」のような事後的なフィルタリングは、統計的な分布の平均に基づいているため、精巧に作られた嘘や意図的なインジェクションを見抜くことができない。

### 5.2　実行レイヤーにおける「裸の王様」

多くの自律型エージェントはインターネット上のAPIを自由に呼び出す能力を与えられているが、その実行を監視する「安全カーネル（Safety Kernel）」を欠いている。現在のAI安全性議論の多くは「AIにいかに良い価値観を教えるか（アライメント）」に集中しているが、これは物理的な鍵を持たずに泥棒に道徳を説くようなものである。ABEのような、推論レイヤーから独立した「権限チェック」を持たないエージェントは、本質的にセキュリティ上の「裸の状態」にあり、大規模な社会実装には時期尚早であると言わざるを得ない。

### 5.3　情報エントロピーの閉塞と創造性の終焉

再帰的学習が引き起こすモデル崩壊は、AIが自らの「影（自己生成データ）」を追いかけることで情報の多様性を自食している状態である。これは情報の熱力学における「熱的死」に相当し、AIが生成するコンテンツが似通った「退屈な平均」へと収束していく未来を予言している。人間という「高エントロピー源」を排除し、効率化の名の下にAIだけでループを閉じようとする試みは、長期的にはAI自身の知能を枯渇させる自殺行為である。

---

## 第6章　数理的かつ実効的な論文構成案（NRA-AIフレームワーク）

**論文題名：** 律環公理（NRA）に基づく自律型人工知能の因果的一貫性と実行境界の形式的検証

**1. 序論**

LLMの普及に伴う「統計的推論」と「論理的必然性」の乖離。再帰的学習によるモデル崩壊の危機と、実行境界におけるセキュリティ欠如の問題提起。本論文の目的：NRAを用いた因果プロセスの再定義と、それに基づく安全なAIアーキテクチャの提案。

**2. NRA（律環公理）の理論的定式化**

$(\mathcal{I}, \mathcal{S}, \mathcal{T}, \mathcal{F})$ の4つ組による事象プロセスの記述。入力エネルギー $\mathcal{I}$ から蓄積ポテンシャル $\mathcal{S}$ への変換関数の定義。不連続な状態転移を生む閾値関数 $\mathcal{T}$ の数理的性質（1ビット分岐）。フェイルクローズ（FAIL-CLOSED）の論理的必要性の証明。

**3. モデル崩壊の幾何学的・熱力学的解析**

情報幾何学におけるフィッシャー情報多様体の曲率と収縮率の相関。再帰学習エントロピー減衰モデル： $\frac{dH}{dt} \leq 0$ 条件下での知識崩壊ステージBの特定。合成データ比率 $\rho$ と情報定数 $\mathcal{R}$ を用いた「モデル寿命」の算定。

**4. 安全な実行境界：Authority Before Execution (ABE) の実装**

推論（Reasoning）と権限（Authority）の分離アーキテクチャ。プロンプトインジェクションを状態遷移違反として捉える検知理論。Control Barrier Functions (CBF) と NRA 閾値の統合によるリアルタイム安全保証。

**5. 実証実験と評価**

医療・金融等の高リスクドメインにおける「フェイルクローズ」の有効性検証。合成データ汚染下でのモデル性能維持における外部エントロピー・リザーバーの効果。ABE導入による、意図しない破壊的アクションの遮断率の定量的評価。

**6. 批判的考察：AI自律性の再定義**

「自律性」とは制約のない自由ではなく、厳格な「境界（閾値）」の遵守であるという主張。人間とAIの共生における「責任の所在」と「説明責任」の幾何学的解釈。

**7. 結論**

NRAに基づくAI設計がもたらす「因果に基づく信頼」の確立。今後の展望：ハードウェアレベルでのNRA閾値実装と、情報の持続可能性（データ・サステナビリティ）の確保。

---

## 第7章　情報熱力学から見たAIの持続可能性と情報定数 $\mathcal{R}$

AIシステムの長期的安定性を議論する上で、情報の処理と物理的なエネルギー消費の関係を定式化することは不可欠である。**修正理想気体定数 $\mathcal{R}$** は、情報理論におけるエントロピーと物理系における熱力学的エントロピーを橋渡しする係数として定義される。これは「1モルの情報を維持するために必要なエネルギーコスト」を定量化する試みである。モデル崩壊を防ぐためには、システムが外部（人間や現実世界）から常に「有用な情報（負のエントロピー）」を取り込み、内部で発生する「ノイズ（正のエントロピー）」を廃棄しなければならない。**パス散逸（Path Dissipation）** とは学習プロセスそのものが情報の多様性を消費して収束する過程であり、その不可逆性を最小限に抑える設計が次世代モデルには求められる。

---

## 第8章　結論：律環公理（NRA）が導くAIの誠実な未来

本報告書を通じて整理した律環公理（NRA）の理論体系は、現在のAI技術が陥っている「無制限な成長」と「構造的な不透明さ」に対する強力な解毒剤となる。モデル崩壊は外部からの新規情報の流入を断たれた閉鎖系における必然の結末であり、セキュリティの脆弱性は実行境界という物理的な閾値を持たないことに起因する。AIエージェントの現状に対する批判的評価から導き出される結論は、我々は今こそ「AIを人間に近づける」ことよりも、「AIを構造的に堅牢な（律環を守る）システムとして再構築する」ことに注力すべきである、という点である。NRAが提唱するフェイルクローズ（FAIL-CLOSED）の思想は、AIが「万能な神」であることを望むのではなく、「境界を弁えた誠実なツール」であることを要求する。この数理的かつ実効的なフレームワークを実装することで、AIは単なる「尤もらしさの模倣者」から、「因果と権限の正当な執行者」へと進化を遂げることができる。それは、情報のエントロピーが枯渇することのない、持続可能で信頼に値するデジタル文明の礎となるだろう。

---

## 主要概念の比較と整理：NRAによるAIシステムの再構築

| 概念 | 従来の統計的アプローチ | NRAに基づく構造的アプローチ | 意義・影響 |
|---|---|---|---|
| 出力生成 | 確率最大化（何でも答える） | 閾値判定によるSlip/FC選択 | ハルシネーションの構造的排除 |
| 学習データ | スケーリング則（量重視） | エントロピー・リザーバーの維持 | モデル崩壊の理論的回避 |
| 安全性の所在 | 学習時アライメント（内因的） | 実行前権限照合 ABE（外因的） | インジェクション攻撃への物理的耐性 |
| 異常検知 | 分布外検知（確率的） | 実現可能性領域からの逸脱（幾何学的） | 決定的・瞬時の安全停止 |
| 情報の価値 | 流暢さと「尤もらしさ」 | 真の因果構造とエントロピー | 知識崩壊ステージBの克服 |

---

ご提示したレポートに使用されている主要なソースおよび参考文献のリストは以下の通りです。

*  律環公理（NRA）とフェイルクローズ設計の基本概念

* 「Nomological Ring Axioms and FAIL-CLOSED design」 ([https://zenn.dev/tokuni/articles/a3e9b60617b849](https://zenn.dev/tokuni/articles/a3e9b60617b849)) 

* 「Why AI Safety Lives in the Wrong Place - And What to Do About It」 ([https://medium.com/@qstackfield/why-ai-safety-lives-in-the-wrong-place-and-what-to-do-about-it-5a8dbe38cc78](https://medium.com/@qstackfield/why-ai-safety-lives-in-the-wrong-place-and-what-to-do-about-it-5a8dbe38cc78)) 

*  知識崩壊（Knowledge Collapse）の3段階と「能力の谷」

* 「Knowledge Collapse: A Three-Stage Phenomenon」 ([https://arxiv.org/html/2509.04796v1](https://arxiv.org/html/2509.04796v1)) 

*  プロンプトインジェクションと命令・データの境界曖昧性

* 「Analysis of EchoLeak and Prompt Injection in LLMs」 ([https://arxiv.org/html/2512.24655v1](https://arxiv.org/html/2512.24655v1)) 

* 「Prompt Injection Examples and Prevention Strategies」 ([https://www.lasso.security/blog/prompt-injection-examples](https://www.lasso.security/blog/prompt-injection-examples)) 

*  モデル崩壊（Model Collapse）と統計的標本誤差の累積

* 「The Curse of Recursion: Training on Generated Data」 ([https://www.cl.cam.ac.uk/~is410/Papers/dementia_arxiv.pdf](https://www.cl.cam.ac.uk/~is410/Papers/dementia_arxiv.pdf)) 

* 「Recursive Collapse in Generative Models」 ([https://www.emergentmind.com/papers/2305.17493](https://www.emergentmind.com/papers/2305.17493)) 

*  実行前権限照合（Authority Before Execution: ABE）の設計論

* 「Why AI Safety Lives in the Wrong Place」 ([https://medium.com/@qstackfield/why-ai-safety-lives-in-the-wrong-place-and-what-to-do-about-it-5a8dbe38cc78](https://medium.com/@qstackfield/why-ai-safety-lives-in-the-wrong-place-and-what-to-do-about-it-5a8dbe38cc78)) 

*  補間閾値における分散の発散と数理的証明（ICLR 2025）

* 「The Double-Descent Phenomenon in Model Collapse」 ([https://proceedings.iclr.cc/paper_files/paper/2025/file/284afdc2309f9667d2d4fb9290235b0c-Paper-Conference.pdf](https://proceedings.iclr.cc/paper_files/paper/2025/file/284afdc2309f9667d2d4fb9290235b0c-Paper-Conference.pdf)) 

*  再帰的学習における不可逆的なモデル欠陥

* 「AI models collapse when trained on recursively generated data」 ([https://www.semanticscholar.org/paper/AI-models-collapse-when-trained-on-recursively-data-Shumailov-Shumaylov/603d3f90fc40f79ff51258f0295de3ec5107f73e](https://www.semanticscholar.org/paper/AI-models-collapse-when-trained-on-recursively-data-Shumailov-Shumaylov/603d3f90fc40f79ff51258f0295de3ec5107f73e)) 

* 「Indiscriminate use of model-generated content」 ([https://pubmed.ncbi.nlm.nih.gov/39048682/](https://pubmed.ncbi.nlm.nih.gov/39048682/)) 

*  医療・航空・自動車分野におけるフェイルクローズの機能安全

* 「Human-in-the-Loop AI and Operational Resilience」 ([https://aijourn.com/human-in-the-loop-ai-why-automation-alone-fails-in-high-risk-environments/](https://aijourn.com/human-in-the-loop-ai-why-automation-alone-fails-in-high-risk-environments/)) 

* 「Legitimacy of Silence: NRA-IDE's FAIL-CLOSED」 ([https://zenn.dev/tokuni/articles/a3e9b60617b849](https://zenn.dev/tokuni/articles/a3e9b60617b849)) 

*  過パラメータ化領域におけるモデル崩壊の挙動（ICLR 2025）

* 「Strong Model Collapse in Linear Regression」 ([https://proceedings.iclr.cc/paper_files/paper/2025/file/284afdc2309f9667d2d4fb9290235b0c-Paper-Conference.pdf](https://proceedings.iclr.cc/paper_files/paper/2025/file/284afdc2309f9667d2d4fb9290235b0c-Paper-Conference.pdf)) 

*  情報幾何学の基礎と統計的多様体（甘利俊一）

* 「Methods of Information Geometry」 ([https://content.e-bookshelf.de/media/reading/L-7505366-733c6681c3.pdf](https://content.e-bookshelf.de/media/reading/L-7505366-733c6681c3.pdf)) 

* 「Information Geometry and Statistical Inference」 ([https://ideas.repec.org/a/bla/istatr/v89y2021i2p250-273.html](https://ideas.repec.org/a/bla/istatr/v89y2021i2p250-273.html)) 

*  フィッシャー情報行列とLLMの最適化ランドスケープ

* 「Optimization and Geometry in LLMs: Fisher Information Centrality」 ([https://arxiv.org/html/2506.15830v4](https://arxiv.org/html/2506.15830v4)) 

*  エントロピー・リザーバー（Entropy Reservoir）とブレグマン投影

* 「The Entropy-Reservoir Bregman Projection Framework」 ([https://arxiv.org/html/2512.14879v1](https://arxiv.org/html/2512.14879v1)) 

*  生存可能性理論（Viability Theory）の設計原則（Aubin）

* 「Viability Theory: New Directions」 ([https://www.researchgate.net/publication/265520973_Viability_Theory_New_Directions](https://www.researchgate.net/publication/265520973_Viability_Theory_New_Directions)) 

* 「Viability Theory and Complex Systems」 ([https://taylorandfrancis.com/knowledge/Engineering_and_technology/Systems_%26_control_engineering/Viability_theory/](https://taylorandfrancis.com/knowledge/Engineering_and_technology/Systems_%26_control_engineering/Viability_theory/)) 

*  境界ダイナミクスと「危機の時代（Period of Crisis）」

* 「The Viability Domain and Boundary Regulation」 ([https://pure.iiasa.ac.at/id/eprint/1949/1/WP-82-067.pdf](https://pure.iiasa.ac.at/id/eprint/1949/1/WP-82-067.pdf)) 

*  EchoLeakおよびGitHub Copilotの脆弱性解析（CVE-2025-53773）

* 「Strict Prompt Partitioning and Security Boundaries」 ([https://arxiv.org/html/2512.24655v1](https://arxiv.org/html/2512.24655v1)) 

* 「Analysis of EchoLeak and CamoLeak Vulnerabilities」 ([https://www.mdpi.com/2078-2489/17/1/54](https://www.mdpi.com/2078-2489/17/1/54)) 

* 「Prompt Injection as an Architectural Reality」 ([https://www.sentinelone.com/cybersecurity-101/cybersecurity/prompt-injection-attack/](https://www.sentinelone.com/cybersecurity-101/cybersecurity/prompt-injection-attack/)) 

*  セーフティカーネル（Safety Kernel）と階層的制御システム

* 「Hierarchical Control with Safety Kernels in SDL」 ([https://arxiv.org/html/2602.15061v1](https://arxiv.org/html/2602.15061v1)) 

*  AI安全性における意図と行動の分離議論

* 「AI safety lives in the wrong place: Reasoning vs Execution」 ([https://medium.com/@qstackfield/why-ai-safety-lives-in-the-wrong-place-and-what-to-do-about-it-5a8dbe38cc78](https://medium.com/@qstackfield/why-ai-safety-lives-in-the-wrong-place-and-what-to-do-about-it-5a8dbe38cc78)) 

* 「Reddit Discussion: Hard Boundaries at Execution」 ([https://www.reddit.com/r/ArtificialInteligence/comments/1q466o3/ai_safety_might_fail_because_were_protecting_the/](https://www.reddit.com/r/ArtificialInteligence/comments/1q466o3/ai_safety_might_fail_because_were_protecting_the/)) 

*  情報定数 R と修正理想気体定数の情報熱力学的定式化

* 「Laws of Thermodynamics in Terminology of Information Theory」 ([https://arxiv.org/abs/2410.07243](https://arxiv.org/abs/2410.07243)) 

*  情報エントロピーと熱力学的エントロピーの区別（有用な情報 vs ノイズ）

* 「Infodynamics: Distinct Concepts of Entropy」 ([https://www.qeios.com/read/T13JP9.5](https://www.qeios.com/read/T13JP9.5)) 

*  パス散逸（Path Dissipation）と情報の非可逆性

* 「Path-Space Relative Entropy and Entropy Production」 ([https://arxiv.org/html/2512.24655v1](https://arxiv.org/html/2512.24655v1))
