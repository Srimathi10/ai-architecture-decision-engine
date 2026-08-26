"""Architecture Pattern Knowledge Base - 20+ patterns."""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum

class ConstraintType(str, Enum):
    HARD = "hard"
    SOFT = "soft"
    PREFERRED = "preferred"

@dataclass
class CostModel:
    component: str
    base_monthly: float
    per_unit: float
    unit: str
    notes: str = ""

@dataclass
class ArchitecturePattern:
    id: str
    name: str
    description: str
    components: List[Dict[str, Any]]
    cost_models: List[CostModel]
    constraints_satisfied: List[str]
    constraints_violated: List[str]
    trade_offs: Dict[str, Any]
    max_scale: str
    complexity: str
    team_size_required: str
    tags: List[str] = field(default_factory=list)

class PatternKnowledgeBase:
    def __init__(self):
        self._patterns: Dict[str, ArchitecturePattern] = {}
        self._load_all()

    def _load_all(self):
        P = ArchitecturePattern
        CM = CostModel
        self._patterns = {
            "rag-basic": P("rag-basic","Basic RAG","Vector search + LLM",[{"name":"Emb","tech":"OpenAI"}],[CM("Emb",0,0.00002,"tokens")],["self_hosted", "cost_efficient"],["gdpr_eu"],{"pros":["Simple"],"cons":["No reranking"]},"100K docs","low","1-2 devs",["rag"]),
            "rag-enterprise": P("rag-enterprise","Enterprise RAG","Hybrid search + reranking + citations",[{"name":"VS","tech":"pgvector"},{"name":"BM25","tech":"ES"},{"name":"Reranker","tech":"Cross-encoder"}],[CM("VS",150,0.15,"GB"),CM("BM25",200,0,"node")],["self_hosted","citations"],[],{"pros":["Best quality","Citations"],"cons":["Higher cost"]},"10M docs","high","3-5 devs",["rag","enterprise"]),
            "rag-serverless": P("rag-serverless","Serverless RAG","Lambda + Pinecone",[{"name":"Lambda","tech":"AWS"}],[CM("Lambda",0,0.0000002,"req")],["serverless"],["on_premise"],{"pros":["Zero ops"],"cons":["Lock-in"]},"1M/day","low","1 dev",["rag"]),
            "agentic-workflow": P("agentic-workflow","Agentic Workflow + HITL","LLM agents with human oversight",[{"name":"Engine","tech":"Custom"},{"name":"LLM","tech":"GPT-4o"},{"name":"HITL","tech":"Custom"}],[CM("Engine",100,0,"inst"),CM("LLM",0,0.03,"1K tok")],["audit_trail","human_oversight"],[],{"pros":["Full audit","Replay"],"cons":["Higher latency"]},"10K/day","high","3-5 devs",["agentic"]),
            "agentic-simple": P("agentic-simple","Simple Agent","Single LLM + tools",[{"name":"LLM","tech":"GPT-4o"}],[CM("LLM",0,0.03,"1K tok")],["python_native"],["audit_trail"],{"pros":["Simple"],"cons":["No audit"]},"100K/day","low","1 dev",["agentic"]),
            "agentic-multi": P("agentic-multi","Multi-Agent","Multiple agents + message bus",[{"name":"Orch","tech":"LangGraph"},{"name":"Bus","tech":"Kafka"}],[CM("Orch",150,0,"inst")],["complex_reasoning"],["simple_crud"],{"pros":["Complex tasks"],"cons":["High cost"]},"1K/day","very_high","4-6 devs",["agentic"]),
            "event-cqrs": P("event-cqrs","Event-Sourced CQRS","Events + projections + audit",[{"name":"EventStore","tech":"PG"},{"name":"Projections","tech":"Workers"}],[CM("Events",30,0.00005,"evt")],["audit_trail","time_travel"],["simple_crud"],{"pros":["Audit trail","Replay"],"cons":["Complexity"]},"1M evt/day","high","2-4 devs",["event-sourcing"]),
            "event-lightweight": P("event-lightweight","Lightweight Events","Event log in PostgreSQL",[{"name":"Log","tech":"PG append-only"}],[CM("Log",20,0.00001,"evt")],["audit_trail"],["high_write"],{"pros":["Simple","Cheap"],"cons":["Limited scale"]},"100K/day","medium","1-2 devs",["event-sourcing"]),
            "data-lakehouse": P("data-lakehouse","Data Lakehouse","Delta Lake batch+stream",[{"name":"Storage","tech":"S3"},{"name":"Compute","tech":"Spark"}],[CM("Storage",23,0.023,"GB")],["batch_streaming"],["real_time"],{"pros":["Unified"],"cons":["Complex"]},"10TB/day","high","3-5 devs",["data"]),
            "data-warehouse": P("data-warehouse","Cloud Warehouse","Snowflake/BigQuery",[{"name":"WH","tech":"Snowflake"}],[CM("WH",0,2,"credits")],["analytics"],["self_hosted"],{"pros":["Fast"],"cons":["Expensive"]},"1PB","medium","2-3 devs",["data"]),
            "streaming": P("streaming","Event Streaming","Kafka real-time",[{"name":"Broker","tech":"Kafka"}],[CM("Kafka",300,0,"cluster")],["real_time", "event_driven"],["simple_crud"],{"pros":["Real-time"],"cons":["Complex"]},"1M evt/sec","very_high","3-5 devs",["data"]),
            "ml-pipeline": P("ml-pipeline","ML Pipeline","End-to-end ML training",[{"name":"Train","tech":"SageMaker"}],[CM("Train",0,3,"GPU hr")],["ml_ops"],["low_cost"],{"pros":["Full MLOps"],"cons":["Expensive"]},"100K/day","high","3-5 devs",["ml"]),
            "ml-batch": P("ml-batch","Batch ML Inference","Scheduled scoring",[{"name":"Sched","tech":"Airflow"}],[CM("Comp",50,0,"inst")],["cost_efficient"],["real_time"],{"pros":["Cheap"],"cons":["Stale"]},"1M/day","low","1-2 devs",["ml"]),
            "api-gateway": P("api-gateway","API Gateway","Centralized gateway + auth",[{"name":"GW","tech":"Kong"}],[CM("GW",100,0,"inst")],["api_management"],["low_latency"],{"pros":["Centralized"],"cons":["SPOF"]},"100K rps","medium","2-3 devs",["api"]),
            "graphql-fed": P("graphql-fed","GraphQL Federation","Apollo distributed schema",[{"name":"Router","tech":"Apollo"}],[CM("Router",100,0,"inst")],["flexible_api"],["simple_crud"],{"pros":["Flexible"],"cons":["Complex"]},"50K rps","high","3-5 devs",["api"]),
            "k8s-micro": P("k8s-micro","K8s Microservices","Containerized on Kubernetes",[{"name":"K8s","tech":"Kubernetes"},{"name":"Mesh","tech":"Istio"}],[CM("K8s",300,0,"cluster")],["microservices","auto_scaling"],["simple_deploy"],{"pros":["Scalable"],"cons":["Complex"]},"10K pods","very_high","4-6 devs",["deployment"]),
            "serverless": P("serverless","Serverless Compute","Lambda event-driven",[{"name":"Lambda","tech":"AWS"}],[CM("Lambda",0,0.0000002,"req")],["serverless","low_ops"],["on_premise"],{"pros":["Zero ops"],"cons":["Cold starts"]},"1M/day","medium","1-2 devs",["deployment"]),
            "blue-green": P("blue-green","Blue-Green Deploy","Two envs + traffic switch",[{"name":"LB","tech":"ALB"}],[CM("Compute (2x)",0,2,"base")],["zero_downtime"],["cost_efficient"],{"pros":["Zero downtime"],"cons":["2x cost"]},"any","medium","2-3 devs",["deployment"]),
            "zero-trust": P("zero-trust","Zero Trust Security","Identity-centric security",[{"name":"IdP","tech":"OAuth2"},{"name":"Policy","tech":"OPA"}],[CM("IdP",100,0,"inst")],["security","compliance"],["simple_deploy"],{"pros":["Strong security"],"cons":["Complex"]},"any","very_high","3-5 devs",["security"]),
            "multi-cloud": P("multi-cloud","Multi-Cloud Active-Active","AWS + Azure global LB",[{"name":"AWS","tech":"ECS"},{"name":"Azure","tech":"Container Apps"}],[CM("AWS",500,0,"base"),CM("Azure",500,0,"base")],["multi_cloud","high_availability"],["cost_efficient"],{"pros":["No lock-in"],"cons":["2x cost"]},"1M users","very_high","5-8 devs",["multi-cloud"]),
        }

    def get_pattern(self, pid): return self._patterns.get(pid)
    def search_patterns(self, tags=None, complexity=None):
        r = list(self._patterns.values())
        if tags: r = [p for p in r if any(t in p.tags for t in tags)]
        if complexity: r = [p for p in r if p.complexity == complexity]
        return r
    def check_constraints(self, pid, required):
        pat = self._patterns.get(pid)
        if not pat: return {"valid": False}
        sat = [c for c in required if c in pat.constraints_satisfied]
        vio = [c for c in required if c in pat.constraints_violated]
        return {"pattern_id": pid, "valid": len(vio)==0, "satisfied": sat, "violated": vio, "satisfaction_rate": len(sat)/len(required) if required else 1.0}
    def estimate_cost(self, pid, scale):
        pat = self._patterns.get(pid)
        if not pat: return {"error": "not found"}
        total = 0; bd = []
        for cm in pat.cost_models:
            uc = scale.get(cm.unit, 0)
            c = cm.base_monthly + cm.per_unit * uc; total += c
            bd.append({"component": cm.component, "total": round(c,2)})
        return {"pattern": pat.name, "monthly_total": round(total,2), "breakdown": bd}
    def get_all_patterns(self):
        return [{"id":p.id,"name":p.name,"complexity":p.complexity,"tags":p.tags} for p in self._patterns.values()]

