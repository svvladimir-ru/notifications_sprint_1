from http import HTTPStatus

from fastapi import APIRouter, Request
from services.notification.broker_service.src.service.rabbit_service import RQWorker
from services.notification.broker_service.src.core import settings

router = APIRouter()


@router.post('/massage')
async def on_massage(pk: Request, routing: Request = settings.RABBIT.ROUTING):
    RQWorker(pk=str(await pk.json()), routing=str(await routing.json())).on_massage()

    return HTTPStatus.OK
