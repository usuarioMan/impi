from selenium_impi.buscador_negativas import set_area_param, click_75_resultados
from selenium_impi.selenium_client import set_driver, busqueda_especial


def recurso_main():
    driver = set_driver()
    busqueda_especial(driver)
    set_area_param(area="marcas", driver=driver)
    click_75_resultados(driver)


if __name__ == '__main__':
    recurso_main()
