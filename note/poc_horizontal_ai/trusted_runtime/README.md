# Trusted Runtime PoC

シャドー安全カーネルから分離し、観察応答の認証、要求の一回性、監査headの固定receiptを扱うPoCである。

## 責務

- `auth.py`：HMAC-SHA256によるpayload認証と用途別subkey導出
- `nonce_store.py`：request IDとnonceの永続一回性、append-only trigger、HMAC chain
- `observer_gateway.py`：要求鮮度、一回性、実観察、認証応答の合成
- `observer_gateway_service.py`：鍵ファイルを起動時だけ読む一要求プロセス
- `anchor_store.py`：audit headとbundle digestの一回固定、認証receipt
- `anchor_service.py`：audit bundle検証後のanchor処理
- `asymmetric_auth.py`：Ed25519署名と公開鍵だけによる検証
- `signed_boundary.py`：署名済み観察応答と署名済みanchor receipt
- `ed25519_observer_service.py`：秘密鍵を保持する観察署名プロセス
- `ed25519_anchor_service.py`：秘密鍵を保持するanchor署名プロセス
- `witness_store.py`：create-only witness記録と複数witness quorum
- `deployment_boundary.py`：リポジトリ、鍵、DB、witnessの配置分離検査
- `trust_bundle.py`：offline root署名付き役割別鍵、rotation、失効、有効期間
- `trust_checkpoint.py`：bundle世代と前digestを永続固定しrollbackを拒否
- `role_verification.py`：観察、anchor、witnessの鍵役割を交差利用させない検証
- `authenticated_witness.py`：witness自身の署名とprincipal単位のquorum
- `runtime_admission.py`：pinned root、checkpoint、鍵role、有効性、秘密鍵一致による署名者の起動認可
- `checkpoint_attestation.py`：trust checkpointの外部署名固定、witness側単調state、principal単位quorum
- `checkpoint_witness_service.py`：独立witnessが旧世代を再署名しない一要求プロセス

## 境界

- HMACは共有鍵方式であり、検証側も秘密鍵を持つ。公開鍵署名ほど強い責務分離ではない。
- HMAC経路は前段互換PoCとして残し、新しい観察・anchor経路はEd25519を推奨する。
- Ed25519検証側は公開鍵だけを保持し、観察またはreceiptを新規署名できない。
- master keyは用途別subkeyへ導出するが、OS key store、HSM、TPMは使用していない。
- SQLite triggerは通常のUPDATE/DELETEを拒否するが、DB所有者によるファイル全置換や末尾切捨てを単独では防げない。
- nonce DBとanchor DBはtrusted runtimeだけが書込めるOS権限へ分離する必要がある。
- anchor receiptを別権限のWORM storageまたはtransparency logへ保存して初めて、末尾切捨てに対する外部証拠になる。
- create-only witnessは同一receiptを二箇所以上へ固定できるが、同一OS identity配下の複数ディレクトリは独立witnessとは証明できない。
- 配置検査はパス分離だけを確認し、OS identity分離を確認できない場合は必ず`OS_IDENTITY_SEPARATION_NOT_ATTESTED`を残す。
- trust bundle受入時は署名鮮度を要求し、後日のcheckpoint chain検証では古い正常世代を時間経過だけで破損扱いしない。
- rotation前後の複数鍵が同じ`principal_id`ならwitness quorumでは一主体として数える。
- Ed25519観察・anchor serviceは、最新checkpointと一致するtrust bundleへ署名鍵が所属しなければ起動しない。
- trusted経路の`signed-payload/1.1`は、trust bundle generationと署名bundle digestを署名対象へ含める。未結合の`1.0`と別trust stateへの結合はtrusted検証で拒否する。
- 観察、anchor、認証witnessは同じtrust-state binding規則を使う。`1.0`は前段PoCの直接署名互換に限り、trusted検証経路では受理しない。
- Ed25519観察・anchor serviceは、最新trust stateに対する異なるwitness principal二主体以上の新鮮なattestationがなければ、checkpoint更新前に起動を拒否する。
- checkpoint witnessは独自のappend-only SQLite stateを持ち、同一stateの新鮮な再証言は許すが、旧世代、世代飛越し、直前digest不一致、同世代別digestを拒否する。
- offline root公開鍵は別経路でpinする必要がある。offline root自体のrotationと緊急失効は未実装である。
- trust checkpoint DBの全置換・末尾切捨ては、独立管理されたwitness serviceが旧stateの再証言を拒否することで検出可能になる。ただし同一管理者がlocal checkpointと全witness DBを置換できる配置では成立しない。
- Capability発行、patch適用、commit、pushなどの実作用は存在しない。

鍵、SQLite DB、receiptはリポジトリ内へ生成しない。試験ではOS一時ディレクトリだけを使用する。

Ed25519実装は手製暗号ではなく`cryptography`を使用する。検証済み環境を再現する版は`requirements.txt`へ固定した。この作業では既存環境の`cryptography 46.0.7`を使用し、新規インストールは行っていない。
