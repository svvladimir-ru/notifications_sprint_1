import os
import logging
from pathlib import Path

from pydantic import BaseSettings

from models.models import Queries, Tables, EventsFileModel


# Инициализация пути к файлам
queries_file_path = Path('configs/queries.json')
tables_file_path = Path('configs/tables.json')
events_file_path = Path('configs/events.json')


# Настройка и инициализация логирования
def set_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')
    handler = logging.StreamHandler()
    log_format = '%(asctime)s | %(levelname)s --> %(message)s'
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class PostgresConfigs(BaseSettings):
    host: str = os.getenv('DB_HOST', 'localhost')
    port: int = os.getenv('DB_PORT', 5432)
    user: str = os.getenv('DB_USER', 'postgres')
    password: str = os.getenv('DB_PASSWORD', 'password')
    dbname: str = os.getenv('DB_NAME', 'movies')

    class Config:
        env_prefix = "DB_"


class MainConfigs(BaseSettings):
    postgres = PostgresConfigs()
    queries = Queries.parse_file(queries_file_path)
    tables = Tables.parse_file(tables_file_path)
    events = EventsFileModel.parse_file(events_file_path)
    logger = set_logger()
