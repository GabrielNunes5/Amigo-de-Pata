from ..database import db


class Animals(db.Model):
    __tablename__ = "animals"
    animal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal_name = db.Column(db.String(100), nullable=False)  # Todos
    animal_age = db.Column(db.String(50), nullable=False)  # Todos
    animal_weight = db.Column(db.Float, nullable=False)  # Todos
    animal_num_age = db.Column(db.String(100), nullable=False)  # Todos
    animal_sex = db.Column(db.String(10), nullable=False)  # Todos
    animal_color = db.Column(db.String(50))  # Gato e Cachorro
    animal_species = db.Column(db.String(50))  # Misc e Birds
    animal_vaccines = db.Column(db.String(255))  # Gato e cachorro
    animal_sized = db.Column(db.String(50))  # Cachorro
    animal_neutered = db.Column(db.Boolean)  # Gato e Cachorro
    animal_special_conditions = db.Column(
        db.String(255))  # Todos mas não obrigatorio
    animal_category = db.Column(db.String(100), nullable=False)  # Todos
    animal_image_url = db.Column(db.String(255), nullable=False)  # Todos
    animal_adopted = db.Column(db.Boolean, default=False)
    adopter_id = db.Column(db.Integer, db.ForeignKey(
        'adopter.adopter_id'))

    adopter = db.relationship('Adopter', backref='animals_adopted', lazy=True)

    def to_json(self):
        return {
            'animal_id': self.animal_id,
            'animal_name': self.animal_name,
            'animal_age': self.animal_age,
            'animal_weight': self.animal_weight,
            'animal_num_age': self.animal_num_age,
            'animal_sex': self.animal_sex,
            'animal_color': self.animal_color,
            'animal_species': self.animal_species,
            'animal_vaccines': self.animal_vaccines,
            'animal_sized': self.animal_sized,
            'animal_neutered': self.animal_neutered,
            'animal_special_conditions': self.animal_special_conditions,
            'animal_category': self.animal_category,
            'animal_image_url': self.animal_image_url,
            'animal_adopted': self.animal_adopted,
            'adopter_id': self.adopter_id,
            'adopter': self.adopter.adopter_full_name if
            self.adopter else None,
        }
