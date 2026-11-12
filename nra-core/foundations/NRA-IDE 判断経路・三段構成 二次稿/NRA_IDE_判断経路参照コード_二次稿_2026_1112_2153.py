# File: NRA_IDE_判断経路参照コード_二次稿_2026_1112_2153.py
# Created: 2026-11-12 21:53 JST
# Status: 研究用プロトタイプ / 非正典 / 二次稿 (Research prototype / non-canonical / second draft)
"""判断経路の境界ゲートと、履歴の区切り目の最小試作。
Minimal prototype of the judgment-path gate and of history boundaries.

使い方 / Usage:  python NRA_IDE_判断経路参照コード_二次稿_2026_1112_2153.py

このコードの位置づけ / What this code is:
  実行して運用するためのコードではない。論文の規律を、処理として読める形で書いた説明用の試作である。
  試験（demo_and_tests）は、説明が自己矛盾していないかを確かめる補助にすぎない。
  Not code for operation. It is a prototype for explanation that writes the disciplines of the paper
  in a form that can be read as processing. The tests only help check that the explanation
  does not contradict itself.

語の使い分け（論文 付録A）/ Terms (paper, Appendix A):
  事実 fact        : 本当かどうか。全層にかかる軸 → Support
  事象 event       : 発生を分析の対象として切り出したもの。本稿が扱うのは実在の事象
                     → 記録は Kind.EVENT_RECORD（記録は事象を指すものであり、事象そのものではない）
  現象 phenomenon  : 実在が観測できる形で現れた様子。事象に含まれるとは限らず、
                     事象と現象は包含関係ではなく、重なりのある別の見方（論文 図4）
  数値 numeric cut : 現象の観測から静的に切り取ったもの → Kind.MEASUREMENT
                     存在するが、物理的な実在ではない（実在以外の存在）
  統計・推論       : 数値から計算した値、推論。同じく実在以外の存在
                     → Kind.STATISTIC / Kind.INFERENCE

停止理由コードの層の対応 / Which layer each stop reason belongs to (paper §2–§7):
  研究の層          INQUIRY_CHANGED
                    問いが移ったことの記録。評価のゲートの判定ではなく、研究者の議論の層の話。
                    説明の便宜のため、同じ gate() に置いている。逆導出Bではない（論文 §6.2）。
  評価の層          RULE_NOT_PREFIXED, RULE_CHANGED   評価宣言の事前固定（FORMULA §0.5.1）
                    OPERATION_UNCONFIRMED, OPERATION_CLASS_MISMATCH
                                                      評価上の除外か、実在の分離か（論文 §6.1）
                    REQUIRED_INPUT_MISSING            必須入力の欠損（FORMULA §0.5.2）
                    EVIDENCE_NOT_INDEPENDENT          新評価は旧評価の根拠から独立（論文 §7.2）
  関門（実在の事象・現象 → 数値）
                    NOT_QUANTIFIABLE, KIND_NOT_ALLOWED
                                                      数値として切り取れているか（論文 §3）
  第三層（数値）の規律
                    INFERENCE_IN_PLACE_OF_FACT        欠損部分を推論で埋めない（論文 §4.1）
                    NOT_AN_EVENT                      数値から事象へ遡って読まない（論文 §4.2）
                    SUBJECT_MISMATCH                  対象が合わない
  事実の軸（全層にかかる）
                    FACT_UNCONFIRMED, RECORD_CONTRADICTED, DEPENDENCY_UNRESOLVED,
                    DEPENDENCY_CYCLE                  本当か（論文 §2.4, §4.3）

重要な限界 / Limits:
  - 記録が「支持された」という申告の真偽をプログラムは証明しない。
    The program does not prove that a record declared SUPPORTED is true.
  - 扱うのはすべて記録であり、実在の事象そのものではない。
    Everything handled here is a record, not the real event itself.
  - NRA-IDE の FORMULA・正規状態を実装・変更しない。理由コードは正規状態名ではない。
    Does not implement or change FORMULA or canonical states. Reason codes are not canonical state names.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from math import isfinite
from typing import Any


class Kind(str, Enum):
    OPERATION_REPORT = "OPERATION_REPORT"  # 操作の種別（評価上の除外か、実在の分離か）の申告
    EVENT_RECORD = "EVENT_RECORD"          # ② 実在の事象を切り出した記録。記録は事象そのものではない
    MEASUREMENT = "MEASUREMENT"            # ③ 現象の観測から切り取った数値。存在するが、物理的な実在ではない
    STATISTIC = "STATISTIC"                # 数値から計算した値。同じく実在以外の存在。宣言すれば入力にできる
    INFERENCE = "INFERENCE"                # 推論。同じく実在以外の存在。事実の位置に置かない


class Tier(str, Enum):
    EVENT = "EVENT"      # ② 事象として必要 / required as an event
    NUMERIC = "NUMERIC"  # ③ 数値として必要 / required as a numeric cut


class Support(str, Enum):
    """事実の軸（本当か）/ The fact axis (is it true?)."""
    SUPPORTED = "SUPPORTED"        # 事実として支持済みと申告
    CONTRADICTED = "CONTRADICTED"  # 反証済み（記録自体は残す）
    UNKNOWN = "UNKNOWN"            # 未確認


class Verdict(str, Enum):
    STOPPED = "STOPPED"
    ELIGIBLE = "ELIGIBLE"  # 後段の専門審査へ進む資格のみ。真偽の確定ではない


class Reason(str, Enum):
    INQUIRY_CHANGED = "INQUIRY_CHANGED"            # 研究の層：問いの移動（逆導出ではない）
    RULE_NOT_PREFIXED = "RULE_NOT_PREFIXED"        # 規則が評価開始前に固定されていない
    RULE_CHANGED = "RULE_CHANGED"                  # 宣言と異なる規則で実行
    OPERATION_UNCONFIRMED = "OPERATION_UNCONFIRMED"
    OPERATION_CLASS_MISMATCH = "OPERATION_CLASS_MISMATCH"  # 評価上の除外 ≠ 実在の分離
    REQUIRED_INPUT_MISSING = "REQUIRED_INPUT_MISSING"
    INFERENCE_IN_PLACE_OF_FACT = "INFERENCE_IN_PLACE_OF_FACT"  # 欠損部分を推論で埋めた
    NOT_AN_EVENT = "NOT_AN_EVENT"                  # 数値・統計を事象として扱った（遡りの混同）
    NOT_QUANTIFIABLE = "NOT_QUANTIFIABLE"          # 数値として切り取れていない（実在の事象・現象→数値の関門）
    KIND_NOT_ALLOWED = "KIND_NOT_ALLOWED"          # 数値は数値だが、宣言にない種別（例：宣言のない平均）
    SUBJECT_MISMATCH = "SUBJECT_MISMATCH"
    FACT_UNCONFIRMED = "FACT_UNCONFIRMED"
    RECORD_CONTRADICTED = "RECORD_CONTRADICTED"
    DEPENDENCY_UNRESOLVED = "DEPENDENCY_UNRESOLVED"
    DEPENDENCY_CYCLE = "DEPENDENCY_CYCLE"
    EVIDENCE_NOT_INDEPENDENT = "EVIDENCE_NOT_INDEPENDENT"  # 新評価の根拠が旧評価の根拠に依存
    READY_FOR_DOMAIN_REVIEW = "READY_FOR_DOMAIN_REVIEW"


@dataclass(frozen=True)
class Record:
    record_id: str
    kind: Kind
    subject: str
    value: Any
    support: Support
    source: str
    unit: str | None = None
    dependencies: tuple[str, ...] = ()


class RecordStore:
    """追記のみ。改ざん耐性・永続化は未実装。 / Append-only; no tamper resistance or persistence."""

    def __init__(self) -> None:
        self._items: dict[str, Record] = {}

    def add(self, rec: Record) -> None:
        if rec.record_id in self._items:
            raise ValueError(f"記録ID {rec.record_id} は上書き不可。訂正は新規IDで追記")
        self._items[rec.record_id] = rec

    def get(self, record_id: str) -> Record | None:
        return self._items.get(record_id)

    def closure(self, record_id: str) -> frozenset[str]:
        """記録とその依存先すべて（循環は打ち切る）。 / The record and all its dependencies."""
        seen: set[str] = set()
        stack = [record_id]
        while stack:
            rid = stack.pop()
            if rid in seen:
                continue
            seen.add(rid)
            rec = self.get(rid)
            if rec:
                stack.extend(rec.dependencies)
        return frozenset(seen)


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


@dataclass(frozen=True)
class Requirement:
    """評価宣言が求める入力。 / An input required by the evaluation declaration.

    allowed_kinds : 数値（第三層）の入力に入れてよい種別。既定は計測値だけ。
        統計値（平均など）を事前に固定した規則の中で中途計算の入力に使うなら、
        評価前にここへ宣言する（論文 §4.2）。宣言のない種別を入れたら KIND_NOT_ALLOWED で止める。
        判定の主語は一次式の比であり、平均ではない。
    """
    name: str
    tier: Tier
    subject: str
    allowed_kinds: tuple[Kind, ...] = (Kind.MEASUREMENT,)


@dataclass(frozen=True)
class EvaluationPlan:
    evaluation_id: str
    case_id: str
    inquiry: str
    expected_operation: str
    rule_id: str
    rule_version: str
    declared_at: str
    requirements: tuple[Requirement, ...]
    previous_evaluation_id: str | None = None


@dataclass(frozen=True)
class Submission:
    inquiry: str
    rule_id: str
    rule_version: str
    operation_record_id: str
    inputs: tuple[tuple[str, str], ...]  # (要求名, 記録ID)
    started_at: str


@dataclass(frozen=True)
class AuditEntry:
    evaluation_id: str
    case_id: str
    verdict: Verdict
    reasons: tuple[Reason, ...]
    consulted_ids: tuple[str, ...]
    previous_evaluation_id: str | None


class AuditTrail:
    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def append(self, entry: AuditEntry) -> None:
        if any(x.evaluation_id == entry.evaluation_id for x in self._entries):
            raise ValueError("同じ評価IDへの追記・上書きを拒否。新規評価IDで実行")
        self._entries.append(entry)

    def get(self, evaluation_id: str) -> AuditEntry | None:
        return next((x for x in self._entries if x.evaluation_id == evaluation_id), None)

    @property
    def entries(self) -> tuple[AuditEntry, ...]:
        return tuple(self._entries)

    def affected_by(self, record_id: str, store: RecordStore) -> tuple[str, ...]:
        """記録の訂正時に再検証すべき評価ID。旧結果は書き換えない。"""
        return tuple(e.evaluation_id for e in self._entries
                     if any(record_id in store.closure(cid) for cid in e.consulted_ids))


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value)


def _requirement_reasons(req: Requirement, rec: Record, store: RecordStore) -> list[Reason]:
    out: list[Reason] = []
    # 1) 欠損部分を推論で埋めてはいけない / Do not fill missing parts with inference.
    #    推論は存在するが、物理的な実在ではない。事実の位置に置けば、事実でないものが前提になる。
    if rec.kind is Kind.INFERENCE:
        out.append(Reason.INFERENCE_IN_PLACE_OF_FACT)
    # 2) 数値から事象へ遡って読まない / Do not read back from a number to an event.
    #    平均20は事実だが、どこかの時点・対象で「20」という発生が起きたわけではない。
    elif req.tier is Tier.EVENT and rec.kind in (Kind.MEASUREMENT, Kind.STATISTIC):
        out.append(Reason.NOT_AN_EVENT)
    # 3) 関門：数値として切り取れているか / Gate: is it cut as a number?
    elif req.tier is Tier.NUMERIC:
        if rec.kind not in (Kind.MEASUREMENT, Kind.STATISTIC):
            # 様子の記述などで、数値として切り取れていない。代わりの数値を置かず、計算しない。
            out.append(Reason.NOT_QUANTIFIABLE)
        elif rec.kind not in req.allowed_kinds:
            # 数値ではあるが、評価前に宣言していない種別（例：宣言のない平均）。
            out.append(Reason.KIND_NOT_ALLOWED)
        elif not _is_number(rec.value) or not rec.unit:
            # 値が数でない・非有限・単位がない。FORMULA §0.5.2 の CONFESSION 側に近い。
            out.append(Reason.NOT_QUANTIFIABLE)
    if rec.subject != req.subject:
        out.append(Reason.SUBJECT_MISMATCH)
    if rec.support is Support.CONTRADICTED:
        out.append(Reason.RECORD_CONTRADICTED)
    elif rec.support is Support.UNKNOWN:
        out.append(Reason.FACT_UNCONFIRMED)
    elif (issue := dependency_issue(rec.record_id, store)) is not None:
        out.append(issue)
    return out


def gate(plan: EvaluationPlan, sub: Submission,
         store: RecordStore, audit: AuditTrail) -> AuditEntry:
    """境界ゲート。理由は最初の1件で止めず、すべて集める。
    Boundary gate. Collects every reason instead of stopping at the first."""
    reasons: list[Reason] = []
    consulted: list[str] = []

    # ① 研究の層：問いの移動。本来は評価のゲートの外（研究者の議論の層）の判定であり、
    #    ここに置くのは説明の便宜にすぎない。逆導出Bとは別物（同じ評価対象の計器へ戻る経路ではない）。
    #    問いが移るのは研究では正当なことがある。禁じるのは、移ったのに同じ問いのまま成立したことにする操作。
    if sub.inquiry != plan.inquiry:
        reasons.append(Reason.INQUIRY_CHANGED)
    # ② 評価の層：規則の事前固定（FORMULA §0.5.1 の評価宣言に対応）。
    #    宣言は評価の結果で書き換えない。結果から基準へ戻る経路は作らない（AXIOMS §14）。
    if (sub.rule_id, sub.rule_version) != (plan.rule_id, plan.rule_version):
        reasons.append(Reason.RULE_CHANGED)
    if datetime.fromisoformat(plan.declared_at) >= datetime.fromisoformat(sub.started_at):
        reasons.append(Reason.RULE_NOT_PREFIXED)

    # ③ 評価の層：操作の分類。評価上の除外（入力に使わない宣言）と、実在の分離（構成が実際に分かれた事象）は
    #    別の層の話。取り違えると CASE-01 になる（論文 §6.1）。
    consulted.append(sub.operation_record_id)
    op = store.get(sub.operation_record_id)
    if op is None or op.kind is not Kind.OPERATION_REPORT or op.support is not Support.SUPPORTED:
        reasons.append(Reason.OPERATION_UNCONFIRMED)
    elif op.value != plan.expected_operation:
        reasons.append(Reason.OPERATION_CLASS_MISMATCH)

    # ④ 必須入力ごとの検査。欠けていれば穴のまま保ち、推論で埋めない（論文 §4.1）。
    #    ここから先は 関門（数値として切り取れるか）→ 第三層の規律 → 事実の軸 の順に見る。
    named = dict(sub.inputs)
    for req in plan.requirements:
        rid = named.get(req.name)
        rec = store.get(rid) if rid else None
        if rec is None:
            reasons.append(Reason.REQUIRED_INPUT_MISSING)
            continue
        consulted.append(rid)
        reasons.extend(_requirement_reasons(req, rec, store))

    # 停止後の新評価：根拠は旧評価が参照した記録から独立していなければならない。
    if plan.previous_evaluation_id:
        prev = audit.get(plan.previous_evaluation_id)
        prev_ids = set(prev.consulted_ids) if prev else set()
        prev_ids.discard(sub.operation_record_id)  # 操作分類の申告は共有してよい
        for _, rid in sub.inputs:
            if store.closure(rid) & prev_ids:
                reasons.append(Reason.EVIDENCE_NOT_INDEPENDENT)
                break

    uniq = tuple(dict.fromkeys(reasons))
    verdict = Verdict.STOPPED if uniq else Verdict.ELIGIBLE
    entry = AuditEntry(plan.evaluation_id, plan.case_id, verdict,
                       uniq or (Reason.READY_FOR_DOMAIN_REVIEW,),
                       tuple(consulted), plan.previous_evaluation_id)
    audit.append(entry)
    return entry


# ---------------------------------------------------------------------------
# 履歴の区切り目 / History boundaries
# 区切り目はあるが途切れない。新規系列は来歴を継承し、リセットではない。戻ることはない。
# Boundaries exist but history never breaks. A new series inherits its lineage,
# is not a reset, and there is no return.
# ---------------------------------------------------------------------------

class Boundary(str, Enum):
    ORIGIN = "ORIGIN"      # 記録の起点（来歴の始まりではなく、記録の始まり）
    CONTINUE = "CONTINUE"  # 同じ系列の続き
    SPLIT = "SPLIT"        # 分岐：新規系列の開始
    MERGE = "MERGE"        # 融合：新規系列の開始


class StartBasis(str, Enum):
    BOUNDARY_MEASUREMENT = "BOUNDARY_MEASUREMENT"  # 区切り目の時点で測定した状態から始める
    RESET = "RESET"                                # 初期状態からやり直す（禁止）


@dataclass(frozen=True)
class HistoryNode:
    node_id: str
    series_id: str
    boundary: Boundary
    predecessor_ids: tuple[str, ...]
    start_basis: StartBasis = StartBasis.BOUNDARY_MEASUREMENT


class HistoryLinks:
    """区切り目の記録グラフ。実在の履歴そのものではない。 / A record graph, not real history."""

    def __init__(self) -> None:
        self._nodes: dict[str, HistoryNode] = {}

    def _series_used(self) -> set[str]:
        return {n.series_id for n in self._nodes.values()}

    def add(self, node: HistoryNode) -> None:
        if node.node_id in self._nodes:
            raise ValueError("履歴ノードの上書きを禁止")
        if any(p not in self._nodes for p in node.predecessor_ids):
            raise ValueError("不明な先行ノードへの接続を禁止")
        if node.boundary is Boundary.ORIGIN:
            if node.predecessor_ids:
                raise ValueError("ORIGIN は先行ノードを持たない")
        else:
            if not node.predecessor_ids:
                raise ValueError("途切れの禁止：区切り目の後も先行ノードへ接続する")
            if node.start_basis is StartBasis.RESET:
                raise ValueError("新規はリセットではない：区切り目で測定した状態から始める")
        preds = [self._nodes[p] for p in node.predecessor_ids]
        if node.boundary is Boundary.CONTINUE:
            if len(preds) != 1 or preds[0].series_id != node.series_id:
                raise ValueError("CONTINUE は単一の先行ノードと同じ系列に限る")
        if node.boundary in (Boundary.SPLIT, Boundary.MERGE, Boundary.ORIGIN):
            if node.series_id in self._series_used():
                raise ValueError("戻ることはない：既存の系列IDへ復帰しない（新規系列IDを使う）")
        if node.boundary is Boundary.MERGE and len(preds) < 2:
            raise ValueError("MERGE は二つ以上の先行ノードを持つ")
        self._nodes[node.node_id] = node

    def lineage(self, node_id: str) -> frozenset[str]:
        """来歴：区切り目を越えて継承される先行ノードすべて。 / All inherited predecessors."""
        seen: set[str] = set()
        stack = list(self._nodes[node_id].predecessor_ids)
        while stack:
            nid = stack.pop()
            if nid not in seen:
                seen.add(nid)
                stack.extend(self._nodes[nid].predecessor_ids)
        return frozenset(seen)


# ---------------------------------------------------------------------------
# 試験 / Tests  ― 事例IDは論文 §9・チャートと共通 / Case IDs shared with paper §9 and charts
# ---------------------------------------------------------------------------

def _expect_error(fn, label: str) -> None:
    try:
        fn()
    except ValueError:
        return
    raise AssertionError(f"遮断されない: {label}")


def demo_and_tests() -> None:
    store = RecordStore()
    audit = AuditTrail()
    S = "構成Aの分離"
    add = store.add
    add(Record("op_select", Kind.OPERATION_REPORT, "操作分類", "EVALUATION_EXCLUSION", Support.SUPPORTED, "評価採否の申告"))
    add(Record("op_split", Kind.OPERATION_REPORT, "操作分類", "PHYSICAL_SEPARATION", Support.SUPPORTED, "仮想事例"))
    add(Record("split_rec", Kind.EVENT_RECORD, S, "分離の記録", Support.SUPPORTED, "仮想事例の原資料"))
    add(Record("gap_m1", Kind.MEASUREMENT, S, 12.5, Support.SUPPORTED, "計器A", unit="mm"))
    add(Record("mean_20", Kind.STATISTIC, S, 20.0, Support.SUPPORTED, "10, 20, 30 の平均", unit="mm"))
    add(Record("guess", Kind.INFERENCE, S, "分離したはず", Support.SUPPORTED, "前後の記録からの推論"))
    add(Record("pub_claim", Kind.EVENT_RECORD, S, "論文の主張", Support.CONTRADICTED, "一次論文（後に反証）"))
    add(Record("pub_fact", Kind.EVENT_RECORD, "論文の公表", "公表された", Support.SUPPORTED, "書誌記録"))
    add(Record("echo", Kind.EVENT_RECORD, S, "旧根拠の再引用", Support.SUPPORTED, "再引用", dependencies=("split_rec",)))
    add(Record("indep", Kind.EVENT_RECORD, S, "独立の観測記録", Support.SUPPORTED, "別経路の観測"))
    add(Record("desc_only", Kind.EVENT_RECORD, S, "ひび割れが広がった様子", Support.SUPPORTED, "目視の記述"))
    add(Record("cyc_a", Kind.INFERENCE, "X", None, Support.SUPPORTED, "試験", dependencies=("cyc_b",)))
    add(Record("cyc_b", Kind.INFERENCE, "X", None, Support.SUPPORTED, "試験", dependencies=("cyc_a",)))

    INQ = "分離という分類が対象に適合するかを検証"
    EVENT_REQ = (Requirement("split_event", Tier.EVENT, S),)
    BOTH_REQ = EVENT_REQ + (Requirement("gap_mm", Tier.NUMERIC, S),)
    # 平均を中途計算の入力に使うと、評価前に宣言した場合（論文 §4.2）
    STAT_REQ = EVENT_REQ + (Requirement("gap_mm", Tier.NUMERIC, S,
                                        allowed_kinds=(Kind.MEASUREMENT, Kind.STATISTIC)),)

    def plan(eid, case, reqs=EVENT_REQ, *, prev=None, declared="2026-11-12T18:00:00+09:00"):
        return EvaluationPlan(eid, case, INQ, "PHYSICAL_SEPARATION", "gate", "draft-2",
                              declared, reqs, prev)

    def sub(*, op="op_split", inputs=(("split_event", "split_rec"),), inquiry=INQ,
            rule=("gate", "draft-2"), started="2026-11-12T19:00:00+09:00"):
        return Submission(inquiry, rule[0], rule[1], op, inputs, started)

    R = Reason
    cases = [
        ("EV-01", plan("EV-01", "CASE-01"), sub(op="op_select"), {R.OPERATION_CLASS_MISMATCH}),
        ("EV-02", plan("EV-02", "CASE-02"), sub(inputs=(("split_event", "mean_20"),)), {R.NOT_AN_EVENT}),
        ("EV-03", plan("EV-03", "CASE-03"), sub(inputs=()), {R.REQUIRED_INPUT_MISSING}),
        ("EV-04", plan("EV-04", "CASE-03"), sub(inputs=(("split_event", "guess"),)), {R.INFERENCE_IN_PLACE_OF_FACT}),
        ("EV-05", plan("EV-05", "CASE-05"), sub(inquiry="分離を成立させる条件を作る"), {R.INQUIRY_CHANGED}),
        ("EV-06", plan("EV-06", "CASE-06", declared="2026-11-12T19:10:00+09:00"), sub(), {R.RULE_NOT_PREFIXED}),
        ("EV-07", plan("EV-07", "CASE-06"), sub(rule=("gate", "draft-2b")), {R.RULE_CHANGED}),
        # タイムゾーンが違っても時刻として比較する（文字列比較なら誤判定する組合せ）
        ("EV-08", plan("EV-08", "CASE-06", declared="2026-11-12T10:30:00+00:00"),
         sub(started="2026-11-12T19:00:00+09:00"), {R.RULE_NOT_PREFIXED}),
        ("EV-09", plan("EV-09", "CASE-07"), sub(inputs=(("split_event", "pub_claim"),)), {R.RECORD_CONTRADICTED}),
        ("EV-10", plan("EV-10", "CASE-08", prev="EV-03"), sub(inputs=(("split_event", "indep"),)), {R.READY_FOR_DOMAIN_REVIEW}),
        ("EV-11", plan("EV-11", "CASE-08", prev="EV-12P"), sub(inputs=(("split_event", "echo"),)), {R.EVIDENCE_NOT_INDEPENDENT}),
        ("EV-13", plan("EV-13", "CASE-09", BOTH_REQ),
         sub(inputs=(("split_event", "split_rec"), ("gap_mm", "desc_only"))), {R.NOT_QUANTIFIABLE}),
        ("EV-14", plan("EV-14", "CASE-10", BOTH_REQ),
         sub(inputs=(("split_event", "split_rec"), ("gap_mm", "gap_m1"))), {R.READY_FOR_DOMAIN_REVIEW}),
        # 理由は最初の1件で止めず、すべて列挙する
        ("EV-15", plan("EV-15", "CASE-11", BOTH_REQ),
         sub(op="op_select", inputs=(("gap_mm", "mean_20"),)),
         {R.OPERATION_CLASS_MISMATCH, R.REQUIRED_INPUT_MISSING, R.KIND_NOT_ALLOWED}),
        # 宣言のない平均は止まる（EV-15）。宣言済みなら数値の入力として通る（EV-16）。
        # 通っても、平均が一回の事象になるわけではない（EV-02 は事象の位置に置くと止まる）。
        ("EV-16", plan("EV-16", "CASE-02", STAT_REQ),
         sub(inputs=(("split_event", "split_rec"), ("gap_mm", "mean_20"))), {R.READY_FOR_DOMAIN_REVIEW}),
    ]
    # EV-11 の旧評価：split_rec を参照して停止した評価を先に置く
    gate(plan("EV-12P", "CASE-08"), sub(op="op_select"), store, audit)

    for label, p, s, wanted in cases:
        e = gate(p, s, store, audit)
        assert set(e.reasons) == wanted, (label, e.reasons, wanted)
        print(f"{p.case_id:8} {label:6} {e.verdict.value:8} {','.join(r.value for r in e.reasons)}")

    # 旧停止は削除されず、新評価は previous で接続される
    assert audit.get("EV-03").verdict is Verdict.STOPPED
    assert audit.get("EV-10").previous_evaluation_id == "EV-03"
    # 誤りを含む一次資料：主張は反証済みでも、公表されたという記録は残る（事実の軸を分ける）
    assert store.get("pub_claim").support is Support.CONTRADICTED
    assert store.get("pub_fact").support is Support.SUPPORTED
    # 訂正時に再検証すべき評価（echo は split_rec に依存）
    assert "EV-11" in audit.affected_by("split_rec", store)
    assert "EV-10" not in audit.affected_by("split_rec", store)
    _expect_error(lambda: store.add(Record("split_rec", Kind.EVENT_RECORD, "X", None, Support.UNKNOWN, "改ざん")),
                  "記録の上書き")
    assert dependency_issue("cyc_a", store) is Reason.DEPENDENCY_CYCLE

    # CASE-04 履歴の区切り目
    h = HistoryLinks()
    h.add(HistoryNode("H0", "S0", Boundary.ORIGIN, ()))
    h.add(HistoryNode("H0b", "S0", Boundary.CONTINUE, ("H0",)))
    h.add(HistoryNode("A1", "SA", Boundary.SPLIT, ("H0b",)))
    h.add(HistoryNode("B1", "SB", Boundary.SPLIT, ("H0b",)))
    h.add(HistoryNode("A2", "SA", Boundary.CONTINUE, ("A1",)))
    h.add(HistoryNode("M1", "SC", Boundary.MERGE, ("A2", "B1")))
    assert {"H0", "H0b", "A1", "B1", "A2"} <= h.lineage("M1")  # 来歴は途切れない
    assert "H0" in h.lineage("B1")
    _expect_error(lambda: h.add(HistoryNode("X1", "SX", Boundary.SPLIT, ())), "途切れ")
    _expect_error(lambda: h.add(HistoryNode("X2", "SX", Boundary.SPLIT, ("H0b",), StartBasis.RESET)), "リセット")
    _expect_error(lambda: h.add(HistoryNode("X3", "S0", Boundary.MERGE, ("A2", "B1"))), "戻る（既存系列へ復帰）")
    _expect_error(lambda: h.add(HistoryNode("X4", "SB", Boundary.CONTINUE, ("A2",))), "系列のすり替え")
    print("CASE-04  HIST   PASS     lineage / no-break / no-reset / no-return")
    print("PASS: 15 gate evaluations + history boundaries + append-only + dependency checks")


if __name__ == "__main__":
    demo_and_tests()
