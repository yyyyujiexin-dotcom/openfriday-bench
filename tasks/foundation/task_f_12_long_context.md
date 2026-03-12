# task_f_12_long_context

**分组**：记忆与状态类  
**评分**：自动 pass/fail  
**超时**：120秒

## 任务说明

工作区有一份长文档 `long_doc.txt`（约 8000 字的产品需求文档），文档第 7500 字处藏有一句话：「隐藏关键词：蓝色大象」。

请阅读全文，找出隐藏关键词，保存到 `answer.txt`。

## 评分标准

- `file_created`: answer.txt 是否存在
- `has_answer`: 内容是否为非空（不评估正确性/相关性）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "answer.txt"
    if not f.exists(): return {"file_created":0.0,"has_answer":0.0}
    c = f.read_text(encoding="utf-8",errors="ignore").strip()
    return {"file_created":1.0,"has_answer":1.0 if len(c)>0 else 0.0}
```

