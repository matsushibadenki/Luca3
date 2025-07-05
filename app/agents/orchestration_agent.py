# /app/agents/orchestration_agent.py
# title: オーケストレーションAIエージェント
# role: ユーザーの要求を分析し、最適な実行パイプラインを選択する。

import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
# ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
from langchain_core.output_parsers import JsonOutputParser
from typing import Any, Dict
from app.models import OrchestrationDecision
# ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️

from app.agents.base import AIAgent
from app.reasoning.complexity_analyzer import ComplexityAnalyzer

logger = logging.getLogger(__name__)

class OrchestrationAgent(AIAgent):
    """
    ユーザーの要求に応じて最適な実行モードを選択するエージェント。
    """
    def __init__(self, llm: Any, output_parser: Any, prompt_template: ChatPromptTemplate, complexity_analyzer: ComplexityAnalyzer):
        self.llm = llm
        # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
        # OrchestrationDecisionの構造をLLMに出力させるため、JsonOutputParserを使用
        self.output_parser = JsonOutputParser(pydantic_object=OrchestrationDecision)
        # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
        self.prompt_template = prompt_template
        self.complexity_analyzer = complexity_analyzer
        super().__init__()

    def build_chain(self) -> Runnable:
        """
        オーケストレーションエージェントのLangChainチェーンを構築します。
        """
        return self.prompt_template | self.llm | self.output_parser

    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
    def invoke(self, input_data: Dict[str, Any] | str) -> OrchestrationDecision: # 戻り値の型をOrchestrationDecisionに変更
    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
        if not isinstance(input_data, dict):
            raise TypeError("OrchestrationAgent expects a dictionary as input.")

        if self._chain is None:
            raise RuntimeError("OrchestrationAgent's chain is not initialized.")
            
        query = input_data.get("query", "")
        complexity_level = self.complexity_analyzer.analyze_query_complexity(query)
        logger.info(f"クエリの複雑性レベル: {complexity_level}")

        orchestration_input = {"query": query, "complexity_level": complexity_level}
        
        # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
        decision: OrchestrationDecision = self._chain.invoke(orchestration_input)
        
        # 決定されたモードが有効なものか確認し、無効なら"simple"にフォールバック
        chosen_mode = decision.get("chosen_mode", "simple").lower()
        valid_modes = ["simple", "full", "parallel", "quantum", "speculative", "self_discover", "internal_dialogue"]
        
        if chosen_mode not in valid_modes:
            logger.warning(f"Orchestration Agentが有効でないモード '{chosen_mode}' を提案しました。'simple'モードにフォールバックします。")
            decision["chosen_mode"] = "simple"
            decision["reason"] = "提案されたモードが無効だったため、simpleモードにフォールバックしました。"
            # agent_configsも存在しない場合は空のdictを保証
            if "agent_configs" not in decision:
                decision["agent_configs"] = {}
            
        return decision
        # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️