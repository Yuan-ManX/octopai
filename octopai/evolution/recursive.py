"""
Recursive Evolution Engine - Octopai's Dynamic Skill Evolution System

This module provides Octopai's proprietary recursive skill evolution mechanism
where the skill library co-evolves with agent performance. Features include
dynamic skill updates based on validation feedback, self-verification,
and adaptive learning strategies.
"""

import os
import json
import hashlib
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path


class EvolutionTrigger(Enum):
    """Triggers for skill evolution"""
    PERFORMANCE_DROP = "performance_drop"
    VALIDATION_FAILURE = "validation_failure"
    NEW_EXPERIENCE = "new_experience"
    SCHEDULED = "scheduled"
    MANUAL = "manual"


class EvolutionStatus(Enum):
    """Status of an evolution cycle"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class ValidationResult:
    """Result from skill validation"""
    validation_id: str
    skill_id: str
    skill_version: int
    passed: bool = False
    test_results: Dict[str, bool] = field(default_factory=dict)
    confidence_score: float = 0.0
    issues_found: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    validated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "validation_id": self.validation_id,
            "skill_id": self.skill_id,
            "skill_version": self.skill_version,
            "passed": self.passed,
            "test_results": self.test_results,
            "confidence_score": self.confidence_score,
            "issues_found": self.issues_found,
            "recommendations": self.recommendations,
            "performance_metrics": self.performance_metrics,
            "validated_at": self.validated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ValidationResult':
        return cls(**data)


@dataclass
class EvolutionProposal:
    """A proposal for skill evolution"""
    proposal_id: str
    skill_id: str
    trigger: EvolutionTrigger
    current_version: int
    proposed_changes: str
    rationale: str
    expected_improvements: List[str] = field(default_factory=list)
    risk_level: str = "medium"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "pending"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "skill_id": self.skill_id,
            "trigger": self.trigger.value,
            "current_version": self.current_version,
            "proposed_changes": self.proposed_changes,
            "rationale": self.rationale,
            "expected_improvements": self.expected_improvements,
            "risk_level": self.risk_level,
            "created_at": self.created_at,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EvolutionProposal':
        data = data.copy()
        data['trigger'] = EvolutionTrigger(data['trigger'])
        return cls(**data)


@dataclass
class EvolutionCycle:
    """A complete evolution cycle"""
    cycle_id: str
    skill_id: str
    trigger: EvolutionTrigger
    status: EvolutionStatus = EvolutionStatus.PENDING
    start_version: int = 0
    end_version: Optional[int] = None
    proposals: List[EvolutionProposal] = field(default_factory=list)
    validations: List[ValidationResult] = field(default_factory=list)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "cycle_id": self.cycle_id,
            "skill_id": self.skill_id,
            "trigger": self.trigger.value,
            "status": self.status.value,
            "start_version": self.start_version,
            "end_version": self.end_version,
            "proposals": [p.to_dict() for p in self.proposals],
            "validations": [v.to_dict() for v in self.validations],
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error_message": self.error_message,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EvolutionCycle':
        data = data.copy()
        data['trigger'] = EvolutionTrigger(data['trigger'])
        data['status'] = EvolutionStatus(data['status'])
        data['proposals'] = [EvolutionProposal.from_dict(p) for p in data.get('proposals', [])]
        data['validations'] = [ValidationResult.from_dict(v) for v in data.get('validations', [])]
        return cls(**data)


@dataclass
class EvolutionConfig:
    """Configuration for the evolution engine"""
    update_threshold: float = 0.4
    max_new_skills_per_cycle: int = 3
    min_success_rate_for_evolution: float = 0.3
    auto_evolve_enabled: bool = True
    validation_required: bool = True
    max_concurrent_cycles: int = 2
    risk_acceptance_level: str = "medium"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "update_threshold": self.update_threshold,
            "max_new_skills_per_cycle": self.max_new_skills_per_cycle,
            "min_success_rate_for_evolution": self.min_success_rate_for_evolution,
            "auto_evolve_enabled": self.auto_evolve_enabled,
            "validation_required": self.validation_required,
            "max_concurrent_cycles": self.max_concurrent_cycles,
            "risk_acceptance_level": self.risk_acceptance_level
        }


class RecursiveEvolutionEngine:
    """
    Recursive Skill Evolution Engine
    
    Features:
    - Dynamic skill evolution based on performance and validation
    - Co-evolution of skill library with agent policy
    - Self-verification of skill improvements
    - Adaptive mutation strategies
    - Rollback capabilities
    - Evolution history and traceability
    """
    
    def __init__(
        self,
        storage_dir: str = "./RecursiveEvolution",
        config: Optional[EvolutionConfig] = None
    ):
        self.storage_dir = Path(storage_dir)
        self.cycles_dir = self.storage_dir / "cycles"
        self.validations_dir = self.storage_dir / "validations"
        self.config_file = self.storage_dir / "config.json"
        
        self.config = config or EvolutionConfig()
        self.cycles: Dict[str, EvolutionCycle] = {}
        self.active_cycles: Set[str] = set()
        self.skill_performance_history: Dict[str, List[Dict[str, Any]]] = {}
        
        self._initialize_storage()
        self._load_data()
    
    def _initialize_storage(self):
        """Initialize storage directories"""
        self.cycles_dir.mkdir(parents=True, exist_ok=True)
        self.validations_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.config_file.exists():
            self._save_config()
    
    def _load_data(self):
        """Load data from disk"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.config = EvolutionConfig(**data)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        for cycle_file in self.cycles_dir.glob("*.json"):
            try:
                with open(cycle_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cycle = EvolutionCycle.from_dict(data)
                    self.cycles[cycle.cycle_id] = cycle
                    if cycle.status == EvolutionStatus.RUNNING:
                        self.active_cycles.add(cycle.cycle_id)
            except Exception as e:
                print(f"Error loading cycle {cycle_file}: {e}")
    
    def _save_config(self):
        """Save configuration to disk"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config.to_dict(), f, indent=2)
    
    def _save_cycle(self, cycle: EvolutionCycle):
        """Save an evolution cycle to disk"""
        filepath = self.cycles_dir / f"{cycle.cycle_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(cycle.to_dict(), f, indent=2)
    
    def _save_validation(self, validation: ValidationResult):
        """Save a validation result to disk"""
        filepath = self.validations_dir / f"{validation.validation_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(validation.to_dict(), f, indent=2)
    
    def _generate_id(self, prefix: str) -> str:
        """Generate a unique ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = hashlib.md5(os.urandom(8)).hexdigest()[:6]
        return f"{prefix}_{timestamp}_{random_suffix}"
    
    def record_skill_performance(
        self,
        skill_id: str,
        version: int,
        success: bool,
        performance_metrics: Optional[Dict[str, float]] = None,
        context: Optional[str] = None
    ):
        """
        Record skill performance for evolution monitoring
        
        Args:
            skill_id: Skill ID
            version: Skill version
            success: Whether the skill application was successful
            performance_metrics: Optional performance metrics
            context: Optional context about the usage
        """
        if skill_id not in self.skill_performance_history:
            self.skill_performance_history[skill_id] = []
        
        record = {
            'version': version,
            'success': success,
            'performance_metrics': performance_metrics or {},
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
        
        self.skill_performance_history[skill_id].append(record)
        
        recent_records = self.skill_performance_history[skill_id][-20:]
        recent_successes = sum(1 for r in recent_records if r['success'])
        recent_success_rate = recent_successes / len(recent_records) if recent_records else 0
        
        if recent_success_rate < self.config.update_threshold and self.config.auto_evolve_enabled:
            self.trigger_evolution(
                skill_id=skill_id,
                trigger=EvolutionTrigger.PERFORMANCE_DROP
            )
    
    def trigger_evolution(
        self,
        skill_id: str,
        trigger: EvolutionTrigger = EvolutionTrigger.MANUAL,
        current_version: int = 1,
        rationale: str = ""
    ) -> Optional[EvolutionCycle]:
        """
        Trigger an evolution cycle for a skill
        
        Args:
            skill_id: Skill ID to evolve
            trigger: Evolution trigger
            current_version: Current skill version
            rationale: Rationale for evolution
            
        Returns:
            Created EvolutionCycle or None
        """
        if len(self.active_cycles) >= self.config.max_concurrent_cycles:
            return None
        
        cycle_id = self._generate_id("cycle")
        
        cycle = EvolutionCycle(
            cycle_id=cycle_id,
            skill_id=skill_id,
            trigger=trigger,
            status=EvolutionStatus.PENDING,
            start_version=current_version,
            metadata={'rationale': rationale}
        )
        
        self.cycles[cycle_id] = cycle
        self._save_cycle(cycle)
        
        return cycle
    
    def start_evolution_cycle(self, cycle_id: str) -> bool:
        """
        Start an evolution cycle
        
        Args:
            cycle_id: Cycle ID to start
            
        Returns:
            True if started successfully
        """
        if cycle_id not in self.cycles:
            return False
        
        cycle = self.cycles[cycle_id]
        if cycle.status != EvolutionStatus.PENDING:
            return False
        
        cycle.status = EvolutionStatus.RUNNING
        cycle.started_at = datetime.now().isoformat()
        self.active_cycles.add(cycle_id)
        self._save_cycle(cycle)
        return True
    
    def create_evolution_proposal(
        self,
        cycle_id: str,
        proposed_changes: str,
        rationale: str,
        expected_improvements: Optional[List[str]] = None,
        risk_level: str = "medium"
    ) -> Optional[EvolutionProposal]:
        """
        Create an evolution proposal within a cycle
        
        Args:
            cycle_id: Evolution cycle ID
            proposed_changes: Description of proposed changes
            rationale: Rationale for the changes
            expected_improvements: Expected improvements
            risk_level: Risk level (low, medium, high)
            
        Returns:
            Created EvolutionProposal or None
        """
        if cycle_id not in self.cycles:
            return None
        
        cycle = self.cycles[cycle_id]
        
        proposal_id = self._generate_id("proposal")
        proposal = EvolutionProposal(
            proposal_id=proposal_id,
            skill_id=cycle.skill_id,
            trigger=cycle.trigger,
            current_version=cycle.start_version,
            proposed_changes=proposed_changes,
            rationale=rationale,
            expected_improvements=expected_improvements or [],
            risk_level=risk_level
        )
        
        cycle.proposals.append(proposal)
        self._save_cycle(cycle)
        return proposal
    
    def validate_skill(
        self,
        cycle_id: str,
        skill_id: str,
        skill_version: int,
        passed: bool,
        test_results: Optional[Dict[str, bool]] = None,
        confidence_score: float = 0.0,
        issues_found: Optional[List[str]] = None,
        recommendations: Optional[List[str]] = None,
        performance_metrics: Optional[Dict[str, float]] = None
    ) -> ValidationResult:
        """
        Validate an evolved skill
        
        Args:
            cycle_id: Evolution cycle ID
            skill_id: Skill ID
            skill_version: Skill version
            passed: Whether validation passed
            test_results: Detailed test results
            confidence_score: Confidence score
            issues_found: Issues found during validation
            recommendations: Recommendations
            performance_metrics: Performance metrics
            
        Returns:
            ValidationResult
        """
        validation_id = self._generate_id("validation")
        
        validation = ValidationResult(
            validation_id=validation_id,
            skill_id=skill_id,
            skill_version=skill_version,
            passed=passed,
            test_results=test_results or {},
            confidence_score=confidence_score,
            issues_found=issues_found or [],
            recommendations=recommendations or [],
            performance_metrics=performance_metrics or {}
        )
        
        self._save_validation(validation)
        
        if cycle_id in self.cycles:
            cycle = self.cycles[cycle_id]
            cycle.validations.append(validation)
            self._save_cycle(cycle)
        
        return validation
    
    def complete_evolution_cycle(
        self,
        cycle_id: str,
        success: bool,
        end_version: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Complete an evolution cycle
        
        Args:
            cycle_id: Cycle ID to complete
            success: Whether the cycle was successful
            end_version: Ending skill version
            error_message: Error message if failed
            
        Returns:
            True if completed successfully
        """
        if cycle_id not in self.cycles:
            return False
        
        cycle = self.cycles[cycle_id]
        if cycle.status != EvolutionStatus.RUNNING:
            return False
        
        cycle.status = EvolutionStatus.COMPLETED if success else EvolutionStatus.FAILED
        cycle.end_version = end_version
        cycle.completed_at = datetime.now().isoformat()
        cycle.error_message = error_message
        
        self.active_cycles.discard(cycle_id)
        self._save_cycle(cycle)
        return True
    
    def rollback_cycle(self, cycle_id: str) -> bool:
        """
        Rollback an evolution cycle
        
        Args:
            cycle_id: Cycle ID to rollback
            
        Returns:
            True if rolled back successfully
        """
        if cycle_id not in self.cycles:
            return False
        
        cycle = self.cycles[cycle_id]
        cycle.status = EvolutionStatus.ROLLED_BACK
        self.active_cycles.discard(cycle_id)
        self._save_cycle(cycle)
        return True
    
    def get_cycle(self, cycle_id: str) -> Optional[EvolutionCycle]:
        """Get an evolution cycle by ID"""
        return self.cycles.get(cycle_id)
    
    def get_skill_cycles(self, skill_id: str) -> List[EvolutionCycle]:
        """Get all evolution cycles for a skill"""
        return [
            cycle for cycle in self.cycles.values()
            if cycle.skill_id == skill_id
        ]
    
    def get_active_cycles(self) -> List[EvolutionCycle]:
        """Get all active evolution cycles"""
        return [
            cycle for cycle in self.cycles.values()
            if cycle.status == EvolutionStatus.RUNNING
        ]
    
    def get_skill_performance_trend(
        self,
        skill_id: str,
        version: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get performance trend for a skill
        
        Args:
            skill_id: Skill ID
            version: Optional version filter
            
        Returns:
            Performance trend data
        """
        records = self.skill_performance_history.get(skill_id, [])
        
        if version is not None:
            records = [r for r in records if r['version'] == version]
        
        if not records:
            return {
                'total_uses': 0,
                'success_rate': 0.0,
                'recent_trend': 'unknown'
            }
        
        total_uses = len(records)
        success_count = sum(1 for r in records if r['success'])
        success_rate = success_count / total_uses
        
        recent_10 = records[-10:] if len(records) >= 10 else records
        recent_success = sum(1 for r in recent_10 if r['success'])
        recent_rate = recent_success / len(recent_10) if recent_10 else 0
        
        trend = 'stable'
        if recent_rate > success_rate + 0.1:
            trend = 'improving'
        elif recent_rate < success_rate - 0.1:
            trend = 'declining'
        
        return {
            'total_uses': total_uses,
            'success_rate': success_rate,
            'recent_success_rate': recent_rate,
            'trend': trend,
            'latest_record': records[-1] if records else None
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get evolution engine statistics"""
        total_cycles = len(self.cycles)
        completed_cycles = sum(
            1 for cycle in self.cycles.values()
            if cycle.status == EvolutionStatus.COMPLETED
        )
        failed_cycles = sum(
            1 for cycle in self.cycles.values()
            if cycle.status == EvolutionStatus.FAILED
        )
        active_cycles = len(self.active_cycles)
        
        skills_tracked = len(self.skill_performance_history)
        
        return {
            'total_cycles': total_cycles,
            'completed_cycles': completed_cycles,
            'failed_cycles': failed_cycles,
            'active_cycles': active_cycles,
            'skills_tracked': skills_tracked,
            'config': self.config.to_dict()
        }
