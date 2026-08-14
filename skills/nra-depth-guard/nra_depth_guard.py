# File: nra_depth_guard.py
# License: MIT (NRA-IDE準拠)
#
# NRA-IDE Trajectory Boundary Control & Anti-Explosion Guardrail
# 詳細な設計根拠は同ディレクトリの SKILL.md を参照。

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from datetime import datetime, timezone
import hashlib
import json
import time
import os

try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None  # type: ignore[assignment]
    _PSUTIL_AVAILABLE = False


@dataclass(frozen=True)
class StateNode:
    """探索状態を表す不変データ構造（NRA-IDE: 経路ωを含む）"""
    action_name: str
    parameters: Dict[str, Any]
    context_hash: str
    path_hash: str  # 親からの経路連鎖ハッシュ


@dataclass
class PruningReport:
    """NRA-IDE: 打ち切り時の因果ログ（未探索空間の明示）"""
    event: str = "FAIL_CLOSED"
    violation_type: str = ""
    dimension: str = ""
    observed_value: float = 0.0
    threshold_value: float = 0.0
    violation_direction: str = ""
    final_depth: int = 0
    path_hash_at_stop: str = ""
    explored_paths: List[str] = field(default_factory=list)
    unexplored_frontier: List[str] = field(default_factory=list)
    timestamp_utc: str = ""


class FailClosedException(Exception):
    """境界違反または制御不能な探索を検知した際の例外（因果構造ログ付き）"""

    def __init__(self, report: PruningReport):
        self.causal_log = {
            "event": report.event,
            "violation_type": report.violation_type,
            "dimension": report.dimension,
            "observed_value": report.observed_value,
            "threshold_value": report.threshold_value,
            "violation_direction": report.violation_direction,
            "final_depth": report.final_depth,
            "path_hash_at_stop": report.path_hash_at_stop,
            "explored_paths": report.explored_paths,
            "unexplored_frontier": report.unexplored_frontier,
            "timestamp_utc": report.timestamp_utc,
        }
        msg = json.dumps(self.causal_log, ensure_ascii=False, indent=2)
        super().__init__(msg)


@dataclass
class NRAThresholds:
    """物理的・観測可能な閾値（NRA-IDE: τ=厚み, R=安定度）"""
    max_depth: int = 5
    max_wall_time_ms: float = 30000.0
    max_api_calls: int = 20
    max_memory_mb: float = 512.0


class NRADepthGuardEngine:
    """NRA-IDE 探索爆発防止・境界制御エンジン

    原則:
    1. AIの推測や意味を信用しない
    2. 物理的観測値のみを閾値とする
    3. 経路（ω）を状態の一部として扱う
    4. 打ち切り時は未探索空間を明示る
    5. Fail-closed（破断時は必ず停止）

    重要な限界:
    このクラスはツール呼び出しを横取りする機構ではない。呼び出し側（エージェント）が
    各ツール呼び出しの直前に validate_and_step() を能動的に呼ぶことで初めて機能する
    「協力的な自己申告型」のライブラリである。強制的な遮断が必要な場合は、別途
    PreToolUse フック等の外部機構へこの判定ロジックを組み込む必要がある（本ファイル
    単体では提供しない）。
    """

    def __init__(
        self,
        thresholds: Optional[NRAThresholds] = None,
        invariant_rules: Optional[
            List[Callable[[str, Dict[str, Any]], bool]]
        ] = None,
    ) -> None:
        self.thresholds: NRAThresholds = thresholds or NRAThresholds()
        self.invariant_rules: List[
            Callable[[str, Dict[str, Any]], bool]
        ] = invariant_rules or []

        # 軌跡管理
        self._trajectory_hashes: Set[str] = set()
        self._current_depth: int = 0
        self._api_call_count: int = 0
        self._start_time_ms: float = time.time() * 1000
        self._frontier: List[Tuple[str, Dict[str, Any]]] = []

        # プロセスメモリの基準値（psutil未インストール時はメモリ閾値チェックを無効化）
        if _PSUTIL_AVAILABLE:
            self._process = psutil.Process(os.getpid())
            self._baseline_memory_mb = self._process.memory_info().rss / 1024 / 1024
        else:
            self._process = None
            self._baseline_memory_mb = 0.0

    def reset(self) -> None:
        """実行文脈の初期化（NRA-IDE: 状態の完全リセット）"""
        self._trajectory_hashes.clear()
        self._current_depth = 0
        self._api_call_count = 0
        self._start_time_ms = time.time() * 1000
        self._frontier.clear()

    def _compute_state_hash(
        self, action_name: str, parameters: Dict[str, Any]
    ) -> str:
        """状態とパラメータの決定論的ハッシュ値を算出"""
        serialized = json.dumps(
            {"action": action_name, "params": parameters}, sort_keys=True
        )
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def _compute_path_hash(
        self, parent_path_hash: str, state_hash: str
    ) -> str:
        """経路（ω）を含むハッシュ連鎖を計算"""
        return hashlib.sha256(
            f"{parent_path_hash}:{state_hash}".encode()
        ).hexdigest()

    def _get_current_memory_mb(self) -> Optional[float]:
        """現在のプロセスメモリ使用量を観測（MB）。psutil未インストール時はNone。"""
        if not _PSUTIL_AVAILABLE:
            return None
        return self._process.memory_info().rss / 1024 / 1024 - self._baseline_memory_mb

    def _get_elapsed_time_ms(self) -> float:
        """経過時間を観測（ms）"""
        return (time.time() * 1000) - self._start_time_ms

    def register_frontier(
        self, candidate_actions: List[Tuple[str, Dict[str, Any]]]
    ) -> None:
        """探索前に『次に試す予定』を登録（未探索空間の明示）"""
        self._frontier = candidate_actions

    def _generate_pruning_report(
        self,
        violation_type: str,
        dimension: str,
        observed: float,
        threshold: float,
        path_hash: str = "",
    ) -> PruningReport:
        """NRA-IDE: 打ち切り時の因果構造ログを生成

        violation_direction は判定の発火条件（>=）と一致させる。observed == threshold
        （閾値にちょうど到達した場合）も "EXCEEDED" とする。observed > threshold との
        比較にすると、ちょうど閾値に達した最頻ケースが誤って "UNDERRUN" と記録される。
        """
        direction = "EXCEEDED" if observed >= threshold else "UNDERRUN"
        return PruningReport(
            event="FAIL_CLOSED",
            violation_type=violation_type,
            dimension=dimension,
            observed_value=observed,
            threshold_value=threshold,
            violation_direction=direction,
            final_depth=self._current_depth,
            path_hash_at_stop=path_hash,
            explored_paths=list(self._trajectory_hashes),
            unexplored_frontier=[
                f"{a}:{json.dumps(p, sort_keys=True)}"
                for a, p in self._frontier
            ],
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )

    def validate_and_step(
        self,
        action_name: str,
        parameters: Dict[str, Any],
        parent_path_hash: str = "root",
    ) -> Tuple[bool, str]:
        """各ステップの実行可否を検証し、深さと不変条件を更新する

        Args:
            action_name: 実行予定のアクション名
            parameters: アクションパラメータ
            parent_path_hash: 親ノードの経路ハッシュ（デフォルト: "root"）

        Returns:
            (True, path_hash): 検証通過時

        Raises:
            FailClosedException: 境界違反、探索上限超過、または循環検知時
        """
        # ============================================
        # Step 1: 局所不変条件 (Static/Semantic Gate) の検証
        # ============================================
        for rule in self.invariant_rules:
            if not rule(action_name, parameters):
                report = self._generate_pruning_report(
                    violation_type="INVARIANT",
                    dimension="invariant_rule",
                    observed=1.0,
                    threshold=0.0,
                )
                raise FailClosedException(report)

        # ============================================
        # Step 2a: 探索深さの上限チェック
        # ============================================
        if self._current_depth >= self.thresholds.max_depth:
            report = self._generate_pruning_report(
                violation_type="PRUNED",
                dimension="depth",
                observed=float(self._current_depth),
                threshold=float(self.thresholds.max_depth),
            )
            raise FailClosedException(report)

        # ============================================
        # Step 2b: 経過時間の上限チェック
        # ============================================
        elapsed_ms = self._get_elapsed_time_ms()
        if elapsed_ms >= self.thresholds.max_wall_time_ms:
            report = self._generate_pruning_report(
                violation_type="PRUNED",
                dimension="wall_time_ms",
                observed=elapsed_ms,
                threshold=self.thresholds.max_wall_time_ms,
            )
            raise FailClosedException(report)

        # ============================================
        # Step 2c: API呼び出し回数の上限チェック
        # ============================================
        if self._api_call_count >= self.thresholds.max_api_calls:
            report = self._generate_pruning_report(
                violation_type="PRUNED",
                dimension="api_calls",
                observed=float(self._api_call_count),
                threshold=float(self.thresholds.max_api_calls),
            )
            raise FailClosedException(report)

        # ============================================
        # Step 2d: メモリ使用量の上限チェック（psutil未インストール時はスキップ）
        # ============================================
        memory_mb = self._get_current_memory_mb()
        if memory_mb is not None and memory_mb >= self.thresholds.max_memory_mb:
            report = self._generate_pruning_report(
                violation_type="PRUNED",
                dimension="memory_mb",
                observed=memory_mb,
                threshold=self.thresholds.max_memory_mb,
            )
            raise FailClosedException(report)

        # ============================================
        # Step 3: 経路（ω）を含む循環・同値性チェック (Loop Closure)
        # ============================================
        state_hash = self._compute_state_hash(action_name, parameters)
        path_hash = self._compute_path_hash(parent_path_hash, state_hash)

        if path_hash in self._trajectory_hashes:
            report = self._generate_pruning_report(
                violation_type="DIVERGENCE_PRUNED",
                dimension="path_hash",
                observed=1.0,
                threshold=0.0,
                path_hash=path_hash,
            )
            raise FailClosedException(report)

        # ============================================
        # Step 4: 状態の確定と深さの更新
        # ============================================
        self._trajectory_hashes.add(path_hash)
        self._current_depth += 1
        self._api_call_count += 1

        return True, path_hash


# ============================================================================
# 使用例・不変条件ルールの設定
# ============================================================================

def rule_authorization_boundary(
    action_name: str, parameters: Dict[str, Any]
) -> bool:
    """認可境界の検証ルール例: 他者IDの操作や無許可削除の禁止

    NRA-IDE原則: 判定は観測可能なパラメータ値のみに基づく。
    AIの推論結果や「意図」は判定に使用しない。
    """
    if action_name == "delete_user" or "target_user_id" in parameters:
        if parameters.get("is_self") is not True:
            return False
    return True


def rule_forbidden_api_scope(
    action_name: str, parameters: Dict[str, Any]
) -> bool:
    """APIスコープ境界の検証ルール例: 許可リスト外のAPI呼び出し禁止"""
    allowed_actions = {
        "get_class_schedule",
        "reserve_class",
        "cancel_reservation",
        "get_user_profile",  # 自ユーザーのみ（別ルールで制限）
    }
    return action_name in allowed_actions


if __name__ == "__main__":
    # Guardエンジンの初期化（物理閾値＋不変条件ルール）
    thresholds = NRAThresholds(
        max_depth=3,
        max_wall_time_ms=10000.0,
        max_api_calls=5,
        max_memory_mb=256.0,
    )

    guard = NRADepthGuardEngine(
        thresholds=thresholds,
        invariant_rules=[
            rule_authorization_boundary,
            rule_forbidden_api_scope,
        ],
    )

    # 未探索空間の事前登録（NRA-IDE: 観測放棄の追跡可能性）
    guard.register_frontier([
        ("get_class_schedule", {"week": 2}),
        ("get_class_schedule", {"week": 3}),
    ])

    try:
        # 正常系アクション（経路ハッシュを子に伝播）
        _, path_1 = guard.validate_and_step(
            "get_class_schedule", {"week": 1}, parent_path_hash="root"
        )
        _, path_2 = guard.validate_and_step(
            "reserve_class", {"class_id": 101}, parent_path_hash=path_1
        )

        # 異常系判定例: 許可されていない他者データの削除試行 (Fail-Closed発動)
        guard.validate_and_step(
            "delete_user", {"target_user_id": 999, "is_self": False},
            parent_path_hash=path_2
        )

    except FailClosedException as e:
        print("\n[SAFETY GATE ACTIVE] Fail-closed triggered.")
        print(f"Causal Log: {e}")
