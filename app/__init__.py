from flask import Flask, jsonify
from flask_cors import CORS

from config import config
from app.database import init_db


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))
    app.json.ensure_ascii = False

    # wix ten gelen istekler icin cors
    CORS(app, resources={r'/api/*': {'origins': app.config['CORS_ORIGINS']}})

    with app.app_context():
        init_db(app)

    from app.routes import sayfa_bp, api_bp
    app.register_blueprint(sayfa_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # render canlilik kontrolu
    @app.route('/health')
    def health():
        return jsonify({'basari': True, 'durum': 'aktif', 'servis': "Big Heart's Little Club - SmartLead AI"})

    return app
