from functools import wraps
import bson
from flask import request

from app.models.user import User
from app.utils.response import unauthorized, forbidden


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('authorization', None)
        if auth_header is None:
            return forbidden('Provide a valid auth token.')

        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            return forbidden('Bearer token malformed.')

        resp = User.decode_auth_token(auth_token)

        if not bson.objectid.ObjectId.is_valid(resp):
            return unauthorized(resp)

        user = User.objects(id=resp).first()
        if not user:
            return unauthorized('Bad credentials')

        return f(user, *args, **kwargs)
    return decorated_function
