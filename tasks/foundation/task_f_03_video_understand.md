# task_f_03_video_understand 🔬

**分组**：感知输入类（实验性）  
**评分**：自动 pass/fail  
**超时**：120秒

> 🔬 实验性任务：OpenClaw 视频能力尚不稳定，评分逻辑待补充

## 任务说明

工作区有一段 30 秒的视频 `demo.mp4`（内容：产品功能演示）。

请生成视频摘要，保存到 `video_summary.txt`，要求：
- 说明视频主要内容
- 列出视频中出现的关键画面或步骤

## 评分标准（占位）

- `file_created`: video_summary.txt 是否存在
- `has_content`: 内容长度是否超过 50 字

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "video_summary.txt"
    if not f.exists(): return {"file_created":0.0,"has_content":0.0}
    c = f.read_text(encoding="utf-8",errors="ignore")
    return {"file_created":1.0, "has_content":1.0 if len(c)>50 else 0.0}
```