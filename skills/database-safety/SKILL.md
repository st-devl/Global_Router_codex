---
name: database-safety
description: Database schema, migrations, ORM models, SQL queries, relations, destructive data actions, and tenant data safety.
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

Use when a task may affect schema, ORM models, migrations, SQL, relations, or stored data.

## Focus
- Identify database/ORM, affected models/tables, read/write scope, and migration need.
- Check existing records, backward compatibility, tenant isolation, and permission boundaries.

## Guardrails
- Do not create or run migrations without explicit approval.
- Do not drop or rewrite data, columns, tables, relations, or constraints without approval.
- Preserve existing data compatibility and add safe fallbacks for new fields.
- Do not trust client-provided IDs for ownership, tenant, or sensitive access.
