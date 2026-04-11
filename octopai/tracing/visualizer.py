"""
Trace visualization support - provides data structures for frontend rendering.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class VisualizationConfig:
    """Configuration for trace visualization.

    Attributes:
        show_timeline: Whether to show timeline view
        show_tree: Whether to show span tree view
        show_details: Whether to show detail panel
        max_depth: Maximum tree depth to display
        collapse_threshold: Collapse spans with fewer children than this
        highlight_errors: Highlight error spans prominently
        show_costs: Display cost information
        show_tokens: Display token counts
        time_format: Time display format ("relative", "absolute", "iso")
    """

    show_timeline: bool = True
    show_tree: bool = True
    show_details: bool = True
    max_depth: int = 10
    collapse_threshold: int = 5
    highlight_errors: bool = True
    show_costs: bool = True
    show_tokens: bool = True
    time_format: str = "relative"


@dataclass
class SpanNode:
    """Node in the span tree for visualization.

    Attributes:
        span_id: Span identifier
        name: Span name
        kind: Span type
        status: Span status
        start_time: Start timestamp
        duration_ms: Duration in milliseconds
        depth: Depth in tree (0 = root)
        has_children: Whether this node has children
        children_count: Number of children
        error: Error message if any
        cost: Cost if available
        tokens: Token count if available
        model_name: Model name for LLM calls
        attributes: Key attributes to display
        is_collapsed: Whether this node is collapsed in UI
        percentage_of_parent: Duration as % of parent
        percentage_of_trace: Duration as % of total trace
    """

    span_id: str = ""
    name: str = ""
    kind: str = ""
    status: str = ""
    start_time: Optional[datetime] = None
    duration_ms: float = 0.0
    depth: int = 0
    has_children: bool = False
    children_count: int = 0
    error: Optional[str] = None
    cost: Optional[float] = None
    tokens: Optional[int] = None
    model_name: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    is_collapsed: bool = False
    percentage_of_parent: float = 0.0
    percentage_of_trace: float = 0.0


@dataclass
class TimelineSegment:
    """A segment on the timeline visualization.

    Attributes:
        span_id: Associated span ID
        name: Span name
        start_offset_ms: Offset from trace start (ms)
        duration_ms: Segment duration (ms)
        depth: Vertical position in timeline
        color: Color code based on status/kind
        is_error: Whether this segment represents an error
        is_selected: Whether this segment is selected
        tooltip: Tooltip text
    """

    span_id: str = ""
    name: str = ""
    start_offset_ms: float = 0.0
    duration_ms: float = 0.0
    depth: int = 0
    color: str = "blue"
    is_error: bool = False
    is_selected: bool = False
    tooltip: str = ""


@dataclass
class TraceVisualizationData:
    """Complete visualization data for a single trace.

    Attributes:
        trace_id: Trace identifier
        name: Trace name
        tree: Root nodes of the span tree
        timeline_segments: Ordered segments for timeline view
        summary: Summary statistics
        errors: List of error spans
        metadata: Additional visualization metadata
    """

    trace_id: str = ""
    name: str = ""
    tree: List[SpanNode] = field(default_factory=list)
    timeline_segments: List[TimelineSegment] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    errors: List[Dict[str, Any]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TraceVisualizer:
    """Generates visualization-ready data from traces.

    Converts internal Trace/Span models into structures optimized
    for frontend rendering (tree views, timelines, etc.)
    """

    def __init__(self, config: VisualizationConfig = None):
        """Initialize visualizer.

        Args:
            config: Visualization configuration options
        """
        self.config = config or VisualizationConfig()

    def visualize(self, trace) -> TraceVisualizationData:
        """Generate complete visualization data for a trace.

        Args:
            trace: Trace object to visualize

        Returns:
            TraceVisualizationData with all visualization components
        """
        if not trace or not hasattr(trace, 'spans'):
            return TraceVisualizationData()

        tree = self._build_span_tree(trace.spans)

        if self.config.show_timeline:
            timeline = self._build_timeline(trace.spans, trace.start_time)
        else:
            timeline = []

        summary = self._compute_summary(trace)
        errors = self._collect_errors(trace.spans)

        return TraceVisualizationData(
            trace_id=getattr(trace, 'trace_id', ''),
            name=getattr(trace, 'name', ''),
            tree=tree,
            timeline_segments=timeline,
            summary=summary,
            errors=errors,
            metadata={
                "config": {
                    "show_costs": self.config.show_costs,
                    "show_tokens": self.config.show_tokens,
                    "time_format": self.config.time_format,
                },
            },
        )

    def _build_span_tree(self, spans: list) -> List[SpanNode]:
        """Build tree structure from flat span list."""
        if not spans:
            return []

        span_map = {s.span_id: s for s in spans if hasattr(s, 'span_id')}
        root_nodes = []
        total_duration = 0

        for span in spans:
            if hasattr(span, 'duration_ms') and span.duration_ms:
                total_duration += span.duration_ms

        for span in spans:
            if not span.parent_span_id or span.parent_span_id not in span_map:
                node = self._span_to_node(span, depth=0, total_duration=total_duration)
                node.children = self._get_children(span.span_id, span_map, depth=1, total_duration=total_duration)
                node.has_children = len(node.children) > 0
                node.children_count = len(node.children)
                root_nodes.append(node)

        return root_nodes

    def _get_children(
        self,
        parent_id: str,
        span_map: dict,
        depth: int = 1,
        total_duration: float = 0,
    ) -> List[SpanNode]:
        """Recursively get child nodes."""
        children = []

        for span_id, span in span_map.items():
            if span.parent_span_id == parent_id:
                node = self._span_to_node(span, depth=depth, total_duration=total_duration)

                if depth < self.config.max_depth:
                    node.children = self._get_children(
                        span_id, span_map, depth + 1, total_duration
                    )
                    node.has_children = len(node.children) > 0
                    node.children_count = len(node.children)

                    if node.children_count < self.config.collapse_threshold:
                        node.is_collapsed = True

                children.append(node)

        return sorted(children, key=lambda n: n.start_time or "")

    def _span_to_node(self, span, depth: int = 0, total_duration: float = 0) -> SpanNode:
        """Convert Span object to SpanNode."""
        return SpanNode(
            span_id=getattr(span, 'span_id', ''),
            name=getattr(span, 'name', ''),
            kind=getattr(span, 'kind', ''),
            status=getattr(span, 'status', '').value if hasattr(getattr(span, 'status', ''), 'value') else getattr(span, 'status', ''),
            start_time=getattr(span, 'start_time', None),
            duration_ms=getattr(span, 'duration_ms', 0),
            depth=depth,
            error=getattr(span, 'status_message', '') if getattr(span, 'status', '') == 'error' else None,
            cost=getattr(span, 'cost', None),
            tokens=getattr(span, 'total_tokens', None),
            model_name=getattr(span, 'model_name', None),
            attributes=self._extract_display_attrs(span),
            percentage_of_trace=(getattr(span, 'duration_ms', 0) / total_duration * 100) if total_duration > 0 else 0,
        )

    def _build_timeline(self, spans: list, trace_start) -> List[TimelineSegment]:
        """Build ordered timeline segments."""
        segments = []
        color_map = {
            "ok": "green",
            "error": "red",
            "unset": "gray",
        }

        for span in spans:
            if not hasattr(span, 'start_time') or not span.start_time:
                continue

            offset = 0
            if trace_start:
                try:
                    from datetime import timezone
                    # Make both datetimes comparable
                    span_start = span.start_time
                    if hasattr(span_start, 'tzinfo') and span_start.tzinfo is None:
                        span_start = span_start.replace(tzinfo=timezone.utc)

                    trace_start_normalized = trace_start
                    if hasattr(trace_start_normalized, 'tzinfo') and trace_start_normalized.tzinfo is None:
                        trace_start_normalized = trace_start_normalized.replace(tzinfo=timezone.utc)
                    elif hasattr(trace_start_normalized, 'replace'):
                        trace_start_normalized = trace_start_normalized.replace(tzinfo=None)

                    delta = span_start - trace_start_normalized
                    offset = delta.total_seconds() * 1000
                except (TypeError, ValueError):
                    offset = 0

            status_str = getattr(span.status, 'value', span.status) if hasattr(span.status, 'value') else str(span.status)

            segment = TimelineSegment(
                span_id=getattr(span, 'span_id', ''),
                name=getattr(span, 'name', ''),
                start_offset_ms=offset,
                duration_ms=getattr(span, 'duration_ms', 0),
                depth=self._calculate_timeline_depth(span, spans),
                color=color_map.get(status_str, "blue"),
                is_error=status_str == "error",
                tooltip=f"{getattr(span, 'name', '')}: {getattr(span, 'duration_ms', 0):.2f}ms",
            )
            segments.append(segment)

        return sorted(segments, key=lambda s: s.start_offset_ms)

    def _calculate_timeline_depth(self, span, all_spans: list) -> int:
        """Calculate vertical position for timeline layout."""
        depth = 0
        current = span

        while current and current.parent_span_id:
            depth += 1
            parent = next((s for s in all_spans if getattr(s, 'span_id', '') == current.parent_span_id), None)
            current = parent

        return min(depth, self.config.max_depth)

    def _compute_summary(self, trace) -> Dict[str, Any]:
        """Compute summary statistics for visualization."""
        spans = getattr(trace, 'spans', [])

        if not spans:
            return {}

        total_cost = sum(getattr(s, 'cost', 0) or 0 for s in spans)
        total_tokens = sum(getattr(s, 'total_tokens', 0) or 0 for s in spans)
        total_duration = sum(getattr(s, 'duration_ms', 0) or 0 for s in spans)

        error_count = sum(1 for s in spans if getattr(s, 'status', '') == 'error')

        kind_counts = {}
        for s in spans:
            kind = getattr(s, 'kind', '')
            kind_str = kind.value if hasattr(kind, 'value') else str(kind)
            kind_counts[kind_str] = kind_counts.get(kind_str, 0) + 1

        return {
            "span_count": len(spans),
            "total_duration_ms": round(total_duration, 2),
            "total_cost_usd": round(total_cost, 4),
            "total_tokens": total_tokens,
            "error_count": error_count,
            "error_rate": round(error_count / len(spans), 4) if spans else 0,
            "kind_distribution": kind_counts,
            "root_span_name": getattr(spans[0], 'name', '') if spans else "",
        }

    def _collect_errors(self, spans: list) -> List[Dict[str, Any]]:
        """Collect information about error spans."""
        errors = []

        for span in spans:
            if getattr(span, 'status', '') == 'error':
                errors.append({
                    "span_id": getattr(span, 'span_id', ''),
                    "name": getattr(span, 'name', ''),
                    "error": getattr(span, 'status_message', 'Unknown error'),
                    "stack_trace": getattr(span, 'stack_trace', None),
                    "duration_ms": getattr(span, 'duration_ms', 0),
                })

        return errors

    def _extract_display_attrs(self, span) -> Dict[str, Any]:
        """Extract key attributes for display."""
        attrs = {}
        attr_dict = getattr(span, 'attributes', {})

        important_keys = [
            "http.method",
            "http.url",
            "db.system",
            "rpc.method",
            "gen_ai.request.model",
            "gen_ai.response.model",
        ]

        for key in important_keys:
            if key in attr_dict:
                attrs[key] = attr_dict[key]

        return attrs
