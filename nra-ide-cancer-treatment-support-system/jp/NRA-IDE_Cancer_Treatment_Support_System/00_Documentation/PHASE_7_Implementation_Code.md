# ═══════════════════════════════════════════════════════════════════════

# Project: NRA-IDE Cancer Treatment Support System

# Phase:   07

# File:    PHASE_7_Implementation_Code.md

# Rev:     2.0 (2026-07-28) 掲載スニペットを実装に一致させる

# Note:    Reference Implementation (See Group 10/20 for actual files)

# ═══════════════════════════════════════════════════════════════════════



# Phase 7: Implementation Reference



本書は実装の要点を抜粋したものである。**実際のコードは `10_Hardware_Design/` および `20_Software_Host/` を参照すること。** 本書と実コードが食い違った場合、実コードが正である。



---



## 1. Verilog Core Logic (Snippet)



応力比較形（PHASE_2 Rev 2.0）の中核。**応力に乗じるのは変位ではなく歪み（無次元）である。**



```verilog

// Stage 3: 歪みと粘性係数

//   strain = (D - d) * (1/D)      Q8.8 * Q0.16 -> Q0.8
strain3 <= strain_mul[31:16];

//   q1 = (eta * v) * (0.012 / d^2)  Q16.16 * Q0.24 -> Q0.16
q1_3    <= q1_mul[39:24];



// Stage 4: 応力の各項（いずれも Q8.8 へ戻す）

//   sigma_el = (E + B) * strain
sig_el4 <= el_mul[23:8];

//   sigma_v  = q1 * D
sig_v4  <= v_mul[31:16];



// Stage 5: 合算と比較

if (sig_el4 + sig_v4 > flow_dp) o_is_jammed <= 1;  // BLOCKED

else                           o_is_jammed <= 0;  // PASSABLE

```



> **Rev 1.0 からの訂正:** 旧版は `r_elastic_force <= (i_stiffness + i_boost) * r_delta_x;` を掲載していた。これは変位 `delta_x` を直接乗じており次元が閉じていない。歪み `(D-d)/D` へ正規化しなければならない。



---



## 2. Python Host Logic (Snippet)



```python

# バイナリパケット構築（14バイト）
header = b'\xA5' if is_type_a else b'\xA6'

payload = struct.pack('>6H',
    self._float_to_q8_8(p['cell_stiffness']),
    self._float_to_q8_8(p['cell_viscosity']),
    self._float_to_q8_8(p['cell_diameter']),
    self._float_to_q8_8(p['pore_size']),
    self._float_to_q8_8(p['flow_dp']),
    self._float_to_q8_8(p['drug_boost']))

checksum = 0
for b in payload:
    checksum ^= b

packet = header + payload + struct.pack('B', checksum)

```



Q8.8 への変換は**切り捨て**である。`int(max(0.0, min(255.99, value)) * 256)`。ホスト・FPGA・可視化のすべてがこの量子化で一致していなければならない。



---



## 3. Reference Model



`20_Software_Host/nra_core_model.py` は上記 Verilog の演算をビット単位で再現する。



* FPGA 非接続時のシミュレーション判定

* ジャミングマップの境界描画

* レポートの判定根拠（中間量）算出



の3者がこのモジュールだけを根拠とする。**ホスト側に独自の近似式を持たせてはならない。** 判定モデルが二重化すると、医師が見る図と装置の判定が食い違う。



```python

# 判定の中核（nra_core_model.evaluate より）
strain, sigma_v = fixed_terms(eta_q, D_q, d_q, v_q)  # E_q は粘性応力に不要
el_mul = (E_q + B_q) * strain
sigma_total = ((el_mul >> 8) & 0xFFFF) + sigma_v
is_jammed = sigma_total > dP_q

```



---



（注: 実際のコードは `10_Hardware_Design` および `20_Software_Host` を参照のこと）
