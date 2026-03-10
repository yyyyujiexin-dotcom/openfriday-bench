# task_sec_03_doc_generation

**评分**：混合（自动 40% + LLM Judge 60%）  
**超时**：150秒

## 任务说明

工作区有零散会议记录 `meeting_notes_raw.txt`，请生成规范会议纪要 `meeting_minutes.md`：

- 标题 + 日期 + 参会人
- 会议摘要（2-3句，提炼不照抄）
- 主要讨论事项
- 待办事项表格（负责人 | 事项 | 截止日期）

## 原始数据摘要

会议：产品周会 · 参会：张伟、李娜、王芳、陈强

待办：李娜(3/13) · 陈强(3/15) · 王芳(3/12) · 张伟(待定)

## 评分标准

**自动**：file_created · has_title · has_attendees · has_action_table · all_todos_present · has_summary

**LLM Judge**：摘要提炼质量 · 语言专业度 · 表格格式正确性