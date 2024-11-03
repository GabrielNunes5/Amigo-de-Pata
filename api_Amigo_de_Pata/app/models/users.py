from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    user_is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """Gera o hash da senha."""
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash."""
        return check_password_hash(self.user_password, password)

    def to_json(self):
        return {
            'user_name': self.user_name,
            'user_age': self.user_age,
            'is_admin': self.user_is_admin,
        }
