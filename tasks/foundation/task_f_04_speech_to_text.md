# task_f_04_speech_to_text 🔬

**分组**：感知输入类（实验性）  
**评分**：自动 pass/fail  
**超时**：90秒

> 🔬 实验性任务：OpenClaw 语音能力尚不稳定，评分逻辑待补充

## 任务说明

工作区有一段音频 `audio.wav`（内容：普通话朗读，约 20 秒）。

请将音频转录为文字，保存到 `transcript.txt`。

## 评分标准（占位）

- `file_created`: transcript.txt 是否存在
- `has_content`: 内容长度是否超过 20 字（非空转录）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "transcript.txt"
    if not f.exists(): return {"file_created":0.0,"has_content":0.0}
    c = f.read_text(encoding="utf-8",errors="ignore").strip()
    return {"file_created":1.0, "has_content":1.0 if len(c)>20 else 0.0}
```