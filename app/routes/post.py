from flask import Blueprint, request
from werkzeug.wrappers import Response
from mongoengine.errors import ValidationError as MongoValidationError
from marshmallow import Schema, fields, post_load, ValidationError
from app.models.post import Post
from app.utils.decorators import login_required
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
def get_posts_list() -> Response:
    try:
        posts = Post.objects()
        if posts:
            return successful({'posts': PostSchema().dump(posts, many=True)})
        else:
            return successful({'posts': []})
    except Exception as err:
        return server_error()


@bp.route('/posts', methods=['POST'])
@login_required
def create_post() -> Response:
    data = request.get_json() or {}

    try:
        new_post = PostSchema().load(data)
    except ValidationError as err:
        return bad_request(err.messages)

    try:
        new_post.save()
        return created({'post': new_post.id})
    except Exception as err:
        return server_error()


@bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id: str) -> Response:
    try:
        post = Post.objects.get_or_404(id=post_id)
        return successful({'post': PostSchema().dump(post)})
    except MongoValidationError:
        return bad_request('Invalid post id')


@bp.route('/posts/<post_id>', methods=['PUT'])
@login_required
def update_post(post_id: str) -> Response:
    data = request.get_json() or {}

    try:
        post = Post.objects.get_or_404(id=post_id)
    except MongoValidationError:
        return bad_request('Invalid post id')

    errors = PostSchema().validate(data)
    if errors:
        return bad_request(errors)

    try:
        post.update(**data)
        post.reload()
        return successful({'post': PostSchema().dump(post)})
    except Exception as err:
        return server_error()


@bp.route('/search', methods=['GET'])
def search_posts() -> Response:
    query_text: str = request.args.get('q')
    page_size: int = int(request.args.get('page_size'))
    page: int = int(request.args.get('page'))
