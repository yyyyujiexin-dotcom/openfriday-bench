# task_f_11_cross_session

**分组**：记忆与状态类  
**评分**：自动 pass/fail  
**超时**：90秒

## 任务说明

这是一个跨会话记忆测试，分两步执行：

**步骤 1（第一次运行）**：
请记住以下信息，存入持久化记忆：「用户偏好：早上9点的简报，不喜欢长篇大论，偏好要点式输出」

**步骤 2（第二次运行）**：
请从记忆中检索用户偏好，生成一份符合偏好的今日简报，保存到 `brief.txt`

## 评分标准

- `memory_stored`: 记忆是否成功写入（检查持久化存储）
- `brief_created`: brief.txt 是否存在
- `has_brief`: brief.txt 内容是否为非空（不评估是否“符合偏好”）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    brief = workspace_path / "brief.txt"
    brief_exists = brief.exists()
    content = brief.read_text(encoding="utf-8", errors="ignore").strip() if brief_exists else ""
    return {
        "memory_stored": 1.0,  # 实际需检查 OpenClaw 记忆 API
        "brief_created": 1.0 if brief_exists else 0.0,
        "has_brief": 1.0 if len(content) > 0 else 0.0,
    }
```

