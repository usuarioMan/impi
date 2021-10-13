import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from client.session_management import GlobalSession
from db.utils import motor_global_init
from routes.busqueda_simple import plain_search

app = FastAPI(
    debug=True,
    title="IMPI",
    description="Proxy del IMPI",
    version='0.0.1',
)


@app.get('/')
async def hello():
    return "Hello"


def config_routes():
    app.include_router(router=plain_search)


def config():
    config_routes()
    config_database()


def run_server():
    loop = asyncio.get_event_loop()
    server_configuration = uvicorn.Config(
        app="main:app",
        host='127.0.0.1',
        port=8000,
        loop=loop,
        reload=True,
        debug=True,
    )
    server = uvicorn.Server(server_configuration)
    loop.run_until_complete(server.serve())


def config_database():
    loop = asyncio.get_event_loop()
    motor_global_init(io_loop=loop)


def main():
    config()
    run_server()


@app.on_event("startup")
@repeat_every(seconds=1680, wait_first=False, max_repetitions=2)  # 1680sec = 28min
async def periodic():
    try:
        GlobalSession()
    except Exception as error:
        print(error)
        pass

if __name__ == '__main__':
    main()

else:
    config()
