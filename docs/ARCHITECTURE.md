# NRA-IDE Architecture
## System Design & Theoretical Framework

### 🏗️ Architectural Overview (アーキテクチャ概要)

The NRA-IDE system implements a **"Sandwich Structure"** to enforce strict causal integrity.
Unlike standard physics engines that calculate "Force from Distance" (Inverse Kinematics), this engine treats **Phase (Time/State)** as the primary driver.

本システムは、厳格な因果整合性を強制するために**「サンドイッチ構造」**を採用しています。
「距離から力を逆算する（逆運動学）」一般的な物理エンジンとは異なり、本エンジンは**「位相（時間・状態）」**を主駆動要因として扱います。

---

### 🧩 The NRA-Sandwich Pipeline

Data flows strictly in one direction (Unidirectional Causal Flow).
データは厳密に一方向（単方向因果フロー）のみを流れます。

```mermaid
graph TD
    UserInput[User Prompt] --> PreNRA
    
    subgraph "NRA-IDE System"
        PreNRA[1. Pre-NRA: Constraint Injection]
        Core[2. IDE Core: Intensional Dynamics]
        PostNRA[3. Post-NRA: Causal Firewall]
    end
    
    PreNRA --"Filtered State"--> Core
    Core --"Quantized Phase"--> PostNRA
    PostNRA --"Safe Output"--> FinalOutput[Generated Response/Action]
    
    style Core fill:#f9f,stroke:#333,stroke-width:4px
1. Pre-NRA: Constraint Injection (制約注入)
Role: Define the "Laws of Physics" for the session.

File: config/ide_foundation_config.json

Function: Sets the maximum stiffness, energy limits, and forbidden states before simulation begins.

役割: セッションにおける「物理法則」を定義します。

機能: シミュレーション開始前に、最大剛性、エネルギー制限、禁止状態を設定します。

2. IDE Core: Intensional Dynamics (内包的力学コア)
Role: Calculate the next state based on Phase Integration.

File: src/ide_core_safe.py

Key Logic:

Phase Locking: Locks floating-point phases to integers to prevent drift.

Residual Discard: Intentionally discards float errors (Micro-Hallucinations).

役割: 位相積分に基づいて次の状態を計算します。

主要ロジック:

位相ロック: 浮動小数点の位相を整数にロックし、ドリフト（ズレ）を防ぎます。

端数廃棄: 計算誤差（ミクロなハルシネーション）を意図的に切り捨てます。

3. Post-NRA: Causal Firewall (因果ファイアウォール)
Role: Audit the output for "Causal Reversal".

File: src/ide_firewall.py

Check: Does Effect precede Cause? If yes, trigger EMERGENCY_STOP.

役割: 出力に対して「因果の逆転」がないか監査します。

チェック: 「結果」が「原因」より先に来ていないか？ その場合、緊急停止します。

⚠️ Theoretical Note (理論上の注意点)
Distance is NOT a Cause. In this engine, "Distance" is merely a result (log) of the interaction between "Energy" and "Tension." Attempting to derive Force from Distance (Hooke's Law in reverse) is mathematically prohibited by the Nomological Ring Axioms.

距離は原因ではない。 本エンジンにおいて、「距離」は「エネルギー」と「張力」の相互作用の結果（ログ）に過ぎません。 距離から力を導き出そうとする行為（フックの法則の逆算）は、**律環公理（NRA）**によって数学的に禁止されています。

(C) 2026 NRA-IDE Project / M-Tokun