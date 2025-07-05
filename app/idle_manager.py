# /app/idle_manager.py
# title: Idle Time Manager
# role: Manages the application's idle state and triggers background tasks.

import time
import logging
import threading
from typing import Optional, List, Dict, Any, Callable

from app.meta_intelligence.self_improvement.evolution import SelfEvolvingSystem
from app.agents.autonomous_agent import AutonomousAgent
from app.agents.consolidation_agent import ConsolidationAgent
from app.meta_intelligence.emergent.network import EmergentIntelligenceNetwork
from app.meta_intelligence.value_evolution.values import EvolvingValueSystem
from app.memory.memory_consolidator import MemoryConsolidator
from app.config import settings

logger = logging.getLogger(__name__)

class IdleManager:
    """
    アプリケーションのアイドル状態を監視し、自己進化、自律思考、記憶整理などの
    バックグラウンドタスクを指定された間隔で起動する。
    """
    def __init__(
        self,
        self_evolving_system: SelfEvolvingSystem,
        autonomous_agent: AutonomousAgent,
        consolidation_agent: ConsolidationAgent,
        emergent_network: EmergentIntelligenceNetwork,
        value_system: EvolvingValueSystem,
        memory_consolidator: MemoryConsolidator,
    ):
        """
        IdleManagerを初期化します。
        """
        self.self_evolving_system = self_evolving_system
        self.autonomous_agent = autonomous_agent
        self.consolidation_agent = consolidation_agent
        self.emergent_network = emergent_network
        self.value_system = value_system
        self.memory_consolidator = memory_consolidator

        self._last_active_time: float = time.time()
        self._is_idle: bool = False
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None

        # 各タスクの最終実行時刻を記録
        self._last_run_times: Dict[str, float] = {
            "self_evolution": 0,
            "autonomous_cycle": 0,
            "consolidation_cycle": 0,
            "wisdom_synthesis": 0,
            "emergent_discovery": 0,
            "value_evolution": 0,
        }

    def _monitor_loop(self):
        """
        アイドル状態を監視し、各バックグラウンドタスクをスケジュールに従って実行するループ。
        """
        logger.info("Idle monitor thread started.")
        while not self._stop_event.is_set():
            # アイドル状態の時のみタスクを実行
            if self._is_idle:
                current_time = time.time()
                
                # --- 各タスクの実行判定 ---
                self._run_task_if_due("self_evolution", settings.IDLE_EVOLUTION_TRIGGER_SECONDS, self._run_self_evolution, current_time)
                self._run_task_if_due("autonomous_cycle", settings.AUTONOMOUS_CYCLE_INTERVAL_SECONDS, self._run_autonomous_cycle, current_time)
                self._run_task_if_due("consolidation_cycle", settings.CONSOLIDATION_CYCLE_INTERVAL_SECONDS, self._run_consolidation_cycle, current_time)
                self._run_task_if_due("wisdom_synthesis", settings.WISDOM_SYNTHESIS_INTERVAL_SECONDS, self._run_wisdom_synthesis, current_time)
                # 以下の2つは非常に重い処理なので、間隔を長めに設定
                self._run_task_if_due("emergent_discovery", settings.WISDOM_SYNTHESIS_INTERVAL_SECONDS * 2, self._run_emergent_discovery, current_time)
                self._run_task_if_due("value_evolution", settings.WISDOM_SYNTHESIS_INTERVAL_SECONDS * 3, self._run_value_evolution, current_time)

            # CPUを過剰に消費しないように、短いスリープを入れる
            time.sleep(5) # 判定ループの間隔を少し長めに設定
        logger.info("Idle monitor thread stopped.")

    def _run_task_if_due(self, task_name: str, interval: int, task_function: Callable[[], None], current_time: float):
        """指定した間隔が経過していればタスクを実行するヘルパー関数。"""
        if current_time - self._last_run_times[task_name] > interval:
            logger.info(f"Idle time task '{task_name}' is due. Starting execution.")
            try:
                task_function()
            except Exception as e:
                logger.error(f"Error during idle task '{task_name}': {e}", exc_info=True)
            finally:
                self._last_run_times[task_name] = current_time
                logger.info(f"Idle time task '{task_name}' finished.")

    # --- 各タスクの実行メソッド ---
    def _run_self_evolution(self):
        import asyncio
        asyncio.run(self.self_evolving_system.analyze_own_performance())

    def _run_autonomous_cycle(self):
        self.autonomous_agent.run_autonomous_cycle()

    def _run_consolidation_cycle(self):
        self.consolidation_agent.run_consolidation_cycle()

    def _run_wisdom_synthesis(self):
        self.consolidation_agent.synthesize_deep_wisdom()
        
    def _run_emergent_discovery(self):
        import asyncio
        # 一般的な問題解決能力について創発性をテスト
        asyncio.run(self.emergent_network.discover_and_foster("complex and abstract problem solving"))

    def _run_value_evolution(self):
        import asyncio
        # 最近のセッションログから経験を取得して価値観を進化させる
        # このメソッドは MemoryConsolidator に実装する必要がある
        if hasattr(self.memory_consolidator, 'get_recent_events'):
            recent_experiences = self.memory_consolidator.get_recent_events(limit=10)
            if recent_experiences:
                asyncio.run(self.value_system.evolve_values(recent_experiences))
            else:
                logger.info("No recent experiences to evolve values from. Skipping.")
        else:
            logger.warning("method 'get_recent_events' not found in MemoryConsolidator. Skipping value evolution.")

    def set_busy(self):
        """
        アプリケーションがアクティブ状態になったことを記録します。
        """
        if self._is_idle:
            logger.debug("System state changed to: Busy")
        self._is_idle = False
        self._last_active_time = time.time()

    def set_idle(self):
        """
        アプリケーションがアイドル状態になったことを記録します。
        """
        if not self._is_idle:
            logger.debug("System state changed to: Idle")
        self._is_idle = True
        self._last_active_time = time.time()

    def start(self):
        """
        アイドル監視スレッドを開始します。
        """
        if self._monitor_thread is None:
            self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()

    def stop(self):
        """
        アイドル監視スレッドを停止します。
        """
        logger.info("Stopping idle monitor thread...")
        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join()
            self._monitor_thread = None