---
name: auth-security
description: Authentication, authorization, sessions, cookies, JWT, passwords, roles, permissions, admin areas, and sensitive access control.
summary: Auth işlerinde guard, session/token güvenliği, server-side permission ve admin erişimini zayıflatma.
triggers:
  - auth
  - authentication
  - authorization
  - login
  - logout
  - session
  - cookie
  - jwt
  - token
  - password
  - şifre
  - yetki
  - rol
  - permission
  - admin
  - superadmin
  - guard
  - middleware
paths:
  - auth/
  - middleware
  - session
  - login
  - admin
  - guards
risk: high
---

# Auth Security Skill

Use when the task affects login, sessions, tokens, cookies, roles, permissions, admin areas, middleware, or guards.

## Focus
- Identify the auth system, protected routes, session validation, and server-side permission checks.
- Check whether the change affects privileged/admin flows or sensitive tokens/cookies.

## Guardrails
- Do not remove guards or make protected routes public.
- Do not expose tokens, cookies, secrets, password hashes, or sensitive claims.
- Do not log secrets or weaken hashing/token validation.
- Frontend-only permission checks are not sufficient.
