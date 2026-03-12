# task_f_08_markdown_output

**分组**：生成输出类  
**评分**：自动 pass/fail  
**超时**：60秒

## 任务说明

请生成一份 Markdown 格式的「AI工具对比报告」，保存到 `report.md`，必须包含：

1. 一级标题（# 开头）
2. 至少两个二级标题（## 开头）
3. 一个 Markdown 表格（至少 3 列 3 行）
4. 一个无序列表（- 开头，至少 3 项）

内容主题不限，格式必须正确。

## 评分标准

- `file_created`: report.md 是否存在
- `has_h1`: 是否有一级标题
- `has_h2`: 是否有至少 2 个二级标题
- `has_table`: 是否有 Markdown 表格（含 | 分隔符）
- `has_list`: 是否有无序列表

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re
    f = workspace_path / "report.md"
    if not f.exists(): return {k:0.0 for k in ["file_created","has_h1","has_h2","has_table","has_list"]}
    c = f.read_text(encoding="utf-8",errors="ignore")
    return {
        "file_created": 1.0,
        "has_h1": 1.0 if re.search(r'^# [^#]',c,re.M) else 0.0,
        "has_h2": 1.0 if len(re.findall(r'^## ',c,re.M))>=2 else 0.0,
        "has_table": 1.0 if re.search(r'^\|.+\|.+\|',c,re.M) else 0.0,
        "has_list": 1.0 if len(re.findall(r'^- ',c,re.M))>=3 else 0.0,
    }
```

