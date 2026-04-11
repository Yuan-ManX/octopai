"""
OctoTrace - Visual tracing and monitoring system for Octopai.

Provides comprehensive tracing capabilities:
- OpenTelemetry-compatible data ingestion
- Trace and span management
- Session tracking
- Cost and token usage monitoring
- Real-time visualization support
- Integration layer for AI Evolution, Skills Hub, AutoResearch
"""

from .tracer import (
    OctoTracer,
    TracerConfig,
    SpanKind,
    SpanStatus,
)
from .models import (
    Trace,
    Span,
    Session,
    TraceEvent,
    TraceListResult,
    TraceDetailResult,
)
from .storage import (
    TraceStorage,
    InMemoryStorage,
    FileStorage,
)
from .otel_transform import OtelTransformer
from .visualizer import TraceVisualizer, VisualizationConfig
from .analytics import TraceAnalytics, AnalyticsReport
from .cost_tracker import (
    CostTracker,
    ModelPricing,
    TokenUsage,
    CostRecord,
    BudgetConfig,
)

__all__ = [
    "OctoTracer",
    "TracerConfig",
    "SpanKind",
    "SpanStatus",
    "Trace",
    "Span",
    "Session",
    "TraceEvent",
    "TraceListResult",
    "TraceDetailResult",
    "TraceStorage",
    "InMemoryStorage",
    "FileStorage",
    "OtelTransformer",
    "TraceVisualizer",
    "VisualizationConfig",
    "TraceAnalytics",
    "AnalyticsReport",
    "CostTracker",
    "ModelPricing",
    "TokenUsage",
    "CostRecord",
    "BudgetConfig",
]
