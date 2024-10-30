import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        'mysql+mysqlconnector://sql10740983:LePl8j1pfl@sql10.freesqldatabase.com:3306/sql10740983'
    )