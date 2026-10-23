# リンドブラッド方程式（GKSL形式）：式の読み方と成立条件

**文書の役割：** 外部技術用語の詳説。NRA-IDEの正典を定義・変更する文書ではない  
**辞書項目：** [リンドブラッド方程式（GKSL形式）](../Glossary_JP.md#^qh-lindblad-equation)  
**対になる英語版：** [Lindblad_GKSL_EN.md](./Lindblad_GKSL_EN.md)  
**更新日：** 2026-10-24  
**状態：** 【草稿】【概念未照合】【全文対訳未確認】

**関連する辞書項目：** [開放量子系](../Glossary_JP.md#^qh-open-quantum-system)、[ハミルトニアン](../Glossary_JP.md#^qh-hamiltonian)、[純粋状態](../Glossary_JP.md#^qh-pure-state)、[混合状態](../Glossary_JP.md#^qh-mixed-state)、[マルコフ近似](../Glossary_JP.md#^qh-markov-approximation)、[ボルン近似（Born近似）](../Glossary_JP.md#^qh-born-approximation)、[永年近似](../Glossary_JP.md#^qh-secular-approximation)、[完全正値性](../Glossary_JP.md#^qh-complete-positivity)、[完全正値・トレース保存写像（CPTP）](../Glossary_JP.md#^qh-cptp-map)、[半群（量子力学的半群）](../Glossary_JP.md#^qh-dynamical-semigroup)

## 1. 式と全体の意味

この式はLindblad（リンドブラッド）方程式、またはGKSL方程式（Gorini–Kossakowski–Sudarshan–Lindblad方程式）と呼ばれる。環境と相互作用する「開放量子系」の、マルコフ型の時間発展を扱う基本的な形式である。あらゆる開放量子系を無条件に記述する式ではない。

以下は有限次元の系を基本とし、単位系は $\hbar=1$ とする。Hはエルミートなハミルトニアンで、必要に応じて環境によるエネルギー準位のずれなどの有効項も含む。時間を秒で表すと、Hはエネルギーを $\hbar$ で割った角周波数の単位で読む。

$$
\dot{\rho}
=
-i[H,\rho]
+
\sum_k\left(
L_k\rho L_k^\dagger
-\frac{1}{2}\{L_k^\dagger L_k,\rho\}
\right).
$$

| 記号 | 意味 |
|---|---|
| $\rho$ | 系の[密度行列](../Glossary_JP.md#^qh-density-matrix)。量子状態を表す |
| $\dot{\rho}$ | 密度行列の時間微分 |
| H | ハミルトニアン。系のエネルギーと可逆的な動きを定める演算子 |
| $L_k$ | Lindblad演算子、ジャンプ演算子、または崩壊演算子（collapse operator）。環境に関わる過程の作用と強さを表す |
| k | 過程を区別する添字 |
| $\dagger$ | 複素共役をとって転置する随伴 |
| I | 恒等演算子 |
| $\operatorname{Tr}$ | 行列の対角成分の和（トレース） |

時間微分、交換子、反交換子の定義は次のとおり。

$$
\dot{\rho}=\frac{\mathrm{d}\rho}{\mathrm{d}t},
\qquad [A,B]=AB-BA,
\qquad \{A,B\}=AB+BA.
$$

第1項はハミルトニアンによるユニタリー発展、第2項は環境に関わる非ユニタリーな効果を表す。代表例はエネルギー緩和、純粋位相緩和、光子漏れである。純粋位相緩和は、エネルギー交換を伴わずに[量子コヒーレンス](../Glossary_JP.md#^qh-quantum-coherence)を減衰させる過程を指す。

## 2. 第1項：閉じた系のフォン・ノイマン方程式

環境項がない場合は、密度行列に対するフォン・ノイマン方程式になる。

$$
\dot{\rho}=-i[H,\rho].
$$

これはユニタリーな時間発展である。ただし「相対位相が常に固定される」「選んだ基準でのコヒーレンスが常に同じ」という意味ではない。ハミルトニアンは[相対位相](../Glossary_JP.md#^qh-quantum-phase)を変化させ得る。

系のエネルギー[期待値](../Glossary_JP.md#^qh-expectation-value)が保存されるのは、ここで用いるHが時間に依存しない場合である。時間依存する外部駆動があれば、ユニタリー発展でも系のエネルギーは変わり得る。この単位系での関係は、

$$
\frac{\mathrm{d}}{\mathrm{d}t}\operatorname{Tr}(H(t)\rho(t))
=
\operatorname{Tr}(\dot{H}(t)\rho(t))
$$

となる。閉じた系の説明と、外部から仕事が加わる駆動系の説明を混同しない。

## 3. 第2項：散逸子

第2項全体を散逸子（dissipator）と呼ぶ。

$$
\mathcal{D}[\rho]
=
\sum_k\left(
L_k\rho L_k^\dagger
-\frac{1}{2}\{L_k^\dagger L_k,\rho\}
\right).
$$

この呼び名にかかわらず、すべての項が必ずエネルギーを減らすとは限らない。純粋位相緩和、熱による励起なども、適切な演算子を用いて扱える。

結合を表す演算子と係数を分ける場合は、次のように書ける。

$$
L_k=\sqrt{\gamma_k}\,A_k,
\qquad \gamma_k\geq0.
$$

無次元の $A_k$ を採ると、$\gamma_k$ の単位は毎秒、$L_k$ の単位は秒のマイナス2分の1乗となる。上の主方程式では速度係数を $L_k$ に含めているため、同じ係数を散逸子の外へ重ねて掛けない。

また、$\gamma_k$ という係数名だけで観測量の減衰速度が決まるわけではない。演算子の規格化と、どの量の減衰を指すかも指定する。位相緩和の係数の例は§6に示す。

## 4. ジャンプ項と非ジャンプ項の読み方

量子ジャンプによる一つの表現では、最初に正規化された状態から、短い時間に各過程が起こる確率を扱う。ジャンプ項そのものは、正規化された「ジャンプ後の状態」ではない。

$$
L_k\rho L_k^\dagger.
$$

この行列のトレースがジャンプの発生率に対応する。微小時間の確率と、ジャンプを条件とした正規化後の状態は、

$$
p_k(\mathrm{d}t)
=
\mathrm{d}t\,
\operatorname{Tr}(L_k\rho L_k^\dagger)
+O((\mathrm{d}t)^2),
\qquad
\rho_k^{\mathrm{jump}}
=
\frac{L_k\rho L_k^\dagger}
{\operatorname{Tr}(L_k\rho L_k^\dagger)}
$$

である。分母がゼロならその過程の発生率はゼロであり、この条件付き状態を割り算で作らない。

ジャンプしない経路の非正規化状態には、次の演算子が働く。

$$
K_0
=
I-\left(iH+\frac{1}{2}\sum_k L_k^\dagger L_k\right)\mathrm{d}t
+O((\mathrm{d}t)^2).
$$

その状態は次で表され、トレースはジャンプしなかった確率に対応する。

$$
K_0\rho K_0^\dagger.
$$

非ジャンプ項は単にノルムを1へ戻す項ではない。条件付きの状態そのものも変化させる。反交換子の項だけではトレースを保存せず、ジャンプ項と合わせた全体が確率を保存する。こうしたジャンプの説明は環境の監視に対応する一つの表現であり、すべての実験で個別のジャンプを直接観測するという意味ではない。[QuTiPの量子ジャンプ解説](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-monte.html)も参照。

## 5. 確率保存とCPTP

有限次元ではトレースの巡回性により、各過程について次が成り立つ。

$$
\begin{aligned}
\operatorname{Tr}\!\left(
L_k\rho L_k^\dagger
-\frac{1}{2}\{L_k^\dagger L_k,\rho\}
\right)
&=
\operatorname{Tr}(L_k^\dagger L_k\rho)
-\frac{1}{2}\operatorname{Tr}(L_k^\dagger L_k\rho)
-\frac{1}{2}\operatorname{Tr}(\rho L_k^\dagger L_k)
\\
&=0.
\end{aligned}
$$

交換子のトレースもゼロなので、初期状態のトレースが1なら、

$$
\frac{\mathrm{d}}{\mathrm{d}t}\operatorname{Tr}\rho
=
\operatorname{Tr}\dot{\rho}
=0,
\qquad
\operatorname{Tr}\rho(t)=1
$$

が保たれる。ただしトレースが1という条件だけでは、負の確率を生まないことまでは保証しない。

GKSL形式が重要なのは、適切な条件下で**完全正値かつトレース保存（CPTP）**の時間発展を与える点にある。

- 正値性：密度行列の半正定値性を保ち、測定確率を負にしない。
- 完全正値性：相関した補助量子系を含めても、対象への操作によって全体の正値性を壊さない。
- トレース保存：測定確率の総和を1に保つ。

厳密に「最も一般的」といえる代表的な範囲は、**有限次元・時間一様で連続なCPTP量子力学的半群の生成子**である。時間一様とは、経過時間が同じなら同じ写像を用いるという意味である。一定のHと $L_k$ からなる生成子を $\mathcal{L}$ とすると、

$$
\Phi_t=e^{t\mathcal{L}},
\qquad
\Phi_{t+s}=\Phi_t\circ\Phi_s,
\qquad t,s\geq0
$$

という半群の性質をもつ。[Gorini–Kossakowski–Sudarshanの論文要旨](https://repository.ias.ac.in/51137/)と[Lindbladの論文要旨](https://link.springer.com/article/10.1007/BF01608499)が、この一般形の対象を示している。

時間依存するHや、非負の速度係数を用いる時間依存GKSL形式も、適切な正則性のもとでCPTP発展を与える。ただし一般には時間一様な半群ではない。「すべての開放系」「すべてのマルコフ性の定義」に対して、条件なしに最一般という説明はしない。

## 6. よく使われる例と速度係数

### 自発放出・エネルギー緩和

励起状態をe、基底状態をgとし、下げ演算子を次で定義する。

$$
\sigma_-=\lvert g\rangle\langle e\rvert,
\qquad
L=\sqrt{\gamma}\,\sigma_-,
\qquad \gamma\geq0.
$$

外部駆動や上向きの励起がないモデルでは、励起状態の割合は次のように減衰する。

$$
\dot{\rho}_{ee}=-\gamma\rho_{ee},
\qquad
\rho_{ee}(t)=\rho_{ee}(0)e^{-\gamma t},
\qquad T_1=\frac{1}{\gamma}\quad(\gamma>0).
$$

[T₁の項目](../Glossary_JP.md#^qh-energy-relaxation-time-t1)の指数減衰モデルに対応する。

### 純粋位相緩和

ここでは $\gamma_\phi$ を、エネルギー交換を伴わない**非対角成分の減衰率**と定義する。この規約では、

$$
L=\sqrt{\frac{\gamma_\phi}{2}}\,\sigma_z,
\qquad
\sigma_z=
\begin{pmatrix}
1&0\\
0&-1
\end{pmatrix},
\qquad \gamma_\phi\geq0
$$

と置くと、ハミルトニアン項を除いたこの散逸子の寄与は、

$$
\mathcal{D}[\rho]
=
\frac{\gamma_\phi}{2}(\sigma_z\rho\sigma_z-\rho),
\qquad
\dot{\rho}_{01}=-\gamma_\phi\rho_{01},
\qquad
\dot{\rho}_{00}=\dot{\rho}_{11}=0
$$

となる。元の例のように係数の2分の1を入れずに書くことも数学的には有効だが、その場合の非対角成分の減衰率は次のように2倍になる。

$$
L=\sqrt{\gamma_\phi}\,\sigma_z
\quad\Longrightarrow\quad
\dot{\rho}_{01}=-2\gamma_\phi\rho_{01}.
$$

したがって、$\gamma_\phi$ を純粋位相緩和率として読むなら、係数の規約を明示する必要がある。エネルギー緩和も含む場合は、独立な指数減衰過程を足し合わせるモデルに限って、

$$
\frac{1}{T_2}
=
\frac{1}{2T_1}+\gamma_\phi
$$

となる。[T₂の項目](../Glossary_JP.md#^qh-coherence-time-t2)と併せて読む。すべての非指数的な雑音過程へ一般化しない。

### 光キャビティの光子漏れ

キャビティは光を閉じ込める共振器、aは光子数を一つ減らす消滅演算子である。漏れの項を次で表す。

$$
L=\sqrt{\kappa}\,a,
\qquad \kappa\geq0.
$$

駆動・熱励起のない損失だけのモデルでは、平均光子数の減衰率と、場の振幅の減衰率は異なる。以下は散逸子の寄与だけを示し、自由ハミルトニアンによる位相回転を除く。

$$
\frac{\mathrm{d}}{\mathrm{d}t}\langle a^\dagger a\rangle
=-\kappa\langle a^\dagger a\rangle,
\qquad
\frac{\mathrm{d}}{\mathrm{d}t}\langle a\rangle
=-\frac{\kappa}{2}\langle a\rangle.
$$

無限次元の光子系では、演算子の定義域や数値計算での光子数打切りも別途確認する。有限次元の一般形に関する説明を、そのまま無条件で拡張しない。

## 7. 導出の近似と適用範囲

実際の系・環境モデルからこの形を導く典型的な手順では、次の仮定を使う。

- 弱結合／Born近似：環境に対する系の影響を小さいものとして扱い、系と環境の相関を近似する。
- マルコフ近似：環境の相関時間が系の緩和時間に比べて短く、環境の記憶を無視できるとする。
- 永年近似：異なる遷移周波数による速い振動項を適切な時間平均で除く。回転波近似と関係するが、ハミルトニアン段階の回転波近似と同じ操作だと無条件に扱わない。

これは**代表的な微視的導出の条件**であり、GKSL形式という数学的構造の必要条件をそのまま列挙したものではない。現象論的なモデルや、別の導出でGKSL形式を得る場合もある。具体的な実機へ適用するときは、H、各演算子、速度係数、環境の記憶、初期相関、時間尺度を確かめる。[QuTiPの導出・近似の説明](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html)も参照。

また、解析的にCPTPな式を採用しても、任意の時間刻み・任意の数値積分法が正値性を保つとは限らない。式の性質と数値解の性質を分けて検証する。

## 8. NRA-IDEとの接続で言える範囲

本式は量子状態の時間発展モデルである。NRA-IDEの境界接近比、更新許可、観測証言の規則とは役割が異なる。密度行列のトレースが保存されることから、熱的安全性、測定の十分性、SPSAの収束、古い結果の適用可否は導けない。

4月案でこの式を時間発展核へ採用したことと、対象系でモデルが妥当と検証されたことも区別する。関連項目は[観測量期待値ベクトル](../Glossary_JP.md#^qh-observable-expectation-vector)、[デコヒーレンス](../Glossary_JP.md#^qh-decoherence)、[更新許可](../Glossary_JP.md#^qh-update-authority)を参照する。

## 9. 出典・照合範囲

1. G. Lindblad, [On the generators of quantum dynamical semigroups](https://link.springer.com/article/10.1007/BF01608499), Communications in Mathematical Physics 48, 119–130 (1976), DOI 10.1007/BF01608499。出版社ページの書誌・要旨を2026-10-24に照合。原論文全文の読了とは区別する。
2. V. Gorini, A. Kossakowski, E. C. G. Sudarshan, [Completely positive dynamical semigroups of N-level systems](https://repository.ias.ac.in/51137/), Journal of Mathematical Physics 17, 821–825 (1976), DOI 10.1063/1.522979。研究機関リポジトリの書誌・要旨を同日に照合。原論文全文は未取得。
3. [QuTiP「Lindblad Master Equation Solver」](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-master.html)：方程式、速度係数を含む崩壊演算子、代表的な導出近似を同日に本文で照合。
4. [QuTiP「Monte Carlo Solver」](https://qutip.readthedocs.io/en/stable/guide/dynamics/dynamics-monte.html)：ジャンプ確率、正規化後の条件付き状態、非ジャンプ発展を同日に本文で照合。

§5のトレース相殺と§6の速度係数は、式から直接検算する関係である。古典的な有限次元検算は数式・実装上の確認であり、量子実機やNRA-IDE結合系の実証ではない。
