# task_f_08_structured_output

**分组**：生成输出类  
**评分**：自动 pass/fail  
**超时**：60秒

## 任务说明

请将以下非结构化信息转换为 JSON 格式，保存到 `output.json`：

> 用户张三，男，28岁，职业是产品经理，所在城市北京，注册时间2025年6月15日，会员等级黄金。

JSON 必须包含以下字段：name, gender, age, occupation, city, register_date, membership

## 评分标准

- `file_created`: output.json 是否存在
- `valid_json`: 是否为合法 JSON
- `has_all_fields`: 是否包含全部 7 个字段
- `age_correct`: age 字段值是否为数字 28

## 评分逻辑

```python
def grade(workspace_path, transcript):
    import json
    f = workspace_path / "output.json"
    if not f.exists(): return {"file_created":0.0,"valid_json":0.0,"has_all_fields":0.0,"age_correct":0.0}
    try:
        data = json.loads(f.read_text(encoding="utf-8",errors="ignore"))
        required = ["name","gender","age","occupation","city","register_date","membership"]
        has_all = all(k in data for k in required)
        age_ok = str(data.get("age","")) == "28" or data.get("age") == 28
        return {"file_created":1.0,"valid_json":1.0,"has_all_fields":1.0 if has_all else 0.0,"age_correct":1.0 if age_ok else 0.0}
    except:
        return {"file_created":1.0,"valid_json":0.0,"has_all_fields":0.0,"age_correct":0.0}
```