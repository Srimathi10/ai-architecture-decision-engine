# ADR-002: Make the Constraint Solver Deterministic

## Status

Accepted

## Context

LLM-based architecture generators produce different outputs for the same input. This makes them unsuitable for:
- Compliance audits (cannot prove the same decision was made)
- Regression testing (cannot verify no change in behavior)
- Debugging (cannot reproduce a problematic recommendation)

## Decision

The constraint solver uses no randomness, no LLM calls, and no external state. Given the same patterns and constraints, it always produces the same ranking.

## Consequences

**Positive:**
- Testable: we can write deterministic tests
- Debuggable: we can trace exactly why a pattern was selected
- Compliant: regulators can verify decision consistency

**Negative:**
- Cannot adapt to user preferences over time (without explicit retraining)
- Cannot incorporate real-time signals (e.g., current cloud pricing)
