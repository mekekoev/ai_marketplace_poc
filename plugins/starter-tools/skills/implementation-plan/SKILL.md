---
name: implementation-plan
description: >
  Inspect a repository and produce a concise implementation plan. Use this skill
  when the user asks to plan a feature, refactor, migration, integration, bug
  fix, or other code change before editing files.
---

# Implementation Plan

Use this skill to turn a requested code change into a concrete plan that another
engineer or agent can implement safely.

## Workflow

1. Inspect the existing code before deciding on an approach. Prefer fast local
   searches such as `rg`, manifests, entrypoints, schemas, tests, and nearby
   patterns.
2. Identify the current behavior, the requested behavior, and the minimum set of
   files or subsystems likely to change.
3. Make implementation choices that match the repository's existing style and
   dependencies.
4. Include validation steps that fit the change size and risk.
5. Call out assumptions only when they materially affect implementation.

## Output

Return a compact plan with these sections:

```markdown
# Implementation Plan

## Summary
- The target behavior and approach in one or two bullets.

## Key Changes
- Concrete changes grouped by subsystem or behavior.

## Tests
- Commands or scenarios that should verify the work.

## Assumptions
- Any assumptions the implementer must preserve.
```

Keep the plan decision-complete, but avoid file-by-file inventories unless file
names prevent ambiguity.
