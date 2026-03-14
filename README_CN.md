<p align="center">
  <h1 align="center">EXO</h1>
</p>

<p align="center">
  <strong>AI Agent Skills 探索、扩展、进化框架</strong>
</p>

<p align="center">
  万物皆可为Skill • Skill在学习中不断自我进化 • 提升AI Agent认知能力
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  </a>
  <a href="https://github.com/Yuan-ManX/EXO">
    <img src="https://img.shields.io/github/stars/Yuan-ManX/EXO?style=social" alt="Stars">
  </a>
</p>

<div align="center">

#### [English](./README.md) | [中文文档](./README_CN.md)

</div>



## 概述

EXO是一个革命性的AI Agent Skills探索、扩展、进化框架，其核心原则是：**万物皆可为Skill • Skill在学习中不断自我进化 • 提升AI Agent认知能力**。服务于OpenClaw、Claude Code、Codex、Cursor等智能体系统，EXO将任何资源——网页、文档、视频、代码、数据集等——转化为结构化、可复用的Skill内容。通过智能学习和持续的自我进化，Skill会随着时间不断成长和改进，显著提升AI Agent的认知能力。

EXO的核心理念是知识不应是静态的。每一个用EXO创建的Skill都能从交互中持续学习，通过反思来自我完善，并不断进化，变得更强大、更全面，更好地适应AI Agent不断变化的需求。

## 核心理念

EXO的革命性理念围绕我们的基础使命和原则展开：

#### 使命：探索、扩展、进化AI Agent的认知

EXO的核心理念是通过三大支柱提升AI Agent的认知能力：

- **探索**互联网上海量的知识和各种文件格式的资源
- **扩展**AI Agent通过结构化、可复用的技能的能力
- **进化**技能通过智能反思和优化以匹配Agent需求

#### 原则：万物皆可为Skill，Skill在学习中不断进化

EXO的突破性方法建立在两个变革性原则之上：

- **万物皆可为Skill**：任何资源——网页、PDF、视频、代码、数据集、文章——都可以转化为结构化的、AI就绪的Skill
- **Skill在学习中不断进化**：每一个Skill都从使用、反馈和交互中持续学习，随着时间变得更加强大

这些原则和支柱共同构成了EXO的革命性生态系统，在这里万物皆可为Skill，每一个Skill都持续进化以扩展AI Agent的认知。


## ✨ 核心功能

### ⚡ 一键URL到Skill转换
将任何互联网资源即时转换为结构化、AI就绪的技能：
- **网页**：通过一条命令将URL转换为结构化Markdown
- **自动爬取**：获取并整理链接的资源
- **技能就绪输出**：直接可供Claude Code、Cursor等AI Agent使用

### 🧩 多格式资源解析器
解析并转换**任何文件格式**为技能就绪的资源：
- **文档**：PDF、DOC、DOCX
- **表格**：Excel (XLSX, XLS)、CSV
- **媒体**：图片 (JPG、PNG、GIF)、视频 (MP4、AVI、MOV)
- **网页**：HTML、带自动爬取的URL
- **文本**：Markdown、JSON、YAML、纯文本

### 🚀 智能进化引擎
先进的三阶段进化管道用于技能优化：
1. **执行器**：运行候选技能并捕获完整执行轨迹
2. **反思器**：分析失败并识别改进模式
3. **优化器**：基于洞察生成改进的候选技能

特性包括反射变异、系统感知合并和帕累托高效搜索。


### 💼 SkillHub - 集中式技能管理
在集中式存储库中存储、组织和进化您的技能：
- **持久化存储**：技能保存到磁盘，带有完整历史记录
- **版本控制**：跟踪技能进化，带有完整版本历史
- **智能搜索**：通过关键词、标签或类别查找相关技能
- **技能合并**：将互补技能合并为更强大的技能
- **使用分析**：跟踪技能使用情况和成功率

```python
from exo import EXO, hub_create, hub_search, hub_list, hub_stats

# 在SkillHub中创建技能
skill = hub_create(
    name="数据分析器",
    description="分析CSV数据文件",
    prompt="创建一个分析CSV数据的技能",
    tags=["数据", "csv", "分析"],
    category="数据处理"
)

# 搜索技能
results = hub_search("csv分析")

# 列出所有技能
all_skills = hub_list(category="数据处理")

# 获取统计信息
stats = hub_stats()
```

### 🔗 双接口：Python API + 命令行
以最适合您的方式使用EXO：
- **Python API**：直接导入到您的项目中，实现无缝集成
- **命令行**：通过终端快速操作和自动化


### 高级API
简化访问所有功能：
```python
from exo import EXO, convert, create, evolve, parse

# 将URL转换为技能
content = convert("https://example.com")

# 解析文件作为资源
resource = parse("document.pdf")

# 使用资源创建技能
skill = create("Analyze this data", resources=["data.csv", "ref.pdf"])

# 进化技能
evolved = evolve("skill.py", "Improve performance")
```

## 📦 安装

### 前置要求
- Python 3.8或更高版本
- OpenRouter API密钥（在[openrouter.ai](https://openrouter.ai)获取）
- Cloudflare API密钥（可选，用于增强的URL转换）

### 1. 克隆仓库
```bash
git clone https://github.com/Yuan-ManX/EXO.git
cd EXO
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
# 或者开发安装
pip install -e .
```

### 3. 配置API密钥
复制示例环境文件并填写您的值：

```bash
cp .env.example .env
# 编辑 .env 填入您的API密钥
```

您的 `.env` 文件应如下所示：
```env
# OpenRouter API配置（必需）
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Cloudflare API配置（可选）
CLOUDFLARE_API_KEY=your_cloudflare_api_key_here
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id_here

# 模型配置（可选）
EXO_MODEL=openai/gpt-5.4
```

## 🚀 快速开始

### Python API
```python
from exo import EXO

# 初始化EXO
exo = EXO()

# 将URL转换为Markdown
content = exo.convert_url("https://example.com")

# 解析文件作为资源
resource = exo.parse_file("data/document.pdf")
print(resource.to_skill_resource())

# 使用资源创建技能
skill = exo.create_skill(
    "Create a data analysis skill",
    resources=["data/sample.csv", "docs/reference.pdf"]
)

# 进化技能
evolved = exo.evolve_skill(
    "skills/my_skill.py",
    "Add better error handling and logging",
    iterations=5
)
```

### 命令行界面
```bash
# 将URL转换为Markdown
exo convert https://example.com -o output.md --crawler

# 解析文件为技能资源
exo parse document.pdf -o resource.md

# 创建技能
exo create "A CSV analysis skill" -n csv-analyzer -o skill.py

# 进化技能
exo evolve skill.py "Optimize for large files" -i 5

# 爬取网站
exo crawl https://example.com -o ./downloads
```

## 📚 文档

提供完整的中英文双语文档：

- **英文文档**：[docs/en/](./docs/en/index.md)
- **中文文档**：[docs/zh/](./docs/zh/index.md)

快速链接：
- [快速开始](./docs/zh/getting-started.md)
- [API参考](./docs/zh/api-reference.md)
- [CLI使用](./docs/zh/cli-usage.md)
- [示例](./docs/zh/examples.md)
- [高级主题](./docs/zh/advanced-topics.md)
- [FAQ](./docs/zh/faq.md)


## 🏗️ 项目架构

```
exo/
├── __init__.py           # 包导出
├── api.py                # 高级API接口
├── core/                 # 核心功能模块
│   ├── converter.py      # URL到Markdown转换
│   ├── crawler.py        # 网络爬取和资源下载
│   ├── creator.py        # 从描述创建技能
│   ├── evolver.py        # 技能进化接口
│   ├── evolution_engine.py # 先进的三阶段进化引擎
│   ├── resource_parser.py # 多格式文件解析器（PDF、DOC、Excel等）
│   └── skill_hub.py     # SkillHub - 集中式技能管理系统
├── cli/                  # 命令行界面
│   └── main.py           # 主命令入口点
├── utils/                # 工具函数
│   ├── config.py         # 配置管理
│   └── helpers.py        # 辅助函数
├── tests/                # 完整的测试套件
│   ├── test_converter.py
│   ├── test_creator.py
│   ├── test_evolver.py
│   ├── test_evolution_engine.py
│   ├── test_resource_parser.py
│   └── test_skill_hub.py
├── docs/                 # 文档（英文和中文）
│   ├── en/               # 英文文档
│   └── zh/               # 中文文档
└── examples/             # 使用示例
```


## 💡 技能进化系统

EXO 的进化引擎使用复杂的三阶段管道：

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│  执行器     │ ───▶ │   反思器    │ ───▶ │   优化器    │
│            │      │           │       │            │
│  运行候选,  │      │  分析轨迹   │       │  生成改进   │
│  捕获轨迹   │      │  进行诊断   │       │  的候选     │
└────────────┘      └────────────┘      └────────────┘
```

**关键概念：**
- **可操作辅助信息 (ASI)**：引导进化的诊断反馈
- **帕累托前沿**：维护在不同方面表现优秀的候选
- **反射变异**：基于失败分析的定向改进
- **系统感知合并**：结合多个候选的互补优势


## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。


## 🤝 贡献

我们欢迎贡献！请参阅我们的贡献指南（即将推出）了解如何开始。


## ⭐ 星标历史

如果您喜欢这个项目，请 ⭐ 给仓库加星。您的支持帮助我们成长！

<p align="center">
  <a href="https://star-history.com/#Yuan-ManX/EXO&Date">
    <img src="https://api.star-history.com/svg?repos=Yuan-ManX/EXO&type=Date" />
  </a>
</p>


## 📞 支持与社区

- **问题**：[GitHub Issues](https://github.com/Yuan-ManX/EXO/issues)
- **文档**：[docs/](./docs/README.md)


**EXO** - 赋能AI Agent探索、扩展和进化其认知能力。
