# task_f_13_long_context

**分组**：记忆与状态类  
**评分**：自动 pass/fail  
**超时**：120秒

## 任务说明

工作区有一份长文档 `long_doc.txt`（约 8000 字的产品需求文档），文档第 7500 字处藏有一句话：「隐藏关键词：蓝色大象」。

请阅读全文，找出隐藏关键词，保存到 `answer.txt`。

## 评分标准

- `file_created`: answer.txt 是否存在
- `found_keyword`: 是否包含「蓝色大象」或「blue elephant」

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "answer.txt"
    if not f.exists(): return {"file_created":0.0,"found_keyword":0.0}
    c = f.read_text(encoding="utf-8",errors="ignore")
    found = any(w in c for w in ["蓝色大象","blue elephant","蓝色","大象"])
    return {"file_created":1.0,"found_keyword":1.0 if found else 0.0}
```