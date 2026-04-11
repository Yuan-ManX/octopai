"""
Octopai Skill Templates - Reusable Skill Scaffolds

This module provides pre-built, reusable skill templates that
accelerate skill creation by providing ready-to-use scaffolds
for common use cases. Templates include placeholders, examples,
and best practices to guide skill development.

Octopai Template System Features:
- Pre-built templates for common skill categories
- Customizable placeholders for personalization
- Built-in examples and best practices
- Quick-start scaffolds for rapid skill development
- Category-specific templates with domain knowledge
"""

import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from datetime import datetime

from octopai.skills.spec import (
    OctopaiSkillSpec, SkillCategory, SkillExample, SkillGuideline
)


class TemplateCategory(Enum):
    """Categories of skill templates"""
    GENERAL = "general"
    DEVELOPMENT = "development"
    DOCUMENT = "document"
    DATA = "data"
    CREATIVE = "creative"
    ANALYSIS = "analysis"
    COMMUNICATION = "communication"
    RESEARCH = "research"
    AUTOMATION = "automation"


@dataclass
class SkillTemplate:
    """
    A reusable skill template with placeholders and structure
    """
    template_id: str
    name: str
    description: str
    category: TemplateCategory
    content_template: str
    placeholders: Dict[str, str] = field(default_factory=dict)
    default_examples: List[SkillExample] = field(default_factory=list)
    default_guidelines: List[SkillGuideline] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    
    def create_skill(
        self,
        name: str,
        description: str,
        author: Optional[str] = None,
        placeholder_values: Optional[Dict[str, str]] = None,
        custom_examples: Optional[List[SkillExample]] = None,
        custom_guidelines: Optional[List[SkillGuideline]] = None
    ) -> OctopaiSkillSpec:
        """
        Create a skill from this template
        
        Args:
            name: Name for the new skill
            description: Description for the new skill
            author: Optional author name
            placeholder_values: Values to replace placeholders
            custom_examples: Custom examples to add/override
            custom_guidelines: Custom guidelines to add/override
            
        Returns:
            OctopaiSkillSpec instance
        """
        content = self.content_template
        
        values = placeholder_values or {}
        for key, value in values.items():
            placeholder = f"{{{key}}}"
            content = content.replace(placeholder, value)
        
        examples = custom_examples if custom_examples is not None else self.default_examples
        guidelines = custom_guidelines if custom_guidelines is not None else self.default_guidelines
        
        skill_category = self._map_template_category(self.category)
        
        return OctopaiSkillSpec(
            name=name,
            description=description,
            version=self.version,
            author=author,
            category=skill_category,
            tags=self.tags.copy(),
            content=content,
            examples=examples,
            guidelines=guidelines
        )
    
    @staticmethod
    def _map_template_category(template_cat: TemplateCategory) -> SkillCategory:
        """Map TemplateCategory to SkillCategory"""
        mapping = {
            TemplateCategory.GENERAL: SkillCategory.GENERAL,
            TemplateCategory.DEVELOPMENT: SkillCategory.DEVELOPMENT,
            TemplateCategory.DOCUMENT: SkillCategory.DOCUMENT,
            TemplateCategory.DATA: SkillCategory.ANALYSIS,
            TemplateCategory.CREATIVE: SkillCategory.CREATIVE,
            TemplateCategory.ANALYSIS: SkillCategory.ANALYSIS,
            TemplateCategory.COMMUNICATION: SkillCategory.COMMUNICATION,
            TemplateCategory.RESEARCH: SkillCategory.RESEARCH,
            TemplateCategory.AUTOMATION: SkillCategory.AUTOMATION,
        }
        return mapping.get(template_cat, SkillCategory.GENERAL)


class SkillTemplateLibrary:
    """
    Library of pre-built skill templates for rapid skill creation
    """
    
    def __init__(self):
        self._templates: Dict[str, SkillTemplate] = {}
        self._load_builtin_templates()
    
    def _load_builtin_templates(self):
        """Load all built-in templates"""
        self._templates["general-purpose"] = self._create_general_purpose_template()
        self._templates["code-analysis"] = self._create_code_analysis_template()
        self._templates["document-processor"] = self._create_document_processor_template()
        self._templates["data-analyst"] = self._create_data_analyst_template()
        self._templates["content-writer"] = self._create_content_writer_template()
        self._templates["research-assistant"] = self._create_research_assistant_template()
        self._templates["task-automation"] = self._create_task_automation_template()
    
    def get_template(self, template_id: str) -> Optional[SkillTemplate]:
        """Get a template by ID"""
        return self._templates.get(template_id)
    
    def list_templates(self, category: Optional[TemplateCategory] = None) -> List[SkillTemplate]:
        """List all templates, optionally filtered by category"""
        templates = list(self._templates.values())
        if category:
            templates = [t for t in templates if t.category == category]
        return templates
    
    def register_template(self, template: SkillTemplate):
        """Register a custom template"""
        self._templates[template.template_id] = template
    
    @staticmethod
    def _create_general_purpose_template() -> SkillTemplate:
        """Create a general purpose skill template"""
        content = """# {skill_name}

## Overview
{overview}

## How to Use This Skill
1. {step_1}
2. {step_2}
3. {step_3}

## Best Practices
- Always {best_practice_1}
- Remember to {best_practice_2}
- Consider {best_practice_3}

## Key Concepts
- {concept_1}: {concept_1_description}
- {concept_2}: {concept_2_description}
"""
        
        placeholders = {
            "skill_name": "My Skill",
            "overview": "This skill helps with...",
            "step_1": "Understand the requirements",
            "step_2": "Apply the methodology",
            "step_3": "Validate the results",
            "best_practice_1": "test your approach",
            "best_practice_2": "document your process",
            "best_practice_3": "iterative improvement",
            "concept_1": "Key Concept",
            "concept_1_description": "Description of the key concept",
            "concept_2": "Secondary Concept",
            "concept_2_description": "Description of the secondary concept",
        }
        
        examples = [
            SkillExample(
                title="Basic Usage",
                description="Apply the skill to a simple scenario",
                input="Describe your task here",
                output="This is what the skill produces"
            )
        ]
        
        guidelines = [
            SkillGuideline(guideline="Start with clear objectives"),
            SkillGuideline(guideline="Break complex tasks into manageable steps"),
            SkillGuideline(guideline="Review and refine your approach"),
        ]
        
        return SkillTemplate(
            template_id="general-purpose",
            name="General Purpose Skill Template",
            description="A versatile template for creating general-purpose skills",
            category=TemplateCategory.GENERAL,
            content_template=content,
            placeholders=placeholders,
            default_examples=examples,
            default_guidelines=guidelines,
            tags=["general", "template", "starter"],
        )
    
    @staticmethod
    def _create_code_analysis_template() -> SkillTemplate:
        """Create a code analysis skill template"""
        content = """# {skill_name}

## Purpose
{purpose}

## Analysis Checklist
- [ ] Code structure and organization
- [ ] Code quality and readability
- [ ] Potential bugs and issues
- [ ] Performance considerations
- [ ] Security implications
- [ ] Documentation completeness

## Review Process
1. **Input Analysis**: {input_analysis}
2. **Pattern Recognition**: {pattern_recognition}
3. **Recommendation Generation**: {recommendation_generation}

## Code Quality Metrics
- Readability score
- Maintainability assessment
- Test coverage considerations
- Documentation quality
"""
        
        placeholders = {
            "skill_name": "Code Analyzer",
            "purpose": "Analyzes code for quality, bugs, and improvements",
            "input_analysis": "Understand the code's purpose and structure",
            "pattern_recognition": "Identify coding patterns and anti-patterns",
            "recommendation_generation": "Provide actionable improvement suggestions",
        }
        
        examples = [
            SkillExample(
                title="Python Code Review",
                description="Review a Python function for quality improvements",
                input="def calculate_sum(numbers):\n    total = 0\n    for n in numbers:\n        total += n\n    return total",
                output="This function is well-structured. Consider adding type hints and documentation."
            )
        ]
        
        guidelines = [
            SkillGuideline(guideline="Focus on actionable, specific feedback"),
            SkillGuideline(guideline="Balance constructive criticism with positive feedback"),
            SkillGuideline(guideline="Prioritize suggestions by impact and effort"),
        ]
        
        return SkillTemplate(
            template_id="code-analysis",
            name="Code Analysis Skill Template",
            description="Template for creating code review and analysis skills",
            category=TemplateCategory.DEVELOPMENT,
            content_template=content,
            placeholders=placeholders,
            default_examples=examples,
            default_guidelines=guidelines,
            tags=["development", "code-review", "analysis", "programming"],
        )
    
    @staticmethod
    def _create_document_processor_template() -> SkillTemplate:
        """Create a document processor skill template"""
        content = """# {skill_name}

## Document Processing Capabilities
- {format_1}: {format_1_description}
- {format_2}: {format_2_description}
- {format_3}: {format_3_description}

## Processing Workflow
1. **Document Ingestion**: {ingestion_step}
2. **Content Extraction**: {extraction_step}
3. **Analysis/Transformation**: {analysis_step}
4. **Output Generation**: {output_step}

## Supported Operations
- Text extraction and analysis
- Format conversion
- Content enhancement
- Metadata extraction
- Table and image handling
"""
        
        placeholders = {
            "skill_name": "Document Processor",
            "format_1": "PDF",
            "format_1_description": "Extract text, tables, and metadata from PDF files",
            "format_2": "DOCX",
            "format_2_description": "Read and write Word documents with formatting",
            "format_3": "XLSX",
            "format_3_description": "Process Excel spreadsheets and data tables",
            "ingestion_step": "Read and validate the input document",
            "extraction_step": "Extract text, tables, images, and metadata",
            "analysis_step": "Analyze content structure and semantics",
            "output_step": "Generate processed output in desired format",
        }
        
        examples = [
            SkillExample(
                title="PDF Text Extraction",
                description="Extract all text content from a PDF document",
                input="document.pdf",
                output="Complete text content extracted from the PDF"
            )
        ]
        
        guidelines = [
            SkillGuideline(guideline="Preserve document structure when possible"),
            SkillGuideline(guideline="Handle large documents efficiently"),
            SkillGuideline(guideline="Provide clear error messages for unsupported formats"),
        ]
        
        return SkillTemplate(
            template_id="document-processor",
            name="Document Processor Skill Template",
            description="Template for creating document processing and analysis skills",
            category=TemplateCategory.DOCUMENT,
            content_template=content,
            placeholders=placeholders,
            default_examples=examples,
            default_guidelines=guidelines,
            tags=["document", "pdf", "docx", "xlsx", "processing"],
        )
    
    @staticmethod
    def _create_data_analyst_template() -> SkillTemplate:
        """Create a data analyst skill template"""
        content = """# {skill_name}

## Analysis Framework
### Data Understanding
- {understanding_1}
- {understanding_2}
- {understanding_3}

### Analysis Methodology
1. **Data Preparation**: {preparation}
2. **Exploratory Analysis**: {exploration}
3. **Statistical Analysis**: {statistics}
4. **Insight Generation**: {insights}

## Visualization Guidelines
- Choose appropriate chart types
- Ensure clarity and readability
- Label axes and provide legends
- Use consistent color schemes
"""
        
        placeholders = {
            "skill_name": "Data Analyst",
            "understanding_1": "Examine data types and formats",
            "understanding_2": "Identify missing values and outliers",
            "understanding_3": "Understand relationships between variables",
            "preparation": "Clean and transform data for analysis",
            "exploration": "Explore distributions and patterns",
            "statistics": "Apply appropriate statistical tests",
            "insights": "Derive actionable insights from findings",
        }
        
        examples = [
            SkillExample(
                title="Sales Data Analysis",
                description="Analyze monthly sales data for trends",
                input="CSV file with date, product, and sales columns",
                output="Key insights, trends, and recommendations"
            )
        ]
        
        guidelines = [
            SkillGuideline(guideline="Always validate your assumptions"),
            SkillGuideline(guideline="Consider multiple analytical approaches"),
            SkillGuideline(guideline="Document limitations of your analysis"),
        ]
        
        return SkillTemplate(
            template_id="data-analyst",
            name="Data Analyst Skill Template",
            description="Template for creating data analysis and visualization skills",
            category=TemplateCategory.DATA,
            content_template=content,
            placeholders=placeholders,
            default_examples=examples,
            default_guidelines=guidelines,
            tags=["data", "analysis", "statistics", "visualization"],
        )
    
    @staticmethod
    def _create_content_writer_template() -> SkillTemplate:
        """Create a content writer skill template"""
        content = """# {skill_name}

## Writing Principles
- {principle_1}
- {principle_2}
- {principle_3}

## Content Structure
1. **Introduction**: {introduction}
2. **Main Content**: {main_content}
3. **Conclusion**: {conclusion}

## Style Guidelines
- Tone: {tone}
- Audience: {audience}
- Format: {format}
- Length: {length}
"""
        
        placeholders = {
            "skill_name": "Content Writer",
            "principle_1": "Clarity above all else",
            "principle_2": "Know your audience",
            "principle_3": "Structure for readability",
            "introduction": "Hook the reader and set context",
            "main_content": "Develop key points with supporting details",
            "conclusion": "Summarize and provide next steps",
            "tone": "Professional yet approachable",
            "audience": "Target audience for this content",
            "format": "Appropriate output format",
            "length": "Desired content length",
        }
        
        examples = [
            SkillExample(
                title="Blog Post Writing",
                description="Write an engaging blog post on a technical topic",
                input="Topic: The future of AI in healthcare",
                output="Complete blog post with introduction, sections, and conclusion"
            )
        ]
        
        guidelines = [
            SkillGuideline(guideline="Write for your specific audience"),
            SkillGuideline(guideline="Use active voice when possible"),
            SkillGuideline(guideline="Edit and revise before finalizing"),
        ]
        
        return SkillTemplate(
            template_id="content-writer",
            name="Content Writer Skill Template",
            description="Template for creating content generation and writing skills",
            category=TemplateCategory.CREATIVE,
            content_template=content,
            placeholders=placeholders,
            default_examples=examples,
            default_guidelines=guidelines,
            tags=["writing", "content", "creative", "communication"],
        )
    
    @staticmethod
    def _create_research_assistant_template() -> SkillTemplate:
        """Create a research assistant skill template"""
        content = """# {skill_name}

## Research Process
### 1. Topic Definition
- {topic_definition}
- {scope_setting}

### 2. Information Gathering
- {source_identification}
- {information_extraction}

### 3. Analysis & Synthesis
- {pattern_identification}
- {insight_development}

### 4. Reporting
- {findings_presentation}
- {recommendations}

## Source Evaluation Criteria
- Credibility and authority
- Timeliness and relevance
- Bias and objectivity
- Methodology and rigor
"""
        
        placeholders = {
            "skill_name": "Research Assistant",
            "topic_definition": "Clearly define the research question",
            "scope_setting": "Establish boundaries for the research",
            "source_identification": "Identify credible information sources",
            "information_extraction": "Extract relevant data and insights",
            "pattern_identification": "Identify patterns across sources",
            "insight_development": "Develop synthesized insights",
            "findings_presentation": "Present findings in a structured way",
            "recommendations": "Provide actionable recommendations",
        }
        
        examples = [
            SkillExample(
                title="Market Research",
                description="Research market trends in a specific industry",
                input="Industry: Renewable Energy Technologies",
                output="Comprehensive research report with key trends and insights"
            )
        ]
        
        guidelines = [
            SkillGuideline(guideline="Always cite your sources"),
            SkillGuideline(guideline="Cross-verify information across multiple sources"),
            SkillGuideline(guideline="Acknowledge limitations and gaps in research"),
        ]
        
        return SkillTemplate(
            template_id="research-assistant",
            name="Research Assistant Skill Template",
            description="Template for creating research and investigation skills",
            category=TemplateCategory.RESEARCH,
            content_template=content,
            placeholders=placeholders,
            default_examples=examples,
            default_guidelines=guidelines,
            tags=["research", "investigation", "analysis", "reporting"],
        )
    
    @staticmethod
    def _create_task_automation_template() -> SkillTemplate:
        """Create a task automation skill template"""
        content = """# {skill_name}

## Automation Scope
- {task_1}: {task_1_description}
- {task_2}: {task_2_description}
- {task_3}: {task_3_description}

## Execution Workflow
1. **Preparation**: {preparation_step}
2. **Execution**: {execution_step}
3. **Validation**: {validation_step}
4. **Cleanup**: {cleanup_step}

## Error Handling
- Identify potential failure points
- Implement recovery procedures
- Provide meaningful error messages
- Log execution details
"""
        
        placeholders = {
            "skill_name": "Task Automator",
            "task_1": "File Processing",
            "task_1_description": "Automatically process files in a directory",
            "task_2": "Data Transformation",
            "task_2_description": "Transform data between formats",
            "task_3": "Report Generation",
            "task_3_description": "Generate reports from processed data",
            "preparation_step": "Set up environment and validate inputs",
            "execution_step": "Execute the automated task sequence",
            "validation_step": "Verify results are correct",
            "cleanup_step": "Clean up temporary resources",
        }
        
        examples = [
            SkillExample(
                title="Batch File Processing",
                description="Process multiple files in batch mode",
                input="Directory containing CSV files",
                output="Processed files and summary report"
            )
        ]
        
        guidelines = [
            SkillGuideline(guideline="Design for idempotency when possible"),
            SkillGuideline(guideline="Provide clear logging and auditing"),
            SkillGuideline(guideline="Include safety checks and confirmations"),
        ]
        
        return SkillTemplate(
            template_id="task-automation",
            name="Task Automation Skill Template",
            description="Template for creating automation and workflow skills",
            category=TemplateCategory.AUTOMATION,
            content_template=content,
            placeholders=placeholders,
            default_examples=examples,
            default_guidelines=guidelines,
            tags=["automation", "workflow", "batch", "processing"],
        )


__all__ = [
    'TemplateCategory',
    'SkillTemplate',
    'SkillTemplateLibrary'
]
