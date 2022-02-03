from flask import Blueprint, jsonify
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

from .router import Router
from extensions import serializer
from conteiner import ApplicationContainer
from modules.updater import Updater


api = Blueprint('unsubscribe', __name__)
router = Router()


@api.route("/", methods=['GET'])
@router.verification(serializer=serializer, action='unsubscribe')
@inject
def unsubscribe(data: BaseModel, updater: Updater = Provide[ApplicationContainer.user_updater]):

    user_id = updater.check(email=data.email)

    if not user_id:
        router.abort(code_name="NOT_FOUND", message_name="USER_DOESNT_EXIST")

    current_data = updater.read(uuid=user_id)

    if not current_data.mail_subscribe:
        router.abort(code_name="BAD_REQUEST", message_name="EMAIL_IS_UNSUBSCRIBED")

    new_data = {
        "mail_subscribe": False
    }

    status = updater.update(current_data=current_data, new_data=new_data)

    if not status:
        router.abort(code_name="BAD_REQUEST", message_name="ADD_DATA_ERROR")

    return jsonify({
        "message": "Вы отписаны от рассылок",
        "data": data.dict(),
    })
