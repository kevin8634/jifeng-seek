# 极峰·求真 | JIFENG SEEK

**面向复杂问题的通用 AI 决策 Skill / A general-purpose AI decision skill for complex problems.**

[中文](#中文) · [English](#english)

## 中文

极峰·求真帮助你先看清问题，再选择行动。它会梳理目标、已知事实、判断与假设，识别关键矛盾和信息缺口，给出一个可执行的下一步，并设计验证方式。它是一套通用决策方法，不是特定思想或行业知识库。

### 安装

**Codex：**将本仓库克隆或下载后，把 `jifeng-seek` 文件夹复制到个人 Skills 目录：

```text
%USERPROFILE%\.codex\skills\jifeng-seek\SKILL.md
```

macOS / Linux 对应路径：`~/.codex/skills/jifeng-seek/SKILL.md`。如果你的 Codex 使用自定义 `CODEX_HOME`，请将目录放在 `$CODEX_HOME/skills/jifeng-seek/`。重启或新开 Codex 会话后即可使用。

也可以只将 `SKILL.md` 与整个 `references/` 目录安装到该位置；保留完整仓库可获得示例、Schema 和评测素材。

### 使用

在 Codex 对话中直接提及“求真”或描述一个需要判断的问题，例如：

> 用极峰求真帮我判断：团队增长停滞，接下来两周应该优先验证什么？

Skill 会先判断问题复杂度。简单问题直接回答；复杂或信息不足时，会先说明关键缺口并提出少量澄清问题，随后形成结构化决策结果。涉及医疗、法律、金融、保险建议、合规、个人敏感数据或对外操作时，会明确不确定性并要求人工复核。

### 初次使用引导

安装后可以先输入：

> 我刚安装了极峰求真。请用简短方式介绍它，并引导我用一个真实问题开始。先问我：我希望改变什么、目前知道哪些事实、有哪些限制、什么结果算成功？

你也可以直接用这个模板：

```text
我想解决：
希望达成：
已确认的事实：
我的判断或猜测：
限制与可用资源：
成功标准：
```

### 项目范围

v0.2 是一个单 Agent、模块化 Skill。它不会自动执行高影响或对外操作，不会假装确定，也不会将任何政治思想做成知识库；方法层抽象为事实核查、调查、矛盾分析、资源聚焦和实践验证。

## English

JIFENG SEEK helps you understand a problem before choosing an action. It clarifies the objective, separates facts from judgments and assumptions, identifies key tensions and missing information, proposes a practical next step, and defines how to test it. It is a general decision method, not a domain knowledge base.

### Installation

Clone or download this repository and copy the `jifeng-seek` folder into your personal Codex Skills directory:

```text
Windows:  %USERPROFILE%\.codex\skills\jifeng-seek\SKILL.md
macOS/Linux: ~/.codex/skills/jifeng-seek/SKILL.md
```

If you use a custom `CODEX_HOME`, install it under `$CODEX_HOME/skills/jifeng-seek/`. Start a new Codex session after installation. Keep the `references/` directory next to `SKILL.md` so the skill can load its detailed guidance.

### Usage

Ask Codex naturally, for example:

> Use JIFENG SEEK to help me decide what our team should validate first during the next two weeks.

The skill answers simple questions directly. For complex or underspecified problems, it identifies information gaps and asks a small number of clarifying questions before producing a structured decision. For medical, legal, financial, insurance, compliance, sensitive-data, or external-action cases, it surfaces uncertainty and requires human review.

### First-run guidance

After installation, try:

> I just installed JIFENG SEEK. Briefly explain how to use it and guide me through a real problem. Ask what I want to change, which facts I know, what constraints I have, and what success would look like.

Or provide this context:

```text
Problem:
Desired outcome:
Confirmed facts:
My judgments or assumptions:
Constraints and available resources:
Success criteria:
```

## Repository layout

- `SKILL.md` — Codex entry point and operating rules
- `references/` — decision method, behavior, safety, and workflow details
- `schemas/` — machine-readable Decision Object contract
- `examples/` and `templates/` — sample input and output format
- `src/` — optional local Python prototype for producing a baseline Decision Object
- `tests/` — prototype checks

## License

MIT. See [LICENSE](LICENSE).

