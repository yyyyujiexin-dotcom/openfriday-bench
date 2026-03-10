# task_f_14_tool_chain

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
- `mentions_price`: 是否提到价格数字
- `mentions_budget`: 是否提到预算或「30万」
- `has_conclusion`: 是否有明确结论（能/不能/够/不够）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "conclusion.txt"
    if not f.exists(): return {k:0.0 for k in ["conclusion_created","mentions_price","mentions_budget","has_conclusion"]}
    c = f.read_text(encoding="utf-8",errors="ignore")
    import re
    return {
        "conclusion_created": 1.0,
        "mentions_price": 1.0 if re.search(r'\d+万|\d+,\d+',c) else 0.0,
        "mentions_budget": 1.0 if any(w in c for w in ["30万","预算","budget"]) else 0.0,
        "has_conclusion": 1.0 if any(w in c for w in ["能","不能","够","不够","可以","负担","afford"]) else 0.0,
    }
```