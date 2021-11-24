import os
from starlette.exceptions import HTTPException
from twilio.request_validator import RequestValidator
from twilio.rest import Client

from starlette.requests import Request

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)


async def http_validation(request: Request):
    # Validador de Requerimientos HTTP.
    validator = RequestValidator(auth_token)

    # Formulario HTML enviado al servidor.
    form_ = await request.form()

    # Valida la existencia de auth_token en el header.
    if not validator.validate(
            str(request.url),
            form_,
            request.headers.get("X-Twilio-Signature", "")
    ):
        raise HTTPException(status_code=400, detail="Error in Twilio Signature")


def create_message():
    message = client.messages.create(body='Estimada . tu marca no vale madres.', from_='13203001523',
                                     to='+524444188968',
                                     media_url=["https://i.ytimg.com/vi/U_JbTHp6uzI/maxresdefault.jpg"])
    print(message.sid)
    print(message)
