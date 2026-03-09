---
name: openfriday-bench
description: Run OpenFriday Bench benchmarks to evaluate OpenClaw agent performance across real-world tasks. Use when testing model capabilities, comparing models, or checking how well your OpenClaw setup handles calendar, email, research, coding, and multi-step workflows.
metadata:
  author: yyyyujiexin-dotcom
  version: "1.0.0"
  homepage: https://github.com/yyyyujiexin-dotcom/openfriday-bench
  repository: https://github.com/yyyyujiexin-dotcom/openfriday-bench
---

# OpenFriday Bench Benchmark Skill

OpenFriday Bench measures how well LLM models perform as the brain of an OpenClaw agent.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenClaw instance (this agent)

## Quick Start

```bash
cd <skill_directory>

# Run benchmark with a specific model
uv run benchmark.py --model anthropic/claude-sonnet-4

# Run only automated tasks (faster)
uv run benchmark.py --model anthropic/claude-sonnet-4 --suite automated-only

# Run specific tasks
uv run benchmark.py --model anthropic/claude-sonnet-4 --suite task_01_calendar,task_02_stock

# Skip uploading results
uv run benchmark.py --model anthropic/claude-sonnet-4 --no-upload
```

## Available Tasks

| Task | Category | Description |
|------|----------|-------------|
| `task_00_sanity` | Basic | Verify agent works |
| `task_01_calendar` | Productivity | Calendar event creation |
| `task_02_stock` | Research | Stock price lookup |
| `task_03_blog` | Writing | Blog post creation |
| `task_04_weather` | Coding | Weather script |
| `task_05_summary` | Analysis | Document summarization |
| `task_06_events` | Research | Conference research |
| `task_07_email` | Writing | Email drafting |
| `task_08_memory` | Memory | Context retrieval |
| `task_09_files` | Files | File structure creation |
| ... | ... | ... |

## Command Line Options

| Option | Description |
|--------|-------------|
| `--model` | Model identifier (e.g., `anthropic/claude-sonnet-4`) |
| `--suite` | `all`, `automated-only`, or comma-separated task IDs |
| `--output-dir` | Results directory (default: `results/`) |
| `--timeout-multiplier` | Scale task timeouts for slower models |
| `--runs` | Number of runs per task for averaging |
| `--no-upload` | Skip uploading to leaderboard |

## Results

Results are saved as JSON in the output directory:

```bash
# View task scores
jq '.tasks[] | {task_id, score: .grading.mean}' results/0001_anthropic-claude-sonnet-4.json

# Show failed tasks
jq '.tasks[] | select(.grading.mean < 0.5)' results/*.json

# Calculate overall score
jq '{average: ([.tasks[].grading.mean] | add / length)}' results/*.json
```

## Adding Custom Tasks

Create a markdown file in `tasks/` following `TASK_TEMPLATE.md`. Each task needs:

- YAML frontmatter (id, name, category, grading_type, timeout)
- Prompt section
- Expected behavior
- Grading criteria
- Automated checks (Python grading function)
