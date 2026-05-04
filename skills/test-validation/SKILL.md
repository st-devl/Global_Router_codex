---
name: test-validation
description: Use for tests, lint, type checks, build validation, CI, quality checks, proof of correctness, and post-change verification.
triggers:
  - test
  - tests
  - lint
  - typecheck
  - build
  - ci
  - validation
  - kontrol
  - hata
  - bug
  - compile
  - derleme
  - unit
  - e2e
  - verify
  - doğrula
  - kanıtla
  - proof
  - quality
paths:
  - test/
  - tests/
  - __tests__/
  - .github/
  - package.json
  - pyproject.toml
  - composer.json
risk: medium
---

# Test Validation Skill

Use this skill when the task involves testing, linting, build checks, CI, proof of correctness, or validation after changes.

## Check First
- Which package manager or build tool is used?
- What scripts exist?
- Are there tests for the affected area?
- Is a full build necessary or is a smaller check enough?
- Could checks be slow or destructive?
- What evidence is enough to prove the change works?

## Rules
- Do not assume test commands; inspect project scripts/config first.
- Prefer targeted tests when possible.
- Run type/lint/build checks when appropriate.
- Do not run destructive or environment-changing commands without approval.
- If tests cannot run, explain why and list manual checks.
- Never mark a non-trivial task complete without evidence.
- When relevant, compare behavior before and after the change.
- Report exact commands and outcomes, not just that checks were done.
- Before finalizing, ask whether a senior engineer would accept the verification.

## Output
1. Commands found
2. Commands run
3. Results
4. Behavior evidence
5. Remaining manual checks or risks
