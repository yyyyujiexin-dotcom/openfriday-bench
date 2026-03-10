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
- `mentions_cat`: 是否提到猫/cat/动物
- `mentions_color`: 是否提到橙色/orange/黄色

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "description.txt"
    if not f.exists(): return {"file_created":0.0,"mentions_cat":0.0,"mentions_color":0.0}
    c = f.read_text(encoding="utf-8",errors="ignore").lower()
    return {
        "file_created": 1.0,
        "mentions_cat": 1.0 if any(w in c for w in ["猫","cat","动物","animal"]) else 0.0,
        "mentions_color": 1.0 if any(w in c for w in ["橙","orange","黄","金"]) else 0.0,
    }
```