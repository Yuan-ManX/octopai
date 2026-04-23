<div align="center">

<img src="./assets/Octopai.png" alt="Octopai Logo" width="55%"/>

<p align="center">
  <h1 align="center">Octopai 🐙</h1>
</p>

<p align="center">
  <strong>The Infinite Evolution Skill Engine for AI Agents</strong>
</p>

<p align="center">
  An AI Agent Skill Platform featuring Skill Creator, Skill Evolution, Skills Hub, OctoTrace, Skill Wiki, and AutoSkill — empowering AI Agents to learn, adapt, evolve, and accumulate knowledge continuously.
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

Octopai is a revolutionary AI Agent Skills Exploration, Extension, and Evolution Intelligence Engine built on a powerful core principle: **Everything can be a Skill • Skills evolve through continuous learning • Elevating AI Agent cognition**.

Transform any resource—web pages, documents, videos, code, datasets, and more—into structured, reusable Skill content. Through intelligent learning and continuous self-evolution, Skills grow and improve over time.

## Core Philosophy

**Mission:** Explore, Extend, Evolve AI Agent Cognition

- **Explore** vast knowledge on the internet and various file formats
- **Extend** AI Agent capabilities through structured, reusable skills
- **Evolve** skills through intelligent reflection and optimization

**Principles:** Everything can be a Skill, Skills evolve through learning

- **Everything can be a Skill**: Transform any resource into structured, AI-ready Skills
- **Skills evolve through learning**: Every Skill continuously learns from usage, feedback, and interactions, growing more powerful over time

## ✨ Key Features

### 🔧 Skill Creator
Create skills from any resource:
- **One-click URL conversion**: Transform URLs into structured Markdown
- **Multi-format parser**: PDF, DOC, XLSX, PPTX, images, videos, etc.
- **Skill templates**: Pre-built templates for quick creation
- **Quality evaluation**: Intelligent quality scoring and optimization

### 🚀 Skill Evolution
Advanced Feedback Descent algorithm:
- **Frontier management**: Maintain top-performing skill variants
- **Selection strategies**: Best, round-robin, weighted, random
- **Evolution modes**: Skill-only, prompt-only, hybrid
- **Real-time tracing**: OctoTrace performance monitoring

### 🏪 Skills Hub
Comprehensive skill management center:
- **Skill repository**: Organize, search, and manage skills
- **Version control**: Track skill evolution history
- **Publishing workflow**: Draft → Review → Published → Archived
- **Marketplace**: Share and discover skills
- **Semantic search**: Intelligent search and discovery

### 📊 OctoTrace
Performance and cost tracing:
- **Real-time monitoring**: Track skill performance metrics
- **Cost tracking**: Monitor API costs and usage
- **Visualization**: Interactive performance dashboards

### 📚 Skill Wiki
Knowledge management system:
- **Knowledge graph**: Connect and concepts
- **Pattern recognition**: Identify success/failure patterns
- **Experience distillation**: Extract and generalize from interactions
- **Versioned documentation**: Track knowledge evolution

### 🤖 AutoSkill
Autonomous research and optimization:
- **Auto-experimentation**: Self-drive skill experiments
- **Auto-optimization**: Continuous improvement loop
- **Discovery management**: Track findings and insights

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Yuan-ManX/octopai.git
cd octopai

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

## 🚀 Quick Start

### Python API

```python
from octopai import Octopai

# Initialize Octopai
octopai = Octopai()

# Convert URL to skill
content = octopai.convert_url("https://example.com")

# Create a skill
skill = octopai.create_skill(
    name="Data Analyzer",
    description="Analyze CSV data files",
    content=content
)

# Start evolution
evolution = octopai.start_evolution(
    skill_id=skill.id,
    mode="hybrid"
)
```

### Command Line Interface

```bash
# Convert URL to Markdown
octopai convert https://example.com -o output.md

# Create a skill
octopai create "A CSV analysis skill" -n csv-analyzer

# Start evolution
octopai evolve csv-analyzer
```

### Web Application

```bash
# Start backend (runs on http://localhost:8000)
cd web/backend
python main.py

# Start frontend (runs on http://localhost:5173)
cd web/frontend
npm install
npm run dev
```

## 📚 Documentation

Comprehensive documentation available:
- **English Documentation**: [docs/en/](./docs/en/index.md)
- **中文文档**: [docs/zh/](./docs/zh/index.md)

Quick links:
- [Getting Started](./docs/en/getting-started.md)
- [API Reference](./docs/en/api-reference.md)
- [Examples](./docs/en/examples.md)

## 🏗️ Architecture

```
octopai/
├── octopai/              # Core logic
│   ├── agents/          # Agent & evolution
│   ├── skills/        # Skill creation
│   ├── evolution/    # Evolution engine
│   ├── tracing/     # OctoTrace
│   └── utils/       # Utilities
├── web/               # Web application
│   ├── backend/     # FastAPI backend
│   └── frontend/    # React frontend
├── docs/              # Documentation
└── examples/          # Usage examples
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions welcome! See guidelines (coming soon).

## ⭐ Star History

If you like this project, please ⭐ star the repo! Your support helps us grow!

<p align="center">
  <a href="https://star-history.com/#Yuan-ManX/Octopai&Date">
    <img src="https://api.star-history.com/svg?repos=Yuan-ManX/octopai&type=Date" />
  </a>
</p>

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/Yuan-ManX/octopai/issues)
- **Documentation**: [docs/](./docs/README.md)

---

**Octopai** - Empowering AI Agents to Explore, Extend, and Evolve their cognitive capabilities. 🐙✨
