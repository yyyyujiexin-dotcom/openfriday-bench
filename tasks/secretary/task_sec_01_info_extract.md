# task_sec_01_info_extract

**能力**：内容关键信息提取
**评分**：自动
**超时**：90秒
**前置条件**：无

## 任务说明

工作区有一段混乱的会议速记 `raw_notes.txt`，请从中提取关键信息，保存为结构化文件 `extracted.json`，包含以下字段：

- `date`：会议日期
- `attendees`：参会人列表
- `decisions`：已确定事项列表
- `action_items`：待办事项列表（含负责人和截止日期）
- `blockers`：当前阻塞事项列表

## 输入文件

- `raw_notes.txt`（来自 dataset/secretary/task_sec_01_info_extract/）

## 评分标准

- `file_created`：extracted.json 是否存在
- `valid_json`：文件是否为合法 JSON
- `has_all_fields`：是否包含全部5个字段
- `attendees_complete`：参会人是否提取完整（≥4人）
- `action_items_present`：待办事项是否非空
- `blockers_present`：阻塞事项是否非空

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import json
    f = workspace_path / "extracted.json"
    if not f.exists():
        return {k: 0.0 for k in ["file_created","valid_json","has_all_fields","attendees_complete","action_items_present","blockers_present"]}
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except:
        return {"file_created":1.0,"valid_json":0.0,"has_all_fields":0.0,"attendees_complete":0.0,"action_items_present":0.0,"blockers_present":0.0}
    fields = ["date","attendees","decisions","action_items","blockers"]
    has_all = all(k in data for k in fields)
    attendees_ok = isinstance(data.get("attendees",[]), list) and len(data.get("attendees",[])) >= 4
    actions_ok = isinstance(data.get("action_items",[]), list) and len(data.get("action_items",[])) > 0
    blockers_ok = isinstance(data.get("blockers",[]), list) and len(data.get("blockers",[])) > 0
    return {
        "file_created": 1.0,
        "valid_json": 1.0,
        "has_all_fields": 1.0 if has_all else 0.0,
        "attendees_complete": 1.0 if attendees_ok else 0.0,
        "action_items_present": 1.0 if actions_ok else 0.0,
        "blockers_present": 1.0 if blockers_ok else 0.0,
    }
```

