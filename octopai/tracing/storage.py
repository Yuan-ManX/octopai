"""
Storage backends for trace data.
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import (
    Trace,
    Span,
    Session,
    TraceListItem,
    TraceListResult,
)


class TraceStorage(ABC):
    """Abstract base class for trace storage backends."""

    @abstractmethod
    def save_trace(self, trace: Trace) -> None:
        """Save a complete trace."""
        pass

    @abstractmethod
    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get a trace by ID."""
        pass

    @abstractmethod
    def list_traces(
        self,
        project_id: str = "",
        page: int = 0,
        limit: int = 50,
        **filters,
    ) -> TraceListResult:
        """List traces with pagination and filtering."""
        pass

    @abstractmethod
    def delete_trace(self, trace_id: str) -> bool:
        """Delete a trace by ID."""
        pass


class InMemoryStorage(TraceStorage):
    """In-memory storage for development and testing.

    Stores all data in memory. Data is lost when process exits.
    """

    def __init__(self):
        """Initialize in-memory storage."""
        self.traces: Dict[str, Trace] = {}
        self.sessions: Dict[str, Session] = {}

    def save_trace(self, trace: Trace) -> None:
        """Save trace to memory."""
        self.traces[trace.trace_id] = trace

        if trace.session_id:
            session = self._get_or_create_session(trace)
            session.trace_count += 1
            session.total_cost += trace.total_cost
            if trace.duration_ms:
                session.total_duration_ms += trace.duration_ms
            self.sessions[session.session_id] = session

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get trace from memory."""
        return self.traces.get(trace_id)

    def list_traces(
        self,
        project_id: str = "",
        page: int = 0,
        limit: int = 50,
        **filters,
    ) -> TraceListResult:
        """List traces from memory with filtering."""
        all_traces = list(self.traces.values())

        if project_id:
            all_traces = [t for t in all_traces if t.project_id == project_id]

        status_filter = filters.get("status")
        if status_filter:
            all_traces = [t for t in all_traces if t.status == status_filter]

        user_filter = filters.get("user_id")
        if user_filter:
            all_traces = [t for t in all_traces if t.user_id == user_filter]

        search_query = filters.get("search")
        if search_query:
            query_lower = search_query.lower()
            all_traces = [
                t for t in all_traces
                if query_lower in t.name.lower()
                or query_lower in (t.trace_id or "")
                or any(query_lower in tag.lower() for tag in t.tags)
            ]

        start_after = filters.get("start_after")
        if start_after:
            all_traces = [
                t for t in all_traces
                if t.start_time > start_after
            ]

        end_before = filters.get("end_before")
        if end_before:
            all_traces = [
                t for t in all_traces
                if t.start_time < end_before
            ]

        sort_by = filters.get("sort_by", "start_time")
        reverse = sort_by in ["start_time", "duration_ms"]
        all_traces.sort(key=lambda t: getattr(t, sort_by, ""), reverse=reverse)

        total = len(all_traces)
        start_idx = page * limit
        end_idx = start_idx + limit
        paginated = all_traces[start_idx:end_idx]

        items = [self._to_list_item(t) for t in paginated]

        return TraceListResult(
            data=items,
            total=total,
            page=page,
            page_size=limit,
            has_more=end_idx < total,
        )

    def delete_trace(self, trace_id: str) -> bool:
        """Delete trace from memory."""
        if trace_id in self.traces:
            del self.traces[trace_id]
            return True
        return False

    def _to_list_item(self, trace: Trace) -> TraceListItem:
        """Convert full trace to list item."""
        input_summary = None
        output_summary = None

        if trace.input:
            input_str = str(trace.input)[:200]
            input_summary = input_str if len(input_str) < len(str(trace.input)) else f"{input_str}..."

        if trace.output:
            output_str = str(trace.output)[:200]
            output_summary = output_str if len(output_str) < len(str(trace.output)) else f"{output_str}..."

        model_names = list(set(
            s.model_name for s in trace.spans if s.model_name
        ))

        return TraceListItem(
            trace_id=trace.trace_id,
            project_id=trace.project_id,
            name=trace.name,
            start_time=trace.start_time,
            user_id=trace.user_id,
            session_id=trace.session_id,
            span_count=len(trace.spans),
            duration_ms=trace.duration_ms,
            status=trace.status,
            input_summary=input_summary,
            output_summary=output_summary,
            cost=trace.total_cost if trace.total_cost else None,
            model_names=model_names,
            tags=list(trace.tags),
        )

    def _get_or_create_session(self, trace: Trace) -> Session:
        """Get existing session or create new one."""
        if trace.session_id and trace.session_id in self.sessions:
            return self.sessions[trace.session_id]

        session_id = trace.session_id or f"session-{trace.trace_id[:8]}"

        session = Session(
            session_id=session_id,
            project_id=trace.project_id,
            user_id=trace.user_id or "",
            start_time=trace.start_time,
        )

        return session

    def __len__(self) -> int:
        """Return number of stored traces."""
        return len(self.traces)

    def clear(self) -> None:
        """Clear all stored data."""
        self.traces.clear()
        self.sessions.clear()


class FileStorage(TraceStorage):
    """File-based storage for persistent local storage.

    Stores traces as JSON files on disk.
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize file storage.

        Args:
            storage_dir: Directory to store trace files
        """
        self.storage_dir = storage_dir or Path(".octopai/traces")
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self._index: Dict[str, str] = {}
        self._load_index()

    def save_trace(self, trace: Trace) -> None:
        """Save trace to file."""
        filename = f"{trace.trace_id}.json"
        filepath = self.storage_dir / filename

        data = trace.model_dump(mode='json')

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        self._index[trace.trace_id] = str(filepath)
        self._save_index()

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get trace from file."""
        filepath_str = self._index.get(trace_id)
        if not filepath_str:
            filepath = self.storage_dir / f"{trace_id}.json"
            if filepath.exists():
                filepath_str = str(filepath)
            else:
                return None

        try:
            with open(filepath_str, 'r') as f:
                data = json.load(f)
            return Trace.model_validate(data)
        except Exception as e:
            print(f"Failed to load trace {trace_id}: {e}")
            return None

    def list_traces(
        self,
        project_id: str = "",
        page: int = 0,
        limit: int = 50,
        **filters,
    ) -> TraceListResult:
        """List traces from files."""
        all_files = list(self.storage_dir.glob("*.json"))

        all_traces = []
        for filepath in all_files:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                trace = Trace.model_validate(data)
                all_traces.append(trace)
            except Exception:
                continue

        if project_id:
            all_traces = [t for t in all_traces if t.project_id == project_id]

        status_filter = filters.get("status")
        if status_filter:
            all_traces = [t for t in all_traces if t.status == status_filter]

        sort_by = filters.get("sort_by", "start_time")
        all_traces.sort(key=lambda t: getattr(t, sort_by, ""), reverse=True)

        total = len(all_traces)
        start_idx = page * limit
        end_idx = start_idx + limit
        paginated = all_traces[start_idx:end_idx]

        items = []
        for t in paginated:
            input_summary = str(t.input)[:200] if t.input else None
            output_summary = str(t.output)[:200] if t.output else None

            items.append(TraceListItem(
                trace_id=t.trace_id,
                project_id=t.project_id,
                name=t.name,
                start_time=t.start_time,
                user_id=t.user_id,
                session_id=t.session_id,
                span_count=len(t.spans),
                duration_ms=t.duration_ms,
                status=t.status,
                input_summary=input_summary,
                output_summary=output_summary,
                cost=t.total_cost,
                tags=list(t.tags),
            ))

        return TraceListResult(
            data=items,
            total=total,
            page=page,
            page_size=limit,
            has_more=end_idx < total,
        )

    def delete_trace(self, trace_id: str) -> bool:
        """Delete trace file."""
        filepath = self.storage_dir / f"{trace_id}.json"
        if filepath.exists():
            filepath.unlink()

        if trace_id in self._index:
            del self._index[trace_id]
            self._save_index()

        return True

    def _save_index(self) -> None:
        """Save trace index to file."""
        index_path = self.storage_dir / "index.json"
        with open(index_path, 'w') as f:
            json.dump(self._index, f, indent=2)

    def _load_index(self) -> None:
        """Load trace index from file."""
        index_path = self.storage_dir / "index.json"

        if index_path.exists():
            try:
                with open(index_path, 'r') as f:
                    self._index = json.load(f)
            except Exception:
                self._index = {}
