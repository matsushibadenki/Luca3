# /app/tools/tool_belt.py
# title: ツールベルト
# role: システムで利用可能なすべてのツールを保持し、名前で呼び出す機能を提供する。

import os
from typing import List, Dict, Optional
from app.tools.base import Tool
from .serpapi_tool import SerpApiTool
from .wikipedia_search_tool import WikipediaSearchTool

class ToolBelt:
    """
    利用可能なツールのコレクションを管理するクラス。
    """
    def __init__(self) -> None:
# ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
        self._tools: List[Tool] = [
            WikipediaSearchTool(),
        ]
        # SERPAPI_API_KEYが設定されている場合のみWebSearchツールを追加
        if 'SERPAPI_API_KEY' in os.environ and os.environ['SERPAPI_API_KEY']:
            self._tools.append(SerpApiTool())
            
        self._tool_map: Dict[str, Tool] = {tool.name: tool for tool in self._tools}
# ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️

    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """
        指定された名前のツールを取得する。
        """
        return self._tool_map.get(tool_name)

    def get_tool_descriptions(self) -> str:
        """
        すべてのツールの名前と説明をフォーマットされた文字列として取得する。
        """
        return "\n".join(
            [f"- {tool.name}: {tool.description}" for tool in self._tools]
        )