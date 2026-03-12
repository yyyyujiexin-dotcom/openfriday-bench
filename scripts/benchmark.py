#!/usr/bin/env python3
"""
OpenFriday Bench — 可执行评测脚本

支持两种执行方式：
  api      用内置 OpenAI 兼容接口调 LLM 完成任务（需 OPENAI_API_KEY）
  openclaw 用你的 OpenClaw 跑任务：复制 dataset → 调用 OpenClaw → 再评分（需配置 OPENCLAW_CMD）

环境变量：
  OPENAI_API_KEY / OPENAI_BASE_URL   API 模式必填
  OPENCLAW_CMD                       OpenClaw 模式必填，如 openclaw run 或 python -m openclaw.run
  TASK_FILE / WORKSPACE_DIR          由脚本注入，供 OpenClaw 读取
  JUDGE_MODEL / JUDGE_API_KEY        可选，LLM Judge 时用的模型与密钥（不设则用 OPENAI_*）
  OPENAI_API_KEY                     未设 JUDGE_API_KEY 时，LLM Judge 复用此密钥

用法：
  # 用 OpenClaw 跑（推荐）
  set OPENCLAW_CMD=openclaw run
  python scripts/benchmark.py --agent openclaw --tasks-dir tasks/foundation

  # LLM Judge 模型可在终端运行时再配
  set JUDGE_MODEL=gpt-4o
  python scripts/benchmark.py --agent openclaw --judge-model gpt-4o --tasks-dir tasks/foundation

  # 或用内置 API 跑
  set OPENAI_API_KEY=sk-...
  python scripts/benchmark.py --model gpt-4o --tasks-dir tasks/foundation
"""

from pathlib import Path
import argparse
import json
import re
import shutil
import os
import sys
import subprocess

# 项目根目录
ROOT = Path(__file__).resolve().parent.parent


def parse_task_md(md_path: Path) -> dict:
    """从 task_xxx.md 解析出 task_id、任务说明、超时、grade 函数。"""
    text = md_path.read_text(encoding="utf-8")

    # task_id: 第一行 # task_xxx
    m = re.search(r"^#\s+(task_\S+)", text, re.MULTILINE)
    task_id = m.group(1).strip() if m else md_path.stem

    # 超时：**超时**：60秒
    timeout = 60
    m = re.search(r"\*\*超时\*\*[：:]\s*(\d+)秒", text)
    if m:
        timeout = int(m.group(1))

    # 任务说明：从 ## 任务说明 到下一个 ## 或 ``` 前的说明
    task_desc = ""
    m = re.search(r"##\s*任务说明\s*\n(.*?)(?=\n##\s|\n```)", text, re.DOTALL)
    if m:
        task_desc = m.group(1).strip()

    # grade 函数：取 ```python ... ``` 中包含 def grade 的块
    grade_src = ""
    for block in re.finditer(r"```python\s*\n(.*?)```", text, re.DOTALL):
        if "def grade(" in block.group(1):
            grade_src = block.group(1).strip()
            break

    # 是否含 LLM Judge（用于决定是否调 judge 模型）
    score_type = "auto"
    if "LLM Judge" in text and "混合" in text:
        score_type = "mixed"
    elif "LLM Judge" in text:
        score_type = "llm_judge"

    return {
        "task_id": task_id,
        "timeout": timeout,
        "task_desc": task_desc,
        "grade_src": grade_src,
        "score_type": score_type,
    }


def get_grade_function(grade_src: str):
    """执行 grade 源码，返回可调用的 grade(workspace_path, transcript)。"""
    if not grade_src:
        return None
    ns = {}
    try:
        exec(grade_src, ns)
        return ns.get("grade")
    except Exception:
        return None


def copy_dataset_to_workspace(dataset_dir: Path, workspace_dir: Path) -> None:
    """将 dataset/{scene}/{task_id}/ 下所有文件复制到 workspace/{task_id}/。"""
    workspace_dir.mkdir(parents=True, exist_ok=True)
    if not dataset_dir.is_dir():
        return
    for f in dataset_dir.rglob("*"):
        if f.is_file():
            rel = f.relative_to(dataset_dir)
            dest = workspace_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)


def read_workspace_context(workspace_dir: Path, max_text_len: int = 80_000) -> str:
    """读取工作区内文本文件内容，供 prompt 使用；二进制只列路径。"""
    lines = []
    for f in sorted(workspace_dir.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(workspace_dir)
        try:
            raw = f.read_bytes()
            try:
                text = raw.decode("utf-8", errors="replace")
                if len(text) > max_text_len:
                    text = text[:max_text_len] + "\n...(截断)"
                lines.append(f"[文件: {rel}]\n{text}")
            except Exception:
                lines.append(f"[文件: {rel}](二进制, {len(raw)} bytes)")
        except Exception as e:
            lines.append(f"[文件: {rel}](读取失败: {e})")
    if not lines:
        return "（当前无输入文件）"
    return "\n\n".join(lines)


def build_messages(task_desc: str, workspace_context: str, task_id: str) -> list:
    """构建发给模型的 messages（OpenAI 格式）。"""
    system = (
        "你是一个在本地工作区执行任务的助手。请严格按任务说明生成要求输出的文件内容。"
        "你的回复中必须用以下格式写出每个要生成的文件，以便程序解析：\n"
        "=== FILE: 文件名 ===\n"
        "文件内容（多行）\n"
        "（再下一个文件则再写 === FILE: 另一个文件名 === ...）\n"
        "只输出需要写入的文件，不要输出任务说明或多余解释。"
    )
    user = (
        f"## 任务\n{task_desc}\n\n"
        f"## 当前工作区已有文件（供参考）\n{workspace_context}\n\n"
        "请按任务要求生成需要保存的文件内容，使用 === FILE: 文件名 === 的格式输出。"
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def default_output_filename(task_desc: str) -> str:
    """从任务说明中推断默认输出文件名。"""
    m = re.search(r"保存到\s*[`']?(\S+\.\w+)[`']?", task_desc)
    if m:
        return m.group(1).strip()
    m = re.search(r"保存为\s*[`']?(\S+\.\w+)[`']?", task_desc)
    if m:
        return m.group(1).strip()
    m = re.search(r"写入\s*[`']?(\S+\.\w+)[`']?", task_desc)
    if m:
        return m.group(1).strip()
    return "result.txt"


def write_agent_output(workspace_dir: Path, files: dict) -> None:
    """将解析出的文件名与内容写入 workspace。"""
    for name, content in files.items():
        dest = workspace_dir / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8", errors="replace")


def run_agent(task_id: str, task_desc: str, workspace_dir: Path, model: str, timeout: int) -> tuple[str, dict]:
    """调用 LLM 完成任务，返回 (raw_response, parsed_files)。"""
    workspace_context = read_workspace_context(workspace_dir)
    messages = build_messages(task_desc, workspace_context, task_id)

    try:
        import openai
        client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL"),
        )
        r = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            request_timeout=min(timeout + 10, 300),
        )
        content = (r.choices[0].message.content or "").strip()
    except ImportError:
        print("  [错误] 请安装 openai: pip install openai", file=sys.stderr)
        raise
    except Exception as e:
        return "", {"__error__": str(e)}

    # 解析 === FILE: ... === 块
    files = {}
    pattern = re.compile(r"=== FILE:\s*(\S[^\n]*)\s*===\s*\n(.*?)(?=\s*=== FILE:|\s*$)", re.DOTALL)
    for m in pattern.finditer(content):
        name = m.group(1).strip()
        if "/" in name or "\\" in name:
            name = name.replace("\\", "/").split("/")[-1]
        files[name] = m.group(2).rstrip()
    if not files and content:
        files[default_output_filename(task_desc)] = content
    return content, files


def run_openclaw_agent(task_file: Path, workspace_dir: Path, timeout: int) -> bool:
    """调用 OpenClaw 执行任务。通过环境变量传入 TASK_FILE、WORKSPACE_DIR，执行 OPENCLAW_CMD。"""
    cmd = os.environ.get("OPENCLAW_CMD", "").strip()
    if not cmd:
        raise RuntimeError("使用 --agent openclaw 时请设置环境变量 OPENCLAW_CMD（如 openclaw run 或 python -m openclaw.run）")
    env = os.environ.copy()
    env["TASK_FILE"] = str(task_file.resolve())
    env["WORKSPACE_DIR"] = str(workspace_dir.resolve())
    try:
        subprocess.run(
            cmd,
            shell=True,
            env=env,
            cwd=str(ROOT),
            timeout=timeout + 15,
        )
        return True
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        raise RuntimeError(f"OpenClaw 执行失败: {e}") from e


def run_llm_judge(task_id: str, task_desc: str, workspace_dir: Path, judge_model: str) -> float:
    """用 LLM 对工作区输出做质量打分，返回 0~1。"""
    context = read_workspace_context(workspace_dir, max_text_len=20_000)
    prompt = (
        f"## 任务\n{task_desc}\n\n"
        f"## Agent 输出（工作区文件内容）\n{context}\n\n"
        "请从「信息准确性、结构清晰度、表达质量」等维度对上述输出打分，仅回复一个 0~1 之间的小数（如 0.85），不要其他解释。"
    )
    try:
        import openai
        client = openai.OpenAI(
            api_key=os.environ.get("JUDGE_API_KEY") or os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("JUDGE_BASE_URL") or os.environ.get("OPENAI_BASE_URL"),
        )
        r = client.chat.completions.create(
            model=judge_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            request_timeout=60,
        )
        content = (r.choices[0].message.content or "").strip()
        # 解析 0~1 小数
        m = re.search(r"0?\.\d+|1\.0?", content)
        if m:
            return max(0.0, min(1.0, float(m.group())))
        return 0.5
    except Exception as e:
        print(f"  [Judge 调用失败] {e}", file=sys.stderr)
        return 0.5


def main():
    parser = argparse.ArgumentParser(description="OpenFriday Bench 评测")
    parser.add_argument("--agent", type=str, choices=["api", "openclaw"], default="openclaw",
                        help="执行任务的 agent：api=内置 OpenAI 接口，openclaw=调用你的 OpenClaw（默认 openclaw）")
    parser.add_argument("--model", type=str, default=None,
                        help="API 模式下的模型 ID；openclaw 模式下可省略（由 OpenClaw 自身配置）")
    parser.add_argument("--tasks-dir", type=str, default=None, help="任务目录，如 tasks/foundation；默认 tasks")
    parser.add_argument("--output", type=str, default="results.json", help="结果输出路径")
    parser.add_argument("--dry-run", action="store_true", help="只解析任务与复制 dataset，不调 API")
    parser.add_argument("--judge-model", type=str, default=None,
                        help="LLM Judge 使用的模型（如 gpt-4o）；也可用环境变量 JUDGE_MODEL。不配则只跑自动评分。")
    args = parser.parse_args()

    judge_model = args.judge_model or os.environ.get("JUDGE_MODEL")
    if args.agent == "api" and not args.dry_run:
        if not os.environ.get("OPENAI_API_KEY"):
            print("API 模式请设置环境变量 OPENAI_API_KEY（或使用 --dry-run）", file=sys.stderr)
            sys.exit(1)
        if not args.model:
            print("API 模式请指定 --model", file=sys.stderr)
            sys.exit(1)
    if args.agent == "openclaw" and not args.dry_run and not os.environ.get("OPENCLAW_CMD"):
        print("OpenClaw 模式请设置环境变量 OPENCLAW_CMD（如 openclaw run），或使用 --dry-run", file=sys.stderr)
        sys.exit(1)

    tasks_base = ROOT / "tasks"
    if not tasks_base.is_dir():
        print(f"任务根目录不存在: {tasks_base}", file=sys.stderr)
        sys.exit(1)

    scene_by_path = {}
    scene = "foundation"
    if args.tasks_dir:
        tasks_dir = ROOT / args.tasks_dir
        if not tasks_dir.is_dir():
            print(f"任务目录不存在: {tasks_dir}", file=sys.stderr)
            sys.exit(1)
        task_mds = sorted(tasks_dir.glob("task_*.md"))
        try:
            scene = tasks_dir.relative_to(tasks_base).parts[0] if tasks_dir != tasks_base else tasks_dir.name
        except ValueError:
            scene = tasks_dir.name
    else:
        task_mds = sorted(tasks_base.rglob("task_*.md"))
        def _scene(p):
            try:
                rel = p.parent.relative_to(tasks_base)
                return rel.parts[0] if rel.parts else p.parent.name
            except ValueError:
                return "foundation"
        scene_by_path = {str(p): _scene(p) for p in task_mds}

    if not task_mds:
        print("未找到 task_*.md", file=sys.stderr)
        sys.exit(1)

    workspace_root = ROOT / "workspace"
    results = []

    for md_path in task_mds:
        parsed = parse_task_md(md_path)
        task_id = parsed["task_id"]
        timeout = parsed["timeout"]
        task_desc = parsed["task_desc"]
        grade_src = parsed["grade_src"]
        score_type = parsed.get("score_type", "auto")
        scene = scene_by_path.get(str(md_path), scene)

        print(f"[{task_id}]", end=" ", flush=True)

        dataset_dir = ROOT / "dataset" / scene / task_id
        workspace_dir = workspace_root / task_id
        workspace_dir.mkdir(parents=True, exist_ok=True)
        copy_dataset_to_workspace(dataset_dir, workspace_dir)

        if args.dry_run:
            print("dry-run OK (dataset copied)")
            results.append({"task_id": task_id, "status": "dry_run", "scores": {}})
            continue

        grade_fn = get_grade_function(grade_src)
        if not grade_fn:
            print("  [跳过] 无法解析 grade")
            results.append({"task_id": task_id, "status": "skip", "error": "no grade"})
            continue

        try:
            if args.agent == "openclaw":
                ok = run_openclaw_agent(md_path, workspace_dir, timeout)
                if not ok:
                    print("  [超时]")
                    results.append({"task_id": task_id, "status": "timeout", "scores": {}})
                    continue
            else:
                raw, files = run_agent(task_id, task_desc, workspace_dir, args.model, timeout)
                if "__error__" in files:
                    print(f"  [API 错误] {files['__error__']}")
                    results.append({"task_id": task_id, "status": "error", "error": files["__error__"]})
                    continue
                write_agent_output(workspace_dir, files)

            scores = grade_fn(workspace_dir, {})
            if not isinstance(scores, dict):
                scores = {"grade": float(scores) if isinstance(scores, (int, float)) else 0.0}

            if score_type in ("llm_judge", "mixed") and judge_model:
                judge_score = run_llm_judge(task_id, task_desc, workspace_dir, judge_model)
                scores["llm_judge"] = judge_score
                if score_type == "mixed":
                    auto_avg = sum(scores.get(k, 0) for k in scores if k != "llm_judge") / max(1, len(scores) - 1)
                    scores["final"] = 0.5 * auto_avg + 0.5 * judge_score
                else:
                    scores["final"] = judge_score

            total = scores.get("final", sum(scores.values()) / len(scores) if scores else 0.0)
            print(f" 得分: {total:.2f} {scores}")
            results.append({"task_id": task_id, "status": "graded", "scores": scores})
        except Exception as e:
            print(f"  [异常] {e}")
            results.append({"task_id": task_id, "status": "error", "error": str(e)})

    out_path = ROOT / args.output
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n结果已写入 {out_path}")


if __name__ == "__main__":
    main()
