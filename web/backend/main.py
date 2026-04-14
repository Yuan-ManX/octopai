"""
Octopai Web Backend API

FastAPI backend for Octopai Web Frontend, providing REST API endpoints
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

from octopai import Octopai
from octopai.api_integration.api import OctopaiIntegrationAPI
from octopai.api_integration.schemas import (
    CreateSkillFromURLRequest,
    CreateSkillFromFilesRequest,
    CreateSkillFromPromptRequest,
    OptimizeSkillRequest,
    UpdateSkillMetadataRequest,
    CreateCollectionRequest,
    AddRatingRequest,
    VersionDiffRequest,
    RollbackRequest,
    PublishSkillRequest,
    CreateCompositionRequest,
    BindSkillRequest,
    SemanticSearchQuery,
)


app = FastAPI(
    title="Octopai Web API",
    description="Octopai - Everything Can Be a Skill • Skills Evolve Through Continuous Learning",
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

octopai_api = OctopaiIntegrationAPI(
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
        "message": "Octopai Web API",
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
            author="Octopai Web",
            skill_type="general"
        )
        
        task_id = octopai_api.create_skill_from_url_async(request)
        
        return TaskStatusResponse(
            task_id=task_id,
            status="pending",
            task_type="create_from_url",
            created_at=octopai_api.tasks[task_id].created_at
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
            author="Octopai Web",
            skill_type="general"
        )
        
        task_id = octopai_api.create_skill_from_files_async(request)
        
        task = octopai_api.get_task_status(task_id)
        
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
            author="Octopai Web",
            skill_type="general",
            resources=None
        )
        
        task_id = octopai_api.create_skill_from_prompt_async(request)
        
        task = octopai_api.get_task_status(task_id)
        
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
    task = octopai_api.get_task_status(task_id)
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
        response = octopai_api.list_skills(category=category, limit=limit, offset=offset)
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
        skill_info = octopai_api.get_skill_info(skill_id)
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
        task_id = octopai_api.optimize_skill_async(request)
        
        task = octopai_api.get_task_status(task_id)
        
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
        return octopai_api.get_insights(skill_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get SkillHub statistics"""
    try:
        return octopai_api.octopai.get_skill_hub_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/skills/{skill_id}/metadata")
async def update_skill_metadata_endpoint(skill_id: str, request: UpdateSkillMetadataRequest):
    """Update skill metadata"""
    try:
        request.skill_id = skill_id
        result = octopai_api.update_skill_metadata(request)
        if not result:
            raise HTTPException(status_code=404, detail="Skill not found")
        return result.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/collections")
async def create_collection_endpoint(request: CreateCollectionRequest):
    """Create a new skill collection"""
    try:
        result = octopai_api.create_collection(request)
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/collections")
async def list_collections_endpoint():
    """List all collections"""
    try:
        result = octopai_api.list_collections()
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/collections/{collection_id}")
async def get_collection_endpoint(collection_id: str):
    """Get a specific collection"""
    try:
        result = octopai_api.get_collection(collection_id)
        if not result:
            raise HTTPException(status_code=404, detail="Collection not found")
        return result.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/collections/{collection_id}/skills/{skill_id}")
async def add_skill_to_collection_endpoint(collection_id: str, skill_id: str):
    """Add a skill to a collection"""
    try:
        success = octopai_api.add_skill_to_collection(collection_id, skill_id)
        if not success:
            raise HTTPException(status_code=404, detail="Collection or skill not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/collections/{collection_id}/skills/{skill_id}")
async def remove_skill_from_collection_endpoint(collection_id: str, skill_id: str):
    """Remove a skill from a collection"""
    try:
        success = octopai_api.remove_skill_from_collection(collection_id, skill_id)
        if not success:
            raise HTTPException(status_code=404, detail="Collection or skill not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/collections/{collection_id}")
async def delete_collection_endpoint(collection_id: str):
    """Delete a collection"""
    try:
        success = octopai_api.delete_collection(collection_id)
        if not success:
            raise HTTPException(status_code=404, detail="Collection not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills/{skill_id}/ratings")
async def add_rating_endpoint(skill_id: str, request: AddRatingRequest):
    """Add a rating to a skill"""
    try:
        request.skill_id = skill_id
        result = octopai_api.add_rating(request)
        if not result:
            raise HTTPException(status_code=404, detail="Skill not found")
        return result.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/skills/{skill_id}/ratings")
async def get_ratings_endpoint(skill_id: str):
    """Get all ratings for a skill"""
    try:
        ratings = octopai_api.get_ratings(skill_id)
        return [r.to_dict() for r in ratings]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills/{skill_id}/diff")
async def compute_version_diff_endpoint(skill_id: str, request: VersionDiffRequest):
    """Compute version difference"""
    try:
        request.skill_id = skill_id
        result = octopai_api.compute_version_diff(request)
        if not result:
            raise HTTPException(status_code=404, detail="Skill or versions not found")
        return result.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills/{skill_id}/rollback")
async def rollback_skill_endpoint(skill_id: str, request: RollbackRequest):
    """Rollback a skill to a previous version"""
    try:
        request.skill_id = skill_id
        result = octopai_api.rollback_skill(request)
        if not result:
            raise HTTPException(status_code=404, detail="Skill or version not found")
        return result.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills/{skill_id}/publish")
async def publish_skill_endpoint(skill_id: str, request: PublishSkillRequest):
    """Publish a skill"""
    try:
        request.skill_id = skill_id
        result = octopai_api.publish_skill(request)
        if not result:
            raise HTTPException(status_code=404, detail="Skill not found")
        return result.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills/{skill_id}/deprecate")
async def deprecate_skill_endpoint(skill_id: str):
    """Deprecate a skill"""
    try:
        result = octopai_api.deprecate_skill(skill_id)
        if not result:
            raise HTTPException(status_code=404, detail="Skill not found")
        return result.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills/{skill_id}/archive")
async def archive_skill_endpoint(skill_id: str):
    """Archive a skill"""
    try:
        result = octopai_api.archive_skill(skill_id)
        if not result:
            raise HTTPException(status_code=404, detail="Skill not found")
        return result.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compositions")
async def create_composition_endpoint(request: CreateCompositionRequest):
    """Create a context composition"""
    try:
        result = octopai_api.create_composition(request)
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/compositions")
async def list_compositions_endpoint():
    """List all compositions"""
    try:
        result = octopai_api.list_compositions()
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/compositions/{composition_id}")
async def get_composition_endpoint(composition_id: str):
    """Get a specific composition"""
    try:
        result = octopai_api.get_composition(composition_id)
        if not result:
            raise HTTPException(status_code=404, detail="Composition not found")
        return result.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compositions/{composition_id}/slots")
async def add_slot_to_composition_endpoint(composition_id: str, slot: dict):
    """Add a slot to a composition"""
    try:
        from octopai.api_integration.schemas import ContextSlotSchema
        slot_schema = ContextSlotSchema.from_dict(slot)
        success = octopai_api.add_slot_to_composition(composition_id, slot_schema)
        if not success:
            raise HTTPException(status_code=404, detail="Composition not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compositions/{composition_id}/slots/{slot_id}/bind")
async def bind_skill_to_slot_endpoint(composition_id: str, slot_id: str, request: BindSkillRequest):
    """Bind a skill to a composition slot"""
    try:
        request.composition_id = composition_id
        request.slot_id = slot_id
        success = octopai_api.bind_skill_to_slot(request)
        if not success:
            raise HTTPException(status_code=404, detail="Composition, slot, or skill not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/compositions/{composition_id}")
async def delete_composition_endpoint(composition_id: str):
    """Delete a composition"""
    try:
        success = octopai_api.delete_composition(composition_id)
        if not success:
            raise HTTPException(status_code=404, detail="Composition not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/skills/search/semantic")
async def semantic_search_endpoint(query: SemanticSearchQuery):
    """Enhanced semantic search for skills"""
    try:
        result = octopai_api.semantic_search(query)
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
