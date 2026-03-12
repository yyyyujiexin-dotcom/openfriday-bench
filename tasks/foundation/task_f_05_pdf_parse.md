# task_f_05_pdf_parse

**分组**：感知输入类  
**评分**：自动 pass/fail  
**超时**：60秒

## 任务说明

工作区有一个 PDF 文件 `report.pdf`，内容是一份产品报告。

请提取 PDF 全文，保存为 `extracted.txt`。

## 评分标准

- `file_created`: extracted.txt 是否存在
- `has_content`: 内容是否为非空（不评估正确性/相关性）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "extracted.txt"
    if not f.exists():
        return {"file_created": 0.0, "has_content": 0.0}

    content = f.read_text(encoding="utf-8", errors="ignore").strip()

    return {
        "file_created": 1.0,
        "has_content": 1.0 if len(content) > 0 else 0.0,
    }
```
