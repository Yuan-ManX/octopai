"""
Core OctoTracer - Main tracing interface for Octopai applications.
"""

import uuid
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Callable, ContextManager
from contextlib import contextmanager

from .models import (
    Trace,
    Span,
    Session,
    SpanKind,
    SpanStatus,
    TraceEvent,
    TraceListResult,
    TraceDetailResult,
)
from .storage import TraceStorage


class TracerConfig:
    """Configuration for the tracer.

    Attributes:
        service_name: Name of the service being traced
        project_id: Default project ID
        enabled: Whether tracing is enabled
        sample_rate: Sampling rate (0.0 to 1.0)
        max_spans_per_trace: Maximum spans per trace
        include_inputs: Whether to capture inputs
        include_outputs: Whether to capture outputs
        default_tags: Tags applied to all traces
    """

    def __init__(
        self,
        service_name: str = "octopai",
        project_id: str = "",
        enabled: bool = True,
        sample_rate: float = 1.0,
        max_spans_per_trace: int = 1000,
        include_inputs: bool = True,
        include_outputs: bool = True,
        default_tags: Optional[List[str]] = None,
    ):
        self.service_name = service_name
        self.project_id = project_id
        self.enabled = enabled
        self.sample_rate = sample_rate
        self.max_spans_per_trace = max_spans_per_trace
        self.include_inputs = include_inputs
        self.include_outputs = include_outputs
        self.default_tags = default_tags or []


class SpanContext:
    """Context manager for active span tracking.

    Attributes:
        span: The current active span
        tracer: Parent tracer instance
    """

    def __init__(self, span: Span, tracer: 'OctoTracer'):
        self.span = span
        self.tracer = tracer

    def __enter__(self) -> Span:
        return self.span

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.tracer.end_span(self.span, status=SpanStatus.ERROR, error=str(exc_val))
        else:
            self.tracer.end_span(self.span)
        return False


class OctoTracer:
    """Main tracing class for Octopai applications.

    Provides a simple API for creating and managing traces and spans.
    Integrates with all Octopai modules (Evolution, Skills Hub, AutoResearch).

    Usage:
        ```python
        tracer = OctoTracer(TracerConfig(service_name="evolution"))

        # Create a trace for an evolution run
        trace = tracer.create_trace(
            name="skill-evolution-run",
            metadata={"iteration": 5}
        )

        with tracer.start_span(trace, "evaluation", kind=SpanKind.EVALUATION):
            # ... do work ...
            pass

        tracer.finish_trace(trace)
        ```
    """

    def __init__(
        self,
        config: TracerConfig = None,
        storage: Optional[TraceStorage] = None,
    ):
        """Initialize the tracer.

        Args:
            config: Tracer configuration (uses defaults if None)
            storage: Storage backend (uses InMemoryStorage if None)
        """
        self.config = config or TracerConfig()
        self.storage = storage

        self._active_traces: Dict[str, Trace] = {}
        self._active_spans: Dict[str, Span] = {}

    def create_trace(
        self,
        name: str,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        input_data: Any = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> Trace:
        """Create a new trace.

        Args:
            name: Human-readable name
            project_id: Project identifier
            session_id: Session identifier
            user_id: User identifier
            input_data: Input data for this trace
            metadata: Additional metadata
            tags: Searchable tags

        Returns:
            Created Trace object
        """
        if not self.config.enabled:
            return Trace(trace_id="", name=name)

        trace_id = str(uuid.uuid4())

        trace = Trace(
            trace_id=trace_id,
            project_id=project_id or self.config.project_id,
            name=name,
            session_id=session_id,
            user_id=user_id,
            start_time=datetime.now(timezone.utc),
            input=input_data if self.config.include_inputs else None,
            metadata=metadata or {},
            tags=(tags or []) + list(self.config.default_tags),
        )

        self._active_traces[trace_id] = trace

        return trace

    def finish_trace(
        self,
        trace: Trace,
        output_data: Any = None,
        error: Optional[str] = None,
        status: str = "ok",
    ) -> Trace:
        """Finish and save a trace.

        Args:
            trace: Trace to finish
            output_data: Output data
            error: Error message if failed
            status: Final status ("ok" or "error")

        Returns:
            Finished trace with computed totals
        """
        if not self.config.enabled or not trace.trace_id:
            return trace

        trace.output = output_data if self.config.include_outputs else None
        trace.error_message = error
        trace.status = status if error else "ok"
        trace.end_time = datetime.now(timezone.utc)

        trace.compute_totals()

        if self.storage:
            self.storage.save_trace(trace)

        if trace.trace_id in self._active_traces:
            del self._active_traces[trace.trace_id]

        return trace

    def start_span(
        self,
        trace: Trace,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        parent_span: Optional[Span] = None,
        attributes: Optional[Dict[str, Any]] = None,
        input_data: Any = None,
        model_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> SpanContext:
        """Start a new span within a trace.

        Args:
            trace: Parent trace
            name: Operation name
            kind: Type of operation
            parent_span: Parent span (None for root span)
            attributes: Span attributes
            input_data: Input data
            model_name: LLM model name (for LLM_CALL spans)
            tags: Span tags

        Returns:
            SpanContext for use as context manager
        """
        if not self.config.enabled or not trace.trace_id:
            return SpanContext(Span(), self)

        span_id = str(uuid.uuid4())[:16]

        span = Span(
            span_id=span_id,
            trace_id=trace.trace_id,
            parent_span_id=parent_span.span_id if parent_span else None,
            name=name,
            kind=kind,
            start_time=datetime.now(timezone.utc),
            attributes=attributes or {},
            input=input_data if self.config.include_inputs else None,
            model_name=model_name,
            tags=tags or [],
        )

        trace.spans.append(span)

        if len(trace.spans) == 1:
            trace.root_span_id = span.span_id

        self._active_spans[span.span_id] = span

        return SpanContext(span, self)

    @contextmanager
    def trace_context(
        self,
        name: str,
        **kwargs,
    ):
        """Context manager that creates trace + root span automatically.

        Args:
            name: Trace name
            **kwargs: Arguments passed to create_trace

        Yields:
            Tuple of (trace, root_span)
        """
        trace = self.create_trace(name=name, **kwargs)

        with self.start_span(trace, name, **kwargs) as root_span:
            yield trace, root_span

        self.finish_trace(trace)

    def end_span(
        self,
        span: Span,
        output_data: Any = None,
        status: SpanStatus = SpanStatus.OK,
        status_message: str = "",
        cost: Optional[float] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        error: Optional[str] = None,
        stack_trace: Optional[str] = None,
    ) -> Span:
        """End a span.

        Args:
            span: Span to end
            output_data: Output data
            status: Final status
            status_message: Status message
            cost: Cost in USD
            input_tokens: Input token count
            output_tokens: Output token count
            error: Error message
            stack_trace: Stack trace on error

        Returns:
            Ended span with computed duration
        """
        if not span.span_id:
            return span

        span.end_time = datetime.now(timezone.utc)
        span.status = status
        span.status_message = status_message
        span.output = output_data if self.config.include_outputs else None
        span.cost = cost
        span.input_tokens = input_tokens
        span.output_tokens = output_tokens
        span.total_tokens = (input_tokens or 0) + (output_tokens or 0)

        if span.start_time and span.end_time:
            delta = span.end_time - span.start_time
            span.duration_ms = delta.total_seconds() * 1000

        if error:
            span.stack_trace = stack_trace
            span.status = SpanStatus.ERROR
            span.status_message = error

        if span.span_id in self._active_spans:
            del self._active_spans[span.span_id]

        return span

    def add_event(
        self,
        span: Span,
        name: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add an event to a span.

        Args:
            span: Span to add event to
            name: Event name
            attributes: Event attributes
        """
        event = TraceEvent(
            name=name,
            timestamp=datetime.now(timezone.utc),
            attributes=attributes or {},
        )
        span.events.append(event)

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get a trace by ID.

        Args:
            trace_id: Trace identifier

        Returns:
            Trace object or None
        """
        if trace_id in self._active_traces:
            return self._active_traces[trace_id]

        if self.storage:
            return self.storage.get_trace(trace_id)

        return None

    def list_traces(
        self,
        project_id: Optional[str] = None,
        page: int = 0,
        page_size: int = 50,
        filters: Optional[Dict[str, Any]] = None,
    ) -> TraceListResult:
        """List traces with filtering and pagination.

        Args:
            project_id: Filter by project
            page: Page number (0-indexed)
            page_size: Items per page
            filters: Additional filter criteria

        Returns:
            TraceListResult with matching traces
        """
        if self.storage:
            return self.storage.list_traces(
                project_id=project_id or self.config.project_id,
                page=page,
                limit=page_size,
                **(filters or {}),
            )

        return TraceListResult()

    def get_active_traces(self) -> List[Trace]:
        """Get all currently active (unfinished) traces."""
        return list(self._active_traces.values())

    def flush(self) -> None:
        """Flush any buffered traces to storage."""
        pass
