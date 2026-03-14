"""
Experience Tracker - EXO's Intelligent Interaction Learning System

This module provides EXO's proprietary experience tracking system that
records, analyzes, and learns from skill interactions to continuously
improve the skill ecosystem.
"""

import os
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum


class InteractionType(Enum):
    """Types of skill interactions"""
    EXECUTION = "execution"
    OPTIMIZATION = "optimization"
    CREATION = "creation"
    VALIDATION = "validation"
    REVIEW = "review"


class InteractionOutcome(Enum):
    """Outcomes of interactions"""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    PENDING = "pending"


@dataclass
class InteractionRecord:
    """Record of a single skill interaction"""
    interaction_id: str
    skill_id: str
    skill_version: int
    interaction_type: InteractionType
    outcome: InteractionOutcome
    started_at: str
    completed_at: Optional[str] = None
    duration_seconds: Optional[float] = None
    user_feedback: Optional[str] = None
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    error_messages: List[str] = field(default_factory=list)
    custom_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "interaction_id": self.interaction_id,
            "skill_id": self.skill_id,
            "skill_version": self.skill_version,
            "interaction_type": self.interaction_type.value,
            "outcome": self.outcome.value,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_seconds": self.duration_seconds,
            "user_feedback": self.user_feedback,
            "performance_metrics": self.performance_metrics,
            "error_messages": self.error_messages,
            "custom_data": self.custom_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InteractionRecord':
        data = data.copy()
        if 'interaction_type' in data:
            data['interaction_type'] = InteractionType(data['interaction_type'])
        if 'outcome' in data:
            data['outcome'] = InteractionOutcome(data['outcome'])
        return cls(**data)


@dataclass
class SkillExperience:
    """Aggregated experience for a specific skill"""
    skill_id: str
    total_interactions: int = 0
    success_rate: float = 0.0
    average_duration: Optional[float] = None
    most_recent_use: Optional[str] = None
    common_errors: List[str] = field(default_factory=list)
    top_performance_metrics: Dict[str, float] = field(default_factory=dict)
    improvement_suggestions: List[str] = field(default_factory=list)
    version_stats: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillExperience':
        return cls(**data)


class ExperienceTracker:
    """
    EXO's Experience Tracker - Intelligent Interaction Learning System
    
    Tracks, analyzes, and learns from skill interactions to provide
    insights and drive continuous improvement in EXO's skill ecosystem.
    """
    
    def __init__(self, storage_dir: str = "./experiences"):
        self.storage_dir = storage_dir
        self.records_dir = os.path.join(storage_dir, "records")
        self.analytics_dir = os.path.join(storage_dir, "analytics")
        
        os.makedirs(self.records_dir, exist_ok=True)
        os.makedirs(self.analytics_dir, exist_ok=True)
        
        self._interaction_cache: Dict[str, InteractionRecord] = {}
        self._experience_cache: Dict[str, SkillExperience] = {}
    
    def start_interaction(
        self,
        skill_id: str,
        skill_version: int,
        interaction_type: InteractionType,
        custom_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Start tracking a new interaction
        
        Args:
            skill_id: ID of the skill being used
            skill_version: Version of the skill
            interaction_type: Type of interaction
            custom_data: Optional custom data to attach
            
        Returns:
            interaction_id for reference
        """
        import uuid
        interaction_id = str(uuid.uuid4())
        
        record = InteractionRecord(
            interaction_id=interaction_id,
            skill_id=skill_id,
            skill_version=skill_version,
            interaction_type=interaction_type,
            outcome=InteractionOutcome.PENDING,
            started_at=datetime.now().isoformat(),
            custom_data=custom_data or {}
        )
        
        self._interaction_cache[interaction_id] = record
        self._save_record(record)
        
        return interaction_id
    
    def complete_interaction(
        self,
        interaction_id: str,
        outcome: InteractionOutcome,
        performance_metrics: Optional[Dict[str, float]] = None,
        error_messages: Optional[List[str]] = None,
        user_feedback: Optional[str] = None
    ) -> InteractionRecord:
        """
        Complete a tracked interaction
        
        Args:
            interaction_id: ID of the interaction to complete
            outcome: Final outcome
            performance_metrics: Optional performance metrics
            error_messages: Optional error messages
            user_feedback: Optional user feedback
            
        Returns:
            Completed interaction record
        """
        if interaction_id not in self._interaction_cache:
            record = self._load_record(interaction_id)
            if not record:
                raise ValueError(f"Interaction {interaction_id} not found")
            self._interaction_cache[interaction_id] = record
        
        record = self._interaction_cache[interaction_id]
        record.completed_at = datetime.now().isoformat()
        record.outcome = outcome
        record.performance_metrics = performance_metrics or {}
        record.error_messages = error_messages or []
        record.user_feedback = user_feedback
        
        if record.started_at and record.completed_at:
            start = datetime.fromisoformat(record.started_at)
            end = datetime.fromisoformat(record.completed_at)
            record.duration_seconds = (end - start).total_seconds()
        
        self._save_record(record)
        self._update_skill_experience(record.skill_id)
        
        return record
    
    def get_interaction(self, interaction_id: str) -> Optional[InteractionRecord]:
        """Get a specific interaction record"""
        if interaction_id in self._interaction_cache:
            return self._interaction_cache[interaction_id]
        return self._load_record(interaction_id)
    
    def get_skill_interactions(
        self,
        skill_id: str,
        limit: int = 100,
        interaction_type: Optional[InteractionType] = None
    ) -> List[InteractionRecord]:
        """
        Get interactions for a specific skill
        
        Args:
            skill_id: Skill ID to query
            limit: Maximum number of records to return
            interaction_type: Optional filter by interaction type
            
        Returns:
            List of interaction records
        """
        records = []
        skill_records_dir = os.path.join(self.records_dir, skill_id)
        
        if not os.path.exists(skill_records_dir):
            return []
        
        for filename in sorted(os.listdir(skill_records_dir), reverse=True):
            if filename.endswith('.json') and len(records) < limit:
                filepath = os.path.join(skill_records_dir, filename)
                try:
                    record = self._load_record_from_path(filepath)
                    if interaction_type is None or record.interaction_type == interaction_type:
                        records.append(record)
                except Exception:
                    continue
        
        return records[:limit]
    
    def get_skill_experience(self, skill_id: str) -> Optional[SkillExperience]:
        """
        Get aggregated experience for a skill
        
        Args:
            skill_id: Skill ID to query
            
        Returns:
            Aggregated skill experience
        """
        if skill_id in self._experience_cache:
            return self._experience_cache[skill_id]
        
        experience = self._load_skill_experience(skill_id)
        if experience:
            self._experience_cache[skill_id] = experience
        
        return experience
    
    def get_all_skill_experiences(self) -> List[SkillExperience]:
        """Get experience data for all skills"""
        experiences = []
        
        if os.path.exists(self.analytics_dir):
            for filename in os.listdir(self.analytics_dir):
                if filename.endswith('_experience.json'):
                    skill_id = filename.replace('_experience.json', '')
                    experience = self.get_skill_experience(skill_id)
                    if experience:
                        experiences.append(experience)
        
        return experiences
    
    def get_insights(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get insights from experience data
        
        Args:
            skill_id: Optional specific skill to analyze, or all skills
            
        Returns:
            Dictionary of insights
        """
        insights = {
            "generated_at": datetime.now().isoformat(),
            "scope": skill_id if skill_id else "all"
        }
        
        if skill_id:
            experience = self.get_skill_experience(skill_id)
            if experience:
                insights["skill_insights"] = self._generate_skill_insights(experience)
        else:
            all_experiences = self.get_all_skill_experiences()
            insights["ecosystem_insights"] = self._generate_ecosystem_insights(all_experiences)
        
        return insights
    
    def _save_record(self, record: InteractionRecord):
        """Save an interaction record to disk"""
        skill_dir = os.path.join(self.records_dir, record.skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        
        filename = f"{record.interaction_id}.json"
        filepath = os.path.join(skill_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(record.to_dict(), f, indent=2)
    
    def _load_record(self, interaction_id: str) -> Optional[InteractionRecord]:
        """Load an interaction record from disk"""
        for root, dirs, files in os.walk(self.records_dir):
            if f"{interaction_id}.json" in files:
                filepath = os.path.join(root, f"{interaction_id}.json")
                return self._load_record_from_path(filepath)
        return None
    
    def _load_record_from_path(self, filepath: str) -> InteractionRecord:
        """Load a record from a specific file path"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return InteractionRecord.from_dict(data)
    
    def _update_skill_experience(self, skill_id: str):
        """Update aggregated experience for a skill"""
        interactions = self.get_skill_interactions(skill_id, limit=1000)
        
        if not interactions:
            return
        
        experience = SkillExperience(skill_id=skill_id)
        experience.total_interactions = len(interactions)
        
        successful = [i for i in interactions if i.outcome == InteractionOutcome.SUCCESS]
        experience.success_rate = len(successful) / len(interactions) if interactions else 0.0
        
        durations = [i.duration_seconds for i in interactions if i.duration_seconds]
        experience.average_duration = sum(durations) / len(durations) if durations else None
        
        if interactions:
            experience.most_recent_use = max(
                i.completed_at or i.started_at 
                for i in interactions
            )
        
        all_errors = []
        for i in interactions:
            all_errors.extend(i.error_messages)
        
        error_counts = {}
        for error in all_errors:
            error_counts[error] = error_counts.get(error, 0) + 1
        
        experience.common_errors = sorted(
            error_counts.keys(),
            key=lambda e: error_counts[e],
            reverse=True
        )[:10]
        
        version_stats = {}
        for i in interactions:
            v = i.skill_version
            if v not in version_stats:
                version_stats[v] = {"count": 0, "successes": 0}
            version_stats[v]["count"] += 1
            if i.outcome == InteractionOutcome.SUCCESS:
                version_stats[v]["successes"] += 1
        
        experience.version_stats = version_stats
        
        self._experience_cache[skill_id] = experience
        self._save_skill_experience(experience)
    
    def _save_skill_experience(self, experience: SkillExperience):
        """Save aggregated skill experience to disk"""
        filename = f"{experience.skill_id}_experience.json"
        filepath = os.path.join(self.analytics_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(experience.to_dict(), f, indent=2)
    
    def _load_skill_experience(self, skill_id: str) -> Optional[SkillExperience]:
        """Load aggregated skill experience from disk"""
        filename = f"{skill_id}_experience.json"
        filepath = os.path.join(self.analytics_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return SkillExperience.from_dict(data)
    
    def _generate_skill_insights(self, experience: SkillExperience) -> Dict[str, Any]:
        """Generate insights for a specific skill"""
        insights = {}
        
        if experience.success_rate < 0.5:
            insights["concern"] = "Low success rate, consider optimization"
        elif experience.success_rate > 0.9:
            insights["strength"] = "Excellent success rate"
        
        if experience.common_errors:
            insights["top_error"] = experience.common_errors[0]
        
        if experience.version_stats:
            best_version = max(
                experience.version_stats.items(),
                key=lambda x: (x[1]["successes"] / x[1]["count"]) if x[1]["count"] > 0 else 0
            )
            insights["best_version"] = best_version[0]
        
        return insights
    
    def _generate_ecosystem_insights(self, experiences: List[SkillExperience]) -> Dict[str, Any]:
        """Generate insights across all skills"""
        if not experiences:
            return {"message": "No experience data available"}
        
        total_interactions = sum(e.total_interactions for e in experiences)
        avg_success = sum(e.success_rate for e in experiences) / len(experiences)
        
        top_skill = max(experiences, key=lambda e: e.total_interactions)
        best_skill = max(experiences, key=lambda e: e.success_rate)
        
        return {
            "total_skills": len(experiences),
            "total_interactions": total_interactions,
            "average_success_rate": avg_success,
            "most_used_skill": top_skill.skill_id,
            "most_successful_skill": best_skill.skill_id
        }
