"""
Octopai Evolution API - Self-Evolving AI Agent System

FastAPI backend for Octopai's self-evolution capabilities.
"""

import os
import asyncio
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from evolution_core import EvolutionEngine, EvolutionConfig
from program_registry import ProgramManager, ProgramConfig, ProgramMetadata


app = FastAPI(
    title="Octopai Evolution API",
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


# Global state for evolution engine
evolution_engine: Optional[EvolutionEngine] = None
program_manager: Optional[ProgramManager] = None
evolution_task: Optional[asyncio.Task] = None
is_running = False


def initialize_systems():
    """Initialize evolution engine and program manager"""
    global evolution_engine, program_manager
    
    if evolution_engine is None:
        evolution_engine = EvolutionEngine()
    
    if program_manager is None:
        program_manager = ProgramManager()


# Request/Response Models
class EvolutionStartRequest(BaseModel):
    max_iterations: Optional[int] = 20
    evolution_mode: Optional[str] = "skill_only"
    continue_mode: Optional[bool] = False


class EvolutionStatusResponse(BaseModel):
    iteration: int
    max_iterations: int
    frontier: List[Dict[str, Any]]
    total_cost: float
    is_running: bool
    config: Dict[str, Any]


class ProgramListResponse(BaseModel):
    programs: List[str]
    current_program: Optional[str]
    frontier: List[Dict[str, Any]]


class ProgramDetailResponse(BaseModel):
    name: str
    metadata: Dict[str, Any]
    system_prompt: str
    skills: List[str]
    allowed_tools: List[str]


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Octopai Evolution API",
        "version": "1.0.0",
        "status": "running",
        "capabilities": [
            "Self-Evolving AI Agent",
            "Program Version Management",
            "Frontier Tracking",
            "Skill Evolution"
        ]
    }


@app.get("/api/health")
async def health_check():
    initialize_systems()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "systems": {
            "evolution_engine": evolution_engine is not None,
            "program_manager": program_manager is not None
        }
    }


# Evolution endpoints
@app.get("/api/evolution/status", response_model=EvolutionStatusResponse)
async def get_evolution_status():
    """Get current evolution status"""
    initialize_systems()
    
    status = evolution_engine.get_status()
    
    return EvolutionStatusResponse(
        iteration=status["iteration"],
        max_iterations=status["max_iterations"],
        frontier=[{"name": name, "score": score} for name, score in status["frontier"]],
        total_cost=status["total_cost"],
        is_running=is_running,
        config=status["config"]
    )


@app.post("/api/evolution/start")
async def start_evolution(request: EvolutionStartRequest):
    """Start the evolution loop"""
    global evolution_engine, evolution_task, is_running
    
    initialize_systems()
    
    if is_running:
        raise HTTPException(status_code=400, detail="Evolution already running")
    
    # Create config
    config = EvolutionConfig(
        max_iterations=request.max_iterations or 20,
        evolution_mode=request.evolution_mode or "skill_only",
        continue_mode=request.continue_mode or False
    )
    
    evolution_engine = EvolutionEngine(config)
    is_running = True
    
    # Start evolution in background
    async def run_evolution():
        global is_running
        try:
            await evolution_engine.run()
        finally:
            is_running = False
    
    evolution_task = asyncio.create_task(run_evolution())
    
    return {
        "status": "started",
        "message": "Evolution loop started",
        "config": {
            "max_iterations": config.max_iterations,
            "evolution_mode": config.evolution_mode,
            "continue_mode": config.continue_mode
        }
    }


@app.post("/api/evolution/stop")
async def stop_evolution():
    """Stop the evolution loop"""
    global evolution_task, is_running
    
    if not is_running:
        raise HTTPException(status_code=400, detail="Evolution not running")
    
    if evolution_task:
        evolution_task.cancel()
        try:
            await evolution_task
        except asyncio.CancelledError:
            pass
    
    is_running = False
    
    return {
        "status": "stopped",
        "message": "Evolution loop stopped"
    }


@app.post("/api/evolution/reset")
async def reset_evolution():
    """Reset evolution engine state"""
    global evolution_engine, program_manager, is_running
    
    if is_running:
        raise HTTPException(status_code=400, detail="Cannot reset while evolution is running")
    
    initialize_systems()
    evolution_engine.reset()
    program_manager.reset()
    
    return {
        "status": "reset",
        "message": "Evolution system reset"
    }


# Program Registry endpoints
@app.get("/api/programs", response_model=ProgramListResponse)
async def list_programs():
    """List all programs"""
    initialize_systems()
    
    programs = program_manager.list_programs()
    current = program_manager._current_program
    frontier = program_manager.get_frontier_with_scores()
    
    return ProgramListResponse(
        programs=programs,
        current_program=current,
        frontier=[{"name": name, "score": score} for name, score in frontier]
    )


@app.get("/api/programs/{name}", response_model=ProgramDetailResponse)
async def get_program(name: str):
    """Get details of a specific program"""
    initialize_systems()
    
    program = program_manager.get_program(name)
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    
    return ProgramDetailResponse(
        name=program.metadata.name,
        metadata=program.metadata.to_dict(),
        system_prompt=program.system_prompt,
        skills=program.skills,
        allowed_tools=program.allowed_tools
    )


@app.post("/api/programs/{name}/switch")
async def switch_program(name: str):
    """Switch to a different program"""
    initialize_systems()
    
    success = program_manager.switch_to(name)
    if not success:
        raise HTTPException(status_code=404, detail="Program not found")
    
    return {
        "status": "switched",
        "program": name
    }


@app.delete("/api/programs/{name}")
async def delete_program(name: str):
    """Delete a program"""
    initialize_systems()
    
    program = program_manager.get_program(name)
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    
    program_manager.discard(name)
    
    return {
        "status": "deleted",
        "program": name
    }


# Initialize baseline program on startup
@app.on_event("startup")
async def startup_event():
    """Initialize baseline program on startup"""
    initialize_systems()
    
    # Create baseline program if it doesn't exist
    if "baseline" not in program_manager.list_programs():
        baseline_metadata = ProgramMetadata(
            name="baseline",
            description="Initial baseline program",
            tags=["baseline", "initial"]
        )
        baseline_config = ProgramConfig(
            metadata=baseline_metadata,
            system_prompt="You are a helpful AI assistant.",
            allowed_tools=[],
            skills=[]
        )
        program_manager.create_program("baseline", baseline_config)
        program_manager.update_frontier("baseline", 0.42)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3002)
