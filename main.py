import asyncio
import uvicorn
from fastapi import FastAPI
from schedueler.global_schedueler import global_schedueler
from routes.twilio.redirect import router as redirect_router
from routes.twilio.sms import router as sms_router
from routes.twilio.status import router as status_router
from routes.twilio.voice import router as voice_router

app = FastAPI()


def config():
    config_routes()


def config_routes():
    app.include_router(redirect_router)
    app.include_router(sms_router)
    app.include_router(status_router)
    app.include_router(voice_router)


def run_server():
    loop = asyncio.get_event_loop()
    server_configuration = uvicorn.Config(
        app="main:app",
        host='127.0.0.1',
        port=8000,
        loop=loop,
        reload=True
    )
    server = uvicorn.Server(server_configuration)
    loop.run_until_complete(server.serve())


@app.on_event('startup')
async def schedueling_tasks():
    # global_schedueler()
    ...


@app.on_event('startup')
def template_configuration():
    from pathlib import Path
    import fastapi_chameleon

    dev_mode = True

    BASE_DIR = Path(__file__).resolve().parent
    template_folder = str(BASE_DIR / 'templates')
    fastapi_chameleon.global_init(template_folder, auto_reload=dev_mode)


# @app.on_event("startup")
# @repeat_every(seconds=10)
# def run_pending_jobs() -> None:
#     print('Running pending jobs ...')
#     run_pending()


def main():
    run_server()
    config()


if __name__ == '__main__':
    main()

else:
    config()
