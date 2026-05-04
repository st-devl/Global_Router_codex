Sen uzman bir terminal tooling / developer experience mühendisisin.

Bana macOS üzerinde, proje bağımsız çalışan, terminalden kullanılabilen, hızlı, güvenli ve düşük token tüketimli bir “Agent Skill Router” sistemi kurmanı istiyorum.

Bu sistemin amacı:
- Codex veya benzeri terminal coding agent’larında kullanılmak üzere prompta göre sadece gerekli skill talimatlarını seçmek.
- Her promptta büyük ve uzun AGENTS.md dosyaları okutmak yerine, kısa ana kurallar + ilgili küçük skill dosyalarını kullanmak.
- Sistemi teknoloji bağımsız yapmak.
- Next.js, Laravel, Django, Python, Go, Rust, Java, Flutter, WordPress gibi farklı projelerde aynı router sistemini kullanabilmek.
- Her projenin kendi özel skill’leri varsa onları da global skill’lerle birlikte değerlendirmek.
- Gereksiz skill dosyalarını prompta eklememek.
- Riskli işlemlerde Codex’i önce plan vermeye zorlamak.
- Database migration, auth değişikliği, deployment değişikliği, destructive command, paket güncelleme gibi işleri kullanıcı onayı olmadan yaptırmamak.

ÇOK ÖNEMLİ:
- Bu sistemi mevcut proje kodlarıyla karıştırma.
- Bu bir uygulama feature’ı değil, bilgisayarımda global çalışan terminal yardımcı aracıdır.
- Sistemi `~/.agent-router/` altına kur.
- Proje içinde sadece isteğe bağlı `.agent/skills/` klasörü ve kısa `AGENTS.md` template’i kullanılacak.
- Mevcut projedeki application dosyalarını değiştirme.
- Eğer şu an bir proje klasöründeysen, proje dosyalarına dokunma. Sadece global `~/.agent-router/` dosyalarını oluştur.
- `~/.zshrc` dosyasına alias/fonksiyon eklemeden önce mevcut içeriği bozma. Sadece gerekli bloğu ekle. Aynı blok zaten varsa tekrar ekleme.
- Kurulum sonunda nasıl kullanılacağını kısa ama net açıkla.
- Her dosyayı oluşturduktan sonra içeriğini kontrol et.
- Shell komutlarını güvenli kullan.
- Destructive komut kullanma.
- Home dizini dışında gereksiz dosya oluşturma.

İSTENEN GLOBAL KLASÖR YAPISI:

`~/.agent-router/`
  - `router.py`
  - `skills/`
    - `architecture-review/SKILL.md`
    - `database-safety/SKILL.md`
    - `auth-security/SKILL.md`
    - `api-safety/SKILL.md`
    - `ui-ux-change/SKILL.md`
    - `test-validation/SKILL.md`
    - `refactor-safety/SKILL.md`
    - `deployment-safety/SKILL.md`
  - `templates/`
    - `PROJECT_AGENTS_SHORT.md`

AYRICA:
- `router.py` çalıştırılabilir olsun.
- Terminalden şu komutlar çalışsın:
  - `agent-route "görev metni"` → routed promptu terminalde göstersin.
  - `agent-copy "görev metni"` → routed promptu panoya kopyalasın.
  - `agent-codex "görev metni"` → routed promptla Codex’i başlatsın.

Eğer macOS dışı bir ortam algılarsan `pbcopy` yerine uygun fallback düşün; ama ana hedef macOS/zsh.

ROUTER DAVRANIŞI:

`router.py` şu şekilde çalışmalı:

1. Komut satırından prompt almalı:
   - Örnek: `agent-route "Admin panelde fiyat alanı ekle"`

2. Mevcut çalışma dizininden proje kökünü bulmalı.
   Proje kökü tespiti için şu marker’ları kullan:
   - `.git`
   - `AGENTS.md`
   - `package.json`
   - `pyproject.toml`
   - `composer.json`
   - `go.mod`
   - `Cargo.toml`
   - `pom.xml`
   - `build.gradle`

3. Global skill klasörünü okumalı:
   - `~/.agent-router/skills`

4. Proje özel skill klasörlerini de desteklemeli:
   - `.agent/skills`
   - `.agents/skills`
   - `.codex/skills`

5. Her skill dosyası şu formatı desteklemeli:
   - `SKILL.md`
   - Başta opsiyonel YAML benzeri frontmatter:
     - `name`
     - `description`
     - `triggers`
     - `paths`
     - `risk`

6. Router gerçek YAML bağımlılığı kullanmadan basit frontmatter parse edebilmeli.
   Ek Python paketi kurma.
   Sadece Python standard library kullan.

7. Skill seçimi:
   - Prompt içindeki kelimeler `triggers`, `paths`, `name`, `description` ile eşleşirse skor ver.
   - Proje özel skill varsa global skill’e göre öncelikli olsun.
   - En fazla 3 skill seç.
   - Hiç skill eşleşmezse sadece local `AGENTS.md` kullanılması gerektiğini söyle.
   - Gereksiz skill dosyalarını çıktıya ekleme.

8. Çıktı formatı:
   Router şu bölümleri üretmeli:

   # Routed Agent Prompt

   ## User Task
   [kullanıcı promptu]

   ## Project Context
   - Project root: ...
   - Read the local `AGENTS.md` if it exists.
   - Do not read unrelated skill files.
   - Use only the selected skills below unless the task clearly requires another one.

   ## Selected Skills
   - seçilen skill’ler

   ## Skill Instructions
   [sadece seçilen SKILL.md içerikleri]

   ## Final Working Rules
   - First identify the relevant files.
   - Before risky changes, provide a short plan.
   - Make the minimum safe change.
   - Do not perform database migrations, destructive actions, package changes, auth changes, or deployment changes without explicit approval.
   - At the end, summarize changed files, checks/tests, and remaining risks.

9. Router Türkçe promptlarda da çalışmalı.
   Trigger listelerinde Türkçe ve İngilizce kelimeler kullanılmalı.

10. Kod güvenli, okunabilir ve yorumlu olsun.

GLOBAL SKILL DOSYALARI:

Aşağıdaki 8 skill dosyasını oluştur.

1) `~/.agent-router/skills/architecture-review/SKILL.md`

İçerik:

---
name: architecture-review
description: Use for understanding project structure, architecture, module boundaries, dependency flow, and impact analysis before code changes.
triggers:
  - architecture
  - mimari
  - yapı
  - proje yapısı
  - klasör
  - module
  - modül
  - dependency
  - bağımlılık
  - refactor
  - impact
  - etki
paths:
  - src/
  - app/
  - lib/
  - modules/
  - services/
risk: medium
---

# Architecture Review Skill

Use this skill when the task requires understanding the project structure, module boundaries, dependencies, or the impact of a change.

## Check First
- What is the project type and main framework?
- Where is the entry point?
- Which module/page/service/component is affected?
- Is the change local or system-wide?
- Does the change affect public, admin, backend, database, auth, or deployment areas?
- Are there existing patterns that should be followed?

## Rules
- Do not assume the framework or architecture; inspect project files first.
- Do not scan the whole repository unless necessary.
- Prefer following existing patterns over creating a new architecture.
- Avoid large refactors unless explicitly requested.
- Before changing shared modules, explain the impact.

## Output Before Risky Work
1. Relevant files
2. Current flow
3. Impacted modules
4. Minimal safe plan

2) `~/.agent-router/skills/database-safety/SKILL.md`

İçerik:

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

3) `~/.agent-router/skills/auth-security/SKILL.md`

İçerik:

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

4) `~/.agent-router/skills/api-safety/SKILL.md`

İçerik:

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

5) `~/.agent-router/skills/ui-ux-change/SKILL.md`

İçerik:

---
name: ui-ux-change
description: Use for visual design, components, layout, responsive behavior, forms, buttons, theme, CSS, accessibility, and frontend user experience.
triggers:
  - ui
  - ux
  - tasarım
  - design
  - component
  - layout
  - css
  - tailwind
  - style
  - responsive
  - mobil
  - mobile
  - button
  - buton
  - form
  - tema
  - renk
  - font
  - accessibility
paths:
  - components/
  - styles/
  - css
  - tailwind
  - pages/
  - app/
risk: medium
---

# UI / UX Change Skill

Use this skill when the task affects visual design, layout, components, responsiveness, CSS, forms, buttons, or theme.

## Check First
- Which component/page is affected?
- Is the component shared?
- Does the change affect desktop and mobile?
- Is there an existing design system or theme?
- Are styles hardcoded or token-based?
- Are forms still usable and accessible?

## Rules
- Do not redesign unrelated areas.
- Do not introduce random colors or inconsistent spacing.
- Preserve responsive behavior.
- Avoid unnecessary animations and heavy dependencies.
- Prefer existing components and style patterns.
- Keep forms usable and labels clear.
- Do not break accessibility basics.

## Output Before Editing
1. Affected UI files
2. Shared component impact
3. Responsive risk
4. Minimal safe plan

6) `~/.agent-router/skills/test-validation/SKILL.md`

İçerik:

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

7) `~/.agent-router/skills/refactor-safety/SKILL.md`

İçerik:

---
name: refactor-safety
description: Use for refactoring, renaming, restructuring, moving files, extracting components, improving architecture, or reducing duplication.
triggers:
  - refactor
  - yeniden düzenle
  - düzenle
  - restructure
  - rename
  - taşı
  - move
  - split
  - extract
  - cleanup
  - clean up
  - sadeleştir
  - tekrar
  - duplication
paths:
  - src/
  - app/
  - lib/
  - components/
risk: high
---

# Refactor Safety Skill

Use this skill when the task involves refactoring, renaming, moving files, splitting modules, extracting components, or changing structure.

## Check First
- What is the exact goal of the refactor?
- Which files are truly affected?
- Are imports/routes/tests affected?
- Is the refactor behavior-preserving?
- Could it affect public API or user flows?

## Rules
- Do not perform broad refactors unless explicitly requested.
- Keep behavior unchanged unless asked.
- Avoid unrelated formatting changes.
- Update imports carefully.
- Do not rename routes, files, exports, or public APIs without a plan.
- Prefer small incremental refactors.

## Output Before Editing
1. Refactor scope
2. Files to change
3. Behavior preservation plan
4. Risk areas

8) `~/.agent-router/skills/deployment-safety/SKILL.md`

İçerik:

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

PROJECT AGENTS TEMPLATE:

`~/.agent-router/templates/PROJECT_AGENTS_SHORT.md` içeriği şöyle olsun:

# AGENTS.md — Project Instructions

Bu proje üzerinde çalışırken önce mevcut mimariyi ve dosya yapısını anlamadan büyük değişiklik yapma.

## Ana Kurallar
- Gereksiz dosya okuma.
- İlgili dosyaları tespit etmeden kod değiştirme.
- Büyük veya riskli değişikliklerden önce kısa plan ver.
- Minimum güvenli değişiklik yap.
- Mevcut mimari ve kod stiline uy.
- Gereksiz paket ekleme.
- Kullanıcı onayı olmadan database migration, destructive command, auth değişikliği, deployment değişikliği veya büyük refactor yapma.

## Skill Router
Bu projede detaylı kurallar global agent skill sistemiyle yönetilir.

Prompta göre sadece ilgili skill’ler kullanılmalıdır. Gereksiz skill dosyaları okunmamalıdır.

Global router:
`~/.agent-router/router.py`

Proje özel skill klasörü:
`.agent/skills/`

## Görev Sonu Raporu
Her iş sonunda kısa rapor ver:

- Yapılanlar
- Değişen dosyalar
- Test / kontrol
- Risk veya manuel kontrol gerekiyorsa belirt

ROUTER.PY İÇERİĞİ:

`~/.agent-router/router.py` dosyasını aşağıdaki mantıkla yaz. Kod temiz, güvenli ve Python standard library ile çalışmalı.

Kullanman gereken örnek referans kod:

```python
#!/usr/bin/env python3
import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

GLOBAL_SKILLS_DIR = Path.home() / ".agent-router" / "skills"

PROJECT_SKILL_DIR_NAMES = [
    ".agent/skills",
    ".agents/skills",
    ".codex/skills",
]

MAX_SKILLS = 3


def find_project_root(start: Path) -> Path:
    current = start.resolve()

    markers = [
        ".git",
        "AGENTS.md",
        "package.json",
        "pyproject.toml",
        "composer.json",
        "go.mod",
        "Cargo.toml",
        "pom.xml",
        "build.gradle",
    ]

    while current != current.parent:
        for marker in markers:
            if (current / marker).exists():
                return current
        current = current.parent

    return start.resolve()


def parse_frontmatter(text: str) -> Tuple[Dict[str, object], str]:
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    raw = parts[1].strip()
    body = parts[2].strip()

    meta: Dict[str, object] = {}
    current_key: Optional[str] = None

    for line in raw.splitlines():
        line = line.rstrip()

        if not line.strip():
            continue

        if re.match(r"^[A-Za-z0-9_-]+:", line):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key

            if value == "":
                meta[key] = []
            else:
                meta[key] = value.strip('"').strip("'")

        elif line.strip().startswith("-") and current_key:
            item = line.strip()[1:].strip().strip('"').strip("'")
            if not isinstance(meta.get(current_key), list):
                meta[current_key] = []
            meta[current_key].append(item)

    return meta, body


def load_skills_from_dir(base_dir: Path, source: str) -> List[Dict[str, object]]:
    skills = []

    if not base_dir.exists():
        return skills

    for skill_file in sorted(base_dir.glob("*/SKILL.md")):
        text = skill_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        name = str(meta.get("name") or skill_file.parent.name)

        triggers = meta.get("triggers", [])
        paths = meta.get("paths", [])

        if isinstance(triggers, str):
            triggers = [triggers]
        if isinstance(paths, str):
            paths = [paths]

        skills.append({
            "name": name,
            "path": skill_file,
            "source": source,
            "meta": meta,
            "body": body,
            "triggers": triggers,
            "paths": paths,
            "description": meta.get("description", ""),
            "risk": meta.get("risk", "medium"),
        })

    return skills


def find_project_skills(project_root: Path) -> List[Dict[str, object]]:
    skills = []

    for rel in PROJECT_SKILL_DIR_NAMES:
        skills.extend(load_skills_from_dir(project_root / rel, "project"))

    return skills


def score_skill(skill: Dict[str, object], prompt: str) -> int:
    prompt_l = prompt.lower()
    score = 0

    for trigger in skill.get("triggers", []):
        trigger_l = str(trigger).lower()
        if trigger_l and trigger_l in prompt_l:
            score += 4

    for path_hint in skill.get("paths", []):
        path_l = str(path_hint).lower()
        if path_l and path_l in prompt_l:
            score += 5

    name = str(skill.get("name", "")).lower().replace("-", " ")
    for part in name.split():
        if len(part) >= 4 and part in prompt_l:
            score += 1

    description = str(skill.get("description", "")).lower()
    for word in re.findall(r"[a-zA-ZığüşöçİĞÜŞÖÇ0-9_/-]{5,}", description):
        if word in prompt_l:
            score += 1

    risk = str(skill.get("risk", "")).lower()
    risky_words = [
        "delete", "remove", "drop", "migration", "database", "auth",
        "security", "deploy", "production", "sil", "kaldır", "veritabanı",
        "yetki", "güvenlik", "token", "şifre", "admin"
    ]

    if risk == "high" and any(w in prompt_l for w in risky_words):
        score += 2

    return score


def select_skills(skills: List[Dict[str, object]], prompt: str) -> List[Tuple[Dict[str, object], int]]:
    scored = []

    for skill in skills:
        s = score_skill(skill, prompt)
        if s > 0:
            scored.append((skill, s))

    scored.sort(key=lambda x: (x[1], 1 if x[0]["source"] == "project" else 0), reverse=True)

    selected = []
    seen_names = set()

    for skill, score in scored:
        name = skill["name"]
        if name in seen_names:
            continue
        selected.append((skill, score))
        seen_names.add(name)

        if len(selected) >= MAX_SKILLS:
            break

    return selected


def build_output(prompt: str, project_root: Path, selected: List[Tuple[Dict[str, object], int]]) -> str:
    lines = []

    lines.append("# Routed Agent Prompt")
    lines.append("")
    lines.append("## User Task")
    lines.append(prompt)
    lines.append("")
    lines.append("## Project Context")
    lines.append(f"- Project root: `{project_root}`")
    lines.append("- Read the local `AGENTS.md` if it exists.")
    lines.append("- Do not read unrelated skill files.")
    lines.append("- Use only the selected skills below unless the task clearly requires another one.")
    lines.append("")

    if selected:
        lines.append("## Selected Skills")
        for skill, score in selected:
            lines.append(f"- `{skill['name']}` from `{skill['source']}` — score {score}")
        lines.append("")

        lines.append("## Skill Instructions")
        for skill, score in selected:
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append(f"# Skill: {skill['name']}")
            lines.append(f"Source: `{skill['source']}`")
            lines.append(f"File: `{skill['path']}`")
            lines.append("")
            lines.append(str(skill["body"]).strip())
            lines.append("")
    else:
        lines.append("## Selected Skills")
        lines.append("- No specific skill matched. Use only the local `AGENTS.md` and make the minimum safe change.")
        lines.append("")

    lines.append("## Final Working Rules")
    lines.append("- First identify the relevant files.")
    lines.append("- Before risky changes, provide a short plan.")
    lines.append("- Make the minimum safe change.")
    lines.append("- Do not perform database migrations, destructive actions, package changes, auth changes, or deployment changes without explicit approval.")
    lines.append("- At the end, summarize changed files, checks/tests, and remaining risks.")
    lines.append("")

    return "\n".join(lines)


def main():
    prompt = " ".join(sys.argv[1:]).strip()

    if not prompt:
        print('Usage: agent-route "your task prompt"')
        sys.exit(1)

    cwd = Path(os.getcwd())
    project_root = find_project_root(cwd)

    global_skills = load_skills_from_dir(GLOBAL_SKILLS_DIR, "global")
    project_skills = find_project_skills(project_root)

    all_skills = project_skills + global_skills

    selected = select_skills(all_skills, prompt)

    print(build_output(prompt, project_root, selected))


if __name__ == "__main__":
    main()



#~/.zshrc içine şu bloğu ekle. Eğer aynı blok zaten varsa tekrar ekleme.

    # Agent Router
alias agent-route='python3 ~/.agent-router/router.py'

agent-copy() {
  python3 ~/.agent-router/router.py "$@" | pbcopy
  echo "Routed prompt panoya kopyalandı."
}

agent-codex() {
  codex "$(python3 ~/.agent-router/router.py "$@")"
}






#KURULUM SONRASI DOĞRULAMA:

Kurulumdan sonra şu testleri yap:

Dosya yapısı oluştu mu?
ls -R ~/.agent-router
Router çalışıyor mu?
python3 ~/.agent-router/router.py "Admin panelde kullanıcı login yetkisini düzelt"
Alias çalışıyor mu?
agent-route "Veritabanına yeni alan ekle"
Panoya kopyalama çalışıyor mu?
agent-copy "Ana sayfadaki butonu mobilde düzelt"
Çıktıda sadece ilgili skill’ler var mı kontrol et:
Auth promptunda auth-security
Database promptunda database-safety
UI promptunda ui-ux-change
Deployment promptunda deployment-safety

KURULUM SONU RAPORU:

İş bitince bana şu formatta rapor ver:

Kurulan Dosyalar
...
Eklenen Terminal Komutları
agent-route
agent-copy
agent-codex
Test Sonuçları
...
Kullanım Örnekleri
...
Notlar
Eğer .zshrc otomatik reload edilmediyse source ~/.zshrc çalıştırmam gerektiğini belirt.
Eğer codex komutu bulunamadıysa sadece agent-route ve agent-copy kullanılabileceğini söyle.

EKSTRA İSTEK:
Ayrıca bulunduğum mevcut proje için hiçbir application dosyasını değiştirmeden, sadece örnek olarak proje özel skill klasörü oluşturma komutunu raporda göster:

mkdir -p .agent/skills/project-specific-skill

Ama bu komutu otomatik çalıştırma; sadece raporda örnek olarak ver.

Şimdi bu sistemi kur.


Bu promptu verdikten sonra Codex’e özellikle şunu söylemen iyi olur: **“Önce plan ver, sonra uygula.”** Ama yukarıdaki prompt zaten bunu güvenlik olarak içeriyor.