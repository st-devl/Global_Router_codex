# Global Router Codex

Global Router Codex, Codex gibi terminal tabanli coding agent'lar icin hazirlanmis
bir **Agent Skill Router** sistemidir.

Kisa anlatim: Sen bir gorev yazarsin, bu sistem gorevin konusunu anlar ve Codex'e
sadece o gorev icin gerekli kurallari ekler. Her promptta butun uzun talimatlari
okutmadigi icin prompt daha kisa, daha odakli ve daha guvenli olur.

## Ne Ise Yarar?

- Auth, database, API, UI, deployment, refactor, test ve bug gibi konulari ayirt eder.
- Goreve uygun skill'i secer.
- Gereksiz skill dosyalarini prompt'a koymaz.
- Token tasarrufu saglar.
- Riskli islerde Codex'i daha dikkatli calistirir.
- Her projeye router kodunu kopyalamaz; bilgisayarda global calisir.

## En Kisa Kullanim

Bilgisayara bir kez kur:

```bash
curl -fsSL https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh | bash
source ~/.zshrc
```

Bir projeye gir ve projeyi hazirla:

```bash
cd /path/to/project
agent-router-init
```

Sonra Codex'i router uzerinden kullan:

```bash
agent-codex "Admin login yetkisini düzelt"
```

## 1. Ilk Defa Bir Projeye Dahil Etmek

Bu sistem iki asamali calisir.

### A. Bilgisayara global kurulum

Bu komut sistemi bilgisayarina kurar:

```bash
curl -fsSL https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh | bash
source ~/.zshrc
```

Bu kurulum sunlari olusturur:

```text
~/.agent-router/
  bin/
  router.py
  skills/
  templates/
  tests/
```

### B. Proje icinde hazirlik

Bir projede bu sistemi kullanmak icin once proje klasorune gir:

```bash
cd /path/to/project
```

Sonra sunu calistir:

```bash
agent-router-init
```

Bu komut proje icine sadece sunlari ekler:

```text
AGENTS.md
.agent/skills/
```

Uygulama kodlarina dokunmaz. Router kodu projeye kopyalanmaz.

## 2. Prompt Yazarken `agent-codex` Yazmak Gerekir Mi?

Evet. Router'in calismasi icin Codex'i normal `codex` komutu yerine
`agent-codex` komutuyla baslatmalisin.

Yani her promptta komut sabittir:

```bash
agent-codex "Görev metni"
```

Degisen kisim sadece tirnak icindeki gorev metnidir:

```bash
agent-codex "Admin panelde kullanıcı yetkisini düzelt"
```

Router bu prompttan `auth-security` skill'ini secer.

```bash
agent-codex "Veritabanına yeni alan ekle"
```

Router bu prompttan `database-safety` skill'ini secer.

```bash
agent-codex "Mobilde buton hizasını düzelt"
```

Router bu prompttan `ui-ux-change` skill'ini secer.

```bash
agent-codex "Testler fail oluyor loglara bakıp düzelt"
```

Router bu prompttan `bug-fix-debugging` ve `test-validation` skill'lerini secer.

Kisaca:

- Router aktif olsun istiyorsan komutun basinda mutlaka `agent-codex` yaz.
- Prompt metninin icine ekstra bir sabit kelime veya sihirli ifade yazma.
- Tırnak icindeki metni isin konusuna gore dogal yaz.

Promptun konusu neyse ona uygun kelimeler kullanmalisin: `login`, `yetki`,
`database`, `migration`, `UI`, `mobil`, `test`, `bug`, `deploy`, `refactor` gibi.

Daha net prompt daha iyi routing demektir. Kotu ornek:

```bash
agent-codex "Bunu düzelt"
```

Daha iyi ornek:

```bash
agent-codex "Admin login sonrası yetki kontrolü yanlış çalışıyor, düzelt"
```

## 3. Gunceleme

Bu sistemi daha once kurduysan ve en guncel halini almak istiyorsan su komutu
calistir:

```bash
curl -fsSL https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh | bash
source ~/.zshrc
```

Bunu bir kez calistirman yeterlidir. Cunku router global calisir:

```text
~/.agent-router/
```

Yani bir kere global guncelleme yapinca, bu bilgisayardaki tum projeler yeni
router'i kullanir. Her projede ayri ayri router guncellemen gerekmez.

Kurulumun calisir ve guncel oldugunu kontrol etmek icin:

```bash
agent-router-check
```

Beklenen basarili sonuc:

```text
Agent Router health: OK
```

Internet yoksa sadece lokal kontrolleri calistirmak icin:

```bash
AGENT_ROUTER_OFFLINE=1 agent-router-check
```

## 4. Komutlar

Promptu terminalde gormek icin:

```bash
agent-route "Görev metni"
```

Promptu panoya kopyalamak icin:

```bash
agent-copy "Görev metni"
```

Codex'i routed prompt ile baslatmak icin:

```bash
agent-codex "Görev metni"
```

Debug bilgisi gormek icin:

```bash
agent-route --debug "Görev metni"
```

Tam skill talimatlarini dahil etmek icin:

```bash
agent-route --full "Görev metni"
```

JSON cikti almak icin:

```bash
agent-route --json "Görev metni"
```

## 5. RTK-AI ile Birlikte Kullanilir Mi?

Evet, kullanilabilir. Ama ikisi ayni isi yapmaz.

Global Router Codex:

```text
Prompt hazirlar, dogru skill'i secer.
```

RTK-AI / RTK:

```text
Shell komut ciktilarini token acisindan optimize eder.
```

Bu yuzden normal proje islerinde birlikte kullanilabilirler. Ornek: Codex bir
test komutu calistiracaksa RTK shell output'unu kisaltabilir:

```bash
rtk npm test
rtk git status
rtk pytest -q
```

Ama dikkat: `agent-route`, `agent-copy` ve `agent-codex` prompt ureten
komutlardir. Bu komutlarin ciktisi RTK tarafindan filtrelenirse Codex'e gidecek
prompt bozulabilir veya eksilebilir.

Bu yuzden onerilen kullanim:

```bash
agent-codex "Admin login yetkisini düzelt"
```

RTK'yi ise Codex'in calistirdigi proje komutlarinda kullan:

```bash
rtk npm run build
rtk npm test
rtk git diff
```

Eger kendi terminalinde mutlaka RTK uzerinden calistirman gerekiyorsa, RTK'nin
raw/proxy modunu kullan:

```bash
rtk proxy agent-route "Admin login yetkisini düzelt"
```

Kisa cevap: Cakisma beklenmez. Performansi dusurmezler; farkli katmanlarda
calisirlar. Sadece routed prompt ciktisini filtreletmemeye dikkat et.

## 6. Nasil Calisir?

Router gorev metnine bakar ve task class belirler:

```text
simple
standard
risky
complex
```

Sonra uygun skill'leri secer. Varsayilan olarak en fazla 2 skill secer. Sadece
bug+verification veya birden fazla bagimsiz risk varsa 3 skill'e cikar.

Ornek skill'ler:

- `auth-security`
- `database-safety`
- `api-safety`
- `ui-ux-change`
- `test-validation`
- `bug-fix-debugging`
- `deployment-safety`
- `refactor-safety`
- `architecture-review`
- `workflow-discipline`

Normal modda prompt kisa tutulur. Skor, dosya yolu ve eslesme nedeni gibi teknik
detaylar sadece `--debug` veya `--json` ile gorunur.

## 7. Proje Ozel Skill Eklemek

Global skill'ler yetmezse proje icinde o projeye ozel skill ekleyebilirsin.

```bash
mkdir -p .agent/skills/project-specific-skill
```

Sonra su dosyayi olustur:

```text
.agent/skills/project-specific-skill/SKILL.md
```

Ornek:

```markdown
---
name: project-specific-skill
description: Bu projeye özel ödeme ve tenant kuralları.
summary: Ödeme ve tenant işlerinde mevcut akışı bozma, veri bütünlüğünü koru.
triggers:
  - ödeme
  - invoice
  - tenant
paths:
  - app/
  - src/
risk: high
---

# Project Specific Skill

Bu projede ödeme, tenant veya fatura alanlarına dokunmadan önce mevcut akışı
incele. Gereksiz refactor yapma. Veri bütünlüğünü koru.
```

## 8. Guvenli Kurulum Yontemi

Hizli kurulum pratik ama script'i once okumak daha guvenlidir.

```bash
curl -fsSL -o /tmp/agent-router-install.sh https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh
less /tmp/agent-router-install.sh
bash /tmp/agent-router-install.sh
source ~/.zshrc
```

## 9. Sorun Giderme

Komut bulunamiyorsa:

```bash
source ~/.zshrc
```

Hala bulunamiyorsa:

```bash
ls -R ~/.agent-router
```

Router'i direkt calistirmak icin:

```bash
python3 ~/.agent-router/router.py "Admin login yetkisini düzelt"
```

Codex komutu yoksa `agent-codex` calismaz. Bu durumda `agent-route` veya
`agent-copy` kullan.

## Kisa Ozet

Ilk kurulum:

```bash
curl -fsSL https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh | bash
source ~/.zshrc
```

Projeye dahil etme:

```bash
cd /path/to/project
agent-router-init
```

Kullanma:

```bash
agent-codex "Görev metni"
```

Guncelleme:

```bash
curl -fsSL https://raw.githubusercontent.com/st-devl/Global_Router_codex/main/install.sh | bash
source ~/.zshrc
```

Kontrol:

```bash
agent-router-check
```
