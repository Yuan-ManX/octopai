"""
Intelligent Content Analyzer - Advanced parsing and analysis for skill creation.

Provides intelligent content analysis capabilities:
- Automatic format detection
- Content quality scoring
- Structure extraction
- Semantic understanding
- Multi-language code analysis
- Document intelligence (tables, images, formulas)
"""

import re
import json
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ContentType(Enum):
    """Detected content types."""
    PLAIN_TEXT = "plain_text"
    MARKDOWN = "markdown"
    CODE = "code"
    DOCUMENT = "document"
    SPREADSHEET = "spreadsheet"
    PRESENTATION = "presentation"
    CONFIGURATION = "configuration"
    API_SPEC = "api_spec"
    DATA_SCHEMA = "data_schema"
    MIXED = "mixed"


class CodeLanguage(Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    GO = "go"
    RUST = "rust"
    RUBY = "ruby"
    PHP = "php"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    SHELL = "shell"
    SQL = "sql"
    HTML = "html"
    CSS = "css"
    YAML = "yaml"
    JSON_FMT = "json"
    XML = "xml"
    UNKNOWN = "unknown"


@dataclass
class ContentAnalysis:
    """Result of content analysis.

    Attributes:
        content_type: Detected primary content type
        language: Detected programming language (if code)
        quality_score: Overall quality score (0.0-1.0)
        complexity: Complexity assessment (low/medium/high)
        structure_score: How well-structured the content is
        completeness: How complete the content appears
        readability: Readability assessment
        sections: Extracted sections/headings
        key_entities: Important entities found (functions, classes, etc.)
        metadata: Additional analysis metadata
        suggestions: Improvement suggestions
        estimated_skill_type: What type of skill this could become
    """

    content_type: ContentType = ContentType.PLAIN_TEXT
    language: CodeLanguage = CodeLanguage.UNKNOWN
    quality_score: float = 0.0
    complexity: str = "medium"
    structure_score: float = 0.0
    completeness: float = 0.0
    readability: float = 0.0
    sections: List[Dict[str, Any]] = field(default_factory=list)
    key_entities: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)
    estimated_skill_type: str = "general"


@dataclass
class ExtractedSection:
    """A section extracted from content.

    Attributes:
        title: Section title/heading
        level: Heading level (1-6)
        content: Section content
        start_pos: Start character position
        end_pos: End character position
        tags: Semantic tags for this section
    """

    title: str = ""
    level: int = 1
    content: str = ""
    start_pos: int = 0
    end_pos: int = 0
    tags: List[str] = field(default_factory=list)


class IntelligentAnalyzer:
    """Advanced content analyzer for intelligent skill creation.

    Provides:
    - Automatic content type detection
    - Quality and complexity assessment
    - Structure extraction and analysis
    - Entity recognition (functions, classes, APIs)
    - Skill type recommendation
    - Improvement suggestions
    """

    def __init__(self):
        """Initialize the analyzer."""
        self._patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, Any]:
        """Compile regex patterns for analysis."""
        return {
            'markdown_heading': re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE),
            'code_block': re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL),
            'function_def': {
                'python': re.compile(r'def\s+(\w+)\s*\([^)]*\)\s*[:]', re.MULTILINE),
                'javascript': re.compile(r'(?:const|let|var|async)?\s*(?:function\s*)?(\w+)\s*\(', re.MULTILINE),
                'java': re.compile(r'(?:public|private|protected)?\s+(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(', re.MULTILINE),
                'go': re.compile(r'func\s+(?:\([^)]*\)\s+)?(\w+)\s*\(', re.MULTILINE),
                'rust': re.compile(r'fn\s+(\w+)\s*\([^)]*\)(?:\s*->\s*.+)?\s*\{', re.MULTILINE),
            },
            'class_def': {
                'python': re.compile(r'class\s+(\w+)(?:\s*\([^)]+\))?\s*:', re.MULTILINE),
                'javascript': re.compile(r'class\s+(\w+)(?:\s+extends\s+\w+)?\s*\{', re.MULTILINE),
                'java': re.compile(r'(?:public|private|protected)?\s+class\s+(\w+)', re.MULTILINE),
            },
            'import_stmt': {
                'python': re.compile(r'^import\s+.+|^from\s+.+\s+import', re.MULTILINE),
                'javascript': re.compile(r'require\s*\(.+\)|import\s+.+from', re.MULTILINE),
            },
            'yaml_front_matter': re.compile(r'^---\n(.+?)\n---', re.DOTALL | re.MULTILINE),
            'table': re.compile(r'\|.+\|\n[\s\-|]+\n\|.+\|', re.MULTILINE),
            'api_endpoint': re.compile(r'(?:@|app\.(?:get|post|put|delete|patch))\(["\']?(\w[^"\']*)["\']?', re.IGNORECASE),
            'html_tag': re.compile(r'<([a-zA-Z][a-zA-Z0-9]*)[^>]*(?:/>|>)'),
            'json_object': re.compile(r'\{(?:[^{}]|\{[^{}]*\})*\}'),
        }

    def analyze(self, content: str, filename: Optional[str] = None) -> ContentAnalysis:
        """Perform comprehensive content analysis.

        Args:
            content: Text content to analyze
            filename: Optional filename for hinting

        Returns:
            Complete ContentAnalysis object
        """
        if not content or not content.strip():
            return ContentAnalysis(quality_score=0.0)

        # Detect content type
        content_type = self._detect_content_type(content, filename)

        # Detect language if code
        language = self._detect_language(content, filename)

        # Extract structure
        sections = self._extract_sections(content)
        entities = self._extract_entities(content, language)

        # Calculate scores
        quality_score = self._calculate_quality(content, sections, entities)
        structure_score = self._calculate_structure_score(content, sections)
        completeness = self._calculate_completeness(content, sections)
        readability = self._calculate_readability(content)
        complexity = self._assess_complexity(content, entities)

        # Generate suggestions
        suggestions = self._generate_suggestions(
            content, content_type, language,
            quality_score, structure_score, completeness
        )

        # Recommend skill type
        skill_type = self._recommend_skill_type(
            content, content_type, language, entities
        )

        # Build metadata
        metadata = self._build_metadata(content, content_type, language, entities)

        return ContentAnalysis(
            content_type=content_type,
            language=language,
            quality_score=quality_score,
            complexity=complexity,
            structure_score=structure_score,
            completeness=completeness,
            readability=readability,
            sections=[{
                'title': s.title,
                'level': s.level,
                'content_length': len(s.content),
                'tags': s.tags,
            } for s in sections],
            key_entities=entities,
            metadata=metadata,
            suggestions=suggestions,
            estimated_skill_type=skill_type,
        )

    def _detect_content_type(self, content: str, filename: Optional[str] = None) -> ContentType:
        """Detect the primary type of content."""
        hints = []

        # Check for markdown features
        if re.search(r'^#{1,6}\s+', content, re.MULTILINE):
            hints.append(('markdown', 3))
        if '```' in content:
            hints.append(('code_blocks', 2))

        # Check for code patterns
        code_indicators = [
            (r'def\s+\w+\s*\(', 'python_function', 4),
            (r'function\s*\w+\s*\(', 'js_function', 4),
            (r'class\s+\w+[\(:]', 'class_definition', 3),
            (r'import\s+\w+', 'import_statement', 3),
            (r'#include\s*[<"]', 'cpp_include', 3),
            (r'package\s+\w+\s*;', 'java_package', 3),
            (r'func\s+\w+\s*\(', 'go_function', 3),
        ]

        for pattern, name, weight in code_indicators:
            if re.search(pattern, content):
                hints.append((name, weight))

        # Check for document features
        if re.search(r'\\section\{|\\chapter\{|\\begin\{', content):
            hints.append(('latex_document', 5))
        if re.search(r'<html|<body|<div', content):
            hints.append(('html_document', 4))

        # Check for configuration files
        if re.search(r'^[\w]+\s*:\s*$', content, re.MULTILINE) and not re.search(r'^#{1,6}\s+', content, re.MULTILINE):
            hints.append(('yaml_config', 2))

        # Check for JSON/API spec
        try:
            json.loads(content)
            hints.append(('json_data', 3))
        except ValueError:
            pass

        # Check filename extension hint
        if filename:
            ext = filename.split('.')[-1].lower()
            ext_map = {
                '.py': ('python_code', 10),
                '.js': ('javascript_code', 10),
                '.ts': ('typescript_code', 10),
                '.md': ('markdown', 8),
                '.json': ('json_data', 7),
                '.yml': ('yaml_config', 7),
                '.yaml': ('yaml_config', 7),
                '.html': ('html_document', 8),
                '.sql': ('sql_code', 9),
                '.sh': ('shell_script', 9),
            }
            if ext in ext_map:
                hints.append(ext_map[ext])

        if not hints:
            return ContentType.PLAIN_TEXT

        # Weight-based decision
        hints.sort(key=lambda x: x[1], reverse=True)
        top_type = hints[0][0]

        type_mapping = {
            'markdown': ContentType.MARKDOWN,
            'code_blocks': ContentType.MARKDOWN,
            'python_function': ContentType.CODE,
            'js_function': ContentType.CODE,
            'class_definition': ContentType.CODE,
            'import_statement': ContentType.CODE,
            'latex_document': ContentType.DOCUMENT,
            'html_document': ContentType.DOCUMENT,
            'yaml_config': ContentType.CONFIGURATION,
            'json_data': ContentType.DATA_SCHEMA,
            'python_code': ContentType.CODE,
            'javascript_code': ContentType.CODE,
            'typescript_code': ContentType.CODE,
            'sql_code': ContentType.CODE,
            'shell_script': ContentType.CODE,
        }

        return type_mapping.get(top_type, ContentType.MIXED)

    def _detect_language(self, content: str, filename: Optional[str] = None) -> CodeLanguage:
        """Detect programming language."""
        if filename:
            ext = filename.split('.')[-1].lower()
            ext_lang = {
                '.py': CodeLanguage.PYTHON,
                '.js': CodeLanguage.JAVASCRIPT,
                '.ts': CodeLanguage.TYPESCRIPT,
                '.java': CodeLanguage.JAVA,
                '.go': CodeLanguage.GO,
                '.rs': CodeLanguage.RUST,
                '.rb': CodeLanguage.RUBY,
                '.php': CodeLanguage.PHP,
                '.swift': CodeLanguage.SWIFT,
                '.kt': CodeLanguage.KOTLIN,
                '.sh': CodeLanguage.SHELL,
                '.sql': CodeLanguage.SQL,
                '.html': CodeLanguage.HTML,
                '.css': CodeLanguage.CSS,
                '.yaml': CodeLanguage.YAML,
                '.yml': CodeLanguage.YAML,
                '.json': CodeLanguage.JSON_FMT,
            }
            if ext in ext_lang:
                return ext_lang[ext]

        # Pattern-based detection
        scores = {}

        # Python indicators
        python_patterns = [r'def\s+\w+\s*\(', r'import\s+\w+', r'from\s+\w+\s+import',
                         r'self\.\w+', r'if __name__']
        scores[CodeLanguage.PYTHON] = sum(1 for p in python_patterns if re.search(p, content))

        # JavaScript/TypeScript indicators
        js_patterns = [r'const\s+\w+\s*=', r'let\s+\w+\s*=', r'var\s+\w+\s*=',
                       r'=>\s*\{', r'function\s*\w+\s*\(', r'module\.exports']
        scores[CodeLanguage.JAVASCRIPT] = sum(1 for p in js_patterns if re.search(p, content))

        # Java indicators
        java_patterns = [r'public\s+class\s+\w+', r'private\s+\w+',
                        r'System\.out\.print', r'public\s+static\s+void\s+main']
        scores[CodeLanguage.JAVA] = sum(1 for p in java_patterns if re.search(p, content))

        # Go indicators
        go_patterns = [r'func\s+\w+\s*\(', r'package\s+\w+',
                      r'\w+\s+\w+\s*:=\s*', r'fmt\.Print']
        scores[CodeLanguage.GO] = sum(1 for p in go_patterns if re.search(p, content))

        # Rust indicators
        rust_patterns = [r'fn\s+\w+\s*\(', r'let\s+mut\s+\w+',
                        r'use\s+::\w+::', r'impl\s+\w+\s*\{']
        scores[CodeLanguage.RUST] = sum(1 for p in rust_patterns if re.search(p, content))

        if not scores or max(scores.values()) == 0:
            return CodeLanguage.UNKNOWN

        return max(scores, key=scores.get)

    def _extract_sections(self, content: str) -> List[ExtractedSection]:
        """Extract structural sections from content."""
        sections = []
        pattern = self._patterns['markdown_heading']

        matches = list(pattern.finditer(content))
        for i, match in enumerate(matches):
            level = len(match.group(1))
            title = match.group(2).strip()
            start = match.start()

            # Find end of this section (start of next heading or end of content)
            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(content)

            section_content = content[start:end].strip()
            
            # Determine semantic tags
            tags = self._classify_section(title, section_content)

            sections.append(ExtractedSection(
                title=title,
                level=level,
                content=section_content,
                start_pos=start,
                end_pos=end,
                tags=tags,
            ))

        return sections

    def _classify_section(self, title: str, content: str) -> List[str]:
        """Classify a section with semantic tags."""
        tags = []

        title_lower = title.lower()
        content_lower = content.lower()

        # Type classification
        if any(word in title_lower for word in ['example', 'usage', 'demo']):
            tags.append('example')
        if any(word in title_lower for word in ['install', 'setup', 'config', 'requirement']):
            tags.append('installation')
        if any(word in title_lower for word in ['api', 'endpoint', 'method']):
            tags.append('api_reference')
        if any(word in title_lower for word in ['parameter', 'argument', 'option']):
            tags.append('parameter')
        if any(word in title_lower for word in ['return', 'response', 'output']):
            tags.append('output')
        if any(word in title_lower for word in ['error', 'exception', 'handling']):
            tags.append('error_handling')

        # Content-based classification
        if '```' in content:
            tags.append('has_code')
        if '| ' in content and '-' in content:
            tags.append('has_table')
        if '{' in content and '}' in content:
            tags.append('has_json')

        return tags

    def _extract_entities(self, content: str, language: CodeLanguage) -> List[Dict[str, Any]]:
        """Extract key entities from content."""
        entities = []

        # Extract functions
        func_pattern = self._patterns['function_def'].get(language.value)
        if func_pattern:
            for match in func_pattern.finditer(content):
                func_name = match.group(1)
                entities.append({
                    'type': 'function',
                    'name': func_name,
                    'language': language.value,
                    'position': match.start(),
                })

        # Extract classes
        class_pattern = self._patterns['class_def'].get(language.value)
        if class_pattern:
            for match in class_pattern.finditer(content):
                class_name = match.group(1)
                entities.append({
                    'type': 'class',
                    'name': class_name,
                    'language': language.value,
                    'position': match.start(),
                })

        # Extract imports/dependencies
        import_pattern = self._patterns['import_stmt'].get(language.value)
        if import_pattern:
            imports = set()
            for match in import_pattern.finditer(content):
                imp = match.group(0).strip()
                imports.add(imp)
            for imp in sorted(imports)[:20]:  # Limit to avoid huge lists
                entities.append({
                    'type': 'dependency',
                    'name': imp,
                    'language': language.value,
                })

        # Extract API endpoints (if applicable)
        api_pattern = self._patterns['api_endpoint']
        for match in api_pattern.finditer(content):
            endpoint = match.group(1)
            entities.append({
                'type': 'api_endpoint',
                'name': endpoint,
                'language': language.value,
            })

        return entities

    def _calculate_quality(self, content: str, sections: List[ExtractedSection],
                          entities: List[Dict]) -> float:
        """Calculate overall quality score."""
        score = 0.5  # Base score

        # Length factor
        length = len(content)
        if length > 50:
            score += 0.05
        if length > 200:
            score += 0.05
        if length > 1000:
            score += 0.05
        if length > 5000:
            score += 0.05

        # Structure factor
        if sections:
            has_multiple_levels = len(set(s.level for s in sections)) > 1
            if has_multiple_levels:
                score += 0.1

        # Entities factor
        if entities:
            entity_types = set(e['type'] for e in entities)
            diversity = min(len(entity_types) / 3, 0.15)
            score += diversity

        # Code quality heuristics
        if entities:
            func_count = sum(1 for e in entities if e['type'] == 'function')
            if func_count >= 3:
                score += 0.05
            if func_count >= 10:
                score += 0.05

        return min(score, 1.0)

    def _calculate_structure_score(self, content: str, sections: List[ExtractedSection]) -> float:
        """Calculate how well-structured the content is."""
        if not content:
            return 0.0

        score = 0.0

        # Has headings
        if re.search(r'^#{1,6}\s+', content, re.MULTILINE):
            score += 0.25

        # Has multiple sections
        if len(sections) >= 3:
            score += 0.2
        elif len(sections) >= 1:
            score += 0.1

        # Has proper hierarchy
        if sections:
            levels = [s.level for s in sections]
            if levels == sorted(levels):
                score += 0.15
            if len(set(levels)) > 1:
                score += 0.1

        # Has code blocks
        if '```' in content:
            score += 0.15

        # Has lists
        if re.search(r'^\s*[-*]\s+', content, re.MULTILINE):
            score += 0.1

        # Has tables
        if '|' in content and '-|' in content:
            score += 0.05

        return min(score, 1.0)

    def _calculate_completeness(self, content: str, sections: List[ExtractedSection]) -> float:
        """Estimate how complete the content is."""
        if not content:
            return 0.0

        score = 0.3  # Base score for having content

        # Check for common sections
        required_sections = ['description', 'usage', 'example', 'install', 'config']
        all_titles = ' '.join(s.title.lower() for s in sections)

        found = sum(1 for req in required_sections if req in all_titles)
        score += (found / len(required_sections)) * 0.5

        # Length adequacy
        if len(content) > 500:
            score += 0.1
        if len(content) > 2000:
            score += 0.1

        return min(score, 1.0)

    def _calculate_readability(self, content: str) -> float:
        """Assess readability of content."""
        if not content:
            return 0.0

        score = 0.5

        # Sentence/line length
        lines = content.split('\n')
        avg_len = sum(len(line.strip()) for line in lines if line.strip()) / max(len(lines), 1)

        if avg_len < 80:
            score += 0.15
        elif avg_len < 120:
            score += 0.1

        # Paragraph density
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        if paragraphs:
            avg_para_len = sum(len(p) for p in paragraphs) / len(paragraphs)
            if 50 < avg_para_len < 500:
                score += 0.15

        # Code vs text balance
        code_ratio = content.count('```') / len(content) * 200 if content else 0
        if 0.1 < code_ratio < 0.4:
            score += 0.1
        elif code_ratio <= 0.1:
            score += 0.05

        # Whitespace consistency
        trailing_spaces = sum(1 for line in lines if line.endswith(' ') or line.endswith('\t'))
        if trailing_spaces / len(lines) < 0.1:
            score += 0.1

        return min(score, 1.0)

    def _assess_complexity(self, content: str, entities: List[Dict]) -> str:
        """Assess overall complexity."""
        factors = []

        # Entity count
        if len(entities) > 20:
            factors.append('high')
        elif len(entities) > 10:
            factors.append('medium')

        # Nesting depth (rough estimate)
        max_indent = 0
        for line in content.split('\n'):
            indent = len(line) - len(line.lstrip())
            if indent > max_indent:
                max_indent = indent

        if max_indent > 24:
            factors.append('high')
        elif max_indent > 12:
            factors.append('medium')

        # Content length
        if len(content) > 5000:
            factors.append('high')
        elif len(content) > 2000:
            factors.append('medium')

        if 'high' in factors:
            return 'high'
        elif 'medium' in factors or factors:
            return 'medium'
        return 'low'

    def _generate_suggestions(self, content: str, content_type: ContentType,
                              language: CodeLanguage, quality: float,
                              structure: float, completeness: float) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []

        if quality < 0.6:
            suggestions.append("Consider adding more detailed documentation and examples")

        if structure < 0.5:
            suggestions.append("Add clear headings and organize content into logical sections")

        if completeness < 0.6:
            suggestions.append("Include usage examples, installation instructions, and error handling")

        if content_type == ContentType.CODE and language != CodeLanguage.UNKNOWN:
            suggestions.append(f"Add docstrings and type hints for {language.value} functions")

        if content_type == ContentType.MARKDOWN:
            if '```' not in content:
                suggestions.append("Add code examples in fenced code blocks")

        if len(suggestions) == 0:
            suggestions.append("Content looks good! Consider adding more examples for clarity")

        return suggestions[:5]  # Limit to top 5

    def _recommend_skill_type(self, content: str, content_type: ContentType,
                               language: CodeLanguage,
                               entities: List[Dict]) -> str:
        """Recommend what type of skill this should become."""
        type_scores = {}

        # Based on content type
        if content_type == ContentType.CODE:
            type_scores['code_execution'] = 0.9
            if language in [CodeLanguage.PYTHON, CodeLanguage.JAVASCRIPT]:
                type_scores['automation'] = 0.8
            if any(e['type'] == 'api_endpoint' for e in entities):
                type_scores['api_integration'] = 0.85

        if content_type in [ContentType.MARKDOWN, ContentType.DOCUMENT]:
            type_scores['knowledge_base'] = 0.8
            if any('example' in s.get('tags', []) for s in []):  # Would use sections
                type_scores['tutorial'] = 0.75

        if content_type == ContentType.CONFIGURATION:
            type_scores['configuration'] = 0.9
            type_scores['environment_setup'] = 0.7

        if content_type == ContentType.DATA_SCHEMA:
            type_scores['data_processing'] = 0.85
            type_scores['validation'] = 0.8

        # Based on entities
        func_count = sum(1 for e in entities if e['type'] == 'function')
        if func_count > 5:
            type_scores['utility_library'] = 0.75

        if not type_scores:
            return 'general'

        return max(type_scores, key=type_scores.get)

    def _build_metadata(self, content: str, content_type: ContentType,
                         language: CodeLanguage,
                         entities: List[Dict]) -> Dict[str, Any]:
        """Build comprehensive metadata about analyzed content."""
        return {
            'length': len(content),
            'line_count': content.count('\n') + 1,
            'word_count': len(content.split()),
            'char_count': len(content),
            'entity_count': len(entities),
            'function_count': sum(1 for e in entities if e['type'] == 'function'),
            'class_count': sum(1 for e in entities if e['type'] == 'class'),
            'dependency_count': sum(1 for e in entities if e['type'] == 'dependency'),
            'has_code_blocks': '```' in content,
            'has_tables': '|' in content and '-|' in content,
            'has_headings': bool(re.search(r'^#{1,6}\s+', content, re.MULTILINE)),
            'estimated_reading_time_min': max(len(content.split()) / 200, 1),
        }

    def get_analysis_summary(self, analysis: ContentAnalysis) -> Dict[str, Any]:
        """Get a human-readable summary of analysis results."""
        return {
            'content_type': analysis.content_type.value,
            'language': analysis.language.value,
            'quality_grade': self._score_to_grade(analysis.quality_score),
            'complexity': analysis.complexity,
            'recommended_skill_type': analysis.estimated_skill_type,
            'key_stats': {
                'sections_found': len(analysis.sections),
                'entities_found': len(analysis.key_entities),
                'functions_found': analysis.metadata.get('function_count', 0),
                'readability_score': f"{analysis.readability:.0%}",
            },
            'top_improvements': analysis.suggestions[:3],
        }

    @staticmethod
    def _score_to_grade(score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 0.9:
            return 'A'
        elif score >= 0.8:
            return 'B'
        elif score >= 0.7:
            return 'C'
        elif score >= 0.6:
            return 'D'
        else:
            return 'F'
