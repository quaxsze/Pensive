import json
from flask import jsonify
from bson import ObjectId


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def json_response(status_code: int, data: str = None) -> dict:
    payload = {'status': status_code}
    if data:
        payload['data'] = data
    response = jsonify(payload)
    response.status_code = status_code
    return response


def json_error(status_code: int, message: str) -> dict:
    payload = {'status': status_code}
    payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def successful(message):
    return json_response(200, message)


def created(message):
    return json_response(201, message)


def bad_request(message):
    return json_error(400, message)


def unauthorized(message):
    return json_error(401, message)


def forbidden(message):
    return json_error(403, message)


def not_found(message):
    return json_error(404, message)


def conflict(message):
    return json_error(409, message)


def server_error():
    return json_error(500, 'Internal Server Error')
