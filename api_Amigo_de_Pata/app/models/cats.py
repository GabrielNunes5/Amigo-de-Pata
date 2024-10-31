from ..database import db


class Cats(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(100), nullable=False, unique=True)
    cat_age = db.Column(db.String(100), nullable=False)
    cat_color = db.Column(db.String(50), nullable=False)
    cat_image_url = db.Column(db.String(255), nullable=False)
    cat_adopted = db.Column(db.Boolean, default=False)
    adopter_id = db.Column(db.Integer, db.ForeignKey(
        'adopter.adopter_id'), nullable=True)

    # Relacionamento para o adotante
    adopter = db.relationship('Adopter', backref='cats_adopted', lazy=True)

    def to_json(self):
        return {
            'cat_name': self.cat_name,
            'cat_age': self.cat_age,
            'cat_color': self.cat_color,
            'cat_image_url': self.cat_image_url,
            'cat_adopted': self.cat_adopted,
            'adopter_id': self.adopter_id,
            'adopter': self.adopter.adopter_full_name if self.adopter else None
        }
