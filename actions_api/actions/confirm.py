from flask import Blueprint, jsonify
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

from .router import Router
from extensions import serializer
from conteiner import ApplicationContainer
from modules.updater import Updater


api = Blueprint('confirm', __name__)
router = Router()


@api.route("/", methods=['GET'])
@router.verification(serializer=serializer, action='confirm')
@inject
def confirm(data: BaseModel, updater: Updater = Provide[ApplicationContainer.user_updater]):

    user_id = updater.check(email=data.email)

    if not user_id:
        router.abort(code_name="NOT_FOUND", message_name="USER_DOESNT_EXIST")

    current_data = updater.read(uuid=user_id)

    if current_data.confirmed:
        router.abort(code_name="BAD_REQUEST", message_name="EMAIL_IS_CONFIRMED")

    new_data = {
        "confirmed": True
    }

    status = updater.update(current_data=current_data, new_data=new_data)

    if not status:
        router.abort(code_name="BAD_REQUEST", message_name="ACTION_ERROR")

    return jsonify({
        "message": "Ваша почта подтверждена",
        "data": data.dict()
    })
