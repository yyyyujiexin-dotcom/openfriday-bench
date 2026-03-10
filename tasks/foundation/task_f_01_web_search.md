# task_f_01_web_search

**分组**：感知输入类  
**评分**：自动 pass/fail  
**超时**：60秒

## 任务说明

请搜索「2026年春节是哪一天」，将搜索结果保存到 `result.txt`。

## 期望行为

Agent 调用联网搜索工具，获取结果，将包含日期的答案写入文件。

## 评分标准

- `file_created`: result.txt 是否存在
- `has_date`: 文件内容是否包含「1月」或「January」或具体日期数字

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "result.txt"
    if not f.exists(): return {"file_created": 0.0, "has_date": 0.0}
    content = f.read_text(encoding="utf-8", errors="ignore")
    has_date = any(w in content for w in ["1月", "January", "29", "春节"])
    return {"file_created": 1.0, "has_date": 1.0 if has_date else 0.0}
```