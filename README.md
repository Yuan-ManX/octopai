<div align="center">

<img src="./assets/Octopai.png" alt="Octopai Logo" width="65%"/>

<p align="center">
  <h1 align="center">Octopai 🐙</h1>
</p>

<p align="center">
  <strong>The Infinite Evolution Skill Engine for AI Agents.</strong>
</p>

<p align="center">
  An AI Agent Platform featuring Skill Creator, Evolution Workbench, Skills Hub, OctoTrace, AI Wiki, and AutoResearch — empowering AI agents to learn, adapt, evolve, and accumulate knowledge continuously.
</p>


<p align="center">
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  </a>
  <a href="https://github.com/Yuan-ManX/octopai">
    <img src="https://img.shields.io/github/stars/Yuan-ManX/octopai?style=social" alt="Stars">
  </a>
</p>


#### [English](./README.md) | [中文文档](./README_CN.md)


</div>



## Overview

Octopai is a revolutionary AI Agent Skills Exploration, Extension, and Evolution Intelligence Engine built on a powerful core principle: **Everything Can Be a Skill • Skills Evolve Through Continuous Learning • Elevating AI Agent Cognition**. Serving OpenClaw, Claude Code, Codex, Cursor, and other intelligent agent systems, Octopai transforms any resource — web pages, documents, videos, code, datasets, and more — into structured, reusable Skill content. Through intelligent learning and continuous self-evolution, Skills grow and improve over time, significantly enhancing the cognitive capabilities of AI Agents.

At the heart of Octopai lies the belief that knowledge should not be static. Every Skill created with Octopai can continuously learn from interactions, refine itself through reflection, and evolve to become more powerful, more comprehensive, and better suited to the evolving needs of AI Agents.

## Core Philosophy

Octopai's revolutionary philosophy is centered around our foundational mission and principles:


#### The Mission: Explore, Extend, Evolve AI Agent Cognition

At its core, Octopai exists to elevate AI Agent cognition through three fundamental pillars:

- **Explore** the vast knowledge available on the internet and in various file formats
- **Extend** the capabilities of AI Agents through structured, reusable skills
- **Evolve** skills through intelligent reflection and optimization to match Agent needs


#### The Principles: Everything Can Be a Skill, Skills Evolve Through Learning

Octopai's groundbreaking approach is built on two transformative principles:

- **Everything Can Be a Skill**: Any resource — web pages, PDFs, videos, code, datasets, articles — can be transformed into a structured, AI-ready Skill
- **Skills Evolve Through Learning**: Every Skill continuously learns from usage, feedback, and interactions, growing more powerful over time

Together, these principles and pillars form Octopai's revolutionary ecosystem where everything becomes a Skill, and every Skill continuously evolves to expand AI Agent cognition.


## ✨ Key Features

### ⚡ One-Click URL to Skill Conversion
Transform any internet resource into structured, AI-ready skills instantly:
- **Web Pages**: Convert URLs to structured Markdown with one command
- **Automatic Crawling**: Fetch and organize linked resources
- **Skill-Ready Output**: Directly usable by AI Agents like Claude Code, Cursor, etc.

### 🧩 Multi-Format Resource Parser
Parse and transform **any file format** into skill-ready resources:
- **Documents**: PDF, DOC, DOCX
- **Spreadsheets**: Excel (XLSX, XLS), CSV
- **Media**: Images (JPG, PNG, GIF), Videos (MP4, AVI, MOV)
- **Web**: HTML, URLs with automatic crawling
- **Text**: Markdown, JSON, YAML, plain text

### 🚀 Intelligent Evolution Engine
Advanced evolution engine with comprehensive capabilities:
- **Curriculum Learning**: Progressive skill development through structured levels
- **Goal-Oriented Evolution**: Directed evolution toward specific objectives
- **Self-Verification**: Automatic validation of skill improvements
- **Meta-Cognition**: Reflective learning and adaptive strategies
- **Adaptive Mutation**: Exploratory, refinement, and reflective mutation strategies

### 📋 Skill Specification - Standardized Skill Format
Defines a powerful, standardized format for skill creation and sharing:
- **OCTOPAI.md Format**: YAML frontmatter + Markdown content for comprehensive skill definition
- **Folder-Based Skills**: Support for skill folders with resources/, scripts/, and assets/ subdirectories
- **Rich Metadata**: Name, version, author, license, category, keywords, dependencies, and more
- **Trigger System**: Event-based skill activation with flexible trigger conditions
- **Skill Categories**: Organized by domain (code, data, content, research, automation, etc.)
- **Validation System**: Built-in validation for skill specifications

```python
from octopai import OctopaiSkillSpec, create_skill_folder

# Create a skill folder structure
skill_folder = create_skill_folder(
    name="data-analyzer",
    path="./skills"
)

# Define a skill specification
skill_spec = OctopaiSkillSpec(
    name="Data Analyzer",
    version="1.0.0",
    author="Octopai Team",
    category="data-processing",
    description="Analyze and visualize data from various sources",
    content="# Data Analyzer\n\nThis skill helps you analyze data..."
)

# Export to OCTOPAI.md
skill_spec.to_skill_md("./skills/data-analyzer/OCTOPAI.md")

# Import from OCTOPAI.md
loaded_spec = OctopaiSkillSpec.from_skill_md("./skills/data-analyzer/OCTOPAI.md")
```

### 🏪 Plugin Marketplace - Skill Repository
Comprehensive skill repository and plugin management system:
- **Skill Import/Export**: Import skills from folders and export to shareable formats
- **Repository Management**: Browse, search, and manage skill repositories
- **Version Management**: Track skill versions and updates
- **Dependency Resolution**: Automatic dependency management for skills
- **Installation System**: One-click skill installation from repositories
- **Skill Discovery**: Browse skills by category, popularity, ratings, and more

### 💼 SkillHub - Comprehensive Skill Management Center
Store, organize, evolve, and manage your skills in a centralized, intelligent repository:
- **Comprehensive Metadata**: Status, visibility, author, version, license, keywords, dependencies, and more
- **Persistent Storage**: Skills saved to disk with full history
- **Version Control**: Track skill evolution with complete version history
- **Version Diffing**: Compare versions with detailed change analysis
- **Rollback Capabilities**: Revert to previous versions instantly
- **Publishing Workflow**: Draft → Review → Published → Deprecated → Archived status management
- **Visibility Control**: Private, Internal, or Public visibility levels
- **Smart Collections**: Organize skills into curated collections
- **Tags & Categories**: Flexible categorization and tagging system
- **Skill Ratings**: User feedback and rating system
- **Semantic Search**: Intelligent search with token-based indexing and relevance scoring
- **Context Composition**: Compose skills into powerful context combinations
- **Skill Dependencies**: Track relationships between skills
- **Skill Merging**: Combine complementary skills into more powerful ones
- **Usage Analytics**: Track skill usage, success rates, and performance metrics

### 📄 Document Processing Skills
Powerful document processing capabilities for various formats:
- **PDF Skills**: Extract text, metadata, images, and structured content from PDF files
- **DOCX Skills**: Read, manipulate, and generate Word documents with rich formatting
- **XLSX Skills**: Process Excel spreadsheets, extract data, and perform calculations
- **PPTX Skills**: Extract text, images, and content from PowerPoint presentations
- **Unified Interface**: Consistent API across all document formats
- **Factory System**: Easy access to document processors through a unified factory

```python
from octopai import DocumentSkillFactory, PDFSkill, DOCXSkill

# Process a PDF file
pdf_processor = PDFSkill()
pdf_content = pdf_processor.extract_text("document.pdf")
pdf_metadata = pdf_processor.extract_metadata("document.pdf")

# Process a Word document
docx_processor = DOCXSkill()
doc_content = docx_processor.read_document("report.docx")
docx_processor.modify_document("report.docx", updates={"title": "New Title"})

# Use the factory for unified access
factory = DocumentSkillFactory()
processor = factory.get_processor("document.xlsx")
data = processor.extract_data("document.xlsx")
```

### 📝 Skill Template System
Pre-built skill templates for rapid skill creation:
- **Built-in Templates**: General-purpose, code-analysis, document-processor, data-analyst, content-writer, research-assistant, task-automation
- **Template Categories**: Organized templates by use case and domain
- **Custom Templates**: Create and save your own templates
- **Template Library**: Comprehensive library of ready-to-use templates
- **Quick Start**: Get started with skill development in minutes

```python
from octopai import SkillTemplateLibrary, TemplateCategory

# Access the template library
library = SkillTemplateLibrary()

# List available templates
templates = library.list_templates(category=TemplateCategory.DATA_ANALYSIS)

# Get a specific template
template = library.get_template("data-analyst")

# Use the template to create a skill
skill_content = template.render({
    "name": "My Data Analyzer",
    "description": "Custom data analysis skill",
    "data_sources": ["CSV", "Excel", "Database"]
})

# Create custom templates
from octopai import SkillTemplate
custom_template = SkillTemplate(
    name="my-template",
    category=TemplateCategory.CONTENT_WRITING,
    content="""# {{name}}\n\n{{description}}\n\n## Features\n{{#features}}\n- {{.}}\n{{/features}}"""
)
library.add_template(custom_template)
```

```python
from octopai import (
    Octopai, hub_create, hub_search, hub_list, hub_stats,
    hub_create_collection, hub_semantic_search, hub_publish
)

# Create a skill in SkillHub
skill = hub_create(
    name="Data Analyzer",
    description="Analyze CSV data files",
    prompt="Create a skill to analyze CSV data",
    tags=["data", "csv", "analysis"],
    category="data-processing"
)

# Create a collection
collection = hub_create_collection(
    name="Data Science Tools",
    description="Essential skills for data science",
    skill_ids=[skill.metadata.skill_id],
    tags=["data-science", "tools"]
)

# Semantic search with advanced scoring
results = hub_semantic_search("csv analysis", category="data-processing")

# Publish a skill
published = hub_publish(skill.metadata.skill_id, visibility="public")

# List all skills
all_skills = hub_list(category="data-processing")

# Get statistics
stats = hub_stats()
```

### 🔗 Dual Interface: Python API + CLI
Use Octopai in the way that works best for you:
- **Python API**: Import directly into your projects for seamless integration
- **Command-Line**: Quick operations and automation through the terminal

### 🌐 Web Application & REST API
Full-stack web application with comprehensive REST API:
- **Modern Web UI**: Beautiful, intuitive frontend for skill management
- **REST API Endpoints**: Complete API for all SkillHub operations
- **Async Task Management**: Background task processing with status tracking
- **Integration Ready**: Designed for easy integration with other systems

### 🔄 Workflow Engine - Advanced Skill Orchestration
Powerful workflow engine for orchestrating complex skill sequences:
- **Multi-Format Workflows**: YAML, JSON, and Markdown workflow definitions
- **Progressive Loading**: Skills loaded only when needed for optimal context usage
- **Conditional Execution**: Smart condition-based step execution
- **Retry & Timeout**: Built-in retry mechanisms and timeout handling
- **Python & Skill Actions**: Execute Python functions and existing skills seamlessly
- **API Integration**: Direct API calls as workflow steps

```python
from octopai import WorkflowEngine, WorkflowDefinition, WorkflowStep

# Initialize workflow engine
engine = WorkflowEngine()

# Create a workflow programmatically
workflow = WorkflowDefinition(
    name="Research Report Generator",
    version="1.0.0",
    description="Generates comprehensive research reports",
    author="Octopai Team",
    tags=["research", "reporting", "automation"],
    variables={"topic": "AI Agents", "output_format": "markdown"}
)

# Add workflow steps
workflow.steps.append(WorkflowStep(
    name="web_research",
    description="Research the topic online",
    action="skill:web_research",
    inputs={"query": "${topic}"},
    outputs=["research_data"]
))

workflow.steps.append(WorkflowStep(
    name="generate_report",
    description="Generate the final report",
    action="skill:report_generation",
    inputs={"data": "${research_data}", "format": "${output_format}"},
    outputs=["final_report"]
))

# Execute the workflow
results = await engine.execute_workflow(workflow)
print(results["final_report"])
```

### 🧠 Subtask Orchestrator - Intelligent Task Decomposition
Advanced system for decomposing and executing complex tasks:
- **Automatic Task Decomposition**: AI-powered task breakdown into parallelizable subtasks
- **Dependency Management**: Smart dependency resolution and execution ordering
- **Priority-Based Execution**: Dynamic prioritization of critical subtasks
- **Parallel Execution**: Concurrent execution of independent subtasks
- **Progress Tracking**: Real-time status monitoring and completion callbacks
- **Error Recovery**: Automatic retry and recovery from subtask failures

```python
from octopai import SubtaskOrchestrator

# Initialize orchestrator
orchestrator = SubtaskOrchestrator()

# Decompose a complex task
task_group = await orchestrator.decompose_task(
    main_task="Create a comprehensive website about AI Agents",
    context={"target_audience": "developers", "style": "modern"}
)

# Execute the decomposed tasks
result = await orchestrator.execute_subtask_group(task_group.id)

print(f"Completed {result['completed_count']} of {result['total_count']} tasks")
print("Results:", result["results"])
```

### 💾 Persistent Memory - User Preference Learning
Sophisticated memory system for personalized interactions:
- **Fact Memory**: Store and retrieve factual knowledge with confidence scoring
- **User Preferences**: Learn and adapt to user preferences over time
- **Conversation History**: Maintain structured summaries of past interactions
- **Writing Style**: Capture and apply user's writing style
- **Technical Stack**: Track user's technology preferences
- **Automatic Extraction**: AI-powered memory extraction from conversations
- **Contextual Retrieval**: Smart context injection based on current task

```python
from octopai import PersistentMemory

# Initialize memory system
memory = PersistentMemory()

# Store a fact
memory.add_fact(
    user_id="user_123",
    content="Prefers Python over JavaScript for data analysis",
    category="preference",
    source="conversation",
    confidence=0.9,
    tags=["programming", "data-analysis"]
)

# Set a user preference
memory.set_preference(
    user_id="user_123",
    key="output_format",
    value="markdown",
    category="formatting",
    description="Preferred output format for documents",
    strength=0.8
)

# Get memory context for a task
context = memory.get_memory_context(
    user_id="user_123",
    current_task="Generate a data analysis report"
)

print("User facts:", context["facts"])
print("User preferences:", context["preferences"])
```

### 🛡️ Sandbox Executor - Isolated Execution Environment
Secure, isolated execution environment for code and commands:
- **Session Management**: Create and manage isolated sandbox sessions
- **File System**: Complete virtual file system with uploads, workspace, and outputs
- **Command Execution**: Secure command execution with timeout and security policies
- **Python Execution**: Run Python code in isolated environments
- **Notebook Support**: Jupyter notebook cell execution
- **Security Policies**: Configurable allowed/blocked command lists
- **Execution History**: Complete audit trail of all operations

```python
from octopai import SandboxExecutor, SandboxConfig

# Initialize sandbox executor
executor = SandboxExecutor()

# Create a sandbox session with custom config
config = SandboxConfig(
    timeout=300,
    max_memory_mb=1024,
    enable_network=False
)
session = executor.create_session(config=config)

# Write a file
executor.write_file(
    session_id=session.id,
    file_path="workspace/analysis.py",
    content="""
import pandas as pd
data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
print(data.describe())
"""
)

# Execute Python code
result = await executor.execute_python_code(
    session_id=session.id,
    code="import pandas as pd; print(pd.__version__)"
)

print("Success:", result.success)
print("Output:", result.stdout)

# Get session summary
summary = executor.get_session_summary(session.id)
print("Session stats:", summary)
```

### 🔧 High-Level API
Simplified access to all functionality:
```python
from octopai import (
    Octopai, convert, create_from_url, create_from_files,
    create_from_prompt, optimize_skill, parse,
    hub_create_collection, hub_semantic_search, hub_publish,
    WorkflowEngine, SubtaskOrchestrator, PersistentMemory, SandboxExecutor,
    OctopaiSkillSpec, create_skill_folder,
    DocumentSkillFactory, PDFSkill, DOCXSkill, XLSXSkill, PPTXSkill,
    SkillTemplateLibrary, SkillTemplate, TemplateCategory
)

# Convert URL to skill content
content = convert("https://example.com")

# Parse files as resources
resource = parse("document.pdf")

# Create skills from various sources
skill1 = create_from_url(
    url="https://example.com",
    name="Web Analysis",
    description="Analyze web content"
)

skill2 = create_from_files(
    file_paths=["data.csv", "reference.pdf"],
    name="Data Processor",
    description="Process structured data"
)

skill3 = create_from_prompt(
    prompt="Create a skill to generate reports",
    name="Report Generator",
    description="Generate comprehensive reports"
)

# Optimize existing skills
optimized = optimize_skill(skill1, target_quality="excellent")

# Advanced SkillHub operations
collection = hub_create_collection(
    name="My Skills",
    description="My personal skill collection"
)

results = hub_semantic_search("report generation", status="published")
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))
- Cloudflare API key (optional, for enhanced URL conversion)

### 1. Clone the Repository
```bash
git clone https://github.com/Yuan-ManX/octopai.git
cd octopai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
# or for development installation
pip install -e .
```

### 3. Configure API Keys
Copy the example environment file and fill in your values:

```bash
cp .env.example .env
# Edit .env with your API keys
```

Your `.env` file should look like:
```env
# OpenRouter API Configuration (Required)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Cloudflare API Configuration (Optional)
CLOUDFLARE_API_KEY=your_cloudflare_api_key_here
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id_here

# Model Configuration (Optional)
OCTOPAI_MODEL=openai/gpt-5.4
```

## 🚀 Quick Start

### Python API
```python
from octopai import Octopai

# Initialize Octopai
octopai = Octopai()

# Convert URL to Markdown
content = octopai.convert_url("https://example.com")

# Parse files as resources
resource = octopai.parse_file("data/document.pdf")
print(resource.to_skill_resource())

# Create a skill with resources
skill = octopai.create_skill_in_hub(
    name="Data Analyzer",
    description="Analyze CSV data files",
    prompt="Create a skill to analyze CSV data",
    tags=["data", "csv", "analysis"],
    category="data-processing"
)

# Create a collection
collection = octopai.create_collection_in_hub(
    name="Data Science",
    description="Data science related skills",
    skill_ids=[skill.metadata.skill_id]
)

# Add a rating
rating = octopai.add_rating_to_skill_in_hub(
    skill_id=skill.metadata.skill_id,
    rating=5.0,
    feedback="Excellent skill!",
    reviewer="User"
)

# Semantic search
results = octopai.semantic_search_in_hub("csv analysis")

# Publish the skill
published = octopai.publish_skill_in_hub(skill.metadata.skill_id)
```

### Command Line Interface
```bash
# Convert URL to Markdown
octopai convert https://example.com -o output.md --crawler

# Parse a file to skill resource
octopai parse document.pdf -o resource.md

# Create a skill
octopai create "A CSV analysis skill" -n csv-analyzer -o skill.py

# Crawl a website
octopai crawl https://example.com -o ./downloads
```

## 📚 Documentation

Comprehensive documentation is available in both English and Chinese:

- **English Documentation**: [docs/en/](./docs/en/index.md)
- **中文文档**: [docs/zh/](./docs/zh/index.md)

Quick links:
- [Getting Started](./docs/en/getting-started.md)
- [API Reference](./docs/en/api-reference.md)
- [CLI Usage](./docs/en/cli-usage.md)
- [Examples](./docs/en/examples.md)
- [Advanced Topics](./docs/en/advanced-topics.md)
- [FAQ](./docs/en/faq.md)

## 🏗️ Project Architecture

```
octopai/
├── __init__.py           # Package exports
├── api.py                # High-level API interface
├── core/                 # Core functionality modules
│   ├── converter.py      # URL to Markdown conversion
│   ├── crawler.py        # Web crawling and resource download
│   ├── skill_factory.py  # Skill creation, optimization, and quality evaluation
│   ├── evolution_engine.py # Advanced evolution with curriculum learning and meta-cognition
│   ├── experience_tracker.py # Experience tracking with pattern recognition
│   ├── resource_parser.py # Multi-format file parser (PDF, DOC, Excel, etc.)
│   ├── skill_hub.py     # SkillHub - comprehensive skill management center
│   ├── skill_packager.py # Skill packaging and distribution
│   ├── pipeline.py      # End-to-end skill engineering pipeline
│   ├── skill_bank.py    # Hierarchical skill library system
│   ├── experience_distiller.py # Experience-based skill extraction system
│   ├── recursive_evolution.py # Dynamic skill evolution engine
│   ├── skill_registry.py # Advanced skill registry system
│   ├── workflow_engine.py # 🆕 Advanced workflow orchestration engine
│   ├── subtask_orchestrator.py # 🆕 Intelligent task decomposition & parallel execution
│   ├── persistent_memory.py # 🆕 User preference learning & persistent memory
│   └── sandbox_executor.py # 🆕 Isolated execution environment
├── api_integration/      # API integration layer
│   ├── __init__.py
│   ├── api.py           # Integration API with async task management
│   └── schemas.py       # Data schemas for API requests/responses
├── cli/                  # Command-line interface
│   └── main.py           # Main command entry point
├── utils/                # Utility functions
│   ├── __init__.py       # Utility module exports
│   ├── config.py         # Configuration management
│   └── helpers.py        # Helper functions
├── web/                  # Web application
│   ├── backend/         # FastAPI backend
│   │   ├── main.py       # Main FastAPI application
│   │   └── requirements.txt
│   └── frontend/        # React/Vite frontend
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── api/
│       │   └── App.jsx
│       └── package.json
├── tests/                # Comprehensive test suite
│   ├── test_converter.py
│   ├── test_creator.py   # Skill creator tests
│   ├── test_evolution_engine.py
│   ├── test_evolver.py   # Skill evolver tests
│   ├── test_resource_parser.py
│   └── test_skill_hub.py
├── docs/                 # Documentation (English & Chinese)
│   ├── en/               # English documentation
│   └── zh/               # Chinese documentation
└── examples/             # Usage examples
    ├── advanced_skill_evolution.py
    └── skill_registry_demo.py
```

## 🚀 Super Agent Capabilities

Octopai now features a comprehensive super agent architecture with:

```
┌─────────────────────────────────────────────────────────────────┐
│                      Octopai Super Agent                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Workflow Engine │  │Subtask Orchestrator│  │   Memory     │ │
│  │  & Skill Chains  │  │  & Parallel Exec  │  │   System     │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │ Sandbox Executor │  │    SkillHub      │  │   Evolution  │ │
│  │  & Code Runtime  │  │   & Skill Bank   │  │   Engine     │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Key Super Agent Features:**
- **Unified Orchestration**: Coordinate skills, workflows, and subtasks seamlessly
- **Adaptive Learning**: Continuous improvement through memory and experience
- **Secure Execution**: Isolated sandbox environments for all code execution
- **Personalization**: User-specific preferences and contextual adaptation
- **Scalability**: Parallel execution and intelligent resource management


## 💡 Skill Evolution System

Octopai's evolution engine uses a sophisticated system with multiple capabilities:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Curriculum     │ ──▶ │  Goal-Oriented  │ ──▶ │  Self-         │
│  Learning       │     │  Evolution      │     │  Verification   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                ▼
                       ┌─────────────────┐
                       │  Meta-Cognition  │
                       │  & Reflection    │
                       └─────────────────┘
```

**Key Concepts:**
- **Curriculum Learning**: Progressive skill development through structured difficulty levels
- **Goal-Oriented Evolution**: Directed evolution with specific objectives and priorities
- **Self-Verification**: Automatic validation and quality assurance
- **Meta-Cognitive Reflection**: Adaptive learning strategies based on experience
- **Pattern Recognition**: Identifying success and failure patterns from interactions
- **Knowledge Transfer**: Cross-skill knowledge sharing and transfer
- **Memory Consolidation**: Long-term memory formation and retrieval


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🤝 Contributing

We welcome contributions! Please see our contribution guidelines (coming soon) for details on how to get started.


## ⭐ Star History

If you like this project, please ⭐ star the repo. Your support helps us grow!

<p align="center">
  <a href="https://star-history.com/#Yuan-ManX/Octopai&Date">
    <img src="https://api.star-history.com/svg?repos=Yuan-ManX/octopai&type=Date" />
  </a>
</p>


## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/Yuan-ManX/octopai/issues)
- **Documentation**: [docs/](./docs/README.md)

