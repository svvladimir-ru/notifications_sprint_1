import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


# Основные модели
class MainTimeStampedMixin:
    created_at = models.DateTimeField()

    class Meta:
        abstract = True


class TimeStampMixin(MainTimeStampedMixin):
    updated_at = models.DateTimeField()

    class Meta:
        abstract = True


# Модели для пользователей
class Role(TimeStampMixin, models.Model):
    id = models.UUIDField(_('ID'), primary_key=True, auto_created=True, default=uuid.uuid4)
    name = models.CharField(_('Name'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('role')
        db_table = "users\".\"role"

    def __str__(self):
        return self.name


class UserRole(MainTimeStampedMixin, models.Model):
    id = models.UUIDField(_('ID'), primary_key=True, auto_created=True, default=uuid.uuid4)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    class Meta:
        db_table = 'users\".\"user_role'
        constraints = [
            models.UniqueConstraint(fields=('user', 'role'), name='user_role_id_unique')
        ]


class User(TimeStampMixin, models.Model):
    id = models.UUIDField(_('ID'), primary_key=True, auto_created=True, default=uuid.uuid4)
    login = models.CharField(_('Login'), max_length=128, unique=True)
    email = models.EmailField(_('Email'), unique=True)
    password = models.CharField(_('Password'), max_length=128)
    confirmed = models.BooleanField(_('Confirmed'), default=False)
    mail_subscribe = models.BooleanField(_('Subscribe'), default=True)

    role = models.ManyToManyField(Role, through='UserRole')

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('user')
        db_table = "users\".\"user"


# Модели для событий
class Templates(TimeStampMixin, models.Model):
    id = models.UUIDField(_('ID'), primary_key=True, auto_created=True, default=uuid.uuid4)
    name = models.CharField(_('Name'), max_length=50, unique=True)
    template = models.TextField(_('Template'))

    class Meta:
        verbose_name = _('templates')
        verbose_name_plural = _('templates')
        db_table = "events\".\"templates"

    def __str__(self):
        return self.name


class Others(MainTimeStampedMixin, models.Model):
    id = models.UUIDField(_('ID'), primary_key=True, auto_created=True, default=uuid.uuid4)
    template = models.ForeignKey('Templates', on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=50)
    description = models.TextField(_('Description'))

    class Meta:
        verbose_name = _('others')
        verbose_name_plural = _('others')
        db_table = "events\".\"others"
