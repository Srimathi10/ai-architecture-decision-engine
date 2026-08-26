# Research Methodology

## Approach

This system uses a **three-layer architecture** that separates concerns:

1. **Requirement Extraction** (LLM-powered) — Converts natural language into structured constraints
2. **Constraint Satisfaction** (Deterministic) — Filters and ranks patterns by hard/soft constraints
3. **Explanation Generation** (LLM-powered) — Produces human-readable justifications

This separation is intentional: the LLM handles language tasks, while the solver handles reasoning tasks. This makes the core decision logic **reproducible and auditable**.

## Constraint Satisfaction Problem (CSP)

The solver models architecture selection as a Constraint Satisfaction Problem:

- **Variables:** Architecture patterns from the knowledge base
- **Domain:** Binary (pattern satisfies constraints or not)
- **Hard constraints:** Must be satisfied (e.g., GDPR compliance, audit trail)
- **Soft constraints:** Preferably satisfied (e.g., low cost, Python-native)
- **Objective:** Maximize soft constraint satisfaction score

### Scoring Formula

```
score = soft_satisfaction_rate * 0.8 + tag_match_rate * 0.2
```

Where:
- `soft_satisfaction_rate` = number of soft constraints satisfied / total soft constraints
- `tag_match_rate` = number of matching tags / total preferred tags

### Why Deterministic?

The solver is deterministic by design. Given the same constraints, it always produces the same recommendations. This is critical for:
- **Reproducibility** — Researchers can verify results
- **Auditability** — Regulators can trace decisions
- **Debugging** — Engineers can identify why a recommendation was made

## Cost Modeling

Cost estimates use a structured cost model per pattern:

```python
CostModel(component, base_monthly, per_unit, unit)
```

For example, the "Enterprise RAG" pattern has:
- Vector Store: $150/mo base + $0.15/GB stored
- Elasticsearch: $200/mo (managed service)
- Reranker: $50/mo (GPU instance)

Total cost = sum of (base + per_unit * scale) for each component.

**Limitation:** These are approximate costs based on list pricing. Real costs vary with reserved instances, enterprise agreements, and usage patterns.

## Trade-off Analysis

Trade-offs are modeled as structured data:

```python
trade_offs = {
    "pros": ["Best quality retrieval", "Citation support"],
    "cons": ["Higher cost", "More infrastructure"],
    "alternatives": ["rag-basic", "rag-serverless"]
}
```

This enables:
- Side-by-side comparison of alternatives
- Cost/quality trade-off visualization
- Team capability matching

## Evaluation Methodology

We evaluate on 50 test cases across 4 dimensions:

1. **Constraint Satisfaction Rate** — Percentage of test cases where all hard constraints are met
2. **Pattern Discovery Rate** — Percentage where the expected pattern appears in top-3
3. **Top-Rank Accuracy** — Percentage where the expected pattern is ranked #1
4. **Latency** — Time to produce a recommendation (should be <100ms)

## Limitations

- The knowledge base contains 20 patterns. It does not cover every possible architecture.
- Cost estimates are approximations.
- The system recommends patterns, not implementations.
- Security analysis is high-level.
- The explanation generator uses LLMs, so explanations may vary between runs.
