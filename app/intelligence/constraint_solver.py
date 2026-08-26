"""
Constraint Solver — finds valid architectures given hard/soft constraints.

This is the genuine architectural reasoning engine:
1. Takes a set of hard constraints (must satisfy) and soft constraints (prefer)
2. Filters patterns by hard constraint satisfaction
3. Ranks remaining patterns by soft constraint score
4. Returns top-N recommendations with cost estimates

WHAT MAKES THIS DIFFERENT FROM JUST ASKING GPT:
- The LLM generates the REQUIREMENTS. The solver VALIDATES them.
- The solver can prove that no valid architecture exists for impossible constraints
- Cost estimates come from the knowledge base, not hallucinated numbers
- The output is reproducible: same constraints always produce same results
"""

from typing import Dict, Any, List, Optional
from app.intelligence.pattern_kb import PatternKnowledgeBase, ConstraintType


class ConstraintSolver:
    """
    Finds and ranks architecture patterns that satisfy given constraints.
    
    This is deterministic: given the same constraints, it always produces
    the same recommendations. The LLM is used for requirement extraction,
    not architecture generation.
    """

    def __init__(self, kb: PatternKnowledgeBase = None):
        self.kb = kb or PatternKnowledgeBase()

    def solve(
        self,
        hard_constraints: List[str],
        soft_constraints: List[str] = None,
        preferred_tags: List[str] = None,
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        Find architectures that satisfy all hard constraints.
        
        Args:
            hard_constraints: Must be satisfied (e.g., ["audit_trail_required", "gdpr_compliance"])
            soft_constraints: Preferably satisfied (e.g., ["low_cost", "python_native"])
            preferred_tags: Filter by tags (e.g., ["rag", "enterprise"])
            max_results: Maximum number of recommendations
        """
        soft_constraints = soft_constraints or []
        preferred_tags = preferred_tags or []

        # Step 1: Filter by tags if specified
        candidates = self.kb.search_patterns(tags=preferred_tags if preferred_tags else None)

        # Step 2: Filter by hard constraints
        valid = []
        for pattern in candidates:
            check = self.kb.check_constraints(pattern.id, hard_constraints)
            if check["valid"]:
                valid.append((pattern, check))

        # Step 3: Score by soft constraint satisfaction
        scored = []
        for pattern, hard_check in valid:
            soft_check = self.kb.check_constraints(pattern.id, soft_constraints)
            score = soft_check["satisfaction_rate"]
            
            # Bonus for matching tags
            if preferred_tags:
                tag_match = len(set(pattern.tags) & set(preferred_tags)) / len(preferred_tags)
                score += tag_match * 0.2

            scored.append({
                "pattern": pattern,
                "hard_satisfaction": hard_check["satisfaction_rate"],
                "soft_satisfaction": soft_check["satisfaction_rate"],
                "score": round(score, 4),
            })

        # Step 4: Sort by score and take top N
        scored.sort(key=lambda x: x["score"], reverse=True)
        top = scored[:max_results]

        # Step 5: Build recommendations
        recommendations = []
        for item in top:
            p = item["pattern"]
            recommendations.append({
                "pattern_id": p.id,
                "name": p.name,
                "description": p.description,
                "score": item["score"],
                "hard_constraints_met": item["hard_satisfaction"] == 1.0,
                "soft_constraints_met": round(item["soft_satisfaction"] * 100),
                "complexity": p.complexity,
                "max_scale": p.max_scale,
                "team_size": p.team_size_required,
                "trade_offs": p.trade_offs,
                "components": [c["name"] for c in p.components],
                "cost_estimate": self.kb.estimate_cost(p.id, {"tokens": 1000000, "1K tokens": 100}),
            })

        return {
            "query": {
                "hard_constraints": hard_constraints,
                "soft_constraints": soft_constraints,
                "preferred_tags": preferred_tags,
            },
            "total_candidates": len(candidates),
            "valid_after_hard_filter": len(valid),
            "recommendations": recommendations,
            "confidence": self._compute_confidence(recommendations),
        }

    def explain_decision(self, pattern_id: str, hard_constraints: List[str]) -> Dict[str, Any]:
        """Generate a detailed explanation of why this pattern was recommended."""
        pattern = self.kb.get_pattern(pattern_id)
        if not pattern:
            return {"error": "Pattern not found"}

        check = self.kb.check_constraints(pattern_id, hard_constraints)
        
        return {
            "pattern": pattern.name,
            "recommendation_rationale": f"'{pattern.name}' satisfies {len(check['satisfied'])}/{len(hard_constraints)} hard constraints.",
            "constraints_analysis": {
                "satisfied": [
                    {"constraint": c, "explanation": f"Pattern includes components that satisfy '{c}'"}
                    for c in check["satisfied"]
                ],
                "violated": [
                    {"constraint": c, "explanation": f"Pattern does not address '{c}' — may require additional components"}
                    for c in check["violated"]
                ],
            },
            "architecture_components": pattern.components,
            "cost_breakdown": [
                {"component": cm.component, "base_monthly": cm.base_monthly, "per_unit": cm.per_unit, "unit": cm.unit}
                for cm in pattern.cost_models
            ],
            "trade_offs": pattern.trade_offs,
            "implementation_notes": {
                "complexity": pattern.complexity,
                "team_size": pattern.team_size_required,
                "max_scale": pattern.max_scale,
            },
        }

    def _compute_confidence(self, recommendations: List[Dict]) -> float:
        """Compute confidence score based on how many candidates matched."""
        if not recommendations:
            return 0.0
        avg_score = sum(r["score"] for r in recommendations) / len(recommendations)
        hard_met = sum(1 for r in recommendations if r["hard_constraints_met"]) / len(recommendations)
        return round(avg_score * 0.5 + hard_met * 0.5, 4)
