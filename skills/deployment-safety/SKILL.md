---
name: deployment-safety
description: Use for deployment, environment variables, Docker, CI/CD, hosting config, build settings, production issues, secrets, and release changes.
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

Use this skill when the task affects deployment, environment variables, hosting config, Docker, CI/CD, build settings, secrets, or production behavior.

## Check First
- Which environment is affected: local, staging, production?
- Are secrets or environment variables involved?
- Does this affect build or runtime?
- Is hosting configuration changed?
- Could deployment break existing users?

## Rules
- Do not expose secrets.
- Do not commit `.env` secrets.
- Do not change production config without explicit approval.
- Do not change CI/CD pipelines casually.
- Preserve existing build behavior.
- Explain deployment risks before editing.

## Output Before Editing
1. Affected deployment/config files
2. Environment impact
3. Secret/security risk
4. Minimal safe plan
