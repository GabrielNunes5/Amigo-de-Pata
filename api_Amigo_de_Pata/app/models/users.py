from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_password = db.Column(db.String(128), nullable=False)  # Hash da senha
    user_endereco = db.Column(db.String(200), nullable=False)
    user_is_admin = db.Column(db.Boolean, default=False)

    # adopted_cats = db.relationship('Cats', backref='cat_adopter', lazy=True)
    # adopted_dogs = db.relationship('Dogs', backref='dog_adopter', lazy=True)

    def set_password(self, password):
        """Gera o hash da senha."""
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash."""
        return check_password_hash(self.user_password, password)

    def to_json(self):
        return {
            'user_name': self.user_name,
            'user_endereco': self.user_endereco,
            'is_admin': self.user_is_admin,
            # 'adopted_cats': [animal.to_json() for animal in self.adopted_cats],
            # 'adopted_dogs': [animal.to_json() for animal in self.adopted_dogs]
        }
