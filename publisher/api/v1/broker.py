import pika
from http import HTTPStatus

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from service.rabbit_service import RQWorker
from database.rabbit import get_rabbit
from database.postgres import get_db
from core import settings


router = APIRouter()


@router.post('/events')
async def on_massage(info: Request,
                     db: Session = Depends(get_db),
                     connection: pika.BlockingConnection(
                         pika.ConnectionParameters(settings.RABBIT.HOST)) = Depends(get_rabbit)
                     ):
    data = await info.json()

    if 'action' in data:
        return {"action": "pong"}

    RQWorker(pk=data['record_id'],
             db=db,
             routing=data['table_name'],
             connection=connection).on_massage()

    return HTTPStatus.OK
