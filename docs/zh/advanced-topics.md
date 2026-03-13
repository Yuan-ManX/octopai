# 高级主题

深入了解 EXO 的高级功能和内部工作原理。

## 进化引擎架构

EXO 的进化引擎使用三阶段管道：

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│  执行器     │ ───▶ │   反射器    │ ───▶ │   优化器    │
└────────────┘      └────────────┘      └────────────┘
```

### 阶段 1：执行器

执行器针对评估任务运行候选解决方案并捕获完整的执行跟踪。

```python
def executor(self, candidates, tasks):
    traces = []
    for candidate in candidates:
        for task in tasks:
            # 执行候选
            score, side_info = self._execute_candidate(candidate, task)
            
            # 捕获带有可操作辅助信息的跟踪
            traces.append(EvolutionTrace(
                candidate=candidate,
                task=task,
                score=score,
                side_info=side_info
            ))
    return traces
```

关键特性：
- 捕获推理链、中间输出
- 收集错误消息和性能指标
- 保留可操作辅助信息 (ASI)

### 阶段 2：反射器

反射器分析跟踪以理解失败模式和因果模式。

```python
def reflector(self, traces):
    # 使用 LLM 分析成功和失败
    analysis = self.llm.analyze_traces(traces)
    
    # 提取见解
    insights = {
        "failure_modes": analysis.extract_failure_modes(),
        "success_patterns": analysis.extract_success_patterns(),
        "improvement_suggestions": analysis.generate_suggestions()
    }
    
    return insights
```

反射器提供：
- 问题的人类可读诊断
- 变更与结果之间的因果关系
- 具体的改进建议

### 阶段 3：优化器

优化器基于反射器的见解生成改进的候选。

```python
def optimizer(self, insights, current_candidates):
    # 使用反射见解生成新候选
    new_candidates = []
    
    for candidate in current_candidates:
        # 反射变异
        improved = self._reflective_mutation(candidate, insights)
        new_candidates.append(improved)
    
    # 系统感知合并互补候选
    if len(current_candidates) >= 2:
        merged = self._system_aware_merge(current_candidates[:2], insights)
        new_candidates.append(merged)
    
    return new_candidates
```

两种候选生成策略：
1. **反射变异**：基于失败分析的定向改进
2. **系统感知合并**：组合多个候选的互补优势

## 可操作辅助信息 (ASI)

ASI 是指导进化过程的诊断性、特定领域的反馈。

### ASI 的类型

```python
# 错误消息
side_info = "错误：第 42 行索引越界"

# 分析信息
side_info = "执行时间：2.3s，内存峰值：128MB"

# 推理跟踪
side_info = "智能体尝试使用归纳推理，但需要反证法"

# 约束违规
side_info = "输出超出最大长度 150 个字符"

# 视觉反馈（通过 VLM）
side_info = "渲染图像显示元素对齐不当"
```

### 有效使用 ASI

```python
from exo.core.evolution_engine import EvolutionEngine

def my_evaluator(candidate, task):
    try:
        result = run_my_code(candidate, task)
        
        # 记录 ASI - 这将被自动捕获
        print(f"中间结果: {result.intermediate}")
        print(f"性能: {result.performance}")
        
        return result.score, f"结果: {result.output}"
    except Exception as e:
        return 0.0, f"错误: {str(e)}"

engine = EvolutionEngine()
result = engine.evolve(
    initial_candidate=my_code,
    tasks=my_tasks,
    evaluator=my_evaluator
)
```

## Pareto 高效搜索

EXO 不是通过单一分数对候选进行排名，而是维护 Pareto 前沿：

```python
class ParetoTracker:
    def __init__(self):
        self.frontier = []
    
    def update(self, candidate, scores):
        # 检查候选是否被前沿上的任何人支配
        is_dominated = any(
            all(s1 >= s2 for s1, s2 in zip(existing.scores, scores))
            for existing in self.frontier
        )
        
        if not is_dominated:
            # 移除被这个新候选支配的候选
            self.frontier = [
                existing for existing in self.frontier
                if not all(scores >= s for s in existing.scores)
            ]
            self.frontier.append(SkillCandidate(candidate, scores))
```

这保留了以不同方式表现出色的候选。

## 自定义评估器

为你的特定用例创建自定义评估器：

```python
from exo.core.evolution_engine import EvolutionEngine

class CustomEvaluator:
    def __init__(self, test_cases):
        self.test_cases = test_cases
    
    def evaluate(self, candidate, task):
        try:
            # 编译/加载候选
            exec(candidate, globals())
            
            # 针对测试用例运行
            result = process_input(task["input"])
            
            # 计算多个指标
            accuracy = self._calculate_accuracy(result, task["expected"])
            speed = self._calculate_speed(result)
            memory = self._calculate_memory(result)
            
            # 组合分数
            score = 0.5 * accuracy + 0.3 * (1/speed) + 0.2 * (1/memory)
            
            # 详细的 ASI
            side_info = (
                f"准确率: {accuracy:.2f}, "
                f"速度: {speed:.2f}s, "
                f"内存: {memory:.2f}MB"
            )
            
            return score, side_info
            
        except Exception as e:
            return 0.0, f"错误: {str(e)}"

# 使用
evaluator = CustomEvaluator(test_cases)
engine = EvolutionEngine()
result = engine.evolve(
    initial_candidate=initial_code,
    tasks=test_cases,
    evaluator=lambda c, t: evaluator.evaluate(c, t)
)
```

## 高级资源解析器配置

自定义 Web 爬虫以满足特定需求：

```python
from exo.core.resource_parser import ResourceParser, BaseParser, ParsedResource, ResourceType
import os

class CustomParser(BaseParser):
    """自定义文件格式解析器"""
    
    def can_parse(self, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext == '.custom'
    
    def parse(self, file_path: str) -> ParsedResource:
        # 自定义解析逻辑
        with open(file_path, 'r') as f:
            content = f.read()
        
        return ParsedResource(
            file_path=file_path,
            resource_type=ResourceType.TEXT,
            text_content=content,
            metadata={'custom': True}
        )

# 使用自定义解析器
parser = ResourceParser()
parser.parsers.insert(0, CustomParser())  # 首先尝试自定义解析器

resource = parser.parse("data.custom")
```

## 扩展 EXO

### 创建自定义转换器

```python
from exo.core.converter import URLConverter

class CustomConverter(URLConverter):
    def _post_process(self, markdown):
        # 自定义 Markdown 处理
        markdown = markdown.replace('old-text', 'new-text')
        
        # 添加自定义头部
        header = "---\ncustom_metadata: true\n---\n\n"
        return header + markdown

# 使用
converter = CustomConverter()
content = converter.convert("https://example.com")
```

### 创建自定义技能模板

```python
from exo.core.creator import SkillCreator

class TemplatedCreator(SkillCreator):
    def __init__(self, template_path):
        super().__init__()
        with open(template_path, 'r') as f:
            self.template = f.read()
    
    def create(self, prompt, **kwargs):
        # 使用模板生成
        skill_content = super().create(prompt, **kwargs)
        
        # 插入模板
        final_skill = self.template.replace('{{SKILL_CONTENT}}', skill_content)
        
        return final_skill
```

## 性能优化

### 缓存结果

```python
from functools import lru_cache
import hashlib

class CachedEXO:
    def __init__(self):
        self.exo = EXO()
        self.cache = {}
    
    def _get_cache_key(self, func_name, *args):
        key = f"{func_name}:{hashlib.md5(str(args).encode()).hexdigest()}"
        return key
    
    def parse_file(self, file_path, **kwargs):
        key = self._get_cache_key('parse', file_path, str(kwargs))
        if key in self.cache:
            return self.cache[key]
        
        result = self.exo.parse_file(file_path, **kwargs)
        self.cache[key] = result
        return result
```

### 并行处理

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def parse_files_parallel(file_paths, max_workers=4):
    exo = EXO()
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {
            executor.submit(exo.parse_file, path): path
            for path in file_paths
        }
        
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                results[path] = future.result()
            except Exception as e:
                results[path] = f"错误: {str(e)}"
    
    return results
```

## 最佳实践

1. **从简单开始**：在深入高级功能之前，从基本 API 使用开始
2. **迭代**：最初使用 3-5 次迭代的进化引擎，然后调整
3. **提供良好的 ASI**：你提供的诊断信息越多，进化效果越好
4. **使用适当的模型**：对复杂进化使用 GPT-5.4，对简单任务使用 GPT-4o-mini
5. **缓存结果**：通过缓存频繁操作来节省 API 成本
6. **监控成本**：跟踪你的 API 使用情况和成本
7. **增量测试**：在大规模进化之前测试小的更改
8. **版本控制**：让你的技能处于版本控制之下
