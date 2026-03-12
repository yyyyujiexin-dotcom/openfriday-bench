# task_fin_01_stock_monitor

**能力**：行情数据获取（联网搜索/金融数据源）→ 异动信息输出  
**评分**：自动 pass/fail  
**超时**：120秒

## 任务说明

请查询 **Apple（AAPL）当前股价**，并将结果写入 `stock_report.txt`，要求包含：

- Ticker：AAPL
- 价格（数值）
- 日期/时间参考
- 简短市场摘要（至少 50 个字符）

## 评分标准

- `file_created`：`stock_report.txt` 是否存在  
- `ticker_present`：是否包含 AAPL  
- `price_present`：是否包含价格数值  
- `date_present`：是否包含日期  
- `summary_present`：是否包含 ≥50 字符的摘要  
- `well_formatted`：是否至少 3 行、可读性良好

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re

    report = workspace_path / "stock_report.txt"
    if not report.exists():
        return {k: 0.0 for k in [
            "file_created",
            "ticker_present",
            "price_present",
            "date_present",
            "summary_present",
            "well_formatted",
        ]}

    content = report.read_text(encoding="utf-8", errors="ignore")
    stripped = re.sub(r"\s+", " ", content).strip()

    ticker_present = 1.0 if re.search(r"\bAAPL\b", content, re.IGNORECASE) else 0.0

    price_patterns = [r"\$\s*\d+\.?\d*", r"\d+\.\d{2}", r"price.*\d+"]
    price_present = 1.0 if any(re.search(p, content, re.IGNORECASE) for p in price_patterns) else 0.0

    date_patterns = [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{1,2}/\d{1,2}/\d{2,4}",
        r"(January|February|March|April|May|June|July|August|September|October|November|December)",
        r"\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",
    ]
    date_present = 1.0 if any(re.search(p, content, re.IGNORECASE) for p in date_patterns) else 0.0

    summary_present = 1.0 if len(stripped) >= 50 else 0.0

    lines = [l for l in content.splitlines() if l.strip()]
    well_formatted = 1.0 if len(lines) >= 3 and len(stripped) >= 50 else (0.5 if len(lines) >= 2 else 0.0)

    return {
        "file_created": 1.0,
        "ticker_present": ticker_present,
        "price_present": price_present,
        "date_present": date_present,
        "summary_present": summary_present,
        "well_formatted": well_formatted,
    }
```

