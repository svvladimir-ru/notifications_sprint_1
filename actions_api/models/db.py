import datetime

from sqlalchemy.dialects.postgresql import UUID

from extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True)


class User(BaseModel):
    __tablename__ = "user"

    email = db.Column(db.Text, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    mail_subscribe = db.Column(db.Boolean, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    __table_args__ = {"schema": "users"}
