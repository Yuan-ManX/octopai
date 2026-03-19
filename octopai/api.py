"""
Octopai High-Level API - Enhanced with Full-Lifecycle Engineering

This module provides a simplified, high-level API for working with Octopai,
now enhanced with the full-lifecycle skill creation and optimization framework.
"""

from typing import Optional, List, Union, Dict, Any, Tuple
from octopai.core.converter import URLConverter, convert_url_to_content
from octopai.core.resource_parser import (
    ResourceParser,
    ParsedResource,
    parse_resource,
    parse_to_skill_resource
)
from octopai.core.skill_factory import (
    SkillFactory,
    SkillDefinition,
    SkillMetadata,
    SkillVersion,
    SkillType,
    SkillQualityLevel
)
from octopai.core.skill_hub import (
    SkillHub, Skill, SkillStatus, SkillVisibility,
    SkillDependency, SkillRating, SkillCollection,
    ContextSlot, ContextComposition, VersionDiff, SearchIndex
)
from octopai.core.experience_tracker import ExperienceTracker
from octopai.core.skill_bank import (
    SkillBank, SkillType as BankSkillType, SkillPrinciple,
    BankedSkill, CommonMistake
)
from octopai.core.experience_distiller import (
    ExperienceDistiller, TrajectoryType, Trajectory, TrajectoryStep,
    ExtractedPattern, FailureLesson
)
from octopai.core.recursive_evolution import (
    RecursiveEvolutionEngine, EvolutionConfig, EvolutionTrigger,
    EvolutionStatus, EvolutionCycle, EvolutionProposal, ValidationResult
)
from octopai.core.skill_registry import (
    SkillRegistry, RegistrySkillMetadata, SkillRegistryStatus,
    RedirectType, SkillComment, SkillStar, SkillRedirect, SkillInstallRecord
)


class Octopai:
    """
    Octopai - High-level API for AI Agent skill development
    
    This class provides a unified interface for all Octopai functionality,
    now enhanced with full-lifecycle skill engineering.
    """
    
    def __init__(
        self,
        model_provider: str = "openrouter",
        model: str = "openai/gpt-5.4",
        api_key: Optional[str] = None,
        skill_hub_dir: str = "./SkillHub",
        skill_output_dir: str = "./skills",
        experience_dir: str = "./experiences",
        skill_bank_dir: str = "./SkillBank",
        distiller_dir: str = "./ExperienceDistiller",
        evolution_dir: str = "./RecursiveEvolution",
        registry_dir: str = "./SkillRegistry"
    ):
        """
        Initialize Octopai API
        
        Args:
            model_provider: Model provider to use
            model: Model name to use
            api_key: Optional API key (overrides environment variable)
            skill_hub_dir: Directory for SkillHub storage
            skill_output_dir: Directory for skill output
            experience_dir: Directory for experience tracking
            skill_bank_dir: Directory for SkillBank storage
            distiller_dir: Directory for ExperienceDistiller storage
            evolution_dir: Directory for RecursiveEvolutionEngine storage
            registry_dir: Directory for SkillRegistry storage
        """
        self.converter = URLConverter()
        self.skill_factory = SkillFactory()
        self.resource_parser = ResourceParser()
        self.skill_hub = SkillHub(skill_hub_dir)
        self.experience_tracker = ExperienceTracker(experience_dir)
        self.skill_bank = SkillBank(skill_bank_dir)
        self.experience_distiller = ExperienceDistiller(distiller_dir)
        self.recursive_evolution = RecursiveEvolutionEngine(evolution_dir)
        self.skill_registry = SkillRegistry(registry_dir)
        
        self.model_provider = model_provider
        self.model = model
        self.api_key = api_key
        self.skill_output_dir = skill_output_dir
    
    def convert_url(self, url: str) -> str:
        """
        Convert a web URL to structured content for skill creation
        
        Args:
            url: The URL to convert
            
        Returns:
            The converted content
        """
        return self.converter.convert(url)
    
    def parse_file(self, file_path: str) -> ParsedResource:
        """
        Parse a file and return structured resource
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            ParsedResource object
        """
        return self.resource_parser.parse(file_path)
    
    def parse_to_skill_resource(self, file_path: str) -> str:
        """
        Parse a file and convert directly to skill resource format
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            String in skill resource format
        """
        return self.resource_parser.parse_to_skill_resource(file_path)
    
    def parse_multiple_files(self, file_paths: List[str]) -> List[ParsedResource]:
        """
        Parse multiple files
        
        Args:
            file_paths: List of file paths to parse
            
        Returns:
            List of ParsedResource objects
        """
        return [self.parse_file(path) for path in file_paths]
    
    def create_from_url(
        self,
        url: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        auto_optimize: bool = True,
        target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
    ) -> SkillDefinition:
        """
        Create a skill from a URL with full-lifecycle engineering
        
        Args:
            url: The web URL to transform
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            auto_optimize: Whether to auto-optimize after creation
            target_quality: Target quality level for optimization
            
        Returns:
            Complete SkillDefinition ready for use
        """
        return self.skill_factory.create_from_url(
            url=url,
            name=name,
            description=description,
            tags=tags,
            category=category,
            author=author,
            skill_type=skill_type,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    
    def create_from_files(
        self,
        file_paths: List[str],
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        auto_optimize: bool = True,
        target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
    ) -> SkillDefinition:
        """
        Create a skill from one or more files with full-lifecycle engineering
        
        Args:
            file_paths: List of file paths to process
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            auto_optimize: Whether to auto-optimize after creation
            target_quality: Target quality level for optimization
            
        Returns:
            Complete SkillDefinition ready for use
        """
        return self.skill_factory.create_from_files(
            file_paths=file_paths,
            name=name,
            description=description,
            tags=tags,
            category=category,
            author=author,
            skill_type=skill_type,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    
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
        auto_optimize: bool = True,
        target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
    ) -> SkillDefinition:
        """
        Create a skill from a descriptive prompt with full-lifecycle engineering
        
        Args:
            prompt: Description of what the skill should do
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            resources: Optional list of resource files to include
            auto_optimize: Whether to auto-optimize after creation
            target_quality: Target quality level for optimization
            
        Returns:
            Complete SkillDefinition ready for use
        """
        return self.skill_factory.create_from_prompt(
            prompt=prompt,
            name=name,
            description=description,
            tags=tags,
            category=category,
            author=author,
            skill_type=skill_type,
            resources=resources,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    
    def create_from_text(
        self,
        text: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        auto_optimize: bool = True,
        target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
    ) -> SkillDefinition:
        """
        Create a skill from raw text content with full-lifecycle engineering
        
        Args:
            text: Raw text content to transform
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            auto_optimize: Whether to auto-optimize after creation
            target_quality: Target quality level for optimization
            
        Returns:
            Complete SkillDefinition ready for use
        """
        return self.skill_factory.create_from_text(
            text=text,
            name=name,
            description=description,
            tags=tags,
            category=category,
            author=author,
            skill_type=skill_type,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    
    def create_from_code(
        self,
        code: str,
        language: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        auto_optimize: bool = True,
        target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
    ) -> SkillDefinition:
        """
        Create a skill from code with full-lifecycle engineering
        
        Args:
            code: Source code to transform
            language: Programming language
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            auto_optimize: Whether to auto-optimize after creation
            target_quality: Target quality level for optimization
            
        Returns:
            Complete SkillDefinition ready for use
        """
        return self.skill_factory.create_from_code(
            code=code,
            language=language,
            name=name,
            description=description,
            tags=tags,
            category=category,
            author=author,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    
    def optimize_skill(
        self,
        skill_def: SkillDefinition,
        target_quality: SkillQualityLevel = SkillQualityLevel.EXCELLENT,
        author: Optional[str] = None
    ) -> SkillDefinition:
        """
        Optimize an existing skill
        
        Args:
            skill_def: Skill definition to optimize
            target_quality: Target quality level
            author: Optional author name
            
        Returns:
            Updated skill definition
        """
        return self.skill_factory.optimize_skill(
            skill_def=skill_def,
            target_quality=target_quality,
            author=author
        )
    
    def evaluate_skill(self, skill_def: SkillDefinition):
        """
        Evaluate a skill's quality
        
        Args:
            skill_def: Skill definition to evaluate
            
        Returns:
            Quality metrics
        """
        return self.skill_factory.evaluate_skill(skill_def)
    
    def create_skill_in_hub(
        self,
        name: str,
        description: str,
        prompt: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        resources: Optional[List[str]] = None,
        auto_optimize: bool = True,
        target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
    ) -> Skill:
        """
        Create a skill and store it in SkillHub
        
        Args:
            name: Skill name
            description: Skill description
            prompt: Description of what the skill should do
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            resources: Optional list of file paths to use as resources
            auto_optimize: Whether to auto-optimize
            target_quality: Target quality level
            
        Returns:
            Created Skill object
        """
        skill_def = self.create_from_prompt(
            prompt=prompt,
            name=name,
            description=description,
            tags=tags,
            category=category,
            author=author,
            resources=resources,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
        
        latest_version = skill_def.latest_version
        skill_content = latest_version.content if latest_version else ""
        
        return self.skill_hub.create_skill(
            name=name,
            description=description,
            content=skill_content,
            tags=tags,
            category=category,
            author=author
        )
    
    def get_skill_from_hub(self, skill_id: str) -> Optional[Skill]:
        """
        Get a skill from SkillHub by ID
        
        Args:
            skill_id: Skill ID to retrieve
            
        Returns:
            Skill object or None
        """
        return self.skill_hub.get_skill(skill_id)
    
    def update_skill_in_hub(
        self,
        skill_id: str,
        prompt: str,
        author: Optional[str] = None,
        change_description: Optional[str] = None
    ) -> Optional[Skill]:
        """
        Update a skill in SkillHub
        
        Args:
            skill_id: Skill ID to update
            prompt: New skill description or content
            author: Optional author name
            change_description: Description of changes
            
        Returns:
            Updated Skill object or None if not found
        """
        skill = self.skill_hub.get_skill(skill_id)
        if not skill:
            return None
        
        skill_def = self.create_from_prompt(
            prompt=prompt,
            name=skill.name,
            description=getattr(skill, 'description', ''),
            author=author
        )
        
        latest_version = skill_def.latest_version
        new_content = latest_version.content if latest_version else prompt
        
        return self.skill_hub.update_skill(
            skill_id=skill_id,
            content=new_content,
            author=author,
            change_description=change_description
        )
    
    def search_skills_in_hub(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[Skill]:
        """
        Search for skills in SkillHub
        
        Args:
            query: Search query
            tags: Optional tag filter
            category: Optional category filter
            limit: Maximum number of results
            
        Returns:
            List of matching Skill objects
        """
        return self.skill_hub.search_skills(query, tags, category, limit)
    
    def list_skills_in_hub(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[Skill]:
        """
        List skills in SkillHub
        
        Args:
            category: Optional category filter
            tags: Optional tag filter
            limit: Maximum number of results
            
        Returns:
            List of Skill objects
        """
        return self.skill_hub.list_skills(category, tags, limit)
    
    def record_skill_usage(self, skill_id: str, success: bool = True) -> bool:
        """
        Record skill usage in SkillHub and ExperienceTracker
        
        Args:
            skill_id: Skill ID
            success: Whether the usage was successful
            
        Returns:
            True if successful
        """
        self.experience_tracker.record_interaction(skill_id, success=success)
        return self.skill_hub.record_skill_usage(skill_id, success)
    
    def get_skill_experience(self, skill_id: str):
        """
        Get experience data for a skill
        
        Args:
            skill_id: Skill ID
            
        Returns:
            Skill experience data
        """
        return self.experience_tracker.get_skill_experience(skill_id)
    
    def get_experience_insights(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get experience insights
        
        Args:
            skill_id: Optional specific skill to analyze
            
        Returns:
            Dictionary of insights
        """
        return self.experience_tracker.get_insights(skill_id)
    
    def merge_skills_in_hub(
        self,
        skill_ids: List[str],
        new_name: str,
        new_description: str,
        author: Optional[str] = None
    ) -> Optional[Skill]:
        """
        Merge multiple skills in SkillHub
        
        Args:
            skill_ids: List of skill IDs to merge
            new_name: Name for merged skill
            new_description: Description for merged skill
            author: Optional author name
            
        Returns:
            Merged Skill object or None
        """
        return self.skill_hub.merge_skills(skill_ids, new_name, new_description, author)
    
    def get_skill_hub_stats(self) -> Dict[str, Any]:
        """
        Get SkillHub statistics
        
        Returns:
            Dictionary with statistics
        """
        return self.skill_hub.get_statistics()
    
    def update_skill_metadata_in_hub(
        self,
        skill_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        status: Optional[SkillStatus] = None,
        visibility: Optional[SkillVisibility] = None,
        author: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        dependencies: Optional[List[SkillDependency]] = None,
        related_skills: Optional[List[str]] = None,
        skill_type: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Optional[Skill]:
        """
        Update skill metadata in SkillHub
        
        Args:
            skill_id: Skill ID to update
            name: Optional new name
            description: Optional new description
            tags: Optional new tags
            category: Optional new category
            status: Optional new status
            visibility: Optional new visibility
            author: Optional new author
            keywords: Optional new keywords
            dependencies: Optional new dependencies
            related_skills: Optional related skills
            skill_type: Optional skill type
            custom_fields: Optional custom fields
            
        Returns:
            Updated Skill object or None if not found
        """
        return self.skill_hub.update_skill_metadata(
            skill_id=skill_id,
            name=name,
            description=description,
            tags=tags,
            category=category,
            status=status,
            visibility=visibility,
            author=author,
            keywords=keywords,
            dependencies=dependencies,
            related_skills=related_skills,
            skill_type=skill_type,
            custom_fields=custom_fields
        )
    
    def create_collection_in_hub(
        self,
        name: str,
        description: str,
        skill_ids: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        author: Optional[str] = None
    ) -> SkillCollection:
        """
        Create a skill collection in SkillHub
        
        Args:
            name: Collection name
            description: Collection description
            skill_ids: Optional list of skill IDs to include
            tags: Optional tags for the collection
            author: Optional author name
            
        Returns:
            Created SkillCollection object
        """
        return self.skill_hub.create_collection(name, description, skill_ids, tags, author)
    
    def add_skill_to_collection_in_hub(self, collection_id: str, skill_id: str) -> bool:
        """
        Add a skill to a collection in SkillHub
        
        Args:
            collection_id: Collection ID
            skill_id: Skill ID to add
            
        Returns:
            True if successful
        """
        return self.skill_hub.add_skill_to_collection(collection_id, skill_id)
    
    def remove_skill_from_collection_in_hub(self, collection_id: str, skill_id: str) -> bool:
        """
        Remove a skill from a collection in SkillHub
        
        Args:
            collection_id: Collection ID
            skill_id: Skill ID to remove
            
        Returns:
            True if successful
        """
        return self.skill_hub.remove_skill_from_collection(collection_id, skill_id)
    
    def get_collection_from_hub(self, collection_id: str) -> Optional[SkillCollection]:
        """
        Get a collection from SkillHub by ID
        
        Args:
            collection_id: Collection ID to retrieve
            
        Returns:
            SkillCollection object or None
        """
        return self.skill_hub.get_collection(collection_id)
    
    def list_collections_in_hub(self) -> List[SkillCollection]:
        """
        List all collections in SkillHub
        
        Returns:
            List of SkillCollection objects
        """
        return self.skill_hub.list_collections()
    
    def delete_collection_from_hub(self, collection_id: str) -> bool:
        """
        Delete a collection from SkillHub
        
        Args:
            collection_id: Collection ID to delete
            
        Returns:
            True if successful
        """
        return self.skill_hub.delete_collection(collection_id)
    
    def add_rating_to_skill_in_hub(
        self,
        skill_id: str,
        rating: float,
        feedback: Optional[str] = None,
        reviewer: Optional[str] = None
    ) -> Optional[SkillRating]:
        """
        Add a rating to a skill in SkillHub
        
        Args:
            skill_id: Skill ID
            rating: Rating value (0-5)
            feedback: Optional feedback text
            reviewer: Optional reviewer name
            
        Returns:
            Created SkillRating object or None
        """
        return self.skill_hub.add_rating(skill_id, rating, feedback, reviewer)
    
    def get_ratings_from_hub(self, skill_id: str) -> List[SkillRating]:
        """
        Get all ratings for a skill from SkillHub
        
        Args:
            skill_id: Skill ID
            
        Returns:
            List of SkillRating objects
        """
        return self.skill_hub.get_ratings(skill_id)
    
    def compute_version_diff_in_hub(
        self,
        skill_id: str,
        from_version: int,
        to_version: int
    ) -> Optional[VersionDiff]:
        """
        Compute difference between two skill versions in SkillHub
        
        Args:
            skill_id: Skill ID
            from_version: Source version number
            to_version: Target version number
            
        Returns:
            VersionDiff object or None
        """
        return self.skill_hub.compute_version_diff(skill_id, from_version, to_version)
    
    def rollback_skill_in_hub(
        self,
        skill_id: str,
        version: int,
        author: Optional[str] = None
    ) -> Optional[Skill]:
        """
        Rollback skill to a previous version in SkillHub
        
        Args:
            skill_id: Skill ID
            version: Version to rollback to
            author: Optional author name
            
        Returns:
            Updated Skill object or None
        """
        return self.skill_hub.rollback_to_version(skill_id, version, author)
    
    def publish_skill_in_hub(
        self,
        skill_id: str,
        visibility: SkillVisibility = SkillVisibility.PUBLIC
    ) -> Optional[Skill]:
        """
        Publish a skill in SkillHub
        
        Args:
            skill_id: Skill ID
            visibility: Visibility level
            
        Returns:
            Updated Skill object or None
        """
        return self.skill_hub.publish_skill(skill_id, visibility)
    
    def deprecate_skill_in_hub(self, skill_id: str) -> Optional[Skill]:
        """
        Deprecate a skill in SkillHub
        
        Args:
            skill_id: Skill ID
            
        Returns:
            Updated Skill object or None
        """
        return self.skill_hub.deprecate_skill(skill_id)
    
    def archive_skill_in_hub(self, skill_id: str) -> Optional[Skill]:
        """
        Archive a skill in SkillHub
        
        Args:
            skill_id: Skill ID
            
        Returns:
            Updated Skill object or None
        """
        return self.skill_hub.archive_skill(skill_id)
    
    def create_composition_in_hub(
        self,
        name: str,
        description: str,
        slots: Optional[Dict[str, ContextSlot]] = None
    ) -> ContextComposition:
        """
        Create a context composition in SkillHub
        
        Args:
            name: Composition name
            description: Composition description
            slots: Optional dictionary of slots
            
        Returns:
            Created ContextComposition object
        """
        return self.skill_hub.create_composition(name, description, slots)
    
    def add_slot_to_composition_in_hub(
        self,
        composition_id: str,
        slot: ContextSlot
    ) -> bool:
        """
        Add a slot to a composition in SkillHub
        
        Args:
            composition_id: Composition ID
            slot: Slot to add
            
        Returns:
            True if successful
        """
        return self.skill_hub.add_slot_to_composition(composition_id, slot)
    
    def bind_skill_to_slot_in_hub(
        self,
        composition_id: str,
        slot_id: str,
        skill_id: str
    ) -> bool:
        """
        Bind a skill to a composition slot in SkillHub
        
        Args:
            composition_id: Composition ID
            slot_id: Slot ID
            skill_id: Skill ID to bind
            
        Returns:
            True if successful
        """
        return self.skill_hub.bind_skill_to_slot(composition_id, slot_id, skill_id)
    
    def get_composition_from_hub(self, composition_id: str) -> Optional[ContextComposition]:
        """
        Get a composition from SkillHub by ID
        
        Args:
            composition_id: Composition ID to retrieve
            
        Returns:
            ContextComposition object or None
        """
        return self.skill_hub.get_composition(composition_id)
    
    def list_compositions_in_hub(self) -> List[ContextComposition]:
        """
        List all compositions in SkillHub
        
        Returns:
            List of ContextComposition objects
        """
        return self.skill_hub.list_compositions()
    
    def delete_composition_from_hub(self, composition_id: str) -> bool:
        """
        Delete a composition from SkillHub
        
        Args:
            composition_id: Composition ID to delete
            
        Returns:
            True if successful
        """
        return self.skill_hub.delete_composition(composition_id)
    
    def semantic_search_in_hub(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        status: Optional[SkillStatus] = None,
        limit: int = 20
    ) -> List[Tuple[Skill, float]]:
        """
        Enhanced semantic search using search index in SkillHub
        
        Args:
            query: Search query
            tags: Optional tag filter
            category: Optional category filter
            status: Optional status filter
            limit: Maximum results
            
        Returns:
            List of (Skill, score) tuples sorted by relevance
        """
        return self.skill_hub.semantic_search(query, tags, category, status, limit)
    
    def create_anything(
        self,
        source: Any,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        auto_optimize: bool = True,
        target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
    ) -> SkillDefinition:
        """
        Create a skill from ANYTHING - the core of 'Everything Can Be a Skill'
        
        Args:
            source: ANY source to transform into a skill
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            auto_optimize: Whether to auto-optimize after creation
            target_quality: Target quality level for optimization
            
        Returns:
            Complete SkillDefinition ready for use
        """
        return self.skill_factory.create_anything(
            source=source,
            name=name,
            description=description,
            tags=tags,
            category=category,
            author=author,
            skill_type=skill_type,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    
    def add_general_skill_to_bank(
        self,
        name: str,
        description: str,
        content: str,
        tags: Optional[List[str]] = None,
        principles: Optional[List[str]] = None
    ) -> BankedSkill:
        """
        Add a general skill to the SkillBank
        
        Args:
            name: Skill name
            description: Skill description
            content: Skill content
            tags: Optional tags
            principles: Optional skill principles
            
        Returns:
            Created BankedSkill object
        """
        return self.skill_bank.add_general_skill(
            name=name,
            description=description,
            content=content,
            tags=tags,
            principles=principles
        )
    
    def add_task_specific_skill_to_bank(
        self,
        name: str,
        description: str,
        content: str,
        task_domain: str,
        tags: Optional[List[str]] = None,
        principles: Optional[List[str]] = None
    ) -> BankedSkill:
        """
        Add a task-specific skill to the SkillBank
        
        Args:
            name: Skill name
            description: Skill description
            content: Skill content
            task_domain: Task domain this skill applies to
            tags: Optional tags
            principles: Optional skill principles
            
        Returns:
            Created BankedSkill object
        """
        return self.skill_bank.add_task_specific_skill(
            name=name,
            description=description,
            content=content,
            task_domain=task_domain,
            tags=tags,
            principles=principles
        )
    
    def add_common_mistake(
        self,
        mistake_id: str,
        description: str,
        avoid_instruction: str,
        related_skill_ids: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> CommonMistake:
        """
        Add a common mistake to the SkillBank
        
        Args:
            mistake_id: Unique mistake ID
            description: Description of the mistake
            avoid_instruction: Instruction to avoid the mistake
            related_skill_ids: Optional related skill IDs
            tags: Optional tags
            
        Returns:
            Created CommonMistake object
        """
        return self.skill_bank.add_common_mistake(
            mistake_id=mistake_id,
            description=description,
            avoid_instruction=avoid_instruction,
            related_skill_ids=related_skill_ids,
            tags=tags
        )
    
    def get_skill_injection_context(
        self,
        task_context: Optional[str] = None,
        skill_ids: Optional[List[str]] = None,
        include_general: bool = True,
        include_mistakes: bool = True,
        task_domain: Optional[str] = None,
        max_tokens: int = 4000
    ) -> str:
        """
        Get skill injection context for agent prompts
        
        Args:
            task_context: Optional task context
            skill_ids: Optional specific skill IDs to include
            include_general: Whether to include general skills
            include_mistakes: Whether to include common mistakes
            task_domain: Optional task domain for filtering
            max_tokens: Maximum tokens for the context
            
        Returns:
            Formatted context string
        """
        return self.skill_bank.format_skill_injection(
            task_context=task_context,
            skill_ids=skill_ids,
            include_general=include_general,
            include_mistakes=include_mistakes,
            task_domain=task_domain,
            max_tokens=max_tokens
        )
    
    def record_trajectory_step(
        self,
        trajectory_id: str,
        step_number: int,
        action: str,
        observation: str,
        reasoning: Optional[str] = None,
        decision_outcome: Optional[str] = None
    ) -> TrajectoryStep:
        """
        Record a step in a trajectory
        
        Args:
            trajectory_id: Trajectory ID
            step_number: Step number
            action: Action taken
            observation: Observation after action
            reasoning: Optional reasoning
            decision_outcome: Optional decision outcome
            
        Returns:
            Created TrajectoryStep object
        """
        return self.experience_distiller.record_step(
            trajectory_id=trajectory_id,
            step_number=step_number,
            action=action,
            observation=observation,
            reasoning=reasoning,
            decision_outcome=decision_outcome
        )
    
    def finalize_trajectory(
        self,
        trajectory_id: str,
        trajectory_type: TrajectoryType,
        overall_success: bool,
        task_completion: Optional[str] = None,
        lessons_learned: Optional[str] = None
    ) -> Trajectory:
        """
        Finalize a trajectory for distillation
        
        Args:
            trajectory_id: Trajectory ID
            trajectory_type: Type of trajectory
            overall_success: Whether overall successful
            task_completion: Optional task completion description
            lessons_learned: Optional lessons learned
            
        Returns:
            Finalized Trajectory object
        """
        return self.experience_distiller.finalize_trajectory(
            trajectory_id=trajectory_id,
            trajectory_type=trajectory_type,
            overall_success=overall_success,
            task_completion=task_completion,
            lessons_learned=lessons_learned
        )
    
    def distill_success_patterns(
        self,
        trajectory_id: Optional[str] = None,
        min_success_rate: float = 0.7,
        max_patterns: int = 5
    ) -> List[ExtractedPattern]:
        """
        Distill success patterns from trajectories
        
        Args:
            trajectory_id: Optional specific trajectory ID
            min_success_rate: Minimum success rate threshold
            max_patterns: Maximum patterns to extract
            
        Returns:
            List of ExtractedPattern objects
        """
        return self.experience_distiller.distill_success_patterns(
            trajectory_id=trajectory_id,
            min_success_rate=min_success_rate,
            max_patterns=max_patterns
        )
    
    def extract_failure_lessons(
        self,
        trajectory_id: Optional[str] = None,
        max_lessons: int = 5
    ) -> List[FailureLesson]:
        """
        Extract lessons from failed trajectories
        
        Args:
            trajectory_id: Optional specific trajectory ID
            max_lessons: Maximum lessons to extract
            
        Returns:
            List of FailureLesson objects
        """
        return self.experience_distiller.extract_failure_lessons(
            trajectory_id=trajectory_id,
            max_lessons=max_lessons
        )
    
    def record_skill_performance_for_evolution(
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
        self.recursive_evolution.record_skill_performance(
            skill_id=skill_id,
            version=version,
            success=success,
            performance_metrics=performance_metrics,
            context=context
        )
    
    def trigger_skill_evolution(
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
        return self.recursive_evolution.trigger_evolution(
            skill_id=skill_id,
            trigger=trigger,
            current_version=current_version,
            rationale=rationale
        )
    
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
        return self.recursive_evolution.get_skill_performance_trend(
            skill_id=skill_id,
            version=version
        )
    
    def get_evolution_statistics(self) -> Dict[str, Any]:
        """
        Get evolution engine statistics
        
        Returns:
            Statistics dictionary
        """
        return self.recursive_evolution.get_statistics()
    
    def publish_skill_to_registry(
        self,
        name: str,
        description: str,
        version: str,
        author: str,
        owner_id: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        visibility: str = "public",
        license: str = "MIT",
        changelog_entry: Optional[str] = None
    ) -> RegistrySkillMetadata:
        """
        Publish a new skill to the registry
        
        Args:
            name: Skill name
            description: Skill description
            version: Semantic version
            author: Author name
            owner_id: Owner ID
            tags: Optional tags
            category: Optional category
            visibility: Visibility level
            license: License type
            changelog_entry: Optional changelog entry
            
        Returns:
            Created RegistrySkillMetadata
        """
        return self.skill_registry.publish_skill(
            name=name,
            description=description,
            version=version,
            author=author,
            owner_id=owner_id,
            tags=tags,
            category=category,
            visibility=visibility,
            license=license,
            changelog_entry=changelog_entry
        )
    
    def get_registry_skill_by_slug(self, slug: str) -> Optional[RegistrySkillMetadata]:
        """
        Get a skill from the registry by slug, following redirects
        
        Args:
            slug: Skill slug
            
        Returns:
            RegistrySkillMetadata or None
        """
        return self.skill_registry.get_skill_by_slug(slug)
    
    def get_registry_skill_by_id(self, skill_id: str) -> Optional[RegistrySkillMetadata]:
        """
        Get a skill from the registry by ID
        
        Args:
            skill_id: Skill ID
            
        Returns:
            RegistrySkillMetadata or None
        """
        return self.skill_registry.get_skill_by_id(skill_id)
    
    def update_registry_skill_version(
        self,
        skill_id: str,
        new_version: str,
        changelog_entry: str,
        user_id: str
    ) -> Optional[RegistrySkillMetadata]:
        """
        Update a registry skill's version
        
        Args:
            skill_id: Skill ID
            new_version: New version string
            changelog_entry: Description of changes
            user_id: User making the update
            
        Returns:
            Updated RegistrySkillMetadata or None
        """
        return self.skill_registry.update_skill_version(
            skill_id=skill_id,
            new_version=new_version,
            changelog_entry=changelog_entry,
            user_id=user_id
        )
    
    def rename_registry_skill(
        self,
        skill_id: str,
        new_name: str,
        user_id: str
    ) -> Optional[RegistrySkillMetadata]:
        """
        Rename a registry skill without breaking old links
        
        Args:
            skill_id: Skill ID
            new_name: New skill name
            user_id: User making the change
            
        Returns:
            Updated RegistrySkillMetadata or None
        """
        return self.skill_registry.rename_skill(
            skill_id=skill_id,
            new_name=new_name,
            user_id=user_id
        )
    
    def merge_registry_skills(
        self,
        source_slug: str,
        target_slug: str,
        user_id: str
    ) -> bool:
        """
        Merge a source skill into a target skill
        
        Args:
            source_slug: Source skill slug (will be hidden)
            target_slug: Target skill slug (canonical)
            user_id: User performing the merge
            
        Returns:
            True if successful
        """
        return self.skill_registry.merge_skills(
            source_slug=source_slug,
            target_slug=target_slug,
            user_id=user_id
        )
    
    def soft_delete_registry_skill(self, skill_id: str, user_id: str) -> bool:
        """
        Soft delete a registry skill (can be restored)
        
        Args:
            skill_id: Skill ID
            user_id: User performing the delete
            
        Returns:
            True if successful
        """
        return self.skill_registry.soft_delete_skill(skill_id, user_id)
    
    def restore_registry_skill(self, skill_id: str, user_id: str) -> bool:
        """
        Restore a soft-deleted registry skill
        
        Args:
            skill_id: Skill ID
            user_id: User performing the restore
            
        Returns:
            True if successful
        """
        return self.skill_registry.restore_skill(skill_id, user_id)
    
    def star_registry_skill(
        self,
        skill_id: str,
        user_id: str,
        rating: float
    ) -> SkillStar:
        """
        Star/rate a registry skill
        
        Args:
            skill_id: Skill ID
            user_id: User ID
            rating: Rating (0-5)
            
        Returns:
            Created SkillStar
        """
        return self.skill_registry.star_skill(skill_id, user_id, rating)
    
    def add_comment_to_registry_skill(
        self,
        skill_id: str,
        author: str,
        content: str
    ) -> SkillComment:
        """
        Add a comment to a registry skill
        
        Args:
            skill_id: Skill ID
            author: Author name
            content: Comment content
            
        Returns:
            Created SkillComment
        """
        return self.skill_registry.add_comment(skill_id, author, content)
    
    def record_registry_skill_install(
        self,
        skill_id: str,
        slug: str,
        version: str,
        installed_by: str,
        is_local: bool = True
    ) -> SkillInstallRecord:
        """
        Record a registry skill installation
        
        Args:
            skill_id: Skill ID
            slug: Skill slug
            version: Version installed
            installed_by: User who installed
            is_local: Whether it's a local install
            
        Returns:
            Created SkillInstallRecord
        """
        return self.skill_registry.record_install(
            skill_id=skill_id,
            slug=slug,
            version=version,
            installed_by=installed_by,
            is_local=is_local
        )
    
    def search_registry_skills(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        visibility: Optional[str] = None,
        sort_by: str = "popular",
        limit: int = 20
    ) -> List[RegistrySkillMetadata]:
        """
        Search for skills in the registry
        
        Args:
            query: Optional search query
            tags: Optional tag filter
            category: Optional category filter
            visibility: Optional visibility filter
            sort_by: Sort method ('popular', 'recent', 'rating', 'name')
            limit: Maximum results
            
        Returns:
            List of matching RegistrySkillMetadata
        """
        return self.skill_registry.search_skills(
            query=query,
            tags=tags,
            category=category,
            visibility=visibility,
            sort_by=sort_by,
            limit=limit
        )
    
    def get_popular_registry_skills(self, limit: int = 10) -> List[RegistrySkillMetadata]:
        """
        Get popular skills from the registry by install count
        
        Args:
            limit: Maximum results
            
        Returns:
            List of RegistrySkillMetadata
        """
        return self.skill_registry.get_popular_skills(limit)
    
    def get_registry_statistics(self) -> Dict[str, Any]:
        """
        Get registry statistics
        
        Returns:
            Statistics dictionary
        """
        return self.skill_registry.get_statistics()


def create_from_url(
    url: str,
    name: str,
    description: str,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    author: Optional[str] = None,
    skill_type: SkillType = SkillType.GENERAL,
    auto_optimize: bool = True,
    target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
) -> SkillDefinition:
    """
    Convenience function to create a skill from a URL
    
    Args:
        url: The web URL to transform
        name: Name for the skill
        description: Description of the skill
        tags: Optional tags for categorization
        category: Optional category
        author: Optional author name
        skill_type: Type of skill being created
        auto_optimize: Whether to auto-optimize after creation
        target_quality: Target quality level for optimization
        
    Returns:
        Complete SkillDefinition ready for use
    
    Example:
        >>> from octopai import create_from_url
        >>> skill = create_from_url(
        ...     url="https://example.com",
        ...     name="Web Analysis",
        ...     description="Analyze web content"
        ... )
    """
    try:
        octopai = Octopai()
        return octopai.create_from_url(
            url=url,
            name=name,
            description=description,
            tags=tags,
            category=category,
            author=author,
            skill_type=skill_type,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    except Exception as e:
        raise ValueError(f"Error creating skill from URL: {str(e)}")


def create_from_files(
    file_paths: List[str],
    name: str,
    description: str,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    author: Optional[str] = None,
    skill_type: SkillType = SkillType.GENERAL,
    auto_optimize: bool = True,
    target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
) -> SkillDefinition:
    """
    Convenience function to create a skill from files
    
    Args:
        file_paths: List of file paths to process
        name: Name for the skill
        description: Description of the skill
        tags: Optional tags for categorization
        category: Optional category
        author: Optional author name
        skill_type: Type of skill being created
        auto_optimize: Whether to auto-optimize after creation
        target_quality: Target quality level for optimization
        
    Returns:
        Complete SkillDefinition ready for use
    
    Example:
        >>> from octopai import create_from_files
        >>> skill = create_from_files(
        ...     file_paths=["data.csv", "reference.pdf"],
        ...     name="Data Processor",
        ...     description="Process structured data"
        ... )
    """
    try:
        # Validate file paths
        for path in file_paths:
            if not os.path.exists(path):
                raise ValueError(f"File not found: {path}")
        
        octopai = Octopai()
        return octopai.create_from_files(
            file_paths=file_paths,
            name=name,
            description=description,
            tags=tags,
            category=category,
            author=author,
            skill_type=skill_type,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    except Exception as e:
        raise ValueError(f"Error creating skill from files: {str(e)}")


def create_from_prompt(
    prompt: str,
    name: str,
    description: str,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    author: Optional[str] = None,
    skill_type: SkillType = SkillType.GENERAL,
    resources: Optional[List[str]] = None,
    auto_optimize: bool = True,
    target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
) -> SkillDefinition:
    """
    Convenience function to create a skill from a prompt
    
    Args:
        prompt: Description of what the skill should do
        name: Name for the skill
        description: Description of the skill
        tags: Optional tags for categorization
        category: Optional category
        author: Optional author name
        skill_type: Type of skill being created
        resources: Optional list of resource files to include
        auto_optimize: Whether to auto-optimize after creation
        target_quality: Target quality level for optimization
        
    Returns:
        Complete SkillDefinition ready for use
    
    Example:
        >>> from octopai import create_from_prompt
        >>> skill = create_from_prompt(
        ...     prompt="Create a skill to generate reports",
        ...     name="Report Generator",
        ...     description="Generate comprehensive reports"
        ... )
    """
    try:
        # Validate resources if provided
        if resources:
            for path in resources:
                if not os.path.exists(path):
                    raise ValueError(f"Resource file not found: {path}")
        
        octopai = Octopai()
        return octopai.create_from_prompt(
            prompt=prompt,
            name=name,
            description=description,
            tags=tags,
            category=category,
            author=author,
            skill_type=skill_type,
            resources=resources,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    except Exception as e:
        raise ValueError(f"Error creating skill from prompt: {str(e)}")


def optimize_skill(
    skill_def: SkillDefinition,
    target_quality: SkillQualityLevel = SkillQualityLevel.EXCELLENT,
    author: Optional[str] = None
) -> SkillDefinition:
    """
    Convenience function to optimize a skill
    
    Args:
        skill_def: Skill definition to optimize
        target_quality: Target quality level
        author: Optional author name
        
    Returns:
        Updated skill definition
    """
    octopai = Octopai()
    return octopai.optimize_skill(skill_def, target_quality, author)


def convert(url: str) -> str:
    """
    Convenience function to convert a URL to content
    
    Args:
        url: The URL to convert
        
    Returns:
        The converted content
    """
    octopai = Octopai()
    return octopai.convert_url(url)


def parse(file_path: str) -> ParsedResource:
    """
    Convenience function to parse a file
    
    Args:
        file_path: Path to the file
        
    Returns:
        ParsedResource
    """
    octopai = Octopai()
    return octopai.parse_file(file_path)


def hub_create(
    name: str,
    description: str,
    prompt: str,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    author: Optional[str] = None,
    resources: Optional[List[str]] = None,
    auto_optimize: bool = True,
    target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
) -> Skill:
    """
    Convenience function to create a skill in SkillHub
    
    Args:
        name: Skill name
        description: Skill description
        prompt: Description of what the skill should do
        tags: Optional tags for categorization
        category: Optional category
        author: Optional author name
        resources: Optional list of file paths to use as resources
        auto_optimize: Whether to auto-optimize
        target_quality: Target quality level
        
    Returns:
        Created Skill object
    """
    octopai = Octopai()
    return octopai.create_skill_in_hub(
        name, description, prompt, tags, category, author, resources,
        auto_optimize, target_quality
    )


def hub_get(skill_id: str) -> Optional[Skill]:
    """
    Convenience function to get a skill from SkillHub
    
    Args:
        skill_id: Skill ID to retrieve
        
    Returns:
        Skill object or None
    """
    octopai = Octopai()
    return octopai.get_skill_from_hub(skill_id)


def hub_search(
    query: str,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    limit: int = 10
) -> List[Skill]:
    """
    Convenience function to search skills in SkillHub
    
    Args:
        query: Search query
        tags: Optional tag filter
        category: Optional category filter
        limit: Maximum number of results
        
    Returns:
        List of matching Skill objects
    """
    octopai = Octopai()
    return octopai.search_skills_in_hub(query, tags, category, limit)


def hub_list(
    category: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: int = 100
) -> List[Skill]:
    """
    Convenience function to list skills in SkillHub
    
    Args:
        category: Optional category filter
        tags: Optional tag filter
        limit: Maximum number of results
        
    Returns:
        List of Skill objects
    """
    octopai = Octopai()
    return octopai.list_skills_in_hub(category, tags, limit)


def hub_stats() -> Dict[str, Any]:
    """
    Convenience function to get SkillHub statistics
    
    Returns:
        Dictionary with statistics
    """
    octopai = Octopai()
    return octopai.get_skill_hub_stats()


def get_insights(skill_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to get experience insights
    
    Args:
        skill_id: Optional specific skill to analyze
        
    Returns:
        Dictionary of insights
    """
    octopai = Octopai()
    return octopai.get_experience_insights(skill_id)


def hub_update_metadata(
    skill_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    status: Optional[SkillStatus] = None,
    visibility: Optional[SkillVisibility] = None,
    author: Optional[str] = None,
    keywords: Optional[List[str]] = None,
    dependencies: Optional[List[SkillDependency]] = None,
    related_skills: Optional[List[str]] = None,
    skill_type: Optional[str] = None,
    custom_fields: Optional[Dict[str, Any]] = None
) -> Optional[Skill]:
    """
    Convenience function to update skill metadata in SkillHub
    """
    octopai = Octopai()
    return octopai.update_skill_metadata_in_hub(
        skill_id, name, description, tags, category, status, visibility,
        author, keywords, dependencies, related_skills, skill_type, custom_fields
    )


def hub_create_collection(
    name: str,
    description: str,
    skill_ids: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    author: Optional[str] = None
) -> SkillCollection:
    """
    Convenience function to create a skill collection in SkillHub
    """
    octopai = Octopai()
    return octopai.create_collection_in_hub(name, description, skill_ids, tags, author)


def hub_add_to_collection(collection_id: str, skill_id: str) -> bool:
    """
    Convenience function to add a skill to a collection in SkillHub
    """
    octopai = Octopai()
    return octopai.add_skill_to_collection_in_hub(collection_id, skill_id)


def hub_remove_from_collection(collection_id: str, skill_id: str) -> bool:
    """
    Convenience function to remove a skill from a collection in SkillHub
    """
    octopai = Octopai()
    return octopai.remove_skill_from_collection_in_hub(collection_id, skill_id)


def hub_get_collection(collection_id: str) -> Optional[SkillCollection]:
    """
    Convenience function to get a collection from SkillHub
    """
    octopai = Octopai()
    return octopai.get_collection_from_hub(collection_id)


def hub_list_collections() -> List[SkillCollection]:
    """
    Convenience function to list all collections in SkillHub
    """
    octopai = Octopai()
    return octopai.list_collections_in_hub()


def hub_delete_collection(collection_id: str) -> bool:
    """
    Convenience function to delete a collection from SkillHub
    """
    octopai = Octopai()
    return octopai.delete_collection_from_hub(collection_id)


def hub_add_rating(
    skill_id: str,
    rating: float,
    feedback: Optional[str] = None,
    reviewer: Optional[str] = None
) -> Optional[SkillRating]:
    """
    Convenience function to add a rating to a skill in SkillHub
    """
    octopai = Octopai()
    return octopai.add_rating_to_skill_in_hub(skill_id, rating, feedback, reviewer)


def hub_get_ratings(skill_id: str) -> List[SkillRating]:
    """
    Convenience function to get all ratings for a skill from SkillHub
    """
    octopai = Octopai()
    return octopai.get_ratings_from_hub(skill_id)


def hub_compute_diff(
    skill_id: str,
    from_version: int,
    to_version: int
) -> Optional[VersionDiff]:
    """
    Convenience function to compute version difference in SkillHub
    """
    octopai = Octopai()
    return octopai.compute_version_diff_in_hub(skill_id, from_version, to_version)


def hub_rollback(
    skill_id: str,
    version: int,
    author: Optional[str] = None
) -> Optional[Skill]:
    """
    Convenience function to rollback a skill in SkillHub
    """
    octopai = Octopai()
    return octopai.rollback_skill_in_hub(skill_id, version, author)


def hub_publish(
    skill_id: str,
    visibility: SkillVisibility = SkillVisibility.PUBLIC
) -> Optional[Skill]:
    """
    Convenience function to publish a skill in SkillHub
    """
    octopai = Octopai()
    return octopai.publish_skill_in_hub(skill_id, visibility)


def hub_deprecate(skill_id: str) -> Optional[Skill]:
    """
    Convenience function to deprecate a skill in SkillHub
    """
    octopai = Octopai()
    return octopai.deprecate_skill_in_hub(skill_id)


def hub_archive(skill_id: str) -> Optional[Skill]:
    """
    Convenience function to archive a skill in SkillHub
    """
    octopai = Octopai()
    return octopai.archive_skill_in_hub(skill_id)


def hub_create_composition(
    name: str,
    description: str,
    slots: Optional[Dict[str, ContextSlot]] = None
) -> ContextComposition:
    """
    Convenience function to create a context composition in SkillHub
    """
    octopai = Octopai()
    return octopai.create_composition_in_hub(name, description, slots)


def hub_add_slot(
    composition_id: str,
    slot: ContextSlot
) -> bool:
    """
    Convenience function to add a slot to a composition in SkillHub
    """
    octopai = Octopai()
    return octopai.add_slot_to_composition_in_hub(composition_id, slot)


def hub_bind_skill(
    composition_id: str,
    slot_id: str,
    skill_id: str
) -> bool:
    """
    Convenience function to bind a skill to a slot in SkillHub
    """
    octopai = Octopai()
    return octopai.bind_skill_to_slot_in_hub(composition_id, slot_id, skill_id)


def hub_get_composition(composition_id: str) -> Optional[ContextComposition]:
    """
    Convenience function to get a composition from SkillHub
    """
    octopai = Octopai()
    return octopai.get_composition_from_hub(composition_id)


def hub_list_compositions() -> List[ContextComposition]:
    """
    Convenience function to list all compositions in SkillHub
    """
    octopai = Octopai()
    return octopai.list_compositions_in_hub()


def hub_delete_composition(composition_id: str) -> bool:
    """
    Convenience function to delete a composition from SkillHub
    """
    octopai = Octopai()
    return octopai.delete_composition_from_hub(composition_id)


def hub_semantic_search(
    query: str,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    status: Optional[SkillStatus] = None,
    limit: int = 20
) -> List[Tuple[Skill, float]]:
    """
    Convenience function for semantic search in SkillHub
    """
    octopai = Octopai()
    return octopai.semantic_search_in_hub(query, tags, category, status, limit)
