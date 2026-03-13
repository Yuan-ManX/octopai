# 常见问题

## 一般问题

### 什么是 EXO？

EXO 是一个全面的 AI Agent Skills 开发平台，提供以下工具：
- 将网页转换为 Markdown
- 从自然语言描述创建 AI 技能
- 使用高级 AI 进化和改进现有技能
- 爬取网站以收集资源

### EXO 与其他 AI 平台有何不同？

EXO 结合了几个独特的功能：
- **进化引擎**：使用基于 LLM 的反射进行智能改进
- **双接口**：通过 Python API 或命令行使用，哪个更方便就用哪个
- **内置爬取**：集成的 Web 爬取以进行资源收集
- **OpenRouter 集成**：通过单个 API 访问数百个 AI 模型

### 我需要编码经验才能使用 EXO 吗？

Python API 有基本的编码经验会有帮助，但 CLI 界面对初学者来说是可访问的。我们提供了大量的示例和文档来帮助你入门。

## 安装和设置

### 如何安装 EXO？

```bash
pip install exo
```

或从源码：
```bash
git clone https://github.com/Yuan-ManX/EXO.git
cd EXO
pip install -e .
```

### 我需要什么 API 密钥？

你需要一个 OpenRouter API 密钥。在 [openrouter.ai](https://openrouter.ai) 注册以获取一个。

### 如何设置我的 API 密钥？

将其设置为环境变量：

```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

或创建 `.env` 文件：

```
OPENROUTER_API_KEY=your-api-key-here
```

## 使用问题

### 我应该使用哪个模型？

- **openai/gpt-5.4**（默认）：大多数任务的成本和质量的良好平衡
- **openai/gpt-5.4**：复杂进化和创建的最佳质量
- **anthropic/claude-4-6-sonnet**：编码任务的良好替代方案
- **google/gemini-3-pro**：另一个可靠的选择

### EXO 成本是多少？

EXO 本身是免费和开源的。你只需通过 OpenRouter 为 AI 模型使用付费。成本因模型而异：
- GPT-5：每 1M 输入 token 约 $0.15
- GPT-5.4：每 1M 输入 token 约 $5

### 我可以离线使用 EXO 吗？

不可以，EXO 需要 API 访问 AI 模型。但是，你可以缓存结果以最小化 API 调用。

### 技能进化需要多长时间？

这取决于：
- 迭代次数（默认：3）
- 使用的模型（GPT-4o 较慢但更好）
- 技能的复杂性

典型时间：
- 简单技能：1-2 分钟
- 具有 5 次迭代的复杂技能：5-10 分钟

## 技术问题

### 什么是进化引擎？

进化引擎是 EXO 的高级功能。它使用三阶段管道：
1. **执行器**：运行候选并捕获跟踪
2. **反射器**：分析失败和成功
3. **优化器**：生成改进的候选

这允许智能的定向改进，而不是随机搜索。

### 什么是可操作辅助信息 (ASI)？

ASI 是帮助进化引擎理解为什么某些事情成功或失败的诊断反馈。示例包括：
- 错误消息
- 性能指标
- 推理跟踪
- 约束违规

提供良好的 ASI 显著提高了进化质量。

### 我可以自定义进化过程吗？

是的！你可以：
- 创建自定义评估器
- 调整迭代次数
- 为不同阶段选择不同的模型
- 定义自定义评估任务

详见 [高级主题](./advanced-topics.md) 部分。

### 资源解析器如何工作？

资源解析器：
1. 检测文件类型
2. 使用适当的解析器
3. 提取文本内容和元数据
4. 返回结构化的 ParsedResource 对象

你可以添加自定义解析器 - 详见 [高级主题](./advanced-topics.md)。

### 支持哪些文件格式？

- **文本**：.txt, .md, .csv, .json, .yaml
- **PDF**：.pdf
- **文档**：.doc, .docx
- **表格**：.xlsx, .xls, .csv
- **图片**：.jpg, .jpeg, .png, .gif, .bmp, .webp
- **视频**：.mp4, .avi, .mov, .mkv, .webm
- **HTML**：.html, .htm

## 故障排除

### 我收到 API 身份验证错误

确保你的 OpenRouter API 密钥设置正确：
```bash
echo $OPENROUTER_API_KEY  # 应显示你的密钥
```

如果没有，设置它：
```bash
export OPENROUTER_API_KEY="your-key-here"
```

### 进化没有改进我的技能

尝试这些步骤：
1. 增加迭代次数（`-i 5` 或更多）
2. 使用更好的模型（`model="openai/gpt-5.4"`）
3. 在你的提示中提供更具体的反馈
4. 确保你的评估器提供良好的 ASI

### 文件解析无法正常工作

检查：
- 你是否为文件类型安装了所需的依赖项
- 文件未损坏
- 文件格式受支持
- 查看错误消息以获取具体问题

所需依赖项：
- PDF：`pip install PyPDF2`
- DOCX：`pip install python-docx`
- Excel：`pip install pandas openpyxl`
- 图片：`pip install Pillow`
- 视频：`pip install opencv-python`
- HTML：`pip install beautifulsoup4`

### 找不到 CLI

确保 EXO 已安装：
```bash
pip show exo
```

如果已安装，检查你的 PATH。你可能需要将 Python 的 bin 目录添加到 PATH。

## 高级用法

### 我可以将 EXO 集成到我现有的项目中吗？

绝对可以！EXO 设计为作为库导入和使用：

```python
from exo import EXO

exo = EXO()
skill = exo.create_skill("我的自定义技能")
```

详见 [API 参考](./api-reference.md) 获取完整文档。

### 我如何为 EXO 做贡献？

我们欢迎贡献！请查看我们的 GitHub 仓库以获取：
- 问题跟踪器
- 贡献指南
- 行为准则

### EXO 可以用于生产吗？

EXO 适用于：
- 原型设计和开发
- 技能创建和进化
- 文档处理
- Web 爬取

对于关键生产系统，我们建议进行彻底的测试。

## 更多帮助

还有问题？

- 查看我们的 [GitHub Issues](https://github.com/Yuan-ManX/EXO/issues)
- 加入我们的社区讨论
- 查看 [示例](./examples.md) 获取实际用例
- 阅读 [高级主题](./advanced-topics.md) 进行深入探讨
