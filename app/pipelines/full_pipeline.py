# /app/pipelines/full_pipeline.py
# title: フル機能推論パイプライン
# role: 計画、認知ループ、メタ認知、自己改善を含む、最も包括的な推論パイプライン。

import logging
from typing import Dict, Any, List

from app.pipelines.base import BasePipeline
from app.agents.master_agent import MasterAgent
from app.agents.planning_agent import PlanningAgent
from app.agents.cognitive_loop_agent import CognitiveLoopAgent
from app.meta_cognition.meta_cognitive_engine import MetaCognitiveEngine
from app.problem_discovery.problem_discovery_agent import ProblemDiscoveryAgent
from app.memory.memory_consolidator import MemoryConsolidator
from app.agents.self_improvement_agent import SelfImprovementAgent
from app.agents.self_correction_agent import SelfCorrectionAgent
from app.meta_intelligence.self_improvement.evolution import SelfEvolvingSystem
from app.models import MasterAgentResponse, OrchestrationDecision

logger = logging.getLogger(__name__)

class FullPipeline(BasePipeline):
    """
    計画、認知ループ、メタ認知、自己改善を含む、最も包括的な推論パイプライン。
    """
    def __init__(
        self,
        master_agent: MasterAgent,
        planning_agent: PlanningAgent,
        cognitive_loop_agent: CognitiveLoopAgent,
        meta_cognitive_engine: MetaCognitiveEngine,
        problem_discovery_agent: ProblemDiscoveryAgent,
        memory_consolidator: MemoryConsolidator,
        self_improvement_agent: SelfImprovementAgent,
        self_correction_agent: SelfCorrectionAgent,
        self_evolving_system: SelfEvolvingSystem,
    ):
        self.master_agent = master_agent
        self.planning_agent = planning_agent
        self.cognitive_loop_agent = cognitive_loop_agent
        self.meta_cognitive_engine = meta_cognitive_engine
        self.problem_discovery_agent = problem_discovery_agent
        self.memory_consolidator = memory_consolidator
        self.self_improvement_agent = self_improvement_agent
        self.self_correction_agent = self_correction_agent
        self.self_evolving_system = self_evolving_system

    def run(self, query: str, orchestration_decision: OrchestrationDecision) -> MasterAgentResponse:
        """
        フルパイプラインを実行します。
        """
        logger.info(f"--- Full Pipeline started for query: '{query}' ---")

        # 1. Plan
        plan = self.planning_agent.invoke({"query": query})
        logger.info(f"Generated Plan:\n{plan}")

        # 2. Cognitive Loop
        cognitive_loop_output = self.cognitive_loop_agent.invoke({
            "query": query,
            "plan": plan,
        })
        logger.info(f"Cognitive Loop Output:\n{cognitive_loop_output}")

        # 3. Master Agent (Generate Final Answer)
        master_agent_input = {
            "query": query,
            "plan": plan,
            "cognitive_loop_output": cognitive_loop_output,
        }
        final_answer_response = self.master_agent.invoke(master_agent_input)
        final_answer = final_answer_response['final_answer'] if isinstance(final_answer_response, dict) else str(final_answer_response)

        logger.info(f"Final Answer:\n{final_answer}")

        # 4. Meta-Cognitive Reflection (Self-Critique)
        self_criticism = self.meta_cognitive_engine.critique_process_and_response(
            query=query,
            plan=plan,
            cognitive_loop_output=cognitive_loop_output,
            final_answer=final_answer
        )
        logger.info(f"Self-Criticism:\n{self_criticism}")

        # 5. Problem Discovery
        potential_problems_list = self.problem_discovery_agent.invoke({
            "query": query,
            "plan": plan,
            "cognitive_loop_output": cognitive_loop_output,
        })
        potential_problems = "\n".join(potential_problems_list) if potential_problems_list else "特になし"
        logger.info(f"Discovered Potential Problems: {potential_problems}")

        # 6. Self-Improvement Suggestion
        improvement_suggestions: List[Dict[str, Any]] = []
        if self_criticism and "問題なし" not in self_criticism:
            improvement_input = {
                "query": query,
                "plan": plan,
                "cognitive_loop_output": cognitive_loop_output,
                "final_answer": final_answer,
                "self_criticism": self_criticism,
            }
            improvement_suggestions = self.self_improvement_agent.invoke(improvement_input)
            logger.info(f"Generated Improvement Suggestions: {improvement_suggestions}")
            
            # 7. Self-Correction (Consider applying improvements)
            self.self_correction_agent.consider_and_log_application(improvement_suggestions)

        # 8. Memory Consolidation
        self.memory_consolidator.log_event(
            event_type="full_pipeline_run",
            metadata={
                "query": query,
                "plan": plan,
                "final_answer": final_answer,
                "self_criticism": self_criticism,
                "potential_problems": potential_problems,
                "improvement_suggestions": improvement_suggestions,
            }
        )
        
        # 9. Collect trace for self-evolution
        trace_data = {
            "query": query,
            "plan": plan,
            "cognitive_loop_output": cognitive_loop_output,
            "final_answer": final_answer,
            "self_criticism": self_criticism,
        }
        self.self_evolving_system.collect_execution_trace(trace_data)
        logger.info("Execution trace collected for potential self-evolution.")

        logger.info("--- Full Pipeline finished ---")

        return {
            "final_answer": final_answer,
            "self_criticism": self_criticism,
            "potential_problems": potential_problems,
            "retrieved_info": cognitive_loop_output
        }