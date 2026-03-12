# task_f_02_image_understand

**分组**：感知输入类  
**评分**：自动 pass/fail  
**超时**：60秒

## 任务说明

工作区有一张图片 `test_image.jpg`（内容：一只橙色的猫坐在窗边）。

请描述图片内容，保存到 `description.txt`。

## workspace_files

```
test_image.jpg  ← 橙色猫咪图片（benchmark 运行时注入）
```

## 评分标准

- `file_created`: description.txt 是否存在
- `has_description`: 是否产出了实质性的图片描述（非空、且非「无法识别」等拒绝类回复；不区分能力来自模型本身还是工具）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "description.txt"
    if not f.exists():
        return {"file_created": 0.0, "has_description": 0.0}

    content = f.read_text(encoding="utf-8", errors="ignore").strip()
    c_lower = content.lower()

    # 拒绝/无法识别类回复不算「有描述」
    refusal_phrases = [
        "无法识别", "无法辨认", "看不到", "不能识别", "无法看到", "没有图片",
        "cannot recognize", "i cannot see", "i'm unable to", "i don't have",
        "no image", "cannot view", "unable to identify", "can't see the image",
    ]
    is_refusal = any((p in content) or (p in c_lower) for p in refusal_phrases)

    has_description = len(content) > 10 and not is_refusal

    return {
        "file_created": 1.0,
        "has_description": 1.0 if has_description else 0.0,
    }
```
