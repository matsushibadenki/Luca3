# /app/pipelines/base.py
# title: パイプライン基底クラス
# role: すべての推論パイプラインが従うべき基本的なインターフェースを定義する。

from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models import MasterAgentResponse
from app.models import OrchestrationDecision # ADDED

class BasePipeline(ABC):
    """
    すべての推論パイプラインの抽象基底クラス。
    """
    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
    @abstractmethod
    def run(self, query: str, orchestration_decision: OrchestrationDecision) -> MasterAgentResponse:
    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
        """
        パイプラインを実行するメソッド。

        Args:
            query (str): ユーザーからのクエリ。
            # ADDED: orchestration_decision (OrchestrationDecision): OrchestrationAgentによって決定された実行モードと関連する設定。

        Returns:
            MasterAgentResponse: パイプラインの実行結果。
        """
        pass