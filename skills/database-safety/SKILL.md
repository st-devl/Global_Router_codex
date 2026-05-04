---
name: database-safety
description: Use for database schema, migrations, ORM models, SQL queries, data relations, destructive data actions, and tenant data safety.
triggers:
  - database
  - db
  - veritabanı
  - prisma
  - migration
  - migrate
  - schema
  - model
  - table
  - tablo
  - column
  - kolon
  - relation
  - sql
  - query
  - seed
  - kayıt
  - veri
paths:
  - prisma/
  - migrations/
  - schema
  - models/
  - database/
  - db/
risk: high
---

# Database Safety Skill

Use this skill when a task may affect database schema, ORM models, migrations, queries, relations, or stored data.

## Check First
- Which database/ORM is used?
- Which schema/model/query files are affected?
- Is this a read-only change or a write/schema change?
- Could existing records break?
- Could data be lost?
- Is a migration required?
- Does the project have multi-tenant or permission-based data isolation?

## Rules
- Do not create or run migrations without explicit user approval.
- Do not run destructive commands without explicit user approval.
- Do not drop tables, columns, relations, or constraints without a clear plan.
- Preserve existing data compatibility.
- Add fallbacks for existing records when adding new fields.
- Do not trust client-provided IDs for sensitive data access.
- Prefer minimal schema changes.

## Output Before Editing
1. Affected models/tables
2. Data risk
3. Whether migration is required
4. Backward compatibility plan
5. Minimal safe implementation plan
