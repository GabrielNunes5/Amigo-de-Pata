from ..database import db


class Adopter(db.Model):
    adopter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adopter_full_name = db.Column(db.String(100), nullable=False)
    adopter_age = db.Column(db.Integer, nullable=False)
    adopter_email = db.Column(db.String(100), unique=True, nullable=False)
    adopter_phone = db.Column(db.String(20), unique=True, nullable=False)
    adopter_address = db.Column(db.String(200), nullable=False)
    adopter_residence_type = db.Column(db.String(50), nullable=False)
    adopter_has_garden = db.Column(db.Boolean, default=False)
    adopter_other_pets = db.Column(db.String(100), nullable=True)
    adopter_pet_type = db.Column(db.String(100), nullable=False)
    adopter_pet_preference = db.Column(db.String(100), nullable=True)
    adopter_occupation = db.Column(db.String(100), nullable=False)
    adopter_work_hours = db.Column(db.String(50), nullable=False)
    adopter_income = db.Column(db.Float, nullable=False)
    adopter_adoption_reason = db.Column(db.Text, nullable=False)
    adopter_commitment_to_care = db.Column(db.Text, nullable=False)
    adopter_experience_with_pets = db.Column(db.Text, nullable=True)
    adopter_additional_info = db.Column(db.Text, nullable=True)

    # Relacionamento com gatos, cachorros, passaros ou outros
    adopted_cats = db.relationship('Cats', backref='cat_adopter', lazy=True)
    adopted_dogs = db.relationship('Dogs', backref='dog_adopter', lazy=True)
    adopted_birds = db.relationship('Birds', backref='bird_adopter', lazy=True)
    adopted_animals = db.relationship(
        'Animals', backref='animal_adopter', lazy=True)

    def to_json(self):
        return {
            "adopter_full_name": self.adopter_full_name,
            "adopter_age": self.adopter_age,
            "adopter_email": self.adopter_email,
            "adopter_phone": self.adopter_phone,
            "adopter_address": self.adopter_address,
            "adopter_residence_type": self.adopter_residence_type,
            "adopter_has_garden": self.adopter_has_garden,
            "adopter_other_pets": self.adopter_other_pets,
            "adopter_pet_type": self.adopter_pet_type,
            "adopter_pet_preference": self.adopter_pet_preference,
            "adopter_occupation": self.adopter_occupation,
            "adopter_work_hours": self.adopter_work_hours,
            "adopter_income": self.adopter_income,
            "adopter_adoption_reason": self.adopter_adoption_reason,
            "adopter_commitment_to_care": self.adopter_commitment_to_care,
            "adopter_experience_with_pets": self.adopter_experience_with_pets,
            "adopter_additional_info": self.adopter_additional_info,
            'adopted_cats': [cat.to_json() for cat in self.adopted_cats],
            'adopted_dogs': [dog.to_json() for dog in self.adopted_dogs],
            'adopted_birds': [bird.to_json() for bird in self.adopted_birds],
            'adopted_animals': [
                animal.to_json() for animal in self.adopted_animals]
        }
