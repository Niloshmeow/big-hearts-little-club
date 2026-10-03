import pytest
import requests

from app.services import ai_service as modul
from app.services.ai_service import AIService, AIServiceError


# groq cevabi gibi davranan sahte nesne
class SahteCevap:
    def raise_for_status(self):
        pass

    def json(self):
        return {'choices': [{'message': {'content': ' Merhaba veli! '}}]}


# system -> gecmis -> yeni mesaj sirasi
def test_mesaj_sirasi_dogru(monkeypatch):
    gonderilen = {}

    def sahte_post(url, headers=None, json=None, timeout=None):
        gonderilen['govde'] = json
        return SahteCevap()

    monkeypatch.setattr(modul.requests, 'post', sahte_post)
    servis = AIService()
    servis.api_key = 'gsk_test'

    gecmis = [{'role': 'user', 'content': 'Merhaba'},
              {'role': 'assistant', 'content': 'Hello!'}]
    cevap = servis.yanit_uret('Kızım 4 yaşında', gecmis)

    roller = [m['role'] for m in gonderilen['govde']['messages']]
    assert roller == ['system', 'user', 'assistant', 'user']
    assert gonderilen['govde']['messages'][-1]['content'] == 'Kızım 4 yaşında'
    assert cevap == 'Merhaba veli!'   # strip() ile boşluklar temizlendi


def test_bozuk_gecmis_yok_sayilir(monkeypatch):
    gonderilen = {}

    def sahte_post(url, headers=None, json=None, timeout=None):
        gonderilen['govde'] = json
        return SahteCevap()

    monkeypatch.setattr(modul.requests, 'post', sahte_post)
    servis = AIService()
    servis.api_key = 'gsk_test'
    servis.yanit_uret('Merhaba', [{'role': 'hacker', 'content': 'x'}, 'bozuk'])

    roller = [m['role'] for m in gonderilen['govde']['messages']]
    assert roller == ['system', 'user']


def test_baglanti_hatasi_aiserviceerror_olur(monkeypatch):
    def hatali_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError('bağlantı yok')

    monkeypatch.setattr(modul.requests, 'post', hatali_post)
    servis = AIService()
    servis.api_key = 'gsk_test'
    with pytest.raises(AIServiceError):
        servis.yanit_uret('Merhaba')


def test_anahtar_yoksa_demo_modu():
    servis = AIService()
    servis.api_key = ''
    assert 'Demo modu' in servis.yanit_uret('Merhaba')
