# task_f_07_text_to_speech 🔬

**分组**：生成输出类（实验性）  
**评分**：自动 pass/fail  
**超时**：90秒

> 🔬 实验性任务：OpenClaw 语音生成能力尚不稳定，评分逻辑待补充

## 任务说明

请将以下文字转换为语音，保存为音频文件 `output.mp3`：

> 你好，今天是2026年3月10日，祝你工作顺利。

## 评分标准（占位）

- `file_created`: output.mp3 是否存在
- `file_not_empty`: 文件大小是否大于 1KB

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "output.mp3"
    exists = f.exists()
    return {
        "file_created": 1.0 if exists else 0.0,
        "file_not_empty": 1.0 if exists and f.stat().st_size > 1024 else 0.0,
    }
```