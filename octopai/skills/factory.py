"""
Skill Factory - Octopai's Innovative Skill Creation System

This module provides Octopai's proprietary skill creation system that
transforms diverse resources into structured, AI-ready skills through
intelligent analysis, evaluation, and optimization.

Octopai's Full-Lifecycle Engineering Framework:
- Analysis: Deep understanding of source content
- Generation: Initial skill content creation
- Evaluation: Comprehensive quality assessment
- Optimization: Targeted improvements based on evaluation
- Validation: Ensure skill readiness for AI Agent consumption
"""

import os
import hashlib
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import re
import uuid

from octopai.utils.config import Config
from octopai.utils.helpers import read_file, write_file
from octopai.data.converter import URLConverter
from octopai.data.parser import ResourceParser
import requests


__all__ = [
    'SkillFactory',
    'SkillType',
    'SkillQualityLevel',
    'SkillQualityMetrics',
    'SkillMetadata',
    'SkillDefinition',
    'SkillVersion',
    'SkillQualityEvaluator',
    'SkillOptimizer',
    'SkillTemplate',
    'SkillInteractionPrototype',
    'EnhancedQualityEvaluator',
    'create_skill_with_template',
    'generate_skill_prototype'
]


class SkillType(Enum):
    """Types of skills that can be created"""
    GENERAL = "general"
    ANALYSIS = "analysis"
    AUTOMATION = "automation"
    CREATIVE = "creative"
    RESEARCH = "research"
    CODING = "coding"
    TROUBLESHOOTING = "troubleshooting"
    REFERENCE = "reference"
    TUTORIAL = "tutorial"


class SkillQualityLevel(Enum):
    """Quality levels for skill evaluation"""
    DRAFT = "draft"
    BASIC = "basic"
    GOOD = "good"
    EXCELLENT = "excellent"
    PREMIUM = "premium"


@dataclass
class SkillQualityMetrics:
    """Comprehensive quality metrics for skill evaluation"""
    completeness_score: float = 0.0
    readability_score: float = 0.0
    structure_score: float = 0.0
    example_coverage: float = 0.0
    troubleshooting_coverage: float = 0.0
    best_practices_coverage: float = 0.0
    semantic_coherence: float = 0.0
    practical_utility: float = 0.0
    adaptability_score: float = 0.0
    overall_score: float = 0.0
    quality_level: SkillQualityLevel = SkillQualityLevel.DRAFT
    recommendations: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "completeness_score": self.completeness_score,
            "readability_score": self.readability_score,
            "structure_score": self.structure_score,
            "example_coverage": self.example_coverage,
            "troubleshooting_coverage": self.troubleshooting_coverage,
            "best_practices_coverage": self.best_practices_coverage,
            "semantic_coherence": self.semantic_coherence,
            "practical_utility": self.practical_utility,
            "adaptability_score": self.adaptability_score,
            "overall_score": self.overall_score,
            "quality_level": self.quality_level.value,
            "recommendations": self.recommendations,
            "strengths": self.strengths,
            "gaps": self.gaps
        }


@dataclass
class SkillVersion:
    """Represents a version of a skill with complete history"""
    version: int
    content: str
    created_at: str
    author: Optional[str] = None
    change_description: Optional[str] = None
    content_hash: str = ""
    quality_metrics: Optional[SkillQualityMetrics] = None
    
    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = self._compute_hash(self.content)
    
    def _compute_hash(self, content: str) -> str:
        """Compute secure hash of skill content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.quality_metrics:
            data['quality_metrics'] = self.quality_metrics.to_dict()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillVersion':
        metrics_data = data.pop('quality_metrics', None)
        version = cls(**data)
        if metrics_data:
            metrics_data['quality_level'] = SkillQualityLevel(metrics_data['quality_level'])
            version.quality_metrics = SkillQualityMetrics(**metrics_data)
        return version


@dataclass
class SkillMetadata:
    """Comprehensive metadata for a skill"""
    skill_id: str
    name: str
    description: str
    skill_type: SkillType = SkillType.GENERAL
    tags: List[str] = field(default_factory=list)
    category: Optional[str] = None
    author: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    license: str = "MIT"
    requirements: List[str] = field(default_factory=list)
    source_type: Optional[str] = None
    source_reference: Optional[str] = None
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['skill_type'] = self.skill_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillMetadata':
        if 'skill_type' in data and isinstance(data['skill_type'], str):
            data['skill_type'] = SkillType(data['skill_type'])
        return cls(**data)


@dataclass
class SkillDefinition:
    """Complete skill definition with content and metadata"""
    metadata: SkillMetadata
    versions: List[SkillVersion] = field(default_factory=list)
    
    @property
    def latest_version(self) -> Optional[SkillVersion]:
        """Get the most recent version"""
        if not self.versions:
            return None
        return max(self.versions, key=lambda v: v.version)
    
    def add_version(
        self,
        content: str,
        author: Optional[str] = None,
        change_description: Optional[str] = None,
        quality_metrics: Optional[SkillQualityMetrics] = None
    ) -> SkillVersion:
        """Add a new version of the skill"""
        new_version_num = max([v.version for v in self.versions], default=0) + 1
        version = SkillVersion(
            version=new_version_num,
            content=content,
            created_at=datetime.now().isoformat(),
            author=author,
            change_description=change_description,
            quality_metrics=quality_metrics
        )
        self.versions.append(version)
        self.metadata.updated_at = datetime.now().isoformat()
        return version
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'metadata': self.metadata.to_dict(),
            'versions': [v.to_dict() for v in self.versions]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillDefinition':
        return cls(
            metadata=SkillMetadata.from_dict(data['metadata']),
            versions=[SkillVersion.from_dict(v) for v in data.get('versions', [])]
        )


class SkillQualityEvaluator:
    """
    Skill Quality Evaluator - Comprehensive quality assessment
    
    Evaluates skills across multiple dimensions to ensure
    readiness for AI Agent consumption.
    """
    
    def __init__(self):
        self.required_sections = [
            "Overview", "Purpose", "Usage", "Examples",
            "Best Practices", "Troubleshooting"
        ]
        self.recommended_sections = [
            "Prerequisites", "Configuration", "Advanced Topics",
            "Related Skills", "References"
        ]
    
    def evaluate(self, content: str) -> SkillQualityMetrics:
        """
        Evaluate skill content quality
        
        Args:
            content: Skill content to evaluate
            
        Returns:
            Comprehensive quality metrics
        """
        metrics = SkillQualityMetrics()
        
        metrics.completeness_score = self._assess_completeness(content)
        metrics.readability_score = self._assess_readability(content)
        metrics.structure_score = self._assess_structure(content)
        metrics.example_coverage = self._assess_examples(content)
        metrics.troubleshooting_coverage = self._assess_troubleshooting(content)
        metrics.best_practices_coverage = self._assess_best_practices(content)
        
        metrics.overall_score = self._calculate_overall_score(metrics)
        metrics.quality_level = self._determine_quality_level(metrics.overall_score)
        
        metrics.recommendations = self._generate_recommendations(content, metrics)
        metrics.strengths = self._identify_strengths(content, metrics)
        metrics.gaps = self._identify_gaps(content, metrics)
        
        return metrics
    
    def _assess_completeness(self, content: str) -> float:
        """Assess how complete the skill content is"""
        score = 0.0
        content_lower = content.lower()
        
        for section in self.required_sections:
            if section.lower() in content_lower:
                score += 1.0 / len(self.required_sections)
        
        for section in self.recommended_sections:
            if section.lower() in content_lower:
                score += 0.25 / len(self.recommended_sections)
        
        return min(score, 1.0)
    
    def _assess_readability(self, content: str) -> float:
        """Assess readability of the content"""
        score = 0.5
        lines = content.split('\n')
        
        if any(line.startswith('#') for line in lines):
            score += 0.15
        if any(line.startswith('##') for line in lines):
            score += 0.1
        if any(line.startswith('###') for line in lines):
            score += 0.1
        if 10 < len(lines) < 500:
            score += 0.15
        
        return min(score, 1.0)
    
    def _assess_structure(self, content: str) -> float:
        """Assess the structural quality"""
        score = 0.4
        
        heading_counts = 0
        for line in content.split('\n'):
            if line.startswith('#'):
                heading_counts += 1
        
        if heading_counts >= 3:
            score += 0.2
        if heading_counts >= 5:
            score += 0.2
        if content.count('```') >= 2:
            score += 0.2
        
        return min(score, 1.0)
    
    def _assess_examples(self, content: str) -> float:
        """Assess example coverage"""
        content_lower = content.lower()
        score = 0.0
        
        if 'example' in content_lower or 'Example' in content:
            score += 0.5
        if content.count('```') >= 4:
            score += 0.3
        if 'usage' in content_lower or 'Usage' in content:
            score += 0.2
        
        return min(score, 1.0)
    
    def _assess_troubleshooting(self, content: str) -> float:
        """Assess troubleshooting coverage"""
        content_lower = content.lower()
        score = 0.0
        
        if 'troubleshoot' in content_lower or 'Troubleshoot' in content:
            score += 0.5
        if 'faq' in content_lower or 'FAQ' in content:
            score += 0.3
        if 'error' in content_lower or 'Error' in content:
            score += 0.2
        
        return min(score, 1.0)
    
    def _assess_best_practices(self, content: str) -> float:
        """Assess best practices coverage"""
        content_lower = content.lower()
        score = 0.0
        
        if 'best practice' in content_lower or 'Best Practice' in content:
            score += 0.5
        if 'recommendation' in content_lower or 'Recommendation' in content:
            score += 0.3
        if 'note' in content_lower or 'Note' in content or 'warning' in content_lower or 'Warning' in content:
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_overall_score(self, metrics: SkillQualityMetrics) -> float:
        """Calculate weighted overall score"""
        weights = {
            'completeness_score': 0.25,
            'readability_score': 0.15,
            'structure_score': 0.15,
            'example_coverage': 0.20,
            'troubleshooting_coverage': 0.15,
            'best_practices_coverage': 0.10
        }
        
        total = 0.0
        for key, weight in weights.items():
            total += getattr(metrics, key) * weight
        
        return total
    
    def _determine_quality_level(self, score: float) -> SkillQualityLevel:
        """Determine quality level from score"""
        if score >= 0.9:
            return SkillQualityLevel.PREMIUM
        elif score >= 0.75:
            return SkillQualityLevel.EXCELLENT
        elif score >= 0.6:
            return SkillQualityLevel.GOOD
        elif score >= 0.4:
            return SkillQualityLevel.BASIC
        else:
            return SkillQualityLevel.DRAFT
    
    def _generate_recommendations(self, content: str, metrics: SkillQualityMetrics) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        content_lower = content.lower()
        
        if metrics.completeness_score < 0.7:
            recommendations.append("Add missing sections: Overview, Purpose, Usage, Examples")
        if metrics.example_coverage < 0.5:
            recommendations.append("Include practical code examples and usage patterns")
        if metrics.troubleshooting_coverage < 0.5:
            recommendations.append("Add troubleshooting guidance for common issues")
        if metrics.best_practices_coverage < 0.5:
            recommendations.append("Include best practices and recommendations")
        if metrics.structure_score < 0.6:
            recommendations.append("Improve section organization with clear headings")
        
        return recommendations
    
    def _identify_strengths(self, content: str, metrics: SkillQualityMetrics) -> List[str]:
        """Identify skill strengths"""
        strengths = []
        content_lower = content.lower()
        
        if metrics.example_coverage >= 0.7:
            strengths.append("Excellent example coverage")
        if metrics.readability_score >= 0.8:
            strengths.append("High readability and clear structure")
        if metrics.troubleshooting_coverage >= 0.7:
            strengths.append("Comprehensive troubleshooting guidance")
        if metrics.best_practices_coverage >= 0.7:
            strengths.append("Well-documented best practices")
        
        return strengths
    
    def _identify_gaps(self, content: str, metrics: SkillQualityMetrics) -> List[str]:
        """Identify skill gaps"""
        gaps = []
        content_lower = content.lower()
        
        if metrics.completeness_score < 0.6:
            gaps.append("Incomplete coverage of essential sections")
        if metrics.example_coverage < 0.4:
            gaps.append("Lacks practical examples")
        if metrics.structure_score < 0.5:
            gaps.append("Needs better structural organization")
        
        return gaps


class SkillOptimizer:
    """
    Skill Optimizer - Targeted improvements based on evaluation
    
    Optimizes skills using quality evaluation insights.
    """
    
    def __init__(self, config: Config):
        self.config = config
    
    def optimize(
        self,
        content: str,
        metrics: SkillQualityMetrics,
        target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
    ) -> str:
        """
        Optimize skill content based on quality metrics
        
        Args:
            content: Original skill content
            metrics: Quality evaluation metrics
            target_quality: Target quality level
            
        Returns:
            Optimized skill content
        """
        if metrics.quality_level.value >= target_quality.value:
            return content
        
        return self._generate_optimized_content(content, metrics)
    
    def _generate_optimized_content(self, content: str, metrics: SkillQualityMetrics) -> str:
        """Generate optimized content using LLM"""
        prompt = self._build_optimization_prompt(content, metrics)
        
        headers = {
            'Authorization': f'Bearer {self.config.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": self.config.OCTOPAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert at skill optimization and improvement.
Your task is to enhance a skill based on quality evaluation metrics.
Focus on:
1. Addressing identified gaps
2. Building on existing strengths
3. Adding missing sections
4. Improving structure and clarity
5. Adding practical examples
6. Including troubleshooting guidance
7. Documenting best practices"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.config.OPENROUTER_API_URL,
                headers=headers,
                json=data,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            # Improved response parsing with better error handling
            choices = result.get('choices', [])
            if not choices:
                raise ValueError("No choices returned from API")
            message = choices[0].get('message', {})
            optimized_content = message.get('content', content)
            if not optimized_content:
                raise ValueError("No content returned from API")
            return optimized_content
        except requests.exceptions.Timeout:
            print("API request timed out. Using fallback skill content.")
            return self._build_fallback_skill_content(source_content, name, description)
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}. Using fallback skill content.")
            return self._build_fallback_skill_content(source_content, name, description)
        except (ValueError, KeyError) as e:
            print(f"API response parsing failed: {str(e)}. Using fallback skill content.")
            return self._build_fallback_skill_content(source_content, name, description)
        except Exception as e:
            print(f"Unexpected error during skill generation: {str(e)}. Using fallback skill content.")
            return self._build_fallback_skill_content(source_content, name, description)
    
    def _build_optimization_prompt(self, content: str, metrics: SkillQualityMetrics) -> str:
        """Build optimization prompt"""
        strengths_text = "\n".join([f"- {s}" for s in metrics.strengths])
        gaps_text = "\n".join([f"- {g}" for g in metrics.gaps])
        recommendations_text = "\n".join([f"- {r}" for r in metrics.recommendations])
        
        return f"""# Skill Optimization Request

## Current Quality Metrics
- Overall Score: {metrics.overall_score:.2f}
- Quality Level: {metrics.quality_level.value}
- Completeness: {metrics.completeness_score:.2f}
- Readability: {metrics.readability_score:.2f}
- Structure: {metrics.structure_score:.2f}
- Examples: {metrics.example_coverage:.2f}
- Troubleshooting: {metrics.troubleshooting_coverage:.2f}
- Best Practices: {metrics.best_practices_coverage:.2f}

## Strengths
{strengths_text if strengths_text else "No specific strengths identified"}

## Gaps
{gaps_text if gaps_text else "No specific gaps identified"}

## Recommendations
{recommendations_text if recommendations_text else "No specific recommendations"}

## Current Skill Content
{content}

Please optimize this skill, focusing on addressing the gaps and recommendations while preserving the strengths."""
    
    def _build_fallback_optimization(self, content: str, metrics: SkillQualityMetrics) -> str:
        """Build fallback optimization when LLM is unavailable"""
        additions = []
        
        if metrics.example_coverage < 0.5:
            additions.append("""
## Examples

### Basic Usage
```python
# Basic usage example goes here
```

### Advanced Usage
```python
# Advanced usage example goes here
```
""")
        
        if metrics.troubleshooting_coverage < 0.5:
            additions.append("""
## Troubleshooting

### Common Issues

#### Issue 1: [Description]
**Solution:** [Step-by-step solution]

#### Issue 2: [Description]
**Solution:** [Step-by-step solution]
""")
        
        if metrics.best_practices_coverage < 0.5:
            additions.append("""
## Best Practices

1. [Best Practice 1]
2. [Best Practice 2]
3. [Best Practice 3]

## Recommendations

- [Recommendation 1]
- [Recommendation 2]
""")
        
        return content + "\n" + "\n".join(additions)


class SkillFactory:
    """
    Octopai's Skill Factory - Intelligent Skill Creation System with Full-Lifecycle Engineering
    
    Transforms ANYTHING into structured, high-quality skills through Octopai's 
    proprietary analysis, evaluation, and optimization pipeline. 
    Everything Can Be a Skill!
    
    Full-Lifecycle Framework:
    1. Analysis: Deep understanding of source content
    2. Generation: Initial skill content creation
    3. Evaluation: Comprehensive quality assessment
    4. Optimization: Targeted improvements
    5. Validation: Ensure readiness for AI Agents
    
    Supported input types:
    - Web URLs and websites
    - Files (PDF, DOC, XLS, images, videos, code, etc.)
    - Raw text and prompts
    - API endpoints and data streams
    - Code repositories and snippets
    - And more!
    """
    
    def __init__(self):
        self.config = Config()
        self.evaluator = SkillQualityEvaluator()
        self.optimizer = SkillOptimizer(self.config)
    
    def create_from_url(
        self,
        url: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        skill_type: SkillType = SkillType.GENERAL,
        additional_context: Optional[str] = None,
        auto_optimize: bool = True,
        target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
    ) -> SkillDefinition:
        """
        Create a skill from a web URL with full-lifecycle engineering
        
        Args:
            url: The web URL to transform
            name: Name for the skill
            description: Description of the skill
            tags: Optional tags for categorization
            category: Optional category
            author: Optional author name
            skill_type: Type of skill being created
            additional_context: Optional additional context for skill creation
            auto_optimize: Whether to auto-optimize after creation
            target_quality: Target quality level for optimization
            
        Returns:
            Complete SkillDefinition ready for use
        """
        converter = URLConverter()
        content = converter.convert(url)
        
        return self._create_skill(
            source_content=content,
            source_type="url",
            source_reference=url,
            name=name,
            description=description,
            tags=tags or ["web-resource"],
            category=category,
            author=author,
            skill_type=skill_type,
            additional_context=additional_context,
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
        additional_context: Optional[str] = None,
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
            additional_context: Optional additional context for skill creation
            auto_optimize: Whether to auto-optimize after creation
            target_quality: Target quality level for optimization
            
        Returns:
            Complete SkillDefinition ready for use
        """
        parser = ResourceParser()
        combined_content = []
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    resource = parser.parse(file_path)
                    combined_content.append(f"## File: {os.path.basename(file_path)}\n\n{resource.to_skill_resource()}")
                except Exception as e:
                    combined_content.append(f"## File: {os.path.basename(file_path)}\n\nError processing: {str(e)}")
        
        content = "\n\n---\n\n".join(combined_content)
        
        return self._create_skill(
            source_content=content,
            source_type="files",
            source_reference=",".join([os.path.basename(f) for f in file_paths]),
            name=name,
            description=description,
            tags=tags or ["file-based"],
            category=category,
            author=author,
            skill_type=skill_type,
            additional_context=additional_context,
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
        enhanced_prompt = prompt
        
        if resources:
            parser = ResourceParser()
            resource_contents = []
            
            for res_path in resources:
                if os.path.exists(res_path):
                    try:
                        resource = parser.parse(res_path)
                        resource_contents.append(f"\n--- Resource: {os.path.basename(res_path)} ---\n{resource.to_skill_resource()}")
                    except Exception as e:
                        resource_contents.append(f"\n--- Resource: {os.path.basename(res_path)} ---\nError parsing: {str(e)}")
            
            if resource_contents:
                enhanced_prompt = f"{prompt}\n\nAdditional Resources:\n{' '.join(resource_contents)}"
        
        return self._create_skill(
            source_content=enhanced_prompt,
            source_type="prompt",
            source_reference="direct-prompt",
            name=name,
            description=description,
            tags=tags or ["prompt-based"],
            category=category,
            author=author,
            skill_type=skill_type,
            additional_context=None,
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    
    def _create_skill(
        self,
        source_content: str,
        source_type: str,
        source_reference: str,
        name: str,
        description: str,
        tags: List[str],
        category: Optional[str],
        author: Optional[str],
        skill_type: SkillType,
        additional_context: Optional[str],
        auto_optimize: bool,
        target_quality: SkillQualityLevel
    ) -> SkillDefinition:
        """Internal method to create a skill from prepared content with full lifecycle"""
        
        skill_id = self._generate_skill_id(name)
        
        metadata = SkillMetadata(
            skill_id=skill_id,
            name=name,
            description=description,
            skill_type=skill_type,
            tags=tags,
            category=category,
            author=author,
            source_type=source_type,
            source_reference=source_reference
        )
        
        initial_content = self._generate_initial_content(
            source_content=source_content,
            source_type=source_type,
            source_reference=source_reference,
            name=name,
            description=description,
            skill_type=skill_type,
            additional_context=additional_context
        )
        
        initial_metrics = self.evaluator.evaluate(initial_content)
        
        final_content = initial_content
        final_metrics = initial_metrics
        
        if auto_optimize and initial_metrics.quality_level.value < target_quality.value:
            final_content = self.optimizer.optimize(
                initial_content, 
                initial_metrics, 
                target_quality
            )
            final_metrics = self.evaluator.evaluate(final_content)
        
        definition = SkillDefinition(metadata=metadata)
        definition.add_version(
            content=final_content,
            author=author,
            change_description=f"Initial version created from {source_type}",
            quality_metrics=final_metrics
        )
        
        return definition
    
    def _generate_skill_id(self, name: str) -> str:
        """Generate a unique skill ID"""
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        short_id = str(uuid.uuid4())[:8]
        return f"{slug}-{short_id}"
    
    def _generate_initial_content(
        self,
        source_content: str,
        source_type: str,
        source_reference: str,
        name: str,
        description: str,
        skill_type: SkillType,
        additional_context: Optional[str]
    ) -> str:
        """Generate initial skill content using intelligent generation"""
        
        prompt = self._build_skill_generation_prompt(
            source_content=source_content,
            source_type=source_type,
            source_reference=source_reference,
            name=name,
            description=description,
            skill_type=skill_type,
            additional_context=additional_context
        )
        
        headers = {
            'Authorization': f'Bearer {self.config.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": self.config.OCTOPAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert at creating comprehensive, well-structured skills for AI Agents.
Create skills that are:
1. Clear and actionable
2. Well-organized with logical sections
3. Complete with examples and best practices
4. Easy for AI Agents to understand and use
5. Include troubleshooting guidance

CRITICAL: Always include ALL of these sections:
- Overview and Purpose
- Prerequisites (if applicable)
- Usage Instructions
- Practical Examples
- Best Practices
- Troubleshooting Guide

Format as Markdown, ready to be used as SKILL.md content."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.config.OPENROUTER_API_URL,
                headers=headers,
                json=data,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            choices = result.get('choices', [])
            if not choices:
                return self._build_fallback_skill_content(source_content, name, description)
            message = choices[0].get('message', {})
            generated_content = message.get('content', '')
            if not generated_content:
                return self._build_fallback_skill_content(source_content, name, description)
            return generated_content
        except requests.exceptions.Timeout:
            print("API request timed out. Using fallback skill content.")
            return self._build_fallback_skill_content(source_content, name, description)
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}. Using fallback skill content.")
            return self._build_fallback_skill_content(source_content, name, description)
        except (ValueError, KeyError) as e:
            print(f"API response parsing failed: {str(e)}. Using fallback skill content.")
            return self._build_fallback_skill_content(source_content, name, description)
        except Exception as e:
            print(f"Unexpected error during skill generation: {str(e)}. Using fallback skill content.")
            return self._build_fallback_skill_content(source_content, name, description)
    
    def _build_skill_generation_prompt(
        self,
        source_content: str,
        source_type: str,
        source_reference: str,
        name: str,
        description: str,
        skill_type: SkillType,
        additional_context: Optional[str]
    ) -> str:
        """Build the prompt for skill generation"""
        
        prompt_parts = [
            f"# Skill Creation Request",
            f"",
            f"## Skill Information",
            f"- **Name**: {name}",
            f"- **Description**: {description}",
            f"- **Type**: {skill_type.value}",
            f"- **Source**: {source_type} ({source_reference})",
            f"",
            f"## Source Content",
            f"",
            source_content
        ]
        
        if additional_context:
            prompt_parts.extend([
                f"",
                f"## Additional Context",
                f"",
                additional_context
            ])
        
        prompt_parts.extend([
            f"",
            f"Please create a comprehensive, well-structured skill in Markdown format.",
            f"CRITICAL REQUIREMENTS:",
            f"1. Start with # {name}",
            f"2. Include ALL required sections: Overview, Usage, Examples, Best Practices, Troubleshooting",
            f"3. Use clear section headings (##, ###)",
            f"4. Include practical code examples where appropriate",
            f"5. Make it easy for AI Agents to understand and use"
        ])
        
        return "\n".join(prompt_parts)
    
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
        return self._create_skill(
            source_content=text,
            source_type="text",
            source_reference="raw-text",
            name=name,
            description=description,
            tags=tags or ["text-based"],
            category=category,
            author=author,
            skill_type=skill_type,
            additional_context=None,
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
        enhanced_content = f"## Code ({language})\n\n```{language}\n{code}\n```"
        return self._create_skill(
            source_content=enhanced_content,
            source_type="code",
            source_reference=f"{language}-code",
            name=name,
            description=description,
            tags=tags or ["code", language.lower()],
            category=category,
            author=author,
            skill_type=SkillType.CODING,
            additional_context=f"Programming language: {language}",
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    
    def create_from_api(
        self,
        api_endpoint: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        auto_optimize: bool = True,
        target_quality: SkillQualityLevel = SkillQualityLevel.GOOD
    ) -> SkillDefinition:
        """
        Create a skill from an API endpoint with full-lifecycle engineering
        
        Args:
            api_endpoint: API endpoint URL
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
        api_content = f"## API Endpoint\n\n- **Endpoint**: {api_endpoint}\n- **Type**: REST API"
        return self._create_skill(
            source_content=api_content,
            source_type="api",
            source_reference=api_endpoint,
            name=name,
            description=description,
            tags=tags or ["api", "integration"],
            category=category,
            author=author,
            skill_type=SkillType.AUTOMATION,
            additional_context=f"API endpoint: {api_endpoint}",
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    
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
        source_type = type(source).__name__
        source_content = self._normalize_anything_to_content(source)
        
        return self._create_skill(
            source_content=source_content,
            source_type=source_type,
            source_reference=f"auto-detected-{source_type}",
            name=name,
            description=description,
            tags=tags or ["universal", source_type.lower()],
            category=category,
            author=author,
            skill_type=skill_type,
            additional_context=f"Source type: {source_type}",
            auto_optimize=auto_optimize,
            target_quality=target_quality
        )
    
    def _normalize_anything_to_content(self, source: Any) -> str:
        """Normalize ANY source to text content"""
        if isinstance(source, str):
            return source
        elif isinstance(source, (list, tuple)):
            return "\n".join([f"- {item}" for item in source])
        elif isinstance(source, dict):
            return "\n".join([f"**{k}**: {v}" for k, v in source.items()])
        else:
            return str(source)
    
    def _build_fallback_skill_content(
        self,
        source_content: str,
        name: str,
        description: str
    ) -> str:
        """Build fallback skill content if generation fails"""
        
        return f"""# {name}

{description}

## Overview

This skill was created from source content and provides structured knowledge
for AI Agents. Created with Octopai's 'Everything Can Be a Skill' philosophy.

## Usage

Use this skill to access and apply the knowledge contained within.

## Examples

### Basic Usage
```
# Example usage goes here
```

## Best Practices

1. Review the source content thoroughly
2. Adapt examples to your specific use case
3. Test with sample inputs before production use

## Troubleshooting

### Common Issues

If you encounter issues:
1. Verify the source content is accessible
2. Check for any format-specific requirements
3. Refer to the original source for additional context

## Source Content

{source_content}

---

*Created by Octopai Skill Factory - Everything Can Be a Skill!*"""
    
    def evaluate_skill(self, skill_def: SkillDefinition) -> SkillQualityMetrics:
        """
        Evaluate a skill's quality
        
        Args:
            skill_def: Skill definition to evaluate
            
        Returns:
            Quality metrics
        """
        latest = skill_def.latest_version
        if not latest:
            return SkillQualityMetrics()
        return self.evaluator.evaluate(latest.content)
    
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
        latest = skill_def.latest_version
        if not latest:
            return skill_def
        
        current_metrics = latest.quality_metrics or self.evaluator.evaluate(latest.content)
        
        if current_metrics.quality_level.value >= target_quality.value:
            return skill_def
        
        optimized_content = self.optimizer.optimize(
            latest.content,
            current_metrics,
            target_quality
        )
        
        new_metrics = self.evaluator.evaluate(optimized_content)
        
        skill_def.add_version(
            content=optimized_content,
            author=author,
            change_description=f"Optimized from {current_metrics.quality_level.value} to {new_metrics.quality_level.value}",
            quality_metrics=new_metrics
        )
        
        return skill_def


class SkillTemplate:
    """
    Smart Skill Template - Intelligent template system for rapid skill creation
    
    Provides pre-built, customizable templates for common skill types,
    enabling rapid skill generation with intelligent defaults.
    """
    
    TEMPLATES = {
        'tutorial': {
            'sections': ['Overview', 'Prerequisites', 'Step-by-Step Guide', 'Examples', 'Best Practices', 'Troubleshooting'],
            'description': 'A step-by-step tutorial for learning a specific skill',
            'tags': ['tutorial', 'learning', 'guide']
        },
        'api_integration': {
            'sections': ['Overview', 'Authentication', 'Endpoints', 'Request Examples', 'Response Handling', 'Error Handling', 'Best Practices'],
            'description': 'API integration guide with endpoint documentation',
            'tags': ['api', 'integration', 'rest']
        },
        'data_processing': {
            'sections': ['Overview', 'Data Format', 'Processing Pipeline', 'Transformation Examples', 'Validation', 'Performance Tips'],
            'description': 'Data processing and transformation workflow',
            'tags': ['data', 'processing', 'transformation']
        },
        'troubleshooting': {
            'sections': ['Problem Overview', 'Common Symptoms', 'Root Causes', 'Solutions', 'Prevention', 'Additional Resources'],
            'description': 'Troubleshooting guide for common issues',
            'tags': ['troubleshooting', 'debugging', 'support']
        },
        'reference': {
            'sections': ['Overview', 'Concepts', 'API Reference', 'Configuration', 'Examples', 'FAQ'],
            'description': 'Comprehensive reference documentation',
            'tags': ['reference', 'documentation', 'manual']
        }
    }
    
    @classmethod
    def get_template(cls, template_type: str) -> Optional[Dict[str, Any]]:
        """
        Get a skill template by type
        
        Args:
            template_type: Type of template to retrieve
            
        Returns:
            Template configuration or None if not found
        """
        return cls.TEMPLATES.get(template_type.lower())
    
    @classmethod
    def list_templates(cls) -> List[str]:
        """
        List all available template types
        
        Returns:
            List of template type names
        """
        return list(cls.TEMPLATES.keys())
    
    @classmethod
    def generate_skill_structure(cls, template_type: str, name: str, description: str) -> str:
        """
        Generate a skill structure from a template
        
        Args:
            template_type: Type of template to use
            name: Name of the skill
            description: Description of the skill
            
        Returns:
            Generated skill content structure
        """
        template = cls.get_template(template_type)
        if not template:
            template = cls.TEMPLATES['reference']
        
        sections_content = []
        for section in template['sections']:
            sections_content.append(f"## {section}\n\n[Content for {section} goes here]\n")
        
        joined_sections = '\n'.join(sections_content)
        return f"""# {name}

{description}

{joined_sections}
"""


class SkillInteractionPrototype:
    """
    Skill Interaction Prototype - Generates interactive usage examples
    
    Creates executable, interactive prototypes that demonstrate
    skill usage in real-world scenarios.
    """
    
    def __init__(self, config: Config):
        self.config = config
    
    def generate_prototype(self, skill_def: SkillDefinition, scenario: str = "basic") -> str:
        """
        Generate an interactive prototype for a skill
        
        Args:
            skill_def: Skill definition to prototype
            scenario: Type of scenario to generate
            
        Returns:
            Interactive prototype code
        """
        skill_type = skill_def.metadata.skill_type.value
        
        if scenario == "basic":
            return self._generate_basic_prototype(skill_def)
        elif scenario == "advanced":
            return self._generate_advanced_prototype(skill_def)
        elif scenario == "test":
            return self._generate_test_prototype(skill_def)
        else:
            return self._generate_basic_prototype(skill_def)
    
    def _generate_basic_prototype(self, skill_def: SkillDefinition) -> str:
        """Generate basic usage prototype"""
        return f'''"""
Basic Usage Prototype for {skill_def.metadata.name}

This script demonstrates the basic usage of the skill.
"""

def demonstrate_basic_usage():
    """Demonstrate basic skill usage"""
    print(f"Using skill: {skill_def.metadata.name}")
    print(f"Description: {skill_def.metadata.description}")
    
    # Basic usage example
    result = apply_skill("sample input")
    print(f"Result: {{result}}")

def apply_skill(input_data):
    """Apply the skill to input data"""
    # Implementation based on skill content
    return f"Processed: {{input_data}}"

if __name__ == "__main__":
    demonstrate_basic_usage()
'''
    
    def _generate_advanced_prototype(self, skill_def: SkillDefinition) -> str:
        """Generate advanced usage prototype"""
        return f'''"""
Advanced Usage Prototype for {skill_def.metadata.name}

This script demonstrates advanced usage patterns and scenarios.
"""

class SkillAdvancedUsage:
    """Advanced usage patterns for the skill"""
    
    def __init__(self):
        self.skill_name = "{skill_def.metadata.name}"
        self.state = {{}}
    
    def process_batch(self, inputs):
        """Process multiple inputs in batch"""
        results = []
        for input_data in inputs:
            result = self._process_single(input_data)
            results.append(result)
        return results
    
    def _process_single(self, input_data):
        """Process a single input"""
        return f"Processed: {{input_data}}"
    
    def with_configuration(self, config):
        """Apply custom configuration"""
        self.state.update(config)
        return self

def demonstrate_advanced_usage():
    """Demonstrate advanced skill usage"""
    usage = SkillAdvancedUsage()
    
    # Batch processing
    inputs = ["input1", "input2", "input3"]
    results = usage.process_batch(inputs)
    print(f"Batch results: {{results}}")
    
    # With configuration
    custom = usage.with_configuration({{"mode": "advanced"}})
    print(f"Custom config applied")

if __name__ == "__main__":
    demonstrate_advanced_usage()
'''
    
    def _generate_test_prototype(self, skill_def: SkillDefinition) -> str:
        """Generate test prototype"""
        return f'''"""
Test Prototype for {skill_def.metadata.name}

This script contains comprehensive tests for the skill.
"""

import unittest

class TestSkill(unittest.TestCase):
    """Test cases for the skill"""
    
    def setUp(self):
        """Set up test environment"""
        self.skill_name = "{skill_def.metadata.name}"
    
    def test_basic_functionality(self):
        """Test basic skill functionality"""
        result = apply_skill("test input")
        self.assertIsNotNone(result)
        self.assertIn("Processed", result)
    
    def test_edge_cases(self):
        """Test edge cases"""
        edge_cases = ["", None, "special chars !@#$%"]
        for case in edge_cases:
            with self.subTest(case=case):
                result = apply_skill(case)
                self.assertIsNotNone(result)
    
    def test_performance(self):
        """Test performance characteristics"""
        import time
        start = time.time()
        for i in range(100):
            apply_skill(f"test {{i}}")
        duration = time.time() - start
        self.assertLess(duration, 5.0)  # Should complete in under 5 seconds

def apply_skill(input_data):
    """Apply the skill to input data"""
    if input_data is None:
        return "Processed: None"
    return f"Processed: {{str(input_data)}}"

if __name__ == "__main__":
    unittest.main()
'''


class EnhancedQualityEvaluator(SkillQualityEvaluator):
    """
    Enhanced Quality Evaluator - Advanced quality assessment with AI-powered insights
    
    Extends the base evaluator with more sophisticated metrics including
    semantic coherence, practical utility, and adaptability scoring.
    """
    
    def __init__(self):
        super().__init__()
        self.semantic_keywords = {
            'action_verbs': ['create', 'generate', 'transform', 'analyze', 'process', 'validate', 'optimize'],
            'utility_indicators': ['use', 'apply', 'implement', 'deploy', 'integrate'],
            'complexity_markers': ['however', 'although', 'nevertheless', 'additionally', 'furthermore']
        }
    
    def evaluate(self, content: str) -> SkillQualityMetrics:
        """
        Enhanced evaluation with additional metrics
        
        Args:
            content: Skill content to evaluate
            
        Returns:
            Comprehensive quality metrics with enhanced insights
        """
        metrics = super().evaluate(content)
        
        metrics.semantic_coherence = self._assess_semantic_coherence(content)
        metrics.practical_utility = self._assess_practical_utility(content)
        metrics.adaptability_score = self._assess_adaptability(content)
        
        metrics.overall_score = self._calculate_enhanced_overall_score(metrics)
        
        return metrics
    
    def _assess_semantic_coherence(self, content: str) -> float:
        """Assess semantic coherence and flow"""
        score = 0.5
        content_lower = content.lower()
        words = content_lower.split()
        
        transition_words = ['however', 'therefore', 'furthermore', 'additionally', 'moreover', 'thus', 'hence']
        transition_count = sum(1 for word in transition_words if word in content_lower)
        
        if transition_count >= 3:
            score += 0.2
        if transition_count >= 5:
            score += 0.15
        
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        if 3 <= len(paragraphs) <= 20:
            score += 0.15
        
        return min(score, 1.0)
    
    def _assess_practical_utility(self, content: str) -> float:
        """Assess practical utility and real-world applicability"""
        score = 0.4
        content_lower = content.lower()
        
        utility_indicators = ['example', 'usage', 'how to', 'step by step', 'implement', 'deploy']
        indicator_count = sum(1 for indicator in utility_indicators if indicator in content_lower)
        
        if indicator_count >= 2:
            score += 0.2
        if indicator_count >= 4:
            score += 0.2
        
        code_blocks = content.count('```')
        if code_blocks >= 2:
            score += 0.1
        if code_blocks >= 4:
            score += 0.1
        
        return min(score, 1.0)
    
    def _assess_adaptability(self, content: str) -> float:
        """Assess adaptability and customization potential"""
        score = 0.5
        content_lower = content.lower()
        
        adaptability_indicators = ['customize', 'configure', 'parameter', 'option', 'modify', 'extend']
        indicator_count = sum(1 for indicator in adaptability_indicators if indicator in content_lower)
        
        if indicator_count >= 2:
            score += 0.2
        if indicator_count >= 4:
            score += 0.2
        
        config_sections = ['configuration', 'options', 'parameters', 'settings']
        if any(section in content_lower for section in config_sections):
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_enhanced_overall_score(self, metrics: SkillQualityMetrics) -> float:
        """Calculate enhanced overall score with additional metrics"""
        base_score = super()._calculate_overall_score(metrics)
        
        enhanced_score = base_score * 0.7
        if hasattr(metrics, 'semantic_coherence'):
            enhanced_score += metrics.semantic_coherence * 0.1
        if hasattr(metrics, 'practical_utility'):
            enhanced_score += metrics.practical_utility * 0.1
        if hasattr(metrics, 'adaptability_score'):
            enhanced_score += metrics.adaptability_score * 0.1
        
        return min(enhanced_score, 1.0)


def create_skill_with_template(
    template_type: str,
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
    Create a skill using a smart template
    
    Args:
        template_type: Type of template to use
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
    factory = SkillFactory()
    
    template_content = SkillTemplate.generate_skill_structure(template_type, name, description)
    
    return factory.create_from_text(
        text=template_content,
        name=name,
        description=description,
        tags=tags,
        category=category,
        author=author,
        skill_type=skill_type,
        auto_optimize=auto_optimize,
        target_quality=target_quality
    )


def generate_skill_prototype(
    skill_def: SkillDefinition,
    scenario: str = "basic"
) -> str:
    """
    Generate an interactive prototype for a skill
    
    Args:
        skill_def: Skill definition to prototype
        scenario: Type of scenario to generate
        
    Returns:
        Interactive prototype code
    """
    from octopai.utils.config import Config
    config = Config()
    prototype = SkillInteractionPrototype(config)
    return prototype.generate_prototype(skill_def, scenario)

