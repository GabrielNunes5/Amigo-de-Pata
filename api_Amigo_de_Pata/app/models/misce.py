from ..database import db


class Animals(db.Model):
    animal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal_name = db.Column(db.String(100), nullable=False, unique=True)
    animal_age = db.Column(db.String(100), nullable=False)
    animal_species = db.Column(db.String(50), nullable=False)
    animal_image_url = db.Column(db.String(255), nullable=False)
    animal_adopted = db.Column(db.Boolean, default=False)
    adopter_id = db.Column(db.Integer, db.ForeignKey(
        'adopter.adopter_id'), nullable=True)

    # Relacionamento para o adotante
    adopter = db.relationship('Adopter', backref='animals_adopted', lazy=True)

    def to_json(self):
        return {
            'cat_name': self.animal_name,
            'cat_age': self.animal_age,
            'cat_color': self.animal_color,
            'cat_image_url': self.animal_image_url,
            'cat_adopted': self.animal_adopted,
            'adopter_id': self.adopter_id,
            'adopter': self.adopter.adopter_full_name if self.adopter else None
        }
