from flask import Flask
from elasticsearch import Elasticsearch
from flask_mongoengine import MongoEngine
from app.utils.response import CustomJSONEncoder
from config import Config

db = MongoEngine()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json_encoder = CustomJSONEncoder

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    db.init_app(app)

    from app import cli
    cli.init_app(app)

    from app.routes.post import bp as post_bp
    app.register_blueprint(post_bp)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
