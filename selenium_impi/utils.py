from lxml.html import document_fromstring, HtmlElement
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


def set_driver():
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': '/Users/usuarioman/Ley/IMPI/DownloadNegativas'}
    # options.add_argument("--headless")
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome('/Users/usuarioman/WebDrivers/chromedriver', options=options)
    return driver


def get_html_element(text_response):
    try:
        h_element = document_fromstring(text_response)
        assert isinstance(h_element, HtmlElement)
        return h_element

    except AssertionError:
        print('Nop, no es un HtmlElement')
        pass


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
