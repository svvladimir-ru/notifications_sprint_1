from random import randint

from flask import Blueprint, jsonify, request

from extensions import serializer


api = Blueprint('test', __name__)


@api.route("/", methods=['GET'])
def test():
    action = request.args['action']
    data = {
        "email": request.args['email'],
        "action": action,
        "i": randint(1, 1000)
    }
    return jsonify({
        "token": serializer.dumps(data=data, salt=action)
    })
