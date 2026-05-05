---
name: workflow-discipline
description: Non-trivial tasks needing planning, staged execution, scope control, progress tracking, or reassessment when assumptions fail.
summary: Non-trivial işlerde router task class'ını takip et, kısa plan yap, çelişen evidence görünce yeniden değerlendir.
triggers:
  - plan
  - planning
  - workflow
  - orchestration
  - kapsam
  - süreç
  - task list
  - görev listesi
  - adım adım
  - complex
  - karmaşık
  - architecture
  - mimari
  - redesign
  - büyük değişiklik
paths:
  - AGENTS.md
  - docs/
  - tasks/
risk: medium
---

# Workflow Discipline Skill

Use for multi-step, risky, unclear, or architecture-sensitive work.

## Focus
- Follow the router's task class: simple, standard, risky, or complex.
- For non-trivial work, create a concise task list and verification plan before editing.
- If evidence contradicts the plan, stop and reassess.
- Keep simple tasks short; use a fuller workflow only when the scope justifies it.

## Guardrails
- Do not create `tasks/todo.md`, lessons, or project management files unless the user asks.
- Track progress in the conversation by default, not project files.
- Keep plans short; simple changes should not become ceremonies.
- Prefer the smallest correct implementation.
