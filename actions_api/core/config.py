import os
from logging import config as logging_config

from .logger import LOGGING

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class BaseConf:
    # Пользовательские переменные
    DB_DRIVER = os.environ.get('DB_DRIVER', 'postgresql+psycopg2')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', 5432)
    DB_NAME = os.environ.get('DB_NAME', 'movies')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

    # Переменные окружения Flask и SQLAlchemy

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SECRET_KEY = os.environ.get('SECRET_KEY', 'ggTTEsxXFFSSSsFFFXX')


class Development(BaseConf):
    DEBUG = True
    DEVELOPMENT = True


class Production(BaseConf):
    DEBUG = False
