"""
Architecture Pattern Knowledge Base — expanded to 20+ patterns.

This is the genuine differentiator: a curated knowledge base of architecture
patterns with real cost data, constraint satisfaction, and composition rules.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ConstraintType(str, Enum):
    HARD = "hard"
    SOFT = "soft"
    PREFERRED = "preferred"


@dataclass
class Constraint:
    name: str
    type: ConstraintType
    description: str


@dataclass
class CostModel:
    component: str
    base_monthly: float
    per_unit: float
    unit: str
    notes: str = ""


@dataclass
class ArchitecturePattern:
    id: str
    name: str
    description: str
    components: List[Dict[str, Any]]
    cost_models: List[CostModel]
    constraints_satisfied: List[str]
    constraints_violated: List[str]
    trade_offs: Dict[str, Any]
    max_scale: str
    complexity: str
    team_size_required: str
    tags: List[str] = field(default_factory=list)


class PatternKnowledgeBase:
    """20+ architecture patterns with costs, constraints, and trade-offs."""

    def __init__(self):
        self._patterns: Dict[str, ArchitecturePattern] = {}
        self._load_all_patterns()

    def _load_all_patterns(self):
        patterns = [
            # === RAG PATTERNS ===
            ArchitecturePattern(
                id="rag-basic", name="Basic RAG Pipeline",
                description="Document ingestion + vector search + LLM generation",
                components=[{"name": "Embeddings", "tech": "OpenAI"}, {"name": "Vector Store", "tech": "pgvector"}, {"name": "LLM", "tech": "GPT-4o"}],
                cost_models=[CostModel("Embeddings", 0, 0.00002, "tokens"), CostModel("Vector Store", 70, 0.1, "GB"), CostModel("LLM", 0, 0.01, "1K tokens")],
                constraints_satisfied=["self_hosted", "python_native"], constraints_violated=["gdpr_eu"],
                trade_offs={"pros": ["Simple", "Fast to build"], "cons": ["No reranking", "No citations"]},
                max_scale="100K docs", complexity="low", team_size_required="1-2 devs", tags=["rag", "search"]),
            ArchitecturePattern(
                id="rag-enterprise", name="Enterprise RAG",
                description="Hybrid search + reranking + citation verification",
                components=[{"name": "Vector Store", "tech": "pgvector"}, {"name": "BM25", "tech": "Elasticsearch"}, {"name": "Reranker", "tech": "Cross-encoder"}, {"name": "Query Router", "tech": "Intent classifier"}, {"name": "Cache", "tech": "Redis"}],
                cost_models=[CostModel("Vector Store", 150, 0.15, "GB"), CostModel("BM25", 200, 0, "node"), CostModel("Reranker", 50, 0, "GPU"), CostModel("Cache", 40, 0, "instance")],
                constraints_satisfied=["self_hosted", "citations", "hybrid_search"], constraints_violated=[],
                trade_offs={"pros": ["Best quality", "Citations", "Query-aware"], "cons": ["Higher cost", "More infra"]},
                max_scale="10M docs", complexity="high", team_size_required="3-5 devs", tags=["rag", "enterprise"]),
            ArchitecturePattern(
                id="rag-serverless", name="Serverless RAG",
                description="Lambda + Pinecone + API Gateway for zero-ops RAG",
                components=[{"name": "Compute", "tech": "AWS Lambda"}, {"name": "Vector DB", "tech": "Pinecone"}, {"name": "API", "tech": "API Gateway"}],
                cost_models=[CostModel("Compute", 0, 0.0000002, "requests"), CostModel("Vector DB", 70, 0.3, "GB")],
                constraints_satisfied=["serverless", "auto_scaling"], constraints_violated=["on_premise", "gdpr_eu"],
                trade_offs={"pros": ["Zero ops", "Auto-scale"], "cons": ["Vendor lock-in", "Cold starts"]},
                max_scale="1M queries/day", complexity="low", team_size_required="1 dev", tags=["rag", "serverless"]),
            # === AGENTIC PATTERNS ===
            ArchitecturePattern(
                id="agentic-workflow", name="Agentic Workflow with HITL",
                description="LLM agents executing multi-step workflows with human oversight",
                components=[{"name": "Workflow Engine", "tech": "Custom/Temporal"}, {"name": "LLM Agents", "tech": "GPT-4o"}, {"name": "HITL Manager", "tech": "Custom"}, {"name": "Event Store", "tech": "PostgreSQL"}],
                cost_models=[CostModel("Engine", 100, 0, "instance"), CostModel("LLM", 0, 0.03, "1K tokens")],
                constraints_satisfied=["audit_trail", "human_oversight", "compliance"], constraints_violated=[],
                trade_offs={"pros": ["Full audit", "Replay", "Retry"], "cons": ["Higher latency", "LLM costs"]},
                max_scale="10K workflows/day", complexity="high", team_size_required="3-5 devs", tags=["agentic", "workflow"]),
            ArchitecturePattern(
                id="agentic-simple", name="Simple Agent Pipeline",
                description="Single LLM call with tool calling, no state machine",
                components=[{"name": "LLM", "tech": "GPT-4o"}, {"name": "Tools", "tech": "Function calling"}, {"name": "API", "tech": "FastAPI"}],
                cost_models=[CostModel("LLM", 0, 0.03, "1K tokens"), CostModel("API", 25, 0, "instance")],
                constraints_satisfied=["python_native", "fast_to_build"], constraints_violated=["audit_trail", "compliance"],
                trade_offs={"pros": ["Simple", "Fast"], "cons": ["No audit", "No HITL"]},
                max_scale="100K calls/day", complexity="low", team_size_required="1 dev", tags=["agentic", "simple"]),
            ArchitecturePattern(
                id="agentic-multi-agent", name="Multi-Agent Orchestration",
                description="Multiple specialized agents collaborating on complex tasks",
                components=[{"name": "Orchestrator", "tech": "LangGraph"}, {"name": "Agents", "tech": "Multiple LLMs"}, {"name": "Message Bus", "tech": "Redis/Kafka"}, {"name": "Shared State", "tech": "PostgreSQL"}],
                cost_models=[CostModel("Orchestrator", 150, 0, "instance"), CostModel("Agents", 0, 0.05, "1K tokens"), CostModel("Bus", 30, 0.00001, "messages")],
                constraints_satisfied=["complex_reasoning", "parallelism"], constraints_violated=["simple_crud"],
                trade_offs={"pros": ["Complex tasks", "Parallel execution"], "cons": ["High cost", "Complex debugging"]},
                max_scale="1K complex tasks/day", complexity="very_high", team_size_required="4-6 devs", tags=["agentic", "multi-agent"]),
            # === EVENT SOURCING PATTERNS ===
            ArchitecturePattern(
                id="event-sourced-api", name="Event-Sourced CQRS",
                description="Write: events. Read: projections. Full audit trail.",
                components=[{"name": "Event Store", "tech": "PostgreSQL"}, {"name": "Projections", "tech": "Async workers"}, {"name": "Read Store", "tech": "PostgreSQL/ES"}],
                cost_models=[CostModel("Event Store", 30, 0.00005, "events"), CostModel("Projections", 50, 0, "instance")],
                constraints_satisfied=["audit_trail", "time_travel", "replay"], constraints_violated=["simple_crud"],
                trade_offs={"pros": ["Audit trail", "Time-travel", "Replay"], "cons": ["Eventual consistency", "Complexity"]},
                max_scale="1M events/day", complexity="high", team_size_required="2-4 devs", tags=["event-sourcing", "cqrs"]),
            ArchitecturePattern(
                id="event-sourced-lightweight", name="Lightweight Event Sourcing",
                description="Event log in PostgreSQL without full CQRS complexity",
                components=[{"name": "Event Log", "tech": "PostgreSQL append-only"}, {"name": "Replay", "tech": "Python script"}],
                cost_models=[CostModel("Event Log", 20, 0.00001, "events")],
                constraints_satisfied=["audit_trail", "replay"], constraints_violated=["high_write_throughput"],
                trade_offs={"pros": ["Simple
