## 📄 README_10.txt



**Project: NRA-IDE Cancer Treatment Support System** 

**Phase: 10 (Communication & Calculation Infrastructure)**

**Date: 26-0203-1620 JST** **Author: M-Tokuni, Gemini (Architect)**



### 1. 概要 (Overview)



本フォルダは、律環公理（NRA）に基づくがん治療支援システムの基盤となる第10フェーズの成果物である 。

主要な目的は、ホストPCとのバイナリ通信（UART）の確立と、物理演算パイプライン（BioCalibrator）の同期実装である。



### 2. ファイル構成 (File Structure)



| 分類 | ファイル名 | 役割 |

| --- | --- | --- |

| **Top** | `Top_Module.v` | システム統合、通信/演算シーケンス制御 



 |

| **I/O** | `UART_Interface.v` | 115200bps 8N1 全二重シリアル通信 



 |

| **Core** | `Cancer_Treatment_Selector.v` | 癌腫別（Type A/B）演算器の選択と統合 



 |

| **Logic** | `BioCalibrator_TypeA.v` | 単一細胞物理判定（3段パイプライン） 



 |

| **Logic** | `BioCalibrator_TypeB.v` | 集団力学封鎖判定（40bit高精度演算） 



 |

| **CSTR** | `timing.sdc` | 100MHz クロックおよびI/O遅延制約 



 |

| **CSTR** | `pinout_cyclone_v.qsf` | DE0-CV (Cyclone V) 用ピン配置 



 |

| **CSTR** | `pinout_artix_7.xdc` | Basys 3 (Artix-7) 用ピン配置 



 |

| **Sim** | `Testbench_Integration.v` | 全系統合検証用テストベンチ |



### 3. 通信プロトコル (Communication Protocol)



ホストPCとの通信は、以下の 14バイト・バイナリパケットによって行われる 。



* 

**[00] Header:** `0xA5` 固定 





* 

**[01-02] Stiffness:**  (Q8.8) 





* 

**[03-04] Viscosity:**  (Q8.8) 





* 

**[05-06] Diameter:**  (Q8.8) 





* 

**[07-08] Pore Size:**  (Q8.8) 





* 

**[09-10] Flow DP:**  (Q8.8) 





* 

**[11-12] Drug Boost:**  (Q8.8) 





* **[13] Checksum:** パケット整合性確認用（※実機実装推奨）



### 4. 修正履歴 & 既知のバグ対応 (Major Bug Fixes)



1. **パイプライン同期エラー**: 計算完了フラグ `o_out_valid` を追加。演算（3サイクル）完了後に UART 送信を開始するようシーケンスを厳密化。

2. **Type B 演算精度**: 細胞数  倍によるオーバーフローを回避するため、内部レジスタを 32bit から **40bit** へ拡張。

3. **UARTサンプリング不備**: 非ブロッキング代入による受信バッファの1クロック遅延を考慮し、計算開始タイミングを調整。

4. **送信ロジック欠落**: `UART_Interface` に送信（TX）ステートマシンを完全実装。



### 5. 実行方法 (How to Run)



1. 

`Testbench_Integration.v` を読み込み、`wave_config.do`  を適用。





2. 14バイトパケットをシミュレーション上で供給し、`uart_tx` から判定結果（`0xFF`: Jammed, `0x00`: Safe）が返ることを確認する。



---

