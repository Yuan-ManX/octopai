"""
Data models for OctoTrace tracing system.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SpanKind(str, Enum):
    """Types of spans representing different operations."""
    INTERNAL = "internal"
    SERVER = "server"
    CLIENT = "client"
    PRODUCER = "producer"
    CONSUMER = "consumer"
    LLM_CALL = "llm_call"
    SKILL_EXECUTION = "skill_execution"
    AGENT_RUN = "agent_run"
    EVOLUTION_ITERATION = "evolution_iteration"
    TOOL_USE = "tool_use"
    EVALUATION = "evaluation"
    MUTATION = "mutation"


class SpanStatus(str, Enum):
    """Status of a span."""
    OK = "ok"
    ERROR = "error"
    UNSET = "unset"


class Span(BaseModel):
    """Individual span within a trace.

    Attributes:
        span_id: Unique identifier for this span
        trace_id: Parent trace ID
        parent_span_id: Parent span ID (None for root)
        name: Operation name
        kind: Type of operation (SpanKind)
        start_time: When the span started
        end_time: When the span ended (None if ongoing)
        status: Status of this span
        status_message: Additional status information
        attributes: Key-value metadata
        events: Events that occurred during this span
        input: Input data for this operation
        output: Output data from this operation
        model_name: LLM model name (for LLM_CALL spans)
        cost: Cost of this operation in USD
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        total_tokens: Total token count
        duration_ms: Duration in milliseconds
        stack_trace: Error stack trace (if error)
        tags: Searchable tags
        metadata: Additional unstructured metadata
    """

    span_id: str = ""
    trace_id: str = ""
    parent_span_id: Optional[str] = None

    name: str = ""
    kind: SpanKind = SpanKind.INTERNAL

    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

    status: SpanStatus = SpanStatus.UNSET
    status_message: str = ""

    attributes: Dict[str, Any] = Field(default_factory=dict)
    events: List[Dict[str, Any]] = Field(default_factory=list)

    input: Optional[Any] = None
    output: Optional[Any] = None

    model_name: Optional[str] = None
    cost: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    duration_ms: float = 0.0
    stack_trace: Optional[str] = None

    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class Trace(BaseModel):
    """Complete trace representing a request/operation.

    Attributes:
        trace_id: Unique trace identifier
        project_id: Project this trace belongs to
        name: Human-readable name for this trace
        session_id: Session this trace belongs to
        user_id: User who initiated this trace
        start_time: Trace start time
        end_time: Trace end time
        status: Overall trace status ("ok" or "error")
        spans: All spans in this trace (ordered by start time)
        root_span_id: Root span ID
        total_cost: Total cost in USD
        total_tokens: Total tokens across all spans
        duration_ms: Total duration in milliseconds
        input: Top-level input
        output: Top-level output
        metadata: Additional trace metadata
        git_ref: Git reference (branch/commit)
        git_repo: Git repository URL
        error_message: Error message if failed
        tags: Searchable tags
    """

    trace_id: str = ""
    project_id: str = ""
    name: str = ""

    session_id: Optional[str] = None
    user_id: Optional[str] = None

    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

    status: str = "ok"

    spans: List[Span] = Field(default_factory=list)
    root_span_id: Optional[str] = None

    total_cost: float = 0.0
    total_tokens: int = 0
    duration_ms: float = 0.0

    input: Optional[Any] = None
    output: Optional[Any] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)

    git_ref: Optional[str] = None
    git_repo: Optional[str] = None

    error_message: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    def compute_totals(self) -> None:
        """Compute aggregated totals from spans."""
        self.total_cost = sum(s.cost or 0 for s in self.spans)
        self.total_tokens = sum(s.total_tokens or 0 for s in self.spans)

        if self.spans:
            starts = [s.start_time for s in self.spans]
            ends = [s.end_time for s in self.spans if s.end_time]

            if starts and ends:
                self.start_time = min(starts)
                self.end_time = max(ends)
                delta = self.end_time - self.start_time
                self.duration_ms = delta.total_seconds() * 1000

            errors = [s for s in self.spans if s.status == SpanStatus.ERROR]
            self.status = "error" if errors else "ok"


class Session(BaseModel):
    """Session grouping multiple traces.

    Attributes:
        session_id: Unique session identifier
        project_id: Project this session belongs to
        user_id: User who owns this session
        start_time: Session start time
        end_time: Session end time (None if active)
        trace_count: Number of traces in this session
        total_cost: Total cost across all traces
        total_duration_ms: Total duration across all traces
        metadata: Session metadata
        tags: Session tags
    """

    session_id: str = ""
    project_id: str = ""
    user_id: str = ""

    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

    trace_count: int = 0
    total_cost: float = 0.0
    total_duration_ms: float = 0.0

    metadata: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class TraceEvent(BaseModel):
    """Event within a span.

    Attributes:
        name: Event name
        timestamp: When event occurred
        attributes: Event attributes
    """

    name: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)
    attributes: Dict[str, Any] = Field(default_factory=dict)


class TraceListItem(BaseModel):
    """Simplified trace representation for list views.

    Attributes:
        trace_id: Trace identifier
        project_id: Project ID
        name: Trace name
        start_time: Start time
        user_id: User ID
        session_id: Session ID
        span_count: Number of spans
        duration_ms: Duration
        status: Status string
        input_summary: Truncated input
        output_summary: Truncated output
        cost: Total cost
        model_names: Models used
        tags: Tags
    """

    trace_id: str = ""
    project_id: str = ""
    name: str = ""
    start_time: datetime = Field(default_factory=datetime.now)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    span_count: int = 0
    duration_ms: Optional[float] = None
    status: str = "ok"
    input_summary: Optional[str] = None
    output_summary: Optional[str] = None
    cost: Optional[float] = None
    model_names: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class TraceListResult(BaseModel):
    """Paginated result of trace listing.

    Attributes:
        data: List of trace items
        total: Total number of matching traces
        page: Current page number
        page_size: Items per page
        has_more: Whether there are more results
    """

    data: List[TraceListItem] = Field(default_factory=list)
    total: int = 0
    page: int = 0
    page_size: int = 50
    has_more: bool = False


class TraceDetailResult(BaseModel):
    """Detailed result with full trace data.

    Attributes:
        trace: Complete trace object
        session: Associated session (if available)
        related_traces: Related trace IDs
        analytics: Pre-computed analytics for this trace
    """

    trace: Optional[Trace] = None
    session: Optional[Session] = None
    related_traces: List[str] = Field(default_factory=list)
    analytics: Dict[str, Any] = Field(default_factory=dict)
