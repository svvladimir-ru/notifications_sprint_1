from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime
from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


from database.db import Base


class DateMixin:

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Template(DateMixin, Base):
    """Модель шаблонов."""

    __tablename__ = "templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    template = Column(Text)

    __table_args__ = {"schema": "events"}


class Welcome(DateMixin, Base):
    """Модель шаблонов."""

    __tablename__ = "welcome"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"))
    template_id = Column("template_id", UUID(as_uuid=True), ForeignKey("templates.id"))

    __table_args__ = {"schema": "events"}


class Others(DateMixin, Base):
    """Модель шаблонов."""

    __tablename__ = "others"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    template_id = Column("template_id", UUID(as_uuid=True), ForeignKey("templates.id"))
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    __table_args__ = {"schema": "events"}


class User(DateMixin, Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    email = Column(Text, nullable=False)
    confirmed = Column(Boolean, nullable=False)
    mail_subscribe = Column(Boolean, nullable=False)

    __table_args__ = {"schema": "users"}
