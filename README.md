# Global Router Codex

Global Router Codex is a small terminal helper for Codex-style coding agents.
It routes a task prompt to only the relevant skill instructions instead of
loading a large `AGENTS.md` file on every request.

The intended setup is:

- Global install once into `~/.agent-router/`
- Project init only when a project needs a short `AGENTS.md` and optional local skills

## Install

Review before running:

```bash
curl -fsSL -o /tmp/agent-router-install.sh https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh
less /tmp/agent-router-install.sh
bash /tmp/agent-router-install.sh
```

Fast install:

```bash
curl -fsSL https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh | bash
```

Then reload your shell:

```bash
source ~/.zshrc
```

## Commands

```bash
agent-route "Admin panelde kullanici login yetkisini duzelt"
agent-copy "Ana sayfadaki butonu mobilde duzelt"
agent-codex "Veritabanina yeni alan ekle"
agent-router-init
```

## Project Init

Inside any project:

```bash
agent-router-init
```

This creates only:

```text
AGENTS.md
.agent/skills/
```

It does not modify application code.

To create a project-specific skill:

```bash
mkdir -p .agent/skills/project-specific-skill
```

Then add:

```text
.agent/skills/project-specific-skill/SKILL.md
```

Project skills are evaluated together with global skills and get priority when
they match the prompt.

## What Gets Installed

```text
~/.agent-router/
  router.py
  skills/
  templates/
```

The installer also adds an idempotent Agent Router block to `~/.zshrc`.

## Safety Rules

The routed prompt always includes final working rules:

- Identify relevant files first.
- Provide a short plan before risky changes.
- Make the minimum safe change.
- Do not perform database migrations, destructive actions, package changes,
  auth changes, or deployment changes without explicit approval.
- Summarize changed files, checks/tests, and remaining risks at the end.

