from aiohttp import ClientSession


# noinspection PyProtectedMember
class GlobalSession:
    """
    Global Session driver.
    Manages the state of the PNT server with the AsyncClient through cookies management.
    """
    __client = None

    def __new__(cls) -> "GlobalSession":
        if cls.__client is None:
            cls.__client = object.__new__(cls)
            cls.__client.async_client = ClientSession()

        return cls.__client


def get_session() -> GlobalSession:
    """
    Returns the GlobalSession instance.
    :return: GlobalSession
    """
    return GlobalSession()


def get_http_client() -> ClientSession:
    """
    Returns the ClientSession instance.
    :return: AsyncClient
    """
    return GlobalSession().async_client
