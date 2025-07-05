# /run.py
# title: アプリケーション実行スクリプト
# role: アプリケーションのDIコンテナを初期化し、メインの対話ループを開始する。

import logging
import sys
import os
from dotenv import load_dotenv
from typing import List, Any

# プロジェクトのルートパスをシステムパスに追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
load_dotenv()

from app.containers import Container
from app.main import main_loop
from app.config import settings
from app.utils.ollama_utils import check_ollama_models_availability
from app.utils.api_key_checker import check_search_api_key

# ロギングの基本設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main() -> None:
    """
    アプリケーションのメインエントリーポイント。
    """
    # 依存関係のチェック
    required_models: List[str] = [
        str(settings.GENERATION_LLM_SETTINGS["model"]),
        settings.EMBEDDING_MODEL_NAME
    ]
    if not check_ollama_models_availability(required_models):
        sys.exit(1)

    check_search_api_key()
    
    # DIコンテナの初期化とワイヤリング
    container = Container()
    container.wire(modules=[__name__, "app.main"])

    # アイドルマネージャーの取得と起動
    idle_manager = container.idle_manager()
    idle_manager.start()

    try:
        # メインループの実行
        main_loop()
    finally:
        # アプリケーション終了時にリソースを解放
        idle_manager.stop()
        container.shutdown_resources()
        logger.info("--- AI協調応答システム終了 ---")


if __name__ == "__main__":
    main()