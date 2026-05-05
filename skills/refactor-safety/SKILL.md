---
name: refactor-safety
description: Refactoring, renaming, restructuring, moving files, extracting components, improving architecture, or reducing duplication.
summary: Refactor işlerinde davranışı koru, public surface etkisini doğrula, unrelated cleanup ve geniş redesign yapma.
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

Use when the task changes structure, names, file locations, public APIs, shared components, or duplication.

## Focus
- Define exact refactor scope and behavior that must remain unchanged.
- Check imports, routes, tests, shared exports, and public API impact.
- Consider whether a smaller local change solves the problem.
- Verify any public surface that may shift: routes, exports, CLI flags, endpoint contracts, or schema-like interfaces.

## Public Surface Verification
- Routes/endpoints: run targeted route/API tests or a smoke request when available.
- Exports/imports: run typecheck, build, or import-focused tests.
- CLI flags/config: run help output, config validation, or the smallest command smoke test.
- Contracts/schemas: run contract tests, schema validation, or affected serialization checks.

## Guardrails
- Do not perform broad refactors unless explicitly requested.
- Avoid unrelated formatting and opportunistic cleanup.
- Do not rename routes, files, exports, or public APIs without a clear plan.
- Prefer incremental, behavior-preserving changes.
- Do not treat "cleanup" as permission to redesign unrelated code.
