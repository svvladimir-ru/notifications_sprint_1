import time
from logging import Logger

import backoff
from requests import ConnectionError

from config import ETLConfigs
from modules.manager import DBManager, RequestManager, DatabaseError
from modules.extractor import Extractor
from modules.transformer import Transformer
from modules.loader import Loader


class ETL:

    def __init__(self, db: DBManager, request: RequestManager, loader: Loader, logger: Logger):
        self.db = db
        self.request = request
        self.loader = loader
        self.logger = logger

    @backoff.on_exception(backoff.expo, DatabaseError, ConnectionError)
    def listener(self):
        if not self.db.check_connection():
            self.logger.info(f"Отсутствует соединение с PostgreSQL, подключение...")
            self.db.connect()
            raise DatabaseError

        if not self.request.ping():
            self.logger.info(f"Отсутствует соединение с сервисом Publisher, ожидание...")
            raise ConnectionError

        self.loader.run()

    def run(self):
        while True:
            self.listener()
            time.sleep(10)


if __name__ == '__main__':
    configs = ETLConfigs()
    db_manager = DBManager(configs=configs.postgres, queries=configs.queries, logger=configs.logger)
    request_manager = RequestManager(configs=configs.publisher, logger=configs.logger)
    extractor = Extractor(manager=db_manager, tables=configs.tables, logger=configs.logger)
    transformer = Transformer(extractor=extractor, logger=configs.logger)
    loader = Loader(
        transformer=transformer,
        request_manager=request_manager,
        logger=configs.logger
    )
    etl = ETL(db=db_manager, request=request_manager, loader=loader, logger=configs.logger)
    etl.run()
