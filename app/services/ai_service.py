import requests
 
from config import Config
 
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'
 
 
class AIServiceError(Exception):
    pass
 
 
class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.AI_MODEL
        self.provider = Config.AI_PROVIDER
 
    def _sistem_talimati(self):
        return Config.BUSINESS_CONTEXT
 
    def _groq_istegi(self, mesajlar):
        basliklar = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        govde = {
            'model': self.model,
            'messages': mesajlar,
            'temperature': 0.7,
            'max_tokens': 1024,
        }
        # gpt-oss icin dusunme suresini kisa tut
        if 'gpt-oss' in self.model:
            govde['reasoning_effort'] = 'low'
 
        try:
            cevap = requests.post(GROQ_URL, headers=basliklar, json=govde, timeout=30)
            cevap.raise_for_status()
            veri = cevap.json()
            return veri['choices'][0]['message']['content'].strip()
        except requests.exceptions.Timeout:
            raise AIServiceError('Yapay zekâ servisi zamanında yanıt vermedi.')
        except requests.exceptions.RequestException as hata:
            raise AIServiceError(f'Yapay zekâ servisine ulaşılamadı: {hata}')
        except (KeyError, IndexError, ValueError):
            raise AIServiceError('Yapay zekâ servisinden beklenmeyen bir yanıt geldi.')
 
    def yanit_uret(self, mesaj, gecmis=None):
        if gecmis is None:
            gecmis = []
 
        # anahtar yoksa demo cevap don
        if not self.api_key:
            return ("(Demo modu) Hello! Ben Big Heart's Little Club veli asistanıyım. "
                    'Gerçek yanıtlar için .env dosyasına GROQ_API_KEY eklenmelidir. '
                    'Çocuğunuz kaç yaşında?')
 
        # sira: system -> gecmis -> yeni mesaj
        mesajlar = [{'role': 'system', 'content': self._sistem_talimati()}]
 
        for kayit in gecmis[-10:]:
            if isinstance(kayit, dict) and kayit.get('role') in ('user', 'assistant'):
                mesajlar.append({'role': kayit['role'], 'content': str(kayit.get('content', ''))})
 
        mesajlar.append({'role': 'user', 'content': mesaj})
 
        if self.provider == 'groq':
            return self._groq_istegi(mesajlar)
        raise AIServiceError(f'Desteklenmeyen yapay zekâ sağlayıcısı: {self.provider}')
 
 
# tek ornek
ai_service = AIService()
 
