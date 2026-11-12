# File: NRA_IDE_判断経路参照コード_2026_1112_1904.py
# Created: 2026-11-12 19:04 JST
# Status: 研究用プロトタイプ / 非正典 / 実世界の真偽を自動認定しない
"""意味型の検査、評価の停止、追記監査と分岐履歴の最小試作。

使い方: python NRA_IDE_判断経路参照コード_2026_1112_1904.py

重要な限界:
  - 『支持された』という入力判定の根拠が真であるとプログラムは証明しない。
  - 現実のEventではなく、すべてEventRecord等の*記録*を扱う。
  - Pythonで検出できるのは宣言済み型・条件の不整合だけである。
  - 実際のNRA-IDE FORMULAや正規状態を実装・変更しない。
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Kind(str, Enum):
    OPERATION_REPORT = "OPERATION_REPORT"  # 分離か、記録不採用か、などに関する主張
    EVENT_REPORT = "EVENT_REPORT"          # 事象についての記録
    MEASUREMENT = "MEASUREMENT"
    STATISTIC = "STATISTIC"
    INFERENCE = "INFERENCE"
    FACT_ASSESSMENT = "FACT_ASSESSMENT"


class Support(str, Enum):
    SUPPORTED = "SUPPORTED"     # この事例で支持済みと*申告*されたもの
    CONTRADICTED = "CONTRADICTED"
    UNKNOWN = "UNKNOWN"


class Verdict(str, Enum):
    STOPPED = "STOPPED"
    ELIGIBLE = "ELIGIBLE"       # 後段の専門計算へ進む資格のみ / 真理性の確定ではない


class Reason(str, Enum):
    OPERATION_UNCONFIRMED = "OPERATION_UNCONFIRMED"
    OPERATION_CLASS_MISMATCH = "OPERATION_CLASS_MISMATCH"
    INTENT_DRIFT = "INTENT_DRIFT"
    RULE_NOT_PREFIXED = "RULE_NOT_PREFIXED"
    REQUIRED_INPUT_MISSING = "REQUIRED_INPUT_MISSING"
    TYPE_MISMATCH = "TYPE_MISMATCH"
    SUBJECT_MISMATCH = "SUBJECT_MISMATCH"
    UNSUPPORTED_RECORD = "UNSUPPORTED_RECORD"
    DEPENDENCY_UNRESOLVED = "DEPENDENCY_UNRESOLVED"
    DEPENDENCY_CYCLE = "DEPENDENCY_CYCLE"
    READY_FOR_DOMAIN_REVIEW = "READY_FOR_DOMAIN_REVIEW"


@dataclass(frozen=True)
class Record:
    record_id: str
    kind: Kind
    subject: str
    value: Any
    support: Support
    source: str  # 出所を保持する。独立の妥当性検証は別途必要。
    dependencies: tuple[str, ...] = ()
    observed_at: str | None = None
    recorded_at: str | None = None


class RecordStore:
    """追記しか提供しない試作。改ざん耐性・永続化は実装していない。"""
    def __init__(self) -> None:
        self._items: dict[str, Record] = {}

    def add(self, rec: Record) -> None:
        if rec.record_id in self._items:
            raise ValueError(f"記録ID {rec.record_id} は上書き不可。訂正は新規IDで追記")
        self._items[rec.record_id] = rec

    def get(self, record_id: str) -> Record | None:
        return self._items.get(record_id)

    def depends_on(self, record_id: str, ancestor_id: str, seen: frozenset[str] = frozenset()) -> bool:
        if record_id == ancestor_id:
            return True
        if record_id in seen:
            return False  # 循環の存在判定は別の関数で行う
        rec = self.get(record_id)
        return bool(rec and any(self.depends_on(parent, ancestor_id, seen | {record_id})
                                for parent in rec.dependencies))


@dataclass(frozen=True)
class Requirement:
    name: str
    kind: Kind
    subject: str


@dataclass(frozen=True)
class EvaluationPlan:
    evaluation_id: str
    case_id: str
    intent: str
    expected_operation: str
    rule_id: str
    rule_version: str
    declared_at: str
    requirements: tuple[Requirement, ...]
    previous_evaluation_id: str | None = None


@dataclass(frozen=True)
class Submission:
    intent: str
    operation_record_id: str
    inputs: tuple[tuple[str, str], ...]  # 要求名, 記録ID
    started_at: str


@dataclass(frozen=True)
class AuditEntry:
    evaluation_id: str
    case_id: str
    verdict: Verdict
    reason: Reason
    consulted_ids: tuple[str, ...]  # 判定が実際に参照した記録だけを依存関係とする
    previous_evaluation_id: str | None
    note: str


class AuditTrail:
    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def append(self, entry: AuditEntry) -> None:
        if any(x.evaluation_id == entry.evaluation_id for x in self._entries):
            raise ValueError("同じ評価IDへの追記・上書きを拒否。新規評価IDで実行")
        self._entries.append(entry)

    @property
    def entries(self) -> tuple[AuditEntry, ...]:
        return tuple(self._entries)

    def affected_by(self, record_id: str, store: RecordStore) -> tuple[str, ...]:
        """指定記録の訂正時に再検証すべき評価IDを列挙。旧結果は書き換えない。"""
        return tuple(entry.evaluation_id for entry in self._entries
                     if any(store.depends_on(eid, record_id) for eid in entry.consulted_ids))


def dependency_issue(record_id: str, store: RecordStore,
                     path: frozenset[str] = frozenset()) -> Reason | None:
    if record_id in path:
        return Reason.DEPENDENCY_CYCLE
    rec = store.get(record_id)
    if rec is None or rec.support is not Support.SUPPORTED:
        return Reason.DEPENDENCY_UNRESOLVED
    for dep_id in rec.dependencies:
        issue = dependency_issue(dep_id, store, path | {record_id})
        if issue:
            return issue
    return None


def gate(plan: EvaluationPlan, sub: Submission,
         store: RecordStore, audit: AuditTrail) -> AuditEntry:
    """境界ゲート。実際の『除外・分離』の意味分類は入力根拠の外部審査に依存。"""
    named_inputs = dict(sub.inputs)
    consulted_ids: list[str] = []

    def finish(verdict: Verdict, reason: Reason, note: str) -> AuditEntry:
        entry = AuditEntry(plan.evaluation_id, plan.case_id, verdict, reason,
                           tuple(consulted_ids), plan.previous_evaluation_id, note)
        audit.append(entry)
        return entry

    # 評価途中で意図をすり替えて、同じ評価が成立したことにしない。
    if sub.intent != plan.intent:
        return finish(Verdict.STOPPED, Reason.INTENT_DRIFT, "検討意図の変更。旧評価を維持し新規評価へ")

    # タイムスタンプのISO表現を固定した試験環境。実運用ではUTC変換・署名等が必要。
    if plan.declared_at >= sub.started_at:
        return finish(Verdict.STOPPED, Reason.RULE_NOT_PREFIXED, "評価規則を開始前に固定できていない")

    consulted_ids.append(sub.operation_record_id)
    operation = store.get(sub.operation_record_id)
    if (operation is None or operation.kind != Kind.OPERATION_REPORT
            or operation.support != Support.SUPPORTED):
        return finish(Verdict.STOPPED, Reason.OPERATION_UNCONFIRMED, "対象操作の分類根拠が不明")
    if operation.value != plan.expected_operation:
        return finish(Verdict.STOPPED, Reason.OPERATION_CLASS_MISMATCH,
                      "記録上の操作種別と評価上の対象分類が異なる")
    if dependency_issue(sub.operation_record_id, store):
        return finish(Verdict.STOPPED, Reason.DEPENDENCY_UNRESOLVED,
                      "分類根拠の依存関係に欠損または循環がある")

    for requirement in plan.requirements:
        record_id = named_inputs.get(requirement.name)
        if record_id is None or store.get(record_id) is None:
            return finish(Verdict.STOPPED, Reason.REQUIRED_INPUT_MISSING,
                          f"必須項目 {requirement.name} の根拠が欠けている")
        consulted_ids.append(record_id)
        rec = store.get(record_id)
        assert rec is not None
        if rec.kind != requirement.kind:
            return finish(Verdict.STOPPED, Reason.TYPE_MISMATCH,
                          f"{requirement.name}: {rec.kind.value} を {requirement.kind.value} に暗黙変換しない")
        if rec.subject != requirement.subject:
            return finish(Verdict.STOPPED, Reason.SUBJECT_MISMATCH,
                          f"{requirement.name}: 数値が一致しても対象が異なる")
        if rec.support != Support.SUPPORTED:
            return finish(Verdict.STOPPED, Reason.UNSUPPORTED_RECORD,
                          f"{requirement.name}: 支持根拠が不明または反証されている")
        issue = dependency_issue(record_id, store)
        if issue is not None:
            return finish(Verdict.STOPPED, issue,
                          f"{requirement.name}: 元根拠の依存関係を解決できない")

    return finish(Verdict.ELIGIBLE, Reason.READY_FOR_DOMAIN_REVIEW,
                  "この試作の宣言チェックを通過。実世界の事実成立やNRA-IDE計算の正当性は未確定")


@dataclass(frozen=True)
class HistoryNode:
    node_id: str
    relation: str             # split / merge / event-record 等の記録上の分類
    predecessor_ids: tuple[str, ...]


class HistoryLinks:
    """分岐・融合の参照グラフの最低限の実装。現実履歴そのものではない。"""
    def __init__(self) -> None:
        self._nodes: dict[str, HistoryNode] = {}

    def add(self, node: HistoryNode) -> None:
        if node.node_id in self._nodes:
            raise ValueError("履歴ノードの上書きを禁止")
        if any(parent not in self._nodes for parent in node.predecessor_ids):
            raise ValueError("不明な先行ノードへの無断接続を禁止")
        self._nodes[node.node_id] = node

    def predecessors(self, node_id: str) -> tuple[str, ...]:
        return self._nodes[node_id].predecessor_ids


def demo_and_tests() -> None:
    records = RecordStore()
    audit = AuditTrail()
    records.add(Record("op_select", Kind.OPERATION_REPORT, "操作分類",
                       "RECORD_SELECTION", Support.SUPPORTED, "評価採否の申告"))
    records.add(Record("op_split", Kind.OPERATION_REPORT, "操作分類",
                       "PHYSICAL_SEPARATION", Support.SUPPORTED, "事例上の仮定・外部精査待ち"))
    records.add(Record("split_report", Kind.EVENT_REPORT, "構成Aの分離",
                       "分離の報告", Support.SUPPORTED, "仮想事例の原資料"))
    records.add(Record("mean_20", Kind.STATISTIC, "構成Aの分離",
                       20.0, Support.SUPPORTED, "10, 20, 30 の平均"))
    records.add(Record("unsupported", Kind.EVENT_REPORT, "構成Aの分離",
                       "未検証の報告", Support.UNKNOWN, "未検証"))
    records.add(Record("revision", Kind.EVENT_REPORT, "構成Aの分離",
                       "別の根拠が追加", Support.SUPPORTED, "独立した別資料と申告、外部審査待ち"))
    records.add(Record("cycle_a", Kind.INFERENCE, "X", None,
                       Support.SUPPORTED, "試験", ("cycle_b",)))
    records.add(Record("cycle_b", Kind.INFERENCE, "X", None,
                       Support.SUPPORTED, "試験", ("cycle_a",)))

    req = (Requirement("split_event", Kind.EVENT_REPORT, "構成Aの分離"),)

    def plan(eid: str, case: str, *, intent: str = "分離分類の適用可否を検証",
             prev: str | None = None, declared: str = "2026-11-12T18:00:00+09:00") -> EvaluationPlan:
        return EvaluationPlan(eid, case, intent, "PHYSICAL_SEPARATION",
                              "research-gate", "draft-0", declared, req, prev)

    def sub(op: str = "op_split", inputs: tuple[tuple[str, str], ...] = (("split_event", "split_report"),),
            intent: str = "分離分類の適用可否を検証") -> Submission:
        return Submission(intent, op, inputs, "2026-11-12T19:00:00+09:00")

    expected = [
        (plan("EV-001", "CASE-EX-001"), sub(op="op_select"), Reason.OPERATION_CLASS_MISMATCH),
        (plan("EV-002", "CASE-TYP-002"), sub(inputs=(("split_event", "mean_20"),)), Reason.TYPE_MISMATCH),
        (plan("EV-003", "CASE-INF-003"), sub(inputs=()), Reason.REQUIRED_INPUT_MISSING),
        (plan("EV-004", "CASE-REV-005"), sub(intent="分離の成立条件を後から作る"), Reason.INTENT_DRIFT),
        (plan("EV-005", "CASE-RULE-008", declared="2026-11-12T19:10:00+09:00"), sub(), Reason.RULE_NOT_PREFIXED),
        (plan("EV-006", "CASE-SRC-007"), sub(inputs=(("split_event", "unsupported"),)), Reason.UNSUPPORTED_RECORD),
        (plan("EV-007", "CASE-HIS-004"), sub(), Reason.READY_FOR_DOMAIN_REVIEW),
        (plan("EV-008", "CASE-REC-006", prev="EV-003"),
         sub(inputs=(("split_event", "revision"),)), Reason.READY_FOR_DOMAIN_REVIEW),
    ]
    for p, s, wanted in expected:
        entry = gate(p, s, records, audit)
        assert entry.reason == wanted, (p.case_id, entry.reason, wanted)
        print(f"{p.case_id} | {entry.verdict.value:8} | {entry.reason.value}")

    # 旧停止は削除されず、新規評価の parent で接続される。
    assert audit.entries[2].verdict == Verdict.STOPPED
    assert audit.entries[7].previous_evaluation_id == "EV-003"
    assert set(audit.affected_by("split_report", records)) == {"EV-007"}
    # EV-008 は新しい記録が独立根拠であるという試験条件に依存する。
    # 旧評価への履歴リンクはあっても、旧情報への根拠依存とは異なる。

    # 異なる記録IDでの追記だけが許可される。
    try:
        records.add(Record("split_report", Kind.EVENT_REPORT, "X", None, Support.UNKNOWN, "改ざん"))
        raise AssertionError("上書きが遮断されない")
    except ValueError:
        pass
    assert dependency_issue("cycle_a", records) == Reason.DEPENDENCY_CYCLE

    history = HistoryLinks()
    history.add(HistoryNode("H0", "common-history-record", ()))
    history.add(HistoryNode("S", "split-record", ("H0",)))
    history.add(HistoryNode("H1", "branch-A-record", ("S",)))
    history.add(HistoryNode("H2", "branch-B-record", ("S",)))
    history.add(HistoryNode("M", "merge-record", ("H1", "H2")))
    history.add(HistoryNode("H3", "post-merge-record", ("M",)))
    assert history.predecessors("M") == ("H1", "H2")
    print("PASS: 8評価試験 + 上書き禁止 + 依存循環 + 履歴分岐融合 + 影響評価追跡")


if __name__ == "__main__":
    demo_and_tests()
