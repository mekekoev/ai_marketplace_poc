---
name: code-review
description: >
  Review code changes for bugs, behavioral regressions, security risks,
  reliability problems, and missing tests. Use this skill when the user asks for
  a review, PR review, diff review, risk check, or quality pass.
---

# Code Review

Use this skill when the user wants a review rather than an implementation.

## Workflow

1. Determine the change under review from the user's prompt, local diff, commit,
   PR branch, or specified files.
2. Read the changed code and the surrounding code needed to understand runtime
   behavior.
3. Prioritize concrete bugs, regressions, security issues, data loss risks, and
   missing tests over style preferences.
4. Ground every finding in a file and line whenever possible.
5. If no actionable issues are found, say so clearly and mention any remaining
   test gaps or residual risk.

## Output

Lead with findings, ordered by severity:

```markdown
## Findings
- [P1] Short issue title - path/to/file:line
  Explain the bug, why it matters, and the scenario that triggers it.

## Open Questions
- Any questions that affect correctness.

## Summary
- Brief context only after findings.
```

Use priorities `P0` through `P3`, where `P0` blocks release and `P3` is minor.
Do not include broad praise or unrelated refactors.
