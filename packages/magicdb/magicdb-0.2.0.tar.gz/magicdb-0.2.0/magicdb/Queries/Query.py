from typing import Union
from magicdb import db, ASCENDING, DESCENDING, DocumentSnapshot

# from magicdb.Models import MagicModel


class Query:
    def __init__(self, cls):
        from magicdb.Models.MagicModel import MagicModel

        self.cls: MagicModel = cls
        self.collection_path = self.cls.get_collection_name()
        self.firebase_query = self.create_query()

    def create_query(self):
        self.firebase_query = db.conn.collection(self.collection_path)
        return self.firebase_query

    def parent(self, parent_or_path):
        from magicdb.Models.MagicModel import MagicModel

        parent_path = (
            parent_or_path
            if not issubclass(type(parent_or_path), MagicModel)
            else parent_or_path.key
        )

        self.collection_path = parent_path + "/" + self.collection_path
        self.create_query()
        return self

    def document(self, document_path):
        self.firebase_query = self.firebase_query.document(document_path)
        return self

    def collection_group(self):
        self.firebase_query = db.conn.collection_group(self.cls.get_collection_name())
        return self

    def collection(self, collection_path):
        self.firebase_query = self.firebase_query.collection(collection_path)
        return self

    """Wrapping Firestore abilities."""

    def where(self, field, action, value):
        self.firebase_query = self.firebase_query.where(field, action, value)
        return self

    def order_by(self, field, direction=None, **kwargs):
        if direction:
            kwargs["direction"] = direction
        if kwargs.get("direction", None) == "asc":
            kwargs["direction"] = ASCENDING
        if kwargs.get("direction", None) == "desc":
            kwargs["direction"] = DESCENDING
        self.firebase_query = self.firebase_query.order_by(field, **kwargs)
        return self

    def start_at(self, fields):
        self.firebase_query = self.firebase_query.start_at(fields)
        return self

    def start_after(self, fields):
        self.firebase_query = self.firebase_query.start_after(fields)
        return self

    def end_at(self, fields):
        self.firebase_query = self.firebase_query.end_at(fields)
        return self

    def end_before(self, fields):
        self.firebase_query = self.firebase_query.end_before(fields)
        return self

    def limit(self, limit):
        self.firebase_query = self.firebase_query.limit(limit)
        return self

    """Querying and creating of the models."""

    def stream(self, validate_db_data=True, **kwargs):
        """Currently defaults to validating the db data, but you can turn this off with the validate_db_data param"""
        docs = list(self.firebase_query.stream(**kwargs))

        constructor = self.cls if validate_db_data else self.cls.construct

        return [
            constructor(from_db=True, key=doc.reference.path, **doc.to_dict())
            for doc in docs
        ]

    def get(self, id=None, create=False, validate_db_data=True, **kwargs):
        doc = (
            self.firebase_query.get(**kwargs)
            if not id
            else self.firebase_query.document(id).get(**kwargs)
        )

        if type(doc) != DocumentSnapshot:
            return None

        d = doc.to_dict()
        if not d:
            return None if not create else self.cls(id=id)

        constructor = self.cls if validate_db_data else self.cls.construct

        return constructor(from_db=True, key=doc.reference.path, **doc.to_dict())

    def get_all(self, ids, validate_db_data=True, **kwargs):
        doc_refs = [db.conn.collection(self.collection_path).document(id) for id in ids]
        docs = db.conn.get_all(doc_refs, **kwargs)
        constructor = self.cls if validate_db_data else self.cls.construct
        return [
            constructor(from_db=True, key=doc.reference.path, **doc.to_dict())
            for doc in docs
        ]

    """Subcollections"""

    def collections(self):
        return self.firebase_query.collections()

    def collections_names(self):
        return [coll.id for coll in self.firebase_query.collections()]
