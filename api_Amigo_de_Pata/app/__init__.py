from flask import Flask
from flask_cors import CORS
from app.config.settings import Config
from app.database import db
from app.routes.users import users_bp
from app.routes.adopter import adopters_bp
from app.routes.animals import animals_bp


def create_app():
    app = Flask(__name__)

    # Carregar as configurações básicas do arquivo Config
    app.config.from_object(Config)

    # Ativar CORS
    CORS(app)

    # Inicializar o banco de dados com a aplicação
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Registrar os Blueprints após garantir que o banco foi inicializado
    app.register_blueprint(users_bp)
    app.register_blueprint(animals_bp)
    app.register_blueprint(adopters_bp)

    return app
