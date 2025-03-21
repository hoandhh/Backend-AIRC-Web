# models/image.py
from database.setup import db
import datetime

class Image(db.Document):
    title = db.StringField(required=True)
    description = db.StringField()
    file_path = db.StringField(required=True)
    uploaded_by = db.ReferenceField('User')
    is_public = db.BooleanField(default=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    captions = db.ListField(db.StringField())
    
    meta = {
        'collection': 'images',
        'indexes': [
            {'fields': ['uploaded_by']},
            {'fields': ['created_at']}
        ]
    }
