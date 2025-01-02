# mongo_models.py
from mongoengine import Document, StringField, IntField


class Person(Document):
    name = StringField(required=True)  # Field name must match 'Name' in MongoDB
    age = IntField()

    meta = {'collection': 'person'} 
	