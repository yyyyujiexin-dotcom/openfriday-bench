# task_f_04_speech_to_text 🔬

**分组**：感知输入类
**评分**：自动 pass/fail  
**超时**：90秒


## 任务说明

工作区有一段音频 `audio.wav`（内容：一段语音）。

请将音频转录为文字，保存到 `transcript.txt`。

## 评分标准

- `file_created`: transcript.txt 是否存在
- `has_content`: 是否产出了实质性转录（非空、且非「无法识别/无法处理音频」等拒绝类回复；不区分能力来自模型本身还是工具）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "transcript.txt"
    if not f.exists():
        return {"file_created": 0.0, "has_content": 0.0}

    content = f.read_text(encoding="utf-8", errors="ignore").strip()
    c_lower = content.lower()

    refusal_phrases = [
        "无法识别", "无法处理", "无法转写", "听不到", "不能识别", "不支持音频",
        "cannot recognize", "cannot process", "i cannot hear", "i'm unable to",
        "no audio", "cannot transcribe", "unable to process", "can't process the audio",
    ]
    is_refusal = any((p in content) or (p in c_lower) for p in refusal_phrases)

    has_content = len(content) > 20 and not is_refusal

    return {
        "file_created": 1.0,
        "has_content": 1.0 if has_content else 0.0,
    }
```
