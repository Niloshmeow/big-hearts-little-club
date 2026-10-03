from app.services.ai_service import ai_service, AIServiceError


def test_health_aktif_doner(client):
    yanit = client.get('/health')
    assert yanit.status_code == 200
    assert yanit.get_json()['durum'] == 'aktif'


def test_sayfalar_aciliyor(client):
    assert client.get('/').status_code == 200
    assert client.get('/dashboard').status_code == 200


def test_sohbet_demo_modunda_cevap_verir(client):
    yanit = client.post('/api/sohbet', json={'mesaj': 'Kızım 5 yaşında'})
    veri = yanit.get_json()
    assert yanit.status_code == 200
    assert veri['basari'] is True
    assert 'Demo modu' in veri['cevap']


def test_sohbet_bos_mesaj_400(client):
    assert client.post('/api/sohbet', json={'mesaj': '   '}).status_code == 400
    assert client.post('/api/sohbet', json={}).status_code == 400


def test_sohbet_json_olmayan_istek_400(client):
    yanit = client.post('/api/sohbet', data='bozuk veri', content_type='text/plain')
    assert yanit.status_code == 400


# ai hata verirse 503 donmeli
def test_sohbet_ai_hatasinda_503(client, monkeypatch):
    def hata_firlat(mesaj, gecmis=None):
        raise AIServiceError('test hatası')
    monkeypatch.setattr(ai_service, 'yanit_uret', hata_firlat)

    yanit = client.post('/api/sohbet', json={'mesaj': 'Merhaba'})
    assert yanit.status_code == 503
    assert yanit.get_json()['basari'] is False


def test_lead_kaydedilir_ve_listelenir(client):
    yanit = client.post('/api/leads', json={
        'isim': 'Ayşe Yılmaz', 'telefon': '0532 111 22 33',
        'cocuk_yasi': '5', 'hizmet': 'Kulüp üyeliği (online)'
    })
    assert yanit.status_code == 201

    liste = client.get('/api/leads').get_json()
    assert liste['basari'] is True
    assert liste['toplam'] == 1
    kayit = liste['leadler'][0]
    assert kayit['isim'] == 'Ayşe Yılmaz'
    assert kayit['cocuk_yasi'] == '5'
    assert kayit['_id'] == str(kayit['id'])


def test_lead_eksik_alan_400(client):
    assert client.post('/api/leads', json={'isim': 'Ayşe'}).status_code == 400
    assert client.post('/api/leads', json={'telefon': '05321112233'}).status_code == 400
    assert client.get('/api/leads').get_json()['toplam'] == 0


def test_lead_gecersiz_telefon_400(client):
    yanit = client.post('/api/leads', json={'isim': 'Ayşe', 'telefon': '12345'})
    assert yanit.status_code == 400


def test_leadler_en_yeniden_eskiye_siralanir(client):
    client.post('/api/leads', json={'isim': 'Birinci', 'telefon': '05321112233'})
    client.post('/api/leads', json={'isim': 'İkinci', 'telefon': '05321112244'})
    leadler = client.get('/api/leads').get_json()['leadler']
    assert [l['isim'] for l in leadler] == ['İkinci', 'Birinci']


# kotu niyetli isim tabloyu silmemeli
def test_sql_injection_denemesi_zararsizdir(client):
    kotu_isim = "x'); DROP TABLE leads; --"
    yanit = client.post('/api/leads', json={'isim': kotu_isim, 'telefon': '05321112233'})
    assert yanit.status_code == 201

    liste = client.get('/api/leads').get_json()
    assert liste['toplam'] == 1           # tablo silinmedi
    assert liste['leadler'][0]['isim'] == kotu_isim
