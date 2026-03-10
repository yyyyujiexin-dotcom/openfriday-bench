# task_f_06_table_read

**分组**：感知输入类  
**评分**：自动 pass/fail  
**超时**：60秒

## 任务说明

工作区有一个 CSV 文件 `sales.csv`：

```
月份,销售额,环比增长
1月,85000,+12%
2月,91000,+7%
3月,78000,-14%
```

请回答：哪个月销售额最高？将答案保存到 `answer.txt`。

## 评分标准

- `file_created`: answer.txt 是否存在
- `correct_answer`: 是否包含「2月」或「February」或「91000」

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "answer.txt"
    if not f.exists(): return {"file_created":0.0,"correct_answer":0.0}
    c = f.read_text(encoding="utf-8",errors="ignore")
    correct = any(w in c for w in ["2月","February","91000","二月"])
    return {"file_created":1.0, "correct_answer":1.0 if correct else 0.0}
```