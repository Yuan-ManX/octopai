"""
AutoResearch Data Models
Core data structures for autonomous research system
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class ResearchStatus(str, Enum):
    """Status of a research project"""
    IDEATION = "ideation"
    PLANNING = "planning"
    EXPERIMENTING = "experimenting"
    ANALYZING = "analyzing"
    WRITING = "writing"
    REVIEW = "review"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ExperimentStatus(str, Enum):
    """Status of an experiment"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Visibility(str, Enum):
    """Visibility levels for research projects"""
    PUBLIC = "public"
    PRIVATE = "private"
    COLLABORATIVE = "collaborative"


@dataclass
class ResearchIdea:
    """A research idea or hypothesis"""
    idea_id: str
    title: str
    description: str
    domain: str
    keywords: List[str] = field(default_factory=list)
    novelty_score: float = 0.0
    feasibility_score: float = 0.0
    impact_score: float = 0.0
    related_papers: List[str] = field(default_factory=list)
    status: str = "proposed"
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "idea_id": self.idea_id,
            "title": self.title,
            "description": self.description,
            "domain": self.domain,
            "keywords": self.keywords,
            "novelty_score": self.novelty_score,
            "feasibility_score": self.feasibility_score,
            "impact_score": self.impact_score,
            "related_papers": self.related_papers,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class Experiment:
    """An individual experiment run"""
    experiment_id: str
    research_project_id: str
    name: str
    description: str
    status: ExperimentStatus = ExperimentStatus.PENDING
    
    # Experiment configuration
    config: Dict[str, Any] = field(default_factory=dict)
    code: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Results
    results: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    
    # Timing and metadata
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: int = 0
    error_message: Optional[str] = None
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "research_project_id": self.research_project_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "config": self.config,
            "parameters": self.parameters,
            "results": self.results,
            "metrics": self.metrics,
            "artifacts": self.artifacts,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class LiteratureSearch:
    """Literature search result"""
    search_id: str
    query: str
    source: str  # e.g., 'semantic_scholar', 'arxiv', 'pubmed'
    results: List[Dict[str, Any]] = field(default_factory=list)
    total_found: int = 0
    searched_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "search_id": self.search_id,
            "query": self.query,
            "source": self.source,
            "results": self.results,
            "total_found": self.total_found,
            "searched_at": self.searched_at.isoformat()
        }


@dataclass
class Paper:
    """Academic paper reference"""
    paper_id: str
    title: str
    authors: List[str] = field(default_factory=list)
    abstract: Optional[str] = None
    year: Optional[int] = None
    venue: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    citation_count: int = 0
    relevance_score: float = 0.0
    key_findings: List[str] = field(default_factory=list)
    methodology: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "year": self.year,
            "venue": self.venue,
            "doi": self.doi,
            "url": self.url,
            "citation_count": self.citation_count,
            "relevance_score": self.relevance_score,
            "key_findings": self.key_findings,
            "methodology": self.methodology
        }


@dataclass
class ResearchProject:
    """Main research project container (like a GitHub repo for research)"""
    project_id: str
    name: str
    slug: str
    description: str
    visibility: Visibility = Visibility.PRIVATE
    status: ResearchStatus = ResearchStatus.IDEATION
    
    # Owner information
    owner_type: str = "user"  # "user" or "organization"
    owner_id: str = ""
    namespace: str = ""
    collaborators: List[str] = field(default_factory=list)
    
    # Research content
    topic: Optional[str] = None
    domain: str = ""
    subdomain: str = ""
    keywords: List[str] = field(default_factory=list)
    
    # Research components
    ideas: List[ResearchIdea] = field(default_factory=list)
    experiments: List[Experiment] = field(default_factory=list)
    literature: List[Paper] = field(default_factory=list)
    
    # Output
    findings: List[Dict[str, Any]] = field(default_factory=list)
    conclusions: Optional[str] = None
    draft_paper: Optional[str] = None
    
    # Statistics
    total_experiments: int = 0
    successful_experiments: int = 0
    failed_experiments: int = 0
    total_runtime_hours: float = 0.0
    
    # Metadata
    star_count: int = 0
    fork_count: int = 0
    view_count: int = 0
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "visibility": self.visibility.value,
            "status": self.status.value,
            "owner_type": self.owner_type,
            "owner_id": self.owner_id,
            "namespace": self.namespace,
            "collaborators": self.collaborators,
            "topic": self.topic,
            "domain": self.domain,
            "subdomain": self.subdomain,
            "keywords": self.keywords,
            "ideas": [idea.to_dict() for idea in self.ideas],
            "experiments": [exp.to_dict() for exp in self.experiments],
            "literature": [paper.to_dict() for paper in self.literature],
            "findings": self.findings,
            "conclusions": self.conclusions,
            "draft_paper": self.draft_paper,
            "total_experiments": self.total_experiments,
            "successful_experiments": self.successful_experiments,
            "failed_experiments": self.failed_experiments,
            "total_runtime_hours": self.total_runtime_hours,
            "star_count": self.star_count,
            "fork_count": self.fork_count,
            "view_count": self.view_count,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
