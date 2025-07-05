# /app/tools/serpapi_tool.py
# title: SerpAPI検索ツール
# role: SerpAPIを使用して、Web上の情報を検索する。

from app.tools.base import Tool
from langchain_community.utilities import SerpAPIWrapper

class SerpApiTool(Tool):
    """
    SerpAPIを実行するためのツール。
    """
    def __init__(self):
        self.name = "WebSearch"
        self.description = "最新の出来事、一般的な知識、特定のトピックについてインターネットで検索します。"
        self.api_wrapper = SerpAPIWrapper()

    def use(self, query: str) -> str:
        """
        指定されたクエリでWeb検索を実行し、結果を返す。
        """
        return self.api_wrapper.run(query)