---
name: auth-security
description: Use for authentication, authorization, sessions, cookies, JWT, passwords, roles, permissions, admin areas, and sensitive access control.
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

Use this skill when the task affects login, session handling, cookies, JWT, roles, permissions, admin areas, middleware, or route guards.

## Check First
- What auth system is used?
- Which routes are public and which are protected?
- Where is session validation done?
- Are roles/permissions checked server-side?
- Does the change affect admin or privileged areas?
- Are cookies/tokens handled securely?

## Rules
- Do not remove auth guards.
- Do not make protected routes public.
- Do not expose tokens, cookies, secrets, or password hashes to the client.
- Do not log secrets.
- Do not weaken password hashing or token validation.
- Server-side permission checks must remain.
- Frontend-only permission checks are not sufficient.

## Output Before Editing
1. Affected auth files
2. Access control impact
3. Security risks
4. Minimal safe plan
