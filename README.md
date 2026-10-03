# Big Heart's Little Club – SmartLead AI

Big Heart's Little Club için yapay zekâ destekli veli asistanı ve müşteri adayı (lead) toplama sistemi. Big Heart's Little Club, 2-8 yaş çocukların İngilizce konuşmaya cesaret ettiği bir kulüptür: her çocuk psikolog ön görüşmesi ve gelişim haritasıyla başlar, velisiyle birlikte duygular temalı oyun gruplarına katılır. Veli karşılama sayfasında asistana sorularını sorar; adını, telefonunu, çocuğunun yaşını ve ilgilendiği hizmeti bırakınca kayıt yönetim panelinde görünür.

**Hazırlayan:** Nil Sena Gülabi

## Mimari

```
smartlead_ai/
├── run.py                  Sunucuyu başlatır
├── config.py               Ayarlar + BUSINESS_CONTEXT (.env okur)
├── requirements.txt
├── requirements-dev.txt    Test paketleri (pytest)
├── pytest.ini
├── .env.example            .env için örnek
├── .gitignore
├── app/
│   ├── __init__.py         create_app() fabrikası + /health
│   ├── database.py         SQL yalnızca burada
│   ├── routes.py           Sadece yönlendirme
│   ├── templates/
│   │   ├── index.html      Karşılama sayfası (Z-Pattern, glassmorphism)
│   │   └── dashboard.html  Yönetim paneli (F-Pattern)
│   └── services/
│       └── ai_service.py   Yapay zekâ çağrıları yalnızca burada
├── tests/                  Otomatik testler (pytest)
│   ├── conftest.py         Geçici veritabanı + demo modu hazırlığı
│   ├── test_api.py         Uç noktaların testleri
│   ├── test_ai_service.py  Yapay zekâ servisinin testleri (sahte istekle)
│   └── test_mimari.py      SQL/AI kodunun doğru dosyada olduğunun kontrolü
├── .github/workflows/
│   └── testler.yml         GitHub'da her push'ta testleri çalıştırır
└── wix/
    ├── karsilama_sayfasi.js  Wix Velo – karşılama sayfası kodu
    └── yonetim_paneli.js     Wix Velo – yönetim paneli kodu
```

## Kurulum (yerelde)

```bash
python -m venv venv
# Windows: venv\Scripts\activate     Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

`.env.example` dosyasını kopyalayıp adını `.env` yapın ve `GROQ_API_KEY` alanına console.groq.com'dan aldığınız anahtarı yazın. Anahtar yoksa asistan "demo modu" cevabı verir, sistemin geri kalanı yine çalışır.

```bash
python run.py
```

Tarayıcıda: `http://localhost:5000` (karşılama), `http://localhost:5000/dashboard` (panel), `http://localhost:5000/health` (canlılık).

## API uç noktaları

| Metod | Yol | Gövde / Cevap |
|---|---|---|
| GET | `/health` | `{basari, durum}` |
| POST | `/api/sohbet` | Gönder: `{mesaj, gecmis}` → Cevap: `{basari, cevap}` (hata: 400 / 503) |
| POST | `/api/leads` | Gönder: `{isim, telefon, mesaj, cocuk_yasi, hizmet}` → 201 `{basari, id}` (hata: 400) |
| GET | `/api/leads` | `{basari, leadler: [...], toplam}` |

## Test (Modül F)

```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/api/sohbet -H "Content-Type: application/json" -d "{\"mesaj\": \"Kızım 5 yaşında, grup dersleri nasıl?\"}"
curl -X POST http://localhost:5000/api/leads -H "Content-Type: application/json" -d "{\"isim\": \"Ayşe\", \"telefon\": \"05321112233\", \"cocuk_yasi\": \"5\", \"hizmet\": \"Kulüp üyeliği (online)\"}"
curl http://localhost:5000/api/leads
```

## Otomatik testler

```bash
pip install -r requirements-dev.txt
python -m pytest -v
```

18 test şunları kontrol eder: `/health` ve sayfaların açılması, sohbetin demo modunda çalışması, boş/bozuk isteklerde 400, yapay zekâ hatasında 503, lead kaydı (201) ve listeleme, eksik alan ve geçersiz telefonda 400, en yeniden eskiye sıralama, SQL Injection denemesinin zararsız kalması, yapay zekâya giden mesaj sırasının doğru olması (system → geçmiş → yeni mesaj) ve mimari sözleşme (SQL yalnızca `database.py`, AI çağrısı yalnızca `ai_service.py` içinde; `.env` `.gitignore`'da). Testler gerçek veritabanına ve gerçek yapay zekâya dokunmaz; geçici bir veritabanı ve sahte istekler kullanır.

GitHub'a yüklendiğinde `.github/workflows/testler.yml` sayesinde testler her push'ta otomatik çalışır; depo sayfasındaki yeşil tik testlerin geçtiğini gösterir.

## GitHub'a yükleme (adım adım)

1. github.com'da **New repository** → isim: `big-hearts-little-club` → **Public** → *Create repository*.
2. Proje klasöründe terminal açın:

```bash
git init
git add .
git commit -m "Big Heart's Little Club - SmartLead AI"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADINIZ/big-hearts-little-club.git
git push -u origin main
```

3. GitHub'da depoyu açıp **`.env` dosyasının listede OLMADIĞINI** kontrol edin (yalnızca `.env.example` görünmeli).
4. **Actions** sekmesinde "Testler" iş akışının yeşil tikle bittiğini görün.

## Wix bağlantısı (Modül G)

Karşılama sayfasındaki eleman ID'leri: `#mesajInput`, `#sorButton`, `#cevapText`, `#isimInput`, `#telefonInput`, `#yasInput` (Dropdown), `#hizmetInput` (Dropdown), `#kaydetButton`, `#durumText`.

Yönetim panelindeki eleman ID'leri: `#leadRepeater` (Repeater) ve içinde `#isimText`, `#telefonText`, `#yasText`, `#hizmetText`, `#mesajText`, `#tarihText`; sayfanın üstünde `#toplamText`.

Her iki `.js` dosyasındaki `API_URL` değerini Render adresinizle değiştirin.

## Yayınlama (Modül H – Render)

1. GitHub'da public bir depo açıp kodu push edin (`.env` yüklenmemeli).
2. Render → New → Web Service → depoyu bağlayın.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn run:app`
5. Environment Variables: `GROQ_API_KEY`, `SECRET_KEY`, `APP_ENV=production`, `CORS_ORIGINS` (Wix site adresiniz).
6. Render adresinizde `/health` "aktif" dönüyorsa yayın tamamdır.
