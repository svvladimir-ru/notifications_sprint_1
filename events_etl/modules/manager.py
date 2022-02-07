import json
from logging import Logger
from typing import Any, Union

import requests
from psycopg2 import DatabaseError, connect as db_connect
from psycopg2.extras import DictCursor

from models.models import TableModel, QueriesModel, TableDataModel
from config import PostgresConfigs, PublisherConfigs


class DBManager:

    def __init__(self, configs: PostgresConfigs, queries: QueriesModel, logger: Logger):
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

    def set_query(self, method: str, table: TableModel, field_value: Any) -> str:
        query = getattr(self.queries, method)
        return query.return_format(field_value=field_value, **table.dict(by_alias=True))

    def read(self, table: TableModel, field_value: Any, one: bool = False):
        if self.check_connection():
            query = self.set_query(method='read', table=table, field_value=field_value)
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


class RequestManager:

    def __init__(self, configs: PublisherConfigs, logger: Logger):
        self.configs = configs
        self.logger = logger
        self.url = f"http://{self.configs.host}:{self.configs.port}{self.configs.interface}"

    def ping(self) -> bool:
        payload = {
            'action': 'ping'
        }
        status = self.send(data=payload)
        try:
            data = json.loads(status)
            if 'action' in data:
                pong = data['action']
                if pong == 'pong':
                    return True
        except Exception:
            return False

    def send(self, data: Union[TableDataModel, dict]):
        payload = data if type(data) is dict else data.post_payload()
        try:
            status = requests.post(url=self.url, json=payload)
            print(status.content)
            return status.content
        except Exception as e:
            self.logger.info(f"RequestManager Error: {e}")
