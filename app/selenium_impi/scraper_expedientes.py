import sys
import time
from lxml.html import document_fromstring
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import re
from math import ceil

from app.exceptions.selenium_impi import ScrapingError

__lista_expedientes = list()


class ScraperExpedientes:
    def __init__(self, driver):
        self.__driver = driver

    def __get_page_source(self):
        html = document_fromstring(self.__driver.page_source)
        return html

    def __extraer_numero_expediente(self, html):
        rows = html.xpath('''//tr[@data-ri="0"]''')
        expedientes = list(set([row[1][0].text for row in rows]))
        return expedientes

    def __next_page(self):
        try:
            WebDriverWait(self.__driver, 30).until(
                ec.visibility_of_element_located(
                    (By.XPATH, '''//a[@class="ui-paginator-next ui-state-default ui-corner-all"]''')
                )).click()

        except ElementClickInterceptedException:
            time.sleep(10)
            try:
                WebDriverWait(self.__driver, 30).until(
                    ec.visibility_of_element_located(
                        (By.XPATH, '''//a[@aria-label="Next Page"]''')
                    )).click()

            except:
                time.sleep(10)
                WebDriverWait(self.__driver, 30).until(
                    ec.element_to_be_clickable((By.XPATH, '''//a[@aria-label="Next Page"]'''))).click()

    def __numero_resultados_obtenidos(self) -> int:
        """
        Toma el código funte de la página arrojada por el buscador y busca el número de resultados.
        Una vez que obtiene el string con el numero de resultados, lo limpia y lo convierte a un
        numero entero que posteriormente retorna.
        :param html:
        :return: int
        """
        # Esperar a que se carguen los resultados. Porque si no esperas te muestra Resultados encontrados: 0
        WebDriverWait(self.__driver, 30).until(
            ec.element_to_be_clickable((By.XPATH, '''//input[@id="busquedaSimpleForm:seleccionarTodos"]''')))
        try:
            html = self.__get_page_source()
            resultados_encontrados = html.xpath('''//label[@id="busquedaSimpleForm:j_idt138"]''')[0].text

            # VERIFICAR QUE EXISTAN RESULTADOS.
            if resultados_encontrados == 'Resultados encontrados: 0':
                time.sleep(10)
                resultados_encontrados = html.xpath('''//label[@id="busquedaSimpleForm:j_idt138"]''')[0].text

                if resultados_encontrados == 'Resultados encontrados: 0':
                    print("WARNING. NO SE ENCONTRARON RESULTADOS PARA LA BÚSQUEDA.")
                    sys.exit(1)

            # VERIFICAR QUE EL ELEMENTO EXISTA.
            assert 'Resultados encontrados:' in resultados_encontrados

        except AssertionError as error:
            raise ScrapingError(f'No fue posible encontrar el número de resultados arrojados por el buscador: {error}')

        resultados = int(re.search(r'\d+', resultados_encontrados).group(0))

        return resultados

    def __extraer_todos_los_numeros_expediente(self, mostrados, obtenidos) -> list:
        """
        Toma el número de resultados mostrados por página.
        Toma el número de resultados obtenidos por la búsqueda.
        Divide el número de resultados obtenidos por el numero de resultados mostrados.
        El resultado lo redondea hacía arriba para determinar el número de páginas que deberán ser escrapeados
        y por lo tanto, el numero de veces que se ha de cambiar de página.

        :param mostrados:
        :param obtenidos:
        :return: list
        """
        numero_paginaciones = ceil(obtenidos / mostrados)
        lista_expedientes = list()

        for pagina in range(numero_paginaciones):
            page_source = self.__get_page_source()
            pagina_lista_expedientes = self.__extraer_numero_expediente(page_source)
            lista_expedientes.append(pagina_lista_expedientes)
            if pagina == (numero_paginaciones - 1):
                break
            self.__next_page()

        flat_expediente = [item for sublist in lista_expedientes for item in sublist]
        return flat_expediente

    def extraer_informacion_expedientes(self, resultados_mostrados):
        resultados_obtenidos = self.__numero_resultados_obtenidos()
        expedientes = self.__extraer_todos_los_numeros_expediente(resultados_mostrados, resultados_obtenidos)
        return expedientes
