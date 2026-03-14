"""
EXO Pipeline - Unified Skill Development Workflow

This module provides EXO's proprietary unified pipeline that orchestrates
the complete skill development lifecycle from creation through optimization
to packaging and management.
"""

import os
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from exo.core.skill_factory import SkillFactory, SkillDefinition, SkillType
from exo.core.evolution_engine import EvolutionEngine, EvolutionConfig
from exo.core.skill_packager import SkillPackager, PackageConfig
from exo.core.skill_hub import SkillHub, Skill
from exo.core.experience_tracker import (
    ExperienceTracker, 
    InteractionType, 
    InteractionOutcome
)
from exo.utils.helpers import write_file
import shutil


class PipelineStage(Enum):
    """Stages in the EXO pipeline"""
    CREATION = "creation"
    OPTIMIZATION = "optimization"
    PACKAGING = "packaging"
    VALIDATION = "validation"
    PUBLISHING = "publishing"


@dataclass
class PipelineResult:
    """Result of a pipeline execution"""
    success: bool
    stage: PipelineStage
    skill_id: Optional[str] = None
    skill_dir: Optional[str] = None
    skill_definition: Optional[SkillDefinition] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    duration_seconds: Optional[float] = None
    
    def mark_complete(self):
        """Mark the result as complete"""
        self.completed_at = datetime.now().isoformat()
        if self.started_at and self.completed_at:
            start = datetime.fromisoformat(self.started_at)
            end = datetime.fromisoformat(self.completed_at)
            self.duration_seconds = (end - start).total_seconds()


@dataclass
class PipelineConfig:
    """Configuration for the EXO pipeline"""
    auto_optimize: bool = True
    auto_package: bool = True
    auto_validate: bool = True
    auto_publish: bool = False
    optimization_config: Optional[EvolutionConfig] = None
    package_config: Optional[PackageConfig] = None
    skill_output_dir: str = "./skills"
    experience_tracking: bool = True


class EXOPipeline:
    """
    EXO's Unified Pipeline - Complete Skill Development Orchestration
    
    Orchestrates the entire skill development lifecycle through EXO's
    proprietary pipeline, providing a seamless, end-to-end experience.
    """
    
    def __init__(
        self,
        config: Optional[PipelineConfig] = None,
        skill_factory: Optional[SkillFactory] = None,
        evolution_engine: Optional[EvolutionEngine] = None,
        skill_packager: Optional[SkillPackager] = None,
        skill_hub: Optional[SkillHub] = None,
        experience_tracker: Optional[ExperienceTracker] = None,
    ):
        self.config = config or PipelineConfig()
        
        self.skill_factory = skill_factory or SkillFactory()
        self.experience_tracker = experience_tracker or ExperienceTracker()
        self.evolution_engine = evolution_engine or EvolutionEngine(
            config=self.config.optimization_config, 
            experience_tracker=self.experience_tracker
        )
        self.skill_packager = skill_packager or SkillPackager(self.config.skill_output_dir)
        self.skill_hub = skill_hub or SkillHub()
        
        self._callbacks: Dict[PipelineStage, List[Callable]] = {
            stage: [] for stage in PipelineStage
        }
    
    def create_from_url(
        self,
        url: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        config: Optional[PipelineConfig] = None
    ) -> PipelineResult:
        """
        Create a complete skill package from a URL
        
        Args:
            url: Web URL to transform
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags
            category: Optional category
            author: Optional author
            skill_type: Type of skill
            config: Optional pipeline config override
            
        Returns:
            Pipeline result with complete skill package
        """
        pipeline_config = config or self.config
        
        result = PipelineResult(
            success=False,
            stage=PipelineStage.CREATION
        )
        
        interaction_id = None
        if pipeline_config.experience_tracking:
            interaction_id = self.experience_tracker.start_interaction(
                skill_id="pending",
                skill_version=1,
                interaction_type=InteractionType.CREATION,
                custom_data={"source": "url", "url": url}
            )
        
        try:
            skill_def = self.skill_factory.create_from_url(
                url=url,
                name=name,
                description=description,
                tags=tags,
                category=category,
                author=author,
                skill_type=skill_type
            )
            
            result.skill_id = skill_def.metadata.skill_id
            result.skill_definition = skill_def
            result.stage = PipelineStage.CREATION
            
            self._trigger_callbacks(PipelineStage.CREATION, result)
            
            if pipeline_config.auto_optimize:
                skill_dir = self._package_initial(skill_def)
                result = self._optimize_skill(result, skill_dir, pipeline_config)
            
            if pipeline_config.auto_package and result.success:
                result = self._package_skill(result, skill_def, pipeline_config)
            
            if pipeline_config.auto_validate and result.success:
                result = self._validate_skill(result)
            
            if pipeline_config.auto_publish and result.success:
                result = self._publish_skill(result)
            
            result.success = True
            
            if pipeline_config.experience_tracking and interaction_id:
                self.experience_tracker.complete_interaction(
                    interaction_id=interaction_id,
                    outcome=InteractionOutcome.SUCCESS,
                    performance_metrics=result.metrics
                )
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
            
            if pipeline_config.experience_tracking and interaction_id:
                self.experience_tracker.complete_interaction(
                    interaction_id=interaction_id,
                    outcome=InteractionOutcome.FAILED,
                    error_messages=[str(e)]
                )
        
        result.mark_complete()
        return result
    
    def create_from_files(
        self,
        file_paths: List[str],
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        config: Optional[PipelineConfig] = None
    ) -> PipelineResult:
        """
        Create a complete skill package from files
        
        Args:
            file_paths: List of file paths
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags
            category: Optional category
            author: Optional author
            skill_type: Type of skill
            config: Optional pipeline config override
            
        Returns:
            Pipeline result with complete skill package
        """
        pipeline_config = config or self.config
        
        result = PipelineResult(
            success=False,
            stage=PipelineStage.CREATION
        )
        
        interaction_id = None
        if pipeline_config.experience_tracking:
            interaction_id = self.experience_tracker.start_interaction(
                skill_id="pending",
                skill_version=1,
                interaction_type=InteractionType.CREATION,
                custom_data={"source": "files", "files": file_paths}
            )
        
        try:
            skill_def = self.skill_factory.create_from_files(
                file_paths=file_paths,
                name=name,
                description=description,
                tags=tags,
                category=category,
                author=author,
                skill_type=skill_type
            )
            
            result.skill_id = skill_def.metadata.skill_id
            result.skill_definition = skill_def
            result.stage = PipelineStage.CREATION
            
            self._trigger_callbacks(PipelineStage.CREATION, result)
            
            if pipeline_config.auto_optimize:
                skill_dir = self._package_initial(skill_def)
                result = self._optimize_skill(result, skill_dir, pipeline_config)
            
            if pipeline_config.auto_package and result.success:
                result = self._package_skill(result, skill_def, pipeline_config)
            
            if pipeline_config.auto_validate and result.success:
                result = self._validate_skill(result)
            
            if pipeline_config.auto_publish and result.success:
                result = self._publish_skill(result)
            
            result.success = True
            
            if pipeline_config.experience_tracking and interaction_id:
                self.experience_tracker.complete_interaction(
                    interaction_id=interaction_id,
                    outcome=InteractionOutcome.SUCCESS,
                    performance_metrics=result.metrics
                )
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
            
            if pipeline_config.experience_tracking and interaction_id:
                self.experience_tracker.complete_interaction(
                    interaction_id=interaction_id,
                    outcome=InteractionOutcome.FAILED,
                    error_messages=[str(e)]
                )
        
        result.mark_complete()
        return result
    
    def create_from_prompt(
        self,
        prompt: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        resources: Optional[List[str]] = None,
        config: Optional[PipelineConfig] = None
    ) -> PipelineResult:
        """
        Create a complete skill package from a prompt
        
        Args:
            prompt: Description of what the skill should do
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags
            category: Optional category
            author: Optional author
            skill_type: Type of skill
            resources: Optional resource files
            config: Optional pipeline config override
            
        Returns:
            Pipeline result with complete skill package
        """
        pipeline_config = config or self.config
        
        result = PipelineResult(
            success=False,
            stage=PipelineStage.CREATION
        )
        
        interaction_id = None
        if pipeline_config.experience_tracking:
            interaction_id = self.experience_tracker.start_interaction(
                skill_id="pending",
                skill_version=1,
                interaction_type=InteractionType.CREATION,
                custom_data={"source": "prompt"}
            )
        
        try:
            skill_def = self.skill_factory.create_from_prompt(
                prompt=prompt,
                name=name,
                description=description,
                tags=tags,
                category=category,
                author=author,
                skill_type=skill_type,
                resources=resources
            )
            
            result.skill_id = skill_def.metadata.skill_id
            result.skill_definition = skill_def
            result.stage = PipelineStage.CREATION
            
            self._trigger_callbacks(PipelineStage.CREATION, result)
            
            if pipeline_config.auto_optimize:
                skill_dir = self._package_initial(skill_def)
                result = self._optimize_skill(result, skill_dir, pipeline_config)
            
            if pipeline_config.auto_package and result.success:
                result = self._package_skill(result, skill_def, pipeline_config)
            
            if pipeline_config.auto_validate and result.success:
                result = self._validate_skill(result)
            
            if pipeline_config.auto_publish and result.success:
                result = self._publish_skill(result)
            
            result.success = True
            
            if pipeline_config.experience_tracking and interaction_id:
                self.experience_tracker.complete_interaction(
                    interaction_id=interaction_id,
                    outcome=InteractionOutcome.SUCCESS,
                    performance_metrics=result.metrics
                )
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
            
            if pipeline_config.experience_tracking and interaction_id:
                self.experience_tracker.complete_interaction(
                    interaction_id=interaction_id,
                    outcome=InteractionOutcome.FAILED,
                    error_messages=[str(e)]
                )
        
        result.mark_complete()
        return result
    
    def optimize_existing(
        self,
        skill_dir: str,
        config: Optional[PipelineConfig] = None
    ) -> PipelineResult:
        """
        Optimize an existing skill
        
        Args:
            skill_dir: Directory containing the skill
            config: Optional pipeline config override
            
        Returns:
            Pipeline result with optimized skill
        """
        pipeline_config = config or self.config
        
        result = PipelineResult(
            success=False,
            stage=PipelineStage.OPTIMIZATION,
            skill_dir=skill_dir
        )
        
        try:
            result = self._optimize_skill(result, skill_dir, pipeline_config)
            result.success = True
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
        
        result.mark_complete()
        return result
    
    def register_callback(
        self,
        stage: PipelineStage,
        callback: Callable[[PipelineResult], None]
    ):
        """
        Register a callback for a pipeline stage
        
        Args:
            stage: Pipeline stage to listen to
            callback: Function to call when stage completes
        """
        self._callbacks[stage].append(callback)
    
    def _package_initial(self, skill_def: SkillDefinition) -> str:
        """Package the initial skill version for optimization"""
        skill_dir = os.path.join(self.config.skill_output_dir, skill_def.metadata.skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        
        latest_version = skill_def.latest_version
        if latest_version:
            skill_file = os.path.join(skill_dir, 'SKILL.md')
            write_file(skill_file, latest_version.content)
        
        return skill_dir
    
    def _optimize_skill(
        self,
        result: PipelineResult,
        skill_dir: str,
        config: PipelineConfig
    ) -> PipelineResult:
        """Internal: Optimize a skill"""
        result.stage = PipelineStage.OPTIMIZATION
        
        interaction_id = None
        if config.experience_tracking and result.skill_id:
            interaction_id = self.experience_tracker.start_interaction(
                skill_id=result.skill_id,
                skill_version=1,
                interaction_type=InteractionType.OPTIMIZATION
            )
        
        optimized_dir = self.evolution_engine.evolve_skill(
            skill_dir,
            config.optimization_config
        )
        
        result.skill_dir = optimized_dir
        result.metrics['optimization_complete'] = True
        
        self._trigger_callbacks(PipelineStage.OPTIMIZATION, result)
        
        if config.experience_tracking and interaction_id:
            self.experience_tracker.complete_interaction(
                interaction_id=interaction_id,
                outcome=InteractionOutcome.SUCCESS
            )
        
        return result
    
    def _package_skill(
        self,
        result: PipelineResult,
        skill_def: SkillDefinition,
        config: PipelineConfig
    ) -> PipelineResult:
        """Internal: Package a skill"""
        result.stage = PipelineStage.PACKAGING
        
        latest_version = skill_def.latest_version
        if latest_version:
            skill_dir = self.skill_packager.create_package(
                skill_name=skill_def.metadata.name,
                skill_description=skill_def.metadata.description,
                skill_content=latest_version.content,
                tags=skill_def.metadata.tags,
                category=skill_def.metadata.category,
                author=skill_def.metadata.author,
                config=config.package_config
            )
            result.skill_dir = skill_dir
        
        result.metrics['packaging_complete'] = True
        self._trigger_callbacks(PipelineStage.PACKAGING, result)
        
        return result
    
    def _validate_skill(
        self,
        result: PipelineResult
    ) -> PipelineResult:
        """Internal: Validate a skill package"""
        result.stage = PipelineStage.VALIDATION
        
        if result.skill_dir:
            is_valid, issues = self.skill_packager.validate_package(result.skill_dir)
            
            if not is_valid:
                result.warnings.extend(issues)
            
            result.metrics['validation_passed'] = is_valid
            result.metrics['validation_issues'] = len(issues)
        
        self._trigger_callbacks(PipelineStage.VALIDATION, result)
        
        return result
    
    def _publish_skill(
        self,
        result: PipelineResult
    ) -> PipelineResult:
        """Internal: Publish a skill to SkillHub"""
        result.stage = PipelineStage.PUBLISHING
        
        if result.skill_dir:
            skill = Skill(
                name=os.path.basename(result.skill_dir),
                path=result.skill_dir
            )
            self.skill_hub.add_skill(skill)
            
            result.metrics['published'] = True
        
        self._trigger_callbacks(PipelineStage.PUBLISHING, result)
        
        return result
    
    def _trigger_callbacks(self, stage: PipelineStage, result: PipelineResult):
        """Trigger callbacks for a stage"""
        for callback in self._callbacks[stage]:
            try:
                callback(result)
            except Exception as e:
                print(f"Callback error: {e}")
