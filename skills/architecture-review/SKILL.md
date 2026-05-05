---
name: architecture-review
description: Project structure, module boundaries, dependency flow, and impact analysis before code changes.
summary: Mimari işlerde framework, entry point, module boundary, shared dependency ve public impact analizini kısa tut.
triggers:
  - architecture
  - mimari
  - yapı
  - proje yapısı
  - module
  - modül
  - dependency
  - bağımlılık
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

Use when the task needs project structure, module boundaries, dependency flow, or change impact.

## Focus
- Identify framework, entry point, affected module, and shared dependencies.
- Determine whether the change is local, cross-module, public API, admin, backend, auth, database, or deployment related.
- Follow existing patterns before proposing new structure.

## Guardrails
- Do not scan the whole repo unless the affected area is unclear.
- Do not introduce new architecture for a local change.
- Explain impact before touching shared modules.
