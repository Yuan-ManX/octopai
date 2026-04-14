"""
Octopai Skills Hub API
Skill registry and management system
"""

import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from skill_hub import (
    SkillManager,
    SkillCreateRequest,
    SkillUpdateRequest,
    SkillVersionCreateRequest,
    SearchRequest,
    StarRequest,
    ForkRequest
)


app = FastAPI(
    title="Octopai Skills Hub API",
    description="Octopai - Skill Registry and Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


skill_manager: Optional[SkillManager] = None


def initialize_manager():
    """Initialize the skill manager"""
    global skill_manager
    if skill_manager is None:
        skill_manager = SkillManager()


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    initialize_manager()
    
    user_id = "demo_user"
    if user_id not in skill_manager._users:
        skill_manager.create_user(
            username="demo",
            email="demo@octopai.ai",
            display_name="Demo User"
        )
        
        sample_skills = [
            {
                "name": "Data Analysis Assistant",
                "description": "Analyze and visualize data with advanced statistical methods",
                "namespace": "demo",
                "visibility": "public",
                "content": """# Data Analysis Assistant
Analyze datasets, generate visualizations, and provide statistical insights.
""",
                "metadata": {
                    "name": "Data Analysis Assistant",
                    "description": "Analyze and visualize data with advanced statistical methods",
                    "version": "1.0.0",
                    "author": "demo",
                    "category": "data",
                    "tags": ["analysis", "statistics", "visualization"],
                    "keywords": ["data", "analysis", "charts", "stats"]
                },
                "categories": ["Data Science"],
                "tags": ["analysis", "statistics"]
            },
            {
                "name": "Web Researcher",
                "description": "Search and summarize information from the web",
                "namespace": "demo",
                "visibility": "public",
                "content": """# Web Researcher
Search the web, gather information, and create comprehensive summaries.
""",
                "metadata": {
                    "name": "Web Researcher",
                    "description": "Search and summarize information from the web",
                    "version": "2.1.0",
                    "author": "demo",
                    "category": "research",
                    "tags": ["web", "search", "research"],
                    "keywords": ["web", "search", "internet", "research"]
                },
                "categories": ["Research"],
                "tags": ["web", "search"]
            },
            {
                "name": "Code Helper",
                "description": "Write, review, and optimize code across multiple languages",
                "namespace": "demo",
                "visibility": "public",
                "content": """# Code Helper
Assist with code writing, review, refactoring, and optimization.
""",
                "metadata": {
                    "name": "Code Helper",
                    "description": "Write, review, and optimize code across multiple languages",
                    "version": "3.0.0",
                    "author": "demo",
                    "category": "development",
                    "tags": ["code", "programming", "development"],
                    "keywords": ["code", "programming", "development", "review"]
                },
                "categories": ["Development"],
                "tags": ["code", "development"]
            },
            {
                "name": "Content Creator",
                "description": "Generate creative content for various purposes",
                "namespace": "demo",
                "visibility": "public",
                "content": """# Content Creator
Generate blog posts, articles, social media content, and more.
""",
                "metadata": {
                    "name": "Content Creator",
                    "description": "Generate creative content for various purposes",
                    "version": "1.5.0",
                    "author": "demo",
                    "category": "content",
                    "tags": ["content", "writing", "creative"],
                    "keywords": ["content", "writing", "creative", "blog"]
                },
                "categories": ["Content Creation"],
                "tags": ["content", "writing"]
            },
            {
                "name": "AI Image Generator",
                "description": "Generate stunning images using AI models",
                "namespace": "demo",
                "visibility": "public",
                "content": """# AI Image Generator
Create beautiful images with AI-powered generation tools.
""",
                "metadata": {
                    "name": "AI Image Generator",
                    "description": "Generate stunning images using AI models",
                    "version": "1.2.0",
                    "author": "demo",
                    "category": "ai-tools",
                    "tags": ["image", "generation", "creative", "ai"],
                    "keywords": ["image", "ai", "generation", "art"]
                },
                "categories": ["AI Tools"],
                "tags": ["image", "ai", "creative"]
            },
            {
                "name": "Document Processor",
                "description": "Process and extract information from various document formats",
                "namespace": "demo",
                "visibility": "public",
                "content": """# Document Processor
Extract text, analyze structure, and process PDFs, Word docs, and more.
""",
                "metadata": {
                    "name": "Document Processor",
                    "description": "Process and extract information from various document formats",
                    "version": "2.0.0",
                    "author": "demo",
                    "category": "productivity",
                    "tags": ["document", "pdf", "processing", "extraction"],
                    "keywords": ["document", "pdf", "word", "extraction"]
                },
                "categories": ["Productivity"],
                "tags": ["document", "pdf"]
            },
            {
                "name": "API Integration Kit",
                "description": "Integrate with popular APIs and services seamlessly",
                "namespace": "demo",
                "visibility": "public",
                "content": """# API Integration Kit
Connect to REST APIs, GraphQL endpoints, and webhooks easily.
""",
                "metadata": {
                    "name": "API Integration Kit",
                    "description": "Integrate with popular APIs and services seamlessly",
                    "version": "1.8.0",
                    "author": "demo",
                    "category": "integration",
                    "tags": ["api", "rest", "graphql", "webhook"],
                    "keywords": ["api", "integration", "rest", "graphql"]
                },
                "categories": ["Integration"],
                "tags": ["api", "integration"]
            },
            {
                "name": "Task Automation Engine",
                "description": "Automate repetitive tasks with intelligent workflows",
                "namespace": "demo",
                "visibility": "public",
                "content": """# Task Automation Engine
Create automated workflows for data processing, notifications, and more.
""",
                "metadata": {
                    "name": "Task Automation Engine",
                    "description": "Automate repetitive tasks with intelligent workflows",
                    "version": "2.5.0",
                    "author": "demo",
                    "category": "automation",
                    "tags": ["automation", "workflow", "tasks", "scheduler"],
                    "keywords": ["automation", "workflow", "tasks", "cron"]
                },
                "categories": ["Automation"],
                "tags": ["automation", "workflow"]
            }
        ]
        
        for skill_data in sample_skills:
            try:
                skill_manager.create_skill(
                    name=skill_data["name"],
                    description=skill_data["description"],
                    namespace=skill_data["namespace"],
                    visibility=skill_data["visibility"],
                    content=skill_data["content"],
                    metadata_dict=skill_data["metadata"],
                    created_by=user_id,
                    categories=skill_data.get("categories"),
                    tags=skill_data.get("tags")
                )
            except ValueError:
                pass


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Octopai Skills Hub API",
        "version": "1.0.0",
        "status": "running",
        "capabilities": [
            "Skill Registry",
            "Version Management",
            "Public/Private Skills",
            "Search & Discovery",
            "Star & Fork"
        ]
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    initialize_manager()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "skill_manager": skill_manager is not None
    }


@app.get("/api/skills", response_model=Dict[str, Any])
async def list_skills(
    namespace: Optional[str] = Query(None),
    visibility: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    sort_by: str = Query("updated_at"),
    sort_order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """List skills with filters"""
    initialize_manager()
    
    skills, total = skill_manager.list_skills(
        namespace=namespace,
        visibility=visibility,
        category=category,
        tags=tags,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )
    
    return {
        "skills": [s.to_dict() for s in skills],
        "total": total,
        "page": page,
        "page_size": page_size,
        "has_next": (page * page_size) < total
    }


@app.post("/api/skills/search", response_model=Dict[str, Any])
async def search_skills(request: SearchRequest):
    """Search skills"""
    initialize_manager()
    
    skills, total = skill_manager.search_skills(
        query=request.query,
        category=request.category,
        tags=request.tags,
        visibility=request.visibility,
        namespace=request.namespace,
        sort_by=request.sort_by,
        sort_order=request.sort_order,
        page=request.page,
        page_size=request.page_size
    )
    
    return {
        "skills": [s.to_dict() for s in skills],
        "total": total,
        "page": request.page,
        "page_size": request.page_size,
        "has_next": (request.page * request.page_size) < total
    }


@app.get("/api/skills/{skill_id}", response_model=Dict[str, Any])
async def get_skill(skill_id: str = Path(...)):
    """Get a skill by ID"""
    initialize_manager()
    
    skill = skill_manager.get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return skill.to_dict()


@app.get("/api/skills/{namespace}/{slug}", response_model=Dict[str, Any])
async def get_skill_by_slug(
    namespace: str = Path(...),
    slug: str = Path(...)
):
    """Get a skill by namespace and slug"""
    initialize_manager()
    
    skill = skill_manager.get_skill_by_slug(namespace, slug)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return skill.to_dict()


@app.post("/api/skills", response_model=Dict[str, Any])
async def create_skill(request: SkillCreateRequest):
    """Create a new skill"""
    initialize_manager()
    
    user_id = "demo_user"
    
    try:
        skill = skill_manager.create_skill(
            name=request.name,
            description=request.description,
            namespace=request.namespace,
            visibility=request.visibility,
            content=request.content,
            metadata_dict=request.metadata.model_dump(),
            created_by=user_id,
            categories=request.categories,
            tags=request.tags
        )
        return skill.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/skills/{skill_id}", response_model=Dict[str, Any])
async def update_skill(
    skill_id: str = Path(...),
    request: SkillUpdateRequest = Body(...)
):
    """Update a skill"""
    initialize_manager()
    
    skill = skill_manager.update_skill(
        skill_id=skill_id,
        name=request.name,
        description=request.description,
        visibility=request.visibility,
        categories=request.categories,
        tags=request.tags
    )
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return skill.to_dict()


@app.delete("/api/skills/{skill_id}")
async def delete_skill(skill_id: str = Path(...)):
    """Delete a skill"""
    initialize_manager()
    
    success = skill_manager.delete_skill(skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return {"status": "deleted", "skill_id": skill_id}


@app.post("/api/skills/{skill_id}/versions", response_model=Dict[str, Any])
async def create_skill_version(
    skill_id: str = Path(...),
    request: SkillVersionCreateRequest = Body(...)
):
    """Create a new skill version"""
    initialize_manager()
    
    user_id = "demo_user"
    
    try:
        version = skill_manager.create_skill_version(
            skill_id=skill_id,
            version=request.version,
            content=request.content,
            metadata_dict=request.metadata.model_dump(),
            created_by=user_id,
            changelog=request.changelog
        )
        
        if not version:
            raise HTTPException(status_code=404, detail="Skill not found")
        
        return version.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/skills/{skill_id}/download")
async def download_skill(
    skill_id: str = Path(...),
    version: Optional[str] = Query(None)
):
    """Download a skill"""
    initialize_manager()
    
    result = skill_manager.download_skill(skill_id, version)
    if not result:
        raise HTTPException(status_code=404, detail="Skill or version not found")
    
    content, ver = result
    return {
        "content": content,
        "version": ver
    }


@app.post("/api/skills/{skill_id}/star")
async def toggle_star(
    skill_id: str = Path(...),
    request: StarRequest = Body(...)
):
    """Toggle star on a skill"""
    initialize_manager()
    
    user_id = "demo_user"
    
    starred = skill_manager.toggle_star(user_id, skill_id)
    return {
        "skill_id": skill_id,
        "starred": starred
    }


@app.get("/api/skills/{skill_id}/starred")
async def check_starred(skill_id: str = Path(...)):
    """Check if skill is starred"""
    initialize_manager()
    
    user_id = "demo_user"
    
    starred = skill_manager.is_starred(user_id, skill_id)
    return {
        "skill_id": skill_id,
        "starred": starred
    }


@app.post("/api/skills/{skill_id}/fork", response_model=Dict[str, Any])
async def fork_skill(
    skill_id: str = Path(...),
    request: ForkRequest = Body(...)
):
    """Fork a skill"""
    initialize_manager()
    
    user_id = "demo_user"
    
    skill = skill_manager.fork_skill(
        skill_id=skill_id,
        new_namespace=request.new_namespace,
        new_name=request.new_name,
        forked_by=user_id
    )
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return skill.to_dict()


@app.get("/api/categories")
async def get_categories():
    """Get all categories"""
    initialize_manager()
    
    categories = set()
    for skill in skill_manager._skills.values():
        if skill.visibility.value == "public":
            categories.update(skill.categories)
    
    return {
        "categories": sorted(list(categories))
    }


@app.get("/api/tags")
async def get_tags():
    """Get all tags"""
    initialize_manager()
    
    tags = set()
    for skill in skill_manager._skills.values():
        if skill.visibility.value == "public":
            tags.update(skill.tags)
    
    return {
        "tags": sorted(list(tags))
    }


@app.get("/api/stats/overview")
async def get_stats_overview():
    """Get platform statistics overview"""
    initialize_manager()
    
    total_skills = len(skill_manager._skills)
    public_skills = sum(1 for s in skill_manager._skills.values() if s.visibility.value == "public")
    private_skills = total_skills - public_skills
    total_downloads = sum(s.download_count for s in skill_manager._skills.values())
    total_stars = sum(s.star_count for s in skill_manager._skills.values())
    total_forks = sum(s.fork_count for s in skill_manager._skills.values())
    total_users = len(skill_manager._users)
    total_orgs = len(skill_manager._organizations)
    
    return {
        "total_skills": total_skills,
        "public_skills": public_skills,
        "private_skills": private_skills,
        "total_downloads": total_downloads,
        "total_stars": total_stars,
        "total_forks": total_forks,
        "total_users": total_users,
        "total_orgs": total_orgs
    }


@app.get("/api/skills/trending", response_model=Dict[str, Any])
async def get_trending_skills(limit: int = Query(10, ge=1, le=50)):
    """Get trending skills based on recent activity"""
    initialize_manager()
    
    public_skills = [s for s in skill_manager._skills.values() if s.visibility.value == "public"]
    
    trending = sorted(
        public_skills,
        key=lambda x: (
            x.star_count * 3 +
            x.download_count * 2 +
            x.fork_count * 5 +
            x.view_count * 0.1
        ),
        reverse=True
    )[:limit]
    
    return {
        "skills": [s.to_dict() for s in trending],
        "limit": limit
    }


@app.get("/api/skills/recent", response_model=Dict[str, Any])
async def get_recent_skills(limit: int = Query(10, ge=1, le=50)):
    """Get recently published or updated skills"""
    initialize_manager()
    
    public_skills = [s for s in skill_manager._skills.values() if s.visibility.value == "public"]
    
    recent = sorted(
        public_skills,
        key=lambda x: x.updated_at,
        reverse=True
    )[:limit]
    
    return {
        "skills": [s.to_dict() for s in recent],
        "limit": limit
    }


@app.get("/api/skills/recommended", response_model=Dict[str, Any])
async def get_recommended_skills(limit: int = Query(10, ge=1, le=50)):
    """Get recommended skills based on popularity and quality"""
    initialize_manager()
    
    public_skills = [s for s in skill_manager._skills.values() if s.visibility.value == "public"]
    
    recommended = sorted(
        public_skills,
        key=lambda x: (
            x.star_count * 4 +
            x.download_count * 1.5 +
            (len(x.versions) if x.versions else 0) * 2 +
            (1 if x.metadata and len(s.tags) > 2 else 0)
        ),
        reverse=True
    )[:limit]
    
    return {
        "skills": [s.to_dict() for s in recommended],
        "limit": limit
    }


@app.get("/api/skills/popular", response_model=Dict[str, Any])
async def get_popular_skills(limit: int = Query(10, ge=1, le=50)):
    """Get most downloaded skills"""
    initialize_manager()
    
    public_skills = [s for s in skill_manager._skills.values() if s.visibility.value == "public"]
    
    popular = sorted(
        public_skills,
        key=lambda x: x.download_count,
        reverse=True
    )[:limit]
    
    return {
        "skills": [s.to_dict() for s in popular],
        "limit": limit
    }


@app.get("/api/leaderboard")
async def get_leaderboard():
    """Get skills leaderboard by category"""
    initialize_manager()
    
    categories = {}
    for skill in skill_manager._skills.values():
        if skill.visibility.value != "public":
            continue
            
        for category in skill.categories:
            if category not in categories:
                categories[category] = []
            categories[category].append(skill)
    
    leaderboard = {}
    for category, skills in categories.items():
        top_skills = sorted(
            skills,
            key=lambda x: x.star_count + x.download_count,
            reverse=True
        )[:5]
        
        leaderboard[category] = [
            {
                "skill_id": s.skill_id,
                "name": s.name,
                "slug": s.slug,
                "namespace": s.namespace,
                "star_count": s.star_count,
                "download_count": s.download_count,
                "description": s.description[:100]
            }
            for s in top_skills
        ]
    
    return {
        "leaderboard": leaderboard,
        "categories": sorted(leaderboard.keys())
    }


@app.get("/api/namespaces/{namespace}/skills")
async def get_namespace_skills(
    namespace: str = Path(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Get all skills from a namespace"""
    initialize_manager()
    
    skills, total = skill_manager.list_skills(
        namespace=namespace,
        page=page,
        page_size=page_size
    )
    
    return {
        "skills": [s.to_dict() for s in skills],
        "total": total,
        "namespace": namespace,
        "page": page,
        "page_size": page_size
    }


@app.get("/api/users/{user_id}/starred")
async def get_user_starred_skills(user_id: str = Path(...)):
    """Get skills starred by a user"""
    initialize_manager()
    
    starred_ids = skill_manager._user_stars.get(user_id, set())
    starred_skills = [
        skill_manager._skills[sid].to_dict()
        for sid in starred_ids
        if sid in skill_manager._skills
    ]
    
    return {
        "skills": starred_skills,
        "total": len(starred_skills),
        "user_id": user_id
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3003)
