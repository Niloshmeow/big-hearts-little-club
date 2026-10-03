import sqlite3

from flask import current_app


def get_db():
    baglanti = sqlite3.connect(current_app.config['DATABASE_URL'])

    baglanti.row_factory = sqlite3.Row
    return baglanti


def init_db(app):
    with app.app_context():
        baglanti = get_db()
        try:
            # leads tablosu (cocuk_yasi ve hizmet bizim ek sutunlarimiz)
            baglanti.execute('''
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isim TEXT NOT NULL,
                    telefon TEXT NOT NULL,
                    mesaj TEXT,
                    cocuk_yasi TEXT,
                    hizmet TEXT,
                    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            baglanti.commit()
        finally:
            baglanti.close()


def lead_ekle(isim, telefon, mesaj='', cocuk_yasi='', hizmet=''):
    baglanti = get_db()
    try:
        # sql injection olmasin diye ? kullaniyorum
        imlec = baglanti.execute(
            'INSERT INTO leads (isim, telefon, mesaj, cocuk_yasi, hizmet) VALUES (?, ?, ?, ?, ?)',
            (isim, telefon, mesaj, cocuk_yasi, hizmet)
        )
        baglanti.commit()
        return imlec.lastrowid
    finally:
        baglanti.close()


def tum_leadler():
    baglanti = get_db()
    try:
        satirlar = baglanti.execute(
            'SELECT id, isim, telefon, mesaj, cocuk_yasi, hizmet, tarih FROM leads ORDER BY id DESC'
        ).fetchall()

        leadler = []
        for satir in satirlar:
            kayit = dict(satir)
            # wix repeater _id istiyor
            kayit['_id'] = str(kayit['id'])
            leadler.append(kayit)
        return leadler
    finally:
        baglanti.close()
