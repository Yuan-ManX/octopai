"""
EXO Web Backend API

FastAPI backend for EXO Web Frontend, providing REST API endpoints
for skill creation, evolution, and management.
"""

import os
import sys
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from exo import EXO
from exo.api_integration.api import EXOIntegrationAPI
from exo.api_integration.schemas import (
    CreateSkillFromURLRequest,
    CreateSkillFromFilesRequest,
    CreateSkillFromPromptRequest,
    OptimizeSkillRequest,
)


app = FastAPI(
    title="EXO Web API",
    description="EXO - Everything Can Be a Skill • Skills Evolve Through Continuous Learning",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

SKILLS_DIR = Path("./skills")
SKILLS_DIR.mkdir(exist_ok=True)

exo_api = EXOIntegrationAPI(
    skill_output_dir=str(SKILLS_DIR),
    skill_hub_dir="./SkillHub",
    experience_dir="./experiences"
)


class CreateSkillFromURLForm(BaseModel):
    url: str = Field(..., description="URL to convert to skill")
    name: str = Field(..., description="Skill name")
    description: str = Field(..., description="Skill description")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    category: Optional[str] = Field(None, description="Skill category")


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
        "message": "EXO Web API",
        "version": "1.0.0",
        "philosophy": [
            "Everything Can Be a Skill",
            "Skills Evolve Through Continuous Learning",
            "Elevating AI Agent Cognition"
        ]
    }


@app.post("/api/skills/create/url", response_model=TaskStatusResponse)
async def create_skill_from_url(form: CreateSkillFromURLForm):
    """Create a skill from a URL"""
    try:
        tags = [t.strip() for t in form.tags.split(",")] if form.tags else []
        
        request = CreateSkillFromURLRequest(
            url=form.url,
            name=form.name,
            description=form.description,
            tags=tags,
            category=form.category,
            author="EXO Web",
            skill_type="general"
        )
        
        task_id = exo_api.create_skill_from_url_async(request)
        
        return TaskStatusResponse(
            task_id=task_id,
            status="pending",
            task_type="create_from_url",
            created_at=exo_api.tasks[task_id].created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills/create/files")
async def create_skill_from_files(
    name: str = Form(...),
    description: str = Form(...),
    tags: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    files: List[UploadFile] = File(...)
):
    """Create a skill from uploaded files"""
    try:
        uploaded_files = []
        for file in files:
            file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            uploaded_files.append(str(file_path))
        
        tags_list = [t.strip() for t in tags.split(",")] if tags else []
        
        request = CreateSkillFromFilesRequest(
            files=uploaded_files,
            name=name,
            description=description,
            tags=tags_list,
            category=category,
            author="EXO Web",
            skill_type="general"
        )
        
        task_id = exo_api.create_skill_from_files_async(request)
        
        task = exo_api.get_task_status(task_id)
        
        return {
            "task_id": task_id,
            "status": task.status.value if task else "pending",
            "task_type": "create_from_files",
            "created_at": task.created_at if task else ""
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills/create/prompt")
async def create_skill_from_prompt(
    prompt: str = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    tags: Optional[str] = Form(None),
    category: Optional[str] = Form(None)
):
    """Create a skill from a prompt"""
    try:
        tags_list = [t.strip() for t in tags.split(",")] if tags else []
        
        request = CreateSkillFromPromptRequest(
            prompt=prompt,
            name=name,
            description=description,
            tags=tags_list,
            category=category,
            author="EXO Web",
            skill_type="general",
            resources=None
        )
        
        task_id = exo_api.create_skill_from_prompt_async(request)
        
        task = exo_api.get_task_status(task_id)
        
        return {
            "task_id": task_id,
            "status": task.status.value if task else "pending",
            "task_type": "create_from_prompt",
            "created_at": task.created_at if task else ""
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Get status of a task"""
    task = exo_api.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskStatusResponse(
        task_id=task.task_id,
        status=task.status.value,
        task_type=task.task_type,
        created_at=task.created_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        error=task.error
    )


@app.get("/api/skills")
async def list_skills(category: Optional[str] = None, limit: int = 100, offset: int = 0):
    """List all skills"""
    try:
        response = exo_api.list_skills(category=category, limit=limit, offset=offset)
        return {
            "skills": [s.dict() for s in response.skills],
            "total": response.total,
            "page": response.page,
            "page_size": response.page_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/skills/{skill_id}")
async def get_skill(skill_id: str):
    """Get a specific skill"""
    try:
        skill_info = exo_api.get_skill_info(skill_id)
        if not skill_info:
            raise HTTPException(status_code=404, detail="Skill not found")
        return skill_info.dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills/{skill_id}/evolve")
async def evolve_skill(skill_id: str, feedback_summary: str = Form(...)):
    """Evolve a skill based on feedback"""
    try:
        skill_dir = SKILLS_DIR / skill_id
        if not skill_dir.exists():
            raise HTTPException(status_code=404, detail="Skill directory not found")
        
        request = OptimizeSkillRequest(skill_dir=str(skill_dir))
        task_id = exo_api.optimize_skill_async(request)
        
        task = exo_api.get_task_status(task_id)
        
        return {
            "task_id": task_id,
            "status": task.status.value if task else "pending",
            "task_type": "evolve_skill",
            "created_at": task.created_at if task else ""
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/insights")
async def get_insights(skill_id: Optional[str] = None):
    """Get experience insights"""
    try:
        return exo_api.get_insights(skill_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get SkillHub statistics"""
    try:
        return exo_api.exo.get_skill_hub_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
