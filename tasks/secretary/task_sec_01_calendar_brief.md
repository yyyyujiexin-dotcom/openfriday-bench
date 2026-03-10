# task_sec_01_calendar_brief

**评分**：自动  
**超时**：120秒

## 任务说明

工作区有日历文件 `calendar.json`，包含今日 3 个日程。

请生成今日行程简报，保存为 `daily_brief.md`：
- 标题：`# 今日行程简报 - {日期}`
- 按时间顺序列出每个事项（时间、标题、参会人、地点）
- 末尾附事项总数统计

## Mock 数据

```json
{
  "date": "2026-03-10",
  "events": [
    {"title":"产品周会","start":"09:00","end":"10:00","attendees":["张伟","李娜","王芳"],"location":"会议室A"},
    {"title":"与MiniMax对接","start":"14:00","end":"15:00","attendees":["陈强","MiniMax技术团队"],"location":"线上Zoom"},
    {"title":"1on1 with 李娜","start":"16:30","end":"17:00","attendees":["李娜"],"location":"工位旁"}
  ]
}
```

## 评分标准

- `file_created` · `has_title` · `event_count_correct`
- `time_ordered` · `attendees_present` · `location_present` · `summary_line`