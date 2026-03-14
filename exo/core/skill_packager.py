"""
Skill Packager - EXO's Standardized Skill Packaging System

This module provides EXO's proprietary skill packaging system that
creates standardized, versioned skill packages ready for distribution
and use by AI Agents.
"""

import os
import yaml
import shutil
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

from exo.utils.helpers import read_file, write_file


@dataclass
class PackageConfig:
    """Configuration for skill packaging"""
    include_scripts: bool = True
    include_assets: bool = True
    include_references: bool = True
    include_agents: bool = False
    generate_readme: bool = True
    generate_changelog: bool = True


class SkillPackager:
    """
    EXO's Skill Packager - Standardized Skill Packaging System
    
    Creates professional, standardized skill packages in EXO's
    proprietary format that is ready for use and distribution.
    """
    
    STANDARD_DIRECTORIES = ['scripts', 'assets', 'references', 'agents']
    
    def __init__(self, output_dir: str = "./skills"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_package(
        self,
        skill_name: str,
        skill_description: str,
        skill_content: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        version: str = "1.0.0",
        requirements: Optional[List[str]] = None,
        resource_files: Optional[List[str]] = None,
        config: Optional[PackageConfig] = None
    ) -> str:
        """
        Create a complete, standardized skill package
        
        Args:
            skill_name: Name of the skill
            skill_description: Description of the skill
            skill_content: Main skill content (SKILL.md)
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            version: Semantic version string
            requirements: Optional list of requirements
            resource_files: Optional list of resource files to include
            config: Optional packaging configuration
            
        Returns:
            Path to the created skill package
        """
        config = config or PackageConfig()
        
        # Create skill directory
        skill_slug = self._slugify(skill_name)
        skill_dir = os.path.join(self.output_dir, skill_slug)
        os.makedirs(skill_dir, exist_ok=True)
        
        # Create standard directories
        for dir_name in self.STANDARD_DIRECTORIES:
            if self._should_include_dir(dir_name, config):
                os.makedirs(os.path.join(skill_dir, dir_name), exist_ok=True)
        
        # Create frontmatter
        frontmatter = self._create_frontmatter(
            name=skill_name,
            description=skill_description,
            version=version,
            author=author,
            tags=tags or [],
            category=category,
            requirements=requirements or []
        )
        
        # Create SKILL.md
        skill_md_path = os.path.join(skill_dir, 'SKILL.md')
        self._write_skill_md(skill_md_path, frontmatter, skill_content)
        
        # Generate README
        if config.generate_readme:
            readme_path = os.path.join(skill_dir, 'README.md')
            self._write_readme(readme_path, frontmatter)
        
        # Generate example script
        if config.include_scripts:
            example_script = os.path.join(skill_dir, 'scripts', 'example.py')
            self._write_example_script(example_script, skill_name)
        
        # Copy resource files
        if resource_files and config.include_assets:
            self._copy_resource_files(skill_dir, resource_files)
        
        return skill_dir
    
    def update_package(
        self,
        skill_dir: str,
        new_content: str,
        version_bump: str = "patch",
        change_description: Optional[str] = None,
        config: Optional[PackageConfig] = None
    ) -> str:
        """
        Update an existing skill package
        
        Args:
            skill_dir: Path to the existing skill package
            new_content: New skill content
            version_bump: Type of version bump ('major', 'minor', 'patch')
            change_description: Description of what changed
            config: Optional packaging configuration
            
        Returns:
            Path to the updated skill package
        """
        config = config or PackageConfig()
        
        # Read existing SKILL.md
        skill_md_path = os.path.join(skill_dir, 'SKILL.md')
        if not os.path.exists(skill_md_path):
            raise ValueError(f"SKILL.md not found in {skill_dir}")
        
        frontmatter, old_content = self._read_skill_md(skill_md_path)
        
        # Bump version
        frontmatter['version'] = self._bump_version(frontmatter.get('version', '1.0.0'), version_bump)
        frontmatter['updated_at'] = datetime.now().isoformat()
        
        # Update SKILL.md
        self._write_skill_md(skill_md_path, frontmatter, new_content)
        
        # Update README
        if config.generate_readme:
            readme_path = os.path.join(skill_dir, 'README.md')
            if os.path.exists(readme_path):
                self._write_readme(readme_path, frontmatter)
        
        # Add changelog entry
        if config.generate_changelog:
            changelog_path = os.path.join(skill_dir, 'references', 'CHANGELOG.md')
            self._add_changelog_entry(changelog_path, frontmatter['version'], change_description)
        
        return skill_dir
    
    def validate_package(self, skill_dir: str) -> tuple[bool, List[str]]:
        """
        Validate a skill package
        
        Args:
            skill_dir: Path to the skill package
            
        Returns:
            (is_valid, list_of_issues)
        """
        issues = []
        
        # Check required files
        skill_md = os.path.join(skill_dir, 'SKILL.md')
        if not os.path.exists(skill_md):
            issues.append("Missing SKILL.md")
        
        readme_md = os.path.join(skill_dir, 'README.md')
        if not os.path.exists(readme_md):
            issues.append("Missing README.md")
        
        # Validate SKILL.md if it exists
        if os.path.exists(skill_md):
            try:
                frontmatter, _ = self._read_skill_md(skill_md)
                if not frontmatter.get('name'):
                    issues.append("SKILL.md missing 'name' field")
                if not frontmatter.get('description'):
                    issues.append("SKILL.md missing 'description' field")
            except Exception as e:
                issues.append(f"Invalid SKILL.md: {str(e)}")
        
        return len(issues) == 0, issues
    
    def _slugify(self, name: str) -> str:
        """Convert name to directory-safe slug"""
        import re
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        return slug
    
    def _bump_version(self, version: str, bump_type: str) -> str:
        """Bump semantic version"""
        try:
            major, minor, patch = map(int, version.split('.'))
            if bump_type == 'major':
                major += 1
                minor = 0
                patch = 0
            elif bump_type == 'minor':
                minor += 1
                patch = 0
            else:
                patch += 1
            return f"{major}.{minor}.{patch}"
        except:
            return version
    
    def _create_frontmatter(
        self,
        name: str,
        description: str,
        version: str,
        author: Optional[str],
        tags: List[str],
        category: Optional[str],
        requirements: List[str]
    ) -> Dict[str, Any]:
        """Create frontmatter dictionary"""
        return {
            'name': name,
            'description': description,
            'version': version,
            'author': author,
            'tags': tags,
            'category': category,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'license': 'MIT',
            'requirements': requirements
        }
    
    def _write_skill_md(self, path: str, frontmatter: Dict[str, Any], content: str):
        """Write SKILL.md with YAML frontmatter"""
        yaml_content = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
        full_content = f"---\n{yaml_content}---\n\n{content}"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(full_content)
    
    def _read_skill_md(self, path: str) -> tuple[Dict[str, Any], str]:
        """Read SKILL.md and parse frontmatter"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                yaml_str = parts[1].strip()
                body = parts[2].strip()
                frontmatter = yaml.safe_load(yaml_str) or {}
                return frontmatter, body
        
        return {}, content
    
    def _write_readme(self, path: str, frontmatter: Dict[str, Any]):
        """Write README.md for the skill"""
        readme_content = f"""# {frontmatter.get('name', 'Unnamed Skill')}

{frontmatter.get('description', '')}

## Version
{frontmatter.get('version', '1.0.0')}

## Tags
{', '.join(frontmatter.get('tags', [])) if frontmatter.get('tags') else 'None'}

## Category
{frontmatter.get('category', 'Uncategorized')}

## Author
{frontmatter.get('author', 'Unknown')}

## License
{frontmatter.get('license', 'MIT')}

## Requirements
{chr(10).join(f'- {req}' for req in frontmatter.get('requirements', [])) if frontmatter.get('requirements') else 'None'}

## Usage

This skill can be used with EXO or compatible AI Agent systems.

---

*Created by EXO Skill Packager*
"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def _write_example_script(self, path: str, skill_name: str):
        """Write example script"""
        script_content = f"""#!/usr/bin/env python3
\"\"\"
Example script for {skill_name}

This is an example script that demonstrates how to use this skill.
\"\"\"

def main():
    print(f"Running {skill_name}...")
    # Add your skill execution logic here
    print("Skill executed successfully!")

if __name__ == "__main__":
    main()
"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(script_content)
    
    def _copy_resource_files(self, skill_dir: str, resource_files: List[str]):
        """Copy resource files into the skill package"""
        assets_dir = os.path.join(skill_dir, 'assets')
        
        for resource_path in resource_files:
            if os.path.exists(resource_path):
                filename = os.path.basename(resource_path)
                dest_path = os.path.join(assets_dir, filename)
                shutil.copy2(resource_path, dest_path)
    
    def _add_changelog_entry(self, path: str, version: str, description: Optional[str]):
        """Add entry to CHANGELOG.md"""
        entry = f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n"
        if description:
            entry += f"- {description}\n"
        entry += "\n"
        
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                existing = f.read()
            content = entry + existing
        else:
            content = f"# Changelog\n\n{entry}"
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _should_include_dir(self, dir_name: str, config: PackageConfig) -> bool:
        """Check if a directory should be included"""
        if dir_name == 'scripts':
            return config.include_scripts
        if dir_name == 'assets':
            return config.include_assets
        if dir_name == 'references':
            return config.include_references
        if dir_name == 'agents':
            return config.include_agents
        return True
