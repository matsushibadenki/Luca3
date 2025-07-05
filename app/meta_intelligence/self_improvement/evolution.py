# /app/meta_intelligence/self_improvement/evolution.py
# title: Self-Evolving System
# role: Analyzes and improves its own intelligence.

from typing import Dict, Any, List
import logging

# 既存の自己改善関連エージェントをインポート
from app.agents.self_improvement_agent import SelfImprovementAgent
from app.agents.self_correction_agent import SelfCorrectionAgent
from app.meta_cognition.meta_cognitive_engine import MetaCognitiveEngine

logger = logging.getLogger(__name__)

class SelfEvolvingSystem:
    """
    自分自身を分析し、改善する知能。
    思考プロセスを客観視し、弱点を発見し、改善戦略を立案・実装（検討）する。
    """
    def __init__(
        self,
        meta_cognitive_engine: MetaCognitiveEngine,
        self_improvement_agent: SelfImprovementAgent,
        self_correction_agent: SelfCorrectionAgent
    ):
        """
        自己進化システムを初期化します。

        Args:
            meta_cognitive_engine (MetaCognitiveEngine): 思考プロセスを批判的に評価するエンジン。
            self_improvement_agent (SelfImprovementAgent): 改善案を生成するエージェント。
            self_correction_agent (SelfCorrectionAgent): 改善案の適用を検討するエージェント。
        """
        self.meta_cognitive_engine = meta_cognitive_engine
        self.self_improvement_agent = self_improvement_agent
        self.self_correction_agent = self_correction_agent
        self.performance_traces: List[Dict[str, Any]] = []

    def collect_execution_trace(self, trace_data: Dict[str, Any]):
        """
        AIの実行トレース（思考の記録）を収集します。
        """
        self.performance_traces.append(trace_data)
        logger.info("Execution trace collected for self-analysis.")

    async def analyze_own_performance(self) -> None:
        """
        収集された実行トレースを基に、自己のパフォーマンスを分析し、改善サイクルを実行します。
        """
        if not self.performance_traces:
            logger.warning("No performance traces to analyze. Skipping self-evolution cycle.")
            return

        logger.info("--- Starting Self-Evolution Cycle ---")

        # 1. 自分の思考プロセスを客観視 (メタ認知分析)
        # ここでは、収集された最後のトレースを分析対象とします。
        latest_trace = self.performance_traces[-1]
        
        logger.info("Step 1: Performing meta-cognitive analysis on the latest trace.")
        self_criticism = self.meta_cognitive_engine.critique_process_and_response(
            query=latest_trace.get("query", ""),
            plan=latest_trace.get("plan", ""),
            cognitive_loop_output=latest_trace.get("cognitive_loop_output", ""),
            final_answer=latest_trace.get("final_answer", "")
        )
        logger.info(f"Meta-cognitive Analysis (Self-Criticism): {self_criticism}")

        if not self_criticism or "問題なし" in self_criticism:
            logger.info("No significant weaknesses found. Concluding self-evolution cycle.")
            self.performance_traces.clear() # 分析が済んだトレースはクリア
            return

        # 2. 改善戦略を立案
        logger.info("Step 2: Designing self-improvement plan based on weaknesses.")
        improvement_input = {
            **latest_trace,
            "self_criticism": self_criticism
        }
        improvement_suggestions = self.self_improvement_agent.invoke(improvement_input)
        
        if not improvement_suggestions:
            logger.warning("Could not design any improvement suggestions.")
            self.performance_traces.clear()
            return
            
        logger.info(f"Generated Improvement Suggestions: {improvement_suggestions}")

        # 3. 実際に自分を改善（の検討と記録）
        logger.info("Step 3: Implementing (considering) improvements.")
        self.self_correction_agent.consider_and_log_application(improvement_suggestions)
        
        # 4. 分析が済んだトレースはクリア
        self.performance_traces.clear()
        logger.info("--- Self-Evolution Cycle Completed ---")