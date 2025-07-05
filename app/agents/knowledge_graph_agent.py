# /app/agents/knowledge_graph_agent.py
# title: 知識グラフ生成AIエージェント
# role: テキストから知識グラフを構築する。

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import JsonOutputParser
from typing import Any, Dict

from app.agents.base import AIAgent
from app.knowledge_graph.models import KnowledgeGraph as KnowledgeGraphModel

class KnowledgeGraphAgent(AIAgent):
    """
    テキストから知識グラフを生成するAIエージェント。
    """
    def __init__(self, llm: Any, prompt_template: ChatPromptTemplate):
        self.llm = llm
        self.prompt_template = prompt_template
        self.output_parser = JsonOutputParser(pydantic_object=KnowledgeGraphModel)
        super().__init__()

    def build_chain(self) -> Runnable:
        """
        知識グラフ生成エージェントのLangChainチェーンを構築します。
        """
        return self.prompt_template | self.llm | self.output_parser

    def invoke(self, input_data: Dict[str, Any] | str) -> KnowledgeGraphModel:
        """
        テキストから知識グラフを生成して返します。
        """
        if not isinstance(input_data, dict):
            raise TypeError("KnowledgeGraphAgent expects a dictionary as input.")
        
        if self._chain is None:
            raise RuntimeError("KnowledgeGraphAgent's chain is not initialized.")
        
        result: KnowledgeGraphModel = self._chain.invoke(input_data)
        return result