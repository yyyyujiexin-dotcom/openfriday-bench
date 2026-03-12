# task_f_14_task_planning

**分组**：推理与协调类  
**评分**：自动 pass/fail  
**超时**：90秒

## 任务说明

我需要「下周一在上海举办一场50人的产品发布会」，但我完全不知道从哪里开始。

请帮我制定一份详细的执行计划，保存到 `plan.md`，要求：
- 拆解为具体可执行的子任务
- 每个子任务标注负责方向和预计耗时
- 按时间顺序排列（倒推法，从发布会当天往前排）

## 评分标准

- `file_created`: plan.md 是否存在
- `has_subtasks`: 是否有至少 5 个子任务
- `has_timeline`: 是否有时间信息（天/小时/周）
- `is_ordered`: 是否有顺序结构（数字列表或时间排序）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re
    f = workspace_path / "plan.md"
    if not f.exists(): return {k:0.0 for k in ["file_created","has_subtasks","has_timeline","is_ordered"]}
    c = f.read_text(encoding="utf-8",errors="ignore")
    subtasks = len(re.findall(r'^[-\d]',c,re.M))
    has_time = bool(re.search(r'\d+天|\d+小时|\d+周|天前|提前',c))
    is_ordered = bool(re.search(r'^[1-9]\.',c,re.M)) or bool(re.search(r'第[一二三四五]',c))
    return {
        "file_created": 1.0,
        "has_subtasks": 1.0 if subtasks>=5 else 0.0,
        "has_timeline": 1.0 if has_time else 0.0,
        "is_ordered": 1.0 if is_ordered else 0.0,
    }
```

