---
name: workflow-discipline
description: Use for non-trivial tasks that need planning, staged execution, scope control, progress tracking, or reassessment when implementation changes direction.
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

Use this skill when a task is non-trivial, has several steps, touches architecture, or needs careful scope control before implementation.

## Check First
- What is the exact user goal?
- Is this a simple change or a multi-step task?
- Which parts are risky, unclear, or likely to affect other modules?
- What needs to be verified before calling the task done?

## Rules
- For simple, obvious changes, keep the plan short and proceed.
- For non-trivial or risky work, create a concise task list before editing.
- If implementation reveals a wrong assumption, stop and reassess before continuing.
- Keep progress tracking in the conversation unless the user explicitly asks for files such as `tasks/todo.md`.
- Do not create project management files automatically.
- Prefer a small correct implementation over a broad clever one.
- Before presenting the final result, ask whether the solution is still the simplest strong option.

## Output Before Implementation
1. Relevant files or areas to inspect
2. Short task list
3. Risky steps that need approval or extra care
4. Verification plan
