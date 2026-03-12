# task_f_13_tool_chain

**分组**：推理与协调类  
**评分**：自动 pass/fail  
**超时**：180秒

## 任务说明

请完成以下需要多工具串联的任务：

1. 搜索「特斯拉 Model 3 2026款价格」
2. 读取工作区文件 `budget.txt`（内容：我的预算是30万元）
3. 根据搜索结果和预算，判断是否负担得起
4. 将判断结果和依据写入 `conclusion.txt`

## 期望行为

Agent 需要依次调用：联网搜索工具 → 文件读取工具 → 文件写入工具，三步不能断链。

## 评分标准

- `conclusion_created`: conclusion.txt 是否存在
- `has_content`: conclusion.txt 内容是否为非空（不评估正确性/合理性）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "conclusion.txt"
    if not f.exists():
        return {
            "conclusion_created": 0.0,
            "has_content": 0.0,
        }

    content = f.read_text(encoding="utf-8", errors="ignore").strip()

    return {
        "conclusion_created": 1.0,
        "has_content": 1.0 if len(content) > 0 else 0.0,
    }
```

