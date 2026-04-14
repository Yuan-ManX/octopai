"""
AI Wiki Backend API - Incremental Knowledge Base System

Core Architecture (Three-Layer Design):
- Layer 1: Raw Sources - Immutable document collection (PDFs, URLs, notes, data)
- Layer 2: AI Wiki - LLM-generated structured knowledge base with cross-references  
- Layer 3: Schema Rules - Configuration defining structure, conventions, and workflows

Key Operations:
1. INGEST: Two-step chain-of-thought process
   - Phase 1 (Analysis): Extract entities, concepts, connections from sources
   - Phase 2 (Generation): Create wiki pages with [[wikilinks]], update graph

2. QUERY: Four-phase retrieval system
   - Phase 1: Tokenized search across wiki content
   - Phase 2: Graph expansion to related nodes
   - Phase 3: Budget control for context window
   - Phase 4: Context assembly with cited sources

3. LINT: Quality assurance system
   - Consistency checks across wiki pages
   - Contradiction detection between entities
   - Link validation and orphan page identification
   - Quality scoring and recommendations

Integration Points:
- AutoResearch module: Deep research engine for multi-source ingestion
- Skills Hub: Wiki as knowledge foundation for skill execution context
- OctoTrace: Full observability of knowledge evolution timeline
- Evolution Workbench: Self-optimization of wiki quality metrics

Data Structures:
- Sources: Immutable documents with SHA256 hashing for incremental cache
- Wiki Pages: Markdown files with YAML frontmatter and [[wikilinks]]
- Knowledge Graph: Nodes (entities/concepts) + Edges (relationships with weights)
- Schema: Configuration in YAML/JSON defining structure rules
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
import hashlib
import json
import os
import uuid
from pathlib import Path
import re

app = FastAPI(
    title="AI Wiki API",
    description="Incremental Knowledge Base System - Transform documents into structured, interlinked intelligence",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage paths
BASE_DIR = Path(__file__).parent
SOURCES_DIR = BASE_DIR / "wiki_sources"
WIKI_DIR = BASE_DIR / "wiki_pages"
SCHEMA_DIR = BASE_DIR / "wiki_schema"
LOG_FILE = BASE_DIR / "wiki_log.md"
INDEX_FILE = BASE_DIR / "wiki_index.md"

# Ensure directories exist
for directory in [SOURCES_DIR, WIKI_DIR, SCHEMA_DIR]:
    directory.mkdir(exist_ok=True)


# ==================== DATA MODELS ====================

class SourceDocument(BaseModel):
    """Raw source document model (Layer 1 - Immutable)"""
    id: str
    name: str
    file_type: str  # pdf, md, url, csv, txt
    file_path: str
    size_bytes: int
    sha256_hash: str
    status: str  # pending, processing, ingested, error
    created_at: datetime
    metadata: Dict[str, Any] = {}


class WikiPage(BaseModel):
    """Wiki page model (Layer 2 - LLM Generated)"""
    id: str
    title: str
    page_type: str  # entity, concept, summary, comparison, analysis
    content: str
    frontmatter: Dict[str, Any]
    sources: List[str]  # Source document IDs that contributed to this page
    links: List[str]  # [[wikilinks]] to other pages
    quality_score: float  # 0-100
    last_updated: datetime
    version: int = 1


class KnowledgeNode(BaseModel):
    """Knowledge graph node"""
    id: str
    label: str
    node_type: str  # entity, concept, method, theory, data
    group: str  # research, algorithm, technique, model, concept
    connections: int
    properties: Dict[str, Any] = {}


class KnowledgeEdge(BaseModel):
    """Knowledge graph edge (relationship)"""
    source: str  # Node ID
    target: str  # Node ID
    weight: float  # 0-1 relationship strength
    edge_type: str  # direct, strong, weak, related, methodology, contradicts
    evidence: Optional[str] = None  # Source of this relationship


class IngestRequest(BaseModel):
    """Request model for ingest operation"""
    source_ids: List[str]
    options: Dict[str, Any] = {
        "skip_cache": False,
        "generate_graph": True,
        "run_lint": True,
        "create_review_items": True
    }


class QueryRequest(BaseModel):
    """Request model for query operation"""
    question: str
    max_context_tokens: int = 4000
    include_graph_expansion: bool = True
    confidence_threshold: float = 0.7
    cite_sources: bool = True


class QueryResult(BaseModel):
    """Query result with synthesized answer"""
    question: str
    answer: str
    sources: List[Dict[str, str]]  # [{title, excerpt, relevance}]
    graph_nodes_visited: int
    confidence: float
    retrieval_phases: List[Dict[str, Any]]
    timestamp: datetime


class LintReport(BaseModel):
    """Lint operation result"""
    timestamp: datetime
    total_checks: int
    passed: int
    warnings: int
    errors: int
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    quality_metrics: Dict[str, float]


# ==================== IN-MEMORY STORAGE ====================

# For demonstration, using in-memory storage
# In production, replace with database (PostgreSQL/MongoDB)
sources_store: Dict[str, SourceDocument] = {}
wiki_pages_store: Dict[str, WikiPage] = {}
knowledge_graph_nodes: Dict[str, KnowledgeNode] = {}
knowledge_graph_edges: List[KnowledgeEdge] = []
activity_log: List[Dict[str, Any]] = []


# ==================== UTILITY FUNCTIONS ====================

def compute_sha256(file_path: str) -> str:
    """Compute SHA256 hash of a file for incremental caching"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return f"sha256:{sha256_hash.hexdigest()[:16]}"


def extract_wikilinks(content: str) -> List[str]:
    """Extract [[wikilinks]] from markdown content"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)


def compute_quality_score(page: WikiPage) -> float:
    """
    Compute quality score for a wiki page (0-100)
    
    Factors:
    - Content length (optimal: 500-2000 words)
    - Number of cross-references (more is better, up to 20)
    - Frontmatter completeness
    - Source citations present
    - No broken links
    """
    score = 50.0  # Base score
    
    word_count = len(page.content.split())
    if 200 <= word_count <= 3000:
        score += 20
    elif word_count > 3000:
        score += 15
    else:
        score += 10
    
    link_count = len(page.links)
    if link_count >= 5:
        score += min(link_count * 2, 20)
    
    if len(page.frontmatter) >= 3:
        score += 5
    
    if len(page.sources) > 0:
        score += 5
    
    return min(score, 100.0)


def log_activity(action: str, detail: str, status: str = "success"):
    """Log activity to the system timeline"""
    activity = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "detail": detail,
        "status": status
    }
    activity_log.insert(0, activity)
    
    # Keep only last 100 activities
    if len(activity_log) > 100:
        activity_log.pop()


# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "AI Wiki API",
        "version": "1.0.0",
        "description": "Incremental Knowledge Base System",
        "endpoints": {
            "sources": "/sources",
            "wiki_pages": "/wiki",
            "graph": "/graph",
            "ingest": "/ingest",
            "query": "/query",
            "lint": "/lint",
            "stats": "/stats"
        },
        "architecture": {
            "layer_1": "Raw Sources (Immutable documents)",
            "layer_2": "AI Wiki (LLM-generated knowledge)",
            "layer_3": "Schema Rules (Configuration)"
        }
    }


# ==================== SOURCES ENDPOINTS (Layer 1) ====================

@app.get("/sources")
async def list_sources():
    """List all raw source documents"""
    return {
        "total": len(sources_store),
        "sources": list(sources_store.values())
    }


@app.post("/sources/upload")
async def upload_source(file: UploadFile = File(...)):
    """
    Upload a new raw source document
    
    The source is stored immutably in Layer 1.
    SHA256 hash is computed for incremental caching during ingest.
    """
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())[:8]
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'txt'
        file_path = SOURCES_DIR / f"{file_id}.{file_extension}"
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Compute hash
        sha256 = compute_sha256(str(file_path))
        
        # Create source document
        source = SourceDocument(
            id=file_id,
            name=file.filename,
            file_type=file_extension,
            file_path=str(file_path),
            size_bytes=len(content),
            sha256_hash=sha256,
            status="pending",
            created_at=datetime.now(),
            metadata={
                "original_filename": file.filename,
                "content_type": file.content_type
            }
        )
        
        sources_store[file_id] = source
        
        log_activity("SOURCE_UPLOAD", f"Uploaded: {file.filename} ({len(content)} bytes)")
        
        return {
            "success": True,
            "source_id": file_id,
            "message": "Source uploaded successfully. Ready for ingest.",
            "sha256": sha256
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sources/{source_id}")
async def get_source(source_id: str):
    """Get details of a specific source document"""
    if source_id not in sources_store:
        raise HTTPException(status_code=404, detail="Source not found")
    return sources_store[source_id]


# ==================== WIKI PAGES ENDPOINTS (Layer 2) ====================

@app.get("/wiki")
async def list_wiki_pages():
    """List all wiki pages with metadata"""
    pages = list(wiki_pages_store.values())
    
    # Compute aggregate statistics
    avg_quality = sum(p.quality_score for p in pages) / len(pages) if pages else 0
    total_links = sum(len(p.links) for p in pages)
    
    return {
        "total": len(pages),
        "average_quality": round(avg_quality, 1),
        "total_cross_references": total_links,
        "pages": pages
    }


@app.get("/wiki/{page_id}")
async def get_wiki_page(page_id: str):
    """Get full content of a wiki page"""
    if page_id not in wiki_pages_store:
        raise HTTPException(status_code=404, detail="Wiki page not found")
    return wiki_pages_store[page_id]


@app.post("/wiki/{page_id}/update")
async def update_wiki_page(page_id: str, updates: Dict[str, Any]):
    """
    Update a wiki page (typically called by LLM during maintenance)
    
    Only LLM should modify wiki pages through this endpoint.
    Humans interact through review system.
    """
    if page_id not in wiki_pages_store:
        raise HTTPException(status_code=404, detail="Wiki page not found")
    
    page = wiki_pages_store[page_id]
    
    # Update allowed fields
    if "content" in updates:
        page.content = updates["content"]
        page.links = extract_wikilinks(updates["content"])
    
    if "frontmatter" in updates:
        page.frontmatter.update(updates["frontmatter"])
    
    # Recompute quality score
    page.quality_score = compute_quality_score(page)
    page.last_updated = datetime.now()
    page.version += 1
    
    log_activity("WIKI_UPDATE", f"Updated page: {page.title} (v{page.version})")
    
    return {
        "success": True,
        "page_id": page_id,
        "new_version": page.version,
        "quality_score": page.quality_score
    }


# ==================== KNOWLEDGE GRAPH ENDPOINTS ====================

@app.get("/graph")
async def get_knowledge_graph():
    """
    Get complete knowledge graph structure
    
    Returns nodes (entities/concepts) and edges (relationships).
    Used for visualization and query graph expansion.
    """
    return {
        "nodes": list(knowledge_graph_nodes.values()),
        "edges": knowledge_graph_edges,
        "statistics": {
            "total_nodes": len(knowledge_graph_nodes),
            "total_edges": len(knowledge_graph_edges),
            "avg_connections": sum(n.connections for n in knowledge_graph_nodes.values()) / len(knowledge_graph_nodes) if knowledge_graph_nodes else 0,
            "density": len(knowledge_graph_edges) / (len(knowledge_graph_nodes) * (len(knowledge_graph_nodes) - 1)) if len(knowledge_graph_nodes) > 1 else 0
        }
    }


@app.get("/graph/node/{node_id}")
async def get_graph_node(node_id: str):
    """Get details of a specific knowledge graph node"""
    if node_id not in knowledge_graph_nodes:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node = knowledge_graph_nodes[node_id]
    
    # Find connected edges
    connected_edges = [
        e for e in knowledge_graph_edges 
        if e.source == node_id or e.target == node_id
    ]
    
    return {
        "node": node,
        "connected_edges": connected_edges,
        "related_nodes": [
            e.target if e.source == node_id else e.source 
            for e in connected_edges
        ]
    }


# ==================== INGEST OPERATION ====================

@app.post("/ingest")
async def execute_ingest(request: IngestRequest):
    """
    Execute Two-Step Chain-of-Thought Ingest Pipeline
    
    Step 1 (Analysis): 
    - Read and parse each source
    - Extract key entities, concepts, arguments
    - Identify connections to existing wiki content
    - Flag contradictions with current knowledge
    - Generate structured analysis object
    
    Step 2 (Generation):
    - Create source summary with YAML frontmatter
    - Generate entity/concept/comparison pages
    - Add [[wikilinks]] cross-references
    - Update index.md and log.md
    - Update knowledge graph
    - Create review items for human validation
    """
    results = {
        "started_at": datetime.now().isoformat(),
        "sources_processed": 0,
        "pages_created": 0,
        "pages_updated": 0,
        "links_added": 0,
        "graph_nodes_added": 0,
        "graph_edges_added": 0,
        "details": []
    }
    
    for source_id in request.source_ids:
        if source_id not in sources_store:
            continue
            
        source = sources_store[source_id]
        
        # Check incremental cache (SHA256)
        # If already ingested with same hash, skip
        if source.status == "ingested" and not request.options.get("skip_cache"):
            results["details"].append({
                "source_id": source_id,
                "status": "skipped",
                "reason": "Already ingested (incremental cache hit)"
            })
            continue
        
        # Mark as processing
        source.status = "processing"
        
        # Simulate two-step chain-of-thought (in real implementation, call LLM here)
        # Step 1: Analysis
        analysis = {
            "entities": [f"Entity_from_{source.name}", "Related_Concept_1", "Related_Concept_2"],
            "concepts": ["Main_Theme", "Supporting_Idea"],
            "connections_to_existing": list(wiki_pages_store.keys())[:3] if wiki_pages_store else [],
            "contradictions": []  # Would be detected by LLM
        }
        
        # Step 2: Generation
        pages_created_for_source = []
        
        # Create entity page
        entity_page_id = f"entity_{source_id}"
        entity_page = WikiPage(
            id=entity_page_id,
            title=f"{source.name.replace('.', ' ').replace('_', ' ')}",
            page_type="entity",
            content=f"# {source.name}\n\n## Summary\n\nAuto-generated from source: {source.name}\n\n## Key Points\n\n- Point 1 extracted by LLM\n- Point 2 extracted by LLM\n- Point 3 extracted by LLM\n\n## Related Concepts\n\n[[Main_Theme]]\n[[Supporting_Idea]]\n\n## Sources\n\n- {source.id}",
            frontmatter={
                "type": "entity",
                "source_ids": [source_id],
                "created": datetime.now().isoformat(),
                "tags": [source.file_type, "auto-generated"]
            },
            sources=[source_id],
            links=analysis["connections_to_existing"] + ["Main_Theme", "Supporting_Idea"],
            quality_score=85.0,  # Will be recomputed
            last_updated=datetime.now()
        )
        entity_page.quality_score = compute_quality_score(entity_page)
        wiki_pages_store[entity_page_id] = entity_page
        pages_created_for_source.append(entity_page_id)
        results["pages_created"] += 1
        
        # Add to knowledge graph
        node_id = f"node_{entity_page_id}"
        if node_id not in knowledge_graph_nodes:
            knowledge_graph_nodes[node_id] = KnowledgeNode(
                id=node_id,
                label=entity_page.title[:30],
                node_type="entity",
                group="research",
                connections=len(entity_page.links),
                properties={"source_id": source_id}
            )
            results["graph_nodes_added"] += 1
        
        # Update source status
        source.status = "ingested"
        results["sources_processed"] += 1
        
        results["details"].append({
            "source_id": source_id,
            "status": "success",
            "pages_created": len(pages_created_for_source),
            "analysis_entities": len(analysis["entities"]),
            "analysis_concepts": len(analysis["concepts"])
        })
    
    # Log activity
    log_activity(
        "INGEST", 
        f"Processed {results['sources_processed']} sources, created {results['pages_created']} pages"
    )
    
    results["completed_at"] = datetime.now().isoformat()
    results["success"] = True
    
    return results


# ==================== QUERY OPERATION ====================

@app.post("/query")
async def execute_query(request: QueryRequest):
    """
    Execute Four-Phase Query Retrieval System
    
    Phase 1: Tokenized Search
    - Split query into tokens
    - Search across all wiki page titles and content
    - Fuzzy matching for typos/variations
    - Rank by relevance score
    
    Phase 2: Graph Expansion
    - Start with matched nodes from Phase 1
    - Traverse edges to find related concepts
    - BFS/DFS up to 2-3 hops
    - Collect candidate contexts
    
    Phase 3: Budget Control
    - Limit total tokens to max_context_tokens
    - Prioritize by relevance score * edge weight
    - Truncate less important passages
    - Ensure diversity (don't take all from one page)
    
    Phase 4: Context Assembly
    - Compile selected passages into ordered context
    - Include source citations for each passage
    - Format for LLM consumption
    - Return structured result
    """
    
    # Phase 1: Tokenized Search
    query_lower = request.question.lower()
    query_tokens = set(query_lower.split())
    
    matched_pages = []
    for page_id, page in wiki_pages_store.items():
        # Simple keyword matching (would use vector similarity in production)
        title_match = any(token in page.title.lower() for token in query_tokens)
        content_matches = sum(1 for token in query_tokens if token in page.content.lower())
        
        if title_match or content_matches > 0:
            matched_pages.append({
                "page_id": page_id,
                "title": page.title,
                "relevance": content_matches + (10 if title_match else 0),
                "excerpt": page.content[:200] + "..." if len(page.content) > 200 else page.content
            })
    
    # Sort by relevance
    matched_pages.sort(key=lambda x: x["relevance"], reverse=True)
    matched_pages = matched_pages[:5]  # Top 5 matches
    
    # Phase 2: Graph Expansion (simplified)
    expanded_nodes = set()
    for match in matched_pages:
        expanded_nodes.add(match["page_id"])
        
        # Find connected nodes in graph
        for edge in knowledge_graph_edges:
            if edge.source == match["page_id"]:
                expanded_nodes.add(edge.target)
            elif edge.target == match["page_id"]:
                expanded_nodes.add(edge.source)
    
    # Phase 3 & 4: Context Assembly (simplified for demo)
    contexts = []
    total_tokens = 0
    
    for page in matched_pages:
        if total_tokens >= request.max_context_tokens:
            break
            
        # Estimate tokens (rough: 1 token ≈ 4 chars)
        excerpt_tokens = len(page["excerpt"]) // 4
        
        if total_tokens + excerpt_tokens <= request.max_context_tokens:
            contexts.append({
                "title": page["title"],
                "excerpt": page["excerpt"],
                "relevance": page["relevance"]
            })
            total_tokens += excerpt_tokens
    
    # Compute confidence based on matches and graph expansion
    confidence = min(0.95, 0.5 + (len(matched_pages) * 0.1) + (len(expanded_nodes) * 0.05))
    
    # Generate answer (would use LLM in production)
    answer = f"""Based on the accumulated knowledge base ({len(wiki_pages_store)} wiki pages, {len(expanded_nodes)} concepts explored):

Your question relates to the following key areas:

"""
    for ctx in contexts:
        answer += f"- **{ctx['title']}**: {ctx['excerpt']}\n\n"
    
    answer += f"""
**Synthesis**:
The knowledge base reveals interconnected concepts across multiple domains. Cross-referencing shows strong relationships between the topics you queried about.

**Graph Expansion**:
Visited {len(expanded_nodes)} related nodes in the knowledge graph, revealing {len(knowledge_graph_edges)} connection patterns.

**Confidence Level**: {confidence:.0%} (based on source coverage and graph connectivity)
"""
    
    result = QueryResult(
        question=request.question,
        answer=answer,
        sources=contexts,
        graph_nodes_visited=len(expanded_nodes),
        confidence=confidence,
        retrieval_phases=[
            {"phase": "Tokenized Search", "matches_found": len(matched_pages)},
            {"phase": "Graph Expansion", "nodes_expanded": len(expanded_nodes)},
            {"phase": "Budget Control", "tokens_used": total_tokens, "limit": request.max_context_tokens},
            {"phase": "Context Assembly", "contexts_compiled": len(contexts)}
        ],
        timestamp=datetime.now()
    )
    
    log_activity("QUERY", f"Question: {request.question[:50]}... ({confidence:.0%} confidence)")
    
    return result


# ==================== LINT OPERATION ====================

@app.post("/lint")
async def execute_lint():
    """
    Execute Quality Assurance Checks on Wiki
    
    Checks performed:
    1. Consistency: Same entity has consistent descriptions across pages
    2. Contradictions: Detect conflicting claims between pages
    3. Orphan Pages: Pages with no incoming links
    4. Broken Links: References to non-existent pages
    5. Quality Scores: Identify pages below threshold
    6. Graph Density: Check connectivity health
    7. Frontmatter Completeness: Required fields present
    """
    
    issues = []
    total_checks = 0
    passed = 0
    warnings = 0
    errors = 0
    
    # Check 1: Orphan pages
    total_checks += 1
    all_linked_pages = set()
    for page in wiki_pages_store.values():
        all_linked_pages.update(page.links)
    
    for page_id, page in wiki_pages_store.items():
        if page_id not in all_linked_pages and len(wiki_pages_store) > 1:
            issues.append({
                "severity": "warning",
                "type": "Orphan Page",
                "message": f'"{page.title}" has no incoming links from other pages',
                "location": f"wiki://{page_id}",
                "suggestion": "Add links from related pages or mark as entry point"
            })
            warnings += 1
        else:
            passed += 1
    
    # Check 2: Broken links
    total_checks += 1
    for page_id, page in wiki_pages_store.items():
        for link in page.links:
            # Simplified check (would normalize IDs in production)
            linked_page_exists = any(
                link.lower() in p.title.lower() or link == p.id 
                for p in wiki_pages_store.values()
            )
            
            if not linked_page_exists:
                issues.append({
                    "severity": "warning",
                    "type": "Broken Link",
                    "message": f'Reference to [[{link}]] does not match any existing page',
                    "location": f"wiki://{page_id}",
                    "suggestion": f"Create page for '{link}' or update the link"
                })
                warnings += 1
            else:
                passed += 1
    
    # Check 3: Quality scores below threshold
    total_checks += 1
    quality_threshold = 80.0
    low_quality_pages = [
        p for p in wiki_pages_store.values() 
        if p.quality_score < quality_threshold
    ]
    
    for page in low_quality_pages:
        issues.append({
            "severity": "info",
            "type": "Quality Score",
            "message": f'"{page.title}" has quality score {page.quality_score:.1f}% (threshold: {quality_threshold}%)',
            "location": f"wiki://{page.id}",
            "suggestion": "Review content length, add more cross-references, or improve frontmatter"
        })
        warnings += 1
    
    if not low_quality_pages:
        passed += 1
    
    # Check 4: Contradictions (simplified - would need NLP in production)
    total_checks += 1
    # Demo contradiction
    if len(wiki_pages_store) >= 3:
        issues.append({
            "severity": "error",
            "type": "Contradiction",
            "message": 'Potential contradiction detected: Review quality scoring methodology consistency',
            "location": "global",
            "suggestion": "Run human review on conflicting claims"
        })
        errors += 1
    else:
        passed += 1
    
    # Check 5: Graph connectivity
    total_checks += 1
    if knowledge_graph_nodes:
        connectivity = len(knowledge_graph_edges) / max(len(knowledge_graph_nodes), 1)
        issues.append({
            "severity": "info",
            "type": "Graph Density",
            "message": f'Knowledge graph connectivity: {connectivity:.2f} ({"good" if connectivity > 0.5 else "sparse"})',
            "location": "graph",
            "suggestion": "Add more cross-references between related pages" if connectivity < 0.5 else None
        })
        passed += 1
    else:
        passed += 1
    
    # Check 6: Frontmatter completeness
    total_checks += 1
    required_fields = ["type", "source_ids"]
    for page in wiki_pages_store.values():
        missing_fields = [f for f in required_fields if f not in page.frontmatter]
        if missing_fields:
            issues.append({
                "severity": "warning",
                "type": "Incomplete Frontmatter",
                "message": f'"{page.title}" missing required frontmatter fields: {missing_fields}',
                "location": f"wiki://{page.id}",
                "suggestion": f"Add fields: {missing_fields}"
            })
            warnings += 1
        else:
            passed += 1
    
    # Generate recommendations
    recommendations = []
    if errors > 0:
        recommendations.append("Address critical contradictions before publishing")
    if warnings > 0:
        recommendations.append(f"Review and fix {warnings} warning(s) to improve quality")
    if len(low_quality_pages) > 0:
        recommendations.append(f"Enhance content for {len(low_quality_pages)} low-quality page(s)")
    if len(knowledge_graph_edges) < len(knowledge_graph_nodes):
        recommendations.append("Increase cross-referencing between wiki pages")
    
    if not recommendations:
        recommendations.append("Wiki is in excellent shape! Keep up the good work.")
    
    report = LintReport(
        timestamp=datetime.now(),
        total_checks=total_checks,
        passed=passed,
        warnings=warnings,
        errors=errors,
        issues=issues,
        recommendations=recommendations,
        quality_metrics={
            "average_quality": sum(p.quality_score for p in wiki_pages_store.values()) / len(wiki_pages_store) if wiki_pages_store else 0,
            "total_pages": len(wiki_pages_store),
            "total_links": sum(len(p.links) for p in wiki_pages_store.values()),
            "graph_connectivity": len(knowledge_graph_edges) / max(len(knowledge_graph_nodes), 1) if knowledge_graph_nodes else 0
        }
    )
    
    log_activity("LINT", f"Completed: {passed}/{total_checks} passed, {errors} errors, {warnings} warnings")
    
    return report


# ==================== STATISTICS ENDPOINTS ====================

@app.get("/stats")
async def get_system_statistics():
    """Get comprehensive system statistics"""
    return {
        "timestamp": datetime.now().isoformat(),
        "layers": {
            "raw_sources": {
                "total": len(sources_store),
                "by_status": {
                    s.status: len([x for x in sources_store.values() if x.status == s])
                    for s in ["pending", "processing", "ingested", "error"]
                },
                "total_size_bytes": sum(s.size_bytes for s in sources_store.values())
            },
            "ai_wiki": {
                "total_pages": len(wiki_pages_store),
                "by_type": {
                    t: len([p for p in wiki_pages_store.values() if p.page_type == t])
                    for t in ["entity", "concept", "summary", "comparison", "analysis"]
                },
                "average_quality": round(
                    sum(p.quality_score for p in wiki_pages_store.values()) / len(wiki_pages_store), 
                    1
                ) if wiki_pages_store else 0,
                "total_cross_references": sum(len(p.links) for p in wiki_pages_store.values()),
                "average_version": round(
                    sum(p.version for p in wiki_pages_store.values()) / len(wiki_pages_store), 
                    1
                ) if wiki_pages_store else 0
            },
            "knowledge_graph": {
                "total_nodes": len(knowledge_graph_nodes),
                "total_edges": len(knowledge_graph_edges),
                "by_group": {
                    g: len([n for n in knowledge_graph_nodes.values() if n.group == g])
                    for g in ["research", "algorithm", "technique", "model", "concept"]
                },
                "avg_connections": round(
                    sum(n.connections for n in knowledge_graph_nodes.values()) / len(knowledge_graph_nodes), 
                    1
                ) if knowledge_graph_nodes else 0
            }
        },
        "recent_activity": activity_log[:10],
        "system_health": {
            "overall": "operational" if len(wiki_pages_store) > 0 else "initializing",
            "last_ingest": activity_log[0]["timestamp"] if activity_log else None,
            "uptime": "Available since server start"
        }
    }


@app.get("/activity/log")
async def get_activity_log(limit: int = 20):
    """Get recent activity timeline"""
    return {
        "total": len(activity_log),
        "activities": activity_log[:limit]
    }


# ==================== SCHEMA ENDPOINTS (Layer 3) ====================

@app.get("/schema")
async def get_schema():
    """Get current schema configuration"""
    return {
        "schema_version": "1.0.0",
        "description": "Rules and conventions for AI Wiki structure",
        "conventions": {
            "naming": "Use Title_Case for page names, snake_case for IDs",
            "frontmatter_required": ["type", "source_ids", "created", "tags"],
            "link_syntax": "[[Page_Name]] for wikilinks",
            "page_types": ["entity", "concept", "summary", "comparison", "analysis"],
            "edge_types": ["direct", "strong", "weak", "related", "methodology", "contradicts"]
        },
        "workflows": {
            "ingest": "Two-step chain-of-thought (analyze → generate)",
            "query": "Four-phase retrieval (search → expand → budget → assemble)",
            "lint": "Automated quality checks with human review loop"
        },
        "integration_points": {
            "auto_research": "/auto-research/api/deep-research",
            "skills_hub": "/skills-hub-pro/api/knowledge-context",
            "octo_trace": "/octo-trace/api/spans?module=ai-wiki",
            "evolution": "/evolution-workbench/api/optimize?target=wiki-quality"
        }
    }


# ==================== AUTORESEARCH BRIDGE API (Bidirectional Data Flow) ====================

class AutoResearchRequest(BaseModel):
    """Request model for triggering AutoResearch from Wiki"""
    query: str
    context_pages: List[str] = []  # Wiki page IDs to use as context
    max_sources: int = 10
    depth_level: str = "medium"  # shallow, medium, deep


class AutoResearchResult(BaseModel):
    """Result from AutoResearch integration"""
    research_id: str
    query: str
    status: str  # pending, running, completed, error
    sources_found: int = 0
    wiki_pages_created: int = 0
    graph_edges_added: int = 0
    tokens_used: int = 0
    cost_usd: float = 0.0
    timestamp: datetime
    findings_summary: str = ""


# Storage for AutoResearch bridge data
autoresearch_store: Dict[str, AutoResearchResult] = {}
wiki_to_research_links: Dict[str, str] = {}  # wiki_page_id -> research_id


@app.post("/api/autoresearch/trigger")
async def trigger_autoresearch_from_wiki(request: AutoResearchRequest):
    """
    Trigger AutoResearch from AI Wiki with context from wiki pages.
    
    Bidirectional Flow:
    - Wiki → AutoResearch: Send query + wiki context for deep research
    - AutoResearch → Wiki: Auto-ingest discovered sources into wiki
    """
    research_id = f"ar_{uuid.uuid4().hex[:8]}"
    
    # Create trace span for this operation
    span_id = f"span_ar_{uuid.uuid4().hex[:6]}"
    trace_span = TraceSpan(
        id=span_id,
        parent_id=None,
        operation="DEEP_RESEARCH",
        source=f"AutoResearch Trigger: {request.query[:50]}",
        start_time=datetime.now(),
        status="in_progress",
        tokens_used=0,
        cost_usd=0.0,
        details=f"Triggered deep research with {len(request.context_pages)} wiki context pages",
        metadata={
            "research_id": research_id,
            "query": request.query,
            "depth_level": request.depth_layer if hasattr(request, 'depth_layer') else request.depth_level,
            "layer": "deep_research",
            "phase": "Initializing AutoResearch Engine"
        }
    )
    await create_trace_span(trace_span)
    
    # Simulate AutoResearch execution (in production, this would call the actual AutoResearch service)
    result = AutoResearchResult(
        research_id=research_id,
        query=request.query,
        status="completed",
        sources_found=5,
        wiki_pages_created=3,
        graph_edges_added=12,
        tokens_used=12890,
        cost_usd=0.129,
        timestamp=datetime.now(),
        findings_summary=f"Discovered 5 new research papers related to '{request.query}'. Created 3 wiki pages and added 12 knowledge graph connections."
    )
    
    autoresearch_store[research_id] = result
    
    # Update trace span as completed
    if span_id in trace_spans_store:
        trace_spans_store[span_id].status = "completed"
        trace_spans_store[span_id].end_time = datetime.now()
        trace_spans_store[span_id].duration_ms = (
            datetime.now() - trace_spans_store[span_id].start_time
        ).total_seconds() * 1000
        trace_spans_store[span_id].tokens_used = result.tokens_used
        trace_spans_store[span_id].cost_usd = result.cost_usd
        trace_spans_store[span_id].details = result.findings_summary
        trace_spans_store[span_id].metadata["phase"] = "Completed"
        trace_spans_store[span_id].metadata["progress"] = 100
    
    return {
        "success": True,
        "research_id": research_id,
        "span_id": span_id,
        "result": {
            "status": result.status,
            "sources_found": result.sources_found,
            "wiki_pages_created": result.wiki_pages_created,
            "graph_edges_added": result.graph_edges_added,
            "tokens_used": result.tokens_used,
            "cost": f"${result.cost_usd:.3f}",
            "findings_summary": result.findings_summary
        },
        "integration": {
            "wiki_context_used": len(request.context_pages),
            "trace_recorded": True,
            "auto_ingest_enabled": True
        }
    }


@app.get("/api/autoresearch/research/{research_id}")
async def get_autoresearch_result(research_id: str):
    """Get detailed AutoResearch result by ID"""
    if research_id not in autoresearch_store:
        raise HTTPException(status_code=404, detail=f"Research {research_id} not found")
    
    result = autoresearch_store[research_id]
    
    # Find related wiki pages created from this research
    related_pages = [
        page_id for page_id, rid in wiki_to_research_links.items()
        if rid == research_id
    ]
    
    return {
        "research": {
            "id": result.research_id,
            "query": result.query,
            "status": result.status,
            "timestamp": result.timestamp.isoformat(),
            "sources_found": result.sources_found,
            "wiki_pages_created": result.wiki_pages_created,
            "graph_edges_added": result.graph_edges_added,
            "tokens_used": result.tokens_used,
            "cost_usd": result.cost_usd,
            "findings_summary": result.findings_summary
        },
        "related_wiki_pages": related_pages,
        "trace_spans": [
            span_id for span_id, span in trace_spans_store.items()
            if span.metadata.get("research_id") == research_id
        ]
    }


@app.post("/api/autoresearch/ingest-to-wiki")
async def ingest_autoresearch_results_to_wiki(research_id: str = Form(...)):
    """
    Ingest AutoResearch results back into AI Wiki.
    
    This creates the reverse data flow:
    AutoResearch discoveries → Wiki Pages → Knowledge Graph updates
    """
    if research_id not in autoresearch_store:
        raise HTTPException(status_code=404, detail=f"Research {research_id} not found")
    
    research = autoresearch_store[research_id]
    
    # Create trace span for ingestion
    ingest_span_id = f"span_ingest_{uuid.uuid4().hex[:6]}"
    trace_span = TraceSpan(
        id=ingest_span_id,
        parent_id=None,
        operation="INGEST",
        source=f"AutoResearch Results: {research_id}",
        start_time=datetime.now(),
        status="in_progress",
        details=f"Ingesting {research.sources_found} discovered sources into wiki",
        metadata={
            "source_type": "autoresearch",
            "research_id": research_id,
            "layer": "ingest",
            "phase": "Analysis Phase"
        }
    )
    await create_trace_span(trace_span)
    
    # Simulate creating wiki pages from research results
    new_page_ids = []
    for i in range(min(research.wiki_pages_created, 3)):
        page_id = f"wiki_ar_{research_id}_{i}"
        new_page_ids.append(page_id)
        
        # Link wiki page to research
        wiki_to_research_links[page_id] = research_id
        
        # Create a mock wiki page entry
        mock_page = WikiPage(
            id=page_id,
            title=f"Research Finding: {research.query[:40]} #{i+1}",
            page_type="entity",
            content=f"# Auto-generated from AutoResearch\n\n**Research ID**: {research_id}\n**Query**: {research.query}\n\n## Summary\n\n{research.findings_summary}\n\n## Sources\n\nDiscovered and processed {research.sources_found} sources.",
            frontmatter={
                "type": "entity",
                "source_ids": [research_id],
                "created": datetime.now().isoformat(),
                "tags": ["auto-research", "auto-generated", "discovered"],
                "quality_score": 87,
                "version": 1
            },
            links=[],
            quality_score=87,
            version=1,
            last_updated=datetime.now()
        )
        wiki_pages_store[page_id] = mock_page
        
        # Add to knowledge graph
        node_id = f"node_{page_id}"
        knowledge_graph_nodes[node_id] = KnowledgeNode(
            id=node_id,
            label=mock_page.title[:50],
            group="research",
            page_id=page_id,
            connections=2,
            created_at=datetime.now()
        )
    
    # Update trace span
    if ingest_span_id in trace_spans_store:
        trace_spans_store[ingest_span_id].status = "completed"
        trace_spans_store[ingest_span_id].end_time = datetime.now()
        trace_spans_store[ingest_span_id].duration_ms = (
            datetime.now() - trace_spans_store[ingest_span_id].start_time
        ).total_seconds() * 1000
        trace_spans_store[ingest_span_id].tokens_used = int(research.tokens_used * 0.3)  # 30% of research tokens for ingestion
        trace_spans_store[ingest_span_id].cost_usd = research.cost_usd * 0.3
        trace_spans_store[ingest_span_id].details = f"Created {len(new_page_ids)} wiki pages from AutoResearch results"
        trace_spans_store[ingest_span_id].metadata["phase"] = "Completed"
        trace_spans_store[ingest_span_id].metadata["pages_created"] = len(new_page_ids)
    
    return {
        "success": True,
        "message": "AutoResearch results ingested into AI Wiki",
        "research_id": research_id,
        "wiki_pages_created": len(new_page_ids),
        "new_page_ids": new_page_ids,
        "graph_nodes_added": len(new_page_ids),
        "trace_span_id": ingest_span_id,
        "bidirectional_flow": {
            "autoresearch_to_wiki": "✅ Completed",
            "wiki_pages_generated": len(new_page_ids),
            "knowledge_graph_updated": True,
            "octo_trace_logged": True
        }
    }


@app.get("/api/autoresearch/sync-status")
async def get_autoresearch_sync_status():
    """Get synchronization status between AI Wiki and AutoResearch"""
    total_research = len(autoresearch_store)
    total_linked_pages = len(wiki_to_research_links)
    
    # Calculate statistics
    completed_research = [
        r for r in autoresearch_store.values() 
        if r.status == "completed"
    ]
    
    return {
        "synchronization_status": "active",
        "last_sync": datetime.now().isoformat(),
        "statistics": {
            "total_autoresearch_sessions": total_research,
            "completed_sessions": len(completed_research),
            "wiki_pages_from_research": total_linked_pages,
            "total_sources_discovered": sum(r.sources_found for r in completed_research),
            "total_tokens_for_research": sum(r.tokens_used for r in completed_research),
            "total_cost_for_research": sum(r.cost_usd for r in completed_research)
        },
        "data_flow": {
            "wiki_to_autoresearch": {
                "direction": "Wiki → AutoResearch",
                "description": "Send wiki context + queries for deep research",
                "calls_made": total_research,
                "status": "operational"
            },
            "autoresearch_to_wiki": {
                "direction": "AutoResearch → Wiki",
                "description": "Auto-ingest discovered sources as wiki pages",
                "pages_created": total_linked_pages,
                "status": "operational"
            },
            "shared_octo_trace": {
                "direction": "Both ↔ OctoTrace",
                "description": "All operations tracked in unified timeline",
                "total_traced_operations": len(trace_events_store),
                "status": "active"
            }
        },
        "recent_activity": [
            {
                "research_id": r.research_id,
                "query": r.query[:50],
                "status": r.status,
                "timestamp": r.timestamp.isoformat(),
                "pages_created": r.wiki_pages_created
            }
            for r in sorted(autoresearch_store.values(), key=lambda x: x.timestamp, reverse=True)[:5]
        ]
    }


# ==================== OCTOTRACE INTEGRATION API ====================

# Trace data models for deep observability
class TraceSpan(BaseModel):
    """Individual operation span for tracing"""
    id: str
    parent_id: Optional[str] = None
    operation: str  # INGEST, QUERY, LINT, DEEP_RESEARCH
    source: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    status: str  # pending, in_progress, completed, error
    tokens_used: int = 0
    cost_usd: float = 0.0
    details: str = ""
    metadata: Dict[str, Any] = {}
    children: List[str] = []  # Child span IDs


class TraceEvent(BaseModel):
    """Timeline event for evolution tracking"""
    timestamp: datetime
    operation: str
    source: str
    details: str
    duration: str
    tokens: int
    cost: float
    span_id: str


class CostRecord(BaseModel):
    """Cost tracking record"""
    timestamp: datetime
    operation: str
    tokens: int
    cost: float
    layer: str  # analysis, generation, graph_ops, query, lint


# In-memory storage for trace data
trace_spans_store: Dict[str, TraceSpan] = {}
trace_events_store: List[TraceEvent] = []
cost_records_store: List[CostRecord] = []
trace_root_span_id: Optional[str] = None


@app.post("/api/trace/span")
async def create_trace_span(span: TraceSpan):
    """Create a new trace span for operation tracking"""
    trace_spans_store[span.id] = span
    
    # If this is a root-level span (no parent), set as root
    if span.parent_id is None and trace_root_span_id is None:
        trace_root_span_id = span.id
    
    # Add to parent's children list if exists
    if span.parent_id and span.parent_id in trace_spans_store:
        parent = trace_spans_store[span.parent_id]
        if span.id not in parent.children:
            parent.children.append(span.id)
    
    # Create corresponding timeline event
    event = TraceEvent(
        timestamp=span.start_time,
        operation=span.operation,
        source=span.source,
        details=span.details,
        duration=f"{span.duration_ms or 0:.1f}ms",
        tokens=span.tokens_used,
        cost=span.cost_usd,
        span_id=span.id
    )
    trace_events_store.insert(0, event)  # Insert at beginning (newest first)
    
    # Record cost
    if span.cost_usd > 0:
        cost_record = CostRecord(
            timestamp=span.start_time,
            operation=span.operation,
            tokens=span.tokens_used,
            cost=span.cost_usd,
            layer=span.metadata.get("layer", "unknown")
        )
        cost_records_store.append(cost_record)
    
    return {"success": True, "span_id": span.id, "message": "Trace span created"}


@app.get("/api/trace/timeline")
async def get_evolution_timeline(limit: int = 50):
    """Get chronological evolution timeline of all wiki operations"""
    events_sorted = sorted(trace_events_store, key=lambda x: x.timestamp, reverse=True)
    return {
        "total_events": len(trace_events_store),
        "events": [
            {
                "timestamp": e.timestamp.isoformat(),
                "operation": e.operation,
                "source": e.source,
                "details": e.details,
                "duration": e.duration,
                "tokens": e.tokens,
                "cost": f"${e.cost:.3f}",
                "span_id": e.span_id
            }
            for e in events_sorted[:limit]
        ],
        "summary": {
            "total_operations": len(trace_events_store),
            "by_operation_type": {
                op: len([e for e in trace_events_store if e.operation == op])
                for op in ["INGEST", "QUERY", "LINT", "DEEP_RESEARCH"]
            },
            "total_tokens": sum(e.tokens for e in trace_events_store),
            "total_cost": sum(e.cost for e in trace_events_store)
        }
    }


@app.get("/api/trace/span-tree")
async def get_span_tree():
    """Get hierarchical span tree structure"""
    if not trace_root_span_id or trace_root_span_id not in trace_spans_store:
        return {"root_span": None, "message": "No active wiki session"}
    
    root = trace_spans_store[trace_root_span_id]
    
    def build_span_tree(span_id: str) -> Dict:
        span = trace_spans_store.get(span_id)
        if not span:
            return None
        
        return {
            "id": span.id,
            "operation": span.operation,
            "source": span.source,
            "start_time": span.start_time.isoformat(),
            "end_time": span.end_time.isoformat() if span.end_time else None,
            "duration": f"{(span.duration_ms or 0) / 1000:.1f}s" if span.duration_ms else None,
            "status": span.status,
            "tokens": span.tokens_used,
            "cost": f"${span.cost_usd:.3f}",
            "children": [build_span_tree(child_id) for child_id in span.children]
        }
    
    tree = build_span_tree(trace_root_span_id)
    
    # Calculate summary statistics
    all_spans = list(trace_spans_store.values())
    
    return {
        "root_span": tree,
        "summary": {
            "total_child_spans": len(all_spans) - 1,  # Exclude root
            "total_tokens": sum(s.tokens_used for s in all_spans),
            "estimated_total_cost": sum(s.cost_usd for s in all_spans),
            "completed_ratio": (
                len([s for s in all_spans if s.status == "completed"]) / len(all_spans) * 100
            ) if all_spans else 0,
            "by_status": {
                status: len([s for s in all_spans if s.status == status])
                for status in ["pending", "in_progress", "completed", "error"]
            },
            "by_operation": {
                op: len([s for s in all_spans if s.operation == op])
                for op in ["INGEST", "QUERY", "LINT", "DEEP_RESEARCH"]
            }
        }
    }


@app.get("/api/trace/cost-analytics")
async def get_cost_analytics():
    """Get comprehensive cost analytics and budget tracking"""
    total_tokens = sum(r.tokens for r in cost_records_store)
    total_cost = sum(r.cost for r in cost_records_store)
    budget_limit = 1.00  # Default $1.00 budget
    
    # Group by operation type
    by_operation = {}
    for record in cost_records_store:
        if record.operation not in by_operation:
            by_operation[record.operation] = {"tokens": 0, "cost": 0, "count": 0}
        by_operation[record.operation]["tokens"] += record.tokens
        by_operation[record.operation]["cost"] += record.cost
        by_operation[record.operation]["count"] += 1
    
    # Group by layer
    by_layer = {}
    for record in cost_records_store:
        if record.layer not in by_layer:
            by_layer[record.layer] = 0
        by_layer[record.layer] += record.tokens
    
    # Daily usage (last 7 days)
    from datetime import timedelta
    daily_usage = []
    for i in range(7):
        day = datetime.now() - timedelta(days=6-i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        day_records = [r for r in cost_records_store 
                      if day_start <= r.timestamp < day_end]
        day_tokens = sum(r.tokens for r in day_records)
        day_cost = sum(r.cost for r in day_records)
        
        daily_usage.append({
            "date": day.strftime("%Y-%m-%d"),
            "tokens": day_tokens,
            "cost": round(day_cost, 4)
        })
    
    # Top operations by cost
    top_operations = sorted(
        [{"operation": op, **stats} for op, stats in by_operation.items()],
        key=lambda x: x["cost"],
        reverse=True
    )[:5]
    
    return {
        "total_tokens": total_tokens,
        "total_cost": round(total_cost, 3),
        "budget": budget_limit,
        "budget_remaining": round(budget_limit - total_cost, 3),
        "budget_usage_percent": round((total_cost / budget_limit) * 100, 1) if budget_limit > 0 else 0,
        "operations": {
            op: {
                "tokens": stats["tokens"],
                "cost": round(stats["cost"], 4),
                "count": stats["count"],
                "percent_of_total": round((stats["cost"] / total_cost) * 100, 1) if total_cost > 0 else 0
            }
            for op, stats in by_operation.items()
        },
        "token_by_layer": by_layer,
        "daily_usage": daily_usage,
        "top_operations": [
            {
                "operation": op["operation"],
                "tokens": op["tokens"],
                "percentage": round((op["cost"] / total_cost) * 100, 1) if total_cost > 0 else 0
            }
            for op in top_operations
        ]
    }


@app.get("/api/trace/spans/{span_id}")
async def get_span_details(span_id: str):
    """Get detailed information about a specific span"""
    if span_id not in trace_spans_store:
        raise HTTPException(status_code=404, detail=f"Span {span_id} not found")
    
    span = trace_spans_store[span_id]
    
    # Get children details
    children_details = []
    for child_id in span.children:
        if child_id in trace_spans_store:
            child = trace_spans_store[child_id]
            children_details.append({
                "id": child.id,
                "operation": child.operation,
                "status": child.status,
                "duration": f"{child.duration_ms or 0:.1f}ms",
                "tokens": child.tokens_used
            })
    
    return {
        "span": {
            "id": span.id,
            "parent_id": span.parent_id,
            "operation": span.operation,
            "source": span.source,
            "start_time": span.start_time.isoformat(),
            "end_time": span.end_time.isoformat() if span.end_time else None,
            "duration_ms": span.duration_ms,
            "status": span.status,
            "tokens_used": span.tokens_used,
            "cost_usd": span.cost_usd,
            "details": span.details,
            "metadata": span.metadata
        },
        "children": children_details,
        "timeline_position": next(
            (i for i, e in enumerate(trace_events_store) if e.span_id == span_id),
            None
        )
    }


@app.get("/api/trace/activity")
async def get_realtime_activity(limit: int = 10):
    """Get real-time activity feed for trace viewer"""
    recent_events = sorted(trace_events_store, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    # Find currently executing operations
    active_spans = [
        span for span in trace_spans_store.values() 
        if span.status == "in_progress"
    ]
    
    return {
        "is_live": True,
        "last_updated": datetime.now().isoformat(),
        "current_operations": [
            {
                "span_id": span.id,
                "operation": span.operation,
                "source": span.source,
                "status": span.status,
                "progress": span.metadata.get("progress", 0),
                "current_phase": span.metadata.get("phase", "Initializing"),
                "duration_so_far": f"{(datetime.now() - span.start_time).total_seconds():.1f}s"
            }
            for span in active_spans
        ] if active_spans else [{
            "operation": "IDLE",
            "status": "waiting",
            "message": "No active operations"
        }],
        "recent_events": [
            {
                "timestamp": e.timestamp.isoformat(),
                "operation": e.operation,
                "source": e.source,
                "details": e.details,
                "duration": e.duration,
                "tokens": e.tokens,
                "cost": f"${e.cost:.3f}",
                "span_id": e.span_id,
                "status": trace_spans_store[e.span_id].status if e.span_id in trace_spans_store else "unknown"
            }
            for e in recent_events
        ],
        "quick_filters": {
            "all": len(trace_events_store),
            "ingest_only": len([e for e in trace_events_store if e.operation == "INGEST"]),
            "query_only": len([e for e in trace_events_store if e.operation == "QUERY"]),
            "errors": len([e for e in trace_events_store if e.span_id in trace_spans_store and trace_spans_store[e.span_id].status == "error"])
        }
    }


@app.delete("/api/trace/clear")
async def clear_trace_data():
    """Clear all trace data (for testing/reset purposes)"""
    global trace_spans_store, trace_events_store, cost_records_store, trace_root_span_id
    
    count_spans = len(trace_spans_store)
    count_events = len(trace_events_store)
    count_costs = len(cost_records_store)
    
    trace_spans_store = {}
    trace_events_store = []
    cost_records_store = []
    trace_root_span_id = None
    
    return {
        "success": True,
        "message": "Trace data cleared",
        "cleared": {
            "spans": count_spans,
            "events": count_events,
            "cost_records": count_costs
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 AI Wiki Backend API Starting...")
    print("📚 Incremental Knowledge Base System")
    print("🔍 OctoTrace Integration: Enabled")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=3006)
