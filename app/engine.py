# /app/engine.py
# title: メタインテリジェンスエンジン
# role: 実行モードに応じて適切な推論パイプラインを選択し、処理を実行する。

from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from app.pipelines.base import BasePipeline
    from app.models import MasterAgentResponse
    from app.models import OrchestrationDecision # ADDED

logger = logging.getLogger(__name__)

class MetaIntelligenceEngine:
    """
    推論パイプラインを管理し、実行するコアエンジン。
    """
    def __init__(self, pipelines: Dict[str, BasePipeline]):
        self.pipelines = pipelines

    # MODIFIED: mode parameter is now OrchestrationDecision
    def run(self, query: str, orchestration_decision: 'OrchestrationDecision') -> MasterAgentResponse:
        """
        指定されたモードで適切なパイプラインを実行する。
        失敗した場合は、フォールバックパイプライン（simpleモード）を試行する。

        Args:
            query (str): ユーザーからのクエリ。
            orchestration_decision (OrchestrationDecision): OrchestrationAgentによって決定された実行モードと関連する設定。

        Returns:
            MasterAgentResponse: パイプラインの実行結果。
        """
        # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
        initial_mode = orchestration_decision.get("chosen_mode", "simple") # OrchestrationDecisionからモードを抽出
        # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
        current_pipeline = None

        try:
            # The OrchestrationAgent should ideally ensure a valid mode is returned.
            # However, keep fallback for robustness if an invalid mode somehow slips through.
            if initial_mode not in self.pipelines:
                logger.warning(f"無効な実行モードが指定されました: {initial_mode}。simpleモードにフォールバックします。")
                initial_mode = "simple" # Fallback to simple

            current_pipeline = self.pipelines[initial_mode]
            logger.info(f"メインパイプライン '{initial_mode}' で実行中...")
            # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
            # orchestration_decisionをパイプラインに渡すように変更
            response = current_pipeline.run(query, orchestration_decision) 
            # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
            
            # Simple check for unsatisfactory response (can be expanded)
            if not response.get("final_answer"):
                logger.warning(f"メインパイプライン '{initial_mode}' が空の回答を返しました。simpleモードにフォールバックします。")
                raise ValueError("Empty final_answer from main pipeline.")

            return response

        except Exception as e:
            logger.error(f"パイプライン '{initial_mode}' の実行中にエラーが発生しました: {e}。simpleモードで再試行します。", exc_info=True)
            
            # Fallback to simple mode
            if initial_mode != "simple": # Check against initial_mode (the one that caused the error)
                try:
                    logger.info("フォールバックパイプライン 'simple' で実行中...")
                    fallback_pipeline = self.pipelines["simple"]
                    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
                    # フォールバックパイプラインにもOrchestrationDecisionを渡す (simpleモードのデフォルトで)
                    fallback_response = fallback_pipeline.run(query, {"chosen_mode": "simple", "reason": "フォールバック", "agent_configs": {}}) 
                    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
                    
                    if not fallback_response.get("final_answer"):
                        logger.error("フォールバックパイプライン 'simple' も空の回答を返しました。")
                        return {
                            "final_answer": "申し訳ありません、要求を処理できませんでした。システム内部で問題が発生しています。",
                            "self_criticism": f"メインパイプライン({initial_mode})とフォールバックパイプライン(simple)の両方で処理に失敗しました。詳細: {e}",
                            "potential_problems": "パイプラインの実行に根本的な問題がある可能性があります。",
                            "retrieved_info": ""
                        }
                    return fallback_response
                except Exception as fallback_e:
                    logger.error(f"フォールバックパイプライン 'simple' の実行中にエラーが発生しました: {fallback_e}。", exc_info=True)
                    return {
                        "final_answer": "申し訳ありません、要求を処理できませんでした。システム内部で重大な問題が発生しています。",
                        "self_criticism": f"メインパイプライン({initial_mode})とフォールバックパイプライン(simple)の両方で処理に失敗しました。詳細: メインエラー: {e}, フォールバックエラー: {fallback_e}",
                        "potential_problems": "フォールバックメカニズムが機能しませんでした。システム全体の安定性を確認してください。",
                        "retrieved_info": ""
                    }
            else:
                logger.error(f"simpleモードでの実行中にエラーが発生しました: {e}。フォールバックオプションがありません。", exc_info=True)
                return {
                    "final_answer": "申し訳ありません、要求を処理できませんでした。システム内部で問題が発生しています。",
                    "self_criticism": f"simpleパイプラインでの処理に失敗しました。詳細: {e}",
                    "potential_problems": "シンプルな実行モードでも問題が発生しました。システムログを確認してください。",
                    "retrieved_info": ""
                }