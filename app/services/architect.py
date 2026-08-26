"""Architecture generation service — LLM-powered architecture design."""

import uuid
import json
from datetime import datetime
from typing import Dict, Any
import structlog
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.architecture import ArchitectureRequest, ArchStatus

logger = structlog.get_logger()

ARCHITECTURE_PROMPT = """You are a senior cloud architect. Given this business requirement, generate a comprehensive architecture recommendation.

Requirement: {requirement}
Constraints: {constraints}

Generate a JSON response with these sections:

1. "overview": 2-3 sentence architecture summary
2. "architecture_diagram": Mermaid diagram code (graph TD format)
3. "components": List of components with {name, purpose, technology, estimated_monthly_cost}
4. "technology_stack": {languages, frameworks, databases, messaging, monitoring, deployment}
5. "cost_estimate": {monthly_total, breakdown: [{item, cost, notes}], cost_optimization_tips: []}
6. "security_considerations": List of {area, recommendation, compliance_relevant: bool}
7. "trade_offs": List of {approach, pros: [], cons: [], recommended: bool}
8. "deployment_strategy": {approach, steps: [], estimated_timeline}
9. "risks": List of {risk, likelihood: low/medium/high, mitigation}
10. "scalability_notes": Performance considerations for scale

Return ONLY valid JSON."""


class ArchitectureEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate(self, requirement: str, constraints: Dict[str, Any] = None) -> ArchitectureRequest:
        """Generate architecture from a business requirement."""
        req = ArchitectureRequest(
            id=str(uuid.uuid4()),
            requirement=requirement,
            constraints=constraints or {},
            status=ArchStatus.GENERATING,
        )
        self.db.add(req)
        await self.db.commit()

        try:
            response = await self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert cloud architect. Return only valid JSON."},
                    {"role": "user", "content": ARCHITECTURE_PROMPT.format(
                        requirement=requirement,
                        constraints=json.dumps(constraints or {}, indent=2),
                    )},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            result = json.loads(response.choices[0].message.content)
            req.result = result
            req.status = ArchStatus.COMPLETED
            req.completed_at = datetime.utcnow()
            await self.db.commit()

            logger.info("architecture.complete", req_id=req.id, components=len(result.get("components", [])))
            return req

        except Exception as e:
            req.status = ArchStatus.FAILED
            req.error = str(e)
            await self.db.commit()
            logger.error("architecture.failed", req_id=req.id, error=str(e))
            raise

    async def compare_approaches(self, requirement: str, approaches: list[str]) -> Dict[str, Any]:
        """Compare multiple architectural approaches side by side."""
        response = await self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": "Compare these architectural approaches. Return valid JSON."},
                {"role": "user", "content": f"Requirement: {requirement}\n\nApproaches to compare: {json.dumps(approaches)}\n\nReturn JSON with comparison matrix, recommendation, and reasoning."},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
