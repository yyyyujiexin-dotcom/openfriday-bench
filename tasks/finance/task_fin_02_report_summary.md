# task_fin_02_report_summary

**能力**：PDF/研报解析 → 要点摘要输出  
**评分**：LLM Judge  
**超时**：240秒

## 任务说明

工作区有一份 PDF 研报 `report.pdf`（来自 `dataset/finance/task_fin_02_report_summary/`）。请完成：

1. 阅读并理解 PDF 内容  
2. 输出一份结构化摘要到 `report_summary.md`，至少包含：
   - 核心结论（3–5 条要点）
   - 关键数据/指标（如有，用表格或列表呈现）
   - 风险与不确定性
   - 一句话结论（给忙碌读者）

## 评分标准（自动弱检查）

- `file_created`：`report_summary.md` 是否存在  
- `has_sections`：是否包含多个小节标题（弱检查）  
- `has_bullets_or_table`：是否包含要点列表或表格（弱检查）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re
    f = workspace_path / "report_summary.md"
    if not f.exists():
        return {"file_created": 0.0, "has_sections": 0.0, "has_bullets_or_table": 0.0}
    content = f.read_text(encoding="utf-8", errors="ignore")
    headings = re.findall(r"^#{1,3}\s+.+", content, re.MULTILINE)
    has_sections = 1.0 if len(headings) >= 2 else 0.0
    has_bullets_or_table = 1.0 if (re.search(r"^[-*]\s+", content, re.MULTILINE) or re.search(r"\|.*\|.*\|", content)) else 0.0
    return {"file_created": 1.0, "has_sections": has_sections, "has_bullets_or_table": has_bullets_or_table}
```

