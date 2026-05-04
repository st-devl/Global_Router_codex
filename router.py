#!/usr/bin/env python3
"""Route a user task to the smallest useful set of agent skills."""

from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Tuple


GLOBAL_SKILLS_DIR = Path.home() / ".agent-router" / "skills"

PROJECT_SKILL_DIR_NAMES = [
    ".agent/skills",
    ".agents/skills",
    ".codex/skills",
]

PROJECT_MARKERS = [
    ".git",
    "AGENTS.md",
    "package.json",
    "pyproject.toml",
    "composer.json",
    "go.mod",
    "Cargo.toml",
    "pom.xml",
    "build.gradle",
]

MAX_SKILLS = 3
MIN_SKILL_SCORE = 4
SECONDARY_SKILL_RATIO = 0.30
PREFIX_TRIGGER_MIN_LEN = 5
DESCRIPTION_MATCH_LIMIT = 2

TOKEN_RE = re.compile(r"[a-zA-ZığüşöçİĞÜŞÖÇ0-9_/-]+")
WORD_RE = re.compile(r"[a-zA-ZığüşöçİĞÜŞÖÇ0-9_/-]{5,}")

TURKISH_ASCII_MAP = str.maketrans(
    {
        "ı": "i",
        "İ": "i",
        "ş": "s",
        "Ş": "s",
        "ğ": "g",
        "Ğ": "g",
        "ü": "u",
        "Ü": "u",
        "ö": "o",
        "Ö": "o",
        "ç": "c",
        "Ç": "c",
    }
)

RISKY_WORDS = [
    "delete",
    "remove",
    "drop",
    "migration",
    "database",
    "auth",
    "security",
    "deploy",
    "production",
    "sil",
    "kaldir",
    "veritabani",
    "yetki",
    "guvenlik",
    "token",
    "sifre",
    "admin",
]

DESCRIPTION_STOP_WORDS = {
    "agent",
    "before",
    "change",
    "changes",
    "checks",
    "files",
    "global",
    "project",
    "safety",
    "skill",
    "tasks",
    "which",
}

REPO_SIGNAL_MAP = {
    "database-safety": [
        "prisma",
        "migrations",
        "migration",
        "database",
        "db",
        "models",
        "seed",
        "sql",
        "schema",
    ],
    "auth-security": [
        "auth",
        "middleware",
        "guards",
        "session",
        "login",
        "admin",
    ],
    "api-safety": [
        "api",
        "routes",
        "controllers",
        "server",
        "actions",
    ],
    "ui-ux-change": [
        "components",
        "styles",
        "css",
        "tailwind",
        "pages",
        "app",
    ],
    "test-validation": [
        "tests",
        "test",
        "__tests__",
        ".github",
        "package.json",
        "pyproject.toml",
        "composer.json",
    ],
    "deployment-safety": [
        "Dockerfile",
        "docker-compose",
        ".env",
        ".github",
        "vercel",
        "deploy",
        "config",
    ],
    "workflow-discipline": [
        "AGENTS.md",
        "docs",
        "tasks",
    ],
    "architecture-review": [
        "src",
        "app",
        "lib",
        "modules",
        "services",
    ],
    "refactor-safety": [
        "src",
        "app",
        "lib",
        "components",
    ],
}

RISK_KEYWORDS = {
    "database",
    "db",
    "migration",
    "migrate",
    "schema",
    "auth",
    "login",
    "permission",
    "admin",
    "deploy",
    "deployment",
    "production",
    "prod",
    "secret",
    "refactor",
}

COMPLEXITY_KEYWORDS = {
    "plan",
    "planning",
    "workflow",
    "orchestration",
    "complex",
    "complexity",
    "architecture",
    "mimari",
    "refactor",
    "redesign",
    "task list",
    "gorev listesi",
    "multi step",
    "multi-step",
    "adim adim",
}


def find_project_root(start: Path) -> Path:
    """Find the nearest parent that looks like a project root."""
    current = start.resolve()

    while current != current.parent:
        if any((current / marker).exists() for marker in PROJECT_MARKERS):
            return current
        current = current.parent

    return start.resolve()


def parse_frontmatter(text: str) -> Tuple[Dict[str, object], str]:
    """Parse a tiny YAML-like frontmatter block without external packages."""
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    raw = parts[1].strip()
    body = parts[2].strip()

    meta: Dict[str, object] = {}
    current_key: Optional[str] = None

    for raw_line in raw.splitlines():
        line = raw_line.rstrip()

        if not line.strip():
            continue

        if re.match(r"^[A-Za-z0-9_-]+:", line):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key

            if value:
                meta[key] = value.strip('"').strip("'")
            else:
                meta[key] = []
            continue

        if line.strip().startswith("-") and current_key:
            item = line.strip()[1:].strip().strip('"').strip("'")
            if not isinstance(meta.get(current_key), list):
                meta[current_key] = []
            meta[current_key].append(item)

    return meta, body


def as_list(value: object) -> List[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def normalize_text(text: object) -> str:
    normalized = str(text).translate(TURKISH_ASCII_MAP).casefold()
    decomposed = unicodedata.normalize("NFKD", normalized)
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def tokenize(text: object) -> List[str]:
    return TOKEN_RE.findall(normalize_text(text))


def matches_prefix(trigger: str, token: str) -> bool:
    return len(trigger) >= PREFIX_TRIGGER_MIN_LEN and token.startswith(trigger)


def load_skills_from_dir(base_dir: Path, source: str) -> List[Dict[str, object]]:
    skills: List[Dict[str, object]] = []

    if not base_dir.exists():
        return skills

    for skill_file in sorted(base_dir.glob("*/SKILL.md")):
        try:
            text = skill_file.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"Warning: could not read skill file {skill_file}: {exc}", file=sys.stderr)
            continue

        meta, body = parse_frontmatter(text)
        name = str(meta.get("name") or skill_file.parent.name)

        skills.append(
            {
                "name": name,
                "path": skill_file,
                "source": source,
                "meta": meta,
                "body": body,
                "triggers": as_list(meta.get("triggers", [])),
                "paths": as_list(meta.get("paths", [])),
                "description": str(meta.get("description", "")),
                "risk": str(meta.get("risk", "medium")),
            }
        )

    return skills


def find_project_skills(project_root: Path) -> List[Dict[str, object]]:
    skills: List[Dict[str, object]] = []

    for rel in PROJECT_SKILL_DIR_NAMES:
        skills.extend(load_skills_from_dir(project_root / rel, "project"))

    return skills


def collect_repo_signals(project_root: Path) -> set[str]:
    signals: set[str] = set()

    for skill_name, hints in REPO_SIGNAL_MAP.items():
        for hint in hints:
            if (project_root / hint).exists():
                signals.add(skill_name)
                break

    return signals


def score_skill(skill: Dict[str, object], prompt: str, repo_signals: set[str]) -> int:
    prompt_l = normalize_text(prompt)
    prompt_tokens = tokenize(prompt)
    prompt_token_set = set(prompt_tokens)
    score = 0
    matched_trigger = False

    for trigger in skill.get("triggers", []):
        trigger_l = normalize_text(trigger)
        if not trigger_l:
            continue

        if " " in trigger_l:
            if trigger_l in prompt_l:
                score += 7
                matched_trigger = True
            continue

        if "/" in trigger_l or "." in trigger_l:
            if trigger_l in prompt_l:
                score += 5
                matched_trigger = True
            continue

        for token in prompt_tokens:
            if token == trigger_l:
                score += 6
                matched_trigger = True
                break
            if matches_prefix(trigger_l, token):
                score += 4
                matched_trigger = True
                break

    for path_hint in skill.get("paths", []):
        path_l = normalize_text(path_hint)
        if path_l and path_l in prompt_l:
            score += 5

    name_parts = tokenize(str(skill.get("name", "")).replace("-", " "))
    for part in name_parts:
        if len(part) >= 4 and (part in prompt_token_set or any(matches_prefix(part, token) for token in prompt_tokens)):
            score += 2

    description_matches = 0
    for word in WORD_RE.findall(normalize_text(skill.get("description", ""))):
        if word in DESCRIPTION_STOP_WORDS:
            continue
        if word in prompt_token_set:
            score += 1
            description_matches += 1
            if description_matches >= DESCRIPTION_MATCH_LIMIT:
                break

    risk = normalize_text(skill.get("risk", ""))
    has_risky_word = any(
        word in prompt_token_set or any(matches_prefix(word, token) for token in prompt_tokens)
        for word in RISKY_WORDS
    )

    if matched_trigger and risk == "high" and has_risky_word:
        score += 2

    if skill.get("source") == "project" and score > 0:
        score += 3

    if skill["name"] in repo_signals and score > 0:
        score += 2

    return score


def select_skills(skills: List[Dict[str, object]], prompt: str, repo_signals: set[str]) -> List[Tuple[Dict[str, object], int]]:
    scored: List[Tuple[Dict[str, object], int]] = []

    for skill in skills:
        score = score_skill(skill, prompt, repo_signals)
        if score >= MIN_SKILL_SCORE:
            scored.append((skill, score))

    scored.sort(
        key=lambda item: (
            item[1],
            1 if item[0].get("source") == "project" else 0,
            str(item[0].get("name", "")),
        ),
        reverse=True,
    )

    if not scored:
        return []

    top_score = scored[0][1]
    cutoff = max(MIN_SKILL_SCORE, int(top_score * SECONDARY_SKILL_RATIO))

    selected: List[Tuple[Dict[str, object], int]] = []
    seen_names = set()

    for skill, score in scored:
        if score < cutoff:
            continue

        name = skill["name"]
        if name in seen_names:
            continue
        selected.append((skill, score))
        seen_names.add(name)

        if len(selected) >= MAX_SKILLS:
            break

    return selected


def classify_task(prompt: str, selected: List[Tuple[Dict[str, object], int]]) -> str:
    prompt_l = normalize_text(prompt)
    prompt_tokens = set(tokenize(prompt))
    selected_names = {skill["name"] for skill, _ in selected}

    if selected and any(skill.get("risk") == "high" for skill, _ in selected):
        return "risky"

    if any(keyword in prompt_l for keyword in COMPLEXITY_KEYWORDS):
        return "complex"

    if any(keyword in prompt_tokens for keyword in RISK_KEYWORDS):
        return "risky"

    if len(selected_names) > 1:
        return "standard"

    if len(prompt_tokens) <= 5:
        return "simple"

    return "standard"


def build_output(prompt: str, project_root: Path, selected: List[Tuple[Dict[str, object], int]], task_class: str) -> str:
    lines: List[str] = []

    lines.append("# Routed Agent Prompt")
    lines.append("")
    lines.append("## User Task")
    lines.append(prompt)
    lines.append("")
    lines.append("## Project Context")
    lines.append(f"- Project root: `{project_root}`")
    lines.append(f"- Task class: `{task_class}`")
    lines.append("- Read the local `AGENTS.md` if it exists.")
    lines.append("- Do not read unrelated skill files.")
    lines.append("- Use only the selected skills below unless the task clearly requires another one.")
    lines.append("")

    if selected:
        lines.append("## Selected Skills")
        for skill, score in selected:
            lines.append(f"- `{skill['name']}` from `{skill['source']}` - score {score}")
        lines.append("")

        lines.append("## Skill Instructions")
        for skill, _score in selected:
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append(f"# Skill: {skill['name']}")
            lines.append(f"Source: `{skill['source']}`")
            lines.append(f"File: `{skill['path']}`")
            lines.append("")
            lines.append(str(skill["body"]).strip())
            lines.append("")
    else:
        lines.append("## Selected Skills")
        lines.append("- No specific skill matched. Use only the local `AGENTS.md` and make the minimum safe change.")
        lines.append("")

    if task_class == "simple":
        lines.append("## Workflow Mode")
        lines.append("- Keep it short. Inspect only what is needed, change the minimum, verify briefly.")
        lines.append("")
    elif task_class == "risky":
        lines.append("## Workflow Mode")
        lines.append("- Stop before risky edits. Give a short plan and require approval for database, auth, deployment, or destructive changes.")
        lines.append("")
    elif task_class == "complex":
        lines.append("## Workflow Mode")
        lines.append("- Create a concise task list, verify assumptions, and proceed incrementally.")
        lines.append("")

    lines.append("## Final Working Rules")
    lines.append("- First identify the relevant files.")
    lines.append("- Before risky changes, provide a short plan.")
    lines.append("- If evidence contradicts the plan, stop and reassess before continuing.")
    lines.append("- Make the minimum safe change.")
    lines.append("- Do not perform database migrations, destructive actions, package changes, auth changes, or deployment changes without explicit approval.")
    lines.append("- Before finishing, verify the work with the most relevant available check.")
    lines.append("- At the end, summarize changed files, checks/tests, behavior evidence, and remaining risks.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    prompt = " ".join(sys.argv[1:]).strip()

    if not prompt:
        print('Usage: agent-route "your task prompt"', file=sys.stderr)
        return 1

    project_root = find_project_root(Path(os.getcwd()))
    global_skills = load_skills_from_dir(GLOBAL_SKILLS_DIR, "global")
    project_skills = find_project_skills(project_root)
    repo_signals = collect_repo_signals(project_root)
    selected = select_skills(project_skills + global_skills, prompt, repo_signals)
    task_class = classify_task(prompt, selected)

    print(build_output(prompt, project_root, selected, task_class))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
