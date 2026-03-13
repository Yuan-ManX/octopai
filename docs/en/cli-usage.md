# CLI Usage

EXO provides a powerful command-line interface for quick operations and automation.

## Installation

Make sure you have EXO installed:

```bash
pip install exo
```

Or install from source:

```bash
git clone https://github.com/Yuan-ManX/EXO.git
cd EXO
pip install -e .
```

## Available Commands

### `exo convert`

Convert a URL to Markdown format.

**Usage:**
```bash
exo convert <url> [options]
```

**Options:**
- `-o, --output PATH`: Output file path
- `-c, --crawler`: Enable web crawler to download resources
- `-v, --verbose`: Enable verbose output

**Examples:**

Basic conversion:
```bash
exo convert https://example.com -o output.md
```

With crawler enabled:
```bash
exo convert https://example.com -o output.md --crawler
```

### `exo create`

Create a new skill from a description.

**Usage:**
```bash
exo create <prompt> [options]
```

**Options:**
- `-n, --name TEXT`: Name for the skill
- `-o, --output PATH`: Output file path
- `-v, --verbose`: Enable verbose output

**Examples:**

Create a skill:
```bash
exo create "A skill that reads JSON files and validates their structure"
```

Create and save to a specific file:
```bash
exo create "A web scraping skill" -n web-scraper -o skills/scraper.py
```

### `exo evolve`

Evolve and improve an existing skill.

**Usage:**
```bash
exo evolve <skill_path> <prompt> [options]
```

**Options:**
- `-e, --engine`: Use the advanced evolution engine (default: True)
- `-i, --iterations INTEGER`: Number of evolution iterations (default: 3)
- `-o, --output PATH`: Output file path (defaults to overwriting input)
- `-v, --verbose`: Enable verbose output

**Examples:**

Basic evolution:
```bash
exo evolve skills/old-skill.py "Add better error handling"
```

Multiple iterations:
```bash
exo evolve skills/analyzer.py "Optimize performance" -i 5
```

Without advanced engine:
```bash
exo evolve skills/simple.py "Minor improvements" --no-engine
```

### `exo crawl`

Crawl a website and download all resources.

**Usage:**
```bash
exo crawl <url> [options]
```

**Options:**
- `-o, --output-dir PATH`: Output directory (default: ./downloads)
- `-v, --verbose`: Enable verbose output

**Examples:**

Basic crawl:
```bash
exo crawl https://example.com
```

Custom output directory:
```bash
exo crawl https://example.com -o ./my-site
```

## Global Options

These options work with all commands:

- `--help`: Show help message and exit
- `--version`: Show the version and exit
- `--config PATH`: Path to configuration file
- `-v, --verbose`: Enable verbose output
- `-q, --quiet`: Suppress non-error output

## Configuration File

You can create a `.exorc` or `exo.config.json` file in your project directory:

```json
{
  "model_provider": "openrouter",
  "model": "openai/gpt-5.4",
  "output_dir": "./output",
  "skills_dir": "./skills"
}
```

## Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `EXO_CONFIG`: Path to custom configuration file
- `EXO_VERBOSE`: Set to "1" for verbose output by default

## Shell Completion

Enable shell completion for better productivity:

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

## Examples

### Workflow: Create and Evolve a Skill

```bash
# 1. Create a new skill
exo create "A skill that processes CSV files" -n csv-processor -o skills/csv.py

# 2. Test it, then evolve for better performance
exo evolve skills/csv.py "Add chunked reading for large files" -i 3

# 3. Evolve again for better error handling
exo evolve skills/csv.py "Add comprehensive error handling and logging"
```

### Workflow: Download and Process a Site

```bash
# 1. Crawl the site
exo crawl https://example.com -o ./my-downloads

# 2. Convert a specific page to Markdown
exo convert https://example.com/docs -o ./docs/page.md --crawler
```

## Tips and Tricks

1. **Pipe to other commands**:
```bash
exo convert https://example.com | head -50
```

2. **Process multiple URLs**:
```bash
for url in $(cat urls.txt); do
    exo convert "$url" -o "output/$(basename "$url").md"
done
```

3. **Use in CI/CD pipelines**:
```yaml
# .github/workflows/process.yml
- name: Process documentation
  run: |
    exo convert https://docs.example.com -o docs/api.md
```

4. **Save your API key**:
```bash
# In ~/.bashrc or ~/.zshrc
export OPENROUTER_API_KEY="your-api-key-here"
```
