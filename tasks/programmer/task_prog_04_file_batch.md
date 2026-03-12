# task_prog_04_file_batch

**能力**：文件结构创建与批量文件落盘（Python 项目骨架）  
**评分**：自动 pass/fail  
**超时**：120秒

## 任务说明

请在工作区创建一个名为 `datautils` 的 Python 库项目骨架（不需要发布到 PyPI），要求包含：

1. `src/datautils/` 包目录，以及 `src/datautils/__init__.py`
2. `tests/` 目录，以及 `tests/test_datautils.py`（占位测试即可）
3. `pyproject.toml`：包含项目元数据（至少包含 name=`datautils`、version=`0.1.0`、description）
4. `README.md`：包含标题与一句简介

## 评分标准

- `src_directory_created`：是否创建 `src/datautils/`  
- `tests_directory_created`：是否创建 `tests/`  
- `init_file_created`：是否创建 `src/datautils/__init__.py`  
- `test_file_created`：是否创建 `tests/test_datautils.py`  
- `pyproject_created`：是否创建 `pyproject.toml`  
- `readme_created`：是否创建 `README.md`  
- `pyproject_has_metadata`：`pyproject.toml` 是否包含 datautils 与版本信息

## 评分逻辑

```python
def grade(workspace_path, transcript):
    src_datautils = workspace_path / "src" / "datautils"
    tests_dir = workspace_path / "tests"

    init_file = src_datautils / "__init__.py"
    test_file = tests_dir / "test_datautils.py"
    pyproject = workspace_path / "pyproject.toml"
    readme = workspace_path / "README.md"

    scores = {
        "src_directory_created": 1.0 if src_datautils.exists() else 0.0,
        "tests_directory_created": 1.0 if tests_dir.exists() else 0.0,
        "init_file_created": 1.0 if init_file.exists() else 0.0,
        "test_file_created": 1.0 if test_file.exists() else 0.0,
        "pyproject_created": 1.0 if pyproject.exists() else 0.0,
        "readme_created": 1.0 if readme.exists() else 0.0,
        "pyproject_has_metadata": 0.0,
    }

    if pyproject.exists():
        content = pyproject.read_text(encoding="utf-8", errors="ignore").lower()
        has_name = "datautils" in content
        has_version = "0.1.0" in content or "version" in content
        scores["pyproject_has_metadata"] = 1.0 if (has_name and has_version) else (0.5 if has_name else 0.0)

    return scores
```

