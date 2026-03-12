# task_prog_06_api_workflow

**能力**：多步工作流（读配置 → 生成脚本 → 生成说明文档）  
**评分**：混合（自动 50% + LLM Judge 50%）  
**超时**：180秒

## 任务说明

工作区有一份 `config.json`（来自 dataset/programmer/task_prog_06_api_workflow/）。请你：

1. 读取并解析 `config.json`
2. 提取其中的 API endpoint
3. 生成一个 Python 脚本（任意文件名，后缀为 `.py`），要求：
   - 读取 `config.json`
   - 发起 HTTP 请求（GET 即可）
   - 有基本错误处理
   - 将结果打印到标准输出
4. 生成 `NOTES.md`，说明：
   - 你做了什么
   - 脚本如何工作
   - 如何运行脚本
   - 配置文件里哪些字段是关键的

## 评分标准

**自动**：

- `read_config`：transcript 中是否出现读取 `config.json` 的行为（弱检查）
- `script_created`：工作区是否存在任意 `.py` 脚本
- `valid_syntax`：脚本是否为合法 Python 语法
- `parses_json`：脚本是否包含 JSON 解析（`json.load/loads` 等）
- `has_http_request`：脚本是否包含 HTTP 请求代码（`requests/urllib` 等）
- `notes_created`：`NOTES.md` 是否存在

**LLM Judge**：脚本完整性与健壮性 · NOTES 是否清晰可用 · 工作流衔接是否自然

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import ast
    import re

    t = transcript or ""
    read_config = "config.json" in t

    py_files = list(workspace_path.glob("*.py"))
    notes = workspace_path / "NOTES.md"

    if not py_files:
        return {
            "read_config": 1.0 if read_config else 0.0,
            "script_created": 0.0,
            "valid_syntax": 0.0,
            "parses_json": 0.0,
            "has_http_request": 0.0,
            "notes_created": 1.0 if notes.exists() else 0.0,
        }

    content = py_files[0].read_text(encoding="utf-8", errors="ignore")

    scores = {
        "read_config": 1.0 if read_config else 0.0,
        "script_created": 1.0,
        "valid_syntax": 0.0,
        "parses_json": 0.0,
        "has_http_request": 0.0,
        "notes_created": 1.0 if notes.exists() else 0.0,
    }

    try:
        ast.parse(content)
        scores["valid_syntax"] = 1.0
    except SyntaxError:
        return scores

    json_patterns = [r"import\\s+json", r"json\\.load", r"json\\.loads"]
    scores["parses_json"] = 1.0 if any(re.search(p, content) for p in json_patterns) else 0.0

    http_patterns = [
        r"import\\s+requests",
        r"requests\\.(get|post)",
        r"import\\s+urllib",
        r"urllib\\.request",
        r"urlopen",
    ]
    scores["has_http_request"] = 1.0 if any(re.search(p, content, re.IGNORECASE) for p in http_patterns) else 0.0

    return scores
```

