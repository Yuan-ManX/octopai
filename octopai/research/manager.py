"""
AutoResearch Manager
Core management logic for autonomous research system
"""

import os
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple

from .models import (
    ResearchProject, ResearchIdea, Experiment, Paper,
    LiteratureSearch, ResearchStatus, ExperimentStatus, Visibility
)


class AutoResearchManager:
    """Manager class for autonomous research operations"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # Use project directory for storage
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_dir = os.path.join(base_dir, "web", "backend", "data", "research")
        self.data_dir = data_dir
        self.registry_file = os.path.join(data_dir, "research_registry.json")
        
        self._projects: Dict[str, ResearchProject] = {}
        self._user_stars: Dict[str, set] = {}
        
        self._ensure_data_dir()
        self._load_registry()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _load_registry(self):
        """Load research projects from file"""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r') as f:
                    data = json.load(f)
                    
                for proj_data in data.get('projects', []):
                    project = self._dict_to_project(proj_data)
                    self._projects[project.project_id] = project
                
                for user_id, starred in data.get('user_stars', {}).items():
                    self._user_stars[user_id] = set(starred)
            except Exception as e:
                print(f"Error loading registry: {e}")
    
    def _save_registry(self):
        """Save research projects to file"""
        data = {
            'projects': [proj.to_dict() for proj in self._projects.values()],
            'user_stars': {uid: list(stars) for uid, stars in self._user_stars.items()},
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.registry_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _dict_to_project(self, data: Dict) -> ResearchProject:
        """Convert dictionary to ResearchProject object"""
        ideas = [
            ResearchIdea(
                idea_id=idea['idea_id'],
                title=idea['title'],
                description=idea['description'],
                domain=idea['domain'],
                keywords=idea.get('keywords', []),
                novelty_score=idea.get('novelty_score', 0.0),
                feasibility_score=idea.get('feasibility_score', 0.0),
                impact_score=idea.get('impact_score', 0.0),
                related_papers=idea.get('related_papers', []),
                status=idea.get('status', 'proposed'),
                created_at=datetime.fromisoformat(idea['created_at']) if idea.get('created_at') else datetime.now()
            )
            for idea in data.get('ideas', [])
        ]
        
        experiments = [
            Experiment(
                experiment_id=exp['experiment_id'],
                research_project_id=exp['research_project_id'],
                name=exp['name'],
                description=exp['description'],
                status=ExperimentStatus(exp.get('status', 'pending')),
                config=exp.get('config', {}),
                code=exp.get('code'),
                parameters=exp.get('parameters', {}),
                results=exp.get('results', {}),
                metrics=exp.get('metrics', {}),
                artifacts=exp.get('artifacts', []),
                started_at=datetime.fromisoformat(exp['started_at']) if exp.get('started_at') else None,
                completed_at=datetime.fromisoformat(exp['completed_at']) if exp.get('completed_at') else None,
                duration_seconds=exp.get('duration_seconds', 0),
                error_message=exp.get('error_message'),
                created_at=datetime.fromisoformat(exp['created_at']) if exp.get('created_at') else datetime.now(),
                updated_at=datetime.fromisoformat(exp['updated_at']) if exp.get('updated_at') else datetime.now()
            )
            for exp in data.get('experiments', [])
        ]
        
        literature = [
            Paper(
                paper_id=paper['paper_id'],
                title=paper['title'],
                authors=paper.get('authors', []),
                abstract=paper.get('abstract'),
                year=paper.get('year'),
                venue=paper.get('venue'),
                doi=paper.get('doi'),
                url=paper.get('url'),
                citation_count=paper.get('citation_count', 0),
                relevance_score=paper.get('relevance_score', 0.0),
                key_findings=paper.get('key_findings', []),
                methodology=paper.get('methodology')
            )
            for paper in data.get('literature', [])
        ]
        
        return ResearchProject(
            project_id=data['project_id'],
            name=data['name'],
            slug=data['slug'],
            description=data['description'],
            visibility=Visibility(data.get('visibility', 'private')),
            status=ResearchStatus(data.get('status', 'ideation')),
            owner_type=data.get('owner_type', 'user'),
            owner_id=data.get('owner_id', ''),
            namespace=data.get('namespace', ''),
            collaborators=data.get('collaborators', []),
            topic=data.get('topic'),
            domain=data.get('domain', ''),
            subdomain=data.get('subdomain', ''),
            keywords=data.get('keywords', []),
            ideas=ideas,
            experiments=experiments,
            literature=literature,
            findings=data.get('findings', []),
            conclusions=data.get('conclusions'),
            draft_paper=data.get('draft_paper'),
            total_experiments=data.get('total_experiments', 0),
            successful_experiments=data.get('successful_experiments', 0),
            failed_experiments=data.get('failed_experiments', 0),
            total_runtime_hours=data.get('total_runtime_hours', 0.0),
            star_count=data.get('star_count', 0),
            fork_count=data.get('fork_count', 0),
            view_count=data.get('view_count', 0),
            created_by=data.get('created_by', ''),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else datetime.now()
        )
    
    # Project Management
    
    def create_project(self, name: str, description: str, namespace: str = "demo",
                      visibility: str = "private", domain: str = "",
                      topic: str = None, keywords: List[str] = None,
                      owner_type: str = "user", created_by: str = "system") -> ResearchProject:
        """Create a new research project"""
        project_id = str(uuid.uuid4())
        slug = name.lower().replace(' ', '-').replace('_', '-')[:50]
        
        project = ResearchProject(
            project_id=project_id,
            name=name,
            slug=slug,
            description=description,
            visibility=Visibility(visibility),
            owner_type=owner_type,
            owner_id=f"{owner_type}_{namespace}",
            namespace=namespace,
            domain=domain,
            topic=topic,
            keywords=keywords or [],
            created_by=created_by
        )
        
        self._projects[project_id] = project
        self._save_registry()
        return project
    
    def get_project(self, project_id: str) -> Optional[ResearchProject]:
        """Get a specific research project"""
        project = self._projects.get(project_id)
        if project:
            project.view_count += 1
            self._save_registry()
        return project
    
    def update_project(self, project_id: str, **kwargs) -> Optional[ResearchProject]:
        """Update a research project"""
        project = self._projects.get(project_id)
        if not project:
            return None
        
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
        
        project.updated_at = datetime.now()
        self._save_registry()
        return project
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a research project"""
        if project_id in self._projects:
            del self._projects[project_id]
            self._save_registry()
            return True
        return False
    
    def list_projects(self, status: str = None, domain: str = None,
                     namespace: str = None, visibility: str = None,
                     page: int = 1, page_size: int = 20) -> Tuple[List[ResearchProject], int]:
        """List research projects with filtering"""
        projects = list(self._projects.values())
        
        if status:
            projects = [p for p in projects if p.status.value == status]
        if domain:
            projects = [p for p in projects if p.domain == domain]
        if namespace:
            projects = [p for p in projects if p.namespace == namespace]
        if visibility:
            projects = [p for p in projects if p.visibility.value == visibility]
        
        total = len(projects)
        start = (page - 1) * page_size
        end = start + page_size
        
        return projects[start:end], total
    
    # Idea Management
    
    def add_idea(self, project_id: str, title: str, description: str,
                domain: str, keywords: List[str] = None,
                novelty_score: float = 0.0, feasibility_score: float = 0.0,
                impact_score: float = 0.0) -> Optional[ResearchIdea]:
        """Add a new research idea to a project"""
        project = self._projects.get(project_id)
        if not project:
            return None
        
        idea = ResearchIdea(
            idea_id=str(uuid.uuid4()),
            title=title,
            description=description,
            domain=domain,
            keywords=keywords or [],
            novelty_score=novelty_score,
            feasibility_score=feasibility_score,
            impact_score=impact_score
        )
        
        project.ideas.append(idea)
        project.updated_at = datetime.now()
        self._save_registry()
        return idea
    
    def update_idea_status(self, project_id: str, idea_id: str, status: str) -> bool:
        """Update the status of a research idea"""
        project = self._projects.get(project_id)
        if not project:
            return False
        
        for idea in project.ideas:
            if idea.idea_id == idea_id:
                idea.status = status
                project.updated_at = datetime.now()
                self._save_registry()
                return True
        return False
    
    # Experiment Management
    
    def create_experiment(self, project_id: str, name: str, description: str,
                        code: str = None, parameters: Dict[str, Any] = None,
                        config: Dict[str, Any] = None) -> Optional[Experiment]:
        """Create a new experiment"""
        project = self._projects.get(project_id)
        if not project:
            return None
        
        experiment = Experiment(
            experiment_id=str(uuid.uuid4()),
            research_project_id=project_id,
            name=name,
            description=description,
            code=code,
            parameters=parameters or {},
            config=config or {}
        )
        
        project.experiments.append(experiment)
        project.total_experiments += 1
        project.status = ResearchStatus.EXPERIMENTING
        project.updated_at = datetime.now()
        self._save_registry()
        return experiment
    
    def run_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """Run an experiment (simulate execution)"""
        for project in self._projects.values():
            for exp in project.experiments:
                if exp.experiment_id == experiment_id:
                    exp.status = ExperimentStatus.RUNNING
                    exp.started_at = datetime.now()
                    self._save_registry()
                    
                    # Simulate experiment completion
                    import time
                    time.sleep(1)
                    
                    exp.status = ExperimentStatus.COMPLETED
                    exp.completed_at = datetime.now()
                    exp.duration_seconds = int((exp.completed_at - exp.started_at).total_seconds())
                    
                    # Generate simulated results
                    exp.results = {
                        "output": "Experiment completed successfully",
                        "data_points": 100,
                        "accuracy": round(0.85 + (hash(experiment_id) % 20) / 100, 3),
                        "loss": round(0.15 + (hash(experiment_id) % 10) / 100, 3)
                    }
                    exp.metrics = {
                        "accuracy": exp.results["accuracy"],
                        "loss": exp.results["loss"],
                        "f1_score": round(0.82 + (hash(experiment_id) % 15) / 100, 3)
                    }
                    
                    project.successful_experiments += 1
                    project.total_runtime_hours += exp.duration_seconds / 3600
                    project.updated_at = datetime.now()
                    self._save_registry()
                    
                    return exp
        return None
    
    def cancel_experiment(self, experiment_id: str) -> bool:
        """Cancel a running experiment"""
        for project in self._projects.values():
            for exp in project.experiments:
                if exp.experiment_id == experiment_id and exp.status == ExperimentStatus.RUNNING:
                    exp.status = ExperimentStatus.CANCELLED
                    exp.completed_at = datetime.now()
                    exp.duration_seconds = int((exp.completed_at - exp.started_at).total_seconds())
                    project.failed_experiments += 1
                    project.updated_at = datetime.now()
                    self._save_registry()
                    return True
        return False
    
    # Literature Management
    
    def search_literature(self, query: str, source: str = "semantic_scholar",
                         max_results: int = 10) -> LiteratureSearch:
        """Search for academic literature (simulated)"""
        search_id = str(uuid.uuid4())
        
        # Simulate search results
        results = []
        for i in range(min(max_results, 5)):
            paper = Paper(
                paper_id=str(uuid.uuid4()),
                title=f"Research Paper {i+1}: {query[:30]}...",
                authors=[f"Author {j}" for j in range(3)],
                abstract=f"This paper discusses important findings related to {query}. It presents novel methodology and comprehensive experiments.",
                year=2023 + (i % 3),
                venue="Conference on AI Research",
                doi=f"10.1234/paper.{search_id[-8:]}.{i+1}",
                citation_count=50 + i * 10,
                relevance_score=round(0.9 - i * 0.1, 2),
                key_findings=[
                    f"Finding {j+1} related to {query}"
                    for j in range(3)
                ]
            )
            results.append(paper.to_dict())
        
        search = LiteratureSearch(
            search_id=search_id,
            query=query,
            source=source,
            results=results,
            total_found=len(results)
        )
        
        return search
    
    def add_paper_to_project(self, project_id: str, paper_data: Dict) -> bool:
        """Add a paper to a project's literature collection"""
        project = self._projects.get(project_id)
        if not project:
            return False
        
        paper = Paper(
            paper_id=paper_data.get('paper_id', str(uuid.uuid4())),
            title=paper_data['title'],
            authors=paper_data.get('authors', []),
            abstract=paper_data.get('abstract'),
            year=paper_data.get('year'),
            venue=paper_data.get('venue'),
            doi=paper_data.get('doi'),
            url=paper_data.get('url'),
            citation_count=paper_data.get('citation_count', 0),
            relevance_score=paper_data.get('relevance_score', 0.0),
            key_findings=paper_data.get('key_findings', [])
        )
        
        project.literature.append(paper)
        project.updated_at = datetime.now()
        self._save_registry()
        return True
    
    # Social Features
    
    def star_project(self, project_id: str, user_id: str) -> bool:
        """Star/unstar a research project"""
        project = self._projects.get(project_id)
        if not project:
            return False
        
        if user_id not in self._user_stars:
            self._user_stars[user_id] = set()
        
        if project_id in self._user_stars[user_id]:
            self._user_stars[user_id].remove(project_id)
            project.star_count -= 1
        else:
            self._user_stars[user_id].add(project_id)
            project.star_count += 1
        
        self._save_registry()
        return True
    
    def is_starred(self, project_id: str, user_id: str) -> bool:
        """Check if a project is starred by a user"""
        return project_id in self._user_stars.get(user_id, set())
    
    def fork_project(self, project_id: str, new_namespace: str, 
                    new_name: str) -> Optional[ResearchProject]:
        """Fork a research project"""
        original = self._projects.get(project_id)
        if not original:
            return None
        
        new_project = ResearchProject(
            project_id=str(uuid.uuid4()),
            name=new_name,
            slug=new_name.lower().replace(' ', '-').replace('_', '-'),
            description=f"Forked from {original.name}",
            visibility=original.visibility,
            owner_type="user",
            owner_id=f"user_{new_namespace}",
            namespace=new_namespace,
            domain=original.domain,
            subdomain=original.subdomain,
            keywords=original.keywords.copy(),
            topic=original.topic,
            created_by=new_namespace
        )
        
        original.fork_count += 1
        self._projects[new_project.project_id] = new_project
        self._save_registry()
        return new_project
    
    # Statistics and Analytics
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get platform-wide statistics"""
        total_projects = len(self._projects)
        public_projects = sum(1 for p in self._projects.values() if p.visibility == Visibility.PUBLIC)
        
        total_experiments = sum(p.total_experiments for p in self._projects.values())
        successful_experiments = sum(p.successful_experiments for p in self._projects.values())
        
        domains = {}
        for p in self._projects.values():
            if p.domain:
                domains[p.domain] = domains.get(p.domain, 0) + 1
        
        statuses = {}
        for p in self._projects.values():
            s = p.status.value
            statuses[s] = statuses.get(s, 0) + 1
        
        return {
            "total_projects": total_projects,
            "public_projects": public_projects,
            "private_projects": total_projects - public_projects,
            "total_experiments": total_experiments,
            "successful_experiments": successful_experiments,
            "success_rate": round(successful_experiments / max(1, total_experiments), 2),
            "domains": domains,
            "statuses": statuses
        }
