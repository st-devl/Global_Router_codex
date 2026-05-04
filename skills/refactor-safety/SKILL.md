---
name: refactor-safety
description: Use for refactoring, renaming, restructuring, moving files, extracting components, improving architecture, or reducing duplication.
triggers:
  - refactor
  - yeniden düzenle
  - düzenle
  - restructure
  - rename
  - taşı
  - move
  - split
  - extract
  - cleanup
  - clean up
  - sadeleştir
  - elegant
  - kalite
  - iyileştir
  - tekrar
  - duplication
paths:
  - src/
  - app/
  - lib/
  - components/
risk: high
---

# Refactor Safety Skill

Use this skill when the task involves refactoring, renaming, moving files, splitting modules, extracting components, or changing structure.

## Check First
- What is the exact goal of the refactor?
- Which files are truly affected?
- Are imports/routes/tests affected?
- Is the refactor behavior-preserving?
- Could it affect public API or user flows?
- Is there a simpler way to get the same outcome without restructuring?

## Rules
- Do not perform broad refactors unless explicitly requested.
- Keep behavior unchanged unless asked.
- Avoid unrelated formatting changes.
- Update imports carefully.
- Do not rename routes, files, exports, or public APIs without a plan.
- Prefer small incremental refactors.
- If the approach feels hacky, reassess and choose the simplest maintainable solution.
- Do not chase elegance at the cost of unnecessary abstraction.

## Output Before Editing
1. Refactor scope
2. Files to change
3. Behavior preservation plan
4. Simpler alternative considered
5. Risk areas
