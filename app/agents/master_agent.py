# /app/agents/master_agent.py
# title: マスターAIエージェント
# role: AIの認知・メタ認知プロセス全体を統括する司令塔。

from __future__ import annotations
import logging
import time
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from typing import Any, Dict, TYPE_CHECKING, List

import app.agents.prompts as prompts # Import prompts module as prompts
from app.agents.orchestration_agent import OrchestrationAgent # New import

from app.agents.base import AIAgent
from app.memory.working_memory import WorkingMemory
from app.cognitive_modeling.predictive_coding_engine import PredictiveCodingEngine
from app.memory.memory_consolidator import MemoryConsolidator
from app.digital_homeostasis.ethical_motivation_engine import EthicalMotivationEngine
from app.models import MasterAgentResponse
from app.engine import MetaIntelligenceEngine

if TYPE_CHECKING:
    from app.agents.planning_agent import PlanningAgent
    from app.agents.cognitive_loop_agent import CognitiveLoopAgent
    from app.meta_cognition.meta_cognitive_engine import MetaCognitiveEngine
    from app.problem_discovery.problem_discovery_agent import ProblemDiscoveryAgent
    from app.value_evolution.value_evaluator import ValueEvaluator
    from app.agents.orchestration_agent import OrchestrationAgent


logger = logging.getLogger(__name__)

class MasterAgent(AIAgent):
    """
    認知アーキテクチャ全体を統括し、最終的な回答を生成するマスターAI。
    """
    def __init__(
        self,
        llm: Any,
        output_parser: Any,
        memory_consolidator: MemoryConsolidator,
        ethical_motivation_engine: EthicalMotivationEngine,
        predictive_coding_engine: PredictiveCodingEngine,
        working_memory: WorkingMemory,
        engine: MetaIntelligenceEngine,
        # REMOVED: execution_mode: str,
        value_evaluator: 'ValueEvaluator',
        orchestration_agent: 'OrchestrationAgent', # ADDED
    ):
        self.llm = llm
        self.output_parser = output_parser
        self.memory_consolidator = memory_consolidator
        self.ethical_motivation_engine = ethical_motivation_engine
        self.predictive_coding_engine = predictive_coding_engine
        self.working_memory = working_memory
        self.engine = engine
        # REMOVED: self.execution_mode = execution_mode
        self.dialogue_history: List[str] = []
        self.value_evaluator = value_evaluator
        self.orchestration_agent = orchestration_agent # ADDED
        
        # MasterAgentのプロンプトは、もはや静的なEXECUTION_MODEに依存しない。
        # 代わりに、デフォルトまたはフルパイプラインの汎用プロンプトを使用する。
        self.prompt_template = prompts.MASTER_AGENT_PROMPT # type: ignore[attr-defined]

        super().__init__()

    def build_chain(self) -> Runnable:
        return self.prompt_template | self.llm | self.output_parser

    def end_session(self):
        """
        セッションを終了し、ワーキングメモリを保存・クリアする。
        """
        logger.info("--- 対話セッション終了処理 ---")
        self.memory_consolidator.save_working_memory_for_consolidation(self.working_memory)
        self.working_memory.clear()
        self.dialogue_history = []
        logger.info("ワーキングメモリを保存し、リセットしました。")

    def invoke(self, input_data: Dict[str, Any] | str) -> MasterAgentResponse:
        if not isinstance(input_data, str):
            raise TypeError("MasterAgent expects a string query as input.")
        query = input_data

        overall_start_time = time.time()
        # MODIFIED: Log message to reflect dynamic mode selection
        logger.info(f"--- Invoking MasterAgent ---")

        start_time = time.time()
        logger.info("START: Predictive Cognitive Modeling")
        
        prediction_error = self.predictive_coding_engine.process_input(query, self.dialogue_history)
        
        distilled_context: str
        if "summary" in prediction_error and prediction_error["summary"] and prediction_error.get("error_type") != "新規情報なし":
            summary = prediction_error["summary"]
            distilled_context = f"ユーザーの現在の要求は「{query}」です。これまでの対話を踏まえると、この要求の新規性（予測誤差）は「{summary}」にあります。この新規性を中心に思考を展開してください。"
        else:
            distilled_context = f"ユーザーの現在の要求は「{query}」です。これまでの対話から特に目新しい情報はありません。"
        
        end_time = time.time()
        logger.info(f"END: Predictive Cognitive Modeling ({(end_time - start_time):.2f} s)")
        logger.info(f"生成された蒸留コンテキスト: {distilled_context}")

        # ADDED: Dynamic mode selection using OrchestrationAgent
        start_time_orchestration = time.time()
        logger.info("START: Orchestration Agent Mode Selection")
        # OrchestrationAgent's invoke method expects a dictionary with 'query'
        chosen_mode = self.orchestration_agent.invoke({"query": query})
        logger.info(f"Orchestration Agent selected mode: '{chosen_mode}' ({(time.time() - start_time_orchestration):.2f} s)")


        # MODIFIED: Pass the dynamically chosen mode to the engine
        response = self.engine.run(distilled_context, chosen_mode)

        motivation = self.ethical_motivation_engine.assess_and_generate_motivation(response["final_answer"])
        self.memory_consolidator.log_event("homeostasis_check", motivation)
        
        self.value_evaluator.assess_and_update_values(response["final_answer"])
        
        self.memory_consolidator.log_interaction(query, response["final_answer"])

        self.dialogue_history.append(f"User: {query}")
        self.dialogue_history.append(f"AI: {response['final_answer']}")

        overall_end_time = time.time()
        logger.info(f"--- MasterAgent Invocation Finished (Total: {(overall_end_time - overall_start_time):.2f} s) ---")

        return response