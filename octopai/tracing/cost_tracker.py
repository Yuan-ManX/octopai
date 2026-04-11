"""
Cost Tracker - Token usage and cost tracking for traces.

Provides:
- Per-model cost calculation
- Token counting and categorization
- Budget management and alerts
- Cost optimization suggestions
- Historical cost analysis
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum


class TokenType(str, Enum):
    """Types of tokens."""
    INPUT = "input"
    OUTPUT = "output"
    TOTAL = "total"


@dataclass
class ModelPricing:
    """Pricing information for a model.

    Attributes:
        model_name: Model identifier (e.g., "gpt-4", "claude-3")
        input_cost_per_1k: Cost per 1k input tokens in USD
        output_cost_per_1k: Cost per 1k output tokens in USD
        max_context_tokens: Maximum context window
        provider: Model provider (OpenAI, Anthropic, etc.)
        category: Category (chat, completion, embedding, etc.)
    """

    model_name: str = ""
    input_cost_per_1k: float = 0.0
    output_cost_per_1k: float = 0.0
    max_context_tokens: int = 4096
    provider: str = ""
    category: str = "chat"


@dataclass
class TokenUsage:
    """Token usage record.

    Attributes:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        total_tokens: Total token count
        model_name: Model used
        timestamp: When this usage occurred
        trace_id: Associated trace ID
        span_id: Associated span ID
        metadata: Additional usage metadata
    """

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    model_name: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def cost(self) -> float:
        """Calculate estimated cost based on default pricing."""
        return (self.input_tokens / 1000 * 0.01 +
                self.output_tokens / 1000 * 0.03)


@dataclass
class CostRecord:
    """Complete cost record for a trace or operation.

    Attributes:
        record_id: Unique identifier
        trace_id: Associated trace ID
        total_cost_usd: Total cost in USD
        total_input_tokens: Total input tokens used
        total_output_tokens: Total output tokens used
        total_tokens: Grand total tokens
        model_breakdown: Costs by model {model: cost}
        timestamp: When this was recorded
        duration_ms: Operation duration
        operations_count: Number of LLM calls
        budget_exceeded: Whether this exceeded any budget
    """

    record_id: str = ""
    trace_id: str = ""
    total_cost_usd: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tokens: int = 0
    model_breakdown: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0
    operations_count: int = 0
    budget_exceeded: bool = False


@dataclass
class BudgetConfig:
    """Budget configuration.

    Attributes:
        daily_limit_usd: Daily spending limit
        monthly_limit_usd: Monthly spending limit
        per_trace_limit_usd: Limit per single trace
        alert_threshold_pct: Alert when this % of budget is used
        hard_stop: Stop execution when budget exceeded
    """

    daily_limit_usd: Optional[float] = None
    monthly_limit_usd: Optional[float] = None
    per_trace_limit_usd: Optional[float] = None
    alert_threshold_pct: float = 80.0
    hard_stop: bool = False


class CostTracker:
    """Tracks and manages costs for tracing system.

    Features:
    - Multi-model pricing database
    - Automatic cost calculation from token counts
    - Budget monitoring and alerts
    - Cost optimization recommendations
    - Historical cost analytics
    """

    # Default pricing for common models (as of early 2025)
    DEFAULT_PRICING = {
        # OpenAI Models
        "gpt-4o": ModelPricing(
            model_name="gpt-4o",
            input_cost_per_1k=0.00275,
            output_cost_per_1k=0.011,
            max_context_tokens=128000,
            provider="openai",
            category="chat",
        ),
        "gpt-4-turbo": ModelPricing(
            model_name="gpt-4-turbo",
            input_cost_per_1k=0.001,
            output_cost_per_1k=0.003,
            max_context_tokens=128000,
            provider="openai",
            category="chat",
        ),
        "gpt-3.5-turbo": ModelPricing(
            model_name="gpt-3.5-turbo",
            input_cost_per_1k=0.0005,
            output_cost_per_1k=0.0015,
            max_context_tokens=16385,
            provider="openai",
            category="chat",
        ),
        # Anthropic Models
        "claude-3-opus": ModelPricing(
            model_name="claude-3-opus",
            input_cost_per_1k=0.015,
            output_cost_per_1k=0.075,
            max_context_tokens=200000,
            provider="anthropic",
            category="chat",
        ),
        "claude-3-sonnet": ModelPricing(
            model_name="claude-3-sonnet",
            input_cost_per_1k=0.003,
            output_cost_per_1k=0.015,
            max_context_tokens=200000,
            provider="anthropic",
            category="chat",
        ),
        "claude-3-haiku": ModelPricing(
            model_name="claude-3-haiku",
            input_cost_per_1k=0.00025,
            output_cost_per_1k=0.00125,
            max_context_tokens=200000,
            provider="anthropic",
            category="chat",
        ),
        # Google Models
        "gemini-pro": ModelPricing(
            model_name="gemini-pro",
            input_cost_per_1k=0.000125,
            output_cost_per_1k=0.000375,
            max_context_tokens=32768,
            provider="google",
            category="chat",
        ),
        # Embedding Models
        "text-embedding-ada-002": ModelPricing(
            model_name="text-embedding-ada-002",
            input_cost_per_1k=0.00002,
            output_cost_per_1k=0.0,
            max_context_tokens=8191,
            provider="openai",
            category="embedding",
        ),
    }

    def __init__(self, custom_pricing: Optional[Dict[str, ModelPricing]] = None):
        """Initialize cost tracker.

        Args:
            custom_pricing: Custom model pricing to add/override defaults
        """
        self.pricing = dict(self.DEFAULT_PRICING)

        if custom_pricing:
            self.pricing.update(custom_pricing)

        self.usage_records: List[TokenUsage] = []
        self.cost_records: List[CostRecord] = []
        self.budget_config = BudgetConfig()

    def register_model_pricing(self, pricing: ModelPricing) -> None:
        """Register or update pricing for a model."""
        self.pricing[pricing.model_name] = pricing

    def get_model_pricing(self, model_name: str) -> Optional[ModelPricing]:
        """Get pricing for a specific model."""
        # Try exact match first
        if model_name in self.pricing:
            return self.pricing[model_name]

        # Try fuzzy match (handle version suffixes like "-2024-01-15")
        base_name = model_name.split("-")[0]
        if base_name in self.pricing:
            return self.pricing[base_name]

        # Try prefix match
        for name, pricing in self.pricing.items():
            if model_name.lower().startswith(name.lower()):
                return pricing

        return None

    def calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        model_name: str,
    ) -> Tuple[float, Optional[ModelPricing]]:
        """Calculate cost for given token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model_name: Model name

        Returns:
            Tuple of (cost_in_usd, pricing_info)
        """
        pricing = self.get_model_pricing(model_name)

        if not pricing:
            # Use fallback estimation
            estimated_cost = (input_tokens / 1000 * 0.003 +
                             output_tokens / 1000 * 0.009)
            return estimated_cost, None

        input_cost = (input_tokens / 1000) * pricing.input_cost_per_1k
        output_cost = (output_tokens / 1000) * pricing.output_cost_per_1k
        total_cost = input_cost + output_cost

        return round(total_cost, 6), pricing

    def track_usage(
        self,
        input_tokens: int,
        output_tokens: int,
        model_name: str,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        **metadata,
    ) -> TokenUsage:
        """Track token usage for a specific operation.

        Args:
            input_tokens: Input tokens used
            output_tokens: Output tokens generated
            model_name: Model that was called
            trace_id: Parent trace ID
            span_id: Parent span ID
            **metadata: Additional metadata

        Returns:
            Created TokenUsage record
        """
        usage = TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            model_name=model_name,
            trace_id=trace_id,
            span_id=span_id,
            metadata=metadata,
        )

        # Calculate actual cost
        usage_cost, _ = self.calculate_cost(input_tokens, output_tokens, model_name)
        # Store calculated cost in metadata
        usage.metadata['calculated_cost'] = usage_cost

        self.usage_records.append(usage)
        return usage

    def create_cost_record(
        self,
        trace_id: str,
        duration_ms: float = 0.0,
    ) -> CostRecord:
        """Create a cost record for a complete trace.

        Aggregates all usage records for the given trace into a cost summary.

        Args:
            trace_id: Trace to create record for
            duration_ms: Duration of the trace

        Returns:
            Complete CostRecord with aggregated data
        """
        trace_usages = [
            u for u in self.usage_records
            if u.trace_id == trace_id
        ]

        if not trace_usages:
            return CostRecord(
                record_id=f"cost-{trace_id}",
                trace_id=trace_id,
                duration_ms=duration_ms,
                operations_count=0,
            )

        total_input = sum(u.input_tokens for u in trace_usages)
        total_output = sum(u.output_tokens for u in trace_usages)
        total_tokens = total_input + total_output

        model_costs: Dict[str, float] = {}
        for usage in trace_usages:
            cost, _ = self.calculate_cost(
                usage.input_tokens,
                usage.output_tokens,
                usage.model_name,
            )
            model_costs[usage.model_name] = model_costs.get(usage.model_name, 0) + cost

        total_cost = sum(model_costs.values())

        record = CostRecord(
            record_id=f"cost-{trace_id}",
            trace_id=trace_id,
            total_cost_usd=round(total_cost, 6),
            total_input_tokens=total_input,
            total_output_tokens=total_output,
            total_tokens=total_tokens,
            model_breakdown={k: round(v, 6) for k, v in model_costs.items()},
            duration_ms=duration_ms,
            operations_count=len(trace_usages),
        )

        self.cost_records.append(record)
        return record

    def check_budget(
        self,
        current_cost: float,
        budget_type: str = "per_trace",
    ) -> Dict[str, Any]:
        """Check if current spending is within budget.

        Args:
            current_cost: Current cost amount
            budget_type: Type of budget to check against

        Returns:
            Dictionary with budget status and details
        """
        result = {
            "within_budget": True,
            "budget_used_pct": 0.0,
            "remaining": 0.0,
            "limit": 0.0,
            "alert_triggered": False,
            "should_stop": False,
        }

        limit_map = {
            "daily": self.budget_config.daily_limit_usd,
            "monthly": self.budget_config.monthly_limit_usd,
            "per_trace": self.budget_config.per_trace_limit_usd,
        }

        limit = limit_map.get(budget_type)
        if limit is None:
            result["within_budget"] = True
            return result

        result["limit"] = limit
        result["used"] = current_cost
        result["remaining"] = max(0, limit - current_cost)
        result["budget_used_pct"] = min((current_cost / limit) * 100, 100) if limit > 0 else 0

        if current_cost >= limit:
            result["within_budget"] = False
            result["should_stop"] = self.budget_config.hard_stop
        elif current_cost >= limit * (self.budget_config.alert_threshold_pct / 100):
            result["alert_triggered"] = True

        return result

    def get_cost_statistics(self, time_range_days: int = 30) -> Dict[str, Any]:
        """Get comprehensive cost statistics.

        Args:
            time_range_days: Number of days to analyze

        Returns:
            Dictionary with cost statistics
        """
        cutoff = datetime.now().timestamp() - (time_range_days * 86400)

        recent_records = [
            r for r in self.cost_records
            if r.timestamp.timestamp() > cutoff
        ]

        recent_usage = [
            u for u in self.usage_records
            if u.timestamp.timestamp() > cutoff
        ]

        if not recent_records:
            return {
                "period_days": time_range_days,
                "total_traces_tracked": len(recentance_records),
                "total_cost_usd": 0.0,
                "total_tokens": 0,
                "avg_cost_per_trace": 0.0,
                "most_expensive_models": [],
                "cost_trend": [],
            }

        total_cost = sum(r.total_cost_usd for r in recent_records)
        total_tokens = sum(r.total_tokens for r in recent_records)
        avg_cost = total_cost / len(recent_records) if recent_records else 0

        # Model breakdown
        model_totals: Dict[str, Dict[str, Any]] = {}
        for r in recent_records:
            for model, cost in r.model_breakdown.items():
                if model not in model_totals:
                    model_totals[model] = {"total_cost": 0, "call_count": 0}
                model_totals[model]["total_cost"] += cost
                model_totals[model]["call_count"] += 1

        most_expensive = sorted(
            model_totals.items(),
            key=lambda x: x[1]["total_cost"],
            reverse=True,
        )[:10]

        # Calculate daily trend
        daily_costs: Dict[str, float] = {}
        for r in recent_records:
            day_key = r.timestamp.strftime("%Y-%m-%d")
            daily_costs[day_key] = daily_costs.get(day_key, 0) + r.total_cost_usd

        sorted_days = sorted(daily_costs.items())
        cost_trend = [{"date": d, "cost": c} for d, c in sorted_days]

        return {
            "period_days": time_range_days,
            "total_traces_tracked": len(recent_records),
            "total_operations": sum(r.operations_count for r in recent_records),
            "total_cost_usd": round(total_cost, 4),
            "total_tokens": total_tokens,
            "avg_cost_per_trace": round(avg_cost, 4),
            "avg_cost_per_1k_tokens": round((total_cost / (total_tokens / 1000)) if total_tokens > 0 else 0, 6),
            "most_expensive_models": [
                {"model": m, **stats} for m, stats in most_expensive
            ],
            "cost_trend": cost_trend[-14:],  # Last 2 weeks
            "peak_cost_day": max(daily_costs.values()) if daily_costs else 0,
            "avg_daily_cost": sum(daily_costs.values()) / len(daily_costs) if daily_costs else 0,
        }

    def get_optimization_suggestions(
        self,
        trace_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Generate cost optimization suggestions.

        Analyzes usage patterns and suggests optimizations.

        Args:
            trace_id: Specific trace to analyze (or all if None)

        Returns:
            List of suggestion dictionaries
        """
        suggestions = []

        usages_to_analyze = (
            [u for u in self.usage_records if u.trace_id == trace_id]
            if trace_id
            else self.usage_records
        )

        if not usages_to_analyze:
            return suggestions

        # Check for expensive models
        model_costs: Dict[str, List[float]] = {}
        for usage in usages_to_analyze:
            cost, _ = self.calculate_cost(
                usage.input_tokens,
                usage.output_tokens,
                usage.model_name,
            )
            if usage.model_name not in model_costs:
                model_costs[usage.model_name] = []
            model_costs[usage.model_name].append(cost)

        for model, costs in model_costs.items():
            avg_cost = sum(costs) / len(costs)
            total_cost = sum(costs)

            pricing = self.get_model_pricing(model)
            if pricing and pricing.category == "chat":
                cheaper_alternatives = [
                    m for m, p in self.pricing.items()
                    if p.category == "chat"
                    and p.input_cost_per_1k < pricing.input_cost_per_1k
                ]
                if cheaper_alternatives and avg_cost > 0.05:
                    suggestions.append({
                        "type": "model_substitution",
                        "priority": "high" if avg_cost > 0.2 else "medium",
                        "current_model": model,
                        "avg_call_cost": round(avg_cost, 4),
                        "total_spent": round(total_cost, 4),
                        "suggestion": f"Consider using cheaper alternatives: {', '.join(cheaper_alternatives[:3])}",
                        "potential_savings": round(total_cost * 0.4, 4),  # Estimate 40% savings
                    })

        # Check for high output token ratios
        high_output = [
            u for u in usages_to_analyze
            if u.total_tokens > 0 and (u.output_tokens / u.total_tokens) > 0.7
        ]
        if len(high_output) > 3:
            suggestions.append({
                "type": "output_optimization",
                "priority": "medium",
                "count": len(high_output),
                "suggestion": f"{len(high_output)} calls have >70% output tokens. Consider setting max_tokens parameter or summarizing outputs.",
                "potential_savings": "10-20%",
            })

        # Check for repeated identical calls
        call_signatures: Dict[str, int] = {}
        for usage in usages_to_analyze:
            sig = f"{usage.model_name}:{usage.metadata.get('prompt_hash', '')}"
            call_signatures[sig] = call_signatures.get(sig, 0) + 1

        duplicates = [(sig, count) for sig, count in call_signatures.items() if count > 3]
        if duplicates:
            suggestions.append({
                "type": "caching_opportunity",
                "priority": "low" if len(duplicates) < 10 else "high",
                "duplicate_patterns": len(duplicates),
                "suggestion": f"Found {len(duplicates)} repeated call patterns. Consider implementing response caching.",
                "potential_savings": "20-50%",
            })

        return suggestions[:10]  # Limit to top 10 suggestions
