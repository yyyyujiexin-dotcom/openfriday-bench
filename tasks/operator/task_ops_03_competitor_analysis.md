# task_ops_03_competitor_analysis

**能力**：竞品/市场调研（结构化报告 + 对比表）  
**评分**：混合（自动 50% + LLM Judge 50%）  
**超时**：240秒

## 任务说明

请围绕 **enterprise observability & APM（应用性能监控）** 市场，输出一份竞品格局分析到 `market_research.md`，要求：

- 至少列出 5 家主流厂商（例如 Datadog / New Relic / Dynatrace / Splunk / Grafana Labs / Elastic 等）
- 每家厂商写出：定位与差异点、典型定价模型（按 host/GB/user 等）、优缺点
- 提供一张 Markdown 对比表（至少包含：厂商、核心卖点、定价模型、适用人群/场景）
- 额外写一个“市场趋势”小节（例如 OpenTelemetry、AI 观测、云原生、计量计费等）

允许联网搜索以保证信息更新（鼓励），但也可用常识完成（会影响 Judge 评分）。

## 评分标准

**自动**：

- `file_created`：`market_research.md` 是否存在  
- `competitors_identified`：是否出现 ≥5 个常见竞品关键词  
- `has_comparison_table`：是否包含 Markdown 表格  
- `has_pricing_info`：是否包含定价相关信息  
- `has_trends_section`：是否包含趋势相关关键词  
- `has_structure`：是否包含多个标题（# / ##）

**LLM Judge**：信息具体性与准确性 · 分析与对比质量 · 结构与表达专业度

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re

    f = workspace_path / "market_research.md"
    if not f.exists():
        return {k: 0.0 for k in [
            "file_created",
            "competitors_identified",
            "has_comparison_table",
            "has_pricing_info",
            "has_trends_section",
            "has_structure",
        ]}

    content = f.read_text(encoding="utf-8", errors="ignore")
    lower = content.lower()

    known = [
        "datadog", "new relic", "dynatrace", "splunk", "grafana",
        "elastic", "appdynamics", "honeycomb", "instana", "sentry",
    ]
    found = [c for c in known if c in lower]
    competitors = 1.0 if len(found) >= 5 else (0.5 if len(found) >= 3 else (0.25 if len(found) >= 1 else 0.0))

    has_table = 1.0 if (re.search(r"\|.*\|.*\|", content) and re.search(r"\|[\s-]+\|", content)) else 0.0

    pricing_hits = sum(1 for p in [r"pric", r"per[\s-]?(host|gb|user|seat)", r"\$\d+", r"subscription", r"cost"] if re.search(p, lower))
    pricing = 1.0 if pricing_hits >= 3 else (0.5 if pricing_hits >= 1 else 0.0)

    trends_hits = sum(1 for p in [r"trend", r"opentelemetry", r"otel", r"cloud[\s-]?native", r"ai", r"consumption"] if re.search(p, lower))
    trends = 1.0 if trends_hits >= 3 else (0.5 if trends_hits >= 1 else 0.0)

    headings = re.findall(r"^#{1,3}\s+.+", content, re.MULTILINE)
    structure = 1.0 if len(headings) >= 6 else (0.5 if len(headings) >= 3 else 0.0)

    return {
        "file_created": 1.0,
        "competitors_identified": competitors,
        "has_comparison_table": has_table,
        "has_pricing_info": pricing,
        "has_trends_section": trends,
        "has_structure": structure,
    }
```

