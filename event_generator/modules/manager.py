from logging import Logger
from typing import Any, Optional

from psycopg2 import DatabaseError, connect as db_connect
from psycopg2.extras import DictCursor
from pydantic import BaseModel

from models.models import TableModel, Queries
from config import PostgresConfigs


class DBManager:

    def __init__(self, configs: PostgresConfigs, queries: Queries, logger: Logger):
        self.configs = configs
        self.queries = queries
        self.logger = logger
        self.connection = None

    def connect(self) -> None:
        try:
            self.logger.info(f"Подключение к Postgres...")
            self.connection = db_connect(**self.configs.dict(), cursor_factory=DictCursor)
        except DatabaseError as e:
            self.connection = None
            self.logger.info(f"Error: {e}")

    def check_connection(self) -> bool:
        self.logger.info(f"Проверка подключения к Postgres...")
        try:
            if self.connection.closed == 0:
                return True
            return False
        except AttributeError:
            return False

    def set_query(self, method: str, **kwargs) -> str:
        query = getattr(self.queries, method)
        return query.format(**kwargs)

    def read(self, table: TableModel, field_value: Any, one: bool = False, attrs: Optional[list] = None):
        if self.check_connection():
            query = self.set_query(
                method='read',
                field_value=field_value,
                attrs=attrs,
                **table.dict(by_alias=True))
            cursor = self.connection.cursor()
            try:
                cursor.execute(query)
                if one:
                    result = cursor.fetchone()
                    yield result

                while result := cursor.fetchmany():
                    yield result
            except DatabaseError as e:
                self.logger.info(f"Error: {e}")
            finally:
                cursor.close()

    def create(self, table: TableModel, data: BaseModel) -> bool:
        query = self.set_query(method='create', **table.dict(by_alias=True), **data.for_create())
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            return True
        except DatabaseError as e:
            self.logger.info(f"Error: {e}")
            self.connection.close()
            self.connect()
            return False
        finally:
            cursor.close()
