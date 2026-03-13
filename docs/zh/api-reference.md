# API 参考

EXO 提供了高级 Python API 和 CLI 接口，以实现最大的灵活性。

## Python API

### `EXO` 类

所有 EXO 功能的主入口点。

```python
from exo import EXO

# 使用默认设置初始化
exo = EXO()

# 或使用自定义配置
exo = EXO(
    model_provider="openrouter",
    model="openai/gpt-5.4",
    api_key="your-api-key"
)
```

#### 方法

##### `convert_url(url, output_path=None, use_crawler=False)`

将网页 URL 转换为 Markdown 格式。

**参数：**
- `url` (str): 要转换的 URL
- `output_path` (str, 可选): 保存输出文件的路径
- `use_crawler` (bool, 可选): 如果为 True，还会下载所有网页资源

**返回：**
- `str`: 转换后的 Markdown 内容

**示例：**
```python
content = exo.convert_url("https://example.com", use_crawler=True)
```

##### `parse_file(file_path)`

解析文件并返回结构化资源。

**参数：**
- `file_path` (str): 要解析的文件路径

**返回：**
- `ParsedResource`: 解析后的资源对象

**示例：**
```python
resource = exo.parse_file("document.pdf")
print(resource.text_content)
print(resource.metadata)
```

##### `parse_to_skill_resource(file_path)`

解析文件并直接转换为技能资源格式。

**参数：**
- `file_path` (str): 要解析的文件路径

**返回：**
- `str`: 技能资源格式的字符串

**示例：**
```python
skill_resource = exo.parse_to_skill_resource("data.csv")
```

##### `parse_multiple_files(file_paths)`

解析多个文件。

**参数：**
- `file_paths` (List[str]): 要解析的文件路径列表

**返回：**
- `List[ParsedResource]`: 解析后的资源对象列表

##### `create_skill(prompt, name=None, output_path=None, resources=None)`

使用 LLM 创建新技能。

**参数：**
- `prompt` (str): 技能功能描述
- `name` (str, 可选): 技能名称
- `output_path` (str, 可选): 保存技能文件的路径
- `resources` (List[str], 可选): 用作资源的文件路径列表

**返回：**
- `str`: 生成的技能内容

**示例：**
```python
skill = exo.create_skill(
    "一个分析 CSV 文件并生成摘要报告的技能",
    name="csv-analyzer",
    resources=["data/sample.csv", "docs/guide.pdf"]
)
```

##### `evolve_skill(skill_path, prompt, use_engine=True, iterations=3)`

进化和改进现有技能。

**参数：**
- `skill_path` (str): 技能文件路径
- `prompt` (str): 进化指令或反馈
- `use_engine` (bool, 可选): 使用高级进化引擎（默认：True）
- `iterations` (int, 可选): 进化迭代次数（默认：3）

**返回：**
- `str`: 进化后的技能内容

**示例：**
```python
evolved = exo.evolve_skill(
    "skills/my-skill.py",
    "使其更高效地处理大文件",
    use_engine=True,
    iterations=5
)
```

##### `process(input_data, operation='convert', **kwargs)`

任何 EXO 操作的通用方法。

**参数：**
- `input_data`: 要处理的输入数据
- `operation` (str): 要执行的操作 ('convert', 'parse', 'create', 'evolve')
- `**kwargs`: 其他操作特定参数

**返回：**
- 操作结果

### 便捷函数

无需实例化类即可快速访问：

```python
from exo import convert, parse, create, evolve, process

# 转换 URL
content = convert("https://example.com")

# 解析文件
resource = parse("document.pdf")

# 创建技能
skill = create("一个翻译文本的技能")

# 进化技能
evolved = evolve("skills/translator.py", "添加法语支持")
```

### 资源解析器

#### `ResourceParser`

多格式文件解析的主类。

```python
from exo.core.resource_parser import ResourceParser

parser = ResourceParser()
resource = parser.parse("document.pdf")

print(f"类型: {resource.resource_type}")
print(f"内容: {resource.text_content[:100]}...")
```

#### `ParsedResource`

表示解析后的资源。

```python
from exo.core.resource_parser import parse_to_skill_resource

# 直接转换为技能资源格式
skill_resource = parse_to_skill_resource("data.xlsx")
print(skill_resource)
```

支持的文件格式：
- **文本**: .txt, .md, .csv, .json, .yaml
- **PDF**: .pdf
- **文档**: .doc, .docx
- **表格**: .xlsx, .xls, .csv
- **图片**: .jpg, .jpeg, .png, .gif, .bmp, .webp
- **视频**: .mp4, .avi, .mov, .mkv, .webm
- **HTML**: .html, .htm

## 配置

### 环境变量

- `OPENROUTER_API_KEY`: 你的 OpenRouter API 密钥
- `EXO_MODEL_PROVIDER`: 默认模型提供商 ('openrouter')
- `EXO_MODEL`: 要使用的默认模型

### 模型配置

EXO 支持通过 OpenRouter 提供的任何模型。热门选择：
- `openai/gpt-5.4`（默认，成本和质量的良好平衡）
- `openai/gpt-5.4`（最佳质量）
- `anthropic/claude-4-6-sonnet`
- `google/gemini-3-pro`

## 错误处理

```python
from exo import EXO

exo = EXO()

try:
    content = exo.convert_url("https://example.com")
except Exception as e:
    print(f"错误: {e}")
    # 适当地处理错误
```
