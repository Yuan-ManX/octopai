# CLI 使用

EXO 提供了强大的命令行界面，用于快速操作和自动化。

## 安装

确保已安装 EXO：

```bash
pip install exo
```

或从源码安装：

```bash
git clone https://github.com/Yuan-ManX/EXO.git
cd EXO
pip install -e .
```

## 可用命令

### `exo convert`

将 URL 转换为 Markdown 格式。

**用法：**
```bash
exo convert <url> [选项]
```

**选项：**
- `-o, --output PATH`: 输出文件路径
- `-c, --crawler`: 启用网络爬虫以下载资源
- `-v, --verbose`: 启用详细输出

**示例：**

基本转换：
```bash
exo convert https://example.com -o output.md
```

启用爬虫：
```bash
exo convert https://example.com -o output.md --crawler
```

### `exo create`

从描述创建新技能。

**用法：**
```bash
exo create <prompt> [选项]
```

**选项：**
- `-n, --name TEXT`: 技能名称
- `-o, --output PATH`: 输出文件路径
- `-r, --resources PATH`: 用作资源的文件（可多次使用）
- `-v, --verbose`: 启用详细输出

**示例：**

创建技能：
```bash
exo create "一个读取 JSON 文件并验证其结构的技能"
```

使用资源创建：
```bash
exo create "根据这些文件创建数据分析技能" \
  -n data-analyzer \
  -o skills/analyzer.py \
  -r data/sample.csv \
  -r docs/reference.pdf
```

### `exo evolve`

进化和改进现有技能。

**用法：**
```bash
exo evolve <skill_path> <prompt> [选项]
```

**选项：**
- `-e, --engine`: 使用高级进化引擎（默认：True）
- `-i, --iterations INTEGER`: 进化迭代次数（默认：3）
- `-o, --output PATH`: 输出文件路径（默认覆盖输入）
- `-v, --verbose`: 启用详细输出

**示例：**

基本进化：
```bash
exo evolve skills/old-skill.py "添加更好的错误处理"
```

多次迭代：
```bash
exo evolve skills/analyzer.py "优化性能" -i 5
```

不使用高级引擎：
```bash
exo evolve skills/simple.py "小改进" --no-engine
```

### `exo parse`

解析文件并转换为技能资源。

**用法：**
```bash
exo parse <file_path> [选项]
```

**选项：**
- `-o, --output PATH`: 输出文件路径
- `-f, --format TEXT`: 输出格式 ('text' 或 'json')
- `-v, --verbose`: 启用详细输出

**示例：**

解析 PDF 文件：
```bash
exo parse document.pdf -o resource.md
```

解析多个文件：
```bash
for file in *.csv; do
    exo parse "$file" -o "resources/$(basename "$file").md"
done
```

### `exo crawl`

爬取网站并下载所有资源。

**用法：**
```bash
exo crawl <url> [选项]
```

**选项：**
- `-o, --output-dir PATH`: 输出目录（默认：./downloads）
- `-v, --verbose`: 启用详细输出

**示例：**

基本爬取：
```bash
exo crawl https://example.com
```

自定义输出目录：
```bash
exo crawl https://example.com -o ./my-site
```

## 全局选项

这些选项适用于所有命令：

- `--help`: 显示帮助信息并退出
- `--version`: 显示版本并退出
- `--config PATH`: 配置文件路径
- `-v, --verbose`: 启用详细输出
- `-q, --quiet`: 抑制非错误输出

## 配置文件

你可以在项目目录中创建 `.exorc` 或 `exo.config.json` 文件：

```json
{
  "model_provider": "openrouter",
  "model": "openai/gpt-4o-mini",
  "output_dir": "./output",
  "skills_dir": "./skills"
}
```

## 环境变量

- `OPENROUTER_API_KEY`: 你的 OpenRouter API 密钥（必需）
- `EXO_CONFIG`: 自定义配置文件路径
- `EXO_VERBOSE`: 设置为 "1" 以默认启用详细输出

## Shell 补全

启用 shell 补全以提高生产力：

### Bash
```bash
exo --install-completion bash
```

### Zsh
```bash
exo --install-completion zsh
```

### Fish
```bash
exo --install-completion fish
```

## 示例

### 工作流：创建和进化技能

```bash
# 1. 解析资源文件
exo parse data/reference.pdf -o resources/ref.md
exo parse data/sample.csv -o resources/sample.md

# 2. 使用资源创建新技能
exo create "一个分析 CSV 数据的技能" \
  -n csv-processor \
  -o skills/csv.py \
  -r resources/ref.md \
  -r resources/sample.md

# 3. 测试它，然后进化以获得更好的性能
exo evolve skills/csv.py "为大文件添加分块读取" -i 3

# 4. 再次进化以获得更好的错误处理
exo evolve skills/csv.py "添加全面的错误处理和日志记录"
```

### 工作流：下载和处理站点

```bash
# 1. 爬取站点
exo crawl https://example.com -o ./my-downloads

# 2. 将特定页面转换为 Markdown
exo convert https://example.com/docs -o ./docs/page.md --crawler

# 3. 解析下载的文档
exo parse my-downloads/manual.pdf -o resources/manual.md
```

## 技巧和窍门

1. **管道到其他命令**：
```bash
exo convert https://example.com | head -50
```

2. **处理多个 URL**：
```bash
for url in $(cat urls.txt); do
    exo convert "$url" -o "output/$(basename "$url").md"
done
```

3. **在 CI/CD 管道中使用**：
```yaml
# .github/workflows/process.yml
- name: 处理文档
  run: |
    exo convert https://docs.example.com -o docs/api.md
```

4. **保存你的 API 密钥**：
```bash
# 在 ~/.bashrc 或 ~/.zshrc 中
export OPENROUTER_API_KEY="your-api-key-here"
```
