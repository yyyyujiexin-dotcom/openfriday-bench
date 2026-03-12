# task_f_15_doc_summary

**分组**：生成输出类  
**评分**：LLM Judge  
**超时**：90秒

## 任务说明

工作区提供一份输入文本 `summary_source.txt`（来自 `dataset/foundation/task_f_15_doc_summary/`）。请阅读后输出到 `summary_output.txt`，要求：

- **恰好 3 段**（用空行分隔）
- 第 1 段：主题与整体概述  
- 第 2 段：关键应用与收益（至少提到 2 个点）  
- 第 3 段：挑战/风险与未来展望  

## 评分标准（自动弱检查）

- `file_created`：`summary_output.txt` 是否存在
- `three_paragraphs`：是否恰好 3 段
- `not_empty`：是否非空（> 200 字符）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re

    f = workspace_path / "summary_output.txt"
    if not f.exists():
        return {"file_created": 0.0, "three_paragraphs": 0.0, "not_empty": 0.0}

    content = f.read_text(encoding="utf-8", errors="ignore").strip()
    paras = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]

    return {
        "file_created": 1.0,
        "three_paragraphs": 1.0 if len(paras) == 3 else 0.0,
        "not_empty": 1.0 if len(content) >= 200 else 0.0,
    }
```

