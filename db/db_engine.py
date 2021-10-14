from mongoengine import connect, Document, StringField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, \
    DateField, ListField
from os import environ
import dateutil.parser

DB_USERNAME = environ['MDB_PNT_OWNER_USERNAME']
DB_PASSWORD = environ['MDB_PNT_OWNER_PWD']

yourdate = dateutil.parser.parse("12/10/2020 09:29:58 AM")


def create_connection():
    connect(host=f"mongodb://127.0.0.1:27017/IMPI")


class Expediente(EmbeddedDocument):
    denominacion = StringField()
    link_visor = StringField()
    numero_expediente = StringField()
    numero_registro = StringField()
    numero_registro_internacional = StringField()
    fecha_presentacion = DateTimeField()
    fecha_publicacion = DateField()
    fecha_inicio_uso = DateField()
    fecha_concesion = DateField()
    fecha_vigencia = DateField()
    tipo_solicitud = StringField()
    tipo_marca = StringField()
    elementos_solicita_proteccion = StringField()
    traduccion = StringField()
    transliteracion = StringField()


class Establecimiento(EmbeddedDocument):
    direccion = StringField()
    poblacion = StringField()
    codigo_postal = StringField()
    pais = StringField()


class Cliente(Document):
    nombre = StringField()
    direccion = StringField()
    poblacion = StringField()
    codigo_postal = StringField()
    nacionalidad = StringField()
    rfc = StringField()
    telefono = StringField()
    Fax = StringField()
    email = StringField()
    codigo_viena = StringField()
    establecimiento = EmbeddedDocumentField(Establecimiento)
    expedientes = ListField(EmbeddedDocumentField(Expediente))
    productos_servicios = StringField()
