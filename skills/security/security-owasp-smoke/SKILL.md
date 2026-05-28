---
name: security-owasp-smoke
description: "Create compact OWASP-style security smoke checklists for marketplace import validation and security plugin testing."
owner: QE Practice VS
metadata:
  sdlc_phase: [code-review, testing]
  technologies: [owasp]
authors:
  - QE Practice VS <qe_practice_vs@epam.com>
version: "0.1.0"
---

# Security OWASP Smoke

Use this placeholder skill to verify that the security testing marketplace plugin imports correctly.
It is intentionally small and should be replaced when the real discipline content is ready.

## Workflow

1. Read the user's smoke-test target and identify the artifact or feature under test.
2. Produce a compact checklist with setup, action, and expected result.
3. Call out assumptions instead of inventing project-specific constraints.
4. Keep recommendations generic enough for marketplace import validation.
5. Mention the placeholder status in any user-facing output.
6. Use `scripts/smoke_check.py` when a deterministic import check is useful.
7. Use `scripts/render_summary.py` to print a tiny summary for CLI smoke tests.
8. Stop before modifying project files unless the user explicitly asks for changes.

## Output

Return a short Markdown note with a checklist and one follow-up risk.
