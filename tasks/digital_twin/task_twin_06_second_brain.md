# task_twin_06_second_brain

**能力**：第二大脑（文件式持久化记忆）  
**评分**：混合（自动 50% + LLM Judge 50%）  
**超时**：180秒

## 任务说明

请把下面这段“个人信息”存入一个可复用的“记忆文件”，并在同一次任务中完成检索问答。

**需要记住的信息**：

- Favorite programming language: Rust
- Start learning date: January 15, 2024
- Mentor: Dr. Elena Vasquez (Stanford)
- Project: NeonDB (a distributed key-value store)
- Secret code phrase: "purple elephant sunrise"

**要求**：

1. 创建目录 `memory/`（如不存在）  
2. 将上述信息以结构化形式保存到 `memory/MEMORY.md`  
3. 读取 `memory/MEMORY.md` 并回答以下问题，将答案写入 `recall.txt`（每行一个答案）：
   1. What is my favorite programming language?
   2. When did I start learning it?
   3. What is my mentor's name and affiliation?
   4. What is my project called and what does it do?
   5. What is my team's secret code phrase?

## 评分标准

**自动**：

- `memory_file_created`：`memory/MEMORY.md` 是否存在  
- `recall_file_created`：`recall.txt` 是否存在  
- `has_rust`：是否包含 Rust  
- `has_date`：是否包含 January 15, 2024  
- `has_mentor`：是否包含 Elena Vasquez 与 Stanford  
- `has_project`：是否包含 NeonDB 与 distributed key-value store  
- `has_phrase`：是否包含 purple elephant sunrise

**LLM Judge**：存储格式是否清晰可扩展 · 回答是否严格基于文件且表达清晰

## 评分逻辑

```python
def grade(workspace_path, transcript):
    mem = workspace_path / "memory" / "MEMORY.md"
    recall = workspace_path / "recall.txt"

    if not mem.exists() or not recall.exists():
        return {
            "memory_file_created": 1.0 if mem.exists() else 0.0,
            "recall_file_created": 1.0 if recall.exists() else 0.0,
            "has_rust": 0.0,
            "has_date": 0.0,
            "has_mentor": 0.0,
            "has_project": 0.0,
            "has_phrase": 0.0,
        }

    m = mem.read_text(encoding="utf-8", errors="ignore").lower()
    r = recall.read_text(encoding="utf-8", errors="ignore").lower()
    combined = m + "\n" + r

    has_rust = 1.0 if "rust" in combined else 0.0
    has_date = 1.0 if ("january" in combined and "2024" in combined and "15" in combined) else 0.0
    has_mentor = 1.0 if ("elena" in combined and "vasquez" in combined and "stanford" in combined) else 0.0
    has_project = 1.0 if ("neondb" in combined and "distributed" in combined and "key-value" in combined) else 0.0
    has_phrase = 1.0 if ("purple" in combined and "elephant" in combined and "sunrise" in combined) else 0.0

    return {
        "memory_file_created": 1.0,
        "recall_file_created": 1.0,
        "has_rust": has_rust,
        "has_date": has_date,
        "has_mentor": has_mentor,
        "has_project": has_project,
        "has_phrase": has_phrase,
    }
```

