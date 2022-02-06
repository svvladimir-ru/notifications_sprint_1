from datetime import datetime
from uuid import uuid4
from hashlib import sha512
from sqlalchemy import Column, DateTime
from sqlalchemy import String, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID


from services.notification.broker_service.src.database.db import Base


class DateMixin:

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Template(DateMixin, Base):
    """Модель шаблонов."""

    __tablename__ = "templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    template = Column(Text)


class Welcome(DateMixin, Base):
    """Модель шаблонов."""

    __tablename__ = "welcome"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = Column("user_id", UUID(as_uuid=True), Base.ForeignKey("users.id"))
    template_id = Column("template_id", UUID(as_uuid=True), Base.ForeignKey("templates.id"))


class Others(DateMixin, Base):
    """Модель шаблонов."""

    __tablename__ = "others"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    template_id = Column("template_id", UUID(as_uuid=True), Base.ForeignKey("templates.id"))
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)


class User(DateMixin, Base):
    __tablename__ = "user"
    email = Column(Text, nullable=False)
    confirmed = Column(Boolean, nullable=False)
    mail_subscribe = Column(Boolean, nullable=False)

    __table_args__ = {"schema": "users"}
