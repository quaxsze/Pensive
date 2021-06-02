from flask import Blueprint, request
from mongoengine.errors import ValidationError as MongoValidationError
from marshmallow import Schema, fields, post_load, ValidationError
from app.models.post import Post
from app.utils.response import bad_request, server_error, successful, created

bp = Blueprint('post', __name__)


class PostSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    remote_url = fields.Str()

    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)


@bp.route('/posts', methods=['GET'])
def get_posts_list():
    try:
        posts = Post.objects()
        if posts:
            return successful({'posts': PostSchema().dump(posts, many=True)})
        else:
            return successful({'posts': []})
    except Exception as err:
        return server_error(str(err))


@bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json() or {}

    try:
        new_post = PostSchema().load(data)
    except ValidationError as err:
        return bad_request(err.messages)

    try:
        new_post.save()
        return created({'post': new_post.id})
    except Exception as err:
        return server_error(str(err))


@bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = Post.objects.get_or_404(id=post_id)
        return successful({'post': PostSchema().dump(post)})
    except MongoValidationError:
        return bad_request('Invalid post id')
