"""
Program Registry Manager

Manages the storage, retrieval, and organization of programs,
with built-in frontier management and version control capabilities.
"""
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import json
import time
import shutil
from datetime import datetime

from .models import (
    ProgramEntry,
    ProgramConfig,
    ProgramStatus,
    Skill,
    SkillMetadata,
    Experiment
)
from octopai.evolution import (
    SelectionStrategy,
    FrontierManager
)


class ProgramRegistry:
    """
    Manages a registry of programs with frontier management.
    
    Provides:
    - Storage and retrieval of programs
    - Frontier management (top-N programs)
    - Selection strategies for choosing parents
    - Git integration (optional)
    - Cost tracking
    """

    def __init__(
        self,
        storage_path: Path,
        frontier_size: int = 3
    ):
        self.storage_path = Path(storage_path)
        self.programs_path = self.storage_path / "programs"
        self.frontier_path = self.storage_path / "frontier"
        self.feedback_path = self.storage_path / "feedback"
        self.experiments_path = self.storage_path / "experiments"
        self.skills_path = self.storage_path / "skills"
        
        # Initialize directories
        for path in [
            self.programs_path,
            self.frontier_path,
            self.feedback_path,
            self.experiments_path,
            self.skills_path
        ]:
            path.mkdir(parents=True, exist_ok=True)
        
        # In-memory cache
        self._programs: Dict[str, ProgramEntry] = {}
        self._frontier: List[str] = []
        self._skills: Dict[str, Skill] = {}
        
        # Load existing state
        self._load_state()
        
        # Frontier manager
        self._frontier_manager = FrontierManager[ProgramConfig](
            max_size=frontier_size
        )

    def _load_state(self):
        """Load existing state from disk."""
        # Load programs
        for program_file in self.programs_path.glob("*.json"):
            try:
                data = json.loads(program_file.read_text())
                entry = ProgramEntry.from_dict(data)
                self._programs[entry.config.name] = entry
            except Exception:
                pass
        
        # Load frontier
        if (self.frontier_path / "frontier.json").exists():
            try:
                data = json.loads((self.frontier_path / "frontier.json").read_text())
                self._frontier = data.get("frontier", [])
            except Exception:
                pass
        
        # Load skills
        for skill_file in self.skills_path.glob("*.json"):
            try:
                data = json.loads(skill_file.read_text())
                skill = Skill.from_dict(data)
                self._skills[skill.id] = skill
            except Exception:
                pass

    def _save_state(self):
        """Save current state to disk."""
        # Save programs
        for name, entry in self._programs.items():
            (self.programs_path / f"{name}.json").write_text(
                json.dumps(entry.to_dict(), indent=2)
            )
        
        # Save frontier
        (self.frontier_path / "frontier.json").write_text(
            json.dumps({"frontier": self._frontier}, indent=2)
        )
        
        # Save skills
        for skill_id, skill in self._skills.items():
            (self.skills_path / f"{skill_id}.json").write_text(
                json.dumps(skill.to_dict(), indent=2)
            )

    def create_program(
        self,
        name: str,
        config: ProgramConfig,
        score: float = 0.0,
        parent: Optional[str] = None
    ) -> ProgramEntry:
        """Create and store a new program."""
        entry = ProgramEntry(
            config=config,
            score=score,
            status=ProgramStatus.ACTIVE,
            created_at=time.time()
        )
        
        self._programs[name] = entry
        self._save_state()
        
        return entry

    def get_program(self, name: str) -> Optional[ProgramEntry]:
        """Get a program by name."""
        return self._programs.get(name)

    def get_current(self) -> Optional[ProgramEntry]:
        """Get the current best program."""
        if not self._frontier:
            return None
        return self._programs.get(self._frontier[0])

    def list_programs(self) -> List[str]:
        """List all program names."""
        return list(self._programs.keys())

    def update_frontier(
        self,
        name: str,
        score: float,
        max_size: Optional[int] = None
    ) -> bool:
        """
        Update the frontier with a new program.
        
        Returns True if the program was added to the frontier.
        """
        if name not in self._programs:
            return False
        
        # Update program score
        self._programs[name].score = score
        
        # Update frontier manager
        entry = self._programs[name]
        added = self._frontier_manager.add(
            name=name,
            content=entry.config,
            score=score,
            generation=entry.config.generation,
            parent_name=entry.config.parent_name
        )
        
        # Update frontier list
        self._frontier = self._frontier_manager.get_names()
        self._save_state()
        
        return added

    def get_frontier(self) -> List[str]:
        """Get the current frontier program names."""
        return self._frontier

    def get_frontier_with_scores(self) -> List[Tuple[str, float]]:
        """Get frontier programs with their scores."""
        return [
            (name, self._programs[name].score)
            for name in self._frontier
        ]

    def get_best_from_frontier(self) -> Optional[str]:
        """Get the name of the best program in the frontier."""
        return self._frontier[0] if self._frontier else None

    def select_from_frontier(
        self,
        strategy: SelectionStrategy,
        iteration: int = 0
    ) -> Optional[str]:
        """Select a parent program from the frontier."""
        frontier_entry = self._frontier_manager.select(strategy, iteration)
        return frontier_entry.name if frontier_entry else None

    def switch_to(self, name: str):
        """Switch to a specific program (move to top of frontier)."""
        if name in self._programs and name in self._frontier:
            self._frontier.remove(name)
            self._frontier.insert(0, name)
            self._save_state()

    def discard(self, name: str):
        """Discard a program (remove from frontier but keep in history)."""
        if name in self._frontier:
            self._frontier.remove(name)
        if name in self._programs:
            self._programs[name].status = ProgramStatus.ARCHIVED
        self._save_state()

    def delete_program(self, name: str):
        """Permanently delete a program."""
        if name in self._programs:
            del self._programs[name]
        if name in self._frontier:
            self._frontier.remove(name)
        self._save_state()
        
        # Delete file
        (self.programs_path / f"{name}.json").unlink(missing_ok=True)

    def add_evaluation_result(
        self,
        name: str,
        result: Dict[str, Any]
    ):
        """Add an evaluation result to a program."""
        if name in self._programs:
            self._programs[name].evaluation_results.append(result)
            self._programs[name].last_evaluated = time.time()
            self._save_state()

    def save_feedback(
        self,
        name: str,
        proposal: str,
        rationale: str,
        outcome: str,
        score: float,
        parent_score: float
    ):
        """Save feedback for a mutation attempt."""
        feedback_file = self.feedback_path / f"{name}_feedback.json"
        
        feedback = {
            "name": name,
            "proposal": proposal,
            "rationale": rationale,
            "outcome": outcome,
            "score": score,
            "parent_score": parent_score,
            "timestamp": time.time()
        }
        
        existing = []
        if feedback_file.exists():
            try:
                existing = json.loads(feedback_file.read_text())
            except Exception:
                pass
        
        existing.append(feedback)
        feedback_file.write_text(json.dumps(existing, indent=2))

    def read_feedback_history(self, name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Read feedback history for a program or all programs."""
        all_feedback = []
        
        if name:
            feedback_file = self.feedback_path / f"{name}_feedback.json"
            if feedback_file.exists():
                try:
                    all_feedback = json.loads(feedback_file.read_text())
                except Exception:
                    pass
        else:
            for feedback_file in self.feedback_path.glob("*.json"):
                try:
                    all_feedback.extend(json.loads(feedback_file.read_text()))
                except Exception:
                    pass
        
        return all_feedback

    # Skills management
    def add_skill(self, skill: Skill) -> str:
        """Add a skill to the registry."""
        self._skills[skill.id] = skill
        self._save_state()
        return skill.id

    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get a skill by ID."""
        return self._skills.get(skill_id)

    def get_skill_by_name(self, name: str) -> Optional[Skill]:
        """Get a skill by name."""
        for skill in self._skills.values():
            if skill.metadata.name == name:
                return skill
        return None

    def list_skills(self) -> List[Skill]:
        """List all skills."""
        return list(self._skills.values())

    def update_skill(self, skill_id: str, updates: Dict[str, Any]):
        """Update a skill."""
        if skill_id in self._skills:
            skill = self._skills[skill_id]
            
            # Update metadata
            for key, value in updates.get("metadata", {}).items():
                setattr(skill.metadata, key, value)
            
            if "content" in updates:
                skill.content = updates["content"]
            
            skill.metadata.updated_at = time.time()
            self._save_state()

    def delete_skill(self, skill_id: str):
        """Delete a skill."""
        if skill_id in self._skills:
            del self._skills[skill_id]
            self._save_state()
            (self.skills_path / f"{skill_id}.json").unlink(missing_ok=True)

    # Experiments management
    def create_experiment(
        self,
        name: str,
        description: str,
        task_config: Dict[str, Any],
        dataset_config: Dict[str, Any],
        evolution_config: Dict[str, Any]
    ) -> Experiment:
        """Create a new experiment."""
        experiment_id = f"exp_{int(time.time())}"
        experiment = Experiment(
            id=experiment_id,
            name=name,
            description=description,
            task_config=task_config,
            dataset_config=dataset_config,
            evolution_config=evolution_config
        )
        
        self._save_experiment(experiment)
        return experiment

    def _save_experiment(self, experiment: Experiment):
        """Save an experiment to disk."""
        (self.experiments_path / f"{experiment.id}.json").write_text(
            json.dumps(experiment.to_dict(), indent=2)
        )

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """Get an experiment by ID."""
        experiment_file = self.experiments_path / f"{experiment_id}.json"
        if not experiment_file.exists():
            return None
        
        try:
            data = json.loads(experiment_file.read_text())
            return Experiment.from_dict(data)
        except Exception:
            return None

    def list_experiments(self) -> List[Experiment]:
        """List all experiments."""
        experiments = []
        for exp_file in self.experiments_path.glob("*.json"):
            try:
                data = json.loads(exp_file.read_text())
                experiments.append(Experiment.from_dict(data))
            except Exception:
                pass
        
        # Sort by created_at descending
        experiments.sort(key=lambda x: x.created_at, reverse=True)
        return experiments

    def update_experiment_status(
        self,
        experiment_id: str,
        status: str,
        results: Optional[Dict[str, Any]] = None,
        log_entry: Optional[str] = None
    ):
        """Update an experiment's status."""
        experiment = self.get_experiment(experiment_id)
        if not experiment:
            return
        
        experiment.status = status
        
        if results:
            experiment.results = results
        
        if log_entry:
            timestamp = datetime.now().isoformat()
            experiment.logs.append(f"[{timestamp}] {log_entry}")
        
        if status == "running" and not experiment.started_at:
            experiment.started_at = time.time()
        
        if status in ["completed", "failed", "stopped"]:
            experiment.completed_at = time.time()
        
        self._save_experiment(experiment)

    def reset(self):
        """Reset the registry (clear all programs but keep skills)."""
        # Keep skills, clear everything else
        skills = dict(self._skills)
        
        # Clear programs
        self._programs.clear()
        self._frontier.clear()
        
        # Delete program files
        for program_file in self.programs_path.glob("*.json"):
            program_file.unlink()
        
        # Clear feedback
        for feedback_file in self.feedback_path.glob("*.json"):
            feedback_file.unlink()
        
        # Reset frontier file
        (self.frontier_path / "frontier.json").write_text(json.dumps({"frontier": []}))
        
        # Restore skills
        self._skills = skills
        self._save_state()

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the registry."""
        return {
            "total_programs": len(self._programs),
            "active_programs": sum(1 for p in self._programs.values() if p.status == ProgramStatus.ACTIVE),
            "frontier_size": len(self._frontier),
            "total_skills": len(self._skills),
            "total_experiments": len(list(self.experiments_path.glob("*.json"))),
            "best_score": self._programs[self._frontier[0]].score if self._frontier else 0,
            "last_updated": time.time()
        }
