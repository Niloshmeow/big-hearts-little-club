import os
import sys

import pytest

# proje klasorunu import yoluna ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config
from app import create_app
from app.services.ai_service import ai_service


@pytest.fixture
def app(tmp_path, monkeypatch):
    # her test icin gecici veritabani
    monkeypatch.setattr(config['testing'], 'DATABASE_URL', str(tmp_path / 'test.db'))

    # testte gercek yapay zekaya istek atmasin
    monkeypatch.setattr(ai_service, 'api_key', '')

    uygulama = create_app('testing')
    yield uygulama


@pytest.fixture
def client(app):
    return app.test_client()
