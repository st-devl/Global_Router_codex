#!/usr/bin/env python3
"""Route a user task to the smallest useful set of agent skills."""

from __future__ import annotations

import os
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Tuple


AGENT_ROUTER_HOME = Path(os.environ.get("AGENT_ROUTER_HOME", Path.home() / ".agent-router"))
GLOBAL_SKILLS_DIR = AGENT_ROUTER_HOME / "skills"

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

DEFAULT_MAX_SKILLS = 2
EXTENDED_MAX_SKILLS = 3
MIN_SKILL_SCORE = 4
SECONDARY_SKILL_RATIO = 0.35
PREFIX_TRIGGER_MIN_LEN = 7

TOKEN_RE = re.compile(r"[a-zA-ZığüşöçİĞÜŞÖÇ0-9_/-]+")

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

REPO_SIGNAL_RULES = {
    "database-safety": [
        "prisma/schema.prisma",
        "prisma/migrations",
        "db/migrations",
        "database/migrations",
        "supabase/migrations",
        "drizzle.config.ts",
        "drizzle.config.js",
        "knexfile.js",
        "alembic",
    ],
    "auth-security": [
        "auth.ts",
        "auth.js",
        "auth.config.ts",
        "middleware.ts",
        "middleware.js",
        "app/api/auth",
        "pages/api/auth",
        "src/auth",
        "guards",
    ],
    "api-safety": [
        "app/api",
        "pages/api",
        "routes/api.php",
        "server/routes",
        "src/routes",
        "controllers",
    ],
    "ui-ux-change": [
        "components",
        "styles",
        "src/components",
        "app/components",
        "tailwind",
        "tailwind.config.js",
        "tailwind.config.ts",
        "postcss.config.js",
    ],
    "test-validation": [
        "tests",
        "__tests__",
        "test",
        "spec",
        "jest.config.js",
        "jest.config.ts",
        "vitest.config.js",
        "vitest.config.ts",
        "pytest.ini",
    ],
    "deployment-safety": [
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        ".env",
        ".github/workflows",
        "vercel",
        "vercel.json",
        "netlify.toml",
        "deploy",
    ],
    "workflow-discipline": [
        "AGENTS.md",
        "docs",
    ],
    "architecture-review": [
        "src",
        "modules",
        "services",
        "packages",
    ],
    "refactor-safety": [
        "src",
        "lib",
        "components",
    ],
}

TASK_CLASS_RULES = {
    "complex": {
        "plan",
        "planning",
        "workflow",
        "orchestration",
        "complex",
        "complexity",
        "architecture",
        "mimari",
        "redesign",
        "task list",
        "gorev listesi",
        "multi step",
        "multi-step",
        "adim adim",
        "kapsamli",
    },
    "risky": {
        "database",
        "db",
        "migration",
        "migrate",
        "schema",
        "auth",
        "login",
        "permission",
        "permissions",
        "admin",
        "deploy",
        "deployment",
        "production",
        "prod",
        "secret",
        "secrets",
        "token",
        "delete",
        "remove",
        "drop",
        "destructive",
        "veritabani",
        "yetki",
        "guvenlik",
        "sifre",
        "sil",
        "kaldir",
    },
}

WORKFLOW_POLICIES = {
    "simple": "Inspect only the relevant files, make the smallest change, run a brief targeted check.",
    "standard": "Use a short plan only when impact is unclear or more than two files are involved.",
    "risky": "Stop before database, auth, deployment, destructive, package, or broad refactor changes and get explicit approval.",
    "complex": "Create a concise task list, verify assumptions, and proceed in small validated steps.",
}

VERIFICATION_POLICIES = {
    "simple": "syntax check, targeted unit test, or direct smoke check",
    "standard": "targeted check plus nearby regression check when shared behavior is touched",
    "risky": "approval first, then the narrowest relevant check plus behavior evidence",
    "complex": "incremental checks after each meaningful step; stop after repeated failure",
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


def contains_rule(text: str, tokens: set[str], rule: str) -> bool:
    rule_l = normalize_text(rule)
    if not rule_l:
        return False
    if " " in rule_l or "/" in rule_l or "." in rule_l:
        return rule_l in text
    return rule_l in tokens


def task_rule_match(prompt: str, class_name: str) -> bool:
    prompt_l = normalize_text(prompt)
    prompt_tokens = set(tokenize(prompt))
    return any(contains_rule(prompt_l, prompt_tokens, rule) for rule in TASK_CLASS_RULES[class_name])


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


def package_json_signals(project_root: Path) -> set[str]:
    signals: set[str] = set()
    package_json = project_root / "package.json"

    if not package_json.exists():
        return signals

    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return signals

    deps = {}
    for key in ("dependencies", "devDependencies"):
        value = data.get(key)
        if isinstance(value, dict):
            deps.update({normalize_text(name): True for name in value})

    if any(name in deps for name in ("prisma", "drizzle-orm", "knex", "sequelize", "typeorm")):
        signals.add("database-safety")
    if any(name in deps for name in ("next-auth", "@auth/core", "passport", "jsonwebtoken", "bcrypt", "bcryptjs")):
        signals.add("auth-security")
    if any(name in deps for name in ("express", "fastify", "hono", "koa", "trpc", "@trpc/server")):
        signals.add("api-safety")
    if any(name in deps for name in ("react", "vue", "svelte", "tailwindcss", "@vitejs/plugin-react")):
        signals.add("ui-ux-change")
    if any(name in deps for name in ("jest", "vitest", "playwright", "cypress", "eslint", "typescript")):
        signals.add("test-validation")

    return signals


def path_exists(project_root: Path, hint: str) -> bool:
    hint = hint.strip().rstrip("/")
    if not hint:
        return False
    return (project_root / hint).exists()


def collect_repo_signals(project_root: Path, skills: List[Dict[str, object]]) -> set[str]:
    signals = package_json_signals(project_root)

    for skill_name, hints in REPO_SIGNAL_RULES.items():
        for hint in hints:
            if path_exists(project_root, hint):
                signals.add(skill_name)
                break

    for skill in skills:
        name = str(skill.get("name", ""))
        for hint in skill.get("paths", []):
            if path_exists(project_root, str(hint)):
                signals.add(name)
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

    name_parts = tokenize(str(skill.get("name", "")).replace("-", " "))
    for part in name_parts:
        if len(part) >= 4 and (part in prompt_token_set or any(matches_prefix(part, token) for token in prompt_tokens)):
            score += 2

    risk = normalize_text(skill.get("risk", ""))
    has_risky_word = task_rule_match(prompt, "risky")

    if matched_trigger and risk == "high" and has_risky_word:
        score += 2

    if skill.get("source") == "project" and score > 0:
        score += 3

    if skill["name"] in repo_signals and score > 0:
        score += 1

    return score


def allowed_skill_count(scored: List[Tuple[Dict[str, object], int]], prompt: str) -> int:
    names = {str(skill.get("name", "")) for skill, _score in scored}
    risk_count = sum(1 for skill, _score in scored if skill.get("risk") == "high")

    if {"bug-fix-debugging", "test-validation"}.issubset(names):
        return EXTENDED_MAX_SKILLS

    if risk_count >= 2 or (task_rule_match(prompt, "complex") and len(names) > DEFAULT_MAX_SKILLS):
        return EXTENDED_MAX_SKILLS

    return DEFAULT_MAX_SKILLS


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
    max_skills = allowed_skill_count(scored, prompt)

    for skill, score in scored:
        if score < cutoff:
            continue

        name = skill["name"]
        if name in seen_names:
            continue
        selected.append((skill, score))
        seen_names.add(name)

        if len(selected) >= max_skills:
            break

    return selected


def classify_task(prompt: str, selected: List[Tuple[Dict[str, object], int]]) -> str:
    prompt_tokens = set(tokenize(prompt))
    selected_names = {skill["name"] for skill, _ in selected}

    if task_rule_match(prompt, "complex"):
        return "complex"

    if selected and any(skill.get("risk") == "high" for skill, _ in selected):
        return "risky"

    if task_rule_match(prompt, "risky"):
        return "risky"

    if len(prompt_tokens) <= 5:
        return "simple"

    if len(selected_names) > 1:
        return "standard"

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

    lines.append("## Workflow Policy")
    lines.append(f"- Mode: {WORKFLOW_POLICIES[task_class]}")
    lines.append(f"- Required verification: {VERIFICATION_POLICIES[task_class]}.")
    lines.append("")

    lines.append("## Final Working Rules")
    lines.append("- First identify the relevant files and the smallest safe file set.")
    lines.append("- Keep plans under 5 bullets unless the user asks for more detail.")
    lines.append("- If evidence contradicts the plan, stop and reassess before continuing.")
    lines.append("- If the same check fails twice, stop and summarize the evidence instead of looping.")
    lines.append("- Keep explanations concise; do not narrate obvious code.")
    lines.append("- Do not perform database migrations, destructive actions, package changes, auth changes, or deployment changes without explicit approval.")
    lines.append("- Done requires changed files, checks/tests, behavior evidence, and remaining risks.")
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
    skills = project_skills + global_skills
    repo_signals = collect_repo_signals(project_root, skills)
    selected = select_skills(skills, prompt, repo_signals)
    task_class = classify_task(prompt, selected)

    print(build_output(prompt, project_root, selected, task_class))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
