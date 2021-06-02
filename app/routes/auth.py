from flask import Blueprint, request, g
from marshmallow import Schema, fields, ValidationError

from app.models.user import User
from app.utils.decorators import login_required
from app.utils.response import bad_request, server_error, unauthorized, successful, created

bp = Blueprint('auth', __name__)


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.String(required=True, load_only=True)


class LoginSchema(Schema):
    name = fields.Str(required=True)
    password = fields.String(required=True)


@bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json() or {}

    try:
        LoginSchema().validate(data)
    except ValidationError as err:
        return bad_request(err.messages)

    try:
        # fetch the user data
        user = User.objects(username=data['username']).first()
        if user and user.check_password(data['password']):
            auth_token = user.encode_auth_token(user.id)
            return created({'token': auth_token.decode()})
        else:
            return unauthorized('Bad credentials')
    except Exception as err:
        return server_error(str(err))


@bp.route('/user', methods=['GET'])
@login_required
def retrieve_user():
    return successful({'user': UserSchema().dump(g.user)})
