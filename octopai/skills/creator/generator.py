"""
Skill generator - converts parsed content into skill definitions.
"""

import json
from typing import Any, Optional
from datetime import datetime

from .models import GeneratedSkill, ParsedContent, SourceType, SkillCreationRequest


class SkillGenerator:
    """Generates skill definitions from parsed content."""

    def __init__(self, llm_client: Optional[Any] = None):
        """Initialize skill generator.

        Args:
            llm_client: Optional LLM client for enhanced generation
        """
        self.llm_client = llm_client

    def generate(
        self,
        request: SkillCreationRequest,
        parsed_content: ParsedContent,
    ) -> GeneratedSkill:
        """Generate a skill from parsed content.

        Args:
            request: Skill creation request
            parsed_content: Parsed content from input source

        Returns:
            Generated skill definition
        """
        skill_id = self._generate_skill_id(request.name, request.version)

        skill_content = self._generate_skill_content(
            request,
            parsed_content,
        )

        metadata = self._generate_metadata(request, parsed_content)

        skill = GeneratedSkill(
            id=skill_id,
            name=request.name,
            description=request.description,
            version=request.version,
            category=request.category,
            tags=request.tags,
            content=skill_content,
            metadata=metadata,
            source_type=self._determine_source_type(request),
            created_at=datetime.now(),
            validation_score=0.0,
            status="draft",
        )

        return skill

    def _generate_skill_id(self, name: str, version: str) -> str:
        """Generate unique skill ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        clean_name = name.lower().replace(" ", "-").replace("_", "-")
        return f"{clean_name}-{version}-{timestamp}"

    def _generate_skill_content(
        self,
        request: SkillCreationRequest,
        parsed_content: ParsedContent,
    ) -> str:
        """Generate skill content in markdown format."""
        content_parts = [
            f"# {request.name}",
            "",
            f"**Version:** {request.version}",
            f"**Category:** {request.category}",
            f"**Author:** {request.author or 'Unknown'}",
            "",
            "## Description",
            "",
            request.description,
            "",
            "## Overview",
            "",
            self._generate_overview(parsed_content),
            "",
            "## Usage",
            "",
            self._generate_usage_instructions(parsed_content),
            "",
            "## Examples",
            "",
            self._generate_examples(parsed_content),
            "",
            "## Requirements",
            "",
            self._generate_requirements(parsed_content),
            "",
            "## Configuration",
            "",
            self._generate_configuration(request),
            "",
        ]

        return "\n".join(content_parts)

    def _generate_overview(self, parsed_content: ParsedContent) -> str:
        """Generate overview section from parsed content."""
        if parsed_content.structured_data.get("headings"):
            overview = "This skill provides the following capabilities:\n\n"
            for heading in parsed_content.structured_data["headings"][:5]:
                indent = "  " * (heading["level"] - 1)
                overview += f"{indent}- {heading['text']}\n"
            return overview

        if parsed_content.structured_data.get("functions"):
            overview = "This skill provides the following functions:\n\n"
            for func in parsed_content.structured_data["functions"][:10]:
                overview += f"- `{func}`\n"
            return overview

        if parsed_content.raw_text:
            preview = parsed_content.raw_text[:500]
            return f"{preview}..."

        return "No overview available."

    def _generate_usage_instructions(self, parsed_content: ParsedContent) -> str:
        """Generate usage instructions."""
        instructions = []

        if parsed_content.code_blocks:
            instructions.append("### Code Examples")
            instructions.append("")
            for i, block in enumerate(parsed_content.code_blocks[:3]):
                instructions.append(f"#### Example {i + 1}")
                instructions.append("")
                instructions.append(f"```{block['language']}")
                instructions.append(block['code'][:200])
                instructions.append("```")
                instructions.append("")

        if parsed_content.structured_data.get("imports"):
            instructions.append("### Dependencies")
            instructions.append("")
            for imp in parsed_content.structured_data["imports"][:10]:
                instructions.append(f"- `{imp}`")
            instructions.append("")

        return "\n".join(instructions) if instructions else "No specific usage instructions provided."

    def _generate_examples(self, parsed_content: ParsedContent) -> str:
        """Generate examples section."""
        examples = []

        if parsed_content.code_blocks:
            examples.append("### Code Examples")
            examples.append("")
            for i, block in enumerate(parsed_content.code_blocks[:2]):
                examples.append(f"#### Example {i + 1}")
                examples.append("")
                examples.append(f"```{block['language']}")
                examples.append(block['code'][:300])
                examples.append("```")
                examples.append("")

        if parsed_content.structured_data.get("paragraphs"):
            examples.append("### Text Examples")
            examples.append("")
            for i, para in enumerate(parsed_content.structured_data["paragraphs"][:2]):
                examples.append(f"#### Example {i + 1}")
                examples.append("")
                examples.append(para[:200])
                examples.append("")
                examples.append("---")
                examples.append("")

        return "\n".join(examples) if examples else "No examples available."

    def _generate_requirements(self, parsed_content: ParsedContent) -> str:
        """Generate requirements section."""
        requirements = []

        if parsed_content.structured_data.get("imports"):
            requirements.append("### Dependencies")
            requirements.append("")
            for imp in parsed_content.structured_data["imports"]:
                requirements.append(f"- `{imp}`")
            requirements.append("")

        if parsed_content.structured_data.get("language"):
            requirements.append("### Language")
            requirements.append("")
            requirements.append(f"- {parsed_content.structured_data['language']}")
            requirements.append("")

        return "\n".join(requirements) if requirements else "No specific requirements."

    def _generate_configuration(self, request: SkillCreationRequest) -> str:
        """Generate configuration section."""
        if not request.config:
            return "No configuration required."

        config_yaml = json.dumps(request.config, indent=2)
        return f"```yaml\n{config_yaml}\n```"

    def _generate_metadata(self, request: SkillCreationRequest, parsed_content: ParsedContent) -> dict[str, Any]:
        """Generate skill metadata."""
        return {
            "created_at": datetime.now().isoformat(),
            "author": request.author,
            "category": request.category,
            "tags": request.tags,
            "quality_score": parsed_content.quality_score,
            "source_type": parsed_content.metadata.get("source_type", "unknown"),
            "file_path": parsed_content.metadata.get("file_path"),
            "has_code": len(parsed_content.code_blocks) > 0,
            "code_count": len(parsed_content.code_blocks),
            "content_length": len(parsed_content.raw_text),
        }

    def _determine_source_type(self, request: SkillCreationRequest) -> SourceType:
        """Determine source type from request."""
        if request.sources:
            return request.sources[0].source_type
        return SourceType.TEXT

    def generate_with_llm(
        self,
        request: SkillCreationRequest,
        parsed_content: ParsedContent,
    ) -> GeneratedSkill:
        """Generate skill using LLM for enhanced content.

        Args:
            request: Skill creation request
            parsed_content: Parsed content from input source

        Returns:
            Generated skill with LLM-enhanced content
        """
        if not self.llm_client:
            return self.generate(request, parsed_content)

        prompt = self._build_llm_prompt(request, parsed_content)

        try:
            response = self.llm_client.generate(prompt)
            enhanced_content = self._parse_llm_response(response)

            skill = self.generate(request, parsed_content)
            skill.content = enhanced_content
            return skill
        except Exception as e:
            print(f"LLM generation failed: {e}")
            return self.generate(request, parsed_content)

    def _build_llm_prompt(self, request: SkillCreationRequest, parsed_content: ParsedContent) -> str:
        """Build prompt for LLM generation."""
        prompt = f"""Generate a comprehensive skill definition for:

**Skill Name:** {request.name}
**Description:** {request.description}
**Category:** {request.category}

**Source Content:**
{parsed_content.raw_text[:2000]}

**Structured Data:**
{json.dumps(parsed_content.structured_data, indent=2)}

Generate a well-structured skill definition in markdown format with:
1. Clear description and overview
2. Detailed usage instructions
3. Practical examples
4. Requirements and dependencies
5. Configuration options

Make the skill comprehensive, well-documented, and ready to use."""
        return prompt

    def _parse_llm_response(self, response: str) -> str:
        """Parse LLM response into skill content."""
        return response.strip()
