import asyncio
import uuid
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class SubtaskStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


@dataclass
class Subtask:
    id: str
    name: str
    description: str
    task_type: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    timeout: int = 300
    retry_count: int = 3
    priority: int = 0
    status: SubtaskStatus = SubtaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    execution_time: float = 0.0


@dataclass
class SubtaskGroup:
    id: str
    name: str
    subtasks: List[Subtask] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    max_concurrent: int = 3
    on_group_complete: Optional[Callable[[], Any]] = None
    on_task_complete: Optional[Callable[[Subtask], Any]] = None


class SubtaskOrchestrator:
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.subtask_groups: Dict[str, SubtaskGroup] = {}
        self.subtask_registry: Dict[str, Callable] = {}
        self._executor: Optional[ThreadPoolExecutor] = None
        
    def register_subtask_type(self, task_type: str, handler: Callable):
        self.subtask_registry[task_type] = handler
        
    def create_subtask(
        self,
        name: str,
        description: str,
        task_type: str,
        inputs: Optional[Dict[str, Any]] = None,
        dependencies: Optional[List[str]] = None,
        timeout: int = 300,
        retry_count: int = 3,
        priority: int = 0
    ) -> Subtask:
        return Subtask(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            task_type=task_type,
            inputs=inputs or {},
            dependencies=dependencies or [],
            timeout=timeout,
            retry_count=retry_count,
            priority=priority
        )
        
    def create_subtask_group(
        self,
        name: str,
        subtasks: Optional[List[Subtask]] = None,
        context: Optional[Dict[str, Any]] = None,
        max_concurrent: int = 3,
        on_group_complete: Optional[Callable[[], Any]] = None,
        on_task_complete: Optional[Callable[[Subtask], Any]] = None
    ) -> SubtaskGroup:
        group = SubtaskGroup(
            id=str(uuid.uuid4()),
            name=name,
            subtasks=subtasks or [],
            context=context or {},
            max_concurrent=max_concurrent,
            on_group_complete=on_group_complete,
            on_task_complete=on_task_complete
        )
        self.subtask_groups[group.id] = group
        return group
        
    def add_subtask_to_group(self, group_id: str, subtask: Subtask):
        if group_id not in self.subtask_groups:
            raise ValueError(f"Subtask group not found: {group_id}")
        self.subtask_groups[group_id].subtasks.append(subtask)
        
    async def decompose_task(
        self,
        main_task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> SubtaskGroup:
        context = context or {}
        
        decomposition_prompt = f"""
        请将以下任务分解为多个可并行执行的子任务：
        
        主任务：{main_task}
        
        上下文信息：
        {json.dumps(context, indent=2, ensure_ascii=False)}
        
        请返回JSON格式的子任务列表，每个子任务包含：
        - name: 子任务名称
        - description: 子任务描述
        - task_type: 子任务类型（如'research', 'analysis', 'generation', 'validation'等）
        - inputs: 子任务输入参数
        - dependencies: 依赖的其他子任务ID列表（如果没有依赖则为空）
        - priority: 优先级（数字越大优先级越高）
        - timeout: 超时时间（秒）
        - retry_count: 重试次数
        """
        
        from octopai.skills.factory import SkillFactory
        factory = SkillFactory()
        
        subtasks = []
        try:
            skill = factory.create_skill(
                name="task_decomposition",
                description="智能任务分解器",
                prompt=decomposition_prompt,
                inputs={"main_task": main_task, "context": context},
                outputs={"subtasks": List[Dict[str, Any]]}
            )
            
            result = await skill.execute()
            subtask_dicts = result.get("subtasks", [])
            
            for subtask_dict in subtask_dicts:
                subtask = self.create_subtask(
                    name=subtask_dict.get("name", ""),
                    description=subtask_dict.get("description", ""),
                    task_type=subtask_dict.get("task_type", "general"),
                    inputs=subtask_dict.get("inputs", {}),
                    dependencies=subtask_dict.get("dependencies", []),
                    priority=subtask_dict.get("priority", 0),
                    timeout=subtask_dict.get("timeout", 300),
                    retry_count=subtask_dict.get("retry_count", 3)
                )
                subtasks.append(subtask)
                
        except Exception as e:
            subtask = self.create_subtask(
                name=main_task,
                description=f"直接执行主任务: {main_task}",
                task_type="general",
                inputs={"main_task": main_task, "context": context}
            )
            subtasks.append(subtask)
            
        return self.create_subtask_group(
            name=f"Decomposed: {main_task}",
            subtasks=subtasks,
            context=context
        )
        
    async def execute_subtask_group(self, group_id: str) -> Dict[str, Any]:
        if group_id not in self.subtask_groups:
            raise ValueError(f"Subtask group not found: {group_id}")
            
        group = self.subtask_groups[group_id]
        
        subtask_map = {st.id: st for st in group.subtasks}
        completed_subtasks = set()
        results = {}
        errors = []
        
        async def execute_subtask_with_retry(subtask: Subtask) -> Any:
            for attempt in range(subtask.retry_count + 1):
                try:
                    return await self._execute_single_subtask(subtask, group.context)
                except Exception as e:
                    if attempt == subtask.retry_count:
                        raise
                    await asyncio.sleep(2 ** attempt)
                    
        def get_ready_subtasks() -> List[Subtask]:
            ready = []
            for subtask in group.subtasks:
                if subtask.status != SubtaskStatus.PENDING:
                    continue
                all_deps_completed = all(
                    dep_id in completed_subtasks 
                    for dep_id in subtask.dependencies
                )
                if all_deps_completed:
                    ready.append(subtask)
            ready.sort(key=lambda x: -x.priority)
            return ready
            
        while len(completed_subtasks) < len(group.subtasks):
            ready_subtasks = get_ready_subtasks()
            
            if not ready_subtasks:
                if len(completed_subtasks) < len(group.subtasks):
                    remaining = [st for st in group.subtasks if st.id not in completed_subtasks]
                    for st in remaining:
                        st.status = SubtaskStatus.FAILED
                        st.error = "Circular dependency or missing dependencies"
                    break
                break
                
            current_batch = ready_subtasks[:group.max_concurrent]
            
            for subtask in current_batch:
                subtask.status = SubtaskStatus.RUNNING
                subtask.started_at = time.time()
                
            tasks = [execute_subtask_with_retry(st) for st in current_batch]
            
            try:
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for subtask, result in zip(current_batch, batch_results):
                    subtask.completed_at = time.time()
                    subtask.execution_time = subtask.completed_at - subtask.started_at
                    
                    if isinstance(result, Exception):
                        subtask.status = SubtaskStatus.FAILED
                        subtask.error = str(result)
                        errors.append({"subtask_id": subtask.id, "error": str(result)})
                    else:
                        subtask.status = SubtaskStatus.COMPLETED
                        subtask.result = result
                        results[subtask.id] = result
                        
                    completed_subtasks.add(subtask.id)
                    
                    if group.on_task_complete:
                        group.on_task_complete(subtask)
                        
            except Exception as e:
                errors.append({"error": str(e)})
                
        if group.on_group_complete:
            group.on_group_complete()
            
        return {
            "group_id": group_id,
            "results": results,
            "completed_count": len(completed_subtasks),
            "total_count": len(group.subtasks),
            "errors": errors,
            "success": len(errors) == 0
        }
        
    async def _execute_single_subtask(self, subtask: Subtask, context: Dict[str, Any]) -> Any:
        if subtask.task_type in self.subtask_registry:
            handler = self.subtask_registry[subtask.task_type]
            if asyncio.iscoroutinefunction(handler):
                return await handler(**subtask.inputs, context=context)
            else:
                return handler(**subtask.inputs, context=context)
                
        from octopai.skills.factory import SkillFactory
        factory = SkillFactory()
        
        skill = factory.create_skill(
            name=f"subtask_{subtask.id}",
            description=subtask.description,
            prompt=f"执行以下任务：\n{subtask.description}\n\n输入参数：\n{json.dumps(subtask.inputs, indent=2, ensure_ascii=False)}",
            inputs=subtask.inputs,
            outputs={"result": Any}
        )
        
        result = await skill.execute()
        return result.get("result", result)
        
    def get_subtask_status(self, group_id: str, subtask_id: Optional[str] = None) -> Any:
        if group_id not in self.subtask_groups:
            raise ValueError(f"Subtask group not found: {group_id}")
            
        group = self.subtask_groups[group_id]
        
        if subtask_id:
            for subtask in group.subtasks:
                if subtask.id == subtask_id:
                    return subtask
            raise ValueError(f"Subtask not found: {subtask_id}")
            
        return group
        
    def cancel_subtask(self, group_id: str, subtask_id: str):
        if group_id not in self.subtask_groups:
            raise ValueError(f"Subtask group not found: {group_id}")
            
        group = self.subtask_groups[group_id]
        for subtask in group.subtasks:
            if subtask.id == subtask_id:
                if subtask.status in [SubtaskStatus.PENDING, SubtaskStatus.QUEUED]:
                    subtask.status = SubtaskStatus.CANCELLED
                break
                
    async def execute_parallel(
        self,
        tasks: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
        max_concurrent: int = 5
    ) -> List[Any]:
        subtasks = []
        for i, task in enumerate(tasks):
            subtask = self.create_subtask(
                name=task.get("name", f"Task {i+1}"),
                description=task.get("description", ""),
                task_type=task.get("task_type", "general"),
                inputs=task.get("inputs", {}),
                priority=task.get("priority", 0)
            )
            subtasks.append(subtask)
            
        group = self.create_subtask_group(
            name="Parallel Execution",
            subtasks=subtasks,
            context=context,
            max_concurrent=max_concurrent
        )
        
        result = await self.execute_subtask_group(group.id)
        return [result["results"].get(st.id) for st in subtasks]


import json
