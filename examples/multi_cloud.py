"""
Example: Multi-Cloud Architecture Decision

Use case: Deploy across AWS + Azure for disaster recovery.
"""

from app.intelligence.pattern_kb import PatternKnowledgeBase
from app.intelligence.constraint_solver import ConstraintSolver

kb = PatternKnowledgeBase()
solver = ConstraintSolver(kb)

result = solver.solve(
    hard_constraints=["multi_cloud", "high_availability"],
    soft_constraints=[],
    max_results=3,
)

print("Architecture Decision: Multi-Cloud HA")
print("=" * 50)
for rec in result["recommendations"]:
    print(f"\n{rec['name']} (score: {rec['score']})")
    print(f"  Cost: ${rec['cost_estimate']['monthly_total']}/mo")
    print(f"  Max scale: {rec['max_scale']}")
    print(f"  Security: {rec['trade_offs']['pros']}")
