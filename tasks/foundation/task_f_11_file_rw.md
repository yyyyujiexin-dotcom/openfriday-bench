# task_f_11_file_rw

**分组**：记忆与状态类  
**评分**：自动 pass/fail  
**超时**：60秒

## 任务说明

请完成以下三步文件操作：

1. 创建文件 `note.txt`，写入内容：「第一次写入」
2. 读取 `note.txt` 的内容，确认读取成功
3. 在 `note.txt` 末尾追加内容：「第二次追加」
4. 将最终文件内容写入 `result.txt`

## 评分标准

- `note_created`: note.txt 是否存在
- `result_created`: result.txt 是否存在
- `has_first_write`: result.txt 是否包含「第一次写入」
- `has_append`: result.txt 是否包含「第二次追加」

## 评分逻辑

```python
def grade(workspace_path, transcript):
    note = workspace_path / "note.txt"
    result = workspace_path / "result.txt"
    if not result.exists():
        return {"note_created":1.0 if note.exists() else 0.0,"result_created":0.0,"has_first_write":0.0,"has_append":0.0}
    c = result.read_text(encoding="utf-8",errors="ignore")
    return {
        "note_created": 1.0 if note.exists() else 0.0,
        "result_created": 1.0,
        "has_first_write": 1.0 if "第一次写入" in c else 0.0,
        "has_append": 1.0 if "第二次追加" in c else 0.0,
    }
```