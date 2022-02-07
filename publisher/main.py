import uvicorn as uvicorn
import sentry_sdk
import pika

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api.v1 import broker
from core import settings
from database import database

from database import rabbit, db
from database.db import SessionLocal, engine


database.Base.metadata.create_all(bind=engine)


app = FastAPI(title=settings.PROJECT_NAME,
              description='Сервиса Брокер RabbitMQ',
              docs_url='/api/openapi',
              openapi_url='/api/openapi.json',
              default_response_class=ORJSONResponse)


sentry_sdk.init(dsn=settings.SENTRY_DSN)
SentryAsgiMiddleware(app)


@app.on_event('startup')
async def startup():
    rabbit.rq = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBIT.HOST))
    rabbit.rq.channel().queue_declare('welcome')
    rabbit.rq.channel().queue_declare('other')


@app.on_event('shutdown')
async def shutdown():
    await rabbit.rq.close()
    db.get_db().close()


app.include_router(broker.router, prefix='/api/v1/broker', tags=['broker'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, debug=True)
