# task_sec_06_doc_generation

**能力**：结构化文档生成（周报 / 纪要）
**评分**：混合（自动 50% + LLM Judge 50%）
**超时**：150秒
**前置条件**：无

## 任务说明

工作区有一份零散的本周工作记录 `work_log.txt`，请生成一份规范的**周报** `weekly_report.md`，包含：

- 标题 + 周次 + 日期范围
- 本周完成事项（分条列出）
- 下周计划（分条列出）
- 需要协调/上升的问题（如有）

## 输入文件

- `work_log.txt`（来自 dataset/secretary/task_sec_06_doc_generation/）

## 评分标准

**自动**：
- `file_created` · `has_title` · `has_completed_section` · `has_next_week_section` · `item_count_sufficient`（完成事项≥4条）

**LLM Judge**：内容提炼质量 · 语言专业规范 · 结构完整清晰

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re
    f = workspace_path / "weekly_report.md"
    if not f.exists():
        return {k: 0.0 for k in ["file_created","has_title","has_completed_section","has_next_week_section","item_count_sufficient"]}
    content = f.read_text(encoding="utf-8")
    has_title = content.strip().startswith("#")
    has_completed = any(w in content for w in ["本周","完成","已完成","这周"])
    has_next_week = any(w in content for w in ["下周","下周计划","next week","待办"])
    # 计算列表项数量（- 或数字开头的行）
    items = re.findall(r'^[\-\*\d]', content, re.MULTILINE)
    item_count_ok = len(items) >= 4
    return {
        "file_created":          1.0,
        "has_title":             1.0 if has_title else 0.0,
        "has_completed_section": 1.0 if has_completed else 0.0,
        "has_next_week_section": 1.0 if has_next_week else 0.0,
        "item_count_sufficient": 1.0 if item_count_ok else 0.0,
    }
```

