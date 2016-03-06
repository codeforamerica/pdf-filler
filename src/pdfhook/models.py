from datetime import datetime
from peewee import *

from src.extensions import db

def create_tables():
    db.connect()
    db.create_tables([PDFForm], True)

class BaseModel(Model):
    class Meta:
        database = db

class PDFForm(BaseModel):
    id = IntegerField(primary_key=True, index=True)
    added_on = DateTimeField(default=datetime.now)
    original_pdf = BlobField()
    original_pdf_title = CharField(max_length=128)
    fdf_mapping = TextField()
    post_count = IntegerField(default=0)
    latest_post = DateTimeField(default=datetime.now)
