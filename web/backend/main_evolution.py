"""
Octopai Evolution Engine API Server
FastAPI application for self-evolving agent management
This module serves as the API layer, calling the core Octopai Agents engine
"""

import sys
import os

# Add parent directory to path to import octopai core modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uuid
import random

# Import from Octopai core agents module
from octopai.agents import EvolutionEngineManager

app = FastAPI(
    title="Octopai AI Agents Evolution Engine API",
    description="Self-Evolving Agent System - Continuous learning and feedback descent optimization",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

evolution_manager = None

def initialize_manager():
    global evolution_manager
    if evolution_manager is None:
        # Use data directory in web backend folder for compatibility
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.octopai_data', 'evolution')
        evolution_manager = EvolutionEngineManager(data_dir=data_dir)
        _seed_sample_agents()
    return evolution_manager


def _seed_sample_agents():
    global evolution_manager
    
    sample_agents = [
        {
            "name": "General Purpose Agent",
            "agent_type": "general",
            "model_name": "gpt-4",
            "visibility": "public",
            "created_by": "system",
            "evolution_config": {
                "strategy": "feedback_descent",
                "learning_rate": 0.1,
                "exploration_rate": 0.3,
                "max_iterations": 50
            }
        },
        {
            "name": "Research Assistant Pro",
            "agent_type": "researcher",
            "model_name": "gpt-4-turbo",
            "visibility": "public",
            "created_by": "system",
            "evolution_config": {
                "strategy": "gradient_ascent",
                "learning_rate": 0.15,
                "exploration_rate": 0.4,
                "max_iterations": 40
            }
        },
        {
            "name": "Code Architect AI",
            "agent_type": "developer",
            "model_name": "claude-3-opus",
            "visibility": "public",
            "created_by": "system",
            "evolution_config": {
                "strategy": "genetic_crossover",
                "learning_rate": 0.12,
                "exploration_rate": 0.35,
                "max_iterations": 60
            }
        },
        {
            "name": "Data Analyst Expert",
            "agent_type": "analyst",
            "model_name": "gpt-4",
            "visibility": "private",
            "created_by": "demo_user",
            "evolution_config": {
                "strategy": "mutation_based",
                "learning_rate": 0.08,
                "exploration_rate": 0.25,
                "max_iterations": 45
            }
        }
    ]
    
    for agent_data in sample_agents:
        agent = evolution_manager.create_agent(**agent_data)
        
        # Execute some initial tasks
        for i in range(random.randint(3, 8)):
            tasks = [
                ("Analyze dataset and generate insights", "data_analysis"),
                ("Research latest developments in AI", "research"),
                ("Generate optimized Python code", "code_generation"),
                ("Create comprehensive report", "communication")
            ]
            task_type = random.choice(tasks)
            evolution_manager.execute_task(
                agent_id=agent.agent_id,
                task_description=task_type[0],
                task_type=task_type[1]
            )
        
        # Run initial evolution
        if random.random() > 0.5:
            evolution_manager.start_evolution(agent.agent_id)


# Agent Endpoints

@app.post("/api/evolution/agents")
async def create_agent(request: Dict[str, Any]):
    manager = initialize_manager()
    
    agent = manager.create_agent(
        name=request.get('name', 'New Agent'),
        agent_type=request.get('agent_type', 'general'),
        model_name=request.get('model_name', 'gpt-4'),
        visibility=request.get('visibility', 'private'),
        created_by=request.get('created_by', 'user'),
        evolution_config=request.get('evolution_config')
    )
    
    return {"agent": agent.to_dict(), "message": "Agent created successfully"}


@app.get("/api/evolution/agents")
async def list_agents(
    visibility: str = Query(None),
    status: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    manager = initialize_manager()
    
    agents, total = manager.list_agents(
        visibility=visibility,
        status=status,
        page=page,
        page_size=page_size
    )
    
    return {
        "agents": [a.to_dict() for a in agents],
        "total": total,
        "page": page,
        "page_size": page_size
    }


@app.get("/api/evolution/agents/{agent_id}")
async def get_agent(agent_id: str = Path(...)):
    manager = initialize_manager()
    
    agent = manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {"agent": agent.to_dict()}


@app.delete("/api/evolution/agents/{agent_id}")
async def delete_agent(agent_id: str):
    manager = initialize_manager()
    
    success = manager.delete_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {"message": "Agent deleted successfully"}


# Evolution Loop Endpoints

@app.post("/api/evolution/agents/{agent_id}/evolve")
async def start_evolution(agent_id: str, request: Dict[str, Any] = None):
    manager = initialize_manager()
    
    run = manager.start_evolution(
        agent_id=agent_id,
        config=(request or {})
    )
    
    if not run:
        raise HTTPException(status_code=400, detail="Cannot start evolution (check if enabled)")
    
    return {"run": run.to_dict(), "message": "Evolution cycle started"}


# Task Execution Endpoints

@app.post("/api/evolution/agents/{agent_id}/tasks")
async def execute_task(agent_id: str, request: Dict[str, Any]):
    manager = initialize_manager()
    
    execution = manager.execute_task(
        agent_id=agent_id,
        task_description=request.get('task_description', ''),
        task_type=request.get('task_type', 'general')
    )
    
    if not execution:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {"execution": execution.to_dict(), "message": "Task executed"}


# Social Features

@app.post("/api/evolution/agents/{agent_id}/star")
async def star_agent(agent_id: str, request: Dict[str, str] = None):
    manager = initialize_manager()
    
    user_id = (request or {}).get('user_id', 'demo_user')
    success = manager.star_agent(agent_id, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    starred = manager.is_starred(agent_id, user_id)
    return {"starred": starred, "message": f"Agent {'starred' if starred else 'unstarred'}"}


@app.post("/api/evolution/agents/{agent_id}/fork")
async def fork_agent(agent_id: str, request: Dict[str, str]):
    manager = initialize_manager()
    
    new_agent = manager.fork_agent(
        agent_id=agent_id,
        new_name=request.get('new_name', f'Forked Agent {uuid.uuid4().hex[:8]}'),
        owner_id=request.get('owner_id', 'user')
    )
    
    if not new_agent:
        raise HTTPException(status_code=404, detail="Original agent not found")
    
    return {"agent": new_agent.to_dict(), "message": "Agent forked successfully"}


# Advanced Feature Endpoints

@app.get("/api/evolution/templates")
async def get_templates():
    """Get all available skill templates for evolution"""
    manager = initialize_manager()
    return {"templates": manager.get_available_templates()}


@app.get("/api/evolution/agents/{agent_id}/performance")
async def get_agent_performance(agent_id: str):
    """Get performance history/trend for an agent"""
    manager = initialize_manager()
    
    history = manager.get_agent_performance_history(agent_id)
    
    return {
        "agent_id": agent_id,
        "performance_history": history,
        "total_records": len(history)
    }


@app.get("/api/evolution/agents/{agent_id}/evolution-tree")
async def get_evolution_tree(agent_id: str):
    """Get skill evolution tree for an agent"""
    manager = initialize_manager()
    
    tree = manager.get_agent_evolution_tree(agent_id)
    agent = manager.get_agent(agent_id)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "agent_id": agent_id,
        "agent_name": agent.name,
        "evolution_tree": tree,
        "current_generation": agent.current_generation,
        "total_skills_created": agent.total_skills_created
    }


@app.get("/api/evolution/agents/{agent_id}/skills")
async def get_agent_skills(agent_id: str):
    """Get all skills for an agent with detailed metrics"""
    manager = initialize_manager()
    
    agent = manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    skills_with_eval = []
    for skill in agent.skills:
        eval_result = manager.evaluator.evaluate_skill(skill)
        skills_with_eval.append({
            **skill.to_dict(),
            "evaluation": eval_result
        })
    
    return {
        "agent_id": agent_id,
        "skills": skills_with_eval,
        "total": len(skills_with_eval),
        "active_count": sum(1 for s in skills_with_eval if s['is_active'])
    }


@app.get("/api/evolution/agents/{agent_id}/feedback")
async def get_agent_feedback(agent_id: str):
    """Get recent feedback buffer for an agent"""
    manager = initialize_manager()
    
    agent = manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "agent_id": agent_id,
        "feedback_buffer": agent.feedback_buffer,
        "total_signals": len(agent.feedback_buffer)
    }


# Statistics Endpoints

@app.get("/api/evolution/stats")
async def get_stats():
    manager = initialize_manager()
    
    stats = manager.get_platform_stats()
    return stats


@app.get("/api/evolution/agent-types")
async def get_agent_types():
    return {
        "types": [
            {"id": "general", "name": "General Purpose", "description": "Versatile agent for various tasks"},
            {"id": "researcher", "name": "Researcher", "description": "Specialized in research and analysis"},
            {"id": "developer", "name": "Developer", "description": "Focused on code generation and software engineering"},
            {"id": "analyst", "name": "Data Analyst", "description": "Expert in data analysis and visualization"}
        ]
    }


@app.get("/api/evolution/strategies")
async def get_evolution_strategies():
    """Get available evolution strategies"""
    return {
        "strategies": [
            {"id": "feedback_descent", "name": "Feedback Descent", "description": "Optimize using gradient-based feedback signals"},
            {"id": "gradient_ascent", "name": "Gradient Ascent", "description": "Climb towards higher quality states"},
            {"id": "genetic_crossover", "name": "Genetic Crossover", "description": "Combine successful skill patterns"},
            {"id": "mutation_based", "name": "Mutation Based", "description": "Introduce controlled variations"},
            {"id": "ensemble_evolution", "name": "Ensemble Evolution", "description": "Multiple strategies working together"}
        ]
    }


# Import and register new AI Evolution API routes
from api_evolution import router as evolution_v1_router
app.include_router(evolution_v1_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3005)
