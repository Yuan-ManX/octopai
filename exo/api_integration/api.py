"""
EXO Integration API - High-Level External Integration

This module provides a standardized, high-level API for integrating
EXO's proprietary skill development platform with external applications.
Features async task management and status tracking.
"""

import uuid
import threading
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future
from enum import Enum

from exo import EXO
from exo.core.pipeline import PipelineStage, PipelineResult
from exo.core.skill_factory import SkillType
from exo.api_integration.schemas import (
    CreateSkillFromURLRequest,
    CreateSkillFromFilesRequest,
    CreateSkillFromPromptRequest,
    OptimizeSkillRequest,
    PipelineStatusResponse,
    SkillInfoResponse,
    SkillListResponse,
    SkillSearchQuery,
    ErrorResponse,
    IntegrationPipelineStage
)


class TaskStatus(Enum):
    """Status of an async task"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AsyncTask:
    """Represents an asynchronous task"""
    task_id: str
    status: TaskStatus
    task_type: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    future: Optional[Future] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "task_type": self.task_type,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error
        }


class EXOIntegrationAPI:
    """
    EXO Integration API - Standardized Interface for External Applications
    
    Provides async task management, status tracking, and
    standardized data formats for external application integration.
    """
    
    def __init__(
        self,
        skill_output_dir: str = "./skills",
        skill_hub_dir: str = "./SkillHub",
        experience_dir: str = "./experiences",
        max_workers: int = 4
    ):
        """
        Initialize EXO Web API
        
        Args:
            skill_output_dir: Directory for skill output
            skill_hub_dir: Directory for SkillHub storage
            experience_dir: Directory for experience tracking
            max_workers: Maximum number of concurrent tasks
        """
        self.exo = EXO(
            skill_output_dir=skill_output_dir,
            skill_hub_dir=skill_hub_dir,
            experience_dir=experience_dir
        )
        
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: Dict[str, AsyncTask] = {}
        self._lock = threading.Lock()
        
        self._setup_pipeline_callbacks()
    
    def _setup_pipeline_callbacks(self):
        """Setup callbacks for pipeline stage updates"""
        
        def on_stage_complete(result: PipelineResult):
            """Callback for pipeline stage completion"""
            pass
        
        self.exo.pipeline.register_callback(PipelineStage.CREATION, on_stage_complete)
        self.exo.pipeline.register_callback(PipelineStage.OPTIMIZATION, on_stage_complete)
        self.exo.pipeline.register_callback(PipelineStage.PACKAGING, on_stage_complete)
        self.exo.pipeline.register_callback(PipelineStage.VALIDATION, on_stage_complete)
    
    def create_skill_from_url_async(
        self,
        request: CreateSkillFromURLRequest
    ) -> str:
        """
        Start async task to create a skill from a URL
        
        Args:
            request: Create skill from URL request
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        with self._lock:
            task = AsyncTask(
                task_id=task_id,
                status=TaskStatus.PENDING,
                task_type="create_from_url",
                created_at=datetime.now().isoformat()
            )
            self.tasks[task_id] = task
        
        def _execute():
            try:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.RUNNING
                    self.tasks[task_id].started_at = datetime.now().isoformat()
                
                result = self.exo.create_from_url(
                    url=request.url,
                    name=request.name,
                    description=request.description,
                    tags=request.tags,
                    category=request.category,
                    author=request.author,
                    skill_type=SkillType(request.skill_type)
                )
                
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.COMPLETED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].result = result
                
            except Exception as e:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.FAILED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].error = str(e)
        
        future = self.executor.submit(_execute)
        
        with self._lock:
            self.tasks[task_id].future = future
        
        return task_id
    
    def create_skill_from_files_async(
        self,
        request: CreateSkillFromFilesRequest
    ) -> str:
        """
        Start async task to create a skill from files
        
        Args:
            request: Create skill from files request
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        with self._lock:
            task = AsyncTask(
                task_id=task_id,
                status=TaskStatus.PENDING,
                task_type="create_from_files",
                created_at=datetime.now().isoformat()
            )
            self.tasks[task_id] = task
        
        def _execute():
            try:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.RUNNING
                    self.tasks[task_id].started_at = datetime.now().isoformat()
                
                result = self.exo.create_from_files(
                    file_paths=request.files,
                    name=request.name,
                    description=request.description,
                    tags=request.tags,
                    category=request.category,
                    author=request.author,
                    skill_type=SkillType(request.skill_type)
                )
                
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.COMPLETED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].result = result
                
            except Exception as e:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.FAILED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].error = str(e)
        
        future = self.executor.submit(_execute)
        
        with self._lock:
            self.tasks[task_id].future = future
        
        return task_id
    
    def create_skill_from_prompt_async(
        self,
        request: CreateSkillFromPromptRequest
    ) -> str:
        """
        Start async task to create a skill from a prompt
        
        Args:
            request: Create skill from prompt request
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        with self._lock:
            task = AsyncTask(
                task_id=task_id,
                status=TaskStatus.PENDING,
                task_type="create_from_prompt",
                created_at=datetime.now().isoformat()
            )
            self.tasks[task_id] = task
        
        def _execute():
            try:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.RUNNING
                    self.tasks[task_id].started_at = datetime.now().isoformat()
                
                result = self.exo.create_from_prompt(
                    prompt=request.prompt,
                    name=request.name,
                    description=request.description,
                    tags=request.tags,
                    category=request.category,
                    author=request.author,
                    skill_type=SkillType(request.skill_type),
                    resources=request.resources
                )
                
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.COMPLETED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].result = result
                
            except Exception as e:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.FAILED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].error = str(e)
        
        future = self.executor.submit(_execute)
        
        with self._lock:
            self.tasks[task_id].future = future
        
        return task_id
    
    def optimize_skill_async(
        self,
        request: OptimizeSkillRequest
    ) -> str:
        """
        Start async task to optimize a skill
        
        Args:
            request: Optimize skill request
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        with self._lock:
            task = AsyncTask(
                task_id=task_id,
                status=TaskStatus.PENDING,
                task_type="optimize_skill",
                created_at=datetime.now().isoformat()
            )
            self.tasks[task_id] = task
        
        def _execute():
            try:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.RUNNING
                    self.tasks[task_id].started_at = datetime.now().isoformat()
                
                result = self.exo.optimize_skill(
                    skill_dir=request.skill_dir
                )
                
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.COMPLETED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].result = result
                
            except Exception as e:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.FAILED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].error = str(e)
        
        future = self.executor.submit(_execute)
        
        with self._lock:
            self.tasks[task_id].future = future
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[AsyncTask]:
        """
        Get status of an async task
        
        Args:
            task_id: Task ID to query
            
        Returns:
            AsyncTask object or None if not found
        """
        with self._lock:
            return self.tasks.get(task_id)
    
    def get_pipeline_status_from_task(self, task_id: str) -> Optional[PipelineStatusResponse]:
        """
        Get pipeline status from a task
        
        Args:
            task_id: Task ID to query
            
        Returns:
            PipelineStatusResponse or None
        """
        task = self.get_task_status(task_id)
        if not task:
            return None
        
        web_status = self._map_task_status_to_integration(task.status)
        
        response = PipelineStatusResponse(
            request_id=task_id,
            status=web_status,
            started_at=task.created_at
        )
        
        if task.started_at:
            response.started_at = task.started_at
        
        if task.completed_at:
            response.completed_at = task.completed_at
        
        if task.error:
            response.errors = [task.error]
        
        if task.result and isinstance(task.result, PipelineResult):
            result = task.result
            response.skill_id = result.skill_id
            response.skill_dir = result.skill_dir
            response.errors = result.errors
            response.warnings = result.warnings
            response.metrics = result.metrics
            
            if result.success:
                response.status = IntegrationPipelineStage.COMPLETED
            else:
                response.status = IntegrationPipelineStage.FAILED
        
        return response
    
    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[AsyncTask]:
        """
        List all tasks, optionally filtered by status
        
        Args:
            status: Optional status filter
            
        Returns:
            List of AsyncTask objects
        """
        with self._lock:
            if status:
                return [t for t in self.tasks.values() if t.status == status]
            return list(self.tasks.values())
    
    def get_skill_info(self, skill_id: str) -> Optional[SkillInfoResponse]:
        """
        Get information about a skill
        
        Args:
            skill_id: Skill ID to query
            
        Returns:
            SkillInfoResponse or None
        """
        skill = self.exo.get_skill_from_hub(skill_id)
        if not skill:
            return None
        
        experience = self.exo.get_skill_experience(skill_id)
        
        response = SkillInfoResponse(
            skill_id=skill_id,
            name=skill.name,
            description=getattr(skill, 'description', ''),
            skill_type='general',
            tags=getattr(skill, 'tags', []),
            path=getattr(skill, 'path', None)
        )
        
        if experience:
            response.usage_count = experience.total_interactions
            response.success_rate = experience.success_rate
        
        return response
    
    def list_skills(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> SkillListResponse:
        """
        List skills with pagination
        
        Args:
            category: Optional category filter
            tags: Optional tag filter
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            SkillListResponse
        """
        skills = self.exo.list_skills_in_hub(category, tags, limit + offset)
        
        skill_infos = []
        for skill in skills[offset:offset + limit]:
            info = self.get_skill_info(skill.skill_id if hasattr(skill, 'skill_id') else skill.name)
            if info:
                skill_infos.append(info)
        
        return SkillListResponse(
            skills=skill_infos,
            total=len(skills),
            page=(offset // limit) + 1,
            page_size=limit
        )
    
    def search_skills(self, query: SkillSearchQuery) -> SkillListResponse:
        """
        Search for skills
        
        Args:
            query: Search query
            
        Returns:
            SkillListResponse
        """
        skills = self.exo.search_skills_in_hub(
            query=query.query,
            tags=query.tags,
            category=query.category,
            limit=query.limit
        )
        
        skill_infos = []
        for skill in skills:
            info = self.get_skill_info(skill.skill_id if hasattr(skill, 'skill_id') else skill.name)
            if info:
                skill_infos.append(info)
        
        return SkillListResponse(
            skills=skill_infos,
            total=len(skill_infos),
            page=1,
            page_size=query.limit
        )
    
    def get_insights(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get experience insights
        
        Args:
            skill_id: Optional specific skill to analyze
            
        Returns:
            Dictionary of insights
        """
        return self.exo.get_experience_insights(skill_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a pending or running task
        
        Args:
            task_id: Task ID to cancel
            
        Returns:
            True if successful
        """
        with self._lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            if task.future and not task.future.done():
                task.future.cancel()
                task.status = TaskStatus.FAILED
                task.error = "Task cancelled by user"
                return True
            
            return False
    
    def cleanup_completed_tasks(self, older_than_hours: int = 24):
        """
        Clean up old completed tasks
        
        Args:
            older_than_hours: Remove tasks older than this
        """
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(hours=older_than_hours)
        
        with self._lock:
            to_remove = []
            for task_id, task in self.tasks.items():
                if task.completed_at:
                    completed = datetime.fromisoformat(task.completed_at)
                    if completed < cutoff:
                        to_remove.append(task_id)
            
            for task_id in to_remove:
                del self.tasks[task_id]
    
    def _map_task_status_to_integration(self, status: TaskStatus) -> IntegrationPipelineStage:
        """Map internal task status to integration API status"""
        mapping = {
            TaskStatus.PENDING: IntegrationPipelineStage.PENDING,
            TaskStatus.RUNNING: IntegrationPipelineStage.CREATION,
            TaskStatus.COMPLETED: IntegrationPipelineStage.COMPLETED,
            TaskStatus.FAILED: IntegrationPipelineStage.FAILED
        }
        return mapping.get(status, IntegrationPipelineStage.PENDING)
    
    def shutdown(self, wait: bool = True):
        """
        Shutdown the executor
        
        Args:
            wait: Whether to wait for running tasks
        """
        self.executor.shutdown(wait=wait)
