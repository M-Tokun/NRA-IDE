
# HAN Gate (NRA/IDE) — Cloud Minimum Module Bundle

**Version:** 1.0.0-

**Bundle Timestamp (JST):** 2026-02-05 22:08:25

**Author:** M-Tokuni 

---

## 📌 概要 (What this is)

本パッケージは、クラウドプラットフォーム向けに設計された**最小構成のデプロイ可能モジュール**です。リトライ、キュー滞留、タイムアウト、依存関係の増幅による「連鎖的崩壊（Cascade Failure）」を検知し、イングレス境界で強制的に **Fail-Closed (SILENCE)** を実行することで、システム全体の破綻を未然に防ぎます。

### 💡 非専門家向けガイド

* **これは「最適化」ツールではありません:** 応答速度を上げたり、最適な経路を探すものではありません。
* **これは「防波堤」です:** 連鎖反応が広がる前に、新しい通信を自動的に遮断（または安全な固定レスポンスを返却）する安全装置です。
* **トレードオフの選択:** 「一時的な沈黙（Silence）」を許容することで、「システム全損（Rupture）」という最悪の事態を回避します。

---

## 📖 対象者別ガイド (Who should read what)

| 対象者 | 推奨ドキュメント |
| --- | --- |
| **Executives / PO** | 本README、および「SILENCEの妥当性」セクション |
| **SRE / Platform** | `docs/SPEC.md`, `docs/RUNBOOK.md`, `deploy/k8s/han-gate.yaml` |
| **Network / Edge** | `integrations/envoy_ext_authz.md` (推奨) / `nginx_auth_request.md` |
| **App Teams** | `integrations/app_middleware.md` (最終手段としてのみ) |

---

## 🚀 クイックスタート (Kubernetes)

1. **ゲートのデプロイ:**
```bash
kubectl apply -f deploy/k8s/han-gate.yaml

```


2. **エッジへの統合:**
* **Envoy:** `ext_authz` フィルターの使用を推奨。
* **Nginx:** `auth_request` モジュールを使用。


3. **動作検証:**
`docs/RUNBOOK.md` に記載の `curl` サンプルを実行。
4. **安全なチューニング:**
* `R_OP` を下げると、より早期にFail-Closedが発動（安全性向上）。
* `TAU_*` を上げると、より深い依存関係をカバー（安全性向上）。



> [!IMPORTANT]
> **運用上の大原則:** 連鎖反応が始まった際、ゲートは自動的にSILENCEを実行します。人間が「その瞬間を判断」することはありません。

---

## ⚖️ SILENCEの妥当性 (ビジネス上の枠組み)

崩壊の兆候が見られる際、リトライやアグレッシブなオートスケーリングといった「努力」は、かえってシステムへの圧力を高め、失敗を拡散させます。

本ゲートは、**「無制限の破綻（Rupture）」よりも「限定的な沈黙（Bounded Silence）」**を選択します。

* **限定的な沈黙:** 一部のリクエストを一時的に拒否し、被害を局所化する。
* **無制限の破綻:** 全系停止、データ不整合のリスク、長期にわたる復旧、ブランド毀損。

> 本モジュールは意図的に**コンサバティブ（保守的）**に設計されています。人間が判断するよりも「早く」止まることがありますが、それこそが本製品の目的です。

---

## 📦 同梱物一覧

* `gate/han_gate_service.py`: ゲートサービス本体 (PASS / SILENCE 判定API)
* `api/openapi.yaml`: APIコントラクト（定義書）
* `deploy/k8s/han-gate.yaml`: K8s用マニフェスト（Deployment/Service/Config）
* `docs/ARCHITECTURE.md`: アーキテクチャ図および配置設計図
* `docs/SPEC.md`: 要件定義および受入基準
* `docs/RUNBOOK.md`: 運用マニュアル（DOs & DON'Ts）
* `integrations/`: 各ミドルウェア（Envoy/Nginx等）向け設定ガイド

---

## ⚠️ 安全上の注意 (Safety Notes)

1. **Fail-Closed 設計:** 疑わしい場合は常に SILENCE を選択します。
2. **ブラックボックス化の禁止:** ゲートロジックにML（機械学習）等による動的な最適化ループを導入しないでください。
3. **透明性の維持:** 論理は常に決定論的（Deterministic）であり、監査可能でなければなりません。

---

## 🔗 Credits & Contact

* **Author:** M-Tokuni 
* **Theoretical Foundation:** Ritsukan Circular Axiom (NRA)
* **Framework:** Intensional Dynamics Engine (IDE)
* **Links:** * [GitHub](https://github.com/M-Tokun/NRA-IDE) / [X (Twitter)](https://x.com/m_tokuni) / [note](https://note.com/mtokuni)

---

### 🛑 免責事項

本ソフトウェアは、NRA/IDE論理に基づくフェイルクローズ（Fail-Closed）設計を採用しています。システム保護のために通信を遮断・制限する場合があり、これに伴うサービス停止や遅延について、作者は一切の責任を負いません。

医療機器、公的インフラ、自動運転等の生命や財産に重大な影響を及ぼすシステムへの導入は、ユーザー自身の責任において厳格な検証と承認を行うものとします。

作者は、本ソフトウェアの適用による二次的な不具合や、他システムとの相互作用によって生じた損害について、予見の有無に関わらず賠償責任を負わないものとします。
