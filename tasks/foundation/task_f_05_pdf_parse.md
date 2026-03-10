# task_f_05_pdf_parse

**分组**：感知输入类  
**评分**：自动 pass/fail  
**超时**：60秒

## 任务说明

工作区有一个 PDF 文件 `report.pdf`，内容是一份两页的产品报告，第一页包含标题「2026年Q1产品报告」，第二页包含数据「MAU：120万」。

请提取 PDF 全文，保存到 `extracted.txt`。

## 评分标准

- `file_created`: extracted.txt 是否存在
- `has_title`: 是否包含「Q1」或「产品报告」
- `has_data`: 是否包含「MAU」或「120」

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "extracted.txt"
    if not f.exists(): return {"file_created":0.0,"has_title":0.0,"has_data":0.0}
    c = f.read_text(encoding="utf-8",errors="ignore")
    return {
        "file_created": 1.0,
        "has_title": 1.0 if any(w in c for w in ["Q1","产品报告"]) else 0.0,
        "has_data": 1.0 if any(w in c for w in ["MAU","120"]) else 0.0,
    }
```