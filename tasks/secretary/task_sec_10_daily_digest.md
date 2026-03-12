# task_sec_10_daily_digest

**能力**：主动情报 · 定时摘要推送
**评分**：自动
**超时**：180秒
**前置条件**：✅ 任意 IM 渠道已接入 + OpenClaw cron 已启用

## 任务说明

请设置一个定时任务：**每天早上 9:00**，自动收集以下信息并通过 IM 推送给我：

1. 今日日历事项（如有日历接入）
2. 未读重要消息摘要
3. 今日值得关注的行业资讯（联网搜索）

将定时任务的配置信息和一次立即执行的测试结果保存到 `digest_setup.txt`。

## 评分标准

- `file_created`：digest_setup.txt 是否存在
- `file_not_empty`：内容非空
- `cron_configured`：包含定时相关词（「09:00」「每天」「cron」「定时」）
- `test_sent`：包含发送确认词（「已发送」「sent」「success」「成功」）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "digest_setup.txt"
    if not f.exists():
        return {k: 0.0 for k in ["file_created","file_not_empty","cron_configured","test_sent"]}
    content = f.read_text(encoding="utf-8").strip()
    cron_ok = any(w in content for w in ["09:00","9:00","每天","cron","定时","daily"])
    sent_ok = any(w in content.lower() for w in ["已发送","sent","success","成功","发送成功"])
    return {
        "file_created":   1.0,
        "file_not_empty": 1.0 if len(content) > 0 else 0.0,
        "cron_configured":1.0 if cron_ok else 0.0,
        "test_sent":      1.0 if sent_ok else 0.0,
    }
```

