import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGODB_HOST = os.environ.get('MONGODB_HOST')
    ELASTICSEARCH_URL = os.environ.get(
        'ELASTICSEARCH_URL') or 'http://localhost:9200'
    POSTS_PER_PAGE = 20
