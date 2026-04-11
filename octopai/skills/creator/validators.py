"""
Skill validator - validates generated skills for quality and completeness.
"""

import re
from typing import Any
from .models import GeneratedSkill


class SkillValidator:
    """Validates generated skills for quality and completeness."""

    def __init__(self, strict_mode: bool = False):
        """Initialize skill validator.

        Args:
            strict_mode: Enable strict validation rules
        """
        self.strict_mode = strict_mode

    def validate(self, skill: GeneratedSkill) -> tuple[bool, list[str], list[str]]:
        """Validate a generated skill.

        Args:
            skill: Skill to validate

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        self._validate_basic_fields(skill, errors, warnings)
        self._validate_content_structure(skill, errors, warnings)
        self._validate_markdown_quality(skill, errors, warnings)
        self._validate_code_blocks(skill, errors, warnings)
        self._validate_examples(skill, errors, warnings)

        is_valid = len(errors) == 0

        if is_valid:
            skill.validation_score = self._calculate_validation_score(skill, warnings)
            skill.status = "validated"
        else:
            skill.status = "invalid"

        return is_valid, errors, warnings

    def _validate_basic_fields(self, skill: GeneratedSkill, errors: list[str], warnings: list[str]) -> None:
        """Validate basic required fields."""
        if not skill.name or skill.name.strip() == "":
            errors.append("Skill name is required")

        if not skill.description or skill.description.strip() == "":
            warnings.append("Skill description is missing or empty")

        if not skill.version:
            warnings.append("Skill version is not specified")

        if not skill.category or skill.category.strip() == "":
            warnings.append("Skill category is not specified")

    def _validate_content_structure(self, skill: GeneratedSkill, errors: list[str], warnings: list[str]) -> None:
        """Validate content structure and sections."""
        if not skill.content or skill.content.strip() == "":
            errors.append("Skill content is empty")

        required_sections = ["Description", "Usage", "Examples"]
        for section in required_sections:
            if section not in skill.content:
                warnings.append(f"Missing recommended section: {section}")

        if "##" not in skill.content:
            warnings.append("Content lacks proper markdown heading structure")

    def _validate_markdown_quality(self, skill: GeneratedSkill, errors: list[str], warnings: list[str]) -> None:
        """Validate markdown formatting quality."""
        if not skill.content:
            return

        content = skill.content

        if not content.startswith("#"):
            warnings.append("Content should start with a main heading (#)")

        if "```" in content:
            code_block_count = content.count("```")
            if code_block_count % 2 != 0:
                errors.append("Unclosed code block detected")

        if "**" in content:
            bold_count = content.count("**")
            if bold_count % 2 != 0:
                warnings.append("Unclosed bold formatting detected")

        if len(content) < 200:
            warnings.append("Content is very short, may lack detail")

        if len(content) > 50000:
            warnings.append("Content is very long, consider splitting into sections")

    def _validate_code_blocks(self, skill: GeneratedSkill, errors: list[str], warnings: list[str]) -> None:
        """Validate code blocks in content."""
        if not skill.content:
            return

        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, skill.content, re.DOTALL)

        for lang, code in matches:
            if not code.strip():
                warnings.append(f"Empty code block found (language: {lang or 'none'})")

            if len(code) < 10:
                warnings.append(f"Very short code block (language: {lang or 'none'})")

            if lang and lang not in ["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust", "bash", "sh", "text"]:
                warnings.append(f"Uncommon code language: {lang}")

    def _validate_examples(self, skill: GeneratedSkill, errors: list[str], warnings: list[str]) -> None:
        """Validate examples section."""
        if not skill.content:
            return

        examples_section = self._extract_section(skill.content, "Examples")
        if not examples_section:
            warnings.append("No examples section found")
            return

        if len(examples_section) < 100:
            warnings.append("Examples section is very short")

        if "```" not in examples_section:
            warnings.append("Examples section lacks code blocks")

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from markdown content."""
        pattern = rf'##+\s*{section_name}\s*\n(.*?)(?=##+\s|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _calculate_validation_score(self, skill: GeneratedSkill, warnings: list[str]) -> float:
        """Calculate overall validation score (0.0 to 1.0)."""
        score = 0.5

        if skill.name:
            score += 0.1

        if skill.description:
            score += 0.1

        if len(skill.content) > 500:
            score += 0.1

        if "##" in skill.content:
            score += 0.05

        if "```" in skill.content:
            score += 0.05

        if len(warnings) == 0:
            score += 0.1

        return min(score, 1.0)

    def quick_validate(self, skill: GeneratedSkill) -> bool:
        """Quick validation check without detailed error reporting.

        Args:
            skill: Skill to validate

        Returns:
            True if skill passes basic validation
        """
        if not skill.name or not skill.content:
            return False

        if len(skill.content) < 100:
            return False

        return True
