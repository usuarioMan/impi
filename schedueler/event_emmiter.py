import json
from aiohttp import ClientSession
import asyncio
from pprint import pprint
import codecs


class AClient:
    __client = None

    def __new__(cls) -> "ClientSession":
        if cls.__client is None:
            cls.__client = object.__new__(cls)
            cls.__client.cs = ClientSession()

        return cls.__client.cs


async def init_global_client(username, password):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'Authorization': 'Basic Og==',
        'Content-Type': 'application/x-www-form-urlencoded'}

    auth_payload = {'grant_type': 'password',
                    'username': username,
                    'password': password}

    client = AClient()

    async with client.request(method="POST",
                              url="http://34.94.15.128/token",
                              headers=headers,
                              data=auth_payload,
                              ) as response:
        try:
            r = await response.json()
            jwt_token = r['access_token']
            token_header = {'Authorization': f'Bearer {jwt_token}'}
            client.headers.update(token_header)
            print("Authentication complete.")

        except:
            print("Auth failed.")


# ----------------------------------------------------------------------------
# NO TOCAR.
async def close_client():
    """
    Returns the ClientSession instance.
    :return: AsyncClient
    """
    c = AClient()
    await c.close()


def get_http_client() -> ClientSession:
    """
    Returns the ClientSession instance.
    :return: AsyncClient
    """
    return AClient()


async def main(user=None, password=None):
    await event_emmiter()


async def event_emmiter():
    client = get_http_client()
    end_point = "http://fast_api/event_handler"
    while True:
        try:
            async with client.request(method="POST",
                                      url=end_point) as response:
                if response.status == 200:
                    print("EXITO")
                else:
                    print("FRACASO")

            await asyncio.sleep(60)
        except:
            await asyncio.sleep(60)
            pass


if __name__ == '__main__':
    USERNAME = ...
    PASSWORD = ...

    asyncio.run(main())
