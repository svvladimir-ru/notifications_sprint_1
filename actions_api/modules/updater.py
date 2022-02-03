import datetime
from uuid import UUID
from logging import Logger
from typing import Union

from flask_sqlalchemy import SessionBase

from models.db import BaseModel, User


class Updater:
    table_model: BaseModel = None

    def __init__(self, session: SessionBase, logger: Logger):
        self.session = session
        self.logger = logger

    def check(self, **kwargs) -> Union[str, UUID]:
        uuid = self.session.query(self.table_model.id).filter_by(**kwargs).first()
        return uuid[0] if uuid else None

    def read(self, uuid: Union[str, UUID]):
        try:
            data = self.session.query(self.table_model).get(uuid)
            return data if data else None
        except Exception as e:
            self.logger.info(f"Error: {e}")
            return None

    def update(self, current_data: BaseModel, new_data: dict) -> bool:
        try:
            for key in new_data:
                setattr(current_data, key, new_data[key])

            current_data.updated_at = datetime.datetime.now()
            self.session.add(current_data)
            self.session.commit()
            return True
        except Exception as e:
            self.logger.info(f"Error: {e}")
            return False


class UserUpdater(Updater):
    table_model = User
