---
name: api-safety
description: Use for API endpoints, route handlers, controllers, server actions, request validation, response shapes, and client-server data flow.
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

Use this skill when the task affects API endpoints, route handlers, controllers, server actions, request validation, or response formats.

## Check First
- Is the endpoint public or protected?
- What auth/permission guard is used?
- What input does it accept?
- What response does the frontend expect?
- Does the endpoint read or write data?
- Is validation present?
- Are sensitive fields returned?

## Rules
- Preserve existing response contracts unless explicitly changing them.
- Do not remove server-side validation.
- Do not expose sensitive data.
- Do not trust client input for ownership, tenant, or permission decisions.
- Keep error messages useful but safe.
- Avoid broad data returns when a smaller response is enough.

## Output Before Editing
1. Affected endpoint/action
2. Auth and validation impact
3. Frontend response compatibility
4. Minimal safe plan
