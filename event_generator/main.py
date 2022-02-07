import time
from logging import Logger

import backoff
from psycopg2 import DatabaseError

from config import MainConfigs
from modules.manager import DBManager
from modules.generator import Generator
from modules.loader import Loader


class EventGenerator:

    def __init__(self, db: DBManager, loader: Loader, logger: Logger):
        self.db = db
        self.loader = loader
        self.logger = logger

    @backoff.on_exception(backoff.expo, DatabaseError)
    def listener(self):
        if not self.db.check_connection():
            self.logger.info(f"Отсутствует соединение с PostgreSQL, подключение...")
            self.db.connect()
            raise DatabaseError

        self.loader.load()
        time.sleep(60)

    def run(self):
        while True:
            self.listener()


if __name__ == '__main__':
    configs = MainConfigs()
    manager = DBManager(
        configs=configs.postgres,
        queries=configs.queries,
        logger=configs.logger
    )
    manager.connect()
    generator = Generator(
        manager=manager,
        template_table=configs.tables.templates,
        events=configs.events.events,
        logger=configs.logger
    )
    loader = Loader(
        manager=manager,
        generator=generator,
        event_table=configs.tables.others,
        logger=configs.logger
    )
    event_generator = EventGenerator(
        db=manager,
        loader=loader,
        logger=configs.logger
    )
    event_generator.run()



