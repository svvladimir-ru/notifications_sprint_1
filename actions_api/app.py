import os

from flask import Flask
from gevent import monkey
from gevent.pywsgi import WSGIServer

from actions import confirm, unsubscribe, test
from conteiner import ApplicationContainer
from extensions import serializer, db


monkey.patch_all()


def reg_routes(app: Flask):
    # Роуты
    app.register_blueprint(confirm.api, url_prefix="/actions/confirm")
    app.register_blueprint(unsubscribe.api, url_prefix="/actions/unsubscribe")
    app.register_blueprint(test.api, url_prefix="/actions/test")


def init_extensions(app: Flask):
    db.init_app(app=app)
    serializer.init_app(app=app)


def create_app() -> Flask:
    # Инициализация Flask
    app = Flask(__name__)
    # Получение настроек
    app.config.from_object(f"core.config.{os.environ.get('FLASK_ENV', 'Development')}")
    # Подключение контейнера
    container = ApplicationContainer()
    app.container = container
    # Инициализация расширений
    init_extensions(app)
    # Регистрация blueprint
    reg_routes(app)

    return app


if __name__ == '__main__':
    app = create_app()

    http_server = WSGIServer((os.environ.get('APP_HOST', 'localhost'),
                              int(os.environ.get('APP_PORT', 8000))),
                             app)
    http_server.serve_forever()
