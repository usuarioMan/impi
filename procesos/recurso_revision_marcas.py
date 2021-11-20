from selenium_impi.buscadores import BusquedaEspecializada
from selenium_impi.extraction_expedientes import extract_expediente


def busqueda_especializada_marcas(num_resultados_mostrados: int = 75):
    """

    :param num_resultados_mostrados: Es el número de resultados que ha de mostrar el buscador. Por defecto es 75
    :return:
    """
    buscador = BusquedaEspecializada()
    buscador.busqueda()
    buscador.area('marcas')
    buscador.presentacion_resultados('crono', 'datos_imagen', num_resultados_mostrados)
    buscador.figura_juridica_marcas('marcas')
    buscador.ultimos_dias(20)
    buscador.escribir_campo('''busquedaSimpleForm:cadenaBusquedaText''', '''Negativa''')
    buscador.enviar_formulario_por_id('''busquedaSimpleForm:buscar''')
    expedientes = buscador.scraper_expedientes(num_resultados_mostrados)
    extract_expediente(buscador.driver, expedientes)


if __name__ == '__main__':
    busqueda_especializada_marcas()
