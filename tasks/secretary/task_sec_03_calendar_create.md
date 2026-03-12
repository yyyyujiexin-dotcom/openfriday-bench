# task_sec_03_calendar_create

**能力**：日程创建
**评分**：自动
**超时**：120秒
**前置条件**：✅ 飞书日历 或 Google Calendar 已接入 OpenClaw

## 任务说明

请根据以下信息，在日历中创建一个会议日程，并将创建结果（事件ID或确认信息）保存到 `calendar_result.txt`：

- 标题：Q2产品规划对齐会
- 时间：下周一 14:00 - 15:30
- 参会人：张伟、李娜、王芳
- 地点：会议室B
- 备注：请提前准备Q2 OKR草稿

## 评分标准

- `file_created`：calendar_result.txt 是否存在
- `file_not_empty`：文件内容非空
- `mentions_title`：结果中包含「Q2」或「规划」（证明标题写入成功）
- `mentions_time`：结果中包含时间相关信息（「14」或「下周」或「monday」）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "calendar_result.txt"
    if not f.exists():
        return {k: 0.0 for k in ["file_created","file_not_empty","mentions_title","mentions_time"]}
    content = f.read_text(encoding="utf-8").strip()
    mentions_title = any(w in content for w in ["Q2","规划","q2"])
    mentions_time = any(w in content for w in ["14","下周","monday","Monday","14:00"])
    return {
        "file_created":   1.0,
        "file_not_empty": 1.0 if len(content) > 0 else 0.0,
        "mentions_title": 1.0 if mentions_title else 0.0,
        "mentions_time":  1.0 if mentions_time else 0.0,
    }
```

