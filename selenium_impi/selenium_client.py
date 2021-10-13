from lxml.html import document_fromstring, HtmlElement
from selenium import webdriver
from selenium_impi.buscador_negativas import buscar_negativas
from selenium_impi.extraction_negativas import extraction


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
    for _ in range(100):
        extraction(driver)


if __name__ == '__main__':
    main()
