# ADR-001: Use a Pattern Knowledge Base Instead of LLM-Only Generation

## Status

Accepted

## Context

Architecture decisions are typically made by:
1. Asking an LLM (hallucination risk, no constraint validation)
2. Following blog posts (opinionated, not tailored)
3. Hiring consultants (expensive, not reproducible)

## Decision

We use a **structured knowledge base** of 20 architecture patterns with:
- Hard/soft constraint annotations
- Cost models per component
- Trade-off analysis
- Maximum scale capabilities

The LLM is used only for:
- Extracting requirements from natural language
- Generating human-readable explanations

The constraint solver is **deterministic** — same inputs always produce same outputs.

## Consequences

**Positive:**
- Reproducible: same requirements → same architecture
- Auditable: constraint satisfaction is verifiable
- Cost-aware: estimates come from structured data, not hallucination

**Negative:**
- Limited to patterns in the KB (20 currently)
- Cannot handle novel architecture patterns
- Cost estimates are approximations
