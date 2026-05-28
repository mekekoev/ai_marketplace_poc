# salesforce-flow-smoke

Prepare lightweight Salesforce flow smoke checks for marketplace validation and domain skill discovery tests.

---

## Install

npx skills add git@git.epam.com:epmt-rtqa/qe-agent-skills.git --skill salesforce-flow-smoke

---

## What This Skill Changes

| Without skill | With skill |
|---|---|
| Marketplace import smoke tests rely on a missing domain testing skill. | A small domain testing placeholder can be installed and invoked. |
| Script discovery cannot be checked for this discipline. | Two deterministic scripts are available for smoke checks. |

---

## When It Triggers

- "Use salesforce-flow-smoke to smoke test marketplace import."
- "Check the domain testing plugin placeholder skill."

---

## Author

QE Practice VS <qe_practice_vs@epam.com>
