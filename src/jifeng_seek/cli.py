"""Command line entry point for the optional prototype."""

import argparse
import json
from pathlib import Path

from . import __version__
from .engine import analyze


def _markdown(result: dict) -> str:
    state = result["current_state"]
    return "\n".join([
        "# 极峰·求真决策简报", "",
        f"**复杂度：** {result['complexity_gate']['level']} · **把握度：** {result['uncertainty']['confidence']:.0%}", "",
        "## 目标", result["objective"]["inferred"], "",
        "## 现状", f"- 事实：{'；'.join(state['facts']) or '尚未识别'}",
        f"- 判断：{'；'.join(state['judgments']) or '尚未识别'}",
        f"- 假设：{'；'.join(state['assumptions']) or '尚未识别'}",
        f"- 未知：{'；'.join(state['unknowns']) or '暂无明显缺口'}", "",
        "## 当前聚焦", result["breakthrough"]["focus"], "",
        "## 下一步", result["action"]["next_step"], "",
        "## 验证", result["validation"]["test"], "",
        "## 人工复核", "需要" if result["human_confirmation"]["required"] else "当前未触发强制复核",
    ])


def main() -> None:
    parser = argparse.ArgumentParser(prog="jifeng-seek", description="JIFENG SEEK decision-object prototype")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    onboard = sub.add_parser("onboard", help="show first-run guidance")
    analyze_cmd = sub.add_parser("analyze", help="analyze a problem statement")
    analyze_cmd.add_argument("--text", help="problem statement")
    analyze_cmd.add_argument("--input", type=Path, help="text file or JSON with problem/text field")
    analyze_cmd.add_argument("--domain", help="optional domain label")
    analyze_cmd.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    if args.command == "onboard":
        print("你好，我是极峰·求真。用一句话描述你想改变的事即可；如果方便，也告诉我已确认的事实、你的猜测、限制和成功标准。我们会先找出最值得验证的一步。\n\nHi, I’m JIFENG SEEK. Describe what you want to change. If useful, add confirmed facts, assumptions, constraints, and success criteria. We’ll identify one useful next step to test.")
        return

    text = args.text
    domain = args.domain
    if args.input:
        raw = args.input.read_text(encoding="utf-8")
        if args.input.suffix.lower() == ".json":
            payload = json.loads(raw)
            text = payload.get("problem") or payload.get("text")
            domain = domain or payload.get("domain")
        else:
            text = raw
    if not text:
        parser.error("provide --text or --input")
    result = analyze(text, domain=domain)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else _markdown(result))


if __name__ == "__main__":
    main()

