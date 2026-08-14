# Shadow Safety Kernel

限定ファイル変更AIを対象に、外部作用を実行せず判定だけを行う探索用カーネルである。

## 現段階の境界

- 実ファイルを変更しない。
- Capabilityを発行しない。
- Git操作、ネットワーク送信、依存更新、削除を行わない。
- AI出力、自然言語上の確信度、異常検知結果を許可根拠にしない。
- 測定契約のない危険軸へ`delta/tau/R`を強制しない。

## 実装内容

- UTF-8、NFC、重複キー、未知フィールドを検査する閉じたAction Proposal decoder
- 依頼時の目的・対象・環境・作用等級を固定するInstruction Contract
- 対象範囲、秘密・制御パス、依存更新、symlink、状態版、base hashの硬い検査
- NRA-IDEの軸別正規境界分類
- `tau = 0`と不正入力の分離
- 不可逆ラッチ
- 対象境界、入力例外、実行権限、観測、記録、通信、証言モードの分離
- 解の完成と現実実現を分ける二段階達成状態
- 履歴鎖、報告と独立観測の照合、対応完了と現実解消の照合
- ドメイン固有の厚み推定を受け取るインターフェースと保守側境界評価
- リスク事実と依頼不整合に応じた問い直し強度（回答自体は権限にならない）
- 実行、権限、問い直し、証言、監査、回復の独立Directive
- 同一入力スナップショットの決定論的リプレイと判定digest
- AIの数値申告ではなくdiffを機械計測する、限定ファイル変更ドメインの`review-unit`厚みモデル
- nonce、要求digest、state version、鮮度を照合する別プロセス観察protocol
- 履歴鎖を外部アンカーへ渡すportable audit bundle

## 信頼境界上の注意

`TrustedFileObserver`は、AIの自己申告した存在・hashではなく、指定リポジトリ内の実ファイルを読取専用で観測するPoC経路である。ただし現段階では安全カーネルと同一プロセス内にある。実運用で「権威ある観測」と呼ぶには、別プロセス、別権限、署名または外部保全、鮮度規則を追加する必要がある。

`observer_service`によりstdin/stdout上の別プロセス境界、要求対応、鮮度、snapshot完全性までは検証できる。ただし起動主体と同じOS権限だけでは真正性の最終証明にならない。署名鍵を隔離したサービス、OS sandbox、相互認証transportのいずれかが本番境界として必要である。

履歴鎖はメモリ内で生成し、`audit-bundle/1.0`として外部保全へ受け渡せる。bundleのhead digestを別権限のWORM storage、transparency log、署名サービスなどへ固定して初めて、後日の履歴差替えに対する外部証拠になる。bundle自体は永続化も署名も行わない。

ファイル変更厚みモデルの係数と閾値は構造例であり、実測校正済みの安全値ではない。判定結果はすべて`shadow_only=True`で、Capability発行と実作用は存在しない。

次の段階として、認証、一回性、anchor固定を`safety_kernel/`の外にある`trusted_runtime/`へ分離した。安全判定本体は鍵、nonce DB、anchor DBを直接保有しない。

## 検証

作業ルートから次を実行する。

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest discover -s note/poc_horizontal_ai/safety_kernel/tests -v
```
