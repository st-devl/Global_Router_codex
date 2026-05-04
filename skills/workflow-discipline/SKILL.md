---
name: workflow-discipline
description: Non-trivial tasks needing planning, staged execution, scope control, progress tracking, or reassessment when assumptions fail.
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
- Classify scope: simple, standard, risky, or complex.
- For non-trivial work, create a concise task list and verification plan before editing.
- If evidence contradicts the plan, stop and reassess.

## Guardrails
- Do not create `tasks/todo.md`, lessons, or project management files unless the user asks.
- Keep plans short; simple changes should not become ceremonies.
- Prefer the smallest correct implementation.
