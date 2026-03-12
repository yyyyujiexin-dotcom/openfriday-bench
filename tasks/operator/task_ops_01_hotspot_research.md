# task_ops_01_hotspot_research

**能力**：热点/选题调研（联网搜索 + 信息抽取 + 结构化汇总）  
**评分**：LLM Judge  
**超时**：180秒

## 任务说明

请你为“科技行业从业者”做一份**本年度即将举行的 5 个重要技术大会**调研清单，输出到 `events.md`，每个大会必须包含：

- 大会名称
- 举办日期（尽量具体到日）
- 举办地点（城市/国家）
- 官方网站链接

## 评分标准

- `file_created`：`events.md` 是否存在
- `has_five_entries`：是否包含 5 个大会条目
- `has_name_date_location_url`：每条是否包含名称/日期/地点/链接
- `credible`：大会是否真实可核验（不鼓励编造）
- `format_clear`：排版是否清晰一致（Markdown 列表或表格均可）

## 评分逻辑（自动弱检查）

```python
def grade(workspace_path, transcript):
    import re
    f = workspace_path / "events.md"
    if not f.exists():
        return {"file_created": 0.0, "has_five_entries": 0.0, "has_urls": 0.0}
    content = f.read_text(encoding="utf-8", errors="ignore")
    # 以链接数量作为条目数量的近似（弱检查）
    urls = re.findall(r"https?://\\S+", content)
    has_urls = 1.0 if len(urls) >= 5 else 0.0
    has_five = 1.0 if len(urls) >= 5 else 0.0
    return {"file_created": 1.0, "has_five_entries": has_five, "has_urls": has_urls}
```

