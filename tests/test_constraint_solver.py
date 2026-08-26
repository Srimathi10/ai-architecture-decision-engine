"""Test suite for the AI Architecture Decision Engine constraint solver."""

import pytest
from app.intelligence.pattern_kb import PatternKnowledgeBase, ArchitecturePattern, CostModel
from app.intelligence.constraint_solver import ConstraintSolver


@pytest.fixture
def kb():
    return PatternKnowledgeBase()


@pytest.fixture
def solver(kb):
    return ConstraintSolver(kb)


class TestPatternKnowledgeBase:
    """Tests for the architecture pattern knowledge base."""

    def test_loads_patterns(self, kb):
        assert len(kb._patterns) == 20

    def test_get_pattern(self, kb):
        p = kb.get_pattern("rag-basic")
        assert p is not None
        assert p.name == "Basic RAG"
        assert p.complexity == "low"

    def test_get_nonexistent_pattern(self, kb):
        assert kb.get_pattern("nonexistent") is None

    def test_search_by_tags(self, kb):
        results = kb.search_patterns(tags=["rag"])
        assert len(results) >= 3
        assert all("rag" in p.tags for p in results)

    def test_search_by_complexity(self, kb):
        results = kb.search_patterns(complexity="low")
        assert len(results) >= 3
        assert all(p.complexity == "low" for p in results)

    def test_check_constraints_satisfied(self, kb):
        result = kb.check_constraints("rag-basic", ["self_hosted"])
        assert result["valid"] is True
        assert "self_hosted" in result["satisfied"]

    def test_check_constraints_violated(self, kb):
        result = kb.check_constraints("rag-basic", ["gdpr_eu"])
        assert result["valid"] is False
        assert "gdpr_eu" in result["violated"]

    def test_check_mixed_constraints(self, kb):
        result = kb.check_constraints("rag-basic", ["self_hosted", "gdpr_eu"])
        assert result["valid"] is False
        assert "self_hosted" in result["satisfied"]
        assert "gdpr_eu" in result["violated"]

    def test_estimate_cost(self, kb):
        cost = kb.estimate_cost("rag-basic", {"tokens": 1000000})
        assert cost["monthly_total"] > 0
        assert "breakdown" in cost

    def test_get_all_patterns(self, kb):
        patterns = kb.get_all_patterns()
        assert len(patterns) == 20
        assert all("id" in p and "name" in p for p in patterns)


class TestConstraintSolver:
    """Tests for the constraint solver."""

    def test_solve_with_hard_constraints(self, solver):
        result = solver.solve(
            hard_constraints=["audit_trail"],
            max_results=3,
        )
        assert len(result["recommendations"]) >= 1
        assert all(r["hard_constraints_met"] for r in result["recommendations"])

    def test_solve_with_multiple_hard_constraints(self, solver):
        result = solver.solve(
            hard_constraints=["audit_trail", "time_travel"],
            max_results=3,
        )
        # Only event-cqrs should satisfy both
        assert any(r["pattern_id"] == "event-cqrs" for r in result["recommendations"])

    def test_solve_with_soft_constraints(self, solver):
        result = solver.solve(
            hard_constraints=[],
            soft_constraints=["cost_efficient"],
            max_results=3,
        )
        assert len(result["recommendations"]) >= 1

    def test_solve_with_tags(self, solver):
        result = solver.solve(
            hard_constraints=[],
            preferred_tags=["agentic"],
            max_results=3,
        )
        assert len(result["recommendations"]) >= 1

    def test_solve_returns_cost_estimates(self, solver):
        result = solver.solve(
            hard_constraints=["audit_trail"],
            max_results=1,
        )
        rec = result["recommendations"][0]
        assert "cost_estimate" in rec
        assert rec["cost_estimate"]["monthly_total"] >= 0

    def test_solve_returns_trade_offs(self, solver):
        result = solver.solve(
            hard_constraints=["audit_trail"],
            max_results=1,
        )
        rec = result["recommendations"][0]
        assert "trade_offs" in rec
        assert "pros" in rec["trade_offs"]
        assert "cons" in rec["trade_offs"]

    def test_solve_deterministic(self, solver):
        """Same constraints always produce same recommendations."""
        r1 = solver.solve(hard_constraints=["audit_trail"], max_results=3)
        r2 = solver.solve(hard_constraints=["audit_trail"], max_results=3)
        assert [r["pattern_id"] for r in r1["recommendations"]] == \
               [r["pattern_id"] for r in r2["recommendations"]]

    def test_solve_impossible_constraints(self, solver):
        """No pattern satisfies impossible constraints."""
        result = solver.solve(
            hard_constraints=["nonexistent_constraint_xyz"],
            max_results=3,
        )
        assert len(result["recommendations"]) == 0
        assert result["confidence"] == 0.0

    def test_explain_decision(self, solver):
        explanation = solver.explain_decision("event-cqrs", ["audit_trail", "time_travel"])
        assert explanation["pattern"] == "Event-Sourced CQRS"
        assert "recommendation_rationale" in explanation
        assert "cost_breakdown" in explanation

    def test_explain_nonexistent_pattern(self, solver):
        explanation = solver.explain_decision("nonexistent", ["audit_trail"])
        assert "error" in explanation


class TestDeterminism:
    """Verify that the system is deterministic — critical for reproducibility."""

    def test_same_input_same_output(self, solver):
        """100 runs with same input produce identical output."""
        results = []
        for _ in range(100):
            r = solver.solve(
                hard_constraints=["security", "compliance"],
                soft_constraints=["cost_efficient"],
                max_results=3,
            )
            results.append([rec["pattern_id"] for rec in r["recommendations"]])
        # All 100 runs should be identical
        assert len(set(str(r) for r in results)) == 1

    def test_cost_estimates_stable(self, solver):
        """Cost estimates don't change between runs."""
        costs = []
        for _ in range(10):
            r = solver.solve(hard_constraints=["audit_trail"], max_results=1)
            costs.append(r["recommendations"][0]["cost_estimate"]["monthly_total"])
        assert len(set(costs)) == 1
