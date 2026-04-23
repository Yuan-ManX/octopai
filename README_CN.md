<div align="center">

<img src="./assets/Octopai.png" alt="Octopai Logo" width="55%"/>

<p align="center">
  <h1 align="center">Octopai 🐙</h1>
</p>

<p align="center">
  <strong>AI Agent 探索、扩展、进化技能引擎 🚀</strong>
</p>

<p align="center">
  AI Agent Skill平台，包含Skill Creator、Skill Evolution、Skills Hub、OctoTrace、Skill Wiki和AutoSkill —— 使AI Agent能够不断学习、适应、进化和积累知识。
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

## 概述

Octopai是一个革命性的AI Agent Skills探索、扩展、进化智能引擎，其核心原则是：**万物皆可为Skill，Skill在学习中不断自我进化，提升AI Agent认知能力。**

将任何资源——网页、文档、视频、代码、数据集等——转化为结构化、可复用的Skill内容。通过智能学习和持续的自我进化，Skill会随着时间不断成长和改进。

## 核心理念

**使命：** 探索、扩展、进化AI Agent的认知

- **探索**互联网上海量的知识和各种文件格式的资源
- **扩展**AI Agent通过结构化、可复用的技能的能力
- **进化**技能通过智能反思和优化以匹配Agent需求

**原则：** 万物皆可为Skill，Skill在学习中不断进化

- **万物皆可为Skill**：任何资源都可以转化为结构化的、AI就绪的Skill
- **Skill在学习中不断进化**：每一个Skill都从使用、反馈和交互中持续学习，随着时间变得更加强大

## ✨ 核心功能

### 🔧 Skill Creator
从任何资源创建技能：
- **一键URL转换**：将URL转换为结构化Markdown
- **多格式解析器**：PDF、DOC、XLSX、PPTX、图片、视频等
- **技能模板**：预构建模板快速创建
- **质量评估**：智能质量评分和优化

### 🚀 Skill Evolution
先进的Feedback Descent算法：
- **前沿管理**：维护性能最佳的技能变体
- **选择策略**：最佳、轮询、加权、随机
- **进化模式**：仅技能、仅提示、混合
- **实时追踪**：OctoTrace性能监控

### 🏪 Skills Hub
全面的技能管理中心：
- **技能存储库**：组织、搜索和管理技能
- **版本控制**：跟踪技能进化历史
- **发布工作流**：草稿→评审→发布→归档
- **市场**：分享和发现技能
- **语义搜索**：智能搜索和发现

### 📊 OctoTrace
性能和成本追踪：
- **实时监控**：跟踪技能性能指标
- **成本追踪**：监控API成本和使用情况
- **可视化**：交互式性能仪表板

### 📚 Skill Wiki
知识管理系统：
- **知识图谱**：连接和概念
- **模式识别**：识别成功/失败模式
- **经验提炼**：从交互中提取和泛化
- **版本化文档**：跟踪知识进化

### 🤖 AutoSkill
自主研究和优化：
- **自动实验**：自动驱动技能实验
- **自动优化**：持续改进循环
- **发现管理**：跟踪发现和洞察

## 📦 安装

### 前置要求
- Python 3.8或更高版本
- OpenRouter API密钥（在[openrouter.ai](https://openrouter.ai)获取）

### 快速安装

```bash
# 克隆仓库
git clone https://github.com/Yuan-ManX/octopai.git
cd octopai

# 安装依赖
pip install -r requirements.txt

# 配置API密钥
cp .env.example .env
# 编辑 .env 填入您的API密钥
```

## 🚀 快速开始

### Python API

```python
from octopai import Octopai

# 初始化Octopai
octopai = Octopai()

# 将URL转换为技能
content = octopai.convert_url("https://example.com")

# 创建技能
skill = octopai.create_skill(
    name="数据分析器",
    description="分析CSV数据文件",
    content=content
)

# 开始进化
evolution = octopai.start_evolution(
    skill_id=skill.id,
    mode="hybrid"
)
```

### 命令行界面

```bash
# 将URL转换为Markdown
octopai convert https://example.com -o output.md

# 创建技能
octopai create "一个CSV分析技能" -n csv-analyzer

# 开始进化
octopai evolve csv-analyzer
```

### Web应用

```bash
# 启动后端（运行在 http://localhost:8000）
cd web/backend
python main.py

# 启动前端（运行在 http://localhost:5173）
cd web/frontend
npm install
npm run dev
```

## 📚 文档

提供完整的文档：
- **英文文档**：[docs/en/](./docs/en/index.md)
- **中文文档**：[docs/zh/](./docs/zh/index.md)

快速链接：
- [快速开始](./docs/zh/getting-started.md)
- [API参考](./docs/zh/api-reference.md)
- [示例](./docs/zh/examples.md)

## 🏗️ 架构

```
octopai/
├── octopai/              # 核心逻辑
│   ├── agents/          # Agent和进化
│   ├── skills/        # 技能创建
│   ├── evolution/    # 进化引擎
│   ├── tracing/     # OctoTrace
│   └── utils/       # 工具函数
├── web/               # Web应用
│   ├── backend/     # FastAPI后端
│   └── frontend/    # React前端
├── docs/              # 文档
└── examples/          # 使用示例
```

## 📄 许可证

MIT License - 详见[LICENSE](LICENSE)文件。

## 🤝 贡献

欢迎贡献！请参阅贡献指南（即将推出）。

## ⭐ 星标历史

如果您喜欢这个项目，请 ⭐ 给仓库加星！您的支持帮助我们成长！

<p align="center">
  <a href="https://star-history.com/#Yuan-ManX/Octopai&Date">
    <img src="https://api.star-history.com/svg?repos=Yuan-ManX/octopai&type=Date" />
  </a>
</p>

## 📞 支持与社区

- **问题**：[GitHub Issues](https://github.com/Yuan-ManX/octopai/issues)
- **文档**：[docs/](./docs/README.md)

---

**Octopai** - 赋能AI Agent探索、扩展和进化其认知能力。🐙✨
