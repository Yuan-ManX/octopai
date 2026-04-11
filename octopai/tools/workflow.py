import os
import yaml
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
import asyncio
from enum import Enum


class WorkflowStepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowStep:
    name: str
    description: str
    action: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: List[str] = field(default_factory=list)
    condition: Optional[str] = None
    timeout: int = 300
    retry_count: int = 3
    status: WorkflowStepStatus = WorkflowStepStatus.PENDING
    result: Any = None
    error: Optional[str] = None


@dataclass
class WorkflowDefinition:
    name: str
    version: str
    description: str
    author: str
    tags: List[str] = field(default_factory=list)
    steps: List[WorkflowStep] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    on_success: Optional[str] = None
    on_failure: Optional[str] = None


class WorkflowEngine:
    def __init__(self, workflow_dir: Optional[str] = None):
        self.workflow_dir = workflow_dir or os.path.join(os.getcwd(), "workflows")
        self.registered_workflows: Dict[str, WorkflowDefinition] = {}
        self._ensure_workflow_dir()
        
    def _ensure_workflow_dir(self):
        if not os.path.exists(self.workflow_dir):
            os.makedirs(self.workflow_dir)
            
    def load_workflow(self, workflow_path: str) -> WorkflowDefinition:
        if workflow_path.endswith(".yaml") or workflow_path.endswith(".yml"):
            return self._load_yaml_workflow(workflow_path)
        elif workflow_path.endswith(".json"):
            return self._load_json_workflow(workflow_path)
        elif workflow_path.endswith(".md"):
            return self._load_markdown_workflow(workflow_path)
        else:
            raise ValueError(f"Unsupported workflow format: {workflow_path}")
            
    def _load_yaml_workflow(self, workflow_path: str) -> WorkflowDefinition:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return self._parse_workflow_dict(data)
        
    def _load_json_workflow(self, workflow_path: str) -> WorkflowDefinition:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return self._parse_workflow_dict(data)
        
    def _load_markdown_workflow(self, workflow_path: str) -> WorkflowDefinition:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        frontmatter = {}
        if frontmatter_match:
            frontmatter_str = frontmatter_match.group(1)
            frontmatter = yaml.safe_load(frontmatter_str)
            content = content[frontmatter_match.end():]
        
        data = {
            **frontmatter,
            'description': content.strip()
        }
        
        return self._parse_workflow_dict(data)
        
    def _parse_workflow_dict(self, data: Dict[str, Any]) -> WorkflowDefinition:
        steps = []
        for step_data in data.get('steps', []):
            step = WorkflowStep(
                name=step_data.get('name', ''),
                description=step_data.get('description', ''),
                action=step_data.get('action', ''),
                inputs=step_data.get('inputs', {}),
                outputs=step_data.get('outputs', []),
                condition=step_data.get('condition'),
                timeout=step_data.get('timeout', 300),
                retry_count=step_data.get('retry_count', 3)
            )
            steps.append(step)
        
        return WorkflowDefinition(
            name=data.get('name', ''),
            version=data.get('version', '1.0.0'),
            description=data.get('description', ''),
            author=data.get('author', ''),
            tags=data.get('tags', []),
            steps=steps,
            variables=data.get('variables', {}),
            on_success=data.get('on_success'),
            on_failure=data.get('on_failure')
        )
        
    def register_workflow(self, workflow: WorkflowDefinition):
        self.registered_workflows[workflow.name] = workflow
        
    def discover_workflows(self, directory: Optional[str] = None) -> List[WorkflowDefinition]:
        target_dir = directory or self.workflow_dir
        workflows = []
        
        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith(('.yaml', '.yml', '.json', '.md')) and file != 'README.md':
                    try:
                        workflow_path = os.path.join(root, file)
                        workflow = self.load_workflow(workflow_path)
                        workflows.append(workflow)
                        self.register_workflow(workflow)
                    except Exception as e:
                        print(f"Failed to load workflow {file}: {e}")
        
        return workflows
        
    async def execute_workflow(
        self,
        workflow: WorkflowDefinition,
        context: Optional[Dict[str, Any]] = None,
        step_callback: Optional[Callable[[WorkflowStep], None]] = None
    ) -> Dict[str, Any]:
        context = context or {}
        context.update(workflow.variables)
        
        results = {}
        
        for step in workflow.steps:
            if step.condition and not self._evaluate_condition(step.condition, context):
                step.status = WorkflowStepStatus.SKIPPED
                if step_callback:
                    step_callback(step)
                continue
                
            step.status = WorkflowStepStatus.RUNNING
            if step_callback:
                step_callback(step)
                
            try:
                step_result = await self._execute_step(step, context)
                step.result = step_result
                step.status = WorkflowStepStatus.COMPLETED
                
                for output_name in step.outputs:
                    if output_name in step_result:
                        context[output_name] = step_result[output_name]
                
                results[step.name] = step_result
                
            except Exception as e:
                step.error = str(e)
                step.status = WorkflowStepStatus.FAILED
                
                if step.retry_count > 0:
                    for attempt in range(step.retry_count):
                        try:
                            step_result = await self._execute_step(step, context)
                            step.result = step_result
                            step.status = WorkflowStepStatus.COMPLETED
                            results[step.name] = step_result
                            break
                        except Exception as retry_e:
                            if attempt == step.retry_count - 1:
                                raise retry_e
                
                if step.status == WorkflowStepStatus.FAILED:
                    if workflow.on_failure:
                        context['error'] = str(e)
                        await self._execute_handler(workflow.on_failure, context)
                    raise
                
            if step_callback:
                step_callback(step)
        
        if workflow.on_success:
            await self._execute_handler(workflow.on_success, context)
            
        return results
        
    async def _execute_step(self, step: WorkflowStep, context: Dict[str, Any]) -> Any:
        resolved_inputs = self._resolve_variables(step.inputs, context)
        
        if step.action.startswith('python:'):
            return await self._execute_python_action(step.action[7:], resolved_inputs, context)
        elif step.action.startswith('skill:'):
            return await self._execute_skill_action(step.action[6:], resolved_inputs, context)
        elif step.action.startswith('api:'):
            return await self._execute_api_action(step.action[4:], resolved_inputs, context)
        else:
            raise ValueError(f"Unknown action type: {step.action}")
            
    def _resolve_variables(self, data: Any, context: Dict[str, Any]) -> Any:
        if isinstance(data, str):
            import re
            pattern = r'\$\{(\w+)\}'
            return re.sub(pattern, lambda m: str(context.get(m.group(1), m.group(0))), data)
        elif isinstance(data, dict):
            return {k: self._resolve_variables(v, context) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._resolve_variables(item, context) for item in data]
        return data
        
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        try:
            resolved = self._resolve_variables(condition, context)
            return eval(resolved, {}, context)
        except:
            return False
            
    async def _execute_python_action(self, action: str, inputs: Dict[str, Any], context: Dict[str, Any]) -> Any:
        import importlib
        try:
            module_name, function_name = action.split(':')
            module = importlib.import_module(module_name)
            func = getattr(module, function_name)
            
            if asyncio.iscoroutinefunction(func):
                return await func(**inputs, context=context)
            else:
                return func(**inputs, context=context)
        except Exception as e:
            raise RuntimeError(f"Failed to execute Python action {action}: {e}")
            
    async def _execute_skill_action(self, skill_name: str, inputs: Dict[str, Any], context: Dict[str, Any]) -> Any:
        from octopai.skills.factory import SkillFactory
        factory = SkillFactory()
        skill = factory.load_skill(skill_name)
        
        if not skill:
            raise ValueError(f"Skill not found: {skill_name}")
            
        result = await skill.execute(**inputs)
        return result
        
    async def _execute_api_action(self, endpoint: str, inputs: Dict[str, Any], context: Dict[str, Any]) -> Any:
        import httpx
        
        method = inputs.get('method', 'GET').upper()
        url = self._resolve_variables(endpoint, context)
        headers = inputs.get('headers', {})
        params = inputs.get('params', {})
        data = inputs.get('data', {})
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            if method == 'GET':
                response = await client.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = await client.post(url, headers=headers, params=params, json=data)
            elif method == 'PUT':
                response = await client.put(url, headers=headers, params=params, json=data)
            elif method == 'DELETE':
                response = await client.delete(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
            
    async def _execute_handler(self, handler: str, context: Dict[str, Any]):
        if handler.startswith('python:'):
            await self._execute_python_action(handler[7:], {}, context)
        elif handler.startswith('skill:'):
            await self._execute_skill_action(handler[6:], {}, context)
