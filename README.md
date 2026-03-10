# OpenFriday Bench

> 面向真实 C 端场景的 OpenClaw Agent 能力评测框架

## 架构

本 Bench 分为两层：

- **基础能力层 Foundation**：15 个原子能力探针，全部 pass/fail
- **场景任务层 Scenarios**：26 个端到端业务任务

## 场景概览

| 层级 | 场景 | 文件夹 | 任务数 |
|---|---|---|---|
| 基础层 | 🔩 Foundation | tasks/foundation/ | 15 |
| 场景层 | 🗓️ 高级秘书 | tasks/secretary/ | 6 |
| 场景层 | 💻 AI 程序员 | tasks/programmer/ | 5 |
| 场景层 | 📢 全域运营官 | tasks/operator/ | 5 |
| 场景层 | 📈 专属金融伙伴 | tasks/finance/ | 5 |
| 场景层 | 🪞 数字分身 | tasks/digital_twin/ | 5 |

合计：**41 个任务**

## 运行方式

```bash
# 跑基础层
python scripts/benchmark.py --model minimax-portal/MiniMax-M2.5 --tasks-dir tasks/foundation

# 跑单个场景
python scripts/benchmark.py --tasks-dir tasks/secretary

# 跑全部
python scripts/benchmark.py
```