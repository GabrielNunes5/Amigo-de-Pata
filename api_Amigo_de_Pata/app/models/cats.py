from ..database import db
from app.models.users import Users


class Cats(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(100), nullable=False, unique=True)
    cat_age = db.Column(db.Integer, nullable=False)
    cat_color = db.Column(db.String(50), nullable=False)
    cat_image_url = db.Column(db.String(255), nullable=False)
    cat_adopted = db.Column(db.Boolean, default=False)
    # cat_adopter_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # # Relacionamento com o modelo User
    # adopter = db.relationship('User', backref='cats_adopted', lazy=True)

    def to_json(self):
        return {
            # 'cat_adopter_id': self.cat_adopter_id,
            # 'adopter': self.adopter.to_json() if self.adopter else None,
            'cat_name': self.cat_name,
            'cat_age': self.cat_age,
            'cat_color': self.cat_color,
            'cat_image_url': self.cat_image_url,
            'cat_adopted': self.cat_adopted
        }
