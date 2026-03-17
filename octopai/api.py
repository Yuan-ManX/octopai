"""
Octopai High-Level API - Enhanced with Full-Lifecycle Engineering

This module provides a simplified, high-level API for working with Octopai,
now enhanced with the full-lifecycle skill creation and optimization framework.
"""

from typing import Optional, List, Union, Dict, Any
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
from octopai.core.skill_hub import SkillHub, Skill
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
