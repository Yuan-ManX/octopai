"""
Experience Tracker - Octopai's Intelligent Interaction Learning System

This module provides Octopai's proprietary experience tracking system that
records, analyzes, and learns from skill interactions to continuously
improve the skill ecosystem. Features include pattern recognition,
cross-skill knowledge transfer, and memory consolidation.
"""

import os
import json
import re
from collections import defaultdict
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
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


class PatternType(Enum):
    """Types of patterns recognized in experience data"""
    SUCCESS_PATTERN = "success_pattern"
    FAILURE_PATTERN = "failure_pattern"
    USAGE_PATTERN = "usage_pattern"
    ERROR_PATTERN = "error_pattern"
    IMPROVEMENT_PATTERN = "improvement_pattern"
    CORRELATION = "correlation"


@dataclass
class ExperiencePattern:
    """Recognized pattern in experience data"""
    pattern_id: str
    pattern_type: PatternType
    description: str
    confidence: float
    supporting_interactions: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    discovered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_observed: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type.value,
            "description": self.description,
            "confidence": self.confidence,
            "supporting_interactions": self.supporting_interactions,
            "metadata": self.metadata,
            "discovered_at": self.discovered_at,
            "last_observed": self.last_observed
        }


@dataclass
class TransferableKnowledge:
    """Knowledge that can be transferred across skills"""
    knowledge_id: str
    source_skill_id: str
    content: str
    applicability_score: float
    categories: List[str] = field(default_factory=list)
    verified: bool = False
    transfer_count: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "knowledge_id": self.knowledge_id,
            "source_skill_id": self.source_skill_id,
            "content": self.content,
            "applicability_score": self.applicability_score,
            "categories": self.categories,
            "verified": self.verified,
            "transfer_count": self.transfer_count,
            "created_at": self.created_at
        }


@dataclass
class MemoryConsolidation:
    """Consolidated memory from multiple interactions"""
    consolidation_id: str
    skill_id: str
    time_window_start: str
    time_window_end: str
    key_insights: List[str] = field(default_factory=list)
    consolidated_lessons: List[str] = field(default_factory=list)
    performance_summary: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "consolidation_id": self.consolidation_id,
            "skill_id": self.skill_id,
            "time_window_start": self.time_window_start,
            "time_window_end": self.time_window_end,
            "key_insights": self.key_insights,
            "consolidated_lessons": self.consolidated_lessons,
            "performance_summary": self.performance_summary,
            "created_at": self.created_at
        }


@dataclass
class TemporalTrend:
    """Temporal trend analysis for skill performance"""
    skill_id: str
    metric_name: str
    trend_direction: str
    trend_strength: float
    data_points: List[Dict[str, Any]] = field(default_factory=list)
    analysis_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "metric_name": self.metric_name,
            "trend_direction": self.trend_direction,
            "trend_strength": self.trend_strength,
            "data_points": self.data_points,
            "analysis_timestamp": self.analysis_timestamp
        }


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
    Octopai's Experience Tracker - Intelligent Interaction Learning System
    
    Tracks, analyzes, and learns from skill interactions to provide
    insights and drive continuous improvement in Octopai's skill ecosystem.
    Features pattern recognition, cross-skill knowledge transfer, and
    memory consolidation.
    """
    
    def __init__(self, storage_dir: str = "./experiences"):
        self.storage_dir = storage_dir
        self.records_dir = os.path.join(storage_dir, "records")
        self.analytics_dir = os.path.join(storage_dir, "analytics")
        self.patterns_dir = os.path.join(storage_dir, "patterns")
        self.knowledge_dir = os.path.join(storage_dir, "transferable_knowledge")
        self.consolidation_dir = os.path.join(storage_dir, "consolidations")
        
        os.makedirs(self.records_dir, exist_ok=True)
        os.makedirs(self.analytics_dir, exist_ok=True)
        os.makedirs(self.patterns_dir, exist_ok=True)
        os.makedirs(self.knowledge_dir, exist_ok=True)
        os.makedirs(self.consolidation_dir, exist_ok=True)
        
        self._interaction_cache: Dict[str, InteractionRecord] = {}
        self._experience_cache: Dict[str, SkillExperience] = {}
        self._patterns_cache: Dict[str, ExperiencePattern] = {}
        self._transferable_knowledge_cache: Dict[str, TransferableKnowledge] = {}
        self._consolidations_cache: Dict[str, MemoryConsolidation] = {}
        
        self._load_patterns()
        self._load_transferable_knowledge()
        self._load_consolidations()
    
    def _load_patterns(self):
        """Load patterns from disk"""
        if os.path.exists(self.patterns_dir):
            for filename in os.listdir(self.patterns_dir):
                if filename.endswith('_pattern.json'):
                    filepath = os.path.join(self.patterns_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            pattern = ExperiencePattern(
                                pattern_id=data['pattern_id'],
                                pattern_type=PatternType(data['pattern_type']),
                                description=data['description'],
                                confidence=data['confidence'],
                                supporting_interactions=data['supporting_interactions'],
                                metadata=data.get('metadata', {}),
                                discovered_at=data['discovered_at'],
                                last_observed=data.get('last_observed')
                            )
                            self._patterns_cache[pattern.pattern_id] = pattern
                    except Exception:
                        continue
    
    def _save_pattern(self, pattern: ExperiencePattern):
        """Save a pattern to disk"""
        filename = f"{pattern.pattern_id}_pattern.json"
        filepath = os.path.join(self.patterns_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(pattern.to_dict(), f, indent=2)
    
    def _load_transferable_knowledge(self):
        """Load transferable knowledge from disk"""
        if os.path.exists(self.knowledge_dir):
            for filename in os.listdir(self.knowledge_dir):
                if filename.endswith('_knowledge.json'):
                    filepath = os.path.join(self.knowledge_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            knowledge = TransferableKnowledge(
                                knowledge_id=data['knowledge_id'],
                                source_skill_id=data['source_skill_id'],
                                content=data['content'],
                                applicability_score=data['applicability_score'],
                                categories=data.get('categories', []),
                                verified=data.get('verified', False),
                                transfer_count=data.get('transfer_count', 0),
                                created_at=data['created_at']
                            )
                            self._transferable_knowledge_cache[knowledge.knowledge_id] = knowledge
                    except Exception:
                        continue
    
    def _save_transferable_knowledge(self, knowledge: TransferableKnowledge):
        """Save transferable knowledge to disk"""
        filename = f"{knowledge.knowledge_id}_knowledge.json"
        filepath = os.path.join(self.knowledge_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(knowledge.to_dict(), f, indent=2)
    
    def _load_consolidations(self):
        """Load memory consolidations from disk"""
        if os.path.exists(self.consolidation_dir):
            for filename in os.listdir(self.consolidation_dir):
                if filename.endswith('_consolidation.json'):
                    filepath = os.path.join(self.consolidation_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            consolidation = MemoryConsolidation(
                                consolidation_id=data['consolidation_id'],
                                skill_id=data['skill_id'],
                                time_window_start=data['time_window_start'],
                                time_window_end=data['time_window_end'],
                                key_insights=data.get('key_insights', []),
                                consolidated_lessons=data.get('consolidated_lessons', []),
                                performance_summary=data.get('performance_summary', {}),
                                created_at=data['created_at']
                            )
                            self._consolidations_cache[consolidation.consolidation_id] = consolidation
                    except Exception:
                        continue
    
    def _save_consolidation(self, consolidation: MemoryConsolidation):
        """Save a memory consolidation to disk"""
        filename = f"{consolidation.consolidation_id}_consolidation.json"
        filepath = os.path.join(self.consolidation_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(consolidation.to_dict(), f, indent=2)
    
    def recognize_patterns(self, skill_id: str, min_confidence: float = 0.6) -> List[ExperiencePattern]:
        """Recognize patterns in a skill's experience data"""
        import uuid
        interactions = self.get_skill_interactions(skill_id, limit=100)
        patterns_found = []
        
        if len(interactions) < 5:
            return patterns_found
        
        success_interactions = [i for i in interactions if i.outcome == InteractionOutcome.SUCCESS]
        failed_interactions = [i for i in interactions if i.outcome == InteractionOutcome.FAILED]
        
        if len(success_interactions) >= 3:
            pattern = ExperiencePattern(
                pattern_id=str(uuid.uuid4()),
                pattern_type=PatternType.SUCCESS_PATTERN,
                description=f"Success pattern identified for skill {skill_id}",
                confidence=min(1.0, len(success_interactions) / len(interactions)),
                supporting_interactions=[i.interaction_id for i in success_interactions[:20]],
                metadata={"success_count": len(success_interactions)}
            )
            patterns_found.append(pattern)
            self._patterns_cache[pattern.pattern_id] = pattern
            self._save_pattern(pattern)
        
        if len(failed_interactions) >= 3:
            pattern = ExperiencePattern(
                pattern_id=str(uuid.uuid4()),
                pattern_type=PatternType.FAILURE_PATTERN,
                description=f"Failure pattern identified for skill {skill_id}",
                confidence=min(1.0, len(failed_interactions) / len(interactions)),
                supporting_interactions=[i.interaction_id for i in failed_interactions[:20]],
                metadata={"failure_count": len(failed_interactions)}
            )
            patterns_found.append(pattern)
            self._patterns_cache[pattern.pattern_id] = pattern
            self._save_pattern(pattern)
        
        common_errors = defaultdict(int)
        for interaction in interactions:
            for error in interaction.error_messages:
                common_errors[error] += 1
        
        for error, count in common_errors.items():
            if count >= 2:
                pattern = ExperiencePattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.ERROR_PATTERN,
                    description=f"Recurring error: {error[:100]}",
                    confidence=min(1.0, count / len(interactions)),
                    supporting_interactions=[i.interaction_id for i in interactions if error in i.error_messages][:20],
                    metadata={"error_count": count, "error": error}
                )
                patterns_found.append(pattern)
                self._patterns_cache[pattern.pattern_id] = pattern
                self._save_pattern(pattern)
        
        return [p for p in patterns_found if p.confidence >= min_confidence]
    
    def extract_transferable_knowledge(self, source_skill_id: str) -> List[TransferableKnowledge]:
        """Extract knowledge that can be transferred to other skills"""
        import uuid
        experience = self.get_skill_experience(source_skill_id)
        if not experience or experience.total_interactions < 10:
            return []
        
        knowledge_items = []
        
        if experience.success_rate > 0.7:
            knowledge = TransferableKnowledge(
                knowledge_id=str(uuid.uuid4()),
                source_skill_id=source_skill_id,
                content=f"Skill demonstrates {experience.success_rate:.1%} success rate",
                applicability_score=0.7,
                categories=["success_pattern", "performance"]
            )
            knowledge_items.append(knowledge)
            self._transferable_knowledge_cache[knowledge.knowledge_id] = knowledge
            self._save_transferable_knowledge(knowledge)
        
        if experience.common_errors:
            for error in experience.common_errors[:3]:
                knowledge = TransferableKnowledge(
                    knowledge_id=str(uuid.uuid4()),
                    source_skill_id=source_skill_id,
                    content=f"Common issue to address: {error}",
                    applicability_score=0.6,
                    categories=["error_handling", "troubleshooting"]
                )
                knowledge_items.append(knowledge)
                self._transferable_knowledge_cache[knowledge.knowledge_id] = knowledge
                self._save_transferable_knowledge(knowledge)
        
        return knowledge_items
    
    def get_relevant_knowledge(self, target_skill_id: str, categories: Optional[List[str]] = None, limit: int = 5) -> List[TransferableKnowledge]:
        """Get transferable knowledge relevant to a target skill"""
        all_knowledge = list(self._transferable_knowledge_cache.values())
        
        if categories:
            all_knowledge = [k for k in all_knowledge if any(cat in k.categories for cat in categories)]
        
        all_knowledge.sort(key=lambda k: k.applicability_score, reverse=True)
        return all_knowledge[:limit]
    
    def consolidate_memory(self, skill_id: str, days: int = 7) -> MemoryConsolidation:
        """Consolidate memory from a time window"""
        import uuid
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        interactions = self.get_skill_interactions(skill_id, limit=1000)
        window_interactions = [
            i for i in interactions
            if datetime.fromisoformat(i.completed_at or i.started_at) >= start_time
        ]
        
        if not window_interactions:
            window_interactions = interactions[:100]
        
        consolidation = MemoryConsolidation(
            consolidation_id=str(uuid.uuid4()),
            skill_id=skill_id,
            time_window_start=start_time.isoformat(),
            time_window_end=end_time.isoformat()
        )
        
        success_count = sum(1 for i in window_interactions if i.outcome == InteractionOutcome.SUCCESS)
        if window_interactions:
            consolidation.key_insights.append(f"Success rate: {success_count / len(window_interactions):.1%} over {len(window_interactions)} interactions")
        
        experience = self.get_skill_experience(skill_id)
        if experience:
            if experience.common_errors:
                consolidation.key_insights.append(f"Top issues: {', '.join(experience.common_errors[:3])}")
                consolidation.consolidated_lessons.extend([f"Address: {err}" for err in experience.common_errors[:5]])
        
        consolidation.performance_summary = {
            "total_interactions": len(window_interactions),
            "success_count": success_count
        }
        
        self._consolidations_cache[consolidation.consolidation_id] = consolidation
        self._save_consolidation(consolidation)
        
        return consolidation
    
    def analyze_temporal_trends(self, skill_id: str, metric_name: str = "success_rate") -> Optional[TemporalTrend]:
        """Analyze temporal trends in skill performance"""
        import uuid
        interactions = self.get_skill_interactions(skill_id, limit=200)
        if len(interactions) < 10:
            return None
        
        data_points = []
        window_size = min(10, len(interactions) // 3)
        
        for i in range(window_size, len(interactions), window_size):
            window = interactions[i-window_size:i]
            success_rate = sum(1 for w in window if w.outcome == InteractionOutcome.SUCCESS) / len(window)
            data_points.append({
                "index": i,
                "success_rate": success_rate,
                "timestamp": window[-1].completed_at or window[-1].started_at
            })
        
        if len(data_points) < 3:
            return None
        
        first_rate = data_points[0]["success_rate"]
        last_rate = data_points[-1]["success_rate"]
        trend_diff = last_rate - first_rate
        
        trend = TemporalTrend(
            skill_id=skill_id,
            metric_name=metric_name,
            trend_direction="improving" if trend_diff > 0.05 else "declining" if trend_diff < -0.05 else "stable",
            trend_strength=abs(trend_diff),
            data_points=data_points
        )
        
        return trend
    
    def get_patterns(self, skill_id: Optional[str] = None, pattern_type: Optional[PatternType] = None) -> List[ExperiencePattern]:
        """Get recognized patterns, optionally filtered"""
        patterns = list(self._patterns_cache.values())
        if skill_id:
            patterns = [p for p in patterns if skill_id in p.description]
        if pattern_type:
            patterns = [p for p in patterns if p.pattern_type == pattern_type]
        return patterns
    
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
