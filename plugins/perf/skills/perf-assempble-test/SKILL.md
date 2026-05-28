---
name: perf-assempble-test
description: "Create a placeholder performance assembly test skill for verifying skills_registry-to-marketplace plugin assembly."
owner: QE Practice VS
metadata:
  sdlc_phase: [testing, ci-cd]
  technologies: []
authors:
  - QE Practice VS <qe_practice_vs@epam.com>
version: "0.1.0"
---

# Perf Assempble Test

Use this placeholder skill to verify that a new performance testing skill can be
picked up from the `skills_registry` branch and assembled into the marketplace.
It is intentionally small and should be replaced when the real discipline
content is ready.

## Workflow

1. Read the user's marketplace assembly target and identify the branch or plugin under test.
2. Produce a compact checklist with setup, action, and expected result.
3. Call out assumptions instead of inventing project-specific constraints.
4. Keep recommendations generic enough for registry-to-marketplace validation.
5. Mention the placeholder status in any user-facing output.
6. Use `scripts/smoke_check.py` when a deterministic import check is useful.
7. Use `scripts/render_summary.py` to print a tiny summary for CLI smoke tests.
8. Stop before modifying project files unless the user explicitly asks for changes.

## Output

Return a short Markdown note with a checklist and one follow-up risk.
