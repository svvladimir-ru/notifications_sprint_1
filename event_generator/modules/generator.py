import random
from logging import Logger

import backoff

from .manager import DBManager, DatabaseError
from models.models import EventModel, TableModel, Event


class Generator:

    template_id = None

    def __init__(self, manager: DBManager, template_table: TableModel, events: list[EventModel], logger: Logger):
        self.manager = manager
        self.events = events
        self.template_table = template_table
        self.logger = logger
        self.get_template_id()

    @backoff.on_exception(backoff.expo, DatabaseError)
    def get_template_id(self):
        try:
            result = self.manager.read(table=self.template_table, field_value="'event'", attrs=['filter'], one=True)
            for id in result:
                self.template_id = id[0]
        except TypeError:
            self.logger.info("Error: Не обнаружено необходимого шаблона! Создайте шаблоны event и welcome")
            raise DatabaseError

    def get_event(self):
        event = random.choice(self.events)
        return Event(
            template_id=self.template_id,
            **event.dict()
        )



