# Global Router Codex

Global Router Codex, Codex gibi terminal tabanlı coding agent'lar için hazırlanmış
global bir **Agent Skill Router** sistemidir.

Amaç basit: Her görevde uzun `AGENTS.md` dosyalarını veya bütün skill
talimatlarını prompt'a eklemek yerine, yazdığın göreve göre sadece gerekli
skill dosyalarını seçmek.

Bu sayede prompt daha kısa, daha odaklı ve daha güvenli olur.

## Ne İşe Yarar?

- Görev metnine göre doğru skill talimatlarını seçer.
- Gereksiz skill dosyalarını prompt'a eklemez.
- Token tüketimini azaltır.
- Database, auth, deployment, refactor gibi riskli işlerde Codex'i daha dikkatli
  çalışmaya zorlar.
- Her projeye router kopyalamadan global çalışır.
- İstersen projeye özel skill dosyalarını da destekler.

Örnek:

```bash
agent-route "Admin login yetkisini düzelt"
```

Bu görev için `auth-security` skill'i seçilir.

```bash
agent-route "Veritabanına yeni alan ekle"
```

Bu görev için `database-safety` skill'i seçilir.

## Çalışma Mantığı

Sistem bilgisayara global olarak kurulur:

```text
~/.agent-router/
```

Projelerin içine router kodu kopyalanmaz. Projeye sadece istersen kısa bir
`AGENTS.md` ve proje özel skill klasörü eklenir:

```text
AGENTS.md
.agent/skills/
```

Router, komutu hangi proje klasöründe çalıştırırsan o klasörden proje kökünü
bulur. Şu dosyalardan biri proje kökü olarak kabul edilir:

```text
.git
AGENTS.md
package.json
pyproject.toml
composer.json
go.mod
Cargo.toml
pom.xml
build.gradle
```

## Kurulum

Güvenli yöntem: Script'i önce indirip oku, sonra çalıştır.

```bash
curl -fsSL -o /tmp/agent-router-install.sh https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh
less /tmp/agent-router-install.sh
bash /tmp/agent-router-install.sh
```

Hızlı kurulum:

```bash
curl -fsSL https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh | bash
```

Kurulumdan sonra terminal ayarlarını yenile:

```bash
source ~/.zshrc
```

## Komutlar

Routed prompt'u terminalde gösterir:

```bash
agent-route "Görev metni"
```

Routed prompt'u panoya kopyalar:

```bash
agent-copy "Görev metni"
```

Routed prompt ile Codex'i başlatır:

```bash
agent-codex "Görev metni"
```

Bulunduğun projeye kısa `AGENTS.md` ve `.agent/skills/` klasörü ekler:

```bash
agent-router-init
```

## Yeni Bir Projede Kullanım

Yeni veya mevcut bir projeye gir:

```bash
cd /path/to/project
```

Projeyi router için hazırla:

```bash
agent-router-init
```

Bu komut sadece şunları oluşturur:

```text
AGENTS.md
.agent/skills/
```

Uygulama kodlarına dokunmaz.

Sonra görevleri router üzerinden çalıştır:

```bash
agent-codex "Admin panelde kullanıcı yetkisini düzelt"
```

veya sadece prompt'u görmek için:

```bash
agent-route "Mobilde buton hizasını düzelt"
```

## Proje Özel Skill Ekleme

Global skill'ler yetmezse proje içinde özel skill ekleyebilirsin.

Örnek:

```bash
mkdir -p .agent/skills/project-specific-skill
```

Sonra şu dosyayı oluştur:

```text
.agent/skills/project-specific-skill/SKILL.md
```

Örnek skill formatı:

```markdown
---
name: project-specific-skill
description: Bu projeye özel iş kuralları.
triggers:
  - ödeme
  - invoice
  - tenant
paths:
  - app/
  - src/
risk: medium
---

# Project Specific Skill

Bu projede ödeme, tenant veya fatura alanlarına dokunmadan önce mevcut akışı
incele. Gereksiz refactor yapma. Veri bütünlüğünü koru.
```

Proje özel skill'leri global skill'lerle birlikte değerlendirilir ve eşleşirse
öncelik kazanır.

## Mevcut Skill'ler

Global olarak gelen skill'ler:

- `architecture-review`
- `database-safety`
- `auth-security`
- `api-safety`
- `ui-ux-change`
- `test-validation`
- `refactor-safety`
- `deployment-safety`

Router en fazla 3 skill seçer. Eşleşme yoksa sadece local `AGENTS.md`
kullanılmasını söyler.

## Güncelleme

Bu repoda yeni özellik geliştirmek için:

```bash
cd /Users/suheyp/Documents/software/CodexAgent
```

Değişiklikleri yap, test et:

```bash
bash -n install.sh
python3 router.py "Admin login yetkisini düzelt"
./install.sh
source ~/.zshrc
```

GitHub'a gönder:

```bash
git status
git add .
git commit -m "Update agent router"
git push
```

Başka bir bilgisayarda veya mevcut bilgisayarda global kurulumu güncellemek için
kurulum komutunu tekrar çalıştırabilirsin:

```bash
curl -fsSL https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh | bash
source ~/.zshrc
```

Kurulum script'i `.zshrc` içindeki Agent Router bloğunu tekrar tekrar çoğaltmaz;
varsa günceller.

## Güvenlik Kuralları

Router çıktısına her zaman şu çalışma kuralları eklenir:

- Önce ilgili dosyaları tespit et.
- Riskli değişikliklerden önce kısa plan ver.
- Minimum güvenli değişiklik yap.
- Kullanıcı onayı olmadan database migration, destructive action, paket
  değişikliği, auth değişikliği veya deployment değişikliği yapma.
- İş sonunda değişen dosyaları, testleri ve kalan riskleri özetle.

## Sorun Giderme

Komut bulunamıyorsa:

```bash
source ~/.zshrc
```

Hala bulunamıyorsa kurulum dosyalarını kontrol et:

```bash
ls -R ~/.agent-router
```

Router'ı direkt çalıştır:

```bash
python3 ~/.agent-router/router.py "Admin login yetkisini düzelt"
```

Codex komutu yoksa `agent-codex` çalışmaz. Bu durumda `agent-route` veya
`agent-copy` kullanabilirsin.

## Kısa Özet

Global kur:

```bash
curl -fsSL https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh | bash
source ~/.zshrc
```

Projede hazırla:

```bash
cd /path/to/project
agent-router-init
```

Codex'i routed prompt ile kullan:

```bash
agent-codex "Görev metni"
```
