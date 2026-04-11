"""
Main Skill Creator - orchestrates the complete skill creation workflow.
"""

import time
from typing import Any, Optional
from pathlib import Path

from .models import (
    CreationResult,
    GeneratedSkill,
    ParsedContent,
    SkillCreationRequest,
    SkillSource,
    SourceType,
)
from .parsers import (
    BaseParser,
    CodeParser,
    DocumentParser,
    MediaParser,
    PresentationParser,
    TemplateParser,
    TextParser,
)
from .generator import SkillGenerator
from .validators import SkillValidator
from .analyzer import IntelligentAnalyzer, ContentAnalysis


class SkillCreator:
    """Main skill creation orchestrator.

    Supports creating skills from various input types:
    - Text/Document inputs (Markdown, PDF, DOCX)
    - Code repositories (GitHub, local files)
    - Audio/Video content (transcription-based)
    - Presentations (PPT, Keynote)
    - Natural language descriptions
    - Existing skill templates

    Enhanced with intelligent content analysis for optimal skill generation.
    """

    def __init__(self, llm_client: Optional[Any] = None):
        """Initialize skill creator.

        Args:
            llm_client: Optional LLM client for enhanced generation
        """
        self.llm_client = llm_client

        self.parsers: dict[SourceType, BaseParser] = {
            SourceType.TEXT: TextParser(),
            SourceType.CODE: CodeParser(),
            SourceType.DOCUMENT: DocumentParser(),
            SourceType.AUDIO: MediaParser(),
            SourceType.VIDEO: MediaParser(),
            SourceType.PRESENTATION: PresentationParser(),
            SourceType.TEMPLATE: TemplateParser(),
            SourceType.URL: TextParser(),
            SourceType.NATURAL_LANGUAGE: TextParser(),
        }

        self.generator = SkillGenerator(llm_client=llm_client)
        self.validator = SkillValidator()
        self.analyzer = IntelligentAnalyzer()

    def analyze_content(self, content: str, filename: Optional[str] = None) -> ContentAnalysis:
        """Analyze content before skill creation.

        Args:
            content: Text content to analyze
            filename: Optional filename for hinting

        Returns:
            Complete content analysis with recommendations
        """
        return self.analyzer.analyze(content, filename)

    def create_skill(
        self,
        request: SkillCreationRequest,
        use_llm: bool = False,
    ) -> CreationResult:
        """Create a new skill from request.

        Args:
            request: Skill creation request with sources
            use_llm: Whether to use LLM for enhanced generation

        Returns:
            CreationResult containing generated skill or errors
        """
        start_time = time.time()

        if not request.sources:
            return CreationResult(
                success=False,
                errors=["No input sources provided"],
                processing_time_ms=(time.time() - start_time) * 1000,
            )

        try:
            all_parsed_contents = []
            source_analysis = {}

            for i, source in enumerate(request.sources):
                parsed_content = self._parse_source(source)

                if not parsed_content.raw_text and not parsed_content.structured_data:
                    return CreationResult(
                        success=False,
                        errors=[f"Failed to parse source {i + 1}: {source.source_type}"],
                        processing_time_ms=(time.time() - start_time) * 1000,
                    )

                all_parsed_contents.append(parsed_content)
                source_analysis[f"source_{i}"] = {
                    "type": str(source.source_type),
                    "quality_score": parsed_content.quality_score,
                    "content_length": len(parsed_content.raw_text),
                    "has_code": len(parsed_content.code_blocks) > 0,
                }

            merged_content = self._merge_parsed_contents(all_parsed_contents)

            if use_llm and self.llm_client:
                skill = self.generator.generate_with_llm(request, merged_content)
            else:
                skill = self.generator.generate(request, merged_content)

            is_valid, errors, warnings = self.validator.validate(skill)

            processing_time = (time.time() - start_time) * 1000

            return CreationResult(
                success=is_valid,
                skill=skill,
                errors=errors,
                warnings=warnings,
                processing_time_ms=processing_time,
                source_analysis=source_analysis,
            )

        except Exception as e:
            return CreationResult(
                success=False,
                errors=[f"Skill creation failed: {str(e)}"],
                processing_time_ms=(time.time() - start_time) * 1000,
            )

    def create_from_text(
        self,
        name: str,
        text_content: str,
        description: str = "",
        **kwargs,
    ) -> CreationResult:
        """Create skill from plain text or markdown content.

        Args:
            name: Skill name
            text_content: Text/markdown content
            description: Skill description
            **kwargs: Additional arguments for SkillCreationRequest

        Returns:
            CreationResult with generated skill
        """
        request = SkillCreationRequest(
            name=name,
            description=description,
            sources=[
                SkillSource(
                    source_type=SourceType.TEXT,
                    content=text_content,
                )
            ],
            **kwargs,
        )

        return self.create_skill(request)

    def create_from_code(
        self,
        name: str,
        file_path: str,
        description: str = "",
        **kwargs,
    ) -> CreationResult:
        """Create skill from code file or repository.

        Args:
            name: Skill name
            file_path: Path to code file
            description: Skill description
            **kwargs: Additional arguments for SkillCreationRequest

        Returns:
            CreationResult with generated skill
        """
        request = SkillCreationRequest(
            name=name,
            description=description,
            sources=[
                SkillSource(
                    source_type=SourceType.CODE,
                    file_path=file_path,
                )
            ],
            **kwargs,
        )

        return self.create_skill(request)

    def create_from_document(
        self,
        name: str,
        file_path: str,
        description: str = "",
        **kwargs,
    ) -> CreationResult:
        """Create skill from document file (PDF, DOCX).

        Args:
            name: Skill name
            file_path: Path to document file
            description: Skill description
            **kwargs: Additional arguments for SkillCreationRequest

        Returns:
            CreationResult with generated skill
        """
        request = SkillCreationRequest(
            name=name,
            description=description,
            sources=[
                SkillSource(
                    source_type=SourceType.DOCUMENT,
                    file_path=file_path,
                )
            ],
            **kwargs,
        )

        return self.create_skill(request)

    def create_from_media(
        self,
        name: str,
        file_path: str,
        media_type: str = "audio",
        description: str = "",
        **kwargs,
    ) -> CreationResult:
        """Create skill from audio/video content.

        Args:
            name: Skill name
            file_path: Path to media file
            media_type: Type of media ("audio" or "video")
            description: Skill description
            **kwargs: Additional arguments for SkillCreationRequest

        Returns:
            CreationResult with generated skill
        """
        request = SkillCreationRequest(
            name=name,
            description=description,
            sources=[
                SkillSource(
                    source_type=SourceType.AUDIO if media_type == "audio" else SourceType.VIDEO,
                    file_path=file_path,
                    metadata={"media_type": media_type},
                )
            ],
            **kwargs,
        )

        return self.create_skill(request)

    def create_from_presentation(
        self,
        name: str,
        file_path: str,
        description: str = "",
        **kwargs,
    ) -> CreationResult:
        """Create skill from presentation file (PPT, PPTX).

        Args:
            name: Skill name
            file_path: Path to presentation file
            description: Skill description
            **kwargs: Additional arguments for SkillCreationRequest

        Returns:
            CreationResult with generated skill
        """
        request = SkillCreationRequest(
            name=name,
            description=description,
            sources=[
                SkillSource(
                    source_type=SourceType.PRESENTATION,
                    file_path=file_path,
                )
            ],
            **kwargs,
        )

        return self.create_skill(request)

    def create_from_template(
        self,
        name: str,
        template_path: str,
        variables: dict[str, Any],
        description: str = "",
        **kwargs,
    ) -> CreationResult:
        """Create skill from existing template.

        Args:
            name: Skill name
            template_path: Path to template file
            variables: Template variables to fill in
            description: Skill description
            **kwargs: Additional arguments for SkillCreationRequest

        Returns:
            CreationResult with generated skill
        """
        template_path_obj = Path(template_path)
        if template_path_obj.exists():
            content = template_path_obj.read_text()
            for var_name, var_value in variables.items():
                content = content.replace(f"{{{{{var_name}}}}}", str(var_value))

            request = SkillCreationRequest(
                name=name,
                description=description,
                sources=[
                    SkillSource(
                        source_type=SourceType.TEMPLATE,
                        content=content,
                        file_path=template_path,
                    )
                ],
                config=variables,
                **kwargs,
            )

            return self.create_skill(request)
        else:
            return CreationResult(
                success=False,
                errors=[f"Template file not found: {template_path}"],
            )

    def create_from_url(
        self,
        name: str,
        url: str,
        description: str = "",
        **kwargs,
    ) -> CreationResult:
        """Create skill from URL content.

        Args:
            name: Skill name
            url: URL to fetch content from
            description: Skill description
            **kwargs: Additional arguments for SkillCreationRequest

        Returns:
            CreationResult with generated skill
        """
        try:
            import urllib.request

            with urllib.request.urlopen(url, timeout=10) as response:
                content = response.read().decode('utf-8')

            request = SkillCreationRequest(
                name=name,
                description=description,
                sources=[
                    SkillSource(
                        source_type=SourceType.URL,
                        content=content,
                        url=url,
                    )
                ],
                **kwargs,
            )

            return self.create_skill(request)

        except Exception as e:
            return CreationResult(
                success=False,
                errors=[f"Failed to fetch URL: {str(e)}"],
            )

    def _parse_source(self, source: SkillSource) -> ParsedContent:
        """Parse a single source using appropriate parser."""
        parser = self.parsers.get(source.source_type)

        if not parser:
            raise ValueError(f"No parser available for source type: {source.source_type}")

        source_dict = {
            "content": source.content,
            "file_path": source.file_path,
            "url": source.url,
            "metadata": source.metadata,
        }

        return parser.parse(source_dict)

    def _merge_parsed_contents(self, contents: list[ParsedContent]) -> ParsedContent:
        """Merge multiple parsed contents into one."""
        if len(contents) == 1:
            return contents[0]

        merged_raw_text = "\n\n---\n\n".join(c.raw_text for c in contents if c.raw_text)
        merged_code_blocks = []
        for c in contents:
            merged_code_blocks.extend(c.code_blocks)

        merged_structured_data = {}
        for c in contents:
            for key, value in c.structured_data.items():
                if key not in merged_structured_data:
                    merged_structured_data[key] = value
                elif isinstance(value, list):
                    if isinstance(merged_structured_data[key], list):
                        merged_structured_data[key].extend(value)
                elif isinstance(value, dict):
                    if isinstance(merged_structured_data[key], dict):
                        merged_structured_data[key].update(value)

        avg_quality = sum(c.quality_score for c in contents) / len(contents)

        return ParsedContent(
            raw_text=merged_raw_text,
            structured_data=merged_structured_data,
            code_blocks=merged_code_blocks,
            metadata={"merged": True, "source_count": len(contents)},
            quality_score=avg_quality,
        )
