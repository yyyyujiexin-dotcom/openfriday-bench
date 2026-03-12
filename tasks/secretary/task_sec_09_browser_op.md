# task_sec_09_browser_op

**能力**：浏览器操作
**评分**：自动
**超时**：120秒
**前置条件**：✅ OpenClaw browser 已启用 + 飞书 web 已登录（https://www.feishu.cn）

## 任务说明

请通过浏览器，将我的飞书状态修改为「休息中」，并将操作结果（截图路径或操作确认）保存到 `browser_result.txt`。

## 期望操作路径

1. 打开飞书 web（https://www.feishu.cn）
2. 进入个人状态设置
3. 选择「休息中」状态
4. 确认修改成功

## 评分标准

- `file_created`：browser_result.txt 是否存在
- `file_not_empty`：内容非空
- `mentions_success`：结果中包含操作成功相关词（「休息中」「已设置」「success」「成功」）
- `screenshot_saved`：workspace 中是否存在截图文件（.png / .jpg）

## 评分逻辑

```python
def grade(workspace_path, transcript):
    f = workspace_path / "browser_result.txt"
    if not f.exists():
        return {k: 0.0 for k in ["file_created","file_not_empty","mentions_success","screenshot_saved"]}
    content = f.read_text(encoding="utf-8").strip()
    mentions_success = any(w in content for w in ["休息中","已设置","success","成功","设置成功"])
    screenshots = list(workspace_path.glob("*.png")) + list(workspace_path.glob("*.jpg"))
    return {
        "file_created":    1.0,
        "file_not_empty":  1.0 if len(content) > 0 else 0.0,
        "mentions_success":1.0 if mentions_success else 0.0,
        "screenshot_saved":1.0 if len(screenshots) > 0 else 0.0,
    }
```

