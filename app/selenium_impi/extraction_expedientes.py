from mongoengine import NotUniqueError
from pymongo.errors import DuplicateKeyError
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from app.db.db_engine import create_connection, create_index
from app.models.cliente import Expediente, Cliente, Apoderado
from app.selenium_impi.data import ids


def buscar_expediente(driver: Chrome, expediente: str):
    url = 'https://acervomarcas.impi.gob.mx:8181/marcanet/vistas/common/datos/bsqExpedienteCompleto.pgi'
    driver.get(url)
    WebDriverWait(driver, 30).until(
        ec.visibility_of_element_located((By.ID, '''frmBsqExp:expedienteId'''))).send_keys(expediente)
    WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.ID, '''frmBsqExp:busquedaId2'''))).click()


def get_by_id(driver: Chrome, _id) -> str:
    WebDriverWait(driver, 1).until(
        ec.visibility_of_element_located((By.ID, _id)))

    text = driver.find_element_by_id(_id).text
    return text


def extraer_informacion_expediente(driver):
    expediente = None
    cliente = None
    apoderado = None
    datos_generales_numero_expediente = None
    datos_generales_fecha_presentacion = None
    datos_generales_fecha_publicacion_solicitud = None
    datos_generales_denominacion = None
    datos_generales_tipo_solicitud = None
    datos_titular_nombre = None
    datos_titular_direccion = None
    datos_titular_poblacion = None
    datos_titular_codigo_postal = None
    datos_titular_pais = None
    datos_titular_nacionalidad = None
    datos_titular_telefono = None
    datos_titular_email = None
    datos_apoderado_nombre = None
    datos_apoderado_direccion = None
    datos_apoderado_poblacion = None
    datos_apoderado_codigo_postal = None
    datos_apoderado_pais = None
    try:

        try:
            datos_generales_numero_expediente = get_by_id(driver, ids['datos_generales']['numero_expediente'])

        except:
            datos_generales_numero_expediente = None

        try:
            datos_generales_fecha_presentacion = get_by_id(driver, ids['datos_generales']['fecha_presentacion'])

        except:
            datos_generales_fecha_presentacion = None

        try:
            datos_generales_fecha_publicacion_solicitud = get_by_id(driver,
                                                                    ids['datos_generales'][
                                                                        'fecha_publicacion_solicitud'])
        except:
            datos_generales_fecha_publicacion_solicitud = None

        try:
            datos_generales_denominacion = get_by_id(driver, ids['datos_generales']['denominación'])

        except:
            datos_generales_denominacion = None

        try:
            datos_generales_tipo_solicitud = get_by_id(driver, ids['datos_generales']['tipo_solicitud'])

        except:
            datos_generales_tipo_solicitud = None

        try:
            datos_titular_nombre = get_by_id(driver, ids['datos_titular']['nombre'])

        except:
            datos_titular_nombre = None

        try:
            datos_titular_direccion = get_by_id(driver, ids['datos_titular']['direccion'])

        except:
            datos_titular_direccion = None

        try:
            datos_titular_poblacion = get_by_id(driver, ids['datos_titular']['poblacion'])

        except:
            datos_titular_poblacion = None

        try:
            datos_titular_codigo_postal = get_by_id(driver, ids['datos_titular']['codigo_postal'])

        except:
            datos_titular_codigo_postal = None

        try:
            datos_titular_pais = get_by_id(driver, ids['datos_titular']['pais'])

        except:
            datos_titular_pais = None

        try:
            datos_titular_nacionalidad = get_by_id(driver, ids['datos_titular']['nacionalidad'])

        except:
            datos_titular_nacionalidad = None

        try:
            datos_titular_telefono = get_by_id(driver, ids['datos_titular']['telefono'])

        except:
            datos_titular_telefono = None

        try:
            datos_titular_email = get_by_id(driver, ids['datos_titular']['email'])

        except:
            datos_titular_email = None

        try:
            datos_apoderado_nombre = get_by_id(driver, ids['datos_apoderado']['nombre'])

        except:
            datos_apoderado_nombre = None

        try:
            datos_apoderado_direccion = get_by_id(driver, ids['datos_apoderado']['direccion'])

        except:
            datos_apoderado_direccion = None

        try:
            datos_apoderado_poblacion = get_by_id(driver, ids['datos_apoderado']['poblacion'])

        except:
            datos_apoderado_poblacion = None

        try:
            datos_apoderado_codigo_postal = get_by_id(driver, ids['datos_apoderado']['codigo_postal'])

        except:
            datos_apoderado_codigo_postal = None

        try:
            datos_apoderado_pais = get_by_id(driver, ids['datos_apoderado']['pais'])

        except:
            datos_apoderado_pais = None

        apoderado = Apoderado(
            nombre=datos_apoderado_nombre,
            direccion=datos_apoderado_direccion,
            poblacion=datos_apoderado_poblacion,
            codigo_postal=datos_apoderado_codigo_postal,
            pais=datos_apoderado_pais,
        )

        expediente = Expediente(
            denominacion=datos_generales_denominacion,
            numero_expediente=datos_generales_numero_expediente,
            fecha_presentacion=datos_generales_fecha_presentacion,
            fecha_publicacion=datos_generales_fecha_publicacion_solicitud,
            tipo_solicitud=datos_generales_tipo_solicitud,
            apoderado=apoderado,
        )

        cliente = Cliente(
            nombre=datos_titular_nombre,
            direccion=datos_titular_direccion,
            poblacion=datos_titular_poblacion,
            pais=datos_titular_pais,
            codigo_postal=datos_titular_codigo_postal,
            nacionalidad=datos_titular_nacionalidad,
            telefono=datos_titular_telefono,
            email=datos_titular_email,
            expedientes=[expediente]
        )
        cliente.save()

    except (DuplicateKeyError, NotUniqueError):
        cliente = Cliente.objects(nombre=datos_titular_nombre).get()
        cliente.expedientes.append(expediente)
        cliente.save()


def extract_expediente(driver: Chrome, lista_expedientes):
    create_connection()
    create_index()
    for expediente in lista_expedientes:
        try:
            buscar_expediente(driver, expediente)
            extraer_informacion_expediente(driver)

        except Exception as error:
            print(error)
            continue
