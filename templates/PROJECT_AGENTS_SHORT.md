# AGENTS.md - Agent Router Project

Bu proje global Agent Router kullanır. Router görevleri `simple`, `standard`,
`risky` veya `complex` olarak etiketler ve yalnızca ilgili skill'leri seçer.

## Rules
- Seçilen skill'leri kullan; ilgisiz skill dosyalarını okuma.
- İlgili dosyaları tespit et, en az dosyayla çöz, doğrulamadan bitirme.
- Riskli değişikliklerde onay almadan migration, destructive command, package
  change, auth/deployment değişikliği veya büyük refactor yapma.
- Gereksiz açıklama ve proje yönetimi dosyası üretme.

## Paths
- Global router: `~/.agent-router/router.py`
- Project skills: `.agent/skills/`
