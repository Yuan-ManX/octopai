"""
Octopai Backend API

The main API server for Octopai, providing endpoints for:
- Skill Creator (create and manage skills)
- Skill Evolution (Feedback Descent optimization)
- Skills Hub (skill marketplace and management)
- OctoTrace (cost and performance tracking)
- Skill Wiki (knowledge management)
- AutoSkill (autonomous research and optimization)

All core logic is imported from the octopai package.
"""
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

# Add project root to path for octopai import
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# Import core functionality from octopai package
try:
    from octopai import (
        # Skill Evolution
        SkillEvolutionEngine,
        SelectionStrategy,
        EvolutionMode,
        FrontierManager,
        FeedbackDescentOptimizer,

        # Skills
        SkillCreator,
        SkillRegistry,
        SkillMetadata,
        Skill,
        SkillHub,

        # Tracing
        OctoTracer,
        CostTracker,

        # Skills Hub
        HubManager as SkillsHubManager,
    )
    octopai_available = True
except ImportError as e:
    print(f"Warning: octopai package not fully available: {e}")
    octopai_available = False
    # Set all to None as fallback
    SkillEvolutionEngine = None
    SelectionStrategy = None
    EvolutionMode = None
    FrontierManager = None
    FeedbackDescentOptimizer = None
    SkillCreator = None
    SkillRegistry = None
    SkillMetadata = None
    Skill = None
    SkillHub = None
    OctoTracer = None
    CostTracker = None
    SkillsHubManager = None


# Initialize app
app = FastAPI(
    title="Octopai API",
    description="The Infinite Evolution Intelligence Engine for AI Agents",
    version="4.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Initialize core systems from octopai
if octopai_available:
    try:
        # Initialize skill registry
        skill_registry = SkillRegistry(
            storage_path=DATA_DIR / "registry"
        )

        # Initialize skills hub manager
        skills_hub_manager = SkillsHubManager(
            storage_dir=DATA_DIR / "skillshub"
        )

        # Initialize tracer and cost tracker
        tracer = OctoTracer(
            config={"storage": "in-memory"}
        )
        cost_tracker = CostTracker()

    except Exception as e:
        print(f"Warning: Some octopai components not fully initialized: {e}")
        # Create simple in-memory storages as fallback
        skill_registry = None
        skills_hub_manager = None
        tracer = None
        cost_tracker = None
else:
    # Create simple in-memory storages as fallback
    skill_registry = None
    skills_hub_manager = None
    tracer = None
    cost_tracker = None

# Active evolution processes
active_evolution: Dict[str, Any] = {}
active_experiments: Dict[str, Any] = {}

# In-memory storage as fallback
skills_storage: Dict[str, Dict] = {}
programs_storage: Dict[str, Dict] = {}
experiments_storage: Dict[str, Dict] = {}
feedback_storage: List[Dict] = []


# ==========================================
# Pydantic Models for Request/Response
# ==========================================

class SkillCreateRequest(BaseModel):
    name: str = Field(..., description="Skill name")
    description: str = Field(..., description="Skill description")
    content: str = Field(..., description="Skill content/code")
    category: str = Field(default="general", description="Skill category")
    author: str = Field(default="anonymous", description="Author name")
    version: str = Field(default="1.0.0", description="Semantic version")
    namespace: str = Field(default="global", description="Namespace to create skill in")
    visibility: str = Field(default="private", description="Visibility: public, private, internal")
    topics: Optional[List[str]] = Field(default_factory=list, description="Related topics")


class EvolutionStartRequest(BaseModel):
    skill_id: Optional[str] = None
    skill_name: Optional[str] = None
    selection_strategy: str = "best"
    evolution_mode: str = "hybrid"
    frontier_size: int = 3
    max_iterations: int = 50


class ExperimentCreateRequest(BaseModel):
    name: str
    description: str
    goal: str
    config: Dict[str, Any] = {}


class NamespaceCreateRequest(BaseModel):
    name: str = Field(..., description="Namespace name")
    owner_id: str = Field(..., description="Owner user ID")
    description: str = Field(default="", description="Namespace description")
    namespace_type: str = Field(default="team", description="Type: global or team")


class SkillVersionCreateRequest(BaseModel):
    version: str = Field(..., description="Semantic version string")
    content: str = Field(..., description="Skill content")
    changelog: str = Field(default="", description="What changed in this version")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class ReviewApproveRequest(BaseModel):
    reviewer_id: str = Field(..., description="Reviewer user ID")
    comment: str = Field(default="", description="Review comment")


class ReviewRejectRequest(BaseModel):
    reviewer_id: str = Field(..., description="Reviewer user ID")
    reason: str = Field(..., description="Reason for rejection")


class PromotionRequestCreate(BaseModel):
    source_skill_id: str = Field(..., description="Source skill ID")
    source_version_id: str = Field(..., description="Source version ID")
    submitter_id: str = Field(..., description="Submitter user ID")
    target_namespace_id: str = Field(default="global", description="Target namespace (usually global)")


class SkillRatingRequest(BaseModel):
    user_id: str = Field(..., description="User ID")
    score: int = Field(..., ge=1, le=5, description="Rating 1-5")


# ==========================================
# WebSocket Connection Manager
# ==========================================

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass


manager = ConnectionManager()


# ==========================================
# Root & Health Endpoints
# ==========================================

@app.get("/")
async def root():
    return {
        "message": "Octopai API v4.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "api": "/api/*"
        }
    }


@app.get("/api/status")
async def get_status():
    return {
        "status": "ok",
        "octopai": {
            "version": "4.0.0",
            "available": octopai_available,
            "components": {
                "skill_registry": skill_registry is not None,
                "skills_hub_manager": skills_hub_manager is not None,
                "tracer": tracer is not None,
                "cost_tracker": cost_tracker is not None
            }
        },
        "timestamp": datetime.now().isoformat()
    }


# ==========================================
# Skill Creator Endpoints
# ==========================================

@app.post("/api/skills")
async def create_skill(request: SkillCreateRequest):
    """Create a new skill"""
    skill_id = f"skill_{int(datetime.now().timestamp())}"

    skill_data = {
        "id": skill_id,
        "name": request.name,
        "description": request.description,
        "content": request.content,
        "category": request.category,
        "author": request.author,
        "version": request.version,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "likes": 0,
        "downloads": 0
    }

    skills_storage[skill_id] = skill_data

    # Try to use Skills Hub Manager if available
    if skills_hub_manager:
        try:
            skill = skills_hub_manager.create_skill(
                namespace_id=request.namespace,
                name=request.name,
                owner_id=request.author,
                summary=request.description,
                visibility=request.visibility,
                category=request.category,
                topics=request.topics
            )
            skills_hub_manager.create_version(
                skill_id=skill.id,
                version=request.version,
                content=request.content,
                created_by=request.author
            )
            skill_data["hub_skill_id"] = skill.id
        except Exception as e:
            print(f"Skills Hub creation failed: {e}")

    return {"success": True, "skill": skill_data}


@app.get("/api/skills")
async def list_skills(category: Optional[str] = None, namespace: Optional[str] = None):
    """List all skills, optionally filtered by category"""
    # Use Skills Hub if available
    if skills_hub_manager:
        skills_list = skills_hub_manager.list_skills(namespace_id=namespace, category=category)
        return {"skills": [s.model_dump() for s in skills_list], "count": len(skills_list)}

    # Fallback to in-memory storage
    skills_list = list(skills_storage.values())
    if category:
        skills_list = [s for s in skills_list if s.get("category") == category]
    return {"skills": skills_list, "count": len(skills_list)}


@app.get("/api/skills/{skill_id}")
async def get_skill(skill_id: str):
    """Get a specific skill by ID"""
    if skills_hub_manager:
        skill = skills_hub_manager.get_skill(skill_id)
        if skill:
            return {"skill": skill.model_dump()}
        raise HTTPException(status_code=404, detail="Skill not found")

    if skill_id not in skills_storage:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"skill": skills_storage[skill_id]}


@app.put("/api/skills/{skill_id}")
async def update_skill(skill_id: str, request: SkillCreateRequest):
    """Update an existing skill"""
    if skills_hub_manager:
        updated = skills_hub_manager.update_skill(
            skill_id=skill_id,
            display_name=request.name,
            summary=request.description,
            category=request.category,
            topics=request.topics
        )
        if updated:
            return {"success": True, "skill": updated.model_dump()}
        raise HTTPException(status_code=404, detail="Skill not found")

    if skill_id not in skills_storage:
        raise HTTPException(status_code=404, detail="Skill not found")

    skills_storage[skill_id].update({
        "name": request.name,
        "description": request.description,
        "content": request.content,
        "category": request.category,
        "version": request.version,
        "updated_at": datetime.now().isoformat()
    })
    return {"success": True, "skill": skills_storage[skill_id]}


@app.delete("/api/skills/{skill_id}")
async def delete_skill(skill_id: str, deleter_id: str = "anonymous"):
    """Delete a skill"""
    if skills_hub_manager:
        success = skills_hub_manager.delete_skill(skill_id, deleter_id)
        if success:
            return {"success": True}
        raise HTTPException(status_code=404, detail="Skill not found")

    if skill_id not in skills_storage:
        raise HTTPException(status_code=404, detail="Skill not found")
    del skills_storage[skill_id]
    return {"success": True}


# ==========================================
# Skill Evolution Endpoints
# ==========================================

@app.post("/api/evolution/start")
async def start_evolution(request: EvolutionStartRequest):
    """Start a skill evolution process"""
    run_id = f"evo_{int(datetime.now().timestamp())}"

    evolution_data = {
        "id": run_id,
        "skill_id": request.skill_id,
        "skill_name": request.skill_name,
        "selection_strategy": request.selection_strategy,
        "evolution_mode": request.evolution_mode,
        "frontier_size": request.frontier_size,
        "max_iterations": request.max_iterations,
        "status": "running",
        "current_iteration": 0,
        "created_at": datetime.now().isoformat()
    }

    active_evolution[run_id] = evolution_data

    # Notify via WebSocket
    await manager.broadcast({
        "type": "evolution_started",
        "data": evolution_data
    })

    return {"success": True, "evolution": evolution_data}


@app.post("/api/evolution/{run_id}/stop")
async def stop_evolution(run_id: str):
    """Stop a running evolution process"""
    if run_id not in active_evolution:
        raise HTTPException(status_code=404, detail="Evolution run not found")

    active_evolution[run_id]["status"] = "stopped"

    await manager.broadcast({
        "type": "evolution_stopped",
        "data": {"id": run_id}
    })

    return {"success": True}


@app.get("/api/evolution/{run_id}")
async def get_evolution_status(run_id: str):
    """Get status of an evolution run"""
    if run_id not in active_evolution:
        raise HTTPException(status_code=404, detail="Evolution run not found")

    return {"evolution": active_evolution[run_id]}


@app.get("/api/evolution/frontier")
async def get_frontier():
    """Get current evolution frontier"""
    # Mock frontier data
    frontier = [
        {
            "id": "variant_1",
            "score": 0.92,
            "generation": 3,
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "variant_2",
            "score": 0.87,
            "generation": 2,
            "created_at": datetime.now().isoformat()
        }
    ]
    return {"frontier": frontier}


@app.get("/api/evolution/programs")
async def list_programs():
    """List all evolution programs"""
    return {"programs": list(programs_storage.values())}


# ==========================================
# Skills Hub Endpoints (Enhanced)
# ==========================================

@app.get("/api/skillshub/stats")
async def get_hub_stats():
    """Get Skills Hub statistics"""
    if skills_hub_manager:
        stats = skills_hub_manager.get_statistics()
        return stats.model_dump()

    return {
        "total_skills": len(skills_storage),
        "total_likes": sum(s.get("likes", 0) for s in skills_storage.values()),
        "total_downloads": sum(s.get("downloads", 0) for s in skills_storage.values()),
        "active_users": 1
    }


@app.get("/api/skillshub/namespaces")
async def list_namespaces(user_id: Optional[str] = None, namespace_type: Optional[str] = None):
    """List all namespaces"""
    if skills_hub_manager:
        namespaces = skills_hub_manager.list_namespaces(user_id=user_id, namespace_type=namespace_type)
        return {"namespaces": [ns.model_dump() for ns in namespaces], "count": len(namespaces)}
    return {"namespaces": [], "count": 0}


@app.post("/api/skillshub/namespaces")
async def create_namespace(request: NamespaceCreateRequest):
    """Create a new namespace"""
    if not skills_hub_manager:
        raise HTTPException(status_code=500, detail="Skills Hub not available")

    try:
        namespace = skills_hub_manager.create_namespace(
            name=request.name,
            owner_id=request.owner_id,
            description=request.description,
            namespace_type=request.namespace_type
        )
        return {"success": True, "namespace": namespace.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/skillshub/namespaces/{namespace_id}")
async def get_namespace(namespace_id: str):
    """Get namespace details"""
    if not skills_hub_manager:
        raise HTTPException(status_code=500, detail="Skills Hub not available")
    namespace = skills_hub_manager.get_namespace(namespace_id)
    if not namespace:
        raise HTTPException(status_code=404, detail="Namespace not found")
    return {"namespace": namespace.model_dump()}


@app.post("/api/skillshub/skills/{skill_id}/versions")
async def create_skill_version(skill_id: str, request: SkillVersionCreateRequest):
    """Create a new skill version"""
    if not skills_hub_manager:
        raise HTTPException(status_code=500, detail="Skills Hub not available")

    try:
        version = skills_hub_manager.create_version(
            skill_id=skill_id,
            version=request.version,
            content=request.content,
            created_by="anonymous",
            changelog=request.changelog,
            metadata=request.metadata
        )
        return {"success": True, "version": version.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/skillshub/skills/{skill_id}/versions/{version_id}/submit")
async def submit_version_for_review(version_id: str, submitter_id: str = "anonymous"):
    """Submit a version for review"""
    if not skills_hub_manager:
        raise HTTPException(status_code=500, detail="Skills Hub not available")

    try:
        version = skills_hub_manager.submit_for_review(version_id, submitter_id)
        if version:
            return {"success": True, "version": version.model_dump()}
        raise HTTPException(status_code=404, detail="Version not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/skillshub/reviews/pending")
async def get_pending_reviews(namespace_id: Optional[str] = None):
    """Get pending review tasks"""
    if not skills_hub_manager:
        return {"reviews": [], "count": 0}
    reviews = skills_hub_manager.get_pending_reviews(namespace_id=namespace_id)
    return {"reviews": [r.model_dump() for r in reviews], "count": len(reviews)}


@app.post("/api/skillshub/reviews/{review_id}/approve")
async def approve_review(review_id: str, request: ReviewApproveRequest):
    """Approve a review task"""
    if not skills_hub_manager:
        raise HTTPException(status_code=500, detail="Skills Hub not available")

    version = skills_hub_manager.approve_version(
        review_id=review_id,
        reviewer_id=request.reviewer_id,
        comment=request.comment
    )
    if version:
        return {"success": True, "version": version.model_dump()}
    raise HTTPException(status_code=404, detail="Review not found")


@app.post("/api/skillshub/reviews/{review_id}/reject")
async def reject_review(review_id: str, request: ReviewRejectRequest):
    """Reject a review task"""
    if not skills_hub_manager:
        raise HTTPException(status_code=500, detail="Skills Hub not available")

    version = skills_hub_manager.reject_version(
        review_id=review_id,
        reviewer_id=request.reviewer_id,
        reason=request.reason
    )
    if version:
        return {"success": True, "version": version.model_dump()}
    raise HTTPException(status_code=404, detail="Review not found")


@app.post("/api/skillshub/promotions")
async def request_promotion(request: PromotionRequestCreate):
    """Request promotion of a skill to global namespace"""
    if not skills_hub_manager:
        raise HTTPException(status_code=500, detail="Skills Hub not available")

    try:
        promotion = skills_hub_manager.request_promotion(
            source_skill_id=request.source_skill_id,
            source_version_id=request.source_version_id,
            submitter_id=request.submitter_id,
            target_namespace_id=request.target_namespace_id
        )
        return {"success": True, "promotion": promotion.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/skillshub/promotions/pending")
async def get_pending_promotions():
    """Get pending promotion requests"""
    if not skills_hub_manager:
        return {"promotions": [], "count": 0}
    promotions = skills_hub_manager.get_pending_promotions()
    return {"promotions": [p.model_dump() for p in promotions], "count": len(promotions)}


@app.post("/api/skillshub/promotions/{promotion_id}/approve")
async def approve_promotion(promotion_id: str, request: ReviewApproveRequest):
    """Approve a promotion request"""
    if not skills_hub_manager:
        raise HTTPException(status_code=500, detail="Skills Hub not available")

    skill = skills_hub_manager.approve_promotion(
        promotion_id=promotion_id,
        reviewer_id=request.reviewer_id,
        comment=request.comment
    )
    if skill:
        return {"success": True, "skill": skill.model_dump()}
    raise HTTPException(status_code=404, detail="Promotion not found")


@app.post("/api/skillshub/promotions/{promotion_id}/reject")
async def reject_promotion(promotion_id: str, request: ReviewRejectRequest):
    """Reject a promotion request"""
    if not skills_hub_manager:
        raise HTTPException(status_code=500, detail="Skills Hub not available")

    promotion = skills_hub_manager.reject_promotion(
        promotion_id=promotion_id,
        reviewer_id=request.reviewer_id,
        reason=request.reason
    )
    if promotion:
        return {"success": True, "promotion": promotion.model_dump()}
    raise HTTPException(status_code=404, detail="Promotion not found")


@app.post("/api/skillshub/skills/{skill_id}/star")
async def star_skill(skill_id: str, user_id: str = "anonymous"):
    """Star a skill"""
    if skills_hub_manager:
        success = skills_hub_manager.star_skill(skill_id, user_id)
        return {"success": success}

    if skill_id in skills_storage:
        skills_storage[skill_id]["likes"] = skills_storage[skill_id].get("likes", 0) + 1
    return {"success": True}


@app.post("/api/skillshub/skills/{skill_id}/unstar")
async def unstar_skill(skill_id: str, user_id: str = "anonymous"):
    """Unstar a skill"""
    if skills_hub_manager:
        success = skills_hub_manager.unstar_skill(skill_id, user_id)
        return {"success": success}

    if skill_id in skills_storage:
        skills_storage[skill_id]["likes"] = max(0, skills_storage[skill_id].get("likes", 0) - 1)
    return {"success": True}


@app.post("/api/skillshub/skills/{skill_id}/rate")
async def rate_skill(skill_id: str, request: SkillRatingRequest):
    """Rate a skill"""
    if not skills_hub_manager:
        raise HTTPException(status_code=500, detail="Skills Hub not available")

    try:
        rating = skills_hub_manager.rate_skill(skill_id, request.user_id, request.score)
        return {"success": True, "rating": rating.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/skillshub/search")
async def search_skills(query: str = "", namespace_id: Optional[str] = None, visibility: Optional[str] = None, category: Optional[str] = None, limit: int = 20):
    """Search for skills"""
    if skills_hub_manager:
        result = skills_hub_manager.search_skills(query=query, namespace_id=namespace_id, visibility=visibility, category=category, limit=limit)
        return result.model_dump()
    return {"skills": [], "total_count": 0, "query": query}


@app.get("/api/skillshub/skills/popular")
async def get_popular_skills(namespace_id: Optional[str] = None, limit: int = 10):
    """Get popular skills"""
    if skills_hub_manager:
        skills = skills_hub_manager.get_popular_skills(namespace_id=namespace_id, limit=limit)
        return {"skills": [s.model_dump() for s in skills], "count": len(skills)}
    return {"skills": [], "count": 0}


@app.get("/api/skillshub/skills/recent")
async def get_recent_skills(namespace_id: Optional[str] = None, limit: int = 10):
    """Get recently updated skills"""
    if skills_hub_manager:
        skills = skills_hub_manager.get_recent_skills(namespace_id=namespace_id, limit=limit)
        return {"skills": [s.model_dump() for s in skills], "count": len(skills)}
    return {"skills": [], "count": 0}


# ==========================================
# OctoTrace Endpoints
# ==========================================

@app.get("/api/octotrace/overview")
async def get_trace_overview():
    """Get OctoTrace overview"""
    return {
        "total_traces": 0,
        "active_sessions": 0,
        "total_cost": 0.0,
        "average_latency": 0.0
    }


@app.get("/api/octotrace/costs")
async def get_costs():
    """Get cost tracking data"""
    return {
        "model_usage": [],
        "total_cost": 0.0,
        "budget_remaining": 100.0
    }


# ==========================================
# Skill Wiki Endpoints
# ==========================================

@app.get("/api/skillwiki/search")
async def search_wiki(query: str = ""):
    """Search the skill wiki"""
    return {
        "query": query,
        "results": [],
        "count": 0
    }


@app.get("/api/skillwiki/knowledge")
async def get_knowledge_graph():
    """Get knowledge graph data"""
    return {
        "nodes": [],
        "edges": [],
        "clusters": []
    }


# ==========================================
# AutoSkill Endpoints
# ==========================================

@app.post("/api/autoskill/experiments")
async def create_experiment(request: ExperimentCreateRequest):
    """Create a new AutoSkill experiment"""
    experiment_id = f"exp_{int(datetime.now().timestamp())}"

    experiment_data = {
        "id": experiment_id,
        "name": request.name,
        "description": request.description,
        "goal": request.goal,
        "config": request.config,
        "status": "created",
        "created_at": datetime.now().isoformat()
    }

    experiments_storage[experiment_id] = experiment_data

    return {"success": True, "experiment": experiment_data}


@app.get("/api/autoskill/experiments")
async def list_experiments():
    """List all AutoSkill experiments"""
    return {"experiments": list(experiments_storage.values())}


@app.get("/api/autoskill/experiments/{experiment_id}")
async def get_experiment(experiment_id: str):
    """Get a specific experiment"""
    if experiment_id not in experiments_storage:
        raise HTTPException(status_code=404, detail="Experiment not found")

    return {"experiment": experiments_storage[experiment_id]}


@app.post("/api/autoskill/experiments/{experiment_id}/start")
async def start_experiment(experiment_id: str):
    """Start an AutoSkill experiment"""
    if experiment_id not in experiments_storage:
        raise HTTPException(status_code=404, detail="Experiment not found")

    experiments_storage[experiment_id]["status"] = "running"
    experiments_storage[experiment_id]["started_at"] = datetime.now().isoformat()
    active_experiments[experiment_id] = experiments_storage[experiment_id]

    await manager.broadcast({
        "type": "experiment_started",
        "data": experiments_storage[experiment_id]
    })

    return {"success": True}


@app.post("/api/autoskill/experiments/{experiment_id}/stop")
async def stop_experiment(experiment_id: str):
    """Stop a running AutoSkill experiment"""
    if experiment_id not in experiments_storage:
        raise HTTPException(status_code=404, detail="Experiment not found")

    experiments_storage[experiment_id]["status"] = "stopped"
    if experiment_id in active_experiments:
        del active_experiments[experiment_id]

    return {"success": True}


# ==========================================
# WebSocket Endpoint
# ==========================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Handle incoming messages
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


# ==========================================
# Frontend Serving (optional)
# ==========================================

frontend_dist = BASE_DIR.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dist / "assets")), name="static")

    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        """Serve frontend application"""
        index_file = frontend_dist / "index.html"
        if index_file.exists():
            return HTMLResponse(content=index_file.read_text())
        return {"message": "Frontend not built yet"}


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("Octopai API Server v4.0")
    print("=" * 60)
    print(f"Project Root: {project_root}")
    print(f"Data Directory: {DATA_DIR}")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
