from flask import Blueprint, jsonify, request, render_template

from app.database import lead_ekle, tum_leadler

from app.services.ai_service import ai_service, AIServiceError


# sayfalar ve api icin iki ayri blueprint
sayfa_bp = Blueprint('sayfalar', __name__)
api_bp = Blueprint('api', __name__)


@sayfa_bp.route('/', methods=['GET'])
def karsilama():
    return render_template('index.html')


@sayfa_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    veri = request.get_json(silent=True) or {}

    mesaj = str(veri.get('mesaj', '')).strip()
    gecmis = veri.get('gecmis', [])

    if not mesaj:
        return jsonify({'basari': False, 'hata': 'Lütfen bir mesaj yazın.'}), 400

    if not isinstance(gecmis, list):
        gecmis = []

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({'basari': True, 'cevap': cevap}), 200
    except AIServiceError as hata:
        print(f'[AI HATASI] {hata}')
        return jsonify({'basari': False,
                        'hata': 'Asistanımız şu an yanıt veremiyor. Lütfen biraz sonra tekrar deneyin.'}), 503


@api_bp.route('/leads', methods=['POST'])
def lead_kaydet():
    veri = request.get_json(silent=True) or {}

    isim = str(veri.get('isim', '')).strip()
    telefon = str(veri.get('telefon', '')).strip()
    mesaj = str(veri.get('mesaj', '')).strip()
    cocuk_yasi = str(veri.get('cocuk_yasi', '')).strip()
    hizmet = str(veri.get('hizmet', '')).strip()

    # isim ve telefon zorunlu
    if not isim or not telefon:
        return jsonify({'basari': False, 'hata': 'İsim ve telefon alanları zorunludur.'}), 400

    # telefonda en az 10 rakam olmali
    rakam_sayisi = sum(1 for karakter in telefon if karakter.isdigit())
    if rakam_sayisi < 10:
        return jsonify({'basari': False, 'hata': 'Lütfen geçerli bir telefon numarası girin.'}), 400

    try:
        yeni_id = lead_ekle(isim, telefon, mesaj, cocuk_yasi, hizmet)
        return jsonify({'basari': True, 'id': yeni_id,
                        'mesaj': 'Bilgileriniz alındı, danışmanımız en kısa sürede sizi arayacak.'}), 201
    except Exception as hata:
        print(f'[VERİTABANI HATASI] {hata}')
        return jsonify({'basari': False, 'hata': 'Kayıt sırasında bir sorun oluştu.'}), 500


@api_bp.route('/leads', methods=['GET'])
def lead_listele():
    try:
        leadler = tum_leadler()
        return jsonify({'basari': True, 'leadler': leadler, 'toplam': len(leadler)}), 200
    except Exception as hata:
        print(f'[VERİTABANI HATASI] {hata}')
        return jsonify({'basari': False, 'hata': 'Kayıtlar getirilemedi.'}), 500
