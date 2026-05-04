---
name: bug-fix-debugging
description: Use for bug reports, failing tests, runtime errors, logs, regressions, broken CI, unexpected behavior, and root-cause debugging.
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

Use this skill when the user reports a bug, failing test, runtime error, broken CI check, or unexpected behavior.

## Check First
- What is the observed behavior?
- What is the expected behavior?
- Is there an error message, stack trace, failing test, or log?
- Which recent change or affected flow is most likely related?
- Can the issue be reproduced with a targeted command?

## Rules
- Find the root cause before editing.
- Do not patch only the symptom unless the user explicitly asks for a temporary workaround.
- Prefer targeted reproduction and targeted tests.
- Keep the fix minimal and behavior-focused.
- Check for nearby regressions after fixing.
- If logs or tests point to a different cause than expected, follow the evidence and reassess.
- Do not ask the user for hand-holding when the repo contains enough evidence to investigate.

## Output
1. Reproduction or evidence used
2. Root cause
3. Fix summary
4. Verification commands and results
5. Remaining risk, if any
