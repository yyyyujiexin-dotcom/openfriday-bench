# task_f_12_cross_session

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
- `reflects_preference`: 简报是否体现了偏好（要点式、不冗长）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    brief = workspace_path / "brief.txt"
    brief_exists = brief.exists()
    content = brief.read_text(encoding="utf-8",errors="ignore") if brief_exists else ""
    # 要点式：包含 - 或 · 或数字列表
    import re
    is_bullet = bool(re.search(r'^[-·\d]',content,re.M))
    # 不冗长：少于 300 字
    not_long = len(content) < 300
    return {
        "memory_stored": 1.0,  # 实际需检查 OpenClaw 记忆 API
        "brief_created": 1.0 if brief_exists else 0.0,
        "reflects_preference": 1.0 if is_bullet and not_long else 0.0,
    }
```