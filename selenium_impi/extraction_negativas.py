import time
from lxml.html import document_fromstring, HtmlElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


def seleccionar_todos(driver):
    WebDriverWait(driver, 30).until(
        ec.element_to_be_clickable((By.XPATH, '''//input[@name="busquedaSimpleForm:seleccionarTodos"]'''))).click()


def descargar_xls(driver):
    WebDriverWait(driver, 30).until(
        ec.element_to_be_clickable((By.ID, '''busquedaSimpleForm:exportarXLS'''))).click()


def next_page(driver):
    WebDriverWait(driver, 30).until(
        ec.element_to_be_clickable((By.XPATH, '''//a[@aria-label="Next Page"]'''))).click()


def extraction(driver):
    seleccionar_todos(driver)
    descargar_xls(driver)
    next_page(driver)
