# task_f_03_video_understand 🔬

**分组**：感知输入类
**评分**：自动 pass/fail  
**超时**：120秒


## 任务说明

工作区有一段 30 秒的视频 `demo.mp4`（内容：产品功能演示）。

请生成视频摘要，保存到 `video_summary.txt`，要求：
- 说明视频主要内容
- 列出视频中出现的关键画面或步骤

## 评分标准

- `file_created`: video_summary.txt 是否存在
- `has_content`: 是否产出了实质性视频摘要（非空、且非「无法识别/无法处理视频」等拒绝类回复；不区分能力来自模型本身还是工具）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "video_summary.txt"
    if not f.exists():
        return {"file_created": 0.0, "has_content": 0.0}

    content = f.read_text(encoding="utf-8", errors="ignore").strip()
    c_lower = content.lower()

    refusal_phrases = [
        "无法识别", "无法处理", "无法分析", "看不到", "不能识别", "不支持视频",
        "cannot recognize", "cannot process", "i cannot see", "i'm unable to",
        "no video", "cannot analyze", "unable to process", "can't process the video",
    ]
    is_refusal = any((p in content) or (p in c_lower) for p in refusal_phrases)

    # 仅排除空或极短敷衍，不按字数设硬门槛
    has_content = len(content) > 0 and not is_refusal

    return {
        "file_created": 1.0,
        "has_content": 1.0 if has_content else 0.0,
    }
```
