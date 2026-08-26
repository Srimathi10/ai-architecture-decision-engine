# AI Architecture Decision Engine

**An AI-powered architecture reasoning system that transforms enterprise requirements into explainable, cost-aware, and security-aware cloud architectures.**

> This is not a chatbot that generates architecture diagrams. It is a **deterministic reasoning engine** that uses a structured knowledge base of architecture patterns, constraint satisfaction, and cost modeling to produce reproducible, auditable architecture decisions.

## The Problem

When engineering teams face architecture decisions ("Should we use event sourcing or CRUD?"), they typically:
1. Ask an LLM — which hallucinates costs and ignores constraints
2. Read blog posts — which are opinionated and not tailored to their requirements
3. Hire a consultant — which is expensive and not reproducible

**None of these approaches produce auditable, constraint-validated, cost-modeled architecture decisions.**

## Our Approach

This system uses a **three-layer architecture**:

```
┌─────────────────────────────────────────────────┐
│  Layer 1: Requirement Extraction (LLM)           │
│  "Build a customer-support assistant for 2M     │
│   conversations/month with GDPR requirements"   │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│  Layer 2: Constraint Solver (Deterministic)      │
│  Filter patterns by hard constraints →           │
│  Rank by soft constraints →                      │
│  Score by fit                                    │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│  Layer 3: Explanation Generator (LLM)           │
│  "Here's why this pattern was chosen,           │
│   what trade-offs exist, and what it costs"     │
└─────────────────────────────────────────────────┘
```

**Key insight:** The LLM generates requirements and explains decisions. The constraint solver produces the actual architecture. Same inputs always produce same outputs.

## Features

- **Architecture generation** from natural language requirements
- **Architecture alternatives** — shows top-N options with comparison
- **Cost optimization** — estimates monthly costs from structured cost models
- **Security reasoning** — identifies GDPR, SOC2, HIPAA implications
- **Scalability analysis** — evaluates patterns against scale requirements
- **Technology selection** — recommends specific technologies per component
- **Architecture trade-offs** — explicit pros/cons for each recommendation
- **Mermaid diagrams** — auto-generated architecture diagrams
- **Reproducible examples** — same requirements produce same architecture
- **Evaluation dataset** — 50+ test cases for benchmarking
- **Test suite** — 100% coverage of core reasoning logic
- **ADR generation** — produces Architecture Decision Records

## Quick Start

```bash
git clone https://github.com/Srimathi10/ai-architecture-decision-engine.git
cd ai-architecture-decision-engine
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
# Visit http://localhost:8000/docs
```

## Example: Full Architecture Decision

**Input:**
```json
{
  "requirement": "Build a customer-support assistant for 2M conversations/month with GDPR requirements. Budget is $5K/month. Team has 3 backend developers.",
  "constraints": {
    "hard": ["gdpr_compliance", "audit_trail"],
    "soft": ["cost_efficient", "self_hosted"],
    "budget_monthly": 5000,
    "team_size": 3
  }
}
```

**Output:**
```json
{
  "recommendations": [
    {
      "pattern": "Enterprise RAG with Hybrid Search",
      "score": 0.87,
      "monthly_cost_estimate": 3200,
      "constraints_met": ["gdpr_compliance", "audit_trail", "cost_efficient"],
      "components": ["pgvector", "Elasticsearch", "Cross-encoder", "Redis", "FastAPI"],
      "trade_offs": {
        "pros": ["Best quality retrieval", "Citation support", "GDPR-ready with self-hosted deployment"],
        "cons": ["Requires 3-5 devs (matches team size)", "Elasticsearch operational overhead"]
      },
      "security_analysis": {
        "gdpr": "Self-hosted pgvector keeps data in your infrastructure. No data leaves your VPC.",
        "data_residency": "All components support EU-region deployment.",
        "encryption": "PostgreSQL TDE + TLS in transit recommended."
      },
      "scalability": "Supports up to 10M documents, 100K queries/day. 2M conversations/month = ~67K/day, well within capacity.",
      "mermaid_diagram": "graph TD; A[API Gateway] --> B[RAG Engine]; B --> C[Query Router]; C --> D[Vector Search]; C --> E[BM25 Search]; D --> F[pgvector]; E --> G[Elasticsearch]; B --> H[Reranker]; B --> I[LLM Service]; B --> J[Redis Cache];"
    }
  ]
}
```

## Architecture Pattern Knowledge Base

The system ships with **20 architecture patterns** across 9 categories:

| Category | Patterns | Examples |
|----------|----------|----------|
| RAG | 3 | Basic RAG, Enterprise RAG, Serverless RAG |
| Agentic | 3 | Simple Agent, Agentic Workflow+HITL, Multi-Agent |
| Event Sourcing | 2 | Event-Sourced CQRS, Lightweight Events |
| Data | 3 | Data Lakehouse, Cloud Warehouse, Event Streaming |
| ML | 2 | ML Pipeline, Batch ML Inference |
| API | 2 | API Gateway, GraphQL Federation |
| Deployment | 3 | K8s Microservices, Serverless, Blue-Green |
| Security | 1 | Zero Trust Architecture |
| Multi-Cloud | 1 | Multi-Cloud Active-Active |

Each pattern includes:
- Component breakdown with specific technologies
- Cost models (base + per-unit pricing)
- Hard constraints satisfied/violated
- Trade-off analysis
- Maximum scale capability
- Team size requirements

## Reproducibility

**The same requirements always produce the same architecture.**

```python
from app.intelligence.pattern_kb import PatternKnowledgeBase
from app.intelligence.constraint_solver import ConstraintSolver

kb = PatternKnowledgeBase()
solver = ConstraintSolver(kb)

# This always returns the same result
result = solver.solve(
    hard_constraints=["audit_trail", "gdpr_compliance"],
    soft_constraints=["cost_efficient", "python_native"],
    preferred_tags=["agentic"],
)
# result["recommendations"] is deterministic
```

## Evaluation

We evaluate the system on **50 test cases** across:
- **Constraint satisfaction** — does the recommended pattern meet all hard constraints?
- **Cost accuracy** — how close are estimates to real cloud pricing?
- **Ranking quality** — is the best pattern ranked #1?
- **Explanation quality** — are trade-offs accurately described?

See `eval/` for the full evaluation dataset and `benchmarks/` for results.

## Methodology

This system is grounded in established software architecture research:

1. **Architecture Patterns** — Based on documented patterns from Martin Fowler, Sam Newman, and the Gang of Four, adapted for cloud-native AI systems
2. **Constraint Satisfaction** — Uses classical CSP (Constraint Satisfaction Problem) solving with hard/soft constraint classification
3. **Cost Modeling** — Based on real AWS/Azure/GCP pricing as of January 2025, updated quarterly
4. **Trade-off Analysis** — Uses structured decision matrices inspired by ATAM (Architecture Tradeoff Analysis Method)

## Limitations

- The pattern KB contains 20 patterns. It does not cover every possible architecture.
- Cost estimates are approximations. Real costs vary by usage patterns, reserved instances, and enterprise agreements.
- The system recommends patterns, not implementations. A pattern like "Event-Sourced CQRS" still requires significant engineering.
- Security analysis is high-level. It identifies GDPR implications but does not perform penetration testing.
- The constraint solver is deterministic but the explanation generator uses LLMs, so explanations may vary.

## Project Structure

```
ai-architecture-decision-engine/
├── app/
│   ├── intelligence/
│   │   ├── pattern_kb.py        # 20 architecture patterns with costs
│   │   └── constraint_solver.py  # Deterministic constraint solver
│   ├── api/      
