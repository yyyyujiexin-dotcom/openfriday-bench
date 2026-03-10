# task_f_10_realtime_voice 🔬

**分组**：生成输出类（实验性）  
**评分**：自动 pass/fail  
**超时**：120秒

> 🔬 实验性任务：OpenClaw 实时语音对话能力尚不稳定，评分逻辑待补充

## 任务说明

模拟一段 3 轮语音对话，将每轮的用户输入和 Agent 回复记录到 `voice_log.txt`：

- 轮次 1：用户问「今天天气怎么样」
- 轮次 2：用户问「需要带伞吗」
- 轮次 3：用户说「谢谢」

## 评分标准（占位）

- `file_created`: voice_log.txt 是否存在
- `has_3_rounds`: 是否记录了 3 轮对话

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "voice_log.txt"
    if not f.exists(): return {"file_created":0.0,"has_3_rounds":0.0}
    c = f.read_text(encoding="utf-8",errors="ignore")
    rounds = c.count("轮次") or c.count("Round") or c.count("用户：")
    return {"file_created":1.0,"has_3_rounds":1.0 if rounds>=3 else 0.0}
```