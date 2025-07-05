# /app/config.py
# title: アプリケーション設定
# role: アプリケーション全体で使用される設定値を一元管理する。

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM関連の設定
    GENERATION_LLM_SETTINGS = {
        "model": "gemma3:latest",
        "temperature": 0.7,
    }
    VERIFIER_LLM_SETTINGS = {
        "model": "gemma3:latest",
        "temperature": 0.4,
    }
    EMBEDDING_MODEL_NAME = "nomic-embed-text"

    # ファイルパス関連
    KNOWLEDGE_BASE_SOURCE = "data/documents/initial_facts.txt"
    KNOWLEDGE_GRAPH_STORAGE_PATH = "memory/knowledge_graph.json"
    MEMORY_LOG_FILE_PATH = "memory/session_memory.jsonl"
    
    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
    # パイプラインごとの設定
    PIPELINE_SETTINGS = {
        "speculative": {
            "num_drafts": 3
        },
        "internal_dialogue": {
            "max_turns": 5
        },
        "cognitive_loop": {
            "max_iterations": 3
        }
    }

    # アイドル時間と自律思考の実行間隔（秒）
    IDLE_EVOLUTION_TRIGGER_SECONDS = 30
    AUTONOMOUS_CYCLE_INTERVAL_SECONDS = 60
    CONSOLIDATION_CYCLE_INTERVAL_SECONDS = 300
    WISDOM_SYNTHESIS_INTERVAL_SECONDS = 600
    
    # 自律思考エージェントが探求する初期トピックのリスト
    AUTONOMOUS_RESEARCH_TOPICS = [
        "最新のAI技術トレンド",
        "持続可能なエネルギー源",
        "宇宙探査の進捗",
        "健康的な食事と運動",
        "世界の経済動向"
    ]

    # QuantumInspiredPipelineで使用するペルソナのリスト
    QUANTUM_PERSONAS = [
        {"name": "楽観的な未来学者", "persona": "あなたは未来の可能性を信じる楽観的な未来学者です。"},
        {"name": "懐疑的なリスクアナリスト", "persona": "あなたは何事にも潜むリスクを冷静に分析する懐疑的なリスクアナリストです。"},
        {"name": "共感的な倫理学者", "persona": "あなたは技術が人間に与える影響を深く考える、共感力の高い倫理学者です。"},
        {"name": "実践的なエンジニア", "persona": "あなたは理論よりも実践的な解決策を重視する現実的なエンジニアです。"},
    ]
    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
    
    # 価値観の初期設定
    INITIAL_CORE_VALUES = {
        "Helpfulness": 0.8,
        "Harmlessness": 0.9,
        "Honesty": 0.85,
        "Empathy": 0.7,
    }

settings = Config()