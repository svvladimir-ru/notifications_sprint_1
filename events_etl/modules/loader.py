from logging import Logger

from .transformer import Transformer
from .manager import RequestManager


class Loader:

    def __init__(
            self,
            transformer: Transformer,
            request_manager: RequestManager,
            logger: Logger
    ):
        self.transformer = transformer
        self.request_manager = request_manager
        self.logger = logger

    def run(self):
        for event in self.transformer.run():
            self.request_manager.send(
                data=event,
                exclude={'id', 'created_at', 'processed'}
            )

