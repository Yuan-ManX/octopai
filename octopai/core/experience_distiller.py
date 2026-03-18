"""
Experience Distiller - Octopai's Experience-Based Skill Extraction System

This module provides Octopai's proprietary experience distillation system that
transforms successful trajectories into strategic patterns and failed ones into
concise lessons. Features include intelligent pattern recognition,
trajectory analysis, and automated skill generation.
"""

import os
import json
import hashlib
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path


class TrajectoryType(Enum):
    """Types of trajectories for distillation"""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


@dataclass
class TrajectoryStep:
    """A single step in a trajectory"""
    step_id: str
    action: str
    observation: str
    reasoning: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "action": self.action,
            "observation": self.observation,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrajectoryStep':
        return cls(**data)


@dataclass
class Trajectory:
    """A complete trajectory of an agent's experience"""
    trajectory_id: str
    trajectory_type: TrajectoryType
    task_description: str
    steps: List[TrajectoryStep] = field(default_factory=list)
    outcome: str = ""
    task_category: Optional[str] = None
    duration_seconds: Optional[float] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "trajectory_id": self.trajectory_id,
            "trajectory_type": self.trajectory_type.value,
            "task_description": self.task_description,
            "steps": [s.to_dict() for s in self.steps],
            "outcome": self.outcome,
            "task_category": self.task_category,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Trajectory':
        data = data.copy()
        data['trajectory_type'] = TrajectoryType(data['trajectory_type'])
        data['steps'] = [TrajectoryStep.from_dict(s) for s in data.get('steps', [])]
        return cls(**data)


@dataclass
class ExtractedPattern:
    """A pattern extracted from trajectories"""
    pattern_id: str
    pattern_type: str
    description: str
    supporting_trajectories: List[str] = field(default_factory=list)
    confidence: float = 0.0
    when_to_apply: str = ""
    examples: List[str] = field(default_factory=list)
    category: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type,
            "description": self.description,
            "supporting_trajectories": self.supporting_trajectories,
            "confidence": self.confidence,
            "when_to_apply": self.when_to_apply,
            "examples": self.examples,
            "category": self.category,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExtractedPattern':
        return cls(**data)


@dataclass
class FailureLesson:
    """A lesson learned from failed trajectories"""
    lesson_id: str
    mistake_description: str
    root_cause: str = ""
    prevention_strategy: str = ""
    recovery_strategy: str = ""
    supporting_trajectories: List[str] = field(default_factory=list)
    occurrence_count: int = 0
    category: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "lesson_id": self.lesson_id,
            "mistake_description": self.mistake_description,
            "root_cause": self.root_cause,
            "prevention_strategy": self.prevention_strategy,
            "recovery_strategy": self.recovery_strategy,
            "supporting_trajectories": self.supporting_trajectories,
            "occurrence_count": self.occurrence_count,
            "category": self.category,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FailureLesson':
        return cls(**data)


class ExperienceDistiller:
    """
    Experience-Based Skill Distillation System
    
    Features:
    - Transform successful trajectories into strategic patterns
    - Extract concise lessons from failed trajectories
    - Intelligent pattern recognition across multiple trajectories
    - Automated skill generation from distilled experience
    - Trajectory storage and management
    - Pattern confidence scoring
    """
    
    def __init__(self, storage_dir: str = "./ExperienceDistiller"):
        self.storage_dir = Path(storage_dir)
        self.trajectories_dir = self.storage_dir / "trajectories"
        self.patterns_file = self.storage_dir / "patterns.json"
        self.lessons_file = self.storage_dir / "lessons.json"
        
        self.trajectories: Dict[str, Trajectory] = {}
        self.patterns: Dict[str, ExtractedPattern] = {}
        self.lessons: Dict[str, FailureLesson] = {}
        
        self._initialize_storage()
        self._load_data()
    
    def _initialize_storage(self):
        """Initialize storage directories"""
        self.trajectories_dir.mkdir(parents=True, exist_ok=True)
        if not self.patterns_file.exists():
            self._save_patterns()
        if not self.lessons_file.exists():
            self._save_lessons()
    
    def _load_data(self):
        """Load all data from disk"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.patterns = {
                        p['pattern_id']: ExtractedPattern.from_dict(p)
                        for p in data
                    }
            except Exception as e:
                print(f"Error loading patterns: {e}")
        
        if self.lessons_file.exists():
            try:
                with open(self.lessons_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.lessons = {
                        l['lesson_id']: FailureLesson.from_dict(l)
                        for l in data
                    }
            except Exception as e:
                print(f"Error loading lessons: {e}")
        
        for trajectory_file in self.trajectories_dir.glob("*.json"):
            try:
                with open(trajectory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    trajectory = Trajectory.from_dict(data)
                    self.trajectories[trajectory.trajectory_id] = trajectory
            except Exception as e:
                print(f"Error loading trajectory {trajectory_file}: {e}")
    
    def _save_patterns(self):
        """Save patterns to disk"""
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.patterns.values()], f, indent=2)
    
    def _save_lessons(self):
        """Save lessons to disk"""
        with open(self.lessons_file, 'w', encoding='utf-8') as f:
            json.dump([l.to_dict() for l in self.lessons.values()], f, indent=2)
    
    def _save_trajectory(self, trajectory: Trajectory):
        """Save a single trajectory to disk"""
        filepath = self.trajectories_dir / f"{trajectory.trajectory_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(trajectory.to_dict(), f, indent=2)
    
    def _generate_id(self, prefix: str, content: str) -> str:
        """Generate a unique ID"""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}_{content_hash}"
    
    def add_trajectory(
        self,
        task_description: str,
        steps: List[Dict[str, str]],
        trajectory_type: TrajectoryType = TrajectoryType.SUCCESS,
        outcome: str = "",
        task_category: Optional[str] = None,
        duration_seconds: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Trajectory:
        """
        Add a new trajectory for distillation
        
        Args:
            task_description: Description of the task
            steps: List of step dicts with action, observation, reasoning
            trajectory_type: Type of trajectory (success, failure, partial)
            outcome: Outcome description
            task_category: Optional task category
            duration_seconds: Optional duration in seconds
            metadata: Optional metadata
            
        Returns:
            Created Trajectory
        """
        trajectory_id = self._generate_id("traj", task_description)
        
        trajectory_steps = []
        for i, step_dict in enumerate(steps):
            step = TrajectoryStep(
                step_id=f"{trajectory_id}_step_{i}",
                action=step_dict.get('action', ''),
                observation=step_dict.get('observation', ''),
                reasoning=step_dict.get('reasoning'),
                metadata=step_dict.get('metadata', {})
            )
            trajectory_steps.append(step)
        
        trajectory = Trajectory(
            trajectory_id=trajectory_id,
            trajectory_type=trajectory_type,
            task_description=task_description,
            steps=trajectory_steps,
            outcome=outcome,
            task_category=task_category,
            duration_seconds=duration_seconds,
            metadata=metadata or {}
        )
        
        self.trajectories[trajectory_id] = trajectory
        self._save_trajectory(trajectory)
        return trajectory
    
    def distill_success_patterns(
        self,
        task_category: Optional[str] = None,
        min_support: int = 2
    ) -> List[ExtractedPattern]:
        """
        Distill strategic patterns from successful trajectories
        
        Args:
            task_category: Optional category filter
            min_support: Minimum number of supporting trajectories
            
        Returns:
            List of extracted patterns
        """
        success_trajectories = [
            t for t in self.trajectories.values()
            if t.trajectory_type == TrajectoryType.SUCCESS
        ]
        
        if task_category:
            success_trajectories = [
                t for t in success_trajectories
                if t.task_category == task_category
            ]
        
        new_patterns = []
        
        if len(success_trajectories) < min_support:
            return new_patterns
        
        action_patterns = self._extract_action_patterns(success_trajectories)
        step_sequence_patterns = self._extract_step_sequence_patterns(success_trajectories)
        
        for pattern_data in action_patterns + step_sequence_patterns:
            if len(pattern_data['supporting_trajectories']) >= min_support:
                pattern_id = self._generate_id("pattern", pattern_data['description'])
                pattern = ExtractedPattern(
                    pattern_id=pattern_id,
                    pattern_type=pattern_data['pattern_type'],
                    description=pattern_data['description'],
                    supporting_trajectories=pattern_data['supporting_trajectories'],
                    confidence=len(pattern_data['supporting_trajectories']) / len(success_trajectories),
                    when_to_apply=pattern_data.get('when_to_apply', ''),
                    examples=pattern_data.get('examples', []),
                    category=task_category
                )
                self.patterns[pattern_id] = pattern
                new_patterns.append(pattern)
        
        self._save_patterns()
        return new_patterns
    
    def _extract_action_patterns(
        self,
        trajectories: List[Trajectory]
    ) -> List[Dict[str, Any]]:
        """Extract patterns based on common actions"""
        from collections import defaultdict
        
        action_groups = defaultdict(list)
        
        for trajectory in trajectories:
            actions = [step.action for step in trajectory.steps]
            action_key = '|'.join(sorted(set(actions)))
            if len(actions) >= 2:
                action_groups[action_key].append(trajectory.trajectory_id)
        
        patterns = []
        for action_key, traj_ids in action_groups.items():
            if len(traj_ids) >= 2:
                patterns.append({
                    'pattern_type': 'action_pattern',
                    'description': f"Use actions: {action_key.replace('|', ', ')}",
                    'supporting_trajectories': traj_ids,
                    'when_to_apply': 'When facing similar task contexts'
                })
        
        return patterns
    
    def _extract_step_sequence_patterns(
        self,
        trajectories: List[Trajectory]
    ) -> List[Dict[str, Any]]:
        """Extract patterns based on step sequences"""
        patterns = []
        
        if len(trajectories) < 2:
            return patterns
        
        for i, traj1 in enumerate(trajectories):
            for traj2 in trajectories[i+1:]:
                common_prefix = self._find_common_prefix(traj1.steps, traj2.steps)
                if len(common_prefix) >= 2:
                    patterns.append({
                        'pattern_type': 'sequence_pattern',
                        'description': f"Follow step sequence: {', '.join(common_prefix)}",
                        'supporting_trajectories': [traj1.trajectory_id, traj2.trajectory_id],
                        'when_to_apply': 'When executing similar task flows'
                    })
        
        return patterns
    
    def _find_common_prefix(
        self,
        steps1: List[TrajectoryStep],
        steps2: List[TrajectoryStep]
    ) -> List[str]:
        """Find common action prefix between two step sequences"""
        prefix = []
        min_len = min(len(steps1), len(steps2))
        for i in range(min_len):
            if steps1[i].action == steps2[i].action:
                prefix.append(steps1[i].action)
            else:
                break
        return prefix
    
    def distill_failure_lessons(
        self,
        task_category: Optional[str] = None,
        min_occurrences: int = 1
    ) -> List[FailureLesson]:
        """
        Extract concise lessons from failed trajectories
        
        Args:
            task_category: Optional category filter
            min_occurrences: Minimum occurrences for a lesson
            
        Returns:
            List of failure lessons
        """
        failure_trajectories = [
            t for t in self.trajectories.values()
            if t.trajectory_type == TrajectoryType.FAILURE
        ]
        
        if task_category:
            failure_trajectories = [
                t for t in failure_trajectories
                if t.task_category == task_category
            ]
        
        new_lessons = []
        
        for trajectory in failure_trajectories:
            lesson = self._analyze_failure_trajectory(trajectory)
            if lesson:
                existing = self._find_similar_lesson(lesson)
                if existing:
                    existing.occurrence_count += 1
                    existing.supporting_trajectories.append(trajectory.trajectory_id)
                else:
                    lesson.occurrence_count = 1
                    lesson.supporting_trajectories = [trajectory.trajectory_id]
                    self.lessons[lesson.lesson_id] = lesson
                    new_lessons.append(lesson)
        
        self._save_lessons()
        return [l for l in new_lessons if l.occurrence_count >= min_occurrences]
    
    def _analyze_failure_trajectory(self, trajectory: Trajectory) -> Optional[FailureLesson]:
        """Analyze a single failure trajectory to extract lessons"""
        if not trajectory.steps:
            return None
        
        last_step = trajectory.steps[-1]
        
        lesson_id = self._generate_id("lesson", last_step.action)
        
        return FailureLesson(
            lesson_id=lesson_id,
            mistake_description=f"Failure when executing: {last_step.action}",
            root_cause=f"Observation after action: {last_step.observation}",
            prevention_strategy="Review the action sequence and adjust approach",
            recovery_strategy="Consider alternative actions or backtrack",
            category=trajectory.task_category
        )
    
    def _find_similar_lesson(self, lesson: FailureLesson) -> Optional[FailureLesson]:
        """Find an existing similar lesson"""
        for existing in self.lessons.values():
            if existing.mistake_description == lesson.mistake_description:
                return existing
        return None
    
    def get_patterns(
        self,
        category: Optional[str] = None,
        pattern_type: Optional[str] = None,
        min_confidence: float = 0.0,
        top_k: Optional[int] = None
    ) -> List[ExtractedPattern]:
        """
        Get extracted patterns with filters
        
        Args:
            category: Optional category filter
            pattern_type: Optional pattern type filter
            min_confidence: Minimum confidence threshold
            top_k: Maximum number of patterns to return
            
        Returns:
            List of ExtractedPattern objects
        """
        patterns = list(self.patterns.values())
        
        if category:
            patterns = [p for p in patterns if p.category == category]
        
        if pattern_type:
            patterns = [p for p in patterns if p.pattern_type == pattern_type]
        
        patterns = [p for p in patterns if p.confidence >= min_confidence]
        patterns.sort(key=lambda x: x.confidence, reverse=True)
        
        if top_k:
            patterns = patterns[:top_k]
        
        return patterns
    
    def get_lessons(
        self,
        category: Optional[str] = None,
        min_occurrences: int = 0,
        top_k: Optional[int] = None
    ) -> List[FailureLesson]:
        """
        Get failure lessons with filters
        
        Args:
            category: Optional category filter
            min_occurrences: Minimum occurrence threshold
            top_k: Maximum number of lessons to return
            
        Returns:
            List of FailureLesson objects
        """
        lessons = list(self.lessons.values())
        
        if category:
            lessons = [l for l in lessons if l.category == category]
        
        lessons = [l for l in lessons if l.occurrence_count >= min_occurrences]
        lessons.sort(key=lambda x: x.occurrence_count, reverse=True)
        
        if top_k:
            lessons = lessons[:top_k]
        
        return lessons
    
    def get_distillation_context(
        self,
        category: Optional[str] = None,
        pattern_top_k: int = 5,
        lesson_top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Get complete distillation context for skill bank integration
        
        Args:
            category: Optional category filter
            pattern_top_k: Number of patterns to include
            lesson_top_k: Number of lessons to include
            
        Returns:
            Dictionary with patterns and lessons
        """
        return {
            'success_patterns': self.get_patterns(category=category, top_k=pattern_top_k),
            'failure_lessons': self.get_lessons(category=category, top_k=lesson_top_k)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get distillation statistics"""
        total_trajectories = len(self.trajectories)
        success_count = sum(
            1 for t in self.trajectories.values()
            if t.trajectory_type == TrajectoryType.SUCCESS
        )
        failure_count = sum(
            1 for t in self.trajectories.values()
            if t.trajectory_type == TrajectoryType.FAILURE
        )
        
        categories = set(t.task_category for t in self.trajectories.values() if t.task_category)
        
        return {
            'total_trajectories': total_trajectories,
            'success_count': success_count,
            'failure_count': failure_count,
            'partial_count': total_trajectories - success_count - failure_count,
            'total_patterns': len(self.patterns),
            'total_lessons': len(self.lessons),
            'categories': list(categories)
        }
