import time
from lxml.html import document_fromstring, HtmlElement
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Chrome

lista_expedientes = list()


def extraer_numero_expediente(driver: Chrome):
    html = document_fromstring(driver.page_source)
    rows = html.xpath('''//tr[@data-ri="0"]''')
    expedientes = list(set([row[1][0].text for row in rows]))
    lista_expedientes.append(expedientes)


def next_page(driver):
    try:
        WebDriverWait(driver, 30).until(
            ec.element_to_be_clickable((By.XPATH, '''//a[@aria-label="Next Page"]'''))).click()

    except ElementClickInterceptedException:
        time.sleep(10)
        try:
            WebDriverWait(driver, 30).until(
                ec.element_to_be_clickable((By.XPATH, '''//a[@aria-label="Next Page"]'''))).click()
        except:
            time.sleep(10)
            WebDriverWait(driver, 30).until(
                ec.element_to_be_clickable((By.XPATH, '''//a[@aria-label="Next Page"]'''))).click()


def extraction(driver):
    extraer_numero_expediente(driver)
    next_page(driver)
