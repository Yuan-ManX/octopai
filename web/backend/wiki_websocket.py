"""
WebSocket Real-time Communication Module for AI Wiki

Features:
- Live trace updates (replace polling in Trace Viewer)
- Real-time operation progress streaming
- Instant notifications for completed operations
- Collaborative editing support (future)
- Multi-client broadcast capabilities

Event Types:
- trace.span.created: New operation span started
- trace.span.updated: Span status/progress changed
- trace.event.added: Timeline event recorded
- cost.recorded: New cost record added
- wiki.page.created: Wiki page generated
- wiki.page.updated: Wiki page modified
- ingest.progress: Ingestion phase progress
- query.completed: Query answer ready
- lint.completed: Lint report available
- system.notification: General system notification
- autoresearch.status: AutoResearch session updates
"""

import asyncio
import json
from typing import Dict, List, Set, Any, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import uuid


class EventType(Enum):
    """WebSocket event type enumeration"""
    # Trace events
    TRACE_SPAN_CREATED = "trace.span.created"
    TRACE_SPAN_UPDATED = "trace.span.updated"
    TRACE_EVENT_ADDED = "trace.event.added"
    
    # Cost events
    COST_RECORDED = "cost.recorded"
    COST_BUDGET_WARNING = "cost.budget.warning"
    
    # Wiki events
    WIKI_PAGE_CREATED = "wiki.page.created"
    WIKI_PAGE_UPDATED = "wiki.page.updated"
    WIKI_PAGE_DELETED = "wiki.page.deleted"
    
    # Operation events
    INGEST_PROGRESS = "ingest.progress"
    QUERY_COMPLETED = "query.completed"
    LINT_COMPLETED = "lint.completed"
    
    # System events
    SYSTEM_NOTIFICATION = "system.notification"
    SYSTEM_STATUS = "system.status"
    
    # AutoResearch events
    AUTORESEARCH_STATUS = "autoresearch.status"
    AUTORESEARCH_COMPLETED = "autoresearch.completed"
    
    # Connection events
    CONNECTION_ESTABLISHED = "connection.established"
    CLIENT_SUBSCRIBED = "client.subscribed"


@dataclass
class WSMessage:
    """Standardized WebSocket message format"""
    event_type: EventType
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    message_id: str = field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:8]}")
    source: str = "server"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "event": self.event_type.value,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "message_id": self.message_id,
            "source": self.source
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())


@dataclass
class WSClient:
    """Connected WebSocket client representation"""
    client_id: str
    websocket: Any  # Actual WebSocket connection object
    connected_at: datetime
    subscriptions: Set[EventType] = field(default_factory=set)
    user_id: Optional[str] = None
    last_ping: datetime = field(default_factory=datetime.now)
    is_authenticated: bool = False


class WebSocketManager:
    """
    Central manager for all WebSocket connections and message broadcasting
    
    Features:
    - Client connection management with authentication
    - Event-based subscription system
    - Selective broadcasting based on subscriptions
    - Heartbeat/ping mechanism for connection health
    - Message queue for offline clients (optional)
    """
    
    def __init__(self):
        # Active connections storage
        self.clients: Dict[str, WSClient] = {}
        
        # Event handlers registry
        self._event_handlers: Dict[EventType, List[Callable]] = {}
        
        # Message history buffer (for reconnection)
        self._message_history: List[WSMessage] = []
        self._max_history_size = 1000
        
        # Statistics
        self._total_connections = 0
        self._messages_broadcasted = 0
        
        # Background tasks
        self._heartbeat_task: Optional[asyncio.Task] = None
    
    async def connect(self, websocket: Any, user_id: str = None) -> str:
        """
        Register a new WebSocket connection
        
        Args:
            websocket: The WebSocket connection object
            user_id: Optional authenticated user ID
            
        Returns:
            Unique client identifier
        """
        client_id = f"client_{uuid.uuid4().hex[:8]}"
        
        client = WSClient(
            client_id=client_id,
            websocket=websocket,
            connected_at=datetime.now(),
            user_id=user_id,
            is_authenticated=user_id is not None
        )
        
        self.clients[client_id] = client
        self._total_connections += 1
        
        # Send welcome message
        welcome_msg = WSMessage(
            event_type=EventType.CONNECTION_ESTABLISHED,
            payload={
                "client_id": client_id,
                "server_time": datetime.now().isoformat(),
                "available_events": [e.value for e in EventType],
                "instructions": "Subscribe to events using {event: 'client.subscribe', payload: {events: [...]}}"
            }
        )
        
        await self._send_to_client(client_id, welcome_msg)
        
        print(f"[WS] Client connected: {client_id} (auth: {client.is_authenticated})")
        return client_id
    
    async def disconnect(self, client_id: str):
        """
        Remove a WebSocket connection
        
        Args:
            client_id: Client identifier to disconnect
        """
        if client_id in self.clients:
            del self.clients[client_id]
            print(f"[WS] Client disconnected: {client_id}")
    
    async def subscribe(self, client_id: str, event_types: List[EventType]):
        """
        Subscribe a client to specific event types
        
        Args:
            client_id: Client identifier
            event_types: List of event types to subscribe to
        """
        if client_id not in self.clients:
            return
        
        client = self.clients[client_id]
        client.subscriptions.update(event_types)
        
        # Send confirmation
        confirm_msg = WSMessage(
            event_type=EventType.CLIENT_SUBSCRIBED,
            payload={
                "subscribed_events": [e.value for e in event_types],
                "total_subscriptions": len(client.subscriptions)
            }
        )
        
        await self._send_to_client(client_id, confirm_msg)
        print(f"[WS] Client {client_id} subscribed to {len(event_types)} events")
    
    async def unsubscribe(self, client_id: str, event_types: List[EventType]):
        """
        Unsubscribe a client from specific event types
        
        Args:
            client_id: Client identifier
            event_types: List of event types to unsubscribe from
        """
        if client_id not in self.clients:
            return
        
        client = self.clients[client_id]
        client.subscriptions.difference_update(event_types)
        print(f"[WS] Client {client_id} unsubscribed from {len(event_types)} events")
    
    async def broadcast(self, message: WSMessage, target_user_id: str = None):
        """
        Broadcast a message to all subscribed clients
        
        Args:
            message: WSMessage object to broadcast
            target_user_id: Optional - only send to specific user's clients
        """
        # Store in history
        self._message_history.append(message)
        if len(self._message_history) > self._max_history_size:
            self._message_history.pop(0)
        
        self._messages_broadcasted += 1
        
        # Find target clients
        targets = []
        for client_id, client in self.clients.items():
            # Check subscription
            if message.event_type not in client.subscriptions:
                continue
            
            # Check user filter if specified
            if target_user_id and client.user_id != target_user_id:
                continue
            
            targets.append(client_id)
        
        # Send to all targets concurrently
        if targets:
            await asyncio.gather(
                *[self._send_to_client(cid, message) for cid in targets],
                return_exceptions=True
            )
    
    async def broadcast_to_all(self, event_type: EventType, payload: Dict):
        """
        Convenience method: Create and broadcast message to all subscribers
        
        Args:
            event_type: Type of event
            payload: Event payload data
        """
        message = WSMessage(event_type=event_type, payload=payload)
        await self.broadcast(message)
    
    async def send_to_client(self, client_id: str, message: WSMessage):
        """
        Send a message to a specific client
        
        Args:
            client_id: Target client identifier
            message: WSMessage to send
        """
        await self._send_to_client(client_id, message)
    
    async def _send_to_client(self, client_id: str, message: WSMessage):
        """
        Internal method to send message to a single client
        
        Handles errors and disconnections gracefully
        """
        if client_id not in self.clients:
            return
        
        try:
            await self.clients[client_id].websocket.send_text(message.to_json())
            self.clients[client_id].last_ping = datetime.now()
        except Exception as e:
            print(f"[WS] Error sending to client {client_id}: {e}")
            # Mark for potential cleanup
            await self.disconnect(client_id)
    
    def register_handler(self, event_type: EventType, handler: Callable):
        """
        Register an event handler function
        
        Args:
            event_type: Type of event to handle
            handler: Async function to call when event occurs
        """
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)
    
    async def emit_event(self, event_type: EventType, payload: Dict, 
                        target_user_id: str = None):
        """
        Emit an event to all subscribed clients and trigger handlers
        
        Args:
            event_type: Type of event
            payload: Event payload
            target_user_id: Optional user filter
        """
        # Create message
        message = WSMessage(event_type=event_type, payload=payload)
        
        # Broadcast to subscribers
        await self.broadcast(message, target_user_id)
        
        # Trigger registered handlers
        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(payload)
                    else:
                        handler(payload)
                except Exception as e:
                    print(f"[WS] Handler error for {event_type}: {e}")
    
    def get_recent_messages(self, limit: int = 50) -> List[Dict]:
        """
        Get recent message history (for reconnection/replay)
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of message dictionaries
        """
        recent = self._message_history[-limit:]
        return [msg.to_dict() for msg in recent]
    
    def get_connection_stats(self) -> Dict:
        """
        Get current connection statistics
        
        Returns:
            Dictionary with connection metrics
        """
        return {
            "active_connections": len(self.clients),
            "total_connections_ever": self._total_connections,
            "messages_broadcasted": self._messages_broadcasted,
            "event_handlers_registered": sum(len(handlers) for handlers in self._event_handlers.values()),
            "history_buffer_size": len(self._message_history),
            "clients_by_subscription": {
                event_type.value: sum(1 for c in self.clients.values() 
                                    if event_type in c.subscriptions)
                for event_type in EventType
            },
            "authenticated_clients": sum(1 for c in self.clients.values() if c.is_authenticated),
            "unauthenticated_clients": sum(1 for c in self.clients.values() if not c.is_authenticated)
        }
    
    async def start_heartbeat(self, interval_seconds: int = 30):
        """
        Start background heartbeat task to monitor connection health
        
        Args:
            interval_seconds: Interval between heartbeat checks
        """
        async def heartbeat_loop():
            while True:
                await asyncio.sleep(interval_seconds)
                
                now = datetime.now()
                stale_clients = [
                    cid for cid, client in self.clients.items()
                    if (now - client.last_ping).seconds > interval_seconds * 3
                ]
                
                # Disconnect stale clients
                for cid in stale_clients:
                    print(f"[WS] Removing stale client: {cid}")
                    await self.disconnect(cid)
                
                # Broadcast system status periodically
                stats = self.get_connection_stats()
                await self.emit_event(EventType.SYSTEM_STATUS, {
                    "status": "operational",
                    "active_connections": stats["active_connections"],
                    "uptime_check": now.isoformat()
                })
        
        self._heartbeat_task = asyncio.create_task(heartbeat_loop())
        print("[WS] Heartbeat task started")
    
    async def stop_heartbeat(self):
        """Stop the background heartbeat task"""
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
            print("[WS] Heartbeat task stopped")


# ==================== SPECIALIZED EMITTERS FOR AI WIKI ====================

class WikiEventEmitter:
    """
    High-level event emitter for AI Wiki operations
    
    Provides convenience methods for emitting common wiki events
    with standardized payload structures.
    """
    
    def __init__(self, ws_manager: WebSocketManager):
        self.ws = ws_manager
    
    async def emit_trace_span_created(self, span_data: Dict):
        """Emit event when new trace span is created"""
        await self.ws.emit_event(EventType.TRACE_SPAN_CREATED, {
            "span_id": span_data.get("id"),
            "operation": span_data.get("operation"),
            "source": span_data.get("source"),
            "status": span_data.get("status", "pending"),
            "user_id": span_data.get("user_id"),
            "metadata": span_data.get("metadata", {}),
            "timestamp": datetime.now().isoformat()
        })
    
    async def emit_trace_span_updated(self, span_id: str, updates: Dict):
        """Emit event when trace span is updated"""
        await self.ws.emit_event(EventType.TRACE_SPAN_UPDATED, {
            "span_id": span_id,
            "updates": updates,
            "timestamp": datetime.now().isoformat()
        })
    
    async def emit_trace_event(self, event_data: Dict):
        """Emit timeline event"""
        await self.ws.emit_event(EventType.TRACE_EVENT_ADDED, {
            "span_id": event_data.get("span_id"),
            "operation": event_data.get("operation"),
            "source": event_data.get("source"),
            "details": event_data.get("details", ""),
            "duration": event_data.get("duration", "0ms"),
            "tokens": event_data.get("tokens", 0),
            "cost": event_data.get("cost", 0.0),
            "timestamp": datetime.now().isoformat()
        })
    
    async def emit_cost_recorded(self, record_data: Dict):
        """Emit event when cost is recorded"""
        await self.ws.emit_event(EventType.COST_RECORDED, {
            "span_id": record_data.get("span_id"),
            "operation": record_data.get("operation"),
            "tokens": record_data.get("tokens", 0),
            "cost": record_data.get("cost", 0.0),
            "layer": record_data.get("layer", "unknown"),
            "running_total": record_data.get("running_total", 0),
            "budget_percent": record_data.get("budget_percent", 0),
            "timestamp": datetime.now().isoformat()
        })
        
        # Check budget warning threshold (>80%)
        if record_data.get("budget_percent", 0) > 80:
            await self.ws.emit_event(EventType.COST_BUDGET_WARNING, {
                "usage_percent": record_data["budget_percent"],
                "remaining_budget": record_data.get("remaining", 0),
                "warning": "Approaching budget limit",
                "severity": "warning" if record_data["budget_percent"] < 95 else "critical"
            })
    
    async def emit_wiki_page_created(self, page_data: Dict):
        """Emit event when wiki page is created"""
        await self.ws.emit_event(EventType.WIKI_PAGE_CREATED, {
            "page_id": page_data.get("id"),
            "title": page_data.get("title"),
            "page_type": page_data.get("page_type"),
            "author_id": page_data.get("user_id"),
            "quality_score": page_data.get("quality_score", 0),
            "version": page_data.get("version", 1),
            "timestamp": datetime.now().isoformat()
        })
    
    async def emit_wiki_page_updated(self, page_id: str, updates: Dict):
        """Emit event when wiki page is updated"""
        await self.ws.emit_event(EventType.WIKI_PAGE_UPDATED, {
            "page_id": page_id,
            "updates": updates,
            "new_version": updates.get("version"),
            "change_summary": updates.get("change_summary", ""),
            "timestamp": datetime.now().isoformat()
        })
    
    async def emit_ingest_progress(self, phase: str, progress_percent: int, 
                                   details: str = "", span_id: str = None):
        """Emit ingestion progress update"""
        await self.ws.emit_event(EventType.INGEST_PROGRESS, {
            "phase": phase,
            "progress": progress_percent,
            "details": details,
            "span_id": span_id,
            "timestamp": datetime.now().isoformat()
        })
    
    async def emit_query_completed(self, query_result: Dict):
        """Emit event when query is completed"""
        await self.ws.emit_event(EventType.QUERY_COMPLETED, {
            "question": query_result.get("question", ""),
            "answer_preview": query_result.get("answer", "")[:200],
            "confidence": query_result.get("confidence_score", 0),
            "sources_count": len(query_result.get("sources_cited", [])),
            "tokens_used": query_result.get("total_tokens", 0),
            "cost": query_result.get("total_cost", 0.0),
            "timestamp": datetime.now().isoformat()
        })
    
    async def emit_lint_completed(self, lint_report: Dict):
        """Emit event when LINT check is completed"""
        await self.ws.emit_event(EventType.LINT_COMPLETED, {
            "overall_score": lint_report.get("overall_quality_score", 0),
            "checks_passed": lint_report.get("checks_passed", 0),
            "checks_failed": lint_report.get("checks_failed", 0),
            "issues_found": len(lint_report.get("issues_found", [])),
            "contradictions": len(lint_report.get("contradictions_detected", [])),
            "recommendations": lint_report.get("recommendations", [])[:5],
            "tokens_used": lint_report.get("total_tokens", 0),
            "cost": lint_report.get("total_cost", 0.0),
            "timestamp": datetime.now().isoformat()
        })
    
    async def emit_autoresearch_status(self, session_id: str, status: str, 
                                       details: Dict = None):
        """Emit AutoResearch session status update"""
        await self.ws.emit_event(EventType.AUTORESEARCH_STATUS, {
            "session_id": session_id,
            "status": status,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        })
    
    async def emit_autoresearch_completed(self, session_result: Dict):
        """Emit AutoResearch completion event"""
        await self.ws.emit_event(EventType.AUTORESEARCH_COMPLETED, {
            "session_id": session_result.get("research_id"),
            "query": session_result.get("query", ""),
            "sources_found": session_result.get("sources_found", 0),
            "pages_created": session_result.get("wiki_pages_created", 0),
            "tokens_used": session_result.get("tokens_used", 0),
            "cost": session_result.get("cost_usd", 0.0),
            "findings_summary": session_result.get("findings_summary", "")[:300],
            "timestamp": datetime.now().isoformat()
        })
    
    async def emit_system_notification(self, title: str, message: str, 
                                       level: str = "info"):
        """Emit general system notification"""
        await self.ws.emit_event(EventType.SYSTEM_NOTIFICATION, {
            "title": title,
            "message": message,
            "level": level,  # info, warning, error, success
            "timestamp": datetime.now().isoformat()
        })


# Global instances
ws_manager_instance: Optional[WebSocketManager] = None
wiki_emitter_instance: Optional[WikiEventEmitter] = None


def get_ws_manager() -> WebSocketManager:
    """Get or create global WebSocket manager instance"""
    global ws_manager_instance
    if ws_manager_instance is None:
        ws_manager_instance = WebSocketManager()
    return ws_manager_instance


def get_wiki_emitter() -> WikiEventEmitter:
    """Get or create global Wiki event emitter instance"""
    global wiki_emitter_instance
    if wiki_emitter_instance is None:
        wiki_emitter_instance = WikiEventEmitter(get_ws_manager())
    return wiki_emitter_instance
