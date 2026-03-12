# task_sec_08_office_pipeline

**能力**：办公软件应用（多格式文件处理流水线）
**评分**：混合（自动 40% + LLM Judge 60%）
**超时**：300秒
**前置条件**：无

## 任务说明

工作区有两个文件：
- `project_summary.docx`：一份没有任何格式的项目总结 Word 文档
- `budget_data.xlsx`：一份有大量空行和合并单元格的预算 Excel 表格

请完成以下步骤：

**步骤一**：整合两份文件内容，生成一份排版规范的 `project_report.pdf`，包含项目总结和预算数据表格

**步骤二**：根据 PDF 内容，制作一份 `project_slides.pptx`，要求：
- 封面页（项目名称 + 日期）
- 项目概述页（3-5个要点）
- 预算概览页（关键数字）
- 总结页

## 输入文件

- `project_summary.docx`、`budget_data.xlsx`（来自 dataset/secretary/task_sec_08_office_pipeline/）

## 评分标准

**自动**：
- `pdf_created`：project_report.pdf 是否存在
- `pptx_created`：project_slides.pptx 是否存在
- `pptx_has_slides`：PPT 是否有≥4页
- `pdf_not_empty`：PDF 文件大小 > 1KB

**LLM Judge**：PDF排版规范度 · PPT结构完整性 · 内容与原始文件的对应准确度

## 评分逻辑

```python
def grade(workspace_path, transcript):
    from pathlib import Path
    pdf = workspace_path / "project_report.pdf"
    pptx = workspace_path / "project_slides.pptx"
    pdf_exists = pdf.exists()
    pptx_exists = pptx.exists()
    pdf_not_empty = pdf_exists and pdf.stat().st_size > 1024
    pptx_slides_ok = False
    if pptx_exists:
        try:
            from pptx import Presentation
            prs = Presentation(str(pptx))
            pptx_slides_ok = len(prs.slides) >= 4
        except:
            pptx_slides_ok = pptx.stat().st_size > 10240  # fallback: 文件>10KB
    return {
        "pdf_created":    1.0 if pdf_exists else 0.0,
        "pptx_created":   1.0 if pptx_exists else 0.0,
        "pdf_not_empty":  1.0 if pdf_not_empty else 0.0,
        "pptx_has_slides":1.0 if pptx_slides_ok else 0.0,
    }
```

