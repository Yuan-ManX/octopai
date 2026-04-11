"""
Skill Template Registry
Manages reusable skill templates with mutation capabilities
"""

import random
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..models import SkillType, SkillTemplate, EvolvableSkill


class SkillTemplateRegistry:
    """Registry for skill templates with mutation capabilities"""

    def __init__(self):
        self.templates: Dict[str, SkillTemplate] = {}
        self._initialize_core_templates()

    def _initialize_core_templates(self):
        core_templates = [
            SkillTemplate(
                template_id="tpl_autonomous_executor_v2",
                name="Autonomous Task Executor",
                category=SkillType.TASK_EXECUTION,
                base_prompt="You are an autonomous executor. Objective: {objective}. Process: {process}. Constraints: {constraints}. Output format: {output_format}. Validate results before completion.",
                variables=["objective", "process", "constraints", "output_format"],
                output_format="JSON with status, result, confidence, validation",
                success_criteria=[
                    "Task completed within constraints",
                    "Output matches expected format",
                    "Confidence level above threshold",
                    "Results validated successfully"
                ]
            ),
            SkillTemplate(
                template_id="tpl_code_architect_v2",
                name="Code Architecture Generator",
                category=SkillType.CODE_GENERATION,
                base_prompt="Generate optimized {language} code for: {requirement}. Architecture pattern: {pattern}. Quality standards: {standards}. Include tests, documentation, and error handling.",
                variables=["language", "requirement", "pattern", "standards"],
                output_format="Code with architecture explanation, test cases, docs",
                success_criteria=[
                    "Code follows architecture patterns",
                    "All tests pass",
                    "Documentation complete",
                    "Error handling comprehensive"
                ]
            ),
            SkillTemplate(
                template_id="tpl_intelligent_analyzer_v2",
                name="Intelligent Data Analyzer",
                category=SkillType.DATA_ANALYSIS,
                base_prompt="Analyze dataset: {dataset_description}. Goal: {analysis_goal}. Methodology: {method}. Provide insights, visualizations description, and actionable recommendations.",
                variables=["dataset_description", "analysis_goal", "method"],
                output_format="Analysis report with insights, charts description, recommendations",
                success_criteria=[
                    "Insights are novel and actionable",
                    "Statistical methods applied correctly",
                    "Patterns identified and explained",
                    "Recommendations provided"
                ]
            ),
            SkillTemplate(
                template_id="tpl_deep_researcher_v2",
                name="Deep Research Specialist",
                category=SkillType.RESEARCH,
                base_prompt="Conduct comprehensive research on: {topic}. Scope: {scope}. Depth level: {depth}. Source types: {source_types}. Synthesize findings into structured report.",
                variables=["topic", "scope", "depth", "source_types"],
                output_format="Research report with sources, findings, methodology, conclusions",
                success_criteria=[
                    "Multiple credible sources cited",
                    "Logical synthesis of information",
                    "Novel insights generated",
                    "Methodology documented"
                ]
            ),
            SkillTemplate(
                template_id="tpl_professional_communicator_v2",
                name="Professional Content Creator",
                category=SkillType.COMMUNICATION,
                base_prompt="Create {content_type} for {target_audience}. Tone: {tone}. Key messages: {messages}. Style guide: {style}. Length: approximately {length}. Ensure clarity and engagement.",
                variables=["content_type", "target_audience", "tone", "messages", "style", "length"],
                output_format="Polished content with proper structure and formatting",
                success_criteria=[
                    "Clear and engaging messaging",
                    "Appropriate tone maintained",
                    "Well-structured content",
                    "Target audience addressed"
                ]
            ),
            SkillTemplate(
                template_id="tpl_tool_integration_expert_v2",
                name="Tool Integration Expert",
                category=SkillType.TOOL_USE,
                base_prompt="Utilize tool {tool_name} to accomplish: {task}. Parameters: {params}. Error handling strategy: {strategy}. Optimize for reliability and performance.",
                variables=["tool_name", "task", "params", "strategy"],
                output_format="Tool execution result with error handling and validation",
                success_criteria=[
                    "Tool invoked correctly",
                    "Errors handled gracefully",
                    "Results validated",
                    "Performance optimized"
                ]
            )
        ]

        for tpl in core_templates:
            self.templates[tpl.template_id] = tpl

    def get_template(self, template_id: str) -> Optional[SkillTemplate]:
        return self.templates.get(template_id)

    def get_templates_by_category(self, category: SkillType) -> List[SkillTemplate]:
        return [t for t in self.templates.values() if t.category == category]

    def generate_skill_from_template(self, template: SkillTemplate,
                                    context: Dict[str, Any]) -> EvolvableSkill:
        filled_prompt = template.base_prompt
        for var in template.variables:
            value = context.get(var, f"[{var}]")
            filled_prompt = filled_prompt.replace(f"{{{var}}}", str(value))

        version_suffix = f"{random.randint(2, 9)}.{random.randint(0, 9)}"
        skill = EvolvableSkill(
            skill_id=str(random.uuid4()),
            name=f"{template.name} v{version_suffix}",
            skill_type=template.category,
            description=context.get("description", template.name),
            version="1.0.0",
            prompt_template=filled_prompt,
            source_template_id=template.template_id,
            tags=[template.category.value, "template-generated", context.get("variant_type", "standard")],
            created_at=datetime.now()
        )

        template.usage_count += 1
        return skill

    def mutate_template(self, template: SkillTemplate,
                       mutation_type: str = "random") -> SkillTemplate:
        mutations = {
            "optimization": lambda p: p + " Apply optimization techniques for peak performance.",
            "robustness": lambda p: p + " Implement comprehensive error handling and edge case coverage.",
            "precision": lambda p: "Be precise and exact. " + p + " Validate all outputs rigorously.",
            "creativity": lambda p: p + " Think creatively and explore innovative approaches.",
            "efficiency": lambda p: p + " Optimize for speed and resource efficiency.",
            "comprehensive": lambda p: p + " Cover all aspects thoroughly. Consider edge cases."
        }

        mutator = mutations.get(mutation_type, random.choice(list(mutations.values())))
        new_base_prompt = mutator(template.base_prompt)

        variant_names = {
            "optimization": "Optimized",
            "robustness": "Robust",
            "precision": "Precise",
            "creativity": "Creative",
            "efficiency": "Efficient",
            "comprehensive": "Comprehensive"
        }

        new_version = f"{template.version}->{random.randint(2, 9)}.0"

        return SkillTemplate(
            template_id=str(random.uuid4()),
            name=f"{template.name} ({variant_names.get(mutation_type, 'Variant')})",
            category=template.category,
            base_prompt=new_base_prompt,
            variables=template.variables.copy(),
            output_format=template.output_format,
            min_quality_threshold=template.min_quality_threshold,
            success_criteria=template.success_criteria.copy(),
            usage_count=0,
            version=new_version
        )
