from ..database import db


class Dogs(db.Model):
    dog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_name = db.Column(db.String(100), nullable=False, unique=True)
    dog_age = db.Column(db.Integer, nullable=False)
    dog_color = db.Column(db.String(50), nullable=False)
    dog_image_url = db.Column(db.String(255), nullable=False)
    dog_adopted = db.Column(db.Boolean, default=False)
    # dog_adopter_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # # Relacionamento com o modelo User
    # adopter = db.relationship('User', backref='dogs_adopted', lazy=True)

    def to_json(self):
        return {
            # 'dog_adopter_id': self.dog_adopter_id,
            # 'adopter': self.adopter.to_json() if self.adopter else None,
            'dog_name': self.dog_name,
            'dog_age': self.dog_age,
            'dog_color': self.dog_color,
            'dog_image_url': self.dog_image_url,
            'dog_adopted': self.dog_adopted
        }
