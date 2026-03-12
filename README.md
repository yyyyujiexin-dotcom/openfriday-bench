# OpenFriday Bench

> 面向真实 C 端场景的 OpenClaw Agent 能力评测框架

## 架构

本 Bench 分为两层：

- **基础能力层 Foundation**：15 个原子能力探针，全部 pass/fail
- **场景任务层 Scenarios**：25 个端到端业务任务

## 评分原则

**Foundation 层**：测「格式/结构层面的正确」，不测「内容/答案层面的准确」。只要 Agent 调用了正确的工具、产出了正确的格式，就给分。

**场景层**：测端到端业务完成质量，内容准确性才纳入评分。

## 场景概览

| 层级   | 场景         | 文件夹              | 任务数 |
|--------|--------------|---------------------|--------|
| 基础层 | 🔩 Foundation | tasks/foundation/   | 15     |
| 场景层 | 🗓️ 高级秘书   | tasks/secretary/    | 11     |
| 场景层 | 💻 AI 程序员  | tasks/programmer/   | 4      |
| 场景层 | 📢 全域运营官 | tasks/operator/     | 3      |
| 场景层 | 📈 专属金融伙伴 | tasks/finance/    | 4      |
| 场景层 | 🪞 数字分身   | tasks/digital_twin/ | 3      |

合计：**40 个任务**

## 目录结构

```
openfriday-bench/
├── tasks/                         # 任务定义文件
│   ├── foundation/
│   │   └── task_f_01_web_search.md
│   ├── secretary/
│   ├── programmer/
│   ├── operator/
│   ├── finance/
│   └── digital_twin/
├── dataset/                       # 输入数据（只读，勿修改）
│   ├── foundation/
│   │   └── task_f_01_web_search/
│   │       └── mock_search_response.json
│   ├── secretary/
│   └── ...
├── workspace/                     # 运行时自动创建，勿手动修改，已加入 .gitignore
│   └── task_f_01_web_search/      # benchmark 初始化，Agent 在此读写文件
│       ├── mock_search_response.json   # 从 dataset 复制的输入
│       └── result.txt                  # Agent 写入的输出
├── scripts/
│   └── benchmark.py
└── README.md
```

## 命名约定

任务 ID 是整个系统的唯一标识，三处必须严格一致：

| 位置           | 格式                        | 示例                                      |
|----------------|-----------------------------|-------------------------------------------|
| 任务定义文件   | tasks/{场景}/{task_id}.md   | tasks/foundation/task_f_01_web_search.md  |
| 数据集文件夹   | dataset/{场景}/{task_id}/   | dataset/foundation/task_f_01_web_search/  |
| 运行时 workspace | workspace/{task_id}/     | workspace/task_f_01_web_search/            |

**不允许例外**。task_id 去掉 .md 后缀即为 dataset 文件夹名。

## 运行时数据流

```
dataset/{场景}/{task_id}/          只读，原始输入数据
        ↓  benchmark 启动时复制
workspace/{task_id}/               运行时沙盒，Agent 的工作台
        ↓  Agent 读输入、写输出
评分脚本检查 workspace/ 里的输出文件
        ↓
results.json
```

workspace 是 Agent 的「沙盒工作台」：每次跑任务前由 benchmark 自动创建并初始化，任务结束后可清理。dataset 是「只读档案室」，永远不会被污染。

## 前置条件说明

部分任务依赖真实渠道或账号，运行前需满足对应前置条件。未满足前置条件的任务会被自动跳过（标注 `skipped: prerequisites_not_met`），不计入总分，但会在报告中提示。

| 前置条件类型     | 示例任务                   | 说明                     |
|------------------|----------------------------|--------------------------|
| 无（开箱即跑）   | Foundation 全部、秘书 sec_01~03 | 使用本地 mock 数据       |
| 飞书渠道         | 秘书 sec_06 跨平台消息聚合 | 需在 OpenClaw 绑定飞书   |
| Google Calendar  | 秘书 sec_04 日历冲突检测   | 需授权 Google Calendar   |
| Browser + 账号    | 运营内容发布类任务         | 需启用 browser 并登录对应平台 |

## 运行方式

依赖：`pip install -r requirements.txt`（主要为 `openai`，OpenClaw 模式仅评分/LLM Judge 时用到）。

### 用 OpenClaw 跑

脚本默认 `--agent openclaw`：只负责复制 dataset → 调用你的 OpenClaw → 再按任务里定义的规则评分。执行任务的模型与工具由 OpenClaw 自己配置。

1. 设置 **OPENCLAW_CMD**：你的 OpenClaw 启动命令（脚本会注入 `TASK_FILE`、`WORKSPACE_DIR` 环境变量，供其读取任务文件与工作区路径）。
2. 在终端运行时可配 **LLM Judge 模型**：部分任务为「LLM Judge」或「混合（自动 + LLM Judge）」；若不配置 judge 模型，只跑自动评分；若配置，会用该模型对输出做质量打分并合并进结果。

```bash
# 必填：OpenClaw 如何被调用（示例，按你本地命令改）
set OPENCLAW_CMD=openclaw run
# 或：set OPENCLAW_CMD=python -m openclaw.run

# 跑基础层
python scripts/benchmark.py --tasks-dir tasks/foundation

# 跑基础层并启用 LLM Judge（终端运行时再配即可）
set JUDGE_MODEL=gpt-4o
set OPENAI_API_KEY=sk-...
python scripts/benchmark.py --tasks-dir tasks/foundation --judge-model gpt-4o

# 跑全部任务
python scripts/benchmark.py
```

LLM Judge 相关环境变量（可选，终端运行时配置即可）：

| 变量 | 说明 |
|------|------|
| `JUDGE_MODEL` | Judge 用的模型 ID（也可用 `--judge-model`） |
| `JUDGE_API_KEY` / `JUDGE_BASE_URL` | 不设则复用 `OPENAI_API_KEY` / `OPENAI_BASE_URL` |
