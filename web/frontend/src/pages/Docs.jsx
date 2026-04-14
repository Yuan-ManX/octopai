import React, { useState } from 'react'

function Docs() {
  const [activeSection, setActiveSection] = useState('getting-started')
  const [language, setLanguage] = useState('en')

  const docs = {
    en: {
      'getting-started': {
        title: 'Getting Started',
        content: `
# Getting Started

This guide will help you get up and running with Octopai in minutes.

## Prerequisites

- Python 3.8 or higher
- API keys for Cloudflare and OpenRouter

## Installation

### 1. Clone the Repository

\`\`\`bash
git clone https://github.com/Yuan-ManX/octopai.git
cd octopai
\`\`\`

### 2. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
# or for development installation
pip install -e .
\`\`\`

### 3. Configure API Keys

Create a \`.env\` file in the project root directory:

\`\`\`env
# Cloudflare API Configuration
CLOUDFLARE_API_KEY=your_cloudflare_api_key
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id

# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key
\`\`\`

## Quick Start

### Using the Python API

The simplest way to use Octopai is through the Python API:

\`\`\`python
import octopai

# Convert a URL to a skill
skill_dir = octopai.convert("https://example.com")
print(f"Skill created at: {skill_dir}")

# Full processing pipeline
final_skill_dir = octopai.process("https://example.com", evolve=True)
print(f"Final skill at: {final_skill_dir}")
\`\`\`
        `
      },
      'api-reference': {
        title: 'API Reference',
        content: `
# API Reference

## Core Functions

### octopai.convert()
Convert a URL or file to a skill.

\`\`\`python
octopai.convert(url_or_path, name=None, output_dir=None)
\`\`\`

### octopai.process()
Full processing pipeline with optional evolution.

\`\`\`python
octopai.process(url_or_path, evolve=False, iterations=3)
\`\`\`

### octopai.evolve()
Evolve an existing skill.

\`\`\`python
octopai.evolve(skill_path, iterations=5, feedback=None)
\`\`\`
        `
      },
      'examples': {
        title: 'Examples',
        content: `
# Examples

## Basic URL to Skill

\`\`\`python
import octopai

# Convert a documentation page
skill = octopai.convert("https://example.com/docs")
print(f"Created skill: {skill}")
\`\`\`

## With Evolution

\`\`\`python
import octopai

# Process and evolve
final_skill = octopai.process(
    "https://example.com/guide",
    evolve=True,
    iterations=5
)
\`\`\`
        `
      },
      'faq': {
        title: 'FAQ',
        content: `
# FAQ

## What is Octopai?

Octopai is an AI Agent Skills Exploration, Extension, and Evolution Framework.

## How does skill evolution work?

Octopai uses a three-stage evolution pipeline: Executor → Reflector → Optimizer.

## What file formats are supported?

PDF, DOC, DOCX, XLSX, CSV, images, videos, and more!
        `
      }
    },
    zh: {
      'getting-started': {
        title: '快速开始',
        content: `
# 快速开始

本指南将帮助您在几分钟内启动并运行Octopai。

## 前置要求

- Python 3.8或更高版本
- Cloudflare和OpenRouter的API密钥

## 安装

### 1. 克隆仓库

\`\`\`bash
git clone https://github.com/Yuan-ManX/octopai.git
cd octopai
\`\`\`

### 2. 安装依赖

\`\`\`bash
pip install -r requirements.txt
# 或者开发安装
pip install -e .
\`\`\`

### 3. 配置API密钥

在项目根目录创建\`.env\`文件：

\`\`\`env
# Cloudflare API配置
CLOUDFLARE_API_KEY=your_cloudflare_api_key
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id

# OpenRouter API配置
OPENROUTER_API_KEY=your_openrouter_api_key
\`\`\`

## 快速开始

### 使用Python API

使用Octopai最简单的方式是通过Python API：

\`\`\`python
import octopai

# 将URL转换为skill
skill_dir = octopai.convert("https://example.com")
print(f"Skill创建于: {skill_dir}")

# 完整处理流程
final_skill_dir = octopai.process("https://example.com", evolve=True)
print(f"最终Skill位于: {final_skill_dir}")
\`\`\`
        `
      },
      'api-reference': {
        title: 'API参考',
        content: `
# API参考

## 核心函数

### octopai.convert()
将URL或文件转换为skill。

\`\`\`python
octopai.convert(url_or_path, name=None, output_dir=None)
\`\`\`

### octopai.process()
带可选进化的完整处理流程。

\`\`\`python
octopai.process(url_or_path, evolve=False, iterations=3)
\`\`\`

### octopai.evolve()
进化现有skill。

\`\`\`python
octopai.evolve(skill_path, iterations=5, feedback=None)
\`\`\`
        `
      },
      'examples': {
        title: '示例',
        content: `
# 示例

## 基本URL转Skill

\`\`\`python
import octopai

# 转换文档页面
skill = octopai.convert("https://example.com/docs")
print(f"已创建skill: {skill}")
\`\`\`

## 带进化

\`\`\`python
import octopai

# 处理和进化
final_skill = octopai.process(
    "https://example.com/guide",
    evolve=True,
    iterations=5
)
\`\`\`
        `
      },
      'faq': {
        title: '常见问题',
        content: `
# 常见问题

## 什么是Octopai？

Octopai是一个AI Agent技能探索、扩展和进化框架。

## Skill进化如何工作？

Octopai使用三阶段进化流程：执行器 → 反思器 → 优化器。

## 支持哪些文件格式？

PDF、DOC、DOCX、XLSX、CSV、图片、视频等！
        `
      }
    }
  }

  const currentDocs = docs[language]
  const sections = ['getting-started', 'api-reference', 'examples', 'faq']

  const renderMarkdown = (content) => {
    return content
      .replace(/^### (.*$)/gm, '<h3 class="text-xl font-bold text-gray-800 mt-6 mb-3">$1</h3>')
      .replace(/^## (.*$)/gm, '<h2 class="text-2xl font-bold text-gray-800 mt-8 mb-4">$1</h2>')
      .replace(/^# (.*$)/gm, '<h1 class="text-3xl font-bold text-gray-800 mb-6">$1</h1>')
      .replace(/```([\s\S]*?)```/g, '<pre class="bg-gray-900 text-green-400 p-4 rounded-lg my-4 overflow-x-auto text-sm"><code>$1</code></pre>')
      .replace(/`([^`]+)`/g, '<code class="bg-gray-100 text-purple-600 px-1 py-0.5 rounded text-sm">$1</code>')
      .replace(/^\* (.*$)/gm, '<li class="ml-6 mb-1">$1</li>')
      .replace(/\n\n/g, '</p><p class="mb-4 text-gray-600">')
      .replace(/^(?!<[h|p|pre|l])(.*$)/gm, '<p class="mb-4 text-gray-600">$1</p>')
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-2">
            Documentation
          </h1>
          <p className="text-gray-600">Complete Octopai usage guide and API reference</p>
        </div>
        <button
          onClick={() => setLanguage(language === 'en' ? 'zh' : 'en')}
          className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all font-semibold"
        >
          {language === 'en' ? '🇨🇳 中文' : '🇺🇸 English'}
        </button>
      </div>

      <div className="flex gap-8">
        <aside className="w-64 flex-shrink-0">
          <nav className="bg-white rounded-2xl shadow-lg p-6 sticky top-8">
            <h3 className="font-bold text-gray-800 mb-4">{language === 'en' ? 'Sections' : '章节'}</h3>
            <ul className="space-y-2">
              {sections.map((section) => (
                <li key={section}>
                  <button
                    onClick={() => setActiveSection(section)}
                    className={`w-full text-left px-4 py-2 rounded-lg transition-all ${
                      activeSection === section
                        ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {currentDocs[section]?.title}
                  </button>
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        <main className="flex-1">
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <div
              dangerouslySetInnerHTML={{
                __html: renderMarkdown(currentDocs[activeSection]?.content || '')
              }}
            />
          </div>
        </main>
      </div>
    </div>
  )
}

export default Docs
