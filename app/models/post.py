from app import db


class Post(db.Document):
    title = db.StringField(max_length=120, required=True)
    content = db.StringField(required=True)
    remote_url = db.StringField(max_length=120)
