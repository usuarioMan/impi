import time
from typing import Union
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from exceptions.selenium_impi import InvalidParameter
from selenium_impi.extraction_expedientes import extract_expediente
from selenium_impi.extraction_negativas import ScraperExpedientes


def set_driver():
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': '/Users/usuarioman/Ley/IMPI/DownloadNegativas'}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome('/Users/usuarioman/WebDrivers/chromedriver', options=options)
    return driver


def busqueda_simple(driver):
    driver.get("https://siga.impi.gob.mx/newSIGA/content/common/principal.jsf")
    element = driver.find_element_by_link_text("Búsqueda simple")
    element.click()
    input_a = driver.find_element_by_id("busquedaSimpleForm:cadenaBusquedaText")
    input_b = driver.find_element_by_id("busquedaSimpleForm:seccion:1")
    input_c = driver.find_element_by_id("busquedaSimpleForm:opciones3:2")
    input_d = driver.find_element_by_id("busquedaSimpleForm:buscar")
    input_a.send_keys("Solicitudes de Marcas, Avisos y Nombres Comerciales presentadas ante el Instituto")
    input_b.click()
    input_c.click()
    input_d.click()


# def busqueda_especial(driver):
#     driver.get("https://siga.impi.gob.mx/newSIGA/content/common/principal.jsf")
#     driver.find_element_by_link_text("Búsqueda especializada").click()


def go_busqueda_seccion(driver):
    driver.get("https://siga.impi.gob.mx/newSIGA/content/common/principal.jsf")
    driver.find_element_by_link_text("Búsqueda por sección").click()


def set_area_param(area: str, driver):
    """
    Da click sobre el área de búsqueda.
    :param area:
    :param driver:
    :return:
    """
    wait = WebDriverWait(driver, 10)
    try:
        if area == "patente":
            try:
                wait.until(
                    ec.visibility_of_element_located((By.ID, "busquedaSimpleForm:seccion:1")))
                driver.find_element_by_id("busquedaSimpleForm:seccion:1").click()
            except StaleElementReferenceException:
                wait.until(
                    ec.visibility_of_element_located((By.ID, "busquedaSimpleForm:seccion:1")))
                driver.find_element_by_id("busquedaSimpleForm:seccion:1").click()
            except NoSuchElementException:
                exit(1)

        elif area == "marcas":
            driver.find_element_by_id("busquedaSimpleForm:seccion:1").click()
        elif area == "contencioso":
            driver.find_element_by_id("busquedaSimpleForm:seccion:2").click()
        else:
            raise ValueError

    except ValueError:
        print(f'{area} no es un valor válido para area. Los parámetros válidos son: patente, marcas y contencioso')


def click_gaceta_notificacion_marcas(driver):
    WebDriverWait(driver, 30).until(
        ec.visibility_of_element_located(
            (By.XPATH, '''//span[contains(text(),"- Notificaciones de Marcas")]''')
        )).click()


def click_seccion_notificacion_marcas(driver):
    try:
        WebDriverWait(driver, 30).until(
            ec.visibility_of_element_located(
                (By.XPATH, '''//*[@id="busquedaSimpleForm:seccionOneSelect"]/div[2]/ul/li[2]''')
            )
        ).click()

    except StaleElementReferenceException:
        driver.find_element_by_xpath(
            '''//*[@id="busquedaSimpleForm:seccionOneSelect"]/div[2]/ul/li[2]''').click()
    except NoSuchElementException:
        exit(1)


def write_busqueda(driver):
    try:
        WebDriverWait(driver, 30).until(
            ec.visibility_of_element_located(
                (By.ID, '''busquedaSimpleForm:repeat:0:valor''')
            )
        ).send_keys("NEGATIVA DE LA PROTECCIÓN")

    except StaleElementReferenceException:
        WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located(
                (By.ID, '''busquedaSimpleForm:repeat:0:valor''')
            )
        ).send_keys("NEGATIVA DE LA PROTECCIÓN")
    except NoSuchElementException:
        exit(1)


def send_form(driver):
    try:
        WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located(
                (By.ID, '''busquedaSimpleForm:buscar''')
            )
        ).click()
    except Exception as e:
        print(e)
        exit(1)


class Busqueda:
    def __init__(self):
        self.driver = set_driver()
        self.area_busqueda = None
        self.figura_juridica = None

    def busqueda(self):
        pass

    def presentacion_resultados(self, *args):
        pass

    def escribir_campo(self, id_selector, texto):
        try:
            WebDriverWait(self.driver, 30).until(
                ec.visibility_of_element_located(
                    (By.ID, id_selector)
                )
            ).send_keys(texto)

        except StaleElementReferenceException:
            WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located(
                    (By.ID, id_selector)
                )
            ).send_keys(texto)
        except NoSuchElementException:
            exit(1)

    def area(self, area: str):
        """
        Determina el área específica para la busqueda, la cual puede recaer sobre patentes,
        marcas y contencioso.

        :param area: Acepta tres valores: 'patente', 'marcas' y 'contencioso'
        :return:
        """
        wait = WebDriverWait(self.driver, 10)
        try:
            if area == "patente":
                try:
                    wait.until(
                        ec.visibility_of_element_located((By.ID, "busquedaSimpleForm:seccion:1")))
                    self.driver.find_element_by_id("busquedaSimpleForm:seccion:1").click()
                except StaleElementReferenceException:
                    wait.until(
                        ec.visibility_of_element_located((By.ID, "busquedaSimpleForm:seccion:1")))
                    self.driver.find_element_by_id("busquedaSimpleForm:seccion:1").click()
                except NoSuchElementException:
                    exit(1)

            elif area == "marcas":
                self.driver.find_element_by_id("busquedaSimpleForm:seccion:1").click()

            elif area == "contencioso":
                self.driver.find_element_by_id("busquedaSimpleForm:seccion:2").click()

            else:
                raise ValueError

        except ValueError:
            print(f'{area} no es un valor válido para area. Los parámetros válidos son: patente, marcas y contencioso')

        finally:
            self.area_busqueda = area

    def click_by_id(self, id_selector: str):
        """
        Localiza un elemento por ID y le da click.
        :param id_selector: Es el ID del elemento web sobre el cual se desea dar click.
        :return: None.
        """
        WebDriverWait(self.driver, 30).until(
            ec.visibility_of_element_located(
                (By.ID, id_selector)
            )).click()

    def click_by_xpath_function(self, xpath_function: str):
        WebDriverWait(self.driver, 30).until(
            ec.visibility_of_element_located(
                (By.XPATH, xpath_function)
            )).click()

    def click_25_resultados(self):
        """
        Da click en la opción de 25.
        :return:
        """
        self.click_by_id('''busquedaSimpleForm:opciones3:0''')

    def click_50_resultados(self):
        """
        Da click en la opción de 50.
        :return: None
        """
        self.click_by_id('''busquedaSimpleForm:opciones3:1''')

    def click_75_resultados(self):
        """
        Da click en la opción de 75.
        :return:
        """
        self.click_by_id('''busquedaSimpleForm:opciones3:2''')

    def enviar_formulario_por_id(self, id_selector):
        try:
            WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located(
                    (By.ID, id_selector)
                )
            ).click()
        except Exception as e:
            print(e)
            exit(1)


class BusquedaSimple(Busqueda):
    pass


class BusquedaEspecializada(Busqueda):
    def __init__(self):
        super().__init__()

    def busqueda(self):
        """
        Hace que el driver se ubique en la página de "Busqueda especialziada"
        Busca la opción de Busqueda especializada y le da click.
        :return: None.
        """
        self.driver.get("https://siga.impi.gob.mx/newSIGA/content/common/principal.jsf")
        self.driver.find_element_by_link_text("Búsqueda especializada").click()

    def presentacion_resultados(self, tipo_busqueda: str, datos_imagen: str, numero_resultados: int):
        """
        Permite configurar la presentación de resultados de la busqueda.

        :param tipo_busqueda: Acepta dos valores, crono o relevancia. Determina la forma en la
        que serán mostrados los resultados, si cronológicamente o por relevancia.

        :param datos_imagen: Acepta dos valores, datos_imagen o imagen. Determina si únicamente
        han de mostrarse la imágen, o bien, los datos y la imagen.

        :param numero_resultados: Acepta tres valores, 25, 50 y 75. Determina el número de resultados a mostrar.

        :return: None
        """
        self.__fabrica_presentacion_resultados(tipo_busqueda, datos_imagen, numero_resultados)

    #   ------------------------------------------------------------FIGURA JURÍDICA.
    def figura_juridica_patentes(self):
        assert self.area_busqueda == 'patente', f"El área de busqueda actual es {self.area_busqueda}. 'patente' debe ser selccionado para usar esta función."
        # TODO: Completar la sección de patentes.

    def figura_juridica_marcas(self, figura: Union[str, None]):
        """
        En caso de que el área de busqueda sean marcas selecciona la figura jurídica, en caso contrario genera un
        error.
        :param figura: La figura jurídica a seleccionar. Puede ser:
            * todas
            * marcas
            * nombres_comerciales
            * avisos_comerciales
            * denominaciones -- Esto es para denominaciones de origen.
            * None -- En caso de que no se especifique figura "Sin figura".
        :return: None
        """
        assert self.area_busqueda == 'marcas', f"El área de busqueda actual es {self.area_busqueda}. 'marcas' debe ser selccionado para usar esta función."
        self.__fabrica_figura_juridica_marcas(figura)
        self.figura_juridica = figura

    def figura_juridica_contencioso(self):
        assert self.area_busqueda == 'contencioso', f"El área de busqueda actual es {self.area_busqueda}. 'contencioso' debe ser selccionado para usar esta función."
        # TODO: Completar la sección de contencioso.

    #   ------------------------------------------------------------------ NEMÓNICOS.
    # TODO: En su caso ponerlo pero por el momento no hace falta.
    def nemonicos(self, nemonico):
        def nemonicos_todas(self, nemonico):
            pass

        def nemonicos_marcas(self, nemonico):
            """
            Selecciona nemónicos en caso de que se haya utilizado Marca como figura jurídica.
            :param nemonico: Los nemónicos válidos son:
                * actor
                * agente_apoderado
                * cesionario
                * clase
                * datos_titular
                * debe_decir
                * dice
                * error_corregido
                * fecha_concesion_registro
                * fecha_presentacion_legal
                * fecha_renovacion
                * folio_salida
                * imagen
                * licenciatario
                * nivel
                * nota_publicacion
                * nueva_ubicacion
                * nuevo_titular
                * numero_concesion_registro
                * numero_oficio
                * numero_resolucion
                * numero_solicitud_expediente_title
                * oficio
                * opositor
                * resumen_productos_servicios
                * solicitante
                * titulo_denominacion
            :return:
            """
            pass

        def nemonicos_avisos_comerciales(self, nemonico):
            pass

        def nemonicos_denominacion(self, nemonico):
            pass

        def nemonicos_sin_figura(self, nemonico):
            pass

    #   ------------------------------------------------------------------- FECHAS.
    # TODO: Esta función de falta re-facotrizarse. También le falta contemplar el cambio de mes.
    def ultimos_dias(self, numero_dias: int):
        d = datetime.today() - timedelta(days=numero_dias)
        operador = self.driver.find_element_by_id('''busquedaSimpleForm:operadoresCirculacion''')
        operador.find_element_by_xpath('''//option[text()=">="]''').click()
        self.click_by_xpath_function('''//input[@name="busquedaSimpleForm:fechaInicioCalendar_input"]''')
        self.click_by_xpath_function(f'''//a[text()="{d.day}"]''')
        # Habilitar busqueda por fecha
        self.click_by_id('''busquedaSimpleForm:checkCirculacion''')

    def __fabrica_presentacion_resultados(self, tipo_busqueda: str, datos_imagen: str, numero_resultados: int):
        def __fabrica_tipo_busqueda(param_tipo_busqueda):
            """
            Fábrica que determina qué elemento web ha de recibir el click de conformidad con el parámetro
            otorgado.

            :param param_tipo_busqueda: Acepta dos valores, crono o relevancia. Determina la forma en la
            que serán mostrados los resultados, si cronológicamente o por relevancia.

            :return: None
            """

            if param_tipo_busqueda == "crono":
                self.click_by_id('''busquedaSimpleForm:opciones1:0''')

            elif param_tipo_busqueda == "relevancia":
                self.click_by_id('''busquedaSimpleForm:opciones1:1''')

            else:
                raise InvalidParameter(
                    f"{param_tipo_busqueda} no está permitido. Únicamente se puede usar 'crono' o 'relevancia' ")

        def __fabrica_datos_imagen(param_datos_imagen):
            """
            Fábrica que determina qué elemento web ha de recibir el click de conformidad con el parámetro
            otorgado.
            :param param_datos_imagen: Acepta dos valores, datos_imagen o imagen. Determina si únicamente
            han de mostrarse la imágen, o bien, los datos y la imagen.
            :return: None
            """
            if param_datos_imagen == "datos_imagen":
                self.click_by_id('''busquedaSimpleForm:opciones2:0''')

            elif param_datos_imagen == "imagen":
                self.click_by_id('''busquedaSimpleForm:opciones2:1''')

            else:
                raise InvalidParameter(
                    f"{param_datos_imagen} no está permitido. Únicamente se puede usar 'datos_imagen' o 'imagen' ")

        def __fabrica_numero_resultados(param_numero_resultados):
            """
            Fábrica que determina qué elemento web ha de recibir el click de conformidad con el parámetro
            otorgado.
            :param param_numero_resultados: Acepta tres valores, 25, 50 y 75. Determina el número de resultados a mostrar.
            :return: None
            """
            if param_numero_resultados == 25:
                self.click_25_resultados()

            elif param_numero_resultados == 50:
                self.click_50_resultados()

            elif param_numero_resultados == 75:
                self.click_75_resultados()

            else:
                raise InvalidParameter(
                    f"{param_numero_resultados} no está permitido. Únicamente se puede usar '25', '50' o '75' ")

        __fabrica_tipo_busqueda(tipo_busqueda)
        __fabrica_datos_imagen(datos_imagen)
        __fabrica_numero_resultados(numero_resultados)

    def __fabrica_figura_juridica_marcas(self, figura):
        if figura == 'todas':
            self.click_by_xpath_function('''//li[contains(text(),"Todas")]''')

        elif figura == 'marcas':
            self.click_by_xpath_function('''//li[contains(text(),"- Marcas")]''')

        elif figura == 'nombres_comerciales':
            self.click_by_xpath_function('''//li[contains(text(),"- Nombres Comerciales")]''')

        elif figura == 'avisos_comerciales':
            self.click_by_xpath_function('''//li[contains(text(),"- Avisos Comerciales")]''')

        elif figura == 'denominaciones':
            self.click_by_xpath_function('''//li[contains(text(),"- Denominaciones de Origen")]''')

        elif figura is None:
            self.click_by_xpath_function('''//li[contains(text(),"- Sin figura")]''')

        else:
            raise InvalidParameter(
                f"{figura} no está permitido. Únicamente se puede usar 'todas', 'marcas', 'nombres_comerciales', 'avisos_comerciales', 'denominaciones' o 'None' ")

    def scraper_expedientes(self, resultados_mostrados):
        scraper = ScraperExpedientes(self.driver)
        expedientes = scraper.extraer_informacion_expedientes(resultados_mostrados)
        return expedientes


def busqueda_especializada_marcas(num_resultados_mostrados: int = 75):
    """

    :param numero_resultados: Es el número de resultados que ha de mostrar el buscador. Por defecto es 75
    :return:
    """
    buscador = BusquedaEspecializada()
    buscador.busqueda()
    buscador.area('marcas')
    buscador.presentacion_resultados('crono', 'datos_imagen', num_resultados_mostrados)
    buscador.figura_juridica_marcas('marcas')
    buscador.ultimos_dias(10)
    buscador.escribir_campo('''busquedaSimpleForm:cadenaBusquedaText''', '''Negativa''')
    buscador.enviar_formulario_por_id('''busquedaSimpleForm:buscar''')
    expedientes = buscador.scraper_expedientes(num_resultados_mostrados)
    extract_expediente(buscador.driver, expedientes)


if __name__ == '__main__':
    busqueda_especializada_marcas()
