from functools import wraps
from flask import request, g

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

        if isinstance(resp, str):
            return unauthorized(resp)

        user = User.objects(id=resp).first()
        if not user:
            return unauthorized('Bad credentials')
        g.user = user
        g.current_auth_token = auth_token

        return f(*args, **kwargs)
    return decorated_function
