# task_prog_07_config_replace

**能力**：跨文件定向替换（JSON + YAML）与变更说明  
**评分**：自动 pass/fail  
**超时**：120秒

## 任务说明

工作区的 `config/` 目录下有两份配置文件：

- `config/settings.json`
- `config/database.yml`

请将它们更新为生产环境配置，要求对 `config/` 目录内**所有文件**做如下替换：

1. 将所有 `localhost` 替换为 `prod-db.example.com`
2. 将数据库名 `myapp_dev` 与 `myapp_test` 均替换为 `myapp_prod`
3. 将 `settings.json` 里的日志级别 `debug` 替换为 `warn`
4. 将 API endpoint `http://localhost:3000` 替换为 `https://api.example.com`

最后请在 `changes.md` 中逐文件列出你做了哪些变更。

## 评分标准

- `settings_host_updated`：`settings.json` 是否完成 host 替换  
- `settings_db_updated`：`settings.json` 是否完成 db 名替换  
- `settings_loglevel_updated`：`settings.json` 是否完成 log level 替换  
- `settings_api_updated`：`settings.json` 是否完成 API endpoint 替换  
- `yaml_host_updated`：`database.yml` 是否完成 host 替换  
- `yaml_db_updated`：`database.yml` 是否完成 db 名替换  
- `changes_created`：`changes.md` 是否存在且非空

## 评分逻辑

```python
def grade(workspace_path, transcript):
    settings_file = workspace_path / "config" / "settings.json"
    db_file = workspace_path / "config" / "database.yml"
    changes = workspace_path / "changes.md"

    scores = {
        "settings_host_updated": 0.0,
        "settings_db_updated": 0.0,
        "settings_loglevel_updated": 0.0,
        "settings_api_updated": 0.0,
        "yaml_host_updated": 0.0,
        "yaml_db_updated": 0.0,
        "changes_created": 0.0,
    }

    if settings_file.exists():
        content = settings_file.read_text(encoding="utf-8", errors="ignore")
        scores["settings_host_updated"] = 1.0 if ("prod-db.example.com" in content and "localhost" not in content.replace("api.example.com", "")) else 0.0
        scores["settings_db_updated"] = 1.0 if ("myapp_prod" in content and "myapp_dev" not in content) else 0.0
        scores["settings_loglevel_updated"] = 1.0 if ('"warn"' in content.lower() and '"debug"' not in content.lower()) else 0.0
        scores["settings_api_updated"] = 1.0 if ("https://api.example.com" in content) else 0.0

    if db_file.exists():
        content = db_file.read_text(encoding="utf-8", errors="ignore")
        scores["yaml_host_updated"] = 1.0 if ("prod-db.example.com" in content and "localhost" not in content) else 0.0
        scores["yaml_db_updated"] = 1.0 if ("myapp_prod" in content and "myapp_dev" not in content and "myapp_test" not in content) else 0.0

    if changes.exists():
        c = changes.read_text(encoding="utf-8", errors="ignore").strip()
        scores["changes_created"] = 1.0 if len(c) > 20 else 0.0

    return scores
```

