from lxml.html import document_fromstring, HtmlElement
from selenium import webdriver
from db.db_engine import create_connection
from selenium_impi.buscador_negativas import buscar_negativas
from selenium_impi.extraction_expedientes import extract_expediente
from selenium_impi.extraction_negativas import extraction, lista_expedientes


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


def get_html_element(text_response):
    try:
        h_element = document_fromstring(text_response)
        assert isinstance(h_element, HtmlElement)
        return h_element

    except AssertionError:
        print('Nop, no es un HtmlElement')
        pass


def set_driver():
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': '/Users/usuarioman/Ley/IMPI/DownloadNegativas'}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome('/Users/usuarioman/WebDrivers/chromedriver', options=options)
    return driver


def main():
    driver = set_driver()
    buscar_negativas(driver)
    try:
        for _ in range(170):
            extraction(driver)

    except Exception:
        pass

    flat_expediente = [item for sublist in lista_expedientes for item in sublist]
    extract_expediente(driver, flat_expediente)


if __name__ == '__main__':
    create_connection()
    main()
