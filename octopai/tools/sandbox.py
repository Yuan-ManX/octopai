import os
import tempfile
import subprocess
import asyncio
import uuid
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
import json
import shutil
from enum import Enum


class SandboxMode(Enum):
    LOCAL = "local"
    ISOLATED = "isolated"


class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class SandboxConfig:
    mode: SandboxMode = SandboxMode.LOCAL
    timeout: int = 300
    max_memory_mb: int = 1024
    max_cpu_cores: float = 1.0
    allowed_commands: List[str] = field(default_factory=list)
    blocked_commands: List[str] = field(default_factory=list)
    enable_network: bool = False
    workspace_dir: Optional[str] = None


@dataclass
class ExecutionResult:
    success: bool
    status: ExecutionStatus
    stdout: str
    stderr: str
    return_code: int
    execution_time: float
    output_files: List[str] = field(default_factory=list)
    error_message: Optional[str] = None


@dataclass
class SandboxSession:
    id: str
    config: SandboxConfig
    workspace_path: str
    created_at: float
    active: bool = True
    execution_history: List[ExecutionResult] = field(default_factory=list)


class SandboxExecutor:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.path.join(os.getcwd(), "sandbox")
        self.sessions: Dict[str, SandboxSession] = {}
        self._ensure_base_dir()
        
    def _ensure_base_dir(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            
    def create_session(
        self,
        config: Optional[SandboxConfig] = None,
        session_id: Optional[str] = None
    ) -> SandboxSession:
        config = config or SandboxConfig()
        session_id = session_id or str(uuid.uuid4())
        
        workspace_path = os.path.join(self.base_dir, f"session_{session_id}")
        os.makedirs(workspace_path, exist_ok=True)
        
        subdirs = ["uploads", "workspace", "outputs", "skills"]
        for subdir in subdirs:
            os.makedirs(os.path.join(workspace_path, subdir), exist_ok=True)
            
        session = SandboxSession(
            id=session_id,
            config=config,
            workspace_path=workspace_path,
            created_at=asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0
        )
        
        self.sessions[session_id] = session
        return session
        
    def get_session(self, session_id: str) -> Optional[SandboxSession]:
        return self.sessions.get(session_id)
        
    def close_session(self, session_id: str):
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.active = False
            if os.path.exists(session.workspace_path):
                shutil.rmtree(session.workspace_path, ignore_errors=True)
            del self.sessions[session_id]
            
    def write_file(
        self,
        session_id: str,
        file_path: str,
        content: str,
        encoding: str = "utf-8"
    ) -> str:
        session = self._get_session_or_raise(session_id)
        full_path = self._resolve_path(session, file_path)
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding=encoding) as f:
            f.write(content)
            
        return full_path
        
    def read_file(
        self,
        session_id: str,
        file_path: str,
        encoding: str = "utf-8"
    ) -> str:
        session = self._get_session_or_raise(session_id)
        full_path = self._resolve_path(session, file_path)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(full_path, 'r', encoding=encoding) as f:
            return f.read()
            
    def list_files(
        self,
        session_id: str,
        directory: str = "."
    ) -> List[Dict[str, Any]]:
        session = self._get_session_or_raise(session_id)
        full_path = self._resolve_path(session, directory)
        
        if not os.path.exists(full_path):
            return []
            
        files = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            stat = os.stat(item_path)
            files.append({
                "name": item,
                "path": os.path.relpath(item_path, session.workspace_path),
                "is_dir": os.path.isdir(item_path),
                "size": stat.st_size,
                "modified": stat.st_mtime
            })
            
        return files
        
    def delete_file(
        self,
        session_id: str,
        file_path: str
    ) -> bool:
        session = self._get_session_or_raise(session_id)
        full_path = self._resolve_path(session, file_path)
        
        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
            return True
        return False
        
    async def execute_command(
        self,
        session_id: str,
        command: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> ExecutionResult:
        session = self._get_session_or_raise(session_id)
        timeout = timeout or session.config.timeout
        
        if not self._is_command_allowed(session, command):
            return ExecutionResult(
                success=False,
                status=ExecutionStatus.FAILED,
                stdout="",
                stderr=f"Command not allowed: {command}",
                return_code=-1,
                execution_time=0,
                error_message="Command blocked by security policy"
            )
            
        work_dir = self._resolve_path(session, cwd or "workspace")
        os.makedirs(work_dir, exist_ok=True)
        
        full_env = os.environ.copy()
        if env:
            full_env.update(env)
            
        start_time = asyncio.get_event_loop().time()
        
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=work_dir,
                env=full_env
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                end_time = asyncio.get_event_loop().time()
                return ExecutionResult(
                    success=False,
                    status=ExecutionStatus.TIMEOUT,
                    stdout="",
                    stderr=f"Command timed out after {timeout} seconds",
                    return_code=-1,
                    execution_time=end_time - start_time,
                    error_message="Execution timeout"
                )
                
            end_time = asyncio.get_event_loop().time()
            stdout_str = stdout.decode('utf-8', errors='replace')
            stderr_str = stderr.decode('utf-8', errors='replace')
            
            output_files = self._collect_output_files(session, work_dir)
            
            result = ExecutionResult(
                success=process.returncode == 0,
                status=ExecutionStatus.COMPLETED if process.returncode == 0 else ExecutionStatus.FAILED,
                stdout=stdout_str,
                stderr=stderr_str,
                return_code=process.returncode,
                execution_time=end_time - start_time,
                output_files=output_files
            )
            
            session.execution_history.append(result)
            return result
            
        except Exception as e:
            end_time = asyncio.get_event_loop().time()
            return ExecutionResult(
                success=False,
                status=ExecutionStatus.FAILED,
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=end_time - start_time,
                error_message=str(e)
            )
            
    async def execute_python_code(
        self,
        session_id: str,
        code: str,
        filename: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> ExecutionResult:
        session = self._get_session_or_raise(session_id)
        
        filename = filename or f"script_{uuid.uuid4().hex[:8]}.py"
        file_path = os.path.join("workspace", filename)
        
        self.write_file(session_id, file_path, code)
        
        command = f"python {filename}"
        return await self.execute_command(
            session_id,
            command,
            cwd="workspace",
            timeout=timeout
        )
        
    async def execute_notebook_cell(
        self,
        session_id: str,
        code: str,
        cell_id: Optional[str] = None
    ) -> Dict[str, Any]:
        result = await self.execute_python_code(session_id, code)
        
        return {
            "cell_id": cell_id or str(uuid.uuid4()),
            "success": result.success,
            "output": result.stdout,
            "error": result.stderr if not result.success else None,
            "execution_time": result.execution_time,
            "output_files": result.output_files
        }
        
    def upload_file(
        self,
        session_id: str,
        source_path: str,
        target_path: Optional[str] = None
    ) -> str:
        session = self._get_session_or_raise(session_id)
        
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file not found: {source_path}")
            
        if target_path is None:
            target_path = os.path.join("uploads", os.path.basename(source_path))
            
        target_full_path = self._resolve_path(session, target_path)
        os.makedirs(os.path.dirname(target_full_path), exist_ok=True)
        
        shutil.copy2(source_path, target_full_path)
        return target_path
        
    def download_file(
        self,
        session_id: str,
        file_path: str,
        target_path: str
    ):
        session = self._get_session_or_raise(session_id)
        source_full_path = self._resolve_path(session, file_path)
        
        if not os.path.exists(source_full_path):
            raise FileNotFoundError(f"File not found in sandbox: {file_path}")
            
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy2(source_full_path, target_path)
        
    def _get_session_or_raise(self, session_id: str) -> SandboxSession:
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        if not session.active:
            raise ValueError(f"Session is closed: {session_id}")
        return session
        
    def _resolve_path(self, session: SandboxSession, path: str) -> str:
        if path.startswith("/"):
            path = path[1:]
        return os.path.abspath(os.path.join(session.workspace_path, path))
        
    def _is_command_allowed(self, session: SandboxSession, command: str) -> bool:
        if session.config.blocked_commands:
            for blocked in session.config.blocked_commands:
                if blocked in command:
                    return False
                    
        if session.config.allowed_commands:
            for allowed in session.config.allowed_commands:
                if allowed in command:
                    return True
            return False
            
        return True
        
    def _collect_output_files(self, session: SandboxSession, work_dir: str) -> List[str]:
        output_files = []
        outputs_dir = os.path.join(session.workspace_path, "outputs")
        
        if os.path.exists(outputs_dir):
            for root, _, files in os.walk(outputs_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, session.workspace_path)
                    output_files.append(rel_path)
                    
        return output_files
        
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        session = self._get_session_or_raise(session_id)
        
        total_executions = len(session.execution_history)
        successful_executions = sum(1 for r in session.execution_history if r.success)
        avg_execution_time = (
            sum(r.execution_time for r in session.execution_history) / total_executions
            if total_executions > 0 else 0
        )
        
        return {
            "session_id": session.id,
            "active": session.active,
            "created_at": session.created_at,
            "workspace_path": session.workspace_path,
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": total_executions - successful_executions,
            "avg_execution_time": avg_execution_time,
            "files": self.list_files(session_id)
        }
