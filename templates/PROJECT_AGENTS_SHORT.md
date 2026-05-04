# AGENTS.md - Project Instructions

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

Prompta göre sadece ilgili skill'ler kullanılmalıdır. Gereksiz skill dosyaları okunmamalıdır.

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

