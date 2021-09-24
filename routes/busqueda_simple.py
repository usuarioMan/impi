from fastapi import APIRouter

plain_search = APIRouter(
    prefix="/v1/simple_search"
)


@plain_search.get('/')
async def busqueda_simple():
    return dict(msg="HOLA")
