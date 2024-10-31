from flask import Flask
from app.config.settings import Config
from app.database import db
from app.routes.users import users_bp
from app.routes.adopter import adopters_bp
from app.routes.cats import cats_bp
from app.routes.dogs import dogs_bp
from app.routes.birds import birds_bp
from app.routes.misce import animals_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Registre os Blueprints após garantir que o banco foi inicializado
    app.register_blueprint(users_bp)
    app.register_blueprint(cats_bp)
    app.register_blueprint(dogs_bp)
    app.register_blueprint(birds_bp)
    app.register_blueprint(animals_bp)
    app.register_blueprint(adopters_bp)

    return app
