from typing import Optional

from flask import Flask
from itsdangerous import URLSafeSerializer


class Serializer:

    key = None
    serializer = None

    def __init__(self, app: Optional[Flask] = None):
        if app:
            self.init_app(app=app)

    def init_app(self, app: Flask):
        self.key = app.config['SECRET_KEY']
        self.serializer = URLSafeSerializer(secret_key=self.key)

    def loads(self, token: str, salt: str) -> [dict, bool]:
        try:
            data = self.serializer.loads(token, salt=salt)
        except Exception:
            return False
        return data

    def dumps(self, data: dict, salt: str) -> str:
        return self.serializer.dumps(data, salt=salt)
