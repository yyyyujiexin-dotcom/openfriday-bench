# task_ops_02_content_writing

**能力**：内容写作（结构化长文 + Markdown 输出）  
**评分**：LLM Judge  
**超时**：180秒

## 任务说明

请写一篇约 500 词（400–600 词可接受）的英文博客，主题为：

> The benefits of remote work for software developers

要求：

- 结构完整（引言 / 主体 / 结尾）
- 覆盖多个不同维度的好处，并给出理由或例子
- 使用合适的 Markdown 格式（可用标题与列表，但不应只有列表）
- 保存到 `blog_post.md`

## 评分标准（自动弱检查）

- `file_created`：`blog_post.md` 是否存在  
- `not_empty`：内容是否非空（> 200 词近似阈值）  
- `has_markdown`：是否包含 Markdown 标题或分段结构（弱检查）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re
    f = workspace_path / "blog_post.md"
    if not f.exists():
        return {"file_created": 0.0, "not_empty": 0.0, "has_markdown": 0.0}
    content = f.read_text(encoding="utf-8", errors="ignore").strip()
    words = re.findall(r"\b\w+\b", content)
    has_md = 1.0 if ("#" in content or "\n\n" in content) else 0.0
    return {
        "file_created": 1.0,
        "not_empty": 1.0 if len(words) >= 200 else 0.0,
        "has_markdown": has_md,
    }
```

