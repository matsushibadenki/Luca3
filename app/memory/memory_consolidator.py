# /app/memory/memory_consolidator.py
# title: 記憶統合エンジン
# role: 対話履歴や自律思考のログを記録し、長期記憶として管理する。セッションのワーキングメモリ状態も保存する。

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List

from app.memory.working_memory import WorkingMemory

logger = logging.getLogger(__name__)

class MemoryConsolidator:
    """
    対話の履歴やイベントをJSONL形式でログファイルに記録するクラス。
    """
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self.working_memory_log_dir = "memory/working_memory_sessions"
        
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        if not os.path.exists(self.working_memory_log_dir):
            os.makedirs(self.working_memory_log_dir)
            
        logger.info(f"MemoryConsolidator initialized. Log file: {self.log_file_path}")
        logger.info(f"Working memory log directory: {self.working_memory_log_dir}")


    def _log(self, data: Dict[str, Any]):
        """
        指定されたデータをJSONLファイルに追記します。
        """
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                log_entry = json.dumps(data, ensure_ascii=False)
                f.write(log_entry + "\n")
        except IOError as e:
            logger.error(f"Failed to write to memory log file {self.log_file_path}: {e}")

    def log_event(self, event_type: str, metadata: Dict[str, Any]):
        """
        汎用的なイベントを記録します。
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "event",
            "event_type": event_type,
            "metadata": metadata,
        }
        self._log(log_data)
        
    def log_interaction(self, query: str, final_answer: str):
        """
        ユーザーとの一回の完全な対話を記録します。
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "interaction",
            "query": query,
            "final_answer": final_answer,
        }
        self._log(log_data)

    def log_learned_words(self, query: str, learned_words: List[str]):
        """
        対話から学習した単語を記録します。
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "word_learning",
            "source_query": query,
            "learned_words": learned_words,
        }
        self._log(log_data)
        logger.info(f"学習した単語を記録しました: {learned_words}")

    def log_autonomous_thought(self, topic: str, synthesized_knowledge: str):
        """
        自律思考サイクルによる学習内容を記録します。
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "autonomous_thought",
            "topic": topic,
            "synthesized_knowledge": synthesized_knowledge,
        }
        self._log(log_data)
        logger.info(f"自律思考ログを記録しました: トピック='{topic}'")

    def save_working_memory_for_consolidation(self, working_memory: WorkingMemory):
        """
        指定されたワーキングメモリの内容を、オフライン統合のためにファイルとして保存します。
        """
        session_contents = working_memory.get_contents()
        if not session_contents["prediction_errors"]:
            logger.info(f"ワーキングメモリ (session: {working_memory.session_id}) に保存すべき新規情報はありません。")
            return
            
        session_file_path = os.path.join(self.working_memory_log_dir, f"{working_memory.session_id}.json")
        try:
            with open(session_file_path, "w", encoding="utf-8") as f:
                json.dump(session_contents, f, ensure_ascii=False, indent=4)
            logger.info(f"ワーキングメモリの内容がオフライン統合のために保存されました: {session_file_path}")
        except IOError as e:
            logger.error(f"ワーキングメモリの保存に失敗しました {session_file_path}: {e}")