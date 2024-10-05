import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        'mysql+mysqlconnector://root:@localhost/amigo_de_pata'
    )