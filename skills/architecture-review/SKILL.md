---
name: architecture-review
description: Use for understanding project structure, architecture, module boundaries, dependency flow, and impact analysis before code changes.
triggers:
  - architecture
  - mimari
  - yapı
  - proje yapısı
  - klasör
  - module
  - modül
  - dependency
  - bağımlılık
  - refactor
  - impact
  - etki
paths:
  - src/
  - app/
  - lib/
  - modules/
  - services/
risk: medium
---

# Architecture Review Skill

Use this skill when the task requires understanding the project structure, module boundaries, dependencies, or the impact of a change.

## Check First
- What is the project type and main framework?
- Where is the entry point?
- Which module/page/service/component is affected?
- Is the change local or system-wide?
- Does the change affect public, admin, backend, database, auth, or deployment areas?
- Are there existing patterns that should be followed?

## Rules
- Do not assume the framework or architecture; inspect project files first.
- Do not scan the whole repository unless necessary.
- Prefer following existing patterns over creating a new architecture.
- Avoid large refactors unless explicitly requested.
- Before changing shared modules, explain the impact.

## Output Before Risky Work
1. Relevant files
2. Current flow
3. Impacted modules
4. Minimal safe plan
