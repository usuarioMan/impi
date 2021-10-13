import time

from lxml.html import document_fromstring, HtmlElement
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, \
    ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

options = webdriver.ChromeOptions()
prefs = {'download.default_directory': '/Users/usuarioman/Ley/IMPI/DownloadNegativas'}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome('/Users/usuarioman/WebDrivers/chromedriver', options=options)


def busqueda_simple():
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


def busqueda_negativas(selenium_driver):
    # 1. Busqueda por sección.
    go_busqueda_seccion(selenium_driver)

    # 2. Area de busqueda.
    set_area_param("marcas", selenium_driver)

    wait = WebDriverWait(selenium_driver, 10)
    wait.until(
        ec.visibility_of_element_located((By.XPATH, '''//span[contains(text(),"- Notificaciones de Marcas")]''')))
    selenium_driver.find_element_by_xpath('''//span[contains(text(),"- Notificaciones de Marcas")]''').click()
    wait.until(ec.visibility_of_element_located(
        (By.XPATH, '''//*[@id="busquedaSimpleForm:seccionOneSelect"]/div[2]/ul/li[2]''')))
    selenium_driver.find_element_by_id("busquedaSimpleForm:opciones3:2").click()
    try:
        selenium_driver.find_element_by_xpath(
            '''//*[@id="busquedaSimpleForm:seccionOneSelect"]/div[2]/ul/li[2]''').click()
    except StaleElementReferenceException:
        selenium_driver.find_element_by_xpath(
            '''//*[@id="busquedaSimpleForm:seccionOneSelect"]/div[2]/ul/li[2]''').click()
    except NoSuchElementException:
        exit(1)

    try:
        wait.until(
            ec.visibility_of_element_located((By.ID, '''busquedaSimpleForm:repeat:0:valor''')))
        selenium_driver.find_element_by_id('busquedaSimpleForm:repeat:0:valor').send_keys("NEGATIVA DE LA PROTECCIÓN")
    except StaleElementReferenceException:
        selenium_driver.find_element_by_id('busquedaSimpleForm:repeat:0:valor').send_keys("NEGATIVA DE LA PROTECCIÓN")
    except NoSuchElementException:
        exit(1)
    try:
        selenium_driver.find_element_by_id('busquedaSimpleForm:buscar').click()
    except Exception as e:
        print(e)


def get_html_element(text_response):
    try:
        h_element = document_fromstring(text_response)
        assert isinstance(h_element, HtmlElement)
        return h_element

    except AssertionError:
        print('Nop, no es un HtmlElement')
        pass


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


onclick_str = """PrimeFaces.ab({s:"busquedaSimpleForm:tabla:2:subTabla:0:linkVidoc",onco:function(xhr,status,args){ga('send', 'event', 'ViDoc', 'click', 'download');window.open('http://vidoc.impi.gob.mx/ViDoc/siga.do?usr=SIGA&texp=SI&tdoc=E&id=MA/E/M/1985/2464501');                                            return false;;}});return false;"""


def scraping(driver: webdriver.Chrome):
    wait = WebDriverWait(driver, 30)

    WebDriverWait(driver, 30).until(
        ec.element_to_be_clickable((By.XPATH, '''//input[@name="busquedaSimpleForm:seleccionarTodos"]'''))).click()

    WebDriverWait(driver, 30).until(
        ec.element_to_be_clickable((By.ID, '''busquedaSimpleForm:exportarXLS'''))
    )
    wait.until(
        ec.element_to_be_clickable((By.ID, '''busquedaSimpleForm:exportarXLS'''))
    )
    driver.find_element_by_id('''busquedaSimpleForm:exportarXLS''').click()

    driver.find_element_by_xpath('''//a[@aria-label="Next Page"]''').click()


busqueda_negativas(driver)
for _ in range(100):
    scraping(driver)
    time.sleep(2)
