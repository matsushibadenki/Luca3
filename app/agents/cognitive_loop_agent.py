# /app/agents/cognitive_loop_agent.py
# title: 認知ループAIエージェント
# role: 計画に基づき、情報検索、評価、改善、知識グラフ化を反復的に実行し、分析結果を生成する。

import logging
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from app.agents.base import AIAgent
from app.agents.knowledge_graph_agent import KnowledgeGraphAgent
from app.agents.query_refinement_agent import QueryRefinementAgent
from app.agents.retrieval_evaluator_agent import RetrievalEvaluatorAgent
from app.knowledge_graph.persistent_knowledge_graph import PersistentKnowledgeGraph
from app.rag.retriever import Retriever
from app.tools.tool_belt import ToolBelt
from app.agents.tool_using_agent import ToolUsingAgent

from app.config import settings # ADDED

logger = logging.getLogger(__name__)

class CognitiveLoopAgent(AIAgent):
    """
    情報収集、評価、改善を反復的に行い、知識を構造化する認知ループを実行するエージェント。
    """
    def __init__(
        self,
        llm: Any,
        output_parser: Any,
        prompt_template: ChatPromptTemplate,
        retriever: Retriever,
        retrieval_evaluator_agent: RetrievalEvaluatorAgent,
        query_refinement_agent: QueryRefinementAgent,
        knowledge_graph_agent: KnowledgeGraphAgent,
        persistent_knowledge_graph: PersistentKnowledgeGraph,
        tool_using_agent: ToolUsingAgent,
        tool_belt: ToolBelt,
    ):
        self.llm = llm
        self.output_parser = output_parser
        self.prompt_template = prompt_template
        self.retriever = retriever
        self.retrieval_evaluator_agent = retrieval_evaluator_agent
        self.query_refinement_agent = query_refinement_agent
        self.knowledge_graph_agent = knowledge_graph_agent
        self.persistent_knowledge_graph = persistent_knowledge_graph
        self.tool_using_agent = tool_using_agent
        self.tool_belt = tool_belt
        super().__init__()

    def build_chain(self) -> Runnable:
        """
        分析結果を生成するための最終的なチェーンを構築します。
        """
        return self.prompt_template | self.llm | self.output_parser

    def _iterative_retrieval(self, query: str) -> str:
        """
        検索、評価、クエリ改善を繰り返して情報の質を高める反復的検索を実行します。
        必要に応じて外部ツールも利用します。
        """
        max_iterations = settings.PIPELINE_SETTINGS["cognitive_loop"]["max_iterations"]
        current_query = query
        final_info = ""
        tool_used_this_cycle = False

        for i in range(max_iterations):
            logger.info(f"検索イテレーション {i+1}/{max_iterations}: クエリ='{current_query}'")
            
            # 1. RAG検索
            docs: List[Document] = self.retriever.invoke(current_query)
            rag_retrieved_info = "\n\n".join([doc.page_content for doc in docs])

            # 2. RAG検索結果の評価
            eval_input = {"query": current_query, "retrieved_info": rag_retrieved_info}
            evaluation = self.retrieval_evaluator_agent.invoke(eval_input)
            
            logger.info(f"RAG検索品質の評価: {evaluation}")

            relevance = evaluation.get("relevance_score", 0)
            completeness = evaluation.get("completeness_score", 0)
            
            current_retrieved_info = rag_retrieved_info

            # 3. 外部ツールの利用判断と実行
            if relevance <= 8 or completeness <= 8:
                logger.info("RAG検索結果が不十分なため、外部ツールの利用を検討します。")
                
                available_tools_desc = self.tool_belt.get_tool_descriptions()
                tool_selection_input = {
                    "tools": available_tools_desc,
                    "task": f"「{current_query}」について、RAGで得られなかった情報を補完するために、最適なツールと検索クエリを選択してください。"
                }
                
                try:
                    tool_decision = self.tool_using_agent.invoke(tool_selection_input)
                    if ": " in tool_decision:
                        chosen_tool_name, tool_query = tool_decision.split(": ", 1)
                        chosen_tool_name = chosen_tool_name.strip()
                        tool_query = tool_query.strip()

                        chosen_tool = self.tool_belt.get_tool(chosen_tool_name)
                        if chosen_tool:
                            logger.info(f"ツール '{chosen_tool_name}' を使用して '{tool_query}' を検索します。")
                            tool_result = chosen_tool.use(tool_query)
                            current_retrieved_info = f"{current_retrieved_info}\n\n--- 外部ツール ({chosen_tool_name}) からの情報 ---\n{tool_result}"
                            logger.info(f"外部ツールからの情報取得完了。")
                            tool_used_this_cycle = True
                        else:
                            logger.warning(f"選択されたツール '{chosen_tool_name}' が見つかりません。")
                    else:
                        logger.warning(f"ToolUsingAgentの出力形式が不正です: {tool_decision}")

                except Exception as e:
                    logger.error(f"ツール利用中にエラーが発生しました: {e}", exc_info=True)
            
            final_info = current_retrieved_info

            # 4. 終了条件の判定
            if (relevance > 8 and completeness > 8) or tool_used_this_cycle:
                logger.info("十分な品質の情報が得られたか、または外部ツールが利用されたため、検索を終了します。")
                break
            
            # 5. クエリの改善
            refine_input = {
                "query": query,
                "evaluation_summary": evaluation.get("summary", ""),
                "suggestions": evaluation.get("suggestions", "")
            }
            refined_query = self.query_refinement_agent.invoke(refine_input)
            logger.info(f"改善されたクエリ: '{refined_query}'")
            current_query = refined_query
        else:
            logger.warning("最大反復回数に達しました。現在の情報で処理を続行します。")

        return final_info

    def invoke(self, input_data: Dict[str, Any] | str) -> str:
        """
        認知ループを実行し、最終的な分析結果を返します。
        """
        if not isinstance(input_data, dict):
            raise TypeError("CognitiveLoopAgent expects a dictionary as input.")

        query = input_data.get("query", "")
        plan = input_data.get("plan", "")

        # 1. 反復的検索（ツール利用を含む）
        final_retrieved_info = self._iterative_retrieval(query)

        # 2. 知識グラフの生成と永続化
        if final_retrieved_info:
            logger.info("検索結果から知識グラフを生成しています...")
            kg_input = {"text_chunk": final_retrieved_info}
            new_knowledge_graph = self.knowledge_graph_agent.invoke(kg_input)
            self.persistent_knowledge_graph.merge(new_knowledge_graph)
            self.persistent_knowledge_graph.save()
            long_term_memory_context = self.persistent_knowledge_graph.get_graph().to_string()
        else:
            long_term_memory_context = "関連する長期記憶はありません。"

        # 3. 最終的な分析結果の生成
        final_input = {
            "query": query,
            "plan": plan,
            "long_term_memory_context": long_term_memory_context,
            "final_retrieved_info": final_retrieved_info,
        }
        
        if self._chain is None:
            raise RuntimeError("CognitiveLoopAgent's chain is not initialized.")
        return self._chain.invoke(final_input)