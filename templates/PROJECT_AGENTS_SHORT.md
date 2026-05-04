# AGENTS.md - Project Instructions

Bu proje global Agent Router ile çalışır. Uzun kurallar yerine görevle ilgili skill'ler router tarafından seçilir.
Router, görevleri simple/standard/risky/complex olarak etiketleyebilir.

## Core Rules
- İlgili dosyaları tespit etmeden kod değiştirme.
- Basit işlerde hızlı ilerle; riskli veya çok adımlı işlerde kısa plan ver.
- Planı kısa tut; mümkünse 5 maddeden fazla yazma.
- Varsayım yanlış çıkarsa dur ve yeniden değerlendir.
- Minimum güvenli değişiklik yap; mevcut mimari ve stile uy.
- Hata düzeltirken semptomu değil kök sebebi çöz.
- İş bitmeden en uygun test veya kontrolle doğrula.
- Kullanıcı onayı olmadan migration, destructive command, package upgrade, auth/deployment değişikliği veya büyük refactor yapma.
- Mümkün olan en az dosyayı değiştir.
- Gereksiz açıklama yapma; kısa ve net kal.

## Skill Router
Global router: `~/.agent-router/router.py`
Proje özel skill klasörü: `.agent/skills/`

Prompta göre sadece seçilen skill'leri kullan. Gereksiz skill dosyalarını okuma.

## Final Report
- Yapılanlar
- Değişen dosyalar
- Test/kontrol ve davranış kanıtı
- Kalan risk veya manuel kontrol
