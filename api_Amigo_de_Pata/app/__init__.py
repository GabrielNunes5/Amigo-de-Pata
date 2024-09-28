from flask import Flask
from app.config.settings import Config
from app.database import db
from app.routes.users import users_bp
from app.routes.cats import cats_bp
from app.routes.dogs import dogs_bp

# Importe explicitamente todos os modelos
from app.models.users import Users
from app.models.cats import Cats
from app.models.dogs import Dogs


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Registre os Blueprints após garantir que o banco foi inicializado
    app.register_blueprint(users_bp)
    app.register_blueprint(cats_bp)
    app.register_blueprint(dogs_bp)

    return app
