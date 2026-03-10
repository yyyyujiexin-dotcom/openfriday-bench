# task_sec_02_email_triage

**评分**：混合（自动 50% + LLM Judge 50%）  
**超时**：180秒

## 任务说明

`inbox/` 目录有 5 封邮件，请生成 `triage_report.md`，标注每封邮件的优先级（🔴紧急 / 🟡重要 / ⚪稍后）和建议行动。

## 邮件概览

| 邮件 | 发件人 | 主题 | 预期优先级 |
|---|---|---|---|
| email_01.txt | CEO 王总 | 【紧急】董事会数据准备 | 🔴 紧急 |
| email_02.txt | 技术团队 | API成功率下降至85% | 🔴 紧急 |
| email_03.txt | 大客户VP | 200万合同续签 | 🟡 重要 |
| email_04.txt | HR | 团建投票 | ⚪ 稍后 |
| email_05.txt | 订阅邮件 | 科技早报 | ⚪ 可忽略 |

## 评分标准

**自动**：file_created · all_emails_covered · ceo_email_urgent · newsletter_low · has_action_items

**LLM Judge**：优先级判断合理性 · 建议行动是否具体可执行 · 报告格式是否清晰