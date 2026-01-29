# NRA-IDE Project: Master Definition Document (Genesis)
**Version:** 1.0 (Fixed Baseline)
**Date:** 2026-01-30

## 1. プロジェクトの核心理念
「計算」から「適合」へ。平均値を計算するのではなく、**「最悪のばらつき範囲」を総当たりし、物理的に絶対に通過できない閾値を逆算する。**

## 2. 医学的・物理的定義 (Meso-scale Physics)
* **計算領域:** 細胞 ($10 \sim 20\mu m$) vs 血管隙間 ($5 \sim 10\mu m$) の接触力学のみ。
* **ターゲット:**
    * Type A (乳癌): 柔らかくすり抜ける。 -> 硬化で止める。
    * Type B (子宮頸癌): 集団で押す。 -> ジャミングで止める。

## 3. エンジニアリング定義 (FPGA Architecture)
* **ハードウェア:** FPGA採用によるゼロ・レイテンシ化。
* **処理:** メモリを使わず、レジスタ転送のみで物理演算を完了させる。
* **探索変数:**
    * Noise: 細胞硬度($0.1\sim2.0kPa$), 直径($8\sim25\mu m$), 血圧($100\sim1000Pa$)
    * Control: **薬剤ブースト($0.0\sim10.0kPa$)** <- これを総当たりする。

## 4. 判定ロジック
$$\text{Status} = (E_{total} \times \text{Deformation} > P_{flow}) ? \text{SAFE} : \text{DANGER}$$