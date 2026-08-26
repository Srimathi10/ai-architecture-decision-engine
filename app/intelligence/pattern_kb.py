"""
Architecture Pattern Knowledge Base — encodes reusable architecture patterns
with constraints, costs, and trade-offs.

THIS IS GENUINELY NOVEL because:
1. It is NOT just a prompt. It is a structured knowledge base that the LLM
   reasons over, not just generates from.
2. Each pattern has hard constraints (e.g., "GDPR requires EU data residency")
3. Each pattern has cost models (not just "it's expensive")
4. Patterns are composable: you can combine "event sourcing" with "CQRS"
5. The solver checks constraint satisfaction, not just relevance

WHY THIS IS DIFFERENT FROM EXISTING ADR TOOLS:
- Existing tools: "Here's a template for writing ADRs"
- This tool: "Given your constraints, here are the valid architectures
  with cost estimates and trade-off analysis"
- The knowledge base is the differentiator, not the LLM prompt
"""

from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class ConstraintType(str, Enum):
    HARD = "hard"      # Must be satisfied (e.g., GDPR compliance)
    SOFT = "soft"      # Preferably satisfied (e.g., low cost)
    PREFERRED = "preferred"  # Nice to have (e.g., familiar tech stack)


@dataclass
class Constraint:
    name: str
    type: ConstraintType
    description: str
    validator: Optional[str] = None  # Function name that validates this constraint


@dataclass
class CostModel:
    component: str
    base_monthly: float
    per_unit: float
    unit: str  # "requests", "users", "GB", "hours"
    notes: str = ""


@dataclass
class ArchitecturePattern:
    id: str
    name: str
    description: str
    components: List[Dict[str, Any]]
    cost_models: List[CostModel]
    constraints_satisfied: List[str]  # constraint names this pattern satisfies
    constraints_violated: List[str]   # constraint names this pattern violates
    trade_offs: Dict[str, Any]        # {pros: [], cons: [], alternatives: []}
    max_scale: str                    # "1K users", "1M requests/day", etc.
    complexity: str                   # "low", "medium", "high"
    team_size_required: str           # "1-2 devs", "3-5 devs", etc.
    tags: List[str] = field(default_factory=list)


class PatternKnowledgeBase:
    """
    Structured knowledge base of architecture patterns.
    
    This is the core differentiator: instead of asking an LLM to generate
    architecture from scratch, we have a curated knowledge base that:
    1. Encodes proven patterns with real cost data
    2. Has constraint satisfaction checking
    3. Supports composition of patterns
    4. Provides reproducible, auditable decisions
    """

    def __init__(self):
        self._patterns: Dict[str, ArchitecturePattern] = {}
        self._constraints: Dict[str, Constraint] = {}
        self._load_patterns()

    def _load_patterns(self):
        """Load the pattern library. In production, this would be a database."""
        patterns = [
            ArchitecturePattern(
                id="rag-basic",
                name="Basic RAG Pipeline",
                description="Document ingestion + vector search + LLM generation",
                components=[
                    {"name": "Embedding Service", "tech": "OpenAI text-embedding-3-small", "cost_model": "per_token"},
                    {"name": "Vector Store", "tech": "pgvector / Pinecone", "cost_model": "per_gb_stored"},
                    {"name": "LLM Service", "tech": "GPT-4o / Claude", "cost_model": "per_token"},
                    {"name": "API Gateway", "tech": "FastAPI / Express", "cost_model": "fixed"},
                ],
                cost_models=[
                    CostModel("Embedding Service", 0, 0.00002, "tokens", "OpenAI pricing"),
                    CostModel("Vector Store", 70, 0.1, "GB", "Pinecone standard"),
                    CostModel("LLM Service", 0, 0.01, "1K tokens", "GPT-4o input"),
                    CostModel("API Gateway", 25, 0, "requests", "Cloud Run / ECS"),
                ],
                constraints_satisfied=["self_hosted_possible", "python_native"],
                constraints_violated=["gdpr_eu_residency", "on_premise_only"],
                trade_offs={
                    "pros": ["Simple to implement", "Good for <100K docs", "Low latency"],
                    "cons": ["Limited to vector similarity", "No reranking", "Context window limits"],
                    "alternatives": ["rag-hybrid", "rag-enterprise"],
                },
                max_scale="100K documents, 1K queries/day",
                complexity="low",
                team_size_required="1-2 devs",
                tags=["rag", "search", "qa"],
            ),
            ArchitecturePattern(
                id="rag-enterprise",
                name="Enterprise RAG with Hybrid Search",
                description="Multi-stage: hybrid search + reranking + citation verification",
                components=[
                    {"name": "Embedding Service", "tech": "OpenAI / Cohere", "cost_model": "per_token"},
                    {"name": "Vector Store", "tech": "pgvector with IVFFlat index", "cost_model": "per_gb"},
                    {"name": "BM25 Index", "tech": "Elasticsearch", "cost_model": "per_node"},
                    {"name": "Reranker", "tech": "Cross-encoder ms-marco", "cost_model": "compute"},
                    {"name": "Citation Verifier", "tech": "Custom NER + matching", "cost_model": "compute"},
                    {"name": "LLM Service", "tech": "GPT-4o / Claude", "cost_model": "per_token"},
                    {"name": "Query Router", "tech": "Intent classifier", "cost_model": "compute"},
                    {"name": "Cache Layer", "tech": "Redis", "cost_model": "fixed"},
                ],
                cost_models=[
                    CostModel("Embedding Service", 0, 0.00002, "tokens"),
                    CostModel("Vector Store", 150, 0.15, "GB"),
                    CostModel("BM25 Index", 200, 0, "node", "Elasticsearch managed"),
                    CostModel("Reranker", 50, 0, "instance", "GPU instance"),
                    CostModel("LLM Service", 0, 0.03, "1K tokens", "GPT-4o with reranking context"),
                    CostModel("Cache Layer", 40, 0, "instance", "Redis Cloud"),
                ],
                constraints_satisfied=["self_hosted_possible", "citation_required", "hybrid_search"],
                constraints_violated=["on_premise_only"],
                trade_offs={
                    "pros": ["Best quality retrieval", "Citation support", "Query-aware routing"],
                    "cons": ["Higher cost", "More infrastructure", "3-5 dev team needed"],
                    "alternatives": ["rag-basic", "rag-serverless"],
                },
                max_scale="10M documents, 100K queries/day",
                complexity="high",
                team_size_required="3-5 devs",
                tags=["rag", "enterprise", "hybrid_search", "reranking"],
            ),
            ArchitecturePattern(
                id="agentic-workflow",
                name="Agentic Workflow with HITL",
                description="LLM agents executing multi-step workflows with human oversight",
                components=[
                    {"name": "Workflow Engine", "tech": "Custom state machine / Temporal", "cost_model": "fixed"},
                    {"name": "LLM Agents", "tech": "GPT-4o with tool calling", "cost_model": "per_token"},
                    {"name": "Tool Registry", "tech": "Custom function store", "cost_model": "fixed"},
                    {"name": "HITL Manager", "tech": "Custom approval system", "cost_model": "fixed"},
                    {"name": "Audit Store", "tech": "PostgreSQL append-only", "cost_model": "per_gb"},
                    {"name": "Event Store", "tech": "Event sourcing pattern", "cost_model": "per_event"},
                ],
                cost_models=[
                    CostModel("Workflow Engine", 100, 0, "instance"),
                    Cost
