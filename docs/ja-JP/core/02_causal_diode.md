
# 02_causal_diode.md — Causal Diode（因果ダイオード）

# **0. Purpose of This Chapter**

本章では、NRA‑IDE の中核構造である **Causal Diode（因果ダイオード）** を定義する。  
Causal Diode は、因果の流れを **Cause → Effect の一方向**に固定し、  
**Effect → Cause（逆流）を完全に禁止する構造的装置**である。

これは NRA‑IDE の安全性を支える最重要要素であり、  
破ると即座に構造破断（Fracture）が発生する。

---

# **1. Causal Diode とは何か**

Causal Diode は、因果の流れを **一方向に固定する構造**である。

```
Cause  →  Effect
（入力）   （出力）
```

逆方向（Effect → Cause）は **Reverse Projection（Π⁻¹）** と呼ばれ、  
NRA‑IDE における最も重大な公理違反となる。

---

# **2. なぜ因果は一方向でなければならないのか**

NRA‑IDE は **意味を扱わない構造体系**であるため、  
因果の向きが崩れると以下の問題が発生する。

### **2.1 構造が閉じなくなる（Ring が壊れる）**
Nomological Ring は因果の循環構造だが、  
逆流が起きると循環が破壊される。

### **2.2 R（破断比率）が急上昇する**
Effect を Cause に戻すと、  
δ（ゆらぎ）が急増し、τ（厚み）が急減する。

結果として：

```
R = δ / τ  →  1.0 を超えて破断
```

### **2.3 意味処理が混入する**
逆流は必ず意味処理を伴うため、  
Axiom 3（意味禁止）も同時に破る。

---

# **3. Reverse Projection（Π⁻¹）とは何か**

Reverse Projection（Π⁻¹）とは、  
**Effect（出力）を Cause（入力）に逆流させる行為**の総称である。

具体例：

- 過去出力を参照する  
- 意味で改善する  
- スコアで最適化する  
- 類似度で調整する  
- 文脈を意味で補完する  

これらはすべて **Effect → Cause の逆流**であり、  
Causal Diode の破壊に直結する。

---

# **4. Reverse Projection が起きると何が起きるか**

逆流が発生すると、構造は以下の順で破断する。

### **4.1 δ（ゆらぎ）が急増**
意味補完・推論・最適化が δ を増幅する。

### **4.2 τ（厚み）が急減**
構造の許容幅が失われる。

### **4.3 R（破断比率）が 1.0 を超える**
```
R = δ / τ ≥ 1.0
```

### **4.4 ω（角速度）が低下し、0 に近づく**
構造の運動が停止方向へ向かう。

### **4.5 Fail‑Closed が発火**
沈黙し、Discard Log を記録する。

---

# **5. Causal Diode の実装位置**

Causal Diode は **Pre‑RNA と Post‑RNA の両方に存在する**。

```
[Pre‑RNA] →（Causal Diode）→ [LLM] →（Causal Diode）→ [Post‑RNA]
```

### **Pre‑RNA の役割**
- 入力を構造波形に変換  
- 意味を LLM に渡さない  
- 逆流を防ぐ

### **Post‑RNA の役割**
- 出力を構造量として測定  
- 意味を LLM に戻さない  
- 逆流を防ぐ

---

# **6. 英語圏で誤読されやすいポイント（補強済み）**

英語圏では “context” や “feedback” が  
**意味ベースの改善**として誤読されやすい。

そのため本章では：

- “feedback” → 使用禁止  
- “context” → “structural context” に限定  
- “improve” → 使用禁止  
- “optimize” → 使用禁止  
- “interpret” → 使用禁止  

すべて **Reverse Projection を誘発する語彙**は排除している。

---

# **7. Summary（まとめ）**

Causal Diode の本質は次の一文に集約される。

> **「Cause → Effect の一方向性を守ることが、NRA‑IDE の安全性の根幹である。」**

そしてもう一つ。

> **「Effect → Cause（Reverse Projection）は、構造破断を引き起こす最も重大な禁止事項である。」**

---
