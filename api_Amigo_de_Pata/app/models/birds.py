from ..database import db


class Birds(db.Model):
    bird_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bird_name = db.Column(db.String(100), nullable=False, unique=True)
    bird_age = db.Column(db.String(100), nullable=False)
    bird_specie = db.Column(db.String(50), nullable=False)
    bird_image_url = db.Column(db.String(255), nullable=False)
    bird_adopted = db.Column(db.Boolean, default=False)
    adopter_id = db.Column(db.Integer, db.ForeignKey(
        'adopter.adopter_id'), nullable=True)

    # Relacionamento para o adotante
    adopter = db.relationship('Adopter', backref='birds_adopted', lazy=True)

    def to_json(self):
        return {
            'cat_name': self.bird_name,
            'cat_age': self.bird_age,
            'cat_color': self.bird_color,
            'cat_image_url': self.bird_image_url,
            'cat_adopted': self.bird_adopted,
            'adopter_id': self.adopter_id,
            'adopter': self.adopter.adopter_full_name if self.adopter else None
        }
