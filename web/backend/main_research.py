"""
AutoResearch API Server
FastAPI application for autonomous research management
"""

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uuid

from auto_research import AutoResearchManager

app = FastAPI(
    title="Octopai AutoResearch API",
    description="Autonomous Research System - Automate scientific discovery and experimentation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

research_manager = None

def initialize_manager():
    """Initialize the research manager"""
    global research_manager
    if research_manager is None:
        research_manager = AutoResearchManager()
        _seed_sample_data()
    return research_manager

def _seed_sample_data():
    """Seed sample research projects for demonstration"""
    global research_manager
    
    # Create sample research projects
    sample_projects = [
        {
            "name": "Neural Architecture Search Optimization",
            "description": "Exploring novel approaches to automate neural architecture design using evolutionary algorithms",
            "namespace": "demo",
            "visibility": "public",
            "domain": "Machine Learning",
            "subdomain": "Deep Learning",
            "topic": "Automated Machine Learning (AutoML)",
            "keywords": ["neural-architecture", "autoML", "evolutionary-algorithms", "deep-learning"]
        },
        {
            "name": "Quantum Computing Applications in Drug Discovery",
            "description": "Investigating quantum algorithms for molecular simulation and drug target identification",
            "namespace": "demo",
            "visibility": "public",
            "domain": "Quantum Computing",
            "subdomain": "Chemistry",
            "topic": "Computational Chemistry",
            "keywords": ["quantum-computing", "drug-discovery", "molecular-simulation", "pharmaceuticals"]
        },
        {
            "name": "Natural Language Understanding for Scientific Literature",
            "description": "Building AI systems to extract knowledge from academic papers and generate research insights",
            "namespace": "demo",
            "visibility": "public",
            "domain": "Natural Language Processing",
            "subdomain": "Information Extraction",
            "topic": "Scientific NLP",
            "keywords": ["NLP", "information-extraction", "scientific-literature", "knowledge-graphs"]
        },
        {
            "name": "Reinforcement Learning for Robotics Control",
            "description": "Developing advanced RL algorithms for autonomous robot manipulation and navigation",
            "namespace": "demo",
            "visibility": "public",
            "domain": "Robotics",
            "subdomain": "Control Systems",
            "topic": "Autonomous Systems",
            "keywords": ["reinforcement-learning", "robotics", "control-systems", "autonomous-navigation"]
        }
    ]
    
    for proj_data in sample_projects:
        # Remove subdomain from create_project kwargs as it's not a parameter
        create_kwargs = {k: v for k, v in proj_data.items() if k != 'subdomain'}
        project = research_manager.create_project(**create_kwargs)
        
        # Add sample ideas
        research_manager.add_idea(
            project_id=project.project_id,
            title=f"Idea 1: Novel approach for {proj_data['name']}",
            description="This idea proposes a new methodology that could significantly improve current state-of-the-art results",
            domain=proj_data["domain"],
            keywords=proj_data["keywords"][:3],
            novelty_score=8.5,
            feasibility_score=7.2,
            impact_score=9.0
        )
        
        # Add sample experiment
        experiment = research_manager.create_experiment(
            project_id=project.project_id,
            name="Baseline Experiment",
            description="Establishing baseline performance metrics using standard methodology"
        )
        
        # Run experiment to generate results
        research_manager.run_experiment(experiment.experiment_id)


# Project Endpoints

@app.post("/api/research/projects")
async def create_project(request: Dict[str, Any]):
    """Create a new research project"""
    manager = initialize_manager()
    
    project = manager.create_project(
        name=request.get('name'),
        description=request.get('description', ''),
        namespace=request.get('namespace', 'demo'),
        visibility=request.get('visibility', 'private'),
        domain=request.get('domain', ''),
        topic=request.get('topic'),
        keywords=request.get('keywords', []),
        created_by=request.get('created_by', 'user')
    )
    
    return {"project": project.to_dict(), "message": "Project created successfully"}


@app.get("/api/research/projects")
async def list_projects(
    status: str = Query(None),
    domain: str = Query(None),
    namespace: str = Query(None),
    visibility: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """List all research projects with filtering"""
    manager = initialize_manager()
    
    projects, total = manager.list_projects(
        status=status,
        domain=domain,
        namespace=namespace,
        visibility=visibility,
        page=page,
        page_size=page_size
    )
    
    return {
        "projects": [p.to_dict() for p in projects],
        "total": total,
        "page": page,
        "page_size": page_size
    }


@app.get("/api/research/projects/{project_id}")
async def get_project(project_id: str = Path(...)):
    """Get a specific research project"""
    manager = initialize_manager()
    
    project = manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"project": project.to_dict()}


@app.put("/api/research/projects/{project_id}")
async def update_project(project_id: str, request: Dict[str, Any]):
    """Update a research project"""
    manager = initialize_manager()
    
    project = manager.update_project(project_id, **request)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"project": project.to_dict(), "message": "Project updated successfully"}


@app.delete("/api/research/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a research project"""
    manager = initialize_manager()
    
    success = manager.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": "Project deleted successfully"}


# Idea Endpoints

@app.post("/api/research/projects/{project_id}/ideas")
async def add_idea(project_id: str, request: Dict[str, Any]):
    """Add a new research idea to a project"""
    manager = initialize_manager()
    
    idea = manager.add_idea(
        project_id=project_id,
        title=request.get('title'),
        description=request.get('description', ''),
        domain=request.get('domain', ''),
        keywords=request.get('keywords', []),
        novelty_score=request.get('novelty_score', 0.0),
        feasibility_score=request.get('feasibility_score', 0.0),
        impact_score=request.get('impact_score', 0.0)
    )
    
    if not idea:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"idea": idea.to_dict(), "message": "Idea added successfully"}


@app.put("/api/research/projects/{project_id}/ideas/{idea_id}/status")
async def update_idea_status(project_id: str, idea_id: str, request: Dict[str, str]):
    """Update the status of a research idea"""
    manager = initialize_manager()
    
    success = manager.update_idea_status(
        project_id=project_id,
        idea_id=idea_id,
        status=request.get('status')
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Idea or project not found")
    
    return {"message": "Idea status updated successfully"}


# Experiment Endpoints

@app.post("/api/research/projects/{project_id}/experiments")
async def create_experiment(project_id: str, request: Dict[str, Any]):
    """Create a new experiment"""
    manager = initialize_manager()
    
    experiment = manager.create_experiment(
        project_id=project_id,
        name=request.get('name'),
        description=request.get('description', ''),
        code=request.get('code'),
        parameters=request.get('parameters', {}),
        config=request.get('config', {})
    )
    
    if not experiment:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"experiment": experiment.to_dict(), "message": "Experiment created successfully"}


@app.post("/api/research/experiments/{experiment_id}/run")
async def run_experiment(experiment_id: str):
    """Run an experiment"""
    manager = initialize_manager()
    
    experiment = manager.run_experiment(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found or already completed")
    
    return {"experiment": experiment.to_dict(), "message": "Experiment executed successfully"}


@app.post("/api/research/experiments/{experiment_id}/cancel")
async def cancel_experiment(experiment_id: str):
    """Cancel a running experiment"""
    manager = initialize_manager()
    
    success = manager.cancel_experiment(experiment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Experiment not found or not running")
    
    return {"message": "Experiment cancelled successfully"}


# Literature Endpoints

@app.post("/api/research/literature/search")
async def search_literature(request: Dict[str, Any]):
    """Search for academic literature"""
    manager = initialize_manager()
    
    search_result = manager.search_literature(
        query=request.get('query', ''),
        source=request.get('source', 'semantic_scholar'),
        max_results=request.get('max_results', 10)
    )
    
    return {"search": search_result.to_dict()}


@app.post("/api/research/projects/{project_id}/literature")
async def add_paper_to_project(project_id: str, request: Dict[str, Any]):
    """Add a paper to a project's literature collection"""
    manager = initialize_manager()
    
    success = manager.add_paper_to_project(
        project_id=project_id,
        paper_data=request
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": "Paper added to project successfully"}


# Social Features

@app.post("/api/research/projects/{project_id}/star")
async def star_project(project_id: str, request: Dict[str, str] = None):
    """Star/unstar a research project"""
    manager = initialize_manager()
    
    user_id = (request or {}).get('user_id', 'demo_user')
    success = manager.star_project(project_id, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    
    starred = manager.is_starred(project_id, user_id)
    return {"starred": starred, "message": f"Project {'starred' if starred else 'unstarred'}"}


@app.get("/api/research/projects/{project_id}/starred")
async def check_starred(project_id: str, user_id: str = Query("demo_user")):
    """Check if a project is starred by a user"""
    manager = initialize_manager()
    
    starred = manager.is_starred(project_id, user_id)
    return {"starred": starred}


@app.post("/api/research/projects/{project_id}/fork")
async def fork_project(project_id: str, request: Dict[str, str]):
    """Fork a research project"""
    manager = initialize_manager()
    
    new_project = manager.fork_project(
        project_id=project_id,
        new_namespace=request.get('new_namespace', 'demo'),
        new_name=request.get('new_name', 'Forked Project')
    )
    
    if not new_project:
        raise HTTPException(status_code=404, detail="Original project not found")
    
    return {"project": new_project.to_dict(), "message": "Project forked successfully"}


# Statistics and Analytics

@app.get("/api/research/stats")
async def get_stats():
    """Get platform statistics"""
    manager = initialize_manager()
    
    stats = manager.get_platform_stats()
    return stats


@app.get("/api/research/domains")
async def get_domains():
    """Get available research domains"""
    manager = initialize_manager()
    
    domains = set()
    for project in manager._projects.values():
        if project.domain:
            domains.add(project.domain)
    
    return {"domains": sorted(list(domains))}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3004)
