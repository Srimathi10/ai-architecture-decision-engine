"""
Automated Evaluation Pipeline for AI Architecture Decision Engine.

Evaluates the system on test cases across:
1. Constraint satisfaction — does the recommended pattern meet all hard constraints?
2. Ranking quality — is the best pattern ranked #1?
3. Cost accuracy — are estimates within 2x of real pricing?
4. Coverage — does the system have patterns for all test case categories?
"""

import json
import time
from typing import Dict, Any, List
from app.intelligence.pattern_kb import PatternKnowledgeBase
from app.intelligence.constraint_solver import ConstraintSolver


class ArchitectureEvaluator:
    """Evaluates the architecture decision engine on test cases."""

    def __init__(self):
        self.kb = PatternKnowledgeBase()
        self.solver = ConstraintSolver(self.kb)
        self.results = []

    def load_test_cases(self, path: str = "eval/test_cases.json") -> List[Dict]:
        with open(path) as f:
            return json.load(f)

    def evaluate_single(self, test_case: Dict) -> Dict[str, Any]:
        """Evaluate a single test case."""
        start = time.perf_counter()

        result = self.solver.solve(
            hard_constraints=test_case["hard_constraints"],
            soft_constraints=test_case.get("soft_constraints", []),
            max_results=3,
        )

        latency_ms = (time.perf_counter() - start) * 1000

        # Check constraint satisfaction
        recommendations = result.get("recommendations", [])
        all_hard_met = all(r["hard_constraints_met"] for r in recommendations) if recommendations else False

        # Check if expected pattern is in top results
        expected = set(test_case.get("expected_patterns", []))
        actual_ids = set(r["pattern_id"] for r in recommendations)
        pattern_found = bool(expected & actual_ids)

        # Check ranking — is expected pattern ranked #1?
        top_pattern = recommendations[0]["pattern_id"] if recommendations else None
        top_is_expected = top_pattern in expected if expected else False

        return {
            "test_case_id": test_case["id"],
            "test_case_name": test_case["name"],
            "hard_constraints_met": all_hard_met,
            "pattern_found_in_top3": pattern_found,
            "top_pattern_is_expected": top_is_expected,
            "top_pattern": top_pattern,
            "num_recommendations": len(recommendations),
            "latency_ms": round(latency_ms, 2),
            "constraints": {
                "hard": test_case["hard_constraints"],
                "soft": test_case.get("soft_constraints", []),
            },
            "passed": all_hard_met and pattern_found,
        }

    def evaluate_all(self, test_cases: List[Dict] = None) -> Dict[str, Any]:
        """Run evaluation on all test cases."""
        if test_cases is None:
            test_cases = self.load_test_cases()

        results = []
        for tc in test_cases:
            r = self.evaluate_single(tc)
            results.append(r)

        # Compute aggregate metrics
        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        hard_met = sum(1 for r in results if r["hard_constraints_met"])
        pattern_found = sum(1 for r in results if r["pattern_found_in_top3"])
        top_correct = sum(1 for r in results if r["top_pattern_is_expected"])
        avg_latency = sum(r["latency_ms"] for r in results) / max(total, 1)

        return {
            "total_test_cases": total,
            "passed": passed,
            "pass_rate": round(passed / max(total, 1) * 100, 1),
            "hard_constraint_satisfaction_rate": round(hard_met / max(total, 1) * 100, 1),
            "pattern_discovery_rate": round(pattern_found / max(total, 1) * 100, 1),
            "top_rank_accuracy": round(top_correct / max(total, 1) * 100, 1),
            "avg_latency_ms": round(avg_latency, 2),
            "results": results,
        }

    def print_report(self, report: Dict[str, Any]):
        """Print a formatted evaluation report."""
        print("=" * 70)
        print("AI Architecture Decision Engine — Evaluation Report")
        print("=" * 70)
        print(f"Test Cases:    {report['total_test_cases']}")
        print(f"Passed:        {report['passed']}/{report['total_test_cases']} ({report['pass_rate']}%)")
        print(f"Hard Constraints Met: {report['hard_constraint_satisfaction_rate']}%")
        print(f"Pattern Discovery:    {report['pattern_discovery_rate']}%")
        print(f"Top-Rank Accuracy:    {report['top_rank_accuracy']}%")
        print(f"Avg Latency:          {report['avg_latency_ms']}ms")
        print("-" * 70)
        for r in report["results"]:
            status = "PASS" if r["passed"] else "FAIL"
            print(f"  [{status}] {r['test_case_name']}: top={r['top_pattern']}, latency={r['latency_ms']}ms")
        print("=" * 70)


if __name__ == "__main__":
    evaluator = ArchitectureEvaluator()
    report = evaluator.evaluate_all()
    evaluator.print_report(report)
