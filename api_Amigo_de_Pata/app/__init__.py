from flask import Flask
from flask_cors import CORS
import os

from app.config.settings import Config
from app.database import db
from app.routes.users import users_bp
from app.routes.adopter import adopters_bp
from app.routes.cats import cats_bp
from app.routes.dogs import dogs_bp
from app.routes.birds import birds_bp
from app.routes.misce import animals_bp


# Definir a URI do banco de dados usando as variáveis de ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


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
    app.register_blueprint(cats_bp)
    app.register_blueprint(dogs_bp)
    app.register_blueprint(birds_bp)
    app.register_blueprint(animals_bp)
    app.register_blueprint(adopters_bp)

    return app
