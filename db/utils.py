from models.cliente import Expediente, Cliente


def save_expedientes(lista_expedientes: list):
    for expediente in lista_expedientes:
        expediente = Expediente(numero_expediente=expediente)
        cliente = Cliente(expedientes=[expediente])
        cliente.save()
