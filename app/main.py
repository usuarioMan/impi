from fastapi import FastAPI
from routes.twilio.redirect import router as redirect_router
from routes.twilio.sms import router as sms_router
from routes.twilio.status import router as status_router

app = FastAPI()


def config():
    config_routes()


def config_routes():
    app.include_router(redirect_router)
    app.include_router(sms_router)
    app.include_router(status_router)


@app.on_event('startup')
def template_configuration():
    from pathlib import Path
    import fastapi_chameleon

    dev_mode = True

    BASE_DIR = Path(__file__).resolve().parent
    template_folder = str(BASE_DIR / 'templates')
    fastapi_chameleon.global_init(template_folder, auto_reload=dev_mode)


@app.on_event('startup')
def kafka_configuration():
    pass


@app.post('/event_handler')
async def event_handler():
    return {"event_reception": True}


def main():
    config()


if __name__ == '__main__':
    main()

else:
    config()
