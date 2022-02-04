from logging import Logger

from pydantic import ValidationError

from .extractor import Extractor
from models.models import Events


class Transformer:

    def __init__(self, extractor: Extractor, logger: Logger):
        self.extractor = extractor
        self.logger = logger

    def run(self):
        for event in self.extractor.run():
            try:
                validated_event = Events.parse_obj(event)
                yield validated_event
            except ValidationError as e:
                self.logger.info(f"Error: {e}")
