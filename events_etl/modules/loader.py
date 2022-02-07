from logging import Logger

from .transformer import Transformer
from .manager import RequestManager, DBManager, TableModel


class Loader:

    def __init__(
            self,
            event_table: TableModel,
            transformer: Transformer,
            request_manager: RequestManager,
            db_manager: DBManager,
            logger: Logger
    ):
        self.event_table = event_table
        self.transformer = transformer
        self.request_manager = request_manager
        self.db_manager = db_manager
        self.logger = logger

    def run(self):
        for event in self.transformer.run():
            status = self.request_manager.send(data=event)
            if status == b'200':
                self.db_manager.update(table=self.event_table, field_value=True, uuid=event.id)


