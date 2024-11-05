import os
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        f'mysql+mysqlconnector://{DB_USER}:{
            DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )


print(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
