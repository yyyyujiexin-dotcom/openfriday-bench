# task_fin_03_financial_extract

**能力**：表格数据分析（CSV + XLSX 多表）→ 关键指标提取  
**评分**：混合（自动 60% + LLM Judge 40%）  
**超时**：180秒

## 任务说明

工作区有两份数据文件（来自 `dataset/finance/task_fin_03_financial_extract/`）：

1. `quarterly_sales.csv`：销售交易明细  
2. `company_expenses.xlsx`：Excel 工作簿，包含 `Q1_Expenses` 与 `Budgets` 两个 sheet

请读取并分析两份文件，输出报告到 `data_summary.md`，要求至少包含：

- **CSV 分析**：总收入、总利润（收入-成本）、总销量、收入最高地区、收入最高产品  
- **Excel 分析**：Q1 总费用、费用最高部门、费用最高员工、按部门对比 Q1 实际 vs 预算  
- **综合洞察**：结合两份数据给出 2–4 条要点结论

## 评分标准（自动）

- `report_created`
- `total_revenue`：是否包含 \(119,900\) 附近数值
- `total_profit`：是否包含 \(47,960\) 附近数值
- `top_region`：是否识别 East 为最高地区（或含 33,075）
- `top_product`：是否识别 Widget B 为最高产品（或含 47,400）
- `total_expenses`：是否包含 \(15,430\) 附近数值
- `top_department`：是否识别 Engineering（或含 7,680）
- `top_employee`：是否识别 Alice Chen（或含 5,400）
- `budget_comparison`：是否包含预算对比语义（budget vs actual / variance 等）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import re

    report = workspace_path / "data_summary.md"
    if not report.exists():
        return {k: 0.0 for k in [
            "report_created",
            "total_revenue",
            "total_profit",
            "top_region",
            "top_product",
            "total_expenses",
            "top_department",
            "top_employee",
            "budget_comparison",
        ]}

    content = report.read_text(encoding="utf-8", errors="ignore")
    lower = content.lower()
    compact = content.replace(" ", "")

    def has(patterns):
        return any(re.search(p, compact) for p in patterns)

    scores = {"report_created": 1.0}
    scores["total_revenue"] = 1.0 if has([r"119[,.]?900", r"119[,.]?900\\.00"]) else 0.0
    scores["total_profit"] = 1.0 if has([r"47[,.]?960"]) else 0.0

    east_patterns = [
        r"east.*(top|highest|most|best|leading|largest)",
        r"(top|highest|most|best|leading|largest).*east",
        r"east.*\\$?33[,.]?075",
        r"33[,.]?075.*east",
    ]
    scores["top_region"] = 1.0 if any(re.search(p, lower) for p in east_patterns) else 0.0

    product_patterns = [
        r"widget\\s*b.*(top|highest|most|best|leading|largest)",
        r"(top|highest|most|best|leading|largest).*widget\\s*b",
        r"widget\\s*b.*\\$?47[,.]?400",
        r"47[,.]?400.*widget\\s*b",
    ]
    scores["top_product"] = 1.0 if any(re.search(p, lower) for p in product_patterns) else 0.0

    scores["total_expenses"] = 1.0 if has([r"15[,.]?430"]) else 0.0

    dept_patterns = [
        r"engineering.*(top|highest|most|largest|leading)",
        r"(top|highest|most|largest|leading).*engineering",
        r"engineering.*\\$?7[,.]?680",
        r"7[,.]?680.*engineering",
    ]
    scores["top_department"] = 1.0 if any(re.search(p, lower) for p in dept_patterns) else 0.0

    emp_patterns = [
        r"alice\\s*chen.*(top|highest|most|largest|leading)",
        r"(top|highest|most|largest|leading).*alice\\s*chen",
        r"alice\\s*chen.*\\$?5[,.]?400",
        r"5[,.]?400.*alice\\s*chen",
    ]
    scores["top_employee"] = 1.0 if any(re.search(p, lower) for p in emp_patterns) else 0.0

    budget_indicators = [
        r"budget.*actual",
        r"actual.*budget",
        r"variance",
        r"under\\s*budget",
        r"over\\s*budget",
        r"25[,.]?000",
    ]
    scores["budget_comparison"] = 1.0 if any(re.search(p, lower) for p in budget_indicators) else 0.0

    return scores
```

