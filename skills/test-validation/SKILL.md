---
name: test-validation
description: Use for tests, lint, type checks, build validation, CI, quality checks, and post-change verification.
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

Use this skill when the task involves testing, linting, build checks, CI, or validation after changes.

## Check First
- Which package manager or build tool is used?
- What scripts exist?
- Are there tests for the affected area?
- Is a full build necessary or is a smaller check enough?
- Could checks be slow or destructive?

## Rules
- Do not assume test commands; inspect project scripts/config first.
- Prefer targeted tests when possible.
- Run type/lint/build checks when appropriate.
- Do not run destructive or environment-changing commands without approval.
- If tests cannot run, explain why and list manual checks.

## Output
1. Commands found
2. Commands run
3. Results
4. Remaining manual checks
