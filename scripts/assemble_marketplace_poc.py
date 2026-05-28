#!/usr/bin/env python3
"""Assemble marketplace plugins from a skills registry checkout.

This is intentionally small PoC automation:
- read `skills/<discipline>/<skill>` and `agents/<discipline>/<agent>`
- generate `plugins/<discipline>`
- update Codex and Claude marketplace files
- do not validate generated artifacts
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


DISCIPLINE_LABELS = {
    "a11y": "Accessibility Testing",
    "aqa": "AQA Automation",
    "common": "Common QE",
    "domain": "Domain Testing",
    "perf": "Performance Testing",
    "qa": "Functional QA",
    "security": "Security Testing",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble marketplace plugins from skills registry.")
    parser.add_argument("--registry", required=True, help="Path to registry checkout.")
    parser.add_argument("--output", required=True, help="Path to marketplace checkout.")
    return parser.parse_args()


def title_from_name(name: str) -> str:
    return DISCIPLINE_LABELS.get(name, " ".join(part.capitalize() for part in name.split("-")))


def short_description(discipline: str, skill_count: int, agent_count: int) -> str:
    return f"{skill_count} skills and {agent_count} agents from the {discipline} registry."


def plugin_description(discipline: str, skill_count: int, agent_count: int) -> str:
    label = title_from_name(discipline)
    return f"{label} plugin assembled from skills_registry with {skill_count} skills and {agent_count} agents."


def read_skill_description(skill_dir: Path) -> str | None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return None
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def copy_skills(registry: Path, output_plugin: Path, discipline: str) -> list[str]:
    source_root = registry / "skills" / discipline
    target_root = output_plugin / "skills"
    target_root.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    if not source_root.is_dir():
        return copied

    for skill_dir in sorted(source_root.iterdir(), key=lambda path: path.name):
        if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").is_file():
            continue
        shutil.copytree(skill_dir, target_root / skill_dir.name, dirs_exist_ok=True)
        copied.append(skill_dir.name)
    return copied


def copy_agents(registry: Path, output_plugin: Path, discipline: str) -> list[str]:
    source_root = registry / "agents" / discipline
    target_root = output_plugin / "agents"
    target_root.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    if not source_root.is_dir():
        return copied

    for agent_dir in sorted(source_root.iterdir(), key=lambda path: path.name):
        agent_md = agent_dir / "AGENT.md"
        if not agent_dir.is_dir() or not agent_md.is_file():
            continue
        shutil.copy2(agent_md, target_root / f"{agent_dir.name}.md")
        copied.append(agent_dir.name)
    return copied


def discover_disciplines(registry: Path) -> list[str]:
    names: set[str] = set()
    for root_name in ("skills", "agents"):
        root = registry / root_name
        if root.is_dir():
            names.update(path.name for path in root.iterdir() if path.is_dir())
    return sorted(names)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_plugin_manifest(discipline: str, skills: list[str], agents: list[str]) -> dict:
    label = title_from_name(discipline)
    description = plugin_description(discipline, len(skills), len(agents))
    prompts = [f"Use {label} to help with a {discipline} task."]
    if skills:
        prompts.append(f"Use ${skills[0]} from {label}.")
    return {
        "name": discipline,
        "version": "0.1.0",
        "description": description,
        "author": {"name": "QE Practice VS"},
        "license": "MIT",
        "keywords": [discipline, "qe", "marketplace"],
        "skills": "./skills/",
        "interface": {
            "displayName": label,
            "shortDescription": short_description(discipline, len(skills), len(agents)),
            "longDescription": description,
            "developerName": "QE Practice VS",
            "category": "Productivity",
            "capabilities": ["Write"],
            "defaultPrompt": prompts[:3],
        },
    }


def marketplace_entry(name: str) -> dict:
    return {
        "name": name,
        "source": {"source": "local", "path": f"./plugins/{name}"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Productivity",
    }


def load_json_object(path: Path, fallback: dict) -> dict:
    if not path.is_file():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def update_codex_marketplace(output: Path, generated_names: list[str]) -> None:
    path = output / ".agents" / "plugins" / "marketplace.json"
    payload = load_json_object(
        path,
        {
            "name": "ai-marketplace",
            "interface": {"displayName": "AI Marketplace"},
            "plugins": [],
        },
    )
    generated = set(generated_names)
    existing = [entry for entry in payload.get("plugins", []) if entry.get("name") not in generated]
    payload["plugins"] = existing + [marketplace_entry(name) for name in generated_names]
    write_json(path, payload)


def update_claude_marketplace(output: Path, generated_names: list[str], descriptions: dict[str, str]) -> None:
    path = output / ".claude-plugin" / "marketplace.json"
    payload = load_json_object(
        path,
        {
            "name": "ai-marketplace",
            "owner": {"name": "Local Developer"},
            "metadata": {"description": "A portable marketplace for shared plugins.", "version": "0.1.0"},
            "plugins": [],
        },
    )
    generated = set(generated_names)
    existing = [entry for entry in payload.get("plugins", []) if entry.get("name") not in generated]
    for name in generated_names:
        existing.append(
            {
                "name": name,
                "description": descriptions[name],
                "version": "0.1.0",
                "source": f"./plugins/{name}",
                "author": {"name": "QE Practice VS"},
                "license": "MIT",
                "category": "productivity",
                "keywords": [name, "qe", "marketplace"],
            }
        )
    payload["plugins"] = existing
    write_json(path, payload)


def assemble(registry: Path, output: Path) -> None:
    generated_names: list[str] = []
    descriptions: dict[str, str] = {}

    for discipline in discover_disciplines(registry):
        plugin_root = output / "plugins" / discipline
        if plugin_root.exists():
            shutil.rmtree(plugin_root)
        (plugin_root / ".codex-plugin").mkdir(parents=True, exist_ok=True)

        skills = copy_skills(registry, plugin_root, discipline)
        agents = copy_agents(registry, plugin_root, discipline)
        if not skills and not agents:
            continue

        manifest = build_plugin_manifest(discipline, skills, agents)
        write_json(plugin_root / ".codex-plugin" / "plugin.json", manifest)
        generated_names.append(discipline)
        descriptions[discipline] = manifest["description"]

    update_codex_marketplace(output, generated_names)
    update_claude_marketplace(output, generated_names, descriptions)
    print(f"Assembled {len(generated_names)} plugins: {', '.join(generated_names)}")


def main() -> None:
    args = parse_args()
    assemble(Path(args.registry).resolve(), Path(args.output).resolve())


if __name__ == "__main__":
    main()
