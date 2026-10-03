import os

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _python_dosyalari():
    for klasor, _, dosyalar in os.walk(os.path.join(KOK, 'app')):
        for dosya in dosyalar:
            if dosya.endswith('.py'):
                yol = os.path.join(klasor, dosya)
                yield os.path.relpath(yol, KOK).replace(os.sep, '/'), open(yol, encoding='utf-8').read()


# sql sadece database.py de olmali
def test_sql_sadece_database_py_icinde():
    for yol, icerik in _python_dosyalari():
        if yol == 'app/database.py':
            continue
        for kelime in ('SELECT ', 'INSERT ', 'CREATE TABLE', 'sqlite3'):
            assert kelime not in icerik, f'{yol} içinde SQL bulundu: {kelime}'


# ai cagrisi sadece ai_service.py de olmali
def test_ai_cagrisi_sadece_ai_service_icinde():
    for yol, icerik in _python_dosyalari():
        if yol == 'app/services/ai_service.py':
            continue
        assert 'requests.post' not in icerik, f'{yol} içinde AI çağrısı bulundu'
        assert 'api.groq.com' not in icerik, f'{yol} içinde Groq adresi bulundu'


def test_env_gitignore_icinde():
    satirlar = open(os.path.join(KOK, '.gitignore'), encoding='utf-8').read().split()
    assert '.env' in satirlar
