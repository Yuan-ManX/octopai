<div align="center">

<img src="./assets/Octopai.png" alt="Octopai Logo" width="65%"/>

<p align="center">
  <h1 align="center">Octopai 🐙</h1>
</p>

<p align="center">
  <strong>The AI Agent Evolution Intelligence Engine.</strong>
</p>

<p align="center">
  Everything Can Be a Skill • Skills Evolve Through Continuous Learning • Elevating AI Agent Cognition
</p>

<p align="center">
  Model(LLM) -> CPU • Agent -> OS • Skills -> Apps
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

### 🔧 High-Level API
Simplified access to all functionality:
```python
from octopai import (
    Octopai, convert, create_from_url, create_from_files,
    create_from_prompt, optimize_skill, parse,
    hub_create_collection, hub_semantic_search, hub_publish
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
│   └── skill_registry.py # Advanced skill registry system
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


**Octopai** - Empowering AI Agents to Explore, Extend, and Evolve their cognitive capabilities.
