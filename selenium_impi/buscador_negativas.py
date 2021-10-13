from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


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


def click_75_resultados(driver):
    WebDriverWait(driver, 30).until(
        ec.visibility_of_element_located(
            (By.ID, '''busquedaSimpleForm:opciones3:2''')
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


def buscar_negativas(driver):
    go_busqueda_seccion(driver)
    set_area_param('marcas', driver)
    click_gaceta_notificacion_marcas(driver)
    click_75_resultados(driver)
    click_seccion_notificacion_marcas(driver)
    write_busqueda(driver)
    send_form(driver)
