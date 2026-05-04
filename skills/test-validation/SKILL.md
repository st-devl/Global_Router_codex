---
name: test-validation
description: Tests, lint, type checks, build validation, CI, quality checks, proof of correctness, and post-change verification.
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

Use when the task requires tests, lint, type checks, build checks, CI, or proof that a change works.

## Focus
- Inspect available scripts/config before choosing commands.
- Prefer targeted checks; run broader checks only when risk or blast radius justifies it.
- Report exact commands, outcomes, and behavior evidence.

## Verification Matrix
- Small local edit: targeted test or syntax check.
- Shared module or API change: targeted test plus one regression check.
- Bug fix: reproduce, fix, rerun repro, and check the nearby path.
- UI change: component smoke check plus responsive sanity check.
- High-risk change: verification only after required approval and with the narrowest useful checks.

## Guardrails
- Do not run destructive or environment-changing commands without approval.
- If checks cannot run, state the blocker and give manual verification steps.
- Do not call non-trivial work done without relevant evidence.
- Keep the verification plan short and specific.
