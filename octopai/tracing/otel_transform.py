"""
OpenTelemetry data transformer for OctoTrace.
"""

import base64
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models import (
    Span,
    Trace,
    SpanKind,
    SpanStatus,
)

logger = logging.getLogger(__name__)


class OtelTransformer:
    """Transforms OpenTelemetry (OTEL) JSON data into OctoTrace format.

    Converts standard OTEL trace JSON (as received from OTLP exporters)
    into the internal Trace/Span models used by OctoTrace.

    Supports:
    - Standard OTLP JSON format from OpenTelemetry SDKs
    - Base64-encoded trace/span IDs
    - CamelCase to snake_case attribute conversion
    - Nested resource/scope/span structure flattening
    """

    KNOWN_ATTRIBUTE_PREFIXES = {
        "octotrace.span.",
        "octotrace.llm.",
        "octotrace.trace.",
        "session.id",
        "user.id",
        "input.value",
        "output.value",
        "gen_ai.",
        "llm.token_count.",
        "llm.model_name",
    }

    def __init__(self):
        """Initialize OTEL transformer."""
        self.transform_count = 0

    def transform(self, otel_data: Dict[str, Any]) -> List[Trace]:
        """Transform OTEL JSON data into Trace objects.

        Args:
            otel_data: Raw OTEL JSON data in standard format

        Returns:
            List of Trace objects extracted from the data
        """
        if not otel_data:
            return []

        resource_spans = otel_data.get("resourceSpans", [])

        traces = []
        for rs in resource_spans:
            resource = rs.get("resource", {})
            resource_attrs = self._extract_attributes(resource.get("attributes", []))

            scope_spans = rs.get("scopeSpans", [])

            for ss in scope_spans:
                spans_data = ss.get("spans", [])
                trace_map: Dict[str, Dict[str, Any]] = {}

                for span_data in spans_data:
                    try:
                        span = self._transform_span(span_data, resource_attrs)

                        if not span or not span.trace_id:
                            continue

                        trace_id = span.trace_id

                        if trace_id not in trace_map:
                            trace_map[trace_id] = {
                                "spans": [],
                                "resource_attrs": resource_attrs,
                                "start_time": None,
                                "end_time": None,
                            }

                        trace_map[trace_id]["spans"].append(span)

                        if span.start_time:
                            if trace_map[trace_id]["start_time"] is None or \
                               span.start_time < trace_map[trace_id]["start_time"]:
                                trace_map[trace_id]["start_time"] = span.start_time

                        if span.end_time:
                            if trace_map[trace_id]["end_time"] is None or \
                               span.end_time > trace_map[trace_id]["end_time"]:
                                trace_map[trace_id]["end_time"] = span.end_time

                    except Exception as e:
                        logger.warning(f"Failed to transform span: {e}")
                        continue

                for trace_id, trace_data in trace_map.items():
                    trace = self._build_trace(trace_id, trace_data)
                    if trace:
                        traces.append(trace)
                        self.transform_count += 1

        return traces

    def _transform_span(
        self,
        span_data: Dict[str, Any],
        resource_attrs: Dict[str, Any],
    ) -> Optional[Span]:
        """Transform a single OTEL span.

        Args:
            span_data: OTEL span data
            resource_attrs: Resource-level attributes

        Returns:
            Transformed Span object or None on failure
        """
        try:
            trace_id = self._decode_id(span_data.get("traceId"))
            span_id = self._decode_id(span_data.get("spanId"))
            parent_id = self._decode_id(span_data.get("parentSpanId"))

            name = span_data.get("name", "unnamed")
            kind_str = span_data.get("kind", "SPAN_KIND_INTERNAL")
            kind = self._map_span_kind(kind_str)

            start_time = self._parse_timestamp(span_data.get("startTimeUnixNano"))
            end_time = self._parse_timestamp(span_data.get("endTimeUnixNano"))

            status_data = span_data.get("status", {})
            status_code = status_data.get("code", "STATUS_CODE_UNSET")
            status = self._map_status(status_code)
            status_message = status_data.get("message", "")

            attributes = {}
            raw_attrs = span_data.get("attributes", [])

            for attr in raw_attrs:
                key = attr.get("key", "")
                value = self._extract_attribute_value(attr.get("value", {}))

                if key and value is not None:
                    attributes[key] = value

            attributes.update(resource_attrs)

            events = []
            for event_data in span_data.get("events", []):
                event = {
                    "name": event_data.get("name", ""),
                    "timestamp": self._parse_timestamp(
                        event_data.get("timeUnixNano")
                    ),
                    "attributes": {},
                }

                for attr in event_data.get("attributes", []):
                    key = attr.get("key", "")
                    value = self._extract_attribute_value(attr.get("value", {}))
                    if key and value is not None:
                        event["attributes"][key] = value

                events.append(event)

            input_val = attributes.pop("input.value", None) or \
                      attributes.pop("input", None)
            output_val = attributes.pop("output.value", None) or \
                       attributes.pop("output", None)

            model_name = attributes.pop("llm.model_name", None) or \
                       attributes.pop("gen_ai.system", None)

            cost = attributes.pop("octotrace.span.cost", None)
            input_tokens = attributes.pop("llm.token_count.input", None) or \
                         attributes.pop("gen_ai.usage.input_tokens", None)
            output_tokens = attributes.pop("llm.token_count.output", None) or \
                          attributes.pop("gen_ai.usage.output_tokens", None)

            tags = [k for k in attributes.keys()
                   if k.startswith("tag.") or k == "tags"]

            duration_ms = 0.0
            if start_time and end_time:
                delta = end_time - start_time
                duration_ms = delta.total_seconds() * 1000

            return Span(
                span_id=span_id or "",
                trace_id=trace_id or "",
                parent_span_id=parent_id,
                name=name,
                kind=kind,
                start_time=start_time or datetime.now(timezone.utc),
                end_time=end_time,
                status=status,
                status_message=status_message,
                attributes=attributes,
                events=events,
                input=input_val,
                output=output_val,
                model_name=model_name,
                cost=float(cost) if cost else None,
                input_tokens=int(input_tokens) if input_tokens else None,
                output_tokens=int(output_tokens) if output_tokens else None,
                total_tokens=(int(input_tokens or 0) + int(output_tokens or 0)) or None,
                duration_ms=duration_ms,
                tags=tags,
            )

        except Exception as e:
            logger.error(f"Error transforming span: {e}")
            return None

    def _build_trace(
        self,
        trace_id: str,
        trace_data: Dict[str, Any],
    ) -> Optional[Trace]:
        """Build a Trace object from collected spans.

        Args:
            trace_id: Trace identifier
            trace_data: Collected spans and metadata

        Returns:
            Constructed Trace object
        """
        spans = trace_data["spans"]

        if not spans:
            return None

        root_span = next((s for s in spans if s.parent_span_id is None), spans[0])

        total_cost = sum(s.cost or 0 for s in spans)
        total_tokens = sum(s.total_tokens or 0 for s in spans)

        errors = [s for s in spans if s.status == SpanStatus.ERROR]
        status = "error" if errors else "ok"

        resource_attrs = trace_data.get("resource_attrs", {})

        user_id = resource_attrs.get("user.id") or \
                 resource_attrs.get("session.user_id")
        session_id = resource_attrs.get("session.id")

        tags = list(set(
            tag for s in spans for tag in s.tags
        ))

        return Trace(
            trace_id=trace_id,
            project_id=resource_attrs.get("project.id", ""),
            name=root_span.name or "untitled-trace",
            session_id=session_id,
            user_id=user_id,
            start_time=trace_data["start_time"],
            end_time=trace_data["end_time"],
            status=status,
            spans=spans,
            root_span_id=root_span.span_id,
            total_cost=total_cost,
            total_tokens=total_tokens,
            tags=tags,
            metadata={
                "source": "otel",
                "resource_attributes": resource_attrs,
            },
        )

    def _decode_id(self, b64_value: Optional[str]) -> Optional[str]:
        """Decode base64-encoded OTEL ID to hex string."""
        if not b64_value:
            return None

        try:
            decoded = base64.b64decode(b64_value)
            return decoded.hex()
        except Exception as e:
            logger.debug(f"Failed to decode ID '{b64_value}': {e}")
            return b64_value

    def _parse_timestamp(self, nanos) -> Optional[datetime]:
        """Parse nanosecond timestamp to datetime."""
        if not nanos:
            return None

        try:
            nanos_int = int(nanos)
            seconds = nanos_int / 1_000_000_000
            return datetime.fromtimestamp(seconds, tz=timezone.utc).replace(tzinfo=None)
        except (ValueError, TypeError, OSError):
            return None

    def _extract_attribute_value(self, attr_value: Dict) -> Any:
        """Extract value from OTEL attribute wrapper."""
        if not attr_value:
            return None

        if "stringValue" in attr_value:
            return attr_value["stringValue"]
        elif "intValue" in attr_value:
            return int(attr_value["intValue"])
        elif "boolValue" in attr_value:
            return bool(attr_value["boolValue"])
        elif "doubleValue" in attr_value:
            return float(attr_value["doubleValue"])
        elif "arrayValue" in attr_value:
            arr = attr_value["arrayValue"].get("values", [])
            return [self._extract_attribute_value(v) for v in arr]
        elif "kvlistValue" in attr_value:
            kv_list = attr_value["kvlistValue"].get("values", [])
            return {
                kv["key"]: self._extract_attribute_value(kv["value"])
                for kv in kv_list
            }

        return None

    def _extract_attributes(self, attrs: List[Dict]) -> Dict[str, Any]:
        """Extract all attributes from a list."""
        result = {}
        for attr in attrs:
            key = attr.get("key", "")
            value = self._extract_attribute_value(attr.get("value", {}))
            if key and value is not None:
                result[key] = value
        return result

    def _map_span_kind(self, kind_str: str) -> SpanKind:
        """Map OTEL span kind string to SpanKind enum."""
        mapping = {
            "SPAN_KIND_INTERNAL": SpanKind.INTERNAL,
            "SPAN_KIND_SERVER": SpanKind.SERVER,
            "SPAN_KIND_CLIENT": SpanKind.CLIENT,
            "SPAN_KIND_PRODUCER": SpanKind.PRODUCER,
            "SPAN_KIND_CONSUMER": SpanKind.CONSUMER,
        }
        return mapping.get(kind_str, SpanKind.INTERNAL)

    def _map_status(self, code: str) -> SpanStatus:
        """Map OTEL status code to SpanStatus enum."""
        if "ERROR" in code.upper():
            return SpanStatus.ERROR
        elif "OK" in code.upper():
            return SpanStatus.OK
        return SpanStatus.UNSET
