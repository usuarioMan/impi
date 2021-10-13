from fastapi import APIRouter

from client.session_management import get_http_client

plain_search = APIRouter(
    prefix="/v1/simple_search"
)


@plain_search.get('/')
async def busqueda_simple():
    client = get_http_client()
    client.get()
