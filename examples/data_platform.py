"""
Example: Data Platform Architecture Decision

Use case: Build a data lakehouse for batch and streaming analytics.
"""

from app.intelligence.pattern_kb import PatternKnowledgeBase
from app.intelligence.constraint_solver import ConstraintSolver

kb = PatternKnowledgeBase()
solver = ConstraintSolver(kb)

# Data platform requirements
result = solver.solve(
    hard_constraints=["batch_streaming", "schema_evolution"],
    soft_constraints=["analytics", "sql_native"],
    preferred_tags=["data"],
    max_results=3,
)

print("Architecture Decision: Data Platform")
print("=" * 50)
for rec in result["recommendations"]:
    print(f"\n{rec['name']} (score: {rec['score']})")
    print(f"  Cost: ${rec['cost_estimate']['monthly_total']}/mo")
    print(f"  Components: {', '.join(rec['components'])}")
    print(f"  Trade-offs: {rec['trade_offs']['pros']} vs {rec['trade_offs']['cons']}")
