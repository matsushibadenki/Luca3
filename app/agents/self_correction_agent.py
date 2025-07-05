# /app/agents/self_correction_agent.py
# title: 自己修正AIエージェント
# role: 自己改善提案を分析し、システムへの適用を検討・記録する。

import logging
from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser # Changed to StrOutputParser as the output is a summary, not strict JSON.

from app.agents.base import AIAgent
from app.memory.memory_consolidator import MemoryConsolidator

logger = logging.getLogger(__name__)

class SelfCorrectionAgent(AIAgent):
    """
    自己改善提案を分析し、その適用を検討・記録するエージェント。
    """
    def __init__(self, llm: Any, output_parser: Any, memory_consolidator: MemoryConsolidator, prompt_template: ChatPromptTemplate):
        self.llm = llm
        self.output_parser = output_parser
        self.memory_consolidator = memory_consolidator
        self.prompt_template = prompt_template
        super().__init__()

    def build_chain(self) -> Runnable:
        """
        自己修正の意思決定のためのLangChainチェーンを構築します。
        """
        return self.prompt_template | self.llm | self.output_parser

    def consider_and_log_application(self, improvement_suggestions: List[Dict[str, Any]]) -> None:
        """
        自己改善提案を検討し、適用を決定した内容をログに記録します。
        """
        if not improvement_suggestions:
            logger.info("適用すべき自己改善提案がありません。")
            return

        logger.info("自己改善提案の適用を検討中...")
        suggestions_str = "\n".join([str(s) for s in improvement_suggestions]) # Convert dicts to strings for prompt

        try:
            # Use the LLM to decide which suggestions to "apply" and how to summarize the action
            application_decision_summary = self.invoke({"improvement_suggestions": suggestions_str})
            
            if application_decision_summary and "適用すべき提案はありません" not in application_decision_summary:
                self.memory_consolidator.log_autonomous_thought(
                    topic="self_improvement_applied_decision",
                    synthesized_knowledge=f"【自己改善の適用決定】\n決定内容: {application_decision_summary}\n元の提案: {suggestions_str}"
                )
                logger.info(f"自己改善の適用が決定され、ログに記録されました:\n{application_decision_summary}")
            else:
                logger.info("自己改善提案の適用は見送られました。")

        except Exception as e:
            logger.error(f"自己修正エージェントによる適用検討中にエラーが発生しました: {e}", exc_info=True)