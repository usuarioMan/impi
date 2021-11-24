import asyncio

import schedule
from procesos.recurso_revision_marcas import busqueda_especializada_marcas


def scheduele_marcas():
    schedule.every(10).seconds.do(busqueda_especializada_marcas)
    #schedule.every(1).minutes.do(busqueda_especializada_marcas)


def global_schedueler():
    scheduele_marcas()
