# common-agent-evaluator

Score AI agent specifications against the **Agent Maturity Model** (L0–L3, 39 practices across 9 categories) and emit a styled, self-contained HTML report.

---

## Install

Install the skill via `npx skills add`:

```bash
npx skills add git@git.epam.com:epmt-rtqa/qe-agent-skills.git --skill common-agent-evaluator
```

By default this installs into the current project's `.claude/skills/`. Pass `--global` (or run from your home directory) to install user-scoped at `~/.claude/skills/` so it is available in every project.

After installing, restart Claude Code so the skill is picked up.

---

## What This Skill Changes

| Without skill | With skill |
|---|---|
| Score agents by gut feel ("looks L2-ish") | Consistent L0/L1/L2/L3 verdict anchored to 39 named practices |
| Miss platform-side capabilities (token tracking, telemetry) | Clarifying-question phase separates agent-spec gaps from platform gaps |
| Vague strength/gap bullets | Every claim traces back to a specific line in the agent spec |
| No cross-agent comparison | Suite-level rollup with anchor-agent rule — not a misleading average |
| Freeform notes, no stakeholder deliverable | Self-contained HTML report in the house template, written to the repo root |
| Inconsistent recommendations | Ordered "to reach L2 / to reach L3" lists, each naming the agent, practice, and observable done state |

---

## When It Triggers

Say any of the following (exact phrasing not required):

- *"evaluate this agent"*
- *"score these agents"*
- *"how mature is this prompt / pipeline?"*
- *"audit the agent suite in folder X"*
- *"rate this against best practices"*
- *"is this L1 or L2?"*
- *"generate a maturity report for my ELITEA pipeline"*
- *"assess the agents in `<client>/agents/`"*

Also triggers when the user points at a folder of `*_agent.md` / `*.yml` files and asks for an assessment, even without using the word "maturity".

---

## Structure

```
common-agent-evaluator/
├── SKILL.md                              # workflow, phases, writing guidelines
├── README.md
└── references/
    ├── maturity_model_requirements.md    # 39 practices, 9 categories, level tags and rationales
    ├── scoring_rubric.md                 # how to translate spec content into a level; suite rollup rules
    ├── clarifying_questions.md           # what to ask the user; platform-side vs agent-side distinction
    ├── report_template.md                # section-by-section skeleton with placeholders
    └── example_report.html               # worked HTML example (anonymised); reuse <style> block verbatim
```

---

## How It Works

The skill runs seven phases in order:

| Phase | What happens |
|---|---|
| 1 — Locate inputs | Detects path mode (folder / file list), pasted mode, or mixed; confirms scope with the user |
| 2 — Load rubric | Reads `maturity_model_requirements.md` and `scoring_rubric.md` in full on every invocation |
| 3 — Clarifying questions | Confirms suite name, author, token economics, eval framework, observability, safety/compliance, anchor agents, and any N/A categories — before any scoring |
| 4 — Score each agent | Works through the 39 practices per agent; tags strengths with evidence; tags gaps by absence, not inference |
| 5 — Suite rollup | Applies anchor-agent rule (not average); states rollup logic explicitly |
| 6 — Generate HTML report | Writes `<suite_slug>_maturity_assessment.html` to the repo root using the house template and CSS from `example_report.html` |
| 7 — Hand off | States suite verdict in one sentence; calls out N/A categories and top 1–3 leverage recommendations |

Phase 3 (clarifying questions) is non-negotiable — it is what separates a defensible report from a wrong one.

---

## The Maturity Model

Four cumulative levels — each includes all practices from the levels below it:

| Level | Label | Practices | Typical use |
|---|---|---|---|
| 🔴 L0 | Beginner | 5 | Internal chatbots, prototypes |
| 🟡 L1 | Foundational | 19 | Customer support, workflow automation |
| 🟢 L2 | Advanced | 35 | Enterprise assistants, multi-step orchestration |
| 🟣 L3 | Autonomous | 39 | Self-improving networks, regulated industries |

The model was authored by Ihar Bylitski (Feb 2026). Full requirements live in `references/maturity_model_requirements.md`.

---

## Report Structure

Every generated HTML report contains the same sections in the same order:

1. **Header** — title, subject path, framework reference, assessment date, author.
2. **Executive Summary** — one-paragraph verdict + 4-card metric grid + scoring caveat.
3. **Per-Agent Scorecard** — one row per agent; level badge; 3–6 strength bullets; 1–4 gap bullets.
4. **Coverage Against the 39-Practice Checklist** — 9 category rows; `High` / `Medium` / `Low` / `N/A` badge; evidence note.
5. **Recommendations** — two ordered lists: "To reach L2" and "To reach L3". Ordered by leverage, not category.
6. **Housekeeping** callout — only if files were changed during assessment.
7. **Footer** — generation date, source path, framework reference.

---

## Notes

- **Inferring vs reading** — if the agent spec doesn't mention a capability, the capability is absent. No inference, no benefit of the doubt.
- **Platform vs agent gaps** — token cost tracking, telemetry, eval harnesses, and audit logs usually live on the platform (ELITEA, LangSmith, in-house), not in the prompt. Phase 3 confirms this before scoring, so real strengths are never mis-marked as gaps.
- **Suite level is not an average** — three L2 anchors and three L1 supporters = "between L1 and L2, anchored at L2 by X and Y", not "L1.5".
- **`L1+` is honest** — if an agent meets most L2 criteria but misses one or two, `L1+` is the correct label. Over-claiming L2 makes the recommendations land wrong.
- **Output path** — the HTML report is written to the **repo root** as `<suite_slug>_maturity_assessment.html`. Tell the user the absolute path after writing.

---

## Author

[Dzmitry Shaplyka](https://git.epam.com/dzmitry_shaplyka) — EPAM QE Practice
