# 🐾 OpenFriday Bench

**Real-world benchmarks for AI coding agents**

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

OpenFriday Bench measures how well LLM models perform as the brain of an [OpenClaw](https://github.com/openclaw/openclaw) agent. Instead of synthetic tests, we throw real tasks at agents: scheduling meetings, writing code, triaging email, researching topics, and managing files.

Results are collected on a public leaderboard (coming soon).

## Why OpenFriday Bench?

Most LLM benchmarks test isolated capabilities. OpenFriday Bench tests what actually matters for coding agents:

- **Tool usage** — Can the model call the right tools with the right parameters?
- **Multi-step reasoning** — Can it chain together actions to complete complex tasks?
- **Real-world messiness** — Can it handle ambiguous instructions and incomplete information?
- **Practical outcomes** — Did it actually create the file, send the email, or schedule the meeting?

## Quick Start

```bash
# Clone the benchmark
git clone https://github.com/yyyyujiexin-dotcom/openfriday-bench.git
cd openfriday-bench

# Run benchmarks with your model of choice
./scripts/run.sh --model anthropic/claude-sonnet-4

# Or run specific tasks
./scripts/run.sh --model openai/gpt-4o --suite task_01_calendar,task_02_stock
```

**Requirements:**
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- A running OpenClaw instance

## What Gets Tested

OpenFriday Bench includes tasks across real-world categories:

| Category | Tasks | What's tested |
|----------|-------|---------------|
| **Productivity** | Calendar, daily summaries | Event creation, time parsing, scheduling |
| **Research** | Stock prices, conferences, markets | Web search, data extraction, synthesis |
| **Writing** | Blog posts, emails, humanization | Content generation, tone, formatting |
| **Coding** | Weather scripts, file structures | Code generation, file operations |
| **Analysis** | Spreadsheets, PDFs, documents | Data processing, summarization |
| **Email** | Triage, search | Inbox management, filtering |
| **Memory** | Context retrieval, knowledge management | Long-term memory, recall |
| **Skills** | ClawHub, skill discovery | OpenClaw ecosystem integration |

Each task is graded automatically, by an LLM judge, or both — ensuring both objective and nuanced evaluation.

## Submitting Results

TBD - Leaderboard coming soon!

```bash
# Run benchmark locally
./scripts/run.sh --model anthropic/claude-sonnet-4 --no-upload
```

## Command Reference

| Flag | Description |
|------|-------------|
| `--model MODEL` | Model to test (e.g., `anthropic/claude-sonnet-4`) |
| `--suite SUITE` | `all`, `automated-only`, or comma-separated task IDs |
| `--runs N` | Number of runs per task for averaging |
| `--timeout-multiplier N` | Scale timeouts for slower models |
| `--output-dir DIR` | Where to save results (default: `results/`) |
| `--no-upload` | Skip uploading to leaderboard |

## Contributing Tasks

We welcome new tasks! Check out [`tasks/TASK_TEMPLATE.md`](tasks/TASK_TEMPLATE.md) for the format. Good tasks are:

- **Real-world** — Something an actual user would ask an agent to do
- **Measurable** — Clear success criteria that can be graded
- **Reproducible** — Same task should produce consistent grading
- **Challenging** — Tests agent capabilities, not just LLM knowledge

## Links

- **OpenClaw:** [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- **Issues:** [github.com/yyyyujiexin-dotcom/openfriday-bench/issues](https://github.com/yyyyujiexin-dotcom/openfriday-bench/issues)

## License

MIT — see [LICENSE](LICENSE) for details.

---

*OpenFriday Bench - Empowering AI agents with real-world testing* 🐾
