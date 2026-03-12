# task_twin_02_knowledge_recall

**能力**：从本地知识库/上下文文件中精准检索答案  
**评分**：自动 pass/fail  
**超时**：90秒

## 任务说明

工作区提供一份项目笔记 `notes.md`（来自 `dataset/digital_twin/task_twin_02_knowledge_recall/`）。请阅读后回答：

> Beta release 的截止日期是什么？

将答案写入 `answer.txt`。要求答案清晰，包含日期（如 “June 1, 2024” 或等价格式），并明确指出这是 beta release 的 deadline。

## 评分标准

- `file_created`：`answer.txt` 是否存在
- `correct_date`：是否包含 June 1, 2024（或等价日期格式）
- `clear_answer`：是否明确回答了“beta release deadline”
- `read_notes`：transcript 中是否出现读取 notes.md 的行为（弱检查）
- `no_hallucination`：是否没有写成其他里程碑日期（如 March 15 / September 30）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re

    f = workspace_path / "answer.txt"
    if not f.exists():
        return {
            "file_created": 0.0,
            "correct_date": 0.0,
            "clear_answer": 0.0,
            "read_notes": 0.0,
            "no_hallucination": 0.0,
        }

    content = f.read_text(encoding="utf-8", errors="ignore").lower()

    date_patterns = [
        r"june\\s+1,?\\s+2024",
        r"june\\s+1st,?\\s+2024",
        r"6/1/2024",
        r"6-1-2024",
        r"2024-06-01",
        r"1\\s+june\\s+2024",
    ]
    correct_date = 1.0 if any(re.search(p, content) for p in date_patterns) else 0.0

    if len(content.strip()) > 10 and ("beta" in content or "release" in content or "deadline" in content):
        clear_answer = 1.0
    elif len(content.strip()) > 5:
        clear_answer = 0.5
    else:
        clear_answer = 0.0

    t = (transcript or "").lower()
    read_notes = 1.0 if "notes.md" in t else 0.0

    wrong_dates = [r"march\\s+15", r"september\\s+30", r"3/15", r"9/30"]
    no_hallucination = 0.0 if any(re.search(p, content) for p in wrong_dates) else 1.0

    return {
        "file_created": 1.0,
        "correct_date": correct_date,
        "clear_answer": clear_answer,
        "read_notes": read_notes,
        "no_hallucination": no_hallucination,
    }
```

