# /app/reasoning/complexity_analyzer.py
# title: 複雑性分析エンジン
# role: ユーザーのクエリの複雑性を簡易的に分析し、推論戦略の選択に役立てる。

class ComplexityAnalyzer:
    """
    ユーザーのクエリの複雑性を分析するクラス。
    """
    def analyze_query_complexity(self, query: str) -> str:
        """
        クエリの複雑性を分析し、'low', 'medium', 'high' のいずれかを返します。
        """
        word_count = len(query.split())
        
        if word_count < 5:
            return "low"
        elif word_count < 15 and ("なぜ" not in query and "どのように" not in query and "比較" not in query):
            return "medium"
        else:
            return "high"