from mongoengine import connect, Document, StringField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, \
    DateField, ListField
from os import environ
import dateutil.parser

DB_USERNAME = environ['MDB_PNT_OWNER_USERNAME']
DB_PASSWORD = environ['MDB_PNT_OWNER_PWD']

yourdate = dateutil.parser.parse("12/10/2020 09:29:58 AM")


def create_connection():
    connect(host=f"mongodb://127.0.0.1:27017/IMPI")
