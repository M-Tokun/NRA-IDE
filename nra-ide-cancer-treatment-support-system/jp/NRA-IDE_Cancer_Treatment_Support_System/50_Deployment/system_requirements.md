
# ═══════════════════════════════════════════════════════════════════════

# Project: NRA-IDE Cancer Treatment Support System

# Phase:   50 (Deployment)

# File:    50_Deployment/system_requirements.md

# ═══════════════════════════════════════════════════════════════════════

## 1. ハードウェア要件 (Hardware Infrastructure)

物理演算の決定論的動作を保証するため、以下のスペックを推奨する。

### 1.1 FPGA Compute Node

* **Target Device:**
* **Xilinx Artix-7:** XC7A35T-1CPG236C (Basys 3) 以上
* **Intel Cyclone V:** 5CEBA4F23C7 (DE0-CV) 以上


* **Clock Frequency:** 100 MHz (安定度 ±50 ppm 以内)
* **I/O Standard:** LVCMOS 3.3V (UART信号の整合性確保のため)

### 1.2 Host PC (Control Layer)

* **CPU:** x86_64 1.5GHz 以上 (Python 実行用)
* **RAM:** 4GB 以上
* **OS:** Ubuntu 22.04 LTS (推奨) / Windows 10 (64-bit)
* **Port:** USB 2.0 / 3.0 Type-A (仮想COMポートとして認識可能なこと)

---

## 2. 通信・環境要件 (Environmental & Connectivity)

### 2.1 シリアル通信規格

* **Baud Rate:** 115200 bps
* **Data Format:** 8-bit, No Parity, 1 Stop bit (8N1)
* **Recommended USB-UART Bridge:**
* FTDI FT2232 / FT232R (低ジッタ・医療現場での実績を重視)
* CP2102 (代替案)



### 2.2 電源品質 (Power Quality)

* **Ripple Noise:** 50mVp-p 以下
* **Stability:** 医療用絶縁トランスまたは医療規格電源の利用を強く推奨する。
* **Rationale:** FPGA内の物理演算における過渡的な電圧降下は、Q8.8 固定小数点演算の「論理的純潔性」を脅かす可能性がある。

### 2.3 動作環境

* **Ambient Temperature:** 15°C 〜 35°C (空調完備の臨床室)
* **Humidity:** 30% 〜 75% (非結露)
* **Rationale:** 熱によるゲート遅延の変化を STA (Static Timing Analysis) の範囲内に収めるため。

---

## 3. ソフトウェア依存性 (Software Stack)

* **Python:** v3.8.10 〜 v3.11.x
* **Dependencies:**
* `pyserial`: v3.5+ (通信コア)
* `numpy`: v1.21+ (行列演算)
* `matplotlib`: v3.5+ (安全マップ生成)



---
