"""
Octopai Web Backend API (Demo Mode)

Simplified FastAPI backend for frontend demonstration.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(
    title="Octopai Web API",
    description="Octopai - Self-Evolving AI Agent Intelligence Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create directories
UPLOAD_DIR = Path("./uploads")
SKILLS_DIR = Path("./skills")
UPLOAD_DIR.mkdir(exist_ok=True)
SKILLS_DIR.mkdir(exist_ok=True)


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    task_type: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    return {
        "message": "Octopai Web API",
        "version": "1.0.0",
        "status": "running",
        "philosophy": [
            "Self-Evolving AI Agent Intelligence Engine",
            "Skills Evolve Through Continuous Learning",
            "AutoResearch - Autonomous Research Platform"
        ]
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/skills/create/url", response_model=TaskStatusResponse)
async def create_skill_from_url(url: str, name: str, description: str):
    """Create a skill from a URL (demo)"""
    import uuid
    task_id = str(uuid.uuid4())[:8]
    
    return TaskStatusResponse(
        task_id=task_id,
        status="completed",
        task_type="create_from_url",
        created_at=datetime.now().isoformat(),
        result={
            "skill_id": f"skill_{task_id}",
            "name": name,
            "url": url,
            "message": "Skill created successfully (demo mode)"
        }
    )


@app.get("/api/skills")
async def list_skills(category: Optional[str] = None, limit: int = 100, offset: int = 0):
    """List all skills (demo data)"""
    demo_skills = [
        {
            "id": "skill_001",
            "name": "Web Research Agent",
            "category": "Research",
            "description": "Autonomous web research and information synthesis",
            "version": "3.2.1",
            "evolution_level": "Advanced",
            "last_evolved": "2 hours ago",
            "status": "published"
        },
        {
            "id": "skill_002",
            "name": "Document Parser Pro",
            "category": "Parsing",
            "description": "Multi-format document extraction engine",
            "version": "2.8.0",
            "evolution_level": "Mature",
            "last_evolved": "5 hours ago",
            "status": "published"
        },
        {
            "id": "skill_003",
            "name": "Code Generator",
            "category": "Development",
            "description": "Intelligent code generation with multi-language support",
            "version": "4.1.0",
            "evolution_level": "Expert",
            "last_evolved": "1 hour ago",
            "status": "published"
        },
        {
            "id": "skill_004",
            "name": "Data Analyst",
            "category": "Analytics",
            "description": "Statistical analysis and pattern recognition engine",
            "version": "2.5.3",
            "evolution_level": "Intermediate",
            "last_evolved": "12 hours ago",
            "status": "evolving"
        }
    ]
    
    return {
        "skills": demo_skills[offset:offset+limit],
        "total": len(demo_skills),
        "page": offset // limit + 1 if limit > 0 else 1,
        "page_size": limit
    }


@app.get("/api/skills/{skill_id}")
async def get_skill(skill_id: str):
    """Get a specific skill (demo)"""
    return {
        "id": skill_id,
        "name": "Demo Skill",
        "description": "This is a demo skill for testing the frontend",
        "version": "1.0.0",
        "evolution_level": "Growing",
        "created_at": datetime.now().isoformat(),
        "capabilities": ["Demo capability 1", "Demo capability 2"],
        "status": "active"
    }


@app.get("/api/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get status of a task (demo)"""
    return TaskStatusResponse(
        task_id=task_id,
        status="completed",
        task_type="demo_task",
        created_at=datetime.now().isoformat(),
        completed_at=datetime.now().isoformat(),
        result={"message": "Task completed successfully"}
    )


@app.get("/api/stats")
async def get_stats():
    """Get SkillHub statistics (demo)"""
    return {
        "total_skills": 6,
        "currently_evolving": 4,
        "total_evolution_cycles": 127,
        "success_rate": 0.98,
        "categories": {
            "Research": 2,
            "Parsing": 1,
            "Development": 1,
            "Analytics": 1,
            "Creative": 1
        }
    }


@app.get("/api/insights")
async def get_insights(skill_id: Optional[str] = None):
    """Get experience insights (demo)"""
    return {
        "total_experiences": 847,
        "recent_improvements": 23,
        "evolution_trend": "upward",
        "top_performing_skills": ["skill_001", "skill_003"]
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🐙 Octopai Web API Server")
    print("="*60)
    print(f"   Frontend: http://localhost:8081")
    print(f"   Backend:  http://localhost:3001")
    print(f"   Docs:     http://localhost:3001/docs")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=3001)
