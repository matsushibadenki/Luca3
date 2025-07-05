# /app/containers.py
# title: アプリケーションDIコンテナ
# role: 各AIエージェント、LLM、プロンプトテンプレート、およびその他の依存関係を定義し、提供する。

from dependency_injector import containers, providers
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from typing import Dict, Any

from app.config import settings
import app.agents.prompts as prompts

from app.agents.base import AIAgent
from app.agents.information_agent import InformationAgent
from app.agents.logical_agent import LogicalAgent
from app.agents.emotional_agent import EmotionalAgent
from app.agents.user_profiling_agent import UserProfilingAgent
from app.agents.master_agent import MasterAgent
from app.agents.fact_checking_agent import FactCheckingAgent
from app.agents.autonomous_agent import AutonomousAgent
from app.agents.word_learning_agent import WordLearningAgent
from app.agents.knowledge_assimilation_agent import KnowledgeAssimilationAgent
from app.agents.planning_agent import PlanningAgent
from app.agents.cognitive_loop_agent import CognitiveLoopAgent
from app.agents.tool_using_agent import ToolUsingAgent
from app.agents.retrieval_evaluator_agent import RetrievalEvaluatorAgent
from app.agents.query_refinement_agent import QueryRefinementAgent
from app.agents.knowledge_graph_agent import KnowledgeGraphAgent
from app.agents.consolidation_agent import ConsolidationAgent
from app.agents.thinking_modules import DecomposeAgent, CritiqueAgent, SynthesizeAgent
from app.agents.self_improvement_agent import SelfImprovementAgent
from app.agents.orchestration_agent import OrchestrationAgent
from app.agents.self_correction_agent import SelfCorrectionAgent
from app.cognitive_modeling.predictive_coding_engine import PredictiveCodingEngine
from app.cognitive_modeling.world_model_agent import WorldModelAgent
from app.integrated_information_processing.integrated_information_agent import IntegratedInformationAgent
from app.internal_dialogue.dialogue_participant_agent import DialogueParticipantAgent
from app.internal_dialogue.mediator_agent import MediatorAgent
from app.internal_dialogue.consciousness_staging_area import ConsciousnessStagingArea
from app.digital_homeostasis import IntegrityMonitor, EthicalMotivationEngine
from app.reasoning.complexity_analyzer import ComplexityAnalyzer
from app.meta_cognition.self_critic_agent import SelfCriticAgent
from app.meta_cognition.meta_cognitive_engine import MetaCognitiveEngine
from app.memory.working_memory import WorkingMemory
from app.memory.memory_consolidator import MemoryConsolidator
from app.problem_discovery.problem_discovery_agent import ProblemDiscoveryAgent
from app.rag.knowledge_base import KnowledgeBase
from app.rag.retriever import Retriever
from app.tools.tool_belt import ToolBelt
from app.knowledge_graph.persistent_knowledge_graph import PersistentKnowledgeGraph
from app.value_evolution.value_evaluator import ValueEvaluator
from app.engine import MetaIntelligenceEngine
from app.pipelines.base import BasePipeline
from app.pipelines.simple_pipeline import SimplePipeline
from app.pipelines.full_pipeline import FullPipeline
from app.pipelines.parallel_pipeline import ParallelPipeline
from app.pipelines.quantum_inspired_pipeline import QuantumInspiredPipeline
from app.pipelines.speculative_pipeline import SpeculativePipeline
from app.pipelines.self_discover_pipeline import SelfDiscoverPipeline
from app.pipelines.internal_dialogue_pipeline import InternalDialoguePipeline
from app.meta_intelligence import (
    MetaIntelligence, MasterSystemConfig, CollectiveIntelligenceOrganizer,
    SelfEvolvingSystem, DynamicArchitecture, EmergentIntelligenceNetwork, EvolvingValueSystem
)
from app.meta_intelligence.providers.base import LLMProvider as BaseLLMProvider, ProviderCapability
from app.idle_manager import IdleManager

class OllamaProvider(BaseLLMProvider):
    def __init__(self, llm_instance: OllamaLLM):
        self._llm = llm_instance

    def get_capabilities(self) -> Dict[ProviderCapability, bool]:
        return {
            ProviderCapability.STANDARD_CALL: True,
            ProviderCapability.STREAMING: False,
            ProviderCapability.TOOLS: False,
            ProviderCapability.FUNCTION_CALLING: False,
            ProviderCapability.ENHANCED_REASONING: False
        }

    async def standard_call(self, prompt: str, system_prompt: str = "", **kwargs) -> Dict[str, Any]:
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = await self._llm.ainvoke(full_prompt, **kwargs)
        return {"text": response, "usage": {}, "model": self._llm.model}

    def should_use_enhancement(self, prompt: str, **kwargs) -> bool:
        return "force_v2" in kwargs and kwargs["force_v2"]

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.main",
            "run",
        ]
    )

    # --- Core Components ---
    llm_instance: providers.Singleton[OllamaLLM] = providers.Singleton(OllamaLLM, **settings.GENERATION_LLM_SETTINGS)
    verifier_llm_instance: providers.Singleton[OllamaLLM] = providers.Singleton(OllamaLLM, **settings.VERIFIER_LLM_SETTINGS)
    output_parser: providers.Singleton[StrOutputParser] = providers.Singleton(StrOutputParser)
    json_output_parser: providers.Singleton[JsonOutputParser] = providers.Singleton(JsonOutputParser)
    tool_belt: providers.Singleton[ToolBelt] = providers.Singleton(ToolBelt)
    knowledge_base: providers.Resource[KnowledgeBase] = providers.Resource(
        KnowledgeBase.create_and_load,
        source=settings.KNOWLEDGE_BASE_SOURCE
    )
    persistent_knowledge_graph: providers.Singleton[PersistentKnowledgeGraph] = providers.Singleton(
        PersistentKnowledgeGraph,
        storage_path=settings.KNOWLEDGE_GRAPH_STORAGE_PATH
    )
    retriever: providers.Singleton[Retriever] = providers.Singleton(Retriever, knowledge_base=knowledge_base)
    memory_consolidator: providers.Singleton[MemoryConsolidator] = providers.Singleton(
        MemoryConsolidator, log_file_path=settings.MEMORY_LOG_FILE_PATH
    )
    working_memory: providers.Singleton[WorkingMemory] = providers.Singleton(WorkingMemory)

    # --- MetaIntelligence System ---
    ollama_provider: providers.Singleton[OllamaProvider] = providers.Singleton(OllamaProvider, llm_instance=llm_instance)
    meta_intelligence_config: providers.Singleton[MasterSystemConfig] = providers.Singleton(MasterSystemConfig)
    meta_intelligence_system: providers.Singleton[MetaIntelligence] = providers.Singleton(
        MetaIntelligence,
        primary_provider=ollama_provider,
        config=meta_intelligence_config
    )
    collective_intelligence_organizer: providers.Factory[CollectiveIntelligenceOrganizer] = providers.Factory(
        CollectiveIntelligenceOrganizer,
        provider=ollama_provider
    )
    dynamic_architecture: providers.Factory[DynamicArchitecture] = providers.Factory(
        DynamicArchitecture,
        provider=ollama_provider
    )
    emergent_intelligence_network: providers.Factory[EmergentIntelligenceNetwork] = providers.Factory(
        EmergentIntelligenceNetwork,
        provider=ollama_provider
    )
    evolving_value_system: providers.Factory[EvolvingValueSystem] = providers.Factory(
        EvolvingValueSystem,
        provider=ollama_provider
    )
    
    self_critic_agent: providers.Factory[SelfCriticAgent] = providers.Factory(
        SelfCriticAgent, llm=llm_instance, output_parser=output_parser,
        prompt_template=prompts.SELF_CRITIC_AGENT_PROMPT
    )
    meta_cognitive_engine: providers.Factory[MetaCognitiveEngine] = providers.Factory(
        MetaCognitiveEngine, self_critic_agent=self_critic_agent
    )
    self_improvement_agent: providers.Factory[SelfImprovementAgent] = providers.Factory(
        SelfImprovementAgent,
        llm=llm_instance,
        output_parser=json_output_parser,
        prompt_template=prompts.SELF_IMPROVEMENT_AGENT_PROMPT
    )
    self_correction_agent: providers.Factory[SelfCorrectionAgent] = providers.Factory(
        SelfCorrectionAgent,
        llm=llm_instance,
        output_parser=output_parser,
        memory_consolidator=memory_consolidator,
        prompt_template=prompts.SELF_CORRECTION_AGENT_PROMPT,
    )

    self_evolving_system: providers.Factory[SelfEvolvingSystem] = providers.Factory(
        SelfEvolvingSystem,
        meta_cognitive_engine=meta_cognitive_engine,
        self_improvement_agent=self_improvement_agent,
        self_correction_agent=self_correction_agent
    )
    
    # --- Agents (の一部) ---
    # IdleManagerが依存するため、先に定義
    autonomous_agent: providers.Factory[AutonomousAgent] = providers.Factory(
        AutonomousAgent,
        llm=llm_instance,
        output_parser=output_parser,
        memory_consolidator=memory_consolidator,
        knowledge_base=knowledge_base,
        tool_belt=tool_belt,
    )
    
    knowledge_graph_agent: providers.Factory[KnowledgeGraphAgent] = providers.Factory(
        KnowledgeGraphAgent,
        llm=llm_instance,
        prompt_template=prompts.KNOWLEDGE_GRAPH_AGENT_PROMPT
    )

    consolidation_agent: providers.Factory[ConsolidationAgent] = providers.Factory(
        ConsolidationAgent,
        llm=llm_instance,
        output_parser=output_parser,
        prompt_template=prompts.CONSOLIDATION_AGENT_PROMPT,
        knowledge_base=knowledge_base,
        knowledge_graph_agent=knowledge_graph_agent,
        memory_consolidator=memory_consolidator,
        persistent_knowledge_graph=persistent_knowledge_graph,
    )
    
    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↓修正開始◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
    idle_manager: providers.Singleton[IdleManager] = providers.Singleton(
        IdleManager,
        self_evolving_system=self_evolving_system,
        autonomous_agent=autonomous_agent,
        consolidation_agent=consolidation_agent,
        emergent_network=emergent_intelligence_network,
        value_system=evolving_value_system,
        memory_consolidator=memory_consolidator,
    )
    # ◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️↑修正終わり◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️◾️
    
    # --- Agents (残り) ---
    complexity_analyzer: providers.Factory[ComplexityAnalyzer] = providers.Factory(ComplexityAnalyzer)
    orchestration_agent: providers.Factory[OrchestrationAgent] = providers.Factory(
        OrchestrationAgent,
        llm=llm_instance,
        output_parser=json_output_parser,
        prompt_template=prompts.ORCHESTRATION_PROMPT,
        complexity_analyzer=complexity_analyzer,
    )
    
    world_model_agent: providers.Factory[WorldModelAgent] = providers.Factory(
        WorldModelAgent,
        llm=llm_instance,
        knowledge_graph_agent=knowledge_graph_agent,
        persistent_knowledge_graph=persistent_knowledge_graph,
    )
    predictive_coding_engine: providers.Factory[PredictiveCodingEngine] = providers.Factory(
        PredictiveCodingEngine,
        world_model_agent=world_model_agent,
        working_memory=working_memory,
        knowledge_graph_agent=knowledge_graph_agent,
        persistent_knowledge_graph=persistent_knowledge_graph,
    )
    integrated_information_agent: providers.Factory[IntegratedInformationAgent] = providers.Factory(
        IntegratedInformationAgent,
        llm=llm_instance,
        output_parser=output_parser
    )
    dialogue_participant_agent: providers.Factory[DialogueParticipantAgent] = providers.Factory(
        DialogueParticipantAgent,
        llm=llm_instance
    )
    mediator_agent: providers.Factory[MediatorAgent] = providers.Factory(
        MediatorAgent,
        llm=llm_instance
    )
    consciousness_staging_area: providers.Factory[ConsciousnessStagingArea] = providers.Factory(
        ConsciousnessStagingArea,
        llm=llm_instance,
        mediator_agent=mediator_agent
    )
    value_evaluator: providers.Factory[ValueEvaluator] = providers.Factory(
        ValueEvaluator,
        llm=llm_instance,
        output_parser=json_output_parser
    )
    integrity_monitor: providers.Factory[IntegrityMonitor] = providers.Factory(
        IntegrityMonitor,
        llm=llm_instance,
        knowledge_graph=persistent_knowledge_graph
    )
    ethical_motivation_engine: providers.Factory[EthicalMotivationEngine] = providers.Factory(
        EthicalMotivationEngine,
        integrity_monitor=integrity_monitor,
        value_evaluator=value_evaluator,
    )
    problem_discovery_agent: providers.Factory[ProblemDiscoveryAgent] = providers.Factory(
        ProblemDiscoveryAgent, llm=llm_instance, output_parser=json_output_parser,
        prompt_template=prompts.PROBLEM_DISCOVERY_AGENT_PROMPT
    )
    
    planning_agent: providers.Factory[PlanningAgent] = providers.Factory(
        PlanningAgent, llm=llm_instance, output_parser=output_parser,
        prompt_template=prompts.PLANNING_AGENT_PROMPT
    )
    retrieval_evaluator_agent: providers.Factory[RetrievalEvaluatorAgent] = providers.Factory(
        RetrievalEvaluatorAgent,
        llm=llm_instance,
        prompt_template=prompts.RETRIEVAL_EVALUATOR_AGENT_PROMPT
    )
    query_refinement_agent: providers.Factory[QueryRefinementAgent] = providers.Factory(
        QueryRefinementAgent,
        llm=llm_instance,
        output_parser=output_parser,
        prompt_template=prompts.QUERY_REFINEMENT_AGENT_PROMPT
    )
    tool_using_agent: providers.Factory[ToolUsingAgent] = providers.Factory(
        ToolUsingAgent,
        llm=llm_instance,
        output_parser=output_parser,
        prompt_template=prompts.TOOL_USING_AGENT_PROMPT
    )
    cognitive_loop_agent: providers.Factory[CognitiveLoopAgent] = providers.Factory(
        CognitiveLoopAgent,
        llm=llm_instance,
        output_parser=output_parser,
        prompt_template=prompts.COGNITIVE_LOOP_AGENT_PROMPT,
        retriever=retriever,
        retrieval_evaluator_agent=retrieval_evaluator_agent,
        query_refinement_agent=query_refinement_agent,
        knowledge_graph_agent=knowledge_graph_agent,
        persistent_knowledge_graph=persistent_knowledge_graph,
        tool_using_agent=tool_using_agent,
        tool_belt=tool_belt,
    )

    decompose_agent: providers.Factory[DecomposeAgent] = providers.Factory(DecomposeAgent, llm=llm_instance, output_parser=output_parser)
    critique_agent: providers.Factory[CritiqueAgent] = providers.Factory(CritiqueAgent, llm=llm_instance, output_parser=output_parser)
    synthesize_agent: providers.Factory[SynthesizeAgent] = providers.Factory(SynthesizeAgent, llm=llm_instance, output_parser=output_parser)
    _master_agent_factory: providers.Factory[MasterAgent] = providers.Factory(
        MasterAgent,
        llm=llm_instance,
        output_parser=output_parser,
        memory_consolidator=memory_consolidator,
        ethical_motivation_engine=ethical_motivation_engine,
        predictive_coding_engine=predictive_coding_engine,
        working_memory=working_memory,
        engine=providers.Self,
        value_evaluator=value_evaluator,
        orchestration_agent=orchestration_agent,
    )
    simple_pipeline: providers.Factory[SimplePipeline] = providers.Factory(
        SimplePipeline,
        master_agent=_master_agent_factory,
        cognitive_loop_agent=cognitive_loop_agent
    )
    full_pipeline: providers.Factory[FullPipeline] = providers.Factory(
        FullPipeline,
        master_agent=_master_agent_factory,
        planning_agent=planning_agent,
        cognitive_loop_agent=cognitive_loop_agent,
        meta_cognitive_engine=meta_cognitive_engine,
        problem_discovery_agent=problem_discovery_agent,
        memory_consolidator=memory_consolidator,
        self_improvement_agent=self_improvement_agent,
        self_correction_agent=self_correction_agent,
        self_evolving_system=self_evolving_system,
    )
    parallel_pipeline: providers.Factory[ParallelPipeline] = providers.Factory(
        ParallelPipeline,
        cognitive_loop_agent_factory=cognitive_loop_agent.provider,
        master_agent=_master_agent_factory
    )
    quantum_inspired_pipeline: providers.Factory[QuantumInspiredPipeline] = providers.Factory(
        QuantumInspiredPipeline,
        master_agent=_master_agent_factory,
        integrated_information_agent=integrated_information_agent,
    )
    speculative_pipeline: providers.Factory[SpeculativePipeline] = providers.Factory(
        SpeculativePipeline,
        drafter_llm=llm_instance,
        verifier_llm=verifier_llm_instance,
        output_parser=output_parser
    )
    self_discover_pipeline: providers.Factory[SelfDiscoverPipeline] = providers.Factory(
        SelfDiscoverPipeline,
        planning_agent=planning_agent,
        decompose_agent=decompose_agent,
        critique_agent=critique_agent,
        synthesize_agent=synthesize_agent,
        cognitive_loop_agent=cognitive_loop_agent
    )
    internal_dialogue_pipeline: providers.Factory[InternalDialoguePipeline] = providers.Factory(
        InternalDialoguePipeline,
        dialogue_participant_agent=dialogue_participant_agent,
        consciousness_staging_area=consciousness_staging_area,
        integrated_information_agent=integrated_information_agent
    )
    engine: providers.Singleton[MetaIntelligenceEngine] = providers.Singleton(
        MetaIntelligenceEngine,
        pipelines=providers.Dict(
            simple=simple_pipeline,
            full=full_pipeline,
            parallel=parallel_pipeline,
            quantum=quantum_inspired_pipeline,
            speculative=speculative_pipeline,
            self_discover=self_discover_pipeline,
            internal_dialogue=internal_dialogue_pipeline
        )
    )
    master_agent: providers.Factory[MasterAgent] = providers.Factory(
        MasterAgent,
        llm=llm_instance,
        output_parser=output_parser,
        memory_consolidator=memory_consolidator,
        ethical_motivation_engine=ethical_motivation_engine,
        predictive_coding_engine=predictive_coding_engine,
        working_memory=working_memory,
        engine=engine,
        value_evaluator=value_evaluator,
        orchestration_agent=orchestration_agent,
    )