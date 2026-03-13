"""
EXO High-Level API

This module provides a simplified, high-level API for working with EXO.
"""

from typing import Optional, List, Union, Dict, Any
from exo.core.converter import URLConverter
from exo.core.creator import SkillCreator
from exo.core.evolver import SkillEvolver
from exo.core.resource_parser import (
    ResourceParser,
    ParsedResource,
    parse_resource,
    parse_to_skill_resource
)
from exo.core.skill_hub import SkillHub, Skill


class EXO:
    """
    EXO - High-level API for AI Agent skill development
    
    This class provides a unified interface for all EXO functionality.
    """
    
    def __init__(self, model_provider: str = "openrouter", model: str = "openai/gpt-5.4", api_key: Optional[str] = None, skill_hub_dir: str = "./SkillHub"):
        """
        Initialize EXO API
        
        Args:
            model_provider: Model provider to use
            model: Model name to use
            api_key: Optional API key (overrides environment variable)
            skill_hub_dir: Directory for SkillHub storage
        """
        self.converter = URLConverter()
        self.creator = SkillCreator()
        self.evolver = SkillEvolver()
        self.resource_parser = ResourceParser()
        self.skill_hub = SkillHub(skill_hub_dir)
        self.model_provider = model_provider
        self.model = model
        self.api_key = api_key
    
    def convert_url(self, url: str, output_path: Optional[str] = None, use_crawler: bool = False) -> str:
        """
        Convert a web URL to Markdown format
        
        Args:
            url: The URL to convert
            output_path: Optional path to save the output file
            use_crawler: Whether to also download web resources
            
        Returns:
            The converted Markdown content
        """
        return self.converter.convert(url, output_path, use_crawler)
    
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
    
    def create_skill(self, prompt: str, name: Optional[str] = None, output_path: Optional[str] = None, resources: Optional[List[str]] = None) -> str:
        """
        Create a new skill using LLM
        
        Args:
            prompt: Description of what the skill should do
            name: Optional name for the skill
            output_path: Optional path to save the skill file
            resources: Optional list of file paths to use as resources
            
        Returns:
            The generated skill content
        """
        enhanced_prompt = prompt
        
        if resources:
            resource_contents = []
            for res_path in resources:
                try:
                    res_content = self.parse_to_skill_resource(res_path)
                    resource_contents.append(f"\n--- Resource: {res_path} ---\n{res_content}")
                except Exception as e:
                    resource_contents.append(f"\n--- Resource: {res_path} ---\nError parsing: {str(e)}")
            
            if resource_contents:
                enhanced_prompt = f"{prompt}\n\nAdditional Resources:\n{' '.join(resource_contents)}"
        
        return self.creator.create(enhanced_prompt, name, output_path)
    
    def evolve_skill(self, skill_path: str, prompt: str, use_engine: bool = True, iterations: int = 3) -> str:
        """
        Evolve and improve an existing skill
        
        Args:
            skill_path: Path to the skill file
            prompt: Evolution instructions or feedback
            use_engine: Whether to use the advanced evolution engine
            iterations: Number of evolution iterations
            
        Returns:
            The evolved skill content
        """
        return self.evolver.evolve(skill_path, prompt, use_engine, iterations)
    
    def create_skill_in_hub(
        self,
        name: str,
        description: str,
        prompt: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        resources: Optional[List[str]] = None
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
            
        Returns:
            Created Skill object
        """
        skill_content = self.create_skill(prompt, name=name, resources=resources)
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
        
        new_content = self.create_skill(prompt, name=skill.metadata.name)
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
        Record skill usage in SkillHub
        
        Args:
            skill_id: Skill ID
            success: Whether the usage was successful
            
        Returns:
            True if successful
        """
        return self.skill_hub.record_skill_usage(skill_id, success)
    
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
    
    def process(self, input_data: Union[str, List[str]], operation: str = "convert", **kwargs) -> Union[str, List[str], ParsedResource, List[ParsedResource], Skill, List[Skill]]:
        """
        Generic method for any EXO operation
        
        Args:
            input_data: The input data to process
            operation: The operation to perform ('convert', 'parse', 'create', 'evolve', 'hub_create', 'hub_search', 'hub_list')
            **kwargs: Additional operation-specific parameters
            
        Returns:
            The result of the operation
        """
        if operation == "convert":
            return self.convert_url(input_data, **kwargs)
        elif operation == "parse":
            if isinstance(input_data, list):
                return self.parse_multiple_files(input_data)
            return self.parse_file(input_data)
        elif operation == "create":
            return self.create_skill(input_data, **kwargs)
        elif operation == "evolve":
            return self.evolve_skill(input_data, **kwargs)
        elif operation == "hub_create":
            return self.create_skill_in_hub(**kwargs)
        elif operation == "hub_search":
            return self.search_skills_in_hub(input_data, **kwargs)
        elif operation == "hub_list":
            return self.list_skills_in_hub(**kwargs)
        else:
            raise ValueError(f"Unknown operation: {operation}")


def convert(url: str, output_path: Optional[str] = None, use_crawler: bool = False) -> str:
    """
    Convenience function to convert a URL to Markdown
    
    Args:
        url: The URL to convert
        output_path: Optional path to save the output file
        use_crawler: Whether to also download web resources
        
    Returns:
        The converted Markdown content
    """
    exo = EXO()
    return exo.convert_url(url, output_path, use_crawler)


def parse(file_path: str) -> ParsedResource:
    """
    Convenience function to parse a file
    
    Args:
        file_path: Path to the file
        
    Returns:
        ParsedResource
    """
    exo = EXO()
    return exo.parse_file(file_path)


def create(prompt: str, name: Optional[str] = None, output_path: Optional[str] = None, resources: Optional[List[str]] = None) -> str:
    """
    Convenience function to create a skill
    
    Args:
        prompt: Description of what the skill should do
        name: Optional name for the skill
        output_path: Optional path to save the skill file
        resources: Optional list of file paths to use as resources
        
    Returns:
        The generated skill content
    """
    exo = EXO()
    return exo.create_skill(prompt, name, output_path, resources)


def evolve(skill_path: str, prompt: str, use_engine: bool = True, iterations: int = 3) -> str:
    """
    Convenience function to evolve a skill
    
    Args:
        skill_path: Path to the skill file
        prompt: Evolution instructions or feedback
        use_engine: Whether to use the advanced evolution engine
        iterations: Number of evolution iterations
        
    Returns:
        The evolved skill content
    """
    exo = EXO()
    return exo.evolve_skill(skill_path, prompt, use_engine, iterations)


def process(input_data: Union[str, List[str]], operation: str = "convert", **kwargs) -> Union[str, List[str], ParsedResource, List[ParsedResource], Skill, List[Skill]]:
    """
    Convenience function for any EXO operation
    
    Args:
        input_data: The input data to process
        operation: The operation to perform
        **kwargs: Additional operation-specific parameters
        
    Returns:
        The result of the operation
    """
    exo = EXO()
    return exo.process(input_data, operation, **kwargs)


def hub_create(
    name: str,
    description: str,
    prompt: str,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    author: Optional[str] = None,
    resources: Optional[List[str]] = None
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
        
    Returns:
        Created Skill object
    """
    exo = EXO()
    return exo.create_skill_in_hub(name, description, prompt, tags, category, author, resources)


def hub_get(skill_id: str) -> Optional[Skill]:
    """
    Convenience function to get a skill from SkillHub
    
    Args:
        skill_id: Skill ID to retrieve
        
    Returns:
        Skill object or None
    """
    exo = EXO()
    return exo.get_skill_from_hub(skill_id)


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
    exo = EXO()
    return exo.search_skills_in_hub(query, tags, category, limit)


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
    exo = EXO()
    return exo.list_skills_in_hub(category, tags, limit)


def hub_stats() -> Dict[str, Any]:
    """
    Convenience function to get SkillHub statistics
    
    Returns:
        Dictionary with statistics
    """
    exo = EXO()
    return exo.get_skill_hub_stats()
