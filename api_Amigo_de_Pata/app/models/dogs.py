from ..database import db


class Dogs(db.Model):
    dog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_name = db.Column(db.String(100), nullable=False, unique=True)
    dog_age = db.Column(db.Integer, nullable=False)
    dog_color = db.Column(db.String(50), nullable=False)
    dog_image_url = db.Column(db.String(255), nullable=False)
    dog_adopted = db.Column(db.Boolean, default=False)

    # Relacionamento com o modelo User (com nome do backref alterado)
    adopter_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    adopter = db.relationship('Users', backref='dogs_adopted')

    def to_json(self):
        return {
            'dog_name': self.dog_name,
            'dog_age': self.dog_age,
            'dog_color': self.dog_color,
            'dog_image_url': self.dog_image_url,
            'dog_adopted': self.dog_adopted,
            'adopter_id': self.adopter_id
        }
