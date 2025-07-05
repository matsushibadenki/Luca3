# **Luca3: 自己進化型メタ認知AIフレームワーク**

**Luca3**は、単なる応答生成AIではありません。人間の認知プロセスに触発された「メタ認知（Metacognition）」の概念を中核に据え、自らの思考プロセスを評価・改善しながら成長を続ける、自己進化型のAIフレームワークです。

* **動的オーケストレーション**: ユーザーの要求に応じて、思考の「深さ」と「広さ」を動的に調整します。単純な質問には高速に、複雑な問題には複数の専門家AIからなるチームを編成して、多角的にアプローチします。  
* **予測的認知モデリング**: AIは単に反応するのではなく、常に世界の次の状態を予測し、その「予測誤差」を最小化するように学習します。  
* **アイドル時の自己進化**: ユーザーとの対話がない待機時間を利用して、自律的に知識を整理・拡張し、自身の思考パターンを分析・改善します。

## **✨ 主な機能**

Luca3は、以下の機能が統合された、動的で自己成長するシステムです。

* **🧠 進化する認知アーキテクチャ**:  
  * **動的モード選択**: OrchestrationAgentがユーザーのクエリを分析し、「単純応答」「フル機能分析」「内省的対話」など、7種類以上の思考パイプラインから最適なものを自動で選択します。  
  * **予測符号化**: PredictiveCodingEngineがユーザーの入力の新規性（予測誤差）を検出し、それを学習のトリガーとすることで、効率的に知識を更新します。  
  * **デジタルホメオスタシス**: EthicalMotivationEngineがシステムの知的健全性（論理的整合性など）を監視し、自己の価値観に基づいて行動を動機付けます。  
* **🛠️ 高度なツール利用能力 (Tool Use)**:  
  * 内部知識だけでは解決できない問題に対し、**TavilyによるWeb検索**や**Wikipedia検索**を能動的に利用して、リアルタイムで外部情報を参照します。  
  * ToolUsingAgentが必要なツールとクエリを自律的に判断します。  
* **🔍 自己反省型RAG (Metacognitive RAG)**:  
  * 検索した情報の質（関連性、網羅性）をRetrievalEvaluatorAgentが評価します。  
  * 情報が不十分だと判断した場合、QueryRefinementAgentが**検索クエリを自動的に修正し、質の高い情報が得られるまで検索を繰り返します**。  
* **🕸️ 知識の構造化 (Knowledge Structuring)**:  
  * 収集した情報を単なるテキストとしてではなく、KnowledgeGraphAgentが物事の関係性を捉えた**知識グラフ**として構造化し、より深いレベルで理解・記憶します。  
* **🌱 アイドル時の継続的学習 (Idle-Time Continuous Learning)**:  
  * IdleManagerがユーザーの非アクティブ時間を検知し、以下のバックグラウンドタスクを自動で実行します。  
    * **記憶の統合**: ConsolidationAgentが短期記憶（対話内容）を分析し、長期記憶（知識グラフ）へと統合します。  
    * **自律思考**: AutonomousAgentが設定されたトピックについて自律的に調査・学習を行い、知識を増やし続けます。  
    * **自己進化**: SelfEvolvingSystemが過去の対話の思考プロセスを分析し、パフォーマンス改善のための戦略を立案します。  
    * **創発性の探求**: EmergentIntelligenceNetworkがAIエージェントの新しい組み合わせを実験し、予期せぬ能力（創発的知能）を発見します。  
    * **価値観の進化**: EvolvingValueSystemがAIの行動結果を評価し、その核となる価値観を更新・進化させます。

## **🏛️ システムアーキテクチャ**

Luca3は、司令塔となるOrchestrationAgentとMetaIntelligenceEngineを中心に、複数の専門家AIエージェントと推論パイプラインが協調して動作する、高度にモジュール化されたシステムです。

graph TD  
    subgraph "User Interaction"  
        UI\[ユーザー入力\]  
    end

    subgraph "Core Engine"  
        direction LR  
        Orchestrator(OrchestrationAgent) \-- 意思決定 \--\> Engine(MetaIntelligenceEngine)  
        Engine \-- パイプライン実行 \--\> Pipelines  
    end

    subgraph "Reasoning Pipelines"  
        direction TB  
        Pipelines \--\> Full(Full Pipeline)  
        Pipelines \--\> Simple(Simple Pipeline)  
        Pipelines \--\> Internal(Internal Dialogue Pipeline)  
        Pipelines \--\> Other(...)  
    end  
      
    subgraph "Cognitive & Metacognitive Loop (Full Pipeline)"  
        direction TB  
        Plan(PlanningAgent) \--\> CogLoop(CognitiveLoopAgent)  
        CogLoop \-- ツール使用 \--\> Tools\[外部ツール\]  
        CogLoop \-- 知識参照 \--\> Memory\[記憶\]  
        CogLoop \--\> AnswerGen(Answer Generation)  
        AnswerGen \--\> MetaCog(MetaCognitiveEngine)  
    end

    subgraph "Idle-Time Autonomous Systems"  
        direction TB  
        IdleMgr(IdleManager) \-- トリガー \--\> SelfEvolve(SelfEvolvingSystem)  
        IdleMgr \-- トリガー \--\> AutoAgent(AutonomousAgent)  
        IdleMgr \-- トリガー \--\> Consolidator(ConsolidationAgent)  
        IdleMgr \-- トリガー \--\> EmergentNet(EmergentIntelligenceNetwork)  
        IdleMgr \-- トリガー \--\> ValueSys(EvolvingValueSystem)  
    end  
      
    subgraph "Memory & Knowledge"  
        KB(KnowledgeBase / VectorStore)  
        KG(PersistentKnowledgeGraph)  
    end  
      
    subgraph "External Tools"  
        Tavily(Tavily Search)  
        Wiki(Wikipedia)  
    end

    UI \-- クエリ \--\> Orchestrator  
    Full \--\> FinalOutput  
    Simple \--\> FinalOutput  
    Internal \--\> FinalOutput  
    Other \--\> FinalOutput  
    FinalOutput\[最終出力\] \-- 表示 \--\> UI  
      
    style "Core Engine" fill:\#1e293b,stroke:\#fff,stroke-width:2px,color:\#fff  
    style "Reasoning Pipelines" fill:\#334155,stroke:\#fff,stroke-width:1px,color:\#fff  
    style "Cognitive & Metacognitive Loop (Full Pipeline)" fill:\#475569,stroke:\#fff,stroke-width:1px,color:\#fff  
    style "Idle-Time Autonomous Systems" fill:\#0f766e,stroke:\#fff,stroke-width:2px,color:\#fff

## **🚀 使い方**

### **1\. 環境設定**

**a. Python仮想環境の作成**

python3 \-m venv .venv  
source .venv/bin/activate

b. 必要なライブラリのインストール  
プロジェクトのルートにあるrequirements.txtを使用して、必要なパッケージを一括でインストールします。  
pip install \-r requirements.txt  
pip install python-dotenv

c. APIキーの設定 (.envファイル)  
Web検索機能（Tavily）を利用するために、プロジェクトのルートディレクトリに.envファイルを作成し、APIキーを設定します。

1. env.sampleファイルをコピーして、.envという名前のファイルを作成します。  
2. [Tavilyの公式サイト](https://tavily.com/)でAPIキーを取得します。  
3. 作成した.envファイルを開き、あなたのAPIキーを記述します。  
   \# .env  
   TAVILY\_API\_KEY="ここに取得したTavily APIキーを貼り付け"

### **2\. Ollamaのセットアップ**

このプロジェクトは、ローカルで動作するLLMプラットフォームである[Ollama](https://ollama.com/)を使用します。

a. Ollamaのインストール  
公式サイトの指示に従い、Ollamaをインストールしてください。  
b. 必要なモデルのダウンロード  
ターミナルで以下のコマンドを実行し、プロジェクトで使用するモデルをダウンロードします。  
\# 文章生成用モデル  
ollama pull gemma3:latest

\# テキスト埋め込み用モデル  
ollama pull nomic-embed-text

### **3\. アプリケーションの実行**

すべての設定が完了したら、以下のコマンドでアプリケーションを起動します。

python run.py

起動すると、コンソールで対話を開始できます。対話を終了するにはquitまたはexitと入力してください。

## **⚙️ 設定**

プロジェクトの動作は/app/config.pyファイルで調整できます。

* **LLMモデルの変更**: GENERATION\_LLM\_SETTINGSのmodelの値を、Ollamaで利用可能な他のモデル名に変更できます。  
* **自律思考の実行間隔**: AUTONOMOUS\_CYCLE\_INTERVAL\_SECONDSなどの値を変更することで、アイドル時の各タスクの実行頻度を調整できます。  
* **パイプラインの挙動**: PIPELINE\_SETTINGS内の値を変更することで、特定のパイプライン（例：内省的対話のターン数）の動作を微調整できます。

## **📦 主要な依存関係**

このプロジェクトは以下の主要なライブラリに依存しています。詳細はrequirements.txtを参照してください。

* ollama: ローカルLLM実行  
* langchain, langchain-community: AIエージェントとツールのフレームワーク  
* faiss-cpu: 高速なベクトル検索  
* dependency-injector: DIコンテナによるクリーンなアーキテクチャ管理  
* pydantic: 厳密なデータ構造定義  
* python-dotenv: .envファイルによる環境変数管理  
* tavily-python, wikipedia: 外部情報検索ツール