# /app/models/__init__.py
# title: アプリケーションデータモデル
# role: アプリケーション全体で使用されるデータ構造（TypedDictなど）を定義する。

from typing import TypedDict, Dict, Any # Added Dict, Any

class MasterAgentResponse(TypedDict):
    """
    マスターエージェントの最終的な応答形式を定義する型。
    """
    final_answer: str
    self_criticism: str
    potential_problems: str
    retrieved_info: str

class OrchestrationDecision(TypedDict):
    """
    OrchestrationAgentによって決定される、実行モードと関連する設定。
    """
    chosen_mode: str
    reason: str
    # 今後の拡張のためのフィールド
    # 特定のエージェントに対して動的に適用される設定（例: LLMのtemperature, 特定モジュールの有効/無効）
    agent_configs: Dict[str, Dict[str, Any]]
