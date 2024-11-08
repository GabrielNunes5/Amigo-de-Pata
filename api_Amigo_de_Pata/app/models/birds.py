from ..database import db


class Birds(db.Model):
    bird_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bird_name = db.Column(db.String(100), nullable=False, unique=True)
    bird_age = db.Column(db.String(100), nullable=False)
    bird_num_age = db.Column(db.String(100), nullable=False)
    bird_specie = db.Column(db.String(50), nullable=False)
    bird_sex = db.Column(db.String(10), nullable=False)
    bird_special_conditions = db.Column(db.String(255), nullable=True)
    bird_image_url = db.Column(db.String(255), nullable=False)
    bird_adopted = db.Column(db.Boolean, default=False)
    adopter_id = db.Column(db.Integer, db.ForeignKey(
        'adopter.adopter_id'), nullable=True)

    adopter = db.relationship('Adopter', backref='birds_adopted', lazy=True)

    def to_json(self):
        return {
            'bird_name': self.bird_name,
            'bird_age': self.bird_age,
            'bird_num_age': self.bird_num_age,
            'bird_specie': self.bird_specie,
            'bird_sex': self.bird_sex,
            'bird_special_conditions': self.bird_special_conditions,
            'bird_image_url': self.bird_image_url,
            'bird_adopted': self.bird_adopted,
            'adopter_id': self.adopter_id,
            'adopter': self.adopter.adopter_full_name if
            self.adopter else None,

        }
