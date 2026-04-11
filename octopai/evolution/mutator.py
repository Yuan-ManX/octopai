"""
Skill Mutator - Generates mutations and variations of skills.

Implements various mutation strategies:
- Content modification (add, remove, rephrase sections)
- Parameter tuning
- Structural changes
- Crossover between variants
- LLM-guided mutation
"""

import random
import re
from typing import Any, Optional, List
from dataclasses import dataclass, field

from .config import SkillVariant, MutationRecord


@dataclass
class MutationProposal:
    """Proposal for a skill mutation.

    Attributes:
        mutation_type: Type of mutation to apply
        description: Human-readable description of the change
        target_section: Section to modify (e.g., "Usage", "Examples")
        proposed_change: Description of what to change
        confidence: Confidence score for this proposal (0.0-1.0)
        rationale: Why this mutation should be applied
    """

    mutation_type: str = "content_modification"
    description: str = ""
    target_section: str = ""
    proposed_change: str = ""
    confidence: float = 0.5
    rationale: str = ""


@dataclass
class MutationResult:
    """Result of applying a mutation.

    Attributes:
        success: Whether mutation was applied successfully
        new_content: Modified content after mutation
        original_content: Content before mutation
        record: Detailed mutation record
        errors: List of error messages if failed
    """

    success: bool = False
    new_content: str = ""
    original_content: str = ""
    record: Optional[MutationRecord] = None
    errors: List[str] = field(default_factory=list)


class SkillMutator:
    """Generates and applies mutations to skill variants.

    Supports multiple mutation strategies that can be combined or used individually.
    """

    MUTATION_TYPES = [
        "content_addition",
        "content_removal",
        "content_rephrase",
        "example_addition",
        "parameter_tuning",
        "structure_reorganization",
        "crossover",
        "llm_guided",
    ]

    def __init__(self, llm_client: Optional[Any] = None):
        """Initialize skill mutator.

        Args:
            llm_client: Optional LLM client for intelligent mutations
        """
        self.llm_client = llm_client

    def propose_mutations(
        self,
        variant: SkillVariant,
        failures: List[dict[str, Any]] = None,
        feedback_history: List[dict] = None,
        num_proposals: int = 3,
    ) -> List[MutationProposal]:
        """Generate mutation proposals based on variant state and context.

        Args:
            variant: Current skill variant
            failures: List of failure cases (if available)
            feedback_history: Historical feedback from past iterations
            num_proposals: Number of proposals to generate

        Returns:
            List of MutationProposal objects
        """
        proposals = []

        if failures and len(failures) > 0:
            proposals.extend(self._propose_from_failures(variant, failures))

        if len(proposals) < num_proposals:
            proposals.extend(self._propose_random(variant, num_proposals - len(proposals)))

        if self.llm_client and len(proposals) < num_proposals:
            llm_proposals = self._propose_with_llm(
                variant, failures, feedback_history, num_proposals - len(proposals)
            )
            proposals.extend(llm_proposals)

        return proposals[:num_proposals]

    def apply_mutation(
        self,
        variant: SkillVariant,
        proposal: MutationProposal,
    ) -> MutationResult:
        """Apply a mutation proposal to create a new variant.

        Args:
            variant: Original skill variant
            proposal: Mutation proposal to apply

        Returns:
            MutationResult with new content and details
        """
        original_content = variant.content

        try:
            if proposal.mutation_type == "content_addition":
                result = self._apply_content_addition(original_content, proposal)
            elif proposal.mutation_type == "content_removal":
                result = self._apply_content_removal(original_content, proposal)
            elif proposal.mutation_type == "content_rephrase":
                result = self._apply_content_rephrase(original_content, proposal)
            elif proposal.mutation_type == "example_addition":
                result = self._apply_example_addition(original_content, proposal)
            elif proposal.mutation_type == "parameter_tuning":
                result = self._apply_parameter_tuning(original_content, proposal)
            elif proposal.mutation_type == "structure_reorganization":
                result = self._apply_structure_reorganization(original_content, proposal)
            elif proposal.mutation_type == "crossover":
                result = original_content
            elif proposal.mutation_type == "llm_guided":
                result = self._apply_llm_guided(original_content, proposal)
            else:
                result = self._apply_generic_modification(original_content, proposal)

            record = MutationRecord(
                mutation_type=proposal.mutation_type,
                description=proposal.description,
                source_section=proposal.target_section,
                old_content=original_content,
                new_content=result,
                success=True,
            )

            return MutationResult(
                success=True,
                new_content=result,
                original_content=original_content,
                record=record,
            )

        except Exception as e:
            return MutationResult(
                success=False,
                new_content=original_content,
                original_content=original_content,
                errors=[str(e)],
            )

    def crossover(
        self,
        parent1: SkillVariant,
        parent2: SkillVariant,
    ) -> tuple[str, str]:
        """Perform crossover operation between two parent variants.

        Creates two child variants by combining parts of both parents.

        Args:
            parent1: First parent variant
            parent2: Second parent variant

        Returns:
            Tuple of two new content strings
        """
        sections1 = self._split_into_sections(parent1.content)
        sections2 = self._split_into_sections(parent2.content)

        if not sections1 or not sections2:
            return parent1.content, parent2.content

        crossover_point = random.randint(1, min(len(sections1), len(sections2)) - 1)

        child1_parts = sections1[:crossover_point] + sections2[crossover_point:]
        child2_parts = sections2[:crossover_point] + sections1[crossover_point:]

        child1 = "\n\n".join(child1_parts)
        child2 = "\n\n".join(child2_parts)

        return child1, child2

    def _propose_from_failures(
        self,
        variant: SkillVariant,
        failures: List[dict[str, Any]],
    ) -> List[MutationProposal]:
        """Generate proposals based on failure analysis."""
        proposals = []

        failure_types = set()
        for failure in failures:
            ftype = failure.get("type", "unknown")
            failure_types.add(ftype)

        for ftype in failure_types:
            if ftype == "missing_capability":
                proposals.append(MutationProposal(
                    mutation_type="content_addition",
                    description=f"Add missing capability handling",
                    target_section="Usage",
                    proposed_change="Add comprehensive error handling and edge case coverage",
                    confidence=0.7,
                    rationale=f"Failures indicate missing capability: {ftype}",
                ))
            elif ftype == "incorrect_output":
                proposals.append(MutationProposal(
                    mutation_type="content_rephrase",
                    description=f"Rephrase output generation logic",
                    target_section="Examples",
                    proposed_change="Improve output format and accuracy",
                    confidence=0.6,
                    rationale=f"Output quality issues detected: {ftype}",
                ))
            elif ftype == "poor_examples":
                proposals.append(MutationProposal(
                    mutation_type="example_addition",
                    description=f"Add more diverse examples",
                    target_section="Examples",
                    proposed_change="Include additional example cases",
                    confidence=0.65,
                    rationale=f"Example coverage insufficient: {ftype}",
                ))

        return proposals

    def _propose_random(
        self,
        variant: SkillVariant,
        count: int,
    ) -> List[MutationProposal]:
        """Generate random mutation proposals."""
        proposals = []
        sections = self._extract_section_names(variant.content)

        for _ in range(count):
            mutation_type = random.choice(self.MUTATION_TYPES[:-2])
            target = random.choice(sections) if sections else "Content"

            proposal = MutationProposal(
                mutation_type=mutation_type,
                description=f"Apply {mutation_type} to {target}",
                target_section=target,
                proposed_change=self._generate_change_description(mutation_type),
                confidence=random.uniform(0.3, 0.8),
                rationale="Random exploration mutation",
            )
            proposals.append(proposal)

        return proposals

    def _propose_with_llm(
        self,
        variant: SkillVariant,
        failures: List[dict[str, Any]],
        feedback_history: List[dict],
        count: int,
    ) -> List[MutationProposal]:
        """Use LLM to generate intelligent mutation proposals."""
        if not self.llm_client:
            return []

        prompt = f"""Analyze this skill and suggest improvements:

**Skill Name:** {variant.name}
**Current Score:** {variant.score}

**Skill Content (first 1500 chars):**
{variant.content[:1500]}

**Recent Failures:** {failures[:3] if failures else 'None'}

Suggest {count} specific improvements as JSON array with fields:
- mutation_type: one of [{', '.join(self.MUTATION_TYPES)}]
- description: brief description
- target_section: which section to modify
- proposed_change: what to change
- confidence: 0.0-1.0
- rationale: why this helps"""

        try:
            response = self.llm_client.generate(prompt)
            proposals = []
            for item in response.strip().split('\n'):
                if '{' in item:
                    import json
                    data = json.loads(item[item.index('{'):item.rindex('}')+1])
                    proposals.append(MutationProposal(**data))
            return proposals[:count]
        except Exception as e:
            print(f"LLM proposal generation failed: {e}")
            return []

    def _apply_content_addition(self, content: str, proposal: MutationProposal) -> str:
        """Add new content to a section."""
        section_pattern = rf'(##+\s+{re.escape(proposal.target_section)}.*?\n)'
        match = re.search(section_pattern, content, re.DOTALL | re.IGNORECASE)

        if match:
            insertion_point = match.end()
            new_text = f"\n\n{proposal.proposed_change}\n"
            return content[:insertion_point] + new_text + content[insertion_point:]
        else:
            return content + f"\n\n## {proposal.target_section}\n\n{proposal.proposed_change}\n"

    def _apply_content_removal(self, content: str, proposal: MutationProposal) -> str:
        """Remove content from a section."""
        lines = content.split('\n')
        in_target_section = False
        lines_to_remove = []

        for i, line in enumerate(lines):
            if re.match(rf'##+\s+{re.escape(proposal.target_section)}', line, re.IGNORECASE):
                in_target_section = True
            elif line.startswith('##') and in_target_section:
                break
            elif in_target_section:
                lines_to_remove.append(i)

        if lines_to_remove:
            for i in reversed(lines_to_remove):
                del lines[i]
            return '\n'.join(lines)

        return content

    def _apply_content_rephrase(self, content: str, proposal: MutationProposal) -> str:
        """Rephrase content in a section."""
        pattern = rf'(##+\s+{re.escape(proposal.target_section)}.*?\n)(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if match:
            before = match.group(1)
            old_content = match.group(2)
            new_content = f"{before}{proposal.proposed_change}\n"
            return content[:match.start()] + new_content + content[match.end():]

        return content

    def _apply_example_addition(self, content: str, proposal: MutationProposal) -> str:
        """Add examples to the Examples section."""
        examples_section = self._find_or_create_section(content, "Examples")
        new_example = f"""
### Example
```python
# {proposal.proposed_change}
result = skill_function(input_data)
print(result)
```
"""
        if examples_section:
            return content + new_example
        else:
            return content + f"\n\n## Examples\n{new_example}"

    def _apply_parameter_tuning(self, content: str, proposal: MutationProposal) -> str:
        """Tune parameters in Configuration section."""
        config_section = self._find_section(content, "Configuration")
        if config_section:
            updated_config = config_section + f"\n# Updated: {proposal.proposed_change}\n"
            return content.replace(config_section, updated_config)
        return content

    def _apply_structure_reorganization(self, content: str, proposal: MutationProposal) -> str:
        """Reorganize document structure."""
        sections = self._split_into_sections(content)
        if len(sections) > 2:
            random.shuffle(sections[1:-1])
            return "\n\n".join(sections)
        return content

    def _apply_llm_guided(self, content: str, proposal: MutationProposal) -> str:
        """Apply LLM-guided modification."""
        if not self.llm_client:
            return content

        prompt = f"""Improve this skill section:

**Target Section:** {proposal.target_section}
**Proposed Change:** {proposal.proposed_change}

**Current Content:**
{content[:2000]}

Return the improved complete content:"""
        try:
            return self.llm_client.generate(prompt)
        except Exception:
            return content

    def _apply_generic_modification(self, content: str, proposal: MutationProposal) -> str:
        """Apply generic text modification."""
        return content + f"\n\n<!-- Modified: {proposal.description} -->\n{proposal.proposed_change}\n"

    def _extract_section_names(self, content: str) -> List[str]:
        """Extract all markdown section names."""
        pattern = r'^##+\s+(.+)$'
        matches = re.findall(pattern, content, re.MULTILINE)
        return matches if matches else ["Content"]

    def _split_into_sections(self, content: str) -> List[str]:
        """Split content into major sections."""
        pattern = r'(^#+\s+.+$)'
        parts = re.split(pattern, content, flags=re.MULTILINE)

        sections = []
        current = ""

        for part in parts:
            if re.match(r'^#+\s+.+$', part, re.MULTILINE):
                if current.strip():
                    sections.append(current.strip())
                current = part
            else:
                current += part

        if current.strip():
            sections.append(current.strip())

        return sections

    def _find_section(self, content: str, section_name: str) -> Optional[str]:
        """Find and return a specific section's content."""
        pattern = rf'(##+\s+{re.escape(section_name)}.*?\n)(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(0) if match else None

    def _find_or_create_section(self, content: str, section_name: str) -> bool:
        """Check if section exists."""
        pattern = rf'^##+\s+{re.escape(section_name)}'
        return bool(re.search(pattern, content, re.MULTILINE | re.IGNORECASE))

    def _generate_change_description(self, mutation_type: str) -> str:
        """Generate generic change description for mutation type."""
        descriptions = {
            "content_addition": "Add new information and capabilities",
            "content_removal": "Remove redundant or outdated content",
            "content_rephrase": "Improve clarity and readability",
            "example_addition": "Include practical usage examples",
            "parameter_tuning": "Optimize configuration parameters",
            "structure_reorganization": "Improve document organization",
        }
        return descriptions.get(mutation_type, "Apply modifications")
