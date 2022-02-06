from logging import Logger

from .manager import DBManager
from .generator import Generator
from models.models import TableModel


class Loader:
    def __init__(self, manager: DBManager, generator: Generator, event_table: TableModel, logger: Logger):
        self.manager = manager
        self.generator = generator
        self.event_table = event_table
        self.logger = logger

    def load(self):
        event = self.generator.get_event()
        status = self.manager.create(table=self.event_table, data=event)
        if status:
            self.logger.info(f"Загрузил новое событие: {event.dict()}")
