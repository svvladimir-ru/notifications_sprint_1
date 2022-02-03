from http import HTTPStatus

from flask import abort, jsonify, make_response, request
from pydantic import ValidationError

from models.enum import APIMessage
from models.action import ActionModel
from modules.security import Serializer


class Router:

    def verification(self, serializer: Serializer, action: str):
        def decorator(func):
            def wrapper(**kwargs):
                token = request.args['token']
                data = serializer.loads(token=token, salt=action)

                if not data:
                    self.abort(code_name='BAD_REQUEST', message_name='BAD_REQUEST')

                try:
                    pars_data = ActionModel.parse_obj(data)
                    return func(data=pars_data, **kwargs)
                except ValidationError:
                    self.abort(code_name='BAD_REQUEST', message_name='BAD_REQUEST')

            return wrapper
        return decorator

    @staticmethod
    def abort(code_name: str, message_name: str):
        error_code = getattr(HTTPStatus, code_name).real
        message = getattr(APIMessage, code_name).value
        detail = getattr(APIMessage, message_name).value

        abort(make_response(jsonify({
            "error": message,
            "detail": detail
        }), error_code))
