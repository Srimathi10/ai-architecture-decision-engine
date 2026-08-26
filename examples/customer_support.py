"""
Example: Customer Support Architecture Decision

Demonstrates the full pipeline:
1. Define requirements
2. Run constraint solver
3. Get recommendations with costs and trade-offs
4. Generate Mermaid diagram
"""

from app.intelligence.pattern_kb import PatternKnowledgeBase
from app.intelligence.constraint_solver import ConstraintSolver

# Initialize
kb = PatternKnowledgeBase()
solver = ConstraintSolver(kb)

# Define requirements
result = solver.solve(
    hard_constraints=["gdpr_compliance", "audit_trail"],
    soft_constraints=["cost_efficient", "self_hosted", "python_native"],
    preferred_tags=["rag", "agentic"],
    max_results=3,
)

# Print results
print("=" * 60)
print("Architecture Decision: Customer Support Assistant")
print("=" * 60)
print(f"\nHard constraints: {result['query']['hard_constraints']}")
print(f"Soft constraints: {result['query']['soft_constraints']}")
print(f"Total candidates: {result['total_candidates']}")
print(f"Valid after hard filter: {result['valid_after_hard_filter']}")
print(f"Confidence: {result['confidence']}")

for i, rec in enumerate(result["recommendations"]):
    print(f"\n--- Recommendation {i+1}: {rec['name']} ---")
    print(f"  Score: {rec['score']}")
    print(f"  Hard constraints met: {rec['hard_constraints_met']}")
    print(f"  Complexity: {rec['complexity']}")
    print(f"  Max scale: {rec['max_scale']}")
    print(f"  Team size: {rec['team_size']}")
    print(f"  Monthly cost: ${rec['cost_estimate']['monthly_total']}")
    print(f"  Components: {', '.join(rec['components'])}")
    print(f"  Pros: {', '.join(rec['trade_offs']['pros'])}")
    print(f"  Cons: {', '.join(rec['trade_offs']['cons'])}")

# Get detailed explanation for top recommendation
if result["recommendations"]:
    top = result["recommendations"][0]
    explanation = solver.explain_decision(top["pattern_id"], result["query"]["hard_constraints"])
    print(f"\n--- Detailed Explanation for {explanation['pattern']} ---")
    print(f"  Rationale: {explanation['recommendation_rationale']}")
    print(f"  Components: {[c['name'] for c in explanation['architecture_components']]}")
    print(f"  Cost breakdown:")
    for item in explanation["cost_breakdown"]:
        print(f"    {item['component']}: ${item['base_monthly']}/mo base + ${item['per_unit']}/{item['unit']}")
