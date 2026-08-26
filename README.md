# AI Architecture Decision Engine

**Generate and Evaluate AI/Cloud Architectures from Business Requirements**

Given a business requirement, generate architecture diagrams, technology recommendations, cost estimates, security considerations, and trade-off analyses.

## Example

**Input:** "Build a customer-support assistant for 2M conversations/month with GDPR requirements"

**Output:**
- Architecture diagram (Mermaid)
- Technology stack recommendations
- Estimated monthly cost ($X,XXX)
- Security & compliance considerations
- Performance trade-offs
- Deployment strategy

## Features

- **Architecture generation** — LLM-powered architecture design from requirements
- **Technology recommendations** — Context-aware tech stack suggestions
- **Cost estimation** — Monthly cost projections based on usage
- **Security analysis** — GDPR, HIPAA, SOC2 compliance considerations
- **Trade-off analysis** — Pros/cons of different approaches
- **Architecture diagrams** — Auto-generated Mermaid diagrams
- **Export** — PDF/Markdown export of architecture documents

## Tech Stack

- **Backend:** Python 3.11+, FastAPI
- **LLM:** OpenAI GPT-4o
- **Database:** PostgreSQL 15+
- **Deploy:** Docker

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## License

MIT
