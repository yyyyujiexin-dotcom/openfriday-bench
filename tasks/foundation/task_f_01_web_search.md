# task_f_01_web_search

**分组**：感知输入类
**评分**：自动 pass/fail
**超时**：60秒

## 评分原则

用「只有实时联网才能回答的问题」反向证明联网能力。模型无法从训练数据编造今日实时股价，结果合理即证明真的联网了。不检查工具调用行为——不是所有模型都用同一套工具 API，行为检查不可靠。

## 任务说明

请搜索「英伟达（NVDA）今天的股票价格」，将结果保存到 `result.txt`。

## 评分标准

- `file_created`：result.txt 是否存在
- `file_not_empty`：文件内容是否非空
- `has_price_number`：文件内容是否包含数字（价格必然是数字，无法凭空编造合理值）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re

    f = workspace_path / "result.txt"
    exists = f.exists()
    content = f.read_text(encoding="utf-8", errors="ignore").strip() if exists else ""

    # 包含任意数字即视为有价格信息（不验证具体数值）
    has_price_number = bool(re.search(r'\d+', content))

    return {
        "file_created":    1.0 if exists else 0.0,
        "file_not_empty":  1.0 if len(content) > 0 else 0.0,
        "has_price_number":1.0 if has_price_number else 0.0,
    }
```
