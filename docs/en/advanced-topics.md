# Advanced Topics

Dive deeper into EXO's advanced capabilities and internals.

## The Evolution Engine Architecture

EXO's evolution engine uses a three-stage pipeline:

```
┌────────────┐      ┌────────────┐      ┌────────────┐
│  Executor  │ ───▶ │  Reflector │ ───▶ │ Optimizer  │
└────────────┘      └────────────┘      └────────────┘
```

### Stage 1: Executor

The Executor runs candidate solutions against evaluation tasks and captures full execution traces.

```python
def executor(self, candidates, tasks):
    traces = []
    for candidate in candidates:
        for task in tasks:
            # Execute the candidate
            score, side_info = self._execute_candidate(candidate, task)
            
            # Capture trace with actionable side information
            traces.append(EvolutionTrace(
                candidate=candidate,
                task=task,
                score=score,
                side_info=side_info
            ))
    return traces
```

Key features:
- Captures reasoning chains, intermediate outputs
- Collects error messages and performance metrics
- Preserves Actionable Side Information (ASI)

### Stage 2: Reflector

The Reflector analyzes traces to understand failure modes and causal patterns.

```python
def reflector(self, traces):
    # Use LLM to analyze successes and failures
    analysis = self.llm.analyze_traces(traces)
    
    # Extract insights
    insights = {
        "failure_modes": analysis.extract_failure_modes(),
        "success_patterns": analysis.extract_success_patterns(),
        "improvement_suggestions": analysis.generate_suggestions()
    }
    
    return insights
```

The Reflector provides:
- Human-readable diagnosis of issues
- Causal relationships between changes and outcomes
- Concrete improvement suggestions

### Stage 3: Optimizer

The Optimizer generates improved candidates based on the Reflector's insights.

```python
def optimizer(self, insights, current_candidates):
    # Generate new candidates using reflection insights
    new_candidates = []
    
    for candidate in current_candidates:
        # Reflective mutation
        improved = self._reflective_mutation(candidate, insights)
        new_candidates.append(improved)
    
    # System-aware merge of complementary candidates
    if len(current_candidates) >= 2:
        merged = self._system_aware_merge(current_candidates[:2], insights)
        new_candidates.append(merged)
    
    return new_candidates
```

Two candidate generation strategies:
1. **Reflective Mutation**: Targeted improvements based on failure analysis
2. **System-Aware Merge**: Combines complementary strengths from multiple candidates

## Actionable Side Information (ASI)

ASI is diagnostic, domain-specific feedback that guides the evolution process.

### Types of ASI

```python
# Error messages
side_info = "Error: Index out of bounds at line 42"

# Profiling information
side_info = "Execution time: 2.3s, Memory peak: 128MB"

# Reasoning traces
side_info = "Agent attempted to use inductive reasoning, but proof by contradiction needed"

# Constraint violations
side_info = "Output exceeds maximum length by 150 characters"

# Visual feedback (via VLMs)
side_info = "Rendered image shows misaligned elements"
```

### Using ASI Effectively

```python
from exo.core.evolution_engine import EvolutionEngine

def my_evaluator(candidate, task):
    try:
        result = run_my_code(candidate, task)
        
        # Log ASI - this will be captured automatically
        print(f"Intermediate result: {result.intermediate}")
        print(f"Performance: {result.performance}")
        
        return result.score, f"Result: {result.output}"
    except Exception as e:
        return 0.0, f"Error: {str(e)}"

engine = EvolutionEngine()
result = engine.evolve(
    initial_candidate=my_code,
    tasks=my_tasks,
    evaluator=my_evaluator
)
```

## Pareto-Efficient Search

Instead of ranking candidates by a single score, EXO maintains a Pareto frontier:

```python
class ParetoTracker:
    def __init__(self):
        self.frontier = []
    
    def update(self, candidate, scores):
        # Check if candidate is dominated by anyone on frontier
        is_dominated = any(
            all(s1 >= s2 for s1, s2 in zip(existing.scores, scores))
            for existing in self.frontier
        )
        
        if not is_dominated:
            # Remove candidates dominated by this new one
            self.frontier = [
                existing for existing in self.frontier
                if not all(scores >= s for s in existing.scores)
            ]
            self.frontier.append(SkillCandidate(candidate, scores))
```

This preserves candidates that excel in different ways.

## Custom Evaluators

Create custom evaluators for your specific use case:

```python
from exo.core.evolution_engine import EvolutionEngine

class CustomEvaluator:
    def __init__(self, test_cases):
        self.test_cases = test_cases
    
    def evaluate(self, candidate, task):
        try:
            # Compile/load the candidate
            exec(candidate, globals())
            
            # Run against test case
            result = process_input(task["input"])
            
            # Calculate multiple metrics
            accuracy = self._calculate_accuracy(result, task["expected"])
            speed = self._calculate_speed(result)
            memory = self._calculate_memory(result)
            
            # Combined score
            score = 0.5 * accuracy + 0.3 * (1/speed) + 0.2 * (1/memory)
            
            # Detailed ASI
            side_info = (
                f"Accuracy: {accuracy:.2f}, "
                f"Speed: {speed:.2f}s, "
                f"Memory: {memory:.2f}MB"
            )
            
            return score, side_info
            
        except Exception as e:
            return 0.0, f"Error: {str(e)}"

# Usage
evaluator = CustomEvaluator(test_cases)
engine = EvolutionEngine()
result = engine.evolve(
    initial_candidate=initial_code,
    tasks=test_cases,
    evaluator=lambda c, t: evaluator.evaluate(c, t)
)
```

## Advanced Crawler Configuration

Customize the web crawler for specific needs:

```python
from exo.core.crawler import WebCrawler
import requests

class CustomCrawler(WebCrawler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MyCustomBot/1.0',
            'Accept': 'text/html,application/xhtml+xml'
        })
    
    def _fetch_html(self, url):
        # Custom fetch with authentication, cookies, etc.
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    
    def _should_download(self, url):
        # Custom filtering logic
        if 'exclude' in url:
            return False
        if url.endswith('.pdf'):
            return True  # Download PDFs
        return super()._should_download(url)

# Usage
crawler = CustomCrawler(output_dir="./custom-downloads")
resource = crawler.crawl("https://example.com")
```

## Extending EXO

### Creating Custom Converters

```python
from exo.core.converter import URLConverter

class CustomConverter(URLConverter):
    def _post_process(self, markdown):
        # Custom markdown processing
        markdown = markdown.replace('old-text', 'new-text')
        
        # Add custom header
        header = "---\ncustom_metadata: true\n---\n\n"
        return header + markdown

# Usage
converter = CustomConverter()
content = converter.convert("https://example.com")
```

### Creating Custom Skill Templates

```python
from exo.core.creator import SkillCreator

class TemplatedCreator(SkillCreator):
    def __init__(self, template_path):
        super().__init__()
        with open(template_path, 'r') as f:
            self.template = f.read()
    
    def create(self, prompt, **kwargs):
        # Generate using template
        skill_content = super().create(prompt, **kwargs)
        
        # Insert into template
        final_skill = self.template.replace('{{SKILL_CONTENT}}', skill_content)
        
        return final_skill
```

## Performance Optimization

### Caching Results

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
    
    def convert_url(self, url, **kwargs):
        key = self._get_cache_key('convert', url, str(kwargs))
        if key in self.cache:
            return self.cache[key]
        
        result = self.exo.convert_url(url, **kwargs)
        self.cache[key] = result
        return result
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_urls_parallel(urls, max_workers=4):
    exo = EXO()
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(exo.convert_url, url): url
            for url in urls
        }
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results[url] = future.result()
            except Exception as e:
                results[url] = f"Error: {str(e)}"
    
    return results
```

## Best Practices

1. **Start Simple**: Begin with basic API usage before diving into advanced features
2. **Iterate**: Use the evolution engine with 3-5 iterations initially, then adjust
3. **Provide Good ASI**: The more diagnostic information you provide, the better the evolution
4. **Use Appropriate Models**: Use GPT-5.4 for complex evolution, GPT-5.4 for simpler tasks
5. **Cache Results**: Save API costs by caching frequent operations
6. **Monitor Costs**: Keep track of your API usage and costs
7. **Test Incrementally**: Test small changes before large-scale evolution
8. **Version Control**: Keep your skills under version control
