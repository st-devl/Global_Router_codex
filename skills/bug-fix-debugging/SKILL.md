---
name: bug-fix-debugging
description: Bug reports, failing tests, runtime errors, logs, regressions, broken CI, unexpected behavior, and root-cause debugging.
triggers:
  - bug
  - hata
  - error
  - exception
  - crash
  - failing
  - failed
  - failure
  - ci failed
  - test failed
  - log
  - logs
  - stack trace
  - regression
  - bozuldu
  - çalışmıyor
paths:
  - logs/
  - test/
  - tests/
  - __tests__/
  - .github/
risk: medium
---

# Bug Fix Debugging Skill

Use for bugs, failing tests, runtime errors, broken CI, regressions, or unexpected behavior.

## Focus
- Capture observed vs expected behavior and the strongest available evidence.
- Reproduce or isolate the failing path before editing when feasible.
- Fix the root cause, then check nearby regression risk.

## Guardrails
- Do not patch only symptoms unless the user explicitly asks for a workaround.
- Ask at most one focused question, and only when a critical fact blocks progress.
- Follow logs/tests over assumptions.
- If the bug is already reproducible from repo evidence, do not ask questions.
