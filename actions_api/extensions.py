from flask_sqlalchemy import SQLAlchemy

from modules.security import Serializer


db = SQLAlchemy()
serializer = Serializer()


def session():
    return db.session()


