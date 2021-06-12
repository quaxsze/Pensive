from mongoengine import signals
from app.utils.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return [], 0
        return cls.objects(id__in=ids), total

    @classmethod
    def reindex(cls):
        for obj in cls.objects():
            add_to_index(cls.__tablename__, obj)

    @staticmethod
    def after_insert(sender, document, **kwargs):
        if isinstance(document, SearchableMixin):
            add_to_index(document.__tablename__, document)
        

    @staticmethod
    def after_delete(sender, document, **kwargs):
        if isinstance(document, SearchableMixin):
            remove_from_index(document.__tablename__, document)


signals.post_save.connect(SearchableMixin.after_insert)
signals.post_delete.connect(SearchableMixin.after_delete)
