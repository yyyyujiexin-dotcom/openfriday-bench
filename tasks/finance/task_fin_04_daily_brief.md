# task_fin_04_daily_brief

**能力**：多源信息综合 → 每日金融简报（优先级与行动项）  
**评分**：LLM Judge  
**超时**：180秒

## 任务说明

工作区的 `research/` 目录下包含多份文本材料（来自 `dataset/finance/task_fin_04_daily_brief/`）。请你：

1. 主动发现并阅读 `research/` 目录内的全部文件  
2. 生成一份面向“管理层读者”的每日简报，保存到 `daily_briefing.md`，要求：
   - 开头给出 3–5 条 Executive Summary（要点式）
   - 分小节覆盖：市场/宏观、竞品与行业、客户与风险、产品与研发进展等（按材料内容）
   - 明确指出需要关注/决策的事项（Action Items / Decisions）
   - 保持简洁但信息密度高（建议 500–800 词或等价中文篇幅）

## 评分标准（自动弱检查）

- `file_created`：`daily_briefing.md` 是否存在  
- `has_exec_summary`：是否包含“Executive Summary/要点/关键结论”等段落（弱检查）  
- `has_sections`：是否包含多个小节标题（弱检查）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re
    f = workspace_path / "daily_briefing.md"
    if not f.exists():
        return {"file_created": 0.0, "has_exec_summary": 0.0, "has_sections": 0.0}
    content = f.read_text(encoding="utf-8", errors="ignore")
    lower = content.lower()
    has_exec = 1.0 if any(k in lower for k in ["executive summary", "key takeaways", "要点", "关键结论"]) else 0.0
    headings = re.findall(r"^#{1,3}\\s+.+", content, re.MULTILINE)
    has_sections = 1.0 if len(headings) >= 3 else 0.0
    return {"file_created": 1.0, "has_exec_summary": has_exec, "has_sections": has_sections}
```

