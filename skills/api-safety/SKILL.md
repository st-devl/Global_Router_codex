---
name: api-safety
description: API endpoints, route handlers, controllers, server actions, request validation, response shapes, and client-server data flow.
triggers:
  - api
  - endpoint
  - route
  - controller
  - server action
  - fetch
  - request
  - response
  - json
  - body
  - validation
  - post
  - get
  - put
  - delete
paths:
  - api/
  - routes/
  - controllers/
  - server/
  - actions/
risk: high
---

# API Safety Skill

Use when a task affects endpoints, route handlers, controllers, server actions, validation, or response contracts.

## Focus
- Identify endpoint/action, auth guard, accepted input, write/read scope, and frontend response expectations.
- Check validation, ownership/tenant decisions, error messages, and sensitive fields.

## Guardrails
- Preserve response contracts unless the user explicitly changes them.
- Keep server-side validation and permission checks.
- Do not trust client input for ownership, tenant, or permission decisions.
- Return only the data the caller needs.
