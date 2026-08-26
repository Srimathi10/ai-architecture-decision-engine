# Known Limitations

## Scope Limitations

1. **Pattern Coverage:** The knowledge base contains 20 patterns. Real-world architecture decisions may require patterns not yet in the KB. We welcome contributions of new patterns.

2. **Cost Accuracy:** Cost estimates are based on list pricing (January 2025). Real costs vary with reserved instances, enterprise agreements, spot instances, and usage patterns. Estimates are typically within 2-3x of actual costs.

3. **Pattern vs. Implementation:** The system recommends architecture patterns (e.g., "Event-Sourced CQRS"), not implementations. A pattern still requires significant engineering to implement.

## Technical Limitations

4. **Security Analysis:** Security analysis is high-level. It identifies GDPR/SOC2/HIPAA implications but does not perform penetration testing or vulnerability scanning.

5. **Explanation Variability:** The constraint solver is deterministic, but the explanation generator uses LLMs. Explanations for the same recommendation may vary between runs.

6. **No Real-Time Pricing:** Cost models are static. They do not fetch real-time cloud pricing from AWS/Azure/GCP APIs.

7. **No ML-Based Ranking:** The scoring formula is rule-based. A production system might use learned rankings from historical architecture decisions.

## Research Limitations

8. **Evaluation Dataset:** The 50 test cases are curated by the author. An independent evaluation by other architects would strengthen the claims.

9. **No User Study:** We have not conducted a user study comparing this system's recommendations to expert architects.

10. **No Comparison to Baselines:** We do not compare against existing ADR tools or LLM-only approaches in a formal benchmark.
