from logging import Logger

from .manager import DBManager
from models.models import Tables


class Extractor:

    def __init__(
            self,
            manager: DBManager,
            tables: Tables,
            logger: Logger
    ):
        self.manager = manager
        self.tables = tables
        self.logger = logger

    def get_events(self):
        for event in self.manager.read(
            table=self.tables.events,
            field_value=False
        ):
            if event:
                self.logger.info(
                    f"Обнаружено новое событие: {event[0]['table_name']}"
                )
                yield event[0]

    def run(self):
        for event in self.get_events():
            yield event
