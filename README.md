# AI Marketplace

Portable custom marketplace for Codex and Claude Code. It has no GUI; it is a
repository layout that both apps can add as a marketplace and install plugins
from.

## Contents

- Codex marketplace: `.agents/plugins/marketplace.json`
- Claude Code marketplace: `.claude-plugin/marketplace.json`
- Demo plugin: `plugins/starter-tools`
- Discipline plugins: `plugins/common`, `plugins/qa`, `plugins/aqa`,
  `plugins/perf`, `plugins/security`, `plugins/a11y`, `plugins/domain`

`starter-tools` includes two shared skills:

- `implementation-plan`: inspect a repo and produce a concise implementation plan
- `code-review`: review changes for bugs, risks, regressions, and missing tests

Claude Code also gets native plugin agents:

- `implementation-planner`
- `code-reviewer`

The discipline plugins package reference QE skills and placeholder agents for
marketplace import smoke testing.

Codex gets per-skill `agents/openai.yaml` metadata for the same two experiences.

## Install Locally

### Claude Code

From any terminal:

```powershell
claude plugin marketplace add "C:\PROJECTS\AI stuff\ai_marketplace"
claude plugin install starter-tools@ai-marketplace
```

Inside Claude Code, you can also run:

```text
/plugin marketplace add C:\PROJECTS\AI stuff\ai_marketplace
/plugin install starter-tools@ai-marketplace
```

After installing, run `/reload-plugins` or start a new Claude Code session.
The skills should be available as:

```text
/starter-tools:implementation-plan
/starter-tools:code-review
```

The plugin agents should appear in `/agents`.

### Codex App

In the Codex app, add a marketplace with:

- Source: `C:\PROJECTS\AI stuff\ai_marketplace`
- Git ref: leave empty for a local folder
- Sparse paths: leave empty for a local folder

Then install `Starter Tools` from the marketplace.

## GitHub Distribution

Push this directory to a GitHub repository, then add the marketplace by repository
name.

For Claude Code:

```text
/plugin marketplace add owner/repo
/plugin install starter-tools@ai-marketplace
```

For Codex app:

- Source: `owner/repo`
- Git ref: `main` or a release tag
- Sparse paths:

```text
.agents/plugins
plugins/starter-tools
```

## Validate

Claude Code:

```powershell
claude plugin validate .
claude plugin validate plugins/starter-tools
```

Codex:

```powershell
python "C:\Users\Yauhen_Mekeko\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" "C:\PROJECTS\AI stuff\ai_marketplace\plugins\starter-tools"
```

JSON and YAML syntax can be checked with a small script if needed:

```powershell
python -c "import json, pathlib, yaml; [json.load(open(p, encoding='utf-8')) for p in pathlib.Path('.').rglob('*.json')]; [yaml.safe_load(open(p, encoding='utf-8')) for p in pathlib.Path('.').rglob('*.yaml')]; print('syntax ok')"
```
