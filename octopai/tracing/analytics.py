"""
Trace analytics - analysis and reporting for trace data.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


@dataclass
class AnalyticsReport:
    """Comprehensive analytics report.

    Attributes:
        report_id: Unique identifier
        generated_at: When report was generated
        period: Time period covered
        project_id: Project this report belongs to
        summary: High-level statistics
        performance_metrics: Performance-related metrics
        cost_analysis: Cost breakdown
        error_analysis: Error patterns and trends
        recommendations: Actionable insights
        top_operations: Most common operations
        trend_data: Time-series data for charts
    """

    report_id: str = ""
    generated_at: str = ""
    period: str = "24h"
    project_id: str = ""
    summary: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    cost_analysis: Dict[str, Any] = field(default_factory=dict)
    error_analysis: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    top_operations: List[Dict[str, Any]] = field(default_factory=list)
    trend_data: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class MetricPoint:
    """Single data point for time-series metrics.

    Attributes:
        timestamp: When this measurement was taken
        value: The measured value
        label: Optional label for grouping
    """

    timestamp: str = ""
    value: float = 0.0
    label: str = ""


class TraceAnalytics:
    """Analytics engine for trace data.

    Provides:
    - Performance analysis (latency, throughput)
    - Cost tracking and optimization suggestions
    - Error pattern detection
    - Trend analysis over time
    - Operational insights
    """

    def __init__(self):
        """Initialize analytics engine."""
        self._reports: List[AnalyticsReport] = []

    def generate_report(
        self,
        traces: list,
        period: str = "24h",
        project_id: str = "",
    ) -> AnalyticsReport:
        """Generate comprehensive analytics report.

        Args:
            traces: List of Trace objects to analyze
            period: Time period string ("1h", "24h", "7d", "30d")
            project_id: Project identifier

        Returns:
            AnalyticsReport with full analysis
        """
        import uuid

        if not traces:
            return AnalyticsReport(
                report_id=str(uuid.uuid4()),
                period=period,
                summary={"error": "No traces available"},
            )

        summary = self._compute_summary(traces)
        performance = self._analyze_performance(traces)
        costs = self._analyze_costs(traces)
        errors = self._analyze_errors(traces)
        operations = self._top_operations(traces)
        trends = self._compute_trends(traces)
        recommendations = self._generate_recommendations(
            summary, performance, costs, errors
        )

        report = AnalyticsReport(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now().isoformat(),
            period=period,
            project_id=project_id,
            summary=summary,
            performance_metrics=performance,
            cost_analysis=costs,
            error_analysis=errors,
            recommendations=recommendations,
            top_operations=operations,
            trend_data=trends,
        )

        self._reports.append(report)

        return report

    def _compute_summary(self, traces: list) -> Dict[str, Any]:
        """Compute high-level summary statistics."""
        total_traces = len(traces)
        total_spans = sum(len(getattr(t, 'spans', [])) for t in traces)

        total_cost = sum(getattr(t, 'total_cost', 0) or 0 for t in traces)
        total_tokens = sum(getattr(t, 'total_tokens', 0) or 0 for t in traces)

        total_duration = sum(getattr(t, 'duration_ms', 0) or 0 for t in traces)

        error_count = sum(1 for t in traces if getattr(t, 'status', '') == 'error')
        error_rate = error_count / total_traces if total_traces > 0 else 0

        unique_users = len(set(
            getattr(t, 'user_id', '') for t in traces if getattr(t, 'user_id', '')
        ))
        unique_sessions = len(set(
            getattr(t, 'session_id', '') for t in traces if getattr(t, 'session_id', '')
        ))

        avg_duration = total_duration / total_traces if total_traces > 0 else 0
        avg_spans_per_trace = total_spans / total_traces if total_traces > 0 else 0

        return {
            "total_traces": total_traces,
            "total_spans": total_spans,
            "unique_users": unique_users,
            "unique_sessions": unique_sessions,
            "total_cost_usd": round(total_cost, 4),
            "total_tokens": total_tokens,
            "total_duration_ms": round(total_duration, 2),
            "avg_trace_duration_ms": round(avg_duration, 2),
            "avg_spans_per_trace": round(avg_spans_per_trace, 2),
            "error_count": error_count,
            "error_rate": round(error_rate, 4),
            "success_rate": round(1.0 - error_rate, 4),
        }

    def _analyze_performance(self, traces: list) -> Dict[str, Any]:
        """Analyze performance metrics."""
        durations = []
        span_durations = []

        for t in traces:
            if hasattr(t, 'duration_ms') and t.duration_ms:
                durations.append(t.duration_ms)

            for s in getattr(t, 'spans', []):
                if hasattr(s, 'duration_ms') and s.duration_ms:
                    span_durations.append({
                        "name": getattr(s, 'name', ''),
                        "duration": s.duration_ms,
                        "kind": getattr(s, 'kind', ''),
                    })

        if not durations:
            return {"error": "No duration data available"}

        durations.sort()
        n = len(durations)

        p50_idx = int(n * 0.50)
        p90_idx = int(n * 0.90)
        p99_idx = int(n * 0.95)

        avg_duration = sum(durations) / n
        min_duration = min(durations)
        max_duration = max(durations)

        slowest_spans = sorted(span_durations, key=lambda x: x["duration"], reverse=True)[:10]

        return {
            "avg_duration_ms": round(avg_duration, 2),
            "min_duration_ms": round(min_duration, 2),
            "max_duration_ms": round(max_duration, 2),
            "p50_duration_ms": round(durations[p50_idx], 2) if p50_idx < n else 0,
            "p90_duration_ms": round(durations[p90_idx], 2) if p90_idx < n else 0,
            "p99_duration_ms": round(durations[p99_idx], 2) if p99_idx < n else 0,
            "slowest_spans": slowest_spans,
            "total_spans_analyzed": len(span_durations),
        }

    def _analyze_costs(self, traces: list) -> Dict[str, Any]:
        """Analyze cost distribution."""
        costs_by_model: Dict[str, float] = {}
        costs_by_operation: Dict[str, float] = {}
        token_usage: Dict[str, int] = {}

        for t in traces:
            trace_cost = getattr(t, 'total_cost', 0) or 0

            for s in getattr(t, 'spans', []):
                model = getattr(s, 'model_name', 'unknown')
                name = getattr(s, 'name', 'unknown')

                cost = getattr(s, 'cost', 0) or 0
                tokens = getattr(s, 'total_tokens', 0) or 0

                costs_by_model[model] = costs_by_model.get(model, 0) + cost
                costs_by_operation[name] = costs_by_operation.get(name, 0) + cost
                token_usage[model] = token_usage.get(model, 0) + tokens

        total_cost = sum(costs_by_model.values())
        total_tokens = sum(token_usage.values())

        most_expensive_models = sorted(
            costs_by_model.items(), key=lambda x: x[1], reverse=True
        )[:5]

        most_expensive_ops = sorted(
            costs_by_operation.items(), key=lambda x: x[1], reverse=True
        )[:10]

        avg_cost_per_1k_tokens = (total_cost / (total_tokens / 1000)) if total_tokens > 0 else 0

        return {
            "total_cost_usd": round(total_cost, 4),
            "total_tokens": total_tokens,
            "avg_cost_per_1k_tokens": round(avg_cost_per_1k_tokens, 6),
            "cost_by_model": dict(most_expensive_models),
            "cost_by_operation": dict(most_expensive_ops),
            "token_usage_by_model": {k: v for k, v in token_usage.most_common(5)} if hasattr(token_usage, 'most_common') else dict(sorted(token_usage.items(), key=lambda x: x[1], reverse=True)[:5]),
        }

    def _analyze_errors(self, traces: list) -> Dict[str, Any]:
        """Analyze error patterns."""
        errors: List[Dict[str, Any]] = []

        for t in traces:
            if getattr(t, 'status', '') != 'error':
                continue

            for s in getattr(t, 'spans', []):
                if getattr(s, 'status', '') == 'error':
                    errors.append({
                        "trace_id": getattr(t, 'trace_id', ''),
                        "span_name": getattr(s, 'name', ''),
                        "error_message": getattr(s, 'status_message', ''),
                        "kind": getattr(s, 'kind', ''),
                        "duration_ms": getattr(s, 'duration_ms', 0),
                    })

        error_types: Dict[str, int] = {}
        error_by_kind: Dict[str, int] = {}

        for e in errors:
            msg = e.get("error_message", "Unknown")[:100]
            error_types[msg] = error_types.get(msg, 0) + 1

            kind = e.get("kind", "")
            kind_str = kind.value if hasattr(kind, 'value') else str(kind)
            error_by_kind[kind_str] = error_by_kind.get(kind_str, 0) + 1

        most_common_errors = sorted(
            error_types.items(), key=lambda x: x[1], reverse=True
        )[:10]

        return {
            "total_errors": len(errors),
            "error_rate": len(errors) / len(traces) if traces else 0,
            "most_common_errors": dict(most_common_errors),
            "errors_by_kind": error_by_kind,
            "recent_errors": errors[-20:] if errors else [],
        }

    def _top_operations(self, traces: list) -> List[Dict[str, Any]]:
        """Identify most frequent operations."""
        operation_stats: Dict[str, Dict[str, Any]] = {}

        for t in traces:
            for s in getattr(t, 'spans', []):
                name = getattr(s, 'name', 'unknown')

                if name not in operation_stats:
                    operation_stats[name] = {
                        "count": 0,
                        "total_duration_ms": 0,
                        "total_cost": 0,
                        "total_tokens": 0,
                        "error_count": 0,
                    }

                stats = operation_stats[name]
                stats["count"] += 1
                stats["total_duration_ms"] += getattr(s, 'duration_ms', 0) or 0
                stats["total_cost"] += getattr(s, 'cost', 0) or 0
                stats["total_tokens"] += getattr(s, 'total_tokens', 0) or 0

                if getattr(s, 'status', '') == 'error':
                    stats["error_count"] += 1

        top_ops = sorted(
            operation_stats.items(),
            key=lambda x: x[1]["count"],
            reverse=True,
        )[:20]

        result = []
        for name, stats in top_ops:
            count = stats["count"]
            avg_duration = stats["total_duration_ms"] / count if count > 0 else 0
            error_rate = stats["error_count"] / count if count > 0 else 0

            result.append({
                "name": name,
                "count": count,
                "avg_duration_ms": round(avg_duration, 2),
                "total_cost_usd": round(stats["total_cost"], 4),
                "total_tokens": stats["total_tokens"],
                "error_count": stats["error_count"],
                "error_rate": round(error_rate, 4),
            })

        return result

    def _compute_trends(self, traces: list) -> List[Dict[str, Any]]:
        """Compute time-series trend data."""
        time_buckets: Dict[str, Dict[str, Any]] = {}

        for t in traces:
            start_time = getattr(t, 'start_time', None)
            if not start_time:
                continue

            if isinstance(start_time, datetime):
                bucket_key = start_time.strftime("%Y-%m-%d %H:00")
            elif isinstance(start_time, str):
                try:
                    dt = datetime.fromisoformat(start_time)
                    bucket_key = dt.strftime("%Y-%m-%d %H:00")
                except Exception:
                    continue
            else:
                continue

            if bucket_key not in time_buckets:
                time_buckets[bucket_key] = {
                    "timestamp": bucket_key,
                    "trace_count": 0,
                    "total_cost": 0,
                    "total_duration": 0,
                    "error_count": 0,
                }

            bucket = time_buckets[bucket_key]
            bucket["trace_count"] += 1
            bucket["total_cost"] += getattr(t, 'total_cost', 0) or 0
            bucket["total_duration"] += getattr(t, 'duration_ms', 0) or 0

            if getattr(t, 'status', '') == 'error':
                bucket["error_count"] += 1

        trends = sorted(time_buckets.values(), key=lambda x: x["timestamp"])

        for t in trends:
            t["avg_cost"] = round(t["total_cost"] / t["trace_count"], 4) if t["trace_count"] > 0 else 0
            t["error_rate"] = round(t["error_count"] / t["trace_count"], 4) if t["trace_count"] > 0 else 0

        return trends[-48:] if len(trends) > 48 else trends

    def _generate_recommendations(
        self,
        summary: Dict,
        performance: Dict,
        costs: Dict,
        errors: Dict,
    ) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []

        error_rate = summary.get("error_rate", 0)
        if error_rate > 0.1:
            recommendations.append(
                f"High error rate detected ({error_rate:.1%}). "
                "Review error patterns and implement retry logic."
            )

        if "p99_duration_ms" in performance:
            p99 = performance["p99_duration_ms"]
            p50 = performance.get("p50_duration_ms", 0)

            if p99 > p50 * 10:
                recommendations.append(
                    "Significant latency variance detected (P99 >> P50). "
                    "Investigate slow outliers and consider timeouts."
                )

        total_cost = costs.get("total_cost_usd", 0)
        if total_cost > 100:
            recommendations.append(
                f"High operational cost (${total_cost:.2f}). "
                "Review most expensive operations for optimization."
            )

        if "most_common_errors" in errors:
            top_error = errors["most_common_errors"]
            if top_error:
                error_msg, count = list(top_error.items())[0]
                recommendations.append(
                    f"Most frequent error: '{error_msg[:50]}...' ({count} occurrences). "
                    "Consider adding specific handling."
                )

        if not recommendations:
            recommendations.append("All metrics within normal ranges.")

        return recommendations
