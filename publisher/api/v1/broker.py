from http import HTTPStatus

from fastapi import APIRouter, Request
from service.rabbit_service import RQWorker
from core import settings

router = APIRouter()


@router.post('/events')
async def on_massage(info: Request):
    data = await info.json()

    if 'action' in data:
        return {"action": "pong"}

    RQWorker(pk=data['record_id'], routing=data['table_name']).on_massage()
    return HTTPStatus.OK
