from flask import Flask, url_for
from config import Config
from app.extensions import db, login_manager
from app.models import Usuario

# Blueprints
from app.painel import bp as painel_bp
from app.auth import bp as auth_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions
    db.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(painel_bp)

    @login_manager.user_loader
    def carregar_usuario(id_usuario):
        return Usuario.query.get(int(id_usuario))

    return app
