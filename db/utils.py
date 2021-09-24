from collections import namedtuple
from os import environ
from typing import Optional


from db.motor_client import MotorClient


def get_motor_client() -> MotorClient:
    """
    Llamar en lugar de instanciar directamente MotorClient.
    Crea una instancia de MotorClient y la retorna.
    :return: motor.motor_asyncio.AsyncIOMotorClient()
    """
    motor_client = MotorClient()
    return motor_client


async def check_if_database_exists(database_name):
    motor_client = get_motor_client()
    dbs_on_server = await motor_client.motor.list_database_names()
    try:
        if database_name not in dbs_on_server:
            raise Exception

    except Exception as error:
        print(error)


def create_connection_string(
        username: str,
        password: str,
        host: str,
        port: str,
        auth_source: Optional[str] = "pnt",
        auth_mechanism: Optional[str] = "SCRAM-SHA-1") -> str:
    """
    This function is used by motor_global_init just once, in order to create the connection with the database.
    :param username: ******** environ
    :param password: ******** environ
    :param host: 127.0.0.1
    :param port: 27017
    :param auth_source: pnt
    :param auth_mechanism: SCRAM-SHA-1
    :return: Connection string
    """
    try:
        connection_string: str = f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_source}" \
                                 f"&authMechanism={auth_mechanism}"
        return connection_string

    except Exception as error:
        print("create_connection_string function failed", error)


def get_credentials_from_environment_variables():
    MongoCredentials = namedtuple('MongoCredentials', ['username', 'password'])
    return MongoCredentials(
        username=environ.get('MDB_PNT_OWNER_USERNAME'),
        password=environ.get('MDB_PNT_OWNER_PWD'),
    )


def motor_global_init(
        io_loop,
        host: str = "127.0.0.1",
        port: str = "27017"):
    # Get credentials for database auth.
    credentials = get_credentials_from_environment_variables()

    # With credentials, create connection string.
    connection_string = create_connection_string(
        username=credentials.username,
        password=credentials.password,
        host=host,
        port=port,
    )

    # Create singleton.
    MotorClient(connection_string=connection_string, io_loop=io_loop)


async def save_funcionario(funcionario: dict):
    client = get_motor_client()
    fun = client.motor.pnt.funcionarios
    await fun.insert_one(funcionario)
    print(f"""FUNCIONARIO INSERTED: {funcionario}""")


async def save_requested_foia(requested_foia):
    historial = get_motor_client().get_collection('pnt', 'historial_foia')
    await historial.insert_one(requested_foia)

