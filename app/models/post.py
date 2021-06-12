from app import db
from app.models.search import SearchableMixin


class Post(db.Document, SearchableMixin):
    __tablename__ = 'posts'
    __searchable__ = ['title', 'content']
    title = db.StringField(max_length=120, required=True)
    content = db.StringField(required=True)
    remote_url = db.StringField(max_length=120)
