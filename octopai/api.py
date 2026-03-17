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
        experience_dir: str = "./experiences"
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
        """
        self.converter = URLConverter()
        self.skill_factory = SkillFactory()
        self.resource_parser = ResourceParser()
        self.skill_hub = SkillHub(skill_hub_dir)
        self.experience_tracker = ExperienceTracker(experience_dir)
        
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
    """
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
    """
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
    """
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
