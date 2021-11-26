from mongoengine import EmbeddedDocument, StringField, DateField, DateTimeField, Document, EmbeddedDocumentField, \
    ListField


class Apoderado(EmbeddedDocument):
    nombre = StringField()
    direccion = StringField()
    poblacion = StringField()
    codigo_postal = StringField()
    pais = StringField()


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
    apoderado = EmbeddedDocumentField(Apoderado)


class Cliente(Document):
    nombre = StringField()
    direccion = StringField()
    poblacion = StringField()
    codigo_postal = StringField()
    nacionalidad = StringField()
    pais = StringField()
    rfc = StringField()
    telefono = StringField()
    Fax = StringField()
    email = StringField()
    codigo_viena = StringField()
    expedientes = ListField(EmbeddedDocumentField(Expediente))
    productos_servicios = StringField()