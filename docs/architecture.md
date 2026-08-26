# System Architecture — AI Architecture Decision Engine

## Overview

The AI Architecture Decision Engine is a three-layer system that transforms natural-language enterprise requirements into deterministic, auditable, cost-modeled architecture decisions.

```
┌──────────────────────────────────────────────────────────────────┐
│                    CLIENT / API LAYER                             │
│  FastAPI + Pydantic schemas + OpenAPI docs                       │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│               INTELLIGENCE LAYER (Core Reasoning)                │
│                                                                  │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │ Requirement   │  │ Constraint       │  │ Pattern          │   │
│  │ Parser (LLM)  │→ │ Solver (Determin.)│→ │ Knowledge Base   │   │
│  │              │  │                  │  │ (20 patterns)     │   │
│  └──────────────┘  └──────────────────┘  └──────────────────┘   │
│         │                    │                     │             │
│         ▼                    ▼                     ▼             │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │ Cost Modeler  │  │ Security/GDPR    │  │ Mermaid Diagram  │   │
│  │              │  │ Analyzer         │  │ Generator        │   │
│  └──────────────┘  └──────────────────┘  └──────────────────┘   │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                     │
│  PostgreSQL (patterns, evaluations, decisions)                   │
│  Redis (caching for repeated queries)                            │
└──────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Pattern Knowledge Base (`app/intelligence/pattern_kb.py`)

**What it is:** A curated database of 20 architecture patterns, each with:
- Component specifications (technology, cost, role)
- Cost models (base monthly + per-unit pricing)
- Hard constraints satisfied/violated
- Trade-off analysis (pros/cons)
- Scalability limits and team size requirements

**Why this matters:** Unlike LLM-generated suggestions, these patterns are deterministic — the same constraints always produce the same recommendations. The cost models are based on real AWS/Azure pricing, not hallucinated numbers.

**Pattern categories:**
| Category | Patterns | Example |
|----------|----------|---------|
| RAG | 3 | Basic RAG, Enterprise RAG, Serverless RAG |
| Agentic | 3 | Simple Agent, Agentic+HITL, Multi-Agent |
| Event Sourcing | 2 | Full CQRS, Lightweight Events |
| Data | 3 | Lakehouse, Cloud Warehouse, Event Streaming |
| ML | 2 | Full Pipeline, Batch Inference |
| API | 2 | API Gateway, GraphQL Federation |
| Deployment | 3 | K8s Microservices, Serverless, Blue-Green |
| Security | 1 | Zero Trust |
| Multi-Cloud | 1 | Multi-Cloud Active-Active |

### 2. Constraint Solver (`app/intelligence/constraint_solver.py`)

**Algorithm:**
```
Input: hard_constraints, soft_constraints, preferred_tags

1. candidates ← KB.search_patterns(tags=preferred_tags)
2. valid ← []
3. FOR each candidate:
     check ← KB.check_constraints(candidate, hard_constraints)
     IF check.violated == [] AND check.satisfied == hard_constraints:
       valid.append(candidate)
4. scored ← []
5. FOR each valid candidate:
     soft_score ← KB.check_constraints(candidate, soft_constraints).satisfaction_rate
     tag_score ← set(candidate.tags) ∩ preferred_tags / |preferred_tags|
     score ← soft_score + tag_score * 0.2
     scored.append((candidate, score))
6. RETURN scored.sort_by(score).top_n(max_results)
```

**Key property:** This is fully deterministic. Given the same constraints, the solver always produces the same output. No randomness, no LLM calls, no temperature parameter.

### 3. Cost Modeler

Each pattern includes cost models with:
- **Base monthly cost** (fixed infrastructure)
- **Per-unit cost** (tokens, requests, storage, compute hours)
- **Unit definitions** (what each unit represents)

The cost modeler multiplies per-unit costs by user-provided scale parameters to produce estimates.

### 4. Evaluation Pipeline (`eval/`)

**Test cases** (`eval/test_cases.json`): 10 enterprise scenarios covering:
- Event sourcing with audit trail
- Multi-cloud disaster recovery
- Zero trust healthcare
- Real-time event streaming
- ML training pipeline
- Agentic workflow with HITL
- Kubernetes auto-scaling
- Cost-efficient self-hosted RAG
- Serverless low-ops
- Zero downtime deployment

**Metrics:**
- **Constraint satisfaction rate:** % of test cases where the solver finds a valid pattern
- **Top-rank accuracy:** % of test cases where the best pattern is ranked #1
- **Latency:** Average solver time (target: <1ms)

**Current results:**
- 10/10 test cases pass (100%)
- Average latency: 0.07ms
- All hard constraints satisfied in all test cases

## Design Decisions

### Why Deterministic, Not LLM-Based?

| Approach | Pros | Cons |
|----------|------|------|
| LLM-only | Fast to build, flexible | Hallucinated costs, non-reproducible, no constraint validation |
| Deterministic solver | Reproducible, auditable, constraint-validated | Requires curated pattern KB, less flexible |
| **Hybrid (our approach)** | LLM extracts requirements, solver makes decisions | Requires both LLM and KB |

**Decision:** The LLM handles requirement extraction (understanding natural language). The solver handles architecture decisions (filtering, ranking, cost estimation). This separation means:
- Architecture decisions are reproducible
- Cost estimates come from real data, not hallucinations
- Constraint violations are provably caught
- The system can explain *why* it rejected alternatives

### Why 20 Patterns?

The pattern KB covers the most common enterprise architecture decisions:
- RAG (3 variants) — most common AI integration pattern
- Agentic (3 variants) — growing category for workflow automation
- Event sourcing (2 variants) — audit/compliance scenarios
- Data (3 variants) — analytics and streaming
- ML (2 variants) — model training and inference
- API (2 variants) — service composition
- Deployment (3 variants) — infrastructure patterns
- Security (1) — zero trust for regulated industries
- Multi-cloud (1) — disaster recovery and vendor neutrality

**Future:** The KB is extensible — adding a new pattern is a single dataclass entry.

## Data Flow

```
User Request
    │
    ▼
POST /api/architectures/analyze
    │
    ▼
Requirement Parser (LLM)
    │  Extracts: constraints, budget, team_size, tags
    ▼
Constraint Solver
    │  1. Search patterns by tags
    │  2. Filter by hard constraints
    │  3. Score by soft constraints
    │  4. Rank by composite score
    ▼
Cost Modeler
    │  Estimate monthly cost per recommendation
    ▼
Response
    {
      recommendations: [...],
      confidence: 0.85,
      rejected_alternatives: [...],
      cost_estimates: {...}
    }
```

## Security Considerations

- No user data is stored beyond the current session
- LLM calls use Azure OpenAI (data not used for training)
- Cost models are local (no external API calls for pricing)
- All decisions are audit-logged

## Limitations

See [docs/limitations.md](limitations.md) for known limitations including:
- Pattern KB is manually curated (not automatically learned)
- Cost models are approximate (not real-time pricing)
- No learning from user feedback yet
- Limited to 20 patterns (extensible but requires manual addition)
