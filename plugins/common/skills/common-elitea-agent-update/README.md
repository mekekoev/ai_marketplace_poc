# common-elitea-agent-update

Push a local Markdown instruction file to an existing ELITEA agent via the REST API. The skill parses a header block in your `.md` (Agent ID / Version ID / Project ID / URL), preserves the agent's existing `llm_settings`, `tools`, `tags`, and other version fields, and only updates what you explicitly change.

---

## Install

Install the skill via `npx skills add`:

```bash
npx skills add git@git.epam.com:epmt-rtqa/qe-agent-skills.git --skill common-elitea-agent-update
```

By default this installs into the current project's `.claude/skills/`. Pass `--global` (or run from your home directory) to install user-scoped at `~/.claude/skills/` so it is available in every project.

After installing, restart Claude Code so the skill is picked up.

Set `ELITEA_API_TOKEN` in your project `.env` (or shell environment). The script walks up from the current working directory looking for the nearest `.env`, stopping at the `.git` boundary.

---

## What This Skill Changes

| Without skill | With skill |
|---|---|
| Hand-craft a PUT body and risk wiping `llm_settings` / `tools` / `tags` | GETs the current version first, merges only changed fields |
| Guess the right API path | Targets the documented `prompt_lib/{project_id}/{agent_id}` endpoint |
| Apply changes blind | Dry-run by default — shows a diff and char counts before `--apply` |
| Hardcode IDs in scripts | Reads `Agent ID` / `Version ID` / `Project ID` / `URL` from the `.md` header |
| Paste tokens into commands | Loads `ELITEA_API_TOKEN` from `.env` automatically |

---

## When It Triggers

Say any of the following (exact phrasing not required):

- *"update the agent instruction"*
- *"sync this .md to the ELITEA agent"*
- *"push my_instr/foo.md to ELITEA"*
- *"update agent 79 with this file"*
- Hand over a `.md` file whose header lists `Agent ID:`, `Version ID:`, `Project ID:`, and `URL:`.

---

## Expected `.md` File Shape

```
Agent ID: 79
Version ID: 79
Project ID: 29
URL: https://next.elitea.ai/

# Role & Persona
You are the ...
```

Recognised header keys (case-insensitive): `Agent ID`, `Version ID`, `Project ID`, `URL`. Everything from the first blank line / first Markdown heading onward becomes the new `instructions` value.

---

## Default Workflow

1. **Dry-run** (default — no `--apply`):

   ```bash
   python3 .claude/skills/common-elitea-agent-update/scripts/update_agent.py path/to/file.md
   ```

   Prints parsed target (agent / version / project / base URL), fetches the current version, and shows a diff-style summary.

2. **Review the summary** with the user.

3. **Apply** only after confirmation:

   ```bash
   python3 .claude/skills/common-elitea-agent-update/scripts/update_agent.py path/to/file.md --apply
   ```

---

## Updating Other Fields

Pass `--set FIELD=VALUE` (repeatable):

- `--set name="New agent name"` — top-level application name
- `--set description="..."` — top-level application description
- `--set welcome_message="..."` — version-level welcome message

```bash
python3 .claude/skills/common-elitea-agent-update/scripts/update_agent.py \
    my_instr/postman_researcher.md \
    --set description="Postman researcher with structured output" \
    --apply
```

---

## Overriding Header Values

If the `.md` header is missing or wrong, override per-invocation:

- `--agent-id`
- `--version-id`
- `--project-id`
- `--base-url`

---

## Structure

```
common-elitea-agent-update/
├── SKILL.md                  # workflow, expected file shape, do-not list
├── README.md
└── scripts/
    └── update_agent.py       # GET-merge-PUT with dry-run by default
```

---

## Notes

- **Endpoint** — `PUT {{base_url}}/api/v1/applications/application/prompt_lib/{{project_id}}/{{agent_id}}`. It lives under `archive/` in the Postman collection but remains the live update path.
- **GET-before-PUT** — the script always fetches the current version and merges only the fields you asked to change, so `llm_settings`, `tools`, `tags`, `conversation_starters`, etc. are preserved.
- **Auth** — `ELITEA_API_TOKEN` is read from env or the nearest `.env`. Never hardcode it.
- **Dry-run first** — apply only after the user has reviewed the diff.

---

## Author

[Dzmitry Shaplyka](https://git.epam.com/dzmitry_shaplyka) — EPAM QE Practice
