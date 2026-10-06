# NRA-IDE現行閾値gate

公開するThresholdGuardian・SafetyAction・SafetyStatusは[共通アダプター](../_canonical_threshold.py)と[正規参照実装](../../nra-core/foundations/NRA-IDE_Architecture_public.py)を使う。定義と権威は[AXIOMS.md](../../theory/AXIOMS.md)による。[設定と状態表](../../config/structural_zones_JP.md)を参照する。

```python
import json
from pathlib import Path
from gate.jp import ThresholdGuardian

demo = json.loads(Path('config/ide_presets.json').read_text(encoding='utf-8'))['presets']['SOFTWARE_DEMO']
gate = ThresholdGuardian(config=demo)  # 未検証のソフトウェア例のみ
notice = gate.evaluate(0.995, 1.0, timestamp='DEMO_T0').as_dict()
assert notice['status'] == 'IRREVERSIBLE_TRANSITION'
assert notice['fail_closed'] is True
```

引数なしconstructorは宣言未設定のJSONを読むため、CONFESSIONで遮断する。観測時点・宣言の不足、不正入力、旧schemaを許可に変換しない。実評価には評価前に宣言したドメイン固有設定を用いる。

互換性: evaluate(delta,tau)の位置引数は保持するが、timestampが必要。SafetyStatusのlevel_name/action/ratio/messageを保持し、全文noticeを追加した。状態は正規7名称、運用動作はCONTINUE/LOG_WARN/FAIL_CLOSED。旧EMERGENCY_BRAKE/SYSTEM_HALTは現行動作ではない。不正なRはNone、tau=0はOUT_OF_DESCRIPTION_DOMAIN、負のdeltaを正値へ補正しない。

同一instanceが不可逆・対象破断の履歴を保持し、reset APIはない。観測・記録・通信は別次元。破断後にRが下がっても固定証言を継続する。不正な新入力はCONFESSIONとし、target_state=RUPTURE_BOUNDARYを解除しない。再起動をまたぐ履歴を呼出し側で保存する。本adapterは履歴永続化を伴う安全サービスではない。

旧公理・力学・空間モジュールは履歴ファイルとして残し、現行packageの公開入口から外した。その旧入口を正規gateとは扱わない。移行前snapshotは[legacy記録](../legacy/v1/README.md)に保存する。物理的・臨床的な安全性は未検証である。
