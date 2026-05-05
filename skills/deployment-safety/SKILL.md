---
name: deployment-safety
description: Deployment, environment variables, Docker, CI/CD, hosting config, build settings, production issues, secrets, and release changes.
summary: Deployment işlerinde secrets, env, CI/CD, production config ve rollback riskini değiştirmeden önce açık et.
triggers:
  - deploy
  - deployment
  - production
  - prod
  - env
  - environment
  - docker
  - ci
  - cd
  - vercel
  - server
  - hosting
  - release
  - secret
  - config
paths:
  - Dockerfile
  - docker-compose
  - .env
  - .github/
  - vercel
  - deploy
  - config
risk: high
---

# Deployment Safety Skill

Use when the task affects deployment, env vars, Docker, CI/CD, hosting, build config, secrets, or production behavior.

## Focus
- Identify affected environment: local, staging, production, build, or runtime.
- Check secret handling, hosting config, CI/CD impact, and rollback risk.

## Guardrails
- Do not expose or commit secrets.
- Do not change production config or CI/CD pipelines casually.
- Preserve existing build/runtime behavior unless explicitly changing it.
- Explain deployment risk before editing risky config.
