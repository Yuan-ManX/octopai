"""
SQLite Database Layer for AI Wiki - Persistent Storage System

Database Schema Design:
- Users: Multi-tenant authentication and authorization
- Wiki Pages: Version-controlled knowledge base with full history
- Sources: Immutable document collection with SHA256 hashing
- Knowledge Graph: Nodes and edges with weighted relationships
- Trace Spans: OctoTrace integration with hierarchical operation tracking
- Cost Records: LLM token usage and budget monitoring
- Activity Log: Unified timeline for all operations
- AutoResearch: Bidirectional data flow with AutoResearch module

Features:
- SQLite for lightweight, serverless persistence
- Full version history with diff support
- Multi-tenant isolation via user_id foreign keys
- Indexing for fast query performance
- Transactional integrity for complex operations
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import json
import hashlib


class WikiDatabase:
    """SQLite database manager for AI Wiki persistent storage"""
    
    def __init__(self, db_path: str = "wiki_database.db"):
        """
        Initialize database connection and create tables if not exist
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        # Enable WAL mode for better concurrent performance
        self.conn.execute('PRAGMA journal_mode=WAL')
        self.conn.execute('PRAGMA synchronous=NORMAL')
        
        # Create all tables
        self._create_tables()
        self._create_indexes()
    
    def _create_tables(self):
        """Create all database tables with proper schema"""
        cursor = self.conn.cursor()
        
        # Users table - Authentication and multi-tenancy
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                settings TEXT DEFAULT '{}'
            )
        ''')
        
        # Wiki Pages table - Core knowledge base with versioning
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wiki_pages (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                page_type TEXT NOT NULL,
                content TEXT NOT NULL,
                frontmatter TEXT DEFAULT '{}',
                quality_score REAL DEFAULT 0.0,
                version INTEGER DEFAULT 1,
                status TEXT DEFAULT 'draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Wiki Page Versions table - Complete version history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wiki_page_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                version_number INTEGER NOT NULL,
                content TEXT NOT NULL,
                frontmatter TEXT DEFAULT '{}',
                change_summary TEXT,
                diff_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (page_id) REFERENCES wiki_pages(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(page_id, version_number)
            )
        ''')
        
        # Sources table - Raw document layer (immutable)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_path TEXT,
                size_bytes INTEGER DEFAULT 0,
                sha256_hash TEXT UNIQUE,
                status TEXT DEFAULT 'pending',
                content TEXT,
                metadata TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ingested_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Knowledge Graph Nodes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS graph_nodes (
                id TEXT PRIMARY KEY,
                label TEXT NOT NULL,
                group_type TEXT DEFAULT 'concept',
                page_id TEXT,
                connections INTEGER DEFAULT 0,
                metadata TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (page_id) REFERENCES wiki_pages(id)
            )
        ''')
        
        # Knowledge Graph Edges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS graph_edges (
                id TEXT PRIMARY KEY,
                source_node_id TEXT NOT NULL,
                target_node_id TEXT NOT NULL,
                weight REAL DEFAULT 0.5,
                edge_type TEXT DEFAULT 'related',
                metadata TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_node_id) REFERENCES graph_nodes(id),
                FOREIGN KEY (target_node_id) REFERENCES graph_nodes(id)
            )
        ''')
        
        # Trace Spans table - OctoTrace integration
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trace_spans (
                id TEXT PRIMARY KEY,
                parent_id TEXT,
                operation TEXT NOT NULL,
                source TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP,
                duration_ms REAL,
                status TEXT DEFAULT 'pending',
                tokens_used INTEGER DEFAULT 0,
                cost_usd REAL DEFAULT 0.0,
                details TEXT DEFAULT '',
                metadata TEXT DEFAULT '{}',
                user_id TEXT,
                FOREIGN KEY (parent_id) REFERENCES trace_spans(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Trace Events table - Timeline events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trace_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                span_id TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                operation TEXT NOT NULL,
                source TEXT NOT NULL,
                details TEXT DEFAULT '',
                duration TEXT DEFAULT '0ms',
                tokens INTEGER DEFAULT 0,
                cost REAL DEFAULT 0.0,
                FOREIGN KEY (span_id) REFERENCES trace_spans(id)
            )
        ''')
        
        # Cost Records table - Budget tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cost_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                span_id TEXT,
                timestamp TIMESTAMP NOT NULL,
                operation TEXT NOT NULL,
                tokens INTEGER DEFAULT 0,
                cost REAL DEFAULT 0.0,
                layer TEXT DEFAULT 'unknown',
                user_id TEXT,
                FOREIGN KEY (span_id) REFERENCES trace_spans(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Activity Log table - Unified timeline
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action TEXT NOT NULL,
                entity_type TEXT,
                entity_id TEXT,
                details TEXT DEFAULT '{}',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # AutoResearch sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autoresearch_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                query TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                sources_found INTEGER DEFAULT 0,
                wiki_pages_created INTEGER DEFAULT 0,
                graph_edges_added INTEGER DEFAULT 0,
                tokens_used INTEGER DEFAULT 0,
                cost_usd REAL DEFAULT 0.0,
                findings_summary TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Wiki-AutoResearch links table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wiki_research_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wiki_page_id TEXT NOT NULL,
                research_session_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (wiki_page_id) REFERENCES wiki_pages(id),
                FOREIGN KEY (research_session_id) REFERENCES autoresearch_sessions(id),
                UNIQUE(wiki_page_id, research_session_id)
            )
        ''')
        
        # Export Jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS export_jobs (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                export_type TEXT NOT NULL,
                entity_type TEXT,
                entity_ids TEXT DEFAULT '[]',
                status TEXT DEFAULT 'pending',
                file_path TEXT,
                file_size INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                error_message TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        self.conn.commit()
    
    def _create_indexes(self):
        """Create database indexes for query performance optimization"""
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_wiki_pages_user ON wiki_pages(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_wiki_pages_type ON wiki_pages(page_type)',
            'CREATE INDEX IF NOT EXISTS idx_wiki_pages_updated ON wiki_pages(updated_at DESC)',
            'CREATE INDEX IF NOT EXISTS idx_sources_user ON sources(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_sources_hash ON sources(sha256_hash)',
            'CREATE INDEX IF NOT EXISTS idx_trace_spans_user ON trace_spans(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_trace_spans_operation ON trace_spans(operation)',
            'CREATE INDEX IF NOT EXISTS idx_trace_spans_status ON trace_spans(status)',
            'CREATE INDEX IF NOT EXISTS idx_trace_events_span ON trace_events(span_id)',
            'CREATE INDEX IF NOT EXISTS idx_trace_events_timestamp ON trace_events(timestamp DESC)',
            'CREATE INDEX IF NOT EXISTS idx_cost_records_user ON cost_records(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_cost_records_timestamp ON cost_records(timestamp)',
            'CREATE INDEX IF NOT EXISTS idx_activity_log_user ON activity_log(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_activity_log_timestamp ON activity_log(timestamp DESC)',
            'CREATE INDEX IF NOT EXISTS idx_versions_page ON wiki_page_versions(page_id)',
            'CREATE INDEX IF NOT EXISTS idx_graph_edges_source ON graph_edges(source_node_id)',
            'CREATE INDEX IF NOT EXISTS idx_graph_edges_target ON graph_edges(target_node_id)'
        ]
        
        cursor = self.conn.cursor()
        for index_sql in indexes:
            cursor.execute(index_sql)
        self.conn.commit()
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, user_id: str, username: str, email: str, 
                   hashed_password: str, role: str = 'user') -> bool:
        """Create a new user account"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO users (id, username, email, hashed_password, role)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, email, hashed_password, role))
            self.conn.commit()
            
            # Log the activity
            self.log_activity(user_id, 'USER_CREATED', 'user', user_id, 
                            {'username': username, 'email': email})
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_user(self, user_id: str = None, username: str = None) -> Optional[Dict]:
        """Get user by ID or username"""
        cursor = self.conn.cursor()
        if user_id:
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        elif username:
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        else:
            return None
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def authenticate_user(self, username: str, password_hash: str) -> Optional[Dict]:
        """Authenticate user credentials"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND hashed_password = ? AND is_active = 1
        ''', (username, password_hash))
        
        row = cursor.fetchone()
        if row:
            user_dict = dict(row)
            # Update last login time
            cursor.execute('''
                UPDATE users SET last_login = ? WHERE id = ?
            ''', (datetime.now().isoformat(), user_dict['id']))
            self.conn.commit()
            return user_dict
        return None
    
    # ==================== WIKI PAGE OPERATIONS ====================
    
    def create_wiki_page(self, page_id: str, user_id: str, title: str, 
                        page_type: str, content: str, 
                        frontmatter: Dict = None) -> Dict:
        """Create a new wiki page with initial version"""
        cursor = self.conn.cursor()
        
        frontmatter_json = json.dumps(frontmatter or {})
        now = datetime.now().isoformat()
        
        # Insert main page record
        cursor.execute('''
            INSERT INTO wiki_pages (id, user_id, title, page_type, content, 
                                   frontmatter, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (page_id, user_id, title, page_type, content, frontmatter_json, now, now))
        
        # Create initial version record
        cursor.execute('''
            INSERT INTO wiki_page_versions (page_id, user_id, version_number, 
                                          content, frontmatter, change_summary)
            VALUES (?, ?, 1, ?, ?, ?)
        ''', (page_id, user_id, content, frontmatter_json, 'Initial version'))
        
        self.conn.commit()
        
        # Log activity
        self.log_activity(user_id, 'PAGE_CREATED', 'wiki_page', page_id,
                         {'title': title, 'type': page_type})
        
        return self.get_wiki_page(page_id)
    
    def get_wiki_page(self, page_id: str) -> Optional[Dict]:
        """Get wiki page by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM wiki_pages WHERE id = ?', (page_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_wiki_page(self, page_id: str, user_id: str, content: str = None,
                        title: str = None, frontmatter: Dict = None,
                        change_summary: str = '') -> Optional[Dict]:
        """Update wiki page and create new version"""
        cursor = self.conn.cursor()
        
        # Get current page
        current = self.get_wiki_page(page_id)
        if not current:
            return None
        
        new_version = current['version'] + 1
        now = datetime.now().isoformat()
        
        # Calculate diff from previous version
        old_content = current['content']
        new_content = content if content is not None else old_content
        diff_content = self._calculate_diff(old_content, new_content)
        
        # Update fields
        updates = []
        values = []
        
        if title is not None:
            updates.append('title = ?')
            values.append(title)
        if content is not None:
            updates.append('content = ?')
            values.append(content)
        if frontmatter is not None:
            updates.append('frontmatter = ?')
            values.append(json.dumps(frontmatter))
        
        updates.append('version = ?')
        values.append(new_version)
        updates.append('updated_at = ?')
        values.append(now)
        values.append(page_id)
        
        cursor.execute(f'''
            UPDATE wiki_pages SET {', '.join(updates)} WHERE id = ?
        ''', values)
        
        # Create version record
        current_frontmatter = json.loads(current['frontmatter'])
        new_frontmatter = frontmatter if frontmatter is not None else current_frontmatter
        
        cursor.execute('''
            INSERT INTO wiki_page_versions 
            (page_id, user_id, version_number, content, frontmatter, 
             change_summary, diff_content)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (page_id, user_id, new_version, new_content, 
              json.dumps(new_frontmatter), change_summary, diff_content))
        
        self.conn.commit()
        
        # Log activity
        self.log_activity(user_id, 'PAGE_UPDATED', 'wiki_page', page_id,
                         {'version': new_version, 'summary': change_summary})
        
        return self.get_wiki_page(page_id)
    
    def get_wiki_page_versions(self, page_id: str, limit: int = 20) -> List[Dict]:
        """Get version history for a wiki page"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT v.*, u.username as author_username
            FROM wiki_page_versions v
            LEFT JOIN users u ON v.user_id = u.id
            WHERE v.page_id = ?
            ORDER BY v.version_number DESC
            LIMIT ?
        ''', (page_id, limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_wiki_page_version(self, page_id: str, version: int) -> Optional[Dict]:
        """Get specific version of a wiki page"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT v.*, u.username as author_username
            FROM wiki_page_versions v
            LEFT JOIN users u ON v.user_id = u.id
            WHERE v.page_id = ? AND v.version_number = ?
        ''', (page_id, version))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def list_wiki_pages(self, user_id: str = None, page_type: str = None,
                       limit: int = 50, offset: int = 0) -> List[Dict]:
        """List wiki pages with optional filters"""
        cursor = self.conn.cursor()
        
        conditions = []
        params = []
        
        if user_id:
            conditions.append('wp.user_id = ?')
            params.append(user_id)
        if page_type:
            conditions.append('wp.page_type = ?')
            params.append(page_type)
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        cursor.execute(f'''
            SELECT wp.*, u.username as author_username
            FROM wiki_pages wp
            LEFT JOIN users u ON wp.user_id = u.id
            {where_clause}
            ORDER BY wp.updated_at DESC
            LIMIT ? OFFSET ?
        ''', params + [limit, offset])
        
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_wiki_page(self, page_id: str, user_id: str) -> bool:
        """Soft delete a wiki page (mark as deleted)"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE wiki_pages SET status = 'deleted', updated_at = ?
            WHERE id = ? AND user_id = ?
        ''', (datetime.now().isoformat(), page_id, user_id))
        self.conn.commit()
        
        if cursor.rowcount > 0:
            self.log_activity(user_id, 'PAGE_DELETED', 'wiki_page', page_id)
            return True
        return False
    
    # ==================== SOURCE OPERATIONS ====================
    
    def create_source(self, source_id: str, user_id: str, name: str,
                     file_type: str, file_path: str = None,
                     content: str = None, metadata: Dict = None) -> Dict:
        """Create a new source document"""
        cursor = self.conn.cursor()
        
        # Calculate SHA256 hash if content provided
        sha256_hash = None
        size_bytes = 0
        if content:
            content_bytes = content.encode('utf-8')
            sha256_hash = hashlib.sha256(content_bytes).hexdigest()
            size_bytes = len(content_bytes)
        
        metadata_json = json.dumps(metadata or {})
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO sources (id, user_id, name, file_type, file_path, 
                                size_bytes, sha256_hash, content, metadata, 
                                created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (source_id, user_id, name, file_type, file_path, size_bytes,
              sha256_hash, content, metadata_json, now))
        
        self.conn.commit()
        
        self.log_activity(user_id, 'SOURCE_CREATED', 'source', source_id,
                         {'name': name, 'type': file_type, 'hash': sha256_hash})
        
        return self.get_source(source_id)
    
    def get_source(self, source_id: str) -> Optional[Dict]:
        """Get source by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM sources WHERE id = ?', (source_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_source_by_hash(self, sha256_hash: str) -> Optional[Dict]:
        """Get source by SHA256 hash (for incremental cache)"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM sources WHERE sha256_hash = ?', (sha256_hash,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_source_status(self, source_id: str, status: str) -> bool:
        """Update source processing status"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat() if status == 'ingested' else None
        
        cursor.execute('''
            UPDATE sources SET status = ?, ingested_at = ?
            WHERE id = ?
        ''', (status, now, source_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def list_sources(self, user_id: str = None, status: str = None,
                    limit: int = 50) -> List[Dict]:
        """List sources with optional filters"""
        cursor = self.conn.cursor()
        
        conditions = []
        params = []
        
        if user_id:
            conditions.append('s.user_id = ?')
            params.append(user_id)
        if status:
            conditions.append('s.status = ?')
            params.append(status)
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        cursor.execute(f'''
            SELECT s.* FROM sources s
            {where_clause}
            ORDER BY s.created_at DESC
            LIMIT ?
        ''', params + [limit])
        
        return [dict(row) for row in cursor.fetchall()]
    
    # ==================== KNOWLEDGE GRAPH OPERATIONS ====================
    
    def create_graph_node(self, node_id: str, label: str, group_type: str = 'concept',
                         page_id: str = None, metadata: Dict = None) -> Dict:
        """Create a knowledge graph node"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO graph_nodes (id, label, group_type, page_id, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (node_id, label, group_type, page_id, json.dumps(metadata or {}),
              datetime.now().isoformat()))
        
        self.conn.commit()
        return self.get_graph_node(node_id)
    
    def get_graph_node(self, node_id: str) -> Optional[Dict]:
        """Get graph node by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM graph_nodes WHERE id = ?', (node_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def create_graph_edge(self, edge_id: str, source_id: str, target_id: str,
                         weight: float = 0.5, edge_type: str = 'related',
                         metadata: Dict = None) -> Dict:
        """Create a knowledge graph edge"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO graph_edges (id, source_node_id, target_node_id, 
                                    weight, edge_type, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (edge_id, source_id, target_id, weight, edge_type,
              json.dumps(metadata or {}), datetime.now().isoformat()))
        
        # Update connection counts
        cursor.execute('''
            UPDATE graph_nodes SET connections = connections + 1 WHERE id = ?
        ''', (source_id,))
        cursor.execute('''
            UPDATE graph_nodes SET connections = connections + 1 WHERE id = ?
        ''', (target_id,))
        
        self.conn.commit()
        return self.get_graph_edge(edge_id)
    
    def get_graph_edge(self, edge_id: str) -> Optional[Dict]:
        """Get graph edge by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM graph_edges WHERE id = ?', (edge_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_knowledge_graph(self) -> Dict:
        """Get complete knowledge graph structure"""
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT * FROM graph_nodes')
        nodes = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute('SELECT * FROM graph_edges')
        edges = [dict(row) for row in cursor.fetchall()]
        
        return {
            'nodes': nodes,
            'edges': edges,
            'total_nodes': len(nodes),
            'total_edges': len(edges)
        }
    
    # ==================== TRACE OPERATIONS (OctoTrace Integration) ====================
    
    def create_trace_span(self, span_data: Dict) -> str:
        """Create a new trace span for operation tracking"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO trace_spans 
            (id, parent_id, operation, source, start_time, end_time, 
             duration_ms, status, tokens_used, cost_usd, details, metadata, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            span_data.get('id'),
            span_data.get('parent_id'),
            span_data.get('operation'),
            span_data.get('source'),
            span_data.get('start_time'),
            span_data.get('end_time'),
            span_data.get('duration_ms'),
            span_data.get('status', 'pending'),
            span_data.get('tokens_used', 0),
            span_data.get('cost_usd', 0.0),
            span_data.get('details', ''),
            json.dumps(span_data.get('metadata', {})),
            span_data.get('user_id')
        ))
        
        self.conn.commit()
        return span_data.get('id')
    
    def update_trace_span(self, span_id: str, **kwargs) -> bool:
        """Update trace span fields"""
        cursor = self.conn.cursor()
        
        sets = []
        values = []
        for key, value in kwargs.items():
            sets.append(f'{key} = ?')
            values.append(value)
        values.append(span_id)
        
        cursor.execute(f'''
            UPDATE trace_spans SET {', '.join(sets)} WHERE id = ?
        ''', values)
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_trace_span(self, span_id: str) -> Optional[Dict]:
        """Get trace span by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM trace_spans WHERE id = ?', (span_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_trace_span_tree(self, root_id: str = None) -> Dict:
        """Get hierarchical span tree structure"""
        cursor = self.conn.cursor()
        
        if root_id:
            cursor.execute('SELECT * FROM trace_spans WHERE id = ?', (root_id,))
        else:
            # Get root spans (those without parents)
            cursor.execute('''
                SELECT * FROM trace_spans 
                WHERE parent_id IS NULL 
                ORDER BY start_time DESC LIMIT 1
            ''')
        
        root_row = cursor.fetchone()
        if not root_row:
            return {'root_span': None}
        
        root = dict(root_row)
        
        # Recursively build children
        def build_children(parent_id: str) -> List[Dict]:
            cursor.execute('''
                SELECT * FROM trace_spans WHERE parent_id = ? ORDER BY start_time
            ''', (parent_id,))
            children = []
            for row in cursor.fetchall():
                child = dict(row)
                child['children'] = build_children(child['id'])
                children.append(child)
            return children
        
        root['children'] = build_children(root['id'])
        
        # Get summary statistics
        cursor.execute('SELECT COUNT(*) as total, SUM(tokens_used) as total_tokens, '
                      'SUM(cost_usd) as total_cost FROM trace_spans')
        stats = dict(cursor.fetchone())
        
        return {
            'root_span': root,
            'summary': stats
        }
    
    def list_trace_spans(self, user_id: str = None, operation: str = None,
                        status: str = None, limit: int = 50) -> List[Dict]:
        """List trace spans with filters"""
        cursor = self.conn.cursor()
        
        conditions = []
        params = []
        
        if user_id:
            conditions.append('ts.user_id = ?')
            params.append(user_id)
        if operation:
            conditions.append('ts.operation = ?')
            params.append(operation)
        if status:
            conditions.append('ts.status = ?')
            params.append(status)
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        cursor.execute(f'''
            SELECT ts.* FROM trace_spans ts
            {where_clause}
            ORDER BY ts.start_time DESC
            LIMIT ?
        ''', params + [limit])
        
        return [dict(row) for row in cursor.fetchall()]
    
    def create_trace_event(self, event_data: Dict) -> int:
        """Create a timeline event"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO trace_events 
            (span_id, timestamp, operation, source, details, duration, tokens, cost)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_data.get('span_id'),
            event_data.get('timestamp'),
            event_data.get('operation'),
            event_data.get('source'),
            event_data.get('details', ''),
            event_data.get('duration', '0ms'),
            event_data.get('tokens', 0),
            event_data.get('cost', 0.0)
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_evolution_timeline(self, limit: int = 50) -> Dict:
        """Get chronological evolution timeline"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT te.*, ts.status as span_status
            FROM trace_events te
            LEFT JOIN trace_spans ts ON te.span_id = ts.id
            ORDER BY te.timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        events = [dict(row) for row in cursor.fetchall()]
        
        # Calculate summary
        cursor.execute('''
            SELECT COUNT(*) as total,
                   SUM(te.tokens) as total_tokens,
                   SUM(te.cost) as total_cost,
                   COUNT(CASE WHEN te.operation = 'INGEST' THEN 1 END) as ingest_count,
                   COUNT(CASE WHEN te.operation = 'QUERY' THEN 1 END) as query_count,
                   COUNT(CASE WHEN te.operation = 'LINT' THEN 1 END) as lint_count,
                   COUNT(CASE WHEN te.operation = 'DEEP_RESEARCH' THEN 1 END) as research_count
            FROM trace_events te
        ''')
        summary = dict(cursor.fetchone())
        
        return {
            'total_events': len(events),
            'events': events,
            'summary': summary
        }
    
    # ==================== COST TRACKING OPERATIONS ====================
    
    def create_cost_record(self, record_data: Dict) -> int:
        """Create a cost tracking record"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO cost_records 
            (span_id, timestamp, operation, tokens, cost, layer, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            record_data.get('span_id'),
            record_data.get('timestamp'),
            record_data.get('operation'),
            record_data.get('tokens', 0),
            record_data.get('cost', 0.0),
            record_data.get('layer', 'unknown'),
            record_data.get('user_id')
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_cost_analytics(self, user_id: str = None, days: int = 7) -> Dict:
        """Get comprehensive cost analytics"""
        cursor = self.conn.cursor()
        
        base_conditions = []
        params = []
        
        if user_id:
            base_conditions.append('cr.user_id = ?')
            params.append(user_id)
        
        where_clause = f"WHERE {' AND '.join(base_conditions)}" if base_conditions else ""
        
        # Total statistics
        cursor.execute(f'''
            SELECT COALESCE(SUM(cr.tokens), 0) as total_tokens,
                   COALESCE(SUM(cr.cost), 0) as total_cost,
                   COUNT(*) as total_operations
            FROM cost_records cr
            {where_clause}
        ''', params)
        totals = dict(cursor.fetchone())
        
        # By operation type
        cursor.execute(f'''
            SELECT cr.operation,
                   SUM(cr.tokens) as tokens,
                   SUM(cr.cost) as cost,
                   COUNT(*) as count
            FROM cost_records cr
            {where_clause}
            GROUP BY cr.operation
        ''', params)
        by_operation = [dict(row) for row in cursor.fetchall()]
        
        # By layer
        cursor.execute(f'''
            SELECT cr.layer, SUM(cr.tokens) as tokens
            FROM cost_records cr
            {where_clause}
            GROUP BY cr.layer
        ''', params)
        by_layer = {row['layer']: row['tokens'] for row in cursor.fetchall()}
        
        # Daily usage trend
        from datetime import timedelta
        daily_usage = []
        for i in range(days):
            day = datetime.now() - timedelta(days=days-1-i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            daily_params = params + [day_start.isoformat(), day_end.isoformat()]
            cursor.execute(f'''
                SELECT COALESCE(SUM(cr.tokens), 0) as tokens,
                       COALESCE(SUM(cr.cost), 0) as cost
                FROM cost_records cr
                {where_clause}
                AND cr.timestamp >= ? AND cr.timestamp < ?
            ''', daily_params)
            day_stats = dict(cursor.fetchone())
            
            daily_usage.append({
                'date': day.strftime('%Y-%m-%d'),
                'tokens': day_stats['tokens'],
                'cost': round(day_stats['cost'], 4)
            })
        
        # Top operations by cost
        cursor.execute(f'''
            SELECT cr.operation, SUM(cr.cost) as total_cost, SUM(cr.tokens) as tokens
            FROM cost_records cr
            {where_clause}
            GROUP BY cr.operation
            ORDER BY total_cost DESC
            LIMIT 5
        ''', params)
        top_operations = [dict(row) for row in cursor.fetchall()]
        
        budget_limit = 1.00  # Default budget
        total_cost = totals['total_cost']
        
        return {
            'total_tokens': totals['total_tokens'],
            'total_cost': round(total_cost, 3),
            'budget': budget_limit,
            'budget_remaining': round(budget_limit - total_cost, 3),
            'budget_usage_percent': round((total_cost / budget_limit) * 100, 1) if budget_limit > 0 else 0,
            'operations': {
                op['operation']: {
                    'tokens': op['tokens'],
                    'cost': round(op['cost'], 4),
                    'count': op['count'],
                    'percent_of_total': round((op['cost'] / total_cost) * 100, 1) if total_cost > 0 else 0
                }
                for op in by_operation
            },
            'token_by_layer': by_layer,
            'daily_usage': daily_usage,
            'top_operations': [
                {
                    'operation': op['operation'],
                    'tokens': op['tokens'],
                    'percentage': round((op['total_cost'] / total_cost) * 100, 1) if total_cost > 0 else 0
                }
                for op in top_operations
            ]
        }
    
    # ==================== ACTIVITY LOG OPERATIONS ====================
    
    def log_activity(self, user_id: str, action: str, entity_type: str = None,
                    entity_id: str = None, details: Dict = None):
        """Log an activity to the unified timeline"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO activity_log (user_id, action, entity_type, entity_id, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, action, entity_type, entity_id, json.dumps(details or {})))
        
        self.conn.commit()
    
    def get_activity_log(self, user_id: str = None, limit: int = 20) -> List[Dict]:
        """Get recent activity log entries"""
        cursor = self.conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT al.*, u.username as username
                FROM activity_log al
                LEFT JOIN users u ON al.user_id = u.id
                WHERE al.user_id = ?
                ORDER BY al.timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT al.*, u.username as username
                FROM activity_log al
                LEFT JOIN users u ON al.user_id = u.id
                ORDER BY al.timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # ==================== AUTORESEARCH OPERATIONS ====================
    
    def create_autoresearch_session(self, session_data: Dict) -> str:
        """Create a new AutoResearch session"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO autoresearch_sessions 
            (id, user_id, query, status, findings_summary, created_at)
            VALUES (?, ?, ?, 'pending', '', ?)
        ''', (
            session_data.get('id'),
            session_data.get('user_id'),
            session_data.get('query'),
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
        return session_data.get('id')
    
    def update_autoresearch_session(self, session_id: str, **kwargs) -> bool:
        """Update AutoResearch session"""
        cursor = self.conn.cursor()
        
        sets = []
        values = []
        for key, value in kwargs.items():
            if key == 'completed_at' and value is True:
                sets.append('completed_at = ?')
                values.append(datetime.now().isoformat())
            else:
                sets.append(f'{key} = ?')
                values.append(value)
        values.append(session_id)
        
        cursor.execute(f'''
            UPDATE autoresearch_sessions SET {', '.join(sets)} WHERE id = ?
        ''', values)
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_autoresearch_session(self, session_id: str) -> Optional[Dict]:
        """Get AutoResearch session by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM autoresearch_sessions WHERE id = ?', (session_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def link_wiki_to_research(self, wiki_page_id: str, research_session_id: str):
        """Link a wiki page to an AutoResearch session"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO wiki_research_links (wiki_page_id, research_session_id)
                VALUES (?, ?)
            ''', (wiki_page_id, research_session_id))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # Link already exists
    
    def get_sync_statistics(self) -> Dict:
        """Get AutoResearch-Wiki synchronization statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM autoresearch_sessions')
        total_research = dict(cursor.fetchone())['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM wiki_research_links')
        total_links = dict(cursor.fetchone())['total']
        
        cursor.execute('''
            SELECT COUNT(*) as completed, 
                   COALESCE(SUM(sources_found), 0) as total_sources,
                   COALESCE(SUM(tokens_used), 0) as total_tokens,
                   COALESCE(SUM(cost_usd), 0) as total_cost
            FROM autoresearch_sessions WHERE status = 'completed'
        ''')
        completed_stats = dict(cursor.fetchone())
        
        return {
            'total_sessions': total_research,
            'completed_sessions': completed_stats['completed'],
            'wiki_pages_from_research': total_links,
            'total_sources_discovered': completed_stats['total_sources'],
            'total_tokens_for_research': completed_stats['total_tokens'],
            'total_cost_for_research': completed_stats['total_cost']
        }
    
    # ==================== EXPORT OPERATIONS ====================
    
    def create_export_job(self, job_id: str, user_id: str, export_type: str,
                         entity_type: str = None, entity_ids: List[str] = None) -> str:
        """Create a new export job"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO export_jobs (id, user_id, export_type, entity_type, 
                                    entity_ids, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'pending', ?)
        ''', (job_id, user_id, export_type, entity_type,
              json.dumps(entity_ids or []), datetime.now().isoformat()))
        
        self.conn.commit()
        return job_id
    
    def update_export_job(self, job_id: str, **kwargs) -> bool:
        """Update export job status"""
        cursor = self.conn.cursor()
        
        sets = []
        values = []
        for key, value in kwargs.items():
            if key == 'completed_at' and value is True:
                sets.append('completed_at = ?')
                values.append(datetime.now().isoformat())
            else:
                sets.append(f'{key} = ?')
                values.append(value)
        values.append(job_id)
        
        cursor.execute(f'''
            UPDATE export_jobs SET {', '.join(sets)} WHERE id = ?
        ''', values)
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_export_job(self, job_id: str) -> Optional[Dict]:
        """Get export job by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM export_jobs WHERE id = ?', (job_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    # ==================== UTILITY METHODS ====================
    
    @staticmethod
    def _calculate_diff(old_content: str, new_content: str) -> str:
        """Calculate simple diff between two text contents"""
        import difflib
        
        differ = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            lineterm='',
            fromfile='previous',
            tofile='current'
        )
        
        return ''.join(differ)
    
    def get_system_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        cursor = self.conn.cursor()
        
        # Count various entities
        stats = {}
        
        cursor.execute('SELECT COUNT(*) as count FROM users')
        stats['total_users'] = dict(cursor.fetchone())['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM wiki_pages WHERE status != "deleted"')
        stats['total_wiki_pages'] = dict(cursor.fetchone())['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM sources')
        stats['total_sources'] = dict(cursor.fetchone())['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM graph_nodes')
        stats['total_graph_nodes'] = dict(cursor.fetchone())['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM graph_edges')
        stats['total_graph_edges'] = dict(cursor.fetchone())['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM trace_spans')
        stats['total_trace_spans'] = dict(cursor.fetchone())['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM wiki_page_versions')
        stats['total_versions'] = dict(cursor.fetchone())['count']
        
        cursor.execute('SELECT COALESCE(SUM(tokens_used), 0) as total FROM trace_spans')
        stats['total_tokens_traced'] = dict(cursor.fetchone())['total']
        
        cursor.execute('SELECT COALESCE(SUM(cost_usd), 0) as total FROM trace_spans')
        stats['total_cost_traced'] = round(dict(cursor.fetchone())['total'], 3)
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


# Global database instance
db_instance: Optional[WikiDatabase] = None


def get_database(db_path: str = "wiki_database.db") -> WikiDatabase:
    """Get or create global database instance"""
    global db_instance
    if db_instance is None:
        db_instance = WikiDatabase(db_path)
    return db_instance
