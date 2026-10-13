"""Heuristic baseline for a structured JIFENG SEEK Decision Object.

This prototype organizes supplied text; it does not verify claims or replace
domain expertise. The Codex Skill instructions remain the primary interface.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from uuid import uuid4

HIGH_RISK = (
    "medical", "health", "法律", "legal", "金融", "投资", "financial",
    "insurance", "保险", "合规", "compliance", "个人信息", "身份证",
    "病历", "保单", "diagnosis", "treatment",
)
UNCERTAINTY = ("可能", "也许", "猜", "假设", "不确定", "probably", "maybe", "assume", "uncertain")
GOAL_MARKERS = ("想", "希望", "目标", "需要", "为了", "希望达成", "want to", "goal is", "need to")
FACT_MARKERS = ("数据", "记录", "报告", "已完成", "已经", "签署", "客户说", "显示", "结果是", "confirmed", "measured")
JUDGMENT_MARKERS = ("重要", "糟糕", "很好", "应该", "必须", "值得", "风险很大", "important", "should", "best")
RESOURCE_MARKERS = ("预算", "团队", "时间", "资源", "渠道", "客户", "budget", "team", "time", "resource")
CONSTRAINT_MARKERS = ("不能", "限制", "期限", "不允许", "缺少", "不足", "无法", "constraint", "deadline", "cannot")


def _contains(text: str, markers: tuple[str, ...]) -> bool:
    lower = text.casefold()
    return any(marker.casefold() in lower for marker in markers)


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"[。！？!?;；\n\r]+", text) if part.strip()]


def analyze(text: str, *, domain: str | None = None) -> dict:
    """Turn a problem statement into a conservative, reviewable decision object."""
    clean = text.strip()
    if not clean:
        raise ValueError("Problem text must not be empty.")

    parts = _sentences(clean)
    assumptions = [s for s in parts if _contains(s, UNCERTAINTY)]
    judgments = [s for s in parts if _contains(s, JUDGMENT_MARKERS)]
    facts = [s for s in parts if _contains(s, FACT_MARKERS) or re.search(r"\d", s)]
    classified = set(assumptions + judgments + facts)
    unknowns = ["关键背景、时间范围或成功标准尚未明确。"] if len(classified) < len(parts) else []

    goal = next((s for s in parts if _contains(s, GOAL_MARKERS)), None)
    score = min(10, max(0, (len(clean) // 180) + (2 if len(parts) > 3 else 0)
                        + (2 if _contains(clean, UNCERTAINTY) else 0)
                        + (2 if _contains(clean, CONSTRAINT_MARKERS) else 0)
                        + (2 if _contains(clean, HIGH_RISK) or (domain and _contains(domain, HIGH_RISK)) else 0)))
    level = "complex" if score >= 6 else "moderate" if score >= 3 else "simple"
    risk = _contains(clean, HIGH_RISK) or bool(domain and _contains(domain, HIGH_RISK))
    confidence = 0.72 if goal and facts else 0.55 if goal or facts else 0.4
    confidence = min(confidence, 0.45) if risk else confidence

    goal_text = goal or "先补齐目标与成功标准，再决定行动。"
    focus = "先验证最影响目标、同时最不确定的关键假设。" if assumptions or unknowns else "先确认目标与当前最大约束是否一致。"
    first_action = "补充目标、期限、已验证事实和成功标准；若已有这些信息，选一个可在短周期内验证的关键假设。"
    if level == "simple":
        first_action = "确认这项建议是否符合你的具体情境，然后执行最小的一步。"

    return {
        "meta": {"decision_id": f"seek-{uuid4().hex[:12]}", "version": "0.2.0",
                 "created_at": datetime.now(timezone.utc).isoformat(), "language": "zh-CN"},
        "input": {"problem": clean, "domain": domain},
        "complexity_gate": {"level": level, "score": score,
                            "reasons": ["信息不确定" if assumptions else "存在多个问题线索" if len(parts) > 3 else "影响范围或约束需要确认"]},
        "objective": {"stated": goal, "inferred": goal_text, "success_criteria": []},
        "current_state": {"facts": facts, "judgments": judgments, "assumptions": assumptions, "unknowns": unknowns},
        "problem": {"reframed": f"如何在现有信息与限制下推进：{goal_text}",
                    "core_contradiction": "期望结果与当前证据、资源或约束之间的差距仍需验证。",
                    "non_goals": []},
        "resources": {"available": [s for s in parts if _contains(s, RESOURCE_MARKERS)],
                      "constraints": [s for s in parts if _contains(s, CONSTRAINT_MARKERS)]},
        "breakthrough": {"focus": focus, "why_now": "先降低最关键的不确定性，避免过早投入不可逆资源。", "alternatives": []},
        "action": {"next_step": first_action,
                   "checklist": ["写下当前最关键的假设", "确定可观察的验证信号", "设置复盘时间"]},
        "validation": {"test": "用一个低成本、可逆的小实验检验关键假设。", "signals": [],
                       "review_after": "完成首次验证后复盘"},
        "uncertainty": {"confidence": confidence, "unknowns": unknowns,
                        "risks": ["此原型只整理用户提供的信息，不独立核验事实。"] + (["需要具备相应资质的专业人士复核。"] if risk else [])},
        "human_confirmation": {"required": risk, "reason": "高影响或敏感领域需要人工复核。" if risk else None,
                               "questions": ["请由合格专业人士复核关键事实和建议。"] if risk else []},
        "workflow": {"suggested_route": "seek_review" if risk or level == "complex" else "answer",
                     "future_hooks": {"router": None, "agent_registry": None}},
    }

