# /app/pipelines/simple_pipeline.py
# title: シンプル推論パイプライン
# role: 高速な応答を目的とした、基本的なRAGと回答生成のパイプライン。

import time
import logging
from typing import Dict, Any

from app.pipelines.base import BasePipeline
from app.agents.master_agent import MasterAgent
from app.agents.cognitive_loop_agent import CognitiveLoopAgent
from app.models import MasterAgentResponse
from app.models import OrchestrationDecision # ADDED

logger = logging.getLogger(__name__)

class SimplePipeline(BasePipeline):
    """
    シンプルなRAGベースの推論パイプライン。
    """
    def __init__(self, master_agent: MasterAgent, cognitive_loop_agent: CognitiveLoopAgent):
        self.master_agent = master_agent
        self.cognitive_loop_agent = cognitive_loop_agent

    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
    def run(self, query: str, orchestration_decision: OrchestrationDecision) -> MasterAgentResponse:
    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
        """
        パイプラインを実行する。
        """
        start_time = time.time()
        logger.info("--- Simple Pipeline START ---")

        docs = self.cognitive_loop_agent.retriever.invoke(query)
        retrieved_info = "\n\n".join([doc.page_content for doc in docs])
        
        simple_input = {"query": query, "retrieved_info": retrieved_info}
        
        if self.master_agent._chain is None:
            raise RuntimeError("MasterAgent's chain is not initialized for this pipeline.")
        final_answer = self.master_agent._chain.invoke(simple_input)
        
        logger.info(f"--- Simple Pipeline END ({(time.time() - start_time):.2f} s) ---")

        return {
            "final_answer": final_answer,
            "self_criticism": "シンプルモードでは自己評価は実行されません。",
            "potential_problems": "シンプルモードでは潜在的な問題の発見は実行されません。",
            "retrieved_info": retrieved_info
        }