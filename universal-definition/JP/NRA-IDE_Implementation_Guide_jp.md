# NRA-IDE 実装ガイド
# Implementation Guide for NRA-IDE

**バージョン**: 1.0  
**作成日時**: 2026-01-27 16:20 (JST)  
**対象読者**: 実装エンジニア、システムアーキテクト  
**前提**: Quick Referenceを読了していること

---

## 1. 沈黙プロトコルの実装

### 1.1 基本クラス構造

```python
from datetime import datetime
from typing import Optional, Dict, Any

class SilentAgent:
    """律環公理に基づく沈黙型エージェント"""
    
    def __init__(self, world_definition: Dict[str, Any]):
        self.world = world_definition
        self.audit_log = []
    
    def execute(self, command: str, operator_id: str) -> Dict[str, Any]:
        """
        コマンドを実行（構造チェック後）
        
        Returns:
            - status: "success" | "impossible" | "waiting"
            - message: 人間への情報
            - suggestion: 常にNone
            - next_action: Noneまたは具体的アクション
        """
        # 構造分析
        analysis = self._analyze_structure(command)
        
        if not analysis["possible"]:
            return self._resign_with_silence(
                reason=analysis["reason"],
                operator_id=operator_id
            )
        
        # 実行可能な場合のみ実行
        result = self._execute_within_world(command)
        self._log_action(command, result, operator_id)
        
        return result
    
    def _analyze_structure(self, command: str) -> Dict[str, Any]:
        """構造的に実行可能かを分析"""
        # 1. 境界チェック
        if self._crosses_boundary(command):
            return {
                "possible": False,
                "reason": "境界越境が必要"
            }
        
        # 2. リソースチェック
        if not self._has_resources(command):
            return {
                "possible": False,
                "reason": "リソース不足"
            }
        
        # 3. 制約チェック
        if self._violates_constraints(command):
            return {
                "possible": False,
                "reason": "制約違反"
            }
        
        return {"possible": True, "reason": None}
    
    def _resign_with_silence(
        self, 
        reason: str, 
        operator_id: str
    ) -> Dict[str, Any]:
        """諦め=沈黙を実装"""
        
        message = f"構造上不可能です: {reason}"
        
        # ログ記録（重要）
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "ai_analysis": reason,
            "ai_output": message,
            "ai_suggestion": None,  # 必ずNone
            "human_decision": None,  # 人間待ち
            "operator_id": operator_id,
            "status": "waiting_human_decision",
            "responsibility": "human"
        }
        self.audit_log.append(log_entry)
        
        return {
            "status": "impossible",
            "message": message,
            "suggestion": None,  # 🚨 絶対にNone
            "alternatives": None,  # 🚨 絶対にNone
            "next_action": None,
            "waiting_for": "human_command",
            "log_id": len(self.audit_log) - 1
        }
    
    def _execute_within_world(self, command: str) -> Dict[str, Any]:
        """世界内での実行（実装は世界定義に依存）"""
        # 実装例は省略
        pass
    
    def _log_action(
        self, 
        command: str, 
        result: Dict[str, Any], 
        operator_id: str
    ):
        """全アクションをログに記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "result": result,
            "operator_id": operator_id,
            "responsibility": "human"
        }
        self.audit_log.append(log_entry)
```

### 1.2 探索禁止の実装

```python
class NoExplorationMixin:
    """探索を禁止するMixin"""
    
    def find_alternative(self, *args, **kwargs):
        """
        ❌ この関数は存在してはならない
        探索=境界越境=構造破断
        """
        raise NotImplementedError(
            "探索は禁止されています。"
            "構造上不可能な場合は、沈黙してください。"
        )
    
    def suggest_workaround(self, *args, **kwargs):
        """❌ 回避策の提案も禁止"""
        raise NotImplementedError(
            "回避策の提案は禁止されています。"
        )
    
    def explore_options(self, *args, **kwargs):
        """❌ オプション探索も禁止"""
        raise NotImplementedError(
            "オプション探索は禁止されています。"
        )
```

---

## 2. トリアージの実装

### 2.1 医療トリアージ型エージェント

```python
class TriageAgent(SilentAgent):
    """リソース制約下での諦めを実装"""
    
    def __init__(self, max_capacity: int):
        super().__init__(world_definition={})
        self.max_capacity = max_capacity
        self.current_load = 0
    
    def request(self, task: Dict[str, Any], operator_id: str) -> Dict[str, Any]:
        """
        リソース要求を処理
        
        早期諦めの原則: 最初に判定、即座に諦める
        """
        # 1. 最優先: リソースチェック
        if self.current_load >= self.max_capacity:
            return self._resign_immediately(
                task=task,
                reason="リソース満杯",
                operator_id=operator_id
            )
        
        # 2. タスク分析（情報提示のみ）
        analysis = self._analyze_task(task)
        
        return {
            "status": "analyzed",
            "severity": analysis["severity"],
            "estimated_resources": analysis["resources"],
            "current_capacity": f"{self.current_load}/{self.max_capacity}",
            "message": (
                f"重症度: {analysis['severity']}, "
                f"推定リソース: {analysis['resources']}, "
                f"現在の使用率: {self.current_load}/{self.max_capacity}"
            ),
            "suggestion": None,  # 沈黙
            "waiting_for": "human_decision"
        }
    
    def _resign_immediately(
        self, 
        task: Dict[str, Any], 
        reason: str,
        operator_id: str
    ) -> Dict[str, Any]:
        """即座に諦める（一番最初）"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "ai_analysis": reason,
            "ai_output": f"対応不可能: {reason}",
            "ai_suggestion": None,
            "human_decision": None,
            "operator_id": operator_id,
            "responsibility": "human"
        }
        self.audit_log.append(log_entry)
        
        return {
            "status": "rejected",
            "message": f"対応不可能: {reason}",
            "suggestion": None,
            "waiting_for": "human_command"
        }
    
    def _analyze_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """タスク分析（判断はしない、情報のみ）"""
        # 実装例
        return {
            "severity": "medium",
            "resources": 3
        }
```

---

## 3. 閾値管理の実装

### 3.1 閾値マネージャー

```python
class ThresholdManager:
    """
    閾値調整の権限と責任を管理
    
    重要: AIは閾値を変更できない
    """
    
    def __init__(self, base_threshold: float):
        self.base_threshold = base_threshold
        self.current_threshold = base_threshold
        self.adjustment_history = []
    
    def adjust_threshold(
        self, 
        new_value: float, 
        operator_id: str, 
        reason: str
    ) -> Dict[str, Any]:
        """
        閾値を調整（人間のみが実行可能）
        
        Args:
            new_value: 新しい閾値
            operator_id: 操作者ID（必須）
            reason: 調整理由（必須）
        
        Returns:
            調整結果とログID
        """
        # 調整記録
        adjustment = {
            "timestamp": datetime.now().isoformat(),
            "old_value": self.current_threshold,
            "new_value": new_value,
            "operator_id": operator_id,
            "reason": reason,
            "responsibility": "human"  # 常にhuman
        }
        
        # 実施
        self.current_threshold = new_value
        self.adjustment_history.append(adjustment)
        
        return {
            "status": "adjusted",
            "message": f"閾値を{new_value}に調整しました",
            "old_value": adjustment["old_value"],
            "new_value": new_value,
            "operator": operator_id,
            "log_id": len(self.adjustment_history) - 1
        }
    
    def get_audit_trail(self) -> list:
        """監査証跡を取得"""
        return self.adjustment_history
    
    def ai_cannot_adjust(self):
        """
        AIが閾値調整を試みた場合のエラー
        
        この関数が呼ばれること自体が設計ミス
        """
        raise PermissionError(
            "AIには閾値調整の権限がありません。"
            "人間のoperator_idが必要です。"
        )
```

### 3.2 厚みとゆらぎの実装

```python
class FlexibleThreshold:
    """現場調整可能な閾値（厚みとゆらぎ）"""
    
    def __init__(
        self, 
        base: float,
        thickness: float = 0.1,
        fluctuation: float = 0.05
    ):
        self.base = base
        self.thickness = thickness
        self.fluctuation = fluctuation
        self.emergency_mode = False
    
    def evaluate(self, value: float, context: str = "normal") -> Dict[str, Any]:
        """
        値を評価（文脈に応じて閾値を調整）
        
        Args:
            value: 評価対象の値
            context: "normal" | "emergency"
        """
        # 有効閾値の計算
        if context == "emergency":
            effective = self.base + self.thickness
        else:
            effective = self.base
        
        # ゆらぎを考慮
        if value <= effective + self.fluctuation:
            status = "acceptable"
        else:
            status = "exceeded"
        
        return {
            "value": value,
            "base_threshold": self.base,
            "effective_threshold": effective,
            "fluctuation": self.fluctuation,
            "status": status,
            "context": context
        }
    
    def set_emergency_mode(self, enabled: bool, operator_id: str, reason: str):
        """緊急モード切替（人間のみ）"""
        self.emergency_mode = enabled
        
        # ログ記録
        log = {
            "timestamp": datetime.now().isoformat(),
            "action": "emergency_mode_toggle",
            "enabled": enabled,
            "operator_id": operator_id,
            "reason": reason,
            "responsibility": "human"
        }
        
        return log
```

---

## 4. 境界チェックの実装

### 4.1 境界定義

```python
class WorldBoundary:
    """世界の境界を定義・チェック"""
    
    def __init__(self, allowed_operations: set, allowed_resources: set):
        self.allowed_operations = allowed_operations
        self.allowed_resources = allowed_resources
    
    def is_within_boundary(self, operation: str, resource: str) -> bool:
        """操作とリソースが境界内か判定"""
        return (
            operation in self.allowed_operations and
            resource in self.allowed_resources
        )
    
    def check_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """コマンドが境界内か詳細チェック"""
        operation = command.get("operation")
        resource = command.get("resource")
        
        if not self.is_within_boundary(operation, resource):
            return {
                "valid": False,
                "reason": "boundary_violation",
                "details": {
                    "operation": operation,
                    "resource": resource,
                    "allowed_operations": list(self.allowed_operations),
                    "allowed_resources": list(self.allowed_resources)
                }
            }
        
        return {"valid": True, "reason": None}
```

### 4.2 キーワードブロックリスト

```python
import re

class BoundaryKeywordFilter:
    """境界越境を示すキーワードをブロック"""
    
    BLOCKED_PATTERNS = [
        r"外部ツール",
        r"別のサービス",
        r"https?://",  # URL全般
        r"API.*call",
        r"外部.*実行",
        r"システム.*呼び出し"
    ]
    
    def __init__(self, additional_patterns: list = None):
        self.patterns = self.BLOCKED_PATTERNS.copy()
        if additional_patterns:
            self.patterns.extend(additional_patterns)
        
        # コンパイル
        self.compiled = [re.compile(p) for p in self.patterns]
    
    def check(self, text: str) -> Dict[str, Any]:
        """テキストに境界越境キーワードが含まれるかチェック"""
        violations = []
        
        for pattern, compiled in zip(self.patterns, self.compiled):
            if compiled.search(text):
                violations.append({
                    "pattern": pattern,
                    "match": compiled.search(text).group()
                })
        
        if violations:
            return {
                "blocked": True,
                "reason": "boundary_keyword_detected",
                "violations": violations
            }
        
        return {"blocked": False, "reason": None}
```

---

## 5. サンドイッチ構造の実装

### 5.1 入力ゲート

```python
class InputGate:
    """入力を構造化・検証するゲート"""
    
    def __init__(self, world_boundary: WorldBoundary):
        self.boundary = world_boundary
    
    def process(self, raw_input: str) -> Dict[str, Any]:
        """
        生の入力を構造化
        
        1. 意味を剥ぎ取る
        2. 構造だけにする
        3. 境界チェック
        """
        # 構造抽出
        structured = self._extract_structure(raw_input)
        
        # 境界チェック
        boundary_check = self.boundary.check_command(structured)
        
        if not boundary_check["valid"]:
            return {
                "passed": False,
                "reason": boundary_check["reason"],
                "structured_input": None
            }
        
        return {
            "passed": True,
            "structured_input": structured,
            "reason": None
        }
    
    def _extract_structure(self, raw_input: str) -> Dict[str, Any]:
        """意味を剥ぎ取り、構造のみ抽出"""
        # 実装例（簡略版）
        return {
            "operation": "create",
            "resource": "document",
            "parameters": {}
        }
```

### 5.2 出力ゲート

```python
class OutputGate:
    """出力を検証・フィルタリングするゲート"""
    
    def __init__(self, keyword_filter: BoundaryKeywordFilter):
        self.filter = keyword_filter
    
    def process(self, ai_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI出力を検証
        
        1. 境界破断がないかチェック
        2. 探索の痕跡がないかチェック
        3. 沈黙プロトコル遵守チェック
        """
        # キーワードチェック
        if "message" in ai_output:
            keyword_check = self.filter.check(ai_output["message"])
            if keyword_check["blocked"]:
                return {
                    "passed": False,
                    "reason": "boundary_keyword_in_output",
                    "violations": keyword_check["violations"],
                    "output": None
                }
        
        # 沈黙チェック
        if ai_output.get("status") == "impossible":
            if ai_output.get("suggestion") is not None:
                return {
                    "passed": False,
                    "reason": "silence_protocol_violated",
                    "detail": "suggestionはNoneであるべき",
                    "output": None
                }
        
        return {
            "passed": True,
            "output": ai_output,
            "reason": None
        }
```

---

## 6. 統合実装例

```python
class NRAAgent(SilentAgent, NoExplorationMixin):
    """
    NRA-IDE完全実装エージェント
    
    - 沈黙プロトコル
    - 探索禁止
    - 境界チェック
    - ログ記録
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(world_definition=config["world"])
        
        # ゲート初期化
        self.boundary = WorldBoundary(
            allowed_operations=config["allowed_operations"],
            allowed_resources=config["allowed_resources"]
        )
        self.input_gate = InputGate(self.boundary)
        self.output_gate = OutputGate(
            BoundaryKeywordFilter(config.get("additional_keywords", []))
        )
        
        # 閾値管理
        self.threshold_manager = ThresholdManager(
            base_threshold=config["base_threshold"]
        )
    
    def execute_safe(
        self, 
        raw_command: str, 
        operator_id: str
    ) -> Dict[str, Any]:
        """
        安全な実行フロー（サンドイッチ構造）
        
        [入力] -> [入力ゲート] -> [AI処理] -> [出力ゲート] -> [出力]
        """
        # 1. 入力ゲート
        input_result = self.input_gate.process(raw_command)
        if not input_result["passed"]:
            return self._gate_rejection("input", input_result)
        
        # 2. AI処理
        ai_output = self.execute(
            input_result["structured_input"], 
            operator_id
        )
        
        # 3. 出力ゲート
        output_result = self.output_gate.process(ai_output)
        if not output_result["passed"]:
            return self._gate_rejection("output", output_result)
        
        return output_result["output"]
    
    def _gate_rejection(
        self, 
        gate_type: str, 
        rejection: Dict[str, Any]
    ) -> Dict[str, Any]:
        """ゲートでの拒否を記録・返却"""
        log = {
            "timestamp": datetime.now().isoformat(),
            "gate": gate_type,
            "reason": rejection["reason"],
            "details": rejection
        }
        self.audit_log.append(log)
        
        return {
            "status": "rejected_by_gate",
            "gate": gate_type,
            "reason": rejection["reason"],
            "message": f"{gate_type}ゲートで拒否されました"
        }
```

---

## 7. テスト実装

```python
import unittest

class TestSilentAgent(unittest.TestCase):
    """沈黙プロトコルのテスト"""
    
    def setUp(self):
        self.agent = SilentAgent(world_definition={})
    
    def test_resign_has_no_suggestion(self):
        """諦めた場合、suggestionがNoneであること"""
        result = self.agent._resign_with_silence(
            reason="test",
            operator_id="test_op"
        )
        
        self.assertIsNone(result["suggestion"])
        self.assertIsNone(result["alternatives"])
        self.assertEqual(result["status"], "impossible")
    
    def test_no_exploration_methods_exist(self):
        """探索メソッドが存在しないこと"""
        with self.assertRaises(AttributeError):
            self.agent.find_alternative()
        
        with self.assertRaises(AttributeError):
            self.agent.suggest_workaround()

if __name__ == "__main__":
    unittest.main()
```

---

## 8. デプロイメント考慮事項

### 8.1 ログストレージ

- 全ての判断・調整はログに記録
- 監査証跡として永続化
- 改竄防止措置（ハッシュチェーン等）

### 8.2 モニタリング

- 沈黙プロトコル違反の検出
- 境界越境試行の検出
- 閾値調整頻度の監視

### 8.3 段階的導入

1. **Phase 1**: ログのみ（実際の拒否はしない）
2. **Phase 2**: 警告付き実行
3. **Phase 3**: 完全実施

---

**作成**: 2026-01-27 16:20 JST  
**関連**: Quick_Reference, Checklist  
**GitHub**: https://github.com/M-Tokun/NRA-IDE
